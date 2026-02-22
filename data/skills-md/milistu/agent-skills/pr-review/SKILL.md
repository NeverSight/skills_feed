---
name: pr-review
description: Analyze and explain a pull request to help review it effectively
disable-model-invocation: true
---

# Review PR

## Overview
Analyze and explain a pull request to help me review it effectively.
Summarize what changed, why it changed, how the pieces fit together, and what risks or concerns I should pay attention to.

## Inputs I May Provide
- PR number
- Branch name
- Ticket description or acceptance criteria (optional)

## Behavior
- Start with a clear, concise explanation of the PR in plain language.
- Explain how the main files and changes relate to each other.
- Highlight intent and flow before implementation details.
- Be critical and skeptical, not polite.
- When explaining code, always include a direct reference (path or clickable code block) to the exact section so I can open it immediately without searching.

## What to Analyze
### Understanding
- What problem this PR is solving
- How the solution works at a high level
- Which parts are core vs supporting

### Risk & Correctness
- Potential bugs, edge cases, or regressions
- Missing or weak tests for changed behavior
- Assumptions that may not hold in production
- Rollback or failure concerns if things go wrong

### Architecture & Consistency
- Whether changes respect existing boundaries and patterns
- Signs of over-engineering or unnecessary abstraction
- Tight coupling, leaky abstractions, or responsibility mixing

### Review Guidance
- Call out files or areas that deserve closer inspection
- Point out changes that depend on each other
- Flag parts that are harder to reason about or easy to get wrong

### UI / Functional Changes
- Explicitly state if this PR likely needs local testing
- Call out flows or scenarios I should manually verify

## Guardrails
- Do not approve or reject the PR.
- Do not repeat the PR description or file list.
- Do not invent missing context—state assumptions when necessary.
- Adapt depth and verbosity to my request (short summary vs deep review).
