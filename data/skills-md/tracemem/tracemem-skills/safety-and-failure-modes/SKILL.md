---
name: safety-and-failure-modes
description: Understanding safety constraints and handling failures.
---

# Skill: TraceMem Safety and Failure Modes

## Purpose
This skill teaches how to handle errors, timeouts, and failures gracefully within the TraceMem ecosystem.

## When to Use
- When writing `try/catch` blocks around your decision logic.
- When handling network errors or policy denials.
- When ensuring your agent is robust.

## When NOT to Use
- Do not use these patterns to swallow critical errors silently.

## Core Rules
- **Fail Closed**: If something goes wrong, the default safe state is "stop and close".
- **Rollback on Error**: If an exception occurs, you MUST catch it and call `decision_close(action="rollback")`.
- **Idempotency**: Use idempotency keys for writes to safely retry them after network blips.

## Correct Usage Pattern

1. **Wrapper Pattern**:
   ```python
   decision_id = None
   try:
      # 1. Create
      decision_id = create(...)
      # 2. Work
      do_work(...)
      # 3. Commit
      close(decision_id, "commit")
   except PolicyDenied:
      # 4a. Handle Denial
      close(decision_id, "rollback") # or abort
   except Exception:
      # 4b. Handle Crash
      if decision_id:
         close(decision_id, "rollback")
      raise
   ```

2. **Handling Timeouts (408/504)**:
   If a request times out, you don't know if it succeeded.
   - For reads: Safe to retry.
   - For writes: Safe to retry ONLY if you provided an `idempotency_key`. If not, you must check state or abort.

3. **Handling Rate Limits (429)**:
   Respect the `Retry-After` header. Wait and retry.

## Common Mistakes
- **Zombie Decisions**: Crashing without a `finally` block or error handler that closes the decision.
- ** Infinite Retries**: Retrying a `deny` result. Policy denials are permanent for that specific context; retrying won't change the policy (unless you change input or get approval).

## Safety Notes
- **Audit of Failure**: TraceMem records "failed" and "aborted" traces too. These are valuable for debugging. Don't be afraid to abort; it's a safety feature.
