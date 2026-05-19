#!/usr/bin/env bash
# Sync web/ + source artifacts to deploy/ and push to Netlify.
# Idempotent — re-running with no changes is a noop deploy.
set -euo pipefail

PROJ="/Volumes/X10 Pro/Zarathustra/zarathustra-pt"
cd "$PROJ"

# 1. sync web assets
mkdir -p deploy/source/chapters
cp -p web/index.html         deploy/
cp -p web/talmud.html        deploy/
cp -p web/about.html         deploy/ 2>/dev/null || true
cp -p web/talmud.js          deploy/
cp -p web/style.css          deploy/
cp -p web/netlify.toml       deploy/ 2>/dev/null || true

# 2. sync source data
cp -p source/commentary.json     deploy/source/
cp -p source/chapter-nav.json    deploy/source/
cp -p source/ch_vorrede.ptx      deploy/source/
cp -p source/streams.config.json deploy/source/ 2>/dev/null || true
rsync -a --delete source/chapters/ deploy/source/chapters/

# 3. push if netlify-cli is available and we have a site
if command -v netlify >/dev/null 2>&1; then
  echo "→ deploying via netlify-cli"
  ( cd deploy && netlify deploy --prod --dir . --site 8967ee45-a392-43b4-9f7d-b484c5fa24ae )
else
  echo "(netlify CLI not found — local sync only)"
fi
