#!/usr/bin/env python3
"""
Editorial cleanup pass:

1. DEDUPE — for every stream, when the same paragraph text appears on
   multiple verses, keep only the single best-scoring placement and drop
   the rest. Same scholarly paragraph being attached to 18 different
   verses (as we saw with one Sánchez Meca quote) is noise, not signal.

2. CLEAN — surgical fixes to known artifacts in note bodies:
     • "Ecce horno"   → "Ecce homo"   (OCR fix)
     • soft hyphens   → joined word   (\\u00ad followed by whitespace)
     • leftover "ed. cit." citations   → stripped
     • "edición citada, p. NNN"        → stripped
     • duplicate spaces / space-before-comma → tidied
     • broken-word OCR mash "i,i ,1c" → drop the note (it's garbage)

3. DROP — any note whose body is now < 30 chars or contains only
   section-header tokens (e.g. "DEUXIÈME PARTIE. TRANSFORMER L'EUROPE…").
"""

from __future__ import annotations
import json, re
from collections import defaultdict
from pathlib import Path

COMM = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt/source/commentary.json")

OCR_FIXES = [
    (re.compile(r"\bEcce\s+horno\b"),               "Ecce homo"),
    (re.compile(r"\bretomo\b(?=\s+(eterno|del|al|a))"), "retorno"),
    (re.compile(r"\b1os\b"),                         "los"),
    (re.compile(r"\b1as\b"),                         "las"),
    (re.compile(r"\b1a\b(?=\s+[a-záéíóú])"),         "la"),
]

# Patterns to strip outright (cited as cruft, irrelevant on this medium)
STRIP = [
    re.compile(r"\s*\(edición citada[^)]*\)\s*"),
    re.compile(r"\s*,?\s*ed\.\s+cit\.[, .]*"),
    re.compile(r"\s*,?\s*éd\.\s+cit\.[, .]*"),
    re.compile(r"\s*,?\s*\bpp?\.\s*\d{1,4}(?:[\-–—]\d{1,4})?(\s*y\s*ss?\.?)?\b"),
    re.compile(r"[­ ]"),  # soft hyphen + nbsp residue
    re.compile(r"\s{3,}"),
]

# Detector for garbage notes — drop them
GARBAGE_PATTERNS = [
    re.compile(r"i,i\s*,1c"),                # the famous OCR mash
    re.compile(r"\bDEUXIÈME PARTIE\b"),       # section heading in middle of note
    re.compile(r"\bPRIMERA PARTE\b"),
    re.compile(r"^\W*\d+\W*$"),               # all-number/punct
]

def clean(text: str) -> str:
    if not text: return text
    for pat, repl in OCR_FIXES:
        text = pat.sub(repl, text)
    for pat in STRIP:
        text = pat.sub(" ", text)
    # tidy whitespace + space-before-punct
    text = re.sub(r"\s+([,;:\.])", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def is_garbage(text: str) -> bool:
    if not text or len(text) < 30: return True
    for pat in GARBAGE_PATTERNS:
        if pat.search(text):
            return True
    return False

def main():
    data = json.loads(COMM.read_text(encoding="utf-8"))

    n_cleaned = 0
    n_garbage = 0
    n_dedup   = 0

    for sname, stream in data["streams"].items():
        if sname.startswith("_"): continue
        notes = stream.get("notes", [])

        # 1. Clean every field + flag garbage
        keep = []
        for n in notes:
            for L in ("en", "fr", "es"):
                before = n.get(L) or ""
                after  = clean(before)
                if before != after:
                    n_cleaned += 1
                    n[L] = after
            # if the post-clean origin-language body is garbage, drop
            origin = stream.get("_origin", "en")
            if is_garbage(n.get(origin) or n.get("en") or ""):
                n_garbage += 1
                continue
            keep.append(n)
        notes = keep

        # 2. Dedupe by text (per stream): keep the best-scoring instance.
        # 'best' = highest score; tie-break by NOT being audit-flagged weak.
        groups = defaultdict(list)
        for i, n in enumerate(notes):
            key = (n.get("en") or n.get("fr") or n.get("es") or "")[:200].lower()
            if key:
                groups[key].append(i)
        drop_idxs = set()
        for key, idxs in groups.items():
            if len(idxs) < 2: continue
            # rank
            def rank(i):
                n = notes[i]
                return (
                    0 if n.get("_audit_flag") == "weak" else 1,  # higher = better
                    n.get("score", 0) or 0,
                )
            best_i = max(idxs, key=rank)
            for i in idxs:
                if i != best_i:
                    drop_idxs.add(i)
                    n_dedup += 1
        notes = [n for i, n in enumerate(notes) if i not in drop_idxs]

        stream["notes"] = notes

    print(f"text fields cleaned:    {n_cleaned}")
    print(f"garbage notes dropped:  {n_garbage}")
    print(f"duplicate notes dropped:{n_dedup}")

    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(s.get("notes",[])) for s in data["streams"].values())
    print(f"commentary.json now has {total} notes")

if __name__ == "__main__":
    main()
