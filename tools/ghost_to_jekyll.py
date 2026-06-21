#!/usr/bin/env python3
"""Import a Ghost JSON export into Jekyll Markdown posts.

Reusable across multiple Ghost blogs. It converts each post's HTML body to
Markdown, writes Jekyll front matter, splits published posts (``_posts/``) from
drafts (``_drafts/``), rewrites Ghost image URLs to local asset paths (logging
every referenced image so the binaries can be sourced later), and auto-detects
each post's language (English / Spanish) so a bilingual blog can route es posts
under an ``/es/`` permalink prefix.

Examples
--------
Import the current blog into the repo root::

    python tools/ghost_to_jekyll.py thoughts-lattice.ghost.2026-06-21.json

Import a second, older blog without touching the first (drafts kept, append to
the same missing-images log)::

    python tools/ghost_to_jekyll.py old-blog.ghost.json \\
        --lang-override some-spanish-post=es \\
        --missing-images MISSING-IMAGES.md --append-missing

Keep images pointing at a still-running Ghost instance instead of local paths::

    python tools/ghost_to_jekyll.py export.json \\
        --ghost-url https://blog.example.com

Requires: ``html2text`` (``pip install html2text``).
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

import html2text

# --------------------------------------------------------------------------- #
# Language detection (dependency-free en/es heuristic)
# --------------------------------------------------------------------------- #
ES_STOPWORDS = {
    "que", "de", "la", "el", "los", "las", "una", "por", "con", "para", "más",
    "está", "están", "son", "como", "pero", "este", "esta", "esto", "cuando",
    "también", "porque", "donde", "sobre", "entre", "hasta", "desde", "muy",
    "sin", "ser", "hacer", "tiene", "todo", "todos", "nada", "algo", "así",
}
EN_STOPWORDS = {
    "the", "and", "of", "to", "is", "in", "that", "it", "for", "with", "as",
    "was", "on", "are", "this", "but", "be", "have", "from", "or", "by", "an",
    "not", "you", "your", "they", "their", "which", "would", "about", "into",
}
WORD_RE = re.compile(r"[a-záéíóúñü]+", re.IGNORECASE)


def detect_language(text, default="en"):
    """Return 'es' or 'en' for the given plain text using a stopword ratio."""
    if not text:
        return default
    sample = text.lower()[:4000]
    # Strong Spanish-only signals.
    if "¿" in sample or "¡" in sample:
        return "es"
    words = WORD_RE.findall(sample)
    if not words:
        return default
    total = len(words)
    es_hits = sum(1 for w in words if w in ES_STOPWORDS)
    en_hits = sum(1 for w in words if w in EN_STOPWORDS)
    accented = sum(sample.count(c) for c in "áéíóúñ")
    es_score = es_hits / total + accented / max(total, 1)
    en_score = en_hits / total
    if es_score == en_score:
        return default
    return "es" if es_score > en_score else "en"


# --------------------------------------------------------------------------- #
# HTML -> Markdown
# --------------------------------------------------------------------------- #
def make_converter():
    h = html2text.HTML2Text()
    h.body_width = 0           # never hard-wrap paragraphs
    h.ignore_links = False
    h.ignore_images = False
    h.protect_links = True
    h.unicode_snob = True      # keep curly quotes / em dashes / accents
    h.wrap_links = False
    return h


# --------------------------------------------------------------------------- #
# Importer
# --------------------------------------------------------------------------- #
class GhostImporter:
    def __init__(self, args):
        self.args = args
        self.converter = make_converter()
        # (post_title, original_ghost_url, resolved_path)
        self.image_refs = []

    # -- image handling ----------------------------------------------------- #
    def resolve_image(self, url, slug, title):
        # Images are grouped per article: /assets/images/<slug>/<filename>.
        prefix = "__GHOST_URL__"
        if not url.startswith(prefix):
            return url  # external image, leave as-is
        path = url[len(prefix):]
        if self.args.ghost_url:
            return self.args.ghost_url.rstrip("/") + path
        if path.startswith("/content/images/"):
            filename = os.path.basename(path)
            local = f"{self.args.assets_prefix.rstrip('/')}/{slug}/{filename}"
            self.image_refs.append((title, url, local))
            return local
        return self.args.assets_prefix.rstrip("/") + path

    def rewrite_images_in_html(self, html, slug, title):
        return re.sub(
            r'src="([^"]+)"',
            lambda m: f'src="{self.resolve_image(m.group(1), slug, title)}"',
            html,
        )

    # -- front matter ------------------------------------------------------- #
    @staticmethod
    def yaml_quote(value):
        if value is None:
            return '""'
        return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'

    @staticmethod
    def parse_dt(value):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def permalink(self, slug, lang):
        if lang != self.args.default_lang:
            return f"/{lang}/{slug}/"
        return f"/{slug}/"

    def build_front_matter(self, post, tags, lang):
        lines = ["---", "layout: post",
                 f"title: {self.yaml_quote(post['title'])}"]
        if post.get("published_at"):
            dt = self.parse_dt(post["published_at"])
            lines.append(f"date: {dt.strftime('%Y-%m-%d %H:%M:%S %z')}")
        lines.append(f"slug: {post['slug']}")
        lines.append(f"lang: {lang}")
        lines.append(f"permalink: {self.permalink(post['slug'], lang)}")
        if tags:
            lines.append("tags:")
            lines.extend(f"  - {t}" for t in tags)
        if post.get("custom_excerpt"):
            lines.append(f"excerpt: {self.yaml_quote(post['custom_excerpt'])}")
        feature = post.get("feature_image")
        if feature:
            lines.append(
                f"feature_image: {self.yaml_quote(self.resolve_image(feature, post['slug'], post['title']))}"
            )
        lines.append(f"original_status: {post['status']}")
        lines.append("---")
        return "\n".join(lines)

    @staticmethod
    def filename_date(post):
        stamp = post.get("published_at") or post.get("created_at")
        return GhostImporter.parse_dt(stamp).strftime("%Y-%m-%d")

    # -- main run ----------------------------------------------------------- #
    def run(self):
        with open(self.args.input) as f:
            data = json.load(f)["db"][0]["data"]
        posts = data["posts"]

        tag_by_id = {t["id"]: t["name"] for t in data.get("tags", [])}
        tags_for_post = {}
        for pt in data.get("posts_tags", []):
            tags_for_post.setdefault(pt["post_id"], []).append(
                (pt.get("sort_order", 0), tag_by_id.get(pt["tag_id"]))
            )

        os.makedirs(self.args.posts_dir, exist_ok=True)
        os.makedirs(self.args.drafts_dir, exist_ok=True)

        overrides = dict(
            o.split("=", 1) for o in self.args.lang_override
        )

        counts = {"published": 0, "draft": 0, "es": 0, "en": 0}
        for post in posts:
            tags = [name for _, name in sorted(tags_for_post.get(post["id"], []))
                    if name]
            lang = overrides.get(post["slug"]) or detect_language(
                post.get("plaintext") or "", self.args.default_lang
            )
            counts[lang] = counts.get(lang, 0) + 1

            html = self.rewrite_images_in_html(
                post.get("html") or "", post["slug"], post["title"])
            body = self.converter.handle(html).strip()
            # Wrap inline image URLs so Jekyll's baseurl is applied (Liquid runs
            # before Markdown): ![alt](/assets/..) -> ![alt]({{ '/assets/..' | relative_url }})
            body = re.sub(
                r'(!\[[^\]]*\]\()(/assets/images/[^)]+)(\))',
                r"\1{{ '\2' | relative_url }}\3",
                body,
            )
            document = self.build_front_matter(post, tags, lang) + "\n\n" + body + "\n"

            if post["status"] == "published":
                path = os.path.join(
                    self.args.posts_dir, f"{self.filename_date(post)}-{post['slug']}.md"
                )
                counts["published"] += 1
            else:
                path = os.path.join(self.args.drafts_dir, f"{post['slug']}.md")
                counts["draft"] += 1

            with open(path, "w") as f:
                f.write(document)
            print(f"  [{lang}] {path}")

        self.write_missing_images()
        print(f"\nDone: {counts['published']} published, {counts['draft']} drafts "
              f"({counts.get('en', 0)} en / {counts.get('es', 0)} es).")
        if self.image_refs and not self.args.ghost_url:
            print(f"Referenced local images: {len(self.image_refs)} "
                  f"(see {self.args.missing_images})")

    def write_missing_images(self):
        if self.args.ghost_url:
            return  # images point at a live URL; nothing to source locally

        existing = {}
        header = (
            "# Missing images\n\n"
            "Images referenced by posts but **not** included in Ghost JSON exports\n"
            "(Ghost stores image binaries separately). Drop each file at the local\n"
            "path shown to make it resolve.\n\n"
            "| Local path | Original Ghost URL | First seen in post |\n"
            "| --- | --- | --- |\n"
        )
        # Preserve prior rows when appending a second blog's import.
        if self.args.append_missing and os.path.exists(self.args.missing_images):
            with open(self.args.missing_images) as f:
                for line in f:
                    m = re.match(r"\| `([^`]+)` \| `([^`]+)` \| (.+) \|", line)
                    if m:
                        existing[m.group(2)] = (m.group(1), m.group(3))

        for title, url, local in self.image_refs:
            existing.setdefault(url, (local, title))

        rows = [
            f"| `{local}` | `{url}` | {title} |"
            for url, (local, title) in sorted(existing.items(),
                                              key=lambda kv: kv[1][0])
        ]
        with open(self.args.missing_images, "w") as f:
            f.write(header + "\n".join(rows) + "\n")


def parse_args(argv):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="Path to the Ghost JSON export")
    p.add_argument("--posts-dir", default="_posts")
    p.add_argument("--drafts-dir", default="_drafts")
    p.add_argument("--assets-prefix", default="/assets/images",
                   help="Local URL prefix for imported images")
    p.add_argument("--ghost-url",
                   help="If set, rewrite __GHOST_URL__ to this base URL instead of "
                        "local asset paths (e.g. https://blog.example.com)")
    p.add_argument("--default-lang", default="en",
                   help="Language assumed when detection is inconclusive")
    p.add_argument("--lang-override", action="append", default=[], metavar="slug=lang",
                   help="Force a post's language, e.g. --lang-override my-post=es "
                        "(repeatable)")
    p.add_argument("--missing-images", default="MISSING-IMAGES.md")
    p.add_argument("--append-missing", action="store_true",
                   help="Merge into an existing missing-images file (for a 2nd blog)")
    return p.parse_args(argv)


if __name__ == "__main__":
    GhostImporter(parse_args(sys.argv[1:])).run()
