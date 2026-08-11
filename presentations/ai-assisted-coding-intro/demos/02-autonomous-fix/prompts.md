# Demo 2 — Autonomous fix

Concept: delegation extends to run–test–iterate. A human-written test is failing
(the seeded bug: `advance()` never marks the workflow completed). Claude fixes,
runs the tests itself, and loops until green. We only review the diff.

Paste in order, from `demos/02-autonomous-fix/wfm/`:

```sh
npm test
```

```sh
claude -p "npm test has one failing test. Find the bug, fix it, and re-run npm test until everything passes. Do not modify the tests." --allowedTools "Read,Edit,Bash(npm test)"
```

```sh
git diff
```

```sh
npm test
```

Say: we didn't run the loop this time — it did. We still read the diff. Note the
guardrail: it may not touch the tests. Segue: "next, it writes the tests too."

Reset after rehearsal (from repo root):
```sh
git checkout -- presentations/ai-assisted-coding-intro/demos/02-autonomous-fix && git clean -fd presentations/ai-assisted-coding-intro/demos/02-autonomous-fix
```
