---
name: c3-ref
description: |
  Manage cross-cutting patterns and conventions as first-class architecture artifacts.
  Use when: "add a pattern", "document this convention", "create a ref", "update ref-X",
  "evolve this pattern", "what patterns exist", "which components use ref-X".
  Requires .c3/ to exist. Refs are authoritative constraints - violations require explicit override.
---

# C3 Ref - Pattern Management

Cross-cutting patterns (refs) are **authoritative constraints**. They define how things should be done system-wide. This skill makes refs first-class citizens with proper workflows.

## CRITICAL: Component Categorization

Load `**/references/component-categories.md` for the full Foundation vs Feature vs Ref rules.

**Key rule for refs:** Refs have NO `## Code References` section. If it needs one, it's a component.

## REQUIRED: Load References

Before proceeding, use Glob to find and Read these files:
1. `**/references/skill-harness.md` - Red flags and complexity rules
2. `**/templates/ref.md` - Ref template structure

## Mode Selection

| User Intent | Mode |
|-------------|------|
| "add/create/document a pattern" | **Add** |
| "update/modify/evolve ref-X" | **Update** |
| "list patterns", "what refs exist" | **List** |
| "who uses ref-X", "where is ref-X cited" | **Usage** |

---

## Mode: Add

Create a new ref from discovered or proposed pattern.

### Flow

```
Describe Pattern → Discover Usage → Generate Ref → Update Citings → Create ADR
```

### Steps

**Step 1: Clarify Pattern**

Use `AskUserQuestion` to understand:

```
AskUserQuestion:
  question: "What pattern do you want to document?"
  options:
    - "Error handling convention"
    - "Data fetching pattern"
    - "Authentication approach"
    - "Something else (describe)"
```

Get:
- Pattern name (slug: `ref-{slug}`)
- Pattern goal (what it standardizes)
- Key rules (what must be followed)

**Step 2: Discover Existing Usage**

Search codebase for pattern indicators:

```bash
# Example for error handling
rg "extends.*Error|throw new|catch\s*\(" --type ts

# Example for retry pattern
rg "retry|backoff|exponential" --type ts
```

Identify:
- Files/components already using this pattern
- Variations in how it's implemented
- Common vs divergent approaches

**Step 3: Generate Ref**

Create `.c3/refs/ref-{slug}.md` from template:

```markdown
---
id: ref-{slug}
title: {Pattern Title}
goal: {What this pattern standardizes}
---

# {Pattern Title}

## Goal

{Why this pattern exists - what inconsistency it prevents}

## Pattern

{Core rules that MUST be followed}

### Required Elements

- {Element 1}
- {Element 2}

### Examples

**Correct:**
\`\`\`typescript
{good example}
\`\`\`

**Incorrect:**
\`\`\`typescript
{bad example}
\`\`\`

## Cited By

<!-- Updated automatically when components cite this ref -->
- c3-{N}{NN} ({component name})
```

**Step 4: Update Citing Components**

For each component that uses this pattern:

1. Read component doc
2. Add ref to `## Related Refs` table
3. Remove any duplicated pattern content (cite instead)

**Step 5: Create Adoption ADR**

Create mini-ADR at `.c3/adr/adr-YYYYMMDD-ref-{slug}-adoption.md`:

```markdown
---
id: adr-YYYYMMDD-ref-{slug}-adoption
title: Adopt {Pattern Title} as standard
status: implemented
---

# Adopt {Pattern Title} as Standard

## Problem

{Pattern was implemented inconsistently across N components}

## Decision

Document pattern as ref-{slug}. All existing usages now cite this ref.

## Affected Layers

| Layer | Change |
|-------|--------|
| refs | Added ref-{slug} |
| components | {list of updated components} |
```

---

## Mode: Update

Modify an existing ref with impact analysis.

### Flow

```
Identify Change → Find Citings → Check Compliance → Surface Violations → Execute
```

### Steps

**Step 1: Clarify Change**

```
AskUserQuestion:
  question: "What change do you want to make to ref-{slug}?"
  options:
    - "Add a new rule"
    - "Modify an existing rule"
    - "Remove a rule"
    - "Clarify/improve documentation"
```

**Step 2: Find All Citings**

```bash
# Find components citing this ref
rg "ref-{slug}" .c3/c3-*/c3-*.md
```

List all citing components.

**Step 3: Check Compliance**

For each citing component:
- Read code references from component doc
- Check if code still complies with proposed change
- Categorize: compliant / needs-update / breaking

**Step 4: Surface Impact**

```
AskUserQuestion:
  question: "This change affects N components. M are already compliant, K need updates."
  options:
    - "Proceed - update ref and K components"
    - "Narrow the change - only affect compliant ones"
    - "Cancel - too much impact"
```

**Step 5: Execute**

If proceeding:

1. Update ref document
2. Create ADR for ref change
3. For non-compliant components: either update or note as TODO in ADR

```markdown
## Affected Components

| Component | Status | Action |
|-----------|--------|--------|
| c3-101 | compliant | None |
| c3-103 | needs-update | Updated code in PR #123 |
| c3-205 | breaking | TODO: refactor in follow-up |
```

**Step 6: Route to c3-alter if Code Changes Required**

If pattern change requires code modifications in components:

> "Pattern update requires code changes in {N} components. Route to /alter to create an ADR for implementation."

All code changes MUST go through c3-alter to maintain the ADR-first principle. Do not edit component code directly from c3-ref.

---

## Mode: List

Show all refs in the system.

### Flow

```bash
ls .c3/refs/ref-*.md
```

For each, read and extract:
- `id`
- `title`
- `goal`
- Count of citings

### Response Format

```
**C3 Patterns (Refs)**

| Ref | Title | Goal | Cited By |
|-----|-------|------|----------|
| ref-error-handling | Error Handling | Consistent error responses | 5 components |
| ref-auth | Authentication | Token-based auth | 3 components |
```

---

## Mode: Usage

Show where a specific ref is used.

### Flow

```bash
# Find citings
rg "ref-{slug}" .c3/c3-*/c3-*.md

# Read each citing component
```

### Response Format

```
**ref-{slug} Usage**

**Cited by:**
- c3-101 (Auth Middleware) - JWT validation
- c3-103 (User Service) - Login flow
- c3-205 (API Gateway) - Request auth

**Pattern Summary:**
{Key rules from the ref}
```

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| Create ref without discovery | Miss existing usages, incomplete citings | Always search codebase first |
| Update ref without impact check | Break existing code silently | Always check citings |
| Duplicate ref content in components | Maintenance nightmare | Cite, don't duplicate |
| Create ref for one-off pattern | Unnecessary overhead | Refs are for repeated patterns |

---

## Examples

**Example 1: Add Pattern**

```
User: "We use a retry pattern across all API calls. Document it."

Step 1: Pattern = retry with exponential backoff
Step 2: rg "retry|backoff" → found in c3-101, c3-103, c3-205
Step 3: Create .c3/refs/ref-retry-pattern.md
Step 4: Update 3 component docs with Related Refs
Step 5: Create adr-20260120-ref-retry-pattern-adoption.md

Response:
Created ref-retry-pattern. Updated 3 components:
- c3-101 (HTTP Client)
- c3-103 (External API)
- c3-205 (Webhook Handler)
```

**Example 2: Update Pattern**

```
User: "Add jitter to the retry pattern"

Step 1: Change = add jitter requirement
Step 2: Citings: c3-101, c3-103, c3-205
Step 3: Check code:
  - c3-101: already uses jitter ✓
  - c3-103: no jitter, needs update
  - c3-205: no jitter, needs update
Step 4: "2 components need updates. Proceed?"
Step 5: User: "Yes"
  - Update ref-retry-pattern.md
  - Create ADR with TODO for c3-103, c3-205
```
