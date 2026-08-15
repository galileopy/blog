# Demo 5 — take sheet

Feature: **create a run from the page.** Scope capped in the request itself, so
the drill cannot explode it into routing.

Session: `tmux attach -t demo` (100×27, already in the repo, sized manually so
attaching will not resize it).

## Before recording

```sh
claude
```

Launch it once and dismiss any first-run trust prompt, then `/exit`. That dialog
firing mid-take is the ugliest possible interruption. Do this **outside** the
recording.

## Record

```sh
asciinema rec --overwrite ~/Documents/repos/galileopy/blog/presentations/ai-assisted-coding-intro/demos/casts/05-harness.cast
```

Then, inside the recording:

```sh
ls .claude/commands/
```

```sh
claude
```

## Phase 1 — drill (already on your clipboard)

```
/1-drill I can't create a run from the app at all — I have to use curl to make one. I want to do it from the page. Keep it inline on the runs page, no new pages or routing.
```

It asks questions; you answer. Expect the two real ones: how steps get entered
(one field, multiline, add-a-row) and what happens when two steps share a title.
Answer as a product person would, not as an engineer. **This is the beat that
sells the demo** — the audience watches ambiguity get resolved out loud.

## Phases 2–5

```
/2-prototype
```

Open the HTML file it writes, in a browser, on camera.

```
/3-refine
```

```
/4-implement
```

```
/5-qa
```

## After

```sh
git --no-pager diff main --stat
```

```sh
gh pr view --web
```

Stop the recording with **Ctrl-D** or `exit` — not Ctrl-C.

## If /4-implement halts

It stops when `app/main-elm.js` was not rebuilt, printing "the feature is
invisible to the user no matter what the tests say". That is the harness working,
not the model failing. Narrate it as such — it is the best unscripted moment
available, and the deck says the same thing in the same words.

## Reset for a re-take

```sh
git checkout main && git branch -D <feature-branch> && git clean -fd docs/
```
