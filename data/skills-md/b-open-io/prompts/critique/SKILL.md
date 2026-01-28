---
name: critique
version: 1.0.0
description: This skill should be used when the user asks to "show me the changes", "what did you change", "let me see the diff", "review the code", "open web preview of changes", "show me what you worked on", "compare branches", "explain what changed", or wants to view git diffs in a terminal UI, web browser, or get AI-powered code review explanations.
---

Review git diffs with syntax highlighting, split view, and word-level diff. Show users what code was changed during a session using terminal UI or web preview.

## Prerequisites

Critique requires Bun (does not work with Node.js):

```bash
# Run directly (no install needed)
bunx critique

# Or install globally
bun install -g critique
```

## Core Commands

### View Current Changes

```bash
# Unstaged changes (includes untracked files)
critique

# Staged changes only
critique --staged

# Watch mode - auto-refresh on file changes
critique --watch
```

### View Commits

```bash
# Last commit
critique HEAD

# Specific commit
critique --commit HEAD~1
critique --commit abc1234

# Combined changes from last N commits
critique HEAD~3 HEAD
```

### Compare Branches (PR-style)

```bash
# What feature-branch added vs main
critique main feature-branch

# What current branch added vs main
critique main HEAD
```

### Filter Files

```bash
# Filter by glob pattern
critique --filter "src/**/*.ts"
critique --filter "src/**/*.ts" --filter "lib/**/*.js"
```

## Web Preview

Generate an HTML preview viewable in a browser - ideal for sharing or detailed review:

```bash
# Generate web preview
critique --web

# Generate and open in browser
critique --web --open

# Web preview for commits
critique HEAD --web --open
critique main HEAD --web --open
```

The web preview provides:
- Full syntax highlighting
- Split view with before/after
- Shareable HTML output
- Better for large diffs

## AI-Powered Review

Generate AI explanations of code changes. Best for reviewing AI-generated changes:

```bash
# Review unstaged changes (uses OpenCode by default)
critique review

# Use Claude Code as the AI backend
critique review --agent claude

# Review specific commits
critique review HEAD
critique review --commit HEAD~1

# Review branch diff (like a PR)
critique review main HEAD

# Include session context for better explanations
critique review --agent claude --session <session-id>

# Generate web preview of AI review
critique review --web
critique review --web --open
```

AI review features:
- Orders hunks in logical reading order
- Splits large hunks into digestible chunks
- Explains changes with diagrams and tables
- Groups related changes across files

## Integrations

### Git Difftool

Configure as default git difftool:

```bash
git config --global diff.tool critique
git config --global difftool.critique.cmd 'critique difftool "$LOCAL" "$REMOTE"'
```

Then use: `git difftool HEAD~1`

### Lazygit

Add to `~/.config/lazygit/config.yml`:

```yaml
git:
  paging:
    pager: critique --stdin
```

## Running from Claude Code

Since the TUI runs inside the Bash tool (hidden/folded), use one of these approaches:

### Option 1: Split Pane (macOS with iTerm2, Recommended)

Open critique in a split pane that auto-closes when done:

```bash
# Horizontal split (top/bottom)
/path/to/skills/critique/scripts/open-critique-pane.sh /path/to/repo -h

# Vertical split (side by side)
/path/to/skills/critique/scripts/open-critique-pane.sh /path/to/repo -v
```

### Option 2: New Terminal Tab (macOS with iTerm2)

Open critique in a new tab:

```bash
/path/to/skills/critique/scripts/open-critique.sh /path/to/repo
```

### Option 3: Web Preview (Cross-platform)

Opens in browser - works everywhere:

```bash
bunx critique --web --open
```

## Recommended Usage After Claude Work

When a user asks to see what changed after Claude has made modifications:

1. **New terminal tab (macOS)**: Use osascript to open critique in iTerm
2. **Web preview**: Run `critique --web --open` for browser view
3. **AI-explained review**: Run `critique review --agent claude --web --open`
4. **Compare to starting point**: Run `critique HEAD~N HEAD --web --open`

## Navigation Keys (Terminal UI)

| Key | Action |
|-----|--------|
| `j/k` or `↓/↑` | Navigate lines |
| `h/l` or `←/→` | Switch files |
| `Tab` | Toggle split/unified view |
| `q` | Quit |
| `?` | Help |
