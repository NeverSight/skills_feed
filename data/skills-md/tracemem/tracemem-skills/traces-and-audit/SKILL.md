---
name: traces-and-audit
description: Auditing memory traces and debugging.
---

# Skill: TraceMem Traces and Audit

## Purpose
This skill explains the concept of the Decision Trace as an artifact. Understanding this helps you write better "evidence" into the system.

## When to Use
- When you need to understand *what* TraceMem is actually recording.
- When generating reports or answering questions about past actions ("Why did you do that?").

## When NOT to Use
- You generally do not "use" this skill to execute actions, but to inform *how* you execute them.

## Core Rules
- **The Trace is the Truth**: If it's not in the trace, it didn't happen (legally/audit-wise).
- **Append-Only**: You cannot go back and fix history.
- **Complete Picture**: A trace includes your ID, the time, the policy version, the data schema version, and the exact outcomes.

## Correct Usage Pattern

1. **Design for Readability**:
   When running a decision, imagine a human reading the trace 6 months later.
   - "Why did this agent delete this user?"
   - Look at the `intent`, look at the `context` you added, look at the `policy` result.
   - If the trace answers the question, you succeeded.

2. **Linking**:
   If you chain decisions (one decision triggers another workflow), reference the parent `decision_id` in the child's `metadata` or `context`.

## Common Mistakes
- **Phantom Actions**: Doing side effects (like calling an external API) *without* recording it in TraceMem or via a Data Product. This creates "dark matter" — actions that have no record.
- **Incomplete Evidence**: Reading data via a side-channel (not a Data Product) and then acting on it. The trace will show the action but not the data that justified it.

## Safety Notes
- **Exoneration**: A good trace protects *you* (the agent). If a policy was wrong, the trace proves you followed the policy correctly. If data was bad, the trace proves you acted on the bad data you were given.
