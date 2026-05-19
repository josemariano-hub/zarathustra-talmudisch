#!/usr/bin/env python3
"""
Generate one PreTeXt source file per chapter of Also sprach Zarathustra
from the three public-domain Gutenberg editions:

  DE  Project Gutenberg #7205  (Original, Leipzig 1883)
  EN  Project Gutenberg #1998  (Thomas Common translation, 1909)
  FR  Project Gutenberg #5258  (Henri Albert translation, 1903)

For Spanish we have no public-domain source; the existing hand-tuned
ES translation for Vorrede §1 stays in ch_vorrede.ptx and the rest of
the book leaves ES empty (the reader gracefully falls back).

Each generated file contains <chapter><section><paragraphs>… with each
<paragraphs xml:id="vNN"> bundling DE/EN/FR variants of one paragraph.

Alignment strategy
------------------
DE has rock-solid markers (each chapter title is on its own line, the
full title list comes from the TOC).  EN has Roman-numeral chapter
markers ("I. THE THREE METAMORPHOSES.").  FR has occasional plain-text
chapter titles (e.g. "Les trois métamorphoses.") preceded by two blank
lines.  We split each language by its own markers, then align chapters
by ordinal index within each Part.  Within a chapter, paragraphs are
aligned by index (DE-paragraph-1 ↔ EN-paragraph-1 ↔ FR-paragraph-1).
When the paragraph counts differ across languages the script logs a
warning and still emits whatever each language has — the renderer
shows missing translations gracefully.
"""

from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from xml.sax.saxutils import escape as xml_escape

ROOT     = Path("/Volumes/X10 Pro/Zarathustra")
ORIG     = ROOT / "original"
PROJECT  = ROOT / "zarathustra-pt"
SRC_DIR  = PROJECT / "source"
GEN_DIR  = SRC_DIR / "chapters"
GEN_DIR.mkdir(parents=True, exist_ok=True)

DE_FILE = ORIG / "Also_sprach_Zarathustra_DE.txt"
EN_FILE = ORIG / "Thus_Spake_Zarathustra_EN_Common.txt"
FR_FILE = ORIG / "Ainsi_Parlait_Zarathoustra_FR.txt"

def strip_pg_license(raw: str) -> str:
    """Remove trailing Project Gutenberg license/credits — they get parsed
    as bogus extra paragraphs in the last chapter otherwise."""
    for marker in ("*** END OF THIS PROJECT GUTENBERG",
                   "*** END OF THE PROJECT GUTENBERG",
                   "End of Project Gutenberg's",
                   "End of the Project Gutenberg",
                   "End of Project Gutenberg"):
        i = raw.find(marker)
        if i > 0:
            raw = raw[:i]
            break
    return raw

# ----------------------------------------------------------------------
# Canonical chapter map (manually curated from the DE TOC) — index, part,
# DE title, EN title, FR title.  The Vorrede (Prologue) is part 0.
# ----------------------------------------------------------------------
CHAPTERS = [
    # (part, idx_in_part, de_title, en_title, fr_title)
    (0, 0,  "Zarathustra's Vorrede",          "ZARATHUSTRA'S PROLOGUE",                  "LE PROLOGUE DE ZARATHOUSTRA"),

    (1, 1,  "Von den drei Verwandlungen",     "THE THREE METAMORPHOSES",                 "Les trois métamorphoses."),
    (1, 2,  "Von den Lehrstühlen der Tugend", "THE ACADEMIC CHAIRS OF VIRTUE",           "Des chaires de vertu."),
    (1, 3,  "Von den Hinterweltlern",         "BACKWORLDSMEN",                           "Les hallucinés de l'arrière-monde."),
    (1, 4,  "Von den Verächtern des Leibes",  "THE DESPISERS OF THE BODY",               "Des contempteurs du corps."),
    (1, 5,  "Von den Freuden- und Leidenschaften", "JOYS AND PASSIONS",                  "Des joies et des passions."),
    (1, 6,  "Vom bleichen Verbrecher",        "THE PALE CRIMINAL",                       "Du criminel blême."),
    (1, 7,  "Vom Lesen und Schreiben",        "READING AND WRITING",                     "Lire et écrire."),
    (1, 8,  "Vom Baum am Berge",              "THE TREE ON THE HILL",                    "De l'arbre sur la montagne."),
    (1, 9,  "Von den Predigern des Todes",    "THE PREACHERS OF DEATH",                  "Des prédicateurs de la mort."),
    (1, 10, "Vom Krieg und Kriegsvolke",      "WAR AND WARRIORS",                        "De la guerre et des guerriers."),
    (1, 11, "Vom neuen Götzen",               "THE NEW IDOL",                            "De la nouvelle idole."),
    (1, 12, "Von den Fliegen des Marktes",    "THE FLIES IN THE MARKET-PLACE",           "Des mouches de la place publique."),
    (1, 13, "Von der Keuschheit",             "CHASTITY",                                "De la chasteté."),
    (1, 14, "Vom Freunde",                    "THE FRIEND",                              "De l'ami."),
    (1, 15, "Von tausend und Einem Ziele",    "THE THOUSAND AND ONE GOALS",              "Des mille et un buts."),
    (1, 16, "Von der Nächstenliebe",          "NEIGHBOUR-LOVE",                          "De l'amour du prochain."),
    (1, 17, "Vom Wege des Schaffenden",       "THE WAY OF THE CREATING ONE",             "Du chemin du créateur."),
    (1, 18, "Von alten und jungen Weiblein",  "OLD AND YOUNG WOMEN",                     "Des vieilles et des jeunes femmelettes."),
    (1, 19, "Vom Biss der Natter",            "THE BITE OF THE ADDER",                   "De la morsure de la vipère."),
    (1, 20, "Von Kind und Ehe",               "CHILD AND MARRIAGE",                      "De l'enfant et du mariage."),
    (1, 21, "Vom freien Tode",                "VOLUNTARY DEATH",                         "De la libre mort."),
    (1, 22, "Von der schenkenden Tugend",     "THE BESTOWING VIRTUE",                    "De la vertu qui donne."),

    (2, 1,  "Das Kind mit dem Spiegel",       "THE CHILD WITH THE MIRROR",               "L'enfant au miroir."),
    (2, 2,  "Auf den glückseligen Inseln",    "IN THE HAPPY ISLES",                      "Sur les îles bienheureuses."),
    (2, 3,  "Von den Mitleidigen",            "THE PITIFUL",                             "Des miséricordieux."),
    (2, 4,  "Von den Priestern",              "THE PRIESTS",                             "Des prêtres."),
    (2, 5,  "Von den Tugendhaften",           "THE VIRTUOUS",                            "Des vertueux."),
    (2, 6,  "Vom Gesindel",                   "THE RABBLE",                              "De la canaille."),
    (2, 7,  "Von den Taranteln",              "THE TARANTULAS",                          "Des tarentules."),
    (2, 8,  "Von den berühmten Weisen",       "THE FAMOUS WISE ONES",                    "Des sages illustres."),
    (2, 9,  "Das Nachtlied",                  "THE NIGHT-SONG",                          "Le chant de la nuit."),
    (2, 10, "Das Tanzlied",                   "THE DANCE-SONG",                          "Le chant de la danse."),
    (2, 11, "Das Grablied",                   "THE GRAVE-SONG",                          "Le chant du tombeau."),
    (2, 12, "Von der Selbst-Überwindung",     "SELF-SURPASSING",                         "De la victoire sur soi-même."),
    (2, 13, "Von den Erhabenen",              "THE SUBLIME ONES",                        "Des hommes sublimes."),
    (2, 14, "Vom Lande der Bildung",          "THE LAND OF CULTURE",                     "Du pays de la civilisation."),
    (2, 15, "Von der unbefleckten Erkenntniss", "IMMACULATE PERCEPTION",                 "De l'immaculée connaissance."),
    (2, 16, "Von den Gelehrten",              "SCHOLARS",                                "Des savants."),
    (2, 17, "Von den Dichtern",               "POETS",                                   "Des poètes."),
    (2, 18, "Von grossen Ereignissen",        "GREAT EVENTS",                            "Des grands événements."),
    (2, 19, "Der Wahrsager",                  "THE SOOTHSAYER",                          "Le devin."),
    (2, 20, "Von der Erlösung",               "REDEMPTION",                              "De la rédemption."),
    (2, 21, "Von der Menschen-Klugheit",      "MANLY PRUDENCE",                          "De la prudence avec les hommes."),
    (2, 22, "Die stillste Stunde",            "THE STILLEST HOUR",                       "L'heure la plus silencieuse."),

    (3, 1,  "Der Wanderer",                   "THE WANDERER",                            "Le voyageur."),
    (3, 2,  "Vom Gesicht und Räthsel",        "THE VISION AND THE ENIGMA",               "De la vision et de l'énigme."),
    (3, 3,  "Von der Seligkeit wider Willen", "INVOLUNTARY BLISS",                       "De la béatitude malgré soi."),
    (3, 4,  "Vor Sonnen-Aufgang",             "BEFORE SUNRISE",                          "Avant le lever du soleil."),
    (3, 5,  "Von der verkleinernden Tugend",  "THE BEDWARFING VIRTUE",                   "De la vertu qui rapetisse."),
    (3, 6,  "Auf dem Ölberge",                "ON THE OLIVE-MOUNT",                      "Sur le mont des Oliviers."),
    (3, 7,  "Vom Vorübergehen",               "PASSING-BY",                              "En passant."),
    (3, 8,  "Von den Abtrünnigen",            "THE APOSTATES",                           "Des transfuges."),
    (3, 9,  "Die Heimkehr",                   "THE RETURN HOME",                         "Le retour."),
    (3, 10, "Von den drei Bösen",             "THE THREE EVIL THINGS",                   "Des trois maux."),
    (3, 11, "Vom Geist der Schwere",          "THE SPIRIT OF GRAVITY",                   "De l'esprit de lourdeur."),
    (3, 12, "Von alten und neuen Tafeln",     "OLD AND NEW TABLES",                      "Des vieilles et des nouvelles tables."),
    (3, 13, "Der Genesende",                  "THE CONVALESCENT",                        "Le convalescent."),
    (3, 14, "Von der grossen Sehnsucht",      "THE GREAT LONGING",                       "Du grand désir."),
    (3, 15, "Das andere Tanzlied",            "THE SECOND DANCE-SONG",                   "L'autre chant de la danse."),
    (3, 16, "Die sieben Siegel",              "THE SEVEN SEALS",                         "Les sept sceaux."),

    (4, 1,  "Das Honig-Opfer",                "THE HONEY SACRIFICE",                     "L'offrande du miel."),
    (4, 2,  "Der Nothschrei",                 "THE CRY OF DISTRESS",                     "Le cri de détresse."),
    (4, 3,  "Gespräch mit den Königen",       "TALK WITH THE KINGS",                     "Entretien avec les rois."),
    (4, 4,  "Der Blutegel",                   "THE LEECH",                               "La sangsue."),
    (4, 5,  "Der Zauberer",                   "THE MAGICIAN",                            "L'enchanteur."),
    (4, 6,  "Ausser Dienst",                  "OUT OF SERVICE",                          "Hors de service."),
    (4, 7,  "Der hässlichste Mensch",         "THE UGLIEST MAN",                         "Le plus laid des hommes."),
    (4, 8,  "Der freiwillige Bettler",        "THE VOLUNTARY BEGGAR",                    "Le mendiant volontaire."),
    (4, 9,  "Der Schatten",                   "THE SHADOW",                              "L'ombre."),
    (4, 10, "Mittags",                        "NOONTIDE",                                "En plein midi."),
    (4, 11, "Die Begrüssung",                 "THE GREETING",                            "La salutation."),
    (4, 12, "Das Abendmahl",                  "THE SUPPER",                              "La Cène."),
    (4, 13, "Vom höheren Menschen",           "THE HIGHER MAN",                          "De l'homme supérieur."),
    (4, 14, "Das Lied der Schwermuth",        "THE SONG OF MELANCHOLY",                  "Le chant de la mélancolie."),
    (4, 15, "Von der Wissenschaft",           "SCIENCE",                                 "De la science."),
    (4, 16, "Unter Töchtern der Wüste",       "AMONG DAUGHTERS OF THE DESERT",           "Parmi les filles du désert."),
    (4, 17, "Die Erweckung",                  "THE AWAKENING",                           "Le réveil."),
    (4, 18, "Das Eselsfest",                  "THE ASS-FESTIVAL",                        "La fête de l'âne."),
    (4, 19, "Das Nachtwandler-Lied",          "THE DRUNKEN SONG",                        "Le chant du noctambule."),
    (4, 20, "Das Zeichen",                    "THE SIGN",                                "Le signe."),
]

# ----------------------------------------------------------------------
# Generic helpers
# ----------------------------------------------------------------------
def slug(s: str) -> str:
    """ASCII slug from a chapter title."""
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:50]

def split_paragraphs(text: str) -> list[str]:
    """Split a chunk of text into paragraphs on blank lines, normalising whitespace."""
    paras = re.split(r"\n[ \t]*\n+", text.strip())
    out = []
    for p in paras:
        p = re.sub(r"\s+", " ", p.strip())
        if p and not re.fullmatch(r"\d+\.?", p):  # drop standalone "1." section markers
            out.append(p)
    return out

# ----------------------------------------------------------------------
# DE parser — uses the chapter-title list from CHAPTERS to split.
# ----------------------------------------------------------------------
def parse_de() -> dict[tuple[int,int], list[str]]:
    """Return {(part, idx): [paragraphs]}."""
    raw = DE_FILE.read_text(encoding="utf-8")
    raw = strip_pg_license(raw)
    # Strip the Gutenberg header up to just before the actual book text.
    start = raw.find("Erster Theil\n\n")
    if start < 0:
        # fallback: find the second occurrence of "Erster Theil"
        idx1 = raw.find("Erster Theil")
        start = raw.find("Erster Theil", idx1 + 1)
    raw = raw[start:]
    # Replace fancy apostrophe so titles match
    norm = raw.replace("’", "'")
    # Build an ordered list of (title, regex) markers from CHAPTERS
    titles = [(p, i, de) for (p, i, de, _en, _fr) in CHAPTERS]
    # Find each title's position
    positions = []
    for part, idx, title in titles:
        t = title.replace("'", "'")
        # The marker line is "<TITLE>." or "<TITLE>"
        # Use a tolerant search
        pat = re.compile(r"\n\s*" + re.escape(t) + r"\.?\s*\n", re.IGNORECASE)
        m = pat.search(norm)
        if not m:
            print(f"  DE MISS: {title}")
            continue
        positions.append((part, idx, title, m.start(), m.end()))
    positions.sort(key=lambda x: x[3])

    out: dict[tuple[int,int], list[str]] = {}
    for i, (part, idx, title, _s, e) in enumerate(positions):
        end = positions[i+1][3] if i+1 < len(positions) else len(norm)
        body = norm[e:end]
        # Drop bare part dividers like "Zweiter Theil" mid-chunk
        body = re.sub(r"\n\s*(Zweiter|Dritter|Vierter und letzter|Vierter)\s+Theil\.?\s*\n", "\n\n", body)
        # Drop standalone section markers (1., 2., ...) but keep them in the
        # paragraph if they're part of paragraph text.
        out[(part, idx)] = split_paragraphs(body)
    return out

# ----------------------------------------------------------------------
# EN parser — uses Roman-numeral chapter markers, plus "ZARATHUSTRA'S PROLOGUE".
# ----------------------------------------------------------------------
ROMAN_RE = re.compile(r"^([IVXLCDM]+)\.\s+([A-Z][A-Z0-9 ,.'’\-]+)\.?\s*$", re.MULTILINE)

def parse_en() -> dict[tuple[int,int], list[str]]:
    raw = EN_FILE.read_text(encoding="utf-8")
    raw = strip_pg_license(raw)
    # Common's edition has a long appendix of translator notes by Ludovici
    # after the last chapter — strip it.
    i = raw.find("NOTES ON ")
    if i > 0: raw = raw[:i]
    # Locate prologue start
    p_start = raw.find("ZARATHUSTRA'S PROLOGUE")
    if p_start < 0:
        p_start = raw.find("ZARATHUSTRA’S PROLOGUE")
    raw = raw[p_start:]

    # Find Prologue end — first roman-numeral chapter marker
    m = ROMAN_RE.search(raw)
    if not m:
        print("  EN: no Roman markers found")
        return {}
    prologue_text = raw[:m.start()]
    body = raw[m.start():]

    out: dict[tuple[int,int], list[str]] = {}
    # Prologue body — strip the title line
    proLines = prologue_text.split("\n", 2)
    out[(0,0)] = split_paragraphs("\n".join(proLines[1:]))

    # Walk the chapter markers
    markers = list(ROMAN_RE.finditer(body))
    for i, m in enumerate(markers):
        roman = m.group(1)
        # Figure out which (part,idx) this corresponds to via global ordinal
        ordinal = roman_to_int(roman)
        # Ordinal mapping:
        # 1..22  -> part1 idx1..22
        # 23..44 -> part2 idx1..22
        # 45..60 -> part3 idx1..16
        # 61..80 -> part4 idx1..20
        if ordinal <= 22: part, idx = 1, ordinal
        elif ordinal <= 44: part, idx = 2, ordinal - 22
        elif ordinal <= 60: part, idx = 3, ordinal - 44
        else: part, idx = 4, ordinal - 60
        start = m.end()
        end = markers[i+1].start() if i+1 < len(markers) else len(body)
        chunk = body[start:end]
        # Drop initial blank lines + footer
        chunk = re.split(r"\n\s*End of Project Gutenberg", chunk)[0]
        out[(part,idx)] = split_paragraphs(chunk)
    return out

def roman_to_int(s: str) -> int:
    m = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    total, prev = 0, 0
    for ch in reversed(s):
        v = m[ch]
        if v < prev: total -= v
        else: total += v
        prev = v
    return total

# ----------------------------------------------------------------------
# FR parser — split by part markers, then by chapter-title patterns.
# ----------------------------------------------------------------------
FR_PARTS = [
    "LE PROLOGUE DE ZARATHOUSTRA",
    "LES DISCOURS DE ZARATHOUSTRA",
    "DEUXIÈME PARTIE",
    "TROISIÈME PARTIE",
    "QUATRIÈME ET DERNIÈRE PARTIE",
]

def parse_fr() -> dict[tuple[int,int], list[str]]:
    """Robust FR parser: split by the file's own ALL-CAPS chapter title
    lines, then assign them ordinally to (part, idx).  This works even when
    individual FR chapter titles deviate from the DE/EN forms."""
    raw = FR_FILE.read_text(encoding="utf-8")
    raw = strip_pg_license(raw)
    # truncate any "APPENDICE" content that follows the book proper
    appx = raw.find("\nAPPENDICE")
    if appx > 0: raw = raw[:appx]
    return _parse_fr_ordinal(raw)

def _parse_fr_ordinal(raw: str) -> dict[tuple[int,int], list[str]]:
    """Detect ALL-CAPS chapter title lines (and the one known mixed-case
    title 'Les trois métamorphoses.'), split by them, then place each
    chunk into (part, idx) by ordinal."""
    out: dict[tuple[int,int], list[str]] = {}

    # part dividers — keep these so we can change "part" as we walk
    part_markers = [
        ("PREMIÈRE PARTIE", 1),
        ("DEUXIÈME PARTIE", 2),
        ("TROISIÈME PARTIE", 3),
        ("QUATRIÈME ET DERNIÈRE PARTIE", 4),
    ]
    # Find positions of every part-marker
    part_positions = []
    for marker, pnum in part_markers:
        i = raw.find(marker)
        if i >= 0: part_positions.append((i, pnum, marker))
    part_positions.sort()

    # Chapter title regex: a line of UPPERCASE (incl. accents, apostrophes,
    # spaces, hyphens) between 4 and 70 chars, on its own line. Plus the
    # special-case mixed-case Part-1 ch.1 title.
    UC = r"A-ZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝŸŒ"
    title_re = re.compile(
        r"(?m)^(?P<t>"
        rf"(?:[{UC}][{UC} '!,\-]{{3,69}})"          # all-caps incl. all accents
        r"|Les trois métamorphoses\."                # mixed-case special
        r")\s*$"
    )

    # Skip these as titles even if they match (they are part-dividers /
    # book heading and shouldn't be a chapter)
    SKIP = {
        "AINSI PARLAIT ZARATHOUSTRA", "PREMIÈRE PARTIE", "DEUXIÈME PARTIE",
        "TROISIÈME PARTIE", "QUATRIÈME ET DERNIÈRE PARTIE",
        "LES DISCOURS DE ZARATHOUSTRA",
        "APPENDICE",
    }

    # walk title matches
    candidates = []
    for m in title_re.finditer(raw):
        t = m.group("t").strip()
        if t in SKIP: continue
        candidates.append((m.start(), m.end(), t))

    # Helper: which part does an absolute position belong to?
    def part_of(pos: int) -> int:
        cur = 0
        for p_start, pnum, _ in part_positions:
            if pos >= p_start: cur = pnum
            else: break
        return cur

    # Group candidates by part, assign ordinal idx starting at 0 for the
    # Prologue (part 0) — there is exactly one chapter in part 0 — and 1
    # for first chapter of each other part.
    # The Prologue title "LE PROLOGUE DE ZARATHOUSTRA" is the first
    # candidate (before PREMIÈRE PARTIE? actually it's after PREMIÈRE).
    # We'll treat "LE PROLOGUE" specifically as (0,0).
    grouped: dict[int, list[tuple[int,int,str]]] = {0:[],1:[],2:[],3:[],4:[]}
    for start, end, t in candidates:
        if t.startswith("LE PROLOGUE"):
            grouped[0].append((start, end, t))
        else:
            grouped[part_of(start)].append((start, end, t))

    # Within each part, assign ordinal idx
    for part, items in grouped.items():
        items.sort()
        for i, (start, end, t) in enumerate(items):
            idx = 0 if part == 0 else (i + 1)
            # body runs from end-of-title to start-of-next-title-in-any-part
            # Find next title position globally
            next_pos = len(raw)
            for q_start, _q_end, _q_t in candidates:
                if q_start > end and q_start < next_pos:
                    next_pos = q_start
            body = raw[end:next_pos]
            # Drop part-divider lines that may be in the body
            body = re.sub(r"\n\s*(?:PREMIÈRE|DEUXIÈME|TROISIÈME|QUATRIÈME ET DERNIÈRE)\s+PARTIE\s*\n", "\n\n", body)
            body = re.sub(r"\n\s*LES DISCOURS DE ZARATHOUSTRA\s*\n", "\n\n", body)
            out[(part, idx)] = split_paragraphs(body)
    return out

    out: dict[tuple[int,int], list[str]] = {}

    # Build a list of every FR chapter title we know about
    chapters_by_part = {p: [] for p in [0,1,2,3,4]}
    for (part, idx, _de, _en, fr) in CHAPTERS:
        chapters_by_part[part].append((idx, fr))

    # The Prologue is treated as one chapter (0,0).  Title marker:
    p_start = raw.find("LE PROLOGUE DE ZARATHOUSTRA")
    if p_start < 0:
        return out

    # End of prologue: next part marker "LES DISCOURS DE ZARATHOUSTRA"
    ld_pos = raw.find("LES DISCOURS DE ZARATHOUSTRA", p_start)
    if ld_pos < 0: ld_pos = len(raw)
    prologue_body = raw[p_start + len("LE PROLOGUE DE ZARATHOUSTRA"):ld_pos]
    out[(0,0)] = split_paragraphs(prologue_body)

    # OLD PATH (kept for reference — replaced by _parse_fr_ordinal which is
    # called from parse_fr() above).
    return out
    # For Parts 1..4, locate the part header and the next part header to get
    # the part-body, then split by chapter title within.
    part_markers = [
        ("LES DISCOURS DE ZARATHOUSTRA", 1),
        ("DEUXIÈME PARTIE", 2),
        ("TROISIÈME PARTIE", 3),
        ("QUATRIÈME ET DERNIÈRE PARTIE", 4),
    ]
    # Find each
    starts = {}
    for marker, part in part_markers:
        pos = raw.find(marker)
        if pos >= 0:
            starts[part] = pos + len(marker)
    # End positions
    for i, (marker, part) in enumerate(part_markers):
        s = starts.get(part)
        if s is None: continue
        # next part start = next marker's position (raw, before consumption)
        if i+1 < len(part_markers):
            e_marker, _ = part_markers[i+1]
            e = raw.find(e_marker, s)
            if e < 0: e = len(raw)
        else:
            e = len(raw)
        body = raw[s:e]
        # find each chapter title in this part body
        titles = chapters_by_part.get(part, [])
        positions = []
        for idx, title in titles:
            # Try (a) exact, (b) without trailing dot, (c) with apostrophe normalised
            t_core = title.rstrip(".").strip()
            candidates = [
                t_core,
                t_core.replace("'", "'"),
                t_core.replace("œ", "oe"),
                t_core.replace("Œ", "Oe"),
            ]
            m = None
            for cand in candidates:
                pat = re.compile(r"\n\s*" + re.escape(cand) + r"\.?\s*\n", re.IGNORECASE)
                m = pat.search(body)
                if m: break
            if not m:
                # very loose: first 4 significant words
                words = re.findall(r"\w{3,}", t_core.lower())[:4]
                if words:
                    loose = r"\s+".join(re.escape(w) for w in words)
                    pat = re.compile(r"\n\s*[A-ZÉÈÊÀÔÎÇ][^\n]{0,80}?" + loose, re.IGNORECASE)
                    m = pat.search(body)
            if not m:
                print(f"  FR MISS [part {part}]: {title}")
                continue
            positions.append((idx, title, m.start(), m.end()))
        positions.sort(key=lambda x: x[2])
        for j, (idx, title, _s, e) in enumerate(positions):
            stop = positions[j+1][2] if j+1 < len(positions) else len(body)
            chunk = body[e:stop]
            out[(part, idx)] = split_paragraphs(chunk)
    return out

# ----------------------------------------------------------------------
# PreTeXt emission
# ----------------------------------------------------------------------
def to_ptx_text(s: str) -> str:
    """Escape special PreTeXt chars and preserve _underline_ as <em>."""
    # Common does _word_ for emphasis; convert to <em>word</em>
    s = re.sub(r"_([^_]+?)_", r"<em>\1</em>", s)
    # Now escape XML except our <em> tags
    # Cheap approach: temporarily swap em markers, escape, swap back
    s = s.replace("<em>", "\x01EM\x01").replace("</em>", "\x01/EM\x01")
    s = xml_escape(s)
    s = s.replace("\x01EM\x01", "<em>").replace("\x01/EM\x01", "</em>")
    return s

def emit_chapter(part: int, idx: int, de_title: str, en_title: str, fr_title: str,
                 de_paras: list[str], en_paras: list[str], fr_paras: list[str]) -> Path:
    n_paras = max(len(de_paras), len(en_paras), len(fr_paras))
    if n_paras == 0:
        print(f"  SKIP empty: {de_title}")
        return None

    safe = slug(de_title)
    fname = f"ch_p{part}_{idx:02d}_{safe}.ptx"
    out = GEN_DIR / fname

    xml_id = f"ch-p{part}-{idx:02d}"
    sec_id = f"sec-{xml_id}"

    lines = []
    lines.append("<?xml version='1.0' encoding='utf-8'?>\n")
    lines.append(f'<chapter xml:id="{xml_id}" xml:lang="de">\n')
    lines.append(f"  <title>{xml_escape(de_title)}</title>\n\n")
    lines.append(f'  <section xml:id="{sec_id}">\n')
    lines.append(f"    <title>{xml_escape(de_title)}</title>\n\n")

    for i in range(n_paras):
        vid = f"v{(i+1):02d}"
        lines.append(f'    <paragraphs xml:id="{xml_id}-{vid}">\n')
        lines.append(f"      <title>{vid}</title>\n")
        if i < len(de_paras):
            lines.append(f'      <p xml:id="{xml_id}-{vid}-de" xml:lang="de">{to_ptx_text(de_paras[i])}</p>\n')
        if i < len(en_paras):
            lines.append(f'      <p xml:id="{xml_id}-{vid}-en" xml:lang="en">{to_ptx_text(en_paras[i])}</p>\n')
        if i < len(fr_paras):
            lines.append(f'      <p xml:id="{xml_id}-{vid}-fr" xml:lang="fr">{to_ptx_text(fr_paras[i])}</p>\n')
        lines.append(f"    </paragraphs>\n\n")

    lines.append("  </section>\n")
    lines.append("</chapter>\n")

    out.write_text("".join(lines), encoding="utf-8")
    print(f"  wrote {fname}  ({len(de_paras)} DE, {len(en_paras)} EN, {len(fr_paras)} FR paragraphs)")
    return out

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    print("Parsing DE…")
    de_map = parse_de()
    print("Parsing EN…")
    en_map = parse_en()
    print("Parsing FR…")
    fr_map = parse_fr()

    # Wipe old generated chapter files (but keep ch_vorrede.ptx — that's the
    # hand-tuned one with rich commentary; we replace it conditionally)
    for old in GEN_DIR.glob("ch_*.ptx"):
        old.unlink()

    written = []
    for part, idx, de_title, en_title, fr_title in CHAPTERS:
        path = emit_chapter(
            part, idx, de_title, en_title, fr_title,
            de_map.get((part,idx), []),
            en_map.get((part,idx), []),
            fr_map.get((part,idx), []),
        )
        if path: written.append((part, idx, de_title, path))

    # Generate an index JSON that the reader can load to populate its chapter nav
    import json
    nav = []
    for part, idx, de_title, en_title, fr_title in CHAPTERS:
        nav.append({
            "part": part, "idx": idx,
            "de": de_title, "en": en_title, "fr": fr_title,
            "xml_id": f"ch-p{part}-{idx:02d}",
            "file": f"chapters/ch_p{part}_{idx:02d}_{slug(de_title)}.ptx",
        })
    (SRC_DIR / "chapter-nav.json").write_text(json.dumps(nav, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote chapter-nav.json with {len(nav)} entries.")

    # Generate include block for main.ptx
    includes = "\n".join(f'    <xi:include href="./chapters/{p.name}" />' for _,_,_,p in written)
    print(f"\n{len(written)} chapters written.")
    print("Include block (paste into main.ptx after the Vorrede line):")
    print(includes[:400] + "...")

if __name__ == "__main__":
    main()
