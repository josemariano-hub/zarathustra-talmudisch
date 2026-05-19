#!/usr/bin/env python3
"""
Scrub OCR residue from Spanish chapter paragraphs and commentary note
bodies. Conservative: every substitution is narrow, with known cause and
known fix. Idempotent.

Targets identified in the chapter-by-chapter audit:

  PTX (ES paragraphs):
    �         replacement-char mojibake — fix on a per-token basis
                   (audit listed exact strings)
    ­         soft-hyphen residue — strip
    ',,'           OCR'd opening „ misread as two commas — replace with „
    '< <' / '>>'   stray angle brackets — replace with « / »
    'word ,'       space-before-punctuation (selective)
    digit-runs glued to a word (e.g. 'hijos260') — strip trailing digits

  commentary.json (any stream, any language):
    'L O U A. SA LO M É' → 'Lou Andreas-Salomé'
    'm a r g i n a l e' → 'marginale'   (and other spaced-letter words)
    Generic: collapse N≥4-letter spaced runs into single tokens
"""
from __future__ import annotations
import json, re
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
CH   = SRC / "chapters"
COMM = SRC / "commentary.json"

# ---- ES PTX scrubs ---------------------------------------------------------

# Named replacements (audit's high-value list)
NAMED_PTX = [
    # ch-p3-13-v28-es: '�quí → «aquí»; '�llá → «allá»
    (re.compile(r"'�quí\""),    "«aquí»"),
    (re.compile(r"'�llá\""),    "«allá»"),
    # ch-p3-10-v47-es: mujer�s → mujeres
    (re.compile(r"mujer�s"),    "mujeres"),
    # ch-p4-19-v09-es: ¡ �­ nid! → ¡Venid!
    (re.compile(r"¡\s*�­?\s*nid"), "¡Venid"),
    # generic mojibake left after the named ones: drop the lone codepoint
    (re.compile(r"�"),          ""),
]

ES_P_RE = re.compile(r'(<p xml:id="[^"]+-es"[^>]*>)(.*?)(</p>)', re.DOTALL)

def scrub_es_body(body: str) -> tuple[str, dict]:
    counts = {"FFFD":0, "softhy":0, "dblcomma":0, "trailingdigits":0,
              "spacepunct":0}
    new = body
    # 1. named FFFD repairs
    for pat, repl in NAMED_PTX:
        before = new
        new = pat.sub(repl, new)
        if new != before: counts["FFFD"] += 1
    # 2. strip soft hyphens
    n_soft = new.count("­")
    if n_soft:
        new = new.replace("­", "")
        counts["softhy"] += n_soft
    # 3. ',,' before an opening quote/space  → „
    new2 = re.sub(r',,\s*"', '«', new)
    new2 = re.sub(r',,\s*(?=[A-ZÉÍÓÚÑa-záéíóúñ])', '«', new2)
    if new2 != new: counts["dblcomma"] += 1
    new = new2
    # 4. trailing digits glued to a word ("hijos260") — only if 2+ digits and
    #    the surrounding word is at least 3 letters
    def strip_trail(m):
        counts["trailingdigits"] += 1
        return m.group(1)
    new = re.sub(r'\b([A-Za-záéíóúñ]{3,})\d{2,4}\b', strip_trail, new)
    # 5. space before comma/period inside es text
    new2 = re.sub(r' +([,;\.\!\?])', r'\1', new)
    if new2 != new: counts["spacepunct"] += 1
    new = new2
    return new, counts

def scrub_ptx(p: Path) -> dict:
    txt = p.read_text(encoding='utf-8')
    totals = {}
    def repl(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        # work on text nodes only (preserve <em>)
        parts = re.split(r'(<[^>]+>)', body)
        for i, part in enumerate(parts):
            if part.startswith('<'): continue
            new, c = scrub_es_body(part)
            parts[i] = new
            for k, v in c.items():
                totals[k] = totals.get(k, 0) + v
        return head + ''.join(parts) + tail
    new_txt = ES_P_RE.sub(repl, txt)
    if new_txt != txt:
        p.write_text(new_txt, encoding='utf-8')
    return totals


# ---- commentary spaced-letter fixes ---------------------------------------

NAMED_NOTES = [
    (re.compile(r'\bL\s*O\s*U\s+A\.\s*SA\s*LO\s*M\s*É\b'), 'Lou Andreas-Salomé'),
    (re.compile(r'\bLOU\s+A\.\s*SALOM[ÉE]\b'),             'Lou Andreas-Salomé'),
    (re.compile(r'\bm\s+a\s+r\s+g\s+i\s+n\s+a\s+l\s+e\b'), 'marginale'),
    (re.compile(r'\bp\s+l\s+a\s+n\s+t\s+e\s+s\b'),         'plantes'),
    (re.compile(r'\bs\s+o\s+y\s+d\s+e\s+l\s+t\s+i\s+p\s+o\b'), 'soy del tipo'),
    (re.compile(r'\bs\s+u\s+i\s+s\s+d\s+u\s+g\s+e\s+n\s+r\s+e\b'), 'suis du genre'),
]

# Detect a generic spaced-letter run of length ≥ 4 and try collapsing it.
# Only collapse runs that, once joined, form a token of plausible length
# (3-20 chars). Otherwise leave alone.
SPACED_RE = re.compile(r'\b([a-záéíóúñü])((?:\s[a-záéíóúñü]){3,})\b', re.IGNORECASE)

def collapse_spaced(text: str) -> tuple[str, int]:
    n = 0
    for pat, repl in NAMED_NOTES:
        before = text
        text = pat.sub(repl, text)
        if text != before: n += 1
    def repl_generic(m):
        nonlocal n
        joined = (m.group(1) + m.group(2)).replace(' ', '')
        if 3 <= len(joined) <= 20:
            n += 1
            return joined
        return m.group(0)
    text = SPACED_RE.sub(repl_generic, text)
    return text, n


def scrub_commentary() -> dict:
    d = json.loads(COMM.read_text(encoding='utf-8'))
    totals = {"named":0, "spaced":0, "softhy":0}
    for sname, st in d['streams'].items():
        if sname.startswith('_'): continue
        for n in st.get('notes', []):
            for L in ('es','en','fr','de'):
                t = n.get(L)
                if not t: continue
                new = t
                # strip soft hyphens in notes too
                ns = new.count("­")
                if ns:
                    new = new.replace("­","")
                    totals['softhy'] += ns
                new2, n_s = collapse_spaced(new)
                if n_s:
                    totals['spaced'] += n_s
                    new = new2
                if new != t:
                    n[L] = new
    COMM.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    return totals


def main():
    totals = {}
    for p in [SRC / 'ch_vorrede.ptx'] + sorted(CH.glob('ch_p*.ptx')):
        c = scrub_ptx(p)
        for k, v in c.items():
            totals[k] = totals.get(k, 0) + v
    print('ES PTX scrubs:')
    for k, v in totals.items():
        print(f'  {k:16s} {v}')
    ct = scrub_commentary()
    print('commentary scrubs:')
    for k, v in ct.items():
        print(f'  {k:16s} {v}')


if __name__ == '__main__':
    main()
