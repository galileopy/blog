# SVG regeneration — spec + single agent prompt

The six loop diagrams were authored against a much older version of the step
list and have drifted badly. Rather than patching six files, we regenerate all
six from one script so the geometry is identical by construction and a future
outline change is a one-line edit plus a re-run.

Paste everything below the line into one Sonnet agent run.

---

# Task

Write `assets/loops/generate.py` and use it to regenerate the six loop diagrams
in `/home/galileo/Documents/repos/galileopy/blog/presentations/ai-assisted-coding-intro/assets/loops/`.

Read `outline.md` (the `### Feedback Loops: ... (Level N)` sections) and
`index.html` (the six `<section class="s-canvas layout-loop">` slides) first.
The diagram must tell the same story as its slide's step list, in glyphs.
Where the existing SVGs disagree with the outline, the outline is right — they
predate almost all of it.

## The core idea: fixed slots

Seven anchor positions around the circle, in this fixed order clockwise from
top. Every level uses the same anchors; a level without a given step leaves
that slot **empty**.

| Slot | Step | Present at |
|---|---|---|
| 1 | Technical design *(optional)* | all |
| 2 | Failing tests | L3+ |
| 3 | Code | all |
| 4 | Run | all |
| 5 | Test | all |
| 6 | Iterate | all |
| 7 | Refactor | L3+ |

Nodes must therefore never move between levels — paging through the stack shows
steps *appearing in place*, never the loop rotating. This mirrors what the slide
list already does with hidden spacer rows.

Three elements sit **outside** the circle:
- `Specify requirements` — start, above the circle, arrow in
- `Until requirements are satisfied` — stop, below the circle
- `Author workflows` — pre-loop, left side, L5 only, arrow into the start

## Per-level spec

Actors: `H` human, `B` bot, `M` machine, `H+B` both. Marks: the stage's **own**
change only — `added` (new step) or `changed` (existing step, new actor).
A step that changed at an earlier level is NOT marked again.

**Level 0 — `loop-01-traditional.svg`** (slots 2, 7 empty)
```
start Specify requirements  H     design H (optional)   Code H
Run M    Test H    Iterate H      stop Until requirements... H
```
No marks at all — this is the baseline.

**Level 1 — `loop-02-ai.svg`** (slots 2, 7 empty)
```
As Level 0, except:  Code  B  [changed]
```

**Level 2 — `loop-03-autonomous.svg`** (slots 2, 7 empty)
```
Code B (carried, unmarked)   Test B [changed]   Iterate B [changed]
design H   Run M   start H   stop H
```
Two marked nodes is correct — the agent takes over testing and iterating in one
move.

**Level 3 — `loop-04-tdd.svg`** (all seven slots)
```
start H   design H (optional)   Failing tests B [added]   Code B
Run M   Test B   Iterate B   Refactor H+B [added]   stop H
```

**Level 4 — `loop-05-spec.svg`** (all seven slots)
```
start Specify requirements  H+B [changed]
design H (optional)   Failing tests B   Code B   Run M   Test B   Iterate B
Refactor B [changed]
stop Until requirements are satisfied  H+B [changed]
```
There is **no `Specs` node** — the old diagrams have one and it must not come
back. Generating the spec merged into the start edge at this level; a separate
node double-counts one activity.

**Level 5 — `loop-06-workflows.svg`** (all seven slots + pre-loop node)
```
pre  Author workflows  H+B [added]
start Specify requirements  H+B      design B [changed] (still optional)
Failing tests B   Code B   Run M   Test B   Iterate B   Refactor B
stop Until requirements are satisfied  H+B
```
End state: no purely-human node anywhere. Every node is B, M, or H+B.
Note the design node carries **both** the graphite `optional` tag and the blue
`changed` tag — make sure they do not collide.

## Visual rules

Actor badge: `<circle r="11">` at the node rect's top-right corner with a small
white stroke glyph inside at `scale(0.62)`. `loop-03-autonomous.svg` already has
one on its Code node — copy that construction, changing only fill and glyph.
Two badges (`H+B`) sit side by side, steel then blue, without overlapping the
node's rounded corner.

| Actor | Badge fill | Glyph |
|---|---|---|
| human | `#c2c2c2` | person (head + shoulders) |
| bot | `#024ad8` | robot (antenna + rounded head + two eyes) |
| machine | `#e8e8e8` | laptop (screen + base) — dark glyph, the fill is pale |
| human + bot | two badges | both, in that order |

Match the slide's SVG sprite (`#i-human`, `#i-bot`, `#i-laptop` in `index.html`)
so the same actor reads the same in both columns.

- Nodes: 92x54, `rx="8"`. Labels must fit — use the short names in the table
  above, never go below `font-size="11"`.
- `optional` → dashed stroke + graphite mono tag under the label.
- Marked node → blue `#024ad8` fill, white label, blue mono tag under it.
- Arrows: steel `#c2c2c2` by default. Only arrows adjacent to a marked node may
  be blue.
- Tokens only: `#024ad8` `#1a1a1a` `#3d3d3d` `#636363` `#c2c2c2` `#e8e8e8`
  `#f7f7f7` `#ffffff`. Fonts `IBM Plex Sans...` / `IBM Plex Mono...`, never
  embedded.
- Keep `viewBox="0 0 800 600"`, the white background rect, the circular spine,
  and each file's `<title>`.

## Verify — render and LOOK, do not trust the XML

```bash
cd /home/galileo/Documents/repos/galileopy/blog/presentations/ai-assisted-coding-intro
for f in assets/loops/loop-0[1-6]*.svg; do
  google-chrome --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --window-size=800,600 --virtual-time-budget=4000 \
    --screenshot="/tmp/$(basename $f .svg).png" "file://$PWD/$f"
done
```
Read every PNG. Check: no overlapping text, no label overflowing its box, every
badge the right colour and not clipped, arrows connecting the right nodes, empty
slots genuinely empty rather than leaving a stray arrow.

Then check them in place — **use a port Chrome allows; 5060 is blocked and
silently screenshots an error page**:
```bash
python3 -m http.server 5081 & sleep 1
for i in 0 1 2 3 4 5; do
  google-chrome --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --window-size=1280,720 --virtual-time-budget=6000 \
    --screenshot="/tmp/slide-$i.png" "http://localhost:5081/#/3/$i"
done
pkill -f "http.server 5081"
```
Read all six. For each, confirm the diagram's node labels and actor badges match
that slide's step list exactly — same names, same actors, same one-or-two things
marked. Then flip between Level 0 and Level 5 and confirm **no node moved**.

## Constraints

- Touch only `assets/loops/*.svg` and the new `generate.py`. Do NOT edit
  `index.html`, `outline.md`, `theme/galileo.css`, or `decisions.log`.
- Leave `loop-00-skeleton.svg` alone — it is orphaned (the skeleton slide was
  folded into Traditional) and nothing references it.
- Update `assets/loops/README.md`: it is stale (claims a seven-slide stack, calls
  Level 1 "AI", and references a `generate.py` that did not exist until now).
- Do not commit.

## Report

What the spec-to-script mapping looks like, what the renders showed, any place
the outline was ambiguous, and any node where the label genuinely would not fit.
