# Demo 5 — Orchestrated harness

Concept: the loop is a pre-authored artifact, and it is *not* one black box. Five
checked-in commands split the work into phases, and every phase ends in a file
you can read — a spec, a mock, an audit, a diff, a QA report on a real PR.

Picks up where demo 2 left off: same project, 13 green tests.
Repo: `github.com/galileopy/workflow-manager`.

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

It will ask you questions. Answer them however you like; the answers land in the
spec's Decisions section. **This is the beat that sells the demo** — the audience
watches ambiguity get resolved out loud instead of guessed at.

## Phase 2 — Prototype → `docs/prototype.md`

```
/2-prototype
```

## Phase 3 — Refine → `docs/spec.md` rewritten, with a Verification table

```
/3-refine
```

## Phase 4 — Implement → branch, tests, code, PR

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

Say: demo 2 was one loop, driven by hand. This is five loops, each one checked
in, each one leaving an artifact a human can review. The spec was written before
the code, the mock before the spec was trusted, and the QA was done by something
that was not allowed to read the implementation. Nothing here is a black box —
that is the point. This is the "Once: author project workflows" line from the
Level 5 slide.

Reset after rehearsal (from repo root):
```sh
git checkout -- presentations/ai-assisted-coding-intro/demos/05-harness && git clean -fd presentations/ai-assisted-coding-intro/demos/05-harness
```
