---
name: init-architect
version: 1.4.0
description: Initializes and maintains architecture artifacts by analyzing the codebase and populating /architecture/architecture.md plus domain docs while preserving skill templates.
---

# Init Architect

## Purpose

Run once after installing skills (and rerun when architecture drifts) to create or refresh architecture-folder artifacts used by `architect-agent`.

## Runtime Configuration

- Read `/orchestra-config.json` from the repository root before starting.
- If `/orchestra-config.json` is missing, create it at repository root with:
  - `{ "issue_tracker": "linear" }`
- Read `issue_tracker` and use it for any generated tracker-facing instructions.
- Allowed `issue_tracker` values: `linear`, `jira`.

## When to Invoke

- Immediately after skill installation, before running `architect-agent`
- When architecture artifacts are stale after major system changes

## Required Inputs

- Repository root path
- Optional existing `/architecture/architecture.md`
- Optional existing `/architecture/docs/*.md`
- Optional existing `skills/init-architect/ARCHITECTURE.md` template

## Outputs

- `/orchestra-config.json` in repository root (created only if missing)
- `/architecture/architecture.md` populated as the architecture index
- `/architecture/docs/*.md` populated for complex domains
- Optional targeted updates to `skills/architect-agent/SKILL.md` reference tables so runtime guidance matches generated docs

## Procedure

1. Ensure `/orchestra-config.json` exists and has key `issue_tracker`.
2. Ensure scaffold exists:
   - `skills/init-architect/ARCHITECTURE.md`
3. Ensure generated artifact paths exist:
   - `/architecture/architecture.md`
   - `/architecture/docs/`
4. If architecture content currently lives under `/ARCHITECTURE.md` or `/docs/`, migrate relevant content into `/architecture/` and stop updating legacy root-level copies.
5. Analyze repository structure (do not read every source file):
   - stack, entry points, boundaries, data layer, integrations, auth, sensitive areas, conventions
6. Write/update `/architecture/architecture.md` as a concise index:
   - system overview
   - component map
   - sensitive areas
   - conventions
   - reference docs table
7. Create/update `/architecture/docs/*.md` only for domains that need detail beyond the index.
8. Keep index shallow; move depth to domain docs.
9. If generated docs change domain/sensitive-area mapping, update relevant sections in `skills/architect-agent/SKILL.md`.

## Guardrails

- This skill owns architecture artifact generation; `architect-agent` must not regenerate architecture docs.
- Do not overwrite `skills/init-architect/ARCHITECTURE.md` template files.
- Keep generated architecture artifacts under `/architecture/` (`/architecture/architecture.md`, `/architecture/docs/*.md`).
- Prefer clarity over coverage; do not scan the full codebase unnecessarily.

## Handoff

Primary consumer: `architect-agent`.
