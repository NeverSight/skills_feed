---
name: rpi
tier: orchestration
description: 'Full RPI lifecycle orchestrator. Research → Plan → Pre-mortem → Crank → Vibe → Post-mortem. One command, sequential skill invocations with human gates and autonomous validation. Triggers: "rpi", "full lifecycle", "end to end", "research to production".'
dependencies:
  - research    # required - Phase 1
  - plan        # required - Phase 2
  - pre-mortem  # required - Phase 3 (gate)
  - crank       # required - Phase 4 (implementation)
  - vibe        # required - Phase 5 (gate)
  - post-mortem # required - Phase 6
  - ratchet     # required - checkpoint tracking
metadata:
  internal: false
---

# /rpi — Full RPI Lifecycle Orchestrator

> **Quick Ref:** One command, full lifecycle. Research → Plan → Pre-mortem → Crank → Vibe → Post-mortem. The session IS the lead. Sub-skills manage their own teams.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## Quick Start

```bash
/rpi "add user authentication"              # Full lifecycle, fully autonomous (default)
/rpi --interactive "add user authentication" # Human gates at research + plan
/rpi --from=plan "add auth"                 # Skip research, start from plan
/rpi --from=crank ag-23k                    # Skip to crank with existing epic
/rpi --from=vibe                            # Just run final validation + post-mortem
/rpi --loop --max-cycles=3 "add auth"       # Gate 4 loop: post-mortem FAIL -> spawn another /rpi cycle
```

## Architecture

```
/rpi <goal | epic-id> [--from=<phase>] [--interactive]
  │  (session = the lead, no TeamCreate)
  │
  ├── Phase 1: /research ── auto (default) or human gate (--interactive)
  ├── Phase 2: /plan ────── auto (default) or human gate (--interactive)
  ├── Phase 3: /pre-mortem ── auto (FAIL → retry loop)
  ├── Phase 4: /crank ────── autonomous (manages own teams)
  ├── Phase 5: /vibe ──────── auto (FAIL → retry loop)
  └── Phase 6: /post-mortem ── auto (council + retro + flywheel)
```

**Human gates (default):** 0 — fully autonomous, all gates are retry loops
**Human gates (--interactive mode):** 2 (research + plan approval, owned by those skills)
**Retry gates:** pre-mortem FAIL → re-plan, vibe FAIL → re-crank, crank BLOCKED/PARTIAL → re-crank (max 3 attempts each)
**Gate 4 (optional):** post-mortem FAIL → spawn another /rpi cycle (enabled via `--loop`)

## Phase Data Contracts

| Transition | Output | Extraction | Input to Next |
|------------|--------|------------|---------------|
| → Research | `.agents/research/YYYY-MM-DD-<slug>.md` | `ls -t .agents/research/ \| head -1` | /plan reads .agents/research/ automatically |
| Research → Plan | Plan doc + bd epic | Most recent epic from `bd list --type epic` | epic-id stored in session state |
| Plan → Pre-mortem | `.agents/plans/YYYY-MM-DD-<slug>.md` | /pre-mortem auto-discovers most recent plan | No args needed |
| Pre-mortem → Crank | Council report with verdict | Grep verdict from council report | epic-id passed to /crank |
| Crank → Vibe | Committed code + closed issues | Check `<promise>` tag | /vibe runs on recent changes |
| Vibe → Post-mortem | Council report with verdict | Grep verdict from council report | epic-id passed to /post-mortem |

## Execution Steps

Given `/rpi <goal | epic-id> [--from=<phase>] [--interactive]`:

### Step 0: Setup

```bash
mkdir -p .agents/rpi
```

Determine the starting phase:
- Default: Phase 1 (research)
- `--from=plan`: Start at Phase 2
- `--from=pre-mortem`: Start at Phase 3
- `--from=crank`: Start at Phase 4 (requires epic-id)
- `--from=vibe`: Start at Phase 5
- `--from=post-mortem`: Start at Phase 6

If input looks like an epic-id (matches `ag-*` or similar bead prefix pattern), treat it as an existing epic and skip to the appropriate phase (default: crank if no --from specified).

**Check for harvested next-work from prior RPI cycles:**

```bash
if [ -f .agents/rpi/next-work.jsonl ]; then
  # Read unconsumed entries (consumed: false)
  # Schema: .agents/rpi/next-work.schema.md
fi
```

If unconsumed entries exist in `.agents/rpi/next-work.jsonl`:
- In `--auto` mode: use the highest-severity item's title as the goal (no user prompt)
- In `--interactive` mode: present items via AskUserQuestion and let user choose or provide custom goal
- If goal was already provided by the user, ignore next-work.jsonl (explicit goal takes precedence)

Initialize state:
```
rpi_state = {
  goal: "<goal string>",
  epic_id: null,     # populated after Phase 2
  phase: "<starting phase>",
  auto: <true unless --interactive flag present>,
  cycle: 1,          # RPI iteration number (incremented on --spawn-next)
  parent_epic: null,  # epic ID from prior cycle (if spawned from next-work)
  verdicts: {}       # populated as phases complete
}
```

### Phase 1: Research

**Skip if:** `--from` is set to a later phase.

```
Skill(skill="research", args="<goal> --auto")   # always --auto unless --interactive
```

By default, /research runs with `--auto` (skips human gate, proceeds automatically).
With `--interactive`, the research skill shows its human gate (AskUserQuestion). /rpi trusts the outcome:
- User approves → research complete, proceed
- User abandons → /rpi stops with message: "Research abandoned by user."

**After research completes:**
1. Record: which research file was produced
2. Write phase summary (keep context lean):
   ```
   Read the research output file.
   Write a 500-token summary to .agents/rpi/phase-1-summary.md
   ```
3. Ratchet checkpoint:
   ```bash
   ao ratchet record research 2>/dev/null || true
   ```

### Phase 2: Plan

**Skip if:** `--from` is set to a later phase.

```
Skill(skill="plan", args="<goal> --auto")   # always --auto unless --interactive
```

By default, /plan runs with `--auto` (skips human gate, proceeds automatically).
With `--interactive`, the plan skill shows its human gate. /rpi trusts the outcome.

**After plan completes:**
1. Extract epic-id:
   ```bash
   # Find most recent epic
   EPIC_ID=$(bd list --type epic --status open 2>/dev/null | head -1 | grep -o 'ag-[a-z0-9]*')
   ```
   Store in `rpi_state.epic_id`.

2. Write phase summary to `.agents/rpi/phase-2-summary.md`

3. Ratchet checkpoint:
   ```bash
   ao ratchet record plan 2>/dev/null || true
   ```

### Phase 3: Pre-mortem

**Skip if:** `--from` is set to a later phase.

```
Skill(skill="pre-mortem")
```

Pre-mortem auto-discovers the most recent plan. No args needed.

**After pre-mortem completes:**
1. Extract verdict from council report:
   ```bash
   REPORT=$(ls -t .agents/council/*pre-mortem*.md 2>/dev/null | head -1)
   ```
   Read the report file and find the verdict line (`## Council Verdict: PASS / WARN / FAIL`).

2. Apply gate logic:
   - **PASS:** Auto-proceed. Log: "Pre-mortem: PASS"
   - **WARN:** Auto-proceed. Log: "Pre-mortem: WARN — see report for concerns"
   - **FAIL:** Retry loop (max 2 retries):
     1. Read the full pre-mortem report to extract specific failure reasons
     2. Log: "Pre-mortem: FAIL (attempt N/3) — retrying plan with feedback"
     3. Re-invoke `/plan` with the goal AND the failure context:
        ```
        Skill(skill="plan", args="<goal> --auto --context 'Pre-mortem FAIL: <key concerns from report>'")
        ```
     4. Re-invoke `/pre-mortem` on the new plan
     5. If still FAIL after 3 total attempts → stop with message:
        "Pre-mortem failed 3 times. Last report: <path>. Manual intervention needed."

3. Store verdict in `rpi_state.verdicts.pre_mortem`

4. Write phase summary to `.agents/rpi/phase-3-summary.md`

5. Ratchet checkpoint:
   ```bash
   ao ratchet record pre-mortem 2>/dev/null || true
   ```

### Phase 4: Crank (Implementation)

**Requires:** `rpi_state.epic_id` (from Phase 2 or --from=crank with epic-id argument)

```
Skill(skill="crank", args="<epic-id>")
```

Crank manages its own waves, teams, and internal validation. /rpi waits for completion.

**After crank completes:**
1. Check completion status from crank's output. Look for `<promise>` tags:
   - `<promise>DONE</promise>` → Proceed to Phase 5
   - `<promise>BLOCKED</promise>` → Retry (max 2 retries):
     1. Read crank output to extract block reason
     2. Log: "Crank: BLOCKED (attempt N/3) — retrying with context"
     3. Re-invoke `/crank` with epic-id and block context
     4. If still BLOCKED after 3 total attempts → stop with message:
        "Crank blocked 3 times. Reason: <reason>. Manual intervention needed."
   - `<promise>PARTIAL</promise>` → Retry remaining (max 2 retries):
     1. Read crank output to identify remaining items
     2. Log: "Crank: PARTIAL (attempt N/3) — retrying remaining items"
     3. Re-invoke `/crank` with epic-id (it picks up unclosed issues)
     4. If still PARTIAL after 3 total attempts → stop with message:
        "Crank partial after 3 attempts. Remaining: <items>. Manual intervention needed."

2. Write phase summary to `.agents/rpi/phase-4-summary.md`

3. Ratchet checkpoint:
   ```bash
   ao ratchet record implement 2>/dev/null || true
   ```

### Phase 5: Final Vibe

```
Skill(skill="vibe", args="recent")
```

Vibe runs a full council on recent changes (cross-wave consistency check).

**After vibe completes:**
1. Extract verdict from council report:
   ```bash
   REPORT=$(ls -t .agents/council/*vibe*.md 2>/dev/null | head -1)
   ```
   Read and extract verdict.

2. Apply gate logic:
   - **PASS:** Auto-proceed. Log: "Vibe: PASS"
   - **WARN:** Auto-proceed. Log: "Vibe: WARN — see report for concerns"
   - **FAIL:** Retry loop (max 2 retries):
     1. Read the full vibe report to extract specific failure reasons
     2. Log: "Vibe: FAIL (attempt N/3) — retrying crank with feedback"
     3. Re-invoke `/crank` with the epic-id AND the failure context:
        ```
        Skill(skill="crank", args="<epic-id> --context 'Vibe FAIL: <key issues from report>'")
        ```
     4. Re-invoke `/vibe` on the new changes
     5. If still FAIL after 3 total attempts → stop with message:
        "Vibe failed 3 times. Last report: <path>. Manual intervention needed."

3. Store verdict in `rpi_state.verdicts.vibe`

4. Write phase summary to `.agents/rpi/phase-5-summary.md`

5. Ratchet checkpoint:
   ```bash
   ao ratchet record vibe 2>/dev/null || true
   ```

### Phase 6: Post-mortem

```
Skill(skill="post-mortem", args="<epic-id>")
```

Post-mortem runs council + retro + flywheel feed. By default, /rpi ends after post-mortem (enable Gate 4 loop via `--loop`).

**After post-mortem completes:**
1. Ratchet checkpoint (with cycle lineage):
   ```bash
   ao ratchet record post-mortem --cycle=<rpi_state.cycle> --parent-epic=<rpi_state.parent_epic> 2>/dev/null || true
   ```

### Phase 6.5: Gate 4 Loop (Optional) — Post-mortem → Spawn Another /rpi

**Default behavior:** /rpi ends after Phase 6.

**Enable loop:** pass `--loop` (and optionally `--max-cycles=<n>`).

**Gate 4 goal:** make the "ITERATE vs TEMPER" decision explicit, and if iteration is required, run another full /rpi cycle with tighter context.

**Loop decision input:** the most recent post-mortem council verdict.

1. Find the most recent post-mortem report:
   ```bash
   REPORT=$(ls -t .agents/council/*post-mortem*.md 2>/dev/null | head -1)
   ```
2. Read `REPORT` and extract the verdict line (`## Council Verdict: PASS / WARN / FAIL`).
3. Apply gate logic (only when `--loop` is set). If verdict is PASS or WARN, stop (TEMPER path). If verdict is FAIL, iterate (spawn another /rpi cycle), up to `--max-cycles`.
4. Iterate behavior (spawn). Read the post-mortem report and extract 3 concrete fixes, then re-invoke /rpi from Phase 1 with a tightened goal that includes the fixes:
   ```
   /rpi "<original goal> (Iteration <n>): Fix <item1>; <item2>; <item3>"
   ```
   If still FAIL after `--max-cycles` total cycles, stop and require manual intervention (file follow-up bd issues).

### Phase 6.6: Spawn Next Work (Optional) — Post-mortem → Queue Next RPI

**Enable:** pass `--spawn-next` flag.

**Complementary to Gate 4:** Gate 4 (`--loop`) handles FAIL→iterate (same goal, tighter). `--spawn-next` handles PASS/WARN→new-goal (different work harvested from post-mortem).

1. Read `.agents/rpi/next-work.jsonl` for unconsumed entries (schema: `.agents/rpi/next-work.schema.md`)
2. If unconsumed entries exist:
   - If `--dry-run` is set: report items but do NOT mutate next-work.jsonl (skip consumption). Log: "Dry run — items not marked consumed."
   - Otherwise: mark the current cycle's entry as consumed (set `consumed: true`, `consumed_by: <epic-id>`, `consumed_at: <now>`)
   - Report harvested items to user with suggested next command:
     ```
     ## Next Work Available

     Post-mortem harvested N follow-up items from <source_epic>:
     1. <title> (severity: <severity>, type: <type>)
     ...

     To start the next RPI cycle:
       /rpi "<highest-severity item title>"
     ```
   - Do NOT auto-invoke `/rpi` — the user decides when to start the next cycle
3. If no unconsumed entries: report "No follow-up work harvested. Flywheel stable."

**Note:** Only `--spawn-next` mutates next-work.jsonl (marks consumed). Phase 0 read is read-only.

### Step Final: Report

Summarize the entire lifecycle to the user:

```markdown
## /rpi Complete

**Goal:** <goal>
**Epic:** <epic-id>
**Cycle:** <rpi_state.cycle> (parent: <rpi_state.parent_epic or "none">)

| Phase | Verdict/Status |
|-------|---------------|
| Research | Complete |
| Plan | Complete (<N> issues, <M> waves) |
| Pre-mortem | <PASS/WARN/FAIL> |
| Crank | <DONE/BLOCKED/PARTIAL> |
| Vibe | <PASS/WARN/FAIL> |
| Post-mortem | Complete |
| Next Work | <N items harvested / none> |

**Artifacts:**
- Research: .agents/research/...
- Plan: .agents/plans/...
- Pre-mortem: .agents/council/...
- Vibe: .agents/council/...
- Post-mortem: .agents/council/...
- Learnings: .agents/learnings/...
- Next Work: .agents/rpi/next-work.jsonl
```

## Error Handling

| Failure | Behavior |
|---------|----------|
| Skill invocation fails | Log error, retry once. If still fails → stop with checkpoint. |
| User abandons at sub-skill gate | /rpi stops with checkpoint (only in --interactive mode) |
| /crank returns BLOCKED | Re-crank with context (max 2 retries). If still blocked → stop. |
| /crank returns PARTIAL | Re-crank remaining items with context (max 2 retries). If still partial → stop. |
| Pre-mortem FAIL | Re-plan with fail feedback → re-run pre-mortem (max 3 total attempts) |
| Vibe FAIL | Re-crank with fail feedback → re-run vibe (max 3 total attempts) |
| Max retries exhausted | Stop with message + path to last report. Manual intervention needed. |
| Context feels degraded | Log warning, suggest starting new session with --from |

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--from=<phase>` | `research` | Start from this phase (research, plan, pre-mortem, crank, vibe, post-mortem) |
| `--interactive` | off | Enable human gates in /research and /plan. Without this flag, /rpi runs fully autonomous. |
| `--auto` | on | (Legacy, now default) Fully autonomous — zero human gates. Kept for backwards compatibility. |
| `--loop` | off | Enable Gate 4 loop: after /post-mortem, iterate only when post-mortem verdict is FAIL (spawns another /rpi cycle). |
| `--max-cycles=<n>` | `1` | Hard cap on total /rpi cycles when `--loop` is set (recommended: 3). |
| `--spawn-next` | off | After post-mortem, read harvested next-work items and report suggested next `/rpi` command. Marks consumed entries. |
| `--dry-run` | off | With `--spawn-next`: report items without marking consumed. Useful for testing the consumption flow. |

## See Also

- `skills/research/SKILL.md` — Phase 1
- `skills/plan/SKILL.md` — Phase 2
- `skills/pre-mortem/SKILL.md` — Phase 3
- `skills/crank/SKILL.md` — Phase 4
- `skills/vibe/SKILL.md` — Phase 5
- `skills/post-mortem/SKILL.md` — Phase 6
