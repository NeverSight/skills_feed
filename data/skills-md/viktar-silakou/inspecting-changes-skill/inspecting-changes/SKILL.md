---
name: inspecting-changes
description: Pre-execution static analysis of code changes. Use when reviewing AI-generated code before execution, commit, or deployment. Triggers on code generation completion, pre-commit review, or risk assessment needs.
---

# Inspecting Changes

Static analysis of code changes BEFORE execution.

## Workflow Checklist

Copy and track progress:

```
Analysis Progress:
- [ ] Step 1: Parse mode (quick/medium/deep) from arguments
- [ ] Step 2: Detect changes (git diff or explicit path)
- [ ] Step 3: Execute phases for selected mode
- [ ] Step 4: Generate report with findings
```

**Step 1: Parse mode**
- If mode in arguments → use it
- If no mode → use AskUserQuestion with options: Quick, Medium, Deep

**Step 2: Detect changes**
- Default: `git diff --name-status` (uncommitted)
- With path: `git diff --name-status -- <path>`
- With ref: `git diff --name-status <ref1>..<ref2>`

**Step 3: Execute phases by mode**

| Mode | Phases | Use Case |
|------|--------|----------|
| quick | 1, 2, 8 | Pre-commit, small changes |
| medium | 1, 2, 2b, 3, 5.1, 8 | Standard review |
| deep | 1, 2, 2b, 3, 4, 5, 6, 7, 8 | Major features, pre-deploy |

**Step 4: Generate report**
- See [modules/output.md](modules/output.md) for format templates

## Tool Rules

**Read-only analysis.** Never modify files. Never execute code.

Allowed:
- `git diff`, `git log`, `git show` (read-only)
- Read, Grep, Glob tools

Every finding MUST include `file:line` reference.

## Phase Reference

| Phase | Focus | Module |
|-------|-------|--------|
| 1 | Scope assessment | [modules/phase-1-assessment.md](modules/phase-1-assessment.md) |
| 2 | Execution flow | [modules/phase-2-flow.md](modules/phase-2-flow.md) |
| 2b | Contract alignment | [modules/phase-2b-contracts.md](modules/phase-2b-contracts.md) |
| 3 | Architecture, smells, legacy | [modules/phase-3-architecture.md](modules/phase-3-architecture.md) |
| 4 | Security | [modules/phase-4-security.md](modules/phase-4-security.md) |
| 5 | Performance (with scale) | [modules/phase-5-performance.md](modules/phase-5-performance.md) |
| 6 | Error handling | [modules/phase-6-errors.md](modules/phase-6-errors.md) |
| 7 | Testability | [modules/phase-7-testing.md](modules/phase-7-testing.md) |
| 8 | Report | [modules/phase-8-report.md](modules/phase-8-report.md) |

**Severity guide**: [reference/severity-guide.md](reference/severity-guide.md)

## Quick Reference

**Invoke**: `/inspecting-changes [mode] [target]`

**Examples**:
- `/inspecting-changes deep` - full analysis
- `/inspecting-changes quick src/auth/` - quick check on path
- `/inspecting-changes medium HEAD~3..HEAD` - medium on commits
