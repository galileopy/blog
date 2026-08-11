# Demo 5 — Orchestrated harness

Concept: the loop itself is a pre-authored artifact. `.claude/commands/feature.md`
encodes requirement → tests → code → verify. On camera we type one line: the goal.

Paste in order, from `demos/05-harness/wfm/`:

```sh
cat .claude/commands/feature.md
```

```sh
claude
```

Then paste into the session:

```
/feature add a "log" command to the CLI that prints each resolved step in order, one line per step, as "done: <title>" or "skipped: <title>", and "nothing resolved yet" when no step has been resolved
```

Let it run the whole loop. Exit, then:

```sh
npm test
```

```sh
node src/cli.js init release build test ship
node src/cli.js advance
node src/cli.js skip test
node src/cli.js log
```

Say: everything we did by hand in demos 1–4 is now steps in a checked-in file —
the workflow is versioned, reviewable, and reusable by the whole team. This is
the "Once: author project workflows" line from the Level 5 slide.

Reset after rehearsal (from repo root):
```sh
git checkout -- presentations/ai-assisted-coding-intro/demos/05-harness && git clean -fd presentations/ai-assisted-coding-intro/demos/05-harness
```
