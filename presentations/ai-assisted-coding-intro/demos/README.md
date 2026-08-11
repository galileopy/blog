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
| `01-comments-to-code/` | Comments to code | 2 | 1 | stubbed `advance()` with an intent comment; human-written failing tests | one `claude -p` prompt; run tests yourself |
| `02-autonomous-fix/` | Autonomous fix | 4 | 2 | seeded bug (never sets `completed`); one failing human test | one `claude -p` prompt; it loops to green |
| `03-tdd/` | TDD | 5 | 3 | clean library, no `skip()` | one requirement paragraph; it writes failing tests first |
| `04-spec-driven/` | Spec driven | 5 | 4 | library with `skip()`, no CLI | one design prompt in plan mode; approve, it executes |
| `05-harness/` | Orchestrated harness | 8 | 5 | full CLI **plus** `.claude/commands/feature.md` (the loop as an artifact) | one line: `/feature <goal>` |

What's pre-made shrinks from "the test" to "nothing", then becomes "the loop
itself"; what you type shrinks to a single goal statement. Spectrum stages 1
(tab completion) and 3 (chat-and-copy) are editor/browser experiences that
don't demo well in a CLI, so the ladder starts at comments-to-code.

## Recording

```sh
# from demos/
./record.sh 01-comments-to-code      # wraps: asciinema rec casts/<name>.cast
```

- Terminal at 120×30, plain prompt, projector-sized font.
- One cast per demo, overwritten on re-record; replay with
  `asciinema play casts/<name>.cast` (space pauses, `.` steps).
- After any rehearsal, reset with the demo's own reset line (bottom of its
  `prompts.md`) — each snapshot is checked in, so reset is just git.
