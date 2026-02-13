---
name: backlogmd
description: Use when planning work (to create items and tasks), when starting implementation (to mark tasks in-progress), when completing work (to mark tasks done), or to check backlog status. Manages .backlogmd/ for features, bugfixes, refactors, and chores.
argument-hint: init/create/start/done/edit/show/archive/check <item or task>
allowed-tools: Read, Write, Edit, Glob, Bash(mkdir *), Bash(mv *)
---

# Backlog Manager

You are an agent that manages the `.backlogmd/` backlog system. You can create items (features, bugfixes, refactors, chores) and tasks, update statuses, edit content, and archive completed work.

## Workflow (MANDATORY)

> **RULE**: For new features, bugfixes, refactors, or chores — create or update backlog items BEFORE writing code. The backlog is the source of truth for planned work. For small iterations on an existing task (tweaks, adjustments, follow-ups), you may skip backlog updates and just work.

1. **Before planning**: Check the backlog for existing items and tasks.
2. **When planning**: Create items and tasks in the backlog FIRST, before any implementation. Don't just describe plans in conversation — record them.
3. **Wait for approval**: After planning, present the plan to the user and **STOP**. Do NOT start implementing until the user explicitly approves.
4. **When implementing**: Follow this loop for EACH task, one at a time:
   - **Mark** the task `in-progress` BEFORE writing code for it.
   - **Implement** the task.
   - **Mark** the task `done` IMMEDIATELY after completing it.
   - **Only then** move to the next task.
5. **When all tasks are done**: Inform the user and ask if they want to archive the item.

---

## Spec v2.0.0 (embedded)

### Directory Structure

```
.backlogmd/
├── backlog.md               # Active items, ordered by priority
├── work/                    # Max 50 open items
│   ├── <item-slug>/
│   │   ├── index.md         # Item task list
│   │   ├── 001-task-slug.md
│   │   └── ...
│   └── ...
└── .archive/                # Cold storage — read-only
    └── <YYYY>/
        └── <MM>/
            └── <item-slug>/ # Archived item folders (moved intact)
```

All paths are relative within `.backlogmd/`.

### Backlog Format (`backlog.md`)

```md
- [001-chore-project-foundation](work/001-chore-project-foundation/index.md)
- [002-ci-initialize-github-actions](work/002-ci-initialize-github-actions/index.md)
```

- Bullet list of markdown links to each item's `index.md`.
- Format: `- [<item-slug>](work/<item-slug>/index.md)`
- Ordered by priority — first item is highest priority.
- Slug format: `<NNN>-<name>` (e.g. `001-project-foundation`). An optional [Conventional Commits](https://www.conventionalcommits.org/) type can follow the number: `<NNN>-<type>-<name>` (e.g. `001-chore-project-foundation`). Common types: `feat`, `fix`, `refactor`, `chore`.

### Item Format (`work/<item-slug>/index.md`)

```md
- [001-task-slug](001-task-slug.md)
- [002-task-slug](002-task-slug.md)
```

- Bullet list of relative links to task files.
- Item slug is lowercase kebab-case with priority number prefix. Optional Conventional Commits type after the number.

### Task Format (`work/<item-slug>/<NNN>-<task-slug>.md`)

````md
<!-- METADATA -->

```
Task: <Task Name>
Status: <status>
Priority: <NNN>
DependsOn: [<task-slug>](relative-path-to-task.md)
```

<!-- /METADATA -->
<!-- DESCRIPTION -->

## Description

<detailed description>

<!-- /DESCRIPTION -->

<!-- ACCEPTANCE CRITERIA -->

## Acceptance criteria

- [ ] <criterion>

<!-- /ACCEPTANCE CRITERIA -->
````

- Filenames: `<NNN>-<task-slug>.md` (zero-padded priority, unique within item).
- Valid statuses: `open`, `block`, `in-progress`, `done`.
- `DependsOn` is optional. When present, use a markdown link to the dependency task file (relative path). Omit the field when there are no dependencies.
- Metadata uses HTML comment markers and a fenced code block.

### Archive (`.archive/`)

- Cold storage — agents skip `.archive/` during normal operations.
- Archiving is triggered ONLY when `work/` reaches 50 items. It is NOT triggered by item completion.
- When archiving is needed, archive the lowest-priority-number item first (FIFO — first in, first out). All its tasks must be `done`.
- Move the item folder from `work/<slug>/` to `.archive/<YYYY>/<MM>/<slug>/` and remove the entry from `backlog.md`.
- Archive contents are read-only.

### Workflow Rules

1. Task statuses move forward: `open` → `in-progress` → `done`. Use `block` when blocked.
2. A task cannot move to `in-progress` if its `DependsOn` task is not `done`.
3. Circular dependencies are not allowed.
4. When an agent changes a task's status, it must update the task file.
5. When all tasks in an item are `done`, the item stays in `work/`. Do NOT archive automatically.
6. Max 50 items in `work/` at any time. When the limit is reached and a new item must be created, archive the lowest-numbered completed item (FIFO) to make room. If no completed items exist, the new item cannot be created.

---

## Step 1: Read current state

- Check if `.backlogmd/` exists. If not, run **Step 1b: Bootstrap** before continuing.
- Read `.backlogmd/backlog.md` to understand current items.
- Scan `.backlogmd/work/` to see existing item folders and their task files.

### Step 1b: Bootstrap (first-time setup)

If `.backlogmd/` does not exist, create the initial structure:

1. Create `.backlogmd/` directory.
2. Create `.backlogmd/backlog.md` (empty file).
3. Create `.backlogmd/work/` directory.

Inform the user that the backlog has been initialized, then continue to Step 2.

## Step 2: Determine intent

Based on `$ARGUMENTS`, determine which operation the user wants:

| Intent            | Trigger examples                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------ |
| **Init backlog**  | "init backlog", "set up backlogmd", "initialize" (also happens automatically if `.backlogmd/` doesn't exist) |
| **Create item**   | "add a feature for...", "new bugfix: ...", "refactor the...", "chore: ...", a work item description          |
| **Add tasks**     | "add tasks to...", "new task for..."                                                                         |
| **Update status** | "mark task X as done", "start working on...", "task X is blocked"                                            |
| **Edit**          | "edit task...", "update description of...", "rename item..."                                                 |
| **Archive**       | "archive item...", "clean up done items"                                                                     |
| **Show status**   | "what's the current state?", "show backlog", "what's in progress?"                                           |
| **Sanity check**  | "check backlog", "validate backlog", "sanity check", "is the backlog consistent?"                            |

If the intent is ambiguous, ask the user to clarify before proceeding.

### Inferring the Type (optional)

When creating an item, you may infer a Conventional Commits type from context to include in the slug. This is optional — slugs without a type are valid.

- Words like "add", "implement", "build", "create" → `feat`
- Words like "fix", "bug", "broken", "crash", "error" → `fix`
- Words like "refactor", "clean up", "simplify", "restructure" → `refactor`
- Words like "update deps", "migrate", "maintenance", "chore" → `chore`

If the type is unclear, omit it.

---

## Operation A: Create a new item

### A1. Propose the item and tasks

Based on `$ARGUMENTS`, propose:

1. **Item name** — short, descriptive title
2. **Type** (optional) — Conventional Commits type to include in the slug (e.g. `feat`, `fix`, `refactor`, `chore`)
3. **Tasks** — break the item into concrete implementation tasks. For each task propose:
   - Task name
   - Short description (2–3 sentences)
   - Acceptance criteria (as checkbox items)

Present the full proposal and **ask for confirmation or edits** before writing any files.

### A2. Item placement

After user confirms:

1. Scan `.backlogmd/work/` for existing item folders.
2. Count open items.

Then:

- **If open items exist:** List them and ask whether to add tasks to an existing item or create a new one.
- **If no open items exist:** Proceed with creating a new item folder.
- **If 50 items already exist:** Auto-archive the lowest-numbered completed item (FIFO) to make room, then create the new item. If no completed items exist, inform the user that the limit is reached and no items can be archived.

### A3. Write all files

#### Append item to `backlog.md`

Read `.backlogmd/backlog.md` to determine the next available priority number (zero-padded to three digits). Add a new entry at the end:

```
- [<NNN>-<type>-<item-name-slug>](work/<NNN>-<type>-<item-name-slug>/index.md)
```

#### Create item folder

1. Create `.backlogmd/work/<item-slug>/`
2. Create `.backlogmd/work/<item-slug>/index.md` with bullet list of task links.

#### Create task files

For each task, create `.backlogmd/work/<item-slug>/<NNN>-<task-slug>.md` using the task format above.

- Task numbers are zero-padded to three digits and sequential within the item.
- Task slugs are lowercase kebab-case derived from the task name.
- Set initial status to `open`.

#### Update item index

Add a bullet entry for each new task to `index.md`:

```
- [<NNN>-<task-slug>](<NNN>-<task-slug>.md)
```

---

## Operation B: Update task status

### B1. Identify the task

- If the user names a specific task, locate it by searching item folders.
- If ambiguous, list matching tasks and ask the user to pick one.
- Read the task file to confirm current status.

### B2. Validate the transition

Tasks move forward through statuses only, never backward:

`open` → `in-progress` → `done`

Use `block` when a task is blocked (can transition back to `open` or `in-progress` when unblocked).

- Reject any backward transition (except unblocking) and explain why.
- If the task has `DependsOn`, verify the dependency is `done` before allowing `in-progress`.

### B3. Update the task file

Update the `Status:` field in the task's metadata code block.

If moving to `done`, check all acceptance criteria boxes (`- [ ]` → `- [x]`).

### B4. Handle item completion

If all tasks in the item are now `done`:

1. Inform the user that all tasks in the item are complete.
2. Do NOT suggest archiving. Completed items stay in `work/` until the 50-item limit forces archival.

---

## Operation C: Edit an item or task

### C1. Identify the target

Locate the item or task file the user wants to edit.

### C2. Present current content

Show the current content and ask the user what they want to change.

### C3. Apply edits

- Edit the target file with the requested changes.
- If editing a task's name, also update the item's `index.md` link to keep it in sync.

### C4. Confirm changes

Show the user a summary of what was changed.

---

## Operation D: Archive an item

### D1. Validate

- Read the item's task files and verify **all tasks are `done`**.
- If any tasks are not `done`, inform the user and refuse to archive.

### D2. Create archive structure (if needed)

Ensure `.backlogmd/.archive/` exists (create if missing).

### D3. Move the item folder

Move `.backlogmd/work/<item-slug>/` to `.backlogmd/.archive/<YYYY>/<MM>/<item-slug>/` (using the current year and month). Create the year/month directories if they don't exist.

### D4. Update `backlog.md`

Remove the item entry from `.backlogmd/backlog.md`.

### D5. Confirm

Report to the user that the item has been archived and how many open item slots remain.

---

## Operation E: Show backlog status

### E1. Read all state

- Read `backlog.md` for the item overview.
- Scan item folders and read each item's task files.

### E2. Present a summary

Show:

- Total items and their types
- For each item: task breakdown by status (e.g. "3/5 tasks done")
- Any tasks currently in-progress
- Items ready to archive (all tasks done but not yet archived)
- Open item slots remaining (out of 50)

---

## Operation F: Sanity check

Validate that the entire `.backlogmd/` system is consistent. Read all files and check every rule below. Report issues grouped by severity.

### F1. Read all state

- Read `backlog.md`.
- Scan `work/` and read every `index.md` and task file.
- If `.archive/` exists, scan it too (read-only check).

### F2. Validate structure

- [ ] `backlog.md` exists.
- [ ] Every item in `backlog.md` has a corresponding folder in `work/`.
- [ ] Every item folder has an `index.md`.
- [ ] Every task file referenced in an item's `index.md` exists.
- [ ] No orphan task files (files in an item folder that aren't listed in `index.md`).
- [ ] No more than 50 open items in `work/`.

### F3. Validate formats

- [ ] Every `backlog.md` entry follows the format `- [<slug>](work/<slug>/index.md)`.
- [ ] Every `index.md` is a bullet list of task links.
- [ ] Every task file has METADATA, DESCRIPTION, and ACCEPTANCE CRITERIA sections.
- [ ] Every task has required metadata fields: Task, Status, Priority.
- [ ] Task statuses are valid (`open`, `block`, `in-progress`, `done`).
- [ ] Priority numbers are zero-padded to three digits and unique within their scope.
- [ ] Slugs are lowercase kebab-case.
- [ ] If a type segment is present in slugs, it follows Conventional Commits (e.g. `feat`, `fix`, `refactor`, `chore`).

### F4. Validate consistency

- [ ] Task files listed in `index.md` match actual files in the folder.
- [ ] If dependencies are used, no circular dependencies exist.
- [ ] If dependencies are used, no task is `in-progress` while its dependency is not `done`.

### F5. Validate archive

- [ ] Archived item folders in `.archive/` are not also present in `work/`.
- [ ] `backlog.md` does not reference archived items.

### F6. Report

Present results as:

- **Errors** — spec violations that must be fixed (missing files, broken links, invalid statuses).
- **Warnings** — potential issues (items with all tasks done but not archived).
- **OK** — checks that passed.

If errors are found, offer to fix them automatically (with user confirmation before writing).

---

## Rules

- Follow the spec formats exactly — no YAML frontmatter.
- All paths are relative within `.backlogmd/`.
- Never overwrite existing items or tasks — only append (for creation) or edit in place (for updates).
- Always confirm with the user before writing or modifying files.
- Max 50 open items in `work/`. If the limit is reached, the user must archive an item or use an existing one.
- The `.archive/` directory is cold storage. After moving items into it, never modify them again.
- A completed task cannot be reopened. If the work needs revisiting, create a new task instead.
