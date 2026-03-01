---
name: docs
description: Initialize or update project documentation. Use when setting up docs for a new project (`--init`) or syncing docs to current codebase and architecture changes (`--update`).
---

# Docs

Create and maintain project documentation in `docs/` with a consistent, lightweight workflow.

## Parameters

- `--init`: Create documentation for the first time.
- `--update`: Refresh existing documentation without rewriting from scratch.

## Outputs

Always maintain these files:

1. `docs/project-pdr.md` — product goals, users, requirements
2. `docs/code-standard.md` — stack, conventions, development rules
3. `docs/codebase.md` — codebase map and key files
4. `docs/architecture.md` — components, interactions, data flow

Also keep `README.md` aligned with current docs links and project summary.

## Workflow

### Step 1: Context Scan (Docs First)

Review documentation first, then inspect code/config only as needed.

Priority order:

1. `docs/project-pdr.md`
2. `docs/code-standard.md`
3. `docs/codebase.md`
4. `docs/architecture.md`
5. `README.md`
6. Key source/config files

Focus on facts that changed: features, architecture, stack, structure, and workflows.

### Step 2: Choose Mode

- If docs do not exist or are incomplete: run `--init` behavior.
- If docs exist: run `--update` behavior.
- If mode is unspecified, infer from repository state and state your assumption.

### Step 3: Produce Documentation

#### `--init`

- Create `docs/` if missing.
- Create all required documentation files.
- Populate each file with concrete, project-specific content.
- Avoid placeholders and generic templates.

#### `--update`

- Preserve useful existing content and section structure.
- Update stale or inaccurate sections.
- Add newly discovered features/components/conventions.
- Remove clearly obsolete statements.

### Step 4: Sync README

Ensure `README.md` includes:

- Short project overview
- Quick start (if present in project)
- Documentation links section pointing to all 4 docs files

### Step 5: Validate Quality

Before finishing, verify:

- Terminology is consistent across files
- No contradictions between docs and code
- Paths and component names are accurate
- Content is concise, specific, and actionable

## Content Requirements by File

### `project-pdr.md`

Include:

- Problem statement
- Product purpose
- Target users
- Core use cases
- Feature scope and constraints
- Success criteria

### `code-standard.md`

Include:

- Languages/frameworks/tools in use
- Naming and structure conventions
- Testing/linting/formatting expectations
- PR/commit expectations if discoverable

### `codebase.md`

Include:

- High-level tree
- Directory responsibilities
- Key entry points and modules
- Important scripts/config files

### `architecture.md`

Include:

- Main components/subsystems
- Data flow between components
- Integration boundaries (internal/external)
- Deployment/runtime assumptions (if known)

## Clarification Rules

Ask targeted questions only when information cannot be reliably inferred, especially for:

- Business goals and domain intent
- Ambiguous ownership/responsibility of modules
- Conflicting conventions
- Unclear architecture decisions

Prefer 1 focused question at a time.

## Rules

- Keep documentation factual; do not invent requirements.
- Prefer concise updates over verbose prose.
- Keep docs aligned with current implementation.
- Follow project conventions from `docs/code-standard.md`.
- When uncertain, mark assumptions explicitly and request confirmation.
