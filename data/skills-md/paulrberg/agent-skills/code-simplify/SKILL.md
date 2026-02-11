---
name: code-simplify
description: Simplify and refactor existing code for readability and maintainability without changing behavior. Use when the user asks to "simplify code", "clean up code", "refactor for clarity", "reduce complexity", "improve readability", "make this easier to maintain", or asks to polish recently modified code.
---

# Code Simplify

## Objective

Simplify code while preserving behavior, public contracts, and side effects. Favor explicit code and local clarity over clever or compressed constructs.

## Operating Rules

- Preserve runtime behavior exactly. Keep inputs, outputs, side effects, and error behavior stable.
- Prefer project conventions over personal preferences. Infer conventions from existing code, linters, formatters, and tests.
- Limit scope to user-requested files or recently modified code unless explicitly asked to broaden.
- Make small, reversible edits. Avoid broad rewrites when targeted simplifications solve the problem.
- Call out uncertainty immediately when behavior may change.

## Workflow

### 1) Determine Scope

- Verify repository context: `git rev-parse --git-dir`.
- Identify candidate files:
  - If the user provides a file list, use it.
  - Otherwise start from `git diff --name-only --diff-filter=ACMR`.
- Exclude generated or low-signal files unless explicitly requested:
  - lockfiles, minified bundles, build outputs, vendored code.
- If no target files are found, ask for explicit scope.

### 2) Build a Behavior Baseline

- Read surrounding context, not only changed lines.
- Identify invariants that must not change:
  - function signatures and exported APIs
  - state transitions and side effects
  - persistence/network behavior
  - user-facing messages and error semantics where externally relied on
- Note available verification commands (lint, tests, typecheck).

### 3) Apply Simplification Passes (in this order)

1. Control flow:
   - Flatten deep nesting with guard clauses and early returns.
   - Replace nested ternaries with clearer conditionals.
2. Naming and intent:
   - Rename ambiguous identifiers when local context supports safe renaming.
   - Separate mixed concerns into small helpers with intent-revealing names.
3. Duplication:
   - Remove obvious duplication.
   - Abstract only when at least two real call sites benefit and the abstraction reduces cognitive load.
4. Data shaping:
   - Break dense transform chains into named intermediate steps when readability improves.
   - Keep hot-path performance characteristics stable unless improvement is explicit and measured.
5. Type and contract clarity:
   - Add or tighten type annotations when they improve readability and safety without forcing broad churn.
   - Preserve external interfaces unless asked to change them.

### 4) Enforce Safety Constraints

- Do not convert sync APIs to async (or reverse) unless explicitly requested.
- Do not alter error propagation strategy unless behavior remains equivalent and verified.
- Do not remove logging, telemetry, guards, or retries that encode operational intent.
- Do not collapse domain-specific steps into generic helpers that hide intent.

### 5) Verify

- Run the narrowest useful checks first:
  - formatter/lint on touched files
  - targeted tests related to touched modules
  - typecheck when relevant
- If fast targeted checks pass, run broader checks only when risk warrants it.
- If checks cannot run, state what was skipped and why.

### 6) Report

Provide:
1. Scope touched (files/functions)
2. Key simplifications with concise rationale
3. Verification commands run and outcomes
4. Residual risks or assumptions

## Simplification Heuristics

- Prefer explicit local variables over nested inline expressions when it reduces cognitive load.
- Prefer one clear branch per condition over compact but ambiguous condition trees.
- Keep function length manageable, but do not split purely for line count.
- Keep comments that explain intent, invariants, or non-obvious constraints.
- Remove comments that restate obvious code behavior.
- Optimize for the next maintainer's comprehension time, not minimum character count.

## Anti-Patterns

- Do not perform speculative architecture rewrites.
- Do not introduce framework-wide patterns while simplifying a small local change.
- Do not replace understandable duplication with opaque utility layers.
- Do not bundle unrelated cleanups into one patch.

## Stop Conditions

- Stop and ask for direction when:
  - simplification requires changing public API/contracts
  - behavior parity cannot be confidently verified
  - the code appears intentionally complex due to domain constraints
  - the requested scope implies a larger redesign rather than simplification

## Output Contract

When presenting simplification results:

1. Show the exact files and regions changed.
2. Explain each meaningful change in one sentence focused on readability/maintainability gain.
3. Confirm behavior-preservation assumptions explicitly.
4. Summarize verification performed (or clearly state omissions).
