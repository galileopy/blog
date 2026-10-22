# Demo 2 — Autonomous debugging

Concept: the loop moves to the model. It gets a bug report in a user's words,
infers the test that should have caught it, runs it to see it fail, fixes the
code, and runs again to prove it. We only read the diff.

The seed is green — no test covers completion, which is exactly why the bug
shipped.

Paste in order, from `demos/02-autonomous-fix/wfm/`:

```sh
npm test
```

```sh
claude --allowedTools "Read,Edit,Write,Bash(npm test)"
```

Then paste into the session:

```
A user filed this bug: "I finished every step in my release run — all of them show done — but wfm never reports the run as completed. I have to advance one extra time, past the last step, before it flips." Reproduce it with a failing test first and run npm test so we can see it red, then fix the code and run the tests again. Do not change the existing tests.
```

Exit the session (`/exit`), then:

```sh
git --no-pager diff
```

```sh
npm test
```

Say: it turned a sentence from a user into a test, watched it fail, then made it
pass. The red step is the point — a fix you never saw fail is a guess. Note the
suite was green when we started; the bug lived in the gap the tests left.
Segue: "next it writes the tests before any code exists at all."

Reset after rehearsal (from repo root):
```sh
git checkout -- presentations/ai-assisted-coding-intro/demos/02-autonomous-fix && git clean -fd presentations/ai-assisted-coding-intro/demos/02-autonomous-fix
```
