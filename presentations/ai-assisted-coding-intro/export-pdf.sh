#!/usr/bin/env bash
# Export the deck to PDF.
#
# Chrome's own --print-to-pdf does NOT work here: its CLI ignores the @page size
# reveal injects (that needs DevTools' preferCSSPageSize, which has no CLI flag),
# so it exports letter-portrait and the 1280px stage overflows and collapses the
# grid layouts. decktape drives a real browser and honours the slide size.
#
# Usage: ./export-pdf.sh [output.pdf]
set -euo pipefail

OUT="${1:-on-ai-assisted-coding.pdf}"
PORT=5081   # NOT 5060 — Chrome blocks it as an unsafe port
DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$DIR"
python3 -m http.server "$PORT" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null || true' EXIT
sleep 1

npx -y decktape@3 reveal \
  -s 1280x720 \
  --chrome-arg=--no-sandbox \
  --chrome-arg=--disable-gpu \
  --chrome-arg=--disable-dev-shm-usage \
  "http://localhost:$PORT/" "$OUT"

echo "Wrote $DIR/$OUT"
