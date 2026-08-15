---
description: Check the built feature against its spec as a black box and post the report to the PR
---

Read `docs/spec.md` and `docs/prototype.md`. QA the branch as if you had not
written it. **You are not allowed to read `src/` in this step** — judge the
feature only by running it, the way a user would.

1. **Exercise it.** For every acceptance criterion, run the real commands that
   would demonstrate it and capture the actual output. Include the empty case
   and at least one thing the spec says should *not* happen.
2. **Compare to the prototype.** Diff the real output against the mock. Note any
   difference, however small — a changed heading is a finding.
3. **Write `docs/qa-report.md`**:
   - A verdict line: **PASS** or **FAIL**.
   - A table: criterion | command run | expected | actual | pass/fail.
   - Findings, worst first, each with the exact reproduction.
   - What you could not test, and why.
4. **Post it** to the pull request: `gh pr comment --body-file docs/qa-report.md`.

Report failures as failures. A green test suite is not evidence the criteria are
met — the suite was written by the same process that wrote the code. If
everything genuinely passes, say so plainly and keep the report short.
