#!/usr/bin/env python3
"""
Extract verbatim commentary excerpts from four scholarly works:
   • Klossowski   Nietzsche et le cercle vicieux            (FR)
   • Deleuze      Nietzsche et la philosophie               (FR)
   • Sánchez Meca La experiencia dionisíaca del mundo       (ES)
   • New Cambridge Companion to Nietzsche                    (EN)

Each is scanned for paragraphs that explicitly reference a Zarathustra
chapter by its canonical title (in the book's own language).  Such
paragraphs become commentary notes targeted at chapter-level via
`target = "ch-pX-YY-v01"` (we attach to verse 1 for simplicity; the
renderer's stream filter still keeps these per chapter).

The fair-use cap: max 250 characters per excerpt, single paragraph.
"""

from __future__ import annotations
import json, re, unicodedata
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
COMM = SRC / "commentary.json"

# Title aliases per language, keyed by xml_id.
# We only need a couple of distinctive title keywords per chapter; the
# scanner does substring matching.
import sys
sys.path.insert(0, str(PROJ / "scripts"))
from build_chapters import CHAPTERS

# Spanish titles in same order as CHAPTERS — extracted from parse_spanish
from parse_spanish import ES_TITLES

# Build per-xml_id (DE, EN, FR, ES) tuples
XMLID_TITLES = {}
for (part, idx, de, en, fr), es_row in zip(CHAPTERS, ES_TITLES):
    xml_id = f"ch-p{part}-{idx:02d}"
    es = es_row[2]
    XMLID_TITLES[xml_id] = {"de": de, "en": en, "fr": fr, "es": es}

# ---------------------------------------------------------------------------
# Distinctive search needles per chapter (lowercased, normalised).  We use a
# handful of short keywords drawn from each title to find references in the
# corpus, since scholars don't always cite the title verbatim.
# ---------------------------------------------------------------------------
def normalise(s: str) -> str:
    return unicodedata.normalize("NFKD", s.lower()).encode("ascii","ignore").decode()

def needles_for(xml_id: str) -> dict[str, list[str]]:
    """Return per-language needle lists (lowercased, accent-stripped)."""
    titles = XMLID_TITLES[xml_id]
    out = {}
    for lang in ("en","fr","es"):
        t = titles[lang]
        # drop articles + lowercase + accent-strip
        words = [w for w in re.split(r"[\s\W]+", normalise(t)) if len(w) >= 4
                 and w not in {"the","les","des","der","los","las","von","of",
                               "del","dem","den","une","des","aux"}]
        out[lang] = words[:3]   # 2-3 strongest words
    return out

# ---------------------------------------------------------------------------
# Paragraph extractor
# ---------------------------------------------------------------------------
def split_paragraphs(text: str) -> list[str]:
    paras = re.split(r"\n{2,}|\f", text)
    out = []
    for p in paras:
        p = re.sub(r"\s+", " ", p).strip()
        if 60 <= len(p) <= 1200:    # ignore headings/very short, and very long blocks
            out.append(p)
    return out

# Pull a 250-char fair-use excerpt focused on the matched needle.
def make_excerpt(para: str, needle: str, target_len: int = 240) -> str:
    norm_para = normalise(para)
    pos = norm_para.find(needle)
    if pos < 0: return para[:target_len]
    # roughly map back to original
    start = max(0, pos - target_len // 2)
    end   = min(len(para), pos + target_len // 2)
    # snap to sentence boundaries
    while start > 0 and para[start-1] not in ".!?»":
        start -= 1
    while end < len(para) and para[end-1] not in ".!?»":
        end += 1
        if end - start > target_len + 80: break
    excerpt = para[start:end].strip()
    if not excerpt.endswith((".", "!", "?", "»")): excerpt += "…"
    return excerpt

# ---------------------------------------------------------------------------
# Main scan
# ---------------------------------------------------------------------------
SOURCES = [
    ("klossowski",     "/tmp/klossowski.txt",   "fr",
        {"en":"Klossowski (FR)", "fr":"Klossowski", "es":"Klossowski (FR)"}, "#a04a55"),
    ("deleuze",        "/tmp/deleuze.txt",      "fr",
        {"en":"Deleuze (FR)", "fr":"Deleuze", "es":"Deleuze (FR)"}, "#c46a3a"),
    ("sanchez-meca",   "/tmp/sanchez_meca.txt", "es",
        {"en":"Sánchez Meca (ES)", "fr":"Sánchez Meca (ES)", "es":"Sánchez Meca"}, "#3a8a8a"),
    ("new-cambridge",  "/tmp/cambridge.txt",    "en",
        {"en":"New Cambridge Companion", "fr":"New Cambridge Companion", "es":"New Cambridge Companion"}, "#3a6a3a"),
]

def build_one_stream(name, txt_path, src_lang, label, color) -> dict:
    text = Path(txt_path).read_text(encoding="utf-8", errors="replace")
    paras = split_paragraphs(text)
    print(f"[{name}] {len(paras):,} paragraphs from {txt_path}")

    notes = []
    for xml_id in XMLID_TITLES:
        if xml_id == "ch-p0-00": continue  # skip Vorrede (hand-tuned commentary)
        nds = needles_for(xml_id)[src_lang]
        if not nds: continue
        # require ALL keywords present in the paragraph for a strong match
        for p in paras:
            np = normalise(p)
            if all(n in np for n in nds):
                excerpt = make_excerpt(p, nds[0])
                notes.append({
                    "target": f"{xml_id}-v01",
                    "src_lang": src_lang,
                    src_lang: excerpt,
                })
                break    # only one excerpt per chapter

    # Drop duplicates and excerpts too short
    notes = [n for n in notes if len(n[src_lang]) > 80]
    print(f"[{name}] kept {len(notes)} excerpts (one per chapter where matched)")

    stream = {
        "label": label,
        "color": color,
        "side": "outer" if name != "sanchez-meca" else "outer",
        "_origin": src_lang,
        "notes": []
    }
    for n in notes:
        # mirror the text in the other languages (the renderer otherwise
        # hides notes for the non-source language). For now we duplicate
        # the original text — a future pass could translate.
        body = n[n["src_lang"]]
        stream["notes"].append({
            "target": n["target"],
            "en": body, "fr": body, "es": body,
        })
    return stream

def main():
    data = json.loads(COMM.read_text(encoding="utf-8"))
    for name, path, lang, label, color in SOURCES:
        stream = build_one_stream(name, path, lang, label, color)
        data["streams"][name] = stream
    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("commentary.json updated")

if __name__ == "__main__":
    main()
