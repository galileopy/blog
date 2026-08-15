---
description: Build the refined spec test-first, on a branch, and open a pull request
---

Read `docs/spec.md`. Build exactly what it says — no more.

1. **Branch.** `git checkout -b feat/<short-slug>`.
2. **Failing tests.** One test per acceptance criterion, named after that
   criterion so the test output reads as the spec. Put them in a new file under
   `test/`. Run `npm test` and confirm they fail *for the right reason* — a
   missing function, not a typo. Show the failure.
3. **Implement.** The smallest change in `src/` that turns them green. Run
   `npm test` until everything passes. Never modify an existing test.
4. **Match the prototype.** Any output the user sees must match
   `docs/prototype.md` byte for byte. If you had to deviate, say why.
5. **Refactor** while green.
6. **Open the PR.** Commit, push, and `gh pr create` with a body that lists the
   acceptance criteria and the test that covers each. Print the PR URL.

If the spec turns out to be unbuildable as written, stop and report which
criterion is the problem — do not reinterpret it.
