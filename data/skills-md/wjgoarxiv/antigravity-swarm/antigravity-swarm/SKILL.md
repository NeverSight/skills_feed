---
name: antigravity-swarm
description: Deploys autonomous sub-agents to perform tasks in the Antigravity IDE. Supports both manual dispatch and dynamic "Auto-Hiring" of agent teams.
---

# Antigravity Subagents Skill

This skill allows you to dispatch autonomous sub-agents to perform tasks.
It features a **Manager** layer (`planner.py`) that can automatically design a team of agents for a complex mission, and an **Orchestrator** (`orchestrator.py`) to run them visually.
Both scripts include a **Plan Mode** (confirmation step) by default to prevent accidental usage limits consumption.

> [!WARNING]
> **Do NOT modify files in this directory while the Orchestrator is running.**
> The system actively reads and writes to `task_plan.md`, `findings.md`, and `subagents.yaml`.
> Manual edits during execution may cause race conditions or inconsistent agent behavior.

## 🛠 Tools

### `dispatch_subagent`

Runs a sub-agent with a specific task.

**Usage:**
Use this when you have a parallelizable task or need to offload a specific job (e.g., "Write a test file", "Analyze this directory").

**Arguments:**

- `task`: A clear, self-contained description of what the sub-agent should do.

**Implementation Details:**
The sub-agent is powered by the `gemini` CLI. A Python wrapper intercepts specific output patterns to perform file system operations and command executions.

**Syntax used by Sub-Agent (Handled Automatically):**

- `<<WRITE_FILE path="...">>...<<END_WRITE>>`
- `<<RUN_COMMAND>>...<<END_COMMAND>>`

### `run_mission` (Dynamic Orchestration)

Analyzes a high-level goal, hires a custom team of sub-agents, and creates a configuration for them.

**Usage:**
Use this for complex, multi-step projects where you don't want to manually define every sub-agent.

**Arguments:**

- `mission`: A description of the overall project (e.g., "Create a Snake game in Python").

**How it works:**

1.  Calls `scripts/planner.py` to generate `subagents.yaml`. (Will prompt for confirmation unless `--yes` is used).
2.  (Optional) You can then run `scripts/orchestrator.py` to execute the team. (Will prompt for confirmation unless `--yes` is used).

## Usage Modes

### Mode 1: CLI User (Terminal Visualization)

Run the Python orchestrator in your terminal to see a TUI.

```bash
python scripts/orchestrator.py
```

### Mode 2: IDE Agent (Chat Visualization)

As an Agent, you act as the Orchestrator.

1.  **Spawn**: Use `run_command` to launch sub-agents in the background. Use `--format json` for logs.
    ```bash
    python scripts/dispatch_agent.py "Task A" --log-file logs/agent_a.json --format json &
    python scripts/dispatch_agent.py "Task B" --log-file logs/agent_b.json --format json &
    ```
2.  **Monitor**: Poll the JSON log files to check for `{"type": "status", "content": "completed"}`.
3.  **Visualize**: Render a Markdown dashboard in your chat response to the user.

## 🚀 Examples

### 1. Manual Dispatch (Single Agent)

```python
run_command("python3 scripts/dispatch_agent.py 'Create a file named hello.py that prints Hello World'")
```

### 2. Auto-Hire a Team (Mission Mode)

```python
# 1. Generate the team
run_command("python3 scripts/planner.py 'Create a fully functional Todo List app in HTML/JS'")

# 2. Run the team
run_command("python3 scripts/orchestrator.py")
```

> [!WARNING]
> You must use `gemini-3-pro` or `gemini-3-flash`. Deprecated or older models may not support the file shim protocol correctly.

## ❓ FAQ & Philosophy

### Why Sub-agents?

1.  **Context Isolation**: Prevents "Context Contamination." A UI Specialist doesn't need to see specific Database Migration code. Separation ensures higher accuracy.
2.  **Scalability**: While loop-based agents process sequentially, Sub-agents are architected to run in parallel threads.
3.  **Fault Tolerance**: If one sub-agent fails (e.g., Syntax Error), it doesn't crash the entire mission; the Orchestrator can retry just that agent.

### Is this truly parallel?

Yes. `orchestrator.py` uses Python's `threading.Thread` to spawn separate OS processes for each agent.
_Note: You may perceive sequential behavior if the underlying `gemini` CLI tool enforces a global lock or if you hit API Rate Limits._

### Planning with Files (Manus Protocol)

This skill adheres to the "Manus" state management philosophy. All agents operate on a shared set of "Memory Files" in the root of the workspace:

1.  `task_plan.md`: The Source of Truth for the mission checklist.
2.  `findings.md`: A shared scratchpad for discoveries and research.
3.  `progress.md`: A log of completed steps and current status.
