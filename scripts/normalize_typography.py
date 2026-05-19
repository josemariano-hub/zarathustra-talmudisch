#!/usr/bin/env python3
"""
Normalize quote characters per language across PreTeXt chapter files and
commentary.json note bodies. Idempotent. Conservative: only touches stray
ASCII " and ' characters by deciding open vs close from local context,
never converts something that is already curly/low-9.

  DE  : stray "  → „ if at a left edge (preceded by whitespace/sentence-start
                     /opening punctuation), → " otherwise
        stray '  → ' (right single, used as apostrophe)
  EN  : stray "  → " / " by left/right context
        stray '  → ' inside words, ' / ' otherwise
  ES / FR : leave alone (already canonical; mixed-FR conventions intact)
"""
from __future__ import annotations
import json, re
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
CH   = SRC / "chapters"
COMM = SRC / "commentary.json"

OPEN_LEFT_CTX = set(' \t\n\r([{¿¡—–-/«„“')   # characters that precede an opening quote
# A " is OPENING if the preceding char is whitespace/start/opening-punct,
# AND the following char is a letter / digit / opening-of-clause.

def _is_opening(prev: str, nxt: str) -> bool:
    if prev == '' or prev in OPEN_LEFT_CTX:
        # at left edge — opening unless next is also whitespace/punct
        return not (nxt == '' or nxt in '.,;:!?)]}»”’')
    return False

def normalize_quotes(text: str, lang: str) -> tuple[str, int]:
    """Normalize only stray ASCII " by pair-tracking within the paragraph.
    Existing curly/low-9 marks toggle the state too, so a paragraph that
    already begins with „ and ends in ASCII " correctly closes with the
    matching closing curly. Apostrophes are left alone."""
    if lang not in ('de', 'en'):
        return text, 0
    OPEN_CHARS  = ('„', '“') if lang == 'de' else ('“',)
    CLOSE_CHARS = ('“',)      if lang == 'de' else ('”',)
    # Note: in DE the closing mark IS U+201C, the same as EN's opening curly,
    # which makes a flat character-set classification ambiguous; we resolve by
    # state below.
    n = 0
    out = []
    dq_open = False
    for c in text:
        if c == '"':
            if not dq_open:
                out.append('„' if lang == 'de' else '“'); dq_open = True
            else:
                out.append('“' if lang == 'de' else '”'); dq_open = False
            n += 1
        elif c == '„':                       # DE low-9 — always opening
            out.append(c); dq_open = True
        elif c == '”':                       # EN closing — always closing
            out.append(c); dq_open = False
        elif c == '“':
            # EN opening, OR DE closing — disambiguate by state
            if lang == 'en':
                out.append(c); dq_open = True
            else:
                # In DE: opening unless we are already open
                if dq_open:
                    out.append(c); dq_open = False
                else:
                    out.append(c); dq_open = True
        else:
            out.append(c)
    return ''.join(out), n


P_RE = re.compile(r'(<p xml:id="[^"]+" xml:lang="(de|en)"[^>]*>)(.*?)(</p>)', re.DOTALL)

def process_ptx(p: Path) -> int:
    txt = p.read_text(encoding='utf-8')
    total = 0
    def repl(m):
        nonlocal total
        head, lang, body, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        # keep tags untouched, work only on text nodes between them
        parts = re.split(r'(<[^>]+>)', body)
        for i, part in enumerate(parts):
            if part.startswith('<'): continue
            new, n = normalize_quotes(part, lang)
            parts[i] = new
            total += n
        return head + ''.join(parts) + tail
    new_txt = P_RE.sub(repl, txt)
    if new_txt != txt:
        p.write_text(new_txt, encoding='utf-8')
    return total

def process_commentary() -> int:
    d = json.loads(COMM.read_text(encoding='utf-8'))
    total = 0
    for sname, st in d['streams'].items():
        if sname.startswith('_'): continue
        for n in st.get('notes', []):
            for L in ('de','en'):
                t = n.get(L)
                if not t: continue
                new, cnt = normalize_quotes(t, L)
                if new != t:
                    n[L] = new
                    total += cnt
    COMM.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    return total

def main():
    total = 0
    for p in [SRC / 'ch_vorrede.ptx'] + sorted(CH.glob('ch_p*.ptx')):
        total += process_ptx(p)
    print(f'PTX files: {total} substitutions')
    c = process_commentary()
    print(f'commentary.json: {c} substitutions')

if __name__ == '__main__':
    main()
