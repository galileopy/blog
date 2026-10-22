// wfm core: a workflow is a named list of steps; a run tracks progress
// through those steps. Everything is plain data so it can live in a JSON file.

export function createWorkflow(name, steps) {
  if (!name) throw new Error("workflow needs a name");
  if (!Array.isArray(steps) || steps.length === 0) {
    throw new Error("workflow needs at least one step");
  }
  return { name, steps: steps.map((title) => ({ title, status: "pending" })) };
}

// Advance the workflow to its next state:
// - mark the first "pending" step as "done"
// - if no pending steps remain, set workflow.completed to true
// - never mutate the input; return a new workflow object
// - calling advance on a completed workflow returns it unchanged
export function advance(workflow) {
  throw new Error("not implemented"); // ← demo 1 fills this in
}

export function currentStep(workflow) {
  return workflow.steps.find((s) => s.status === "pending") ?? null;
}
