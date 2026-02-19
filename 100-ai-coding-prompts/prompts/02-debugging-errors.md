# Category 2: Debugging & Error Resolution (10 Prompts)

---

## Prompt #13 — Stack Trace Decoder

```
Decode this error and tell me exactly what's broken.

Error + stack trace:
[paste full error output]

My code:
[paste the relevant file(s)]

Language/framework: [e.g., Python 3.12, FastAPI]
Last working state: [what changed recently, if known]

I need:
1. Root cause (not just "there's an error on line X")
2. Why this error happens (the underlying mechanism)
3. The exact fix (code, not advice)
4. How to prevent this class of error in the future
```

---

## Prompt #14 — "It Works on My Machine" Debugger

```
This code works locally but fails in [production / staging / CI / Docker].

Code:
[paste code]

Local environment:
- OS: [e.g., macOS 14, Ubuntu 22.04]
- Runtime version: [e.g., Node 20.11, Python 3.12]
- Relevant env vars: [list them]

Failing environment:
- OS: [e.g., Alpine Linux in Docker]
- Runtime version: [version]
- Error: [paste error or describe behavior]

Common suspects to investigate:
1. File path separators (/ vs \)
2. Missing system dependencies (native modules, shared libraries)
3. Environment variable differences
4. File permissions
5. DNS resolution / networking
6. Timezone differences
7. Locale/encoding (UTF-8 assumptions)

Walk through each possibility and tell me which one is most likely given the error.
```

---

## Prompt #15 — Intermittent Bug Hunter

```
I have a bug that only happens sometimes. Help me track it down.

Symptoms:
- What happens: [describe the intermittent failure]
- Frequency: [e.g., ~1 in 20 requests, every few hours, only under load]
- When it started: [date/deploy if known]

Relevant code:
[paste code]

What I've checked:
[list what you've already investigated]

This smells like: (check what applies)
- [ ] Race condition
- [ ] Resource exhaustion (connections, memory, file handles)
- [ ] Timeout under load
- [ ] Stale cache
- [ ] External dependency flakiness
- [ ] Floating-point or time-based comparison

For the most likely cause:
1. Explain the exact sequence of events that triggers it
2. Show me how to add logging/instrumentation to confirm
3. Provide the fix
4. Provide a test that reliably reproduces it
```

---

## Prompt #16 — Performance Degradation Diagnosis

```
My application got slower. Help me find out why.

Before: [describe performance — e.g., API responded in 50ms, page loaded in 1.2s]
After: [current performance — e.g., 800ms response time, 5s page load]

What changed recently:
[list recent deploys, config changes, traffic changes]

Available data:
[paste any of: slow query log, profiler output, APM trace, htop output, error logs]

Code that might be involved:
[paste suspicious code]

Investigate:
1. Is it CPU, memory, I/O, or network bound?
2. New N+1 queries or missing indexes?
3. Connection pool exhaustion?
4. Increased payload sizes?
5. External service latency increase?
6. Missing caching that existed before?

Give me a ranked list of suspects with specific diagnostic commands to run.
```

---

## Prompt #17 — Data Inconsistency Debugger

```
I'm seeing inconsistent data. Some records have wrong values.

What's wrong:
[describe the data inconsistency — e.g., "order totals don't match line items"]

Database/storage: [PostgreSQL, MongoDB, Redis, etc.]
Application code that writes this data:
[paste code]

Known facts:
- First noticed: [when]
- Affected records: [count or pattern — e.g., "only orders from last week"]
- Concurrent writers: [yes/no, how many processes write to this table]

Possible causes to investigate:
1. Race condition between concurrent writes
2. Missing transaction boundaries
3. Partial failure (step 1 succeeds, step 2 fails, no rollback)
4. Stale read (reading cached/old value, writing based on it)
5. Schema migration that didn't backfill correctly
6. Application bug in calculation logic

For each plausible cause, show me a diagnostic query to confirm or rule it out.
```

---

## Prompt #18 — Dependency Conflict Resolver

```
I'm hitting a dependency conflict and can't install/build.

Error:
[paste full error output from pip/npm/cargo/maven/etc.]

My dependency file:
[paste requirements.txt / package.json / Cargo.toml / etc.]

What I've tried:
[list attempts]

I need:
1. Explain which packages conflict and why
2. Show the dependency tree (which package requires which version)
3. Give me the resolution (version pins, overrides, or alternative packages)
4. Tell me if the resolution introduces any risk (using an older/beta version)
```

---

## Prompt #19 — Docker Container Debugger

```
My Docker container won't start / crashes / behaves differently than expected.

Dockerfile:
[paste Dockerfile]

docker-compose.yml (if applicable):
[paste compose file]

Error output:
[paste docker logs or error]

The app works outside Docker: [yes/no]

Check:
1. Base image compatibility (Alpine missing glibc? Slim missing packages?)
2. Build step failures (are dependencies installed at build time?)
3. Runtime config (env vars, volume mounts, network)
4. Port mapping issues
5. File permission issues (running as non-root?)
6. Health check failures
7. Resource limits (memory, CPU)

Provide the fixed Dockerfile/compose with inline comments explaining each change.
```

---

## Prompt #20 — Auth Flow Debugger

```
Authentication/authorization isn't working right.

Symptoms:
[describe: 401s? 403s? Token expired? Wrong user data? CORS preflight failing?]

Auth implementation:
[paste relevant auth code — middleware, token generation, verification]

Auth flow:
1. Login: [describe how user logs in]
2. Token: [JWT / session / OAuth — describe token type and storage]
3. Verification: [how does the server verify each request]

Network info (if applicable):
[paste relevant request/response headers, especially Authorization, Set-Cookie, CORS headers]

Common auth bugs to check:
1. Token not being sent (cookie settings, header missing)
2. Token expired but not refreshed
3. Wrong secret/key between services
4. Clock skew between servers (JWT exp validation)
5. CORS blocking preflight with credentials
6. Same-site cookie policy blocking cross-origin

Trace the exact request flow and point to where it breaks.
```

---

## Prompt #21 — "Why Is This Slow?" Query Analyzer

```
This query is slow. Make it fast.

Query:
[paste SQL query]

EXPLAIN/EXPLAIN ANALYZE output:
[paste query plan]

Table info:
- Table(s): [name, approximate row count]
- Existing indexes: [list them]
- Database: [PostgreSQL / MySQL / SQLite / etc.]

Current execution time: [e.g., 3.2 seconds]
Target execution time: [e.g., <100ms]

I need:
1. Read the query plan and point to the bottleneck (seq scan, sort, nested loop)
2. Suggest index(es) to create (with exact CREATE INDEX statement)
3. Rewrite the query if the current structure is fundamentally slow
4. Estimate the improvement
5. Warn about any trade-offs (index write overhead, space)
```

---

## Prompt #22 — Environment Variable Missing / Wrong

```
My app is reading the wrong config or missing an env variable.

Expected behavior: [what should happen]
Actual behavior: [what's happening — wrong values, defaults being used, crash]

How I set the env vars:
[paste: .env file, docker-compose env section, export commands, etc.]

How my code reads them:
[paste config loading code]

Environment: [local / Docker / Kubernetes / Heroku / Vercel / etc.]

Debug steps to perform:
1. Print all env vars the app sees at startup (give me the code to add)
2. Check for: typos in var names, whitespace in values, quotes being included literally
3. Check for: .env file not being loaded, wrong .env file being loaded
4. Check for: env vars being overridden (system > .env, docker > .env)
5. Check for: runtime vs build-time env vars (common in Next.js, Vite)

Show the fix.
```
