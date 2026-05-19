#!/usr/bin/env python3
"""
Drop notes flagged `_audit_flag: "weak"` from a specific stream (or
streams). Used to prune corpora where the LLM audit consistently judged
the corpus a poor fit for the targets it was being assigned to — e.g.
*sanchez-meca*, which was running at 77 % weak before culling.

Usage:
    python cull_weak_in_stream.py sanchez-meca [stream2 …]

Idempotent.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

COMM = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt/source/commentary.json")

def cull(streams: list[str]):
    data = json.loads(COMM.read_text(encoding="utf-8"))
    total_dropped = 0
    for sname in streams:
        st = data["streams"].get(sname)
        if not st:
            print(f"  {sname}: stream not found")
            continue
        before = len(st.get("notes", []))
        st["notes"] = [n for n in st.get("notes", [])
                       if n.get("_audit_flag") != "weak"]
        after = len(st["notes"])
        dropped = before - after
        total_dropped += dropped
        print(f"  {sname}: {before} → {after}  ({dropped} weak dropped)")
    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"total weak dropped: {total_dropped}")

def main():
    streams = sys.argv[1:] or ["sanchez-meca"]
    cull(streams)

if __name__ == "__main__":
    main()
