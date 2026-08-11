# Demo 3 — TDD

Concept: test authoring changes hands. We state a requirement; Claude writes the
failing tests first, shows them failing, then implements until green.

Paste in order, from `demos/03-tdd/wfm/` (interactive session this time):

```sh
npm test
```

```sh
claude
```

Then paste into the session:

```
We need a new function skip(workflow, title) in src/workflow.js: it marks the named step as "skipped" if that step is still pending, leaves any other step untouched, is pure like advance(), and completes the workflow when no pending steps remain. Skipping an unknown or already-done step returns the workflow unchanged. Work TDD: write failing tests for this in test/workflow.test.js first, run npm test to show they fail, then implement skip() until all tests pass. Do not change existing tests.
```

Exit the session, then:

```sh
git diff
```

```sh
npm test
```

Say: the requirement was one paragraph; tests came from the model, and the tests
failing *first* is the proof they test something. Segue: "next, the design
itself is delegated — plan mode."

Reset after rehearsal (from repo root):
```sh
git checkout -- presentations/ai-assisted-coding-intro/demos/03-tdd && git clean -fd presentations/ai-assisted-coding-intro/demos/03-tdd
```
