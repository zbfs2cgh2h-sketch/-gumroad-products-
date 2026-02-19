# Category 5: Refactoring & Code Quality (10 Prompts)

---

## Prompt #43 — Extract and Decompose

```
This function/class is too big. Break it apart.

Code:
[paste the oversized function or class]

Current responsibilities (what this code does):
[list 2-5 things, or say "figure it out"]

Rules:
1. Each extracted function/class should have ONE clear responsibility
2. Function names should describe WHAT, not HOW (e.g., `validate_email` not `check_string_format`)
3. Keep the public API the same (callers shouldn't need to change)
4. No function longer than 30 lines
5. Show me the dependency graph between the new pieces

Show:
- The refactored code (complete, not snippets)
- A before/after comparison of the call flow
- Which tests need updating (if test file provided)
```

---

## Prompt #44 — Remove Duplication (DRY Refactor)

```
Find and eliminate duplicated code.

Code files:
[paste 2+ files with suspected duplication]

Find:
1. Exact duplicates (copy-paste code)
2. Structural duplicates (same pattern, different variables)
3. Logical duplicates (different code that does the same thing)

For each duplication:
- Show both locations
- Extract a shared function/module/mixin
- Show how both call sites use the shared version
- Explain if any duplication is actually OKAY to keep (sometimes DRY is wrong)

Don't create abstractions more complex than the duplication they eliminate.
```

---

## Prompt #45 — Modernize Legacy Code

```
Modernize this code to use current language features and best practices.

Code:
[paste legacy code]

Language version: [current — e.g., Python 3.12, ES2024, Java 21]
Original language version (if known): [e.g., Python 2.7, ES5, Java 8]

Modernize:
1. Replace deprecated APIs with current equivalents
2. Use modern syntax (f-strings, destructuring, pattern matching, etc.)
3. Replace hand-rolled utilities with standard library equivalents
4. Update error handling patterns
5. Use type hints/annotations if the language supports them
6. Replace callbacks with async/await if applicable

Keep the same logic and behavior. Mark each change with a comment explaining what's different and why.
```

---

## Prompt #46 — Add Type Safety

```
Add type annotations/definitions to this code.

Code:
[paste untyped code]

Language: [TypeScript / Python (type hints) / Java (generics) / etc.]

Requirements:
1. Type every function parameter and return value
2. Type complex objects (create interfaces/types/dataclasses for shapes)
3. Handle nullable/optional types explicitly (no implicit any/Any/Object)
4. Use union types where multiple types are valid
5. Use generics where the same logic works for multiple types
6. Don't just slap `any` everywhere — that defeats the purpose

For ambiguous types (could be string or number), add a TODO comment asking for clarification.
Return the fully typed code.
```

---

## Prompt #47 — Simplify Complex Conditionals

```
Simplify this conditional logic. It's gotten out of hand.

Code:
[paste code with complex if/else chains, nested ternaries, or switch statements]

What the code is supposed to do:
[describe the business logic in plain language]

Simplification strategies to consider:
1. Guard clauses (early return instead of nesting)
2. Lookup tables/maps instead of if chains
3. Strategy pattern instead of type-checking switches
4. Polymorphism instead of instanceof checks
5. State machine if the logic is state-dependent
6. Extract predicate functions (readable boolean expressions)

Show:
- The simplified version
- A truth table or decision matrix proving it's equivalent
- Cyclomatic complexity before and after
```

---

## Prompt #48 — Dependency Injection Refactor

```
Refactor this code to use dependency injection. Currently it creates its own dependencies internally.

Code:
[paste code with hardcoded dependencies — new SomeService(), direct DB calls, etc.]

Problems with current code:
1. Can't test without hitting real [database / API / file system]
2. Can't swap implementations (e.g., switch from MySQL to PostgreSQL)
3. Configuration is scattered throughout the code

Refactor to:
1. Accept dependencies through constructor/function parameters
2. Define interfaces/protocols for each dependency
3. Create a composition root / factory that wires everything together
4. Show how to test with mock dependencies

Pattern preference: [constructor injection / factory / service locator / DI container — or let the AI choose]

Show both the refactored code and a test demonstrating the improved testability.
```

---

## Prompt #49 — Error Handling Overhaul

```
Overhaul the error handling in this code. It's a mess.

Code:
[paste code]

Current problems (check all that apply):
- [ ] Bare except/catch that swallows errors silently
- [ ] Same error handling copy-pasted everywhere
- [ ] Errors not logged or logged without context
- [ ] User sees raw stack traces
- [ ] No distinction between recoverable and fatal errors
- [ ] Resources not cleaned up on error

Redesign error handling with:
1. Custom error types/classes for domain-specific errors
2. Appropriate granularity (don't catch everything at the top)
3. Error context (stack trace, input values, operation being attempted)
4. User-facing vs. developer-facing error messages
5. Cleanup in finally/defer/with blocks
6. Error propagation strategy (when to catch, when to let it bubble)

Show the complete refactored code, not just the error handling bits.
```

---

## Prompt #50 — Performance Refactor

```
Refactor this code for better performance. Don't change what it does, just how fast it does it.

Code:
[paste code]

Performance problem: [describe — slow response, high memory, CPU spikes]
Current numbers: [e.g., 2.3s for 10K records, 500MB memory usage]
Target numbers: [e.g., <200ms, <50MB]

Optimization strategies to consider:
1. Algorithm change (O(n²) → O(n log n))
2. Data structure swap (array → hash map, list → set)
3. Caching (memoization, LRU cache)
4. Lazy loading / pagination
5. Batch processing instead of one-by-one
6. Reduce allocations (reuse objects, pre-allocate)
7. Async/parallel processing where possible

For each optimization:
- What it changes
- Expected improvement (with reasoning)
- Any trade-offs (memory vs speed, complexity vs readability)

Include before/after benchmarking code.
```

---

## Prompt #51 — Convert Callbacks to Async/Await

```
Convert this callback-based (or promise-chain) code to async/await.

Code:
[paste code with callbacks, .then() chains, or nested async patterns]

Language: [JavaScript/TypeScript / Python / C# / etc.]

Requirements:
1. Replace every callback/promise chain with async/await
2. Preserve error handling (callbacks with err param → try/catch)
3. Convert parallel callbacks to Promise.all / asyncio.gather equivalent
4. Don't accidentally make parallel operations sequential
5. Handle cleanup properly (close connections, release resources)
6. Mark every function in the call chain that needs to be async

Show the complete converted code and highlight any behavior differences.
```

---

## Prompt #52 — Configuration Refactor

```
The configuration in this code is a mess. Centralize and clean it up.

Code:
[paste code with scattered config — hardcoded values, magic numbers, inline URLs, etc.]

Current config problems:
- Hardcoded values that should be configurable
- Config values defined in multiple places
- No validation on config values
- No clear defaults
- Sensitive values (API keys, passwords) mixed with regular config

Refactor to:
1. Single configuration source (file, env vars, or config class)
2. Typed config with validation (reject invalid values at startup, not runtime)
3. Clear defaults for optional values
4. Separate sensitive config (secrets) from regular config
5. Environment-specific overrides (dev / staging / prod)
6. Document every config option (what it does, valid values, default)

Show the config schema, loading code, and updated application code.
```
