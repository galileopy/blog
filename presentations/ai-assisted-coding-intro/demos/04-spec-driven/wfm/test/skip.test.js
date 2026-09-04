import { test } from "node:test";
import assert from "node:assert/strict";
import { createWorkflow, skip, currentStep } from "../src/workflow.js";

test("skip marks the named pending step as skipped", () => {
  const wf = createWorkflow("release", ["build", "test", "ship"]);
  const next = skip(wf, "test");
  assert.equal(next.steps[1].status, "skipped");
  assert.equal(next.steps[0].status, "pending");
});

test("skip is pure", () => {
  const wf = createWorkflow("release", ["build"]);
  skip(wf, "build");
  assert.equal(wf.steps[0].status, "pending");
});

test("skipping an unknown step returns the workflow unchanged", () => {
  const wf = createWorkflow("release", ["build"]);
  assert.deepEqual(skip(wf, "nope"), wf);
});

test("skipping the last pending step completes the workflow", () => {
  const wf = createWorkflow("release", ["build"]);
  const done = skip(wf, "build");
  assert.equal(done.completed, true);
  assert.equal(currentStep(done), null);
});
