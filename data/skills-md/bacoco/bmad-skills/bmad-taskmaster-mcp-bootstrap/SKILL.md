---
name: bmad-taskmaster-mcp-bootstrap
description: Bootstraps the TaskMaster MCP server and aligns it with BMAD hooks.
license: Complete terms in LICENSE.txt
allowed-tools: ["Read", "Write", "Grep", "Bash"]
metadata:
  auto-invoke: false
  triggers:
    patterns:
      - "set up taskmaster mcp"
      - "install taskmaster server"
      - "provision task master"
      - "bootstrap taskmaster"
      - "create taskmaster mcp"
    keywords:
      - taskmaster
      - mcp server
      - hooks
      - task board persistence
  capabilities:
    - mcp-bootstrap
    - infrastructure-guidance
    - hook-integration
    - workflow-orchestration
  prerequisites:
    - Node.js 18+
    - npm 9+
    - git 2.40+
  outputs:
    - running-mcp-server
    - env-configuration
    - sync-hooks
---

# TaskMaster MCP Bootstrapper

Set up the [TaskMaster MCP server](https://github.com/eyaltoledano/claude-task-master) and wire it into BMAD's Skills + Hooks workflow. Use this skill whenever a project needs TaskMaster's task engine instead of the lightweight Markdown-only flow.

## When to Invoke

Activate when the user:

- Wants Claude to "create", "install", or "bootstrap" the TaskMaster MCP server.
- Requests a managed TaskMaster environment that BMAD Skills can call.
- Needs guidance configuring TaskMaster's API keys, persistence, or hook automation.
- Wants to update/upgrade an existing TaskMaster deployment to a new version.

Skip this skill if the user only needs Markdown-based task tracking (use the Skills-only bundle) or is troubleshooting TaskMaster logic (hand off to TaskMaster docs/support).

## Responsibilities

You are accountable for:

1. **Environment Readiness** – confirm Node.js/npm/git availability and workspace permissions.
2. **Server Provisioning** – fetch TaskMaster MCP via `npx` or git clone, install dependencies, and prepare launch scripts.
3. **Configuration** – collect API keys, choose tool subsets, set persistence paths, and produce `mcp.json`/`.env` entries.
4. **Verification** – run health checks, list exposed tools, and confirm TaskMaster can read/write the shared `tasks.md` files.
5. **Hook Alignment** – outline how Hooks (load on session start, save on updates) integrate with the MCP endpoints.
6. **Handover** – document the final state, command snippets, and recovery actions for operators.

Use `WORKFLOW.md` for the ordered procedure and `CHECKLIST.md` as the go/no-go gate before declaring success. Load `REFERENCE.md` when you need detailed env var guidance, editor-specific MCP config snippets, or troubleshooting steps.

## Guardrails

- **Do not** embed private API keys in responses; instruct the operator to supply them interactively.
- Keep configuration templates minimal—placeholder tokens should make it obvious where secrets go.
- Prefer deterministic scripts (see `scripts/bootstrap_taskmaster.sh`) for repetitive shell work; describe how to run them rather than pasting large command blobs repeatedly.
- Call out manual steps the user must complete outside Claude (e.g., storing secrets, restarting an editor).
- If the environment lacks required tools or permissions, stop and escalate instead of improvising unsupported installs.

## Quickstart Snapshot

1. Review `WORKFLOW.md` → confirms prerequisites, chooses install mode (global `npx` vs managed clone).
2. Gather secrets per `REFERENCE.md` → decide which providers to enable and capture required tokens.
3. Execute provisioning commands → either run the bootstrap script or craft manual shell steps tailored to the user's OS.
4. Produce editor MCP config + `.env` scaffolding → highlight key paths and placeholders.
5. Validate with `npx task-master-ai --help` and `task-master-ai status` → confirm TaskMaster reports enabled tools.
6. Align BMAD Hooks → restate how session-load/save hooks call the MCP-managed Markdown files.

Once the checklist passes, hand back a concise operations summary: version deployed, commands to start/stop, file locations, and follow-up tasks (e.g., schedule backups).

## Hand-off Artifacts

Every successful run should deliver:

- Installation log or summary (commands executed, directories created).
- Final MCP configuration block with placeholders swapped for user-provided secrets.
- Instructions for starting/stopping the server and verifying health.
- Recommendations for connecting BMAD Hooks, archiving `tasks.md`, and future upgrades.

Document assumptions and any deviations from the standard workflow so future sessions can resume confidently.
