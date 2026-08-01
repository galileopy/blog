#!/usr/bin/env sh
# Re-vendor plugin/highlight.js — reveal's own dist build inlines the FULL
# highlight.js (921K). This rebuilds an equivalent at ~138K.
#
#   sh build-highlight.sh [hljs-version] [reveal-version]
set -eu
HLJS="${1:-11.9.0}"; REVEAL="${2:-6.0.1}"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT; cd "$tmp"
npm pack "@highlightjs/cdn-assets@$HLJS" >/dev/null
tar xzf ./*.tgz
curl -sfL "https://raw.githubusercontent.com/hakimel/reveal.js/$REVEAL/plugin/highlight/plugin.js" -o plugin.js
python3 - "$HLJS" "$REVEAL" <<'PY'
import sys
hljs_v, rev_v = sys.argv[1], sys.argv[2]
src = open('plugin.js').read()
# The hljs bundle above declares a top-level `var hljs`. Anything we add must
# live in its own scope or the browser throws "Identifier 'hljs' has already
# been declared" and the whole script — including RevealHighlight — never runs.
src = src.replace("import hljs from 'highlight.js';",
                  "const hljs = window.hljs;", 1)
src = "(function(){\n" + src
src = src.rstrip()
assert src.endswith("export default () => Plugin;"), "reveal changed its plugin export"
src = src[:-len("export default () => Plugin;")] + "window.RevealHighlight = () => Plugin;\n})();\n"
hdr = f"""/* reveal.js highlight plugin — vendored, trimmed offline bundle.
   = @highlightjs/cdn-assets@{hljs_v} highlight.min.js ("common" languages)
   + reveal.js {rev_v} plugin/highlight/plugin.js, rewritten from ESM to a
     window.RevealHighlight global that reads window.hljs.
   Replaces reveal's own dist plugin/highlight.js (921K), which inlines the
   FULL highlight.js. Same API, incl. data-trim / data-line-numbers stepping.
   Re-vendor with build-highlight.sh. */
"""
open('out.js','w').write(hdr + open('package/highlight.min.js').read() + "\n\n" + src)
PY
cat out.js
