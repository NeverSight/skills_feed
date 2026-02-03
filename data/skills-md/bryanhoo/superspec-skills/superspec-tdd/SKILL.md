---
name: superspec-tdd
description: Use when executing superspec tasks to enforce strict TDD for behavior changes and allow NON-TDD exceptions only for doc/config/generated/format-only work with mechanical verification.
user-invocable: false
---

# Superspec TDD (Mechanical Enforcement)

## Iron Law
NO PRODUCTION CODE BEFORE A VERIFIED FAILING TEST.

## Task Tags

- [TDD][RED]
- [TDD][VERIFY_RED]
- [TDD][GREEN]
- [TDD][VERIFY_GREEN]
- [TDD][REFACTOR]
- [NON-TDD][DO]
- [NON-TDD][VERIFY]

## Allowed [NON-TDD] Scope (ONLY)

- docs-only
- config-only (no behavior change)
- generated outputs
- formatting/renaming only

## Core Principle

If you didn't watch the test fail, you don't know if it tests the right thing.

## Gates (non-negotiable)

- A task line with `[TDD][GREEN]` MUST NOT be executed unless its corresponding `[TDD][VERIFY_RED]` task for the same Scenario is completed.
- A `[NON-TDD][DO]` task MUST NOT be executed unless there is a corresponding `[NON-TDD][VERIFY]` task line.

## VERIFY_RED Decision Table (zero-decision)

A `[TDD][VERIFY_RED]` task MUST result in exactly one of these outcomes:

- PASS: STOP. The test is not proving missing behavior. Fix the test/spec/Test Obligation. Do not write production code.
- ERROR (test runner/config/typo): STOP. Fix the error and re-run until it FAILs for the expected reason.
- FAIL: Continue only if output contains the required `Expected (RED)` substring.

## VERIFY_GREEN Decision Table (zero-decision)

A `[TDD][VERIFY_GREEN]` task MUST result in exactly one of these outcomes:

- PASS: Continue.
- FAIL: Fix production code (not the test).
- Other tests failing: STOP and fix until all relevant tests are green.

## REFACTOR Rule

- `[TDD][REFACTOR]` is allowed only after `[TDD][VERIFY_GREEN]`.
- After refactor, re-run the same Verify Command and confirm it still passes.

## [NON-TDD] Verification Rule

- A `[NON-TDD][VERIFY]` step MUST be mechanical (command output / file existence / `openspec validate --all --json`), not a manual check.
- If you cannot express verification as a command or deterministic check, this is not [NON-TDD].

## When Stuck (zero-decision)

- Don't know how to test: the contract is unclear. Update `specs/**/spec.md` Test Obligation and/or `design.md` Test Commands.
- Test setup is huge: simplify the contract or split the Scenario.
- Must mock everything: code is too coupled. Stop and revise design boundaries.

## Strict Prohibitions

- NEVER test mock behavior.
- NEVER add test-only methods to production code.
- NEVER mock without understanding dependency side effects.

Reference: `references/testing-anti-patterns.md`
