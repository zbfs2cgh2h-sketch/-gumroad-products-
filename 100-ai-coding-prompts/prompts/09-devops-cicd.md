# Category 9: DevOps & CI/CD Automation (10 Prompts)

---

## Prompt #83 — GitHub Actions Workflow from Scratch

```
Write a GitHub Actions CI/CD pipeline for this project.

Project:
- Language: [e.g., Python 3.12, Node 20, Go 1.22]
- Package manager: [pip, npm, pnpm, yarn, go modules]
- Test command: [e.g., pytest, npm test, go test ./...]
- Build command: [e.g., docker build, npm run build]
- Deploy target: [e.g., AWS ECS, Vercel, GCP Cloud Run, bare EC2]

Pipeline stages:
1. **Lint** (run linter/formatter check — fail if code isn't formatted)
2. **Test** (run all tests, upload coverage report)
3. **Build** (compile/bundle/build Docker image)
4. **Security scan** (dependency audit, container scan)
5. **Deploy to staging** (on push to main)
6. **Deploy to production** (on tag/release, with manual approval)

Requirements:
- Cache dependencies between runs
- Run lint + test in parallel
- Use matrix strategy for multiple versions if applicable
- Secrets stored in GitHub, not hardcoded
- Status checks required before merge

Output: Complete .github/workflows/ YAML file(s) with comments.
```

---

## Prompt #84 — Dockerfile Optimizer

```
Optimize this Dockerfile for production.

Current Dockerfile:
[paste Dockerfile]

Application: [what it runs]
Current image size: [if known, or "check it"]

Optimize for:
1. **Image size** (multi-stage build, minimal base image, .dockerignore)
2. **Build speed** (layer caching — put least-changing layers first)
3. **Security** (non-root user, no unnecessary tools, minimal attack surface)
4. **Reproducibility** (pinned versions for base image and packages)
5. **Health check** (HEALTHCHECK instruction)
6. **Labels** (OCI labels: version, maintainer, description)

Show:
- Optimized Dockerfile with comments on each change
- .dockerignore file
- Expected size reduction
- Build time comparison tip
```

---

## Prompt #85 — Docker Compose for Local Development

```
Create a docker-compose.yml for local development of this application.

Application stack:
[describe services — e.g., "Python API + React frontend + PostgreSQL + Redis + RabbitMQ"]

Requirements:
1. **Hot reload** for application code (volume mounts, not rebuild)
2. **Database** with persistent volume (data survives restart)
3. **Database seed** (run migrations and seed data on first start)
4. **Network** (services can talk to each other by name)
5. **Environment variables** (.env file, not hardcoded in compose)
6. **Health checks** (dependent services wait for DB to be ready)
7. **Ports** (map to non-conflicting local ports)
8. **One command start** (docker compose up works without prior setup)

Also provide:
- .env.example file
- Makefile with common commands (start, stop, logs, reset-db, shell-into-service)
- Troubleshooting section (common issues and fixes)
```

---

## Prompt #86 — Kubernetes Deployment Manifest

```
Write Kubernetes manifests for deploying this application.

Application:
- Image: [e.g., myapp:latest]
- Port: [e.g., 8080]
- Replicas: [e.g., 3]
- Resource needs: [e.g., 256Mi memory, 200m CPU per pod]
- Environment: [list env vars needed]
- Secrets: [list secrets needed]
- Dependencies: [what external services it connects to]

Create manifests for:
1. **Deployment** (rolling update strategy, resource limits + requests, liveness + readiness probes)
2. **Service** (ClusterIP for internal, LoadBalancer or Ingress for external)
3. **Ingress** (with TLS — cert-manager annotations)
4. **ConfigMap** (non-sensitive configuration)
5. **Secret** (sensitive values — show structure, not actual values)
6. **HPA** (Horizontal Pod Autoscaler — scale on CPU/memory/custom metrics)
7. **PDB** (Pod Disruption Budget — don't kill all pods during rolling update)
8. **NetworkPolicy** (restrict traffic to what's necessary)

Include: kustomization.yaml for environment-specific overlays (dev/staging/prod).
```

---

## Prompt #87 — Infrastructure as Code (Terraform)

```
Write Terraform configuration for this infrastructure.

What I need:
[describe infrastructure — e.g., "VPC + ECS Fargate service + RDS PostgreSQL + ElastiCache Redis + ALB"]

Cloud provider: [AWS / GCP / Azure]
Region: [e.g., us-east-1]
Environment: [dev / staging / production]

Requirements:
1. **Modules** (reusable, not one giant main.tf)
2. **Variables** (configurable for different environments)
3. **Outputs** (export important values: URLs, connection strings, ARNs)
4. **Security** (security groups, IAM roles with least privilege)
5. **State** (remote state in S3/GCS with locking)
6. **Tags** (consistent tagging for cost tracking)
7. **Cost estimate** (approximate monthly cost)

Show:
- File structure (modules/, environments/)
- Main configuration
- Variable definitions with descriptions
- Example tfvars for production
- README with `terraform apply` instructions
```

---

## Prompt #88 — Deployment Rollback Procedure

```
Write a deployment rollback procedure for this system.

Deployment method: [e.g., GitHub Actions → Docker image → ECS, Helm → k8s, Vercel, raw SSH]
Current deployment steps: [describe or paste the deploy script]

Rollback procedure should cover:
1. **Detection** (how to know a deploy went bad — error rate spike, health check failure, user reports)
2. **Decision** (when to rollback vs when to fix-forward — provide a decision tree)
3. **Application rollback** (revert to previous version — exact commands)
4. **Database rollback** (if migrations ran, can they be reversed? How?)
5. **Cache invalidation** (if cached data is now stale)
6. **Feature flag disable** (if the bad code is behind a flag)
7. **Communication** (template for status page update, team notification)
8. **Verification** (how to confirm the rollback worked)
9. **Post-mortem** (template for documenting what happened)

Make this a checklist someone can follow during an incident without thinking too hard.
```

---

## Prompt #89 — CI Pipeline Debugger

```
My CI pipeline is failing or slow. Help me fix it.

CI system: [GitHub Actions / GitLab CI / Jenkins / CircleCI]
Pipeline config:
[paste YAML/Jenkinsfile]

Problem:
[describe — e.g., "build takes 25 minutes", "tests pass locally but fail in CI", "flaky tests"]

Error output:
[paste relevant CI logs]

Diagnose:
1. **If failing**: Read the error, trace it to root cause, provide fix
2. **If slow**: Find the bottleneck (no caching? Sequential steps that could parallel? Large images?)
3. **If flaky**: Identify non-deterministic tests (time-dependent, order-dependent, network-dependent)

Optimizations to check:
- Dependency caching configured properly?
- Docker layer caching?
- Parallel test execution?
- Unnecessary steps running on every push?
- Base image pulls cached?
- Test database setup optimized?

Provide the fixed pipeline config.
```

---

## Prompt #90 — Monitoring Alert Rules

```
Write monitoring alert rules for this service.

Service: [name, what it does]
Metrics available: [Prometheus / Datadog / CloudWatch metrics — list them]
Current monitoring: [none / basic / describe]

Create alerts for:

**Critical (page someone at 3am):**
1. Service down (health check failing for >2 minutes)
2. Error rate >5% for >3 minutes
3. Database connection pool exhausted
4. Disk >90% full
5. SSL certificate expiring in <7 days

**Warning (investigate during business hours):**
1. Response time p99 >1s for >10 minutes
2. Error rate >1% for >5 minutes
3. Memory usage >80%
4. Queue depth growing (consumers can't keep up)
5. External dependency latency increase

For each alert:
- Alert name and description
- Query/expression (PromQL, Datadog query, etc.)
- Threshold and duration
- Severity (critical/warning)
- Runbook link (what to check first)
- Who gets notified (channel/PagerDuty service)

Anti-patterns to avoid:
- Alerting on symptoms only (alert on cause too)
- Alert storms (group related alerts)
- Flappy alerts (proper thresholds + hysteresis)
```

---

## Prompt #91 — Log Aggregation Setup

```
Set up centralized log aggregation for this system.

System: [describe — e.g., "3 microservices on ECS, 1 cron job on Lambda, PostgreSQL on RDS"]
Current logging: [describe — e.g., "each service logs to stdout, we SSH in to read logs"]
Log volume: [estimate — e.g., "~10GB/day"]

Tool preference: [ELK / Loki+Grafana / CloudWatch / Datadog / etc.]

Set up:
1. **Structured logging** in each service (JSON format, consistent fields)
   - Required fields: timestamp, level, service, request_id, message
   - Show logging library config for [language]
2. **Log shipping** (how logs get from services to the aggregator)
3. **Index/label strategy** (by service, environment, log level)
4. **Retention** (how long to keep logs at each tier)
5. **Search** (common queries: all logs for a request ID, all errors in last hour)
6. **Dashboard** (error rate by service, log volume, recent errors)
7. **Alerts** (alert when error rate spikes in logs)
8. **Cost management** (log sampling, filtering out noisy debug logs)

Show: logging library config, shipping config, and 5 most useful log queries.
```

---

## Prompt #92 — Secrets Management Setup

```
Set up secrets management for this application.

Current state: [describe — e.g., "secrets in .env files committed to git", "hardcoded in code", "in CI environment variables"]
Environment: [local / Docker / Kubernetes / cloud — specify]

Secrets to manage:
[list — e.g., "database password, API keys for 3 services, JWT signing key, TLS certificate"]

Set up:
1. **Local development** (how developers get secrets — .env file from vault? 1Password CLI?)
2. **CI/CD** (how the pipeline gets secrets — GitHub secrets? Vault? AWS Secrets Manager?)
3. **Production** (how the running app gets secrets — env vars, mounted files, API call to vault?)
4. **Rotation** (how to rotate a secret without downtime)
5. **Access control** (who/what can read which secrets)
6. **Audit** (log every secret access)
7. **Emergency** (process for revoking a leaked secret)

Tool recommendation: [AWS Secrets Manager / HashiCorp Vault / Doppler / 1Password — with pros/cons for our setup]

Show: configuration, code to read secrets, and rotation procedure.
```
