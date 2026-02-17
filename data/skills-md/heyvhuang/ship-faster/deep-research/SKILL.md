---
name: deep-research
description: "Research a topic thoroughly in this repo and return a structured summary with file references. Use when you need to understand how something works, find patterns across modules, or audit implementations."
metadata:
  stage: tool
  tags:
    - research
context: fork
agent: Explore
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Deep Research (Explore)

Research $ARGUMENTS thoroughly.

## Required output

1. **Findings**: 3-10 bullets, each backed by specific file references
2. **Key code locations**: a short list of the most important paths to read next
3. **Open questions / unknowns**: what you could not confirm from the repo

## Method

- Start broad: use Glob to find likely modules.
- Then go deep: use Grep to locate exact identifiers and call sites.
- Read the top-ranked files and follow references until the flow is clear.
- Stop when you hit diminishing returns (two additional searches yield no new information).

## Rules

- Be evidence-driven: always cite file paths.
- Do not implement changes; this skill is for investigation only.
