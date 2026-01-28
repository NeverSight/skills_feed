---
name: clean-transient-comments
description: Use when the user asks to "clean transient comments", "remove temporary comments", or remove comments that describe past changes rather than documenting current code.
version: 1.1.0
---

Remove comments that read like commit messages or dev notes about refactors.

## Detection Heuristics

Flag comments that:
- Use past tense or temporal words ("now", "was", "used to", "moved", "changed", "updated", "fixed")
- Reference where code came from or went ("moved to X", "extracted from Y")
- Explain *that* something changed rather than *why* it exists

Examples to remove:
- `// This is now done via mixin`
- `// Moved to ItemFunctions.java`
- `// Updated to use new API`

## Preserve

- WHY explanations (rationale, edge cases, warnings)
- TODO/FIXME with ongoing relevance
- Ticket/issue references
- Domain logic documentation

## Process

### Phase 1: Scan

Scan provided paths, or default to src/, lib/, and common source files.

### Phase 2: Report

List files, specific comments planned for removal with context, and rationale.

**Wait for approval before removing.**

### Phase 3: Remove

After approval, delete flagged comments. Preserve all code structure and formatting.