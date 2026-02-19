# Category 10: Career & Communication (8 Prompts)

---

## Prompt 10.1 — Write a Pull Request Description

```
You are a senior developer reviewing my PR. Write a PR description for:

Code changes: [paste diff or describe changes]
Ticket/issue: [link or description]
Impact: [what breaks if this is wrong]

Include:
- Summary (2-3 sentences, non-technical)
- Technical changes (bullet points)
- Testing steps (numbered)
- Screenshots section placeholder
- Breaking changes (if any)

Tone: professional, direct. Max 300 words.
```

**Best for**: GitHub, GitLab, Bitbucket PRs
**Output**: Markdown-formatted PR description

---

## Prompt 10.2 — Explain Technical Debt to a Manager

```
I need to explain this technical debt to a non-technical manager and justify fixing it now vs. later.

The problem: [describe the tech debt]
Current impact: [slow deploys / bugs / onboarding friction]
If we fix it: [time savings, risk reduction]
If we don't: [compounding cost, risk]

Write a 3-paragraph explanation that:
1. Explains the problem without jargon
2. Frames it as business risk (not developer preference)
3. Proposes a fix timeline with estimated effort

Audience: product manager or CTO who cares about delivery speed.
```

**Best for**: Quarterly planning, tech debt prioritization
**Output**: Business-friendly justification

---

## Prompt 10.3 — Write a Tech Spec / RFC

```
Write a technical specification (RFC) for:

Feature: [feature name]
Problem it solves: [1-2 sentences]
Proposed solution: [high-level approach]
Constraints: [performance / security / timeline]
Affected systems: [services / databases / APIs]

Structure:
1. Summary
2. Motivation
3. Proposed Design (with diagrams placeholder)
4. Alternatives Considered
5. Risks & Mitigations
6. Implementation Plan (phases)
7. Open Questions

Keep it under 1000 words. Use headers and bullet points.
```

**Best for**: Architecture decisions, new features
**Output**: Markdown RFC ready for team review

---

## Prompt 10.4 — Prepare for a Code Review

```
I'm about to review this code. Help me prepare meaningful feedback:

Code: [paste code]
Context: [what it's supposed to do]
Author level: [junior / mid / senior]

For each issue found, give me:
- Line reference
- Issue category (logic / performance / security / style / readability)
- Why it matters
- Suggested fix (code snippet)
- Teaching point (for junior devs)

Be direct. Skip praise. Max 10 issues. Prioritize by severity.
```

**Best for**: Code review preparation
**Output**: Actionable review comments by severity

---

## Prompt 10.5 — Write a Postmortem Report

```
Write a blameless postmortem for this incident:

What happened: [timeline of events]
Impact: [users affected, duration, revenue loss]
Root cause: [technical cause]
Contributing factors: [monitoring gaps, process issues]
What we did to fix it: [immediate actions]

Structure:
1. Incident Summary
2. Timeline (UTC timestamps)
3. Root Cause Analysis
4. Impact Assessment
5. What Went Well
6. What Went Wrong
7. Action Items (owner + due date for each)

Tone: factual, blameless, forward-looking.
```

**Best for**: Incident retrospectives, SRE teams
**Output**: Professional postmortem document

---

## Prompt 10.6 — Write a Job Ladder Promotion Case

```
I'm making the case for my promotion from [current level] to [target level].

My key contributions this year:
- [project 1 + impact]
- [project 2 + impact]
- [project 3 + impact]

Skills demonstrated: [list]
Team impact: [mentoring, process improvements]
Business impact: [metrics if available]

Write a promotion case document (1 page) that:
- Uses the engineering ladder criteria format
- Quantifies impact where possible
- Addresses scope, impact, and influence
- Sounds confident, not boastful

Company context: [startup/enterprise/mid-size]
```

**Best for**: Performance reviews, promotion cycles
**Output**: Structured promotion case

---

## Prompt 10.7 — Respond to a Negative Code Review

```
I received this code review comment and I disagree (or need help responding professionally):

Comment: "[paste the review comment]"
My code: [paste relevant code]
My reasoning: [why I wrote it this way]

Help me write a response that:
1. Acknowledges their concern
2. Explains my reasoning with evidence
3. Proposes a path forward (compromise / agree to disagree / ask for pairing)
4. Keeps the relationship intact

Tone: professional, curious, not defensive. Under 150 words.
```

**Best for**: Code review disagreements
**Output**: Professional response message

---

## Prompt 10.8 — Write a Technical Blog Post Outline

```
I want to write a technical blog post about: [topic]

Target audience: [junior devs / experienced devs / tech managers]
My angle/unique insight: [what makes my take different]
Key takeaway for reader: [one sentence]

Create an outline with:
- Attention-grabbing title (3 options)
- Hook paragraph (first 3 sentences)
- 5-7 section headers with 1-line description each
- Code example ideas for each section
- CTA at the end

Optimize for: [dev.to / Medium / personal blog]
Target length: [500 / 1000 / 2000 words]
```

**Best for**: Developer content marketing, knowledge sharing
**Output**: Ready-to-write blog outline

---

*Built by Jackson Studio — [jacksonlee71.gumroad.com](https://jacksonlee71.gumroad.com)*
