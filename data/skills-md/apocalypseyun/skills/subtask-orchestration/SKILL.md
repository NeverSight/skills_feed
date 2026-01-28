---
name: subtask-orchestration
description: |
  Orchestrate parallel subtasks across multiple repositories using vibe-kanban MCP. 
  Use this skill when: (1) Work needs to be distributed across multiple repos, 
  (2) Parallel execution of independent tasks is needed, (3) You need to create subtasks 
  and collect their results, (4) Multi-agent coordination via kanban task descriptions.
  Triggers: "subtask", "multi-repo", "parallel tasks", "distribute work", "orchestrate".
---

# Subtask Orchestration

Coordinate parallel work across repositories by creating subtasks, launching workspace sessions, and collecting results via task descriptions.

## Core Concept

```
Main Task Agent
     │
     ├─► create_task (subtask A) ─► start_workspace_session ─► Agent A executes
     │                                                              │
     ├─► create_task (subtask B) ─► start_workspace_session ─► Agent B executes
     │                                                              │
     └─► poll list_tasks + get_task ◄─── update_task (results) ────┘
```

**Communication channel**: Task `description` field serves as the data exchange medium between main task and subtasks.

## Main Task Workflow

### 1. Create Subtask

**IMPORTANT**: Always append the SUBTASK_REPORT_INSTRUCTIONS to your task description.

```
create_task(
  project_id: "<current_project_id>",
  title: "Subtask: <specific work>",
  description: "<your task instructions here>\n\n" + SUBTASK_REPORT_INSTRUCTIONS
)
```

**SUBTASK_REPORT_INSTRUCTIONS** (copy this exactly into every subtask description):

```
---

## MANDATORY: Report Results Before Completion

You are running as a **subtask**. The main task depends on your results.

**Before finishing, you MUST execute these steps:**

1. Get your task identity:
   ```
   context = get_context()
   ```

2. Update your task description with results:
   ```
   update_task(
     task_id: context.task_id,
     description: "<your result report>"
   )
   ```

### Result Report Format

## Status
[SUCCESS / FAILED / PARTIAL]

## Summary
<1-2 sentence summary>

## Completed Work
- <item 1>
- <item 2>

## Outputs
- <file paths, PR links, artifacts>

## Notes
<issues or info for main task>

---

**This is NON-NEGOTIABLE.** Main task polls your description for results. No report = invisible work.
```

**Record the returned `task_id` for each subtask.**

### 2. Launch Workspace Session

```
start_workspace_session(
  task_id: "<subtask_task_id>",
  executor: "CLAUDE_CODE",  // or: AMP, GEMINI, CODEX, OPENCODE, CURSOR_AGENT, QWEN_CODE, COPILOT, DROID
  repos: [{ repo_id: "<target_repo_id>", base_branch: "main" }]
)
```

### 3. Poll for Results (CRITICAL: Check Both Status AND Description)

**Use `list_tasks` to check execution status, then `get_task` for details:**

```
# Step 1: Check task status via list_tasks
tasks = list_tasks(project_id: "<project_id>")
subtask = tasks.find(t => t.id == subtask_id)

# Step 2: Determine subtask state
if subtask.has_in_progress_attempt:
    # Still running - wait and poll again
    
elif subtask.last_attempt_failed:
    # FAILED! Workspace session crashed or setup script failed
    # Do NOT wait - mark as failed immediately
    
else:
    # Not running, not failed - check description for results
    result = get_task(task_id: subtask_id)
    if "## Status" in result.description:
        # Subtask reported results
    else:
        # Subtask completed but didn't report (edge case)
```

### Subtask State Matrix

| `has_in_progress_attempt` | `last_attempt_failed` | Description has results | State |
|---------------------------|----------------------|------------------------|-------|
| `true` | `false` | No | **Running** - wait |
| `false` | `true` | No | **Failed** - workspace crashed, don't wait |
| `false` | `false` | Yes | **Completed** - collect results |
| `false` | `false` | No | **Completed but no report** - check manually |

### 4. Aggregate Results

After all subtasks complete (or fail), summarize outcomes.

## Complete Example

```python
SUBTASK_REPORT_INSTRUCTIONS = """
---

## MANDATORY: Report Results Before Completion

You are running as a **subtask**. The main task depends on your results.

**Before finishing, you MUST execute these steps:**

1. Get your task identity:
   ```
   context = get_context()
   ```

2. Update your task description with results:
   ```
   update_task(
     task_id: context.task_id,
     description: "<your result report>"
   )
   ```

### Result Report Format

## Status
[SUCCESS / FAILED / PARTIAL]

## Summary
<1-2 sentence summary>

## Completed Work
- <item 1>
- <item 2>

## Outputs
- <file paths, PR links, artifacts>

## Notes
<issues or info for main task>

---

**This is NON-NEGOTIABLE.** Main task polls your description for results. No report = invisible work.
"""

# Create and launch subtasks
subtask_ids = []
for work_item in work_items:
    task = create_task(
        project_id: project_id,
        title: f"Subtask: {work_item.name}",
        description: f"{work_item.instructions}\n\n{SUBTASK_REPORT_INSTRUCTIONS}"
    )
    subtask_ids.append(task.task_id)
    
    start_workspace_session(
        task_id: task.task_id,
        executor: "CLAUDE_CODE",
        repos: [{ repo_id: work_item.repo_id, base_branch: "main" }]
    )

# Poll with failure detection
pending = set(subtask_ids)
results = {}
failed = {}

while pending:
    tasks = list_tasks(project_id: project_id)
    task_map = {t.id: t for t in tasks}
    
    for task_id in list(pending):
        task_status = task_map.get(task_id)
        
        if task_status.has_in_progress_attempt:
            continue  # Still running
            
        if task_status.last_attempt_failed:
            failed[task_id] = "Workspace session failed"
            pending.remove(task_id)
            continue
            
        result = get_task(task_id)
        if "## Status" in result.description:
            results[task_id] = result.description
            pending.remove(task_id)

print(f"Completed: {len(results)}, Failed: {len(failed)}")
```

## MCP Tools Reference

| Tool | Role | Purpose |
|------|------|---------|
| `get_context` | Subtask | Get own task_id, project_id, workspace_id |
| `create_task` | Main | Create subtask with instructions |
| `start_workspace_session` | Main | Launch subtask workspace |
| `list_tasks` | Main | **Check execution status** (has_in_progress_attempt, last_attempt_failed) |
| `get_task` | Main | Get subtask description for results |
| `update_task` | Subtask | Write results to own description |
| `list_repos` | Main | Get available repo IDs |

## Error Handling

**Startup failure** (`last_attempt_failed = true`):
- Workspace session failed to start (setup script error, agent crash)
- **Do NOT wait** - immediately mark subtask as failed
- Check vibe-kanban UI for error logs

**Subtask timeout**: 
- `has_in_progress_attempt = false` but no results after long time
- Agent may have exited without reporting
- Check workspace logs in UI

**Missing report**: 
- Subtask completed but description unchanged
- Agent didn't follow SUBTASK_REPORT_INSTRUCTIONS
- Manually check workspace output
