# Category 3: Test Generation & QA (10 Prompts)

---

## Prompt #23 — Unit Test Suite Generator

```
Generate a complete unit test suite for this function/class.

Code to test:
[paste code]

Language: [language]
Test framework: [pytest / Jest / JUnit / Go testing / RSpec / etc.]

Requirements:
1. Cover every public method
2. Test happy path, edge cases, and error cases
3. Use descriptive test names that explain the scenario (not "test1", "test2")
4. Each test should be independent (no shared state between tests)
5. Mock external dependencies (database, API calls, file system)
6. Aim for branch coverage, not just line coverage

Edge cases I know about:
[list any specific edge cases, or say "identify them for me"]

Output: Ready-to-run test file with setup/teardown if needed.
```

---

## Prompt #24 — Edge Case Brainstorm

```
I need to find edge cases for this function before it breaks in production.

Function:
[paste code]

What it does: [1-sentence description]

Generate edge cases organized by category:

1. **Boundary values**: min, max, zero, negative, overflow
2. **Empty/null inputs**: empty string, empty array, null, undefined, None
3. **Type edge cases**: very long strings, Unicode (emoji, RTL text, null bytes), special chars
4. **Concurrency**: what if called twice simultaneously? What if interrupted mid-execution?
5. **Resource limits**: very large input, disk full, network timeout
6. **State-dependent**: what if called before initialization? After cleanup? Twice?
7. **Business logic**: weird but valid combinations users will eventually try

For each edge case:
- Input example
- Expected behavior
- Why it might break
```

---

## Prompt #25 — Integration Test Builder

```
Write integration tests for this module that interacts with external systems.

Code:
[paste module code]

External dependencies:
[list: PostgreSQL, Redis, third-party API, file system, message queue, etc.]

Test environment:
[describe: Docker Compose available? Testcontainers? In-memory fakes? Mock server?]

Framework: [pytest + testcontainers / Jest + supertest / etc.]

I need:
1. Setup: How to spin up test dependencies
2. Seed data: Realistic test fixtures
3. Happy path: Full flow from input to output
4. Failure modes: What happens when [dependency] is down/slow/returns errors
5. Cleanup: Proper teardown so tests don't pollute each other

Don't mock what I can test for real. Only mock truly external services (third-party APIs).
```

---

## Prompt #26 — API Endpoint Test Suite

```
Generate API tests for these endpoints.

Endpoints:
[paste route definitions or OpenAPI spec snippet]

Implementation:
[paste controller/handler code if available]

Test framework: [supertest / requests + pytest / httpx / REST Assured / etc.]

For each endpoint, test:
1. Happy path (200/201 response, correct body)
2. Invalid input (400 — bad request body, missing fields, wrong types)
3. Authentication (401 — missing/expired/invalid token)
4. Authorization (403 — valid user, wrong permissions)
5. Not found (404 — valid request, resource doesn't exist)
6. Conflict (409 — duplicate creation, version mismatch)
7. Rate limiting (429 — if applicable)
8. Response shape (assert exact JSON structure, not just status code)

Include: setup (create test user, seed data), teardown (cleanup).
```

---

## Prompt #27 — Regression Test from Bug Report

```
A bug was found. Write a regression test that fails with the current code and passes after the fix.

Bug description:
[describe the bug — what happens, what should happen]

Reproduction steps:
[list steps]

Affected code:
[paste the buggy code]

Fix (if already known):
[paste the fix, or say "not yet determined"]

I need:
1. A test that reproduces the exact bug scenario
2. The test should fail RIGHT NOW on the current code
3. Name the test clearly: test_[descriptive_name]_regression
4. Add a comment linking to the bug report/ticket
5. After the fix, verify the test passes
```

---

## Prompt #28 — Property-Based Test Designer

```
Design property-based tests for this function.

Function:
[paste code]

Property-based testing means: instead of testing specific examples, define properties that should ALWAYS hold true, then let the framework generate random inputs.

Framework: [Hypothesis (Python) / fast-check (JS) / QuickCheck / etc.]

Identify properties:
1. **Invariants**: What should ALWAYS be true regardless of input?
2. **Idempotency**: Does calling it twice give the same result?
3. **Reversibility**: If there's an inverse operation, does round-trip work?
4. **Monotonicity**: Does increasing input always increase/decrease output?
5. **Equivalence**: Is there a simpler (slower) version to compare against?
6. **Bounds**: Does output always stay within expected range?

Write the property-based tests with appropriate generators for the input types.
```

---

## Prompt #29 — Test Fixture & Mock Generator

```
Generate test fixtures and mocks for this code.

Code under test:
[paste code]

Dependencies to mock:
[list: database connection, HTTP client, file system, cache, etc.]

I need:
1. **Fixtures**: Realistic test data (not "foo", "bar", "test123")
   - Use plausible values (real-looking emails, names, timestamps)
   - Cover: typical case, minimum valid, maximum valid, edge case
2. **Mocks**: For each dependency:
   - Success response mock
   - Error/timeout response mock
   - Configure mock behavior per test (not global)
3. **Factory functions**: Make it easy to create variations
   - `make_user(overrides)` pattern
   - Default values that make sense

Framework: [pytest fixtures / Jest mocks / Mockito / etc.]
```

---

## Prompt #30 — Snapshot/Golden Test Creator

```
Create snapshot tests (golden tests) for this output-generating code.

Code:
[paste code that generates output — HTML, JSON, config files, reports, etc.]

Framework: [Jest snapshots / pytest-snapshot / approval tests / etc.]

I need:
1. Tests that capture the current output as a "golden" reference
2. Future changes to the output will cause test failure (intentional)
3. Easy way to update snapshots when changes are approved
4. Separate snapshots for different scenarios/inputs
5. Don't snapshot things that change every run (timestamps, random IDs)
   — show how to normalize those before snapshotting

Include instructions for updating snapshots when intentional changes are made.
```

---

## Prompt #31 — Load Test Scenario

```
Design a load test for this endpoint/service.

Target:
- Endpoint: [URL or description]
- Expected load: [e.g., 500 requests/sec, 10K concurrent users]
- SLA: [e.g., p99 < 200ms, error rate < 0.1%]

Tool preference: [k6 / Locust / Artillery / JMeter / wrk / etc.]

Write a load test script that:
1. Simulates realistic traffic patterns (not just hammering one endpoint)
2. Ramps up gradually (don't spike to full load instantly)
3. Includes think time between requests (real users pause)
4. Tests multiple user flows if applicable
5. Collects: response time (p50, p95, p99), error rate, throughput
6. Has clear pass/fail thresholds based on the SLA

Also provide:
- How to run it
- How to read the results
- Common bottlenecks to watch for at these load levels
```

---

## Prompt #32 — Test Coverage Gap Analyzer

```
Analyze my existing tests and find the gaps.

Source code:
[paste the code being tested]

Existing tests:
[paste current test file(s)]

Find:
1. **Untested functions/methods**: Public API not covered at all
2. **Untested branches**: if/else paths, switch cases, error handlers
3. **Missing edge cases**: null, empty, boundary, overflow
4. **Missing error scenarios**: what if this throws/rejects/panics?
5. **Missing integration points**: tested in isolation but not together
6. **Assertions too weak**: test runs but doesn't actually verify anything meaningful (e.g., just checks status 200, not response body)

Priority rank the gaps: Critical (could miss production bugs) → Nice-to-have.
Write the top 5 missing tests.
```
