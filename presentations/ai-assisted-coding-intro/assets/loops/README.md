# Feedback loop diagrams

Six 4:3 SVGs for the Feedback Loops vertical stack (left card).

| File | Slide |
|---|---|
| `loop-01-traditional.svg` | 1 of 6 Traditional |
| `loop-02-ai.svg` | 2 of 6 AI |
| `loop-03-autonomous.svg` | 3 of 6 Autonomous |
| `loop-04-tdd.svg` | 4 of 6 TDD |
| `loop-05-spec.svg` | 5 of 6 Spec driven |
| `loop-06-workflows.svg` | 6 of 6 Spec + workflows |

**Visual system**
- Stable circular spine; nodes grow as the loop deepens
- `added` / `changed` / `varies` → primary blue fill + mono tag (mirrors `li.diff-move`)
- `optional` → dashed stroke, graphite tag
- Short labels + stroke glyphs; full copy stays on the right column
- Tokens from galileo theme (`#024ad8`, `#1a1a1a`, `#636363`, …)

**Wiring** (other agent): replace `.ph.ph-4x3` with e.g.
```html
<img class="loop-diagram" src="assets/loops/loop-02-ai.svg" alt="AI feedback loop">
```
Regenerate: `python3 assets/loops/generate.py` (if present) or re-run the authoring script.
