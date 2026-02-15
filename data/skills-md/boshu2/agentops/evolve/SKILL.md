---
name: evolve
description: Goal-driven fitness-scored improvement loop. Measures goals, picks worst gap, runs /rpi, compounds via knowledge flywheel.
metadata:
  tier: orchestration
  dependencies:
    - rpi         # required - executes each improvement cycle
    - post-mortem # required - auto-runs at teardown to harvest learnings
  triggers:
    - evolve
    - improve everything
    - autonomous improvement
    - run until done
---

# /evolve — Goal-Driven Compounding Loop

> **Purpose:** Measure what's wrong. Fix the worst thing. Measure again. Compound.

Thin fitness-scored loop over `/rpi`. The knowledge flywheel provides compounding — each cycle loads learnings from all prior cycles.

**Dormancy is success.** When all goals pass and no harvested work remains, the system enters dormancy — a valid, healthy state. The system does not manufacture work to justify its existence. Nothing to do means everything is working.

## Quick Start

```bash
/evolve                      # Run forever until kill switch or stagnation
/evolve --max-cycles=5       # Cap at 5 improvement cycles
/evolve --dry-run            # Measure fitness, show what would be worked on, don't execute
```

## Execution Steps

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

### Step 0: Setup

```bash
mkdir -p .agents/evolve
```

Load accumulated learnings (COMPOUNDING):
```bash
ao inject 2>/dev/null || true
```

Parse flags:
- `--max-cycles=N` (default: **unlimited**) — optional hard cap. Without this flag, the loop runs **forever** until kill switch or stagnation.
- `--dry-run` — measure and report only, no execution

**Capture session-start SHA** (for multi-commit revert):
```bash
SESSION_START_SHA=$(git rev-parse HEAD)
```

Initialize state:
```
evolve_state = {
  cycle: 0,
  max_cycles: <from flag, or Infinity if not set>,
  dry_run: <from flag, default false>,
  test_first: <from flag, default false>,
  session_start_sha: $SESSION_START_SHA,
  idle_streak: 0,         # consecutive cycles with nothing to do
  max_idle_streak: 3,     # stop after this many consecutive idle cycles
  history: []
}
```

### Step 1: Kill Switch Check

Check at the TOP of every cycle iteration:

```bash
# External kill (outside repo — can't be accidentally deleted by agents)
if [ -f ~/.config/evolve/KILL ]; then
  echo "KILL SWITCH ACTIVE: $(cat ~/.config/evolve/KILL)"
  # Write acknowledgment
  echo "{\"killed_at\": \"$(date -Iseconds)\", \"cycle\": $CYCLE}" > .agents/evolve/KILLED.json
  exit 0
fi

# Local convenience stop
if [ -f .agents/evolve/STOP ]; then
  echo "STOP file detected: $(cat .agents/evolve/STOP 2>/dev/null)"
  exit 0
fi
```

If either file exists, log reason and **stop immediately**. Do not proceed to measurement.

### Step 2: Measure Fitness (MEASURE_FITNESS)

Read `GOALS.yaml` from repo root. For each goal:

```bash
# Run the check command
if eval "$goal_check" > /dev/null 2>&1; then
  # Exit code 0 = PASS
  result = "pass"
else
  # Non-zero = FAIL
  result = "fail"
fi
```

Record results with **continuous values** (not just pass/fail):
```bash
# Write fitness snapshot
cat > .agents/evolve/fitness-${CYCLE}.json << EOF
{
  "cycle": $CYCLE,
  "timestamp": "$(date -Iseconds)",
  "cycle_start_sha": "$(git rev-parse HEAD)",
  "goals": [
    {"id": "$goal_id", "result": "$result", "weight": $weight, "value": $metric_value, "threshold": $threshold},
    ...
  ]
}
EOF
```

For goals with measurable metrics, extract the continuous value:
- `go-coverage-floor`: parse `go test -cover` output → `"value": 85.7, "threshold": 80`
- `doc-coverage`: count skills with references/ → `"value": 20, "threshold": 16`
- `shellcheck-clean`: count of warnings → `"value": 0, "threshold": 0`
- Other goals: `"value": null` (binary pass/fail only)

**Snapshot enforcement (HARD GATE):** After writing the snapshot, validate it:
```bash
if ! jq empty ".agents/evolve/fitness-${CYCLE}.json" 2>/dev/null; then
  echo "ERROR: Fitness snapshot write failed or invalid JSON. Refusing to proceed."
  exit 1
fi
```
Do NOT proceed to Step 3 without a valid fitness snapshot.

**Bootstrap mode:** If a check command fails to execute (command not found, permission denied), mark that goal as `"result": "skip"` with a warning. Do NOT block the entire loop because one check is broken.

### Step 3: Select Work

```
failing_goals = [g for g in goals if g.result == "fail"]

if not failing_goals:
  # All goals pass — check harvested work from prior /rpi cycles
  if [ -f .agents/rpi/next-work.jsonl ]; then
    items = read_unconsumed(next-work.jsonl)  # entries with consumed: false
    if items:
      evolve_state.idle_streak = 0  # reset — we found work
      selected_item = max(items, by=severity)  # highest severity first
      log "All goals met. Picking harvested work: {selected_item.title}"
      # Execute as an /rpi cycle (Step 4), then mark consumed
      /rpi "{selected_item.title}" --auto --max-cycles=1 --test-first   # if --test-first set
      /rpi "{selected_item.title}" --auto --max-cycles=1                 # otherwise
      mark_consumed(selected_item)  # set consumed: true, consumed_by, consumed_at
      # Skip Steps 4-5 (already executed above), go to Step 6 (log cycle)
      log_cycle(cycle, goal_id="next-work:{selected_item.title}", result="harvested")
      continue loop  # → Step 1 (kill switch check)

  # Nothing to do THIS cycle — but don't quit yet
  evolve_state.idle_streak += 1
  log "All goals met, no harvested work. Idle streak: {idle_streak}/{max_idle_streak}"

  if evolve_state.idle_streak >= evolve_state.max_idle_streak:
    log "Stagnation: {max_idle_streak} consecutive idle cycles. Nothing left to improve."
    STOP → go to Teardown

  # NOT stagnant yet — re-measure next cycle (external changes, new harvested work)
  log "Re-measuring next cycle in case conditions changed..."
  continue loop  # → Step 1 (kill switch check)

# We have failing goals — reset idle streak
evolve_state.idle_streak = 0

# Sort by weight (highest priority first)
failing_goals.sort(by=weight, descending)

# Simple strike check: skip goals that failed the last 3 consecutive cycles
for goal in failing_goals:
  recent = last_3_cycles_for(goal.id)
  if all(r.result == "regressed" for r in recent):
    log "Skipping {goal.id}: regressed 3 consecutive cycles. Needs human attention."
    continue
  selected = goal
  break

if no goal selected:
  log "All failing goals have regressed 3+ times. Human intervention needed."
  STOP → go to Teardown
```

### Step 4: Execute

**If `--dry-run`:** Report the selected goal (or harvested item) and stop.

```
log "Dry run: would work on '{selected.id}' (weight: {selected.weight})"
log "Description: {selected.description}"
log "Check command: {selected.check}"

# Also show queued harvested work
if [ -f .agents/rpi/next-work.jsonl ]; then
  items = read_unconsumed(next-work.jsonl)
  if items:
    log "Harvested work queue ({len(items)} items):"
    for item in items:
      log "  - [{item.severity}] {item.title} ({item.type})"

STOP → go to Teardown
```

**Otherwise:** Run a full /rpi cycle on the selected goal.

```
/rpi "Improve {selected.id}: {selected.description}" --auto --max-cycles=1 --test-first   # if --test-first set
/rpi "Improve {selected.id}: {selected.description}" --auto --max-cycles=1                 # otherwise
```

This internally runs the full lifecycle:
- `/research` — understand the problem
- `/plan` — decompose into issues
- `/pre-mortem` — validate the plan
- `/crank` — implement (spawns workers)
- `/vibe` — validate the code
- `/post-mortem` — extract learnings + `ao forge` (COMPOUNDING)

**Wait for /rpi to complete before proceeding.**

### Step 5: Full-Fitness Regression Gate

**CRITICAL: Re-run ALL goals, not just the target.**

After /rpi completes, re-run MEASURE_FITNESS on **every goal** (same as Step 2). Write result to `fitness-{CYCLE}-post.json`.

Compare the pre-cycle snapshot (`fitness-{CYCLE}.json`) against the post-cycle snapshot (`fitness-{CYCLE}-post.json`) for **ALL goals**:

```
# Load pre-cycle results
pre_results = load("fitness-{CYCLE}.json")

# Re-measure ALL goals (writes fitness-{CYCLE}-post.json)
post_results = MEASURE_FITNESS()

# Check the target goal
if selected_goal.post_result == "pass":
  outcome = "improved"
else:
  outcome = "unchanged"

# FULL REGRESSION CHECK: compare ALL goals, not just the target
newly_failing = []
for goal in post_results.goals:
  pre = pre_results.find(goal.id)
  if pre.result == "pass" and goal.result == "fail":
    newly_failing.append(goal.id)

if newly_failing:
  outcome = "regressed"
  log "REGRESSION: {newly_failing} started failing after fixing {selected.id}"

  # Multi-commit revert using cycle start SHA
  cycle_start_sha = pre_results.cycle_start_sha
  commit_count = $(git rev-list --count ${cycle_start_sha}..HEAD)
  if commit_count == 0:
    log "No commits to revert"
  elif commit_count == 1:
    git revert HEAD --no-edit
  else:
    git revert --no-commit ${cycle_start_sha}..HEAD
    git commit -m "revert: evolve cycle ${CYCLE} regression in {newly_failing}"
  log "Reverted ${commit_count} commits. Moving to next goal."
```

**Snapshot enforcement:** Validate `fitness-{CYCLE}-post.json` was written and is valid JSON before proceeding.

### Step 6: Log Cycle

Append to `.agents/evolve/cycle-history.jsonl`:

```jsonl
{"cycle": 1, "goal_id": "test-pass-rate", "result": "improved", "commit_sha": "abc1234", "timestamp": "2026-02-11T21:00:00Z"}
{"cycle": 2, "goal_id": "doc-coverage", "result": "regressed", "commit_sha": "def5678", "reverted_to": "abc1234", "timestamp": "2026-02-11T21:30:00Z"}
```

### Step 7: Loop or Stop

```
evolve_state.cycle += 1

# Only stop for max-cycles if the user explicitly set one
if evolve_state.max_cycles != Infinity and evolve_state.cycle >= evolve_state.max_cycles:
  log "Max cycles ({max_cycles}) reached."
  STOP → go to Teardown

# Otherwise: loop back to Step 1 (kill switch check) — run forever
```

### Teardown

**Auto-run /post-mortem on the full evolution session:**

```
/post-mortem "evolve session: $CYCLE cycles, goals improved: X, harvested: Y"
```

This captures learnings from the ENTIRE evolution run (all cycles, all /rpi invocations) in one council review. The post-mortem harvests follow-up items into `next-work.jsonl`, feeding the next `/evolve` session.

**Then write session summary:**

```bash
cat > .agents/evolve/session-summary.md << EOF
# /evolve Session Summary

**Date:** $(date -Iseconds)
**Cycles:** $CYCLE of $MAX_CYCLES
**Goals measured:** $(wc -l < GOALS.yaml goals)

## Cycle History
$(cat .agents/evolve/cycle-history.jsonl)

## Final Fitness
$(cat .agents/evolve/fitness-${CYCLE}.json)

## Post-Mortem
<path to post-mortem report from above>

## Next Steps
- Run \`/evolve\` again to continue improving
- Run \`/evolve --dry-run\` to check current fitness without executing
- Create \`~/.config/evolve/KILL\` to prevent future runs
- Create \`.agents/evolve/STOP\` for a one-time local stop
EOF
```

Report to user:
```
## /evolve Complete

Cycles: N of M
Goals improved: X
Goals regressed: Y (reverted)
Goals unchanged: Z
Post-mortem: <verdict> (see <report-path>)

Run `/evolve` again to continue improving.
```

---

Read `references/compounding.md` for details on how the knowledge flywheel and work harvesting compound across cycles.

---

## Kill Switch

Two paths, checked at every cycle boundary:

| File | Purpose | Who Creates It |
|------|---------|---------------|
| `~/.config/evolve/KILL` | Permanent stop (outside repo) | Human |
| `.agents/evolve/STOP` | One-time local stop | Human or automation |

To stop /evolve:
```bash
echo "Taking a break" > ~/.config/evolve/KILL    # Permanent
echo "done for today" > .agents/evolve/STOP       # Local, one-time
```

To re-enable:
```bash
rm ~/.config/evolve/KILL
rm .agents/evolve/STOP
```

---

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--max-cycles=N` | unlimited | Optional hard cap. Without this, loop runs forever. |
| `--test-first` | off | Pass `--test-first` through to `/rpi` → `/crank` |
| `--dry-run` | off | Measure fitness and show plan, don't execute |

---

Read `references/goals-schema.md` for the GOALS.yaml format.

---

## Artifacts

| File | Purpose |
|------|---------|
| `GOALS.yaml` | Fitness goals (repo root) |
| `.agents/evolve/fitness-{N}.json` | Pre-cycle fitness snapshot (continuous values) |
| `.agents/evolve/fitness-{N}-post.json` | Post-cycle fitness snapshot (for regression comparison) |
| `.agents/evolve/cycle-history.jsonl` | Cycle outcomes log (includes commit SHAs) |
| `.agents/evolve/session-summary.md` | Session wrap-up |
| `.agents/evolve/STOP` | Local kill switch |
| `.agents/evolve/KILLED.json` | Kill acknowledgment |
| `~/.config/evolve/KILL` | External kill switch |

---

---

## Examples

### Infinite Autonomous Improvement

**User says:** `/evolve`

**What happens:**
1. Agent checks kill switch files (none found, continues)
2. Agent measures fitness against GOALS.yaml (3 of 5 goals passing)
3. Agent selects worst-failing goal by weight (test-pass-rate)
4. Agent invokes `/rpi "Improve test-pass-rate"` with full lifecycle
5. Agent re-measures fitness post-cycle (test-pass-rate now passing, all others unchanged)
6. Agent logs cycle to history, increments cycle counter
7. Agent loops to next cycle, selects next failing goal
8. After all goals pass, agent checks harvested work from post-mortem — finds 3 items
9. Agent works through harvested items, each generating more via post-mortem
10. After 3 consecutive idle cycles (no failing goals, no harvested work), agent runs `/post-mortem` and writes session summary
11. To stop earlier: create `~/.config/evolve/KILL` or `.agents/evolve/STOP`

**Result:** Runs forever — fixing goals, consuming harvested work, re-measuring. Only stops on kill switch or stagnation (3 idle cycles).

### Dry-Run Mode

**User says:** `/evolve --dry-run`

**What happens:**
1. Agent measures fitness (3 of 5 goals passing)
2. Agent identifies worst-failing goal (doc-coverage, weight 5)
3. Agent reports what would be worked on: "Dry run: would work on 'doc-coverage' (weight: 5)"
4. Agent shows harvested work queue (2 items from prior RPI cycles)
5. Agent stops without executing

**Result:** Fitness report and next-action preview without code changes.

### Regression with Revert

**User says:** `/evolve --max-cycles=3`

**What happens:**
1. Agent improves goal A in cycle 1 (commit abc123)
2. Agent measures fitness post-cycle: goal A passes, but goal B now fails (regression)
3. Agent reverts commit abc123 with annotated message
4. Agent logs regression to history, moves to next goal
5. Agent completes 3 cycles (cap reached), runs post-mortem

**Result:** Fitness regressions are auto-reverted, preventing compounding failures.

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `/evolve` exits immediately with "KILL SWITCH ACTIVE" | Kill switch file exists | Remove `~/.config/evolve/KILL` or `.agents/evolve/STOP` to re-enable |
| "No goals to measure" error | GOALS.yaml missing or empty | Create GOALS.yaml in repo root with fitness goals (see references/goals-schema.md) |
| Cycle completes but fitness unchanged | Goal check command is always passing or always failing | Verify check command logic in GOALS.yaml produces exit code 0 (pass) or non-zero (fail) |
| Regression revert fails | Multiple commits in cycle or uncommitted changes | Check cycle-start SHA in fitness snapshot, commit or stash changes before retrying |
| Harvested work never consumed | All goals passing but `next-work.jsonl` not read | Check file exists and has `consumed: false` entries. Agent picks harvested work after goals met. |
| Loop stops after N cycles | `--max-cycles` was set (or old default of 10) | Omit `--max-cycles` flag — default is now unlimited. Loop runs until kill switch or 3 idle cycles. |

---

## See Also

- `skills/rpi/SKILL.md` — Full lifecycle orchestrator (called per cycle)
- `skills/vibe/SKILL.md` — Code validation (called by /rpi)
- `skills/council/SKILL.md` — Multi-model judgment (called by /rpi)
- `GOALS.yaml` — Fitness goals for this repo
