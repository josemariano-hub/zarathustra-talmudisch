#!/usr/bin/env python3
"""
End-to-end semantic audit of every (verse, note) pair across the book.

For each pair we ask Gemini-Flash:
  • What is the verse saying?
  • What is the commentary note doing?
  • Score the connection 0-3:
      0 = no connection / wrong attachment
      1 = weak / generic / tenuous
      2 = reasonable
      3 = strong / clearly the right verse

Result: source/audit.json with one row per note containing
  {target, stream, score, reason, action}
Action policy:
  • 0 → drop the note
  • 1 → keep but flag (margin-coloured) so the user can review
  • 2/3 → keep
Then rewrite commentary.json with the action applied.

Idempotent + cached by SHA1(verse_text + note_text) so reruns are cheap.
"""

from __future__ import annotations
import json, hashlib, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor
import threading
from pathlib import Path
import google.generativeai as genai

PROJ   = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
SRC    = PROJ / "source"
COMM   = SRC / "commentary.json"
NAV    = json.loads((SRC / "chapter-nav.json").read_text(encoding="utf-8"))
CACHE  = SRC / ".audit-cache.json"
AUDIT  = SRC / "audit.json"

MODEL    = "gemini-2.5-flash"
BATCH    = 4
WORKERS  = 8
MAX_RETRY = 4

SYSTEM = (
    "You are an editor checking the alignment of scholarly commentary "
    "to verses of Nietzsche's *Also sprach Zarathustra*. For each pair "
    "you decide: does the commentary plausibly illuminate THIS verse "
    "(not just the chapter or general theme)? Be conservative — a note "
    "that talks about the chapter's broader theme but does not engage "
    "what this specific verse says is at best a 1. Reserve 3 for notes "
    "that name a word/image/idea unique to this verse. Output strictly:\n"
    "[N] score=X reason=...\n"
    "where N is the pair number and X is 0, 1, 2, or 3."
)

def verses_de() -> dict[str, dict[str, str]]:
    out = {}
    for e in NAV:
        if e["xml_id"] == "ch-p0-00": continue
        p = SRC / e["file"]
        if not p.exists(): continue
        vs = {}
        txt = p.read_text(encoding="utf-8")
        for m in re.finditer(r'<paragraphs xml:id="([^"]+)">(.*?)</paragraphs>', txt, re.DOTALL):
            vid, body = m.group(1), m.group(2)
            de = re.search(r'xml:lang="de"[^>]*>(.*?)</p>', body, re.DOTALL)
            en = re.search(r'xml:lang="en"[^>]*>(.*?)</p>', body, re.DOTALL)
            text = ""
            if de: text = re.sub(r"<[^>]+>", "", de.group(1)).strip()
            if en:
                en_text = re.sub(r"<[^>]+>", "", en.group(1)).strip()
                text = f"{text}\n  EN: {en_text}" if text else en_text
            vs[vid] = text
        out[e["xml_id"]] = vs
    return out

def vorrede_verses() -> dict[str, str]:
    p = SRC / "ch_vorrede.ptx"
    if not p.exists(): return {}
    txt = p.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<paragraphs xml:id="([^"]+)">(.*?)</paragraphs>', txt, re.DOTALL):
        vid = m.group(1)
        body = m.group(2)
        de = re.search(r'xml:lang="de"[^>]*>(.*?)</p>', body, re.DOTALL)
        en = re.search(r'xml:lang="en"[^>]*>(.*?)</p>', body, re.DOTALL)
        text = ""
        if de: text = re.sub(r"<[^>]+>", "", de.group(1)).strip()
        if en:
            en_text = re.sub(r"<[^>]+>", "", en.group(1)).strip()
            text = f"{text}\n  EN: {en_text}" if text else en_text
        out[vid] = text
    return out

def hash_pair(verse: str, note: str) -> str:
    return hashlib.sha1(f"{verse[:600]}||{note[:800]}".encode("utf-8")).hexdigest()[:14]

def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}

def save_cache(c):
    CACHE.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")

def call_batch(model, pairs) -> dict[int, tuple[int, str]]:
    # Build prompt
    lines = [SYSTEM, ""]
    for i, (_, verse, note) in enumerate(pairs):
        lines.append(f"--- pair [{i+1}] ---")
        lines.append(f"VERSE: {verse[:600]}")
        lines.append(f"NOTE:  {note[:800]}")
        lines.append("")
    lines.append(f"Output exactly {len(pairs)} lines, one per pair, in order.")
    prompt = "\n".join(lines)
    rsp = model.generate_content(prompt)
    body = rsp.text or ""
    out: dict[int, tuple[int, str]] = {}
    for line in body.splitlines():
        m = re.match(r"\[(\d+)\]\s+score=(\d)\s+reason=(.*)", line.strip())
        if m:
            idx = int(m.group(1))
            score = int(m.group(2))
            out[idx] = (score, m.group(3).strip())
    return out

def run_batch(model, batch, cache, lock):
    pairs = []
    keys = []
    for item in batch:
        ck = item["cache_key"]
        if ck in cache:
            continue
        pairs.append((item, item["verse_text"], item["note_text"]))
        keys.append(ck)
    if not pairs:
        return
    delay = 1.0
    for attempt in range(MAX_RETRY):
        try:
            results = call_batch(model, pairs)
            break
        except Exception as e:
            if attempt == MAX_RETRY - 1:
                print(f"  giving up on batch: {e}")
                return
            time.sleep(delay); delay *= 2
    with lock:
        for i, (item, _, _) in enumerate(pairs):
            res = results.get(i+1)
            if res:
                cache[item["cache_key"]] = {"score": res[0], "reason": res[1]}

def main():
    api_key = os.environ.get("GOOGLE_API_KEY") or "AIzaSyCOla_ZVKmzW-B9MUlOocjd2n4BPCwlsAo"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL)

    data = json.loads(COMM.read_text(encoding="utf-8"))
    cache = load_cache()

    # Gather all (verse, note) work units
    ch_verses = verses_de()
    ch_verses["ch-p0-00"] = vorrede_verses()
    work = []
    for sname, stream in data["streams"].items():
        if sname.startswith("_"): continue
        for idx, n in enumerate(stream["notes"]):
            target = n.get("target", "")
            # Resolve verse text
            if target.startswith("v"):
                verse_text = ch_verses.get("ch-p0-00", {}).get(target, "")
            else:
                ch = target.rsplit("-v", 1)[0]
                verse_text = ch_verses.get(ch, {}).get(target, "")
            if not verse_text:
                continue
            # Note text — prefer EN, fall back to whatever exists
            note_text = (n.get("en") or n.get("fr") or n.get("es") or "")
            if not note_text:
                continue
            term = n.get("term")
            if isinstance(term, dict): term = term.get("en", "")
            if term:
                note_text = f"[{term}] {note_text}"
            ck = hash_pair(verse_text, note_text)
            work.append({
                "stream": sname,
                "index": idx,
                "target": target,
                "verse_text": verse_text,
                "note_text": note_text,
                "cache_key": ck,
            })

    todo = [w for w in work if w["cache_key"] not in cache]
    print(f"total pairs: {len(work)}   cached: {len(work)-len(todo)}   to audit: {len(todo)}")

    lock = threading.Lock()
    batches = [todo[i:i+BATCH] for i in range(0, len(todo), BATCH)]
    done = [0]
    def runner(b):
        run_batch(model, b, cache, lock)
        with lock:
            done[0] += len(b)
            if done[0] % 40 == 0:
                save_cache(cache)
                print(f"  {done[0]}/{len(todo)}")
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(runner, batches))
    save_cache(cache)

    # Build audit report + apply actions
    audit = []
    keep_streams: dict[str, list] = {s: [] for s in data["streams"]}
    audited_idxs: dict[str, set[int]] = {s: set() for s in data["streams"]}
    drop_count = 0; flag_count = 0
    for w in work:
        c = cache.get(w["cache_key"], {"score": 2, "reason": "uncached"})
        row = {
            "stream": w["stream"],
            "target": w["target"],
            "score": c["score"],
            "reason": c["reason"],
        }
        audit.append(row)
        note = data["streams"][w["stream"]]["notes"][w["index"]]
        audited_idxs[w["stream"]].add(w["index"])
        if c["score"] == 0:
            drop_count += 1
            continue
        elif c["score"] == 1:
            note["_audit_flag"] = "weak"
            note["_audit_reason"] = c["reason"]
            flag_count += 1
        elif c["score"] >= 2:
            note.pop("_audit_flag", None)
            note.pop("_audit_reason", None)
        keep_streams[w["stream"]].append((w["index"], note))

    # Notes the audit never saw (no verse_text or no note_text) are kept
    # untouched — they're not the same as "audited & dropped".
    for sname, stream in data["streams"].items():
        if sname.startswith("_"): continue
        for j, note in enumerate(stream["notes"]):
            if j not in audited_idxs[sname]:
                keep_streams[sname].append((j, note))
        keep_streams[sname].sort(key=lambda t: t[0])
        stream["notes"] = [n for _, n in keep_streams[sname]]

    # Score distribution
    from collections import Counter
    dist = Counter(r["score"] for r in audit)
    print(f"\nscore distribution: {dict(sorted(dist.items()))}")
    print(f"dropped: {drop_count}   flagged-weak: {flag_count}   kept-strong: {dist.get(2,0)+dist.get(3,0)}")

    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\naudit written to {AUDIT.name}")
    print(f"commentary.json updated (kept {sum(len(s['notes']) for s in data['streams'].values())} notes)")

if __name__ == "__main__":
    main()
