---
name: c3-provision
description: |
  Documents architecture WITHOUT implementation. Creates ADR and component docs with status: provisioned.

  MUST use this skill when user wants to DESIGN or PLAN without implementing:
  - "provision X", "provision a component", "provision new service"
  - "design the architecture for X", "design a component"
  - "plan X", "plan a new service", "plan the architecture"
  - "document X architecture", "architect X"
  - "envision X", "sketch X architecture"

  DO NOT use this skill if prompt contains:
  - "pattern", "patterns" → route to c3-ref
  - "ref", "refs" → route to c3-ref
  - "convention", "standard" → route to c3-ref

  Key indicator: User wants documentation/design output, NOT code changes.
  Requires .c3/ to exist. Creates ADR with status: provisioned.
  For implementation requests, route to c3-alter.
---

# C3 Provision - Architecture Without Implementation

**Document architecture before code exists.** ADR captures design decision, component docs created with status: provisioned.

**Relationship to c3-orchestrator agent:** This skill uses orchestrator analysis stages but stops after ADR acceptance. No c3-dev execution.

## REQUIRED: Load References

Before proceeding, use Glob to find and Read these files:
1. `**/references/skill-harness.md` - Red flags and complexity rules
2. `**/references/layer-navigation.md` - How to traverse C3 docs
3. `**/references/adr-template.md` - ADR structure
4. `**/references/component-lifecycle.md` - Provisioned status model

## Core Workflow

```
User Request ("provision X", "design X", "plan X")
    ↓
Stage 1: Intent Clarification (Socratic)
    ↓
Stage 2: Current State (analyze existing architecture)
    ↓
Stage 3: Scope Impact (what containers/components affected)
    ↓
Stage 4: Create ADR (status: proposed)
    ↓
Stage 4b: User Accepts ADR
    ↓
Stage 5: Create Provisioned Docs
    ├── New component: .c3/provisioned/c3-X/c3-xxx.md
    └── Update to existing: .c3/provisioned/c3-X/c3-xxx.md (with supersedes:)
    ↓
Stage 6: Update ADR status: provisioned
    ↓
DONE (no execution phase)
```

## Progress Checklist

Copy and track as you work:

```
Provision Progress:
- [ ] Stage 1: Intent clarified (what to provision, why)
- [ ] Stage 2: Current state documented
- [ ] Stage 3: Scope assessed (affected containers/components)
- [ ] Stage 4: ADR created (status: proposed)
- [ ] Stage 4b: ADR accepted by user
- [ ] Stage 5: Provisioned docs created
- [ ] Stage 6: ADR status updated to provisioned
```

---

## Stage 1: Intent

| Step | Action |
|------|--------|
| Analyze | What component/feature? New or update? Why provision vs implement? |
| Ask | Use AskUserQuestion: What problem does this solve? Scope? |
| Synthesize | `Intent: Provision [component] Goal: [outcome] Type: [new/update]` |
| Review | User confirms or corrects |

**Key question:** "Are you looking to document the design now and implement later, or do you want to implement immediately?"

---

## Stage 2: Current State

| Step | Action |
|------|--------|
| Analyze | Read affected C3 docs via layer navigation |
| Ask | Any existing components this relates to? |
| Synthesize | List related components, their behavior, dependencies |
| Review | User confirms or corrects |

---

## Stage 3: Scope Impact

| Step | Action |
|------|--------|
| Analyze | Which containers affected? New or update? |
| Ask | Clarify boundaries, dependencies |
| Synthesize | List all affected c3 IDs |
| Review | User confirms scope |

---

## Stage 4: Create ADR

Generate at `.c3/adr/adr-YYYYMMDD-{slug}.md`.

**Provisioning ADR template:**

```yaml
---
id: adr-YYYYMMDD-{slug}
title: [Design Decision Title]
status: proposed
date: YYYY-MM-DD
affects: [c3 IDs]
approved-files: []
base-commit:
implements:
superseded-by:
---
```

**Key sections:**
- Problem (why this design is needed)
- Decision (what we're provisioning)
- Rationale (design tradeoffs)
- Affected Layers (what docs will be created)

**Note:** `approved-files` stays empty for provisioning (no code changes).

---

## Stage 4b: ADR Acceptance

Use AskUserQuestion:

```
question: "Review the ADR. Ready to accept and create provisioned docs?"
options:
  - "Accept - create provisioned component docs"
  - "Revise - update scope or decision"
  - "Cancel - abandon this provisioning"
```

**On Accept:**
1. Update ADR status: `proposed` → `accepted`
2. Proceed immediately to Stage 5

---

## Stage 5: Create Provisioned Docs

**PREREQUISITE:** ADR must be in `status: accepted` before creating docs.

### For NEW component:

Create directory structure first:
```bash
mkdir -p .c3/provisioned/c3-X-container
```

Create at `.c3/provisioned/c3-X-container/c3-XXX-name.md`:

```yaml
---
id: c3-XXX-name
status: provisioned
adr: adr-YYYYMMDD-{slug}
---

# [Component Name] (Provisioned)

## Purpose

[What this component will do]

## Behavior

[Expected behavior when implemented]

## Dependencies

- Uses: [c3 IDs of components this will use]
- Used by: [c3 IDs of components that will use this]

## Notes

This component is provisioned (designed) but not yet implemented.
Implementation will be tracked via a separate ADR.
```

**IMPORTANT:** Do NOT include `## Code References` section - provisioned components have no code.

### For UPDATE to existing component:

Create at `.c3/provisioned/c3-X-container/c3-XXX-name.md`:

```yaml
---
id: c3-XXX-name
status: provisioned
supersedes: ../../c3-X-container/c3-XXX-name.md
adr: adr-YYYYMMDD-{slug}
---

# [Component Name] (Provisioned Update)

[Full component doc as it will be after implementation]
```

### Update container README (optional)

If creating new component, add to container's README under "Provisioned" section:

```markdown
## Provisioned Components

Components designed but not yet implemented:

| ID | Name | ADR |
|----|------|-----|
| c3-XXX | Name | adr-YYYYMMDD-slug |
```

---

## Stage 6: Finalize ADR

Update ADR frontmatter:

```yaml
status: provisioned    # Changed from accepted
```

Add to end of ADR:

```markdown
## Provisioned

Component docs created:
- `.c3/provisioned/c3-X/c3-XXX.md`

To implement this design, create a new ADR with `implements: adr-YYYYMMDD-{slug}`.
```

---

## Examples

**Example 1: Provision new component**

```
User: "provision a rate limiter for the API"

Stage 1 - Intent:
  Intent: Provision rate limiter
  Goal: Document rate limiting design before implementing
  Type: New component

Stage 2 - Current State:
  Related: c3-2-api (API Backend)
  No existing rate limiting

Stage 3 - Scope:
  New: c3-206-rate-limiter in c3-2-api
  Integrates with: c3-201-auth-middleware

Stage 4 - ADR:
  Created: .c3/adr/adr-20260129-rate-limiter.md
  Status: proposed

Stage 4b - Accept:
  User accepts → ADR status: accepted

Stage 5 - Create Docs:
  Created: .c3/provisioned/c3-2-api/c3-206-rate-limiter.md
  Component status: provisioned

Stage 6 - Finalize:
  ADR status: accepted → provisioned
```

**Example 2: Provision update to existing**

```
User: "design OAuth support for the auth middleware"

Stage 1 - Intent:
  Intent: Provision OAuth addition
  Goal: Document OAuth design before implementing
  Type: Update to existing c3-201

Stage 2 - Current State:
  Existing: c3-201-auth-middleware (basic auth only)

Stage 3 - Scope:
  Update: c3-201-auth-middleware
  No new components

Stage 4 - ADR:
  Created: .c3/adr/adr-20260129-oauth-support.md

Stage 4b - Accept:
  User accepts → ADR status: accepted

Stage 5 - Create Docs:
  Created: .c3/provisioned/c3-2-api/c3-201-auth-middleware.md
  (supersedes: ../../c3-2-api/c3-201-auth-middleware.md)

Stage 6 - Finalize:
  ADR status: accepted → provisioned
```

---

## Response Format

```
**Stage N: {Name}**
{findings}
**Open Questions:** {list or "None - confident"}
**Next:** {what happens next}
```
