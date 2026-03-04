---
name: project-roadmap-manager
description: Create and maintain a repository-root ROADMAP.md as the single source of truth for project milestones and accepted plans. Use when bootstrapping any new project, accepting/completing a plan, defining or updating milestone/version roadmaps, marking milestones as reached/changed/de-scoped, or answering where roadmap and milestone status should be referenced.
---

# Project Roadmap Manager

Maintain `ROADMAP.md` in the project root as the canonical roadmap record. Prefer updating existing sections over appending duplicates, and keep `Current Milestone` synchronized with the latest accepted plan.

## Workflow

1. Load active customization config:
   - Prefer `<skill_root>/config/customization.yaml`.
   - Fall back to `<skill_root>/config/customization.template.yaml`.
   - Apply settings under `settings` to roadmap generation and update decisions.
   - Treat missing sub-milestone keys in user config as template defaults.
2. Identify project root and target file:
   - Use `<project_root>/ROADMAP.md`.
   - If root is ambiguous, infer from repository root.
3. Ensure `ROADMAP.md` exists:
   - If missing, create it using the template in this skill.
4. Classify the request into one of these event types:
   - Project bootstrap.
   - Plan acceptance/completion.
   - Milestone/version roadmap set or changed.
   - Milestone reached/blocked/de-scoped.
   - Roadmap reference/query.
5. Apply the event-specific update rules.
6. Keep all sections internally consistent:
   - `Current Milestone` matches active milestone in `Milestones`.
   - `Plan History` includes accepted plan snapshots.
   - `Change Log` captures each roadmap mutation with date and reason.
   - When sub-milestones are enabled, parent/child linkage and ID uniqueness are valid.

## Customization Workflow

When a user asks to customize this skill, use this deterministic flow:

1. Read active config from `config/customization.yaml`; if missing, use `config/customization.template.yaml`.
2. Confirm target profile and desired behavior for:
   - `milestoneIdStyle`
   - `targetStyle`
   - `statusValues`
   - sub-milestone enablement, ID style, and status model
   - owner/dependency fields
   - plan history and changelog verbosity
3. Propose 2-4 option bundles with one recommended default.
4. Create or update `config/customization.yaml` from the template and set:
   - `schemaVersion: 1`
   - `isCustomized: true`
   - `profile: <selected-profile>`
5. Apply the selected settings immediately to roadmap output behavior.
6. Validate with a dry-run roadmap update and report changed keys plus behavior deltas.

## Customization Reference

- Detailed knobs and examples: `references/customization.md`
- YAML schema and allowed values: `references/config-schema.md`

## ROADMAP.md Template

Use this structure when creating a new roadmap:

```markdown
# Project Roadmap

## Current Milestone
- ID: M1
- Name: Initial Setup
- Status: Planned
- Target Version: v0.1.0
- Last Updated: YYYY-MM-DD
- Summary: One-paragraph summary of the currently accepted plan.

## Milestones
| ID | Name | Target Version | Status | Target Date | Notes |
| --- | --- | --- | --- | --- | --- |
| M1 | Initial Setup | v0.1.0 | Planned | YYYY-MM-DD | Bootstrap milestone |

<!-- Include this section only when settings.enableSubMilestones is true. -->
## Sub-Milestones
| ID | Parent Milestone | Name | Status | Target Date | Notes |
| --- | --- | --- | --- | --- | --- |
| M1.1 | M1 | First deliverable | Planned | YYYY-MM-DD | Optional child milestone |

## Plan History
### YYYY-MM-DD - Accepted Plan (v0.1.0 / M1)
- Scope:
- Acceptance Criteria:
- Risks/Dependencies:

## Change Log
- YYYY-MM-DD: Initialized roadmap.
```

## Event Handling Rules

### Project Bootstrap

- Create `ROADMAP.md` if absent.
- Add an initial milestone (`M1` unless user provides a different identifier).
- If `enableSubMilestones` is true and initial child milestones are provided, generate IDs deterministically from style settings.
- Add a changelog entry indicating roadmap initialization.

### Plan Acceptance or Completion

- Update `Current Milestone` to reflect the accepted plan.
- Add or update corresponding row in `Milestones`.
- If `enableSubMilestones` is true, add or update affected child entries under the active milestone.
- Append an `Accepted Plan` entry in `Plan History` with scope and acceptance criteria.
- Add a changelog entry summarizing what changed and why (include parent + child transition details when child entries changed).

### Milestone or Version Roadmap Set/Update

- Update existing milestone by ID/version if it exists.
- Add milestone only when no matching milestone exists.
- Avoid duplicate milestones for the same ID or target version.
- When `enableSubMilestones` is true:
  - Avoid duplicate child IDs within the same parent milestone.
  - Keep child status values inside `subMilestoneStatusValues` (or inherit `statusValues` when child list is absent).
  - Use deterministic ID generation rules from settings:
    - `hierarchical`: `<milestoneID><delimiter><n>` (default `M2.1`).
    - `letter`: `<milestoneID><letter>` (for example `M2a`).
    - `ticket`: `<prefix><delimiter><zero-padded n>` and render with parent context (for example `M2-T01`).
    - `external`: accept tracker IDs only when `allowExternalTrackerIds` is true.
- If the updated milestone is active, sync `Current Milestone`.

### Milestone Reached/Changed

- Update milestone status (`Completed`, `In Progress`, `Blocked`, `De-scoped`, or `Planned`).
- Update `Current Milestone` if active milestone changed.
- If `enableSubMilestones` is true, keep child transitions and parent/child linkage consistent.
- Add a dated note in `Change Log` that captures transition and reason (include parent + child details when children are involved).

### Roadmap Reference Requests

- Point explicitly to `<project_root>/ROADMAP.md`.
- Cite the relevant section name (`Current Milestone`, `Milestones`, `Plan History`, or `Change Log`).
- If file is missing, create it first, then reference it.

## Quality Bar

- Preserve existing useful roadmap content.
- Use ISO date format (`YYYY-MM-DD`) for all dated fields.
- Keep edits minimal and deterministic.
- Never leave conflicting milestone statuses across sections.
- If sub-milestones are disabled, do not require or mutate any sub-milestone section.
- If sub-milestones are enabled, enforce deterministic child ID style and unique IDs within parent scope.

## Automation Templates

Use `$project-roadmap-manager` inside automation prompts so Codex consistently applies the roadmap update rules.

For ready-to-fill Codex App and Codex CLI (`codex exec`) templates, including bounded-edit guardrails and placeholders, use:
- `references/automation-prompts.md`

## References

- Automation prompt templates: `references/automation-prompts.md`
- Customization guide: `references/customization.md`
- Customization schema: `references/config-schema.md`
