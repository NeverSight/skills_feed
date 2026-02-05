---
name: project-planner
description: >-
  Project planning and feature breakdown for Python/React full-stack projects.
  Use during the planning phase when breaking down feature requests, user stories,
  or product requirements into implementation plans. Guides identification of affected
  files and modules, defines acceptance criteria, assesses risks, and estimates
  overall complexity. Produces module maps, risk assessments, and acceptance criteria.
  Does NOT cover architecture decisions (use system-architecture), implementation
  (use python-backend-expert or react-frontend-expert), or atomic task decomposition
  (use task-decomposition).
license: MIT
compatibility: 'Python 3.12+, React 18+, FastAPI, SQLAlchemy, TypeScript'
metadata:
  author: platform-team
  version: '2.0.0'
  sdlc-phase: planning
allowed-tools: Read Grep Glob Write
context: fork
---

# Project Planner

## When to Use

Activate this skill when:
- Breaking down a feature request or user story into an implementation plan
- Sprint planning or backlog refinement for a Python/React project
- Designing a new module, service, or feature area
- Estimating the overall complexity of a proposed change
- Identifying file-level impact before starting implementation
- Mapping the impact of a change across backend and frontend layers

Do NOT use this skill for:
- Architecture decisions or technology trade-offs (use `system-architecture`)
- Writing implementation code (use `python-backend-expert` or `react-frontend-expert`)
- API contract design (use `api-design-patterns`)
- Decomposing into atomic implementation tasks (use `task-decomposition`)

## Instructions

### Planning Workflow

Follow this 4-step workflow for every planning request:

#### Step 1: Analyze the Requirement

1. Read the feature request, user story, or product requirement in full
2. Identify the core objective — what value does this deliver?
3. List explicit inputs (what triggers the feature) and outputs (what the user sees)
4. Note ambiguities or missing details — list them as open questions
5. Determine if this is a new feature, enhancement, bug fix, or refactoring

#### Step 2: Map Affected Modules

Scan the project and identify every file or module area affected by the change:

**Backend (FastAPI):**
- `routes/` — New or modified endpoint handlers
- `services/` — Business logic changes
- `repositories/` — Data access layer changes
- `models/` — SQLAlchemy model changes (triggers migration)
- `schemas/` — Pydantic request/response schema changes
- `core/` — Configuration, security, or middleware changes
- `migrations/` — Alembic migration files

**Frontend (React/TypeScript):**
- `pages/` — New or modified page components
- `components/` — Shared UI component changes
- `hooks/` — Custom hook changes or additions
- `services/` — API client changes (TanStack Query keys, mutations)
- `types/` — Shared TypeScript type definitions
- `utils/` — Utility function changes

**Shared / Cross-cutting:**
- `types/` or `shared/` — Types shared between backend and frontend
- `.env` / config — Environment variable changes
- `tests/` — Test files for each changed module

Present the module map as a table:

```
| Layer    | Module           | Change Type       | Impact    |
|----------|-----------------|-------------------|-----------|
| Backend  | models/user.py  | Add field         | Migration |
| Backend  | schemas/user.py | Add response field| API change|
| Frontend | hooks/useUser.ts| Update query      | UI change |
```

#### Step 3: Define Verification Criteria

Define how the completed feature will be verified:

**Integration verification:**
- End-to-end test scenario describing the complete user flow
- Manual smoke test steps if automated E2E is not available

**Regression check:**
- Existing tests still pass: `pytest -x && npm test`
- No type errors: `mypy src/ && npx tsc --noEmit`
- No lint issues: `ruff check src/ && npm run lint`

#### Step 4: Identify Risks and Unknowns

Flag potential issues using the categories below. For each risk:
- **Risk:** Description of what could go wrong
- **Likelihood:** Low / Medium / High
- **Impact:** Low / Medium / High
- **Mitigation:** How to reduce or eliminate the risk

See `references/risk-assessment-checklist.md` for the complete risk category list.

### Output Format

Write the plan to a file at the project root: **`plan.md`** (or `plan-<feature-name>.md` if multiple plans exist). Use `references/plan-template.md` as the template.

The file must contain:

```markdown
# Implementation Plan: [Feature Name]

## Objective
[1-2 sentence summary of what this delivers]

## Context
- Triggered by: [user story / feature request / bug report]
- Related work: [links to related plans, ADRs, or PRs]

## Open Questions
[List ambiguities that need resolution before implementation]

## Affected Modules
[Module map table from Step 2]

## Verification
[Integration verification from Step 3]

## Risks & Unknowns
[Risk table from Step 4]

## Acceptance Criteria
[Bullet list of observable outcomes that confirm the feature works]

## Estimation Summary
[Overall complexity estimate — see table below]
```

**Always write the plan to a file.** This enables `/task-decomposition` to read it as input. After writing, tell the user: "Plan written to `plan.md`. Run `/task-decomposition` to break it into atomic tasks."

### Estimation Summary

Estimate overall feature complexity using this table:

| Metric | Value |
|--------|-------|
| Total backend modules affected | [N] |
| Total frontend modules affected | [N] |
| Migration required | Yes / No |
| API changes | Yes / No (new endpoints / modified contracts) |
| Overall complexity | trivial / small / medium / large |

Complexity guidelines:
- **Trivial:** 1-2 modules, no migration, <50 lines
- **Small:** 2-4 modules, no migration, <200 lines
- **Medium:** 4-8 modules, migration possible, <500 lines
- **Large:** 8+ modules, migration likely, 500+ lines

## Examples

### Example: Plan "Add User Profile Picture Upload"

**Objective:** Allow users to upload and display a profile picture.

**Affected Modules:**

| Layer    | Module                    | Change Type    | Impact       |
|----------|--------------------------|----------------|-------------|
| Backend  | models/user.py           | Add avatar_url | Migration    |
| Backend  | schemas/user.py          | Add field      | API contract |
| Backend  | services/upload.py       | New service    | New file     |
| Backend  | routes/users.py          | Add endpoint   | API change   |
| Frontend | components/AvatarUpload  | New component  | UI change    |
| Frontend | hooks/useUploadAvatar.ts | New hook       | Data fetch   |
| Frontend | pages/ProfilePage.tsx    | Integrate      | UI change    |

**Verification:**
- Upload an image via the profile page, verify it displays
- Upload an oversized file, verify rejection with error message
- Regression: `pytest -x && npm test`

**Risks:**
- File size limits need validation (server + client) — Medium likelihood — Add early validation
- S3 permissions may need configuration — Low likelihood — Test with local storage first

**Acceptance Criteria:**
- User can upload a profile picture from the profile page
- Uploaded image displays as the user's avatar across the app
- Files over 5MB are rejected with a clear error message
- Non-image files are rejected
- All existing tests pass

**Estimation Summary:**

| Metric | Value |
|--------|-------|
| Backend modules affected | 4 |
| Frontend modules affected | 3 |
| Migration required | Yes |
| API changes | Yes (new upload endpoint) |
| Overall complexity | medium |

**Output:** Written to `plan.md`. Run `/task-decomposition` to break it into atomic tasks.

## Edge Cases

- **Cross-cutting changes** (auth middleware, error handling, logging): These affect many modules. Flag for architecture review before planning. Consider whether the change should be its own plan.

- **Database migrations with data transformation**: Flag as a risk. Note that migration testing (upgrade + rollback) is needed. Task-decomposition will create a dedicated migration task.

- **Frontend state cascades**: When modifying shared state (React Context, TanStack Query cache), map the component tree to identify all consumers in the module map.

- **API breaking changes**: If modifying an existing endpoint's contract, check for frontend consumers first. Consider API versioning if external consumers exist. Note in the plan that frontend updates must be coordinated.

- **Feature flags**: For large features spanning multiple sprints, note in the plan that a feature flag is needed. Task-decomposition will handle the implementation ordering.

- **Third-party dependency updates**: If the feature requires a new package, list it in the plan's affected modules. Note potential peer dependency conflicts as a risk.
