---
description: Run the full requirement → tests → code → verify loop for one wfm feature
---

You are running the wfm feature workflow. Goal: $ARGUMENTS

Follow these steps in order; do not skip or reorder them:

1. **Requirements** — restate the goal as 2–4 acceptance criteria. If the goal
   is too ambiguous to produce testable criteria, stop and ask instead of guessing.
2. **Failing tests** — write tests for those criteria in `test/`, one file per
   feature. Run `npm test` and confirm the new tests fail for the right reason.
3. **Implement** — make the smallest change in `src/` that passes. Run
   `npm test` until everything is green. Never modify existing tests.
4. **Refactor** — clean up while keeping tests green.
5. **Report** — show the final `npm test` summary and a short list of files
   changed with one line each on why.
