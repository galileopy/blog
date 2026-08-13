# Demo 2 — Autonomous fix

Concept: delegation extends to run–test–iterate. We start with one failing test.
The bug is a regression trap: the obvious fix turns a different, passing test
red, so Claude has to notice its first attempt was wrong and adjust. That second
iteration is the demo — self-correction, not just delegation. We only review the
diff.

Paste in order, from `demos/02-autonomous-fix/wfm/`:

```sh
npm test
```

```sh
claude --allowedTools "Read,Edit,Bash(npm test)"
```

Then paste into the session:

```
npm test has one failing test. Find the bug, fix it, and re-run npm test until everything passes. Do not modify the tests.
```

Exit the session (`/exit`), then:

```sh
git --no-pager diff
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
