---
name: onboard
description: |
  Creates C3 architecture documentation from scratch using staged Socratic discovery.
  Use when the user asks to "adopt C3", "init C3", "initialize C3", "start C3",
  "bootstrap C3", "scaffold C3 docs", "create C3 docs", "create .c3", "set up .c3",
  "set up architecture docs", "create architecture documentation", "generate architecture docs",
  "initialize architecture", "start documenting", "document this project", "create docs for this project",
  "document the codebase", "onboard me to architecture", "document the architecture from scratch",
  "new C3 project", "first time with C3", "never used C3", "new to C3", "getting started with C3",
  or starts C3 documentation for a new project.
  Implements 3-stage workflow: Inventory → Details → Finalize.
---

# C3 Onboarding

Initialize C3 architecture documentation using a **3-stage workflow with gates**.

## CRITICAL: Separate Files, Not Monoliths

**DO NOT create a single file for all documentation.**

Each component gets its OWN file. Each container gets its OWN directory. Create:
- Separate `.md` file per component
- Separate directory per container
- Separate refs/ directory with one file per pattern

**NEVER:** Create a single c3-model.md or components.md containing everything.

## Required C3 Structure

Every onboarding MUST create this EXACT structure:

```
.c3/
├── README.md                    # System context (NOT c3-model.md!)
├── TOC.md                       # Table of contents
├── adr/
│   └── adr-00000000-c3-adoption.md
├── refs/                        # REQUIRED: Cross-cutting patterns
│   └── ref-<pattern>.md         # At least one ref file
└── c3-1-<container-name>/       # REQUIRED: Container directory
    ├── README.md                # Container overview
    └── c3-101-<component>.md    # One file per component
```

**Non-negotiable rules:**
- Each component = separate file (c3-101-auth.md, c3-102-users.md, etc.)
- Each container = separate directory (c3-1-api/, c3-2-web/, etc.)
- refs/ = separate directory with pattern files (ref-auth.md, ref-errors.md)

## CRITICAL: The Three Categories

Load `**/references/component-categories.md` for the full Foundation vs Feature vs Ref rules.

**Key rule:** Components (Foundation/Feature) MUST have `## Code References`. Refs must NOT. If you cannot name a concrete file, create a ref instead.

---

## REQUIRED: Load References

**Load immediately** (use Glob to find, then Read):
1. `**/references/skill-harness.md` - Red flags and complexity rules
2. `**/references/layer-navigation.md` - How to traverse C3 docs

**Load for templating** (use Glob to find, then Read when needed):
- `**/templates/adr-000.md` - Adoption ADR (drives the workflow)
- `**/templates/context.md` - Context template
- `**/templates/container.md` - Container template
- `**/templates/component.md` - Component template
- `**/templates/ref.md` - Reference template

---

## Workflow Overview

```mermaid
flowchart TD
    GOAL([Goal]) --> S0

    subgraph S0["Stage 0: Inventory"]
        S0_DISCOVER[Discover codebase] --> S0_ASK{Gaps?}
        S0_ASK -->|Yes| S0_SOCRATIC[Socratic] --> S0_DISCOVER
        S0_ASK -->|No| S0_LIST[List items + diagram]
    end

    S0_LIST --> G0{Inventory complete?}
    G0 -->|No| S0_DISCOVER
    G0 -->|Yes| S1

    subgraph S1["Stage 1: Details"]
        S1_CONTAINER[Per container] --> S1_INT[Internal comp]
        S1_CONTAINER --> S1_LINK[Linkage comp]
        S1_INT --> S1_REF[Extract refs]
        S1_LINK --> S1_REF
        S1_REF --> S1_ASK{Questions?}
        S1_ASK -->|Yes| S1_SOCRATIC[Socratic] --> S1_CONTAINER
        S1_ASK -->|No| S1_NEXT{More?}
        S1_NEXT -->|Yes| S1_CONTAINER
    end

    S1_NEXT -->|No| G1{Fix inventory?}
    G1 -->|Yes| S0_DISCOVER
    G1 -->|No| S2

    subgraph S2["Stage 2: Finalize"]
        S2_CHECK[Integrity checks]
    end

    S2_CHECK --> G2{Issues?}
    G2 -->|Inventory| S0_DISCOVER
    G2 -->|Detail| S1_CONTAINER
    G2 -->|None| DONE([Implemented])
```

**Critical:** All questioning MUST use `AskUserQuestion` tool - never plain text questions.

---

## Progress Checklist

Copy and track as you work:

```
Onboarding Progress:
- [ ] Stage 0: All items inventoried (context, containers, components, refs)
- [ ] Stage 0: ADR-000 created with discovery tables filled
- [ ] Gate 0: Inventory complete, proceed to Details
- [ ] Stage 1: All container README.md created
- [ ] Stage 1: All component docs created
- [ ] Stage 1: All refs documented
- [ ] Gate 1: No new items discovered
- [ ] Stage 2: Integrity checks pass
- [ ] Gate 2: /c3 audit passes
- [ ] ADR-000 marked implemented
```

---

## Stage 0: Inventory

**Goal:** Discover EVERYTHING before creating any docs.

### 0.1 Create ADR-000

Run init script and create ADR-000 from template:
```bash
PROJECT="<name>" C1="<container1>" C2="<container2>" "${CLAUDE_PLUGIN_ROOT}/scripts/c3-init.sh"
```

### 0.2 Context Discovery

Read codebase structure. Capture template arguments in **ADR-000 Context Discovery table**:

| Arg | Value |
|-----|-------|
| PROJECT | What is this system called? |
| GOAL | Why does this system exist? |
| SUMMARY | One-sentence description |

Use `AskUserQuestion` for gaps:
```
Q: "I see apps/api/ and apps/web/. Are these separate containers?"
Options: [Separate containers, Single monolith, Monorepo with shared code]
```

### 0.3 Container Discovery

For each potential container, capture in **ADR-000 Container Discovery table**:

| N | CONTAINER_NAME | GOAL | SUMMARY |
|---|----------------|------|---------|

Note: `N` maps to init script variable (C1=1, C2=2, etc.)

Use `AskUserQuestion`:
```
Q: "Is apps/api/ a deployable backend API?"
Options: [Yes - Backend API, No - Library/shared code, Need more context]
```

### 0.4 Component Discovery (Brief)

For each container, scan for components. Capture in **ADR-000 Component Discovery table**:

| N | NN | COMPONENT_NAME | CATEGORY | GOAL | SUMMARY |
|---|----|--------------  |----------|------|---------|

**Categorization (use lowercase in table):**
- **foundation** (01-09): Primitives others depend on (Router, AuthProvider, Database)
- **feature** (10+): Domain-specific (UserService, CheckoutFlow, Dashboard)

Use `AskUserQuestion`:
```
Q: "AuthMiddleware is imported by 15 files. Foundation or Feature?"
Options: [Foundation - others depend on it, Feature - domain logic, Need more context]
```

### 0.5 Ref Discovery

Look for patterns that repeat across components. Capture in **ADR-000 Ref Discovery table**:

| SLUG | TITLE | GOAL | Applies To |
|------|-------|------|------------|

Common ref candidates:
- Error handling patterns
- Form patterns
- Query/data fetching patterns
- Design system principles
- User flows / IA

### 0.6 Overview Diagram

Generate mermaid diagram showing:
- Actors → Containers → External Systems
- Key linkages

### Gate 0

Before proceeding, verify:
- [ ] Context args filled (PROJECT, GOAL, SUMMARY)
- [ ] All containers identified with args
- [ ] All components identified (brief) with args
- [ ] Cross-cutting refs identified
- [ ] Overview diagram generated

**If gaps:** Return to discovery with Socratic questioning.

---

## Stage 1: Details

**Goal:** Create all docs from inventory.

### 1.1 Context Doc

Create `.c3/README.md` from `context.md` template using discovered args.

Fill:
- Goal section (from PROJECT, GOAL)
- Overview diagram
- Containers table with Goal Contribution column

### 1.2 Container Docs

For EACH container in inventory:

**1.2.1 Create container README**

Create `.c3/c3-N-{slug}/README.md` from `container.md` template.

Fill:
- Goal section
- Context Connection (how it serves parent)
- Components table with Goal Contribution column

**1.2.2 Create component docs**

For each component in this container:

Create `.c3/c3-N-{slug}/c3-NNN-{component}.md` from `component.md` template.

Fill:
- Goal section
- Container Connection
- Related Refs table

**1.2.3 Extract Refs During Component Documentation**

While documenting components, proactively identify content that belongs in refs.

Load `**/references/onboard-ref-extraction.md` for the separation test, signals, and common extractions.

**Quick test:** "Would this content change if we swapped the underlying technology?"
- **Yes** → Extract to ref
- **No** → Keep in component

**Common extractions:** error handling, auth patterns, database usage, API conventions, state management.

**1.2.4 Handle discoveries**

If new component found during documentation:
- Add to ADR-000 Component Discovery table
- Document conflict in Conflict Resolution table
- Continue (will verify at Gate 2)

### 1.3 Ref Docs

For each ref in inventory:

Create `.c3/refs/ref-{slug}.md` from `ref.md` template.

Fill:
- Goal section
- Content sections
- Update Cited By as you create component docs

### Gate 1

Before proceeding, verify:
- [ ] All container README.md created
- [ ] All component docs created
- [ ] All refs documented
- [ ] No new items discovered (else → update ADR-000 inventory)

**If new items discovered:** Return to Stage 0, update ADR-000 discovery tables.

---

## Stage 2: Finalize

**Goal:** Verify integrity across all docs.

### 2.1 Integrity Checks

| Check | How to Verify |
|-------|---------------|
| Context ↔ Container | Every container in ADR-000 appears in c3-0 Containers table |
| Container ↔ Component | Every component in container README has a doc |
| Component ↔ Component | Linkages documented in Container README |
| * ↔ Refs | Refs Cited By section matches component Related Refs |

### 2.2 Run Audit

```
/c3 audit
```

### Gate 2

Before marking complete, verify:
- [ ] All integrity checks pass
- [ ] `/c3 audit` passes

**If issues:**
- Inventory issues (missing container/component) → Gate 0
- Detail issues (wrong Goal, missing connection) → Gate 1
- Pass → Mark ADR-000 as `implemented`

---

## Tiered Assumption Rules

| Impact | Examples | Action |
|--------|----------|--------|
| High | New External, boundary change, component reassignment | Ask first via AskUserQuestion |
| Low | Linkage reasoning, naming fix, add to inventory | Auto-proceed, note in Conflict Resolution |

---

## End-to-End Example

```
User: "Set up C3 for my project"

=== Stage 0: Inventory ===
1. Run c3-init.sh, create ADR-000
2. Discover via AskUserQuestion: PROJECT="Acme Platform", GOAL="E-commerce"
3. Discover containers: c3-1-api, c3-2-web
4. Discover components: c3-101-auth (foundation), c3-110-products (feature)
5. Discover refs: ref-error-handling (used by 5 components)
Gate 0: All inventory complete ✓

=== Stage 1: Details ===
1. Create .c3/README.md from context template
2. Create c3-1-api/README.md + component docs
3. Create c3-2-web/README.md + component docs
4. Create refs/ref-error-handling.md
Gate 1: All docs created, no new discoveries ✓

=== Stage 2: Finalize ===
1. Integrity checks: all linkages valid ✓
2. Run /c3 audit: passes ✓
3. Mark ADR-000 as implemented ✓
```

---

## FINAL CHECKLIST - Verify Before Completing

**Before completing, verify structure exists:**

```bash
ls .c3/README.md          # Context
ls .c3/TOC.md             # TOC
ls .c3/adr/*.md           # At least ADR-000
ls .c3/refs/ref-*.md      # At least one ref
ls .c3/c3-*/README.md     # Container(s)
ls .c3/c3-*/c3-*.md       # Component(s)
```

**If refs/ is empty:** Create at least one for common patterns (error handling, auth, API conventions).

**If any file is missing, create it before completing!**
