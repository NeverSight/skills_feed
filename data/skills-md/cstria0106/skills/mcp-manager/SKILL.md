---
name: mcp-manager
description: Manage MCP servers in Codex quickly and safely. Use this skill when the user asks to add, update, remove, inspect, or troubleshoot MCP servers, especially from a GitHub URL. The skill enforces scope selection (project `./.codex/config.toml` vs global `~/.codex/config.toml`), checks for existing entries, and asks the user to choose required options before making changes.
---

Manage Codex MCP servers with explicit scope and conflict handling.

## Command Reference

Use Codex CLI as the primary interface:

```bash
codex mcp list
codex mcp list --json
codex mcp get <name>
codex mcp add <name> -- <command> [args...]
codex mcp add <name> --url <url> [--bearer-token-env-var <ENV_VAR>]
codex mcp remove <name>
```

Use these config table shapes when editing TOML directly:

```toml
[mcp_servers.example]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.example.env]
API_KEY = "value"
```

```toml
[mcp_servers.example]
url = "https://example.com/mcp"
bearer_token_env_var = "MCP_TOKEN"
```

## Required Decision Flow

Follow this sequence for every install/update request.

1. Resolve target server details by input type (URL vs name).
2. Present a short MCP summary to the user before install.
3. Ask for install scope.
4. Check whether server already exists in the chosen scope.
5. Ask for conflict action if it exists.
6. Ask for options before writing config (required + optional env vars, bearer token env var, server name).
7. Ask for final installation confirmation.
8. Apply change and verify.

Do not skip user choices when ambiguity exists.
Do not write config until step 7 is explicitly completed.

## Source Validation By Input Type

Always validate MCP details before deciding command/url config:

1. If user provides a URL:
- Open/fetch that URL directly and read the install section.
- Confirm repository/package/server name, transport type, launch command or endpoint, and auth/env requirements from the source.
- Do not rely on memory-only fast path without opening the provided URL.

2. If user provides only a name:
- Search for the MCP first, then open the most relevant official source (repo/docs/registry page).
- Confirm the same fields (name, transport, launch method, auth/env requirements) from that source.
- If multiple candidates exist, present concise options and ask user to choose before install.

If verification is incomplete or conflicting, ask a clarification question and wait.

## Pre-Install MCP Summary

Before any scope/conflict/env questions, provide a brief MCP summary from validated sources:

- what the MCP does (1 line)
- official install/launch method to be used
- auth/env expectations (required vs optional)
- chosen server name (or proposed default name)

Only after this summary, proceed with structured install prompts.

## Non-Skippable Prompt Gate

Before any `codex mcp add` or config edit, the assistant must collect an explicit user answer for each applicable prompt:

1. Scope selected (`project` or `global`) unless already specified by user.
2. Conflict action selected if server name already exists.
3. Env/auth options prompt asked with available options and defaults.
4. Final install confirmation received.

If any gate is unanswered, stop and ask. Do not proceed with a "minimal default" install.

## Questioning Mode Policy

Collect user choices with this mode-specific policy:

1. If `request_user_input` tool is available, use it first.
2. If unavailable (for example Default mode), ask in normal chat.

In both cases, ask once in a single structured prompt that covers all applicable fields:

- scope (`project` or `global`)
- conflict action (only if existing server name is found)
- env/auth options with defaults, and which values user wants to set
- server name (only if needed)
- final confirmation (`install now` or `cancel`)

Do not split these into multiple back-and-forth prompts unless the user answer is incomplete.

## Env Option Prompting Rules

For env/auth, do not ask a binary yes/no question.

1. List available options and describe each briefly.
2. Show default behavior/value for each option when user does not provide one.
3. Ask user which options to set and what values to use.
4. Apply only values explicitly provided by the user.
5. If user provides nothing, proceed with documented defaults.

## Scope Selection

Always ask this first unless user already specified scope:

- `Project scope`: write to `./.codex/config.toml` in current repository.
- `Global scope`: write to `~/.codex/config.toml`.

Prefer project scope for repo-specific tools; prefer global scope for reusable personal tools.

## Existing Server Handling

If the same server name exists in chosen scope, ask user to choose:

- `Keep existing` (no change).
- `Update in place` (replace command/url/options for same name).
- `Remove and re-add`.
- `Use a new name`.

Never overwrite existing entries silently.

## Install from GitHub URL

When user gives a GitHub repo URL:

1. Inspect repo docs quickly to find the official MCP launch method.
2. Infer transport type:
- `stdio` if docs provide executable command (`npx`, `uvx`, binary, docker command).
- `streamable HTTP` if docs provide MCP endpoint URL.
3. Extract required options:
- `stdio`: executable command, args, optional env vars.
- `HTTP`: URL, optional bearer token env var.
4. If still ambiguous, ask a focused clarification question before writing config.

Known fast path:

- `https://github.com/upstash/context7` -> `npx -y @upstash/context7-mcp`

Fast path only resolves command/args. It does not skip the decision flow or prompt gate.

## Apply Changes

Use this implementation strategy:

- Global scope:
- Prefer `codex mcp add/remove/get/list`.
- Project scope:
- Edit `./.codex/config.toml` directly with `[mcp_servers.<name>]` blocks.
- Create `./.codex/config.toml` if missing.

When adding stdio server in project scope, write:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

When adding HTTP server in project scope, write:

```toml
[mcp_servers.<name>]
url = "https://host/path"
bearer_token_env_var = "TOKEN_ENV_VAR"
```

## Verification Checklist

After changes:

1. Confirm config file changed in expected scope.
2. Confirm entry shape is valid (`command` + `args`, or `url`).
3. Run scope-appropriate check:
- Global: `codex mcp get <name>` or `codex mcp list --json`.
- Project: inspect `./.codex/config.toml` and verify table values.
4. Report what was installed, where, and any env vars user must set.

## User Interaction Templates

Use concise prompts like:

- `Choose install scope: project (./.codex/config.toml) or global (~/.codex/config.toml)?`
- `Server "context7" already exists in project scope. Choose: keep, update, remove+re-add, or new name?`
- `Available env/auth options: API_KEY (default: not set, lower rate limits). Provide only the values you want to set; unspecified options will use defaults.`
- `Final check: proceed with installation using the resolved settings? (install now/cancel)`

Keep questions short and only ask what is required to proceed safely.

Single structured prompt template (preferred):

`Please answer these in one message: (1) scope: project/global, (2) if server exists: keep/update/remove+re-add/new name, (3) env/auth options you want to set from the list below and their values (unspecified options use defaults), (4) final confirmation: install now/cancel.`
