# On AI Assisted Coding

## Contents
- Part 1 - The Evolution of the Feedback Loop
- Part 2 - Workflows
- Part 3 - Cool Tips, Tricks and Links

## Temperature Check
- Prompt tests or new functions
- Vibe coding simple apps
- Plan mode in tools
- Spec driven framework
    - Canned, spec-kit/conductor
    - In house
- Workflows and dynamic workflows
    - Set of prompts that describe the whole SDLC
- Managing context

## Part 1 - The Evolution of the Feedback Loop

### Intro

It is still coding.
You have a different feedback loop.

### Feedback Loops

Six loops, each one a step further from doing it all yourself.

- Level 0 - Traditional
- Level 1 - AI Assisted Coding
- Level 2 - Autonomous
- Level 3 - Test Driven, TDD
- Level 4 - Spec Driven
- Level 5 - Spec Driven, Predefined Workflows

### Feedback Loops: Traditional (Level 0)
Start: Specify requirements :human:
- Technical design of a solution * :human:
- Code :human:
- Run :laptop:
- Test :human:
- Iterate :human:

Stop: Until requirements are satisfied :human:

Use case: Traditionally, all of it

### Feedback Loops: AI Assisted Coding (Level 1)
Start: Specify requirements :human:
- Technical design of a solution * :human:
- Code :bot:
- Run :laptop:
- Test :human:
- Iterate :human:

Stop: Until requirements are satisfied :human:

Use case: center a div

### Feedback Loops: Autonomous (Level 2)
Start: Specify requirements :human:
- Technical design of a solution * :human:
- Code :bot:
- Run :laptop:
- Test :bot:
- Iterate :bot:

Stop: Until requirements are satisfied :human:

Use case: Debugging
You can use this with plan mode in most tools

### Feedback Loops: Test Driven - TDD (Level 3)
Start: Specify requirements :human:
- Technical design of a solution * :human:
- Generate failing tests :bot:
- Code :bot:
- Run :laptop:
- Test :bot:
- Iterate :bot:
- Refactor :human: :bot:

Stop: Until requirements are satisfied :human:

Use case: add complex feature

You'd need specific skills

### Feedback Loops: Spec Driven (Level 4)
Start: Specify requirements :human: :bot:
- Technical design of a solution :human: :bot:
- Generate failing tests :bot:
- Code :bot:
- Run :laptop:
- Test :bot:
- Iterate :bot:
- Refactor :bot:
Stop: Until requirements are satisfied :human: :bot:

Use case: generate new greenfield apps

You can use plan mode or start using more complex frameworks.

### Feedback Loops: Spec Driven, Predefined Workflows (Level 5)
Once: Author project workflows :human: :bot:
Start: Specify requirements :human: :bot:
- Technical design of a solution :human: :bot:
- Generate failing tests :bot:
- Code :bot:
- Run :laptop:
- Test :bot:
- Iterate :bot:
- Refactor :bot:
Stop: Until requirements are satisfied :human: :bot:

Use case: brownfield projects

Brownfield projects have more context baked in.

### Questions

Questions so far?

Next:
- Part 2 - Workflows
- Part 3 - Cool Tips, Tricks and Links

## Part 2 - Workflows

### Three runs at the same goal
Same goal, three runs. What changes is when the correction was authored.

- Correct as you go
    - Manual prompting in chat
- Plan first, then execute
    - Prompt a plan into existence, then execute and correct when needed
    - A plan.md or a tool's plan mode, or an LLM-generated self-contained prompt
      encoding the goal, the checkpoints, and how to verify them
- Reusable workflow
    - A pre-set skill per step, collected in an orchestrator prompt that knows
      how to use them
- Bonus: a skill that composes the workflow dynamically according to the problem

### Pre-built prompts and skills
Applies to anything that is managed by code.

- Requirements
    - Stage goal: clear requirements, functional and non functional
    - Gather - let the agent act as a PM and drill you one question at a time, prodding for edge cases
    - Refine tickets - turn the raw requirements into structured ones using User Stories, EARS and Gherkin
    - Scope trimming - run INVEST over the stories to isolate one vertical slice, then rebuild the requirements
    - Narrative (optional) - write the spec so a less technical audience can review it
        - (notes) no industry standard here; Joel Spolsky's four-part series on writing functional specs, condensed into a skill
- Implementation
    - Stage goal: working code that satisfies the requirements
    - Technical design - feed the agent the requirements and repo access to produce an outline of the code changes
    - Plan - sequence the work, and opt into red/green or red/green/blue TDD cycles
    - Code - work the task list one verifiable step at a time
    - Refactor - clean up inside each cycle, then once more across the finished slice
        - General authoring practices
        - Object oriented preferences
        - Local preferences not enforceable by traditional lint checks or deterministic tooling
    - Validation - close the loop with the checks the agent iterates against
    - (notes) Stencils - the stage repeats, so learn from the plans and build stencils for
      recurring patterns: unit tests, integration tests, endpoints, controllers, resolvers
- Validation - implementation's last step
    - End to end - give the agent curl or Playwright so it can exercise the running system
    - Test tiers - review the requirements and pick the right tier for each; not everything
      needs a unit test, not everything needs an e2e test. The validation plan feeds back into the
      implementation plan as notes
    - Review cycle - have a different model review the work against the requirements, in CI
    - Drift check - a check before a PR is considered merge-ready; requirements are tracked in
      code now, so drift has to be prevented. Runs in CI and inside the implementation loop

#### Dynamic Workflows vs Static Workflows
- Not everything needs to be fixed the same way.
- Preferences on particular steps
    - Dev preferences
    - Project differences

## Part 3 - Cool Tips, Tricks and Links

### Cool Tricks
- During incidents - connect the agent to live logs alongside the repo to triage likely root causes
    - (notes) handle with care, agents love red herrings
- Post mortems - have the agent generate the monitoring dashboards
- Infrastructure as code - run the same loop against Terraform or CDK instead of service code
- Load testing - improve and revalidate against the results
- Isolated worktrees - develop features in parallel, with an isolated stack per worktree
    - (notes) requires real familiarity with the workflows before it pays off

### Helpful links

- groundcrew - https://github.com/ClipboardHealth/groundcrew
- spec-kit - https://github.com/github/spec-kit
- conductor - https://github.com/gemini-cli-extensions/conductor
