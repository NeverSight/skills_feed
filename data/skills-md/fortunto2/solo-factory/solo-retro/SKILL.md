---
name: solo-retro
description: Post-pipeline retrospective — parse logs, score process quality, find waste patterns, suggest skill/script patches. Use after pipeline completes or when user says "retro", "evaluate pipeline", "what went wrong", "pipeline review", "check pipeline logs".
license: MIT
metadata:
  author: fortunto2
  version: "2.1.0"
  openclaw:
    emoji: "🔮"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__session_search, mcp__solograph__codegraph_explain, mcp__solograph__codegraph_query
argument-hint: "[project-name]"
---

# /retro

This skill is self-contained — follow the phases below instead of delegating to other skills (/review, /audit, /build) or spawning Task subagents. Run all analysis directly.

Post-pipeline retrospective. Parses pipeline logs, counts productive vs wasted iterations, identifies recurring failure patterns, scores the pipeline run, and suggests concrete patches to skills/scripts to prevent the same failures next time.

## When to use

After a pipeline completes (or gets cancelled). This is the process quality check — `/review` checks **code quality**, `/retro` checks **pipeline process quality**.

Can also be used standalone on any project — with or without pipeline logs.

## MCP Tools (use if available)

- `session_search(query)` — find past pipeline runs and known issues
- `codegraph_explain(project)` — understand project architecture context
- `codegraph_query(query)` — query code graph for project metadata

If MCP tools are not available, fall back to Glob + Grep + Read.

## Phase 1: Locate Artifacts

1. **Detect project** from `$ARGUMENTS` or CWD:
   - If argument provided: use it as project name
   - Otherwise: extract from CWD basename (e.g., `~/projects/my-app` -> `my-app`)

2. **Find pipeline state file:** `.solo/pipelines/solo-pipeline-{project}.local.md` (project-local) or `~/.solo/pipelines/solo-pipeline-{project}.local.md` (global fallback)
   - If it exists: pipeline is still running or wasn't cleaned up — read YAML frontmatter for `project_root:`
   - If not: pipeline completed — use CWD as project root

3. **Verify artifacts exist (parallel reads):**
   - Pipeline log: `{project_root}/.solo/pipelines/pipeline.log`
   - Iter logs: `{project_root}/.solo/pipelines/iter-*.log`
   - Progress file: `{project_root}/.solo/pipelines/progress.md`
   - Plan-done directory: `{project_root}/docs/plan-done/`
   - Active plan: `{project_root}/docs/plan/`

4. **Determine analysis mode:**
   - If pipeline log exists: proceed with full log-based analysis (Phases 2-4)
   - If NO pipeline log: switch to **fallback mode** (see Fallback Analysis below)

5. **Count iter logs** (if they exist): `ls {project_root}/.solo/pipelines/iter-*.log | wc -l`
   - Report: "Found {N} iteration logs"

## Fallback Analysis (No Pipeline Logs)

If no pipeline logs exist, the retro can still provide value by analyzing:

1. **Git history:** `git log --oneline --since="1 week ago"` — commit frequency, patterns, conventional format
2. **Test results:** run test suite if configured in CLAUDE.md or package.json
3. **Build status:** run build if configured
4. **CLAUDE.md changes:** `git log --oneline -- CLAUDE.md` — how docs evolved
5. **Code quality metrics:** file counts, TODO/FIXME density, dead code indicators
6. **Project structure:** completeness of docs/, tests/, CI config

Skip Phases 2-4 and proceed directly to Phase 5 (Plan Fidelity) and Phase 6 (Git & Code Quality). Adjust Phase 7 scoring to weight available data more heavily.

## Phase 2: Parse Pipeline Log (quantitative)

Read `pipeline.log` in full. Parse line-by-line, extracting structured data from log tags:

**Log format:** `[HH:MM:SS] TAG | message`

**Extract by tag:**

| Tag | What to extract |
|-----|----------------|
| `START` | Pipeline run boundary — count restarts (multiple START lines = restarts) |
| `STAGE` | `iter N/M \| stage S/T: {stage_id}` — iteration count per stage |
| `SIGNAL` | `<solo:done/>` or `<solo:redo/>` — which stages got completion signals |
| `INVOKE` | Skill invoked — extract skill name, check for wrong names |
| `ITER` | `commit: {sha} \| result: {stage complete\|continuing}` — per-iteration outcome |
| `CHECK` | `{stage} \| {path} -> FOUND\|NOT FOUND` — marker file checks |
| `FINISH` | `Duration: {N}m` — total duration per run |
| `MAXITER` | `Reached max iterations ({N})` — hit iteration ceiling |
| `QUEUE` | Plan cycling events (activating, archiving) |
| `CIRCUIT` | Circuit breaker triggered (if present) |
| `CWD` | Working directory changes |
| `CTRL` | Control signals (pause/stop/skip) |

**Compute metrics:**

```
total_runs = count of START lines
total_iterations = count of ITER lines
productive_iters = count of ITER lines with "stage complete"
wasted_iters = total_iterations - productive_iters
waste_pct = wasted_iters / total_iterations * 100
maxiter_hits = count of MAXITER lines
plan_cycles = count of QUEUE lines with "Cycling"

per_stage = {
  stage_id: {
    attempts: count of STAGE lines for this stage,
    successes: count of ITER lines with "stage complete" for this stage,
    waste_ratio: (attempts - successes) / attempts * 100,
  }
}
```

## Phase 3: Parse Progress.md (qualitative)

Read `progress.md` and scan for error patterns:

1. **Unknown skill errors:** grep for `Unknown skill:` — extract which skill name was wrong
2. **Empty iterations:** iterations where "Last 5 lines" show only errors or session header (no actual work done)
3. **Repeated errors:** same error appearing in consecutive iterations -> spin-loop indicator
4. **Doubled signals:** `<solo:done/><solo:done/>` in same iteration -> minor noise (note but don't penalize)
5. **Redo loops:** count how many times build->review->redo->build cycles occurred

For each error pattern found, record:
- Pattern name
- First occurrence (iteration number)
- Total occurrences
- Consecutive streak (max)

## Phase 4: Analyze Iter Logs (sample-based)

Do NOT read all iter logs — could be 60+. Use smart sampling:

1. **First failed iter per pattern:** For each failure pattern found in Phase 3, read the first iter log that shows it
   - Strip ANSI codes when reading: `sed 's/\x1b\[[0-9;]*m//g' < iter-NNN-stage.log | head -100`

2. **First successful iter per stage:** For each stage that eventually succeeded, read the first successful iter log
   - Look for `<solo:done/>` in the output

3. **Final review iter:** Read the last `iter-*-review.log` (the verdict)

4. **Extract from each sampled log:**
   - Tools called (count of tool_use blocks)
   - Errors encountered (grep for `Error`, `error`, `Unknown`, `failed`)
   - Signal output (`<solo:done/>` or `<solo:redo/>` present?)
   - First 5 and last 10 meaningful lines (skip blank lines)

## Phase 5: Plan Fidelity Check

For each track directory in `docs/plan-done/` and `docs/plan/`:

1. **Read spec.md** (if exists):
   - Count acceptance criteria: total `- [ ]` and `- [x]` checkboxes
   - Calculate: `criteria_met = checked / total * 100`

2. **Read plan.md** (if exists):
   - Count tasks: total `- [ ]` and `- [x]` checkboxes
   - Count phases (## headers)
   - Check for SHA annotations (`<!-- sha:... -->`)
   - Calculate: `tasks_done = checked / total * 100`

3. **Compile per-track summary:**
   - Track ID, criteria met %, tasks done %, has SHAs

## Phase 6: Git & Code Quality (lightweight)

Quick checks only — NOT a full /review:

1. **Commit count and format:**
   ```bash
   git -C {project_root} log --oneline | wc -l
   git -C {project_root} log --oneline | head -30
   ```
   - Count commits with conventional format (`feat:`, `fix:`, `chore:`, `test:`, `docs:`, `refactor:`, `build:`, `ci:`, `perf:`)
   - Calculate: `conventional_pct = conventional / total * 100`

2. **Committer breakdown:**
   ```bash
   git -C {project_root} shortlog -sn --no-merges | head -10
   ```

3. **Test status** (if test command exists in CLAUDE.md or package.json):
   - Run test suite, capture pass/fail count
   - If no test command found, skip and note "no tests configured"

4. **Build status** (if build command exists):
   - Run build, capture success/fail
   - If no build command found, skip and note "no build configured"

## Phase 7: Score & Report

Load scoring rubric from `${CLAUDE_PLUGIN_ROOT}/skills/retro/references/eval-dimensions.md`.
If plugin root not available, use the embedded weights:

**Scoring weights:**
- Efficiency (waste %): 25%
- Stability (restarts): 20%
- Fidelity (criteria met): 20%
- Quality (test pass rate): 15%
- Commits (conventional %): 5%
- Docs (plan staleness): 5%
- Signals (clean signals): 5%
- Speed (total duration): 5%

**Note:** In fallback mode (no pipeline logs), redistribute Efficiency and Stability weights to Fidelity, Quality, and Commits.

**Generate report** at `{project_root}/docs/retro/{date}-retro.md`:

```markdown
# Pipeline Retro: {project} ({date})

## Overall Score: {N}/10

## Pipeline Efficiency

| Metric | Value | Rating |
|--------|-------|--------|
| Total iterations | {N} | |
| Productive iterations | {N} ({pct}%) | {emoji} |
| Wasted iterations | {N} ({pct}%) | {emoji} |
| Pipeline restarts | {N} | {emoji} |
| Max-iter hits | {N} | {emoji} |
| Total duration | {time} | {emoji} |

## Per-Stage Breakdown

| Stage | Attempts | Successes | Waste % | Notes |
|-------|----------|-----------|---------|-------|
| scaffold | | | | |
| setup | | | | |
| plan | | | | |
| build | | | | |
| deploy | | | | |
| review | | | | |

## Failure Patterns

### Pattern 1: {name}
- **Occurrences:** {N} iterations
- **Root cause:** {analysis}
- **Wasted:** {N} iterations
- **Fix:** {concrete suggestion with file reference}

### Pattern 2: ...

## Plan Fidelity

| Track | Criteria Met | Tasks Done | SHAs | Rating |
|-------|-------------|------------|------|--------|
| {track-id} | {N}% | {N}% | {yes/no} | {emoji} |

## Code Quality (Quick)

- **Tests:** {N} pass, {N} fail (or "not configured")
- **Build:** PASS / FAIL (or "not configured")
- **Commits:** {N} total, {pct}% conventional format

## Three-Axis Growth

| Axis | Score | Evidence |
|------|-------|----------|
| **Technical** (code, tools, architecture) | {0-10} | {what changed} |
| **Cognitive** (understanding, strategy, decisions) | {0-10} | {what improved} |
| **Process** (harness, skills, pipeline, docs) | {0-10} | {what evolved} |

If only one axis is served — note what's missing.

## Recommendations

1. **[CRITICAL]** {patch suggestion with file:line reference}
2. **[HIGH]** {improvement}
3. **[MEDIUM]** {optimization}
4. **[LOW]** {nice-to-have}

## Suggested Patches

### Patch 1: {file} — {description}

**What:** {one-line description}
**Why:** {root cause reference from Failure Patterns}

\```diff
- old line
+ new line
\```
```

**Rating guide (use these emojis):**
- GREEN = excellent
- YELLOW = acceptable
- RED = needs attention

## Phase 8: Interactive Patching

After generating the report:

1. **Show summary** to user: overall score, top 3 failure patterns, top 3 recommendations

2. **For each suggested patch** (if any), use `AskUserQuestion`:
   - Question: "Apply patch to {file}? {one-line description}"
   - Options: "Apply" / "Skip" / "Show diff first"

3. **If "Show diff first":** display the full diff, then ask again (Apply / Skip)

4. **If "Apply":** use Edit tool to apply the change directly

5. **After all patches processed:**
   - If any patches were applied: suggest committing with `fix(retro): {description}`
   - Do NOT auto-commit — just suggest the command

## Phase 9: CLAUDE.md Revision

After patching, revise the project's CLAUDE.md to keep it lean and useful for future agents.

### Steps:

1. **Read CLAUDE.md** and check size: `wc -c CLAUDE.md`
2. **Add learnings from this retro:**
   - Pipeline failure patterns worth remembering (avoid next time)
   - New workflow rules or process improvements
   - Updated commands or tooling changes
   - Architecture decisions that emerged during the pipeline run
3. **If over 40,000 characters — trim ruthlessly:**
   - Collapse completed phase/milestone histories into one line each
   - Remove verbose explanations — keep terse, actionable notes
   - Remove duplicate info (same thing explained in multiple sections)
   - Remove historical migration notes, old debugging context
   - Remove examples that are obvious from code or covered by skill/doc files
   - Remove outdated troubleshooting for resolved issues
4. **Verify result <= 40,000 characters** — if still over, cut least actionable content
5. **Write updated CLAUDE.md**, update "Last updated" date

### Priority (keep -> cut):
1. **ALWAYS KEEP:** Tech stack, directory structure, Do/Don't rules, common commands, architecture decisions
2. **KEEP:** Workflow instructions, troubleshooting for active issues, key file references
3. **CONDENSE:** Phase histories (one line each), detailed examples, tool/MCP listings
4. **CUT FIRST:** Historical notes, verbose explanations, duplicated content, resolved issues

### Rules:
- Never remove Do/Don't sections — critical guardrails
- Preserve overall section structure and ordering
- Every line must earn its place: "would a future agent need this to do their job?"
- Commit the update: `git add CLAUDE.md && git commit -m "docs: revise CLAUDE.md (post-retro)"`

## Phase 10: Factory Critic (optional)

**Run this phase only if `${CLAUDE_PLUGIN_ROOT}` is available** (i.e., solo-factory is installed). Skip if running as a standalone skill without the factory context.

After evaluating the project pipeline, step back and evaluate **the factory itself** — the skills, scripts, and pipeline logic that produced this result. Be a harsh critic.

### What to evaluate:

1. **Read the skills that were invoked** in this pipeline run (from INVOKE lines in pipeline.log):
   - For each skill: `${CLAUDE_PLUGIN_ROOT}/skills/{stage}/SKILL.md`
   - Did the skill have the right instructions for this project's needs?
   - Did it miss context it should have had?

2. **Read pipeline script** signal handling and stage logic:
   - `${CLAUDE_PLUGIN_ROOT}/scripts/solo-dev.sh`
   - Were there structural issues (wrong stage order, missing re-exec, broken redo)?

3. **Cross-reference with failure patterns** from Phase 3:
   - For each failure: was the root cause in the skill, the script, or the project?
   - Skills that caused waste = factory defects

### Score the factory (not the project):

```
Factory Score: {N}/10

Skill quality:
- {skill}: {score}/10 — {why}
- {skill}: {score}/10 — {why}

Pipeline reliability: {N}/10 — {why}

Missing capabilities:
- {what the factory couldn't do that it should have}

Top factory defects:
1. {defect} → {which file to fix} → {concrete fix}
2. {defect} → {which file to fix} → {concrete fix}
```

### Harness Evolution — think about the bigger picture

After scoring the factory, step back further and think about the **harness** — the entire system that guides agents (CLAUDE.md, docs/, linters, skills, templates). Ask:

1. **Context engineering:** Did the agent have everything it needed in-repo? Or did it struggle because knowledge was missing / scattered / stale?
   - Missing docs -> add to `docs/` or CLAUDE.md
   - Stale docs -> flag for doc-gardening
   - Knowledge only in your head -> encode it

2. **Architectural constraints:** Did the agent break module boundaries, produce inconsistent patterns, or ignore conventions?
   - Repeated boundary violations -> need a linter or structural test
   - Inconsistent patterns -> need golden principle in CLAUDE.md
   - Data shape errors -> need parse-at-boundary enforcement

3. **Decision traces:** What worked well that future agents should reuse? What failed that they should avoid?
   - Good patterns -> capture as precedent in docs or CLAUDE.md
   - Bad patterns -> encode as anti-pattern or lint rule
   - Think: "if another agent hits this same problem tomorrow, what should it find?"

4. **Skill gaps:** Which skills need better instructions? Which new skills should exist?
   - Skill that caused waste -> concrete SKILL.md patch
   - Missing capability -> new skill idea for evolution log

### Write to evolution log:

Append findings to `{project_root}/docs/evolution.md` (create if not exists). If `~/.solo/evolution.md` exists, append there as well for cross-project tracking.

```markdown
## {YYYY-MM-DD} | {project} | Factory Score: {N}/10

Pipeline: {stages run} | Iters: {total} | Waste: {pct}%

### Defects
- **{severity}** | {skill/script}: {description}
  - Fix: {concrete file:change}

### Harness Gaps
- **Context:** {what knowledge was missing or stale for the agent}
- **Constraints:** {what boundary violations or inconsistencies occurred}
- **Precedents:** {patterns worth capturing for future agents — good or bad}

### Missing
- {capability the factory lacked}

### What worked well
- {skill/pattern that performed efficiently}
```

**Rules:**
- Be brutally honest — if a skill is broken, say so
- Every defect must have a concrete fix (file + what to change)
- Track what works well too — don't regress good patterns
- Keep entries compact — this file accumulates over time

## Signal Output

**Output signal:** `<solo:done/>`

**Important:** `/retro` always outputs `<solo:done/>` — it never needs redo. Even if pipeline was terrible, the retro itself always completes.

## Edge Cases

- **No pipeline.log and no git history:** abort with clear message — "No pipeline log or git history found. Nothing to analyze."
- **No pipeline.log but git history exists:** switch to fallback mode (see Fallback Analysis)
- **Empty pipeline.log:** report "Pipeline log is empty — was the pipeline cancelled before any iteration?"
- **No iter logs:** skip Phase 4 sampling, note in report
- **No plan-done:** skip Phase 5, note "No completed plans found"
- **No test/build commands:** skip those checks in Phase 6, note in report
- **Pipeline still running:** warn user — "State file exists, pipeline may still be running. Retro on partial data."

## Reference Files

- `${CLAUDE_PLUGIN_ROOT}/skills/retro/references/eval-dimensions.md` — scoring rubric (8 axes, weights)
- `${CLAUDE_PLUGIN_ROOT}/skills/retro/references/failure-catalog.md` — known failure patterns and fixes
