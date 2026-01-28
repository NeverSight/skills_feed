---
name: spec-implement
description: Execute implementation by processing tasks defined in tasks.md. Use when user says "/spec-implement", "implement the feature", "start coding" after /spec-tasks to begin phase-by-phase implementation.
---

# Spec-Implement

Execute implementation plan by processing tasks.md.

**Prerequisites**: tasks.md must exist (run `/spec-tasks` first).

## Workflow

1. **Initialize** - Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks`
2. **Check checklists** - Verify all checklists complete (if any)
3. **Load context** - tasks.md, plan.md, data-model.md, contracts/
4. **Setup verification** - Create/verify ignore files
5. **Parse tasks** - Extract phases, dependencies, parallel markers
6. **Execute** - Phase-by-phase implementation
7. **Track progress** - Mark completed tasks `[X]`
8. **Validate** - Verify completion and test results

## Checklist Gate

If `FEATURE_DIR/checklists/` exists:

```markdown
| Checklist | Total | Completed | Incomplete | Status |
|-----------|-------|-----------|------------|--------|
| ux.md     | 12    | 12        | 0          | ✓ PASS |
| test.md   | 8     | 5         | 3          | ✗ FAIL |
```

- All PASS → Proceed automatically
- Any FAIL → Ask user confirmation

## Ignore Files Setup

Detect and create based on tech stack:

| Detection | Create |
|-----------|--------|
| `.git` exists | `.gitignore` |
| `Dockerfile*` | `.dockerignore` |
| `.eslintrc*` | `.eslintignore` |
| `package.json` | `.npmignore` |
| `*.tf` files | `.terraformignore` |

## Execution Rules

### Phase Order
1. **Setup** - Project initialization
2. **Tests** - Write failing tests (if TDD)
3. **Core** - Models, services, CLI
4. **Integration** - DB, middleware, external services
5. **Polish** - Optimization, documentation

### Dependency Rules
- Sequential tasks → In order
- `[P]` tasks → Can run together
- Same file → Sequential
- Phase complete → Next phase

### Progress Tracking
- Report after each task
- Halt on non-parallel failure
- Mark completed: `- [X] T001...`

## Technology Patterns

### Node.js/TypeScript
```
node_modules/, dist/, build/, *.log, .env*
```

### Python
```
__pycache__/, *.pyc, .venv/, dist/, *.egg-info/
```

### Go
```
*.exe, *.test, vendor/, *.out
```

### Rust
```
target/, debug/, release/, *.rs.bk
```

## Completion Validation

- All required tasks completed
- Implementation matches specification
- Tests pass (if applicable)
- Coverage meets requirements

## Next Steps

After `/spec-implement`:
- Run tests and verify
- Create PR or deploy
