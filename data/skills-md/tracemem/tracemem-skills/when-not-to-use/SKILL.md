---
name: when-not-to-use
description: Scenarios where TraceMem should not be used.
---

# Skill: TraceMem When NOT to Use

## Purpose
This skill helps agents determine when TraceMem is *unnecessary* or potentially harmful to performance/complexity. Not every line of code needs a decision envelope.

## When to Use
- When planning a task.
- During architectural decision making.

## When NOT to Use
- When the task is trivial, internal, or clearly outside the scope of "governance".

## Core Rules
- **No Side Effects? No Trace needed**: If you are just calculating pi or formatting a string, you don't need TraceMem.
- **Public Data Only? Low Risk**: If you are fetching public weather data, you *might* not need TraceMem (unless your organization requires tracking *all* external inputs). Default to using it if unsure, but know it's optional for non-sensitive public reads.
- **High Frequency**: If you need to write 10,000 records per second, TraceMem's HTTP/JSON-RPC overhead (and policy checks per write) might be too slow. TraceMem is for *decisions*, not bulk ETL.

## Correct Usage Pattern

### Scenario: "I need to summarize this text."
- **Action**: Purely computational.
- **TraceMem?**: **NO**.
- **Reason**: No side effects, no private data fetch (assuming text is already in memory).

### Scenario: "I need to delete a user."
- **Action**: Side effect, sensitive, irreversible.
- **TraceMem?**: **YES**.
- **Reason**: High risk, requires governance.

### Scenario: "I need to look up a timezone for a city."
- **Action**: Read public utility data.
- **TraceMem?**: **OPTIONAL / NO**.
- **Reason**: Low risk. But if "timezone" is from a proprietary customer database, then **YES**.

## Common Mistakes
- **Over-instrumentation**: Wrapping every single function call in a new Decision Envelope. Envelopes are for *logical units of work* (e.g., "Process Order"), not atomic instructions ("Add number").
- **Bulk Loading**: Trying to push millions of rows through `decision_write` one by one. (TraceMem connectors may support batching, but if not, this is inefficient).

## Safety Notes
- **Consistency**: If you skip TraceMem for "small" writes, you break the guarantee of the audit log. "Small" usage is the most dangerous exception. Be very strict: if it touches *governed* data, it *must* go through TraceMem. The "When NOT to use" applies primarily to *non-governed* or *computational* scopes.
