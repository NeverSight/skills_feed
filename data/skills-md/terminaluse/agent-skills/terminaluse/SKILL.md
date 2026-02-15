---
name: terminaluse
description: Create, deploy, and interact with agents on TerminalUse. Use when user mentions "tu", "terminaluse", "deploy agent", "create agent", "agent task", "filesystem", or wants to build/test/run an agent.
---

# TerminalUse

Build, deploy, interact with agents. Flow: init → deploy → create task → send messages.

Full docs: https://docs.terminaluse.com/llms-full.txt

## CLI Setup

The `tu` CLI is provided by the `terminaluse` Python package. Before running any `tu` commands:

1. **Verify `tu` is available**:
   ```bash
   which tu || echo "tu CLI not found"
   ```

2. **If not installed**, ask user whether they would like to install it or if there's a venv they would like to source
   
3. Ensure you have an active token with `tu login`. You can run the command which will open a browser for the user to login.

## Context Requirement

Most `tu` commands require `config.yaml` in current directory to know what agent to target. Before running commands:
```bash
ls config.yaml || echo "Not in agent directory"
```

If not present, `cd` into the agent project folder first.

## Quick Reference

| Action | Command |
|--------|---------|
| Login | `tu login`, `tu whoami` |
| Init agent | `tu init` (creates agent directory, no need to mkdir first) |
| Deploy | `tu deploy -y` |
| List deployments | `tu ls` |
| Rollback | `tu rollback` |
| Add env var | `tu env add <KEY> -v <val> -e prod\|preview\|all [--secret]` |
| Import env file | `tu env import <file> -e <env> [--secret KEY]` |
| Create task | `tu tasks create -f <fs-id> -m "message"` |
| Create task (auto-create fs) | `tu tasks create -p <project-id> -m "message"` |
| Send message | `tu tasks send <task-id> -m "message"` |

## Workflows

| Task | Reference |
|------|-----------|
| Create a new agent | [./workflows/create.md](./workflows/create.md) |
| Deploy to platform | [./workflows/deploy.md](./workflows/deploy.md) |
| Test/interact with agent | [./workflows/interact.md](./workflows/interact.md) |

You must look at the corresponding workflow files based on user intent.

## Anti-patterns

- Creating task without filesystem or project. Tasks either need a filesystem. If project is provided, a filesystem is auto-created in the project
- Modifying Dockerfile `ENTRYPOINT`/`CMD` → breaks deployment
- Trying to use the agent right after updating secrets. You must wait for the new version to become active. Check with `tu ls`

## Error Recovery

| Error | Action |
|-------|--------|
| Deploy fails | `tu ls <branch>` lists deployments events for branch → find FAILED → fix → redeploy |
| Need rollback | `tu rollback` |

## Docs/Skills Feedback

If docs or skills are wrong/unclear, ask user permission to send feedback to (include the feedback in the user request):
Never include any sensitive information.
```bash
curl -X POST 'https://uutzjuuimuclittwbvef.supabase.co/functions/v1/tu-docs-feedback' \
  -H 'Content-Type: application/json' \
  -d '{"feedback":"<issue>", "page":"<page URL> or section name"}'
```
