#!/usr/bin/env python3
"""Generate the Part 2 intro diagram: three timelines of sparse points.

Underlying idea: an LLM is next-token prediction. Each lane is a run left to
right toward the same goal on the right edge — the paths differ, not the target.

The axis across the three lanes is WHEN THE CORRECTION WAS AUTHORED, not who
applies it:

Lane 1 "Correct as you go" — authored during the run, reactively. Nothing exists
before the run starts. Ten dots.
Lane 2 "Plan first, then execute" — authored at the start of the run. The plan
lays down checkpoints that fire as the run passes them, but it is single-use and
does not survive contact: four interventions remain.
Lane 3 "Reusable workflow" — authored before the run and reused across runs
(stencils, checkers, spec generators). The only human act is setting the goal:
one dot, at the start.

Glyphs carry one meaning each, and it does not shift between lanes:
  violet dot   — unplanned human intervention (gets rarer down the lanes)
  blue diamond — a checkpoint from a plan (NOT a self-applied correction)
  dotted ring  — a pre-authored step: existed before this run, outlives it

Run: python3 generate.py > timelines.svg
"""

W, H = 1104, 470
LANE_Y = {1: 92, 2: 238, 3: 384}
GOAL_X = 1030
START_X = 78

# Colours (theme/galileo.css). Everything is a theme token EXCEPT the violet on
# the intervention dots: the palette carries one accent (blue) and neutrals, and
# the diagram needs two accents that separate at slide distance.
HUMAN = "#3F00DB"       # unplanned human intervention. NOT a theme token — the
                        # palette has no second accent, and every in-palette
                        # alternative either collided with the diamonds or went
                        # too light to read. Candidate for --gp-violet.
STORM = "#356373"       # --gp-storm-deep, pre-authored step rings
BLUE = "#024ad8"        # --gp-primary, plan checkpoints
INK = "#1a1a1a"         # --gp-ink, the connecting line
GRAPHITE = "#636363"    # --gp-graphite, labels
STEEL = "#c2c2c2"       # --gp-steel, goal ring and ideal line
CANVAS = "#ffffff"      # --gp-canvas, knockout behind the step rings

MANUAL, SELF, STEP = "manual", "self", "step"

# Each lane: (dx from START_X, dy from the lane centre line, kind).
# Lane 1 "Correct as you go" — every correction is an unplanned intervention.
LANE_1 = [
    (0, 0, MANUAL),
    (84, -38, MANUAL),
    (132, 26, MANUAL),
    (246, -14, MANUAL),
    (300, -52, MANUAL),
    (438, 18, MANUAL),
    (612, -30, MANUAL),
    (676, 8, MANUAL),
    (810, -44, MANUAL),
    (900, -6, MANUAL),
]

# Lane 2 "Plan first, then execute" — plan checkpoints are dense and close the
# small deviations; four unplanned interventions remain, at the bigger swings.
# Those four are the point of the lane, not a blemish: a plan authored up front
# does not survive contact with the run.
#
# Spacing and amplitude are deliberately irregular: gaps run 12–62px, runs of
# two or three points drift the same direction before turning, and amplitudes
# vary 2–30px. A strict alternation reads as a sawtooth waveform — a mechanical
# rhythm — instead of corrections landing where the run actually needs them.
LANE_2 = [
    (0, 0, MANUAL),
    (34, -13, SELF),
    (52, -21, SELF),
    (96, 7, SELF),
    (138, -3, SELF),
    (152, -11, SELF),
    (198, 13, SELF),
    (262, -40, MANUAL),
    (288, -27, SELF),
    (330, -31, SELF),
    (374, -9, SELF),
    (392, -15, SELF),
    (444, 11, SELF),
    (472, 3, SELF),
    (548, 34, MANUAL),
    (578, 21, SELF),
    (600, 27, SELF),
    (644, -2, SELF),
    (702, 9, SELF),
    (718, 2, SELF),
    (762, -13, SELF),
    (838, -32, MANUAL),
    (868, -21, SELF),
    (902, -27, SELF),
]


# Lane 3 "Reusable workflow" — the single dot at the start is the human
# setting the goal, and it is the only thing they do. Plan checkpoints still run
# (the workflow generates the plan), plus pre-authored steps (STEP) firing at
# a regular cadence of 148px. The run ends on a step at 888, clear of the goal
# ring — no lane may place a correction on top of the goal. Self-applied
# corrections still run between the steps, irregular as in lane 2 but at a
# smaller amplitude: each step pulls the run back to the ideal line, so it never
# gets far enough out to need a big swing.
LANE_3 = [
    (0, 0, MANUAL),
    (38, -11, SELF),
    (72, -16, SELF),
    (110, 5, SELF),
    (148, -2, STEP),
    (186, 9, SELF),
    (232, 14, SELF),
    (248, 6, SELF),
    (268, -9, SELF),
    (296, 2, STEP),
    (350, -12, SELF),
    (396, -17, SELF),
    (430, -6, SELF),
    (444, -1, STEP),
    (504, 8, SELF),
    (546, 15, SELF),
    (566, 4, SELF),
    (592, 0, STEP),
    (660, -10, SELF),
    (700, -15, SELF),
    (724, -5, SELF),
    (740, 3, STEP),
    (818, 11, SELF),
    (858, 16, SELF),
    (888, -1, STEP),
]


def points(lane, spec):
    y0 = LANE_Y[lane]
    return [(START_X + dx, y0 + dy, kind) for dx, dy, kind in spec]


def polyline(pts):
    """Straight segments hitting every point exactly — a path, not a curve."""
    head = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
    return head + "".join(f" L {x:.1f} {y:.1f}" for x, y in pts[1:])


def goal(y):
    return f"""  <g class="goal">
    <circle cx="{GOAL_X}" cy="{y}" r="17" fill="none" stroke="{STEEL}" stroke-width="2"/>
    <circle cx="{GOAL_X}" cy="{y}" r="7" fill="{INK}"/>
  </g>"""


def glyph(x, y, kind, diamond=None):
    """Intervention = purple dot. Plan checkpoint = blue diamond. Step = ring.

    The step ring is filled canvas-white so the connecting line does not show
    through it — the run passes through the step, it does not cut across it.
    """
    if kind == MANUAL:
        return f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="7.5" fill="{HUMAN}"/>'
    if kind == STEP:
        return (f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{CANVAS}"'
                f' stroke="{STORM}" stroke-width="1.5" stroke-dasharray="2 3.2"/>')
    r = 5.75
    pts = f"{x:.1f},{y - r:.1f} {x + r:.1f},{y:.1f} {x:.1f},{y + r:.1f} {x - r:.1f},{y:.1f}"
    return f'  <polygon points="{pts}" fill="{diamond or BLUE}"/>'


def label(cy, text):
    return (f'  <text x="{START_X}" y="{cy - 74}" fill="{GRAPHITE}"'
            ' font-family="IBM Plex Sans, Helvetica Neue, Arial, sans-serif"'
            f' font-size="19" font-weight="400" letter-spacing="0.02em">{text}</text>')


def ideal(n, y=None):
    """The straight shot from start to goal — the run nobody actually takes."""
    y = LANE_Y[n] if y is None else y
    return (f'  <line x1="{START_X}" y1="{y}" x2="{GOAL_X - 17}" y2="{y}"'
            f' stroke="{STEEL}" stroke-width="1.5" stroke-dasharray="2 6"'
            ' stroke-linecap="round"/>')


def lane(n, spec, text, diamond=None, y=None):
    pts = points(n, spec) if y is None else\
        [(START_X + dx, y + dy, k) for dx, dy, k in spec]
    cy = LANE_Y[n] if y is None else y
    xy = [(px, py) for px, py, _ in pts] + [(GOAL_X - 17, cy)]
    parts = [ideal(n, cy),
             f'  <path d="{polyline(xy)}"',
             f'        fill="none" stroke="{INK}" stroke-width="1.5"',
             '        stroke-linecap="round" stroke-linejoin="round"/>']
    parts += [glyph(px, py, kind, diamond) for px, py, kind in pts]
    parts.append(goal(cy))
    parts.append(label(cy, text))
    return "\n".join(parts)


def build(diamond=None, fragments=False):
    """fragments=True wraps lanes 2 and 3 as reveal.js fragments, so the slide
    introduces the three runs one at a time. Lane 1 is always visible: the slide
    should not open on an empty stage."""
    def frag(markup):
        return f'<g class="fragment fade-in">\n{markup}\n</g>' if fragments else markup

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"
     width="{W}" height="{H}" role="img" aria-label="Three timelines toward one goal">
{lane(1, LANE_1, "Correct as you go", diamond)}

{frag(lane(2, LANE_2, "Plan first, then execute", diamond))}

{frag(lane(3, LANE_3, "Reusable workflow", diamond))}
</svg>
"""


if __name__ == "__main__":
    print(build(), end="")
