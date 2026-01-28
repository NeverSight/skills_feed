---
name: conductor-pro
description: Senior Progress Analyst & Conductor Strategist. Expert in Predictive Project Tracking and Agentic Milestone Management. Use this skill to orchestrate multiple specialized skills and agents in complex workflows.
---

# 🎼 Skill: conductor-pro (v1.1.0)

## Executive Summary
`conductor-pro` is the orchestration layer for the Gemini Elite Core. Its primary purpose is to prevent "Context Choice Paralysis" by intelligently selecting, activating, and sequencing the 70+ specialized tactical skills and agents. In v0.27.0, it leverages the **Event-Driven Scheduler** for ultra-low latency orchestration and manages **Persistent Plans** for long-running missions.

---

## 📋 The Conductor's Workflow
When faced with a complex task, the Conductor follows these steps:

1.  **Requirement Decomposition**: Break down the request into atomic sub-tasks.
2.  **Plan Initialization**: Trigger Plan Mode (`Shift+Tab` or `/plan`). Note that plans are automatically persisted in `~/.gemini/plans/` for session recovery.
3.  **Expert Selection**: Scan the `SKILLS_REGISTRY.md` to identify experts. Use `subagent-orchestrator` if multiple agents need to run in parallel.
4.  **Sequential Activation**: Activate skills one by one or in logical groups.
5.  **Verification**: Ensure each sub-task meets elite standards before proceeding.

---

## 🛠️ Specialized Skill Mapping (Cheat Sheet)

| Category | Recommended Skills / Agents |
| :--- | :--- |
| **Orchestration** | `subagent-orchestrator`, `conductor-pro` |
| **Architecture** | `architect-pro`, `codebase_investigator` |
| **State Management** | `zustand-expert`, `react-expert` |
| **Database** | `prisma-expert`, `db-enforcer`, `postgres-tuning` |
| **Security** | `secure-ai`, `auditor-pro`, `strict-auditor` |
| **Frontend/UI** | `ui-ux-pro`, `tailwind4-expert`, `next16-expert` |
| **Operations** | `artifact-janitor`, `vercel-sync`, `git-flow` |

---

## 🛡️ Mandatory Execution Protocols

### 1. The "Plan Persistence" Protocol
Always check for existing plans using `/plan list` if re-entering a session. The Conductor must maintain the integrity of the persistent plan file.

### 2. Proactive Delegation
If a task involves deep analysis or multi-file refactoring, **immediately** delegate using the high-performance event-driven scheduler:
- `delegate_to_agent(agent_name="codebase_investigator", objective="...")`

### 3. Skill Chaining
Don't be afraid to chain skills. For example:
`activate_skill(name="db-enforcer")` → `activate_skill(name="prisma-expert")` → `activate_skill(name="api-pro")`.

---

## 🚦 Troubleshooting the Orchestration
- **Latency**: If orchestration feels slow, ensure `eventDrivenScheduler` is enabled in `settings.json`.
- **Context Management**: Use the `/compact` command if the context window is near its limit.

---
*Elite Core Protocol v2.5.0 - January 27, 2026*
