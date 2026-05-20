#!/usr/bin/env python3
"""
Translate the RAG commentary streams into the two non-origin languages.

Until now, retrieve_commentary.py wrote the SAME source-language paragraph
into all three en/fr/es fields, so a Spanish reader of Klossowski was
actually shown French text labeled as Spanish.  This script fixes that:
for every note in a RAG stream, we keep the _origin language as-is and
translate it into the other two via Anthropic API (Haiku — fast/cheap).

Cache keyed by (_corpus_idx, _origin, target_lang) in
source/.translation-cache.json so re-runs are free.
"""

from __future__ import annotations
import json, os, sys, time, hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import google.generativeai as genai

PROJ  = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
COMM  = PROJ / "source" / "commentary.json"
CACHE = PROJ / "source" / ".translation-cache.json"

# Streams that needed initial translation away from a single source language
RAG_STREAMS = {"klossowski", "deleuze", "sanchez-meca", "new-cambridge",
               "sp-introduction", "sanchez-pascual-notes"}

# All four reader languages — DE is a target now so the reader can see
# notes when reading the German Urtext side without any translation pairing.
LANG_NAME = {"en": "English", "fr": "French", "es": "Spanish", "de": "German"}
TARGET_LANGS = ("en", "fr", "es", "de")

MODEL = "gemini-2.5-flash"
BATCH = 4       # notes per API call
WORKERS = 8     # concurrent API calls
MAX_RETRY = 4   # per batch

SYSTEM = (
    "You are a literary translator working on academic commentary about "
    "Nietzsche's *Also sprach Zarathustra*. Preserve the scholar's voice, "
    "philosophical register, and quoted material verbatim. Render proper "
    "nouns and Nietzsche terms (Übermensch, Untergang, Wille zur Macht, "
    "ewige Wiederkunft) per standard academic convention in the target "
    "language. Translate the passages given; output ONLY the translations, "
    "numbered, one per line, no preamble."
)

def load_cache():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}

def save_cache(c):
    CACHE.write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")

def batched(items, n):
    for i in range(0, len(items), n):
        yield items[i:i+n]

def translate_batch(model, src_lang, tgt_lang, texts) -> list[str]:
    src_name = LANG_NAME[src_lang]; tgt_name = LANG_NAME[tgt_lang]
    numbered = "\n\n".join(f"[{i+1}]\n{t}" for i, t in enumerate(texts))
    prompt = (
        f"{SYSTEM}\n\n"
        f"Translate these {len(texts)} {src_name} passages into {tgt_name}. "
        f"Output exactly {len(texts)} numbered blocks in the SAME order. "
        f"Use the form '[1]\\n<translation>\\n\\n[2]\\n<translation>' — nothing else.\n\n"
        f"{numbered}"
    )
    rsp = model.generate_content(prompt)
    body = rsp.text
    chunks = {}
    cur = None; buf = []
    for ln in body.splitlines():
        s = ln.strip()
        if s.startswith("[") and s.endswith("]") and s[1:-1].isdigit():
            if cur is not None: chunks[cur] = "\n".join(buf).strip()
            cur = int(s[1:-1]); buf = []
        elif cur is not None:
            buf.append(ln)
    if cur is not None: chunks[cur] = "\n".join(buf).strip()
    out = [chunks.get(i+1, "") for i in range(len(texts))]
    return out

def main():
    api_key = os.environ.get("GOOGLE_API_KEY") or "AIzaSyCOla_ZVKmzW-B9MUlOocjd2n4BPCwlsAo"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL)

    data = json.loads(COMM.read_text(encoding="utf-8"))
    cache = load_cache()

    todo: list[tuple] = []  # (stream, idx, src_lang, tgt_lang, text, cache_key)
    for sname, stream in data["streams"].items():
        if sname.startswith("_"): continue
        # Pick a source language to translate from. RAG streams have an
        # explicit _origin; hand-curated multilingual streams (philology,
        # crossref) fall back to EN as the canonical source for translation.
        src = stream.get("_origin") or "en"
        for i, n in enumerate(stream["notes"]):
            origin_text = n.get(src, "") or n.get("en") or n.get("fr") or n.get("es")
            if not origin_text: continue
            # Hash-based cache key so caching survives changes in corpus_idx
            h = hashlib.sha1(origin_text.encode("utf-8")).hexdigest()[:12]
            n[src] = origin_text  # canonicalise
            for tgt in TARGET_LANGS:
                if tgt == src: continue
                # Skip if target already has a non-empty value
                if n.get(tgt): continue
                ck = f"{src}->{tgt}::{h}"
                if ck in cache:
                    n[tgt] = cache[ck]
                else:
                    todo.append((sname, i, src, tgt, origin_text, ck))

    print(f"to translate: {len(todo)}  (cache hits already applied)")

    # Group by (src, tgt) so each batch shares the same prompt header
    by_pair: dict[tuple[str,str], list] = {}
    for item in todo:
        by_pair.setdefault((item[2], item[3]), []).append(item)

    lock = threading.Lock()
    cache_dirty = [False]
    completed = [0]
    total = sum(len(items) for items in by_pair.values())

    def run_batch(model, src, tgt, batch):
        texts = [it[4] for it in batch]
        delay = 1.0
        for attempt in range(MAX_RETRY):
            try:
                return translate_batch(model, src, tgt, texts)
            except Exception as e:
                msg = str(e)[:120]
                if attempt == MAX_RETRY - 1:
                    print(f"  giving up: {msg}")
                    return [""] * len(texts)
                time.sleep(delay)
                delay *= 2

    def commit(items, results):
        with lock:
            for it, tr in zip(items, results):
                if not tr: continue
                sname, idx, _, _, _, ck = it
                data["streams"][sname]["notes"][idx][tgt_of(it)] = tr
                cache[ck] = tr
            cache_dirty[0] = True
            completed[0] += sum(1 for r in results if r)
            if completed[0] % 40 == 0:
                save_cache(cache)
                cache_dirty[0] = False

    def tgt_of(item): return item[3]

    for (src, tgt), items in by_pair.items():
        print(f"\n[{src} -> {tgt}] {len(items)} notes (8 workers, batch={BATCH})")
        batches = list(batched(items, BATCH))
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = []
            for b in batches:
                futures.append(pool.submit(run_batch, model, src, tgt, b))
            for f, b in zip(futures, batches):
                try:
                    results = f.result()
                    commit(b, results)
                    print(f"  {completed[0]}/{total}", end="\r", flush=True)
                except Exception as e:
                    print(f"  worker error: {e}")
        save_cache(cache)
        COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print()

    COMM.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\ncommentary.json updated with real translations")

if __name__ == "__main__":
    main()
