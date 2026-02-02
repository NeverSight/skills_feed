---
name: triaging-bugs
description: Use when a bug report is ambiguous or incomplete and you need a consistent way to assess severity, impact, reproducibility, and the next investigative step.
---

# Triaging Bugs

## Overview
Turn an unclear bug report into an actionable ticket by clarifying impact, reproducibility, scope, and ownership of next steps.

## When to Use
- The report lacks repro steps or expected vs. actual behavior
- Severity/priority is unclear or disputed
- You need to route the issue (frontend/backend/data/infra) with minimal back-and-forth

**When NOT to use**
- The bug is already well-scoped with reliable repro steps and clear fix owner

## Core Pattern
Classify first, then investigate:
- **Impact**: who is affected and how badly
- **Scope**: how widespread (all users vs. subset)
- **Repro**: steps, environment, frequency
- **Regressed?**: did it work before
- **Next step**: one concrete action to reduce uncertainty

## Quick Reference
Ask for (or infer) these fields:
- **Title**: short + specific (feature + symptom)
- **Environment**: prod/stage/local, browser/device, version/commit
- **Expected vs. Actual**
- **Repro steps** + **frequency**
- **Logs/IDs**: request IDs, user IDs, timestamps, screenshots
- **Severity** (impact) and **Priority** (when to do it)

## Implementation
1. Rewrite the report into Expected vs. Actual plus minimal repro.
2. Assign a severity (impact-based) and priority (schedule-based) with a one-line rationale.
3. Decide the next step:
   - Need repro → ask targeted questions and request artifacts
   - Repro exists → identify likely component boundary and assign owner
   - Production-only → request request IDs/timestamps and add logging/metrics task

## Common Mistakes
- **Conflating severity and priority**: high severity can still be low priority if rare and mitigated.
- **Asking vague questions**: “can you provide more details?” → ask for environment + exact steps + frequency.

