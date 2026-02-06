---
name: 01-new
description: "Create or update `tasks/todo.md` with a project overview and a prioritized feature list (top-to-bottom). Use when starting a new project, planning an MVP feature set, building a backlog/roadmap, adding new items (feat/fix/chore), or re-prioritizing. Triggers: new project, MVP features, feature list, backlog, roadmap, add feature, add fix, bugfix, chore, reprioritize, update todo.md, planning."
---

# 01 new

Create or update `tasks/todo.md` as the source of truth for what the project is and what features will be built.

---

## Guardrails

- Do not implement code.
- Do not write individual feature prds (use `02-plan` for that).
- Keep features “prd-sized”: one feature = one prd; split anything that feels like an epic.
- Prefer a stable `todo.md` structure; edit in place rather than rewriting.
- Write `tasks/todo.md` so a junior dev (or another AI) can pick it up without extra context.
- Do not use Markdown tables (use checklists + bullets).
- Do not check feature boxes unless the prd actually exists (typically updated by `02-plan`).

---

## Workflow

1. Determine intent:
   - **New project** → initialize `tasks/todo.md`.
   - **Add/update features** → edit the existing `tasks/todo.md`.
2. If `tasks/memory.md` exists, skim relevant sections (project, key decisions, notes/gotchas) so you don’t conflict with prior decisions.
3. Ask clarifying questions only when needed (use A/B/C/D options).
4. Update `tasks/todo.md` using the template below:
   - **New project**: write a crisp Project section + propose an initial prioritized feature list, ordered by priority (highest first).
   - **Add/update**: add, merge, re-scope, and/or re-order features.
     - If adding a new `Type: fix` item and the user didn’t specify placement, explicitly ask if it should move up the list (priority is determined by list order).
5. Ensure each feature has clear in-scope vs out-of-scope boundaries and dependencies (if any).
6. Reply with the updated file path and a short change summary (what you added/changed).

---

## Clarifying Questions (Only If Needed)

Ask up to ~7 high-value questions. Keep them answerable via `1A, 2C, 3B`.

Focus on ambiguity around:

- target user + primary use case
- the problem + desired outcome
- constraints (platforms, timeline, integrations)
- success metrics / how we know it worked
- scope boundaries (what’s explicitly in vs out)
- priority order (what should be done first)
- whether an item should be `Type: feat` vs `fix` vs `chore` (and where it should sit in priority order)
- dependencies between features (by ID)

### Example question format

```text
1. What are we doing right now?
   A. Start a brand new project
   B. Add new features to an existing plan
   C. Refine/re-scope existing planned features
   D. Other: [describe]
```

---

## `tasks/todo.md` Template (Markdown)

If `tasks/todo.md` does not exist, create it with this structure (fill in details; keep it concise).

```markdown
# TODO: <Project name>

## Project
- **One-liner**: …
- **Target users**: …
- **Problem**: …
- **Success metrics**: …
- **Constraints** (optional): …
- **Non-goals**: …

## Features

Checkbox meaning: unchecked = prd not written yet; checked = prd exists.
Leave unchecked until a prd exists.

Status legend: — = not started | 🔨 = implemented | ✅ = merged

### Features (priority order)
- Higher in the list = higher priority.
- [ ] f-01: <feature name>  |  —
  - Type: feat | fix | chore
  - Outcome: <user-visible outcome>
  - In scope: <what ships>
  - Out of scope: <what does not ship>
  - Dependencies: <none> | f-02, f-10

- [ ] f-02: <feature name>  |  —
  - Type: feat | fix | chore
  - Outcome: <user-visible outcome>
  - In scope: <what ships>
  - Out of scope: <what does not ship>
  - Dependencies: <none> | f-01

## Open Questions
- Q-1: …
```

---

## Update Rules (When `tasks/todo.md` Exists)

- Preserve existing content and wording unless the user asks to change it.
- Avoid duplicates: if a new feature overlaps an existing one, merge or propose a rename instead of adding a second item.
- Keep IDs stable; IDs must be globally unique within `tasks/todo.md`.
- When adding a new feature, use the next ID as `(max existing f-##) + 1` (never reuse old IDs).
- If duplicate IDs already exist, resolve by renumbering the newer/less-referenced item(s) and updating any `Dependencies:` references.
- Keep the list prioritized top-to-bottom; if placement is unclear, ask where to insert (or add to the bottom).
- If a feature depends on another feature, ensure the dependency is listed above it (or explicitly confirm the ordering).
- Keep checkbox meaning consistent: checked means “prd exists”.
- Keep status indicator consistent: `—` = not started, `🔨` = implemented, `✅` = merged.
- Do not update status indicators; they are managed by `03-implement` (`🔨`) and `05-review` (`✅` after merge).
- Ensure each feature entry includes:
  - a type (feat/fix/chore)
  - a clear user-visible outcome
  - in scope / out of scope boundaries
  - dependencies by ID (if any)
  - a status indicator (`—` for new features)
- Do not add prd links/paths here; `prd:` lines are owned by `02-plan`.

---

## Feature Writing Guidelines

- Prefer feature names as verb phrases (e.g., “Invite teammates”, “Export CSV”).
- For fix items, name them clearly (e.g., “Fix <problem>”) and set `Type: fix`.
- For chores, keep them crisp and outcome-oriented (e.g., “Chore: remove dead code”) and set `Type: chore`.
- Ensure each feature has a crisp outcome (what changes for the user).
- Avoid implementation tasks (“refactor”, “set up DB”) unless they are truly user-facing requirements.
- If a feature is too large, split by user goal or workflow step until each item could reasonably become a single prd.

---

## Output

- Create or reuse `tasks/`.
- Create or update `tasks/todo.md`.
- After updating, suggest the next feature to spec with `02-plan` (by ID/name): highest priority unchecked feature (checked = prd exists).
- When a prd is created via `02-plan`, ensure the matching feature checkbox is checked in `tasks/todo.md`.
- If you made a durable project decision (scope boundary, constraint, key choice), capture it in `tasks/memory.md` via `06-memory`.

---

## Quality Checklist

Before finalizing `tasks/todo.md`:

- [ ] Project section explains what the project is and who it serves.
- [ ] Feature list is prioritized and reasonably sized (avoid 30 “must-haves”).
- [ ] Feature IDs are unique and stable (no duplicates).
- [ ] No feature is checked unless its prd exists.
- [ ] Each feature has a `Type:` (`feat` / `fix` / `chore`).
- [ ] Each feature has a user-visible outcome and explicit scope boundaries.
- [ ] Dependencies (if any) reference valid feature IDs.
- [ ] Duplicates/overlaps are merged or clearly distinguished.
