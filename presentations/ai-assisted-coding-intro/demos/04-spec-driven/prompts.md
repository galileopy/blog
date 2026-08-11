# Demo 4 — Spec driven

Concept: the technical design is delegated too. We prompt a plan into existence
in plan mode, approve it on camera, then it executes the plan TDD-style.

Paste in order, from `demos/04-spec-driven/wfm/`:

```sh
npm test
```

```sh
claude --permission-mode plan
```

Then paste into the session:

```
wfm is a library with no user interface yet. Design a CLI for it: src/cli.js exposing the commands "init <name> <step...>", "status", "advance", and "skip <title>", persisting the workflow to a workflow.json file in the current directory through a small src/store.js module. status prints one line per step with a marker for its state and highlights the current step; every command exits nonzero with a clear message when there is no workflow.json yet. Plan first: list the files you will create, the test cases, and the order of work. After I approve, implement it TDD-style with npm test green at the end.
```

Review the plan on screen, approve it, let it run. Exit, then:

```sh
npm test
```

```sh
node src/cli.js init release build test ship
node src/cli.js advance
node src/cli.js status
```

Say: the spec was born as a plan we approved — that approval is the human
checkpoint that vibe coding skips. Segue: "one step left: make the whole loop a
reusable artifact."

Reset after rehearsal (from repo root):
```sh
git checkout -- presentations/ai-assisted-coding-intro/demos/04-spec-driven && git clean -fd presentations/ai-assisted-coding-intro/demos/04-spec-driven
```
