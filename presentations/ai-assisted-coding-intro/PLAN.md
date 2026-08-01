# Deck plan — On AI Assisted Coding

Tracking doc, one entry per major outline section. Source of truth for content is
`outline.md`; this file only records how it maps to slides and what state each
section is in.

Status legend: `built` · `in progress` · `planned`

---

## 0 · Opening — status: built

| # | Layout | Band | Content |
|---|---|---|---|
| 01 | L-01 title | canvas | "On AI Assisted Coding" + subtitle |

---

## 1 · Temperature Check — status: needs rework

Outline changed: the items were regrouped (vibe coding split out, "managing
context" promoted to its own bullet). Now 7 top-level items — L-02 caps at 6.

Plan: keep L-02, fold the two sub-bullets of "Spec driven framework" and the
sub-bullet of "Workflows" into their parent lines, giving 6 items:

1. Prompt tests or new functions
2. Vibe coding simple apps
3. Plan mode in tools
4. Spec driven framework — canned (spec-kit/conductor) or in house
5. Workflows and dynamic workflows — prompts describing the whole SDLC
6. Managing context

| # | Layout | Band | Content |
|---|---|---|---|
| 02 | L-02 agenda | cloud | "Where are you at today?" — 6 items above |

**TODO:** slide 02 in `index.html` still carries the old 5-item wording.

---

## 2 · Intro + Feedback Loops — status: in progress

The spine of the talk. One statement slide, then a **vertical stack** of six
L-06 two-column slides — diagram left, steps right — so the loop reads as one
topic that evolves rather than six separate slides.

Uniform template by explicit request (overrides the skill's "vary the layout"
heuristic): `.card-feature` + `.ph.ph-4x3` diagram placeholder on the left;
eyebrow "Feedback Loops · N of 6", `d-md` heading, `ol.agenda.diff` steps,
`badge badge-soft` use case on the right.

**Stable spine treatment**: every stage carries the full normalized skeleton;
nothing is ever removed. Unmarked steps recede to graphite, `li.diff-move` gets
a blue left-bar and a mono tag (`added` / `changed`), `span.opt` marks the
optional steps. CSS at the end of `theme/galileo.css` (deck-local copy), tokens
only. See `decisions.log` for why this replaced the earlier +/- diff.

| # | Hash | Layout | Content |
|---|---|---|---|
| 03 | `#/2` | L-04 statement | "It is still coding. / You have a different feedback loop." |
| 04 | `#/3/0` | L-06 | Traditional — the baseline, every step human · all of it |
| 04 | `#/3/1` | L-06 | AI — *changed*: prompt, generate code · center a div |
| 04 | `#/3/2` | L-06 | Autonomous — *changed*: iterate, feed results back · debugging |
| 04 | `#/3/3` | L-06 | TDD — *added*: failing tests, *added*: refactor · complex feature |
| 04 | `#/3/4` | L-06 | Spec driven — *added*: prompt, generate specs · greenfield |
| 04 | `#/3/5` | L-06 | Spec driven + workflows — *added*: author workflows · brownfield |

**Actor glyphs**: every row carries a human or bot mark in a trailing column,
showing who performs the step. Traditional is all human; the bot progressively
takes over the `Prompt —` steps, ending with the human authoring only workflows
and requirements. In progress — Traditional done, stages 2–6 pending.

Open items:
- [x] Author the loop SVG diagrams (seven: skeleton + 1–6) in `assets/loops/` — wiring into placeholders still open for the slides agent.
- [ ] Decide whether stage 6 belongs here or after the Brownfield divider —
      it is outline-wise a Brownfield subsection, but it is the natural end of
      the progression. Currently in the stack, with a brownfield badge.

---

## 3 · Brownfield Projects — status: planned

Outline is one line: "Brownfield projects have more context baked in."

| # | Layout | Band | Content |
|---|---|---|---|
| — | L-03 divider | ink | "Brownfield Projects" |
| — | L-04 statement | canvas | The one line, given air |

---

## 4 · Conventions — status: planned

Now a top-level section in the outline (it used to sit under Brownfield).
"How to add X" branches three ways.

| # | Layout | Band | Content |
|---|---|---|---|
| — | L-07 three-up | cloud | External interface (REST / GraphQL field / RPC-WS handler) · Infrastructure component · Tests and tiers (e2e / integration / unit) |

---

## 5 · Cool Tricks — status: planned · NEW SECTION

New in the revised outline. Four parallel scenarios, each with detail — too much
for one L-08, so: divider, then two slides.

| # | Layout | Band | Content |
|---|---|---|---|
| — | L-03 divider | ink | "Cool Tricks" |
| — | L-07 three-up | cloud | Refinement (Linear, structured English: user stories / EARS / Gherkin, INVEST splits) · Incidents (live logs + repo to triage; agents love red herrings) · Post mortems (generate monitoring dashboards) |
| — | L-06 two-column | canvas | Load testing and improving/revalidating + isolated worktrees for concurrent features (needs an isolated stack; requires workflow familiarity) |

Note: "Handle with care, agents love red herrings" is delivery commentary —
candidate for `<aside class="notes">` rather than slide text.

---

## 6 · Workflows — status: planned

| # | Layout | Band | Content |
|---|---|---|---|
| — | L-03 divider | ink | "Workflows" |
| — | L-04 statement | canvas | "It's about encoding what you do in prompts and then iterating automatically." |
| — | L-08 four-up | canvas | Tracking requirements · Refining tickets · Review cycle (adversarial, different model) · Drift check |
| — | L-07 three-up | cloud | Implementation process guidelines (TDD, testing tier preferences) · Clean code practices (general authoring, OO preferences) · Local preferences not enforceable by tooling |
| — | L-06 two-column | canvas | Dynamic vs static workflows — not everything needs to be fixed the same way; dev preferences; project differences |

**Outline gap:** line 125 reads "Local preferences not enforceable by [tooling?
— sentence looks cut off]". Needs the user's actual wording before it goes on a
slide. Do not guess.

---

## 7 · Existing Infrastructure — status: planned

| # | Layout | Band | Content |
|---|---|---|---|
| — | L-03 divider | ink | "Existing Infrastructure" |
| — | L-06 two-column | canvas | "Applies to anything that is managed by code" — how to add an infrastructure component: Terraform, CDK |

---

## 8 · Close — status: planned

| # | Layout | Band | Content |
|---|---|---|---|
| — | L-13 closing | ink | Required by the design system. Closing line still to be chosen — the drift-check question ("are requirements, code, and acceptance tests all aligned?") is the strongest candidate already in the outline. |

---

## Standing constraints

- Never invent content that is not in `outline.md`.
- Do not change the `Reveal.initialize` config (1280×720, `margin: 0`,
  `center: false`) — the theme's absolute px assume that stage.
- Verify over HTTP with hash deep-links, screenshot at 1280×720, and *read* the
  PNGs; a slide overflowing 720px is the failure no grep catches.
- Nothing committed yet; work lives on branch `presentations/ai-assisted-coding-intro`.
