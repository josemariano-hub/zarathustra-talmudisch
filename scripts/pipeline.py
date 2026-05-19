#!/usr/bin/env python3
"""
The pipeline. The ONE pipeline. Stop running scripts out of order.

Every step is idempotent. Every step that mutates commentary.json is
followed by apply_streams_config.py so stream metadata never drifts.

Run a subset:
    python pipeline.py                # everything from clean rebuild
    python pipeline.py --from audit   # resume after audit
    python pipeline.py --only deploy  # deploy only
    python pipeline.py --skip llm     # skip steps that hit the LLM
    python pipeline.py --dry          # show plan without executing
"""
from __future__ import annotations
import argparse, os, subprocess, sys, time
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SCRIPTS = PROJ / "scripts"

# (tag, description, command, hits_llm)
STEPS = [
    ("build-chapters",    "Build chapter PTX from raw sources",
        ["python3", "scripts/build_chapters.py"],                       False),
    ("parse-spanish",     "Parse Spanish source into chapter ES",
        ["python3", "scripts/parse_spanish.py"],                        False),
    ("fix-segmentation",  "Re-segment ch-p3-15 bells + ch-p4-19 reprise",
        ["python3", "scripts/fix_segmentation.py"],                     False),
    ("normalize-typography","Normalize stray ASCII quotes in DE/EN paragraphs",
        ["python3", "scripts/normalize_typography.py"],                 False),
    ("align-fr",          "LaBSE-DP align FR paragraphs to DE",
        ["python3", "scripts/align_fr_via_embeddings.py", "fr"],        False),
    ("align-en",          "LaBSE-DP align EN paragraphs to DE",
        ["python3", "scripts/align_fr_via_embeddings.py", "en"],        False),
    ("align-es",          "LaBSE-DP align ES paragraphs to DE",
        ["python3", "scripts/align_es_via_embeddings.py"],              False),
    ("parse-es-notes",    "Parse SP footnote markers from chapter ES",
        ["python3", "scripts/parse_es_notes.py"],                       False),
    ("fix-es-attr",       "Fix sanchez-pascual-notes attribution",
        ["python3", "scripts/fix_es_notes_attribution.py"],             False),
    ("retrieve",          "RAG-retrieve commentary from corpora",
        ["python3", "scripts/retrieve_commentary.py"],                  False),
    ("apply-streams-1",   "Re-apply streams.config.json (post-retrieve)",
        ["python3", "scripts/apply_streams_config.py"],                 False),
    ("translate-1",       "Translate RAG notes into all languages",
        ["python3", "scripts/translate_commentary.py"],                 True),
    ("dedupe-1",          "Dedupe + clean (post-translate)",
        ["python3", "scripts/dedupe_and_clean.py"],                     False),
    ("post-audit-cleanup","Targeted text cleanups (soft-hyphen, OCR, …)",
        ["python3", "scripts/post_audit_cleanup.py"],                   False),
    ("audit-llm",         "LLM audit every (verse, note) pair",
        ["python3", "scripts/audit_notes_with_llm.py"],                 True),
    ("drop-audit-zero",   "Drop notes with audit score 0",
        ["python3", "scripts/drop_audit_zero.py"],                      False),
    ("apply-streams-2",   "Re-apply streams.config.json (post-drop)",
        ["python3", "scripts/apply_streams_config.py"],                 False),
    ("refill",            "Refill missing sides (LLM-gated)",
        ["python3", "scripts/refill_missing_sides.py"],                 True),
    ("multilang-reassign","Multi-language reassign notes to best verse",
        ["python3", "scripts/multilang_reassign.py"],                   False),
    ("cull-weak",         "Drop weak-flagged notes from sanchez-meca",
        ["python3", "scripts/cull_weak_in_stream.py", "sanchez-meca"],  False),
    ("cull-damaged",      "Drop OCR-damaged + truncated notes",
        ["python3", "scripts/cull_damaged_notes.py"],                   False),
    ("normalize-citations","Canonical biblical refs, §1 disambiguation, KJV Mt 26:40",
        ["python3", "scripts/normalize_citations.py"],                  False),
    ("translate-2",       "Translate any newly-placed notes",
        ["python3", "scripts/translate_commentary.py"],                 True),
    ("dedupe-2",          "Final dedupe + clean",
        ["python3", "scripts/dedupe_and_clean.py"],                     False),
    ("apply-streams-3",   "Re-apply streams.config.json (final)",
        ["python3", "scripts/apply_streams_config.py"],                 False),
    ("validate",          "Schema-validate commentary.json",
        ["python3", "scripts/validate_commentary.py"],                  False),
    ("snapshot",          "Verify file hashes vs golden snapshot",
        ["python3", "scripts/snapshot.py"],                             False),
    ("alignment-export",  "Build alignment.json for search index + API",
        ["python3", "scripts/build_alignment_export.py"],               False),
    ("deploy",            "Copy to deploy/ and push to Netlify",
        ["bash", "-c", "scripts/deploy.sh || echo '(no deploy.sh — skipped)'"],
        False),
]

def run_step(tag: str, desc: str, cmd: list, dry: bool) -> tuple[bool, float]:
    bar = "─" * 72
    print(f"\n{bar}\n▶ [{tag}]  {desc}\n  $ {' '.join(cmd)}\n{bar}", flush=True)
    if dry:
        return True, 0.0
    t0 = time.time()
    r = subprocess.run(cmd, cwd=str(PROJ))
    return (r.returncode == 0), (time.time() - t0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from",  dest="from_tag",  help="resume from this step")
    ap.add_argument("--until", dest="until_tag", help="stop after this step")
    ap.add_argument("--only",  dest="only_tag",  help="run only this step")
    ap.add_argument("--skip",  dest="skip_tags", action="append", default=[],
                    help="tag (or 'llm') to skip; can repeat")
    ap.add_argument("--dry",   action="store_true", help="show plan only")
    args = ap.parse_args()

    plan = list(STEPS)
    if args.only_tag:
        plan = [s for s in plan if s[0] == args.only_tag]
        if not plan:
            sys.exit(f"--only {args.only_tag}: tag not found")
    else:
        if args.from_tag:
            tags = [s[0] for s in plan]
            if args.from_tag not in tags:
                sys.exit(f"--from {args.from_tag}: tag not found")
            plan = plan[tags.index(args.from_tag):]
        if args.until_tag:
            tags = [s[0] for s in plan]
            if args.until_tag not in tags:
                sys.exit(f"--until {args.until_tag}: tag not found")
            plan = plan[:tags.index(args.until_tag) + 1]
    skip_llm = "llm" in args.skip_tags
    plan = [s for s in plan if s[0] not in args.skip_tags
            and not (skip_llm and s[3])]

    print(f"pipeline plan ({len(plan)} steps):")
    for tag, desc, *_ in plan:
        print(f"  • {tag:22s} {desc}")

    failures = []
    totals = 0.0
    for tag, desc, cmd, _ in plan:
        ok, dt = run_step(tag, desc, cmd, args.dry)
        totals += dt
        if not ok:
            failures.append(tag)
            print(f"\n!! [{tag}] FAILED (after {dt:.1f}s) — aborting")
            break

    print(f"\n{'═'*72}\npipeline {'OK' if not failures else 'FAILED'} "
          f"({totals:.1f}s, {len(plan)-len(failures)}/{len(plan)} steps)")
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
