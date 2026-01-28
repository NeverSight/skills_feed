---
name: agent-exec
description: Use the agent-exec CLI to run Codex/Claude/Cursor and manage skills for this repo.
---

# agent-exec

Use this skill when you need to run the local agent-exec CLI, select an agent, or install skills.

## When to use

- Run Codex/Claude/Cursor via a single wrapper command.
- Install or update skills using the open agent skills ecosystem.
- Capture a JSON summary of git changes after an agent runs.

## Instructions

1. Run agent-exec from the repo root unless a different `--dir` is required.
2. For normal tasks, run:
   - `npx agent-exec "<prompt>"`
   - If a specific agent is required: `npx agent-exec "<prompt>" --agent codex|claude|cursor`
   - To pass through agent-specific flags: `npx agent-exec "<prompt>" -- --model ...`
3. For skills installation, run:
   - `npx agent-exec skills add <owner>/<repo>`
   - Add `-g` for global installs and `-y` to skip prompts.
4. JSON output uses headless defaults (codex `exec`, claude `-p`, cursor `--print`).
   Override with `AGENT_EXEC_*_ARGS` (set to empty to disable defaults).
5. Default output is JSON. Use `--format text` only if human-readable logs are explicitly needed.
6. Codex has an experimental "run terminal in background" capability. If it is enabled,
   prefer that for long-running commands so the agent can continue while the job runs.
