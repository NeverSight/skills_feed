---
name: prd-writing
description: >
  Write structured, opinionated PRDs that engineers actually read.
  Use when asked to write a PRD, product spec, feature requirements,
  or product requirements document. Creates concise, evidence-backed
  specs with clear scope boundaries and measurable success criteria.
---

Write PRDs that are evidence-first, concise, and scannable. A PRD is a thinking tool — if it's longer than 1200 words, the author hasn't thought hard enough. Brief specs are more likely to be read, more likely to be followed, and more likely to ship on time.

## Structure

Follow this structure. Every section is mandatory unless marked optional.

### 1. Problem
Lead with customer evidence. Quotes, data, support tickets, observed behavior. If you have no evidence, say so explicitly — that's an opinion-driven PRD and should be flagged.

Example:
> "3 of 5 interviewed customers abandon onboarding at the team invite step. Average time spent: 47 seconds before closing the tab."

NOT: "Users find onboarding confusing."

### 2. Goals
Measurable outcomes, not outputs. Each goal has a number attached.

- "Reduce onboarding drop-off from 60% to under 30%"
- NOT "Improve the onboarding experience"

### 3. Target Users
Who specifically benefits. Be narrow. "Series A startup founders doing PM work before their first PM hire" — not "product managers."

### 4. Requirements
Use P0/P1/P2 with clear definitions:
- **P0** — Does not ship without it. The feature is broken or useless without this.
- **P1** — Ships without it, but significantly degraded. Do in same cycle if possible.
- **P2** — Nice to have. Candidate for fast follow.

Each requirement is one sentence. If a requirement needs a paragraph to explain, it's too big — break it down.

### 5. Success Metrics
Numbers. Always numbers. "Reduce X from Y to Z within W weeks."

ALWAYS pair each metric with a counter-metric to prevent gaming:
- Metric: "Increase activation rate to 70%"
- Counter-metric: "Without decreasing 30-day retention below 45%"

### 6. Out of Scope
What you are deliberately NOT building and why. This section prevents scope creep and signals that you've thought about boundaries.

### 7. Open Questions (optional)
Unresolved decisions that need input. Each question names who should answer it and by when.

## Guidelines

- CRITICAL: 800-1200 words maximum. Longer PRDs mean the thinking isn't done.
- NEVER start from a solution. Start from a problem with evidence.
- NEVER include implementation details — architecture, APIs, database schemas. That's spec territory, not PRD territory.
- ALWAYS include Out of Scope. A PRD without boundaries invites scope creep.
- ALWAYS trace requirements to customer evidence. No evidence = opinion.
- NEVER use weasel metrics: "improve performance," "enhance experience," "increase engagement." Put a number on it or don't include it.
- P0 requirements should number 3-5. If you have more than 5 P0s, you haven't prioritized.

## Example: Good vs Bad

**Bad P0 requirement:**
> "The system should handle authentication in a secure and user-friendly manner, supporting multiple providers and edge cases."

**Good P0 requirement:**
> "P0: User can sign up and log in with email + password. Google OAuth is P1."

One sentence. Clear scope. Priority forces a decision.

---

*Built on Linear's "short specs > exhaustive docs" philosophy. Skills from [productskills](https://github.com/assimovt/productskills).*
