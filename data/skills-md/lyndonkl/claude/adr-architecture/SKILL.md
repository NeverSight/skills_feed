---
name: adr-architecture
description: Use when documenting significant technical or architectural decisions that need context, rationale, and consequences recorded. Invoke when choosing between technology options, making infrastructure decisions, establishing standards, migrating systems, or when team needs to understand why a decision was made. Use when user mentions ADR, architecture decision, technical decision record, or decision documentation.
---

# Architecture Decision Records (ADR)

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is an ADR?](#what-is-an-adr)
- [Workflow](#workflow)
  - [1. Understand the Decision](#1--understand-the-decision)
  - [2. Choose ADR Template](#2--choose-adr-template)
  - [3. Document the Decision](#3--document-the-decision)
  - [4. Validate Quality](#4--validate-quality)
  - [5. Deliver and File](#5--deliver-and-file)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Document significant architectural and technical decisions with full context, alternatives considered, trade-offs analyzed, and consequences understood. ADRs create a decision trail that helps teams understand "why" decisions were made, even years later.

## When to Use This Skill

- Recording architecture decisions (microservices, databases, frameworks)
- Documenting infrastructure choices (cloud providers, deployment strategies)
- Capturing technology selections (libraries, tools, platforms)
- Logging process decisions (branching strategy, deployment process)
- Establishing technical standards or conventions
- Migrating or sunsetting systems
- Making security or compliance choices
- Resolving technical debates with documented rationale
- Onboarding new team members who need decision history

**Trigger phrases:** "ADR", "architecture decision", "document this decision", "why did we choose", "decision record", "technical decision log"

## What is an ADR?

An Architecture Decision Record is a document capturing a single significant decision. It includes:

- **Context**: What situation necessitates this decision?
- **Decision**: What are we choosing to do?
- **Alternatives**: What other options did we consider?
- **Consequences**: What are the trade-offs and implications?
- **Status**: Proposed, accepted, deprecated, superseded?

**Quick Example:**

```markdown
# ADR-042: Use PostgreSQL for Primary Database

**Status:** Accepted
**Date:** 2024-01-15
**Deciders:** Backend team, CTO

## Context
Need to select primary database for new microservices platform.
Requirements: ACID transactions, complex queries, 10k+ QPS at launch.

## Decision
Use PostgreSQL 15+ as primary relational database.

## Alternatives Considered
- MySQL: Weaker JSON support, less robust constraint handling
- MongoDB: No ACID across documents, eventual consistency issues
- CockroachDB: Excellent but adds operational complexity we can't support yet

## Consequences
✓ Strong consistency and data integrity
✓ Excellent JSON support for semi-structured data
✓ Team has deep PostgreSQL experience
✗ Vertical scaling limits (will need read replicas at 50k+ QPS)
✗ More complex to shard than DynamoDB if we need it
```

## Workflow

Copy this checklist and track your progress:

```
ADR Progress:
- [ ] Step 1: Understand the decision
- [ ] Step 2: Choose ADR template
- [ ] Step 3: Document the decision
- [ ] Step 4: Validate quality
- [ ] Step 5: Deliver and file
```

**Step 1: Understand the decision**

Gather decision context: what decision needs to be made, why now, who decides, constraints (budget, timeline, skills, compliance), requirements (functional, non-functional, business), and scope (one service vs organization-wide). This ensures the ADR addresses the right problem.

**Step 2: Choose ADR template**

For technology selection (frameworks, libraries, databases) → Use `resources/template.md`. For complex architectural decisions with multiple interdependent choices → Study `resources/methodology.md`. To see examples → Review `resources/examples/` (database-selection.md, microservices-migration.md, api-versioning.md).

**Step 3: Document the decision**

Create `adr-{number}-{short-title}.md` with: clear title, metadata (status, date, deciders), context (situation and requirements), decision (specific and actionable), alternatives considered (with pros/cons), consequences (trade-offs, risks, benefits), implementation notes if relevant, and links to related ADRs. See [Common Patterns](#common-patterns) for decision-type specific guidance.

**Step 4: Validate quality**

Self-check using `resources/evaluators/rubric_adr_architecture.json`. Verify: context explains WHY, decision is specific and actionable, 2-3+ alternatives documented with trade-offs, consequences include benefits AND drawbacks, technical details accurate, understandable to unfamiliar readers, honest about downsides. Minimum standard: Score ≥ 3.5 (aim for 4.5+ if controversial/high-impact).

**Step 5: Deliver and file**

Present the completed ADR file, highlight key trade-offs identified, suggest ADR numbering if not provided, recommend review process for high-stakes decisions, and note any follow-up decisions needed. Filing convention: Store ADRs in `docs/adr/` or `architecture/decisions/` directory with sequential numbering.

## Common Patterns

**For technology selection:**
- Focus on technical capabilities vs requirements
- Include performance benchmarks if available
- Document team expertise level
- Consider operational complexity

**For architectural changes:**
- Include migration strategy in consequences
- Document backward compatibility impact
- Consider team velocity impact during transition
- Note monitoring and rollback plans

**For standards and conventions:**
- Include examples of the standard in practice
- Document exceptions or escape hatches
- Consider enforcement mechanisms
- Note educational/onboarding implications

**For deprecations:**
- Set status to "Deprecated" or "Superseded"
- Link to superseding ADR
- Document sunset timeline
- Include migration guide

## Guardrails

**Do:**
- Be honest about trade-offs (every choice has downsides)
- Write for future readers who lack current context
- Include specific technical details (versions, configurations)
- Acknowledge uncertainty and risks
- Keep ADRs immutable (status changes, but content doesn't)
- Write one ADR per decision (focused scope)

**Don't:**
- Make decisions sound better than they are
- Omit alternatives that were seriously considered
- Use jargon without explanation
- Write vague consequences ("might improve performance")
- Revisit/edit old ADRs (write new superseding ADR instead)
- Combine multiple independent decisions in one ADR

## Quick Reference

- **Standard template**: `resources/template.md`
- **Complex decisions**: `resources/methodology.md`
- **Examples**: `resources/examples/database-selection.md`, `resources/examples/microservices-migration.md`, `resources/examples/api-versioning.md`
- **Quality rubric**: `resources/evaluators/rubric_adr_architecture.json`

**ADR Naming Convention**: `adr-{number}-{short-kebab-case-title}.md`
- Example: `adr-042-use-postgresql-for-primary-database.md`
