#!/usr/bin/env python3
"""
RAG-style commentary retrieval — per-verse assignment edition.

For each chapter:
  • Embed EVERY DE verse separately.
  • Embed every paragraph of each commentary corpus once.
  • For each commentary paragraph, find its argmax-similarity verse in
    the chapter; the paragraph's chapter-score is that max.
  • Keep the top-K paragraphs per (chapter, corpus) above MIN_SCORE
    and target them at the verse they actually matched.
  • Apply a diversity cap: each commentary paragraph can win at most
    DIVERSITY_CAP chapters before its score is demoted by
    DIVERSITY_PENALTY per additional use. Stops one Deleuze paragraph
    from "explaining" every chapter.
  • Record (corpus, paragraph_index, char_offset) for traceability.

Pass-2 fallback unchanged: any chapter with zero matches gets the
single best paragraph across all corpora regardless of threshold.
"""

from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path
import numpy as np

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
COMM = SRC / "commentary.json"

sys.path.insert(0, str(PROJ / "scripts"))

NAV = json.loads((SRC/"chapter-nav.json").read_text(encoding="utf-8"))

# ---- Corpora -------------------------------------------------------------
SOURCES = [
    # outer = chapter-level scholarly readings (Tosafot column)
    ("klossowski",     "/tmp/klossowski.txt",   "fr",
        {"en":"Klossowski (FR)","fr":"Klossowski","es":"Klossowski (FR)"}, "#a04a55", "outer"),
    ("deleuze",        "/tmp/deleuze.txt",      "fr",
        {"en":"Deleuze (FR)","fr":"Deleuze","es":"Deleuze (FR)"}, "#c46a3a", "outer"),
    # inner = Spanish scholarly philology, sits next to SP translator notes
    ("sanchez-meca",   "/tmp/sanchez_meca.txt", "es",
        {"en":"Sánchez Meca (ES)","fr":"Sánchez Meca (ES)","es":"Sánchez Meca"}, "#3a8a8a", "inner"),
    # bottom = contextual / background / classical citations (mesoreh strata)
    ("new-cambridge",  "/tmp/cambridge.txt",    "en",
        {"en":"New Cambridge Companion","fr":"New Cambridge Companion","es":"New Cambridge Companion"}, "#3a6a3a", "bottom"),
    ("sp-introduction","/tmp/sp_intro.txt",     "es",
        {"en":"Sánchez Pascual — Introducción","fr":"Sánchez Pascual — Introducción","es":"Sánchez Pascual — Introducción"}, "#b58a3a", "bottom"),
]

# ---- Tuning knobs --------------------------------------------------------
MIN_HIGH          = 0.50   # raised from 0.46 — B4
TOP_K             = 2
DIVERSITY_CAP     = 3      # B5
DIVERSITY_PENALTY = 0.05   # B5

# ---- Junk filter ---------------------------------------------------------
def is_junk(p: str) -> bool:
    if len(p) < 80 or len(p) > 1500: return True
    word_chars = sum(1 for c in p if c.isalpha())
    if word_chars < 50: return True
    if word_chars / len(p) < 0.55: return True
    if len(re.findall(r"\bp\.\s*\d", p)) >= 3 and word_chars / len(p) < 0.7:
        return True
    if p.count(".") / len(p) > 0.08 and re.search(r"\.\s*\d", p): return True
    if re.search(r"\b[A-Z]{1,4}\s*=\s*", p) and p.count("=") > 1: return True
    if re.search(r"(?i)\bcap[íi]tulo\b.*\d.*\d", p) and word_chars / len(p) < 0.8:
        return True
    return False

def split_paragraphs_with_offsets(text: str) -> list[tuple[str, int]]:
    """Return [(clean_paragraph, char_offset_in_source), ...]."""
    out = []
    pos = 0
    # Walk the text manually so we keep offsets.
    for m in re.finditer(r"(.+?)(\n{2,}|\f|\Z)", text, re.DOTALL):
        raw, sep = m.group(1), m.group(2)
        start = m.start(1)
        p = re.sub(r"\s+", " ", raw).strip()
        p = re.sub(r"(\w)­\s+(\w)", r"\1\2", p)
        if not is_junk(p):
            out.append((p, start))
        if sep == "":
            break
    return out

# ---- Build per-verse queries --------------------------------------------
PARA_RE = re.compile(
    r'<paragraphs xml:id="(?P<vid>[^"]+)">(?P<body>.*?)</paragraphs>',
    re.DOTALL
)
DE_P_RE = re.compile(r'<p[^>]*xml:lang="de"[^>]*>(?P<txt>.*?)</p>', re.DOTALL)

def chapter_verses() -> dict[str, list[tuple[str, str]]]:
    """xml_id -> [(verse_id, de_text), ...]  + title slice at index 0 as ('__title__', text)."""
    out: dict[str, list[tuple[str, str]]] = {}
    for entry in NAV:
        if entry["xml_id"] == "ch-p0-00": continue
        path = SRC / entry["file"]
        if not path.exists(): continue
        text = path.read_text(encoding="utf-8")
        verses: list[tuple[str, str]] = []
        # Title slice (helps weak/poetic chapters)
        title_bits = " ".join(filter(None, (entry.get("de",""), entry.get("en",""), entry.get("fr",""))))
        if title_bits:
            verses.append(("__title__", f"chapter “{title_bits}”"))
        for m in PARA_RE.finditer(text):
            vid = m.group("vid")
            dm = DE_P_RE.search(m.group("body"))
            if not dm: continue
            t = re.sub(r"<[^>]+>", "", dm.group("txt")).strip()
            if len(t) >= 20:
                verses.append((vid, t[:800]))
        if len(verses) > 1:  # at least one real verse
            out[entry["xml_id"]] = verses
    return out

def main():
    print("Loading model…")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/LaBSE")

    verses_by_ch = chapter_verses()
    print(f"verses built for {len(verses_by_ch)} chapters")

    # Embed every chapter's verses (one row per verse).
    print("Embedding chapter verses…")
    verse_embeds: dict[str, np.ndarray] = {}
    verse_ids:    dict[str, list[str]]  = {}
    for xml_id, vlist in verses_by_ch.items():
        ids   = [vid for vid, _ in vlist]
        texts = [txt for _, txt in vlist]
        verse_embeds[xml_id] = model.encode(texts, normalize_embeddings=True, batch_size=32, show_progress_bar=False)
        verse_ids[xml_id]    = ids

    # Embed every paragraph in every corpus once.
    corpora: dict[str, tuple[list[str], list[int], np.ndarray]] = {}
    for name, path, src_lang, label, color, side in SOURCES:
        raw = Path(path).read_text(encoding="utf-8", errors="replace")
        pairs = split_paragraphs_with_offsets(raw)
        paras   = [p for p, _ in pairs]
        offsets = [o for _, o in pairs]
        if not paras:
            corpora[name] = ([], [], np.zeros((0, 768)))
            continue
        emb = model.encode(paras, normalize_embeddings=True, batch_size=64, show_progress_bar=False)
        corpora[name] = (paras, offsets, emb)
        print(f"[{name}] {len(paras):,} clean paragraphs embedded")

    # Track diversity: (corpus, para_idx) -> times used
    usage: dict[tuple[str, int], int] = {}
    def penalty(corpus: str, idx: int) -> float:
        used = usage.get((corpus, idx), 0)
        if used < DIVERSITY_CAP: return 0.0
        return DIVERSITY_PENALTY * (used - DIVERSITY_CAP + 1)

    streams = {n: {"label": label, "color": color, "side": side, "_origin": src_lang, "notes": []}
               for n, _p, src_lang, label, color, side in SOURCES}

    # PASS 1 — per-verse assignment, top-K per (chapter, corpus)
    print(f"\nPass 1 (MIN_SCORE={MIN_HIGH}, TOP_K={TOP_K}, DIVERSITY_CAP={DIVERSITY_CAP}):")
    coverage_by_ch: dict[str, int] = {x: 0 for x in verses_by_ch}
    for xml_id, vlist in verses_by_ch.items():
        v_emb  = verse_embeds[xml_id]            # (V, 768)
        v_ids  = verse_ids[xml_id]
        for name, _path, _src, _lbl, _col, _sd in SOURCES:
            paras, offsets, p_emb = corpora[name]
            if len(paras) == 0: continue
            # similarity matrix: paragraphs (P) × verses (V)
            sims = p_emb @ v_emb.T                # (P, V)
            best_verse_idx  = sims.argmax(axis=1)  # (P,)
            best_verse_score = sims.max(axis=1)    # (P,) raw score
            # Apply diversity penalty per paragraph
            adj = np.array([best_verse_score[i] - penalty(name, i) for i in range(len(paras))])
            # Pick top-K paragraphs by adjusted score
            order = np.argsort(-adj)
            kept = 0
            for p_idx in order:
                s_adj = float(adj[p_idx])
                s_raw = float(best_verse_score[p_idx])
                if s_adj < MIN_HIGH: break
                v_idx = int(best_verse_idx[p_idx])
                vid = v_ids[v_idx]
                if vid == "__title__":
                    # If best match is the title slice, fall back to the second-best
                    # real verse so we don't waste a slot on a non-existent target.
                    real_v = [j for j in range(v_emb.shape[0]) if v_ids[j] != "__title__"]
                    if not real_v: continue
                    v_idx = int(real_v[int(np.argmax(sims[p_idx, real_v]))])
                    vid = v_ids[v_idx]
                streams[name]["notes"].append({
                    "target":   vid,
                    "rank":     kept + 1,
                    "score":    round(s_raw, 3),
                    "_corpus_idx":  int(p_idx),
                    "_source_offset": offsets[p_idx],
                    "en": paras[p_idx], "fr": paras[p_idx], "es": paras[p_idx],
                })
                usage[(name, int(p_idx))] = usage.get((name, int(p_idx)), 0) + 1
                coverage_by_ch[xml_id] += 1
                kept += 1
                if kept >= TOP_K: break

    # ----------------------------------------------------------------
    # PASS 2 — per-side guaranteed coverage.
    # For every chapter, every margin SIDE (inner / outer / bottom)
    # must carry at least one note. If Pass 1 left a side empty for a
    # chapter, find the best paragraph among that side's corpora and
    # force-insert it. This is what makes the full Talmudic page work:
    # the bottom strata is never visually empty.
    print("\nPass 2 (per-side guaranteed coverage):")
    # Build (xml_id, side) → bool of whether Pass 1 hit it
    side_of = {name: side for name, _p, _src, _lbl, _col, side in SOURCES}
    side_hit: dict[tuple[str, str], bool] = {}
    for xml_id in verses_by_ch:
        for s in ("inner", "outer", "bottom"):
            side_hit[(xml_id, s)] = False
    for name, stream in streams.items():
        s = side_of.get(name)
        if not s: continue
        for n in stream["notes"]:
            t = n["target"]
            # Normalise the chapter id (verse ids are "ch-pX-YY-vNN")
            ch = t.rsplit("-v", 1)[0]
            if (ch, s) in side_hit:
                side_hit[(ch, s)] = True

    forced = 0
    sides_active = sorted({s for s in side_of.values()})
    for xml_id in verses_by_ch:
        v_emb = verse_embeds[xml_id]
        v_ids = verse_ids[xml_id]
        for side in sides_active:
            if side_hit[(xml_id, side)]: continue
            # Find best paragraph from any corpus on this side
            candidates = []
            for name, _path, _src, _lbl, _col, _sd in SOURCES:
                if _sd != side: continue
                paras, offsets, p_emb = corpora[name]
                if len(paras) == 0: continue
                sims = p_emb @ v_emb.T
                best_v = sims.argmax(axis=1)
                best_p_score = sims.max(axis=1)
                p_best = int(np.argmax(best_p_score))
                candidates.append((float(best_p_score[p_best]), name, p_best, int(best_v[p_best])))
            if not candidates: continue
            candidates.sort(reverse=True)
            score, name, p_idx, v_idx = candidates[0]
            paras, offsets, _emb = corpora[name]
            vid = v_ids[v_idx] if v_ids[v_idx] != "__title__" else v_ids[1]
            streams[name]["notes"].append({
                "target":   vid,
                "rank":     1,
                "score":    round(score, 3),
                "_forced":  True,
                "_corpus_idx":  int(p_idx),
                "_source_offset": offsets[p_idx],
                "en": paras[p_idx], "fr": paras[p_idx], "es": paras[p_idx],
            })
            forced += 1
            print(f"  forced {xml_id}/{side} → {name} (score={score:.3f})")
    print(f"forced {forced} fill-in excerpts to keep every side populated")

    # Final per-stream summary
    print("\n=== final stream counts ===")
    for name, stream in streams.items():
        verses_hit = len(set(n["target"] for n in stream["notes"]))
        print(f"  {name:20s} {len(stream['notes']):4d} notes, {verses_hit:4d} unique verses")

    # Merge into commentary.json
    data = json.loads(COMM.read_text(encoding="utf-8"))
    for name, stream in streams.items():
        data["streams"][name] = stream
    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("commentary.json updated")

if __name__ == "__main__":
    main()
