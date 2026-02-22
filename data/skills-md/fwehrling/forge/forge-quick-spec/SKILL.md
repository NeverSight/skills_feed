---
name: forge-quick-spec
description: >
  FORGE Quick Track — Spec + direct implementation for bug fixes and small changes.
  Usage: /forge-quick-spec "change description"
---

# /forge-quick-spec — FORGE Quick Track

Fast-track mode for bug fixes and small changes (<1 day).
Skips the planning and architecture phases.

## French Language Rule

All content generated in French MUST use proper accents (é, è, ê, à, ù, ç, ô, î, etc.), follow French grammar rules (agreements, conjugations), and use correct spelling.

## Workflow

1. Analyze the request
2. Generate a quick spec (in-memory, no artifact)
3. Write tests (unit + functional for the fix)
4. Implement the change
5. Validate (lint + typecheck + tests)
6. Propose the commit
