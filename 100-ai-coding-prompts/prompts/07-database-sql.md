# Category 7: Database & SQL Optimization (10 Prompts)

---

## Prompt #63 — Query Optimizer

```
Optimize this slow SQL query.

Query:
[paste SQL]

EXPLAIN ANALYZE output:
[paste query plan — if not available, describe the table sizes]

Table schemas:
[paste CREATE TABLE statements or describe columns + types]

Table sizes:
[approximate row counts for each table]

Existing indexes:
[list them, or say "none" / "unknown"]

Current execution time: [e.g., 3.4 seconds]
Target: [e.g., <100ms]

I need:
1. Read the query plan and explain the bottleneck in plain English
2. Suggest indexes (with exact CREATE INDEX statements)
3. Rewrite the query if structural changes would help
4. Estimate improvement for each change
5. Warn if any optimization hurts write performance
```

---

## Prompt #64 — N+1 Query Detector and Fixer

```
Find and fix N+1 query problems in this code.

Code:
[paste ORM/database code — the full data access layer or controller]

ORM: [SQLAlchemy / Django ORM / ActiveRecord / Prisma / TypeORM / Sequelize / etc.]

Symptoms:
[e.g., "page takes 2s to load", "I see 500 queries in my APM for one page", or "just audit it"]

For each N+1 found:
1. Show which line triggers the N+1
2. How many extra queries it generates (e.g., "1 + N where N = number of orders")
3. The fix: eager loading, joins, or subquery (show exact ORM code)
4. Before/after query count

Also check for:
- Queries inside loops
- Lazy loading in serializers/templates
- Missing select_related / prefetch_related / include / eager_load
```

---

## Prompt #65 — Schema Migration Writer

```
Write a database migration for this schema change.

Current schema:
[paste current CREATE TABLE or ORM model]

Desired schema change:
[describe what needs to change — new column, rename, type change, new table, etc.]

Database: [PostgreSQL / MySQL / SQLite / etc.]
Migration tool: [Alembic / Django migrations / Prisma / Flyway / Knex / raw SQL]

Requirements:
1. Forward migration (apply the change)
2. Backward migration (rollback — undo the change)
3. Handle existing data (if adding NOT NULL column, what's the default? If changing types, how to convert?)
4. Zero-downtime compatible (no locks on large tables, no column drops that break running code)
5. Test data migration (if data needs transforming, include the transform logic)

If the migration involves a large table (>1M rows), show the approach for running it without locking the table.
```

---

## Prompt #66 — Complex Report Query Builder

```
Build a SQL query for this business report.

Report requirements:
[describe in plain language — e.g., "Monthly revenue by product category, with comparison to previous month and YoY growth, for the last 12 months"]

Tables available:
[paste schema or describe tables and columns]

Output should include:
[list exact columns the report needs]

Additional requirements:
- [ ] Handle NULL values gracefully (show 0, not NULL)
- [ ] Handle division by zero (growth calculation when previous = 0)
- [ ] Time zone: [UTC / specific timezone]
- [ ] Currency/amount format: [cents to dollars? Rounding?]
- [ ] Pagination: [yes — offset/limit or cursor-based]

Database: [PostgreSQL / MySQL / etc.]

Provide:
1. The query (with comments explaining each CTE/subquery)
2. Expected output example (sample rows)
3. Indexes needed to make this query fast
4. How to schedule this as a materialized view or batch job if it's too slow for real-time
```

---

## Prompt #67 — Database Index Strategy

```
Design an indexing strategy for this table.

Table schema:
[paste CREATE TABLE]

Row count: [current and growth rate]

Query patterns (ranked by frequency):
1. [most common query — e.g., "SELECT * FROM users WHERE email = ?"]
2. [second most common]
3. [third]
4. [etc.]

Write patterns:
[describe — e.g., "100 inserts/sec, 50 updates/sec on status column"]

Current indexes:
[list existing, or "just the primary key"]

I need:
1. Which indexes to create (with exact SQL)
2. Which indexes to drop (unused or redundant)
3. Composite index strategy (column order matters — explain why)
4. Covering indexes for the top queries (avoid table lookups)
5. Partial indexes where applicable (e.g., WHERE status = 'active')
6. Impact on write performance (each index slows writes — quantify the trade-off)
7. Estimated storage overhead for each index

Database: [PostgreSQL / MySQL / etc.]
```

---

## Prompt #68 — Data Model Review

```
Review this data model for correctness and scalability.

Schema:
[paste all CREATE TABLE statements or ORM models]

Application context:
[describe what the application does]

Review:
1. **Normalization**: Over-normalized (too many joins needed)? Under-normalized (data redundancy/inconsistency risk)?
2. **Relationships**: Are foreign keys correct? Missing any? Cascade rules make sense?
3. **Data types**: Right types for each column? (VARCHAR(255) for everything?)
4. **Constraints**: NOT NULL where needed? UNIQUE where needed? CHECK constraints?
5. **Naming**: Consistent naming convention? (plural/singular, snake_case/camelCase)
6. **Scaling concerns**: Any table that will become a bottleneck? Hot spots?
7. **Audit fields**: created_at, updated_at, soft delete (deleted_at)?
8. **Enums vs lookup tables**: Which is better for each case?
9. **JSON columns**: Appropriate use or schema avoidance?

Rate: Solid / Needs Work / Redesign Required
Provide specific fixes for each issue found.
```

---

## Prompt #69 — Bulk Data Operation Optimizer

```
I need to process/import/update a large amount of data efficiently.

Operation:
[describe — e.g., "import 5M rows from CSV", "update status for 2M records", "delete old data"]

Current approach:
[paste code — probably a loop doing one-by-one operations]

Data volume: [number of records]
Time constraint: [e.g., "must complete within 1 hour", "can run overnight"]
Acceptable downtime: [none / some / full maintenance window]

Optimize with:
1. Batch processing (COPY, bulk insert, executemany)
2. Cursor-based iteration (don't load all into memory)
3. Transaction strategy (commit every N rows, not per row or after all)
4. Disable/rebuild indexes during bulk operation
5. Parallel processing (if safe for this operation)
6. Progress reporting (log every N rows processed)
7. Error handling (skip bad rows? Fail entire batch? Dead-letter queue?)

Show the optimized code with estimated completion time.
Database: [PostgreSQL / MySQL / etc.]
Language: [Python / Node / Java / etc.]
```

---

## Prompt #70 — Query to ORM Translation (and vice versa)

```
Convert between raw SQL and ORM code.

Direction: [SQL → ORM] or [ORM → SQL]

Input:
[paste the query or ORM code]

ORM: [SQLAlchemy / Django ORM / Prisma / TypeORM / Sequelize / ActiveRecord / etc.]

Requirements:
1. Exact equivalent (same result, same performance characteristics)
2. Use ORM best practices (not just raw SQL wrapped in ORM)
3. Include eager loading / joins as ORM relations, not manual joins
4. Handle aggregations and subqueries properly
5. Show the SQL that the ORM will generate (so I can verify equivalence)

If the ORM can't express this query efficiently, say so and recommend using raw SQL for this specific case.
```

---

## Prompt #71 — Database Connection Pool Tuning

```
Help me configure database connection pooling.

Application:
- Framework: [e.g., FastAPI, Spring Boot, Express]
- Connection library: [e.g., psycopg2, HikariCP, pg]
- Deployment: [e.g., 3 pods with 4 workers each]

Database:
- Engine: [PostgreSQL / MySQL / etc.]
- Max connections: [e.g., default 100 for PostgreSQL]
- Current connection errors: [paste any "too many connections" or timeout errors]

Traffic:
- Peak concurrent requests: [number]
- Average query duration: [e.g., 5ms]
- Long-running queries: [any? Duration?]

Calculate:
1. Optimal pool size per worker (with formula: connections = (cores * 2) + effective_spindle_count)
2. Total connections across all workers (workers × pool_size < max_connections)
3. Connection timeout settings
4. Idle connection timeout
5. Connection lifetime / recycling
6. Overflow strategy (queue requests? Return error?)

Provide: Configuration code/settings with comments explaining each value.
```

---

## Prompt #72 — Data Archival Strategy

```
Design a data archival strategy for this table.

Table: [name]
Current size: [rows, storage size]
Growth rate: [rows/day or rows/month]
Retention requirement: [e.g., "last 90 days active, 7 years archived"]

Query patterns on recent data:
[list queries and frequency]

Query patterns on archived data:
[list — probably rare, reporting only]

Design:
1. **Partition strategy** (range partitioning by date? Hash?)
2. **Archive destination** (separate table? Cold storage? Object storage like S3?)
3. **Archive process** (cron job? Event-driven? How often?)
4. **Archive format** (Parquet for analytics? CSV for compliance? Keep in DB?)
5. **Access to archives** (how to query archived data when needed)
6. **Deletion policy** (when to permanently delete, if ever)
7. **Migration script** (how to implement this on the existing table without downtime)

Show: partitioning DDL, archive job code, and restoration procedure.
```
