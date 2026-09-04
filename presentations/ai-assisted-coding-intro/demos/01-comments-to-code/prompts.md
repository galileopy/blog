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
claude --allowedTools "Read,Edit" --disallowedTools "Bash"
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

Say: the comment is the spec. The model cannot run anything — `Bash` is denied,
so writing the code is all it does. We wrote the tests and we run them; the loop
is ours. Segue: "what if it could close that loop itself?"

Reset after rehearsal (from repo root):
```sh
git checkout -- presentations/ai-assisted-coding-intro/demos/01-comments-to-code && git clean -fd presentations/ai-assisted-coding-intro/demos/01-comments-to-code
```
