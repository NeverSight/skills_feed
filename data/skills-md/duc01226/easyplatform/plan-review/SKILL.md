---
name: plan-review
description: "[Planning] Self-review plan for validity, correctness, and best practices"
argument-hint: [plan-path]
infer: true
---

> **CRITICAL:** Do NOT use `EnterPlanMode` tool — it blocks Write/Edit/Task tools. Follow the workflow below.

## Your Mission

Critically self-review the implementation plan to ensure quality before coding begins.

## Plan Resolution

1. If `$ARGUMENTS` provided → Use that path
2. Else check `## Plan Context` → Use active plan path
3. If no plan found → Error: run `/plan` first

## Review Checklist

| Category           | Check                                                      |
| ------------------ | ---------------------------------------------------------- |
| **Structure**      | Has plan.md with YAML frontmatter (title, status, effort)? |
| **Structure**      | Phases numbered and linked correctly?                      |
| **Logic**          | Dependencies between phases mapped?                        |
| **Logic**          | Risk assessment present with mitigations?                  |
| **Patterns**       | Uses platform patterns (not custom solutions)?             |
| **Patterns**       | Files in correct project locations?                        |
| **Completeness**   | Success criteria defined and measurable?                   |
| **Completeness**   | All edge cases considered?                                 |
| **Best Practices** | Follows YAGNI/KISS/DRY principles?                         |
| **Best Practices** | No over-engineering or premature abstraction?              |

## Review Process

1. **Read** plan.md and all phase-*.md files
2. **Evaluate** each checklist item
3. **Identify** issues with specific locations and fixes
4. **Output** approval or revision requirements

## Output Format

**If Plan Passes:**
```
✅ Plan Review: APPROVED

- Structure: Valid
- Logic: Sound
- Patterns: Compliant
- Completeness: Adequate
- Best Practices: Followed

Proceeding to implementation...
```

**If Issues Found:**
```
⚠️ Plan Review: NEEDS REVISION

Issues:
1. [Category] [File:Line] Issue description → Fix suggestion
2. [Category] [File:Line] Issue description → Fix suggestion

Update plan before proceeding.
```

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed

## Important Notes

- Focus on **major issues** that would impact implementation
- Don't nitpick formatting or style unless it affects clarity
- If plan is simple and solid, approve quickly
- Always provide actionable fix suggestions for issues
