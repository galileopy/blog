# On AI Assisted Coding
Galileo Sánchez

The development loop as a feedback loop for AI, and how to find the right
abstractions to build reusable workflows.

## Contents
- Part 1 - The Evolution of the Feedback Loop
- Part 2 - Workflows
- Part 3 - Cool Tips, Tricks and Links

## Temperature Check

Where are you at today? How much of the loop you hand over.

- Manual
    1. Code completion - press tab to accept the suggested lines
    2. Comments to code - write a comment describing the intent and the model writes the body
    3. Chat and copy code - you paste the answer into the file yourself
- Agentic
    4. In file changes - the agent edits the files and you review the diff
    5. Spec driven - the agent works from a plan you approved first
    6. Vibe coding - you accept the output without reading the diff
- Harness Engineering
    7. Pre-built frameworks - adopt a published workflow such as spec-kit or conductor
    8. In house workflows - you author the loop the agent runs

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
- Write failing tests :human:
- Code :human:
- Run :laptop:
- Test :human:
- Iterate :human:
- Refactor :human:

Stop: Until requirements are satisfied :human:

Use case: Traditionally, all of it

### Feedback Loops: AI Assisted Coding (Level 1)
Start: Specify requirements :human:
- Technical design of a solution * :human:
- Write failing tests :human:
- Code :bot:
- Run :laptop:
- Test :human:
- Iterate :human:
- Refactor :human:

Stop: Until requirements are satisfied :human:

Use case: center a div

### Feedback Loops: Autonomous (Level 2)
Start: Specify requirements :human:
- Technical design of a solution * :human:
- Write failing tests :human:
- Code :bot:
- Run :laptop:
- Test :bot:
- Iterate :bot:
- Refactor :human:

Stop: Until requirements are satisfied :human:

Use case: Debugging
You can use this with plan mode in most tools

### Demo: Autonomous Debugging

One bug report, in a user's words. No file named, no function named.

- The model finds it, writes the failing test, and runs it red
- Then fixes it, and runs it green
- We read the diff

The loop closed without us. We only checked the result.

### Feedback Loops: Test Driven - TDD (Level 3)
Start: Specify requirements :human:
- Technical design of a solution * :human:
- Write failing tests :bot: (changed)
- Code :bot:
- Run :laptop:
- Test :bot:
- Iterate :bot:
- Refactor :human: :bot: (changed)

Stop: Until requirements are satisfied :human:

Use case: add complex feature

You'd need specific skills

### Feedback Loops: Spec Driven (Level 4)
Start: Specify requirements :human: :bot:
- Technical design of a solution :human: :bot:
- Write failing tests :bot:
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
- Write failing tests :bot:
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

Legend:
- Filled dot - manual prompting or intervention
- Diamond - agent self-heal with automated validation: test, compile, QA
- Dotted outline - pre-built steering artifact, part of a bigger workflow

### Workflow
A predefined set of steps to follow during implementation.

- Requirements
    - Stage goal: clear requirements, functional and non functional
    - Gather - let the agent act as a PM and drill you one question at a time, prodding for edge cases
    - Refine tickets - turn the raw requirements into structured ones using User Stories, EARS and Gherkin
    - Scope trimming - run INVEST over the user stories to isolate one vertical slice, then rebuild the requirements around it
    - Narrative (optional) - write the spec so a less technical audience can review it
        - (notes) no industry standard here; Joel Spolsky's four-part series on writing functional specs, condensed into a skill
- Planning
    - Technical design - feed the agent the requirements and repo access to produce an outline of the code changes
    - Testing plan - plan the tests that verify the work against the requirements
    - Implementation plan - sequence the code changes, verified against the tests
    - Testing tiers review - check both plans for a better distribution of tests, following company
      policy: integration first, testing pyramid, testing trophy, or e2e only
- Implementation loop
    - Code - implement the tests, implement the code for those tests, then refactor keeping the tests green
    - Review - get another model's input and iterate the implementation loop
    - Validation - run the end to end validation steps, then iterate or submit proof of the work done
    - Drift check - review code, requirements and checks, and ensure the triplet aligns
    - All green: merge
    - (notes) Stencils - the loop repeats, so learn from the plans and build stencils for
      recurring patterns: unit tests, integration tests, endpoints, controllers, resolvers
    - (notes) Clean code practices for the refactor step: general authoring practices, object oriented
      preferences, and local preferences not enforceable by traditional lint checks or deterministic tooling

At any stage the agent can fall back to human control, if the requirements were too ambiguous
or scope creep was introduced into the loop or implied in the original spec.

### Demo: A Workflow You Can Read

Five phases, five checked-in commands. Each one leaves an artifact.

- Drill - a spec, with the questions asked and the answers given
- Prototype - a clickable screen, before any code exists
- Refine - the spec again, every assumption checked against the source
- Implement - a branch, failing tests first, then a pull request
- QA - a report, posted to that pull request

QA is not allowed to read the code it is checking.

The workflow is versioned, reviewable, and someone else can run it.

### When the Harness Stops

A run that halts at a named check is the system working.
It looks like the system failing.

That is why each phase leaves something behind.

#### Dynamic Workflows vs Static Workflows
- Not everything needs to be fixed the same way.
- Preferences on particular steps
    - Dev preferences
    - Project differences

## Part 3 - Cool Tips, Tricks and Links

### Cool Tricks
- During incidents - connect the agent to live logs alongside the repo to triage likely root causes
    - (notes) handle with care, agents love red herrings
- Post mortems - have the agent generate monitoring dashboards for what the incident exposed
- Infrastructure as code - point the implementation workflow at Terraform or CDK instead of service code
- Load testing - have the agent load test the service, then improve and revalidate against the results
- Isolated worktrees - develop features in parallel, with an isolated stack per worktree
    - (notes) requires real familiarity with the workflows before it pays off

### Helpful links

- spec-kit - a reusable spec driven framework - https://github.com/github/spec-kit
- conductor - the same, packaged as a Gemini CLI extension - https://github.com/gemini-cli-extensions/conductor
- groundcrew - a task list monitor that dispatches CLI agents with refined tickets for
  autonomous execution - https://github.com/ClipboardHealth/groundcrew

## Close

### Quote

The best way to learn these systems is trying, failing and learning. There is no
right way to do it, but there are many ways to have fun and keep learning.

### Questions

Questions?

### Thank you

Galileo Sánchez
