#!/usr/bin/env python3
"""
Schema-validate source/commentary.json.

Catches the regressions that nearly shipped:
  • notes with same text duplicated across all three languages
    (a translation never happened)
  • target ids that don't exist in any chapter .ptx
  • streams referencing colors / sides that the renderer can't display
  • notes missing the mother-tongue field they claim to support
"""

from __future__ import annotations
import json, re, sys
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC  = PROJ / "source"
COMM = SRC / "commentary.json"
NAV  = json.loads((SRC / "chapter-nav.json").read_text(encoding="utf-8"))

VALID_SIDES = {"inner", "outer", "bottom"}
LANGS = ("en", "fr", "es")
COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

def collect_valid_targets() -> set[str]:
    out: set[str] = set()
    # Auto chapters
    for e in NAV:
        if e["xml_id"] == "ch-p0-00":
            # Vorrede uses bare v01..v12
            for i in range(1, 13):
                out.add(f"v{i:02d}")
            continue
        path = SRC / e["file"]
        if not path.exists(): continue
        for m in re.finditer(r'<paragraphs xml:id="([^"]+)">', path.read_text(encoding="utf-8")):
            out.add(m.group(1))
    return out

def main():
    data = json.loads(COMM.read_text(encoding="utf-8"))
    streams = data.get("streams", {})
    valid_targets = collect_valid_targets()

    errors: list[str] = []
    warnings: list[str] = []

    for name, s in streams.items():
        if name.startswith("_"): continue
        # Required structural fields
        for k in ("label", "color", "side", "notes"):
            if k not in s:
                errors.append(f"[{name}] missing required field '{k}'")
        if s.get("side") not in VALID_SIDES:
            errors.append(f"[{name}] invalid side {s.get('side')!r} (expected one of {VALID_SIDES})")
        if not COLOR_RE.match(s.get("color", "")):
            errors.append(f"[{name}] invalid color {s.get('color')!r}")
        label = s.get("label", {})
        for lang in LANGS:
            if not label.get(lang):
                warnings.append(f"[{name}] label.{lang} missing")

        notes = s.get("notes", [])
        same_text_count = 0
        for i, n in enumerate(notes):
            if "target" not in n:
                errors.append(f"[{name}][{i}] missing target")
                continue
            if n["target"] not in valid_targets:
                errors.append(f"[{name}][{i}] target {n['target']!r} does not match any chapter verse")
            # At least one language must be populated
            populated = [lang for lang in LANGS if n.get(lang)]
            if not populated:
                errors.append(f"[{name}][{i}] no language fields populated")
            # Translation duplication check: if all three fields are equal
            if len(populated) == 3 and len({n[lang] for lang in LANGS}) == 1:
                same_text_count += 1
        if same_text_count:
            warnings.append(f"[{name}] {same_text_count}/{len(notes)} notes are untranslated (en==fr==es)")

    if warnings:
        print("WARNINGS:")
        for w in warnings: print(" ", w)
    if errors:
        print("\nERRORS:")
        for e in errors: print(" ", e)
        sys.exit(1)
    print(f"\nOK — {sum(len(s.get('notes',[])) for s in streams.values())} notes across {len(streams)} streams validated.")

if __name__ == "__main__":
    main()
