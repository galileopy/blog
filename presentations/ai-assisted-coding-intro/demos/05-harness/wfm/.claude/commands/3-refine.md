---
description: Audit the spec against the real codebase and fold the prototype back in
---

Read `docs/spec.md` and `docs/prototype.md`. Before anyone builds this, check
that the spec is true about *this* codebase and consistent with its own mock.

1. **Verify every assumption.** For each claim the spec makes about existing
   behaviour, find the code that proves or disproves it. Write the verdict as
   `confirmed` or `contradicted`, each with the file and line you checked. An
   assumption you could not check is `unverified` — say so; do not guess.
2. **Reconcile the prototype.** Work through its open questions. Where the mock
   and the spec disagree, decide which is right and record why.
3. **Blindspot pass.** Name what neither document covers: failure modes, empty
   and boundary states, interaction with existing functions, anything that
   persists between runs. Add criteria for the ones that matter.
4. **Rewrite `docs/spec.md` in place** with the corrections folded in, and append
   a **Verification** section holding the table from step 1.

If a contradiction invalidates the feature as specified, stop and say so plainly
rather than repairing the spec into something the user did not ask for. Still no
code.
