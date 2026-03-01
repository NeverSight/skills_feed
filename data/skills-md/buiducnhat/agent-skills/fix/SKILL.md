---
name: fix
description: Diagnose and fix bugs with root-cause analysis and verification. Use when you have a concrete issue report, failing behavior, runtime error, or test regression that should be resolved safely. For ambiguous, high-risk, or broad-scope issues, stop and route to write-plan first.
---

# Fix

## Overview

Use this skill to resolve bugs through a structured flow:

1. Intake a clear bug report
2. Reproduce and isolate root cause
3. Apply the smallest safe fix
4. Verify with focused and project-wide checks
5. Document what changed and why

Prefer correctness and safety over speed. Do not guess.

## Workflow

### Step 1: Bug Report Intake

Collect or confirm the minimum required issue context before changing code.

Required intake fields:

- **Title:** short bug summary
- **Expected behavior:** what should happen
- **Actual behavior:** what happens now
- **Reproduction steps:** exact steps/inputs
- **Evidence:** logs, stack trace, screenshots, failing test output
- **Environment:** branch, OS/runtime, app version/commit (if available)
- **Impact:** severity and affected users/areas

If key fields are missing, ask targeted follow-up questions first.

### Step 2: Reproduce and Diagnose

1. Reproduce the issue consistently.
2. Locate the failure point (file, function, line range, or subsystem).
3. Trace data/control flow to identify the **root cause**.
4. Define a fix hypothesis and confirm it explains the observed behavior.

Guidelines:

- Read surrounding code, not just the failing line.
- Prefer root-cause fixes, not symptom patches.
- Add temporary diagnostics/logging only if needed to isolate behavior.
- Remove or clean up temporary diagnostics after verification.

### Step 3: Complexity Gate (Go / No-Go)

Classify the fix before implementation:

#### Simple Fix (proceed in this skill)

All or most are true:

- Clear root cause
- Localized change (small surface area)
- Low architectural risk
- Limited file impact
- Verification path is straightforward

#### Complex/Risky Fix (stop and route to `write-plan`)

Any are true:

- Root cause still unclear
- Cross-cutting or architectural changes needed
- Significant refactor or migration involved
- High regression risk
- Multi-phase rollout required
- External dependency or infra uncertainty

If complex, stop and recommend creating a plan with `write-plan`.

### Step 4: Implement the Fix (Simple Path)

1. State a brief fix plan in 1-3 bullets.
2. Apply minimal, targeted code changes.
3. Keep behavior changes explicit and scoped.
4. Add/adjust tests to prevent regression when applicable.

Implementation rules:

- Avoid unrelated refactors.
- Preserve existing conventions and project standards.
- Keep changes idempotent and safe to re-run where relevant.

### Step 5: Verify

Run verification in increasing scope:

1. **Focused checks** for the affected module/feature
2. **Regression checks** for nearby behavior
3. **Project checks** as relevant (lint/typecheck/tests/build)

Bug is fixed only when:

- Reproduction no longer fails
- Expected behavior is confirmed
- No critical regressions introduced

If verification fails unexpectedly, stop and reassess diagnosis.

### Step 6: Complete and Report

Provide a concise completion report:

- **Root cause**
- **What changed**
- **Why this fix works**
- **Verification performed and results**
- **Residual risks / follow-ups** (if any)

If architecture, codebase structure, or product behavior changed materially, update documentation artifacts (typically `docs/project-pdr.md`, `docs/codebase.md`, `docs/architecture.md`) via the `docs` workflow.

## Rules

- **No guessing:** ask when critical context is missing.
- **Root cause first:** never ship symptom-only patches knowingly.
- **Smallest safe change:** minimize blast radius.
- **Verify before done:** no fix is complete without checks.
- **Escalate complexity:** use `write-plan` for risky/broad changes.
- **Follow project docs:** align with `docs/` guidance, especially `docs/code-standard.md`.

## Optional Bug Report Template

Use this template when the user provides an incomplete issue report:

- Title:
- Expected behavior:
- Actual behavior:
- Reproduction steps:
- Error logs/stack trace:
- Environment:
- Impact/severity:
- Additional context:
