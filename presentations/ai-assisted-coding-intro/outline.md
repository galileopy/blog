# On AI Assisted Coding

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

### Intro

It is still coding.
You have a different feedback loop.

### The coding feedback loop

Start: Collect requirements
- Technical design of a solution *
- Build step
- Run
- Test, get feedback
- Iterate

Stop: Until requirements are satisfied

### Traditional Feedback Loop
Start: Collect requirements
- Technical design of a solution *
- Code, compile
- Run
- Test, get feedback
- Iterate, manually

Stop: Until requirements are satisfied
Use case: Traditionally, all of it

### AI Feedback Loop
Start: Collect requirements
- Technical design of a solution *
- Prompt - generate code
- Run
- Test, get feedback
- Iterate, manually

Stop: Until requirements are satisfied
Use case: center a div

### Autonomous Feedback Loop
Start: Collect requirements
- Technical design of a solution *
- Prompt - generate code
- Run
- Test, get feedback
- Iterate, feed test results back into agent

Stop: Until requirements are satisfied

Use case: Debugging
You can use this with plan mode in most tools

### Test Driven Feedback Loop - TDD
Start: Collect requirements
- Technical design of a solution *
- Prompt - generate failing tests
- Prompt - generate code
- Run
- Test, get feedback
- Iterate, feed test results back into agent
- Prompt - refactor

Stop: Until requirements are satisfied

Use case: add complex feature

You'd need specific skills

### Spec Driven Feedback Loop
Start: Collect requirements
- Prompt - generate specs
- Technical design of a solution *
- Prompt - generate failing tests
- Prompt - generate code
- Run
- Test, get feedback
- Iterate, feed test results back into agent
- Prompt - refactor

Stop: Until requirements are satisfied
Use case: generate new greenfield apps

You can use plan mode or start using more complex frameworks.

## Brownfield Projects
Brownfield projects have more context baked in.

### Spec Driven Feedback Loop with Predefined Workflows
- Author project specific workflows

Start: Collect requirements

- Prompt - generate specs
- Technical design of a solution *
- Prompt - generate failing tests
- Prompt - generate code
- Run
- Test, get feedback
- Iterate, feed test results back into agent
- Prompt - refactor

Stop: Until requirements are satisfied

## Conventions
- How to add X
    - External interface
        - REST endpoint
        - GraphQL Field
        - RPC/WS handler
    - Infrastructure component
    - Tests and tiers
        - e2e tests
        - Integration tests
        - Unit tests

## Cool Tricks
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

## Workflows
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
    - Local preferences not enforceable by [tooling? — sentence looks cut off]
- Drift check: are requirements, code, and acceptance tests all aligned

### Dynamic Workflows vs Static Workflows
- Not everything needs to be fixed the same way.
- Preferences on particular steps
    - Dev preferences
    - Project differences

## Existing Infrastructure
Applies to anything that is managed by code
### Conventions
- How to add an infrastructure component
    - Terraform
    - CDK
