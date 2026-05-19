#!/usr/bin/env python3
"""
Graph-based, multi-language re-assignment of every note to the verse
that best fits it across ALL FOUR language views (DE / EN / FR / ES).

The RAG retrieval scored only DE-verse ↔ note-in-native-language. LaBSE
projects into a shared space, but you still get noise from any one
language pair. This script combines four signals:

  score(note, verse) = mean of available cross-language similarities
    sim( note[L_note], verse[L_verse] )  for L_note, L_verse ∈ {de,en,fr,es}
    diagonals weighted heavier (same-language pair).

Reassignment rule:
  • compute score against every verse in the note's chapter
  • if the best verse beats the current target by ≥ MARGIN, move it
  • otherwise keep it (the original retrieval was already argmax of
    one signal — we only move when multiple signals agree)

Idempotent. Cached embeddings.
"""

from __future__ import annotations
import json, re
from pathlib import Path
import numpy as np

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
COMM = SRC / "commentary.json"
NAV  = json.loads((SRC / "chapter-nav.json").read_text(encoding="utf-8"))

LANGS = ("de", "en", "fr", "es")
MARGIN = 0.04  # move only when the new verse beats current by this much
DIAG_BONUS = 1.5  # same-language pair counts more

def chapter_verse_texts() -> dict[str, dict[str, dict[str, str]]]:
    """xml_id → vid → {lang: text}"""
    out: dict[str, dict[str, dict[str, str]]] = {}
    for e in NAV:
        if e["xml_id"] == "ch-p0-00": continue
        p = SRC / e["file"]
        if not p.exists(): continue
        vs: dict[str, dict[str, str]] = {}
        txt = p.read_text(encoding="utf-8")
        for m in re.finditer(r'<paragraphs xml:id="([^"]+)">(.*?)</paragraphs>', txt, re.DOTALL):
            vid, body = m.group(1), m.group(2)
            langs = {}
            for L in LANGS:
                pm = re.search(rf'xml:lang="{L}"[^>]*>(.*?)</p>', body, re.DOTALL)
                if pm:
                    langs[L] = re.sub(r"<[^>]+>", "", pm.group(1)).strip()
            vs[vid] = langs
        out[e["xml_id"]] = vs
    return out

def main():
    print("Loading model…")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/LaBSE")

    data = json.loads(COMM.read_text(encoding="utf-8"))
    ch_verses = chapter_verse_texts()

    # Pre-embed every chapter's verses across all four languages.
    print("Embedding verses across DE/EN/FR/ES…")
    embeds: dict[str, dict[str, np.ndarray]] = {}  # ch -> {lang: (V, 768)} ; verse ids consistent across langs
    verse_ids:  dict[str, list[str]] = {}
    for ch, vs in ch_verses.items():
        vids = list(vs.keys())
        verse_ids[ch] = vids
        by_lang = {L: [] for L in LANGS}
        for vid in vids:
            for L in LANGS:
                by_lang[L].append(vs[vid].get(L, ""))
        embeds[ch] = {}
        for L in LANGS:
            texts = by_lang[L]
            if not any(texts):
                continue
            # Replace empties with a single space to keep array shapes
            cleaned = [t if t else " " for t in texts]
            embeds[ch][L] = model.encode(cleaned, normalize_embeddings=True,
                                         batch_size=64, show_progress_bar=False)

    # For each note: embed each language version once, then score against
    # all (lang, verse) entries in the note's chapter.
    moved = 0; checked = 0
    for sname, stream in data["streams"].items():
        if sname.startswith("_"): continue
        for n in stream["notes"]:
            target = n.get("target", "")
            if not target.startswith("ch-"):
                continue
            ch = target.rsplit("-v", 1)[0]
            if ch not in embeds: continue
            ch_emb = embeds[ch]
            vids = verse_ids[ch]
            if target not in vids: continue
            # Note texts per language
            n_lang_text = {L: (n.get(L) or "").strip() for L in ("en", "fr", "es")}
            n_lang_text = {L: t for L, t in n_lang_text.items() if t}
            if not n_lang_text: continue
            note_embs = {}
            for L, t in n_lang_text.items():
                note_embs[L] = model.encode([t[:600]], normalize_embeddings=True,
                                            show_progress_bar=False)[0]
            # Combined score per verse
            n_verses = len(vids)
            combined = np.zeros(n_verses)
            count = np.zeros(n_verses)
            for nL, nE in note_embs.items():
                for vL, vE in ch_emb.items():
                    sim = vE @ nE   # (V,)
                    w = DIAG_BONUS if (nL == vL) else 1.0
                    combined += w * sim
                    count    += w
            combined = combined / np.maximum(count, 1)
            cur_idx = vids.index(target)
            cur_score = float(combined[cur_idx])
            best_idx = int(np.argmax(combined))
            best_score = float(combined[best_idx])
            checked += 1
            if best_idx != cur_idx and best_score > cur_score + MARGIN:
                n["_multilang_moved_from"] = target
                n["_multilang_cur_score"] = round(cur_score, 3)
                n["_multilang_new_score"] = round(best_score, 3)
                n["target"] = vids[best_idx]
                moved += 1

    print(f"\nchecked {checked} notes; moved {moved} based on multi-language consensus")
    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("commentary.json updated")

if __name__ == "__main__":
    main()
