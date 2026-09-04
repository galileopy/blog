# Demos — climbing the delegation ladder

Live/recorded demos for the talk, one per rung of the delegation spectrum, all
run with Claude Code in a terminal and recorded with asciinema. Everything is
pre-staged: on stage you only paste lines from the demo's `prompts.md`, in order.

Subject project: `wfm` — a tiny workflow manager CLI (dogfooding: we use AI
workflows to build a workflow manager). Node, zero dependencies, `npm test`.

## Layout

Each demo directory is a frozen snapshot: its `wfm/` is the *end state of the
previous demo*, pre-staged with whatever that rung needs, plus a `prompts.md`
paste sheet with the exact commands, prompts, talking points, and reset line.

**Only two demos are recorded for the talk.** Stage time is short, so the ladder
is cut to its two endpoints — the loop driven by hand, then the same loop as a
checked-in artifact.

| Dir | Demo | Spectrum stage | Loop level | Pre-made | You paste |
|---|------|---|---|---|---|
| `02-autonomous-fix/` | Autonomous debugging | 4 | 2 | an off-by-one in `advance()`; suite ships **green**, nothing covers completion | a user's bug report; it writes the missing test, runs it red, fixes, runs green |
| `05-harness/` | Orchestrated harness | 8 | 5 | demo 2's end state **plus** `.claude/commands/feature.md` (the loop as an artifact) | one line: `/feature <goal>` |

The two demos run on continuous project state: demo 5's `wfm/` is exactly where
demo 2 finished, so the second cast picks up the first without a visible jump.
They differ by *who closes the loop*, not by task size — in demo 2 you supply the
bug report and read every step; in demo 5 the loop is a file and you supply only
a goal.

Cut, and why: `01-comments-to-code/` (the model can't run anything and you verify
by hand) is a cleaner Level 0 but shows the model doing *less*, which makes the
jump to a harness read as a cut rather than a climb. `03-tdd/` and
`04-spec-driven/` are absorbed — demo 2 already shows tests-before-fix, and
demo 5's `/feature` goal is the `skip()` requirement those two were built
around. Their directories are kept in the repo, unrecorded, in case time opens
up. Spectrum stages 1 (tab completion) and 3 (chat-and-copy) are editor/browser
experiences that don't demo well in a CLI.

## Recording

```sh
# from demos/
./record.sh 02-autonomous-fix        # wraps: asciinema rec casts/<name>.cast
```

- Terminal at **100×28**, plain prompt, projector-sized font. Taller than ~30
  rows letterboxes badly in the slide player at 1280×720 and shrinks the type
  past reading distance.
- One cast per demo, overwritten on re-record; replay with
  `asciinema play casts/<name>.cast` — space pauses, `.` steps a frame while
  paused, **`q` quits**. Quit with `q`, not Ctrl+C: interrupting the player
  leaves the terminal in a raw state that spews escape codes, recoverable with
  `reset`. Long model pauses review faster with `-s 2 -i 0.5` (double speed,
  idle capped at half a second).
- After any rehearsal, reset with the demo's own reset line (bottom of its
  `prompts.md`) — each snapshot is checked in, so reset is just git.
