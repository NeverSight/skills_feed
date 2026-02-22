---
name: eval-harness-updater
description: Refresh evaluation harnesses with live/fallback parser reliability, SLO gates, and regression checks.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Glob, Grep, Bash, Skill, MemoryRecord, WebSearch, WebFetch]
args: '--harness <path-or-name> [--trigger reflection|evolve|manual]'
error_handling: graceful
streaming: supported
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Eval Harness Updater

Refresh eval harnesses to keep live + fallback modes actionable under unstable environments.

## Focus Areas

- Prompt and parser drift
- Timeout/partial-stream handling
- SLO and regression gates
- Dual-run fallback consistency

## Workflow

1. Resolve harness path.
2. Research test/eval best practices.
3. Add RED regressions for parsing and timeout edge cases.
4. Patch minimal harness logic.
5. Validate eval outputs and CI gates.
