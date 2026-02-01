---
name: kanban
description: "Automates a file-system based development Kanban loop: todo to doing to test to done."
---

# Skill: kanban

Automates a development Kanban loop using Node.js scripts and structured resources.

## Structure
- `kanban/01-backlog/01-draft/`: Active requirement incubation area.
- `kanban/01-backlog/02-task/`: Staging area for "Frozen" requirements.
- `kanban/02-doing/[TaskName]/`: Active development.
- `kanban/03-test/[TaskName]/`: Verification stage.
- `kanban/04-done/[TaskName]/`: Finalized knowledge assets.
- `kanban/99-templates/`: Standard document templates (deployed from resources).

## Core Commands

### `/kanban:init`
1. **Script Execution**: Runs `node ./scripts/init.js`.
2. **Baseline Initialization**: If the project already has source code, the agent performs a manual scan and stores results in `kanban/04-done/00-initial-baseline/`.

### `/kanban:spec <TaskName>`
1. **In-place Specification**: Locates `<TaskName>.md` in `kanban/01-backlog/01-draft/`.
2. **Analysis & Rewrite**: Polishes the content using the templates found in `./resources/templates/`.
3. **Outcome**: The draft file evolves into a professional specification.

### `/kanban:start <TaskName> [--yolo]`
1. **Validation**: Ensures the file exists in `kanban/01-backlog/02-task/`.
2. **Setup**: Creates the task folder in `02-doing/` and moves the PRD.
3. **Design**: Generates `SSD.md` (optional), `TDD.md`, and `implementation_plan.md`.

### [Auto-Transition] Doing -> Test
- Triggered on plan completion.
- Summarizes changes and prepares `VERIFICATION_REPORT.md`.
- Automatically moves the folder to `kanban/03-test/`.

### `/kanban:fix <TaskName>`
- Reads `## Reported Issues` from the test report.
- Moves the folder back to `02-doing/` and injects fix steps into the plan.

### `/kanban:done <TaskName>`
- Validates the verification report.
- Moves the task to `04-done/` and cleans up temporary files.

## Resources
- Templates are stored in `./resources/templates/`.
- Automation scripts are stored in `./scripts/`.
