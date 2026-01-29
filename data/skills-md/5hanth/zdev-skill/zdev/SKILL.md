---
name: zdev
description: Manage isolated dev environments with git worktrees, auto ports, and preview URLs
---

# zdev Skill

Use `zdev` to manage isolated development environments when working on features. Each feature gets its own git worktree, ports, and optional public preview URL.

## Prerequisites

- `zdev` CLI installed (`bunx zdev` or `bun add -g zdev`)
- Vite-based frontend project (Convex backend is optional, auto-detected)

## Creating a New Project

```bash
# Basic TanStack Start project
zdev create my-app

# With Convex backend
zdev create my-app --convex

# Flat structure (no monorepo)
zdev create my-app --flat
```

Creates:
- TanStack Start app with clean routes
- `.zdev/setup.sh` for worktree setup
- Agentation for UI feedback (dev only)

## Initializing an Existing Project

```bash
zdev init /path/to/project
```

Creates `.zdev/project.json` with project metadata.

## Configuration

First-time setup (or to change settings):

```bash
zdev config --set devDomain=dev.example.com
zdev config --set traefikConfigDir=/etc/traefik/dynamic
zdev config --list
```

## Before Starting Any Feature

```bash
# Check what's already running
zdev list
```

If your feature already exists, just `cd` to the worktree path shown.

## Starting a New Feature

```bash
# Start feature with public URL
zdev start <feature-name> -p /path/to/project

# Start without public URL (local only)
zdev start <feature-name> -p /path/to/project --local

# Start with seed data (Convex projects)
zdev start <feature-name> -p /path/to/project --seed

# Use different base branch
zdev start <feature-name> -p /path/to/project --base-branch main
```

After starting:
1. `.zdev/setup.sh` runs automatically (installs deps, etc.)
2. Note the worktree path (e.g., `~/.zdev/worktrees/project-feature`)
3. Note the local URL (e.g., `http://localhost:5173`)
4. Note the public URL if available (e.g., `https://project-feature.dev.example.com`)
5. `cd` to the worktree path to begin work

## While Working

You're in an isolated git worktree with its own:
- Branch (`feature/<name>`)
- Node modules
- Convex dev instance (if applicable)
- Port allocation

Work normally. Commit often. Push when ready for review.

```bash
git add .
git commit -m "description"
git push -u origin feature/<name>
```

## Stopping Work (End of Session)

```bash
# Stop servers but keep worktree (resume later)
zdev stop <feature-name> -p /path/to/project --keep

# Or just leave it running if you'll be back soon
```

## Resuming Work

```bash
# Check status
zdev list

# If stopped, restart
zdev start <feature-name> -p /path/to/project

# If already running, just cd to the worktree
cd ~/.zdev/worktrees/project-feature
```

## Presenting Output

When showing zdev output to users:
- **Never put URLs inside markdown tables or code blocks** — they won't be clickable
- Place URLs on their own line as plain text
- Use bold labels before URLs, not inline formatting

Example:
```
**Local:** http://localhost:5185
**Public:** https://project-feature.dev.example.com
```

NOT like this:
```
| Local | `http://localhost:5185` |  ← URLs not clickable!
```

## Creating a Pull Request

```bash
# Create PR with auto-generated title and preview URL
zdev pr -p /path/to/project

# Create PR with custom title
zdev pr -p /path/to/project --title "Add user authentication"

# Create draft PR
zdev pr -p /path/to/project --draft

# Open PR in browser instead of CLI
zdev pr -p /path/to/project --web
```

The PR body automatically includes the preview URL.

## After PR is Merged

```bash
# Clean up completely
zdev clean <feature-name> -p /path/to/project
```

This removes the worktree, Traefik route, and port allocation.

## Quick Reference

| Task | Command |
|------|---------|
| Create new project | `zdev create NAME` |
| Init existing project | `zdev init PATH` |
| Configure | `zdev config --list` |
| See what's running | `zdev list` |
| Start feature | `zdev start NAME -p PATH` |
| Create PR | `zdev pr -p PATH` |
| Stop (keep files) | `zdev stop NAME -p PATH --keep` |
| Stop (full) | `zdev stop NAME -p PATH` |
| Remove after merge | `zdev clean NAME -p PATH` |

## Troubleshooting

**"Feature already exists"** → It's already running. Use `zdev list` to find the worktree path.

**"Failed to create worktree: invalid reference"** → Use `--base-branch master` or the correct branch name.

**Port conflict** → Specify a port: `zdev start NAME --port 5200`

**No public URL** → Run `zdev config --set devDomain=dev.example.com` first.

**Convex not working** → Run `bunx convex dev` once in the main project first to select a Convex project.

**Vite "host not allowed" / 403 on preview URL** → `zdev start` auto-patches `vite.config.ts` with `server.allowedHosts` using the configured `devDomain`. If it didn't work: check `zdev config --list` has `devDomain` set, and that your vite config uses `defineConfig({})` or `export default {}`.
