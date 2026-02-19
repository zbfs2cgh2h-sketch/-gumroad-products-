# Quick Reference Card — Top 20 AI Coding Prompts

*Copy. Paste. Ship.*

---

## ⚡ CODE REVIEW & SECURITY
**1.1 Security Scan** → "Review [code] for OWASP Top 10 vulnerabilities. List each with severity + fix."
**1.3 Logic Audit** → "Find edge cases and off-by-one errors in [code]. Show the failure scenario."

## 🐛 DEBUGGING
**2.1 Error Explainer** → "Explain this error: [paste error]. Root cause + fix + how to prevent it."
**2.4 Rubber Duck** → "I expect [X] but get [Y]. Walk me through what actually happens line by line."

## ✅ TESTING
**3.1 Unit Test Gen** → "Write pytest tests for [function]. Cover: happy path, edge cases, error cases."
**3.5 Mock Builder** → "Create mocks for [dependency] that simulate success, timeout, and 4xx/5xx responses."

## 📝 DOCUMENTATION
**4.1 README Writer** → "Write a README for [project]. Include: what it does, install, usage, examples, license."
**4.3 Inline Comments** → "Add inline comments to [code]. Explain WHY, not what. Skip obvious lines."

## 🔧 REFACTORING
**5.1 Simplify** → "Refactor [code] to reduce complexity. Keep behavior identical. Show before/after."
**5.3 Extract Function** → "Extract reusable functions from [code]. Name them by what they do, not how."

## 🏗️ ARCHITECTURE
**6.1 Design Review** → "Review this architecture: [diagram/description]. List risks, bottlenecks, missing pieces."
**6.4 Trade-off Analysis** → "Compare [option A] vs [option B] for [use case]. Table format: pros/cons/when-to-use."

## 🗄️ DATABASE
**7.1 Query Optimizer** → "Optimize this SQL: [query]. Explain the issue + add index recommendations."
**7.3 Schema Review** → "Review this schema: [schema]. Find normalization issues, missing indexes, type mismatches."

## 🔌 API
**8.1 REST Design** → "Design REST endpoints for [resource]. Include: URL, method, request/response, status codes."
**8.5 Error Handler** → "Add consistent error handling to [API code]. Use RFC 7807 problem+json format."

## 🚀 DEVOPS
**9.1 GitHub Actions** → "Write a GitHub Actions workflow for [task]: lint → test → build → deploy to [target]."
**9.3 Dockerfile** → "Write a production Dockerfile for [app]. Multi-stage, non-root user, minimal image."

## 💬 CAREER
**10.1 PR Description** → "Write a PR description for [changes]. Include: summary, technical changes, testing steps."
**10.5 Postmortem** → "Write a blameless postmortem for [incident]. Timeline + root cause + action items."

---

*Full prompts: see prompts/01-10 folders*
*Built by Jackson Studio — [jacksonlee71.gumroad.com](https://jacksonlee71.gumroad.com)*
