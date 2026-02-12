---
name: agentic-backlog-scrum
description: Keep AI implementation work synced with a backlog through MCP tools. Use when creating, updating, tracking, or reviewing tasks during coding workflows.
metadata:
  author: hakenshi
  version: "0.3.0"
---

# Agentic Backlog Scrum

Use this skill whenever you are doing implementation work and need task tracking discipline.

## What this skill is

- This skill is documentation for agent behavior.
- It defines workflow, guardrails, and tool usage conventions.
- It is not a database, API server, or business-logic runtime.

This skill assumes a local MCP server named `agentic-backlog` is available.

## Runtime boundary

- The running backlog API/application is the source of truth.
- MCP is how the agent reads context from and sends operations to that running API.
- This skill only tells the agent how to behave when using MCP tools.

## API bootstrap fallback (required)

If backlog MCP calls fail because the API is not reachable (connection refused, timeout, 5xx from missing service), the agent must bootstrap the API container before continuing.

1. Pull latest API image:
   - `docker pull lonelyww/agentic-backlog-elysia:latest`
2. Replace any stale container instance:
   - `docker rm -f agentic-backlog-api || true`
3. Run API on localhost `:38117`:
   - `docker run -d --name agentic-backlog-api -p 38117:8000 -e PORT=8000 -e BACKLOG_DB_PATH=/data/backlog.sqlite -v agentic-backlog-data:/data lonelyww/agentic-backlog-elysia:latest`
4. Verify health:
   - `curl http://127.0.0.1:38117/api/health`
5. Retry the failed backlog MCP call.

Notes:

- Use Docker named volume `agentic-backlog-data` to persist SQLite without host bind mount paths.
- If MCP points to a different port, update `BACKLOG_API_BASE_URL` to match (recommended default: `http://127.0.0.1:38117/api`).

## MCP connectivity check (required)

After API bootstrap, validate MCP end-to-end before doing backlog operations:

1. Confirm API health endpoint:
   - `curl http://127.0.0.1:38117/api/health`
2. Run a lightweight MCP tool call to verify data path:
   - `backlog.health` then `backlog.version`
   - `backlog.identify_project`

If the MCP tool call fails because the MCP server is not configured in the current client:

- Register a local MCP server named `agentic-backlog` in the active client.
- Use local command: `npx -y @hakenshi/agentic-backlog-mcp-server`.
- Set env: `BACKLOG_API_BASE_URL=http://127.0.0.1:38117/api`.

If the API health check fails, run the API bootstrap fallback section above.

Client examples (optional):

- OpenCode: `opencode mcp add` and `opencode mcp list`
- Any MCP-capable client: add server `agentic-backlog` with the same command/env above

## Trigger phrases

Use this skill proactively when the user says things like:

- `\agentic-backlog:add`
- `\agentic-backlog:remove`
- `\agentic-backlog:update`
- `\agentic-backlog:read`
- `\agentic-backlog:board`
- `\agentic-backlog:in-progress`
- `\agentic-backlog:show-task`
- `\agentic-backlog:update-task`

Expected behavior by trigger:

- **\agentic-backlog:add** -> create a task (`backlog.create_task`)
- **\agentic-backlog:remove** -> delete only with explicit confirmation (`backlog.delete_task` + `confirm: "DELETE"`)
- **\agentic-backlog:update** -> update task fields or status (`backlog.update_task` / `backlog.update_task_status`)
- **\agentic-backlog:read** -> fetch board/task snapshot (`backlog.get_board` / `backlog.get_console_table`)
- **\agentic-backlog:board** -> return board overview (`backlog.get_board` + `backlog.get_console_table`)
- **\agentic-backlog:in-progress** -> list active WIP (`backlog.list_tasks` with `status: in_progress`)
- **\agentic-backlog:show-task** -> find a specific task by title keywords, then show it (`backlog.find_tasks_by_title` + `backlog.get_task`)
- **\agentic-backlog:update-task** -> find a specific task by title keywords, then update it (`backlog.update_task_by_title`)

Task-by-name behavior:

- Use user-provided title keywords to search current project tasks.
- Prefer exact title match; otherwise use best partial match.
- If multiple close matches exist, show top candidates and ask which one to use.
- For updates, always echo the matched task title/id before applying the change.

## Core tools (CRUD)

- `backlog.create_task`
- `backlog.get_task`
- `backlog.list_tasks`
- `backlog.find_tasks_by_title`
- `backlog.update_task`
- `backlog.update_task_by_title`
- `backlog.delete_task`

## Core tools (operational)

- `backlog.health`
- `backlog.version`

When available in current MCP version:

- `backlog.get_focus`
- `backlog.claim_task`
- `backlog.release_task`
- `backlog.restore_task`

## Capability check (required)

- Before relying on operational tools, verify availability in the current MCP server.
- If `backlog.health`/`backlog.version` are unavailable, fallback to `backlog.identify_project` as connectivity check.
- If `backlog.get_focus` is unavailable, fallback to `backlog.get_board` + `backlog.list_tasks(status=in_progress|blocked)`.
- If `backlog.restore_task` is unavailable, communicate that restore is not exposed in this MCP version.

## Goal

Keep a shared backlog that multiple AI agents can update consistently.

## Mandatory workflow

1. Identify project
   - Call `backlog.identify_project` first.
   - Store returned `project.id`.
2. Get current board
    - Call `backlog.get_board` and inspect WIP.
    - Call `backlog.get_focus` to prioritize blocked/stale/high-impact work.
    - Refresh board before each major implementation step.
    - When reporting progress to the user, call `backlog.get_console_table`.
3. Ensure active task exists
   - If no suitable task exists, call `backlog.create_task`.
4. Start work
   - Move task to `in_progress` with `backlog.update_task_status` or `backlog.update_task`.
5. During work
    - Add short progress notes with `backlog.add_task_note` using 3 fields:
      - `feito:`
      - `bloqueio:`
      - `proximo:`
    - Re-read the board after each note/status transition.
6. On completion
    - Before moving to `review` or `done`, add a compact summary note with outcome + remaining risks.
    - Move to `review` or `done`.
7. On blockers
   - Move to `blocked` and include reason.

## Status model

- `backlog`
- `todo`
- `in_progress`
- `blocked`
- `review`
- `done`
- `cancelled`

## Tool usage contract

Always include metadata when available:

- `source`: agent/client name (for example `codex`, `claude-code`, `opencode`, `cursor`)
- `agent_id`: stable agent identity when available
- `session_id`: current conversation/session id when available

## Ambiguity protocol (required)

- If a title query returns multiple plausible tasks, do not auto-apply update/delete.
- Show top 3 candidates (id, title, status, updated_at) and request explicit selection.
- Only proceed after user chooses one candidate.

## Failure protocol (required)

- If MCP/API is unavailable, return this standard message:
  - `Backlog indisponivel no momento. Vou restabelecer conexao e tentar novamente.`
- MCP fail-fast behavior:
  - The MCP may open a short circuit window after timeout/5xx errors and return immediate 503 responses.
  - This is expected and prevents long agent stalls when API is down.
  - During this window, use `backlog.health` and `backlog.version` as recovery probes.
- Then execute recovery in order:
  1. `backlog.health`
  2. API bootstrap fallback (section above)
  3. `backlog.version`
  4. Retry original operation once
- Retry rules:
  - Retry only timeout/5xx.
  - Do not retry 4xx validation/auth/conflict errors.

## Planning mode

Use `backlog.plan_from_context` for fast task drafting from plain text.

- Default behavior is preview mode.
- Use `apply=true` to persist generated actions.
- Apply only if actions are relevant to the current project scope.

## Guardrails

- Do not perform large code changes without linking to a task.
- Keep notes objective and short.
- Prefer one active `in_progress` task per agent/session.
- Deletions must be explicit: call `backlog.delete_task` with `confirm: "DELETE"`.
- Keep updates frequent: at least one status or note update per completed sub-step.
