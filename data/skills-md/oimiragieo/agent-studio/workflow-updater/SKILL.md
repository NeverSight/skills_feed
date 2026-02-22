---
name: workflow-updater
description: Refresh existing workflows with phase-gate regression checks and idempotency validation.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Glob, Grep, Bash, Skill, MemoryRecord, WebSearch, WebFetch]
args: '--workflow <name-or-path> [--trigger reflection|evolve|manual]'
error_handling: graceful
streaming: supported
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Workflow Updater

Refresh existing workflows safely with explicit gate validation, transition integrity checks, and idempotency regression tests.

## Iron Law

No workflow refresh without proving gate correctness and idempotent phase progression.

## Research Gate (MANDATORY)

Minimum 2 Exa queries before proposing any workflow changes:

```javascript
Skill({ skill: 'research-synthesis' });
```

## Risk Scoring Model

- `high`: gate changes (phase transitions, blocking conditions, agent selection logic)
- `medium`: step reordering, new optional phases, documentation of existing behavior
- `low`: wording clarifications, examples, non-gate documentation

For `high` risk changes, require explicit diff review and confirmation before apply mode.

## Core Steps

1. Resolve existing workflow file.
2. **Research Gate**: Run at least 2 Exa queries via `research-synthesis` (MANDATORY).
3. **Companion Validation**: Check companion artifacts are present and aligned.
4. Build RED tests for gate regressions and duplicate transition handling.
5. Apply minimal workflow updates.
6. Verify workflow validation + integration docs + registry references.
7. Record learnings, decisions, and issues in memory.

## Companion Validation

Before modifying any workflow, validate companion artifacts:

```javascript
const { checkCompanions } = require('.claude/lib/creators/companion-check.cjs');
const result = checkCompanions('workflow', workflowName, { projectRoot });
```

## Memory + Search

Use existing memory/search stack for evidence and record updated workflow learnings in memory files.
