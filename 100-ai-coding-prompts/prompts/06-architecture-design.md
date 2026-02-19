# Category 6: Architecture & System Design (10 Prompts)

---

## Prompt #53 — System Design from Scratch

```
Design a system for [describe what it does].

Requirements:
- Users: [expected number — e.g., 10K DAU, 1M monthly]
- Read/write ratio: [e.g., 100:1, 1:1]
- Latency target: [e.g., p99 < 200ms]
- Availability target: [e.g., 99.9%]
- Data volume: [e.g., 50GB/month growth]
- Budget constraints: [e.g., $500/month infrastructure]

Design:
1. **High-level architecture** (ASCII diagram showing components and data flow)
2. **Technology choices** (with justification — why X over Y)
3. **Data model** (tables/collections, key relationships)
4. **API design** (key endpoints, request/response shapes)
5. **Scaling strategy** (what happens at 10x, 100x current load)
6. **Failure modes** (what breaks first, how to handle it)
7. **Cost estimate** (rough monthly cost for the initial design)

Trade-offs: For each major decision, explicitly state what we gain and what we give up.
```

---

## Prompt #54 — Microservices vs Monolith Decision

```
Should this be a monolith or microservices? Help me decide.

Current system:
[describe what exists — monolith? Multiple services? Nothing yet?]

Team:
- Size: [number of developers]
- Experience with distributed systems: [none / some / extensive]
- Deployment frequency: [daily / weekly / monthly]

Requirements:
- [list key functional requirements]
- [list key non-functional requirements: scale, latency, availability]

Analyze:
1. **Monolith pros/cons** for this specific case (not generic advice)
2. **Microservices pros/cons** for this specific case
3. **Modular monolith** as a middle ground — viable here?
4. **Operational cost** of each approach (monitoring, debugging, deployment)
5. **Team readiness** — does this team have the skills for distributed systems?

Recommendation: Pick one and defend it with specifics. Include "migrate when..." triggers for evolving the architecture later.
```

---

## Prompt #55 — Database Schema Design

```
Design a database schema for this application.

Application description:
[describe the domain — e.g., "e-commerce platform with products, orders, users, and reviews"]

Key entities:
[list main objects and their relationships]

Query patterns (what reads happen most):
[list — e.g., "get user's order history", "search products by category", "leaderboard of top sellers"]

Write patterns:
[list — e.g., "create order with multiple items atomically", "update inventory on purchase"]

Design:
1. **Tables/Collections** with columns/fields, types, and constraints
2. **Indexes** based on the query patterns above
3. **Relationships** (foreign keys, join tables for many-to-many)
4. **Normalization decisions** (when to denormalize for performance)
5. **Timestamps/audit fields** (created_at, updated_at, soft delete?)
6. **Migration script** (CREATE TABLE statements or ORM model code)

Database: [PostgreSQL / MySQL / MongoDB / etc.]
ORM preference: [SQLAlchemy / Prisma / TypeORM / raw SQL / etc.]

Include: seed data script with realistic test data.
```

---

## Prompt #56 — Caching Strategy Designer

```
Design a caching strategy for this system.

System overview:
[describe the application and its data flow]

Current performance problem:
[describe — slow queries, high DB load, repeated API calls, etc.]

Traffic patterns:
- Read/write ratio: [e.g., 50:1]
- Hot data: [what's accessed most — e.g., "product pages", "user sessions"]
- Data freshness requirement: [real-time / seconds / minutes / hours / stale-OK]

Design:
1. **What to cache** (not everything — identify the highest-impact items)
2. **Cache location** (client, CDN, application, database query cache)
3. **Cache technology** (Redis, Memcached, in-process, HTTP cache headers)
4. **Eviction strategy** (TTL, LRU, LFU, explicit invalidation)
5. **Cache invalidation** (the hard part — how to keep cache consistent with DB)
6. **Cache warming** (preload on deploy, or lazy-load on first request?)
7. **Failure mode** (what happens when the cache is down — fallback to DB or error?)
8. **Metrics** (cache hit rate, latency with/without cache)

Show the implementation: key naming convention, read-through pattern, write-through or write-behind.
```

---

## Prompt #57 — Event-Driven Architecture Design

```
Design an event-driven architecture for this use case.

Use case:
[describe — e.g., "when a user places an order, we need to: update inventory, send confirmation email, notify warehouse, update analytics"]

Current approach:
[describe — e.g., "everything happens synchronously in one API call, taking 3-5 seconds"]

Design:
1. **Events** (define each event: name, payload schema, producer, consumers)
2. **Message broker** (Kafka, RabbitMQ, SQS, Redis Streams — pick and justify)
3. **Event flow diagram** (ASCII: producer → broker → consumers)
4. **Delivery guarantees** (at-least-once, exactly-once, at-most-once — per event)
5. **Idempotency** (how consumers handle duplicate events)
6. **Ordering** (does order matter? How to guarantee it if yes)
7. **Dead letter queue** (what happens when a consumer fails)
8. **Monitoring** (lag, processing time, error rate per consumer)
9. **Saga pattern** (if this requires distributed transactions, show the saga)

Show code for: event producer, event consumer, and retry/DLQ handling.
```

---

## Prompt #58 — API Versioning Strategy

```
Design an API versioning strategy for this service.

Current API:
[describe or paste current API endpoints]

Problem:
[why we need versioning — breaking changes coming, multiple client versions, etc.]

Clients:
[list consumers — mobile app, web frontend, partner APIs, etc.]

Evaluate these approaches for our case:
1. **URL versioning** (`/api/v1/users`, `/api/v2/users`)
2. **Header versioning** (`Accept: application/vnd.api.v2+json`)
3. **Query parameter** (`/api/users?version=2`)
4. **No versioning** (backward-compatible changes only + deprecation)

For the recommended approach:
1. Implementation plan (how to add versioning to existing code)
2. How to maintain multiple versions without duplicating all code
3. Deprecation policy (how long to keep old versions)
4. Documentation strategy (separate docs per version? Unified?)
5. Client communication plan (how to notify about deprecation)

Show the code structure: route organization, shared logic, version-specific overrides.
```

---

## Prompt #59 — Authentication & Authorization Architecture

```
Design the auth architecture for this application.

Application type: [web app / mobile app / API / multi-tenant SaaS / microservices]

Requirements:
- Users: [number, growth rate]
- User types: [e.g., admin, org member, guest, API consumer]
- Auth methods needed: [email+password, OAuth/social login, SSO/SAML, API keys]
- MFA required: [yes/no, for which user types]
- Session duration: [e.g., 30 min idle, 24h absolute]

Design:
1. **Authentication flow** (registration, login, logout, password reset)
2. **Token strategy** (JWT vs sessions, access + refresh tokens, token storage)
3. **Authorization model** (RBAC, ABAC, or simple role checks)
4. **Permission structure** (roles → permissions matrix)
5. **Token security** (signing algorithm, expiration, rotation)
6. **Cross-service auth** (if microservices: how do services verify tokens?)
7. **Rate limiting** (login attempts, password reset requests)
8. **Audit logging** (what auth events to log)

Include: Database schema for users/roles/permissions, middleware code for auth verification, and example protected endpoint.
```

---

## Prompt #60 — Monitoring & Observability Design

```
Design a monitoring and observability stack for this system.

System:
[describe architecture — number of services, infrastructure, traffic volume]

Current visibility: [none / basic logs / some metrics / ???]

Design:
1. **Metrics** (what to measure)
   - Infrastructure: CPU, memory, disk, network
   - Application: request rate, error rate, latency (RED method)
   - Business: signups, purchases, feature usage
   - Which tool: [Prometheus / Datadog / CloudWatch / etc.]

2. **Logging** (what to log)
   - Structured logging format (JSON with consistent fields)
   - Log levels strategy (when DEBUG vs INFO vs ERROR)
   - Correlation IDs (trace requests across services)
   - Which tool: [ELK / Loki / CloudWatch Logs / etc.]

3. **Tracing** (distributed tracing)
   - Which requests to trace (sampling strategy)
   - Which tool: [Jaeger / Zipkin / Tempo / etc.]

4. **Alerting** (when to wake someone up)
   - Critical alerts: [list scenarios — downtime, error spike, data loss]
   - Warning alerts: [list — degraded performance, disk filling, cert expiring]
   - Alert fatigue prevention (no flappy alerts, proper thresholds)

5. **Dashboards** (what to display)
   - Ops dashboard (system health at a glance)
   - Service dashboard (per-service deep dive)
   - Business dashboard (KPIs for stakeholders)

Include: example Grafana/dashboard JSON or Prometheus alert rules.
```

---

## Prompt #61 — Data Pipeline Architecture

```
Design a data pipeline for this use case.

Input: [describe data sources — database, API, files, streams]
Output: [describe where data needs to go — data warehouse, dashboard, ML model, API]
Volume: [e.g., 10K events/sec, 50GB/day, 1TB historical]
Freshness: [real-time / near-real-time / hourly / daily batch]

Design:
1. **Ingestion** (how data gets in: CDC, webhooks, polling, file drops)
2. **Processing** (transform, clean, enrich, aggregate)
3. **Storage** (raw → processed → serving layers)
4. **Orchestration** (what triggers each step: schedule, event, dependency)
5. **Schema management** (how to handle schema changes without breaking things)
6. **Backfill strategy** (how to reprocess historical data when logic changes)
7. **Monitoring** (data quality checks, pipeline lag, failure alerts)
8. **Cost** (estimate monthly cost at current + 10x volume)

Tools: [prefer specific tools — e.g., Kafka, Spark, dbt, Airflow, BigQuery]
Show the pipeline as an ASCII diagram with data flow and processing stages.
```

---

## Prompt #62 — Feature Flag System Design

```
Design a feature flag system for this team.

Team size: [number of developers]
Deployment frequency: [how often]
Current feature branching pain: [describe — long-lived branches, merge conflicts, etc.]

Requirements:
- Simple on/off toggles
- Percentage rollout (release to 10% of users first)
- User targeting (enable for specific users/groups)
- A/B testing support (optional)
- Kill switch (disable a feature instantly in production)

Design:
1. **Flag storage** (database, config file, dedicated service, third-party)
2. **Evaluation logic** (how the app checks if a flag is enabled for a user)
3. **Admin interface** (how developers create/modify flags)
4. **SDK/client code** (how to use flags in application code — keep it simple)
5. **Flag lifecycle** (temporary experiment → permanent → cleanup)
6. **Performance** (flag evaluation must be fast — how to avoid DB call per request)
7. **Audit trail** (who changed what flag, when)

Build vs buy analysis: [LaunchDarkly / Unleash / Flagsmith / custom — with cost comparison]

Show: implementation code for the SDK/client, example usage in a feature, and the cleanup checklist for removing a flag.
```
