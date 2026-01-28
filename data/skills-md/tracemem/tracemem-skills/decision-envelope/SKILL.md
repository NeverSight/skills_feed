---
name: decision-envelope
description: Using the decision envelope pattern for structured thinking.
---

# Skill: TraceMem Decision Envelopes

## Purpose
This skill teaches how to correctly manage the lifecycle of a Decision Envelope. The Decision Envelope is the mandatory boundary for all governed operations in TraceMem.

## When to Use
- Every time you intend to perform a task that requires reading private data or affecting system state.
- At the very beginning of a new task or workflow.
- When an existing decision has been closed and you need to perform follow-up actions (start a new decision).

## When NOT to Use
- Do not nest decisions (e.g., do not open a decision if you are already inside one, unless explicitly starting a sub-task that requires independent audit).
- Do not open a decision for purely computational tasks (e.g., formatting text) that require no external data or side effects.

## Core Rules
- **One Decision, One Lifecycle**: A decision must be explicitly created (`open`), operated upon, and then explicitly closed (`commit` or `rollback`).
- **Mandatory Intents**: You must provide a structured `intent` string (e.g., `customer.onboarding.verification`) that describes *why* this decision exists.
- **Mandatory Automation Mode**: You must certify the `automation_mode` (e.g., `propose`, `approve`, `autonomous`).
- **Close Required**: A decision left open is a "zombie" decision. You *must* ensure `decision_close` is called in `finally` blocks or error handlers.

## Correct Usage Pattern

1. **Create the Envelope**:
   Call `decision_create` with:
   - `intent`: A dot-separated string (e.g., `financial.report.generate`).
   - `automation_mode`: One of `propose`, `approve`, `override`, `autonomous`.
   - `actor`: Your agent identity.
   
   *Result*: You receive a `decision_id`.

2. **Operate within the Envelope**:
   Perform all `decision_read`, `decision_evaluate`, and `decision_write` calls using the `decision_id`.

3. **Close the Envelope**:
   - If successful: Call `decision_close` with `action: "commit"`.
   - If error/aborted: Call `decision_close` with `action: "rollback"` (or `abort` if strictly tracking abandonment).

   *Note*: Writes are only permanently applied when the decision is committed (depending on system configuration, but logically, the decision is not "done" until committed).

## Common Mistakes
- **Forgetting to close**: Leaving decisions open forever consumes resources and confuses auditors.
- **Vague Intents**: Using generic intents like `task.do` or `agent.act`. Use specific, domain-relevant intents (`user.password.reset`, `invoice.payment.process`).
- **Wrong Automation Mode**: Claiming `autonomous` when the task requires human oversight, or `propose` when you intend to execute immediately.

## Safety Notes
- **Audited Lifecycle**: The timestamps of open and close are recorded. Long-running open decisions may trigger alerts.
- **Fail Closed**: If your process crashes, the decision remains open (and potentially locks resources). Always wrap your workflow in a try/finally block to ensure `decision_close` is attempted.
