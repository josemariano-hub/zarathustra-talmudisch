#!/usr/bin/env python3
"""
Targeted cleanup based on the verse-audit-editor.md findings:
  • strip Unicode soft-hyphen (U+00AD) from chapter ES bodies
  • strip stranded page-number tokens at the end of ES strings
    (e.g. "…todo fue!"248  → "…todo fue!")
  • strip chapter-title injection at start of v01 ES (the OCR'd PDF
    pasted the chapter title onto the first paragraph)
  • re-sync `_audit_flag` field of every note to match source/audit.json
    so weak-flagged notes are consistent
  • patch known OCR errors in the Klossowski FR text inside
    commentary.json (Vannée→l'année, w n→un, footnote-167 anchor, etc.)
"""
from __future__ import annotations
import json, re
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
COMM = SRC / "commentary.json"
AUDIT = SRC / "audit.json"

# ---- chapter ES cleanup -----------------------------------------------------
def clean_chapter_es():
    nav = json.loads((SRC / "chapter-nav.json").read_text(encoding="utf-8"))
    n_soft = n_page = n_title = 0
    for e in nav:
        if e["xml_id"] == "ch-p0-00":
            path = SRC / "ch_vorrede.ptx"
        else:
            path = SRC / e["file"]
        if not path.exists(): continue
        txt = path.read_text(encoding="utf-8")
        orig = txt
        # 1. Soft hyphens inside <p xml:lang="es"> bodies
        def kill_softhyphen(m):
            nonlocal n_soft
            body = m.group(1)
            new_body = body.replace("­", "")
            if new_body != body: n_soft += 1
            return f'<p xml:lang="es"{m.group(2)}>{new_body}</p>'
        txt = re.sub(
            r'<p xml:lang="es"([^>]*)>(.*?)</p>',
            lambda m: f'<p xml:lang="es"{m.group(1)}>{m.group(2).replace(chr(0xad), "")}</p>',
            txt, flags=re.DOTALL,
        )
        # 2. Stranded trailing digits like  text!"248  →  text!"
        def strip_trail(m):
            nonlocal n_page
            inner = m.group(2)
            new = re.sub(r'([»"\'\.\?!\)\]…])\d{1,4}\s*$', r'\1', inner.rstrip())
            if new != inner:
                n_page += 1
            return f'<p xml:lang="es"{m.group(1)}>{new}</p>'
        txt = re.sub(r'<p xml:lang="es"([^>]*)>(.*?)</p>', strip_trail, txt, flags=re.DOTALL)
        # 3. Chapter-title injection at start of v01 ES
        es_title = e.get("es", "")
        if es_title:
            esc = re.escape(es_title)
            def kill_title_v01(m):
                nonlocal n_title
                inner = m.group(1)
                # The injection looks like:
                #   "De las alegrias y de las pasiones H ermano mío..."
                # i.e. the chapter title's letters, optionally with extra spaces
                # / OCR mangling, followed by a single capital letter and a space.
                # We try a fuzzy strip: remove leading occurrence of the title up
                # to a position where a single capital + space precedes lowercase.
                # Build a fuzzy regex tolerant of split single letters.
                title_pat = "\\s*".join(re.escape(ch) for ch in es_title if ch.isalpha())
                trimmed = re.sub(
                    rf'^\s*{title_pat}\s+([A-ZÁÉÍÓÚÑ])\s+([a-záéíóúñü])',
                    lambda mm: mm.group(1) + mm.group(2), inner,
                    flags=re.IGNORECASE,
                )
                if trimmed != inner: n_title += 1
                return f'<p xml:id="{m.group(0).split("xml:id=")[1].split(chr(34))[1]}" xml:lang="es">{trimmed}</p>' if False else None
            # do via simpler approach — only first v01 ES block per chapter
            block_re = re.compile(
                rf'(<paragraphs xml:id="{re.escape(e["xml_id"])}-v01">.*?<p xml:id="[^"]+-es"[^>]*>)(.*?)(</p>)',
                re.DOTALL,
            )
            def fixer(m):
                nonlocal n_title
                inner = m.group(2)
                title_pat = "\\s*".join(re.escape(ch) for ch in es_title if ch.isalpha())
                new_inner = re.sub(
                    rf'^\s*{title_pat}\s+([A-ZÁÉÍÓÚÑ])\s+([a-záéíóúñü])',
                    lambda mm: mm.group(1) + mm.group(2), inner,
                    count=1, flags=re.IGNORECASE,
                )
                if new_inner != inner: n_title += 1
                return m.group(1) + new_inner + m.group(3)
            txt = block_re.sub(fixer, txt)
        if txt != orig:
            path.write_text(txt, encoding="utf-8")
    print(f"chapter ES: {n_soft} soft-hyphens stripped, {n_page} trailing-page-#s stripped, {n_title} v01 chapter-title injections removed")

# ---- _audit_flag sync -------------------------------------------------------
def sync_audit_flags():
    data = json.loads(COMM.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    by_key = {(a["stream"], a["target"]): a for a in audit}
    n_set = n_unset = 0
    for sname, stream in data["streams"].items():
        if sname.startswith("_"): continue
        for n in stream.get("notes", []):
            key = (sname, n.get("target"))
            row = by_key.get(key)
            if not row:
                # No audit entry — leave it alone (already flagged or unflagged)
                continue
            sc = row.get("score")
            if sc == 1:
                if n.get("_audit_flag") != "weak":
                    n["_audit_flag"] = "weak"
                    n["_audit_reason"] = row.get("reason", "")
                    n_set += 1
            else:
                if "_audit_flag" in n:
                    n.pop("_audit_flag", None)
                    n.pop("_audit_reason", None)
                    n_unset += 1
    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"audit_flag: set={n_set}, cleared={n_unset}")

# ---- Klossowski FR OCR patches ---------------------------------------------
FR_OCR_FIXES = [
    (re.compile(r"\bVannée\b"),        "l'année"),
    (re.compile(r"\bVidée\b"),         "l'idée"),
    (re.compile(r"\bVart\b"),          "l'art"),
    (re.compile(r"\bVesprit\b"),       "l'esprit"),
    (re.compile(r"\bVoubli\b"),        "l'oubli"),
    (re.compile(r"\bw n\b"),           "un"),
    (re.compile(r"\bm a\b"),           "ma"),
    (re.compile(r"\ben tan t qu(['e])"), r"en tant qu\1"),
    (re.compile(r"\b1' « esprit »"),    "l'« esprit »"),
    (re.compile(r"\bN'avait-il pas sul-\s*sistê\b"), "N'avait-il pas subsisté"),
    (re.compile(r"\bsul-\s*sistê\b"),  "subsisté"),
    (re.compile(r"167\s*$"),           ""),  # stranded footnote anchor
]

def fix_klossowski_fr():
    data = json.loads(COMM.read_text(encoding="utf-8"))
    notes = data["streams"].get("klossowski", {}).get("notes", [])
    n_fixed = 0
    for n in notes:
        for L in ("fr", "en", "es"):
            t = n.get(L)
            if not t: continue
            new = t
            for pat, repl in FR_OCR_FIXES:
                new = pat.sub(repl, new)
            if new != t:
                n[L] = new
                n_fixed += 1
    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Klossowski OCR: {n_fixed} fields patched")

def main():
    clean_chapter_es()
    sync_audit_flags()
    fix_klossowski_fr()

if __name__ == "__main__":
    main()
