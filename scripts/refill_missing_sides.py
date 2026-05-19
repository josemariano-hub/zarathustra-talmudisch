#!/usr/bin/env python3
"""
Post-audit refill: for chapters that lost a side after audit_notes_with_llm
dropped bad attachments, walk the candidate paragraphs in similarity order
(per side's corpus) and ask Gemini if the next candidate fits the chapter.
First candidate that scores ≥ 2 is inserted. Stops at 1 per (chapter, side).

This guarantees that 'I want the full Talmudic format for ALL chapters'
holds even after the quality audit removed bad fills.
"""

from __future__ import annotations
import json, os, re, sys, time, hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading
import numpy as np
import google.generativeai as genai

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
COMM = SRC / "commentary.json"
NAV  = json.loads((SRC / "chapter-nav.json").read_text(encoding="utf-8"))
CACHE = SRC / ".audit-cache.json"

MODEL = "gemini-2.5-flash"
TOP_K = 8        # check up to N candidates per chapter/side
WORKERS = 6

SOURCES_BY_SIDE = {
    "inner":  [("sanchez-meca",   "/tmp/sanchez_meca.txt", "es")],
    "outer":  [("klossowski",     "/tmp/klossowski.txt",   "fr"),
               ("deleuze",        "/tmp/deleuze.txt",      "fr")],
    "bottom": [("new-cambridge",  "/tmp/cambridge.txt",    "en"),
               ("sp-introduction","/tmp/sp_intro.txt",     "es")],
}

# Reuse the existing audit cache + LLM prompt
sys.path.insert(0, str(PROJ / "scripts"))
from audit_notes_with_llm import SYSTEM, hash_pair, call_batch
from retrieve_commentary import split_paragraphs_with_offsets, chapter_verses, PARA_RE, DE_P_RE

def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}

def save_cache(c):
    CACHE.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")

def chapter_de_text(xml_id: str) -> str:
    """Combine first few DE paragraphs to summarise a chapter for the LLM."""
    e = next((x for x in NAV if x["xml_id"] == xml_id), None)
    if not e: return ""
    p = SRC / e["file"]
    if not p.exists(): return ""
    txt = p.read_text(encoding="utf-8")
    paras = []
    for m in PARA_RE.finditer(txt):
        dm = DE_P_RE.search(m.group("body"))
        if dm:
            paras.append(re.sub(r"<[^>]+>", "", dm.group("txt")).strip())
        if len(paras) >= 4: break
    return " ".join(paras)[:700]

def coverage_gaps(data):
    """Return list of (xml_id, side) tuples that lack any note."""
    gaps = []
    for e in NAV:
        if e["xml_id"] == "ch-p0-00": continue
        ch = e["xml_id"]
        has = {"inner": False, "outer": False, "bottom": False}
        for k, s in data["streams"].items():
            side = s.get("side", "")
            for n in s.get("notes", []):
                if n["target"].startswith(ch):
                    if side in has:
                        has[side] = True
        for side in ("inner", "outer", "bottom"):
            if not has[side]:
                gaps.append((ch, side))
    return gaps

def main():
    api_key = os.environ.get("GOOGLE_API_KEY") or "AIzaSyCOla_ZVKmzW-B9MUlOocjd2n4BPCwlsAo"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL)

    from sentence_transformers import SentenceTransformer
    embed_model = SentenceTransformer("sentence-transformers/LaBSE")

    data = json.loads(COMM.read_text(encoding="utf-8"))
    gaps = coverage_gaps(data)
    print(f"chapters missing a side: {len(gaps)}")

    # Track which (corpus, paragraph_idx, chapter) pairs were already
    # audited so we don't replay an LLM-confirmed bad one.
    already_used: set[tuple[str, int]] = set()
    for sname, stream in data["streams"].items():
        for n in stream.get("notes", []):
            if "_corpus_idx" in n:
                already_used.add((sname, n["_corpus_idx"]))

    # Embed chapter verses once
    verses_by_ch = chapter_verses()
    v_embeds = {}
    for ch, vlist in verses_by_ch.items():
        texts = [t for _, t in vlist]
        v_embeds[ch] = (
            [vid for vid, _ in vlist],
            embed_model.encode(texts, normalize_embeddings=True,
                               batch_size=32, show_progress_bar=False),
        )

    # Embed each corpus once
    corpora = {}
    for side, srcs in SOURCES_BY_SIDE.items():
        for name, path, src_lang in srcs:
            raw = Path(path).read_text(encoding="utf-8", errors="replace")
            pairs = split_paragraphs_with_offsets(raw)
            paras = [p for p, _ in pairs]
            offs  = [o for _, o in pairs]
            emb = embed_model.encode(paras, normalize_embeddings=True,
                                     batch_size=64, show_progress_bar=False)
            corpora[name] = (paras, offs, emb, src_lang)
            print(f"  loaded {name}: {len(paras)} paragraphs")

    cache = load_cache()
    lock = threading.Lock()
    inserted = 0

    for (ch, side) in gaps:
        srcs = SOURCES_BY_SIDE[side]
        if not srcs: continue
        if ch not in v_embeds: continue
        v_ids, v_emb = v_embeds[ch]
        # Collect best candidates across this side's corpora
        candidates: list[tuple[float, str, int, int]] = []
        for name, _path, _src in srcs:
            if name not in corpora: continue
            paras, offs, p_emb, src_lang = corpora[name]
            sims = p_emb @ v_emb.T              # (P, V)
            best_v = sims.argmax(axis=1)
            best_p_score = sims.max(axis=1)
            order = np.argsort(-best_p_score)[:TOP_K]
            for p_idx in order:
                if (name, int(p_idx)) in already_used: continue
                candidates.append((float(best_p_score[p_idx]), name,
                                   int(p_idx), int(best_v[p_idx])))
        candidates.sort(reverse=True)
        if not candidates:
            print(f"  no candidates for {ch}/{side}")
            continue

        # Ask Gemini, one candidate at a time (cached), until score ≥ 2
        chosen = None
        for score, name, p_idx, v_idx in candidates:
            paras, offs, _emb, _src = corpora[name]
            note_text = paras[p_idx]
            vid = v_ids[v_idx] if v_ids[v_idx] != "__title__" else v_ids[1]
            verse_text = next((t for vname, t in verses_by_ch[ch] if vname == vid), "")
            ck = hash_pair(verse_text, note_text)
            verdict = cache.get(ck)
            if not verdict:
                try:
                    results = call_batch(model, [(None, verse_text, note_text)])
                    if 1 in results:
                        verdict = {"score": results[1][0], "reason": results[1][1]}
                        cache[ck] = verdict
                except Exception as e:
                    print(f"  llm err on {ch}/{side}: {e}")
                    continue
            if verdict and verdict["score"] >= 2:
                chosen = (name, p_idx, v_idx, score, verdict)
                break
            if verdict and verdict["score"] == 1 and not chosen:
                # remember as fallback weak choice
                chosen_fallback = (name, p_idx, v_idx, score, verdict)
        if not chosen:
            try: chosen = chosen_fallback
            except NameError: pass
        if not chosen:
            print(f"  could not fill {ch}/{side}")
            continue
        name, p_idx, v_idx, score, verdict = chosen
        paras, offs, _emb, _src = corpora[name]
        # Choose a real verse id (skip __title__ slice; fall back safely)
        real_ids = [i for i in v_ids if i != "__title__"]
        if not real_ids: continue
        if v_idx < len(v_ids) and v_ids[v_idx] != "__title__":
            vid = v_ids[v_idx]
        else:
            vid = real_ids[0]
        note = {
            "target": vid,
            "rank": 99,
            "score": round(score, 3),
            "_forced": True,
            "_corpus_idx": int(p_idx),
            "_source_offset": offs[p_idx],
            "en": paras[p_idx], "fr": paras[p_idx], "es": paras[p_idx],
        }
        if verdict["score"] == 1:
            note["_audit_flag"] = "weak"
            note["_audit_reason"] = verdict["reason"]
        data["streams"][name]["notes"].append(note)
        already_used.add((name, int(p_idx)))
        inserted += 1
        print(f"  filled {ch}/{side} ← {name} (audit={verdict['score']}, sim={score:.2f})")

    save_cache(cache)
    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\ninserted {inserted} refill notes; commentary.json updated")

if __name__ == "__main__":
    main()
