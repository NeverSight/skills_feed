---
name: prd
description: "Create, update, or list PRDs for features, fixes, and chores. Handles project setup (first PRD) and ongoing PRD management. Each PRD is a self-contained spec with status, priority, and acceptance criteria. Triggers: prd, new feature, write prd, plan feature, create spec, list prds, update prd, add feature."
---

# prd

Create, update, or list PRDs. Each PRD is a self-contained feature spec with status and priority.

---

## Guardrails

- Do not implement code.
- Keep features "PRD-sized": one feature = one PRD.
- Split the feature if it spans >2 subsystems, >1 UI surface + backend, or >~1 day of work.
- Prefer asking a small number of high-value questions; otherwise write a draft PRD with explicit assumptions.
- Write the PRD so a junior dev (or another AI) can implement it without extra context.
- Use plain language, explicit edge cases, and verifiable acceptance criteria.
- Do not use Markdown tables (use checklists + bullets).
- When asking users for decisions, always provide numbered options with low-keystroke reply formats.
- Treat context capture as built-in.
- If durable decisions are made, update `tasks/context.md` in this step.
- Do not defer to a separate context pass.

---

## Modes

- **Create / update** (default): write or revise a single PRD.
- **List**: scan `tasks/` for active (non-archived) PRDs and display a summary of feature ID, name, status, and priority. No file modifications.

---

## Workflow — Create / Update

1. **Determine intent:**
   - **New project** (no `tasks/context.md` or empty): ask project-definition questions, initialise `tasks/context.md` with project gist, then write the first PRD.
   - **New PRD** (project exists): proceed to PRD creation.
   - **Update existing PRD**: locate the existing PRD file and edit in place.
2. **Read context:**
   - If `tasks/context.md` exists, skim project gist, key decisions, and notes/gotchas.
   - Avoid conflicts with prior decisions.
3. **Assign feature ID:**
   - Scan existing PRD files in `tasks/` and `tasks/archive/` for the highest `f-##` number.
   - New PRD gets `(max existing f-##) + 1`.
   - For updates, preserve the existing ID.
4. **Ask clarifying questions** only when needed (numbered A/B/C/D options, up to ~7, answerable like `1A, 2C`).
5. **Determine PRD file path:**
   - Look for an existing active PRD matching the feature ID in `tasks/` (`tasks/f-##-*.md`).
   - If found, use it (update in place).
   - Otherwise use `tasks/f-##-<feature-slug>.md`.
6. **Write or update the PRD** at the chosen path using `references/prd-template.md`:
   - Set `Status:` and `Priority:` in the Summary section.
   - For new PRDs, default `Status: draft`. Prompt the user to confirm `ready` when scope is locked.
   - `Priority:` uses P0 (critical), P1 (high), P2 (medium), P3 (low).
   - Ensure implementation progress is trackable via checklist items.
   - For UI/UX-heavy features, include expected design inputs and state whether `design` should run before `implement`.
7. **Update context:**
   - Update project gist in `tasks/context.md` if this is the first PRD or project scope changed.
   - Capture any durable decisions or constraints.
8. **Reply** with updated file paths and a short change summary.

---

## Workflow — List

1. Scan `tasks/` for files matching `f-##-*.md` (exclude `tasks/archive/`).
2. For each file, extract from the Summary section: Feature ID, name, Type, Status, Priority.
3. Display sorted by priority (P0 first), then by feature ID.
4. Suggest the highest-priority `Status: ready` PRD as the next candidate for `implement`.
5. No file modifications in list mode.

---

## Clarifying Questions (Only If Needed)

Ask up to ~7 high-value questions. Keep them answerable via `1A, 2C, 3B`.

Focus on ambiguity around:

- target user + primary use case
- the problem + desired outcome
- constraints (platforms, timeline, integrations)
- success metrics / how we know it worked
- scope boundaries (what's explicitly in vs out)
- whether this is `Type: feat` vs `fix` vs `chore`
- priority (P0 / P1 / P2 / P3)
- dependencies between features (by ID)

### Example question format

```text
1. What are we building?
   A. A brand new feature
   B. A fix for existing behaviour
   C. A maintenance/chore item
   D. Other: [describe]
```

---

## Feature Writing Guidelines

- Prefer feature names as verb phrases (e.g., "Invite teammates", "Export CSV").
- For fix items, name them clearly (e.g., "Fix <problem>") and set `Type: fix`. Include minimal bug info:
  - Current behaviour: …
  - Expected behaviour: …
  - Repro steps (if known): …
- For chores, keep them crisp and outcome-oriented (e.g., "Chore: remove dead code") and set `Type: chore`.
- Ensure each feature has a crisp outcome (what changes for the user).
- Avoid implementation tasks ("refactor", "set up DB") unless they are truly user-facing requirements.
- If a feature is too large, split by user goal or workflow step until each item could reasonably become a single PRD.

---

## Update Rules (When a PRD Exists)

- If a PRD already exists at that path, update it in place.
- Do not create a duplicate PRD unless the user asks.
- Do not reset existing checklist items inside the PRD.
- Preserve existing `Status:` and `Priority:` unless the user explicitly asks to change them.
- Keep feature IDs stable; IDs must be globally unique across `tasks/` and `tasks/archive/`.
- When adding a new feature, use the next ID as `(max existing f-##) + 1` (never reuse old IDs).

---

## PRD Template

Use `references/prd-template.md` as the default PRD template and checklist.

- Read it before drafting a new PRD.
- For updates to an existing PRD, edit only impacted sections and preserve existing checkbox state.
- Keep acceptance criteria concrete and verifiable; examples are in the reference file.

---

## Output

- Create or reuse `tasks/`.
- Save/update the PRD at the chosen path.
- Update `tasks/context.md` when durable decisions or project scope changes warrant it.
- For UI/UX-heavy PRDs, recommend `design` (optional) before `implement`.
- Suggest the next action:
  - If `Status: draft`, suggest refining to `ready`.
  - If `Status: ready`, suggest `implement`.
- End with a short status block:
  - **Files changed**: list of created/updated files
  - **Key decisions**: any assumptions or choices made (if any)
  - **Next step**: recommended next skill or action

---

## Quality Checklist

Before saving:

- [ ] PRD Summary includes `Feature ID`, `Type`, `Status`, and `Priority`.
- [ ] Feature ID is unique and stable (checked against existing PRDs in `tasks/` and `tasks/archive/`).
- [ ] If updating an existing PRD, existing story/task checkboxes were preserved (not reset).
- [ ] If a PRD already existed, it was updated in place (no duplicates).
- [ ] Each feature has a user-visible outcome and explicit scope boundaries (goals + non-goals).
- [ ] Dependencies reference valid feature IDs.
- [ ] Acceptance criteria are concrete and verifiable.
- [ ] PRD is consistent with `tasks/context.md` (or `tasks/context.md` was updated in this run).
