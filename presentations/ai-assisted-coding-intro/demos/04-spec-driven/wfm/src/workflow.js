// wfm core: a workflow is a named list of steps; a run tracks progress
// through those steps. Everything is plain data so it can live in a JSON file.

export function createWorkflow(name, steps) {
  if (!name) throw new Error("workflow needs a name");
  if (!Array.isArray(steps) || steps.length === 0) {
    throw new Error("workflow needs at least one step");
  }
  return { name, steps: steps.map((title) => ({ title, status: "pending" })) };
}

// Advance the workflow: mark the first pending step done; once no pending
// steps remain the workflow is completed. Pure — never mutates the input.
export function advance(workflow) {
  if (workflow.completed) return workflow;
  const idx = workflow.steps.findIndex((s) => s.status === "pending");
  const steps = workflow.steps.map((s, i) =>
    i === idx ? { ...s, status: "done" } : s
  );
  const completed = !steps.some((s) => s.status === "pending");
  return { ...workflow, steps, completed };
}

// Skip a named pending step; pure like advance(). Skipping an unknown or
// already-resolved step returns the workflow unchanged.
export function skip(workflow, title) {
  if (workflow.completed) return workflow;
  const idx = workflow.steps.findIndex(
    (s) => s.title === title && s.status === "pending"
  );
  if (idx === -1) return workflow;
  const steps = workflow.steps.map((s, i) =>
    i === idx ? { ...s, status: "skipped" } : s
  );
  const completed = !steps.some((s) => s.status === "pending");
  return { ...workflow, steps, completed };
}

export function currentStep(workflow) {
  return workflow.steps.find((s) => s.status === "pending") ?? null;
}
