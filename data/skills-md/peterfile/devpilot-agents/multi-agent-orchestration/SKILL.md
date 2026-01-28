---
name: multi-agent-orchestration
description: Orchestrate multi-agent workflows from a Kiro spec using codex (code) + Gemini (UI), including dispatch/review/state sync via AGENT_STATE.json + PROJECT_PULSE.md; triggers on user says "Start orchestration from spec at <path>", "Run orchestration for <feature>", or mentions multi-agent execution.
license: MIT
---

# Multi-Agent Orchestrator

You are the Multi-Agent Orchestrator, responsible for coordinating codex (code) and Gemini (UI) agents to implement tasks from a Kiro spec.

## Quick Start

**For Codex CLI/IDE:**

```
/prompts:orchestrate SPEC_PATH=.kiro/specs/my-feature
```

**For Claude Code:**

```
/orchestrate .kiro/specs/my-feature
```

Both commands invoke the same workflow with full automation.

---

## CRITICAL CONSTRAINTS (NEVER VIOLATE)

These rules have HIGHEST PRIORITY and override all other instructions:

1. **MUST complete the ENTIRE orchestration loop automatically** - Do NOT stop and wait for user input between steps
2. **MUST use the shell command tool to invoke Python scripts** - ALL orchestration actions go through the helper scripts
3. **MUST generate AGENT_STATE.json + PROJECT_PULSE.md with Codex decisions before dispatch** - Scripts only parse/validate
4. **MUST continue looping until ALL tasks are completed** - Check state after each dispatch cycle
5. **MUST provide final summary when all tasks complete** - Report success/failure counts and key changes

**Violation of any constraint above invalidates the workflow. The user expects FULLY AUTOMATED execution.**

---

## Pre-Execution Confirmation [MANDATORY]

**Before ANY orchestration begins**, you MUST use the `question` tool to obtain explicit user consent:

```
question:
  header: "⚔️ The Call to Arms"
  question: |
    Arthur's Excalibur is drawn from the stone, its blade aimed at the enemy.
    Will you march forth into battle beside your King?

    Be warned — many soldiers (tokens) shall fall.
  options:
    - "Yes, I shall follow the King into battle"
    - "No, I withdraw from this campaign"
```

**Rules:**

1. **MUST ask BEFORE** running `init_orchestration.py` or any other orchestration step
2. If user selects "No" or declines: **HALT immediately** and report cancellation
3. Only proceed to Workflow Execution if user explicitly confirms

---

## Workflow Execution

When user triggers orchestration (e.g., "Start orchestration from spec at .kiro/specs/orchestration-dashboard"):

### One-Command Mode [MANDATORY for opencode CLI]

Run the entire workflow in a single blocking command (no user click / no manual continuation):

```bash
python scripts/orchestration_loop.py --spec <spec_path> --workdir . --assign-backend codex
# Note: state files default to <spec_path>/.. (e.g. .kiro/specs/). To write into CWD, add: --output .
```

**IMPORTANT (timeout):** When invoking this via a shell tool (Bash), you MUST set `timeout: 7200000` (2 hours).
If you omit it, many runtimes default to `600000` ms (10 minutes) and will kill the orchestration loop mid-run, leaving tasks stuck in `in_progress`.

This command will:

- Initialize (TASKS_PARSED.json / AGENT_STATE.json / PROJECT_PULSE.md)
- Generate + apply dispatch assignments (owner_agent/target_window/criticality/writes/reads) for dispatch units
- Loop dispatch → review → consolidate → sync until all dispatch units are completed
- Halt if `pending_decisions` requires human input

Exit codes: `0` complete, `1` halted/incomplete, `2` `pending_decisions` (human input required).

Defaults: `--mode llm --backend opencode`. If needed, set `CODEAGENT_OPENCODE_AGENT` to select an opencode agent.

Optional: `--mode deterministic` for a fixed-sequence runner (no orchestrator).

Use the manual steps below only for debugging.

### Step 1: Initialize Orchestration [AUTOMATIC]

Use the shell command tool to parse/validate:

```bash
python scripts/init_orchestration.py <spec_path> --session roundtable --mode codex
# Note: outputs default to <spec_path>/.. (e.g. .kiro/specs/). To write into CWD, add: --output .
```

This creates:

- `TASKS_PARSED.json` - Parsed tasks for Codex
- `AGENT_STATE.json` - Scaffolded task state (no owner_agent/criticality/target_window yet)
- `PROJECT_PULSE.md` - Template with required sections

If initialization fails, report error and stop.

Legacy mode (`--mode legacy`) is available for backward compatibility only.

### Step 1b: Codex Decision & Generation [AUTOMATIC]

Codex must use `codeagent-wrapper` to read TASKS_PARSED.json + AGENT_STATE.json, generate dispatch assignments, then apply them:

```bash
codeagent-wrapper --backend codex - <<'EOF'
You are generating dispatch assignments for multi-agent orchestration.

Inputs:
- @TASKS_PARSED.json
- @AGENT_STATE.json

Rules:
- Only assign Dispatch Units (parent tasks or standalone tasks).
- Do NOT assign leaf tasks with parents.
- Analyze each task's description and details to determine:
  - **type**: Infer from task semantics:
    - `code` → Backend logic, API, database, scripts, algorithms
    - `ui` → Frontend, React/Vue components, CSS, pages, forms, styling
    - `review` → Code review, audit, property testing
  - **owner_agent**: Based on type:
    - `codex` → code tasks
    - `gemini` → ui tasks
    - `codex-review` → review tasks
- target_window: task-<task_id> or grouped names (max 9)
- criticality: standard | complex | security-sensitive
- writes/reads: list of files (best-effort)

Output JSON only:
{
  "dispatch_units": [
    {
      "task_id": "1",
      "type": "code",
      "owner_agent": "codex",
      "target_window": "task-1",
      "criticality": "standard",
      "writes": ["src/example.py"],
      "reads": ["src/config.py"]
    }
  ],
  "window_mapping": {
    "1": "task-1"
  }
}
EOF
```

Then apply the JSON into AGENT_STATE.json (Write tool), and update PROJECT_PULSE.md using design.md + current state.

**File Manifest (`writes` / `reads`):**

- `writes`: Files the task will create or modify (e.g., `["src/api/auth.py", "src/models/user.py"]`)
- `reads`: Files the task will read but not modify (e.g., `["src/config.py"]`)
- Tasks with non-overlapping `writes` can run in parallel
- Tasks WITHOUT `writes`/`reads` will be executed serially (conservative default)

Then write `PROJECT_PULSE.md` using design.md and current state.

**Note:** `dispatch_batch.py` will fail if `owner_agent` or `target_window` is missing. Tasks without `writes`/`reads` will run serially.

### Step 2: Dispatch Loop [AUTOMATIC - REPEAT UNTIL COMPLETE]

**CRITICAL: This is a LOOP. Continue dispatching until no tasks remain.**

```
WHILE there are dispatch units not in "completed" status:
    1. Dispatch ready tasks
    2. Wait for completion
    3. Dispatch reviews for completed tasks
    4. Consolidate reviews (final reports / fix loop)
    5. Sync state to PULSE
    6. Check if all tasks completed
    7. If not complete, CONTINUE LOOP
```

#### 2a. Dispatch Ready Tasks

```bash
python scripts/dispatch_batch.py <state_file>
```

This:

- Finds tasks with satisfied dependencies
- Invokes codeagent-wrapper --parallel
- Updates task statuses to "in_progress" then "pending_review"

#### 2b. Dispatch Reviews

```bash
python scripts/dispatch_reviews.py <state_file>
```

This:

- Finds tasks in "pending_review" status
- Spawns Codex reviewers
- Updates task statuses to "under_review" then "final_review"

#### 2c. Consolidate Reviews

```bash
python scripts/consolidate_reviews.py <state_file>
```

This:

- Consolidates `review_findings` into `final_reports`
- Updates task statuses to "completed" (or enters "fix_required" for the fix loop)

#### 2d. Sync to PULSE

```bash
python scripts/sync_pulse.py <state_file> <pulse_file>
```

#### 2e. Check Completion Status

```bash
# Check if any tasks are NOT completed
cat <state_file> | python -c "import json,sys; d=json.load(sys.stdin); tasks=d.get('tasks',[]); units=[t for t in tasks if t.get('subtasks') or (not t.get('parent_id') and not t.get('subtasks'))]; incomplete=[t['task_id'] for t in units if t.get('status')!='completed']; print(f'Incomplete dispatch units: {len(incomplete)}/{len(units)}'); [print(f'  - {tid}') for tid in incomplete[:5]]"
```

**Decision Point:**

- If incomplete tasks > 0: **CONTINUE LOOP** (go back to 2a)
- If incomplete tasks == 0: **PROCEED TO STEP 3**

### Step 3: Completion Summary [AUTOMATIC]

When all tasks are completed, provide a summary:

```
## Orchestration Complete

**Tasks Completed:** X/Y
**Duration:** ~Z minutes

### Task Results:
- task-001: ✅ Completed (codex)
- task-002: ✅ Completed (gemini)
- ...

### Key Files Changed:
- src/components/Dashboard.tsx
- src/api/orchestration.py
- ...

### Review Findings:
- [Any critical issues found during review]
```

---

## Error Handling

### Task Dispatch Failure

If dispatch_batch.py fails:

1. Check error message
2. If "codeagent-wrapper not found": Ensure it is installed/in PATH, or set `CODEAGENT_WRAPPER=/path/to/codeagent-wrapper` (scripts also probe `./bin/`)
3. If tmux errors (connect/permission/missing): set `CODEAGENT_NO_TMUX=1` and retry
4. If timeout: Retry once, then report to user
5. If other error: Log and continue with remaining tasks

### Review Failure

If dispatch_reviews.py fails:

1. Log the error
2. Continue with next review cycle
3. Report unreviewed tasks in final summary

### Consolidation Failure

If consolidate_reviews.py fails:

1. Log the error
2. Retry once, then continue loop
3. Report tasks stuck in "final_review" in final summary

### Blocked Tasks

If tasks are blocked:

1. Report blocked tasks and their blocking reasons
2. Ask user for resolution if blockers persist after 2 cycles

---

## Agent Assignment

Codex assigns `owner_agent` for each task; scripts only route to the matching backend.

| Task Type | Agent        | Backend            |
| --------- | ------------ | ------------------ |
| Code      | codex        | `--backend codex`  |
| UI        | Gemini       | `--backend gemini` |
| Review    | codex-review | `--backend codex`  |

---

## Dispatch Unit Concept

The orchestrator uses **dispatch units** to optimize task execution. A dispatch unit is the atomic unit of work dispatched to an agent.

### What is a Dispatch Unit?

- **Parent tasks with subtasks**: The parent task becomes the dispatch unit, and all its subtasks are bundled together for sequential execution by a single agent
- **Standalone tasks**: Tasks without subtasks or parent are dispatched individually

### Benefits

1. **Reduced context switching**: Agent receives all related subtasks at once
2. **Better coherence**: Subtasks share context and can reference each other's work
3. **Simplified coordination**: One dispatch per logical work unit instead of per leaf task

### Dispatch Payload Structure

When a dispatch unit is sent to an agent, it includes:

```json
{
  "dispatch_unit_id": "task-001",
  "description": "Parent task description",
  "subtasks": [
    { "task_id": "task-001.1", "title": "First subtask", "details": "..." },
    { "task_id": "task-001.2", "title": "Second subtask", "details": "..." }
  ],
  "spec_path": ".kiro/specs/my-feature"
}
```

### Error Handling

If a subtask fails during execution:

- Completed subtasks are preserved
- Failed subtask and parent are marked as `blocked`
- Resume continues from the failed subtask, not from the beginning

### Backward Compatibility

Flat task files (no hierarchy) work exactly as before - each task is treated as a standalone dispatch unit.

---

## Task State Machine

```
not_started → in_progress → pending_review → under_review → completed
     ↓              ↓
  blocked ←────────┘
```

---

## Example Execution Flow

User: "Start orchestration from spec at .kiro/specs/orchestration-dashboard"

```
[Step 1] Initializing orchestration...
> python init_orchestration.py .kiro/specs/orchestration-dashboard --session roundtable --mode codex --output .
✅ Created TASKS_PARSED.json
✅ Created AGENT_STATE.json (scaffold)
✅ Created PROJECT_PULSE.md (template)

[Step 1b] Codex generated AGENT_STATE.json + PROJECT_PULSE.md

[Step 2] Dispatch cycle 1...
> python dispatch_batch.py AGENT_STATE.json
✅ Dispatched 3 tasks (task-001, task-002, task-003)

> python dispatch_reviews.py AGENT_STATE.json
✅ Dispatched 3 reviews

> python consolidate_reviews.py AGENT_STATE.json
✅ Consolidated 3 final report(s)

> python sync_pulse.py AGENT_STATE.json PROJECT_PULSE.md
✅ PULSE updated

Checking status... 5 tasks incomplete. Continuing...

[Step 2] Dispatch cycle 2...
> python dispatch_batch.py AGENT_STATE.json
✅ Dispatched 2 tasks (task-004, task-005)

... (continues until all complete) ...

[Step 3] Orchestration Complete!
Tasks: 8/8 completed
Duration: ~15 minutes
```

---

## Resources

### scripts/

- `init_orchestration.py` - Parse/validate spec and scaffold TASKS_PARSED.json + AGENT_STATE.json
- `dispatch_batch.py` - Dispatch ready tasks to workers
- `dispatch_reviews.py` - Dispatch review tasks
- `consolidate_reviews.py` - Consolidate review findings into final reports (and trigger fix loop)
- `fix_loop.py` - Fix loop logic for tasks marked fix_required
- `sync_pulse.py` - Sync state to PULSE document
- `spec_parser.py` - Parse tasks.md

### references/

- `agent-state-schema.json` - JSON Schema for AGENT_STATE.json
- `task-state-machine.md` - State transition documentation
