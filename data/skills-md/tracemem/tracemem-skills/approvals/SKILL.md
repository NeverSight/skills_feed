---
name: approvals
description: Guidelines for seeking user approval for sensitive actions.
---

# Skill: TraceMem Approvals and Human-in-the-Loop

## Purpose
This skill teaches how to handle scenarios where an action requires human approval. This is a core feature of TraceMem's governance model.

## When to Use
- When `decision_evaluate` returns `outcome: "requires_exception"`.
- When your automation mode is `approve` (meaning you *expect* to wait for approval).
- When you detect a high-risk situation and voluntarily want to ask for confirmation.

## When NOT to Use
- Do not ask for approval if the policy `deny`s the action outright (you cannot bypass a deny).
- Do not ask for approval for trivial read-only tasks that don't need it.

## Core Rules
- **Request and Wait**: Approval is an asynchronous process. You request it, then you poll (wait) for the result.
- **Do Not Proceed Unapproved**: If you receive a `rejected` status, you must abort the operation. Proceeding is a violation.
- **Provide Rationale**: When requesting approval, explain *why* the exception is needed. This helps the human decider.

## Correct Usage Pattern

1. **Request Approval**:
   Call `decision_request_approval` with:
   - `decision_id`: Current decision.
   - `title`: Short summary (e.g., "High Value Refund").
   - `message`: Detailed explanation ("Refund of $500 exceeds $100 auto-limit").
   - `require_rationale`: `true` (usually good practice).
   - `expires_in_seconds`: e.g., 3600 (1 hour).

   *Result*: You get an `approval_id` and status `requested`.

2. **Poll for Concluson**:
   Loop and call `decision_get` periodically (e.g., every 5-10 seconds).
   Check `status` field.
   - If `open` or `needs_approval`: Continue waiting.
   - If `approved`: Break loop and proceed.
   - If `rejected`: Break loop and handle rejection (abort/rollback).

3. **Proceed**:
   Once `approved`, you can retry the operation (e.g., the write) that was previously blocked or required the exception. The policy check should now pass (or you can proceed if the approval *was* the gate).

## Common Mistakes
- **Busy Waiting**: Polling too fast (e.g., every 10ms) will hit rate limits. Use reasonable sleep (5-10s).
- **Ignoring Rejection**: Treating `rejected` as a "soft" error and trying again immediately.
- **Timeout Handling**: Waiting forever. Set a max wait time (e.g., 5 minutes) and abort if no human responds.

## Safety Notes
- **Notification Channels**: The human is notified via configured channels (Slack, Email). You don't need to send the email yourself; TraceMem handles the routing.
- **Context**: The approver sees the *Context* and *Reads* you performed. Ensure you added enough context *before* requesting approval so they have the full picture.
