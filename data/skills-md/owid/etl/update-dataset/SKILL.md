---
name: update-dataset
description: End-to-end dataset update workflow with PR creation, snapshot, meadow, garden, and grapher steps. Use when user wants to update a dataset, refresh data, run ETL update, or mentions updating dataset versions.
---

# Update Dataset (PR → snapshot → steps → grapher)

Use this skill to run a complete dataset update with Claude Code subagents, keep a live progress checklist, and pause for approval at a checkpoint **after every numbered workflow step** before continuing.

## Inputs

- `<namespace>/<old_version>/<name>`
- Get `<new_version>` as today's date by running `date -u +"%Y-%m-%d"`

Optional trailing args:
- branch: The working branch name (defaults to current branch)

Assumptions:
- All artifacts are written to `workbench/<short_name>/`.
- Persist progress to `workbench/<short_name>/progress.md` and update it after each step.

## Progress checklist (maintain, tick live, and persist to progress.md)

(Checkpoint rule: After you finish each item below that represents a workflow step, immediately run the CHECKPOINT procedure. Do not batch multiple steps before a checkpoint.)
- [ ] Parse inputs and resolve: channel, namespace, version, short_name, old_version, branch
- [ ] Clean workbench directory: delete `workbench/<short_name>` unless continuing existing update
- [ ] Run ETL update workflow via `etl-update` subagent (help → dry run → approval → real run)
- [ ] Create or reuse draft PR and work branch
- [ ] Update snapshot and compare to previous version; capture summary
- [ ] Meadow step: run + fix + diff + summarize
- [ ] Garden step: run + fix + diff + summarize
- [ ] Grapher step: run + verify (skip diffs), or explicitly mark N/A
- [ ] CHECKPOINT — present consolidated summary and request approval
- [ ] If approved, commit, push, and update PR description
- [ ] Optional: run indicator upgrade on staging and persist report

Persistence:
- After ticking each item, update `workbench/<short_name>/progress.md` with the current checklist state and a timestamp.

## CHECKPOINT (mandatory user approval)

Always performed **immediately after completing each numbered workflow step** (1–6). Never start the next step until approval is granted.

Procedure (each time):
1. Present a concise summary of what just changed, key diffs/issues resolved, and what the next step will do.
2. Ask exactly: Proceed? reply: yes/no
3. Only continue if the user replies exactly yes (case-insensitive). Any other reply = no; stop and wait.
4. On approval:
   - Update progress checklist (tick the completed item) and write `workbench/<short_name>/progress.md` with timestamp.
   - Commit related changes (if any), push.
   - Update (or append to) the PR description: add a collapsed section titled with the step name (e.g., "Snapshot Update", "Meadow Update") containing the summary.

## Mandatory per-step checkpoints (rule)

You MUST:
- Stop after each workflow step (1–6) and run CHECKPOINT before starting the next (step 7 is optional and still requires a checkpoint if executed).
- Never chain multiple steps inside a single approval.
- Treat missing or ambiguous replies as no.

## Workflow orchestration

0) Initial setup
   - Check if `workbench/<short_name>/progress.md` exists to determine if continuing existing update
   - If starting fresh: delete `workbench/<short_name>` directory if it exists
   - Create fresh `workbench/<short_name>` directory for artifacts

1) Run ETL update command (etl-update subagent)
   - Inputs: `<namespace>/<old_version>/<short_name>` plus any required flags
   - Perform help check, dry run, approval, then real execution; capture summary for later PR notes
   - CHECKPOINT (stop → summarize → ask → require yes)
2) Create PR and integrate update via subagent (etl-pr)
   - Inputs: `<namespace>/<old_version>/<short_name>`
   - Create or reuse draft PR, set up work branch, and incorporate the ETL update outputs
   - CHECKPOINT
3) Snapshot run & compare (snapshot-runner subagent)
   - Inputs: `<namespace>/<new_version>/<short_name>` and `<old_version>`
   - CHECKPOINT
4) Meadow step repair/verify (step-fixer subagent, channel=meadow)
   - Run, fix, re-run; produce diffs
   - Save diffs and summaries
   - CHECKPOINT
5) Garden step repair/verify (step-fixer subagent, channel=garden)
   - Run, fix, re-run; produce diffs
   - Save diffs and summaries
   - CHECKPOINT
6) Grapher step run/verify (step-fixer subagent, channel=grapher, add --grapher)
   - Skip diff
   - CHECKPOINT
7) Indicator upgrade (optional, staging only)
   - Use indicator-upgrader subagent with `<short_name> <branch>`
   - CHECKPOINT (if executed)

## Guardrails and tips

- Never return empty tables or comment out logic as a workaround — fix the parsing/transformations instead.
- Column name changes: update garden processing code and metadata YAMLs (garden/grapher) to match schema changes.
- Indexing: avoid leaking index columns from `reset_index()`; format tables with `tb.format(["country", "year"])` as appropriate.
- Metadata validation errors are guidance — update YAML to add/remove variables as indicated.

## Artifacts (expected)

- `workbench/<short_name>/snapshot-runner.md`
- `workbench/<short_name>/progress.md`
- `workbench/<short_name>/meadow_diff_raw.txt` and `meadow_diff.md`
- `workbench/<short_name>/garden_diff_raw.txt` and `garden_diff.md`
- `workbench/<short_name>/indicator_upgrade.json` (if indicator-upgrader was used)

## Example usage

- Minimal catalog URI with explicit old version:
  - `update-dataset data://snapshot/irena/2024-11-15/renewable_power_generation_costs 2023-11-15 update-irena-costs`

---

### Common issues when data structure changes

- SILENT FAILURES WARNING: Never return empty tables or comment code as workarounds!
- Column name changes: If columns are renamed/split (e.g., single cost → local currency + PPP), update:
  - Python code references in the garden step
  - Garden metadata YAML (e.g., `food_prices_for_nutrition.meta.yml`)
  - Grapher metadata YAML (if it exists)
- Index issues: Check for unwanted `index` columns from `reset_index()` — ensure proper indexing with `tb.format(["country", "year"])`.
- Metadata validation: Use error messages as a guide — they show exactly which variables to add/remove from YAML files.
