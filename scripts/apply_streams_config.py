#!/usr/bin/env python3
"""
Single source of truth enforcement: read source/streams.config.json
and re-apply side/color/label/_origin/bibliographic onto
source/commentary.json. Any other script that mutates commentary.json
must be followed by this one so the stream metadata never drifts.

Idempotent. No notes are touched.
"""
from __future__ import annotations
import json
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
CFG  = SRC / "streams.config.json"
COMM = SRC / "commentary.json"

KEYS = ("side", "color", "label", "_origin", "bibliographic")

def main():
    cfg = json.loads(CFG.read_text(encoding="utf-8"))["streams"]
    data = json.loads(COMM.read_text(encoding="utf-8"))

    n_streams = 0
    n_field_writes = 0
    n_created = 0
    n_orphan = []

    for sname, meta in cfg.items():
        if sname not in data["streams"]:
            data["streams"][sname] = {"notes": []}
            n_created += 1
        st = data["streams"][sname]
        for k in KEYS:
            v = meta.get(k)
            if v is None and k == "_origin":
                # keep None explicitly
                if st.get(k) != None:
                    st[k] = None
                    n_field_writes += 1
                else:
                    st.setdefault(k, None)
                continue
            if v is None:
                continue
            if st.get(k) != v:
                st[k] = v
                n_field_writes += 1
        n_streams += 1

    # report streams in commentary but missing from config
    for sname in data["streams"]:
        if sname.startswith("_"): continue
        if sname not in cfg:
            n_orphan.append(sname)

    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"apply_streams_config: {n_streams} streams synced, {n_field_writes} fields written, {n_created} created")
    if n_orphan:
        print(f"  WARNING: streams in commentary.json but not in streams.config.json: {n_orphan}")

if __name__ == "__main__":
    main()
