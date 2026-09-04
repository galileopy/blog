import { test } from "node:test";
import assert from "node:assert/strict";
import {
  createWorkflow,
  advance,
  fail,
  retry,
  currentStep,
} from "../src/workflow.js";

const blocked = () => fail(createWorkflow("release", ["build", "ship"]), "build");

test("fail marks the named pending step as failed", () => {
  const wf = createWorkflow("release", ["build", "ship"]);
  assert.equal(fail(wf, "build").steps[0].status, "failed");
});

test("fail is pure", () => {
  const wf = createWorkflow("release", ["build"]);
  fail(wf, "build");
  assert.equal(wf.steps[0].status, "pending");
});

test("failing an unknown or resolved step returns the workflow unchanged", () => {
  const wf = createWorkflow("release", ["build"]);
  assert.deepEqual(fail(wf, "nope"), wf);
  assert.deepEqual(fail(advance(wf), "build"), advance(wf));
});

test("a failed step blocks the workflow, so advance does nothing", () => {
  const wf = blocked();
  assert.deepEqual(advance(wf), wf);
});

test("a blocked workflow has no current step", () => {
  assert.equal(currentStep(blocked()), null);
});

test("retry returns a failed step to pending and unblocks the workflow", () => {
  const wf = retry(blocked(), "build");
  assert.equal(wf.steps[0].status, "pending");
  assert.equal(currentStep(wf).title, "build");
  assert.equal(advance(wf).steps[0].status, "done");
});

test("retrying a step that has not failed returns the workflow unchanged", () => {
  const wf = createWorkflow("release", ["build"]);
  assert.deepEqual(retry(wf, "build"), wf);
});
