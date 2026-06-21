# Thoughts Lattice

A Jekyll blog for GitHub Pages, imported from a Ghost export. Bilingual (English
at the root, Spanish under `/es/`).

## Local preview

```bash
bundle install
bundle exec jekyll serve --drafts   # http://127.0.0.1:4000  (--drafts shows _drafts/)
```

> The system Ruby's `bundle` may be broken on this machine (it points at a
> missing `ruby2.7`). Use a Ruby manager such as `rbenv`/`asdf`, or run
> `gem install bundler jekyll` for the active Ruby (3.2 is fine).

## Deploying to GitHub Pages

1. Push this directory to a GitHub repo.
2. **Settings → Pages → Build and deployment → Deploy from a branch**, pick your
   branch and `/ (root)`.
3. Set your custom domain in two places (they must match):
   - `CNAME` (currently `CHANGE-ME.example.com`)
   - `url:` in `_config.yml`
   Then add the DNS records GitHub shows and tick **Enforce HTTPS**.

## Importing a Ghost export (reusable)

`tools/ghost_to_jekyll.py` converts any Ghost JSON export to Jekyll Markdown.
It needs `html2text` (`pip install html2text`).

```bash
# This blog (already done):
python tools/ghost_to_jekyll.py thoughts-lattice.ghost.2026-06-21-08-58-19.json

# A second, older blog — keep this blog's images log and append to it:
python tools/ghost_to_jekyll.py ../old-blog.ghost.json \
    --append-missing \
    --lang-override una-entrada-vieja=es
```

What it does:

- HTML → Markdown with Jekyll front matter (`title`, `date`, `slug`,
  `permalink`, `tags`, `excerpt`, `feature_image`, `lang`).
- Published posts → `_posts/YYYY-MM-DD-slug.md`; drafts → `_drafts/slug.md`.
- Rewrites Ghost image URLs (`__GHOST_URL__/content/images/...`) to
  `/assets/images/...` and logs every referenced file in `MISSING-IMAGES.md`
  (Ghost JSON exports do **not** contain image binaries).
- Detects each post's language (en/es) from its text. Override per post with
  `--lang-override <slug>=<lang>`.

Useful flags: `--ghost-url https://blog.example.com` (point images at a live
Ghost site instead of local paths), `--default-lang`, `--posts-dir`,
`--drafts-dir`, `--assets-prefix`. See `python tools/ghost_to_jekyll.py -h`.

## Languages

- Default language (`en`) is served at `/slug/`; Spanish at `/es/slug/`.
- Post language lives in each post's `lang:` front matter.
- To link a translation pair, add the same `ref: some-key` to both posts; the
  post layout then shows a link to the other language.

### Translation sync TODO

`tools/translation_todo.py` writes `TRANSLATIONS.md` (a local, untracked working
doc) listing posts that still need an EN or ES counterpart. Run it after adding
or pairing posts:

```bash
python tools/translation_todo.py
```

A post counts as translated once it and its counterpart share the same `ref`.

## Missing images

See `MISSING-IMAGES.md`. Drop each file at the listed `/assets/images/...` path
(create the folders under `assets/images/`) to make them resolve. The original
Ghost URL for each is listed so you can pull it from a Ghost content backup or
the live site while it's still up.
