---
name: writing-release-notes
description: Use when changes are ready to ship and you need to communicate what changed, who it affects, and any required actions without exposing internal-only details.
---

# Writing Release Notes

## Overview
Summarize shipped changes in a way that is accurate, scannable, and appropriate for the intended audience (internal, customers, or both).

## When to Use
- A set of PRs/issues is ready for release and needs a coherent summary
- Stakeholders need to know impact, risk, and required follow-ups
- You must communicate changes without leaking sensitive/internal details

**When NOT to use**
- No user-visible or operationally relevant changes occurred

## Core Pattern
Write for outcomes, not implementation:
- **What changed** (user-facing)
- **Who is affected** (segments, plans, roles)
- **Anything required** (migration steps, toggles, downtime)
- **Known issues** (if applicable)

## Quick Reference
Use this structure:
- **Highlights** (2–5 bullets)
- **Improvements**
- **Fixes**
- **Breaking changes** (if any) + mitigation
- **Operational notes** (deploy windows, feature flags) (internal-only)

## Implementation
1. List included tickets/PRs and group by theme.
2. Rewrite each item as “Outcome + affected area” in plain language.
3. Add any required actions and clearly label breaking changes.
4. Remove internal-only details (stack traces, customer names, security-sensitive info).

## Common Mistakes
- **Changelog dump**: raw PR titles are rarely meaningful—rewrite.
- **Overclaiming**: avoid “fixed forever”; be precise about scope.
- **Missing required actions**: if users must do something, put it near the top.

