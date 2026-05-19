#!/usr/bin/env python3
"""
Parse Sánchez Pascual's Spanish translation (Alianza, 1997/2003) from the
pdftotext-extracted plain-text dump, split it into chapters, align them
paragraph-by-paragraph with the existing DE/EN/FR chapter files, and patch
every chapter .ptx in source/chapters/ to add <p xml:lang="es"> entries.

Also extracts the "Notas del traductor" section and writes a new commentary
stream (commentary-sp.json) that targets specific verses.
"""

from __future__ import annotations
import re, json, sys
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
TXT  = Path("/tmp/sp_zaratustra.txt")
SRC  = PROJ / "source"
CH   = SRC / "chapters"
NAV  = json.loads((SRC / "chapter-nav.json").read_text(encoding="utf-8"))

# Spanish chapter titles, in the order the book presents them.
ES_TITLES = [
    (0, 0, "Prólogo de Zaratustra"),
    (1, 1, "De las tres transformaciones"),
    (1, 2, "De las cátedras de la virtud"),
    (1, 3, "De los trasmundanos"),
    (1, 4, "De los despreciadores del cuerpo"),
    (1, 5, "De las alegrías y de las pasiones"),
    (1, 6, "Del pálido delincuente"),
    (1, 7, "Del leer y el escribir"),
    (1, 8, "Del árbol de la montaña"),
    (1, 9, "De los predicadores de la muerte"),
    (1, 10, "De la guerra y el pueblo guerrero"),
    (1, 11, "Del nuevo ídolo"),
    (1, 12, "De las moscas del mercado"),
    (1, 13, "De la castidad"),
    (1, 14, "Del amigo"),
    (1, 15, "De las mil metas y de la única meta"),
    (1, 16, "Del amor al prójimo"),
    (1, 17, "Del camino del creador"),
    (1, 18, "De viejecillas y de jovencillas"),
    (1, 19, "De la picadura de la víbora"),
    (1, 20, "Del hijo y del matrimonio"),
    (1, 21, "De la muerte libre"),
    (1, 22, "De la virtud que hace regalos"),
    (2, 1, "El niño del espejo"),
    (2, 2, "En las islas afortunadas"),
    (2, 3, "De los compasivos"),
    (2, 4, "De los sacerdotes"),
    (2, 5, "De los virtuosos"),
    (2, 6, "De la chusma"),
    (2, 7, "De las tarántulas"),
    (2, 8, "De los sabios famosos"),
    (2, 9, "La canción de la noche"),
    (2, 10, "La canción del baile"),
    (2, 11, "La canción de los sepulcros"),
    (2, 12, "De la superación de sí mismo"),
    (2, 13, "De los sublimes"),
    (2, 14, "Del país de la cultura"),
    (2, 15, "Del inmaculado conocimiento"),
    (2, 16, "De los doctos"),
    (2, 17, "De los poetas"),
    (2, 18, "De grandes acontecimientos"),
    (2, 19, "El adivino"),
    (2, 20, "De la redención"),
    (2, 21, "De la cordura respecto a los hombres"),
    (2, 22, "La más silenciosa de todas las horas"),
    (3, 1, "El caminante"),
    (3, 2, "De la visión y enigma"),
    (3, 3, "De la bienaventuranza no querida"),
    (3, 4, "Antes de la salida del sol"),
    (3, 5, "De la virtud empequeñecedora"),
    (3, 6, "En el monte de los olivos"),
    (3, 7, "Del pasar de largo"),
    (3, 8, "De los apóstatas"),
    (3, 9, "El retorno a casa"),
    (3, 10, "De los tres males"),
    (3, 11, "Del espíritu de la pesadez"),
    (3, 12, "De tablas viejas y nuevas"),
    (3, 13, "El convaleciente"),
    (3, 14, "Del gran anhelo"),
    (3, 15, "La otra canción del baile"),
    (3, 16, "Los siete sellos"),       # plus "(o: La canción «Sí y Amén»)"
    (4, 1, "La ofrenda de la miel"),
    (4, 2, "El grito de socorro"),
    (4, 3, "Coloquio con los reyes"),
    (4, 4, "La sanguijuela"),
    (4, 5, "El mago"),
    (4, 6, "Jubilado"),
    (4, 7, "El más feo de los hombres"),
    (4, 8, "El mendigo voluntario"),
    (4, 9, "La sombra"),
    (4, 10, "A mediodía"),
    (4, 11, "El saludo"),
    (4, 12, "La Cena"),
    (4, 13, "Del hombre superior"),
    (4, 14, "La canción de la melancolía"),
    (4, 15, "De la ciencia"),
    (4, 16, "Entre hijas del desierto"),
    (4, 17, "El despertar"),
    (4, 18, "La fiesta del asno"),
    (4, 19, "La canción del noctámbulo"),
    (4, 20, "El signo"),
]

def load_book_text() -> str:
    raw = TXT.read_text(encoding="utf-8")
    # pdftotext inserts form-feed characters between pages. Treat them as
    # additional blank-line separators.
    raw = raw.replace("\f", "\n\n")
    # Locate the actual book start (the chapter title line on its own).
    # The Intro mentions "el Prólogo de Zaratustra" earlier; we want the
    # SECOND or later standalone-line occurrence.
    matches = [m.start() for m in re.finditer(r"(?m)^Prólogo de Zaratustra\s*$", raw)]
    if not matches:
        sys.exit("could not find Prólogo de Zaratustra start")
    start = matches[0]
    # Locate end-of-book marker
    end = raw.find("Fin de Así HABL")
    if end < 0:
        end = raw.find("Notas del traductor")
    if end < 0:
        end = len(raw)
    return raw[start:end]

# Page-header pattern: title with a page number left or right.  The PDF
# sometimes splits page-number digits with a stray space ("1 73" for 173)
# so we tolerate any sequence of digits-and-spaces in the page-number slot.
def strip_running_headers(text: str) -> str:
    lines = text.split("\n")
    out = []
    titles_set = {t for _, _, t in ES_TITLES}
    titles_set.update({
        "Asi habló Zaratustra", "Así habló Zaratustra",
        "Los discursos de Zaratustra",
        "Primera parte", "Segunda parte", "Tercera parte",
        "Cuarta parte", "Cuarta y última parte",
    })
    # Pre-normalise the titles_set for tolerant matching (ignore the
    # title-text rendering quirks like missing l → 1, missing accents, …)
    def squash(s: str) -> str:
        s = unicodedata.normalize("NFKD", s.lower()).encode("ascii","ignore").decode()
        s = re.sub(r"[^a-z]", "", s).replace("1","l").replace("j","l").replace("i","l")
        # OCR: 'rn' often renders as 'm', so collapse both to 'm' for matching
        s = s.replace("rn", "m")
        return s
    titles_squash = {squash(t) for t in titles_set}

    # Tolerate split digits: page numbers may render as "1 73" or "173"
    title_left_re  = re.compile(r"^\s*\d[\d\s]{0,4}\s{2,}(.+?)\s*$")
    title_right_re = re.compile(r"^(.+?)\s{2,}\d[\d\s]{0,4}\s*$")
    bare_num_re    = re.compile(r"^\s*\d[\d\s]{0,4}\s*$")

    for ln in lines:
        if bare_num_re.match(ln):
            continue
        m = title_left_re.match(ln) or title_right_re.match(ln)
        if m and squash(m.group(1)) in titles_squash:
            continue
        out.append(ln)
    return "\n".join(out)

import unicodedata

# Footnote markers appear as a digit (or digits) glued to the previous word.
# Examples in the PDF text:  "años2", "casa9", "ocaso5•", "luz4"
# We remove them.
def strip_footnote_markers(text: str) -> str:
    # PASS 0 — bullet/raised-dot characters (they often sit between a
    # footnote digit and the next sentence and would otherwise block the
    # Pass B/C lookaheads).
    text = re.sub(r"[•·]+", "", text)
    # PASS A — numbers stuck to a word OR closing punctuation (Sánchez
    # Pascual's 1-4 digit footnote markers): "años2", "mí!»333", "luz4".
    # NOTE: cluster excludes \w / digits so it can't accidentally swallow
    # part of the marker (e.g. "él»27" must not match as group1="l»2", group2="7").
    text = re.sub(
        r"([A-Za-záéíóúñüÁÉÍÓÚÑÜ][\.,;:!\?\)»«]{0,3})(\d{1,4})(?=[\s\.,;:!\?\)»«—\-]|$)",
        lambda m: m.group(1),
        text,
    )
    # PASS B — pdftotext sometimes splits the digits of a footnote marker
    # with stray spaces ("moral 1 1:" for "moral11:"). A second pass strips
    # a digit-and-spaces cluster between a word/punct end and the next
    # punctuation, capital, or line end. We consume trailing whitespace
    # together so the lookahead sees the punctuation / capital directly,
    # even when a newline sat between the digits and "¡".
    text = re.sub(
        r"(?<=[A-Za-záéíóúñüÁÉÍÓÚÑÜ\.!\?»\)\-—])\s+(\d(?:[\s\d]{0,4}\d)?[º°]?)\s*"
        r"(?=$|[\.,:;!\?»«—\-A-ZÁÉÍÓÚÑ¡¿“])",
        " ",
        text,
    )
    # PASS C — footnote ref between two lowercase words: "cuadrado 1 4 de"
    # → "cuadrado de". Nietzsche's prose in this edition has no genuine
    # numeric content other than SP's footnote markers, so it's safe to
    # strip any short digit cluster sitting alone between two letter runs.
    text = re.sub(
        r"(?<=[A-Za-záéíóúñüÁÉÍÓÚÑÜ])\s+\d(?:[\s\d]{0,4}\d)?\s+"
        r"(?=[A-Za-záéíóúñüÁÉÍÓÚÑÜ])",
        " ",
        text,
    )
    # Fix hyphenated line-wraps "es-\npíritu" -> "espíritu"
    text = re.sub(r"(\w+)­\n\s*(\w+)", r"\1\2", text)
    text = re.sub(r"(\w+)-\n\s*(\w+)", r"\1-\2", text)
    # Common OCR slips in the Sánchez Pascual scan
    text = re.sub(r"\bEcce\s+horno\b", "Ecce homo", text)
    # "1a", "1os" — leading '1' should be 'l' when followed by Spanish-looking word
    text = re.sub(r"(?<![\w])1(os|as|a|o)\b(?=\s+\w)", r"l\1", text)
    # "retomo" → "retorno" (only in known title contexts handled elsewhere; here
    # we leave alone to avoid harming legitimate "retomo" if it existed)
    # OCR: lowercase "i" at start of sentence after «  →  inverted bang/question
    # The Sánchez Pascual PDF often renders "¡" as "i" and "¿" as "i".
    # Detect:  «iWord  or  ! iWord  patterns → restore proper punctuation.
    text = re.sub(r"(«)i(?=[A-ZÁÉÍÓÚÑa-záéíóúñü])", r"\1¡", text)
    text = re.sub(r"([\.!?]\s+)i(?=[A-ZÁÉÍÓÚÑ])", r"\1¡", text)
    return text

ACCENT_MAP = {
    "á": "[aá]", "é": "[eé]", "í": "[ií]", "ó": "[oó]", "ú": "[uú]", "ñ": "[nñ]",
    "Á": "[AÁ]", "É": "[EÉ]", "Í": "[IÍ]", "Ó": "[OÓ]", "Ú": "[UÚ]", "Ñ": "[NÑ]",
}

def title_to_fuzzy_regex(title: str) -> re.Pattern:
    """Build a regex tolerant of pdftotext's quirks on this edition:
      • lowercase 'l' may render as '1' or be lost entirely
      • capital 'L' may render as '1'
      • 'rn' may merge to 'm' (retorno → retomo)
      • accents may be stripped (í → i)
      • angle quotes or other punctuation may surround a word
      • a column break inserts a stray space mid-word
      • a footnote marker (digits, optionally split) may follow the title
    """
    parts = []
    i = 0
    while i < len(title):
        ch = title[i]
        # rn → optional m substitution
        if ch == "r" and i+1 < len(title) and title[i+1] == "n":
            parts.append(r"(?:r\s*n|m)\s*")
            i += 2; continue
        if ch == "l":
            # pdftotext may render l as 1, I, J, or drop it entirely
            parts.append(r"[l1IJ]?\s*")
        elif ch == "L":
            parts.append(r"[L1IJ]\s*")
        elif ch == " ":
            parts.append(r"[\s«»\"'()]+")
        elif ch in ACCENT_MAP:
            parts.append(r"[«\"']*" + ACCENT_MAP[ch] + r"[»\"']*\s*")
        else:
            parts.append(re.escape(ch) + r"\s*")
        i += 1
    body = "".join(parts)
    # Trailing slop: footnote markers may use ° º · stray characters mixed
    # with digits (e.g. "5º1" for footnote 501).
    return re.compile(r"(?m)^[\s«]*" + body + r"\s*[\d°º·\s]{0,8}$", re.IGNORECASE)

def split_by_chapters(text: str) -> dict[tuple[int,int], str]:
    """Find each ES title's start position, return {(part,idx): chapter_body}."""
    out = {}
    positions = []
    for part, idx, title in ES_TITLES:
        pat = title_to_fuzzy_regex(title)
        m = pat.search(text)
        if not m:
            print(f"  ES MISS: ({part},{idx}) {title}")
            continue
        positions.append((m.start(), m.end(), part, idx, title))
    positions.sort()
    for i, (s, e, part, idx, title) in enumerate(positions):
        end = positions[i+1][0] if i+1 < len(positions) else len(text)
        body = text[e:end]
        out[(part, idx)] = body
    return out

def split_paragraphs(body: str) -> list[str]:
    """Split a chapter body into paragraphs.

    In Sánchez Pascual's edition (pdftotext output), a new paragraph starts
    with a line indented by 2 or more spaces, OR after a blank line.  Inside
    a paragraph the lines wrap at column ~65 with no leading indent.
    """
    # Drop standalone section number lines (subsection markers)
    body = re.sub(r"(?m)^\s*\d{1,2}\s*$", "", body)
    body = re.sub(r"(?m)^\s*Los discursos de Zaratustra\s*$", "", body)

    raw_lines = body.split("\n")
    paragraphs: list[list[str]] = []
    cur: list[str] = []
    def flush():
        if cur:
            paragraphs.append(cur[:])
            cur.clear()
    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        # New paragraph if:
        #   - line begins with 2+ spaces (the typical paragraph indent), OR
        #   - line begins with "—" / "-" / "«" (often paragraph start)
        leading_ws = len(line) - len(line.lstrip(" "))
        if cur and (leading_ws >= 2 or stripped.startswith(("—","-","«"))) and not _is_continuation(cur[-1]):
            flush()
        cur.append(stripped)
    flush()

    out = []
    for para_lines in paragraphs:
        p = " ".join(para_lines)
        p = re.sub(r"\s+", " ", p).strip()
        # Fix dropped-cap "T     res" → "Tres"
        p = re.sub(r"^([A-ZÁÉÍÓÚÑ])\s+(\w{1,10})\b", lambda m: m.group(1)+m.group(2), p)
        # Drop paragraphs that are just punctuation / orphan glyphs
        if not p or p in {"—", "-", "—-", "«"}: continue
        if len(p.strip(' .-—«»"\'')) < 3: continue
        out.append(p)

    # Second pass: rejoin page-break orphans. pdftotext leaves blank lines
    # where a running-header was stripped, which made the splitter break a
    # paragraph mid-sentence. Merge prev+next when prev ends WITHOUT
    # sentence-terminator and next starts lowercase / hyphen-prefixed.
    SENT_END = set(".!?»\":")
    LOWER = set("abcdefghijklmnñopqrstuvwxyzáéíóúüü")
    merged: list[str] = []
    for p in out:
        if merged:
            prev = merged[-1]
            prev_last = prev.rstrip().rstrip("-—")[-1:] if prev.rstrip() else ""
            next_first = p.lstrip()[:1]
            if (prev_last and prev_last not in SENT_END and prev_last in LOWER
                and (next_first in LOWER or p.lstrip().startswith(("«", "—", "-")))):
                merged[-1] = prev.rstrip() + " " + p.lstrip()
                continue
        merged.append(p)
    return merged

def _is_continuation(prev_line: str) -> bool:
    """Heuristic: previous line ends mid-sentence, so the next line is its
    continuation (we should NOT start a new paragraph)."""
    if not prev_line: return False
    last = prev_line.rstrip()[-1:]
    # If the previous line ended on . ! ? : or quote, this is likely a new
    # paragraph; otherwise (comma, dash, no punct, etc.) it's a continuation.
    return last not in {".", "!", "?", "»", '"', ":"}

def main():
    raw = load_book_text()
    print(f"book text region: {len(raw):,} chars")
    raw = strip_running_headers(raw)
    raw = strip_footnote_markers(raw)
    print(f"after cleanup: {len(raw):,} chars")

    by_chapter = split_by_chapters(raw)
    print(f"matched {len(by_chapter)}/{len(ES_TITLES)} chapter titles")

    # Backfill ES titles into chapter-nav.json so the live reader's
    # title-linking knows the Spanish chapter names.
    es_lookup = {(p, i): t for p, i, t in ES_TITLES}
    nav_path = SRC / "chapter-nav.json"
    nav = json.loads(nav_path.read_text(encoding="utf-8"))
    for e in nav:
        es = es_lookup.get((e["part"], e["idx"]))
        if es:
            e["es"] = es
    nav_path.write_text(json.dumps(nav, ensure_ascii=False, indent=2), encoding="utf-8")
    NAV[:] = nav  # update in-memory reference too

    # Patch each chapter .ptx with ES paragraphs
    patched = 0
    for nav_entry in NAV:
        part, idx = nav_entry["part"], nav_entry["idx"]
        es_body = by_chapter.get((part, idx))
        if not es_body:
            continue
        paras = split_paragraphs(es_body)
        target = SRC / nav_entry["file"]
        if not target.exists():
            # Vorrede is at source/ch_vorrede.ptx, not chapters/
            if nav_entry["xml_id"] == "ch-p0-00":
                # We won't touch ch_vorrede.ptx — it already has hand-tuned ES.
                continue
            print(f"  skip (no file): {target}")
            continue
        patch_es_into_ptx(target, paras, nav_entry["xml_id"])
        patched += 1
    print(f"patched {patched} chapter files with ES")

def patch_es_into_ptx(path: Path, es_paragraphs: list[str], xml_id: str):
    """Insert <p xml:id=…-es xml:lang='es'> entries into each <paragraphs>
    block, aligned by ordinal."""
    text = path.read_text(encoding="utf-8")
    # Find all <paragraphs> blocks (vNN)
    pblock_re = re.compile(
        r'(<paragraphs xml:id="' + re.escape(xml_id) + r'-v(\d+)">.*?)(</paragraphs>)',
        re.DOTALL
    )
    # Walk all paragraphs blocks, ordered
    blocks = list(pblock_re.finditer(text))
    if not blocks:
        return
    out_parts = []
    last_end = 0
    for i, m in enumerate(blocks):
        if i >= len(es_paragraphs):
            break
        out_parts.append(text[last_end:m.start()])
        block_start = m.group(1)
        block_close = m.group(3)
        v = m.group(2)
        es_para = xml_safe(es_paragraphs[i])
        # Only insert if there isn't already a -es <p> in this block
        if 'xml:lang="es"' in block_start:
            out_parts.append(block_start + block_close)
        else:
            insert = f'      <p xml:id="{xml_id}-v{v}-es" xml:lang="es">{es_para}</p>\n    '
            out_parts.append(block_start + insert + block_close)
        last_end = m.end()
    out_parts.append(text[last_end:])
    path.write_text("".join(out_parts), encoding="utf-8")

def xml_safe(s: str) -> str:
    # Preserve _word_ as <em>word</em>, then xml-escape rest
    s = re.sub(r"_([^_]+?)_", r"<em>\1</em>", s)
    s = s.replace("<em>", "\x01EM\x01").replace("</em>", "\x01/EM\x01")
    from xml.sax.saxutils import escape
    s = escape(s)
    s = s.replace("\x01EM\x01", "<em>").replace("\x01/EM\x01", "</em>")
    return s

if __name__ == "__main__":
    main()
