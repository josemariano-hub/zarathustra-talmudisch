#!/usr/bin/env python3
"""
Drop every note whose audit_score is 0 according to source/audit.json.
The audit said these notes don't fit their target verse; they should not
be served to the reader. Idempotent.
"""
from __future__ import annotations
import json
from pathlib import Path

COMM  = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt/source/commentary.json")
AUDIT = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt/source/audit.json")

def main():
    data  = json.loads(COMM.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))

    # Set of (stream, target) pairs with score=0
    bad = {(a["stream"], a["target"]) for a in audit if a.get("score") == 0}
    print(f"audit rows with score=0: {len(bad)}")

    dropped = 0
    for sname, stream in data["streams"].items():
        if sname.startswith("_"): continue
        before = len(stream.get("notes", []))
        stream["notes"] = [
            n for n in stream.get("notes", [])
            if (sname, n.get("target")) not in bad
        ]
        after = len(stream["notes"])
        if before != after:
            print(f"  {sname}: {before} → {after}  ({before - after} dropped)")
            dropped += before - after
    print(f"\ntotal notes dropped: {dropped}")
    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"commentary.json: {sum(len(s.get('notes',[])) for s in data['streams'].values())} notes remain")

if __name__ == "__main__":
    main()
