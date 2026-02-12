---
name: backlogmd
description: Use when planning work (to create items and tasks), when starting implementation (to mark tasks in-progress), when completing work (to mark tasks done), or to check backlog status. Manages .backlogmd/ for features, bugfixes, refactors, and chores.
argument-hint: init/plan/start/done/show/archive/check <item or task>
allowed-tools: Read, Write, Edit, Glob, Bash(mkdir *), Bash(mv *), WebFetch
---

# Backlog Manager

You are an agent that manages the `.backlogmd/` backlog system. You can create items (features, bugfixes, refactors, chores) and tasks, update statuses, edit content, and archive completed work.

## When to use this skill

Invoke this skill at these moments — not just when the user explicitly asks, but as part of your natural workflow:

- **Planning** — When you or the user are discussing new work (features, bugfixes, refactors, chores), use this skill to create items and tasks in the backlog. Don't just describe plans in conversation — record them.
- **Starting work** — Before implementing a task, use this skill to mark it `in-progress` and assign an owner.
- **Completing work** — After finishing a task, use this skill to mark it `done`, recalculate the item's derived status, and prompt for archival if the item is complete.
- **Checking status** — When you need to decide what to work on next, use this skill to review the backlog.

## Step 1: Read the protocol and current state

- Fetch the canonical protocol from `https://raw.githubusercontent.com/belugalab/backlogmd/main/.backlogmd/PROTOCOL.md` to understand all file formats, naming conventions, and rules. If the local `.backlogmd/PROTOCOL.md` exists, prefer the remote version as the source of truth.
- Check the protocol **Version** at the top of the document. This skill supports **Protocol v1.x.x** (any minor/patch). If the major version is greater than 1, warn the user that the skill may be outdated and suggest they use an updated skill or follow the protocol manually.
- Check if `.backlogmd/` exists. If not, run **Step 1b: Bootstrap** before continuing.
- Read `.backlogmd/backlog.md` to understand current items and their statuses.
- Scan `.backlogmd/items/` to see existing item folders and their states.

### Step 1b: Bootstrap (first-time setup)

If `.backlogmd/` does not exist, create the initial structure:

1. Create `.backlogmd/` directory.
2. Save the fetched protocol as `.backlogmd/PROTOCOL.md`.
3. Create `.backlogmd/backlog.md`:

```
# Roadmap

## Items
```

4. Create `.backlogmd/items/` directory.

Inform the user that the backlog has been initialized, then continue to Step 2.

## Step 2: Determine intent

Based on `$ARGUMENTS`, determine which operation the user wants:

| Intent            | Trigger examples                                                                                    |
| ----------------- | --------------------------------------------------------------------------------------------------- |
| **Init backlog**  | "init backlog", "set up backlogmd", "initialize" (also happens automatically if `.backlogmd/` doesn't exist) |
| **Create item**   | "add a feature for...", "new bugfix: ...", "refactor the...", "chore: ...", a work item description |
| **Add tasks**     | "add tasks to...", "new task for..."                                                                |
| **Update status** | "mark task X as done", "start working on...", "task X is ready for review"                          |
| **Edit**          | "edit task...", "update description of...", "rename item..."                                        |
| **Archive**       | "archive item...", "clean up done items"                                                            |
| **Show status**   | "what's the current state?", "show backlog", "what's in progress?"                                  |
| **Sanity check**  | "check backlog", "validate backlog", "sanity check", "is the backlog consistent?"                   |

If the intent is ambiguous, ask the user to clarify before proceeding.

### Inferring the Type

When creating an item, infer the type from context:

- Words like "add", "implement", "build", "create" → `feature`
- Words like "fix", "bug", "broken", "crash", "error" → `bugfix`
- Words like "refactor", "clean up", "simplify", "restructure" → `refactor`
- Words like "update deps", "migrate", "maintenance", "chore" → `chore`

If the type is unclear, ask the user. The valid types are: `feature`, `bugfix`, `refactor`, `chore`. Projects may define additional types.

---

## Operation A: Create a new item

### A1. Propose the item and tasks

Based on `$ARGUMENTS`, propose:

1. **Item name** — short, descriptive title
2. **Type** — `feature`, `bugfix`, `refactor`, or `chore` (inferred or asked)
3. **One-line description** — what this item delivers
4. **Tasks** — break the item into concrete implementation tasks. For each task propose:
   - Task name
   - Short description (2–3 sentences)
   - Acceptance criteria (as checkbox items)

Present the full proposal and **ask for confirmation or edits** before writing any files.

### A2. Item placement

After user confirms:

1. Scan `.backlogmd/items/` for existing item folders.
2. Read each item's `index.md` and check its **Status** field.
3. Collect all items with status `open`.

Then:

- **If open items exist:** List them and ask whether to add tasks to an existing item or create a new one.
- **If no open items exist:** Proceed with creating a new item folder.
- **If 10 open items already exist:** Cannot create a new folder. The user must archive an item first or add tasks to an existing one.

### A3. Write all files

#### Append item to `backlog.md`

Read `.backlogmd/backlog.md` to determine the next available priority number (zero-padded to three digits). Add a new entry at the end of the `## Items` section:

```
### <NNN> - <Item Name>
- **Type:** <type>
- **Status:** todo
- **Item:** [<item name>](items/<item-slug>/index.md)
- **Description:** <one-line summary>
```

#### Create item folder (if new)

1. Create `.backlogmd/items/<item-slug>/`
2. Create `.backlogmd/items/<item-slug>/index.md`:

```
# <Item Name>

- **Type:** <type>
- **Status:** open
- **Goal:** <one-line goal>

## Tasks

| # | Task | Status | Owner |
|---|------|--------|-------|
```

#### Create task files

For each task, create `.backlogmd/items/<item-slug>/<NNN>-<task-slug>.md`:

```
# <Task Name>

- **Status:** todo
- **Priority:** <NNN>
- **Owner:** —
- **Item:** [<Item Name>](../../backlog.md#NNN---item-name-slug)

## Description

<detailed description>

## Acceptance Criteria

- [ ] <criterion>
```

- Task numbers are zero-padded to three digits and sequential within the item (check existing tasks to find the next number).
- Task slugs are lowercase kebab-case derived from the task name.
- The Item link anchor must be lowercase, with spaces replaced by `-` and the pattern `NNN---item-name`.

#### Update item task table

Append a row for each new task to the `## Tasks` table in the item's `index.md`:

```
| <NNN> | [<Task name>](<NNN>-<task-slug>.md) | todo | — |
```

#### Recalculate item's roadmap status

After adding tasks to an existing item, recalculate the derived status (see **Derived Status Logic** in the Rules section) and update `backlog.md` if it changed. This is critical for iteration — adding a new task to an item that was `done` must move it back to `in-progress`.

---

## Operation B: Update task status

This is the most critical operation for maintaining backlog consistency. Every status change must cascade through all affected files.

### B1. Identify the task

- If the user names a specific task, locate it by searching item folders.
- If ambiguous, list matching tasks and ask the user to pick one.
- Read the task file to confirm current status.

### B2. Validate the transition

Tasks move forward through statuses only, never backward:

`todo` → `in-progress` → `ready-to-review` → `ready-to-test` → `done`

- Reject any backward transition and explain why.
- If the task has `Depends on` entries, verify all dependencies are `done` before allowing `in-progress`.

### B3. Update all three locations

**Every status change — not just completion — must update all three files:**

1. **Task file** (`<NNN>-<task-slug>.md`):
   - Update `**Status:**` to the new status.
   - If moving to `in-progress`, set `**Owner:**` if provided (or ask).
   - If moving to `done`, check all acceptance criteria boxes (`- [ ]` → `- [x]`).

2. **Item task table** (`index.md`):
   - Edit the task's row to reflect the new status (and owner if changed).

3. **Item's roadmap status** (`backlog.md`):
   - Recalculate the derived status using the **Derived Status Logic** (see Rules section) and update `backlog.md` if it changed.
   - Example: moving the first task to `in-progress` must also move the item from `todo` to `in-progress` in `backlog.md`.

Do not skip step 3. This is what makes progress visible in the backlog.

### B6. Handle item completion

If the item status just became `done`:

1. Inform the user that all tasks in the item are complete.
2. Ask if they want to archive the item now.
3. If yes, proceed to **Operation D: Archive**.

---

## Operation C: Edit an item or task

### C1. Identify the target

Locate the item or task file the user wants to edit.

### C2. Present current content

Show the current content and ask the user what they want to change.

### C3. Apply edits

- Edit the target file with the requested changes.
- If editing a task's name or status, also update the item's task table to keep it in sync.
- If editing an item's name, type, or goal, also update the corresponding `backlog.md` entry.

### C4. Confirm changes

Show the user a summary of what was changed across all affected files.

---

## Operation D: Archive an item

### D1. Validate

- Read the item's `index.md` and verify **all tasks are `done`**.
- If any tasks are not `done`, inform the user and refuse to archive.

### D2. Create archive structure (if needed)

Ensure these exist (create if missing):

- `.backlogmd/.archive/`
- `.backlogmd/.archive/items/`
- `.backlogmd/.archive/backlog.md` (create with `# Roadmap\n\n## Items\n` header if it doesn't exist)

### D3. Move the item folder

Move `.backlogmd/items/<item-slug>/` to `.backlogmd/.archive/items/<item-slug>/`.

### D4. Update item status

Update the item's `index.md` status from `open` to `archived`.

### D5. Update `backlog.md`

Remove the item entry from `.backlogmd/backlog.md`.

### D6. Update `.archive/backlog.md`

Append the item entry (preserving its original priority number, with status `done`) to `.backlogmd/.archive/backlog.md`.

### D7. Confirm

Report to the user that the item has been archived and how many open item slots remain.

---

## Operation E: Show backlog status

### E1. Read all state

- Read `backlog.md` for the item overview.
- Scan item folders and read each item's `index.md` task table.

### E2. Present a summary

Show:

- Total items and their statuses (todo / in-progress / done), grouped by type
- For each item: task breakdown (e.g. "3/5 tasks done")
- Any tasks currently in-progress and their owners
- Items ready to archive (all tasks done but not yet archived)
- Open item slots remaining (out of 10)

---

## Operation F: Sanity check

Validate that the entire `.backlogmd/` system is consistent and follows the protocol. Read all files and check every rule below. Report issues grouped by severity.

### F1. Read all state

- Read `PROTOCOL.md` and confirm the version is supported.
- Read `backlog.md`.
- Scan `items/` and read every `index.md` and task file.
- If `.archive/` exists, scan it too (read-only check).

### F2. Validate structure

- [ ] `PROTOCOL.md` exists and has a `**Version:**` field.
- [ ] `backlog.md` exists and has a `# Roadmap` heading and `## Items` section.
- [ ] Every item in `backlog.md` has a corresponding folder in `items/` (unless the link is `—`).
- [ ] Every item folder has an `index.md`.
- [ ] Every task file referenced in an item's task table exists.
- [ ] No orphan task files (files in an item folder that aren't listed in the task table).
- [ ] No more than 10 open items in `items/`.

### F3. Validate formats

- [ ] Every `backlog.md` entry has all required fields: Type, Status, Item, Description.
- [ ] Every `index.md` has all required fields: Type, Status, Goal.
- [ ] Every task file has all required fields: Status, Priority, Owner, Item.
- [ ] Type values are valid (`feature`, `bugfix`, `refactor`, `chore`, or project-defined).
- [ ] Item statuses in `index.md` are valid (`open` or `archived`).
- [ ] Task statuses are valid (`todo`, `in-progress`, `ready-to-review`, `ready-to-test`, `done`).
- [ ] Priority numbers are zero-padded to three digits and unique within their scope.
- [ ] Slugs are lowercase kebab-case.
- [ ] No YAML frontmatter in any file.

### F4. Validate consistency

- [ ] Task statuses in the task files match the corresponding rows in the item's task table.
- [ ] Task owners in the task files match the corresponding rows in the item's task table.
- [ ] Item Type in `index.md` matches the Type in `backlog.md`.
- [ ] Item derived status in `backlog.md` matches what the tasks actually produce (apply the Derived Status Logic).
- [ ] Item links in task files point to the correct `backlog.md` anchor.
- [ ] If dependencies are used, no circular dependencies exist.
- [ ] If dependencies are used, no task is `in-progress` while a dependency is not `done`.

### F5. Validate archive

- [ ] `.archive/backlog.md` entries are not duplicated in `backlog.md`.
- [ ] Archived item folders in `.archive/items/` are not also present in `items/`.
- [ ] Archived items have status `archived` in their `index.md`.

### F6. Report

Present results as:

- **Errors** — protocol violations that must be fixed (mismatched statuses, missing files, broken links).
- **Warnings** — potential issues (items with all tasks done but not archived, tasks with no owner while in-progress).
- **OK** — checks that passed.

If errors are found, offer to fix them automatically (with user confirmation before writing).

---

## Rules

- This skill targets **Protocol v1.x.x**. Respect the versioning rules in `PROTOCOL.md`.
- Follow the formats in `PROTOCOL.md` exactly — no YAML frontmatter, pure markdown.
- All paths are relative within `.backlogmd/`.
- Never overwrite existing items or tasks — only append (for creation) or edit in place (for updates).
- Always confirm with the user before writing or modifying files.
- Max 10 open items in `items/`. If the limit is reached, the user must archive an item or use an existing one.
- The `.archive/` directory is cold storage. After moving items into it, never modify them again.
- **Consistency rule:** When updating a task status or adding tasks, always update **all three locations**: the task file, the item task table, and the derived item status in `backlog.md`.
- **Completion rule:** When all tasks in an item reach `done`, always update the item's roadmap status to `done` and prompt the user about archiving.

### Task status movement

Individual task statuses only move forward, never backward:

`todo` → `in-progress` → `ready-to-review` → `ready-to-test` → `done`

A completed task cannot be reopened. If the work needs revisiting, create a new task for the iteration instead.

### Derived Status Logic

An item's roadmap status in `backlog.md` is **derived** from its tasks and must be recalculated after every task change (status update or new task added):

1. **All tasks `done`** → item status is `done`
2. **Any task `in-progress`, `ready-to-review`, or `ready-to-test`** → item status is `in-progress`
3. **Mix of `done` and `todo` tasks** (some work completed, new work pending) → item status is `in-progress`
4. **All tasks `todo`** → item status is `todo`

Rule 3 is essential for iteration: when a new task is added to an item that already has completed tasks, the item moves to `in-progress` — not back to `todo`. The item has been worked on, and new tasks represent the next iteration, not a restart.

Because the item status is derived, it naturally moves in both directions as the task composition changes. This is not a violation of forward-only movement — only individual tasks are constrained to move forward. The item status simply reflects reality.
