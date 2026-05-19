#!/usr/bin/env python3
"""
Golden snapshot for the build pipeline.

Hashes every generated artifact and compares to source/.snapshot.json.
Fails loudly when something silently changed; pass --accept to update
the snapshot after an intentional change.

Usage:
  python scripts/snapshot.py            # verify
  python scripts/snapshot.py --accept   # rewrite golden hashes
"""

from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
SNAP = SRC / ".snapshot.json"

# Files / globs to track
TRACKED: list[Path] = []
TRACKED.append(SRC / "commentary.json")
TRACKED.append(SRC / "chapter-nav.json")
TRACKED.append(SRC / "ch_vorrede.ptx")
TRACKED.extend(sorted((SRC / "chapters").glob("ch_*.ptx")))

def hashes() -> dict[str, str]:
    out: dict[str, str] = {}
    for p in TRACKED:
        if not p.exists():
            out[str(p.relative_to(PROJ))] = "MISSING"
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        out[str(p.relative_to(PROJ))] = h
    return out

def main():
    accept = "--accept" in sys.argv
    current = hashes()

    if accept or not SNAP.exists():
        SNAP.write_text(json.dumps(current, indent=2), encoding="utf-8")
        print(f"snapshot {'updated' if SNAP.exists() else 'created'}: {len(current)} files")
        return

    golden = json.loads(SNAP.read_text(encoding="utf-8"))
    drift = []
    for k, v in current.items():
        if k not in golden:
            drift.append(f"  NEW   {k}")
        elif golden[k] != v:
            drift.append(f"  DIFF  {k}")
    for k in golden:
        if k not in current:
            drift.append(f"  GONE  {k}")

    if drift:
        print("snapshot drift detected:")
        for d in drift: print(d)
        print("\nIf intentional, re-run with --accept to update.")
        sys.exit(1)
    print(f"OK — {len(current)} files match golden snapshot")

if __name__ == "__main__":
    main()
