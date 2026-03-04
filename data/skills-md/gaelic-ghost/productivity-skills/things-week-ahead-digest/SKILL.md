---
name: things-week-ahead-digest
description: Summarize Things todos and recommend next actions using recent activity across projects, areas, and checklist-like notes, plus a week/weekend-ahead preview. Use when asked for Things planning digests, productivity check-ins, weekly previews, or automation that turns Things data into concise priorities.
---

# Things Week Ahead Digest

Build a repeatable Things planning digest with four sections:
- Snapshot
- Recently Active
- Week/Weekend Ahead
- Suggestions

## Inputs

Collect data with Things MCP tools:
1. `things_read_areas`
2. `things_read_projects` with `status="open"`
3. `things_read_todos` with `status="open"` (set `limit` high enough for a full view, usually 300-500)
4. `things_read_todos` with `status="completed"` and `completed_after=<today-7d>`
5. Optional: `things_read_todo` for top candidate tasks (`include_notes=true`) when notes/checklist signals are needed

If any call fails because of permissions, report the missing permission and continue with the best available subset.

## Workflow

1. Load active customization config:
   - Prefer `<skill_root>/config/customization.yaml`.
   - Fall back to `<skill_root>/config/customization.template.yaml`.
2. Build urgency buckets from open todos:
   - overdue: `deadline < today`
   - due soon: `deadline <= today + <dueSoonDays>`
   - week/weekend ahead: `deadline` between today and `today + <daysAhead>`
3. Score recent activity by project and area using configured weights:
   - recent completions (last 7 days)
   - open tasks
   - due soon / overdue counts
   - checklist-like hints from notes (`- [ ]`, `- [x]`, multiline bullet blocks)
4. Identify top active projects/areas from the score.
5. Generate configured number of concrete suggestions:
   - one next action for top projects
   - one risk/triage action for overdue work
   - one planning action for weekend or Monday readiness when relevant
6. Format with the template in `references/output-format.md`.

Keep tone concise and operational. Prefer verbs and specific task titles over generic advice.

## Scripts

Use `scripts/build_digest.py` when deterministic scoring/formatting is preferred (automation, repeatability, large datasets).

```bash
uv run --with pyyaml python scripts/build_digest.py \
  --areas areas.json \
  --projects projects.json \
  --open-todos open_todos.json \
  --recent-done recent_done.json
```

The script reads JSON exported from Things MCP responses and prints Markdown digest output.

Configuration precedence:

1. CLI flags
2. `config/customization.yaml`
3. `config/customization.template.yaml`
4. Script hardcoded defaults

## Customization Workflow

When a user asks to customize this skill, use this deterministic flow:

1. Read active config from `config/customization.yaml`; if missing, use `config/customization.template.yaml`.
2. Confirm desired behavior for:
   - due-soon and planning windows
   - top project/area counts
   - scoring weights and open-count cap
   - suggestion cap and output style
3. Propose 2-4 option bundles with one recommended default.
4. Create or update `config/customization.yaml` from template and set:
   - `schemaVersion: 1`
   - `isCustomized: true`
   - `profile: <selected-profile>`
5. Validate by generating a sample digest and report changed keys plus behavior deltas.

## Customization Reference

- Detailed knobs and examples: `references/customization.md`
- YAML schema and allowed values: `references/config-schema.md`

## Automation Templates

Use `$things-week-ahead-digest` inside automation prompts so Codex reliably loads this workflow.

For ready-to-fill Codex App and Codex CLI (`codex exec`) templates, including Things MCP fallback guidance, placeholders, and customization knobs, use:
- `references/automation-prompts.md`

## References

- Scoring and suggestion rules: `references/suggestion-rules.md`
- Output shape and section template: `references/output-format.md`
- Automation prompt templates: `references/automation-prompts.md`
- Customization guide: `references/customization.md`
- Customization schema: `references/config-schema.md`
