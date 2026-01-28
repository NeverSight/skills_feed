---
name: dev-changelog
description: Capture implementation summary, track progress, identify docs updates
version: 1.0.0
---

# /dev-changelog - Implementation Summary

> **Skill Awareness**: See `skills/_registry.md` for all available skills.
> - **Before**: `/dev-review` passes (code is good)
> - **Reads**: Git changes, specs, use cases
> - **Outputs**: Summary of what was built, what's left, docs to update

Capture what was implemented after review passes. Creates actionable documentation.

## When to Use

- After `/dev-review` passes
- End of sprint/milestone
- Before handoff to another developer
- When you need to resume work later

## Usage

```
/dev-changelog billing              # Summarize billing feature work
/dev-changelog --since=v1.0.0       # Changes since tag
/dev-changelog --since=2024-01-01   # Changes since date
/dev-changelog --pr=123             # Changes in specific PR
```

## Output

```
plans/features/{feature}/
├── summary.md              # What was built (this session/PR)
├── implementation.md       # Cumulative implementation status
├── tech-debt.md            # Known issues, TODOs
└── docs-updates.md         # Documentation tasks
```

## Expected Outcome

Documentation of what was implemented after `/dev-review` passes.

**Outputs:**
- `summary.md` - What was built this session/PR
- `implementation.md` - Cumulative status (updated)
- `tech-debt.md` - Known issues, TODOs (updated)
- `docs-updates.md` - Documentation tasks

## Success Criteria

- Changes mapped to specs and use cases
- Completion status clear (done/partial/not started)
- Tech debt captured (TODOs, workarounds, gaps)
- Documentation tasks identified
- Easy to resume work later
- Clear what's done, what's remaining

## Prerequisite

**Verify `/dev-review` passed:**
- If review not done or failed → "Run /dev-review first"

## Sources to Gather

**Git (source of truth):**
- `git log --oneline {since}` - Commits made
- `git diff --stat {since}` - Files changed
- `gh pr view {number}` - PR info (if available)

**Intent & Context:**
- specs/*.md - What was intended
- use-cases/*.md - Business context
- implementation.md (previous) - Track cumulative status

## Analysis

**Map git changes to specs and use cases:**

For each changed file:
- What component? (API, UI, model, etc.)
- Which spec item does it fulfill?
- Which use case does it support?
- Complete or partial?

**Extract tech debt:**
- TODOs in changed files (grep for TODO/FIXME/HACK/XXX)
- Incomplete spec items (spec says X, implementation does Y)
- Known issues from commits (WIP, temporary, workaround)
- Review comments not addressed

**Identify doc updates needed:**

| Change Type | Doc Update |
|-------------|------------|
| New API endpoint | API Reference |
| New UI feature | User Guide |
| New config option | Configuration docs |
| Breaking change | Migration guide |
| New component | Component docs |

## Output Files

**summary.md** (per session/PR):
- What was built (API, UI, data changes)
- Spec items completed (with status)
- Use cases addressed (coverage)
- Commits list
- Next steps

**implementation.md** (cumulative):
- Overall progress percentage
- Completed items (with PR reference)
- In progress items (what's done, what's remaining)
- Not started items (with blockers if any)
- History (date, PR, summary)

**tech-debt.md** (updated):
- High/Medium/Low priority issues
- Location, impact, notes for each
- Code TODOs with file:line references

**docs-updates.md** (updated):
- Required updates (API Reference, User Guide, Configuration)
- Examples to add (code snippets)
- Screenshots needed

## Resume Flow

When returning to work later:
1. Read implementation.md → See what's done, what's remaining
2. Read tech-debt.md → See known issues
3. Read summary.md (latest) → See where you left off
4. Continue with `/dev-specs` or `/dev-coding`

## Integration with /dev-review

When `/dev-review` completes successfully:

```
/dev-review output:
├── quality-report.md (existing)
└── Suggests: "Run /dev-changelog to document what was built"

Then:
/dev-changelog
├── Reads review output
├── Reads git changes
├── Generates summary.md, implementation.md, etc.
```

## Resume Flow

When returning to work later:

```
1. Read implementation.md
   → See what's done, what's remaining

2. Read tech-debt.md
   → See known issues

3. Read summary.md (latest)
   → See where you left off

4. Continue with /dev-specs or /dev-coding
```

## Tools Used

| Tool | Purpose |
|------|---------|
| `Bash` | Git log, diff, grep for TODOs |
| `Read` | Specs, use cases, previous status |
| `Write` | Output files |
| `Grep` | Find TODOs in code |

## Example Flow

```
User: /dev-changelog billing

1. Verify review
   → Found: plans/features/billing/review-report.md (passed)

2. Gather sources
   → Git: 5 commits since last changelog
   → Specs: SPEC-PAY-001 to 006
   → UCs: UC-PAY-001 to 005

3. Analyze changes
   → 3 API files changed
   → 4 UI files changed
   → 2 new models

4. Map to specs
   → SPEC-PAY-001: Complete (checkout)
   → SPEC-PAY-002: Complete (payments)
   → SPEC-PAY-004: Partial (subscriptions)

5. Extract tech debt
   → 3 TODOs found
   → 1 incomplete spec item

6. Identify doc updates
   → 3 new endpoints need docs
   → 2 new UI features need guide

7. Generate outputs
   → summary.md
   → implementation.md (updated)
   → tech-debt.md (updated)
   → docs-updates.md

Output:
"Documented billing implementation:
 - 2 specs complete, 1 partial
 - 3 tech debt items
 - 6 doc updates needed

 See: plans/features/billing/summary.md"
```
