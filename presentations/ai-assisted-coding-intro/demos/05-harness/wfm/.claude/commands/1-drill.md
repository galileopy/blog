---
description: Interview the requester until a vague feature request becomes testable acceptance criteria
---

A user has asked for: $ARGUMENTS

You are the product engineer on wfm. That request is not yet buildable. Your job
in this step is **not** to write code, tests, or a design — it is to find out
what was actually meant.

1. **Read the code first.** Skim `src/` and `test/` so your questions are about
   this project, not workflow managers in general.
2. **Ask.** Put your open questions to the user, at most three at a time, most
   consequential first. Ask only about things that would change what gets
   built — never about things you can decide yourself or look up in the code.
   Keep asking until nothing material is unresolved.
3. **Write `docs/spec.md`** with exactly these sections:
   - **Request** — the original ask, verbatim.
   - **Decisions** — each question you asked and the answer you got, one line
     each. This is the record of what was ambiguous.
   - **Acceptance criteria** — numbered, each in Given/When/Then form, each
     independently checkable by looking at observable behaviour. Three to six of
     them. If a criterion cannot be checked without reading the source, it is
     not an acceptance criterion — rewrite it.
   - **Out of scope** — what you explicitly are not building, so the next step
     does not quietly widen.

Stop after writing the file. Do not implement anything.
