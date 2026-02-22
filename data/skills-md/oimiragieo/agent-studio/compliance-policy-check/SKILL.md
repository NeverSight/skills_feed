---
name: compliance-policy-check
description: Validate planned changes against local framework rules and policy guardrails before implementation or creation.
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

# Compliance Policy Check

## Overview

Evaluate a design/plan against framework policy and rule constraints before execution. Use this for regulated or high-risk changes.

## When to Use

- Before creator workflows for new artifacts
- Before HIGH/EPIC implementation phases
- During reflection when repeated policy violations are observed

## The Iron Law

```
DO NOT EXECUTE OR MODIFY CODE HERE.
ONLY ASSESS POLICY ALIGNMENT AND REPORT GAPS.
```

## Workflow

### Step 1: Gather Policy Context

- Read relevant files in `.claude/rules/`
- Read applicable workflow/agent constraints
- Read enforcement hook docs if needed

### Step 2: Evaluate Proposed Change

Assess against:

1. Creator guard and artifact lifecycle rules
2. Routing and specialist-first requirements
3. Security and quality gate requirements
4. Memory/search/token-saver policy expectations

### Step 3: Produce Decision

Return one policy decision:

- `PASS`: policy-aligned
- `CONDITIONAL`: allowed with required mitigations
- `FAIL`: not policy-compliant

Use this output shape:

```json
{
  "decision": "PASS|CONDITIONAL|FAIL",
  "policyFindings": ["..."],
  "requiredMitigations": [],
  "evidencePaths": ["..."],
  "recommendedNextStep": "..."
}
```

## Output Protocol

For `CONDITIONAL` and `FAIL`, include precise remediation tasks and ownership (agent type).

## Memory Protocol

Record recurring policy drift patterns in `.claude/context/memory/issues.md` and stabilized controls in `.claude/context/memory/decisions.md`.
