# On AI Assisted Coding — working agreements

Reveal.js deck built with the galileo-presentation design system. This file holds
*how we work on it*; it is not a status tracker.

## Files and their roles

| File | Role |
|---|---|
| `outline.md` | **Source of truth for content.** Outline-level only — headings and bullets, no process notes, no commentary. |
| `index.html` | The deck. Kept in sync with `outline.md` *at the outline level*: every slide traces to an outline node, and nothing on a slide exists that the outline does not have. |
| `decisions.log` | Rationale, process decisions, commentary, things tried and rejected. Anything that is *why* rather than *what* goes here, not in the outline. |
| `svg-prompts.md` | Spec for regenerating the Part 1 loop diagrams. |
| `theme/galileo.css` | Design system. Layout classes (`layout-loop`, `layout-divider`, …) live here. |

## Rules

- **One slide at a time.** Always. Pick the slide, choose its layout, build it,
  verify it, log the decision — then stop and check in before moving to the next.
  Never batch several slides into one pass, even when they look similar or the
  section plan lists them together.
- Never put content on a slide that is not in `outline.md`. If new content is
  wanted, add it to the outline first, then build the slide.
- Never put process commentary in `outline.md`. It goes in `decisions.log`.
- For new or reworked slides, consult the `presentation:reveal` skill for the
  layout catalog and pick a template that fits the content shape — do not default
  to a bullet list.
- Record every non-obvious decision in `decisions.log` as you make it.
- After a work session, re-sync `outline.md` against `index.html`. (There was a
  `PLAN.md` tracker; it served its purpose and was deleted — do not recreate it.
  `git show 657005d:presentations/ai-assisted-coding-intro/PLAN.md` if the old
  slide-mapping tables are ever wanted.)
- Do not change the `Reveal.initialize` config (1280×720, `margin: 0`,
  `center: false`) — the theme's absolute px positions assume that stage.
- **Transitions stay off**, including on fragments. reveal ships
  `transition`/`will-change` on `.fragment`, which promotes a compositing layer
  and blurs slide text while it is standing still; `theme/galileo.css` nulls it
  alongside the `.slides`/`section` rules. Do not add `backface-visibility` or
  `will-change: transform` either.
- Verify over HTTP with hash deep-links, screenshot at 1280×720, and *read* the
  PNGs. Chrome blocks port 5060 (`ERR_UNSAFE_PORT`) and silently screenshots an
  error page.

## Structure

Three parts, each opened by an ink divider; every content slide is `s-canvas`
(white). The dividers are the deck's only band change — that is what makes them
read as structural boundaries.
