---
name: system-design
description: >-
  Guide architectural design decisions for software systems. Use this skill
  when designing new systems, evaluating architecture trade-offs, or creating
  technical design documents. Helps produce clear, well-structured design
  artifacts including component diagrams, data flow, and decision records.
---

# System Design

Guide architectural decisions and produce structured design artifacts.

## When to Use

- Designing a new system or major feature from scratch
- Evaluating trade-offs between architectural approaches
- Creating Architecture Decision Records (ADRs)
- Reviewing existing architecture for scalability, reliability, or maintainability concerns
- Decomposing a monolith or planning a migration

## Workflow

### Step 1: Clarify Requirements

Before designing, gather:

1. **Functional requirements** - What must the system do?
2. **Non-functional requirements** - Performance, availability, security, cost constraints
3. **Scope boundaries** - What is explicitly out of scope?
4. **Existing constraints** - Current tech stack, team skills, timeline

Ask the user to clarify any ambiguous requirements before proceeding.

### Step 2: Identify Components

Break the system into components:

- **Data stores** - What data exists? How is it accessed?
- **Services / modules** - What are the logical units of work?
- **Interfaces** - How do components communicate? (API, events, shared DB, files)
- **External dependencies** - Third-party services, APIs, infrastructure

### Step 3: Evaluate Alternatives

For each significant decision, document at least 2 options:

| Criterion | Option A | Option B |
|-----------|----------|----------|
| Complexity | ... | ... |
| Scalability | ... | ... |
| Operational cost | ... | ... |
| Team familiarity | ... | ... |

Recommend one option with clear reasoning.

### Step 4: Produce Design Artifact

Output a structured design document:

```markdown
# Design: <Title>

## Context
[Problem statement and motivation]

## Requirements
- Functional: ...
- Non-functional: ...

## Architecture
[Component diagram or description]

## Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| ... | ... | ... |

## Data Model
[Schema or entity relationships]

## API Surface
[Key endpoints or interfaces]

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| ... | ... | ... |

## Open Questions
- ...
```

### Step 5: Review Checklist

Before finalizing, verify:

- [ ] Single responsibility per component
- [ ] No circular dependencies between modules
- [ ] Failure modes identified and handled
- [ ] Data consistency model is explicit (strong vs eventual)
- [ ] Security boundaries are defined
- [ ] Observability points (logging, metrics, tracing) are planned

## Principles

1. **Start simple** - Add complexity only when requirements demand it
2. **Make trade-offs explicit** - Every choice has a cost; document it
3. **Design for change** - Interfaces should be stable; implementations should be replaceable
4. **Separate concerns** - Data, logic, and presentation should not be entangled
5. **Fail gracefully** - Design for partial failures, not just the happy path
