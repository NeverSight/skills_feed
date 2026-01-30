---
name: go
description: Resume work on a fiction project. Loads context and suggests what to do next.
argument-hint: "[path/to/project]"
---

Resume work on a fiction project. This loads the project into context and provides a clear recommendation for what to work on next.

## Current State

- Recent changes: !`git log --oneline -3 2>/dev/null || echo "not a git repo"`
- Progress file: !`cat progress.md 2>/dev/null | head -20 || echo "no progress.md"`

## What to Do

### 1. Load the Project

**Find Project Root** — Look for README.md with story information, chapters/ directory, characters/ directory.

**Read Core Documents:**
- README.md — Project overview, status, key decisions
- themes.md — Central question, thematic content
- craft/tone.md — Voice and style guidance

**Read Character Documents** — All files in characters/

**Read World Documents** — All files in world/

**Scan Chapters:**
- For 10+ chapters: spawn parallel reader-skim agents
- For smaller projects: scan directly (first 1-2 paragraphs, word counts, status)

**Check Supporting Directories:**
- builds/ — Most recent build date
- covers/ — Cover iterations, final cover.png
- critiques/ — Most recent critique date
- synopses/ — Most recent synopsis date

### 2. Assess and Recommend

After loading, use the next agent to assess status and suggest what to do:

```
Task tool with subagent_type: "fiction:next"
prompt: "Assess project status and suggest next steps for: [project-path]"
```

### 3. Output

Output the combined result:

```markdown
## Project Loaded: [Name]

**Premise:** [One sentence]

**Status:** [X] chapters drafted, [Y] outlined

**Characters:**
- [Protagonist] — [brief description]
- [Other key characters]

**Builds:** [Latest: builds/2026-01-18/name.epub] or [No builds yet]
**Covers:** [X iterations, final cover ready] or [No covers yet]
**Critiques:** [X critiques, latest: 2026-01-19] or [No critiques yet]
**Synopses:** [X synopses, latest: 2026-01-19] or [No synopses yet]

---

## What to Do Now

**[Single clear recommendation from next agent]**

[Why this is the priority]

### Concrete Steps

1. **[First action]** — [Specific, immediate]
2. **[Second action]** — [What follows]
3. **[Third action]** — [Completion point]

## Command to Run
`/fiction:[relevant command]`
```

## Arguments

```
/fiction:go                    # Resume project in current directory
/fiction:go /path/to/project   # Resume specific project
```

If arguments provided: $ARGUMENTS

## When to Use

- Starting a writing session
- Coming back after time away
- Don't know where you left off
- Need direction on what to work on next

## Notes

- If you already have context and just want suggestions, use `/fiction:next`
