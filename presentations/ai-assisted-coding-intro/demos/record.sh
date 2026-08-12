#!/usr/bin/env sh
# Record a demo take: ./record.sh 01-comments-to-code
# Records at the terminal's native size — size the window/pane before starting,
# since asciinema replays at whatever geometry it captured.
set -eu
name="${1:?usage: ./record.sh <demo-name>}"
dir="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$dir/casts"
exec asciinema rec --overwrite "$dir/casts/$name.cast"
