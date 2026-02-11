---
name: codex-review
description: Run code review via Codex CLI
---

# Codex Code Review

Run a code review using the Codex CLI in read-only mode with high reasoning effort.

## Review Presets

| Preset        | Alias | Description                                    |
| ------------- | ----- | ---------------------------------------------- |
| `base`        | `1`   | Review against a base branch (PR style)        |
| `uncommitted` | `2`   | Review staged, unstaged, and untracked changes |
| `commit`      | `3`   | Review a specific commit                       |
| `custom`      | `4`   | Custom review instructions                     |

## Execution

### Step 1: Determine Review Mode

If user specifies a preset (`1`-`4` or `base`, `uncommitted`, `commit`, `custom`), use that preset directly.

If no argument is provided, use AskUserQuestion to ask which review mode:

- **Options:**
  1. "Review against base branch (PR style)" - Compare current branch against main/master
  2. "Review uncommitted changes" - Review all local changes not yet committed
  3. "Review a specific commit" - Review changes from a single commit
  4. "Custom review" - Provide custom review instructions

### Step 2: Gather Additional Information (if needed)

- **base** mode: Ask which base branch to compare against (default: `main`)
- **commit** mode: Ask for the commit SHA to review (show recent commits with `git log --oneline -10`)
- **custom** mode: Ask for the custom review instructions

### Step 3: Execute Codex Review

Run the codex review command (uses default model from `~/.codex/config.toml`):

```bash
# base branch review:
codex review --base <branch>

# uncommitted changes:
codex review --uncommitted

# specific commit:
codex review --commit <sha>

# custom review:
codex review "<custom instructions>"
```

### Step 4: Report Results

After codex completes, summarize the key findings for the user.
