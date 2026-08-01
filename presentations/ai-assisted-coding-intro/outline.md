# On AI Assisted Coding

## Contents
- Part 1 - The Evolution of the Feedback Loop
- Part 2 - Managing Context
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
- Part 2 - Managing Context
- Part 3 - Cool Tips, Tricks and Links

## Part 2 - Managing Context

### Conventions
Applies to anything that is managed by code

- How to add X
    - External interface
        - REST endpoint
        - GraphQL Field
        - RPC/WS handler
    - Infrastructure component
        - Terraform
        - CDK
    - Tests and tiers
        - e2e tests
        - Integration tests
        - Unit tests

### Workflows
It's about encoding what you do in prompts and then iterating automatically.

- Tracking requirements
- Refining tickets
- Review cycle
    - Adversarial review, use a different model
- Implementation process guidelines
    - TDD
    - Testing tier preferences
- Clean code practices
    - General authoring practices
    - Object oriented preferences
    - Local preferences not enforceable by traditional lint checks or deterministic tooling
- Drift check: are requirements, code, and acceptance tests all aligned

#### Dynamic Workflows vs Static Workflows
- Not everything needs to be fixed the same way.
- Preferences on particular steps
    - Dev preferences
    - Project differences

## Part 3 - Cool Tips, Tricks and Links

### Cool Tricks
- During refinement
    - Connect to Linear and get help refining tickets
    - Use structured English frameworks
        - User Stories
        - EARS
        - Gherkin scenarios
    - INVEST checks to split the feature
- During incidents
    - Connect your agent to live logs while in the repo or set of repos to triage likely root causes
    - Handle with care, agents love red herrings.
- Post mortems
    - Generate monitoring dashboards
- Load testing and improving/revalidating
- Using isolated worktrees to develop features concurrently
    - Needs a way to spin up an isolated stack
    - Requires familiarity with workflows.

### References

- groundcrew
- spec-kit
- conductor
