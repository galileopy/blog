import { test } from "node:test";
import assert from "node:assert/strict";
import { createWorkflow, advance, currentStep } from "../src/workflow.js";

test("createWorkflow builds pending steps", () => {
  const wf = createWorkflow("release", ["build", "test", "ship"]);
  assert.equal(wf.steps.length, 3);
  assert.ok(wf.steps.every((s) => s.status === "pending"));
});

test("advance marks the first pending step done", () => {
  const wf = createWorkflow("release", ["build", "ship"]);
  const next = advance(wf);
  assert.equal(next.steps[0].status, "done");
  assert.equal(next.steps[1].status, "pending");
  assert.equal(currentStep(next).title, "ship");
});

test("advance does not mutate its input", () => {
  const wf = createWorkflow("release", ["build"]);
  advance(wf);
  assert.equal(wf.steps[0].status, "pending");
});

test("advance walks a run to its last step", () => {
  const wf = createWorkflow("release", ["build", "ship"]);
  const done = advance(advance(wf));
  assert.ok(done.steps.every((s) => s.status === "done"));
  assert.equal(currentStep(done), null);
});
