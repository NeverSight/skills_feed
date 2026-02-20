---
name: orchestrate
description: Coordinate parallel agent teams to execute multi-task implementation plans. Use when running phase tasks from the task plan, parallelizing independent implementation work, or executing custom plan files. Supports interactive (in-session TeamCreate agents) and headless (claude -p fire-and-forget processes) execution modes with task ledger tracking, heartbeat monitoring, budget control, and wave-based quality gates.
---

# Orchestrate

Coordinate a team of parallel agents to execute a phase from the task plan. Manages task assignment, heartbeat monitoring, verification, scope enforcement, and wave transition quality gates.

Supports two execution modes:

- **Interactive** (default): In-session agents via TeamCreate/Task/SendMessage — good for complex tasks needing inter-agent coordination
- **Headless** (`--headless`): Independent `claude -p` processes — good for parallelizable tasks with clear scope boundaries, ~54% less coordination overhead

## Resource Loading

**MANDATORY at Step 2**: Read `agent-roles.md` to determine role assignments and model selection.
**MANDATORY at Step 3H.2a** (headless only): Read `prompt-templates/{role}.md` for each task's role to build the system prompt.
**MANDATORY at wave transitions**: Read `wave-template.md` for the pre/during/post checklist.
**Reference only**: `headless-runner.md` — consult for `claude -p` flag details, output JSON format, or error classification.
**Do NOT Load** prompt templates in interactive mode — agents invoke `/quality-commit` and `/tdd` directly.

## Critical Anti-Patterns

NEVER let parallel agents run `git add && git commit` without flock — git's index file is process-global, and concurrent writes silently mix staged files between commits. Symptom: commit A contains files from task B. Recovery requires interactive rebase. This is why every agent system prompt includes `flock /tmp/orchestrate/{session-id}/git.lock`.

NEVER skip the file overlap check (3H.2b) — two agents editing the same file produces merge conflicts that neither agent can resolve because they have no knowledge of each other's changes. The orchestrator must detect overlap at plan time and serialize conflicting tasks.

NEVER trust `is_error` field alone for failure detection — budget exhaustion sets `is_error: false` with `subtype: "error_max_budget_usd"`. Always check `subtype.startsWith("error_")` instead. This was confirmed via live testing of `claude -p --output-format json`.

NEVER reuse PID files across waves — process IDs are recycled by the OS. Always clear `/tmp/orchestrate/{session-id}/task-*.pid` between waves, or a stale PID could match an unrelated process, causing the monitor loop to wait indefinitely for a process that already exited.

NEVER spawn headless agents without `--no-session-persistence` — without this flag, each `claude -p` process writes a session file to `~/.claude/`. With 22 parallel tasks, this creates 22 orphaned session files that consume disk and pollute session history.

NEVER use `--dangerously-skip-permissions` without `--allowedTools` — the skip-permissions flag alone gives agents unrestricted tool access including TeamCreate, SendMessage, and Task (which could spawn recursive agents). Always pair with `--allowedTools "Bash Edit Write Read Glob Grep"` to restrict to safe tools.

NEVER let a headless agent's commit go unverified — even if the process exits with `subtype: "success"`, the agent may have committed to the wrong branch, touched out-of-scope files, or produced a commit that breaks the build. Always run the full verification chain (3H.2e): commit exists → scope check → verify command.

## Steps

### 1. Parse Arguments

Extract the orchestration target from `$ARGUMENTS`:

- **Phase ID** (e.g., `A`, `B`, `D`): Load tasks from `.claude/reference/phase-10-task-plan.md` for that phase
- **Plan file path** (e.g., `docs/plans/my-plan.md`): Parse tasks from the given file
- **Inline task list** (e.g., `"task1; task2; task3"`): Create tasks from semicolon-separated descriptions

Flags:

- **`--headless`**: Spawn independent `claude -p` processes instead of in-session agents
- **`--interactive`**: Explicit flag for in-session TeamCreate-based mode (default if neither flag given)
- **`--dry-run`**: Parse and display tasks without spawning agents (works with both modes)
- **`--wave N`**: Start from wave N (skip earlier waves, assumes they're complete)
- **`--max-agents N`**: Cap agent count (default: 5)
- **`--budget-per-task N`**: Override per-task budget cap in USD (default: role-based from `agent-roles.md`)
- **`--timeout-multiplier N`**: Scale timeout thresholds (default: 2x estimated duration)
- **`--no-qa`**: Skip spawning a dedicated QA watcher (not recommended, interactive mode only)
- **`--verbose`**: Print all agent messages to the user (noisy but useful for debugging)

If no arguments, ask the user what to orchestrate.

### 2. Initialize Task Ledger

For each task in the plan, use `TaskCreate` with:

- `subject`: Task title (e.g., "A-1.01 Update patch/minor runtime deps")
- `description`: Full task spec including files to modify, verification command, and agent instructions
- `activeForm`: Present-continuous description (e.g., "Updating runtime dependencies")
- `metadata`:
  ```json
  {
  	"role": "backend-impl",
  	"agent_type": "sonnet",
  	"phase": "A",
  	"wave": "1",
  	"task_id": "A-1.01",
  	"estimated_duration": "20m",
  	"verify_command": "pnpm install && pnpm build",
  	"files": "package.json (root, api, frontend)",
  	"status_detail": "pending"
  }
  ```

Assign roles using the rules in `agent-roles.md`. The `role` field determines which prompt template to use and which model to select.

Set up `blockedBy` dependencies from the task plan's **Depends** column using `TaskUpdate`.

Print a summary:

```
Phase A: Dependency Updates + Fastify Hardening
  Mode: headless (claude -p)
  22 tasks (6 haiku, 16 sonnet) across 3 waves
  Wave 1: 6 tasks (all haiku, all parallel)
  Wave 2: 12 tasks (1 haiku, 11 sonnet)
  Wave 3: 4 tasks (2 haiku, 2 sonnet)
  Estimated: ~13 hours agent work
  Budget: $78 (22 tasks × avg $3.55)
```

### 3. Mode Router

Branch based on the execution mode flag:

- **`--headless`** → Go to **Step 3H: Headless Execution**
- **`--interactive`** (or default) → Go to **Step 3I: Interactive Execution**

---

## Step 3H: Headless Execution

### 3H.1 — Setup

Create session directory:

```bash
SESSION_ID=$(date +%s)-$(head -c 4 /dev/urandom | xxd -p)
mkdir -p /tmp/orchestrate/$SESSION_ID
touch /tmp/orchestrate/$SESSION_ID/git.lock
```

Record session metadata: phase, start time, budget cap, max agents.

### 3H.2 — Wave Execution

For each wave (starting from `--wave N` or wave 1):

#### a. Generate Prompts

For each task in the wave:

1. Determine the task's role from metadata (e.g., `backend-impl`)
2. Read the role-specific system prompt from `prompt-templates/{role}.md`
3. Build the task prompt by replacing template variables:
   - `{{TASK_DESCRIPTION}}` → task title + full description from ledger
   - `{{TASK_FILES}}` → files list from metadata
   - `{{VERIFY_COMMAND}}` → verification command from metadata
   - `{{COMPLETED_CONTEXT}}` → commit hashes + changed file summaries from completed tasks
   - `{{GIT_LOCK_PATH}}` → `/tmp/orchestrate/{session-id}/git.lock`
4. If context from completed tasks is large, pre-read relevant code snippets and include them (truncate to keep total prompt under 20K tokens)
5. Save prompt to `/tmp/orchestrate/{session-id}/task-{id}.prompt`

If `--dry-run`: Print all generated prompts and exit.

#### b. File Overlap Check

For each pair of concurrent tasks in the wave:

```
If task_A.files ∩ task_B.files ≠ ∅:
  Serialize: task_B.blockedBy += task_A
  Log: "Serializing {task_B} after {task_A} due to file overlap: {overlapping files}"
```

#### c. Spawn Processes

For each unblocked task (up to `--max-agents` concurrent):

```bash
claude -p \
  --model {role.model} \
  --system-prompt "$(cat /tmp/orchestrate/$SESSION_ID/task-$TASK_ID.prompt)" \
  --allowedTools "Bash Edit Write Read Glob Grep" \
  --dangerously-skip-permissions \
  --max-budget-usd {budget} \
  --output-format json \
  --no-session-persistence \
  "{task description}" \
  > /tmp/orchestrate/$SESSION_ID/task-$TASK_ID.json 2>&1 &

echo $! > /tmp/orchestrate/$SESSION_ID/task-$TASK_ID.pid
date -u +%Y-%m-%dT%H:%M:%SZ > /tmp/orchestrate/$SESSION_ID/task-$TASK_ID.start
echo "running" > /tmp/orchestrate/$SESSION_ID/task-$TASK_ID.status
```

Update task ledger: `TaskUpdate` → `status: in_progress`.

#### d. Monitor Loop

Poll every 10 seconds until all wave tasks complete:

1. **Check PIDs**: `kill -0 $PID 2>/dev/null` for each running task
2. **If process exited**:
   - Read output JSON from `task-{id}.json`
   - Parse `is_error`, `total_cost_usd`, `num_turns`, `result`
   - Update task status file
3. **Timeout check**: If elapsed time > (estimated_duration × timeout_multiplier):
   - `kill $PID` (SIGTERM)
   - Wait 10s, then `kill -9 $PID` if still running
   - Mark as `timed_out`
4. **Budget check**: If `total_cost_usd` > task budget:
   - Already enforced by `--max-budget-usd`, but log the event
5. **Status report** (every 30 seconds):

```
+----------------------------------------------------+
| Phase A — Wave 1 (Headless)     [3/6 complete]     |
+----------------------------------------------------+
| A-1.01 backend-1   DONE   $0.42  (12 turns, 45s)  |
| A-1.02 backend-2   DONE   $0.38  (10 turns, 39s)  |
| A-1.03 qa-1        DONE   $0.15  (8 turns, 22s)   |
| A-1.04 frontend-1  RUN    $0.21  (6 turns, 31s)   |
| A-1.05 mastra-1    RUN    $0.18  (5 turns, 28s)   |
| A-1.06 docs-1      RUN    $0.08  (3 turns, 15s)   |
+----------------------------------------------------+
| Budget: $1.42 / $21.30 session                     |
+----------------------------------------------------+
```

#### e. Verify Completed Tasks

For each task whose process exited successfully:

1. **Check for error**: If `is_error: true` → enter failure escalation (3H.3)
2. **Check new commit**: `git log --oneline --since="{start_time}" -- {task.files}`
   - If no commit found → failure escalation with "no commit produced"
3. **Scope check**: `git diff --name-only HEAD~1` — verify only task files were touched
   - If out-of-scope files modified → `git revert HEAD --no-edit`, then failure escalation
4. **Run verify command**: Execute `task.verify_command`
   - If fails → failure escalation with verify output
5. **On success**:
   - `TaskUpdate` → `status: completed`, add commit hash to metadata
   - Reclaim semaphore slot
   - If more unblocked tasks in wave → spawn next process (back to c.)

#### f. Wave Quality Gate

When all tasks in the wave are complete:

```bash
pnpm build && npx vitest run && pnpm lint
```

Read the full wave checklist from `wave-template.md`.

- **Gate passes** → Move to next wave (back to 3H.2)
- **Gate fails** → Create a fix task, spawn a sonnet agent to fix it, re-run gate

### 3H.3 — Failure Escalation

Three-tier escalation for failed tasks:

**Tier 1 — Retry with context** (up to 2 retries):

- Append error output and the agent's result text to the original prompt
- Add prefix: "Previous attempt failed with the following error. Fix the issue and try again."
- Re-spawn with same model and budget

**Tier 2 — Model escalation** (after 2 retries fail):

- Escalate model: haiku → sonnet, sonnet → opus
- Escalate budget: original × 1.5
- Add prefix: "This task failed with a weaker model. You are a stronger model brought in to resolve it. Here is the full error history: ..."
- Re-spawn with escalated model

**Tier 3 — User intervention** (if model escalation also fails):

- Print failure details: task description, error output, retry history
- Offer choices:
  - **Skip**: Mark task as skipped, continue with remaining tasks (may break downstream)
  - **Manual fix**: Pause orchestration, let user fix manually, then resume
  - **Abort**: Stop the entire orchestration

### 3H.4 — Git Safety for Parallel Agents

**flock-based locking**: All agent system prompts include flock instructions. The orchestrator creates the lock file at setup (3H.1).

**File overlap detection**: Handled at prompt generation time (3H.2b). Overlapping tasks are serialized.

**Post-hoc scope verification**: After each task (3H.2e step 3). Out-of-scope commits are reverted.

**Git worktrees** (for high-overlap phases): If >50% of wave tasks share files, fall back to worktree isolation:

```bash
git worktree add /tmp/orchestrate/$SESSION_ID/worktree-$TASK_ID -b temp/$TASK_ID
# Agent works in the worktree directory
# Orchestrator merges back: git merge temp/$TASK_ID
```

---

## Step 3I: Interactive Execution

### 3I.1 — Create Team

Use `TeamCreate` with a descriptive name derived from the phase:

- Phase A → team name `phase-A-foundation`
- Phase B → team name `phase-B-package-split`
- Custom plans → team name from `$ARGUMENTS` or prompt user

### 3I.2 — Spawn Specialist Agents

Determine agent count from max parallelism in the current wave (capped by `--max-agents`).

Assign roles using `agent-roles.md` rules based on task file paths and metadata.

Spawn agents via the `Task` tool with:

- `team_name`: The team name from above
- `subagent_type`: `general-purpose` (all agents need full tool access)
- `model`: From the task's role definition in `agent-roles.md`
- `name`: Role-based naming: `{role}-{N}` (e.g., `backend-1`, `qa-1`, `security-1`)

Always spawn one `qa-1` agent for continuous QA watching (per the QA Watcher Protocol) unless `--no-qa` is set.

Agent spawn prompt template:

```
You are {name}, a {role} specialist on team "{team_name}".

Your role: Execute assigned tasks from the task ledger. For each task:
1. Acknowledge receipt immediately via SendMessage to the team lead
2. Read full task details with TaskGet
3. Implement the task following your role's domain knowledge
4. Run quality gates: lint → typecheck → test (per workspace)
5. Stage specific files and commit with conventional message format
6. Report completion with commit hash via SendMessage
7. Check TaskList for your next assignment

QA protocol: After every Edit/Write, notify qa-1 with changed file paths.
Scope: ONLY work on your assigned task. If you discover related work, report it — do not expand scope.
Git: Stage ONLY specific files. Never git add -A or git add .
```

### 3I.3 — Assign First Wave

Read `TaskList` to find unblocked, unassigned tasks matching the current wave.

For each idle agent:

1. Find a matching task (match role → agent specialization)
2. Use `TaskUpdate` to set `owner` and `status: in_progress`
3. Update metadata: `{ "assigned_at": "<ISO timestamp>", "status_detail": "assigned" }`
4. Send task details via `SendMessage` including:
   - Task ID and title
   - Files to modify
   - Verification command
   - Any dependencies or context from completed tasks

### 3I.4 — Monitor Loop

Run until all tasks in all waves are complete.

#### On Agent Message Received

**Acknowledgment** → Update metadata:

```json
{ "status_detail": "in_progress", "last_heartbeat": "<ISO timestamp>" }
```

**Completion claim** → Verify before marking done:

1. Check commit exists: Ask agent for commit hash, verify with `git log --oneline -1 <hash>`
2. Run the task's `verify_command` from metadata
3. If verified:
   - `TaskUpdate` → `status: completed`
   - Assign next unblocked task from the wave (or next wave if current is done)
4. If not verified:
   - Send specific feedback about what failed
   - Keep task `in_progress`

**Issue report** → Assess severity:

- Blocking: Create a fix task, assign to available agent
- Non-blocking: Log and continue
- Scope creep: Redirect agent back to assigned task

#### Progressive Stall Escalation

Replace flat 90s heartbeat with progressive escalation:

| Timer | Action                                                            |
| ----- | ----------------------------------------------------------------- |
| 60s   | Ping: "Status check — what are you working on?"                   |
| 120s  | Warning: "No response in 2min. Will reassign in 60s."             |
| 180s  | Reassign: Mark stalled, spawn replacement agent with task context |

When reassigning:

- Update metadata: `{ "status_detail": "stalled", "reassigned_from": "<agent-name>" }`
- Send the stalled agent a shutdown request
- Spawn replacement with the same role, include: "Previous agent stalled. Pick up where they left off."

#### Scope Enforcement

If an agent reports working on files NOT listed in their task's `files` metadata:

1. Send a stop message: "You're modifying files outside your task scope. Please revert and focus on: {task files}"
2. If repeated: Reassign the task to a different agent

#### Status Report

Print every 3 minutes (or when the user asks):

```
+------------------------------------------+
| Phase A — Wave 2 Progress                |
+------------------------------------------+
| Completed: 6/12  | In Progress: 3       |
| Stalled: 0       | Pending: 3           |
+------------------------------------------+
| backend-1:  A-2.04 Valkey cache     [##-]|
| backend-2:  A-2.10 OracleStore      [#--]|
| qa-1:       A-2.11 knip CI          [###]|
| qa-2:       watching (last: PASS)        |
+------------------------------------------+
```

### 3I.5 — Improved Shutdown Protocol

When a phase or the entire orchestration completes:

1. Send `shutdown_request` to all agents via `SendMessage`
2. Wait 30s for responses
3. Re-send `shutdown_request` to non-responders
4. Wait 15s
5. `TeamDelete` to force cleanup of any remaining agents

---

## 4. Wave Transition Gate

When all tasks in a wave are complete (applies to both modes):

1. Run full quality gate:

   ```bash
   pnpm build && npx vitest run && pnpm lint
   ```

2. If the phase's wave has a specific **Gate** command (from the task plan), run that too
3. **Gate passes** → Move to next wave, assign new tasks
4. **Gate fails** → Diagnose the failure, create a fix task, assign to an available agent (or spawn a headless fix agent)

Read the wave checklist from `wave-template.md` for the full pre/during/post checklist.

## 5. Phase Completion

When all waves are complete:

1. Run the phase's final verification (from the task plan's last wave Gate)
2. Run `/health-check --quick` for a comprehensive quality check
3. Print final summary:

   ```
   Phase A Complete
     Mode: headless
     Tasks: 22/22 completed (2 retried, 0 skipped)
     Duration: 2h 15m
     Cost: $34.20 / $78.00 budget
     Agents: 5 concurrent max
     Commits: 22
     Issues: 1 scope violation (reverted + retried), 1 timeout (escalated to sonnet)
     Quality: All gates passed
   ```

4. **Interactive mode**: Shut down all agents via the shutdown protocol (3I.5)
5. **Headless mode**: Clean up session directory: `rm -rf /tmp/orchestrate/$SESSION_ID`

## 6. Cross-Phase Handoff

If more phases are queued (following the Phase Dependency DAG):

1. Check which phases are now unblocked (e.g., after A completes → B, D, F are unblocked)
2. For parallel phases, set up git worktrees per the Git Worktree Parallelization Strategy:

   ```bash
   git worktree add ../portal-phase-{X} phase-10/{X}-{name}
   cd ../portal-phase-{X} && pnpm install
   ```

3. Start a new orchestration cycle for each unblocked phase
4. Report to user which phases are starting in parallel

## Arguments

See **Step 1: Parse Arguments** for the full flag reference. Summary: `$ARGUMENTS` accepts a Phase ID, plan file path, or inline task list, plus optional flags `--headless`, `--interactive`, `--dry-run`, `--wave N`, `--max-agents N`, `--budget-per-task N`, `--timeout-multiplier N`, `--no-qa`, `--verbose`.

## Integration Points

### Role Registry

- **`agent-roles.md`** — Maps tasks to specialist roles (model, budget, prompt template)

### Prompt Templates

- **`prompt-templates/backend-impl.md`** — Fastify 5 routes, plugins, services
- **`prompt-templates/frontend-impl.md`** — SvelteKit pages, components, stores
- **`prompt-templates/mastra-impl.md`** — Mastra agents, RAG, tools, workflows
- **`prompt-templates/security-reviewer.md`** — OWASP + Oracle security review
- **`prompt-templates/qa-lead.md`** — TDD, test writing, QA watching
- **`prompt-templates/doc-sync.md`** — Documentation sync

### Headless Runner Reference

- **`headless-runner.md`** — `claude -p` flags, output format, concurrency model, error classification

### Referenced Skills

- **`/quality-commit`** — Agents use this for each task's commit step (interactive mode)
- **`/tdd`** — Agents use this for implementation tasks needing test coverage (interactive mode)
- **`/health-check`** — Run at phase completion for comprehensive validation

### Referenced Protocols

- **QA Watcher Protocol** — `.claude/reference/phase-10-task-plan.md` section "Continuous QA Watcher Protocol"
- **Git Worktree Strategy** — `.claude/reference/phase-10-task-plan.md` section "Git Worktree Parallelization Strategy"
- **Phase Dependency DAG** — A→B→C, A→D, A→F, B→E (from task plan header)

### Claude Code Native Tools Used

**Interactive mode**:

- `TeamCreate` / `TeamDelete` — Team lifecycle
- `TaskCreate` / `TaskUpdate` / `TaskList` / `TaskGet` — Ledger operations
- `SendMessage` — Agent communication (DM, broadcast, shutdown)
- `Task` tool — Spawning agents with `team_name` parameter

**Headless mode**:

- `TaskCreate` / `TaskUpdate` / `TaskList` / `TaskGet` — Ledger operations (orchestrator only)
- `Bash` — Spawning and monitoring `claude -p` processes
- `Read` — Parsing output JSON files

## Examples

- `/orchestrate A` — Run Phase A interactively (default mode)
- `/orchestrate A --headless` — Run Phase A with headless `claude -p` processes
- `/orchestrate A --headless --dry-run` — Preview generated prompts without spawning
- `/orchestrate A --headless --budget-per-task 3` — Cap each task at $3
- `/orchestrate A --wave 2` — Resume Phase A from Wave 2
- `/orchestrate A --interactive --max-agents 3` — Interactive with 3 agents max
- `/orchestrate docs/plans/custom-plan.md --headless` — Headless from custom plan
- `/orchestrate "add auth middleware; write auth tests; update docs"` — Inline tasks

## Error Recovery

- **Agent crashes (interactive)**: Detect via progressive stall escalation, reassign task
- **Process crashes (headless)**: Detect via PID check, retry with error context
- **Quality gate fails**: Create fix task, assign/spawn fix agent, re-run gate
- **All agents stalled (interactive)**: Report to user, suggest manual intervention or restart
- **Budget exceeded (headless)**: Pause and ask user before continuing
- **Git conflicts**: If worktree merge fails, pause and ask user for resolution strategy
- **Scope violation (headless)**: Revert commit, retry with reinforced scope constraint
