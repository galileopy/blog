---
layout: post
title: "Service Test Best Practices"
date: 2026-06-21 12:00:00 +0000
slug: service-test-best-practices
lang: en
permalink: /service-test-best-practices/
tags:
  - testing
  - best-practice
original_status: published
---

> 📺 There's an interactive, code-along companion to this article — the
> **[Learn Haskell service-test series](https://galileopy.github.io/learn-haskell/)**,
> which builds the same ideas up from scratch with runnable examples.

## Motivation

I have been experimenting with an approach to testing that was called service testing at a company I worked before. They're aimed at improving both test automation and test quality. This document presents the principles behind it.

The goal is test automation that is both fast and faithful: quick enough to run on every change, and close enough to production that a passing suite is real evidence the service works. A **service test** starts one real instance of a single service and drives it over its real transport the way a caller would, then checks the results and real interactions with the service.

Every service test balances two goals that pull against each other:

1. **Fidelity.** The test executes against the integrated service as it runs in production. Some configuration differs (database pool size, log levels), but the code path is the same that is going to be running in production.
2. **Speed.** The suite is fast enough to belong in the developer's coding cycle and in CI, on the order of a second per test.

Every rule that follows comes from holding both of these at once. The two reference models below are weighed against this goal.

### Pyramid vs Trophy

Two reference models frame how a suite is distributed across tiers. The classic **test pyramid** puts many unit tests at the base and a few end-to-end tests at the top. The **testing trophy** instead puts the most weight on the middle — the service tier — with thinner layers of unit and end-to-end tests around it.

![Test pyramid versus testing trophy]({{ '/assets/images/service-test-best-practices/figure-pyramid-vs-trophy.svg' | relative_url }})

We aim for the trophy. A service test is more involved than a unit test and runs a little slower, but it exercises a whole request path through the running service instead of a single function in isolation, and because it only ever touches the contract, it keeps passing after the internals are refactored. The trade is deliberate: fewer tests for the same coverage, each slightly slower, with much less rework over time.

---

## What a service test is

A service test isolates a single service and exercises it through its public API, against its real dependencies (real state store, real message broker, real auth path). Dependencies are either real Docker instances of the real dependency or stubbed fakes.

| Tier    | Exercises                          | Dependencies | Asserts on                                       |
| ------- | ---------------------------------- | ------------ | ------------------------------------------------ |
| Unit    | one function                       | none         | the return value                                 |
| Service | the running service, end to end    | real         | the response, and any state the service persisted |

**TL;DR** service tests are scoped to a **single service**, **API-level**, **implementation-agnostic**, and a better version of unit tests. They use **real dependencies** (Postgres, ClickHouse, etc.) as much as possible while staying fast to run.

We specifically target testing **backend APIs**. Testing UIs and full end-to-end testing across services are out of scope.

![Service test setup]({{ '/assets/images/service-test-best-practices/figure-1-service-test-setup.svg' | relative_url }})

**Figure 1 — Service test setup.** The service under test as the real component, painted in its own colour, surrounded by its dependencies in two further colours: real Docker test instances (e.g., Postgres) and stubbed fakes. Worked example: `payments-api`, with a Docker Postgres and WireMock stubbing the payment gateway upstream. An integration service uses a similar setup with Docker plus WireMock to stub its third-party providers.

![Environment injection]({{ '/assets/images/service-test-best-practices/figure-1b-environment-injection.svg' | relative_url }})

**Figure 1b — Environment injection.** The same system with everything painted in the "real" colour except the service under test. During a service test neither the service code nor its instance changes — only the upstream providers change, by re-pointing the environment variables.

### Qualities of a good service test

- Tests the application's **public contract** (REST, GraphQL, events).
- **Does not depend on implementation details** (database type, caching, code organization, framework) for setup or assertions.
- Tests **one behavior** per test case.
- **Avoids shared setup.**
- **Avoids mocking.** (see note below)
- **Runs under 1 second.**
- Can be **run in parallel.**

> **Note on "avoids mocking":** this means not modifying, in code, the dependencies injected into a service to mock an upstream dependency. It does not apply to WireMock stubs, which sit outside the service — which, to avoid confusion, we call **Stubbed Fakes**.

---

## Two processes, one boundary

A service-test run involves two distinct processes, and conflating them is the most common mistake.

1. **The system under test** is a normally-started instance of the service, listening on its real transport, configured for the test environment. The test reaches it only over that transport, exactly as a real caller would.
2. **The test process** drives the system under test over the wire, and it may hold a direct, read-only handle to the service's stores so it can verify persisted state and reset between tests. This process does not serve traffic and is not the service.

Everything else follows from this one boundary: input always goes in over the transport, and verification reads either the response (over the transport) or the store (through the test process's store handle). Nothing reaches into the running service itself.

---

## Principles

### Use the test context for setup

The **test context** is the per-test bundle of everything a test is allowed to touch: HTTP and GraphQL clients, fakes for external services, and read/reset handles to the real stores. It is created and torn down before and after each test, so tests stay reliable and idempotent. It is defined in full under Tools → Test Context.

Setup (the "Arrange" phase) goes through the test context, not through low-level calls.

- **Arranging the test with low-level calls is an anti-pattern.** Manually populating the database with internal code (like Drizzle writes) makes tests depend on the implementation and can bypass business rules, setting up states the service would never allow.

### Exercise the public contract

The right mindset is that of a **manual tester**, treating the application as a **black box** and testing behavior. The unit of the contract is an **operation**: a REST endpoint, a GraphQL query or mutation, or a consumed message.

| A tester needs to know:                        | A tester can ignore:                          |
| ---------------------------------------------- | --------------------------------------------- |
| The endpoint to be used                        | The application language                      |
| The API approach (REST, GraphQL, etc.)         | The persistence layer (Postgres, etc.)        |
| The authentication scheme and credentials      | Internal caching (Redis, etc.)                |
| How to feed the app with data                  | Internal code structure                       |
| The expected response schema                   | Frameworks in use (NestJS, Drizzle, etc.)     |

#### Test steps example

1. Create a user with the correct permissions.
2. Obtain an authentication token.
3. Make a request to the API.
4. Verify the response.

### The test client and flow helpers

The **test client** is the test-side object with exactly one typed method per operation (e.g., `TestApiService.startPayment`). Each method is a **primitive**: it performs that single interaction over the public contract and returns the typed result. A primitive carries no assertions and forces no outcome, so the same `startPayment(...)` serves the success, auth-failure, and validation-failure cases. It provides defaults for arguments so a test only passes the parameters it cares about, and credentials are parameters rather than hard-coded values. Writing tests against the client keeps them in the caller's vocabulary — you call `startPayment`, not `http.post('/payments')` — which is the same thing as testing the contract.

```ts
// service-test/test-api-service.ts — mirrors the controllers
export class TestApiService {
  constructor(private readonly baseUrl: string) {}

  // one typed method per operation
  startPayment(amount: number, token: string) {
    return this.post('/v1/payments',
      { amount },
      { Authorization: `Bearer ${token}` });
  }

  listPayments(token: string, query = {}) {
    return this.get(
      this.buildPath('/v1/payments', query),
      { Authorization: `Bearer ${token}` });
  }
}
```

When a precondition needs two or more operations in sequence, compose primitives into a named **flow helper**. For example, _create account → change settings_ becomes a single `SettingsFlow.createAccountAndUpdate` a settings test calls to reach a known starting point. A flow helper that wraps a single primitive is a smell; call the primitive directly.

```ts
// service-test/flows/payment.flow.ts — composes primitives to arrange
export class PaymentFlow {
  constructor(private readonly api: TestApiService) {}

  // two operations, one named helper: start a payment request, then capture it
  async startAndCapture(token: string) {
    const { id } = await this.api.startPayment(1000, token);
    await this.api.capturePayment(id, token);
    return id;
  }
}
```

The test client and flow helpers are for the "Arrange" phase, not the "Act" phase.

- **Overusing helpers in the Act phase is an anti-pattern.** Using a helper to perform the action under test obscures what the endpoint actually does. The primary action should be one explicit primitive call, so the test's purpose is obvious.

---

## Tools

### Test Context

The test context bundles the helpers and clients that exercise the contract: HTTP clients, GraphQL clients, and fakes for external services, plus read/reset handles to the real stores. It provides all necessary entry points but **does not expose internals** (no `INestApplication`, no internal services), and it is created and torn down before and after each test.

```ts
// service-test/test-context.ts
export async function createTestContext() {
  const config = ServiceTestConfig();        // env guard runs here
  const moduleRef = await Test.createTestingModule({
    imports: [ConfigModule, DatabaseModule],
  }).compile();
  const app = await moduleRef.init();

  return {
    api: new TestApiService(config.baseUrl),                 // test client
    db:  new TestDatabaseService(app.get(DatabaseService)),  // whitebox reads
    close: () => app.close(),
  };
}
```

### Stubbed Fakes — WireMock

**Faking** replaces a dependency the team neither owns nor can run locally with a stand-in that answers over real HTTP. We use **WireMock** to stub third-party HTTP APIs rather than implementing fakes in TypeScript. The line is the process boundary: the service still opens a real connection and makes a real HTTP call, and only the far side of the wire answers with canned data. This is why "avoids mocking" and "use WireMock stubs" are not in conflict — WireMock sits outside the service.

#### Third-party HTTP APIs

WireMock stubs external upstreams the service calls over HTTP — for example a payment gateway, or third-party REST providers such as a CMMS or CRM that sit behind an integration service. Each is replaced by a stub server the service still calls over real HTTP.

#### Internal services owned by other teams

A shared, full-featured fake for an internal service owned by another team is rarely worth building: it is expensive to maintain and easily drifts from the real thing. The recommendation is to write a **scoped WireMock fake** that stubs only the calls the system under test actually makes, the same way any other third-party HTTP dependency is faked.

### Real Test Instances

A dependency you own and can run locally runs for real, as a disposable test-only instance in Docker. A real dependency covers more behavior than any substitute and needs no upkeep to stay faithful, so it is the default for everything runnable.

| Component               | Real or Fake? | Comments                                          |
| ----------------------- | ------------- | ------------------------------------------------- |
| MongoDB                 | **Real**      | Important, easy to set up, fast.                  |
| PostgreSQL              | **Real**      | Important, fast.                                  |
| Redis                   | **Real**      | Lightweight.                                      |
| ClickHouse              | **Real**      | Run as a Docker test instance.                    |
| ElasticMQ (for SQS)     | **Real**      | Local stand-in for SQS, run in Docker.            |
| LLM Providers           | **Fake**      | Real versions are slow and expensive; stubbed with WireMock. |
| External Services       | **Fake**      | Examples: LaunchDarkly, Firebase.                 |
| Other Internal Services | **Fake**      | Complicated setup, resource intensive.            |

#### Docker Postgres / ClickHouse

PostgreSQL and ClickHouse run as real, test-only instances via Docker (important, fast).

#### ElasticMQ — SQS

Where the service uses SQS, the queue is provided locally by **ElasticMQ** as a real Docker instance, so the service talks to a real queue over its normal client rather than a mock.

---

## Exception to the Principles

### Whiteboxing

Asserting through the public contract is the rule. **Whiteboxing** — asserting on the service's internal state store rather than on the response — is the exception, off by default and reached for only when the response alone cannot prove the behavior.

- **Default: do not whitebox.** It is an escape hatch, not part of the default flow. Some behavior cannot be proven from a single response — a write spanning several records, a rollback on failure, idempotency, a cascade on delete — and only there do you read persisted state, through the test context's store handle.
- **What it's for.** Asserting _desired_ behavior that is not yet covered by user acceptance criteria — behavior a user cannot currently exercise through the contract.
- **Why it's usually a smell.** A whitebox test is typically a flag that we are future-proofing, and that work should not sit in the default flow.
- **Why it isn't forbidden.** Sometimes it is useful to introduce debug artifacts, tracing, or other internal features that may be dropped later; a whitebox test lets us assert them in the meantime.
- **Red-flag rule.** A high number of whitebox tests should prompt us to look into the service and question whether what we are building is really necessary _now_, since it is not yet usable by a user.

Two boundaries keep whitebox narrow. First, direct store access is for **assertions only** — arranging through the store is forbidden, because a test that both arranges and checks the store never exercises the service at all. Second, asserting on a store the service exists to populate **for other consumers** is part of its observable contract, not whiteboxing (see the note below).

#### Choosing which test to write

![Choosing which test to write]({{ '/assets/images/service-test-best-practices/figure-2-choosing-a-test.svg' | relative_url }})

**Foundational fixtures.** Some state cannot be produced through any operation, because the service exposes no operation that creates it. The canonical case is identity: a service rarely offers "create a tenant" or "create a user," yet every test authenticates as someone. Declare that baseline once, as a minimal foundational fixture applied before the suite. Everything downstream of those identities is still arranged through the API, as that identity.

**Factory for inexpressible state.** Some state is real but no operation can set it — a controlled timestamp, or a deliberate tie an ordering or pagination test needs. For these, a direct store write is allowed, but only behind a named **factory**, and only for state the API genuinely cannot express. "It is faster than calling the API" does not qualify.

### A note on internal vs external dependencies

A service's relationship to a datastore decides whether reading it is contract or whitebox:

1. **Service importing to an external store:** the test **should** check the data in that store, because writing it is part of the service's observable functionality — this is contract, always allowed.
2. **CRUD service with an internal store:** the test reads that store only as the **whiteboxing** escape hatch above (desired-but-not-yet-user-facing behavior), never as a blanket habit and never to arrange.

---

## Appendix

### Sharing helpers and fakes across services

Fakes and helpers built for one service rarely transfer cleanly to another. Prefer **minimal, repo-specific helpers**: a thin helper you understand beats a shared one you do not.

### Bugs revealed by service tests

Beyond preventing regressions, service tests are effective at revealing **existing bugs**. Because they assert on behavior and never peek into implementation details, a failure points cleanly at either the application or the test, rather than at some coupling between them.

**How to handle revealed bugs:**

1. If the bug is from your PR, **fix it in that PR**.
2. If it is high impact, switch focus to **addressing the bug first**.
3. If it is not critical, **assert the current behavior**, add a descriptive comment / ticket link, and notify the owning team.

### Other rules worth following

These follow from the principles above and are collected here so nothing is lost.

- **Real auth, deterministic identities.** Service tests exercise the **real authentication path** — the same guard production uses; auth is never bypassed. What changes for tests is the verification _mode_, not the path: the service runs in a test-only mode that accepts deterministically-derived credentials, and that mode must be impossible to enable in production (enforced by the environment guard). Identities are defined by their claims, with the credential **derived** by a helper, never a pasted blob; specs reference them by **name** from a shared fixture set, never built inline. The fixture set includes the identities needed to prove **scoping** — a second principal under a different tenant, and, where they exist, the same principal under another tenant.
- **Environment guard.** The test process refuses to start unless it is pointed at the dedicated **test environment**. Config validation hard-fails on any non-test marker, so neither the test process nor the served instance can run against development or production state. The test environment (its store, ports, and values) is owned per service, not shared infrastructure.
- **Per-test isolation and reset.** Each test arranges its own state and depends on nothing another test left behind. Tests that write shared state reset it afterward, truncating the affected stores children-first. A serial suite keeps isolation simple; a parallel suite must guarantee isolation by construction (per-test tenanting), not by luck.
- **Three layers, one job each.** Service-test code separates into **primitives** (the test client), **flow helpers** (reusable multi-step arrangement), and **specs** (assertions only). A spec arranges via a primitive or a flow helper, acts via a primitive, and asserts — it never defines its own arrangement helper or inline factory. Small read-only observation helpers inside a spec (find a row, count matches) are assertion conveniences and are fine.
- **Test-client discipline.** An operation is not done until its primitive exists on the test client — that is part of its definition of done, visible in review. The test client is not a generic transport client: hand-built raw transport calls are allowed only to exercise transport-level behaviour that deliberately violates the contract (malformed payloads, wrong content type). Result types are imported from the service's own contract, never re-declared.
- **Whitebox "removed" assertions.** When a whitebox test asserts that a side effect was _removed_, it must first assert the side effect _existed_ — otherwise the check passes vacuously.
- **Naming and organisation.** Service-test files carry a distinct marker (a filename suffix or directory convention) so the tier runs independently of unit tests. Contract cases (response shape, status codes) are kept separate from behaviour cases, each stating what it does _not_ re-test. Test titles are direct present-tense statements of behaviour ("returns 401 when no credential is provided"), not "should"-prefixed phrasing.
