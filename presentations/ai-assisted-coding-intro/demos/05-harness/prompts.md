# Demo 5 — Orchestrated harness

Concept: the loop is a pre-authored artifact, and it is *not* one black box. Five
checked-in commands split the work into phases, and every phase ends in something
you can read and disagree with — a spec, a clickable mock, an audit, a diff, a QA
report on a real pull request.

**The project lives in its own repo:** `github.com/galileopy/workflow-manager`
(Elm + Express, cloned locally at `~/Documents/repos/galileopy/workflow-manager`).
The five commands live there in `.claude/commands/` — that repo is the source of
truth for them, not this directory. This file is only the paste sheet.

Run everything from the workflow-manager checkout.

Show the harness first:

```sh
ls .claude/commands/
```

```sh
claude
```

## Phase 1 — PM drilling → `docs/spec.md`

```
/1-drill people keep asking me what actually happened in a run — I want to be able to see it
```

It asks you questions; your answers land in the spec's Decisions section. **This
is the beat that sells the demo** — the audience watches ambiguity get resolved
out loud instead of guessed at.

## Phase 2 — Prototype → a clickable HTML mock

```
/2-prototype
```

Open the file it writes in a browser and show it. Static, mock data, real
stylesheet — a screen that looks like the product before any of the product
exists.

## Phase 3 — Refine → `docs/spec.md` rewritten, with a Verification table

```
/3-refine
```

## Phase 4 — Implement → branch, failing tests first, code, PR

```
/4-implement
```

## Phase 5 — QA → `docs/qa-report.md`, posted to the PR

```
/5-qa
```

Exit the session, then show the trail:

```sh
git --no-pager diff main --stat
```

```sh
gh pr view --web
```

Say: this is five loops, each one checked in, each one leaving an artifact a
human can review. The spec was written before the code, the mock before the spec
was trusted, and the QA was done by something that was not allowed to read the
implementation. Nothing here is a black box — that is the point. This is the
"Once: author project workflows" line from the Level 5 slide.

Reset after rehearsal: in the workflow-manager repo, `git checkout main` and
delete the feature branch. Nothing in this deck's repo changes.
