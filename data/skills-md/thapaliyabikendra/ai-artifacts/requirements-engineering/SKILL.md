---
name: requirements-engineering
description: "Transform stakeholder needs into structured, testable specifications with user stories, acceptance criteria, and business rules. Use when: (1) creating requirements documents, (2) writing user stories with acceptance criteria, (3) defining business rules and process flows, (4) analyzing feature requests."
layer: 2
tech_stack: [agnostic, markdown]
topics: [user-stories, acceptance-criteria, business-rules, process-flows, requirements]
depends_on: []
complements: [domain-modeling]
keywords: [UserStory, AcceptanceCriteria, INVEST, Gherkin, Given-When-Then, Requirement]
---

# Requirements Engineering

Transform raw requirements into structured, testable specifications that guide development teams.

## When to Use

- Creating feature requirements documents
- Writing user stories with acceptance criteria
- Defining business rules and constraints
- Documenting process flows
- Prioritizing features (MoSCoW, RICE)
- Analyzing stakeholder needs

## Requirements Document Structure

A complete requirements document includes:

1. **Feature Overview** - Business context and success metrics
2. **User Stories** - Who, what, why format
3. **Acceptance Criteria** - Given/When/Then scenarios
4. **Data Model** - Fields, types, constraints
5. **Business Rules** - BR-XXX format
6. **Permission Requirements** - Role-based access
7. **Open Questions** - Items needing clarification

## Core Templates

### User Story Format

```markdown
**US-[XXX]: [Title]**

As a [role],
I want to [action],
So that [benefit].

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [expected result]
- [ ] Given [context], when [action], then [expected result]
- [ ] Given [context], when [action], then [expected result]

**Priority**: Must Have | Should Have | Could Have | Won't Have
**Effort**: S (1-2 days) | M (3-5 days) | L (1-2 weeks) | XL (2+ weeks)
**Dependencies**: [List any dependent stories]
```

### Acceptance Criteria Patterns

**Happy Path:**
```
Given a logged-in [role]
When they [perform action] with valid [inputs]
Then [expected success outcome]
And [side effects if any]
```

**Validation Error:**
```
Given a logged-in [role]
When they [perform action] with invalid [input type]
Then the system displays "[error message]"
And [the operation is not completed]
```

**Authorization:**
```
Given a user without [permission]
When they attempt to [perform action]
Then the system returns 403 Forbidden
And [logs the unauthorized attempt]
```

**Edge Case:**
```
Given [edge condition exists]
When [action is performed]
Then [graceful handling occurs]
```

### Business Rule Format

> **Full format**: See [domain-modeling](../domain-modeling/SKILL.md#business-rule-format) skill for detailed patterns and categories.

Quick format for requirements:

| ID | Rule | Enforcement | Impact |
|----|------|-------------|--------|
| BR-{CAT}-001 | [Rule description] | [Create/Update/Delete] | [Reject with error] |

### Data Model Template

> **Full entity modeling**: See [domain-modeling](../domain-modeling/SKILL.md) skill for complete entity definitions with relationships, state transitions, and API access.

Quick format for requirements:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| Id | Guid | Yes | PK | Unique identifier |
| Name | string | Yes | Max 100 chars | Display name |
| Email | string | Yes | Valid email, Unique | Contact email |
| Status | enum | Yes | Active/Inactive | Current state |

### Process Flow Template

```markdown
## Process: [Process Name]

### Actors
| Actor | Role | Responsibility |
|-------|------|----------------|
| [Role 1] | [Title] | [What they do] |
| [Role 2] | [Title] | [What they do] |

### Flow
1. **[Actor]** initiates [action]
2. **System** validates [criteria]
3. If valid:
   a. [Success step 1]
   b. [Success step 2]
   c. [Notification/confirmation]
4. If invalid:
   a. [Error handling]
   b. [User feedback]

### Business Rules Applied
- BR-001: [Rule applied at step X]
- BR-002: [Rule applied at step Y]
```

## Prioritization Methods

### MoSCoW Method

| Priority | Meaning | Guideline |
|----------|---------|-----------|
| **Must Have** | Critical for launch | ~60% of effort |
| **Should Have** | Important but not critical | ~20% of effort |
| **Could Have** | Nice to have | ~20% of effort |
| **Won't Have** | Out of scope for this release | Document for future |

### RICE Scoring

```
RICE Score = (Reach × Impact × Confidence) / Effort

Reach: How many users affected per quarter (number)
Impact: Effect on each user (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal)
Confidence: How sure are we (100%=high, 80%=medium, 50%=low)
Effort: Person-months to complete (number)
```

## Quality Checklist

Before finalizing requirements:

- [ ] At least 3 user stories defined
- [ ] Each story has 2+ acceptance criteria
- [ ] Acceptance criteria are testable (Given/When/Then)
- [ ] Data model includes all fields with types
- [ ] Business rules are numbered and documented
- [ ] Permissions align with existing roles
- [ ] Open questions are captured
- [ ] Priority assigned to each story
- [ ] Dependencies identified

## Integration with Domain Modeling

When creating requirements, always consider domain impact:

1. **Before writing requirements**: Review existing domain in `docs/domain/`
2. **During analysis**: Identify new/modified entities, rules, permissions
3. **After requirements**: Create impact analysis using `domain-modeling` skill

The `business-analyst` agent combines requirements-engineering with domain-modeling for complete analysis.

## References

- [references/user-story-examples.md](references/user-story-examples.md) - Real-world examples
- [references/acceptance-criteria-patterns.md](references/acceptance-criteria-patterns.md) - Common patterns
