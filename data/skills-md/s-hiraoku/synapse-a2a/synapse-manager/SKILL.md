---
name: synapse-manager
description: >-
  Multi-agent management workflow — task delegation, progress monitoring,
  quality verification with regression testing, feedback delivery, and
  cross-review orchestration. Use this skill when coordinating multiple agents
  on a shared task, monitoring delegated work, or ensuring quality across
  agent outputs.
---

# Synapse Manager

Orchestrate multi-agent work with structured delegation, monitoring, and quality gates.

## When to Use

- Coordinating 2+ agents on related subtasks
- Monitoring progress of delegated work
- Verifying agent outputs (tests, file changes, integration)
- Sending targeted feedback with error details and fix guidance
- Orchestrating cross-review between agents
- Implementing a multi-phase plan (3+ phases or 10+ file changes)
- Executing an implementation plan with multiple deliverables
- Planning agent assignment for multi-file changes across a codebase

## Workflow (7 Steps)

### Step 1: Plan & Setup

Prepare the task board, assess available agents, and fill gaps by spawning.

**FIRST: Check existing agents in the same WORKING_DIR:**
```bash
synapse list
```
Review the output carefully:
- **WORKING_DIR**: Only agents in your directory can collaborate efficiently
- **ROLE**: Match tasks to agents with relevant roles
- **STATUS**: Only READY agents can accept work immediately
- **TYPE**: Prefer delegating to different model types for diverse perspectives

**THEN: Assign tasks to existing agents BEFORE spawning new ones.**
This is more efficient — spawning has overhead (startup, instruction injection, readiness wait).
Only spawn when no existing agent can handle the task, or when you need parallel execution.

**Start as a manager (delegate mode — no file editing):**
```bash
synapse claude --delegate-mode --name Manager --role "task manager"
```

**Use saved agent definitions for consistent team composition:**
```bash
# List available agent definitions
synapse agents list

# Spawn agents from saved definitions
synapse spawn calm-lead
synapse spawn sharp-checker
```

**Spawn with worktree isolation when multiple agents will edit files:**
```bash
synapse spawn claude --worktree --name Impl --role "feature implementation"
synapse spawn gemini -w --name Tester --role "test writer"
```

**Cross-model preference**: Spawn different model types to (1) leverage diverse strengths and
(2) distribute token usage across providers, avoiding rate limits on any single model.

**Wait for readiness:**
```bash
elapsed=0
while ! synapse list | grep -q "Impl.*READY"; do
  sleep 1; elapsed=$((elapsed + 1))
  [ "$elapsed" -ge 30 ] && echo "ERROR: Impl not READY after ${elapsed}s" >&2 && exit 1
done
```

### Step 2: Delegate via Task Board

Use the shared task board for structured task tracking instead of ad-hoc messages.

**Create tasks with priority and dependencies:**
```bash
# Create implementation task (priority 4 = urgent)
synapse tasks create "Implement auth module" \
  -d "Add OAuth2 with JWT in synapse/auth.py. Follow patterns in synapse/server.py." \
  --priority 4

# Create test task, blocked by implementation
synapse tasks create "Write auth tests" \
  -d "Cover: valid login, invalid credentials, token expiry, refresh flow" \
  --blocked-by 1
```

**Assign tasks to agents:**
```bash
synapse tasks assign 1 Impl
synapse tasks assign 2 Tester
```

**Send detailed instructions with file attachments:**
```bash
synapse send Impl "Implement auth module — see task #1 on the board.
- Add OAuth2 flow in synapse/auth.py
- Update server.py with /auth/* endpoints
- Follow existing patterns" --attach synapse/server.py --silent

synapse send Tester "Write auth tests — see task #2 (blocked by #1).
- Prepare test structure now, fill in after impl lands
- Follow pytest patterns in existing tests" --attach tests/test_a2a_compat.py --silent
```

**Key rules:**
- Include specific file names, function names, and acceptance criteria
- Reference existing code patterns the agent should follow
- Use `--attach` to send reference files the agent should study
- Use `--silent` for delegated tasks where you don't need a response
- Use `--wait` if you need immediate results and want to block
- Use `--notify` (default) for async notification on completion

### Step 3: Monitor

Check agent status, task board progress, and work artifacts.

**Live status (auto-updates on registry changes):**
```bash
synapse list
```

**Task board status:**
```bash
synapse tasks list
synapse tasks list --status in_progress
```

**Check task history for completed work:**
```bash
synapse history list --agent Impl
synapse history list --agent Tester
```

**Verify expected output:**
```bash
git diff --name-only
ls tests/test_auth.py synapse/auth.py
```

**Monitoring cadence:**
- Check `synapse list` every 1-2 minutes during active work
- Once an agent shows READY after being PROCESSING, inspect its output
- If an agent stays PROCESSING for >5 minutes, send an interrupt:
  ```bash
  synapse interrupt Impl "Status update — what is your current progress?"
  ```

**Broadcast status check to all agents:**
```bash
synapse broadcast "Status check — report your progress" --priority 4
```

### Step 4: Approve Plans

When agents submit plans for review, use plan approval to gate execution.

**Review and approve:**
```bash
synapse approve <task_id>
```

**Reject with actionable feedback:**
```bash
synapse reject <task_id> --reason "Use refresh tokens instead of long-lived JWTs. See RFC 6749 section 1.5."
```

### Step 5: Verify

Run tests to validate quality. This is the critical quality gate.

**Run new tests first (fast feedback):**
```bash
pytest tests/test_auth.py -v
```

**Then run full regression tests (every time new tests pass):**
```bash
pytest --tb=short -q
```

**Regression triage — distinguish new breakage from pre-existing:**
```bash
git stash
pytest tests/test_failing_module.py -v
git stash pop
```
- If the test **also fails on clean state** → pre-existing issue, not caused by the agent. Note it and continue.
- If the test **passes on clean state** → the agent's changes introduced the regression. Proceed to Step 6 with the diff that caused it.

**Update task board on completion or failure:**
```bash
synapse tasks complete <task_id>
synapse tasks fail <task_id> --reason "test_refresh_token fails — TypeError on line 42"
```

**On test failure:** Identify failing test name and error message, determine if new-test or regression, proceed to Step 6 (Feedback).

### Step 6: Feedback

When issues are found, send concrete, actionable feedback.

**Feedback message structure:**
```bash
synapse send Impl "Issues found — please fix:

1. FAILING TEST: test_token_expiry (tests/test_auth.py)
   ERROR: TypeError: cannot unpack non-iterable NoneType object
   FIX: Add None guard at the top of validate_token()

2. REGRESSION: test_existing_endpoint broke
   ERROR: AssertionError: expected 200, got 401
   CAUSE: auth middleware intercepts all routes
   FIX: Exclude health-check endpoints from auth" --silent
```

**Save lessons learned to shared memory:**
```bash
synapse memory save auth-middleware-pattern \
  "Auth middleware must exclude /status and /.well-known/* endpoints from authentication" \
  --tags auth,middleware --notify
```

**Key rules:**
- Always include the failing test name and exact error
- Always suggest a fix direction (not just "it's broken")
- Distinguish between new-test failures and regressions
- Save recurring patterns to shared memory so other agents learn
- After sending feedback, return to Step 3 (Monitor)

### Step 7: Review & Wrap-up

After all tests pass, orchestrate cross-review and finalize.

**Cross-review with file attachments:**
```bash
synapse send Tester "Review implementation changes. Focus on: correctness, edge cases, naming consistency" \
  --attach synapse/auth.py --wait

synapse send Impl "Review test coverage. Focus on: missing edge cases, test isolation, assertion quality" \
  --attach tests/test_auth.py --wait
```

**Final verification:**
```bash
pytest --tb=short -q
git diff --stat
```

**Trace task history for full audit trail:**
```bash
synapse trace <task_id>
```

**Check token/cost usage:**
```bash
synapse history stats
synapse history stats --agent Impl
synapse history stats --agent Tester
```

**Save key decisions to shared memory:**
```bash
synapse memory save auth-architecture \
  "OAuth2 with JWT + refresh tokens. Auth middleware excludes /status and /.well-known/*." \
  --tags auth,architecture --notify
```

**Mark tasks complete on the board:**
```bash
synapse tasks complete 1
synapse tasks complete 2
```

**Cleanup (MANDATORY — do NOT leave orphaned agents):**
```bash
synapse kill Impl -f
synapse kill Tester -f
# Verify all spawned agents are cleaned up:
synapse list
```

**Report completion:**
- Summarize what was done
- List files changed (`git diff --stat`)
- Confirm all tests pass
- Note any remaining concerns from cross-review
- Reference task board IDs and shared memory keys

## Decision Table

| Situation | Action |
|-----------|--------|
| Agent stuck PROCESSING >5min | `synapse interrupt <name> "Status?"` |
| Need to check all agents at once | `synapse broadcast "Status check" --priority 4` |
| New test fails | Feedback with error + suggested fix |
| Regression test fails | Feedback with cause analysis + fix direction |
| Agent READY but no output | Check `git diff`, re-send task if needed |
| Agent submits a plan | `synapse approve` or `synapse reject --reason "..."` |
| Discovered a reusable pattern | `synapse memory save <key> "<pattern>" --tags ... --notify` |
| Need to check past work | `synapse history list --agent <name>` |
| Need full audit trail | `synapse trace <task_id>` |
| Cross-review finds issue | Send fix request with `--attach`, re-verify |
| All tests pass, reviews clean | `synapse tasks complete`, kill agents, report done |
| Need cost breakdown | `synapse history stats --agent <name>` |

## A2A Features Reference

| Feature | Command | Purpose |
|---------|---------|---------|
| **Task Board** | `synapse tasks create/assign/complete/fail/reopen/list` | Structured task tracking with priorities and dependencies |
| **Plan Approval** | `synapse approve/reject` | Gate execution with review feedback |
| **Shared Memory** | `synapse memory save/search/list/show` | Cross-agent knowledge sharing and pattern retention |
| **History & Tracing** | `synapse history list/show/stats` + `synapse trace` | Audit trail and token/cost tracking |
| **Delegate Mode** | `--delegate-mode` | Manager agent that coordinates without editing files |
| **Broadcast** | `synapse broadcast` | Send to all agents at once |
| **File Attachments** | `--attach file.py` | Send reference files with messages |
| **Saved Agents** | `synapse agents list` + `synapse spawn <id>` | Reusable agent definitions for consistent teams |
| **Priority Levels** | `--priority 1-5` | Control urgency (5 = emergency, bypasses readiness gate) |
| **Soft Interrupt** | `synapse interrupt` | Urgent status check (shorthand for `-p 4 --silent`) |
| **Response Modes** | `--wait / --notify / --silent` | Blocking, async notification, or fire-and-forget |
| **Reply Routing** | `synapse reply` | Auto-routed responses to original sender |
| **Message Files** | `--message-file / --stdin` | Send large messages without shell limits |

## Auto-Approve (Yolo) Mode

Each CLI agent has a **different flag** to skip permission prompts. Pass these after `--` when spawning:

| Agent | Flag | Example |
|-------|------|---------|
| **Claude Code** | `--dangerously-skip-permissions` | `synapse spawn claude -- --dangerously-skip-permissions` |
| **Gemini CLI** | `-y` (or `--yolo`) | `synapse spawn gemini -- -y` |
| **Codex CLI** | `--full-auto` | `synapse spawn codex -- --full-auto` |
| **GitHub Copilot CLI** | `--allow-all-tools` | `synapse spawn copilot -- --allow-all-tools` |
| **OpenCode** | *(no flag available)* | N/A |

!!! note "Codex CLI details"
    `--full-auto` = `-a on-request --sandbox workspace-write` (sandboxed auto-approve).
    For fully unrestricted: `--dangerously-bypass-approvals-and-sandbox`.

**Team start with mixed agents:**
```bash
# Some CLIs silently ignore unknown flags, but others may error.
# When passing shared flags, test that all target agents accept them.
synapse team start claude gemini -- --dangerously-skip-permissions -y
```

!!! warning "Agent-specific flags may cause errors"
    Not all CLIs ignore unknown flags — some will exit with an error. If combining flags fails, start agents individually with their specific flags:
    ```bash
    synapse spawn claude -- --dangerously-skip-permissions
    synapse spawn gemini -- -y
    ```

**Via API:**
```bash
curl -X POST http://localhost:8100/spawn \
  -H "Content-Type: application/json" \
  -d '{"profile": "gemini", "tool_args": ["-y"]}'
```

## Commands Quick Reference

| Command | Purpose |
|---------|---------|
| `synapse list` | Check agent status (auto-updates) |
| `synapse spawn <type\|id> --name <n> --role "<r>"` | Start agent (ad-hoc or from saved definition) |
| `synapse send <name> "<msg>" --silent` | Delegate task (fire-and-forget) |
| `synapse send <name> "<msg>" --wait` | Request reply (blocking) |
| `synapse send <name> "<msg>" --attach <file>` | Send with reference files |
| `synapse broadcast "<msg>" --priority <n>` | Message all agents |
| `synapse interrupt <name> "<msg>"` | Urgent status check (priority 4) |
| `synapse tasks create "<subject>" -d "<desc>" --priority <n>` | Create task on board |
| `synapse tasks assign <id> <agent>` | Assign task |
| `synapse tasks complete <id>` | Mark task done |
| `synapse tasks fail <id> --reason "<why>"` | Mark task failed |
| `synapse approve <id>` | Approve agent plan |
| `synapse reject <id> --reason "<feedback>"` | Reject with guidance |
| `synapse memory save <key> "<content>" --tags <t> --notify` | Share knowledge |
| `synapse memory search "<query>"` | Find shared knowledge |
| `synapse history list --agent <name>` | Check task history |
| `synapse history stats --agent <name>` | Token/cost breakdown |
| `synapse trace <task_id>` | Full audit trail |
| `synapse kill <name> -f` | Terminate agent |

## Worker Agent Guide

When you receive a task from a manager or pick one from the task board:

### On Task Receipt
1. Start work immediately (`[REPLY EXPECTED]` requires a reply; otherwise no reply needed)
2. Check shared knowledge: `synapse memory search "<task topic>"`
3. Lock files before editing: `synapse file-safety lock <file> $SYNAPSE_AGENT_ID`

### During Work
- Report progress if the task takes >5 minutes: `synapse send <manager> "Progress: <update>" --silent`
- Report blockers immediately: `synapse send <manager> "<specific question>" --wait`
- Save findings: `synapse memory save <key> "<finding>" --tags <topic>`
- **You can delegate subtasks too**: If your task has independent parts, spawn helpers
  (prefer different model types to distribute load and avoid rate limits)
- **ALWAYS clean up**: Kill any agents you spawn after their work is done: `synapse kill <name> -f`

### On Completion
1. Update task board: `synapse tasks complete <task_id>`
2. Report to manager: `synapse send <manager> "Done: <change summary>" --silent`
3. Include test results if tests were run

### On Failure
1. Update task board: `synapse tasks fail <task_id> --reason "<reason>"`
2. Report details to manager: `synapse send <manager> "Failed: <error details>" --silent`
3. Do NOT silently move on — the manager needs to know the situation

### When No Manager Exists
If there is no manager/coordinator agent in the team:
- Assess the situation yourself by running `synapse list`
- Coordinate directly with available teammates
- Proactively delegate and spawn agents when it would improve efficiency
- Use `synapse memory` to share decisions and findings with the team
