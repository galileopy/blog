// wfm core: a workflow is a named list of steps; a run tracks progress
// through those steps. Everything is plain data so it can live in a JSON file.
//
// A step is "pending" until it resolves. It resolves as "done" when it runs
// cleanly, or as "failed" when it does not. A failed step blocks the run until
// it is retried.

export function createWorkflow(name, steps) {
  if (!name) throw new Error("workflow needs a name");
  if (!Array.isArray(steps) || steps.length === 0) {
    throw new Error("workflow needs at least one step");
  }
  return { name, steps: steps.map((title) => ({ title, status: "pending" })) };
}

const isBlocked = (steps) => steps.some((s) => s.status === "failed");

const isResolved = (s) => s.status === "done" || s.status === "skipped";

export function advance(workflow) {
  if (workflow.completed) return workflow;
  if (isBlocked(workflow.steps)) return workflow;
  const idx = workflow.steps.findIndex((s) => s.status === "pending");
  const steps = workflow.steps.map((s, i) =>
    i === idx ? { ...s, status: "done" } : s
  );
  return { ...workflow, steps, completed: steps.every(isResolved) };
}

export function fail(workflow, title) {
  const idx = workflow.steps.findIndex(
    (s) => s.title === title && s.status === "pending"
  );
  if (idx === -1) return workflow;
  const steps = workflow.steps.map((s, i) =>
    i === idx ? { ...s, status: "failed" } : s
  );
  return { ...workflow, steps };
}

export function retry(workflow, title) {
  const idx = workflow.steps.findIndex(
    (s) => s.title === title && s.status === "failed"
  );
  if (idx === -1) return workflow;
  const steps = workflow.steps.map((s, i) =>
    i === idx ? { ...s, status: "pending" } : s
  );
  return { ...workflow, steps, completed: false };
}

export function skip(workflow, title) {
  const idx = workflow.steps.findIndex(
    (s) => s.title === title && s.status === "pending"
  );
  if (idx === -1) return workflow;
  const steps = workflow.steps.map((s, i) =>
    i === idx ? { ...s, status: "skipped" } : s
  );
  return { ...workflow, steps, completed: steps.every(isResolved) };
}

export function currentStep(workflow) {
  if (isBlocked(workflow.steps)) return null;
  return workflow.steps.find((s) => s.status === "pending") ?? null;
}
