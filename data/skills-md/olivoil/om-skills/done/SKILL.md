---
name: done
description: Capture a session summary (decisions, questions, follow-ups) into the Obsidian vault and link it from the daily note. Use when the user types /done or asks to wrap up a coding session.
allowed-tools: Read, Write, Edit, Bash(git *)
---

# Session Summary

Capture the key outcomes of this Claude Code session into a markdown file in the Obsidian vault, and link it from today's daily note.

## Steps

### 0. Resolve vault path

Run `echo $OBSIDIAN_VAULT_PATH` to get the Obsidian vault root directory. If empty, ask the user for the path before proceeding.

### 1. Gather metadata

- **Date**: Use today's date (YYYY-MM-DD format)
- **Branch**: Run `git branch --show-current` in the current working directory
- **Repo**: Derive from the working directory (e.g. `olivoil/obsidian` from `/home/olivier/Code/github.com/olivoil/obsidian`)
- **Session ID**: Find the most recently modified `.jsonl` file in the project's `.claude/projects/` directory. Extract the UUID from the filename (the part before `.jsonl`) and use the first 8 characters.

### 2. Generate the summary

Review the full conversation and extract:

- **One-line summary**: A single sentence describing what was accomplished
- **Decisions**: Key decisions made during the session (bullet list)
- **Open questions**: Unresolved items or things that need further investigation (bullet list)
- **Follow-ups**: Next steps or tasks to do later (checklist with `- [ ]`)
- **Files changed**: Run `git diff --name-only $(git merge-base HEAD main)..HEAD 2>/dev/null || git diff --name-only HEAD` to get changed files on this branch. If there are unstaged changes, also include output from `git diff --name-only` and `git diff --name-only --cached`. Deduplicate the list.

If a section has no items, omit it entirely.

### 3. Write the session file

**Path**: `$OBSIDIAN_VAULT_PATH/💻 Coding/{date}--{repo-name}--{branch}.md`

Use just the repo name (e.g. `om-skills` from `olivoil/om-skills`). If the branch name contains `/`, replace them with `-` (e.g. `feature/foo` becomes `feature-foo`).

If a file already exists at that path (same branch, same day), append a counter: `{date}--{repo-name}--{branch}--2.md`, `{date}--{repo-name}--{branch}--3.md`, etc.

**Format**:

```markdown
---
date: {date}
branch: {branch}
repo: {repo}
session: {session-id}
---

# Session: {branch}

> {one-line summary}

## Decisions
- Decision 1
- Decision 2

## Open Questions
- Question 1

## Follow-ups
- [ ] Task 1
- [ ] Task 2

## Files Changed
- path/to/file1.ts
- path/to/file2.md
```

### 4. Link from the daily note

**Path**: `$OBSIDIAN_VAULT_PATH/📅 Daily Notes/{date}.md`

If the daily note doesn't exist, create it.

Look for an existing `### Coding Sessions` section. If found, append the new link under it.

If not found, insert a new `### Coding Sessions` section. The daily note typically has this structure:

1. **Hours list** (lines like `- [[Project]] - task - duration`)
2. **Todos section** (`### Todos`)
3. **Coding Sessions** ← insert here
4. **Other notes sections** (e.g. `### Technomic`, `### Khov`, etc.)

To find the right insertion point: look for the first `---` horizontal rule or `###` heading that comes **after** the Todos section. Insert the Coding Sessions block just before it. If there's no Todos section, insert before the first `###` heading that isn't Todos. If there are no other sections at all, append to the end.

The block to insert:

```markdown

------
### Coding Sessions
- [[{date}--{repo-name}--{branch}]] - {one-line summary}
```

If the section already exists, just append the new bullet:

```markdown
- [[{date}--{repo-name}--{branch}]] - {one-line summary}
```

### 5. Confirm

Tell the user:
- The path of the created session file
- That the daily note was updated
- A brief preview of the summary
