---
name: deslop-code
description: Clean up AI-generated code changes by reviewing diffs against main and removing stylistic or structural artifacts (over-commenting, unnecessary defensive checks, try/catch noise, any-casts, inconsistent style). Use when asked to “remove AI code slop,” “humanize” changes, or align a branch’s edits with existing codebase conventions.
---

# Deslop Code

## Overview

Strip AI-generated artifacts from a branch by comparing against main and aligning edits with local conventions and surrounding code style.

## Workflow

1. Establish baseline
- Use git diff against main to identify AI-introduced changes.
- Review surrounding context in each file to understand local conventions.

2. Remove slop patterns
- Delete comments that read like explanations, narrations, or redundant restatements of code.
- Remove defensive checks or try/catch blocks that are inconsistent with trusted code paths or nearby style.
- Replace any-casts or similar type escapes with proper typing or remove them if unnecessary.
- Normalize style to match the file (naming, ordering, error handling, control flow).

3. Verify consistency
- Ensure behavior remains unchanged unless removal requires a small refactor to restore intended behavior.
- Keep changes minimal and localized; avoid refactors not needed for cleanup.

4. Report
- End response with a 1–3 sentence summary of what changed.
