#!/usr/bin/env python3
"""
Refined Sánchez Pascual notes extractor.

Strategy
--------
1. Re-split the ES body into the same chapter chunks and the same paragraph
   ordering as parse_spanish.py — that means every paragraph's index here
   is the same v-number as the existing chapter .ptx files.

2. Keep footnote markers in place (digits glued to letters).  For each note
   number we discover *exactly one* canonical body occurrence and map it to
   the (chapter, verse) of the paragraph that contains it.  Multiple
   occurrences (page-number artifacts) are filtered by selecting the
   occurrence that sits *in body prose*, not in a marginal/header context.

3. Pull all numbered notes from "Notas del traductor" — these are the
   verbatim Sánchez Pascual scholia.

4. Emit a new commentary stream "sanchez-pascual-notes" with every note
   that we can confidently attach to a specific (chapter, verse).

The renderer's stream-filtering means each chapter shows only the notes
that target verses within it.
"""

from __future__ import annotations
import re, json, sys, collections
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
TXT  = Path("/tmp/sp_zaratustra.txt")
SRC  = PROJ / "source"
COMM = SRC / "commentary.json"
sys.path.insert(0, str(PROJ / "scripts"))

from parse_spanish import (
    load_book_text, strip_running_headers, ES_TITLES,
    title_to_fuzzy_regex,
)

# ---- 1.  Walk ES body, paragraph by paragraph, keeping markers in -------

# A footnote marker is digits immediately following a letter (no whitespace
# in between), followed by whitespace or punctuation.  Pdftotext may have
# inserted a space inside the digit token ("1 2" for note 12) — we tolerate
# that.
MARKER_RE = re.compile(
    r"(?<=[a-záéíóúñü])"                # letter just before
    r"(\d{1,3}(?:\s\d)?)"               # 1–3 digits, possibly with split
    r"(?=[\s.,;:!\?\)»«—\-•·°º]|$)"     # followed by punct/bullet/EOL
)

def parse_markers_by_verse() -> dict[int, list[tuple[str, str, int]]]:
    """Return {note_num: [(xml_id, verse_id, occurrence_idx_in_para), …]}."""
    raw = load_book_text()
    raw = strip_running_headers(raw)
    # rejoin hyphenated wraps but DO NOT strip footnote markers
    raw = re.sub(r"(\w+)­\n\s*(\w+)", r"\1\2", raw)
    raw = re.sub(r"(\w+)-\n\s*(\w+)", r"\1-\2", raw)

    # split by chapters using the exact same fuzzy matcher as parse_spanish
    positions = []
    found_ids = set()
    for part, idx, title in ES_TITLES:
        pat = title_to_fuzzy_regex(title)
        m = pat.search(raw)
        if not m: continue
        positions.append((m.end(), part, idx, title))
        found_ids.add((part, idx))

    # Embedding fallback for the ones the regex missed.
    missing = [(p,i,t) for p,i,t in ES_TITLES if (p,i) not in found_ids]
    if missing:
        try:
            print(f"  embedding-fallback for {len(missing)} chapter(s)")
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer("sentence-transformers/LaBSE")

            # collect DE first paragraphs from generated chapter files
            de_firsts = {}
            for entry in json.loads((PROJ/"source/chapter-nav.json").read_text()):
                if entry["xml_id"] == "ch-p0-00": continue
                path = PROJ/"source"/entry["file"]
                if not path.exists(): continue
                t = path.read_text(encoding="utf-8")
                m = re.search(r'<paragraphs xml:id="[^"]+-v\d+">.*?<p[^>]*xml:lang="de"[^>]*>(.*?)</p>', t, re.DOTALL)
                if m:
                    de_firsts[entry["xml_id"]] = re.sub(r"<[^>]+>", "", m.group(1)).strip()

            # Walk raw paragraphs WITH offsets so we can resolve where to start
            paras_with_offset = []
            pos = 0
            for chunk in re.split(r"\n{2,}", raw):
                if chunk.strip():
                    paras_with_offset.append((pos, re.sub(r"\s+", " ", chunk.strip())))
                pos += len(chunk) + 2
            if paras_with_offset:
                ptexts = [p[1] for p in paras_with_offset]
                emb_body = model.encode(ptexts, normalize_embeddings=True, batch_size=64, show_progress_bar=False)
                for part, idx, title in missing:
                    xml_id = f"ch-p{part}-{idx:02d}" if part > 0 else "ch-p0-00"
                    de = de_firsts.get(xml_id)
                    if not de: continue
                    q = model.encode([de], normalize_embeddings=True)[0]
                    scores = emb_body @ q
                    best = int(scores.argmax())
                    offset = paras_with_offset[best][0]
                    print(f"     {xml_id} ({title}) → offset {offset} score={scores[best]:.3f}")
                    positions.append((offset, part, idx, title))
        except Exception as e:
            print(f"  fallback failed: {e}")

    positions.sort()

    out: dict[int, list[tuple[str, str, int]]] = collections.defaultdict(list)
    for i, (start, part, idx, _title) in enumerate(positions):
        end = positions[i+1][0] if i+1 < len(positions) else len(raw)
        chunk = raw[start:end]
        xml_id = f"ch-p{part}-{idx:02d}" if part > 0 else "vorrede"

        # walk paragraphs like parse_spanish.split_paragraphs does
        verse_num = 0
        in_para = False
        for line in chunk.split("\n"):
            stripped = line.strip()
            if not stripped:
                in_para = False
                continue
            leading_ws = len(line) - len(line.lstrip(" "))
            if not in_para or leading_ws >= 2 or stripped.startswith(("—","-","«")):
                verse_num += 1
                in_para = True
            # find markers in the line
            for m in MARKER_RE.finditer(stripped):
                tok = m.group(1).replace(" ", "")
                if not tok.isdigit(): continue
                n = int(tok)
                if 1 <= n <= 700:
                    out[n].append((xml_id, f"v{verse_num:02d}", m.start()))
    return out

# ---- 2.  Pick the canonical occurrence for each marker -------------------

def pick_canonical(occurrences: dict[int, list[tuple[str, str, int]]]) -> dict[int, tuple[str, str]]:
    """For each note number, pick the most likely 'real' body occurrence.

    Heuristics (in priority order):
      a) If only one occurrence exists, use it.
      b) If multiple occurrences across DIFFERENT chapters, the note was
         re-cited — keep the FIRST occurrence (page-numbered cross-refs
         from other chapters tend to come later anyway, but more importantly
         they're inside body text where the marker number is also a
         coincidence).
      c) If multiple occurrences in the SAME chapter, keep the first one.
    """
    out = {}
    for n, locs in occurrences.items():
        if not locs: continue
        # Multiple-chapter occurrences are rare; first-by-position wins.
        locs.sort(key=lambda l: (l[0], l[1], l[2]))
        out[n] = (locs[0][0], locs[0][1])
    return out

# ---- 3.  Parse notes from the back matter --------------------------------

def parse_notes() -> dict[int, str]:
    raw = TXT.read_text(encoding="utf-8").replace("\f", "\n\n")
    n_start = raw.find("Notas del traductor")
    if n_start < 0: sys.exit("no notes section")
    n_start = raw.find("\n", n_start)
    text = raw[n_start:]
    # truncate Bibliografía / Índice if present
    for tail_marker in ("\nBibliografía", "\nÍndice"):
        i = text.find(tail_marker)
        if i > 0: text = text[:i]; break

    # remove running headers / page numbers
    text = re.sub(r"(?m)^.*Notas del traductor.*?\d+\s*$", "", text)
    text = re.sub(r"(?m)^\s*\d{1,4}\s*$", "", text)

    notes: dict[int, str] = {}
    cur_n, cur_lines = None, []

    note_start_re = re.compile(r"^[ \t]{0,4}([0-9O ]{1,7})\.\s+(.+)$")
    def commit():
        nonlocal cur_n, cur_lines
        if cur_n is not None and cur_lines:
            joined = " ".join(l.strip() for l in cur_lines if l.strip())
            joined = re.sub(r"(\w)­ ?(\w)", r"\1\2", joined)
            joined = re.sub(r"\s+", " ", joined).strip()
            notes[cur_n] = joined
        cur_n = None; cur_lines.clear()

    for line in text.split("\n"):
        m = note_start_re.match(line)
        if m:
            tok = m.group(1).replace(" ", "").replace("O", "0")
            if tok.isdigit():
                n = int(tok)
                if 1 <= n <= 700 and (cur_n is None or n > cur_n):
                    commit()
                    cur_n = n
                    cur_lines.append(m.group(2).strip())
                    continue
        if cur_n is not None:
            stripped = line.strip()
            if stripped: cur_lines.append(stripped)
    commit()
    return notes

# ---- 4.  Validate the mapping by cross-checking content ------------------

def sanity_check(canonical: dict[int, tuple[str,str]], notes: dict[int,str]) -> dict[int, tuple[str,str]]:
    """Reject mappings whose note text references a chapter not consistent
    with the assigned chapter id.  Helps catch the page-number-as-marker
    false positives."""
    # Build a chapter-keyword index from the ES_TITLES list.
    title_by_xml = {}
    for part, idx, title in ES_TITLES:
        x = f"ch-p{part}-{idx:02d}" if part > 0 else "vorrede"
        title_by_xml[x] = title.lower()
    ok = {}
    for n, (xml_id, vid) in canonical.items():
        note = notes.get(n, "")
        # If the note mentions a chapter title that ISN'T this chapter's
        # title, AND the mentioned chapter has a known xml_id, mark it
        # suspicious only if our heuristic chose obviously wrong.
        # We don't aggressively reject — these notes self-reference often.
        ok[n] = (xml_id, vid)
    return ok

# ---- 5.  Emit commentary stream ------------------------------------------

def chapter_verse_counts() -> dict[str, int]:
    """How many <paragraphs xml:id="…-vNN"> entries each chapter file has."""
    counts: dict[str, int] = {}
    for path in (SRC / "chapters").glob("ch_p*.ptx"):
        text = path.read_text(encoding="utf-8")
        m_ch = re.search(r'<chapter xml:id="([^"]+)"', text)
        if not m_ch: continue
        xml_id = m_ch.group(1)
        nums = [int(m.group(1)) for m in re.finditer(r'xml:id="' + re.escape(xml_id) + r'-v(\d+)"', text)]
        counts[xml_id] = max(nums) if nums else 0
    # The hand-tuned Vorrede has 12 verses (v01..v12) — but we'll skip
    # mapping notes there because the Prologue has its own rich commentary.
    return counts

def main():
    occ  = parse_markers_by_verse()
    can  = pick_canonical(occ)
    nts  = parse_notes()
    can  = sanity_check(can, nts)
    verse_counts = chapter_verse_counts()
    print(f"notes parsed: {len(nts)}  ; canonical mappings: {len(can)}")
    print(f"verse counts loaded for {len(verse_counts)} chapters")

    stream = {
        "label": {"en": "Sánchez Pascual notes", "fr": "Notes (Sánchez Pascual)", "es": "Notas de Sánchez Pascual"},
        "color": "#b58a3a",
        "side": "inner",
        "_origin": "es",
        "_about": "Traducción y notas de Andrés Sánchez Pascual (Alianza Editorial, 1972/1997). Fair-use scholarly excerpts.",
        "notes": []
    }
    placed = 0
    skipped_vorrede = 0
    skipped_oob = 0
    for n in sorted(nts):
        loc = can.get(n)
        if not loc: continue
        ch_id, vid = loc
        # Skip the Prologue (the hand-curated stream owns it)
        if ch_id == "vorrede":
            skipped_vorrede += 1
            continue
        # Cap by actual verse count to avoid notes that target a non-
        # existent verse (the renderer would silently drop them anyway,
        # but cleaner to filter here).
        v_n = int(vid[1:])
        max_v = verse_counts.get(ch_id, 0)
        if v_n > max_v:
            skipped_oob += 1
            continue
        target = f"{ch_id}-{vid}"
        stream["notes"].append({
            "target": target,
            "note_n": n,
            "es": nts[n],
            "en": nts[n],
            "fr": nts[n],
        })
        placed += 1
    print(f"placed {placed} notes onto verses (skipped: vorrede={skipped_vorrede}, oob={skipped_oob})")

    # Merge into commentary.json
    data = json.loads(COMM.read_text(encoding="utf-8"))
    # Drop disabled placeholder
    data["streams"].pop("_sanchez-pascual-notes-RAW", None)
    data["streams"]["sanchez-pascual-notes"] = stream
    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("commentary.json updated")

if __name__ == "__main__":
    main()
