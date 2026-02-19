# Category 1: Code Review & Security Audit (12 Prompts)

---

## Prompt #1 — Full Security Audit

```
You're a senior security engineer. Audit this code for vulnerabilities.

Code:
[paste code]

Check for:
1. Injection flaws (SQL, NoSQL, command, LDAP)
2. Broken authentication or session management
3. Sensitive data exposure (hardcoded secrets, logging PII)
4. Missing input validation or sanitization
5. Insecure deserialization
6. Known vulnerable dependencies (if imports visible)

For each finding:
- Severity: Critical / High / Medium / Low
- Line number(s)
- What the vulnerability is
- Proof-of-concept exploit (1-2 lines showing how it breaks)
- Fix with code diff

If nothing found, say "No issues found" — don't invent problems.
```

---

## Prompt #2 — PR Review (Production Quality)

```
Review this pull request diff as a senior developer who's on-call this week.

Diff:
[paste git diff or code changes]

Context: This is going to production. Focus on:
1. Logic bugs (off-by-one, null handling, race conditions)
2. Error handling (what happens when things fail?)
3. Performance regressions (new O(n²) loops, missing indexes, N+1 queries)
4. API contract changes (breaking changes for consumers?)
5. Missing tests for new code paths

Format your review as GitHub PR comments:
- File: [filename]
- Line: [number]
- Comment: [your review]
- Severity: Blocker / Suggestion / Nit
```

---

## Prompt #3 — Memory Leak Detection

```
Analyze this code for memory leaks and resource management issues.

Language: [language]
Code:
[paste code]

Check for:
1. Resources opened but never closed (files, connections, sockets)
2. Event listeners registered but never removed
3. Circular references preventing garbage collection
4. Growing collections that are never pruned
5. Closures capturing more than they should
6. Missing cleanup in error/exception paths

For each issue, show the fix and explain why it leaks.
```

---

## Prompt #4 — Concurrency Safety Review

```
Review this code for concurrency and thread-safety issues.

Code:
[paste code]

Concurrency model: [threads / asyncio / goroutines / actors / etc.]
Shared state: [describe any shared variables, databases, files]

Look for:
1. Race conditions
2. Deadlock potential
3. Starvation scenarios
4. Atomicity violations (check-then-act patterns)
5. Missing synchronization on shared state
6. Unsafe use of non-thread-safe data structures

For each issue, provide:
- Description of the race/deadlock scenario
- Steps to reproduce (A does X, B does Y, then...)
- Thread-safe fix using [language-appropriate primitives]
```

---

## Prompt #5 — Input Validation Audit

```
Audit every input boundary in this code.

Code:
[paste code]

Map every place where external data enters the system:
- User input (forms, query params, request bodies)
- File uploads
- API responses from third parties
- Database reads
- Environment variables
- Command-line arguments

For each input boundary:
1. What validation exists (if any)
2. What validation is missing
3. What an attacker could send to break it
4. The fix (validation code, not just "add validation")
```

---

## Prompt #6 — Error Handling Review

```
Review the error handling in this code. I want to know what happens when things go wrong.

Code:
[paste code]

For every operation that can fail:
1. Is the error caught?
2. Is it caught too broadly (bare except, catch Exception)?
3. Is the error logged with enough context to debug at 3am?
4. Is the error communicated to the caller (return value, exception, error code)?
5. Are resources cleaned up in the error path?
6. Could this error cascade and take down unrelated features?

Rate the overall error handling: Robust / Adequate / Brittle / Dangerous
Provide a refactored version of the worst section.
```

---

## Prompt #7 — Dependency Risk Assessment

```
Evaluate the dependencies in this project for risk.

Dependencies:
[paste package.json / requirements.txt / go.mod / Cargo.toml / etc.]

For each dependency:
1. Last updated (is it maintained?)
2. Known CVEs (check version numbers)
3. Bus factor (1 maintainer = risk)
4. License compatibility with [MIT / Apache / GPL — specify yours]
5. Size/weight (do we import 50KB for one function?)
6. Alternatives if this dep dies

Flag any dependency that hasn't been updated in 12+ months.
Rate overall dependency health: Healthy / Concerning / Critical
```

---

## Prompt #8 — API Security Checklist

```
I'm exposing this API to the internet. Review it for security.

API code:
[paste endpoint handlers/controllers]

Check:
1. Authentication: Is every endpoint properly authenticated?
2. Authorization: Can user A access user B's data?
3. Rate limiting: Can someone hammer this endpoint?
4. Input size limits: Can someone send a 10GB request body?
5. Response data: Am I leaking internal IDs, stack traces, or PII?
6. CORS: Is the policy correct, or wide open?
7. HTTPS: Any HTTP-only paths?
8. CSRF/SSRF: Applicable to this API?

Provide a scored checklist (pass/fail/partial for each item).
```

---

## Prompt #9 — Code Smell Detector

```
Scan this code for code smells and anti-patterns.

Code:
[paste code]

Language: [language]
Framework: [framework, if applicable]

Flag:
1. God classes / functions (>100 lines or >5 responsibilities)
2. Feature envy (method uses another class more than its own)
3. Primitive obsession (strings/ints where domain types belong)
4. Shotgun surgery (one change requires editing 5+ files)
5. Dead code (unreachable branches, unused parameters)
6. Magic numbers/strings
7. Copy-paste code (duplicated logic)
8. Inappropriate intimacy between modules

For each smell: location, why it's a problem, and a concrete refactoring step.
```

---

## Prompt #10 — Backward Compatibility Check

```
I'm changing this code. Will it break existing consumers?

Current code (before):
[paste current version]

New code (after):
[paste proposed changes]

Consumers include:
- [list: other services, frontend apps, SDKs, CLI users, etc.]

Check for:
1. Removed or renamed public functions/methods
2. Changed function signatures (new required params, type changes)
3. Different return types or response shapes
4. Changed error types or error messages that consumers might match on
5. Environment/config changes needed
6. Database schema changes that require migration

Verdict: Breaking / Non-breaking / Breaking-with-migration-path
If breaking, provide a migration guide for consumers.
```

---

## Prompt #11 — Performance Review (Micro)

```
Review this code strictly for performance. I don't care about style right now.

Code:
[paste code]

Expected load: [requests/sec, data volume, concurrent users]

Find:
1. Unnecessary allocations (creating objects in hot loops)
2. Redundant computations (same calculation done multiple times)
3. Missing caching opportunities
4. Suboptimal data structures (array where a set would be O(1))
5. Blocking calls in async paths
6. Missing early returns / short circuits

For each issue:
- Current time complexity
- Optimized time complexity
- Code diff showing the fix
- Estimated improvement (2x, 10x, marginal)
```

---

## Prompt #12 — Accessibility & i18n Review (Frontend)

```
Review this frontend code for accessibility and internationalization.

Code:
[paste component/template code]

Check accessibility:
1. Semantic HTML (div soup vs proper elements)
2. ARIA labels on interactive elements
3. Keyboard navigation (Tab order, focus management)
4. Color contrast issues (if CSS is provided)
5. Screen reader compatibility
6. Alt text on images

Check i18n:
1. Hardcoded strings that should be in translation files
2. Date/number formatting assumptions
3. RTL layout support
4. String concatenation that breaks in other languages
5. Pluralization handling

Provide fixes with code examples.
```
