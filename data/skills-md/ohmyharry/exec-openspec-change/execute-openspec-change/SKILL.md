---
name: execute-openspec-change
description: "Execute an OpenSpec change through the complete automated workflow: design check → plan → worktree → subagent → review → test → merge. Triggered by phrases like /execute or /exec."
---

# OpenSpec Execute Change

## Overview

Automates the complete execution workflow for OpenSpec proposals/changes. This skill orchestrates multiple Superpowers skills to provide a seamless execution experience from proposal to merged code.

**Core principle:** Orchestration + State Management + Superpowers Integration = Reliable Execution.

**Announce at start:** "I'm using the execute-openspec-change skill to execute the [change-id] proposal."

## Trigger Detection

### Supported Trigger Patterns

| Pattern | Example | Match Rule |
|---------|---------|------------|
| Command | `/execute add-subagent-display` | Prefix `/execute` or `/exec` |
| Command | `/exec add-sub` | Short form |
| Natural | `执行 add-subagent-display` | Contains `执行` + change-id |
| Natural | `帮我完成这个变更` | Contains `完成`/`实现` + change-id |
| Natural | `开始实现 fix-permission` | Contains `开始` + change-id |
| Context | `执行这个 change` | Infer from conversation history |

### Intent Recognition Logic

```
1. Extract change-id
   ├─ Explicit: Use directly
   ├─ Context infer: From conversation history/recent files
   └─ Interactive: List options if uncertain

2. Safety checks
   ├─ Verify change-id exists in openspec/changes/
   ├─ Warn if change is archived
   └─ Check if tasks.md exists

3. Parse parameters
   ├─ Mode: auto | guided | debug
   ├─ Test failure strategy: prompt | auto_fix | abort
   └─ Parallel strategy: serial | parallel+detect | domain-isolated
```

### Execution Modes

```
/execute <change-id> --mode=auto     # Fully automated (default)
/execute <change-id> --mode=guided   # Pause at each checkpoint
/execute <change-id> --mode=debug    # Verbose output,随时介入
```

## State Machine

### State Definitions

```
PENDING → DESIGNING → PLANNING → EXECUTING → REVIEWING → TESTING → READY → MERGED/ABANDONED
```

### State Transitions

| Current | Trigger | Next | Action |
|---------|---------|------|--------|
| `PENDING` | Start | `DESIGNING` | Check design.md |
| `DESIGNING` | design.md complete | `PLANNING` | Enter planning |
| `DESIGNING` | design.md incomplete | `DESIGNING` | Run brainstorming |
| `PLANNING` | tasks.md complete | `EXECUTING` | Create worktree |
| `PLANNING` | tasks.md incomplete | `PLANNING` | Run writing-plans + merge |
| `EXECUTING` | All tasks done | `REVIEWING` | Auto trigger code review |
| `REVIEWING` | Review pass | `TESTING` | Run tests |
| `TESTING` | Tests pass | `READY` | Wait for user acceptance |
| `READY` | User confirms merge | `MERGED` | Merge to main |
| `READY` | User aborts | `ABANDONED` | Cleanup worktree |
| `ANY` | User aborts | `ABANDONED` | Keep state for resume |

### State Persistence

```json
// openspec/changes/<id>/.exec-state.json
{
  "change_id": "add-subagent-display",
  "status": "EXECUTING",
  "mode": "auto",
  "worktree_path": "/worktrees/server-add-sub",
  "domain": "server",
  "current_task": 15,
  "total_tasks": 20,
  "checkpoints": [
    {"task": 5, "timestamp": "2026-02-01T10:30:00Z", "summary": "..."},
    {"task": 10, "timestamp": "2026-02-01T11:15:00Z", "summary": "..."}
  ],
  "test_failure_strategy": "prompt",
  "dependencies": ["another-change-id"],
  "created_at": "2026-02-01T10:00:00Z",
  "updated_at": "2026-02-01T11:20:00Z"
}
```

## Phase 1: Design Validation

### Design Completeness Check

```
Check if changes/<id>/design.md exists:
├─ Not exist → Run brainstorming skill
├─ Exists but empty → Run brainstorming skill
├─ Exists but incomplete → Check missing sections, run brainstorming to supplement
└─ Exists and complete → Skip to next phase
```

### Completeness Criteria

design.md must contain these sections to be complete:

```markdown
## Context          [Required]
## Goals / Non-Goals [Required]
## Decisions        [Required]
## Risks / Trade-offs [Optional but recommended]
## Migration Plan   [If needed]
## Open Questions   [If any]
```

**Action:** If incomplete, use `superpowers:brainstorming` to generate/supplement the design.

## Phase 2: Planning

### Smart Merge Logic

```
1. Read existing tasks.md
2. Run writing-plans skill to generate new plan
3. Merge strategy:
   ├─ Keep completed [x] tasks from existing tasks.md
   ├─ Add unique tasks from new plan
   ├─ Update overlapping task descriptions
   └─ Maintain tasks.md format and structure
4. Show merge diff to user, confirm before writing
```

### Task Source Priority

```
1. Completed [x] tasks → Keep
2. New plan tasks → Merge
3. Manual tasks → Keep
4. Conflict tasks → Ask user
```

**Action:** Use `superpowers:writing-plans` to generate plan, then intelligently merge with existing tasks.md.

## Phase 3: Worktree Creation

### Domain Classification

| Domain | Typical Files | Conflict Risk |
|--------|---------------|---------------|
| `server` | `server/*.py`, `server/**/*.py` | Medium (shared state machine) |
| `frontend` | `server/static/*.html`, `server/static/*.js` | Medium (shared API) |
| `openspec` | `openspec/**/*.md` | Low (doc conflicts easy) |
| `config` | `*.json`, `*.plist`, `.env` | High (global config) |
| `tests` | `test_*.py`, `**/*test.py` | Low |

### Worktree Naming

```
/worktrees/<domain>-<change-id-short>/
Example: /worktrees/server-add-sub, /worktrees/frontend-fix-icon
```

**Action:** Use `superpowers:using-git-worktrees` to create isolated workspace.

## Phase 4: Execution

### Execution Flow

```
1. Create Worktree
   ┌─ Call superpowers:using-git-worktrees
   ├─ Smart directory selection
   ├─ Safety verification
   └─ Get worktree path

2. Start Subagent
   ┌─ Call superpowers:subagent-driven-development
   ├─ Pass tasks.md as task list
   ├─ Set checkpoint interval (default: 5 tasks)
   └─ Set interaction level based on mode

3. Monitor Execution
   ┌─ Listen to subagent output
   ├─ Update .exec-state.json progress
   ├─ Handle subagent help requests
   └─ Guided mode: pause at each checkpoint

4. Completion Detection
   ┌─ All tasks.md items marked [x]
   └─ Or subagent reports completion

5. Auto Code Review
   ┌─ Call superpowers:requesting-code-review
   ├─ Compare against proposal.md requirements
   └─ Generate review report
```

### Subagent Configuration

```json
{
  "task_source": "openspec/changes/<id>/tasks.md",
  "checkpoint_interval": 5,
  "mode": "auto",
  "error_handling": "pause_on_error",
  "review_trigger": "on_completion",
  "max_retries": 3
}
```

## Phase 5: Code Review

Auto-triggered after execution completion using `superpowers:requesting-code-review`.

### Review Checklist

```
Comparison:
1. Requirements in proposal.md
2. Actual implementation
3. tasks.md completion status

Verify:
- All requirements implemented
- Code follows project standards
- No obvious bugs or security issues
- Test coverage adequate
```

### Review Report Format

```markdown
# Code Review Report: <change-id>

## ✅ Pass Items
- All tasks.md tasks completed (N/N)
- Code follows standards
- Core functionality correct

## ⚠️ Improvement Suggestions
- file:line - specific suggestion

## 🔴 Blocking Issues
- critical issues that must be fixed

## Conclusion
✅ PASS / ❌ FAIL - Ready for testing / Needs fixes
```

## Phase 6: Testing & Verification

### Test Strategy

```bash
# 1. Automated tests
- Run project test suite (if exists)
- Code style checks
- Static analysis

# 2. Functional verification
- Verify each scenario from proposal.md
- Generate verification report

# 3. Integration tests (if needed)
- Test interaction with other modules
- Test API contracts
```

### Test Failure Handling

| Strategy | Behavior |
|----------|----------|
| `prompt` | Pause, show test failure log, let user decide |
| `auto_fix` | Let subagent attempt to fix (max max_retries) |
| `abort` | Stop immediately, keep worktree for manual fix |

### Verification Report

```markdown
# Verification Report: <change-id>

## Automated Tests
✅ Test Suite: N/N passed
✅ Lint: No issues
✅ Type Check: No issues

## Functional Verification
✅ Scenario 1: description
✅ Scenario 2: description
✅ Scenario 3: description

## Issues
- Any issues found

## Conclusion
✅ READY - Can merge to main / ❌ NOT READY
```

## Phase 7: Merge & Risk Control

### Pre-Merge Report

```
┌─────────────────────────────────────────┐
│ 📋 Pre-Merge Report                      │
├─────────────────────────────────────────┤
│ Change: <change-id>                      │
│ Status: READY ✅                          │
│                                          │
│ Changed files:                           │
│   path/to/file (+N, -M)                 │
│                                          │
│ Affected modules:                        │
│   - Module A                             │
│   - Module B                             │
│                                          │
│ Conflict detection:                      │
│   ✅ No conflicts with other worktrees   │
│   ✅ No breaking changes                 │
│                                          │
│ Dependencies:                            │
│   - None / List                          │
│                                          │
│ Blocked:                                 │
│   - None / List                          │
└─────────────────────────────────────────┘

Choose:
[A] Merge to main now
[B] View detailed diff
[C] Stash (keep worktree)
[D] Abort (delete worktree)
```

### Merge Flow

```
1. Create backup tag
   git tag before-merge-<change-id>-<timestamp>

2. Attempt merge
   git merge worktree-branch

3. If conflict → Pause, let user resolve

4. Merge success → Run quick verification

5. Update status to MERGED

6. Prompt to archive change
```

### Rollback Mechanism

```bash
/rollback before-merge-<change-id>-<timestamp>
```

Keep worktree until user confirms delete (default: 24 hours).

## Status Query & Management

### Query Commands

```bash
/status                           # Show all active worktrees
/status <change-id>               # Show specific change progress
/status --all                     # Include completed
```

### Output Format

```
📊 OpenSpec Execution Status

Active Executions:
  server-add-subagent      [████████░░] 80%  (16/20 tasks)
    ├─ Status: EXECUTING
    ├─ Mode: auto
    ├─ Subagent: Working
    └─ Last activity: 2 min ago

  frontend-fix-icon        [███░░░░░░░░] 30%  (3/10 tasks)
    ├─ Status: EXECUTING (paused)
    ├─ Mode: guided
    ├─ Waiting: User input
    └─ Checkpoint: Waiting confirmation

Ready for Acceptance:
  fix-thinking-bug         [██████████] 100% ✅
    ├─ Status: READY
    ├─ Tests: Pass
    └─ Code Review: Pass

Recently Completed:
  add-config-timeout       ✅ Merged (2 hours ago)
  refactor-session         ✅ Merged (yesterday)
```

## Cleanup & Maintenance

### Cleanup Commands

```bash
/cleanup                           # Detect and clean orphan worktrees
/cleanup --dry-run                 # Preview what will be deleted
/cleanup --force                   # Force cleanup all inactive worktrees
```

### Auto-Cleanup Rules

| Condition | Action |
|-----------|--------|
| Worktree inactive > 7 days | Mark ABANDONED, ask to delete |
| .exec-state.json ABANDONED > 3 days | Auto delete |
| Change archived | Ask to delete worktree |
| Merged > 24 hours | Auto delete worktree |

### Log Management

```
~/.claude/openspec-exec-logs/
  ├── 2026-02-01-<change-id>/
  │   ├── exec.log              # Main flow log
  │   ├── subagent.log          # Subagent output
  │   ├── review.log            # Code review results
  │   ├── test.log              # Test results
  │   └── metadata.json         # Execution metadata
  └── archive/                  # Old logs archive
```

Log retention:
- Successful execution: 30 days
- Failed execution: 90 days
- Archive & compress: Auto compress logs > 7 days

## Dependency Management

### Proposal Extension

```markdown
## Dependencies
- depends_on: add-subagent-display
- blocks: multi-session-support

## Conflicts With
- May conflict with exclusive-state-change (both modify state_machine.py)
```

### Execution Engine Detection

```
1. Parse dependencies
2. Check dependent change status:
   - MERGED → Can execute
   - Not complete → Prompt to complete first, or batch execute
3. Check blocks
   - If changes waiting for current → Prompt when complete
```

### Batch Execution

```bash
/execute add-sub fix-perm --auto-resolve-deps
# Execute multiple changes in dependency order automatically
```

## Error Handling & Recovery

### Interrupt Recovery

```bash
/execute <change-id> --resume
# Resume from interrupted point
```

### Exception Handling

| Exception Type | Handling |
|----------------|----------|
| Subagent crash | Save state, report error, wait for user |
| Worktree conflict | Pause, show conflict details, provide options |
| Test failure | Handle per test_failure_strategy |
| Network/resource | Retry (max 3), pause on failure |
| User interrupt | Save state, support --resume |

### Error Report

```
❌ Execution Interrupted: <change-id>

Error Type: Subagent abnormal exit
Error Message: ...
Location: checkpoint 3, task 1.4

Suggested Actions:
[R] Retry current task
[S] Skip current task, continue next
[A] Abort execution, keep state
[L] View detailed logs
```

## Conflict Detection

### File-Level Conflict

```bash
# Check for file conflicts
git diff --name-only worktree-A | sort > /tmp/A.files
git diff --name-only worktree-B | sort > /tmp/B.files
comm -12 /tmp/A.files /tmp/B.files  # Output conflict files
```

### Semantic-Level Conflict (Enhanced)

```bash
# Check if modifying same functions/classes
# Check if modifying same spec requirements
# Detect introduced breaking changes
```

### Decision Matrix

| Conflict Type | No Conflict | File Conflict | Semantic Conflict |
|---------------|-------------|---------------|-------------------|
| Parallel strategy | Allow | Warn | Block |

## Worktree Registry

```json
// .worktree-registry.json
{
  "active_worktrees": [
    {
      "change_id": "add-subagent-display",
      "path": "/worktrees/server-add-sub",
      "domain": "server",
      "status": "EXECUTING",
      "pid": "subagent-xxx",
      "created_at": "2026-02-01T10:00:00Z",
      "last_activity": "2026-02-01T11:20:00Z"
    }
  ]
}
```

## Integration with Superpowers Skills

| Phase | Superpowers Skill | Purpose |
|-------|-------------------|---------|
| Pre-trigger | superpowers:brainstorming | Generate/supplement design.md |
| Plan | superpowers:writing-plans | Generate execution plan |
| Worktree | superpowers:using-git-worktrees | Create isolated environment |
| Execution | superpowers:subagent-driven-development | Run implementation tasks |
| Review | superpowers:requesting-code-review | Verify code quality |
| Acceptance | superpowers:verification-before-completion | Final verification |

## Quick Reference

| Command | Purpose |
|---------|---------|
| `/execute <id>` | Start execution |
| `/execute <id> --mode=guided` | Guided execution |
| `/execute <id> --resume` | Resume interrupted execution |
| `/status` | Show execution status |
| `/status <id>` | Show specific change status |
| `/cleanup` | Clean up orphan worktrees |
| `/rollback <tag>` | Rollback merge |

## Common Mistakes

### Skipping design completeness check

- **Problem:** Incomplete design leads to implementation gaps
- **Fix:** Always check design.md sections before proceeding

### Not using Superpowers skills

- **Problem:** Reinventing the wheel, inconsistent behavior
- **Fix:** Always delegate worktree, subagent, review to dedicated skills

### Missing state persistence

- **Problem:** Can't resume after interruption
- **Fix:** Always update .exec-state.json at each checkpoint

### Ignoring conflict detection

- **Problem:** Parallel worktrees overwrite each other
- **Fix:** Always check conflicts before starting parallel execution

### Forgetting backup before merge

- **Problem:** Can't rollback if merge causes issues
- **Fix:** Always create tag before merging

## Red Flags

**Never:**
- Skip design.md completeness check
- Create worktree manually (use using-git-worktrees)
- Run subagent without state persistence
- Merge without creating backup tag
- Ignore conflict warnings

**Always:**
- Check design.md completeness first
- Use Superpowers skills for specialized work
- Persist state to .exec-state.json
- Create backup tag before merge
- Check for conflicts before parallel execution
- Handle errors gracefully with recovery options

## Example Workflow

```
User: /execute add-subagent-display

You: I'm using the execute-openspec-change skill to execute the add-subagent-display proposal.

[Detect change exists, check safety]
[Read .exec-state.json - doesn't exist, fresh execution]
[Check design.md - complete]
[Check tasks.md - incomplete, run writing-plans]
[Merge plan with tasks.md]
[Create worktree using using-git-worktrees]
[Start subagent using subagent-driven-development]
[Monitor execution, update checkpoints]
[Execution complete, auto-trigger code-reviewer]
[Review passes, run tests]
[Tests pass, show pre-merge report]
[User selects A: Merge]
[Create backup tag, merge to main]
[Update status to MERGED]
[Archive change]

✅ Execution complete: add-subagent-display
   - Merged to main
   - Worktree cleaned up
   - Change ready for archival
```

---

# Implementation Guide

This section provides concrete implementation steps for the AI agent following this skill.

## Step 1: Trigger Detection & Intent Recognition

### 1.1 Parse User Input

First, determine if the user wants to execute a change:

```python
# Pseudo-code for trigger detection
user_input = get_user_message()

# Check for command-style triggers
if user_input.startswith("/execute") or user_input.startswith("/exec"):
    # Extract change-id and parameters
    parts = user_input.split()
    change_id = parts[1] if len(parts) > 1 else None
    # Parse flags (--mode, --resume, etc.)
    return detected_intent("command", change_id, flags)

# Check for natural language triggers (Chinese/English)
execute_keywords = ["执行", "完成", "实现", "开始", "execute", "complete", "implement", "start"]
if any(keyword in user_input.lower() for keyword in execute_keywords):
    # Extract potential change-id from message
    change_id = extract_change_id_from_message(user_input)
    return detected_intent("natural_language", change_id, {})

# Check for context inference
if "这个" in user_input or "this" in user_input.lower():
    change_id = infer_from_conversation_history()
    return detected_intent("context", change_id, {})
```

### 1.2 Extract Change-ID

```python
def extract_change_id_from_message(message):
    # Try to match known change patterns
    known_changes = list_openspec_changes()

    # Direct match
    for change in known_changes:
        if change in message:
            return change

    # Partial match (e.g., "add-sub" for "add-subagent-display")
    for change in known_changes:
        if message.split()[-1] in change:
            return change

    return None
```

### 1.3 Safety Checks

```bash
# Verify change exists
if [ ! -d "openspec/changes/$CHANGE_ID" ]; then
    # Check if it's archived
    if [ -d "openspec/changes/archive/*/$CHANGE_ID" ]; then
        echo "⚠️ This change is archived. Are you sure you want to execute it?"
        # Ask user confirmation
    else
        echo "❌ Change not found: $CHANGE_ID"
        # List available changes
        openspec list
        exit 1
    fi
fi

# Check if tasks.md exists
if [ ! -f "openspec/changes/$CHANGE_ID/tasks.md" ]; then
    echo "⚠️ No tasks.md found. This change may not be ready for execution."
    echo "   Please create tasks.md first using openspec workflow."
    exit 1
fi
```

## Step 2: State Initialization & Resume Check

### 2.1 Check for Existing Execution State

```python
import json
from pathlib import Path

exec_state_path = Path(f"openspec/changes/{change_id}/.exec-state.json")

if exec_state_path.exists():
    with open(exec_state_path) as f:
        state = json.load(f)

    # Ask user if they want to resume
    if state["status"] in ["EXECUTING", "REVIEWING", "TESTING"]:
        print(f"⚠️ This change has an active execution (status: {state['status']})")
        print(f"   Progress: {state['current_task']}/{state['total_tasks']} tasks")
        # Ask: Resume or restart?

    if "--resume" in flags:
        return resume_from_state(state)
else:
    # Create new state
    state = {
        "change_id": change_id,
        "status": "PENDING",
        "mode": flags.get("--mode", "auto"),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    save_state(state)
```

### 2.2 State Persistence Functions

```python
def save_state(state):
    state["updated_at"] = datetime.now().isoformat()
    with open(f"openspec/changes/{state['change_id']}/.exec-state.json", "w") as f:
        json.dump(state, f, indent=2)

def update_checkpoint(state, task_num, summary):
    if "checkpoints" not in state:
        state["checkpoints"] = []
    state["checkpoints"].append({
        "task": task_num,
        "timestamp": datetime.now().isoformat(),
        "summary": summary
    })
    save_state(state)
```

## Step 3: Design Validation

### 3.1 Check Design Completeness

```bash
DESIGN_MD="openspec/changes/$CHANGE_ID/design.md"

if [ ! -f "$DESIGN_MD" ]; then
    echo "📝 No design.md found. Running brainstorming..."
    # Call brainstorming skill
    use_skill("superpowers:brainstorming")
    exit
fi

# Check for required sections
REQUIRED_SECTIONS=("Context" "Goals" "Decisions")
for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "## $section" "$DESIGN_MD"; then
        echo "⚠️ design.md missing section: $section"
        echo "   Running brainstorming to supplement..."
        use_skill("superpowers:brainstorming", "supplement_design")
        break
    fi
done
```

## Step 4: Planning & Task Merge

### 4.1 Run Writing-Plans if Needed

```python
tasks_path = f"openspec/changes/{change_id}/tasks.md"

# Check if tasks.md is detailed enough
with open(tasks_path) as f:
    tasks_content = f.read()

# Simple heuristic: if < 5 tasks, need more detail
task_count = tasks_content.count("- [ ")
if task_count < 5:
    print(f"📋 tasks.md has only {task_count} tasks. Generating detailed plan...")
    use_skill("superpowers:writing-plans")

    # Now merge the new plan with existing tasks.md
    merge_tasks_with_plan(tasks_path, new_plan)
```

### 4.2 Smart Merge Logic

```python
def merge_tasks_with_plan(existing_path, new_plan_content):
    """Merge new plan with existing tasks.md, preserving completed tasks."""

    with open(existing_path) as f:
        existing = f.read()

    # Extract completed tasks from existing
    completed_tasks = extract_marked_tasks(existing, status="[x]")

    # Extract new tasks from plan
    new_tasks = extract_tasks_from_plan(new_plan_content)

    # Merge: keep completed, add new
    merged = combine_tasks(completed_tasks, new_tasks)

    # Show diff to user
    print_diff(existing, merged)

    if confirm("Apply merged tasks?"):
        with open(existing_path, "w") as f:
            f.write(merged)
```

## Step 5: Worktree Creation

### 5.1 Determine Domain

```python
def infer_domain(change_id):
    """Infer execution domain from change contents."""

    # Check proposal.md for hints
    proposal = read_file(f"openspec/changes/{change_id}/proposal.md")

    if "server" in proposal.lower() or "state_machine" in proposal.lower():
        return "server"
    elif "frontend" in proposal.lower() or "ui" in proposal.lower():
        return "frontend"
    elif "openspec" in proposal.lower():
        return "openspec"
    else:
        return "server"  # Default
```

### 5.2 Call using-git-worktrees

```python
domain = infer_domain(change_id)
worktree_name = f"{domain}-{change_id[:10]}"  # Shortened change-id

print(f"🌳 Creating worktree: {worktree_name}")
use_skill("superpowers:using-git-worktrees", {
    "branch_name": worktree_name,
    "suggested_name": worktree_name
})

# The skill will return the worktree path
# Store it in state
state["worktree_path"] = get_worktree_path(worktree_name)
state["domain"] = domain
save_state(state)
```

## Step 6: Subagent Execution

### 6.1 Start Subagent

```python
state["status"] = "EXECUTING"
save_state(state)

print(f"🤖 Starting subagent execution (mode: {state['mode']})...")
use_skill("superpowers:subagent-driven-development", {
    "task_source": f"openspec/changes/{change_id}/tasks.md",
    "checkpoint_interval": 5,
    "mode": state["mode"],
    "worktree_path": state["worktree_path"]
})
```

### 6.2 Monitor & Update Checkpoints

```python
# This would be called by the subagent at checkpoints
def on_checkpoint(checkpoint_num, summary):
    state["current_task"] = checkpoint_num
    update_checkpoint(state, checkpoint_num, summary)

    # In guided mode, pause for confirmation
    if state["mode"] == "guided":
        show_progress(state)
        if not confirm("Continue to next checkpoint?"):
            # Wait for user to review
            wait_for_user()
```

### 6.3 Handle Completion

```python
def on_completion():
    state["status"] = "REVIEWING"
    save_state(state)
    print("✅ All tasks completed!")
    return trigger_code_review()
```

## Step 7: Code Review

### 7.1 Auto-Trigger Review

```python
def trigger_code_review():
    print("🔍 Running automatic code review...")
    use_skill("superpowers:requesting-code-review", {
        "change_id": change_id,
        "proposal_path": f"openspec/changes/{change_id}/proposal.md",
        "worktree_path": state["worktree_path"]
    })

    # Review result will be returned
    if review["status"] == "PASS":
        state["status"] = "TESTING"
        save_state(state)
        return run_tests()
    else:
        print("⚠️ Code review found issues:")
        print(review["suggestions"])
        # Ask user how to proceed
        return handle_review_feedback(review)
```

## Step 8: Testing

### 8.1 Run Tests

```python
def run_tests():
    print("🧪 Running tests...")

    # Check for test commands in project
    test_commands = detect_test_commands()

    results = []
    for cmd in test_commands:
        result = run_command(cmd, cwd=state["worktree_path"])
        results.append(result)

    # Generate report
    report = generate_test_report(results)

    if report["status"] == "PASS":
        state["status"] = "READY"
        save_state(state)
        return show_merge_report()
    else:
        return handle_test_failure(report, state["test_failure_strategy"])
```

## Step 9: Merge Decision

### 9.1 Generate Pre-Merge Report

```python
def show_merge_report():
    print("📋 Pre-Merge Report")
    print("=" * 50)
    print(f"Change: {change_id}")
    print(f"Status: READY ✅")
    print()

    # Show changed files
    changes = get_git_diff_summary(state["worktree_path"])
    print("Changed files:")
    for file in changes:
        print(f"  {file}")

    # Show conflict detection
    conflicts = check_conflicts_with_active_worktrees()
    if conflicts:
        print("⚠️ Conflicts detected:")
        for conflict in conflicts:
            print(f"  - {conflict}")

    # Present options
    return ask_merge_decision()
```

### 9.2 Execute Merge

```python
def execute_merge(decision):
    if decision == "A":  # Merge now
        # Create backup tag
        tag_name = f"before-merge-{change_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        run_command(f"git tag {tag_name}")

        # Merge worktree branch
        run_command(f"git merge {state['worktree_path']}")

        # Cleanup
        cleanup_worktree(state["worktree_path"])

        state["status"] = "MERGED"
        save_state(state)

        print(f"✅ Merged to main!")
        print(f"   Backup tag: {tag_name}")
        return True
    elif decision == "B":  # View diff
        show_detailed_diff()
        return ask_merge_decision()
    elif decision == "C":  # Stash
        print("💾 Worktree kept. Resume with:")
        print(f"   /execute {change_id} --resume")
        return False
    else:  # Abort
        cleanup_worktree(state["worktree_path"])
        state["status"] = "ABANDONED"
        save_state(state)
        return False
```

## Helper Functions

### Conflict Detection

```python
def check_conflicts_with_active_worktrees():
    """Check for file and semantic conflicts with other active worktrees."""

    active_worktrees = load_worktree_registry()
    my_files = get_modified_files(state["worktree_path"])

    conflicts = []

    for wt in active_worktrees:
        if wt["change_id"] == change_id:
            continue

        other_files = get_modified_files(wt["path"])

        # File-level conflict
        file_conflicts = set(my_files) & set(other_files)
        if file_conflicts:
            conflicts.append({
                "type": "file",
                "with": wt["change_id"],
                "files": list(file_conflicts)
            })

        # TODO: Semantic conflict detection
        # (check same functions, classes, etc.)

    return conflicts
```

### Worktree Registry

```python
def load_worktree_registry():
    registry_path = ".worktree-registry.json"
    if Path(registry_path).exists():
        with open(registry_path) as f:
            return json.load(f)["active_worktrees"]
    return []

def register_worktree(change_id, path, domain):
    """Register a new worktree in the registry."""

    registry_path = ".worktree-registry.json"
    registry = {"active_worktrees": load_worktree_registry()}

    registry["active_worktrees"].append({
        "change_id": change_id,
        "path": path,
        "domain": domain,
        "status": "EXECUTING",
        "created_at": datetime.now().isoformat(),
        "last_activity": datetime.now().isoformat()
    })

    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

def unregister_worktree(change_id):
    """Remove a worktree from the registry."""

    registry = {"active_worktrees": load_worktree_registry()}
    registry["active_worktrees"] = [
        wt for wt in registry["active_worktrees"]
        if wt["change_id"] != change_id
    ]

    with open(".worktree-registry.json", "w") as f:
        json.dump(registry, f, indent=2)
```

## Status Query Implementation

```python
def show_status(change_id=None):
    """Show execution status for one or all changes."""

    if change_id:
        # Show specific change
        state_path = f"openspec/changes/{change_id}/.exec-state.json"
        if Path(state_path).exists():
            with open(state_path) as f:
                state = json.load(f)
            print_change_status(state)
        else:
            print(f"No execution state found for: {change_id}")
    else:
        # Show all active
        show_all_statuses()

def show_all_statuses():
    """Display status dashboard."""

    print("📊 OpenSpec Execution Status")
    print("=" * 60)
    print()

    # Group by status
    by_status = group_changes_by_status()

    if by_status.get("EXECUTING"):
        print("Active Executions:")
        for state in by_status["EXECUTING"]:
            print_execution_status(state)

    if by_status.get("READY"):
        print("Ready for Acceptance:")
        for state in by_status["READY"]:
            print_ready_status(state)

    if by_status.get("MERGED"):
        print("Recently Completed:")
        for state in by_status["MERGED"][-3:]:  # Last 3
            print_merged_status(state)
```

## Logging

```python
import logging
from datetime import datetime

log_dir = Path.home() / ".claude" / "openspec-exec-logs" / datetime.now().strftime("%Y-%m-%d") / change_id
log_dir.mkdir(parents=True, exist_ok=True)

exec_log = logging.getLogger("exec")
exec_log.addHandler(logging.FileHandler(log_dir / "exec.log"))

subagent_log = logging.getLogger("subagent")
subagent_log.addHandler(logging.FileHandler(log_dir / "subagent.log"))

review_log = logging.getLogger("review")
review_log.addHandler(logging.FileHandler(log_dir / "review.log"))

test_log = logging.getLogger("test")
test_log.addHandler(logging.FileHandler(log_dir / "test.log"))
```

## Dependency Management

### Parse Dependencies from Proposal

```python
import re

def parse_dependencies(change_id):
    """Extract dependencies from proposal.md."""

    proposal_path = f"openspec/changes/{change_id}/proposal.md"

    if not Path(proposal_path).exists():
        return {"depends_on": [], "blocks": [], "conflicts": []}

    with open(proposal_path) as f:
        content = f.read()

    deps = {
        "depends_on": [],
        "blocks": [],
        "conflicts": []
    }

    # Parse ## Dependencies section
    if "## Dependencies" in content:
        deps_section = content.split("## Dependencies")[1].split("\n##")[0]

        for line in deps_section.split("\n"):
            if "depends_on:" in line or "- depends_on:" in line:
                dep = re.search(r'[-:]?\s*depends_on:\s*([\w-]+)', line)
                if dep:
                    deps["depends_on"].append(dep.group(1))

            if "blocks:" in line or "- blocks:" in line:
                block = re.search(r'[-:]?\s*blocks:\s*([\w-]+)', line)
                if block:
                    deps["blocks"].append(block.group(1))

    # Parse ## Conflicts With section
    if "## Conflicts With" in content:
        conflicts_section = content.split("## Conflicts With")[1].split("\n##")[0]
        # Extract conflict information
        deps["conflicts_description"] = conflicts_section.strip()

    return deps
```

### Check Dependency Status

```python
def check_dependencies_satisfied(change_id):
    """Check if all dependencies are satisfied."""

    deps = parse_dependencies(change_id)

    if not deps["depends_on"]:
        return {"satisfied": True, "blocking": []}

    blocking = []
    for dep_id in deps["depends_on"]:
        dep_state = get_change_state(dep_id)

        if dep_state["status"] != "MERGED":
            blocking.append({
                "change_id": dep_id,
                "status": dep_state["status"],
                "state": dep_state
            })

    return {
        "satisfied": len(blocking) == 0,
        "blocking": blocking
    }

def get_change_state(change_id):
    """Get the current state of a change."""

    # Check exec-state.json
    exec_state_path = f"openspec/changes/{change_id}/.exec-state.json"

    if Path(exec_state_path).exists():
        with open(exec_state_path) as f:
            return json.load(f)

    # Check if change exists but never executed
    if Path(f"openspec/changes/{change_id}").exists():
        return {"status": "PENDING", "change_id": change_id}

    # Change doesn't exist
    return {"status": "NOT_FOUND", "change_id": change_id}
```

### Dependency Validation Before Execution

```python
def validate_dependencies(change_id):
    """Validate dependencies before starting execution."""

    deps = parse_dependencies(change_id)
    check = check_dependencies_satisfied(change_id)

    if not check["satisfied"]:
        print("⚠️ Dependencies not satisfied:")
        for block in check["blocking"]:
            print(f"  - {block['change_id']} (status: {block['status']})")

        print()
        print("Options:")
        print("  [1] Execute dependencies first (recommended)")
        print("  [2] Execute anyway (may cause issues)")
        print("  [3] Cancel")

        choice = ask_user_choice()

        if choice == "1":
            return execute_dependencies_first(change_id, check["blocking"])
        elif choice == "2":
            print("⚠️ Proceeding despite unsatisfied dependencies...")
            return True
        else:
            return False

    return True
```

### Execute Dependencies First

```python
def execute_dependencies_first(change_id, blocking_deps):
    """Execute blocking dependencies in order."""

    # Sort by dependencies (topological sort)
    execution_order = topological_sort(blocking_deps)

    print(f"📋 Will execute dependencies in order:")
    for i, dep in enumerate(execution_order, 1):
        print(f"  {i}. {dep['change_id']}")

    if not confirm("Proceed?"):
        return False

    # Execute each dependency
    for dep in execution_order:
        print(f"\n🔄 Executing dependency: {dep['change_id']}")
        result = execute_change(f"/execute {dep['change_id']}")

        if result["status"] != "MERGED":
            print(f"❌ Dependency {dep['change_id']} failed to complete")
            return False

    # All dependencies satisfied, now execute original change
    print(f"\n✅ All dependencies satisfied. Executing: {change_id}")
    return True

def topological_sort(changes):
    """Sort changes topologically by dependencies."""

    # Simple implementation - for complex cases use proper algorithm
    sorted_changes = []
    visited = set()

    def visit(change):
        if change["change_id"] in visited:
            return
        visited.add(change["change_id"])

        # Visit dependencies first
        deps = parse_dependencies(change["change_id"])["depends_on"]
        for dep_id in deps:
            dep_state = get_change_state(dep_id)
            if dep_state["status"] != "MERGED":
                visit(dep_state)

        sorted_changes.append(change)

    for change in changes:
        visit(change)

    return sorted_changes
```

### Notify Blocked Changes

```python
def notify_blocked_changes(change_id):
    """Notify changes that are blocked by this change."""

    # Scan all changes to find ones blocked by current change
    all_changes = list_all_changes()

    for other_id in all_changes:
        if other_id == change_id:
            continue

        deps = parse_dependencies(other_id)

        if change_id in deps["depends_on"]:
            print(f"ℹ️ Change '{other_id}' is waiting for '{change_id}' to complete")

            # Update its state to indicate it's unblocked
            other_state_path = f"openspec/changes/{other_id}/.exec-state.json"
            if Path(other_state_path).exists():
                with open(other_state_path) as f:
                    other_state = json.load(f)

                if "unblocked_dependencies" not in other_state:
                    other_state["unblocked_dependencies"] = []

                other_state["unblocked_dependencies"].append(change_id)

                with open(other_state_path, "w") as f:
                    json.dump(other_state, f, indent=2)
```

### Batch Execution with Auto-Resolve

```python
def batch_execute(change_ids, auto_resolve_deps=True):
    """Execute multiple changes, resolving dependencies automatically."""

    # Parse all dependencies
    all_deps = {}
    for cid in change_ids:
        all_deps[cid] = parse_dependencies(cid)

    # Build dependency graph
    graph = build_dependency_graph(change_ids, all_deps)

    # Topological sort
    execution_order = topological_sort_graph(graph)

    print(f"📋 Batch execution order:")
    for i, cid in enumerate(execution_order, 1):
        print(f"  {i}. {cid}")

    if not confirm("Proceed with batch execution?"):
        return False

    # Execute in order
    results = {}
    for cid in execution_order:
        print(f"\n🔄 Executing: {cid}")
        result = execute_change(f"/execute {cid}")
        results[cid] = result

        if result["status"] != "MERGED" and auto_resolve_deps:
            print(f"❌ {cid} failed, stopping batch execution")
            break

    return results

def build_dependency_graph(change_ids, all_deps):
    """Build a dependency graph for topological sorting."""

    graph = {cid: [] for cid in change_ids}

    for cid in change_ids:
        for dep_id in all_deps[cid]["depends_on"]:
            if dep_id in change_ids:
                graph[dep_id].append(cid)

    return graph

def topological_sort_graph(graph):
    """Topological sort using Kahn's algorithm."""

    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue = [node for node in graph if in_degree[node] == 0]
    result = []

    while queue:
        node = queue.pop(0)
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(graph):
        raise ValueError("Circular dependency detected")

    return result
```

### Integration with Main Execution Flow

```python
def execute_change(user_input):
    """Main execution entry point with dependency support."""

    # Step 1: Parse intent
    intent = parse_intent(user_input)
    change_id = intent["change_id"]
    flags = intent.get("flags", {})

    # Step 1.5: Validate dependencies
    if not validate_dependencies(change_id):
        print("❌ Execution cancelled due to unsatisfied dependencies")
        return None

    # Step 2: Check state / resume
    state = get_or_create_state(change_id, flags)

    if flags.get("--resume") and state["status"] != "PENDING":
        return resume_execution(state)

    # ... rest of execution flow ...

    # On completion, notify blocked changes
    if state["status"] == "MERGED":
        notify_blocked_changes(change_id)

    return state
```

## Complete Execution Flow

```python
def execute_change(user_input):
    """Main execution entry point."""

    # Step 1: Parse intent
    intent = parse_intent(user_input)
    change_id = intent["change_id"]
    flags = intent.get("flags", {})

    # Step 2: Check state / resume
    state = get_or_create_state(change_id, flags)

    if flags.get("--resume") and state["status"] != "PENDING":
        return resume_execution(state)

    # Step 3: Design validation
    validate_design(change_id)

    # Step 4: Planning
    ensure_detailed_tasks(change_id)

    # Step 5: Worktree
    create_worktree(state)

    # Step 6: Execute
    run_subagent(state)

    # Step 7: Review
    run_code_review(state)

    # Step 8: Test
    run_tests(state)

    # Step 9: Merge decision
    handle_merge_decision(state)

    return state
```

This implementation guide provides the concrete steps for each phase of the execution workflow. The AI agent should follow these steps in order, adapting as needed based on user feedback and execution context.
