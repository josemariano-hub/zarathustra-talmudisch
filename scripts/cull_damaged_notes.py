#!/usr/bin/env python3
"""
Drop notes that contain unmistakable OCR damage or that begin
mid-sentence (a fragment retrieved without a leading sentence
boundary). The patterns here are deliberately narrow — they only
match strings that no clean editorial text would contain:

  • runs of 4+ space-separated single letters  ("l i n a 'immoral")
  • bare pipe followed by punctuation             ("|,taxis")
  • apostrophe-dot-letter                         ("n '.spect")
  • the OCR signature " i »"                      ("u n i »nexos")
  • the classic OCR misreadings "w n" / "m a"     (un / ma)
  • any note whose ES/EN/FR/DE field starts with "…" or "..."

Idempotent. Run after retrieve / refill steps.
"""
from __future__ import annotations
import json, re
from pathlib import Path

COMM = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt/source/commentary.json")

OCR_PATTERNS = [
    re.compile(r'\b[a-z]( [a-z]){3,}\b'),
    re.compile(r'\|[,\.]'),
    re.compile(r"\b[a-z]\s*[''\"′]\s*\.[a-z]"),
    re.compile(r' i »'),
    re.compile(r'\b[wm]\s[an]\b'),
]
FRAG_PATTERNS = [
    re.compile(r'^\s*…'),
    re.compile(r'^\s*\.\.\.'),
]

def is_damaged(note: dict) -> tuple[bool, list[str]]:
    reasons = []
    for L in ('es', 'en', 'fr', 'de'):
        t = note.get(L) or ''
        if not t: continue
        for p in OCR_PATTERNS:
            if p.search(t):
                reasons.append(f"OCR/{L}")
                break
        for p in FRAG_PATTERNS:
            if p.search(t):
                reasons.append(f"fragment/{L}")
                break
    return (len(reasons) > 0, reasons)

def main():
    d = json.loads(COMM.read_text(encoding="utf-8"))
    total_before = 0
    total_dropped = 0
    for sname, st in d["streams"].items():
        if sname.startswith("_"): continue
        notes = st.get("notes", [])
        total_before += len(notes)
        keep = []
        dropped = []
        for n in notes:
            bad, reasons = is_damaged(n)
            if bad:
                dropped.append((n.get("target"), reasons))
            else:
                keep.append(n)
        if dropped:
            print(f"{sname}: dropping {len(dropped)}/{len(notes)}")
            for tgt, reasons in dropped:
                print(f"   - {tgt}  {reasons}")
        st["notes"] = keep
        total_dropped += len(dropped)
    print(f"\ntotal: {total_before} → {total_before - total_dropped}  "
          f"({total_dropped} dropped)")
    COMM.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
