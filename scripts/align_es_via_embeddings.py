#!/usr/bin/env python3
"""
Embed every DE paragraph and every ES paragraph (per chapter) with LaBSE,
then run dynamic-programming alignment maximising cosine similarity under
a monotonicity constraint.  This produces a correct paragraph-to-paragraph
map between the German Urtext and Sánchez Pascual's Spanish, regardless of
PDF artifacts in either source.

Output: rewrites the ES <p xml:lang="es"> entries inside every ch_pX_YY*.ptx
so they line up with the correct DE verse number.
"""

from __future__ import annotations
import json, re, sys
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
import numpy as np

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
CH   = SRC / "chapters"
NAV  = json.loads((SRC / "chapter-nav.json").read_text(encoding="utf-8"))

sys.path.insert(0, str(PROJ / "scripts"))
from parse_spanish import (
    load_book_text, strip_running_headers, strip_footnote_markers,
    ES_TITLES, title_to_fuzzy_regex, split_paragraphs,
)

# ---------- 1. Get raw ES chapter bodies ---------------------------------
#
# Strategy: try regex-based chapter title detection first; for any chapter
# the regex misses, fall back to embedding-based localisation — embed the
# corresponding DE chapter's first paragraph (which we have reliably) and
# find the ES paragraph in the body whose embedding is the closest match.
# That paragraph becomes the chapter start.

def es_body_paragraphs() -> tuple[str, list[str], list[int]]:
    """Return (raw_text, [paragraphs], [offsets_in_raw])."""
    raw = load_book_text()
    raw = strip_running_headers(raw)
    raw = strip_footnote_markers(raw)
    raw = re.sub(r"(\w+)­\n\s*(\w+)", r"\1\2", raw)
    raw = re.sub(r"(\w+)-\n\s*(\w+)", r"\1-\2", raw)
    # Reuse split_paragraphs but we need the OFFSETS too — do the walk
    # ourselves so we can return them.
    raw2 = re.sub(r"(?m)^\s*\d{1,2}\s*$", "", raw)  # drop subsection markers
    raw2 = re.sub(r"(?m)^\s*Los discursos de Zaratustra\s*$", "", raw2)

    paragraphs: list[str] = []
    offsets: list[int] = []
    cur_lines = []
    cur_start = 0
    pos = 0
    in_para = False
    def flush():
        nonlocal cur_lines, cur_start, in_para
        if cur_lines:
            text = " ".join(cur_lines).strip()
            text = re.sub(r"\s+", " ", text)
            if text:
                paragraphs.append(text)
                offsets.append(cur_start)
        cur_lines = []
        in_para = False
    for line in raw2.split("\n"):
        line_len = len(line) + 1
        stripped = line.strip()
        if not stripped:
            flush()
            pos += line_len
            continue
        leading_ws = len(line) - len(line.lstrip(" "))
        if cur_lines and (leading_ws >= 2 or stripped.startswith(("—","-","«"))) and not _is_continuation(cur_lines[-1]):
            flush()
        if not cur_lines:
            cur_start = pos
        cur_lines.append(stripped)
        in_para = True
        pos += line_len
    flush()
    return raw2, paragraphs, offsets

def _is_continuation(prev: str) -> bool:
    return prev.rstrip()[-1:] not in {".","!","?","»",'"',":"}

def es_chapter_paragraphs(model) -> dict[str, list[str]]:
    raw, paragraphs, offsets = es_body_paragraphs()

    # 1. regex pass for chapters whose title we can detect
    positions: list[tuple[int,int,int]] = []   # (offset, part, idx)
    found_ids: set[str] = set()
    for part, idx, title in ES_TITLES:
        m = title_to_fuzzy_regex(title).search(raw)
        if m:
            positions.append((m.end(), part, idx))
            found_ids.add(f"ch-p{part}-{idx:02d}" if part > 0 else "ch-p0-00")

    # 2. embedding fallback for the missing ones
    missing = [(p,i,t) for p,i,t in ES_TITLES if (f"ch-p{p}-{i:02d}" if p>0 else "ch-p0-00") not in found_ids]
    if missing:
        print(f"  embedding-fallback for {len(missing)} chapter(s): {[t for _,_,t in missing]}")
        de_first_paras = {}
        for entry in NAV:
            path = SRC / entry["file"]
            if not path.exists(): continue
            t = path.read_text(encoding="utf-8")
            m = PARA_RE.search(t)
            if m:
                dm = DE_P_RE.search(m.group("body"))
                if dm:
                    de_first_paras[entry["xml_id"]] = re.sub(r"<[^>]+>", "", dm.group("txt")).strip()
        # Embed all body paragraphs once
        emb_body = model.encode(paragraphs, normalize_embeddings=True, batch_size=64, show_progress_bar=False)
        # Bounds: we don't want to match inside an already-located chapter,
        # but for simplicity we just find the global best and trust it.
        for part, idx, title in missing:
            xml_id = f"ch-p{part}-{idx:02d}" if part > 0 else "ch-p0-00"
            de_para = de_first_paras.get(xml_id)
            if not de_para:
                print(f"     no DE reference for {xml_id} — skip")
                continue
            q = model.encode([de_para], normalize_embeddings=True)[0]
            scores = emb_body @ q
            best = int(np.argmax(scores))
            print(f"     {xml_id} ({title}) → ES paragraph {best} ('{paragraphs[best][:60]}…') score={scores[best]:.3f}")
            positions.append((offsets[best], part, idx))

    positions.sort()
    out: dict[str, list[str]] = {}
    for i, (start, part, idx) in enumerate(positions):
        end = positions[i+1][0] if i+1 < len(positions) else len(raw)
        chunk = raw[start:end]
        xml_id = f"ch-p{part}-{idx:02d}"
        out[xml_id] = split_paragraphs(chunk)
    return out

# ---------- 2. Get DE paragraph text from each ch_*.ptx -------------------
PARA_RE = re.compile(
    r'<paragraphs xml:id="(?P<chap>[^"]+)-v(?P<v>\d+)">(?P<body>.*?)</paragraphs>',
    re.DOTALL
)
DE_P_RE = re.compile(
    r'<p[^>]*xml:lang="de"[^>]*>(?P<txt>.*?)</p>', re.DOTALL
)

def de_chapter_paragraphs() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for entry in NAV:
        path = SRC / entry["file"]
        if not path.exists(): continue
        text = path.read_text(encoding="utf-8")
        paras = []
        for m in PARA_RE.finditer(text):
            chap = m.group("chap")
            de_m = DE_P_RE.search(m.group("body"))
            de_text = re.sub(r"<[^>]+>", "", de_m.group("txt")).strip() if de_m else ""
            paras.append(de_text)
        out[entry["xml_id"]] = paras
    return out

# ---------- 3. Alignment --------------------------------------------------
def align(de: list[str], es: list[str], model) -> list[int|None]:
    """Return list of len(de): each item is the ES paragraph index (or None)
    matched to that DE paragraph. Monotonically non-decreasing.

    Many-to-one DP: a single ES paragraph can absorb 2 or 3 consecutive DE
    paragraphs (very common when Sánchez Pascual joins Nietzsche's bullet-
    style '—' fragments into one paragraph).  Conversely a single DE
    paragraph can be split across 2 ES.

    Transitions allowed at (i,j) representing 'aligned through de[:i] and
    es[:j]':
      • 1↔1  i-1,j-1  + sim(i-1,j-1)
      • 2↔1  i-2,j-1  + max(sim(i-2,j-1), sim(i-1,j-1)) - merge_bonus       (two DE → one ES)
      • 3↔1  i-3,j-1  + max(sim(i-3..i-1, j-1))         - 2*merge_bonus     (three DE → one ES)
      • 1↔2  i-1,j-2  + max(sim(i-1,j-2..j-1))          - merge_bonus       (one DE → two ES)
      • skip de  i-1,j  + SKIP
      • skip es  i,j-1  + SKIP
    """
    if not de or not es:
        return [None] * len(de)

    emb_de = model.encode(de, normalize_embeddings=True, batch_size=32, show_progress_bar=False)
    emb_es = model.encode(es, normalize_embeddings=True, batch_size=32, show_progress_bar=False)
    sim = emb_de @ emb_es.T

    n, m = sim.shape
    SKIP   = -0.15
    MERGE  = -0.02     # tiny penalty so 1:1 wins ties, but cheap to merge
    NEG = -1e9
    dp = np.full((n+1, m+1), NEG, dtype=np.float32)
    # back encoding:  (di, dj, assigned_es_index_for_each_de_in_block)
    back = [[None] * (m+1) for _ in range(n+1)]
    dp[0, 0] = 0.0
    for j in range(1, m+1):
        dp[0, j] = j * SKIP
        back[0][j] = (0, 1, [])
    for i in range(1, n+1):
        dp[i, 0] = i * SKIP
        back[i][0] = (1, 0, [None])

    for i in range(1, n+1):
        for j in range(1, m+1):
            # 1↔1
            best = dp[i-1, j-1] + sim[i-1, j-1]
            bk = (1, 1, [j-1])
            # 2↔1: merge de[i-2], de[i-1] → es[j-1]
            if i >= 2:
                cand = dp[i-2, j-1] + max(sim[i-2, j-1], sim[i-1, j-1]) + MERGE
                if cand > best: best, bk = cand, (2, 1, [j-1, j-1])
            # 3↔1
            if i >= 3:
                cand = dp[i-3, j-1] + max(sim[i-3, j-1], sim[i-2, j-1], sim[i-1, j-1]) + 2*MERGE
                if cand > best: best, bk = cand, (3, 1, [j-1, j-1, j-1])
            # 1↔2: de[i-1] mapped to two consecutive ES (rare but possible)
            if j >= 2:
                cand = dp[i-1, j-2] + max(sim[i-1, j-2], sim[i-1, j-1]) + MERGE
                if cand > best: best, bk = cand, (1, 2, [j-2])
            # skip DE
            cand = dp[i-1, j] + SKIP
            if cand > best: best, bk = cand, (1, 0, [None])
            # skip ES
            cand = dp[i, j-1] + SKIP
            if cand > best: best, bk = cand, (0, 1, [])
            dp[i, j] = best
            back[i][j] = bk

    # Backtrack
    result = [None] * n
    i, j = n, m
    while i > 0 or j > 0:
        bk = back[i][j]
        if bk is None: break
        di, dj, assigned = bk
        # assigned has length di; each entry is the ES index for the
        # corresponding DE paragraph in this transition.
        for k, es_idx in enumerate(assigned):
            de_idx = i - di + k
            if de_idx >= 0:
                result[de_idx] = es_idx
        i -= di; j -= dj
    return result

# ---------- 4. Patch ch_*.ptx with the corrected ES paragraphs ------------
def to_ptx_text(s: str) -> str:
    s = re.sub(r"_([^_]+?)_", r"<em>\1</em>", s)
    s = s.replace("<em>", "\x01EM\x01").replace("</em>", "\x01/EM\x01")
    s = xml_escape(s)
    s = s.replace("\x01EM\x01", "<em>").replace("\x01/EM\x01", "</em>")
    return s

def patch_chapter(entry, alignment: list[int|None], es_paras: list[str]):
    path = SRC / entry["file"]
    text = path.read_text(encoding="utf-8")
    xml_id = entry["xml_id"]

    # Dedupe: when the many-to-one DP assigns the SAME es_idx to N
    # consecutive DE paragraphs (a "Sánchez Pascual merged two German
    # bullets into one Spanish sentence" case), only the LAST DE verse
    # in the run carries the ES text. Earlier DE verses get None so the
    # Spanish doesn't visually duplicate across adjacent verses.
    dedup = list(alignment)
    for i in range(len(dedup) - 1):
        if dedup[i] is not None and dedup[i] == dedup[i + 1]:
            dedup[i] = None

    def patch_block(m):
        body = m.group(0)
        vm = re.match(r'<paragraphs xml:id="' + re.escape(xml_id) + r'-v(\d+)">', body)
        if not vm: return body
        v_idx = int(vm.group(1)) - 1
        es_idx = dedup[v_idx] if 0 <= v_idx < len(dedup) else None

        body = re.sub(r'      <p xml:id="[^"]+-es"[^>]*>.*?</p>\n', "", body, flags=re.DOTALL)

        if es_idx is not None:
            es_text = to_ptx_text(es_paras[es_idx])
            new_p = f'      <p xml:id="{xml_id}-v{v_idx+1:02d}-es" xml:lang="es">{es_text}</p>\n'
            body = body.replace("</paragraphs>", "    " + new_p + "    </paragraphs>")
        return body

    new_text = PARA_RE.sub(patch_block, text)
    path.write_text(new_text, encoding="utf-8")

# ---------- main ----------------------------------------------------------
def main():
    print("Loading model…")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/LaBSE")
    print("ok")

    print("Extracting ES chapter paragraphs…")
    es_by_ch = es_chapter_paragraphs(model)
    print("Extracting DE chapter paragraphs…")
    de_by_ch = de_chapter_paragraphs()

    common = set(es_by_ch) & set(de_by_ch)
    print(f"chapters in both: {len(common)}")

    stats = []
    for entry in NAV:
        xml_id = entry["xml_id"]
        if xml_id not in common: continue
        de = de_by_ch[xml_id]
        es = es_by_ch[xml_id]
        if not de or not es:
            continue
        align_map = align(de, es, model)
        matched = sum(1 for a in align_map if a is not None)
        stats.append((xml_id, len(de), len(es), matched))
        # Patch chapter file
        patch_chapter(entry, align_map, es)
        print(f"  {xml_id}: DE={len(de):3} ES={len(es):3} matched={matched:3} ({matched/len(de):.0%})")

    print("\n=== summary ===")
    print(f"chapters processed: {len(stats)}")
    avg_coverage = np.mean([m / d for _, d, _, m in stats]) if stats else 0
    print(f"avg DE→ES coverage: {avg_coverage:.1%}")

if __name__ == "__main__":
    main()
