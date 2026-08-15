# Demo 5 — take sheet

Feature: **create a run from the page.** Scope capped in the request itself, so
the drill cannot explode it into routing.

Repo: `~/Documents/repos/galileopy/workflow-manager`. Ticket: **COFFE-14**.
Session: `tmux attach -t demo` (100×28, sized manually so attaching will not
resize it).

The loop ships as a local plugin in that repo — `plugins/craft/`. The five
phases spell **CRAFT**, and each one posts its artifact as a comment on the
ticket, opening with the command that produced it. Nothing lands in the repo but
code and tests.

**One command runs the whole thing.** That is the demo. `/craft:start` is the
orchestrator: it dispatches each phase in turn as a cold subagent. Typing the
five phases by hand would show the audience a person driving the loop, which is
the opposite of the claim being made.

## Before recording

```sh
claude
```

Launch it once and dismiss any first-run trust prompt, then `/exit`. That dialog
firing mid-take is the ugliest possible interruption. Do this **outside** the
recording.

Confirm the plugin is live — type `/craft:` and check six entries complete. If
they do not, the installed copy is a stale cached snapshot; see the reinstall
note at the bottom.

## Record

```sh
asciinema rec --overwrite ~/Documents/repos/galileopy/blog/presentations/ai-assisted-coding-intro/demos/casts/05-harness.cast
```

Then, inside the recording:

```sh
claude
```

```
/craft:start COFFE-14
```

That is the whole run.

## What you do while it runs

**Collect** is the only phase that needs you, and it is the beat that sells the
demo — the audience watches ambiguity get resolved out loud. Expect two real
questions: how steps get entered (one field, multiline, add-a-row) and what
happens when two steps share a title. Answer as a product person would, not as
an engineer.

The second question is not decoration. `server/workflow.mjs` matches steps by
title and takes the first hit, so two steps sharing a name silently target the
wrong one. The drill surfaces that from the requirements side, before any code
is read.

**Render** writes a clickable HTML mock. Open it in a browser, on camera, before
any code exists.

**Audit, forge, test** run without you.

## After

```sh
git --no-pager diff main --stat
```

Then open COFFE-14 in Linear on camera — five comments, one per phase, in order.
That is the artifact trail, and it is the point of the demo.

## If forge halts

It stops when `app/main-elm.js` was not rebuilt, printing that the feature is
invisible to the user no matter what the tests say. That is the harness working,
not the model failing. Narrate it as such — it is the best unscripted moment
available, and the deck says the same thing in the same words.

The stale-plugin trap has the identical shape: `claude plugin update` compares
versions, not content, so an edited command can sit in the repo while the old
text is what runs. Same lesson, two places in one repo.

If you show that trap live, grep the **version-pinned** plugin path, not the
cache root. The cache keeps old versions beside new ones, so a grep across the
root surfaces stale text from a version nothing is loading — you would
"reproduce" a bug that is already fixed and have to talk your way out of it.

## If start stalls mid-flow

The five phases run standalone and pick up where it stopped:

```
/craft:collect COFFE-14
```

```
/craft:render
```

```
/craft:audit
```

```
/craft:forge
```

```
/craft:test
```

## Reset for a re-take

```sh
git checkout main && git branch -D <feature-branch> && rm -rf .artifacts/
```

The Linear comments on COFFE-14 do **not** reset — delete them by hand, or the
next run posts a sixth, seventh, eighth comment onto the same ticket.

## If /craft: does not complete

The installed plugin is a cached snapshot and `update` only fires on a version
bump. Force it:

```sh
claude plugin uninstall craft@workflow-manager
```

```sh
claude plugin install craft@workflow-manager
```
