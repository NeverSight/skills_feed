---
name: ln-1000-pipeline-orchestrator
description: "Meta-orchestrator (L0): reads kanban board, drives Stories through pipeline 300->310->400->500 in parallel via TeamCreate. Max 3 concurrent Stories. Auto squash-merge to develop on quality gate PASS."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Pipeline Orchestrator

Meta-orchestrator that reads the kanban board, builds a priority queue of Stories, and drives them through the full pipeline (task planning -> validation -> execution -> quality gate) using Claude Code Agent Teams for parallel Story processing.

## Purpose & Scope
- Parse kanban board and build Story priority queue
- Ask business questions in ONE batch before execution; make technical decisions autonomously
- Spawn per-story workers via TeamCreate (max 3 concurrent)
- Drive each Story through 4 stages: ln-300 -> ln-310 -> ln-400 -> ln-500
- Auto squash-merge to develop after quality gate PASS
- Handle failures, retries, and escalation to user

## Hierarchy

```
L0: ln-1000-pipeline-orchestrator (TeamCreate lead, delegate mode)
  +-- Story Workers (fresh per stage, shutdown after completion)
       |   All stages: Opus 4.6  |  Effort: Stage 0 = low | Stage 1,2 = medium | Stage 3 = medium
       +-- L1: ln-300 / ln-310 / ln-400 / ln-500 (invoked via Skill tool, as-is)
            +-- L2/L3: existing hierarchy unchanged
```

**Key principle:** ln-1000 does NOT modify existing skills. Workers invoke ln-300/ln-310/ln-400/ln-500 through Skill tool exactly as a human operator would.

## MCP Tool Preferences

When `mcp__hashline-edit__*` tools are available, workers MUST prefer them over standard file tools:

| Standard Tool | Hashline-Edit Replacement | Why |
|---------------|--------------------------|-----|
| `Read` | `mcp__hashline-edit__read_file` | Hash-prefixed lines enable precise edits |
| `Edit` | `mcp__hashline-edit__edit_file` | Atomic validation prevents corruption |
| `Write` | `mcp__hashline-edit__write_file` | Same behavior, consistent interface |
| `Grep` | `mcp__hashline-edit__grep` | Results include hashline refs for follow-up edits |

**Fallback:** If hashline-edit MCP unavailable (tools not in ToolSearch), use standard tools. No error.

## Task Storage Mode

**MANDATORY READ:** Load `shared/references/storage_mode_detection.md` for Linear vs File mode detection and operations.

## When to Use
- Multiple Stories ready for processing across kanban board statuses
- Need end-to-end automation: task planning -> validation -> execution -> quality gate -> merge
- Want parallel Story processing with minimal manual intervention

## Pipeline: 4-Stage State Machine

**MANDATORY READ:** Load `references/pipeline_states.md` for transition rules and guards.

```
Backlog       --> Stage 0 (ln-300) --> Backlog      --> Stage 1 (ln-310) --> Todo
(no tasks)        create tasks         (tasks exist)      validate            |
                                                          | NO-GO             |
                                                          v                   v
                                                       [retry/ask]    Stage 2 (ln-400)
                                                                             |
                                                                             v
                                                                      To Review
                                                                             |
                                                                             v
                                                                      Stage 3 (ln-500)
                                                                       |          |
                                                                      PASS       FAIL
                                                                       |          v
                                                                     Done    To Rework -> Stage 2
                                                                   (merged)    (max 2 cycles)
```

| Stage | Skill | Input Status | Output Status |
|-------|-------|-------------|--------------|
| 0 | ln-300-task-coordinator | Backlog (no tasks) | Backlog (tasks created) |
| 1 | ln-310-story-validator | Backlog (tasks exist) | Todo |
| 2 | ln-400-story-executor | Todo / To Rework | To Review |
| 3 | ln-500-story-quality-gate | To Review | Done / To Rework |

## Team Lead Responsibilities

This skill runs as a **team lead** in delegate mode. The agent executing ln-1000 MUST NOT write code or invoke skills directly.

| Responsibility | Description |
|---------------|-------------|
| **Coordinate** | Assign stages to workers, process completion reports, advance pipeline |
| **Verify board** | Re-read kanban/Linear after each stage. Workers update via skills; lead ASSERTs expected state transitions |
| **Escalate** | Route failures to user when retry limits exceeded |
| **Merge to develop** | Squash-merge to develop after quality gate PASS (lead-only action) |
| **Shutdown** | Graceful worker shutdown, team cleanup |

**NEVER do as lead:** Invoke ln-300/ln-310/ln-400/ln-500 directly. Edit source code. Skip quality gate. Force-kill workers.

## Workflow

### Phase 0: Recovery Check

```
IF .pipeline/state.json exists AND complete == false:
  # Previous run interrupted — resume from saved state
  1. Read .pipeline/state.json → restore: story_state, worker_map,
     quality_cycles, validation_retries, crash_count, priority_queue_ids,
     story_results, infra_issues, worktree_map, depends_on,
     stage_timestamps, git_stats, pipeline_start_time, readiness_scores
  2. Read .pipeline/checkpoint-*.json → validate story_state consistency
     (checkpoint.stage should match story_state[id])
  3. Re-read kanban board → rebuild priority_queue from priority_queue_ids
     (skip stories already DONE/PAUSED)
  4. Re-parse Story dependencies → rebuild depends_on (defense in depth)
  5. Read team config → verify worker_map members still exist
  6. Set suspicious_idle[*] = false (ephemeral, reset on recovery)
  7. For each story with story_state IN ("STAGE_0".."STAGE_3"):
     IF checkpoint.agentId exists → Task(resume: checkpoint.agentId)
     ELSE → respawn worker with checkpoint context (see checkpoint_format.md)
  8. Jump to Phase 4 event loop

IF .pipeline/state.json NOT exists OR complete == true:
  # Fresh start — proceed to Phase 1
```

### Phase 1: Discovery & Kanban Parsing

**MANDATORY READ:** Load `references/kanban_parser.md` for parsing patterns.

1. Auto-discover `docs/tasks/kanban_board.md` (or Linear API via storage mode detection)
2. Extract project brief from target project's CLAUDE.md (NOT skills repo):
   ```
   project_brief = {
     name: <from H1 or first line>,
     tech: <from Development Commands / tech references>,
     type: <inferred: "CLI", "API", "web app", "library">,
     key_rules: <2-3 critical rules>
   }
   IF not found: project_brief = { name: basename(project_root), tech: "unknown" }
   ```
3. Parse all status sections: Backlog, Todo, In Progress, To Review, To Rework
4. Extract Story list with: ID, title, status, Epic name, task presence
5. Build priority queue:
   ```
   Priority: To Review > To Rework > In Progress > Todo > Backlog
   ```
6. Filter: skip Stories in Done, Postponed, Canceled
7. Detect task presence per Story:
   - Has `_(tasks not created yet)_` → **no tasks** → Stage 0
   - Has task lines (4-space indent) → **tasks exist** → Stage 1+
8. Extract dependencies per Story (see `references/kanban_parser.md` Dependency Extraction):
   - Read each Story file → parse `## Dependencies / ### Depends On` section
   - Build `depends_on[storyId] = [prerequisite IDs]`
   - Prerequisites already Done → satisfied, ignore. Not found → WARN, treat as none
   - Circular dependencies → ESCALATE to user
9. Extract story briefs from Linear (for lead awareness):
   ```
   FOR EACH story in priority_queue:
     description = get_issue(story.id).description
     story_briefs[id] = parse <!-- ORCHESTRATOR_BRIEF_START/END --> markers
     IF no markers: story_briefs[id] = { tech: project_brief.tech, keyFiles: "unknown" }
   ```
10. Show pipeline plan to user:
   ```
   Project: {project_brief.name} ({project_brief.tech})

   Pipeline Plan:
   | # | Story | Tech | Approach | Stage | Deps | Action |
   |---|-------|------|----------|-------|------|--------|
   | 1 | PROJ-42 | Python, FastAPI | Token middleware | 3 | — | Quality gate |
   | 2 | PROJ-55 | Python, FastAPI | CRUD + Alembic | 0 | PROJ-42 | Create tasks |
   ```

### Phase 2: Pre-flight Questions (ONE batch)

1. Load Story descriptions (metadata only) for top stories in pipeline scope
2. Scan for business ambiguities — questions where:
   - Answer cannot be found in codebase, docs, or standards
   - Answer requires business/product decision (payment provider, auth flow, UI preference)
3. Collect ALL business questions into single AskUserQuestion:
   ```
   "Before starting pipeline:
    Story PROJ-42: Which payment provider? (Stripe/PayPal/both)
    Story PROJ-45: Auth flow — JWT or session-based?"
   ```
4. Technical questions — resolve using project_brief:
   - Library versions: MCP Ref / Context7 (for `project_brief.tech` ecosystem)
   - Architecture patterns: `project_brief.key_rules`
   - Standards compliance: ln-310 Phase 2 handles this
5. Store answers in shared context (pass to workers via spawn prompt)

**Skip Phase 2** if no business questions found. Proceed directly to Phase 3.

### Phase 3: Team Setup

**MANDATORY READ:** Load `references/settings_template.json` for required permissions and hooks.

#### 3.0 Linear Status Cache (Linear mode only)

```
IF storage_mode == "linear":
  statuses = list_issue_statuses(teamId=team_id)
  status_cache = {status.name: status.id FOR status IN statuses}

  REQUIRED = ["Backlog", "Todo", "In Progress", "To Review", "To Rework", "Done"]
  missing = [s for s in REQUIRED if s not in status_cache]
  IF missing: ABORT "Missing Linear statuses: {missing}. Configure workflow."

  # Persist in state.json (added in 3.2) and pass to workers via prompt CONTEXT
```

#### 3.1 Pre-flight: Settings Verification

Verify `.claude/settings.local.json` in target project:
- `defaultMode` = `"bypassPermissions"` (required for workers)
- `hooks.Stop` registered → `pipeline-keepalive.sh`
- `hooks.TeammateIdle` registered → `worker-keepalive.sh`

If missing or incomplete → copy from `references/settings_template.json` and install hook scripts via Bash `cp` (NOT Write tool — Write produces CRLF on Windows, breaking `#!/bin/bash` shebang):
```
mkdir -p .claude/hooks
Bash: cp {skill_repo}/ln-1000-pipeline-orchestrator/references/hooks/pipeline-keepalive.sh .claude/hooks/pipeline-keepalive.sh
Bash: cp {skill_repo}/ln-1000-pipeline-orchestrator/references/hooks/worker-keepalive.sh  .claude/hooks/worker-keepalive.sh
```

**Hook troubleshooting:** If hooks fail with "No such file or directory":
1. Verify hook commands use `bash .claude/hooks/script.sh` (relative path, no env vars — `$CLAUDE_PROJECT_DIR` is NOT available in hook shell context)
2. Verify `.claude/hooks/*.sh` files exist and have `#!/bin/bash` shebang
3. On Windows: ensure LF line endings in .sh files (see hook installation above — use Bash `cp`, not Write tool)

#### 3.2 Initialize Pipeline State

```
Write .pipeline/state.json (full schema — see checkpoint_format.md):
  { "complete": false, "active_workers": 0, "stories_remaining": N, "last_check": <now>,
    "story_state": {}, "worker_map": {}, "quality_cycles": {}, "validation_retries": {},
    "crash_count": {}, "priority_queue_ids": [<all story IDs>],
    "worktree_map": {}, "depends_on": {}, "story_results": {}, "infra_issues": [],
    "status_cache": {<status_name: status_uuid>},    # Empty object if file mode
    "stage_timestamps": {}, "git_stats": {}, "pipeline_start_time": <now>, "readiness_scores": {},
    "skill_repo_path": <absolute path to skills repository root>,
    "team_name": "pipeline-{YYYY-MM-DD}",
    "business_answers": {<question: answer pairs from Phase 2, or {} if skipped>},
    "total_merged_stories": 0,
    "storage_mode": "file"|"linear",
    "project_brief": {<name, tech, type, key_rules from Phase 1 step 2>},
    "story_briefs": {<storyId: {tech, keyFiles, approach, complexity} from Phase 1 step 9>} }   # Recovery-critical
Write .pipeline/lead-session.id with current session_id   # Stop hook uses this to only keep lead alive
```

#### 3.2a Sleep Prevention (Windows only)

```
IF platform == "win32":
  Bash: cp {skill_repo}/ln-1000-pipeline-orchestrator/references/hooks/prevent-sleep.ps1 .claude/hooks/prevent-sleep.ps1
  Bash: powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File .claude/hooks/prevent-sleep.ps1 &
  sleep_prevention_pid = $!
  # Script polls .pipeline/state.json — self-terminates when complete=true
  # Fallback: Windows auto-releases execution state on process exit
```

#### 3.3 Create Team & Spawn Workers

**Worktrees:** Every worker gets its own worktree with a named feature branch (`feature/{id}-{slug}`). Created in Phase 4 spawn loop.

**Model routing:** All stages use `model: "opus"`. Effort routing via prompt: `effort_for_stage(0) = "low"`, `effort_for_stage(1) = "medium"`, `effort_for_stage(2) = "medium"`, `effort_for_stage(3) = "medium"`. Crash recovery = same as target stage. Thinking mode: always enabled (adaptive).

1. Ensure `develop` branch exists:
   ```
   IF `develop` branch not found locally or on origin:
     git branch develop master        # Create from master
     git push -u origin develop
   git checkout develop               # Start pipeline from develop
   ```

2. Create team:
   ```
   TeamCreate(team_name: "pipeline-{YYYY-MM-DD}")
   ```

Workers are spawned by Phase 4 spawn loop on first heartbeat — NOT here. This avoids duplicate spawn logic.

### Phase 4: Execution Loop

**MANDATORY READ:** Load `references/message_protocol.md` for exact message formats and parsing regex.
**MANDATORY READ:** Load `references/worker_health_contract.md` for crash detection and respawn rules.

**Lead operates in delegate mode — coordination only, no code writing.**

**MANDATORY READ:** Load `references/checkpoint_format.md` for checkpoint schema and resume protocol.

```
# --- INITIALIZATION ---
active_workers = 0                    # Current worker count (invariant: <= 3)
quality_cycles = {}                   # {storyId: count} — FAIL→retry counter, limit 2
validation_retries = {}               # {storyId: count} — NO-GO retry counter, limit 1
crash_count = {}                      # {storyId: count} — crash respawn counter, limit 1
suspicious_idle = {}                  # {storyId: bool} — crash detection flag
story_state = {}                      # {storyId: "STAGE_0"|"STAGE_1"|"STAGE_2"|"STAGE_3"|"DONE"|"PAUSED"}
worker_map = {}                       # {storyId: worker_name}
depends_on = {}                       # {storyId: [prerequisite IDs]} — from Phase 1 step 7
worktree_map = {}                     # {storyId: worktree_dir | null} — tracks which stories use worktrees
story_results = {}                    # {storyId: {stage0: "...", stage1: "...", ...}} — for pipeline report
infra_issues = []                     # [{phase, type, message}] — infrastructure problems for report
heartbeat_count = 0                   # Heartbeat cycle counter (ephemeral, resets on recovery)
stage_timestamps = {}                # {storyId: {stage_N_start: ISO, stage_N_end: ISO}}
git_stats = {}                       # {storyId: {lines_added, lines_deleted, files_changed}}
pipeline_start_time = now()          # ISO 8601 — wall-clock start for duration metrics
readiness_scores = {}                # {storyId: readiness_score} — from Stage 1 GO, used for Stage 3 fast-track

# Helper functions for heartbeat formatting
skill_name_from_stage(stage):
  """Returns skill name for stage number."""
  RETURN {0: "ln-300-task-coordinator", 1: "ln-310-story-validator",
          2: "ln-400-story-executor", 3: "ln-500-story-quality-gate"}[stage]

predict_next_step(current_stage):
  """Predicts next pipeline step for story."""
  IF current_stage == 0: RETURN "Validation (ln-310) → Todo"
  IF current_stage == 1: RETURN "Execution (ln-400) → To Review"
  IF current_stage == 2: RETURN "Quality gate (ln-500) → PASS/FAIL"
  IF current_stage == 3: RETURN "Squash merge to develop → Done"

stage_duration(story_id, stage_num):
  """Returns formatted duration (Xm Ys) for a stage, or None if timestamps missing."""
  start = stage_timestamps[story_id].get("stage_{stage_num}_start")
  end = stage_timestamps[story_id].get("stage_{stage_num}_end")
  IF start AND end: RETURN format_duration(end - start)
  RETURN None

# Initialize counters for all queued stories
FOR EACH story IN priority_queue:
  quality_cycles[story.id] = 0
  validation_retries[story.id] = 0
  crash_count[story.id] = 0
  suspicious_idle[story.id] = false
  story_state[story.id] = "QUEUED"

# --- EVENT LOOP (driven by Stop hook heartbeat) ---
# HOW THIS WORKS:
# 1. Lead's turn ends → Stop event fires
# 2. pipeline-keepalive.sh reads .pipeline/state.json → complete=false → exit 2
# 3. stderr "HEARTBEAT: N workers, M stories..." → new agentic loop iteration
# 4. Any queued worker messages (SendMessage) delivered in this cycle
# 5. Lead processes messages via ON handlers (reactive) + verifies done-flags (proactive)
# 6. Lead's turn ends → Go to step 1
#
# The Stop hook IS the event loop driver. Each heartbeat = one iteration.
# Lead MUST NOT say "waiting for messages" and stop — the heartbeat keeps it alive.
# If no worker messages arrived: output brief status, let turn end → next heartbeat.
#
# --- CONTEXT RECOVERY PROTOCOL ---
# Claude Code may compress conversation history during long pipelines.
# When this happens, you lose SKILL.md instructions and state variables.
# The Stop hook includes "---PIPELINE RECOVERY CONTEXT---" in EVERY heartbeat stderr.
#
# IF you see this block and don't recall the pipeline protocol:
#   Follow CONTEXT RECOVERY PROTOCOL in references/phases/phase4_heartbeat.md (7 steps).
#   Quick summary: state.json → SKILL.md(FULL) → handlers → heartbeat → known_issues → ToolSearch → resume
#
# Cost: ~5 file reads (~1300 lines, ~2500 tokens), one-time per compression event.
# Normal operation: 0 extra reads. Recovery block in stderr is passive anchor.
#
# FRESH WORKER PER STAGE: Each stage transition = shutdown old worker + spawn new one.
# active_workers stays same (net-zero). Only DONE/PAUSED/ERROR decrement active_workers.
#
# BIDIRECTIONAL HEALTH MONITORING (Phase 4, Step 3):
# - Reactive: ON handlers process worker completion messages
# - Proactive: Verify done-flags without messages (lost message recovery)
# - Defense-in-depth: Handles network issues, context overflow, worker crashes

WHILE ANY story_state[id] NOT IN ("DONE", "PAUSED"):

  # 1. Spawn workers for queued stories (respecting concurrency + dependency limits)
  WHILE active_workers < 3 AND priority_queue NOT EMPTY:
    story = priority_queue.peek()            # Don't pop yet — may be blocked

    # Dependency guard: all prerequisites must be DONE
    blocked_deps = [d for d in depends_on[story.id] if story_state[d] != "DONE"]
    IF blocked_deps NOT EMPTY:
      priority_queue.skip(story.id)          # Move to next candidate
      CONTINUE                               # Try next story in queue
    priority_queue.pop()                     # Safe to start

    target_stage = determine_stage(story)    # See pipeline_states.md guards
    worker_name = "story-{story.id}-s{target_stage}"

    worktree_dir = ".worktrees/story-{story.id}"
    git worktree add -b feature/{story.id}-{slug} {worktree_dir} develop

    worktree_map[story.id] = worktree_dir
    project_root = Bash("pwd")           # Absolute path for PIPELINE_DIR in worktree mode
    Task(name: worker_name, team_name: "pipeline-{date}",
         model: "opus", mode: "bypassPermissions",
         subagent_type: "general-purpose",
         prompt: worker_prompt(story, target_stage, business_answers, worktree_dir, project_root))
    worker_map[story.id] = worker_name
    story_state[story.id] = "STAGE_{target_stage}"
    stage_timestamps[story.id] = stage_timestamps.get(story.id, {})
    stage_timestamps[story.id]["stage_{target_stage}_start"] = now()
    active_workers++
    Write .pipeline/worker-{worker_name}-active.flag     # For TeammateIdle hook
    Update .pipeline/state.json: active_workers, last_check
    SendMessage(recipient: worker_name,
                content: "Execute Stage {target_stage} for {story.id}",
                summary: "Stage {target_stage} assignment")

  # 1b. Deadlock detection: all remaining stories blocked on non-DONE dependencies
  IF active_workers == 0 AND priority_queue NOT EMPTY:
    unblockable = [s for s in priority_queue if ALL d in depends_on[s.id]: story_state[d] == "DONE"]
    IF unblockable EMPTY:
      FOR EACH s IN priority_queue: story_state[s.id] = "PAUSED"
      ESCALATE: "Deadlocked: remaining stories depend on PAUSED/incomplete stories: {ids}"

  # 2. Process worker messages (reactive message handling)
  #
  **MANDATORY READ:** Load `references/phases/phase4_handlers.md` for all ON message handlers:
  - Stage 0 COMPLETE / ERROR (task planning outcomes)
  - Stage 1 COMPLETE (GO / NO-GO validation outcomes with retry logic)
  - Stage 2 COMPLETE / ERROR (execution outcomes)
  - Stage 3 COMPLETE (PASS/CONCERNS/WAIVED/FAIL quality gate outcomes with rework cycles)
  - Worker crash detection (3-step protocol: flag → probe → respawn)

  Handlers include sender validation and state guards to prevent duplicate processing.

  # 2.5. Active done-flag verification (proactive health monitoring)
  #
  **MANDATORY READ:** Load `references/phases/phase4_heartbeat.md` for bidirectional health monitoring:
  - Lost message detection (done-flag exists but state not advanced)
  - Synthetic recovery from checkpoint + kanban verification (all 4 stages)
  - Fallback to probe protocol when checkpoint missing
  - Structured heartbeat output (table format with worker status)
  - Helper functions (skill_name_from_stage, predict_next_step)

  This complements reactive crash detection (ON TeammateIdle) with proactive polling every ~60s.

  # 3. Heartbeat state persistence
  #
  ON HEARTBEAT (Stop hook stderr: "HEARTBEAT: N workers, M stories..."):
    Write .pipeline/state.json with ALL state variables.
    # See phase4_heartbeat.md for persistence details
```

**`determine_stage(story)` routing:** See `references/pipeline_states.md` Stage-to-Status Mapping table.

#### Phase 4a: Git Flow & Squash Merge

**MANDATORY READ:** Load `references/phases/phase4a_git_merge.md` for squash-merge procedure:
- Sync with develop (rebase → fallback to merge on conflict)
- Squash merge into develop (single commit per Story)
- Worktree cleanup
- Context refresh (reload SKILL.md after large merges)
- Story report appending (stage results + counters + problems)
- Kanban + Linear verification (sync check)

Executed after Stage 3 PASS verdict from ln-500-story-quality-gate.

#### Phase 4b: Cross-Story Health Check (every 5th merged Story)

After squash-merge, increment `total_merged_stories` counter. When `total_merged_stories % 5 == 0`:

1. On develop branch, Grep for top-5 hotspot patterns across `src/` (count mode):
   - Error handlers: `catch.*Error|handleError|handleCommandError`
   - Validators: `validate|isValid|checkInput`
   - Config access: `getSettings|getConfig|loadConfig`
   - HTTP wrappers: `httpClient|apiClient|fetchWrapper`
   - Parsers: `parseResponse|parseError|parseApi`
2. If ANY pattern appears in **5+ files** → WARN user:
   ```
   Cross-Story Health Check (after {N} Stories):
   WARNING: {pattern} duplicated in {count} files.
   Recommend: create refactoring Epic or run ln-620-codebase-auditor.
   ```
3. Log result in pipeline report (`story_results` → health_check entry)

**NOTE:** Warning-only — does NOT block pipeline. User decides whether to act.

### Phase 5: Cleanup & Self-Verification

```
# 0. Signal pipeline complete (allows Stop hook to pass)
Write .pipeline/state.json: { "complete": true, ... }

# 1. Wait for all active workers to complete
ASSERT active_workers == 0

# 2. Self-verify against Definition of Done
verification = {
  kanban_parsed:    priority_queue was built          # Phase 1 ✓
  questions_asked:  business_answers stored OR none   # Phase 2 ✓
  team_created:     team exists                       # Phase 3 ✓
  all_processed:    ALL story_state[id] IN ("DONE", "PAUSED")  # Phase 4 ✓
  merged_develop:   EVERY "DONE" story squash-merged to develop  # Phase 4a ✓
  linear_synced:    IF storage_mode == "linear": ALL "DONE" stories match Linear status  # Phase 4a.6 ✓
  on_develop:       Current branch is develop              # Phase 5 ✓
}
IF ANY verification == false: WARN user with details

# 3. Finalize pipeline report
Prepend summary header to docs/tasks/reports/pipeline-{date}.md:
  # Pipeline Report — {date}
  | Metric | Value |
  |--------|-------|
  | Stories processed | {total} |
  | Completed (DONE) | {count where story_state == "DONE"} |
  | Paused (needs intervention) | {count where story_state == "PAUSED"} |
  | Total quality rework cycles | {sum of quality_cycles} |
  | Total validation retries | {sum of validation_retries} |
  | Total crash recoveries | {sum of crash_count} |
  | Infrastructure issues | {len(infra_issues)} |
  | **Models used** | **{list of unique models from session}** |
  | **Total tokens consumed** | **{sum of tokens from all tool uses}** |

  **Note:** Model and token data collected from session analysis (all Task spawns + tool uses).
  Breakdown: Lead (Opus 4.6) + Workers (per-stage model allocation).

# 3b. Stage Duration Breakdown
Append Stage Duration section:
  ## Stage Duration Breakdown
  | Story | Stage 0 | Stage 1 | Stage 2 | Stage 3 | Total | Bottleneck |
  |-------|---------|---------|---------|---------|-------|------------|
  FOR EACH story WHERE story_state[id] IN ("DONE", "PAUSED"):
    durations = {N: stage_timestamps[id]["stage_{N}_end"] - stage_timestamps[id]["stage_{N}_start"]
                 FOR N IN 0..3 IF both timestamps exist}
    total = sum(durations.values())
    bottleneck = key with max(durations)
    | {id} | {durations[0] or "—"} | {durations[1] or "—"} | {durations[2] or "—"} | {durations[3] or "—"} | {total} | Stage {bottleneck} |

# 3c. Code Output Metrics
Append Code Output section:
  ## Code Output Metrics
  | Story | Files Changed | Lines Added | Lines Deleted | Net Lines |
  |-------|--------------|-------------|---------------|-----------|
  FOR EACH story WHERE git_stats[id] exists:
    | {id} | {git_stats[id].files_changed} | +{git_stats[id].lines_added} | -{git_stats[id].lines_deleted} | {net} |
  **Total:** {sum files_changed} files, +{sum lines_added} / -{sum lines_deleted} lines

# 3d. Cost Estimate
Append Cost Estimate section:
  ## Cost Estimate
  | Metric | Value |
  |--------|-------|
  | Wall-clock time | {now() - pipeline_start_time} |
  | Total worker spawns | {count of Task() calls in session} |
  | Hashline-edit usage | {count mcp__hashline-edit__* calls in Stage 2 workers} / {total file edits} |

# 3a. Collect infrastructure issues
# Analyze entire pipeline session for non-fatal problems:
# hook/settings failures, git conflicts, worktree errors, merge issues,
# Linear sync mismatches, worker crashes, permission errors, any unexpected fallbacks.
# Populate infra_issues = [{phase, type, message}] from session context.

Append Infrastructure Issues section:
  ## Infrastructure Issues
  IF infra_issues NOT EMPTY:
    | # | Phase | Type | Details |
    |---|-------|------|---------|
    FOR EACH issue IN infra_issues:
      | {N} | {issue.phase} | {issue.type} | {issue.message} |
  ELSE:
    _No infrastructure issues._

Append Operational Recommendations section (auto-generated from counters):
  ## Operational Recommendations
  - IF any quality_cycles > 0: "Story {id} needed {N} quality cycles. Improve task specs or acceptance criteria."
  - IF any validation_retries > 0: "Story {id} failed validation. Review Story/Task structure."
  - IF any crash_count > 0: "Worker crashed {N} times for {id}. Check for context-heavy operations."
  - IF any PAUSED: "Stories {ids} require manual intervention."
  - IF any Linear sync mismatches: "Linear/kanban sync issues detected for {ids}. Verify statuses manually."
  - IF any infra_issues with type "hook": "Hook configuration errors. Verify settings.local.json and .claude/hooks/."
  - IF any infra_issues with type "git": "Git conflicts encountered. Rebase feature branches more frequently."
  - IF any infra_issues with type "worktree": "Worktree failures. Check disk space and existing worktree state."
  - IF all DONE with 0 retries AND no infra_issues: "Clean run — no issues detected."

Append Process Improvement section (auto-generated from pipeline analysis):
  ## Process Improvement Suggestions
  Analyze pipeline session and generate suggestions in 4 categories:

  ### Efficiency (reduce time/steps)
  - IF any story went through all 4 stages (0→1→2→3): "Consider skipping Stage 0/1 for stories with pre-validated tasks (resume from Stage 2)."
  - IF multiple stories produced similar Stage 0 output: "Stories {ids} had similar task plans. Consider task templates to skip planning."
  - IF Stage 2 was bottleneck (longest stage across stories): "Execution dominated pipeline time. Split large stories for better parallelism."

  ### Cost (reduce token usage)
  - IF any crash_count > 0: "Crashes waste full stage token budget. Reduce context-heavy operations or add intermediate checkpoints."
  - IF quality_cycles > 0: "Rework cycles multiply cost — Stage 2+3 repeated {N} times. Invest in better task specs upfront (ln-300)."
  - IF validation_retries > 0: "Validation retry = wasted Stage 0+1. Improve story templates or run ln-310 earlier."
  - General: "Review worker prompt sizes. Shorter focused prompts reduce per-spawn token cost."

  ### Quality (improve output)
  - IF any Stage 3 verdict was CONCERNS: "Story {id} passed with concerns. Tighter AC or stricter test coverage may prevent debt."
  - IF any Stage 3 score < 80: "Low quality ({score}/100) for {id}. Consider: more specific AC, ln-002 research before coding, stricter ln-402 review."
  - IF agent reviews (ln-514) found issues not caught by ln-402: "External agents caught missed issues. Consider running agent review earlier."
  - IF all scores > 90: "High quality scores. Current process works well — maintain."

  ### Process Architecture (structural improvements)
  - IF pipeline ran > 5 stories: "Large batch. Consider increasing max_workers or grouping into sub-batches."
  - IF any PAUSED: "PAUSED stories indicate systematic issues. Analyze: task spec quality? Missing context? Unclear AC?"
  - IF depends_on blocked stories for extended periods: "Dependency chains caused idle workers. Reorder stories to minimize blocking."
  - General: "Compare metrics across runs to track trends: quality_score, avg cycles per story, crash rate."

# 4. Show pipeline summary to user
```
Pipeline Complete:
| Story | Stage 0 | Stage 1 | Stage 2 | Stage 3 | Merged | Final State |
|-------|---------|---------|---------|---------|--------|------------|
| PROJ-42 | skip | skip | skip | PASS 92 | yes | DONE |
| PROJ-55 | 5 tasks | GO | Done | PASS 85 | yes | DONE |
| PROJ-60 | skip | NO-GO | — | — | — | PAUSED |

Report saved: docs/tasks/reports/pipeline-{date}.md
```
# 5. Shutdown remaining workers (if any still active)
FOR EACH worker_name IN worker_map.values():
  SendMessage(type: "shutdown_request", recipient: worker_name)

# 6. Cleanup team
TeamDelete

# 7. Remove remaining worktrees (PAUSED stories not cleaned by Phase 4a)
IF .worktrees/ directory exists:
  FOR EACH story in worktree_map WHERE worktree_dir != null:
    git worktree remove {worktree_dir} --force
  rm -rf .worktrees/

# 8. Ensure on develop branch
git checkout develop

# 9. Remove pipeline state files

# 9a. Stop sleep prevention (Windows safety net — script should have self-terminated)
IF sleep_prevention_pid:
  kill $sleep_prevention_pid 2>/dev/null || true
Delete .pipeline/ directory

# 10. Report results and report location to user
```

## Kanban as Single Source of Truth

- **Lead = single writer** to kanban_board.md. Workers report results via SendMessage; lead updates the board
- **Re-read board** after each stage completion for fresh state
- **Update algorithm:** Follow `shared/references/kanban_update_algorithm.md` for Epic grouping and indentation

## Error Handling

| Situation | Detection | Action |
|-----------|----------|--------|
| ln-300 task creation fails | Worker reports error | Escalate to user: "Cannot create tasks for Story {id}" |
| ln-310 NO-GO (Score <5) | Worker reports NO-GO | Retry once (ln-310 auto-fixes). If still NO-GO -> ask user |
| Task in To Rework 3+ times | Worker reports rework loop | Escalate: "Task X reworked 3 times, need input" |
| ln-500 FAIL | Worker reports FAIL verdict | Fix tasks auto-created by ln-500. Stage 2 re-entry. Max 2 quality cycles |
| Worker crash | TeammateIdle without completion msg | Re-spawn worker, resume from last stage |
| All Stories blocked | Empty actionable queue | Report to user, cleanup team |
| Business question mid-execution | Worker encounters ambiguity | Worker -> lead -> user -> lead -> worker (message chain) |
| Merge conflict | git merge --squash fails | Escalate to user, Story PAUSED, manual resolution required |

## Critical Rules

1. **Max 3 concurrent Stories.** Never spawn more than 3 story-workers simultaneously
2. **Delegate mode.** Lead coordinates only — never invoke ln-300/ln-310/ln-400/ln-500 directly. Workers do all execution
3. **Skills as-is.** Never modify or bypass existing skill logic. Workers call `Skill("ln-310-story-validator", args)` exactly as documented
4. **Kanban verification.** Workers update Linear/kanban via skills. Lead re-reads and ASSERTs expected state after each stage. In file mode, lead resolves merge conflicts
5. **Quality cycle limit.** Max 2 quality FAILs per Story (original + 1 rework cycle). After 2nd FAIL, escalate to user
6. **Squash per Story.** Each Story that passes quality gate gets squash-merged to develop separately. No batch merges
7. **Re-read kanban.** After every stage completion, re-read board for fresh state. Never cache
8. **Graceful shutdown.** Always shutdown workers via shutdown_request. Never force-kill

## Known Issues

**MANDATORY READ:** Load `references/known_issues.md` for production-discovered problems and self-recovery patterns.

## Anti-Patterns
- Running ln-300/ln-310/ln-400/ln-500 directly from lead instead of delegating to workers
- Spawning >3 workers simultaneously
- Lead skipping kanban verification after worker updates (workers write via skills, lead MUST re-read + ASSERT)
- Skipping quality gate after execution
- Merging to develop before quality gate PASS
- Caching kanban state instead of re-reading
- Reading `~/.claude/teams/*/inboxes/*.json` directly (messages arrive automatically)
- Using `sleep` + filesystem polling for message checking
- Parsing internal Claude Code JSON formats (permission_request, idle_notification)
- Reusing same worker across stages (context exhaustion — spawn fresh worker per stage)
- Processing messages without verifying sender matches worker_map (stale message confusion from old/dead workers)

## Plan Mode Support

When invoked in Plan Mode, generate execution plan without creating team:

1. Parse kanban board (Phase 1)
2. Build priority queue
3. Show pipeline plan table (which Stories, which stages)
4. Write plan to plan file, call ExitPlanMode

**Plan Output Format:**
```
## Pipeline Plan for {date}

| # | Story | Status | Stage | Skill | Expected Outcome |
|---|-------|--------|-------|-------|-----------------|
| 1 | {ID}: {Title} | To Review | 3 | ln-500 | Done + PR |
| 2 | {ID}: {Title} | Todo | 2 | ln-400 | To Review |

### Execution Sequence
1. TeamCreate("pipeline-{date}")
2. Spawn story-worker for {Story-1} -> Stage 3 (ln-500)
3. Spawn story-worker for {Story-2} -> Stage 2 (ln-400)
4. Wait for completions, advance stages, squash-merge to develop
5. Cleanup
```

## Definition of Done (self-verified in Phase 5)

| # | Criterion | Verified By |
|---|-----------|-------------|
| 1 | Kanban board parsed, priority queue built | `priority_queue` was populated |
| 2 | Business questions asked in single batch (or none found) | `business_answers` stored OR skip |
| 3 | Team created, workers spawned (max 3 concurrent) | `active_workers` never exceeded 3 |
| 4 | ALL Stories processed: state = DONE or PAUSED | `ALL story_state[id] IN ("DONE", "PAUSED")` |
| 4b | Cross-story health checked (if threshold met) | Warning logged or N/A |
| 5 | Every DONE Story squash-merged into develop | Feature branches merged, on develop branch |
| 6 | Pipeline summary shown to user | Phase 5 table output |
| 7 | Team cleaned up (workers shutdown, TeamDelete) | `active_workers == 0`, TeamDelete called |

## Reference Files

### Phase 4 Procedures (Progressive Disclosure)
- **Message handlers:** `references/phases/phase4_handlers.md` (Stage 0-3 ON handlers, crash detection)
- **Heartbeat & verification:** `references/phases/phase4_heartbeat.md` (Active done-flag checking, structured heartbeat output)
- **Git flow:** `references/phases/phase4a_git_merge.md` (Squash merge, worktree cleanup, sync verification)

### Core Infrastructure
- **Known issues:** `references/known_issues.md` (production-discovered problems and self-recovery)
- **Message protocol:** `references/message_protocol.md`
- **Worker health:** `references/worker_health_contract.md`
- **Checkpoint format:** `references/checkpoint_format.md`
- **Settings template:** `references/settings_template.json`
- **Hooks:** `references/hooks/pipeline-keepalive.sh`, `references/hooks/worker-keepalive.sh`
- **Kanban parsing:** `references/kanban_parser.md`
- **Pipeline states:** `references/pipeline_states.md`
- **Worker prompts:** `references/worker_prompts.md`
- **Kanban update algorithm:** `shared/references/kanban_update_algorithm.md`
- **Storage mode detection:** `shared/references/storage_mode_detection.md`
- **Auto-discovery patterns:** `shared/references/auto_discovery_pattern.md`

### Delegated Skills
- `../ln-300-task-coordinator/SKILL.md`
- `../ln-310-story-validator/SKILL.md`
- `../ln-400-story-executor/SKILL.md`
- `../ln-500-story-quality-gate/SKILL.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-02-13
