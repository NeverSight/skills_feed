---
name: implementation-verify
description: >
  Verifies implementation against specifications by checking requirement fulfillment,
  task completion, and contract implementation. Generates a fulfillment report with
  coverage metrics. Always run after /speckit.implement completes.
version: 0.0.1
license: MIT
compatibility: Requires spec kit with check-prerequisites.sh, tasks.md must exist
metadata:
  author: drillan
  category: quality-gate
  repository: https://github.com/drillan/speckit-gates
---

# implementation-verify

Verifies implementation against specifications after `/speckit.implement` completes.

## Purpose

This skill automatically verifies that your implementation fulfills the specified requirements. It checks:

- **FR requirement fulfillment**: How many FR-XXX requirements are addressed by completed tasks
- **Task completion rate**: Percentage of tasks marked complete in tasks.md
- **Contract implementation**: API endpoints implemented as specified (if contracts/ exists)
- **Test coverage alignment**: Implementation aligns with test requirements

## Output

The skill outputs a **Fulfillment Report** with:

- Coverage metrics (FR, task, contract percentages)
- List of unimplemented requirements
- Recommended actions to improve coverage

## Usage

This skill runs automatically after `/speckit.implement`. You can also run it manually:

```bash
npx skills run implementation-verify
```

## Exit Codes

| Code | Status | Meaning |
|------|--------|---------|
| 0 | Complete | 100% fulfillment |
| 1 | Partial | >80% fulfillment |
| 2 | Low | <80% fulfillment |
| 3 | Error | Required files missing |

## Checks Performed

### Task Completion Analysis

1. Parse tasks.md for all task items
2. Count completed tasks (marked with [X] or [x])
3. Calculate completion percentage per phase
4. Identify blocked or incomplete tasks

### FR Fulfillment Analysis

1. Extract all FR-XXX references from spec.md
2. Cross-reference with completed tasks
3. Identify FRs without corresponding completed tasks
4. Calculate fulfillment percentage

### Contract Implementation (if contracts/ exists)

1. Parse contract files for endpoint definitions
2. Check if corresponding implementation exists
3. Calculate contract coverage percentage

## Metrics Explained

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| FR Coverage | Implemented FRs / Total FRs | Requirements addressed |
| Task Completion | Completed Tasks / Total Tasks | Work progress |
| Contract Coverage | Implemented Endpoints / Total Endpoints | API completeness |

## Recommendations

After receiving low coverage:

1. Review unimplemented requirements list
2. Check for blocked tasks and resolve blockers
3. Ensure task completion is properly marked in tasks.md
4. Re-run `/speckit.implement` for remaining work
5. Run `implementation-verify` again to verify progress
