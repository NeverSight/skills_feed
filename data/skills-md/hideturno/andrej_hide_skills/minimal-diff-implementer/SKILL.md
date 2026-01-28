---
name: minimal-diff-implementer
description: Implement the smallest safe change and avoid bloat; use for most coding tasks to prevent overengineering, unrelated edits, or destructive refactors.
---

# Minimal Diff Implementer

## Quick start

- Touch the fewest files possible.
- Preserve existing comments and structure.
- Avoid refactors unless explicitly requested.

## Procedure

1) Find the narrowest place to implement the change.
2) Prefer local edits over new abstractions.
3) Keep APIs stable unless required.
4) Do not delete or rewrite code you do not fully understand.
5) If a refactor seems needed, ask first.

## Output format

- Changes: short list of files edited and why.
- Notes: any tradeoffs or limitations.

## Guardrails

- Do not remove comments or formatting as collateral.
- Do not expand scope to "clean up".
- If code grows, justify why the growth is required.
