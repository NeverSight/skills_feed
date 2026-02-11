---
name: update-allowed-tools
description: Scans a skill's SKILL.md and sibling files for tool references (Bash commands, file tools, skill invocations) and adds missing entries to the allowed-tools frontmatter. Use when creating or editing a skill that uses Bash commands or external tools
context: fork
user-invocable: true
model: haiku
allowed-tools:
  - Grep
  - Glob
  - Read
  - Edit
  - Bash(find:*)
---

# Overview

Analyzes a skill's full content -- SKILL.md and any sibling files in the same directory -- to find tools it references or requires, then compares against the skill's `allowed-tools` frontmatter to find missing entries.

## Usage

```
/update-allowed-tools <skill name>
/update-allowed-tools @path/to/SKILL.md
```

## Instructions

1. **Parse argument**: The argument is either a file path to a SKILL.md file, or a skill name/description. If no file path is provided, search for the skill using Glob — first in the current working directory (e.g., `**/skills/**/<name>/SKILL.md`), then in `~/.claude/skills/**/<name>/SKILL.md`.

2. **Read the skill file** and separate the YAML frontmatter from the body content. Also read any other files in the same directory (sibling files referenced by or bundled with the skill).

3. **Extract declared allowed-tools**: Parse all entries under `allowed-tools:` in the frontmatter.

4. **Scan all skill content** (SKILL.md body + sibling files) for tool usage. Look for:
   - Explicit tool names: e.g., `Read`, `Write`, `Edit`, `Bash`, `WebFetch`, `WebSearch`, `Task`, `AskUserQuestion`, `Skill`, etc.
   - Bash command patterns: e.g., `git diff`, `git commit`, `make`, `npm`, `docker`, `python`, `curl`, etc.
   - For Bash commands found, the required allowed-tool format is `Bash(<command>:*)` (e.g., `git stash push` needs `Bash(git stash:*)`)
   - For file tools with path patterns (Read, Write, Edit), note the paths referenced (e.g., `/tmp/` needs `Read(//tmp/**)`)
   - Skill invocations: e.g., `commit`, `Use the commit skill`, `Skill(commit)`. The required allowed-tool format is `Skill(<name>)` (e.g., `commit` needs `Skill(commit)`)

5. **Compare**: For each tool detected in the body, check if it's covered by an entry in `allowed-tools`. Rules:
   - `Glob`, `Grep`, `Read`, `Write`, `Edit` are available by default for files within the project directory. Only add these when the skill needs to access files **outside** the project (e.g., `Read(//tmp/**)`, `Write(~/.config/**)`).
   - `Bash` commands always need explicit `Bash(<command>:*)` entries.
   - A Bash pattern covers subcommands (e.g., `Bash(git stash:*)` covers `git stash push`).
   - Exact match counts as covered (e.g., `WebSearch` matches `WebSearch`).

6. **Update the skill file**: For any missing tools found, add them to the `allowed-tools` list in the skill's YAML frontmatter using the Edit tool. Then report what was added.

7. **Validate**: Re-read the updated file to confirm YAML frontmatter remains syntactically valid (proper indentation, no duplicate entries, correct list format).
