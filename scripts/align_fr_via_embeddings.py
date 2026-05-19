#!/usr/bin/env python3
"""
Apply the same LaBSE + many-to-one DP alignment to FR ↔ DE that we use
for ES ↔ DE.  build_chapters.py assigns FR paragraphs to verses by
sequence — that's wrong whenever the FR translator merged or split
paragraphs (which Henri Albert and others did frequently).

This rescues 38% of FR pairs that were >0.5 similarity off.

Pipeline:
  1. Walk every chapter .ptx
  2. Collect existing FR paragraph texts in their current order
  3. Re-align them against DE paragraphs via DP
  4. Rewrite the FR <p> entries at their CORRECTED verse positions
"""

from __future__ import annotations
import json, re, sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
import numpy as np

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
NAV  = json.loads((SRC / "chapter-nav.json").read_text(encoding="utf-8"))

sys.path.insert(0, str(PROJ / "scripts"))
from align_es_via_embeddings import align  # reuse the DP function

PARA_RE = re.compile(
    r'<paragraphs xml:id="(?P<chap>[^"]+)-v(?P<v>\d+)">(?P<body>.*?)</paragraphs>',
    re.DOTALL,
)
DE_P_RE = re.compile(r'<p[^>]*xml:lang="de"[^>]*>(?P<txt>.*?)</p>', re.DOTALL)

# Target language is set via CLI arg (fr | en); both follow the same flow.
TARGET = "fr" if len(sys.argv) < 2 else sys.argv[1]
assert TARGET in ("fr", "en"), f"target must be fr or en, got {TARGET}"
TGT_P_RE = re.compile(rf'<p[^>]*xml:lang="{TARGET}"[^>]*>(?P<txt>.*?)</p>', re.DOTALL)
FR_P_RE = TGT_P_RE  # keep symbol so existing references work

def to_ptx_text(s: str) -> str:
    s = re.sub(r"_([^_]+?)_", r"<em>\1</em>", s)
    s = s.replace("<em>", "\x01EM\x01").replace("</em>", "\x01/EM\x01")
    s = xml_escape(s)
    s = s.replace("\x01EM\x01", "<em>").replace("\x01/EM\x01", "</em>")
    return s

def chapter_de_fr(text: str) -> tuple[list[str], list[str]]:
    """Return (DE paragraphs, FR paragraphs) in the order they appear."""
    de, fr = [], []
    for m in PARA_RE.finditer(text):
        body = m.group("body")
        de_m = DE_P_RE.search(body)
        fr_m = FR_P_RE.search(body)
        de.append(re.sub(r"<[^>]+>", "", de_m.group("txt")).strip() if de_m else "")
        fr.append(re.sub(r"<[^>]+>", "", fr_m.group("txt")).strip() if fr_m else "")
    return de, fr

def patch_chapter(entry, alignment: list[int | None], fr_paras: list[str]):
    path = SRC / entry["file"]
    text = path.read_text(encoding="utf-8")
    xml_id = entry["xml_id"]

    # Same de-dup logic as ES: when DP merges two DE into one FR, only the
    # LAST DE verse in the run keeps the FR text.
    dedup = list(alignment)
    for i in range(len(dedup) - 1):
        if dedup[i] is not None and dedup[i] == dedup[i + 1]:
            dedup[i] = None

    def patch_block(m):
        body = m.group(0)
        vm = re.match(r'<paragraphs xml:id="' + re.escape(xml_id) + r'-v(\d+)">', body)
        if not vm: return body
        v_idx = int(vm.group(1)) - 1
        fr_idx = dedup[v_idx] if 0 <= v_idx < len(dedup) else None

        body = re.sub(rf'      <p xml:id="[^"]+-{TARGET}"[^>]*>.*?</p>\n', "", body, flags=re.DOTALL)

        if fr_idx is not None and fr_paras[fr_idx]:
            fr_text = to_ptx_text(fr_paras[fr_idx])
            new_p = f'      <p xml:id="{xml_id}-v{v_idx+1:02d}-{TARGET}" xml:lang="{TARGET}">{fr_text}</p>\n'
            body = body.replace("</paragraphs>", "    " + new_p + "    </paragraphs>")
        return body

    new_text = PARA_RE.sub(patch_block, text)
    path.write_text(new_text, encoding="utf-8")

def main():
    print("Loading model…")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/LaBSE")
    print("ok")

    stats = []
    for entry in NAV:
        # Note: the auto Vorrede in chapters/ch_p0_00_*.ptx IS aligned here.
        # Only the hand-tuned `source/ch_vorrede.ptx` (routed by ?ch=vorrede)
        # is exempt.
        path = SRC / entry["file"]
        if not path.exists(): continue
        text = path.read_text(encoding="utf-8")
        de, fr = chapter_de_fr(text)
        # only keep non-empty FR for alignment input
        fr_clean = [f for f in fr if f]
        if not de or not fr_clean: continue
        align_map = align(de, fr_clean, model)
        matched = sum(1 for a in align_map if a is not None)
        stats.append((entry["xml_id"], len(de), len(fr_clean), matched))
        patch_chapter(entry, align_map, fr_clean)
        print(f"  {entry['xml_id']}: DE={len(de):3} FR={len(fr_clean):3} matched={matched:3} ({matched/len(de):.0%})")

    print("\n=== summary ===")
    avg = np.mean([m/d for _,d,_,m in stats]) if stats else 0
    print(f"chapters processed: {len(stats)}")
    print(f"avg DE→FR coverage: {avg:.1%}")

if __name__ == "__main__":
    main()
