---
name: fix-review-issues
description: "Orchestrate fixing issues found by $review. Handles issue discovery, user confirmation, plan creation, and execution via $implement. Triggers: fix review issues, fix findings, address review feedback."
---

**User request**: $ARGUMENTS

Systematically address issues found from `$review` runs. Orchestrates: discover issues → confirm scope → plan → execute → verify.

**Flags**: `--autonomous` → skip Phase 2 scope confirmation and Phase 5 next-steps prompt (requires scope args)

## Workflow

### Phase 0: Parse Arguments

Parse `$ARGUMENTS` to determine scope:

| Argument | Effect |
|----------|--------|
| (none) | Fix ALL issues from review |
| `--severity <level>` | Filter by severity (critical, high, medium, low) |
| `--category <type>` | Filter by category (use categories found in review output) |
| File paths | Focus on specific files only |

Multiple filters combine: `--severity critical,high --category <cat1>,<cat2>`

### Phase 1: Discover Review Results

**Step 1**: Check if review results exist in the current conversation context.

**Step 2**: If NO review results found, ask the user:

```
No Review Results Found

I couldn't find recent $review output in this conversation. What would you like to do?
Options:
  - Run $review now - perform a fresh review first
  - Paste review output - I'll provide the review results
  - Cancel - I'll run $review myself first
```

- If "Run $review now": Inform user to run `$review` first, then return to `$fix-review-issues`
- If "Paste review output": Wait for user to provide the review results
- If "Cancel": End the workflow

**Step 3**: If review results ARE found, extract and categorize all issues:

1. Parse each issue for: severity, category, file path, line number, description, suggested fix
2. Group issues by category
3. Count totals by severity

### Phase 1.5: Validate Findings Against Higher-Priority Sources

**Before confirming scope, filter findings that conflict with higher-priority sources (AGENTS.md, Plan, Spec).**

#### Step 1: Check for AGENTS.md Adherence Conflicts

Review all findings from non-adherence reviewers (simplicity, maintainability, type-safety, docs, coverage) against AGENTS.md adherence findings:

1. For each AGENTS.md adherence finding, identify what rule/guideline it enforces
2. Check if other reviewers suggest changes that would **violate** that rule:
   - **Simplicity** suggests inlining code → but AGENTS.md requires helper functions for that pattern → REMOVE simplicity finding
   - **Maintainability** suggests consolidating files → but AGENTS.md specifies file structure → REMOVE maintainability finding
   - **Type-safety** suggests stricter types → but AGENTS.md allows flexibility for that case → REMOVE type-safety finding
3. Report filtered findings:
   ```
   ## Findings Filtered (Conflict with AGENTS.md Rules)

   The following issues were removed because they conflict with AGENTS.md project rules:
   - [Simplicity issue]: Filtered—AGENTS.md rule X specifies this pattern
   - [Maintainability issue]: Filtered—AGENTS.md requires this structure
   ```

**Why this matters:** AGENTS.md contains user-defined rules specific to this project. Generic reviewer suggestions that contradict explicit user rules should be discarded—the user's decisions take precedence.

#### Step 2: Check for Plan/Spec Conflicts

Search for plan and spec files:
```bash
# Look for plan files
ls /tmp/plan-*.md 2>/dev/null | head -5
find . -name "plan-*.md" -o -name "PLAN.md" 2>/dev/null | head -5

# Look for spec files
ls /tmp/spec-*.md 2>/dev/null | head -5
find . -name "spec-*.md" -o -name "SPEC.md" -o -name "requirements*.md" 2>/dev/null | head -5
```

**If plan/spec files exist:**

1. Read the plan/spec files
2. For each review finding, check if it contradicts planned/specified behavior:
   - **Simplicity issues**: If the plan explicitly requires the pattern (e.g., "use factory pattern for extensibility"), REMOVE the finding
   - **Maintainability issues**: If the plan specifies the structure (e.g., "separate concerns into X files"), REMOVE findings that critique this
   - **Type safety issues**: If the spec requires the flexibility (e.g., "must accept arbitrary JSON"), REMOVE strict typing findings
3. Report filtered findings with explanation:
   ```
   ## Findings Filtered (Justified by Plan/Spec)

   The following issues were removed because they're justified by the implementation plan or spec:
   - [Issue]: Filtered because plan specifies "..."
   - [Issue]: Filtered because spec requires "..."
   ```

**Why this matters:** Review agents run without plan context. A "premature abstraction" finding may actually be an intentional pattern the plan required for future extensibility. Blindly fixing such issues would undo deliberate architectural decisions.

### Phase 2: Confirm Scope with User

**If `--autonomous` OR scope arguments provided** → skip Phase 2, proceed to Phase 3

**If NO arguments** (fix all):

```
Review Issues Summary

Found {N} total issues from the review. What would you like to fix?

[Display: Issue breakdown by category and severity]

Options:
  - Fix all issues (Recommended)
  - Only critical and high severity
  - Only specific categories - let me choose
  - Only specific files - let me specify
```

**If "Only specific categories"**:

Present multi-select with categories found in the review output (dynamically generated from Phase 1 parsing).

**If "Only specific files"**:

```
Specify Files

Which files or directories should I focus on?
(e.g., src/auth/ or src/utils.ts, src/helpers.ts)
```

### Phase 3: Create Fix Plan

**Order issues by priority** before creating the plan (see Issue Priority Order section):
1. Bugs first
2. AGENTS.md Adherence issues
3. Type Safety
4. Coverage
5. Maintainability
6. Simplicity
7. Docs

Invoke the plan skill to create the implementation plan: `$plan Fix these review issues in priority order (bugs → AGENTS.md adherence → type safety → coverage → maintainability → simplicity → docs): [summary of issues within confirmed scope, grouped by priority]`

Once the plan is approved, note the plan file path (typically `/tmp/plan-*.md`) and proceed to execution.

### Phase 4: Execute Fixes

Invoke the implement skill to execute the plan: `$implement <plan-file-path>`

The `$implement` skill handles dependency-ordered execution, progress tracking, and auto-fixing gate failures.

### Phase 5: Next Steps

**If `--autonomous`**: Skip prompt, end after implementation completes. Caller handles verification.

**Otherwise**, ask the user:

```
Fixes Complete

Implementation finished. What would you like to do next?
Options:
  - Run $review again - verify fixes are complete (Recommended)
  - Show diff - see all changes made
  - Done - I'll verify manually
```

## Issue Priority Order

When fixing issues, follow this priority hierarchy:

| Priority | Category | Rationale |
|----------|----------|-----------|
| **1** | Bugs | Correctness issues that cause incorrect behavior—always fix first |
| **2** | AGENTS.md Adherence | User-defined project rules take precedence over generic best practices |
| **3** | Type Safety | Prevents runtime errors and improves reliability |
| **4** | Coverage | Tests protect against regressions |
| **5** | Maintainability | Long-term code health |
| **6** | Simplicity | Nice-to-have improvements |
| **7** | Docs | Lowest priority unless blocking other work |

**Why AGENTS.md adherence is high priority**: The AGENTS.md file contains user-defined rules specific to this project. When other reviewers (simplicity, maintainability, etc.) suggest changes that conflict with AGENTS.md guidelines, the user's explicit rules win. Fixing AGENTS.md adherence issues early prevents wasted effort fixing issues that would later be undone.

### Conflict Resolution

When reviewer findings conflict with each other:

1. **AGENTS.md vs other reviewers**: AGENTS.md adherence wins. If simplicity reviewer says "inline this helper" but AGENTS.md specifies "use helper functions for X pattern"—keep the helper.
2. **Plan/Spec vs reviewers**: Plan/Spec wins (handled in Phase 1.5). Intentional architectural decisions aren't mistakes.
3. **Between equal-priority reviewers**: Defer to the verification agent's reconciliation from `$review`.

## Key Principles

- **Respect User Rules**: AGENTS.md adherence issues take precedence—these are explicit user decisions that override generic reviewer suggestions
- **Respect the Plan**: Filter out findings that contradict the implementation plan or spec—these are intentional decisions, not mistakes
- **User Control**: Confirm scope before making changes
- **Reduce Cognitive Load**: Offer clear options with recommended option first
- **High Confidence Only**: Only fix issues that are clearly unintentional problems, not design decisions
