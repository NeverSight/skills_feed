---
name: agent-dev-guardrails
description: Enforce disciplined agent development workflows with plan-first development, small-slice execution, specialized self-review roles, quality gates, and project setup. Use when starting a new project, setting up development conventions, wanting structured planning, or needing the agent to follow best practices for code quality, review, and validation.
---

# Agent Dev Guardrails

> Mental model: The agent is an extremely confident junior dev with amnesia. This skill provides guardrails, progressive context, and automated quality checks.

This skill enforces disciplined development workflows. Essentials are here in SKILL.md; detailed patterns are in `references/`, loaded only when needed.

## Non-Negotiables (Always Apply)

1. **Plan first, implement second.** For non-trivial changes: produce plan, risks, and task checklist before editing.
2. **Work in small slices.** Implement 1–2 checklist items at a time; pause for review/testing between slices.
3. **Never leave errors behind.** Run checks and fix failures before moving on.
4. **Be explicit about changes.** Every response that edits code must include:
   - Files changed (paths)
   - Why the change is correct
   - How it was validated (commands + outcome)
5. **If stuck for 30 minutes, stop.** Ask for narrower scope or propose different approach; don't thrash.

## Hook System

### Pre-Work Hook (Before Coding)

Before proposing code changes:

1. **Identify scope** — Small fix (no dev-docs) or large task (create dev-docs folder)
2. **State applicable skills** — Which domain skills apply (e.g., python-engineering, security)
3. **For non-trivial work:**
   - Ask clarifying questions (see [references/planning-protocol.md](references/planning-protocol.md))
   - Produce plan with phases + tasks + risks
   - Wait for plan acceptance before implementation

### Post-Work Hook (After Coding)

After every code edit:

1. **Run linting** — Use `ReadLints` on edited files
2. **Fix failures** — Do not leave errors behind
3. **Self-review** — Apply specialized roles (see [references/specialized-roles.md](references/specialized-roles.md))
4. **Summarize:**
   - Files changed
   - Commands run + outcomes
   - Next slice (if applicable)

## When to Read Which Reference

| Situation | Read |
|-----------|------|
| Need to plan or ask clarifying questions | [references/planning-protocol.md](references/planning-protocol.md) |
| Complex task (>30 min), need task folders | [references/dev-docs-system.md](references/dev-docs-system.md) |
| Self-reviewing code after edits | [references/specialized-roles.md](references/specialized-roles.md) |
| Setting up new project conventions | [references/project-setup.md](references/project-setup.md) |
| Checking Definition of Done | [references/quality-gates.md](references/quality-gates.md) |

## Quick Patterns

- **Token efficiency**: Request only the context you need; reference file paths and symbols instead of pasting large code blocks.
- **Planning**: Ask minimum context → produce plan with risks/tasks → wait for acceptance
- **Questions**: Ask "What are the tradeoffs? What breaks? What's missing?" not "Is this good?"
- **Slicing**: One slice = 1–2 checklist items; each slice ends with validation
- **Review**: Apply reviewer role personas (Architecture, Security, Test Engineer)
- **Done**: Code compiles, lint passes, edge cases handled, docs updated

## Quick Reference / Examples

| Task | Approach |
|------|----------|
| Start non-trivial work | Read [references/planning-protocol.md](references/planning-protocol.md), produce plan, wait for approval |
| Create task docs | Read [references/dev-docs-system.md](references/dev-docs-system.md), create `dev/active/<task-name>/` |
| Self-review code | Read [references/specialized-roles.md](references/specialized-roles.md), apply relevant personas |
| Set up new project | Run the setup script from the skill's `scripts/` folder (see [references/project-setup.md](references/project-setup.md) for path and options) |
| Check if slice is done | Read [references/quality-gates.md](references/quality-gates.md), verify all criteria |

**Pre-work check example:**
```
Scope: Large task (auth feature)
Skills: agent-dev-guardrails + python-engineering
Plan: [3 phases, 8 tasks, 2 risks identified]
Waiting for approval before implementation.
```

**Post-work summary example:**
```
Files changed: src/auth.py, tests/test_auth.py
Validation: ReadLints (0 errors), pytest (12 passed)
Self-review: ✓ Input validation, ✓ No hardcoded secrets, ⚠ Consider rate limiting
Next: Slice 2 (login endpoint)
```

## Workflow

1. **Starting any change** → Check scope, activate skills, follow pre-work hook
2. **Planning complex work** → Read [references/planning-protocol.md](references/planning-protocol.md), then [references/dev-docs-system.md](references/dev-docs-system.md)
3. **After every edit** → Follow post-work hook, apply [references/specialized-roles.md](references/specialized-roles.md)
4. **Setting up a project** → Run the setup script from the skill's `scripts/` folder; see [references/project-setup.md](references/project-setup.md)
5. **Marking work complete** → Verify against [references/quality-gates.md](references/quality-gates.md)

Keep SKILL.md lean; load reference files only when relevant to the task.
