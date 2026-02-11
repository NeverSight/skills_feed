---
name: hook-manager
version: 1.0.0
description: Discover and install automation hooks for Claude Code and Opencode. This skill should be used when users ask to "list hooks", "install a hook", "show available hooks", "enable hook", "what hooks are available", or need help managing agent automation hooks.
---

# Hook Manager

Discover, install, and manage automation hooks from the bopen-tools collection for Claude Code and Opencode.

## Available Hooks

| Hook | Event | Description | Auto-install |
|------|-------|-------------|--------------|
| `protect-env-files` | PreToolUse | Blocks edits to .env files (security) | Recommended |
| `uncommitted-reminder` | Stop | Shows uncommitted changes when agent stops | Optional |
| `auto-git-add` | PostToolUse | Auto-stages files after edits | Optional |
| `time-dir-context` | UserPromptSubmit | Adds timestamp/dir/branch to prompts | Optional |
| `lint-on-save` | PostToolUse | Runs lint:fix after file edits | Optional |
| `lint-on-start` | SessionStart | Runs linting on session start | Optional |
| `auto-test-on-save` | PostToolUse | Runs tests after file edits | Optional |
| `protect-shadcn-components` | PreToolUse | Protects shadcn UI components | Optional |

## Installing a Hook

Hooks are installed by copying the JSON config to your agent's hooks directory:

### Claude Code
```bash
# Create hooks directory if needed
mkdir -p ~/.claude/hooks

# Copy hook from plugin cache
cp ~/.claude/plugins/cache/bopen-tools/user/.claude/hooks/<hook-name>.json ~/.claude/hooks/
```

### Opencode
```bash
# Create hooks directory if needed
mkdir -p ~/.opencode/hooks

# Copy hook from plugin cache
cp ~/.opencode/plugins/cache/bopen-tools/user/.claude/hooks/<hook-name>.json ~/.opencode/hooks/
```

Then restart your agent to load the hook.

## Hook Details

### protect-env-files (Recommended)

**Security hook** - Prevents accidental edits to environment files containing secrets.

- Blocks: `.env`, `.env.local`, `.env.production`, `.env.staging`
- Prompts for confirmation if edit attempted
- No performance impact

### uncommitted-reminder

Shows git status when Claude finishes responding if there are uncommitted changes.

- Helps prevent forgotten commits
- Exit code 2 feeds back to Claude

### auto-git-add

Automatically runs `git add -A` after Write/Edit/MultiEdit operations.

- Only stages, never commits
- 5 second timeout

### time-dir-context

Adds context line to every prompt: timestamp, working directory, git branch.

- Example: `Context: 2025-01-24 14:32:15 | /Users/you/project | Branch: main`

### lint-on-save

Runs `bun lint:fix` after file edits.

- Requires project with `lint:fix` script in package.json
- Requires `bun` and `jq`
- Works with statusline for lint count display

### lint-on-start

Runs linting when session starts.

- Same requirements as lint-on-save

### auto-test-on-save

Runs tests after file edits.

- Can be slow on large test suites
- Consider project-specific setup

### protect-shadcn-components

Prevents edits to shadcn/ui component files.

- Only relevant for projects using shadcn/ui

## Installing This Skill

```bash
bunx skills add b-open-io/bopen-tools --skill hook-manager
```

## Uninstalling a Hook

**Claude Code:**
```bash
rm ~/.claude/hooks/<hook-name>.json
```

**Opencode:**
```bash
rm ~/.opencode/hooks/<hook-name>.json
```

Restart your agent.

## Listing Installed Hooks

**Claude Code:**
```bash
ls ~/.claude/hooks/
```

**Opencode:**
```bash
ls ~/.opencode/hooks/
```

## Quick Install Commands

### Claude Code
```bash
# Security (recommended)
cp ~/.claude/plugins/cache/bopen-tools/user/.claude/hooks/protect-env-files.json ~/.claude/hooks/

# Workflow helpers
cp ~/.claude/plugins/cache/bopen-tools/user/.claude/hooks/uncommitted-reminder.json ~/.claude/hooks/
cp ~/.claude/plugins/cache/bopen-tools/user/.claude/hooks/auto-git-add.json ~/.claude/hooks/

# Context enrichment
cp ~/.claude/plugins/cache/bopen-tools/user/.claude/hooks/time-dir-context.json ~/.claude/hooks/

# Development automation
cp ~/.claude/plugins/cache/bopen-tools/user/.claude/hooks/lint-on-save.json ~/.claude/hooks/
cp ~/.claude/plugins/cache/bopen-tools/user/.claude/hooks/lint-on-start.json ~/.claude/hooks/
```

### Opencode
```bash
# Security (recommended)
cp ~/.opencode/plugins/cache/bopen-tools/user/.claude/hooks/protect-env-files.json ~/.opencode/hooks/

# Workflow helpers
cp ~/.opencode/plugins/cache/bopen-tools/user/.claude/hooks/uncommitted-reminder.json ~/.opencode/hooks/
cp ~/.opencode/plugins/cache/bopen-tools/user/.claude/hooks/auto-git-add.json ~/.opencode/hooks/

# Context enrichment
cp ~/.opencode/plugins/cache/bopen-tools/user/.claude/hooks/time-dir-context.json ~/.opencode/hooks/

# Development automation
cp ~/.opencode/plugins/cache/bopen-tools/user/.claude/hooks/lint-on-save.json ~/.opencode/hooks/
cp ~/.opencode/plugins/cache/bopen-tools/user/.claude/hooks/lint-on-start.json ~/.opencode/hooks/
```

## Verifying Installation

After installing and restarting your agent:

```bash
claude --debug
```

Look for hook registration messages in the debug output.
