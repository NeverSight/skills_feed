---
name: retro
description: "Comprehensive session retrospective that turns one session's outcomes into persistent improvements. Adaptive depth: deep by default, with light mode via --light (and tiny-session auto-light). Triggers: \"cwf:retro\", \"retro\", \"retrospective\", \"회고\""
---

# Session Retrospective

Adaptive end-of-session review that converts outcomes into durable process/context/tool improvements. Deep by default; light mode is used with `--light` or for tiny routine sessions. Produces `retro.md` alongside `plan.md` and `lessons.md` in the session artifact directory.

## Quick Start

```text
/retro [path]            # adaptive (deep by default)
/retro --deep [path]     # full analysis with expert lens
/retro --from-run [path] # internal flag when invoked by cwf:run
```

- `path`: optional override for output directory
- `--deep`: force full 7-section analysis (expert lens, learning resources, web search)
- `--from-run`: internal invocation context flag; enables compact report for run-chain orchestration

## Workflow

### 0. Update Live State

Run:

```bash
bash {CWF_PLUGIN_DIR}/scripts/cwf-live-state.sh set . phase="retro"
```

### 1. Locate Output Directory

Resolution order:
1. If `[path]` argument provided, use it
2. Reuse `.cwf/projects/` path already used in this session (plan.md/lessons.md writes)
3. If reused session path date prefix (`YYMMDD`) differs from today's local date, AskUserQuestion:
   - Continue existing session directory (recommended for same logical session across midnight/day rollover)
   - Start a new dated directory for today
4. If user selects a new dated directory, run `{CWF_PLUGIN_DIR}/scripts/next-prompt-dir.sh --bootstrap <title>`, then copy `plan.md` and `lessons.md` from the previous session directory when present so retro context is preserved.
5. If multiple candidates exist, AskUserQuestion with candidates
6. Otherwise run `{CWF_PLUGIN_DIR}/scripts/next-prompt-dir.sh --bootstrap <title>`

#### 1.1 Non-Interactive Fallback (Required)

If AskUserQuestion is unavailable/blocked, do not wait. Resolve path in this order: explicit `[path]` -> `live.dir` -> latest `.cwf/projects/` -> bootstrap via `{CWF_PLUGIN_DIR}/scripts/next-prompt-dir.sh --bootstrap retro-light`. Record a short note (`Fast path` or `Post-Retro Findings`) so the fallback choice is auditable.

#### 1.2 Early Light Fast-Path Short-Circuit (Required)

If invocation includes `--light`, run deterministic fast path immediately after output-dir resolution (before evidence collection and large artifact reads):

```bash
bash {CWF_PLUGIN_DIR}/scripts/retro-light-fastpath.sh \
  --session-dir "{output-dir}" \
  --invocation "{invocation_mode}" \
  --lang "{user-language}"
```

Then validate retro stage gate immediately:

```bash
bash {CWF_PLUGIN_DIR}/scripts/check-run-gate-artifacts.sh \
  --session-dir "{output-dir}" \
  --stage retro \
  --strict
```

Rules:
- Determine `invocation_mode` with the same criteria as Section 3.1 before running this command.
- In non-interactive direct runs, stop after this short-circuit path succeeds.
- Do not call AskUserQuestion in this path.

### 2. Read Existing Artifacts

Skip this section when Section 1.2 completed and execution already ended in non-interactive light mode.

Before reading artifacts, run the evidence collector (it includes best-effort Codex session-log sync with timeout protection):

```bash
bash {CWF_PLUGIN_DIR}/scripts/retro-collect-evidence.sh --session-dir "{output-dir}"
```

Then read `retro-evidence.md` (if generated), `plan.md`, `lessons.md`, and `cwf-state.yaml`. Read AGENTS/adapter docs and project-context docs only when those files exist.

When running deep mode (or when user explicitly specifies a diff baseline/scope), generate coverage-contract artifacts before drafting narrative sections:

```bash
bash {CWF_PLUGIN_DIR}/scripts/retro-coverage-contract.sh \
  --session-dir "{output-dir}" \
  --base-ref "{retro_base_ref:-HEAD~1}"
```

Then cite at least:
- total changed file count (artifact name: "diff-all-excl-session-logs.txt")
- top-level breakdown (artifact name: "diff-top-level-breakdown.txt")
- historical lessons/retro primary corpus count (artifact name: "project-lessons-retro-primary.txt")

### 3. Select Mode

Parse the `--deep` flag from the invocation arguments.

**If `--deep` is present**: mode = deep (full 7 sections).

**If `--deep` is absent**: assess session weight to decide mode:
- **Light** (Sections 1-4 + 7): Only when `--light` is explicitly specified, OR session < 3 turns with routine/simple tasks (config changes, small fixes, doc edits)
- **Default bias**: Deep. Invoking retro is itself a signal that the session warrants analysis. Use `--light` to explicitly request lightweight mode when cost savings is desired.

### 3.2 Light Fast Path (Required for `--light`)

Reuse the command and gate in Section 1.2. Do not rerun unless `retro.md` is missing/invalid. In non-interactive runs, stop after fast path + gate. Do not call AskUserQuestion when fallback policy is sufficient.

### 3.1 Detect Invocation Context

Determine invocation context from arguments and live task:

- **Run-chain invocation**: `--from-run` present, or live task explicitly indicates `cwf:run`.
- **Direct user invocation**: all other cases.

Persist this as:

```yaml
invocation_mode: run_chain | direct
```

### 4. Draft Retro

Draft everything internally before writing to file.

#### Light Mode Path

After fast path bootstrap, enrich sections 1-4 and 7 inline only if time/context budget allows. No sub-agents.

#### Deep Mode Path

Draft sections 1-3 inline (these require full conversation access), then launch parallel sub-agents in two batches.

**Resolve session directory**: Resolve the effective live-state file, then read `live.dir`.

```bash
live_state_file=$(bash {CWF_PLUGIN_DIR}/scripts/cwf-live-state.sh resolve)
```

```yaml
session_dir: "{live.dir value from resolved live-state file}"
```

Apply the [context recovery protocol](../../references/context-recovery-protocol.md) to these files before launching each batch:

| Batch | Agent | Output file |
|-------|-------|-------------|
| 1 | CDM Analysis | `{session_dir}/retro-cdm-analysis.md` |
| 1 | Learning Resources | `{session_dir}/retro-learning-resources.md` |
| 2 | Expert α | `{session_dir}/retro-expert-alpha.md` |
| 2 | Expert β | `{session_dir}/retro-expert-beta.md` |

Stage-tier policy for deep mode outputs:
- **Critical (hard gate)**: `{session_dir}/retro-cdm-analysis.md`
- **Non-critical (soft gate)**: `{session_dir}/retro-learning-resources.md`,
  `{session_dir}/retro-expert-alpha.md`, `{session_dir}/retro-expert-beta.md`

For all outputs: bounded retry = 1 for missing/invalid files.
- Shared output persistence contract: [agent-patterns.md § Sub-agent Output Persistence Contract](../../references/agent-patterns.md#sub-agent-output-persistence-contract).

Run slot preflight before each batch launch:

```bash
bash {CWF_PLUGIN_DIR}/scripts/agent-slot-preflight.sh --required 2 --json
```

- If preflight returns `launch_mode=blocked`, wait/close active agents and retry once.
- If it returns `launch_mode=multi_batch`, run the batch sequentially agent-by-agent.
- Otherwise keep the default parallel launch.

**Batch 1** — launch with the preflight-selected mode (only for agents whose result files are missing or invalid):

- **Agent A — CDM Analysis**: `subagent_type: general-purpose`, `max_turns: 16`. Read `{SKILL_DIR}/references/cdm-guide.md`, analyze Sections 1-3 summary + relevant `cwf-state.yaml`, write Section 4 content to `{session_dir}/retro-cdm-analysis.md`, append `<!-- AGENT_COMPLETE -->`.
- **Agent B — Learning Resources**: `subagent_type: general-purpose`, `max_turns: 20`. Find 2-3 external resources using the Web Research Protocol in `{CWF_PLUGIN_DIR}/references/agent-patterns.md`, write Section 6 content to `{session_dir}/retro-learning-resources.md`, append `<!-- AGENT_COMPLETE -->`.

Wait for Batch 1 to complete. Read output files from session directory:
- `{session_dir}/retro-cdm-analysis.md` — CDM analysis (needed by Batch 2 experts)
- `{session_dir}/retro-learning-resources.md` — Learning resources

Gate behavior after Batch 1:
- If `retro-cdm-analysis.md` remains invalid after retry: **hard fail** deep retro.
- If `retro-learning-resources.md` remains invalid after retry: continue with
  warning and render Section 6 with explicit omission note.
- Record gate path in output (`PERSISTENCE_GATE=HARD_FAIL` or
  `PERSISTENCE_GATE=SOFT_CONTINUE`, or equivalent wording).

**Batch 2** — launch with the preflight-selected mode (after Batch 1, only for agents whose result files are missing or invalid):

- **Agent C — Expert alpha**: `subagent_type: general-purpose`, `max_turns: 20`. Read `{CWF_PLUGIN_DIR}/references/expert-advisor-guide.md` + `{SKILL_DIR}/references/expert-lens-guide.md`, analyze Sections 1-4 summary (including CDM output), write to `{session_dir}/retro-expert-alpha.md`, append `<!-- AGENT_COMPLETE -->`.
- **Agent D — Expert beta**: `subagent_type: general-purpose`, `max_turns: 20`. Same contract as Expert alpha; write to `{session_dir}/retro-expert-beta.md`, append `<!-- AGENT_COMPLETE -->`.

After Batch 2: read output files from session directory (`{session_dir}/retro-expert-alpha.md`, `{session_dir}/retro-expert-beta.md`). Draft Section 5 with the required agreement/disagreement synthesis subsection, then draft Section 7 inline (capability/tool scan), then integrate all results into retro.md.

Gate behavior after Batch 2:
- If either expert file remains invalid after retry: continue with warning and
  render Section 5 from available expert output(s) plus explicit omission note.
- Record soft gate path in output (`PERSISTENCE_GATE=SOFT_CONTINUE` or equivalent).

**Rationale for 2-batch design**: Expert Lens depends on CDM results. Batch 1 produces CDM + Learning in parallel, Batch 2 runs experts after CDM is available.

#### Section 1: Context Worth Remembering

Use section-writing guidance from [section-authoring.md](references/section-authoring.md#section-authoring-guide).

#### Section 2: Collaboration Preferences

Use section-writing guidance from [section-authoring.md](references/section-authoring.md#section-2-collaboration-preferences).

#### Section 3: Waste Reduction

Use section-writing guidance from [section-authoring.md](references/section-authoring.md#section-3-waste-reduction), including mandatory 5 Whys depth for major waste signals.

#### Section 4: Critical Decision Analysis (CDM)

Use section-writing guidance from [section-authoring.md](references/section-authoring.md#section-4-critical-decision-analysis-cdm).

#### Section 5: Expert Lens

Use section-writing guidance from [section-authoring.md](references/section-authoring.md#section-5-expert-lens). Agreement/disagreement synthesis subsection remains mandatory in deep mode.

#### Section 6: Learning Resources

Use section-writing guidance from [section-authoring.md](references/section-authoring.md#section-6-learning-resources).

#### Section 7: Relevant Tools (Capabilities Included)

Use section-writing guidance from [section-authoring.md](references/section-authoring.md#section-7-relevant-tools-capabilities-included), including capability inventory, gap classification, and action path.

### 5. Write retro.md

Write to `{output-dir}/retro.md` using the format below.

Immediately enforce deterministic retro artifact gate:

```bash
bash {CWF_PLUGIN_DIR}/scripts/check-run-gate-artifacts.sh \
  --session-dir "{output-dir}" \
  --stage retro \
  --strict \
  --record-lessons
```

If this gate fails, do not mark retro complete. Fix artifacts/mode labeling first, then re-run the gate.

### 6. Link Session Log

Discover runtime logs under:

1. `.cwf/sessions/`

- Prefer suffix files: `{YYMMDD}-*.claude.md`, `{YYMMDD}-*.codex.md`
- Also allow unsuffixed files: `{YYMMDD}-*.md`

Then:
1. Filter out already-symlinked candidates.
2. Read a sample of each candidate to verify it matches the current session.
3. Ensure `{output-dir}/session-logs/` exists.
4. For each verified log, create a relative symlink:
   ```bash
   ln -s "{relative-log-path}/{filename}" "{output-dir}/session-logs/{filename}"
   ```
5. If no candidates or directories do not exist, skip silently.

### 7. Persist Findings

retro.md is session-specific. Persist findings to project-level improvements with a required ownership check before applying the **eval > state > doc** hierarchy.

#### 7.0 Ownership Gate (Required, before tiering)

For each finding, classify ownership first:

- `owner=repo` — the fix belongs to this repository's local artifacts/policies.
- `owner=plugin` — the fix belongs to CWF plugin/runtime/shared tooling behavior.

Then set apply layer deterministically:

- `owner=repo` -> `apply_layer=local`
- `owner=plugin` -> `apply_layer=upstream`

Required metadata for every persist proposal:

- `owner`
- `apply_layer`
- `promotion_target`
- `due_release`
- `evidence` (command output, artifact path, or session-log line)

Routing rules:

- `owner=repo`: continue with tiering and local target updates.
- `owner=plugin`: do not propose local AGENTS/doc edits as the primary fix. Output an upstream backlog item (issue/patch target under `plugins/cwf/` or related shared runtime files). Local edits are allowed only as clearly marked stopgaps.
- If ownership is ambiguous: default to `owner=plugin`, state uncertainty explicitly, and avoid adding repo-local policy noise.
- Keep durable behavior contracts in AGENTS/runtime adapters. Keep `next-session.md` delta-focused; do not move global contracts there.

After ownership routing, evaluate enforcement mechanisms strongest-first:

1. **Tier 1: Eval/Hook** (deterministic) — Can a script/hook catch this?
   - `check-session.sh` / `session_defaults` for missing artifacts
   - PreToolUse/PostToolUse hook for tool usage patterns
   - Lint rule for style enforcement

2. **Tier 2: State** (structural) — Does this change workflow state?
   - `cwf-state.yaml` schema (new artifacts, stage transitions)
   - `session_defaults` (new always/milestone artifacts)

3. **Tier 3: Doc** (behavioral, last resort) — Only for judgment calls
   - `project-context.md` for architectural patterns
   - AGENTS.md or runtime adapter docs only for rules that can't be automated

**Per-section persist actions**:

- **S1 Context** → `project-context.md` (Tier 3 — context is inherently behavioral). Offer to append new context.
- **S2 Collaboration** → Classify owner first, then evaluate tier. AskUserQuestion "Apply?" for AGENTS.md/adapter changes only when `owner=repo`.
- **S3 Waste / Root causes** → For each 5 Whys structural cause, present: "**Finding**: X. **Owner**: {repo|plugin}. **Apply layer**: {local|upstream}. **Recommended tier**: {1|2|3}. **Mechanism**: {specific change}. **Evidence**: {concrete trace}." Right-placement check: AGENTS.md (or runtime adapters) for behavioral rules, `project-context.md` for architectural patterns, protocol/skill docs for process changes.
- **S4 CDM** → Key lessons through tiers (most → Tier 3 `project-context.md`).
- **S7 Tools** → For `owner=repo`, AskUserQuestion "Implement now?". For `owner=plugin`, AskUserQuestion "Queue upstream issue/patch now?".

**Expert Roster Maintenance** (deep mode only, when Section 5 was produced):

1. Extract expert names from Section 5 (Expert Lens) output
2. Follow the Roster Maintenance procedure in `{CWF_PLUGIN_DIR}/references/expert-advisor-guide.md` (including the retro-specific gap analysis step)
3. Report changes to the user in the retro output (Section 5 or post-section note) for visibility

### 8. Direct Invocation Report (Mandatory)

After writing `retro.md`, always report outcomes to the user.

If `invocation_mode=direct` (user-triggered `/retro` or `cwf:retro`):

1. Provide `Retro Brief` with 4-6 bullets:
   - session objective/result
   - top waste/root-cause signal
   - most important CDM lesson
   - critical tool/capability takeaway
2. Provide `Persist Proposals` with 2-5 concrete items:
   - Finding
   - Owner (`repo`, `plugin`)
   - Apply layer (`local`, `upstream`)
   - Promotion target (gate/script/doc/backlog endpoint)
   - Due release (or due date)
   - Recommended tier (`Eval-Hook`, `State`, `Doc`)
   - Evidence
   - Target file/script (local) or upstream backlog target (plugin)
   - Apply-now recommendation
3. Ask whether to apply persist proposals now:
   - repo-owned items: apply locally now? (yes/no)
   - plugin-owned items: queue upstream issue/patch now? (yes/no)

If `invocation_mode=run_chain`:

- Provide compact 2-3 bullet completion report (pipeline continuity first), and include at least one concrete takeaway (waste/root-cause signal, CDM lesson, or next action).
- Include a short `Persist Proposals` mini-list with 1-2 concrete items that each state owner/apply-layer/target (file or backlog). If no actionable item exists, state that explicitly.
- Do not ask apply-now questions in run-chain mode; keep this report informative and hand off execution decisions to downstream run/ship flow.

### 9. Post-Retro Discussion

The user may continue the conversation after the retro. During post-retro discussion:
- Update `retro.md` — append under `### Post-Retro Findings`
- Update `lessons.md` with new learnings
- **Ownership check first** — for each new learning, classify `owner`/`apply_layer`, then evaluate through eval > state > doc.
- If `owner=plugin`, append an upstream backlog note instead of adding repo-local policy prose.
- For deep retro lessons, include metadata lines:
  - `- **Owner**: \`repo|plugin\``
  - `- **Apply Layer**: \`local|upstream\``
  - `- **Promotion Target**: \`...\``
  - `- **Due Release**: \`...\``
- If plugin code was changed, follow normal release procedures (version bump and release note updates in README/docs as needed)

Do not prompt the user to start this discussion.

## Output Format

Use canonical templates from [section-authoring.md](references/section-authoring.md#output-templates) for both light/deep modes.

## Rules

1. Never duplicate content already in lessons.md.
2. Be specific — cite session moments, not generic advice.
3. Keep each section focused; if there is no meaningful signal, state that briefly.
4. AGENTS.md/runtime adapter changes require explicit user approval.
5. Use the deterministic gate checklist in [retro-gates-checklist.md](references/retro-gates-checklist.md) for deep-mode artifacts, persistence tiering, and direct-invocation reporting requirements.
6. For Section 5 in deep mode, use `{SKILL_DIR}/references/expert-lens-guide.md` and include the mandatory agreement/disagreement synthesis subsection.
7. **Language override**: `retro.md` and deep-mode companion outputs are written in the user's language.

## References

- `{SKILL_DIR}/references/cdm-guide.md` — CDM probe methodology and output format
- `{SKILL_DIR}/references/expert-lens-guide.md` — Retro-specific expert lens constraints and output format
- [section-authoring.md](references/section-authoring.md) — Section 1-7 writing guidance and canonical light/deep output templates
- [retro-gates-checklist.md](references/retro-gates-checklist.md) — Deterministic retro artifact gates and reporting checklist
- [expert-advisor-guide.md](../../references/expert-advisor-guide.md) — Expert identity, grounding, selection, and retro mode format
- [agent-patterns.md](../../references/agent-patterns.md) — Shared agent orchestration patterns
