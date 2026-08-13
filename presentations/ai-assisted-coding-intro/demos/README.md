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

| Dir | Demo | Spectrum stage | Loop level | Pre-made | You paste |
|---|------|---|---|---|---|
| `01-comments-to-code/` | Comments to code | 2 | 1 | stubbed `advance()` with an intent comment; human-written failing tests | one prompt; `Bash` is denied, so **you** run the tests |
| `02-autonomous-fix/` | Autonomous debugging | 4 | 2 | an off-by-one in `advance()`; suite ships **green**, nothing covers completion | a user's bug report; it writes the missing test, runs it red, fixes, runs green |
| `03-tdd/` | TDD | 5 | 3 | library with failure handling, no `skip()` | one requirement paragraph; it writes failing tests first |
| `04-spec-driven/` | Spec driven | 5 | 4 | library with `skip()`, no CLI | one design prompt in plan mode; approve, it executes |
| `05-harness/` | Orchestrated harness | 8 | 5 | full CLI **plus** `.claude/commands/feature.md` (the loop as an artifact) | one line: `/feature <goal>` |

The rungs differ by *who closes the loop*, not by task size: at demo 1 the model
cannot run anything and you verify its work; from demo 2 on it runs the tests
itself; by demo 5 the loop is a checked-in artifact and you supply only a goal. Spectrum stages 1
(tab completion) and 3 (chat-and-copy) are editor/browser experiences that
don't demo well in a CLI, so the ladder starts at comments-to-code.

## Recording

```sh
# from demos/
./record.sh 01-comments-to-code      # wraps: asciinema rec casts/<name>.cast
```

- Terminal at 120×30, plain prompt, projector-sized font.
- One cast per demo, overwritten on re-record; replay with
  `asciinema play casts/<name>.cast` — space pauses, `.` steps a frame while
  paused, **`q` quits**. Quit with `q`, not Ctrl+C: interrupting the player
  leaves the terminal in a raw state that spews escape codes, recoverable with
  `reset`. Long model pauses review faster with `-s 2 -i 0.5` (double speed,
  idle capped at half a second).
- After any rehearsal, reset with the demo's own reset line (bottom of its
  `prompts.md`) — each snapshot is checked in, so reset is just git.
