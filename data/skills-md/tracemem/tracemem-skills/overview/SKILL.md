---
name: overview
description: Overview of TraceMem core features, rules, and best practices.
---

# Skill: TraceMem Overview and Mental Model

## Purpose
This skill provides the foundational mental model for using TraceMem. It explains what TraceMem is, why an agent should use it, and how to think about its core primitives: Decision Envelopes and Decision Traces.

## When to Use
- When you are an AI agent performing actions that affect the real world (reading private data, changing state, spending money).
- When you need to prove *why* you did something to a human or auditor.
- When you encounter instructions to "use TraceMem", "open a decision", or "check policy".
- When you need to persist memory or context across different execution sessions (TraceMem is your long-term memory).

## When NOT to Use
- For scratchpad operations, intermediate chain-of-thought, or temporary variable storage that does not need audit.
- For purely internal data processing that has no external side effects and strictly public data.
- When low-latency (<10ms) direct database access is required (TraceMem adds governance overhead).

## Core Rules
- **TraceMem is the Courtroom**: You are the agent/defendant. You must present evidence (reads), cite laws (policies), and record your verdict (outcome).
- **All Actions Require a Decision**: You cannot read or write governed data without first opening a Decision Envelope.
- **You are Untrusted**: TraceMem assumes you (the agent) might hallucinate or be compromised. You must explicitly log your reasoning and prove your actions are safe.
- **Traces are Forever**: Everything you do in TraceMem is recorded in an immutable append-only trace. Do not store secrets or PII in purpose fields or context summaries.

## Correct Usage Pattern

1. **Start with a Decision**: Before doing any work, you open a "Decision Envelope". This is your workspace.
2. **Access Data via Products**: You do not use SQL or API calls directly. You ask TraceMem to read/write via "Data Products" (governed interfaces).
3. **Check Policies**: You check if your intended action is allowed by evaluating "Policies".
4. **Respect Approvals**: If a policy requires human approval, you pause and wait. You never bypass denials.
5. **Close the Decision**: When finished, you "commit" (if successful) or "aborted" (if stopped) or "failed" (if errored).

## Common Mistakes
- **Treating TraceMem as a database**: It is not a generic database; it is a governance log with attached storage.
- **Skipping the Decision Envelope**: Trying to read/write data without an active `decision_id` will fail.
- **Thinking you have authority**: You (the agent) never authorize actions. You *request* them. Policies and humans authorize them.

## Safety Notes
- **Immutable Record**: Never put sensitive credentials (API keys, passwords) into any TraceMem field (intent, purpose, context). These records are often readable by broad audiences for audit.
- **Governance Layer**: Do not try to bypass TraceMem to "save time". All bypassed actions are unauditable and effectively "rogue" behavior.
