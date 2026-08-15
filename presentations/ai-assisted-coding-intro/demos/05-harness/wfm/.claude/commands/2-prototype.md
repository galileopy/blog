---
description: Mock the user-visible surface from the spec, before any code exists
---

Read `docs/spec.md`. Build a paper prototype of what the user will actually see.

wfm is a terminal tool, so the surface is its printed output. Write
`docs/prototype.md` containing:

1. **Sample sessions** — literal terminal transcripts, fenced as ```text, for
   the main path plus every interesting edge the spec's criteria imply (nothing
   yet, one item, many items, a blocked or failed run). Show the command typed
   and the exact bytes printed back. Invent realistic data; do not run anything.
2. **Format notes** — column alignment, ordering, truncation, what is shown when
   a value is missing. Be specific enough that two people implementing from this
   would print the same characters.
3. **Open questions** — anything the mock forced into the open that `docs/spec.md`
   did not settle.

This is a design artifact, not code. Do not create or modify anything in `src/`
or `test/`. If the prototype contradicts a criterion in the spec, say so in the
open questions rather than silently changing either one.
