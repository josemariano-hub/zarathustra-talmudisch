#!/usr/bin/env python3
"""
Citation / cross-reference scrubs applied to commentary.json after the
note bodies are settled. Idempotent.

  4s  biblical citations: normalize variants to "Book Ch:V"
        Lucas, 3, 23      → Lucas 3:23
        Lucas 3, 23       → Lucas 3:23
        Gospel of Luke, 3:23 → Luke 3:23
        Évangile selon Luc, 3, 23 → Luc 3:23
  4t  ch-p1-22-v25 SP note: disambiguate "§ 1" → "§ 1 of this chapter"
        (per-language)
  4u  Sánchez Pascual self-references "nota NN" without a target work
        → suffix " (Alianza 1972)"
  6dd ch-p4-20-v04 Matthew quote: replace with KJV verbatim
"""
from __future__ import annotations
import json, re
from pathlib import Path

COMM = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt/source/commentary.json")

BIBLICAL_BOOKS = (
    # Spanish
    'Génesis','Éxodo','Levítico','Números','Deuteronomio','Josué','Jueces',
    'Rut','Samuel','Reyes','Crónicas','Esdras','Nehemías','Ester','Job',
    'Salmos','Proverbios','Eclesiastés','Cantares','Isaías','Jeremías',
    'Lamentaciones','Ezequiel','Daniel','Oseas','Joel','Amós','Abdías',
    'Jonás','Miqueas','Nahúm','Habacuc','Sofonías','Ageo','Zacarías',
    'Malaquías','Mateo','Marcos','Lucas','Juan','Hechos','Romanos',
    'Corintios','Gálatas','Efesios','Filipenses','Colosenses','Tesalonicenses',
    'Timoteo','Tito','Filemón','Hebreos','Santiago','Pedro','Apocalipsis',
    # English
    'Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges',
    'Ruth','Kings','Chronicles','Ezra','Nehemiah','Esther','Job','Psalms',
    'Proverbs','Ecclesiastes','Song of Songs','Isaiah','Jeremiah',
    'Lamentations','Ezekiel','Daniel','Hosea','Joel','Amos','Obadiah',
    'Jonah','Micah','Nahum','Habakkuk','Zephaniah','Haggai','Zechariah',
    'Malachi','Matthew','Mark','Luke','John','Acts','Romans','Corinthians',
    'Galatians','Ephesians','Philippians','Colossians','Thessalonians',
    'Timothy','Titus','Philemon','Hebrews','James','Peter','Revelation',
    # French
    'Genèse','Exode','Lévitique','Nombres','Deutéronome','Josué','Juges',
    'Rois','Chroniques','Esdras','Néhémie','Esther','Psaumes','Proverbes',
    'Ecclésiaste','Cantique','Isaïe','Jérémie','Ézéchiel','Daniel','Osée',
    'Joël','Amos','Abdias','Jonas','Michée','Nahum','Habacuc','Sophonie',
    'Aggée','Zacharie','Malachie','Matthieu','Marc','Luc','Jean','Actes',
    'Romains','Galates','Éphésiens','Philippiens','Colossiens',
    'Thessaloniciens','Timothée','Tite','Philémon','Hébreux','Jacques',
    'Pierre','Apocalypse',
)

BOOK_ALT = "|".join(sorted({re.escape(b) for b in BIBLICAL_BOOKS}, key=len, reverse=True))

# "Gospel of <book>, c:v" / "Evangelio de <book>, c, v" / "Évangile selon <book>, c:v"
GOSPEL_PREFIX_RE = re.compile(
    r'\b(?:el\s+)?(?:Evangelio de|the\s+Gospel\s+of|Évangile\s+selon)\s+(' + BOOK_ALT + r')\b,?\s*',
    re.IGNORECASE
)

# "Book c, v" or "Book c:v" or "Book c, v–w" → canonical "Book c:v"
CITATION_RE = re.compile(
    r'\b(' + BOOK_ALT + r')\s*,?\s+(\d{1,3})\s*[,:]\s*(\d{1,3}(?:[-–]\d{1,3})?)'
)

KJV_MATTHEW_26_40 = (
    "Matthew 26:40 (KJV): "
    "“And he cometh unto the disciples, and findeth them asleep.”"
)
KJV_MATTHEW_26_40_ES = (
    "Mateo 26:40 (Reina-Valera): "
    "«Y vino a sus discípulos, y los halló durmiendo.»"
)
KJV_MATTHEW_26_40_FR = (
    "Matthieu 26:40 (Louis Segond): "
    "«Et il vint vers ses disciples, et les trouva dormant.»"
)


def fix_biblical(text: str) -> tuple[str, int]:
    n = 0
    def repl_prefix(m):
        nonlocal n
        n += 1
        return m.group(1) + " "
    text2 = GOSPEL_PREFIX_RE.sub(repl_prefix, text)
    def repl_cite(m):
        nonlocal n
        n += 1
        return f"{m.group(1)} {m.group(2)}:{m.group(3)}"
    text2 = CITATION_RE.sub(repl_cite, text2)
    return text2, n


def fix_4t(d):
    """ch-p1-22-v25 SP note: disambiguate § 1."""
    n = 0
    for st in d['streams'].values():
        if isinstance(st, str): continue
        for note in st.get('notes', []):
            if note.get('target') != 'ch-p1-22-v25': continue
            # Substitute "§ 1" with chapter-scoped phrasing
            for L, suffix in (
                ('es', '§ 1 de este capítulo'),
                ('en', '§ 1 of this chapter'),
                ('fr', '§ 1 de ce chapitre'),
            ):
                if L not in note: continue
                old = note[L]
                new = re.sub(r'§\s*1(?!\d)', suffix, old, count=1)
                if new != old:
                    note[L] = new; n += 1
    return n


def fix_4u(d):
    """SP self-refs 'nota NN' without context → add ' (Alianza 1972)' once."""
    n = 0
    for sname, st in d['streams'].items():
        if isinstance(st, str): continue
        if sname not in ('sanchez-pascual-notes', 'sanchez-pascual',
                         'sp-introduction'):
            continue
        for note in st.get('notes', []):
            for L in ('es','en','fr','de'):
                t = note.get(L)
                if not t: continue
                # Only flag bare "nota NN" / "note NN" that ends a clause —
                # i.e. is followed by sentence punctuation or end-of-string.
                # When followed by "del traductor a *Work*" we leave it alone
                # because the work is already named.
                pat = re.compile(
                    r'\b(nota|note)\s+(\d{1,3})\b(?=\s*[\.;:,!\?\]\)»”\'""]|\s*$)'
                )
                def repl(m):
                    nonlocal n
                    n += 1
                    return f"{m.group(0)} (Alianza 1972)"
                new = pat.sub(repl, t)
                if new != t:
                    note[L] = new
    return n


def fix_6dd(d):
    """ch-p4-20-v04 SP note: replace Matthew paraphrase with KJV verbatim."""
    n = 0
    for st in d['streams'].values():
        if isinstance(st, str): continue
        for note in st.get('notes', []):
            if note.get('target') != 'ch-p4-20-v04': continue
            # Replace only the Matthew clause; preserve the lead-in
            for L, canon in (('en', KJV_MATTHEW_26_40),
                              ('es', KJV_MATTHEW_26_40_ES),
                              ('fr', KJV_MATTHEW_26_40_FR)):
                if L not in note: continue
                t = note[L]
                # crude replace: drop the existing "see Gospel… 26:40:" tail
                m = re.search(r'(see|véase|véase|voir|cf\.|cf)\b[^.]*?(Matthew|Mateo|Matthieu|Luke|Lucas|Luc)\b[^.]*?\d{1,2}[:,]\s*\d{1,2}[:"”»]?[^.]*\.?$', t, re.IGNORECASE)
                if m:
                    new = t[:m.start()].rstrip().rstrip(';,.').rstrip() + ". " + canon
                    if new != t:
                        note[L] = new; n += 1
    return n


def main():
    d = json.loads(COMM.read_text(encoding='utf-8'))
    n_bib = 0
    for st in d['streams'].values():
        if isinstance(st, str): continue
        for note in st.get('notes', []):
            for L in ('es','en','fr','de'):
                t = note.get(L)
                if not t: continue
                new, c = fix_biblical(t)
                if new != t:
                    note[L] = new; n_bib += c
    n_4t = fix_4t(d)
    n_4u = fix_4u(d)
    n_6dd = fix_6dd(d)
    COMM.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'normalize_citations:')
    print(f'  4s biblical citations normalized:   {n_bib}')
    print(f'  4t §1 disambiguations applied:      {n_4t}')
    print(f'  4u "nota NN" provenance added:      {n_4u}')
    print(f'  6dd Matthew 26:40 quotes rewritten: {n_6dd}')


if __name__ == '__main__':
    main()
