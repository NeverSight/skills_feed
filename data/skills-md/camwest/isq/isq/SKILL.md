---
name: isq
description: Use the isq CLI for instant, offline-first GitHub, Linear, and JIRA issue management. Use this skill when the user wants to list issues, create issues, comment on issues, start working on an issue (creates git worktree), manage goals (milestones/projects), sync repositories, or work with issues offline. isq provides sub-millisecond reads from a local SQLite cache and integrates with git worktrees for seamless development workflows.
---

# isq CLI

A CLI for GitHub, Linear, and JIRA issues. Instant. Offline-first.

## Prerequisites

The `isq` command must be installed and available in PATH. Install via:

**macOS / Linux:**
```bash
curl -LsSf https://cameronwestland.com/isq/install.sh | sh
```

**Windows (PowerShell):**
```powershell
irm https://cameronwestland.com/isq/install.ps1 | iex
```

## Why isq is Fast

isq syncs issues to a local SQLite database. All reads come from this cache—no network round-trip. A background daemon keeps the cache fresh automatically.

```
CLI reads → Local SQLite (instant, <1ms)
CLI writes → API directly (then cached)
Daemon → Syncs in background every 15s
```

## Core Commands

### Link a Repository

Before using isq, link your repo to GitHub, Linear, or JIRA:

```bash
isq link github    # Link current repo to GitHub Issues
isq link linear    # Link current repo to Linear
isq link jira      # Link current repo to JIRA Cloud
```

For JIRA, you can also use options to select a specific project:

```bash
isq link jira -o list-projects   # List available JIRA projects
isq link jira -o project=MYPROJ  # Link to specific project
```

Linking also installs a git commit hook that auto-appends issue references to commits.

### Sync Issues

Manually sync issues from the remote:

```bash
isq sync
```

The daemon also syncs automatically in the background.

### List Issues

```bash
isq issue list                          # All issues (sorted by priority)
isq issue list --state=open             # Open issues only
isq issue list --state=closed           # Closed issues only
isq issue list --label=bug              # Filter by label
isq issue list --mine                   # Issues assigned to me
isq issue list --unassigned             # Issues with no assignee
isq issue list --goal "v1"              # Issues in a goal/milestone
isq issue list --id 7,12,45             # Filter by specific issue IDs
isq issue list --sort newest            # Sort by issue number (newest first)
isq issue list --sort updated           # Sort by last updated
isq issue list --label=bug --state=open # Combine filters
isq issue list --json                   # JSON output
isq issue list --tree                   # Show as parent-child hierarchy
isq issue list --root-only              # Only top-level issues (no parents)
isq issue list --children-of 42         # Children of issue #42 for scripts
```

**Note:** `--id` gives a compact list view of specific issues. Use `isq issue show <id>` for full details including description and comments.

### Show Issue Details

```bash
isq issue show 423        # Show issue #423
isq issue show 423 --json # JSON output
```

### Create Issues

```bash
isq issue create --title "Fix login bug"
isq issue create --title "Add feature" --body "Description here"
isq issue create --title "Bug" --label=bug
```

### Comment on Issues

```bash
isq issue comment 423 "Fixed in commit abc123"
```

### Close and Reopen

```bash
isq issue close 423
isq issue reopen 423
```

### Manage Labels

```bash
isq issue label 423 add bug
isq issue label 423 remove bug
```

### Assign Users

```bash
isq issue assign 423 username
```

### Label Commands

List and create repository labels (for discovery and priority setup):

```bash
isq label list                              # List all repo labels
isq label list --json                       # JSON output
isq label create P0 --color ff0000          # Create a label
isq label create P1 --color orange --description "High priority"
```

## Development Workflow

isq integrates with git worktrees so your filesystem becomes your context. Each worktree is associated with an issue—no need to track issue IDs manually.

### Start Working on an Issue

```bash
isq start 891
```

This command:
1. Creates a git worktree at `~/src/myapp-891-fix-auth-timeout`
2. Creates a branch named `891-fix-auth-timeout`
3. Marks the issue as in-progress (adds labels on GitHub, transitions state on Linear)
4. Runs any setup script defined in `.config/isq.toml`

### Show Current Issue

```bash
isq              # Show current issue with full details
isq current      # Just the issue number (for scripts)
isq current -q   # Quiet mode: no output if no issue, exit code 1
```

When in a worktree, `isq` (no args) shows the associated issue:

```
#891 Auth timeout on slow connections                        open
───────────────────────────────────────────────────────────────────
Connections time out after 30s on slow networks...

Branch: 891-fix-auth-timeout
Worktree: ~/src/myapp-891-fix-auth-timeout
```

### Automatic Commit References

When you commit in a worktree with an associated issue, the commit message automatically gets the issue reference appended:

```bash
git commit -m "Fix connection pool sizing"
# Becomes: "Fix connection pool sizing [#891]"
```

### Clean Up

When done with an issue (PR merged, etc.):

```bash
isq cleanup         # Remove worktree, clear association, and clean up issue state
isq cleanup --keep  # Keep worktree directory, just clear association
```

Cleanup undoes what `isq start` did:
- **GitHub**: Removes labels added on start (e.g., "in progress")
- **Linear/JIRA**: Can transition issue back to a state (e.g., "backlog")

Configure in `.config/isq.toml`:

```toml
[on_cleanup]
remove_labels = ["in progress"]  # GitHub
# transition = "backlog"         # Linear/JIRA
```

## Goal Commands

Goals are time-bound containers for issues. They map to GitHub Milestones and Linear Projects.

### List Goals

```bash
isq goal list                 # Open goals (default)
isq goal list --state=closed  # Closed goals
isq goal list --state=all     # All goals
isq goal list --json          # JSON output
```

### Show Goal Details

```bash
isq goal show "v1"        # Show goal by name
isq goal show "v1" --json # JSON output
```

### Create Goals

```bash
isq goal create "v1"
isq goal create "v1" --target 2026-02-01
isq goal create "v1" --target 2026-02-01 --body "First public release"
```

### Assign Issues to Goals

```bash
isq goal assign 423 "v1"  # Assign issue #423 to goal "v1"
```

### Close Goals

```bash
isq goal close "v1"
```

## Daemon Commands

The daemon syncs issues in the background and enables instant reads.

```bash
isq daemon start    # Start the background daemon
isq daemon stop     # Stop the daemon
isq daemon status   # Check daemon status and watched repos
```

## Diagnostics and Updates

```bash
isq doctor            # Diagnose common issues and suggest fixes
isq doctor --verbose  # Show detailed diagnostics
isq doctor --check auth  # Run specific check (auth, repo, sync, service, database, network)

isq update check      # Check if a newer version is available
isq update install    # Download and install the latest version
```

## Other Commands

```bash
isq status        # Show auth, sync health, and daemon status
isq unlink        # Remove link and commit hook from current repo
isq logout github # Remove stored credentials for a forge
```

## Offline Support

When offline, write operations queue locally and sync when back online:

```bash
# Works offline - queues the operation
isq issue create --title "New issue"
# Output: ✓ Queued: New issue (offline, 8ms)

# When back online, daemon syncs automatically
isq daemon status
# Output: ✓ Synced 2 pending operations
```

## JSON Output

All commands support `--json` for machine-readable output. Use this for scripts and AI agent workflows:

```bash
isq issue list --json
isq issue show 423 --json
isq issue create --title "Bug" --json
isq status --json
```

## Views (Saved Filters)

Views are named filter combinations that save you from typing repetitive flags. They're stored in your user config (`~/.config/isq/config.toml`) and work across all repositories.

### Create a View

```bash
# Create a view for high-priority bugs assigned to me
isq view create my-bugs --label=bug --state=open --mine --priority-lte=2

# Create a view for stale unassigned issues
isq view create stale --unassigned --updated-before="30 days"

# Create a view for backlog triage
isq view create triage --state=open --unassigned --label-not=wontfix
```

### Use a View

Reference views with `@` prefix in issue list:

```bash
isq issue list @my-bugs      # Expands to: --label=bug --state=open --mine --priority-lte=2
isq issue list @stale        # Expands to: --unassigned --updated-before="30 days"
isq issue list @triage       # Expands to: --state=open --unassigned --label-not=wontfix
```

Views can be combined with additional flags (CLI flags override view settings):

```bash
isq issue list @my-bugs --label=security  # Overrides label from view
isq issue list @triage --json             # Adds json output
```

### Manage Views

```bash
isq view list             # List all views
isq view show my-bugs     # Show view details
isq view delete stale     # Delete a view
```

### Available View Filters

| Flag | Description | Example |
|------|-------------|---------|
| `--label` | Include issues with this label | `--label=bug` |
| `--label-not` | Exclude issues with this label | `--label-not=wontfix` |
| `--label-any` | Include issues with any of these labels (comma-separated) | `--label-any=bug,security` |
| `--state` | Filter by state | `--state=open` |
| `--mine` | Issues assigned to me | `--mine` |
| `--unassigned` | Issues with no assignee | `--unassigned` |
| `--goal` | Issues in a goal/milestone | `--goal="v1"` |
| `--priority` | Exact priority match | `--priority=1` |
| `--priority-lte` | Priority ≤ value (0=urgent, 1=high, ...) | `--priority-lte=2` |
| `--priority-gte` | Priority ≥ value | `--priority-gte=2` |
| `--updated-before` | Not updated in duration | `--updated-before="30 days"` |
| `--updated-after` | Updated within duration | `--updated-after="7 days"` |
| `--created-before` | Created before duration | `--created-before="90 days"` |
| `--created-after` | Created within duration | `--created-after="7 days"` |
| `--sort` | Sort order | `--sort=updated` |

### User Defaults

You can also set default JSON output mode in your config:

```toml
# ~/.config/isq/config.toml
[defaults]
json = true    # All commands output JSON by default
```

## Command Reference

| Command | Description |
|---------|-------------|
| `isq link <github\|linear\|jira>` | Link repo to backend, install commit hook |
| `isq unlink` | Remove link and commit hook |
| `isq logout <forge>` | Remove stored credentials from keychain |
| `isq status` | Show auth, sync health, and daemon status |
| `isq doctor` | Diagnose common issues and suggest fixes (--verbose, --check) |
| `isq sync` | Manually sync issues and goals |
| `isq update check` | Check if a newer version is available |
| `isq update install` | Download and install the latest version |
| `isq start <id>` | Create worktree, branch, mark issue in-progress |
| `isq current` | Show current issue number (-q for scripts) |
| `isq cleanup` | Remove worktree, clear association, clean up issue state (--keep to preserve) |
| `isq issue list` | List issues (--label, --state, --mine, --tree, --root-only, --children-of, --json) |
| `isq issue list --id 7,12` | Filter to specific issue IDs (compact view) |
| `isq issue list --mine` | Show only issues assigned to me |
| `isq issue list --unassigned` | Show only unassigned issues |
| `isq issue list --goal "X"` | Filter to issues in goal/milestone X |
| `isq issue list --sort priority` | Sort by priority (default) |
| `isq issue list --sort newest` | Sort by issue number (newest first) |
| `isq issue list --sort updated` | Sort by last updated |
| `isq issue list --tree` | Display as hierarchical tree (indented by parent-child) |
| `isq issue list --root-only` | Show only root issues (no parent) |
| `isq issue list --children-of 42` | Show only children of issue #42 |
| `isq issue show <id>` | Show issue details |
| `isq issue create --title "..."` | Create new issue |
| `isq issue comment <id> "..."` | Add comment |
| `isq issue close <id>` | Close issue |
| `isq issue reopen <id>` | Reopen issue |
| `isq issue label <id> add\|remove <label>` | Manage labels on an issue |
| `isq issue assign <id> <user>` | Assign user |
| `isq label list` | List all labels in the repository |
| `isq label create <name>` | Create a label (--color, --description) |
| `isq goal list` | List goals (--state, --json) |
| `isq goal show <name>` | Show goal details |
| `isq goal create <name>` | Create goal (--target, --body) |
| `isq goal assign <issue> <goal>` | Assign issue to goal |
| `isq goal close <name>` | Close goal |
| `isq view create <name>` | Create a view (--label, --state, --mine, --priority-lte, etc.) |
| `isq view list` | List all views |
| `isq view show <name>` | Show view details |
| `isq view delete <name>` | Delete a view |
| `isq issue list @<view>` | Use a view in issue list |
| `isq daemon start` | Start background daemon |
| `isq daemon stop` | Stop daemon |
| `isq daemon status` | Check daemon status |

## Guidance

- **Prefer the CLI** for all issue operations rather than calling GitHub/Linear APIs directly
- **Use `isq start`** when beginning work on an issue—it sets up the worktree and tracks context automatically
- **NEVER manually create branches with `git checkout -b` when starting issue work**—always use `isq start <id>` instead, then `cd` into the created worktree
- **NEVER remove or clean up worktrees created by `isq start`**—they are the intended working environment
- **Use `--json`** when you need structured output for further processing
- **Reads are instant** because they come from the local cache—no need to worry about API rate limits for queries
- **Writes go directly to the API** when online, or queue locally when offline
- **The daemon is optional** but recommended—it keeps the cache fresh automatically

## Common Workflows

### Initial Setup
```bash
cd /path/to/your/repo
isq link github      # or: isq link linear, isq link jira
isq sync             # Initial sync
isq daemon start     # Start background sync
```

### Feature Development
```bash
# Find an issue to work on
isq issue list --state=open --label=feature

# Start working (creates worktree, branch, marks in-progress)
isq start 891

# Work on the feature...
# Commits auto-reference the issue: "Add feature [#891]"

# When done, clean up
isq cleanup
```

### Daily Issue Triage
```bash
isq issue list --state=open --label=bug
isq issue show 423
isq issue comment 423 "Looking into this"
isq issue close 423
```

### Working Offline
```bash
# On a plane, no internet
isq issue list                    # Works! Reads from cache
isq issue create --title "Idea"   # Queues locally

# Back online
isq daemon status                 # Shows pending ops synced
```

## Finding What to Work On

When users ask "what should I work on?" or similar, use these patterns.

### Understanding Priority

Issues have priority levels (shown in JSON output):
- `0` / `urgent` — Drop everything, fix now
- `1` / `high` — Important, do soon
- `2` / `medium` — Normal priority
- `3` / `low` — Nice to have
- `4` / `none` — No priority set

Issues are sorted by priority by default. Always recommend highest priority first.

**Linear:** Priority is native (works out of box).

**GitHub:** Priority requires explicit `[priority]` config in `.config/isq.toml`:

```toml
[priority]
P0 = 0  # urgent
P1 = 1  # high
bug = 1 # treat bugs as high priority
P2 = 2  # medium
P3 = 3  # low
```

### Pre-assigned Teams

If issues are assigned during sprint planning, find the user's top priority work:

```bash
isq issue list --mine --json
```

Recommend the highest priority assigned issue.

### Pull-from-Backlog Teams

If the team pulls from a shared backlog:

```bash
isq issue list --goal "Sprint 5" --unassigned --json
```

Recommend the highest priority unassigned issue, then assign and start:

```bash
isq issue assign 42 username
isq start 42
```

### Not Sure Which Model?

Ask: "Does your team pre-assign issues, or do you pull from a shared backlog?"

### Example Workflow: "What Should I Work On?"

```bash
# Pre-assigned model
isq issue list --mine --json
# Look at top result (highest priority)
# Recommend it to user
isq start <id>

# Pull model
isq issue list --goal "Current Sprint" --unassigned --json
# Look at top result
# Recommend it, then:
isq issue assign <id> <username>
isq start <id>
```

### Setting Up Priority (GitHub)

If priority labels aren't configured for a GitHub repo:

1. Check existing labels: `isq label list`
2. Either map existing labels to priorities in `.config/isq.toml`
3. Or create priority labels: `isq label create P0 --color ff0000`

Example configuration:

```toml
# .config/isq.toml
[priority]
P0 = 0
P1 = 1
bug = 1
P2 = 2
P3 = 3
```

## Troubleshooting

### General Diagnosis
```bash
isq doctor            # Check auth, repo, sync, service, database, network
isq doctor --verbose  # Show detailed diagnostics
```

### Daemon Not Starting
```bash
isq daemon status
# If stuck on macOS:
launchctl stop com.isq.daemon
isq daemon start
```

### Stale Cache
```bash
isq sync    # Force manual sync
```

### Check What's Linked
```bash
isq status
```
