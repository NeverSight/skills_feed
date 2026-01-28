---
name: notes-and-context
description: Managing context and notes within the memory system.
---

# Skill: TraceMem Notes and Context

## Purpose
This skill teaches how to "show your work" by adding context and reasoning to the decision trace. This makes the agent's internal logic visible to auditors and humans.

## When to Use
- Before making a significant decision (e.g., "I decided to approve this because X").
- When model confidence is relevant ("Confidence: 0.85").
- To summarize findings from multiple reads ("Found 3 matching records, selecting the most recent").

## When NOT to Use
- Do not use as a general logging facility for debugging (use your standard logging for that).
- Do not dump raw massive JSON payloads (summarize them).

## Core Rules
- **Show Your Logic**: If you make a choice, record *why*.
- **No Secrets**: Never put API keys, passwords, or highly sensitive PII in the context summary.
- **Structured Data**: Use the `payload` field for machine-readable context (e.g., scores, counts), and `summary` for human-readable text.

## Correct Usage Pattern

1. **Add Context**:
   Call `decision_add_context` with:
   - `decision_id`: Current decision.
   - `summary`: A clear sentence (e.g., "Selected plan B due to cost constraints.").
   - `payload`: Optional JSON object with details (e.g., `{"plan_a_cost": 100, "plan_b_cost": 50}`).

2. **Timing**:
   Add context *as you go*. Do not wait until the end to dump everything. A chronological trace is easier to read.

## Common Mistakes
- **Empty Context**: Making complex decisions without logging any context makes the trace hard to audit ("Blue box effect").
- **Redundant Context**: Logging "I am about to read data" (the read event itself logs this). Log *reasoning*, not *actions*.
- **Over-verbosity**: Logging every single token or intermediate thought.

## Safety Notes
- **Privacy**: Context strings are often visible in dashboards. Assume your manager can read them.
- **Immutable**: Once added, context cannot be edited.
