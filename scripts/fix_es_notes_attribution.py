#!/usr/bin/env python3
"""
Semantic re-attachment of Sánchez Pascual's translator notes.

parse_es_notes.py determines (chapter, verse) for each footnote marker
by counting paragraph indents — fragile across page breaks and footnote
clusters. Result: ~117 notes land on verses whose content has near-zero
similarity to the note.

This script post-processes commentary.json:
  • for each sanchez-pascual-notes entry, embed its body and every DE
    verse in its chapter;
  • if the current target's cosine similarity is < CUR_FLOOR AND another
    verse in the same chapter scores better by at least MARGIN, reassign
    to that better verse;
  • respect the existing target if the note's content genuinely
    aligns with it (don't over-move good attachments).

Idempotent: re-running on a corrected file is a no-op.
"""

from __future__ import annotations
import json, re
from pathlib import Path
import numpy as np

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
COMM = SRC / "commentary.json"
NAV  = json.loads((SRC / "chapter-nav.json").read_text(encoding="utf-8"))

CUR_FLOOR = 0.40    # if current target sim is below this AND
MARGIN    = 0.08    # another verse beats it by this much, we reassign.

def chapter_verse_de() -> dict[str, dict[str, str]]:
    out = {}
    for e in NAV:
        if e["xml_id"] == "ch-p0-00": continue
        p = SRC / e["file"]
        if not p.exists(): continue
        txt = p.read_text(encoding="utf-8")
        vs = {}
        for m in re.finditer(r'<paragraphs xml:id="([^"]+)">(.*?)</paragraphs>', txt, re.DOTALL):
            vid, body = m.group(1), m.group(2)
            de = re.search(r'xml:lang="de"[^>]*>(.*?)</p>', body, re.DOTALL)
            if de:
                vs[vid] = re.sub(r"<[^>]+>", "", de.group(1)).strip()
        out[e["xml_id"]] = vs
    return out

def main():
    print("Loading model…")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/LaBSE")

    data = json.loads(COMM.read_text(encoding="utf-8"))
    verses_by_ch = chapter_verse_de()

    stream = data["streams"]["sanchez-pascual-notes"]
    notes = stream["notes"]

    # Pre-embed every chapter's verses once
    print("Embedding chapter verses…")
    ch_emb: dict[str, tuple[list[str], np.ndarray]] = {}
    for ch, verses in verses_by_ch.items():
        vids = list(verses.keys())
        texts = list(verses.values())
        emb = model.encode(texts, normalize_embeddings=True, batch_size=64, show_progress_bar=False)
        ch_emb[ch] = (vids, emb)

    reassigned = 0
    moves: list[tuple[str, str, float, float]] = []
    for n in notes:
        target = n.get("target", "")
        if not target.startswith("ch-"):  # skip vorrede / malformed
            continue
        ch = target.rsplit("-v", 1)[0]
        if ch not in ch_emb: continue
        vids, embs = ch_emb[ch]
        if target not in vids: continue
        # Use ES (origin) text for similarity vs DE verses
        text = n.get("es") or n.get("en") or n.get("fr") or ""
        if not text: continue
        note_emb = model.encode([text[:400]], normalize_embeddings=True,
                                show_progress_bar=False)[0]
        sims = embs @ note_emb
        cur_idx = vids.index(target)
        cur_sim = float(sims[cur_idx])
        best_idx = int(np.argmax(sims))
        best_sim = float(sims[best_idx])
        if cur_sim < CUR_FLOOR and best_sim > cur_sim + MARGIN and best_idx != cur_idx:
            n["target"] = vids[best_idx]
            n["_reassigned_from"] = target
            n["_reassign_cur_sim"] = round(cur_sim, 3)
            n["_reassign_new_sim"] = round(best_sim, 3)
            moves.append((target, vids[best_idx], cur_sim, best_sim))
            reassigned += 1

    print(f"\nreassigned {reassigned}/{len(notes)} notes")
    for src, dst, c, b in moves[:20]:
        print(f"  {src} → {dst}  ({c:.2f} → {b:.2f})")

    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("commentary.json updated")

if __name__ == "__main__":
    main()
