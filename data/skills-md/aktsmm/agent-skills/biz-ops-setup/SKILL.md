---
name: biz-ops-setup
description: "Business operations workspace setup with workIQ integration. Creates report generation, task management, and customer management system. Use when: setting up new workspace, initializing biz-ops environment, creating business management system."
license: CC BY-NC-SA 4.0
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# Biz-Ops Workspace Setup

Initialize a business operations workspace with integrated reporting and task management.

## When to Use

- **biz-ops setup**, **業務管理ワークスペース**, **レポート管理**
- Setting up a new workspace from scratch
- Deploying workIQ-based reporting and task management

## Prerequisites

| Item                     | Required | Description             |
| ------------------------ | -------- | ----------------------- |
| VS Code + GitHub Copilot | Yes      | Agent execution         |
| Git + PowerShell 7+      | Yes      | Version control/scripts |
| workIQ MCP Server        | Optional | M365 integration        |

## Setup Flow

```
Interview → Folder Structure → Deploy Agents → Customer Workspaces → Config → Done
```

## Phase 1: Interview (MANDATORY)

Collect the following information:

1. **Customer list**: Name, ID, primary contact
2. **External folders**: Tech QA, Blog, OneDrive paths (optional)
3. **Holiday config**: japan / us / other
4. **workIQ availability**: Yes (M365 auto) / No (manual input)

> ⚠️ **CRITICAL**: Always run `Get-Date` before generating reports.

## Phase 2-5: Setup Execution

**Recommended: Use scripts**

```powershell
# Phase 2: Create folder structure
.\scripts\Initialize-BizOpsWorkspace.ps1 -WorkspacePath "D:\my-biz-ops" -Customers @("contoso")

# Phase 3: Deploy agents and prompts
.\scripts\Deploy-BizOpsTemplates.ps1 -WorkspacePath "D:\my-biz-ops"
```

**Manual setup** → [references/setup-phases.md](references/setup-phases.md)

## Deployed Components

| Type    | Count | Examples                                      |
| ------- | ----- | --------------------------------------------- |
| Agents  | 6     | orchestrator, report-generator, task-manager  |
| Prompts | 4     | daily-report, weekly-report, monthly-report   |
| Folders | 7     | ActivityReport/, Customers/, Tasks/, \_inbox/ |

## Done Criteria

- [ ] All folders created (ActivityReport/, Customers/, Tasks/, etc.)
- [ ] 6 agents deployed to `.github/agents/`
- [ ] 4 prompts deployed to `.github/prompts/`
- [ ] Customer mappings configured in `copilot-instructions.md`
- [ ] Workflow verification passed (daily report test)

## Key References

| Topic            | Reference                                                        |
| ---------------- | ---------------------------------------------------------------- |
| Setup Phases     | [references/setup-phases.md](references/setup-phases.md)         |
| Folder Structure | [references/folder-structure.md](references/folder-structure.md) |
| Agent List       | [references/agent-list.md](references/agent-list.md)             |
| Holidays         | [references/holidays.md](references/holidays.md)                 |
