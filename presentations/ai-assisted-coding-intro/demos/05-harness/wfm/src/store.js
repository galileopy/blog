import { readFileSync, writeFileSync, existsSync } from "node:fs";

const FILE = "workflow.json";

export function load() {
  if (!existsSync(FILE)) {
    console.error("no workflow here — run: wfm init <name> <step...>");
    process.exit(1);
  }
  return JSON.parse(readFileSync(FILE, "utf8"));
}

export function save(workflow) {
  writeFileSync(FILE, JSON.stringify(workflow, null, 2) + "\n");
}
