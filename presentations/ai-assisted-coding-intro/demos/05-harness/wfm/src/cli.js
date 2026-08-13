#!/usr/bin/env node
import { createWorkflow, advance, skip, currentStep } from "./workflow.js";
import { load, save } from "./store.js";

const MARKS = { pending: "·", done: "✔", skipped: "»", failed: "✗" };
const [cmd, ...args] = process.argv.slice(2);

switch (cmd) {
  case "init": {
    const [name, ...steps] = args;
    save(createWorkflow(name, steps));
    console.log(`started "${name}" with ${steps.length} steps`);
    break;
  }
  case "status": {
    const wf = load();
    const current = currentStep(wf);
    for (const s of wf.steps) {
      const here = s === current ? " ← current" : "";
      console.log(` ${MARKS[s.status]} ${s.title}${here}`);
    }
    if (wf.completed) console.log(`"${wf.name}" is completed`);
    break;
  }
  case "advance": {
    save(advance(load()));
    break;
  }
  case "skip": {
    save(skip(load(), args[0]));
    break;
  }
  default:
    console.error("usage: wfm <init|status|advance|skip>");
    process.exit(1);
}
