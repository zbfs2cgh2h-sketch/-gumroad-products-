# Category 4: Documentation & Technical Writing (10 Prompts)

---

## Prompt #33 — README Generator (Production-Grade)

```
Write a README.md that makes someone actually want to use this project.

Project info:
- Name: [name]
- One-line description: [what it does]
- Language/framework: [tech stack]
- Target audience: [who is this for]

Code/project structure:
[paste file tree or main entry point]

Include these sections:
1. **Badges** (build status, version, license — use shields.io format)
2. **TL;DR** — What it does in 2 sentences, with a screenshot/GIF placeholder
3. **Quick Start** — From `git clone` to "it works" in under 2 minutes
4. **Installation** — System requirements, package manager commands
5. **Usage** — 3 real-world examples (simple, medium, advanced)
6. **Configuration** — All options with defaults and descriptions
7. **API Reference** — If applicable, link or inline
8. **Troubleshooting** — Top 5 issues people will hit
9. **Contributing** — How to set up dev environment, run tests, submit PRs
10. **License** — [specify]

Tone: Technical but friendly. No marketing fluff. Show, don't tell.
```

---

## Prompt #34 — Inline Code Documentation

```
Add documentation to this code. I need someone new to understand it within 10 minutes.

Code:
[paste code]

Language: [language]
Doc style: [JSDoc / Sphinx / Javadoc / Godoc / Rustdoc / inline comments]

Rules:
1. Document EVERY public function/method/class
2. Include: what it does, parameters (with types), return value, exceptions/errors
3. Add usage example for non-obvious functions
4. Document WHY for any non-obvious logic (not WHAT — the code already says what)
5. Don't document obvious things (don't write "// increment i" above "i++")
6. Flag any "here be dragons" sections with warnings
7. Use the actual doc format that generates API docs for this language

Return the complete file with documentation added inline.
```

---

## Prompt #35 — API Documentation Writer

```
Write developer-facing API documentation from this code.

API code:
[paste endpoint handlers, route definitions, or OpenAPI spec]

For each endpoint, document:
1. **Method + Path** (e.g., `POST /api/v1/users`)
2. **Description** (what it does, when to use it)
3. **Authentication** (required? What type?)
4. **Request**: Headers, query params, path params, request body (with JSON schema)
5. **Response**: Status codes, response body (with JSON examples)
6. **Errors**: Every error code this endpoint can return, with meaning
7. **Rate Limits**: If applicable
8. **Example**: Complete curl command that actually works

Format: [Markdown / OpenAPI 3.0 YAML / Slate / Redoc]

Include a "Getting Started" section: get an API key → make your first request → handle the response.
```

---

## Prompt #36 — Architecture Decision Record (ADR)

```
Write an Architecture Decision Record for this technical decision.

Decision: [what we decided — e.g., "Use PostgreSQL instead of MongoDB for the user service"]

Context:
[describe the situation — what problem were we solving, what constraints exist]

Options we considered:
1. [Option A] — [brief description]
2. [Option B] — [brief description]
3. [Option C] — [brief description]

Format (Michael Nygard's ADR template):
1. **Title**: Short descriptive title
2. **Status**: Proposed / Accepted / Deprecated / Superseded
3. **Context**: The forces at play (technical, business, team constraints)
4. **Decision**: What we chose and why
5. **Consequences**: 
   - Positive: What gets better
   - Negative: What gets worse or harder
   - Neutral: What changes but isn't clearly better/worse
6. **Alternatives Rejected**: Why the other options lost

Keep it under 500 words. Future-you should understand this in 2 minutes.
```

---

## Prompt #37 — Runbook / Incident Response Doc

```
Write an operational runbook for this system/service.

Service: [name and what it does]
Infrastructure: [where it runs — AWS, GCP, k8s, bare metal]
Dependencies: [databases, caches, message queues, external APIs]

Include:
1. **Service Overview**: What it does, why it matters, who owns it
2. **Health Checks**: How to verify the service is healthy (URLs, commands)
3. **Common Alerts & Fixes**:
   - Alert: [description] → Diagnosis: [commands to run] → Fix: [steps]
   - (Cover at least 5 common scenarios)
4. **Scaling**: How to scale up/down (manual and auto-scaling config)
5. **Restart Procedure**: How to safely restart without dropping requests
6. **Rollback Procedure**: How to roll back a bad deploy
7. **Disaster Recovery**: What to do if the service is completely down
8. **Contact**: On-call rotation, escalation path

This will be read at 3am by someone half-asleep. Make it scannable and unambiguous.
```

---

## Prompt #38 — Changelog Generator

```
Generate a user-facing changelog from these commits/PRs.

Git log or PR list:
[paste git log --oneline or PR titles/descriptions]

Previous version: [e.g., v2.3.0]
New version: [e.g., v2.4.0]

Rules:
1. Group by: ✨ Features / 🐛 Bug Fixes / ⚡ Performance / 🔧 Maintenance / 💥 Breaking Changes
2. Write for users, not developers (they don't care about "refactored internal module")
3. Each item: one sentence, past tense, starts with a verb
4. Include PR/issue numbers as links
5. Highlight breaking changes with migration instructions
6. If a commit is purely internal (CI config, dev tooling), skip it

Format: Keep a Changelog (keepachangelog.com) style.
```

---

## Prompt #39 — Onboarding Guide for New Developers

```
Write a "Getting Started" guide for a new developer joining this project.

Project: [name]
Tech stack: [languages, frameworks, tools]
Repo structure: [paste file tree]
Local dev setup: [any special requirements — Docker, specific DB, etc.]

Write a guide that covers:
1. **Day 1 Setup** (clone → install → run → see it working)
   - Every command they need to type
   - Expected output at each step
   - Common setup failures and fixes
2. **Codebase Tour** (where's what)
   - Entry points
   - Key directories and their purpose
   - Config files that matter
3. **Development Workflow** (how we work)
   - Branching strategy
   - How to run tests
   - How to create and submit a PR
   - Code review expectations
4. **First Task** (suggest a good first issue)
   - A small, self-contained change they can make today
   - Touches one file, has tests, builds confidence

Assume they're a competent developer who's never seen this codebase. Don't explain Git or what a function is.
```

---

## Prompt #40 — Technical Spec / Design Doc

```
Write a technical design document for this feature.

Feature: [name and 1-sentence description]
Problem: [what user/business problem this solves]
Scope: [what's included and what's explicitly NOT included]

Structure:
1. **Overview**: What we're building and why (3-5 sentences)
2. **Goals**: Measurable outcomes (e.g., "reduce checkout time from 8 clicks to 3")
3. **Non-Goals**: What we're NOT doing (prevent scope creep)
4. **Proposed Solution**: 
   - Architecture diagram (describe in text/ASCII)
   - Data model changes
   - API changes
   - Key algorithms or logic
5. **Alternatives Considered**: What else we could do and why we didn't
6. **Risks & Mitigations**: What could go wrong
7. **Rollout Plan**: Feature flags? Gradual rollout? A/B test?
8. **Metrics**: How we'll know it's working
9. **Timeline**: Rough phases with estimates
10. **Open Questions**: Things we still need to decide

This should be enough for a senior engineer to implement without asking 20 questions.
```

---

## Prompt #41 — Error Message Writer

```
Write user-facing error messages for these error scenarios.

Scenarios:
[list error scenarios, e.g.:
- Email already registered
- Payment declined
- File too large (max 10MB)
- Rate limit exceeded
- Server error]

For each error, provide:
1. **Title**: Short, scannable (e.g., "Email already in use")
2. **Message**: What happened in plain language (no jargon, no blame)
3. **Action**: What the user can do to fix it
4. **Technical detail** (for logs/developers, not shown to users)

Rules:
- Never blame the user ("You entered an invalid email" → "This email format isn't recognized")
- Never be vague ("Something went wrong" → "We couldn't process your payment — your card wasn't charged")
- Always include a next step
- Be specific about limits ("File must be under 10MB" not "File too large")
- For server errors: apologize briefly, offer retry, provide support contact
```

---

## Prompt #42 — Migration Guide

```
Write a migration guide from v[X] to v[Y] of this library/framework/API.

Breaking changes:
[list all breaking changes]

New features relevant to migration:
[list new features that replace old ones]

Deprecated features:
[list what's deprecated and what replaces it]

Structure the guide as:
1. **Before You Start**: Prerequisites, backup instructions, estimated time
2. **Step-by-Step Migration**:
   - For each breaking change:
     - What changed
     - Before (old code)
     - After (new code)
     - Search pattern (regex) to find all instances in your codebase
3. **Deprecated → New**: Mapping table of old → new APIs
4. **Testing After Migration**: What to verify works
5. **Rollback Plan**: How to undo if things break
6. **FAQ**: Common issues people hit during this migration

Include a `grep` or `codemod` command for each change so they can find all affected code.
```
