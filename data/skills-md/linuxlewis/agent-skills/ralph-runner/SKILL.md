---
name: ralph-runner
description: Run Ralph Wiggum autonomous coding loops. Use when user asks to run ralph, start autonomous coding, execute a PRD, implement features from a task list, or wants Claude Code to work through user stories iteratively.
license: MIT
compatibility: Requires ralph-cli and Claude Code CLI installed
metadata:
  author: linuxlewis
  version: "1.0.0"
---

# Ralph Runner

Run autonomous AI coding loops that implement features from a PRD (Product Requirements Document) iteratively.

## Prerequisites

- **Claude Code** - `claude --version`
- **ralph-cli** - `ralph --version`

## Quick Start

```bash
# Check status of a PRD
ralph status prd.json

# Run the loop
ralph run prd.json

# With context files
ralph run prd.json --context AGENTS.md --context ./docs

# More iterations
ralph run prd.json --iterations 20
```

## Workflow

### 1. Create PRD

Create a `prd.json` file with user stories:

```json
{
  "project": "MyApp",
  "branchName": "ralph/feature-name",
  "description": "Feature description",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add login form",
      "priority": 1,
      "passes": false
    }
  ]
}
```

### 2. Run Ralph

```bash
ralph run prd.json --context AGENTS.md
```

### 3. Monitor Progress

```bash
ralph status prd.json
```

## How It Works

Each iteration:
1. Reads `prd.json`, picks highest priority story where `passes: false`
2. Spawns fresh Claude Code instance
3. Claude implements that ONE story
4. Runs quality checks (typecheck, lint, tests)
5. If passing: commits, updates `prd.json`, appends to `progress.txt`
6. Outputs `<promise>COMPLETE</promise>` when all done

Memory persists via:
- Git history (commits)
- `progress.txt` (learnings)
- `prd.json` (status)

## CLI Reference

### `ralph run <prd>`

```bash
ralph run prd.json [options]

Options:
  -i, --iterations <n>    Max iterations (default: 10)
  -c, --context <paths>   Context files/dirs to include
  -p, --prompt <path>     Custom prompt template
  --headed                Show Claude output live
  --dry-run               Preview without running
```

### `ralph status [prd]`

```bash
ralph status prd.json
```

Shows progress bar and story status.

## PRD Format

See [references/prd-format.md](references/prd-format.md) for complete format specification.

## Best Practices

1. **Keep stories small** - Each should complete in one context window
2. **Good acceptance criteria** - Be specific about "done"
3. **Include typecheck** - Add "Typecheck passes" to criteria
4. **Use context** - Pass in AGENTS.md and relevant docs
5. **Check progress.txt** - Contains learnings from previous iterations
