#!/usr/bin/env sh
# Record a demo take: ./record.sh 01-comments-to-code
set -eu
name="${1:?usage: ./record.sh <demo-name>}"
dir="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$dir/casts"
exec asciinema rec --overwrite --cols 120 --rows 30 "$dir/casts/$name.cast"
