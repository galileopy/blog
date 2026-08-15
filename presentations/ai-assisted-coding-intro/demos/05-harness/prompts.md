# Demo 5 — Orchestrated harness

Concept: the loop itself is a pre-authored artifact. `.claude/commands/feature.md`
encodes requirement → tests → code → verify. On camera we type one line: the goal.

Picks up exactly where demo 2 left off — same project, same 13 green tests.

Paste in order, from `demos/05-harness/wfm/`:

```sh
cat .claude/commands/feature.md
```

```sh
npm test
```

```sh
claude
```

Then paste into the session:

```
/feature add a skip(workflow, title) function that marks a pending step as "skipped" instead of running it, leaves everything else untouched, and counts as resolved so a run whose remaining steps are all skipped is completed
```

Let it run the whole loop — requirements, failing tests, implementation, green.
Exit, then:

```sh
git --no-pager diff
```

```sh
npm test
```

Say: in demo 2 we drove that loop by hand — reproduce, fix, verify. Here the
same loop is a checked-in file, so it is versioned, reviewable, and reusable by
the whole team. This is the "Once: author project workflows" line from the
Level 5 slide.

Reset after rehearsal (from repo root):
```sh
git checkout -- presentations/ai-assisted-coding-intro/demos/05-harness && git clean -fd presentations/ai-assisted-coding-intro/demos/05-harness
```
