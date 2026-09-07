---
name: diagnose
description: Use when diagnosing hard bugs, intermittent flakes, unexplained test failures, or performance regressions before proposing mutations.
---

# diagnose — Root-Cause Isolation & Diagnostic Engine

Isolate root causes of complex bugs, intermittent flakes, and regressions through tight feedback loops, load-bearing minimization, and falsifiable hypotheses before proposing code modifications.

## Operating Invariants

- **Scope Discipline**: Focus exclusively on isolating and resolving the specific reported defect. Forbid unsolicited refactoring, styling, or feature alterations outside the defect's blast radius.
- **Pre-Mutation Gate**: Isolate the root cause and present verified findings in Lean Delivery format. Forbid modifying codebase implementation files or permanent tests without affirmative human authorization.
- **Isolated Scratchpad**: Write all temporary reproduction scripts, throwaway harnesses, and fixture traces strictly inside `.agents/scratch/`. Forbid creating temporary test files in repository root or source directories.
- **Clean Room Tagging**: Tag all temporary diagnostic logging and probes with an isolated unique prefix (`[DEBUG-<hex>]`). Forbid leaving debug probes in working tree upon completion.
- **Tight Signal Requirement**: Mandate a single deterministic command that executes in seconds and asserts the exact user symptom. Forbid proposing code patches based solely on code inspection.
- **Redaction Guardrail**: Replace all secrets, tokens, API keys, credentials, and sensitive environment payloads with `<REDACTED>`.
- **Circuit Breaker on Verification Failure**: If the atomic fix fails to verify GREEN, stop execution immediately, report stderr, and ask the user whether to revert or keep debugging.

## Domain Engine & Standards

### 1. Diagnostic Guardrails (When NOT to Touch)
- **No Speculative Harnesses**: If the failure is an unambiguous syntax error, typo, or deterministic trace with verified root cause, bypass throwaway harnesses and proceed directly to Step 3 (Fast-Path Triage).
- **No Unanchored Scratch Files**: Confine all temporary test scripts, mock harnesses, and curl scripts strictly to `.agents/scratch/` (e.g. `.agents/scratch/repro.<ext>`). Never touch or pollute the host codebase with disposable test files.
- **No Theory Without Signal**: Forbid formulating hypotheses or inspecting implementation logic until a reproducible command fails RED.
- **No Shallow Tests**: If no natural architectural seam exists, report the architectural deficiency plainly rather than authoring shallow mocks that yield false confidence.

### 2. Feedback Loop Hierarchy (Tightest to Loosest)
1. *Automated Test*: Unit, integration, or e2e test exercising the failure at the call site.
2. *Direct Invocation*: CLI or HTTP curl command against running process with diffed output.
3. *Isolated Harness*: Minimal throwaway script in `.agents/scratch/` exercising the faulty function in isolation with mocked external I/O.
4. *Trace Replay*: Replaying saved network payload, event log, or HAR file from `.agents/scratch/`.
5. *Bisection Harness*: Automated check command passed to `git bisect run`.
6. *Human-In-The-Loop*: Interactive terminal script copied to `.agents/scratch/hitl-loop.sh` and executed.

### 3. Flaky & Non-Deterministic Strategies
- Elevate reproduction rate: loop execution $N$ times, inject concurrency, narrow timing windows, or pin random seeds until the failure rate is actionable.

### 4. Falsifiable Hypothesis Rubric
- Formulate 3–5 ranked hypotheses before probing.
- State an explicit testable prediction for each:
  `"If <Cause X>, then <Intervention Y> causes <Observed Result Z>."`

## Execution Protocol

### Step 1: Feedback Loop Construction & Minimization
1. Construct the tightest viable command asserting the user's exact reported symptom (using existing tests, direct invocation, or an isolated harness in `.agents/scratch/`).
2. Execute the command to verify that it turns RED (fails).
3. Minimise inputs, config, and steps until every remaining element is load-bearing (removing any element makes the test turn green).

### Step 2: Hypothesis Formulation & Probing
1. Formulate 3–5 ranked falsifiable hypotheses according to the rubric.
2. Probe hypotheses one variable at a time using debugger inspection or tagged logs (`[DEBUG-<hex>]`).
3. Isolate the confirmed root cause and verify that removing the trigger resolves the red signal.

### Step 3: Diagnostic Staging & Pre-Mutation Gate
1. Present the diagnosis in Lean Delivery format:
   ```text
   ### Root-Cause Diagnosis
   - **Confirmed Cause**: <Exact mechanism and offending symbol/file>
   - **Verification Proof**: `<single command>` producing RED signal, confirmed by probe `<tag>`.
   - **Architectural Seam**: <Seam available for regression test | Architectural deficiency noted>

   ### Proposed Changeset
   📁 <directory>/
   └── 📄 <target_file>
       └── [UPDATE] <Atomic fix summary>
   ```
2. Offer execution options: approve applying atomic fix with regression test, hand off proposed changeset to `/forge`, or inspect alternate hypotheses.
3. Forbid modifying codebase source files within this turn.
4. Halt turn immediately and wait for affirmative human authorization.

### Step 4: Atomic Fix, Verification & Cleanup
1. Upon receiving approval, author the regression test at the confirmed seam (verify RED).
2. Apply the atomic fix to codebase files (verify GREEN).
3. Apply the Circuit Breaker: If the fix fails to verify GREEN, stop execution immediately, report stderr, and ask the user whether to revert or keep debugging.
4. Re-run the Phase 1 feedback loop against the original scenario.
5. Remove all temporary `[DEBUG-<hex>]` instrumentation, and delete temporary artifacts in `.agents/scratch/` (verify clean tree via `grep` and `git status`).
6. Report verified resolution and provide git commit message documenting the confirmed root cause and hypothesis.
