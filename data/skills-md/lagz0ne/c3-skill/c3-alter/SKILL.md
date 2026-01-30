---
name: c3-alter
description: |
  Makes architectural changes through ADR-first workflow with staged intent clarification.
  Use when the user asks to "add a component", "change architecture", "refactor X", "implement feature",
  "fix bug", "create new service", "update diagram", or "remove component".
  Requires .c3/ to exist. All changes flow through ADR process. For questions, route to c3-query.
---

# C3 Alter - Change Through ADR

**Every change flows through an ADR.** No exceptions.

**Relationship to c3-orchestrator agent:** This skill defines the change workflow stages. The `c3-skill:c3-orchestrator` agent implements this workflow, dispatching to sub-agents (c3-analysis, c3-synthesizer) for comprehensive analysis. Use the agent when spawning via Task tool; use this skill directly for inline execution.

## REQUIRED: Load References

Before proceeding, use Glob to find and Read these files:
1. `**/references/skill-harness.md` - Red flags and complexity rules
2. `**/references/layer-navigation.md` - How to traverse C3 docs
3. `**/references/adr-template.md` - ADR structure (for Stage 4)
4. `**/references/component-lifecycle.md` - Provisioned status model (for Stage 2b)

## Core Loop (All Stages)

```
ANALYZE → ASK (until confident) → SYNTHESIZE → REVIEW
              │                        │
              └── until no open ───────┘
                  questions

On conflict: ASCEND → fix earlier stage → re-descend
```

**Confident = No open questions.** Don't proceed with "TODO" or unclear fields.

## Progress Checklist

Copy and track as you work:

```
Change Progress:
- [ ] Stage 1: Intent clarified (type, goal confirmed)
- [ ] Stage 2: Current state documented (affected components listed)
- [ ] Stage 3: Scope assessed (all c3 IDs, breaking changes noted)
- [ ] Stage 4: ADR created (proposed, validation passed)
- [ ] Stage 4b: ADR accepted by user
- [ ] Stage 5: Plan created with ordered steps
- [ ] Stage 6: Execution complete (docs, code, diagrams)
- [ ] Stage 7: Audit passed, ADR marked implemented
```

---

## Stage 1: Intent

| Step | Action |
|------|--------|
| Analyze | Add/modify/remove/fix? What problem? Scope hint? |
| Ask | Use AskUserQuestion: feature vs fix? problem? urgency? |
| Synthesize | `Intent: [action] Goal: [outcome] Type: [feature/fix/refactor]` |
| Review | User confirms or corrects |

---

## Stage 2: Current State

| Step | Action |
|------|--------|
| Analyze | Read affected C3 docs via layer navigation |
| Ask | Are docs accurate? Recent code changes not documented? |
| Synthesize | List affected components, their current behavior, dependencies |
| Review | User confirms or corrects |

---

## Stage 2b: Detect Provisioned Components

Check if component has a provisioned version:

```bash
# Check for provisioned version
ls .c3/provisioned/c3-*/c3-XXX-*.md 2>/dev/null
```

**If provisioned version exists:**

```
AskUserQuestion:
  question: "Found provisioned design for this component at .c3/provisioned/... Implement from this design?"
  options:
    - "Yes - use provisioned design as starting point"
    - "No - start fresh (will supersede provisioned)"
```

**On "Yes":**
1. Load provisioned doc as starting point for analysis
2. ADR frontmatter: add `implements: <provisioned-adr>`
3. After implementation complete, promote provisioned docs

**On "No":**
1. Proceed with normal alter flow (fresh analysis)
2. After implementation, delete orphaned provisioned file
3. Update provisioned ADR: `superseded-by: <this-adr>` with note "Design not used"

---

## Stage 3: Scope Impact

| Step | Action |
|------|--------|
| Analyze | Which layers change? Dependencies? Linkages? Diagrams? |
| Ask | External systems involved? Breaking changes? Keep or replace? |
| Synthesize | List all affected c3 IDs, note breaking changes |
| Review | User confirms or expands |

---

## Stage 4: Create ADR

Generate at `.c3/adr/adr-YYYYMMDD-{slug}.md`. Use `**/references/adr-template.md`.

**Key sections:** Problem, Decision, Rationale, Affected Layers, References Affected, Verification

**Note:** ADR is only created after synthesizer validation passes. The synthesizer validates architectural coherence before ADR generation.

---

## Stage 4b: ADR Acceptance

Use AskUserQuestion to ask the user to approve or reject the ADR.

| On Accept | Update status to `accepted`, **then immediately execute Stage 5 and 6** |
|-----------|---------------------------------------------|
| On Reject | Return to Stage 1/3 based on what changed |

**CRITICAL - After user accepts ADR:** You MUST continue executing without stopping. Create the component documentation file(s) and update the container README. Do NOT end after receiving approval.

---

## Stage 5: Create Plan

Generate at `.c3/adr/adr-YYYYMMDD-{slug}.plan.md`.

**Include:**
- Pre-execution checklist (update `## References` in affected components)
- Ordered steps: docs first, then code, then diagrams
- Verification commands

**After ADR acceptance, immediately create the plan and continue to execution.**

---

## Stage 6: Execute

**Execute the plan immediately after creating it.** For documentation-only changes (no code implementation requested), this means:

1. **Create component documentation** - Write the new component file (e.g., `c3-106-*.md`)
2. **Update container README** - Add new component to the Components table
3. **Update TOC** - Add link to new component

Follow plan order:
1. Make change (doc or code)
2. Check for conflicts
3. Update `## References` if code moved/added/removed

**On conflict - Tiered response:**

| Impact | Action |
|--------|--------|
| High: scope expansion, breaking change, new layer | Ask user, update ADR if needed |
| Low: wording fix, diagram update, ID fix | Auto-fix, note in log |

### Ref Maintenance

If change affects a pattern:
1. Check if `ref-*` exists for pattern
2. Update ref if pattern changes
3. Create new ref if pattern is new and reusable

**Critical: The Three Categories**

Load `**/references/component-categories.md` for the full Foundation vs Feature vs Ref rules.

**Key rule:** Components (Foundation/Feature) MUST have `## Code References`. Refs must NOT. If you cannot name a concrete file, create a ref instead.

### Promoting Provisioned Components

If implementing a provisioned component (detected in Stage 2b):

1. **Move file:**
   ```bash
   mv .c3/provisioned/c3-X/c3-XXX.md .c3/c3-X/c3-XXX.md
   ```

2. **Update frontmatter:**
   ```yaml
   status: active    # Changed from provisioned
   # Remove supersedes: field if present
   # Remove adr: field (or update to implementation ADR)
   ```

3. **Add Code References section** pointing to implemented files

**Note:** The provisioned ADR is superseded by `c3-adr-transition` agent AFTER verification passes in Stage 7, not during execution. This ensures we don't mark the design as superseded if implementation fails verification.

---

## Stage 7: Verify

Run `/c3 audit`. Check diagrams, IDs, linkages, code-doc match.

| On Pass | Update ADR status to `implemented` |
|---------|-----------------------------------|
| On Fail | Fix issue, re-audit, loop until pass |

---

## Examples

**Example 1: Add feature**
```
User: "Add rate limiting to the API"

Stage 1 - Intent:
  Intent: Add rate limiting
  Goal: Prevent API abuse
  Type: Feature

Stage 2 - Current State:
  Affected: c3-2-api (API Backend)
  Current: No rate limiting exists
  Depends on: c3-201-auth-middleware (good injection point)

Stage 3 - Scope:
  Changes: Add c3-206-rate-limiter component
  Affects: c3-201 (middleware chain)
  Breaking: No

Stage 4 - ADR:
  Created: .c3/adr/adr-20260109-rate-limiting.md
  Status: proposed (validation passed)

Stage 4b - Accept:
  User accepts → status: accepted

Stage 5 - Plan:
  1. Create c3-206-rate-limiter.md
  2. Update c3-2-api/README.md inventory
  3. Implement src/api/middleware/rate-limiter.ts
  4. Update c3-201 hand-offs

Stage 6 - Execute: Follow plan
Stage 7 - Verify: /c3 audit
```

**Example 2: Fix bug**
```
User: "Fix the login timeout issue"

Stage 1 - Intent:
  Intent: Fix bug
  Goal: Login doesn't timeout prematurely
  Type: Fix

Stage 2 - Current State:
  Affected: c3-201-auth-middleware
  Current: Session TTL hardcoded to 15min
  Issue: Users report logout after 10min

Stage 3 - Scope:
  Changes: Modify existing component
  Affects: c3-201 only
  Breaking: No

Stage 4 - ADR:
  Created: .c3/adr/adr-20260109-login-timeout-fix.md
  Status: proposed (validation passed, simpler ADR for bugfix)

Stage 4b - Accept:
  User accepts → status: accepted

Stage 5-7: Execute and verify
```

---

## Response Format

```
**Stage N: {Name}**
{findings}
**Open Questions:** {list or "None - confident"}
**Next:** {what happens next}
```
