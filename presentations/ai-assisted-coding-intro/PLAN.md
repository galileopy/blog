# Deck plan — On AI Assisted Coding

Tracking doc for the **whole deck**, one entry per major outline section. Source
of truth for content is `outline.md`; this file records how it maps to slides and
what state each section is in. Rationale lives in `decisions.log`; the SVG
regeneration task has its own spec in `svg-prompts.md`.

Status legend: `built` · `in progress` · `planned`

**Built so far: 4 top-level slides (9 including the vertical stack).** Everything
from Conventions onward is still unbuilt.

---

## 0 · Opening — status: built

| # | Hash | Layout | Content |
|---|---|---|---|
| 01 | `#/0` | L-01 title | "On AI Assisted Coding" + subtitle, blue chevrons |

---

## 1 · Temperature Check — status: built

Resolved: the section now carries 6 items, with the spec-driven and workflows
sub-bullets folded into their parent lines (L-02 caps at 6).

| # | Hash | Layout | Content |
|---|---|---|---|
| 02 | `#/1` | L-02 agenda | "Where are you at today?" — 6 items |

---

## Part 1 · The Evolution of the Feedback Loop — status: built

The spine of the talk. One statement slide, then a **vertical stack** of six
two-column slides — diagram left, steps right — so the loop reads as one topic
that evolves rather than six separate slides.

| # | Hash | Layout | Content |
|---|---|---|---|
| 03 | `#/2` | L-04 statement | "It is still coding. / You have a different feedback loop." |
| 04 | `#/3/0` | L-06 | Level 0 · Traditional · traditionally, all of it |
| 04 | `#/3/1` | L-06 | Level 1 · AI Assisted Coding · center a div |
| 04 | `#/3/2` | L-06 | Level 2 · Autonomous · debugging |
| 04 | `#/3/3` | L-06 | Level 3 · Test Driven — TDD · add complex feature |
| 04 | `#/3/4` | L-06 | Level 4 · Spec Driven · generate new greenfield apps |
| 04 | `#/3/5` | L-06 | Level 5 · Spec Driven, Predefined Workflows · brownfield projects |

**Canonical steps.** Seven execution steps in fixed order — technical design
(optional), failing tests, code, run, test, iterate, refactor — bracketed by
three edges: `once` (author workflows, L5 only), `start` (specify requirements),
`stop` (until requirements are satisfied). A level carries every step introduced
at or before it; nothing is ever removed.

**Actor glyphs.** Every row carries `:human:`, `:bot:`, `:laptop:`, or a
human+bot pair. Run is machine at every level — it never changes hands. A step is
tagged `changed` at the level where its actor changes, `added` where the step
itself is new; earlier changes are carried unmarked.

**Both pins use hidden spacers, not pixel offsets.** Levels without a pre-loop
step reserve its slot with an invisible `.loop-edge.pre.spacer`; short lists pad
to seven steps with `li.spacer` rows. Result: start at y=227 and stop at y=522 on
all six. Spacers must mirror the real row's *structure* (tags and glyphs), not
just its text, or the row heights drift ~2px. Hidden rows still increment the
step counter, so they only ever go at the end of a list.

Open items:
- [ ] Regenerate the six SVGs — see `svg-prompts.md`. They predate almost all of
      the above and are the last thing out of sync.
- [ ] `loop-00-skeleton.svg` is orphaned (skeleton slide folded into Traditional);
      delete or keep deliberately.

---

## Part 2 · Managing Context — status: planned

Conventions, Workflows, and Existing Infrastructure all answer the same
question: how the agent gets the context it needs. Grouped under one part.

| # | Layout | Band | Content |
|---|---|---|---|
| — | L-03 divider | **ink** | "Part 2 — Managing Context" |
| — | L-07 three-up | canvas | Conventions, "how to add X": External interface (REST / GraphQL field / RPC-WS handler) · Infrastructure component (Terraform / CDK) · Tests and tiers (e2e / integration / unit). Framing line: "Applies to anything that is managed by code" |
| — | L-04 statement | canvas | "It's about encoding what you do in prompts and then iterating automatically." |
| — | L-08 four-up | canvas | Tracking requirements · Refining tickets · Review cycle (adversarial, different model) · Drift check |
| — | L-10 or L-08 | canvas | Implementation process guidelines (TDD, testing tiers) · Clean code practices (general authoring, OO preferences, local preferences) — **layout depends on the blocked line below** |
| — | L-06 two-column | canvas | Dynamic vs static workflows — dev preferences, project differences |

**BLOCKED — needs the user's wording.** `outline.md` reads "Local preferences not
enforceable by [tooling? — sentence looks cut off]". It is the third sub-item of
Clean code practices and load-bearing for that slide. Do not guess it.

Resolved: "Existing Infrastructure" is no longer its own section. Terraform/CDK
folded in as the Infrastructure component sub-items, which also makes the
three-up symmetrical (each branch now has sub-items) and removes a duplicate
"how to add X" framing.

Note: the guidelines slide is **two** groups, not three — "local preferences" is
a sub-bullet of clean code practices, not a peer. Pick the layout once the
blocked line lands.

---

## Part 3 · Cool Tips, Tricks and Links — status: planned

| # | Layout | Band | Content |
|---|---|---|---|
| — | L-03 divider | **ink** | "Part 3 — Cool Tips, Tricks and Links" |
| — | L-07 three-up | canvas | Refinement (Linear; structured English: user stories / EARS / Gherkin; INVEST splits) · Incidents (live logs + repo to triage) · Post mortems (generate monitoring dashboards) |
| — | L-06 two-column | canvas | Load testing and improving/revalidating + isolated worktrees for concurrent features |
| — | L-07 three-up | canvas | References: groundcrew · spec-kit · conductor |

Note: "agents love red herrings" is delivery commentary — candidate for
`<aside class="notes">` rather than slide text.

**Open:** the References slide is names only. spec-kit and conductor already
appear in Temperature Check ("canned, spec-kit/conductor"), so this slide should
add something new — a URL each at minimum. Groundcrew appears nowhere else and
arrives cold.

---

## Close — status: planned

| # | Layout | Band | Content |
|---|---|---|---|
| — | L-13 closing | ink | Closing line still to be chosen — the drift-check question ("are requirements, code, and acceptance tests all aligned?") is the strongest candidate already in the outline. |

---

## Standing constraints

- Never invent content that is not in `outline.md`.
- Do not change the `Reveal.initialize` config (1280×720, `margin: 0`,
  `center: false`) — the theme's absolute px assume that stage.
- **All transitions are off** (`transition: 'none'`, `backgroundTransition:
  'none'`, plus CSS `!important` overrides). Any transform-based transition
  resamples a rasterized slide mid-motion and softens display type. Do not add
  `backface-visibility: hidden` or `will-change: transform` either — both promote
  layers and cause *static* blur on the stacked sections.
- **White (`s-canvas`) for every content slide; ink slabs for Part dividers
  only.** The flat surface keeps the six loop slides reading as one continuous
  topic; the three Part dividers going dark is then the deck's only band change,
  which is what makes it read as a structural boundary rather than decoration.
  Do not reintroduce cloud/fog tints for ordinary slides.
- Blue is well past the design system's "at most twice per slide": Level 4 alone
  carries three `changed` tags and seven bot glyphs. Consequence of the glyph
  system, not a regression — but if the slides start reading as uniformly blue,
  desaturate the *carried* glyphs and let only flagged rows stay blue.
- Verify over HTTP with hash deep-links, screenshot at 1280×720, and *read* the
  PNGs. Chrome blocks port 5060 (`ERR_UNSAFE_PORT`) and silently screenshots an
  error page — a measurement pass on that port looks clean and means nothing.
- Committed through `8031fc0` on branch `presentations/ai-assisted-coding-intro`.
