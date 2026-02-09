---
name: implement
description: "Implement a PRD by building the feature in the codebase (`Type: feat` / `fix` / `chore`), updating tests, running checks, and checking off completed PRD stories/tasks. Triggers: implement, build, execute, code this feature, run plan, finish implementation."
---

# implement

Implement a feature from a PRD.

---

## Guardrails

- Follow the repo's `AGENTS.md` instructions (if present) for any files you touch.
- Keep changes simple and handoff-friendly: assume a junior dev (or another AI) will maintain this later.
- Do not change product scope while executing:
  - If the PRD is missing details or ambiguous, stop and use `plan` to refine the PRD first.
  - If implementation reveals the PRD is incorrect, pause and propose PRD edits via `plan` before continuing; do not silently deviate.
  - If the feature is missing from `tasks/todo.md`, stop and use `new` first.
  - If you discover out-of-scope requirements or bugs during execution, do not expand scope—create a new backlog item via `new` instead.
- Do not edit `tasks/todo.md` in this skill.
- Do not reset any existing PRD checklist items when updating an existing PRD.
- Treat memory capture as built-in: when implementation yields durable decisions/gotchas, update `tasks/memory.md` in this step.
- Do not claim tests passed or checks succeeded without actually running them; if you didn't run it, say so.

---

## Workflow

1. **Identify the PRD**
   - Ask for the PRD path if not provided (usually `tasks/f-##-<slug>.md`).
   - Confirm which feature ID/name this PRD corresponds to.

2. **Preflight**
   - Read `AGENTS.md` (if present) and follow it.
   - Check priority (if `tasks/todo.md` exists):
     - Priority is determined by list order.
     - If there are higher-priority items above this feature, ask the user to confirm they want to work on it now (vs a higher-priority item).
       - If the higher-priority item is unchecked (no PRD yet), recommend writing its PRD via `plan` first.
   - Create a new feature branch before making changes (unless you are already on an appropriate feature branch):
     - Base it off the repository default branch (resolve via `origin/HEAD` or repo policy); if unclear, ask the user before branching.
     - Name it based on the PRD Summary `Type` (or match repo conventions):
       - `Type: fix` → `fix/f-##-<short-slug>`
       - `Type: chore` → `chore/f-##-<short-slug>`
       - default (`Type: feat`) → `feat/f-##-<short-slug>`
   - If `tasks/memory.md` exists, skim key decisions / notes / gotchas relevant to this area before coding.
   - Parse the PRD into an execution plan: user stories, functional requirements, non-goals, risks, rollout, and testing notes.
   - Verify dependencies:
     - Read this PRD's "Dependencies & Constraints" section for feature dependency IDs.
     - For each dependency ID, locate PRD files by feature ID in `tasks/` and `tasks/archive/`.
     - Treat dependencies as complete only when the dependency PRD is archived in `tasks/archive/`.
     - If any dependency is still in `tasks/`, recommend finalising that dependency first.
     - If a dependency has no PRD yet, stop and use `plan` to create that dependency PRD first.
     - Override: if the user confirms dependencies are satisfied (e.g., dependency PR merged but not yet archived), proceed and record the override in `tasks/memory.md`.

3. **Execute**
   - Implement the feature as specified.
   - Implement in small checkpoints aligned to PRD user stories to enable atomic commits.
   - Add/update tests as appropriate.
   - Run the project's normal checks (typecheck/lint/tests/build) per `AGENTS.md` or project conventions.

4. **Verify**
   - Verify acceptance criteria and edge cases from the PRD.
   - Perform any manual QA steps listed in the PRD.

5. **Update checklist progress (in-place)**
   - Check off completed user stories/tasks and acceptance criteria in the PRD as implementation progresses.
   - If the PRD lacks checklist items for implementation progress, add a small checklist section and use it.
   - Do not reset existing checked items.

6. **Update memory inline when needed**
   - Update `tasks/memory.md` when implementation produces durable information:
     - important gotchas or constraints
     - architectural/technical decisions with trade-offs
     - milestone-level completion notes worth preserving

7. **Close out**
   - Summarise what was changed and what remains.
   - Next steps:
     - PR flow: run `review` (local) when needed, then `commit`, then `open-pr`, then run `review` (PR mode) when needed, then `commit` (finalise mode).
     - Local flow: run `review` (local) when needed, then `commit`.

---

## Output

- Update code and tests as needed.
- Update PRD story/task checklist progress in the PRD file.
- If you discover a durable decision/gotcha or complete a significant milestone, update `tasks/memory.md` in the same run.
- Reply with:
  - PRD path
  - Which checklist items were completed
  - Any follow-ups or open issues
- End with a short status block:
  - **Files changed**: list of created/updated files
  - **Key decisions**: any assumptions or choices made (if any)
  - **Next step**: recommended next skill or action
