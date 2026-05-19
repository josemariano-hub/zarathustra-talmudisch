#!/usr/bin/env python3
"""
Build source/alignment.json — a flat, machine-readable export of the
per-verse alignment across DE/EN/FR/ES.

Schema: a JSON array, one row per verse:
  { "id": "ch-p1-22-v07", "ch": "ch-p1-22", "title": "v07",
    "de": "...", "en": "...", "fr": "...", "es": "..." }

The Vorrede (ch_vorrede.ptx) uses bare ids "v01"…"v12"; we keep those as-is
but tag ch="vorrede" for indexing.

Used by the search overlay in talmud.js (loaded lazily on first search).
"""
from __future__ import annotations
import json, re
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
CH   = SRC / "chapters"
OUT  = SRC / "alignment.json"

PARA_RE = re.compile(r'<paragraphs xml:id="([^"]+)">(.*?)</paragraphs>', re.DOTALL)
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.DOTALL)
P_RE = re.compile(r'<p xml:id="[^"]+" xml:lang="([^"]+)"[^>]*>(.*?)</p>', re.DOTALL)

def strip_tags(s: str) -> str:
    return re.sub(r'<[^>]+>', '', s).strip()

def extract(file: Path, ch: str) -> list[dict]:
    out = []
    txt = file.read_text(encoding='utf-8')
    for m in PARA_RE.finditer(txt):
        vid, body = m.group(1), m.group(2)
        tm = TITLE_RE.search(body)
        title = tm.group(1).strip() if tm else vid
        row = {"id": vid, "ch": ch, "title": title}
        for pm in P_RE.finditer(body):
            lang = pm.group(1)
            row[lang] = strip_tags(pm.group(2))
        out.append(row)
    return out

def main():
    rows = []
    rows.extend(extract(SRC / "ch_vorrede.ptx", "vorrede"))
    for f in sorted(CH.glob("ch_p*.ptx")):
        # "ch_p1_01_*.ptx" → "ch-p1-01"
        m = re.match(r'ch_p(\d+)_(\d+)_', f.name)
        if not m: continue
        ch_id = f"ch-p{m.group(1)}-{m.group(2)}"
        rows.extend(extract(f, ch_id))
    OUT.write_text(json.dumps(rows, ensure_ascii=False), encoding='utf-8')
    print(f'alignment.json: {len(rows)} rows, {OUT.stat().st_size//1024} KB')

if __name__ == '__main__':
    main()
