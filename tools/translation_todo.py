#!/usr/bin/env python3
"""Generate TRANSLATIONS.md — a local TODO of posts missing a translation.

Scans _posts for each post's `lang` and optional `ref` (the translation-pair
key). A post is "covered" when another post shares its `ref` in the other
language; otherwise it needs a translation. Output is a local working doc, not
site content.

Workflow to mark a pair done: give both the original and its translation the
same `ref: <key>` front matter, then re-run this script.

Usage: python tools/translation_todo.py
"""
import glob
import os
import re

POSTS_DIR = "_posts"
OUTPUT = "TRANSLATIONS.md"
LANGS = ("en", "es")
OTHER = {"en": "es", "es": "en"}


def field(front_matter, key):
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', front_matter, re.M)
    return m.group(1) if m else None


def load_posts():
    posts = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        fm = open(path).read().split("---", 2)[1]
        posts.append({
            "path": path,
            "title": field(fm, "title"),
            "lang": field(fm, "lang") or "en",
            "ref": field(fm, "ref"),
            "permalink": field(fm, "permalink"),
        })
    return posts


def main():
    posts = load_posts()
    # ref -> set of languages present, for pairs that are linked.
    langs_by_ref = {}
    for p in posts:
        if p["ref"]:
            langs_by_ref.setdefault(p["ref"], set()).add(p["lang"])

    needs = {"en": [], "es": []}   # keyed by the language to be PRODUCED
    done = []
    for p in posts:
        other = OTHER[p["lang"]]
        covered = p["ref"] and other in langs_by_ref.get(p["ref"], set())
        if covered:
            if p["lang"] == "en":   # record the pair once
                done.append(p)
        else:
            needs[other].append(p)

    lines = [
        "# Translation sync — TODO",
        "",
        "Regenerate with `python tools/translation_todo.py`. To mark a pair done,",
        "add the same `ref: <key>` to both the source post and its translation,",
        "then re-run. (Local working doc — not published.)",
        "",
        f"Source posts: {len(posts)} · pairs complete: {len(done)} · "
        f"need EN: {len(needs['en'])} · need ES: {len(needs['es'])}",
    ]

    headings = {
        "en": "## Need an English version (currently ES-only)",
        "es": "## Need a Spanish version (currently EN-only)",
    }
    for produce in ("en", "es"):
        lines += ["", headings[produce], ""]
        items = needs[produce]
        if not items:
            lines.append("- _none_")
            continue
        for p in items:
            lines.append(f"- [ ] **{p['title']}** — from `{p['path']}` "
                         f"({p['lang'].upper()} → {produce.upper()})")

    lines += ["", "## Complete pairs", ""]
    if done:
        for p in done:
            lines.append(f"- [x] {p['title']} (ref: `{p['ref']}`)")
    else:
        lines.append("- _none_")
    lines.append("")

    with open(OUTPUT, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {OUTPUT}: need EN={len(needs['en'])}, need ES={len(needs['es'])}, "
          f"complete pairs={len(done)}")


if __name__ == "__main__":
    main()
