---
name: ralph-driven-development-linear
description: Ralph Driven Development workflow that pulls Linear project issues via the Linear MCP and runs them sequentially with Codex. Use when automating task execution from a Linear project and when you need a runner that advances issues and asks for the next task automatically.
---

# Ralph Driven Development (Linear)

## Description and Goals

This skill provides a Ralph Driven Development workflow that pulls Linear project issues via the Linear MCP and runs them sequentially with Codex. It automates task execution from a Linear project and advances issues automatically.

### Goals

- Automate development workflow using Linear project issues
- Integrate with Linear MCP for issue management
- Run Codex agents sequentially against Linear issues
- Track progress and handle retries automatically
- Support customizable runner configuration

## What This Skill Should Do

When automating task execution from a Linear project, this skill should:

1. **Connect to Linear** - Authenticate with Linear MCP and resolve project
2. **Fetch issues** - Pull issues from the specified Linear project
3. **Execute sequentially** - Run Codex against each issue in order
4. **Track progress** - Monitor completion and handle retries
5. **Advance issues** - Automatically move to the next issue after completion

Use this skill when automating task execution from a Linear project and when you need a runner that advances issues and asks for the next task automatically.

## Information About the Skill

### Prerequisites

- `codex` is on PATH.
- Linear MCP is authenticated: `codex mcp login linear`
- Provide a project via `--project` or `AGENTS.MD`.

### Run

```bash
python scripts/ralph-linear.py --project "Project Name"
```

### Flags

- `--project` Linear project name or ID. If omitted, reads `Linear Project:` under `## PROJECT` in `AGENTS.MD`.
- `--agents-path` Path to `AGENTS.MD`. Default: `AGENTS.MD`.
- `--codex-exe` Codex executable name or path. Default: `codex`.
- `--codex-args` Space-separated Codex args string. Default: `exec --dangerously-bypass-approvals-and-sandbox`.
- `--codex-timeout` Seconds before killing a Codex run; `0` = unlimited. Default: `0`.
- `--max-tasks` Max issues to process; `0` = unlimited. Default: `0`.
- `--max-attempts-per-task` Retries per issue. Default: `5`.
- `--log-path` Log file path (repo-relative or absolute). Default: `docs/logs/linear.log`.
- `--dry-run` Resolve project and exit without running Codex.

### Examples

```bash
python scripts/ralph-linear.py --project "VisionOS Agents" --max-tasks 3
```

```bash
python scripts/ralph-linear.py \
  --project "VisionOS Agents" \
  --codex-args 'exec --full-auto -m gpt-5.2-codex'
```
