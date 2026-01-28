---
name: progress-report
description: >
  Displays progress dashboard showing phase completion, blocked tasks,
  and remaining work estimate. Provides at-a-glance view of implementation
  status. Run anytime to check progress.
version: 0.0.1
license: MIT
compatibility: Requires tasks.md
metadata:
  author: drillan
  category: reporting
  repository: https://github.com/drillan/speckit-gates
---

# progress-report

Displays a progress dashboard showing implementation status.

## Purpose

This skill provides an at-a-glance view of your implementation progress:

- **Phase completion**: Progress bar for each phase in tasks.md
- **Blocked tasks**: Highlights tasks that are blocked
- **Potentially complete**: Tasks that may be done but not marked
- **Remaining work**: Estimate of remaining tasks

## Output

The skill outputs a **ProgressDashboard** with:

- Overall completion percentage
- Per-phase progress breakdown
- List of blocked tasks
- Potentially complete tasks (based on file existence)
- Remaining work estimate

## Usage

This is a manual skill - run it anytime to check progress:

```bash
npx skills run progress-report
```

Or via AI agent:
```
User: Show me the progress report
```

## Exit Codes

| Code | Status | Meaning |
|------|--------|---------|
| 0 | Success | Report generated |
| 3 | Error | tasks.md missing |

## Dashboard Sections

### Overall Progress

```
Overall Progress: [##########----------] 50% (25/50 tasks)
```

### Phase Breakdown

```
| Phase | Progress | Completed | Total |
|-------|----------|-----------|-------|
| Setup | [####----] 50% | 2 | 4 |
| Core  | [########] 100% | 10 | 10 |
| Tests | [##------] 25% | 3 | 12 |
```

### Blocked Tasks

Tasks that cannot proceed due to dependencies or issues:

```
- T015: Waiting for API specification
- T023: Blocked by T015
```

### Potentially Complete

Tasks that reference files which already exist (FR-031a):

```
- T008: File skills/planning-validate/SKILL.md exists
- T009: File skills/planning-validate/scripts/validate.sh exists
```

### Remaining Work

```
- Incomplete tasks: 25
- Blocked tasks: 2
```

## Detection Logic

### Blocked Tasks

A task is considered blocked if:
- Its description contains "blocked" or "waiting"
- It depends on an incomplete task (future enhancement)

### Potentially Complete Tasks

A task is potentially complete if:
- It references a file path that exists
- File was created/modified recently
- Task is not yet marked as complete
