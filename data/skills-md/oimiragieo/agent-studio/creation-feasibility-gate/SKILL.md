---
name: creation-feasibility-gate
description: Validate whether a proposed new artifact is feasible in the current stack before creator workflows run.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Glob, Grep, Skill]
error_handling: graceful
streaming: supported
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Creation Feasibility Gate

## Overview

Run a fast preflight feasibility check before creating a new agent/skill/workflow/hook/template/schema. This prevents low-value or impossible creator runs.

## When to Use

- Phase 0.5 dynamic creation flow
- User asks for net-new capability
- Reflection/evolution recommends artifact creation

## The Iron Law

```
DO NOT CREATE ARTIFACTS IN THIS SKILL.
ONLY RETURN PASS/BLOCK/WARN WITH EVIDENCE.
```

## Workflow

### Step 1: Resolve Target

- Identify proposed artifact type and name
- Identify expected runtime/tool dependencies
- Identify expected owner agents

### Step 2: Preflight Checks

Run these checks with concrete evidence:

1. **Existence/duplication check**
   - Catalogs + registry + artifact paths
2. **Stack compatibility check**
   - Required tooling/runtime present in current project conventions
3. **Integration readiness check**
   - Can it be routed/discovered/assigned after creation?
4. **Security/creator boundary check**
   - Ensure creator path and governance can be satisfied

### Step 3: Decision

Return one status:

- `PASS`: creation is feasible now
- `WARN`: feasible with clear caveats
- `BLOCK`: not feasible; must resolve blockers first

Use this output shape:

```json
{
  "status": "PASS|WARN|BLOCK",
  "artifactType": "agent|skill|workflow|hook|template|schema",
  "artifactName": "example-name",
  "evidence": ["..."],
  "blockers": [],
  "nextActions": ["..."]
}
```

## Output Protocol

If `BLOCK`, include concrete remediation tasks and recommended target agents.
If `PASS` or `WARN`, include exact creator skill chain to run next.

## Memory Protocol

Record feasibility patterns and recurring blockers to `.claude/context/memory/learnings.md`.
