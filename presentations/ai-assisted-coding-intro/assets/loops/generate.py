#!/usr/bin/env python3
"""Generate the six loop diagram SVGs for the AI-assisted-coding deck.

Seven fixed anchor slots sit clockwise around a circle, always in the same
place regardless of level:

    1 Design (optional)   2 Failing tests   3 Code   4 Run
    5 Test   6 Iterate    7 Refactor

A level that doesn't use a slot leaves it empty (no node, no arrow segment
through it). Three extra nodes sit outside the circle: pre-loop "Author
workflows" (L5 only), the "Specify requirements" start, and the "Until
requirements are satisfied" stop.

Run: python3 assets/loops/generate.py
"""
import math
import os

BLUE = "#024ad8"
INK = "#1a1a1a"
GRAPHITE = "#3d3d3d"
MUTE = "#636363"
STEEL = "#c2c2c2"
PALE = "#e8e8e8"
FOG = "#f7f7f7"
WHITE = "#ffffff"

FONT_SANS = "IBM Plex Sans, Helvetica Neue, Arial, sans-serif"
FONT_MONO = "IBM Plex Mono, ui-monospace, Menlo, monospace"

CX, CY, R = 420, 318, 200
NODE_W, NODE_H = 92, 54

# Glyph paths, drawn in a 24x24 box, stroke-based (except bot dots / run
# triangle which use fill). Matches the #i-human / #i-bot / #i-laptop sprite
# in index.html, redrawn as raw paths since the SVGs have no <use> targets.
GLYPH_HUMAN = '<path d="M12 3.5a3.6 3.6 0 1 0 0 7.2 3.6 3.6 0 0 0 0-7.2zM4.8 20.2c0-3.6 3.2-6 7.2-6s7.2 2.4 7.2 6" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
GLYPH_BOT = (
    '<circle cx="12" cy="2.8" r="1.3" fill="{c}"/>'
    '<path d="M12 4.1v2.1M2.6 11v3M21.4 11v3" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>'
    '<rect x="4.4" y="6.2" width="15.2" height="12" rx="3.2" fill="none" stroke="{c}" stroke-width="1.6"/>'
    '<circle cx="9.2" cy="12.2" r="1.35" fill="{c}"/>'
    '<circle cx="14.8" cy="12.2" r="1.35" fill="{c}"/>'
)
GLYPH_LAPTOP = (
    '<rect x="5" y="4.5" width="14" height="9.5" rx="1.5" fill="none" stroke="{c}" stroke-width="1.6"/>'
    '<path d="M2.5 17.5h19l-1.8 2.7a2 2 0 0 1-1.7.9H6a2 2 0 0 1-1.7-.9L2.5 17.5z" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
)

# Per-step glyphs (bespoke small icons, echoing the old files' style)
GLYPH_DESIGN = '<path d="M5 5h5v1.8H6.8V10H5V5zM14 5h5v5h-1.8V6.8H14V5zM5 14h1.8v3.2H10V19H5v-5zM17.2 14H19v5h-5v-1.8h3.2V14zM9.2 12l2.8-2.8L14.8 12 12 14.8z" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
GLYPH_FAILING = '<circle cx="12" cy="12" r="7.5" fill="none" stroke="{c}" stroke-width="1.7"/><path d="M9 9l6 6M15 9l-6 6" stroke="{c}" stroke-width="1.7" stroke-linecap="round"/>'
GLYPH_CODE = '<path d="M8.5 6.5 4.5 12l4 5.5M15.5 6.5l4 5.5-4 5.5" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
GLYPH_RUN = '<path d="M9 6.5l9.5 5.5L9 17.5z" fill="{c}" stroke="none"/>'
GLYPH_TEST = '<path d="M6 7h11M6 12h8M6 17h9M15.5 10.5l2 2 3.5-3.5" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
GLYPH_ITERATE = '<path d="M7.5 11.2a5.2 5.2 0 0 1 8.6-3.2M16.2 6.5V9h2.6M16.5 12.8a5.2 5.2 0 0 1-8.6 3.2M7.8 17.5V15H5.2M12 10.2v3.6M10.2 12h3.6" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
GLYPH_REFACTOR = '<path d="M6 6l5.5 5.5M13.5 13.5L18 18M6 18l4-4M14 10l4-4M9 9l1.5-1.5a2.1 2.1 0 0 1 3 0l0 0a2.1 2.1 0 0 1 0 3L12 12" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
GLYPH_START = '<path d="M6.2 6.2v11.2h5V21l4-3.6h4.6V6.2z" fill="none" stroke="{c}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
GLYPH_STOP = '<rect x="6" y="6" width="12" height="12" rx="2" fill="none" stroke="{c}" stroke-width="1.7"/>'
GLYPH_WORKFLOW = '<circle cx="6" cy="6" r="2.4" fill="none" stroke="{c}" stroke-width="1.6"/><circle cx="18" cy="6" r="2.4" fill="none" stroke="{c}" stroke-width="1.6"/><circle cx="12" cy="18" r="2.4" fill="none" stroke="{c}" stroke-width="1.6"/><path d="M8.1 7.1L11 16M15.9 7.1L13 16M8.4 6h7.2" fill="none" stroke="{c}" stroke-width="1.4" stroke-linecap="round"/>'

def slot_pos(k):
    """k in 1..7, clockwise from top."""
    theta = math.radians(-90 + (k - 1) * (360 / 7))
    return CX + R * math.cos(theta), CY + R * math.sin(theta)

SLOTS = {k: slot_pos(k) for k in range(1, 8)}

START_POS = (CX, 55)
STOP_POS = (CX, 578)
PRE_POS = (150, 55)

ACTOR_FILL = {"human": STEEL, "bot": BLUE, "machine": PALE}
ACTOR_GLYPH = {"human": GLYPH_HUMAN, "bot": GLYPH_BOT, "machine": GLYPH_LAPTOP}
ACTOR_GLYPH_COLOR = {"human": WHITE, "bot": WHITE, "machine": GRAPHITE}


def fnum(v):
    return f"{v:.1f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def badge(cx, cy, actor):
    fill = ACTOR_FILL[actor]
    glyph_color = ACTOR_GLYPH_COLOR[actor]
    glyph = ACTOR_GLYPH[actor].format(c=glyph_color)
    gx, gy = cx - 11 * 0.62, cy - 11 * 0.62
    return (
        f'<circle cx="{fnum(cx)}" cy="{fnum(cy)}" r="11" fill="{fill}"/>'
        f'<g transform="translate({fnum(gx)} {fnum(gy)}) scale(0.62)">{glyph}</g>'
    )


def actor_badges(x, y, w, actors):
    """Place badges at the node's top-right corner. Two actors sit side by
    side, steel (human) then blue (bot), moving left so neither overlaps the
    rounded corner."""
    out = []
    n = len(actors)
    # rightmost badge center sits just inside the top-right corner
    base_cx = x + w - 14
    base_cy = y
    for i, actor in enumerate(actors):
        # lay out right-to-left so the last actor (bot, in H+B) stays at the
        # corner and the first (human) sits further left
        idx_from_right = n - 1 - i
        cx = base_cx - idx_from_right * 20
        out.append(badge(cx, base_cy, actor))
    return "".join(out)


def node(x, y, w, h, label, glyph, actors, marked=False, optional=False, tag=None, glyph_scale=0.81):
    parts = []
    if marked:
        fill, stroke, sw, label_fill = "#c9e0fc", BLUE, 2.0, INK
        text_glyph_color = BLUE
    else:
        fill, stroke, sw, label_fill = WHITE, STEEL, 1.5, GRAPHITE
        text_glyph_color = GRAPHITE
    dash = ' stroke-dasharray="4 3"' if optional else ""
    parts.append(
        f'<rect x="{fnum(x)}" y="{fnum(y)}" width="{w}" height="{h}" rx="8" ry="8" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>'
    )
    glyph_size = 24 * glyph_scale
    gx = x + (w - glyph_size) / 2
    gy = y + 9
    gcolor = text_glyph_color
    parts.append(
        f'<g transform="translate({fnum(gx)} {fnum(gy)}) scale({glyph_scale})" '
        f'fill="none" stroke="{gcolor}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
        f'{glyph.format(c=gcolor)}</g>'
    )
    label_y = y + h - 8
    parts.append(
        f'<text x="{fnum(x + w / 2)}" y="{fnum(label_y)}" text-anchor="middle" '
        f'font-family="{FONT_SANS}" font-size="11" font-weight="500" letter-spacing="0.16" '
        f'fill="{label_fill}">{label}</text>'
    )
    # tags: optional (graphite) and/or marked (blue) mono captions below node,
    # stacked so they never collide with each other
    tag_y = y + h + 15
    if optional:
        parts.append(
            f'<text x="{fnum(x + w / 2)}" y="{fnum(tag_y)}" text-anchor="middle" '
            f'font-family="{FONT_MONO}" font-size="9" letter-spacing="0.32" fill="{MUTE}">optional</text>'
        )
        tag_y += 13
    if tag:
        parts.append(
            f'<text x="{fnum(x + w / 2)}" y="{fnum(tag_y)}" text-anchor="middle" '
            f'font-family="{FONT_MONO}" font-size="9" letter-spacing="0.32" fill="{BLUE}">{tag}</text>'
        )
    parts.append(actor_badges(x, y, w, actors))
    return "".join(parts)


def wide_node(cx, cy, w, h, lines, glyph, actors, marked=False, glyph_scale=0.81):
    """Icon-left / text-right layout for the start and pre-loop nodes: their
    labels run two lines, so there is no room to stack an icon above the
    text the way the circle-slot nodes do without the icon riding into the
    first line. `lines` is a list of 1-2 strings, vertically centered as a
    block to the right of the icon."""
    x, y = cx - w / 2, cy - h / 2
    parts = []
    if marked:
        fill, stroke, sw, label_fill = "#c9e0fc", BLUE, 2.0, INK
    else:
        fill, stroke, sw, label_fill = WHITE, STEEL, 1.5, GRAPHITE
    gcolor = BLUE if marked else GRAPHITE
    parts.append(
        f'<rect x="{fnum(x)}" y="{fnum(y)}" width="{w}" height="{h}" rx="8" ry="8" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )
    glyph_size = 24 * glyph_scale
    icon_cx = x + 26
    gx = icon_cx - glyph_size / 2
    gy = cy - glyph_size / 2
    parts.append(
        f'<g transform="translate({fnum(gx)} {fnum(gy)}) scale({glyph_scale})" '
        f'fill="none" stroke="{gcolor}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
        f'{glyph.format(c=gcolor)}</g>'
    )
    text_cx = icon_cx + glyph_size / 2 + 14 + (w - 52 - glyph_size) / 2
    line_h = 14
    top = cy - (len(lines) - 1) * line_h / 2
    for i, line in enumerate(lines):
        parts.append(
            f'<text x="{fnum(text_cx)}" y="{fnum(top + i * line_h + 4)}" text-anchor="middle" '
            f'font-family="{FONT_SANS}" font-size="11" font-weight="500" letter-spacing="0.16" '
            f'fill="{label_fill}">{line}</text>'
        )
    parts.append(actor_badges(x, y, w, actors))
    return "".join(parts)


def arc_arrow(k_from, k_to, blue=False):
    """Draw the circle-spine arc between two adjacent slot angles (k in 1..7,
    wrapping 7->1)."""
    a0 = -90 + (k_from - 1) * (360 / 7)
    a1 = -90 + (k_to - 1) * (360 / 7)
    if a1 <= a0:
        a1 += 360
    # pull the arc endpoints in from the node centers so the arrowhead
    # doesn't sit under the box
    pad_deg = 12
    a0r, a1r = a0 + pad_deg, a1 - pad_deg
    x0 = CX + R * math.cos(math.radians(a0r))
    y0 = CY + R * math.sin(math.radians(a0r))
    x1 = CX + R * math.cos(math.radians(a1r))
    y1 = CY + R * math.sin(math.radians(a1r))
    color = BLUE if blue else STEEL
    d = f"M{fnum(x0)} {fnum(y0)} A{R} {R} 0 0 1 {fnum(x1)} {fnum(y1)}"
    # arrowhead
    tangent = math.radians(a1r + 90)
    hx, hy = math.cos(tangent), math.sin(tangent)
    px, py = -hy, hx
    tip = (x1, y1)
    base1 = (x1 - hx * 7 - px * 3.4, y1 - hy * 7 - py * 3.4)
    base2 = (x1 - hx * 7 + px * 3.4, y1 - hy * 7 + py * 3.4)
    head = f'<path d="M{fnum(tip[0])} {fnum(tip[1])} L{fnum(base1[0])} {fnum(base1[1])} L{fnum(base2[0])} {fnum(base2[1])} Z" fill="{color}"/>'
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>' + head
    )


def straight_arrow(p0, p1, color=STEEL, curve=None):
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    tipx, tipy = x1 - ux * 3, y1 - uy * 3
    startx, starty = x0 + ux * 3, y0 + uy * 3
    if curve:
        d = f"M{fnum(startx)} {fnum(starty)} Q{fnum(curve[0])} {fnum(curve[1])} {fnum(tipx)} {fnum(tipy)}"
        # tangent approx at end using curve control point
        tux, tuy = tipx - curve[0], tipy - curve[1]
        tl = math.hypot(tux, tuy)
        tux, tuy = tux / tl, tuy / tl
    else:
        d = f"M{fnum(startx)} {fnum(starty)} L{fnum(tipx)} {fnum(tipy)}"
        tux, tuy = ux, uy
    px, py = -tuy, tux
    base1 = (tipx - tux * 8 - px * 3.6, tipy - tuy * 8 - py * 3.6)
    base2 = (tipx - tux * 8 + px * 3.6, tipy - tuy * 8 + py * 3.6)
    head = f'<path d="M{fnum(tipx)} {fnum(tipy)} L{fnum(base1[0])} {fnum(base1[1])} L{fnum(base2[0])} {fnum(base2[1])} Z" fill="{color}"/>'
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round"/>' + head


NODE_SPEC = {
    1: ("Design", GLYPH_DESIGN),
    2: ("Failing tests", GLYPH_FAILING),
    3: ("Code", GLYPH_CODE),
    4: ("Run", GLYPH_RUN),
    5: ("Test", GLYPH_TEST),
    6: ("Iterate", GLYPH_ITERATE),
    7: ("Refactor", GLYPH_REFACTOR),
}


def build_svg(title, page_label, steps, start, stop, pre=None):
    """steps: dict slot -> {"actors": [...], "marked": bool, "optional": bool}
    start/stop: {"actors":[...], "marked": bool}
    pre: {"actors":[...], "marked": bool} or None
    """
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600" '
        f'role="img" aria-label="{title}">'
    )
    parts.append(f"<title>{title}</title>")
    parts.append(f'<rect width="800" height="600" fill="{WHITE}"/>')
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{PALE}" stroke-width="1.1"/>')

    # arcs between consecutive present slots only (skip through empty ones,
    # connecting straight across the gap so the spine still reads as a loop)
    present = [k for k in range(1, 8) if k in steps]
    for i, k in enumerate(present):
        nxt = present[(i + 1) % len(present)]
        blue = steps[k]["marked"] or steps[nxt]["marked"]
        parts.append(arc_arrow(k, nxt, blue=blue))

    # start -> first present slot
    first_k = present[0]
    fx, fy = SLOTS[first_k]
    sx, sy = START_POS
    parts.append(straight_arrow((sx, sy + 24), (fx, fy - NODE_H / 2 - 4), color=BLUE if (start["marked"] or steps[first_k]["marked"]) else STEEL))
    # Stop is an unlinked exit condition -- it is not wired into the ring or
    # into any particular step, so it floats below the circle with no
    # connecting arrow. Likewise start is not part of the loop itself: the
    # only arrow drawn here is the single entry stroke into the first slot.
    ex, ey = STOP_POS

    # pre node -> start: both sit outside the loop, side by side above the
    # circle, so this is a short straight arrow rather than a curve that has
    # to detour around ring nodes.
    if pre:
        px, py = PRE_POS
        parts.append(straight_arrow((px + 66, py), (sx - 80, sy), color=BLUE if pre["marked"] else STEEL))
        parts.append(
            wide_node(px, py, 120, 54, ["Author", "workflows"], GLYPH_WORKFLOW, pre["actors"], marked=pre["marked"])
        )

    # start node
    parts.append(
        wide_node(sx, sy, 148, 54, ["Specify", "requirements"], GLYPH_START, start["actors"], marked=start["marked"])
    )

    # stop node (wide bar, no glyph -- matches earlier files' style)
    stop_fill = "#c9e0fc" if stop["marked"] else FOG
    stop_stroke = BLUE if stop["marked"] else PALE
    stop_text_fill = INK if stop["marked"] else MUTE
    parts.append(
        f'<rect x="{ex - 148}" y="{ey - 15}" width="296" height="30" rx="4" fill="{stop_fill}" stroke="{stop_stroke}" stroke-width="1.25"/>'
        f'<text x="{fnum(ex)}" y="{fnum(ey + 4)}" text-anchor="middle" font-family="{FONT_SANS}" font-size="11" fill="{stop_text_fill}">Until requirements are satisfied</text>'
    )
    parts.append(actor_badges(ex - 148, ey - 15, 296, stop["actors"]))
    if stop["marked"]:
        parts.append(
            f'<text x="{fnum(ex)}" y="{fnum(ey + 28)}" text-anchor="middle" font-family="{FONT_MONO}" font-size="9" letter-spacing="0.32" fill="{BLUE}">changed</text>'
        )

    # circle slot nodes
    for k in range(1, 8):
        if k not in steps:
            continue
        label, glyph = NODE_SPEC[k]
        cx, cy = SLOTS[k]
        st = steps[k]
        parts.append(
            node(
                cx - NODE_W / 2,
                cy - NODE_H / 2,
                NODE_W,
                NODE_H,
                label,
                glyph,
                st["actors"],
                marked=st["marked"],
                optional=st.get("optional", False),
                tag=st.get("tag"),
            )
        )

    parts.append("</svg>")
    return "\n".join(parts)


def step(actors, marked=False, optional=False):
    tag = "changed" if marked else None
    return {"actors": actors, "marked": marked, "optional": optional, "tag": tag}


def added_step(actors, optional=False):
    return {"actors": actors, "marked": True, "optional": optional, "tag": "added"}


LEVELS = []

# Level 0 -- Traditional
LEVELS.append(dict(
    file="loop-01-traditional.svg",
    title="Traditional Feedback Loop",
    page="1 of 6",
    steps={
        1: step(["human"], optional=True),
        2: step(["human"]),
        3: step(["human"]),
        4: step(["machine"]),
        5: step(["human"]),
        6: step(["human"]),
        7: step(["human"]),
    },
    start=step(["human"]),
    stop=step(["human"]),
    pre=None,
))

# Level 1 -- AI Assisted Coding
LEVELS.append(dict(
    file="loop-02-ai.svg",
    title="AI Assisted Coding Feedback Loop",
    page="2 of 6",
    steps={
        1: step(["human"], optional=True),
        2: step(["human"]),
        3: step(["bot"], marked=True),
        4: step(["machine"]),
        5: step(["human"]),
        6: step(["human"]),
        7: step(["human"]),
    },
    start=step(["human"]),
    stop=step(["human"]),
    pre=None,
))

# Level 2 -- Autonomous
LEVELS.append(dict(
    file="loop-03-autonomous.svg",
    title="Autonomous Feedback Loop",
    page="3 of 6",
    steps={
        1: step(["human"], optional=True),
        2: step(["human"]),
        3: step(["bot"]),
        4: step(["machine"]),
        5: step(["bot"], marked=True),
        6: step(["bot"], marked=True),
        7: step(["human"]),
    },
    start=step(["human"]),
    stop=step(["human"]),
    pre=None,
))

# Level 3 -- TDD
LEVELS.append(dict(
    file="loop-04-tdd.svg",
    title="Test Driven Feedback Loop",
    page="4 of 6",
    steps={
        1: step(["human"], optional=True),
        2: step(["bot"], marked=True),
        3: step(["bot"]),
        4: step(["machine"]),
        5: step(["bot"]),
        6: step(["bot"]),
        7: step(["human", "bot"], marked=True),
    },
    start=step(["human"]),
    stop=step(["human"]),
    pre=None,
))

# Level 4 -- Spec Driven
LEVELS.append(dict(
    file="loop-05-spec.svg",
    title="Spec Driven Feedback Loop",
    page="5 of 6",
    steps={
        1: step(["human", "bot"], marked=True),
        2: step(["bot"]),
        3: step(["bot"]),
        4: step(["machine"]),
        5: step(["bot"]),
        6: step(["bot"]),
        7: step(["bot"], marked=True),
    },
    start=step(["human", "bot"], marked=True),
    stop=step(["human", "bot"], marked=True),
    pre=None,
))

# Level 5 -- Spec Driven, Predefined Workflows
LEVELS.append(dict(
    file="loop-06-workflows.svg",
    title="Spec Driven Feedback Loop With Predefined Workflows",
    page="6 of 6",
    steps={
        1: step(["bot"], marked=True),
        2: step(["bot"]),
        3: step(["bot"]),
        4: step(["machine"]),
        5: step(["bot"]),
        6: step(["bot"]),
        7: step(["bot"]),
    },
    start=step(["human", "bot"]),
    stop=step(["human", "bot"]),
    pre=added_step(["human", "bot"]),
))


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    for lvl in LEVELS:
        svg = build_svg(lvl["title"], lvl["page"], lvl["steps"], lvl["start"], lvl["stop"], lvl["pre"])
        path = os.path.join(out_dir, lvl["file"])
        with open(path, "w") as f:
            f.write(svg + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
