// wfm core: a workflow is a named list of steps; a run tracks progress
// through those steps. Everything is plain data so it can live in a JSON file.
//
// A step is "pending" until it resolves. It resolves as "done" when it runs
// cleanly, or as "failed" when it does not.

export function createWorkflow(name, steps) {
  if (!name) throw new Error("workflow needs a name");
  if (!Array.isArray(steps) || steps.length === 0) {
    throw new Error("workflow needs at least one step");
  }
  return { name, steps: steps.map((title) => ({ title, status: "pending" })) };
}

export function advance(workflow) {
  if (workflow.completed) return workflow;
  const idx = workflow.steps.findIndex((s) => s.status === "pending");
  const steps = workflow.steps.map((s, i) =>
    i === idx ? { ...s, status: "done" } : s
  );
  const completed = steps.every(
    (s) => s.status === "done" || s.status === "skipped"
  );
  return { ...workflow, steps, completed };
}

export function fail(workflow, title) {
  throw new Error("not implemented");
}

export function retry(workflow, title) {
  throw new Error("not implemented");
}

export function currentStep(workflow) {
  return workflow.steps.find((s) => s.status === "pending") ?? null;
}
