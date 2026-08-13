import { test } from "node:test";
import assert from "node:assert/strict";
import { createWorkflow, advance } from "../src/workflow.js";

test("a run is completed once its last step is done", () => {
  const wf = createWorkflow("release", ["build", "ship"]);
  assert.equal(advance(advance(wf)).completed, true);
});

test("a run is not completed while a step is still pending", () => {
  const wf = createWorkflow("release", ["build", "ship"]);
  assert.ok(!advance(wf).completed);
});
