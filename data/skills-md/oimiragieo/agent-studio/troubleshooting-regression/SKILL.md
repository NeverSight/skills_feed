---
name: troubleshooting-regression
description: Regression troubleshooting workflow for hook/router/memory/search failures with enforced evidence and fix validation
argument-hint: '[--prompt "..."] [--log-path <path>] [--mode quick|full]'
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Troubleshooting Regression

Use this skill when the framework appears stale, stuck, or regressed and you need deterministic diagnosis plus fix verification.

## When to Use

- Claude debug sessions stall after spawning agents.
- Hooks block expected actions unexpectedly.
- Memory/search/token-saver enforcement appears inconsistent.
- A regression needs a repeatable reproduction and validation run.

## Iron Law

Do not declare a regression fixed without:

1. reproducible trigger prompt,
2. trace evidence from `pnpm trace:query`,
3. hook/tool evidence from debug logs,
4. targeted test pass for touched scope.

## Workflow

1. Identify session and log source.
2. Run trace query first (`pnpm trace:query --trace-id <traceId> --compact --since <ISO-8601> --limit 200`).
3. Extract high-signal errors (excluding known MCP auth/startup noise).
4. Map each error to owning hook/module.
5. Patch minimal code path and add/update regression test.
6. Run targeted checks (tests + lint/format on changed files).
7. Re-run debug prompt and verify error class no longer reproduces.
8. Record learnings/issues in memory.

## Evidence Model

- Source of truth: `C:\\Users\\<user>\\.claude\\debug\\*.txt`
- Trace source of truth: `pnpm trace:query` output for the same incident window
- Filter: ignore external MCP transport/auth noise; keep framework/runtime errors
- Error classes:
  - routing/task lifecycle
  - memory/search/token-saver guardrails
  - hook contract/schema violations
  - workflow phase/idempotency failures

## Command Surface

Primary wrapper:

```bash
node .claude/skills/troubleshooting-regression/scripts/main.cjs --prompt "search the codebase for any issues or bugs"
pnpm trace:query --trace-id <traceId> --compact --since <ISO-8601> --limit 200
```

Optional direct log analysis:

```bash
node .claude/skills/troubleshooting-regression/scripts/main.cjs --log-path "C:\\Users\\<user>\\.claude\\debug\\<session>.txt"
```

## Output Contract

- `ok`: boolean
- `logPath`: analyzed log path
- `findings[]`: normalized findings with severity and owner file hints
- `nextActions[]`: concrete fix/validation actions

## Related Artifacts

- Workflow: `.claude/workflows/troubleshooting-regression-skill-workflow.md`
- Tool: `.claude/tools/troubleshooting-regression/troubleshooting-regression.cjs`
- Command: `.claude/commands/troubleshooting-regression.md`

## Examples

```bash
# Analyze latest log
node .claude/skills/troubleshooting-regression/scripts/main.cjs --mode quick

# Analyze specific log and fail when critical findings exist
node .claude/skills/troubleshooting-regression/scripts/main.cjs --log-path "<path>" --strict
```

## Memory Protocol

Before starting:

```bash
cat .claude/context/memory/learnings.md
```

After completing:

- Regression pattern -> `.claude/context/memory/learnings.md`
- Open defect or risk -> `.claude/context/memory/issues.md`
- New enforcement decision -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
