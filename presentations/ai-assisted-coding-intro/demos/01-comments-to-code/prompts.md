# Demo 1 — Comments to code

Concept: the human owns the loop; the model only turns an intent comment into code.

Paste in order, from `demos/01-comments-to-code/wfm/`:

```sh
cat src/workflow.js
```

```sh
npm test
```

```sh
claude --allowedTools "Read,Edit,Bash(npm test)"
```

Then paste into the session:

```
In src/workflow.js, implement the advance() function exactly as its comment describes. Change nothing else in the repo.
```

Exit the session (`/exit`), then:

```sh
git --no-pager diff
```

```sh
npm test
```

Say: the comment is the spec; tests were written and run by us. Segue: "what if it could run the tests itself?"

Reset after rehearsal (from repo root):
```sh
git checkout -- presentations/ai-assisted-coding-intro/demos/01-comments-to-code && git clean -fd presentations/ai-assisted-coding-intro/demos/01-comments-to-code
```
