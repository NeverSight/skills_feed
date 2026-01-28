---
name: bd
description: Git-native issue tracking with first-class dependency support. Issues stored alongside code in .beads/ directory, dual-persisted in SQLite (queries) and JSONL (git-friendly history). Hash-based IDs, DAG dependencies, daemon mode with RPC, and LSP-inspired multi-workspace support.
version: 0.28.0
triggers:
  - task tracking
  - issue management
  - project planning
  - bug triage
  - dependency modeling
  - git-integrated workflows
  - sprint planning
  - epic decomposition
  - work prioritization
  - ai agent task execution
capabilities:
  - create_issues
  - update_issues
  - dependency_management
  - git_sync
  - daemon_rpc
  - visualization
  - multi_repo
  - label_management
  - comment_system
  - search_filter
related_tools:
  - git (version control)
  - bv (issue graph visualization)
  - sqlite3 (database queries)
  - jq (json processing)
  - graphviz (dependency graphs)
---

# bd - Git-Native Issue Tracking

## Core Principle

**Use bd for all task and issue operations—it's git-native and agent-friendly.**

Issues live where your code lives: in git. No external API, no network dependency, no vendor lock-in. Just files, tracked by git, queryable via SQLite, and optimized for AI agent workflows.

## When to Use bd

### Primary Use Cases

1. **Task Tracking**: Create, update, close issues for any work item
2. **Issue Management**: Organize bugs, features, chores with labels and priorities
3. **Project Planning**: Break down epics into subtasks with dependencies
4. **Dependency Modeling**: Express work relationships as a DAG
5. **Sprint Planning**: Assign work, set priorities, track progress
6. **Bug Triage**: Classify, assign, and track defects
7. **AI Agent Workflows**: Autonomous task execution with dependency awareness

### When NOT to Use bd

- Public issue tracking (use GitHub Issues for public visibility)
- Customer-facing support tickets (use dedicated support systems)
- Marketing/sales workflows (use CRM tools)
- Document management (use proper DMS)

## Quick Start

### Installation Check

```bash
# Verify bd is installed
which bd
# Expected: /opt/homebrew/bin/bd (or similar)

bd --version
# Expected: bd version 0.28.0+
```

### Initialize in Repository

```bash
# Initialize bd in current git repo
bd init

# Configure project-specific prefix (optional)
bd config set prefix myapp

# Verify setup
bd status
```

### Basic Operations

```bash
# Create an issue
bd create "Add user authentication"

# Create with metadata
bd create "Fix login bug" \
  --type bug \
  --priority 1 \
  --assignee alice \
  --labels backend,security

# List issues
bd list
bd list --status open --assignee alice
bd list --label urgent --priority-min 0 --priority-max 1

# Update issue
bd update bd-1 --status in_progress
bd update bd-1 --priority 0
bd update bd-1 --assignee bob

# Add comment
bd comment bd-1 "Started investigating root cause"

# Close issue
bd close bd-1

# Show details
bd show bd-1
bd show bd-1 --json  # Structured output for parsing
```

## Core Concepts

### Issue Structure

Every issue has:

- **ID**: Hash-based (e.g., `bd-a3f8e9`) or sequential (legacy)
- **Title**: Brief summary (required)
- **Description**: Detailed explanation (markdown)
- **Type**: bug | feature | task | epic | chore
- **Status**: open | in_progress | blocked | closed
- **Priority**: 0-4 (0=highest, 4=lowest)
- **Assignee**: Username or actor
- **Labels**: Tags for organization
- **Dependencies**: Relationships to other issues
- **Timestamps**: created_at, updated_at, closed_at

### Dual Persistence

bd uses TWO storage formats:

1. **SQLite** (`.beads/*.db`)
   - Fast queries and filtering
   - Full-text search
   - Indexed relationships
   - Ephemeral: rebuilds from JSONL

2. **JSONL** (`.beads/beads.jsonl`)
   - Git-friendly line-by-line format
   - Complete audit history
   - Source of truth for sync
   - Human-readable events

**Key insight:** SQLite is for speed, JSONL is for git. Changes are written to both automatically.

### Dependency DAG

Issues form a **Directed Acyclic Graph** (no cycles allowed):

```
bd-1 (Design) → bd-2 (Backend) → bd-3 (Frontend) → bd-4 (Tests)
```

**Dependency types:**
- `blocks` / `blocked_by`: Hard dependencies
- `discovered-from`: Context tracking
- `parent` / `child`: Hierarchical relationships

**Why DAG?**
- Prevents deadlocks (no circular dependencies)
- Enables critical path analysis
- Clear work ordering
- Parallel work identification

### Issue Lifecycle

```
┌─────────────────────────────────────────┐
│                                         │
│  open ──> in_progress ──> closed       │
│    │            │                       │
│    └────> blocked                       │
│              │                          │
│              └──> in_progress           │
│                                         │
│  closed ──> reopen ──> open             │
│                                         │
└─────────────────────────────────────────┘
```

## Common Workflows

### Daily Developer Workflow

```bash
# Morning: Review work
git pull                              # Sync issues from team
bd ready                              # Show unblocked work
bd list --assignee $USER              # Your assigned issues

# During work: Update status
bd update bd-5 --status in_progress   # Start work
bd comment bd-5 "Implementing JWT"    # Progress notes

# Found a bug? Create it
bd create "Fix null pointer in auth" \
  --type bug \
  --priority 1 \
  --deps discovered-from:bd-5

# End of day: Sync
git add .beads/
git commit -m "Progress on bd-5"
git push
```

### Epic Decomposition

```bash
# 1. Create epic
bd create "Redesign authentication" \
  --type epic \
  --priority 0

EPIC_ID="bd-1"  # Replace with actual ID

# 2. Create subtasks
bd create "Design auth schema" --parent $EPIC_ID --priority 0
bd create "Implement backend" --parent $EPIC_ID --deps bd-2
bd create "Update frontend" --parent $EPIC_ID --deps bd-3
bd create "Write tests" --parent $EPIC_ID --deps bd-3,bd-4

# 3. Visualize plan
bd dep tree $EPIC_ID --long
```

### Sprint Planning

```bash
# 1. Review backlog
bd list --status open --no-assignee --sort priority

# 2. Assign sprint work
bd update bd-10,bd-11,bd-12 --assignee alice
bd label add sprint-5 bd-10,bd-11,bd-12

# 3. Set priorities
bd update bd-10,bd-11 --priority 0  # Critical

# 4. Review sprint
bd list --label sprint-5 --long
```

### Bug Triage

```bash
# 1. Create bug with full context
bd create "Login fails with special chars" \
  --type bug \
  --priority 2 \
  --description "Steps: 1) Use p@ss\$word! 2) Try login 3) Fails" \
  --labels backend,security

# 2. Assign and track
bd update bd-20 --assignee backend-team --status in_progress

# 3. Add investigation notes
bd update bd-20 --notes "Root cause: encoding issue in auth/password.go"

# 4. Close when fixed
bd close bd-20
```

## Dependency Management

### Adding Dependencies

```bash
# Single dependency
bd dep add bd-1 blocks bd-2

# Multiple at creation
bd create "New feature" --deps bd-1,bd-2,bd-3

# Explicit types
bd create "Bug fix" --deps discovered-from:bd-5,blocks:bd-10

# Hierarchical
bd create "Subtask" --parent bd-1
```

### Viewing Dependencies

```bash
# Dependency tree
bd dep tree bd-1

# All blocked issues
bd blocked

# All ready work (no blockers)
bd ready

# Export as graph
bd list --format dot | dot -Tpng -o issues.png
bd list --format digraph > issues.txt
```

### Removing Dependencies

```bash
# Remove specific dependency
bd dep remove bd-1 blocks bd-2
```

### Cycle Detection

```bash
# Find cycles (deadlocks)
bd dep cycles

# Output example:
# Cycle detected: bd-5 -> bd-7 -> bd-9 -> bd-5
```

## Advanced Features

### Daemon Mode

Long-running RPC server for hot database and multi-workspace:

```bash
# Start daemon (auto-started by default)
bd daemon start

# Check status
bd daemon status

# Stop daemon
bd daemon stop

# Force direct mode (bypass daemon)
bd --no-daemon list
```

**Benefits:**
- <10ms create/update operations (vs ~100ms direct)
- Hot SQLite cache
- Multi-workspace support
- Background sync
- JSON-RPC protocol

### Templates

```bash
# Create template
bd template create bug-report \
  --type bug \
  --priority 2 \
  --description "## Steps to Reproduce\n\n## Expected\n\n## Actual"

# Use template
bd create "New bug" --from-template bug-report
```

### Labels

```bash
# Add labels
bd label add urgent bd-5
bd label add backend,security bd-5

# Remove labels
bd label remove urgent bd-5

# Query by labels
bd list --label backend         # AND: must have ALL
bd list --label-any urgent,high # OR: must have AT LEAST ONE
```

### Search & Filtering

```bash
# Text search
bd search "authentication"

# Filter by multiple criteria
bd list \
  --status open,in_progress \
  --priority-min 0 --priority-max 1 \
  --assignee alice \
  --label backend \
  --created-after 2024-01-01 \
  --sort priority \
  --reverse

# Empty description (needs work)
bd list --empty-description

# No assignee (needs owner)
bd list --no-assignee --status open
```

### Comments

```bash
# Add comment
bd comment bd-5 "Started implementation"
bd comment bd-5 --body "Multi-line comment"

# View comments
bd comments list bd-5

# Add inline (via update)
bd update bd-5 --notes "Design notes here"
```

### Export/Import

```bash
# Export to JSONL
bd export > backup.jsonl
bd export --status closed --created-after 2024-01-01 > archive.jsonl

# Import from JSONL
bd import backup.jsonl

# Migrate between repos
bd migrate-issues --from ~/old-repo --to ~/new-repo
```

### Multi-Repository

```bash
# Configure multiple repos
bd repo add backend ~/repos/backend --prefix api
bd repo add frontend ~/repos/frontend --prefix ui

# Create in specific repo
bd create "Add endpoint" --repo backend

# Auto-routing (based on cwd)
cd ~/repos/backend
bd create "Add endpoint"  # Automatically creates in backend repo
```

## Git Integration

### Automatic Sync

```bash
# bd auto-syncs with JSONL on operations
bd create "New issue"
# Writes to SQLite AND .beads/beads.jsonl

git add .beads/
git commit -m "Add issue"
git push
```

### Git Hooks

```bash
# Install hooks for auto-sync
bd hooks install

# Hooks added:
# pre-commit: Validate issue references in commits
# post-commit: Auto-export to JSONL
```

### Manual Sync

```bash
# Pull from remote
git pull  # Merges .beads/beads.jsonl

# Push to remote
git add .beads/
git commit -m "Update issues"
git push

# Or use bd sync
bd sync pull
bd sync push
```

### Merge Conflicts

bd includes custom merge driver:

```bash
# .gitattributes (auto-configured by bd init)
.beads/beads.jsonl merge=beads

# Conflicts are resolved by:
# 1. Preserving both changes in JSONL
# 2. Rebuilding SQLite from merged JSONL
# 3. Detecting cycles if any
```

## Visualization

### bv (Interactive Graph)

```bash
# Open interactive visualization
bv .beads/beads.jsonl

# Features:
# - Colored nodes by status
# - Dependency edges with types
# - Filter by labels, status, assignee
# - Click nodes for details
# - Export as PNG/SVG
```

### Graphviz

```bash
# Generate DOT format
bd list --format dot > issues.dot

# Render with Graphviz
dot -Tpng -o issues.png issues.dot
dot -Tsvg -o issues.svg issues.dot

# Customize layout
neato -Tpng -o issues-neato.png issues.dot  # Force-directed
circo -Tpng -o issues-circo.png issues.dot  # Circular
```

### Text-Based Tree

```bash
# ASCII dependency tree
bd dep tree bd-1

# Long format (more details)
bd dep tree bd-1 --long
```

## Health & Maintenance

### Validation

```bash
# Full database health check
bd validate

# Check for issues:
# - Orphaned dependencies
# - Cycles in DAG
# - Corrupted records
# - JSONL/SQLite inconsistencies
```

### Doctor

```bash
# Comprehensive health check
bd doctor

# Checks:
# - Installation integrity
# - Database schema
# - Config validity
# - Git integration
# - Daemon status
```

### Repair

```bash
# Fix orphaned dependencies
bd repair-deps
bd repair-deps --dry-run  # Preview only

# Detect and clean test pollution
bd detect-pollution
bd detect-pollution --clean

# Find and merge duplicates
bd duplicates
bd duplicates --auto-merge
```

### Cleanup

```bash
# Compact old closed issues (save space, keep git history)
bd compact --older-than 90d

# Delete closed issues from DB (keep in JSONL for sync)
bd cleanup --older-than 30d

# Purge deleted issues entirely (careful!)
bd delete bd-1 --purge  # Removes from JSONL too
```

## AI Agent Workflows

### Autonomous Task Loop

```bash
#!/bin/bash
# agent-work-loop.sh

while true; do
  # Get ready work
  READY=$(bd ready --json --assignee agent)

  if [ "$READY" = "[]" ]; then
    sleep 60
    continue
  fi

  # Pick highest priority
  ISSUE_ID=$(echo $READY | jq -r '.[0].id')

  # Mark in progress
  bd update $ISSUE_ID --status in_progress

  # Execute work (agent-specific)
  agent-execute $ISSUE_ID

  # Mark complete
  bd close $ISSUE_ID

  # Sync
  git add .beads/
  git commit -m "Completed $ISSUE_ID"
  git push
done
```

### Context-Aware Creation

```bash
#!/bin/bash
# agent-discover-issues.sh

# Find TODOs in code
rg "TODO:" --json | jq -c '.[] | select(.type == "match")' | \
while read line; do
  FILE=$(echo $line | jq -r '.data.path.text')
  TEXT=$(echo $line | jq -r '.data.lines.text' | sed 's/.*TODO: //')

  bd create "$TEXT" \
    --type task \
    --priority 2 \
    --description "Found in $FILE" \
    --labels auto-generated
done
```

### Dependency-Aware Planning

```bash
#!/bin/bash
# agent-plan-work.sh

# Build dependency graph
GRAPH=$(bd list --format digraph)

# Compute work order (topological sort)
echo "$GRAPH" | golang.org/x/tools/cmd/digraph allpaths | \
while read path; do
  echo "Execution order: $path"
done
```

## JSON Output & Parsing

### Structured Output

```bash
# Get JSON output (all commands support --json)
bd list --json
bd show bd-1 --json
bd ready --json
bd blocked --json
```

### Example Parsing

```bash
# Get all high-priority open issues
bd list --status open --json | \
  jq '.[] | select(.priority <= 1) | {id, title, priority}'

# Find issues with no assignee
bd list --json | \
  jq '.[] | select(.assignee == null or .assignee == "") | .id'

# Count issues by status
bd list --json | \
  jq 'group_by(.status) | map({status: .[0].status, count: length})'

# Extract dependency graph
bd list --json | \
  jq '.[] | {id, blocks: [.dependencies[] | select(.type=="blocks") | .target_id]}'
```

## JSONL Direct Access

### Reading JSONL

For direct file access (e.g., in agent scripts):

```bash
# Read all events
cat .beads/beads.jsonl | jq -c '.'

# Filter by event type
cat .beads/beads.jsonl | jq -c 'select(.type == "create")'

# Get latest issue state
cat .beads/beads.jsonl | \
  jq -c 'select(.type == "create" or .type == "update")' | \
  jq -s 'group_by(.issue.id) | map(sort_by(.issue.updated_at) | last | .issue)'
```

### JSONL Event Types

```jsonl
{"type":"create","issue":{...}}
{"type":"update","issue":{...}}
{"type":"close","id":"bd-1","closed_at":"...","actor":"..."}
{"type":"reopen","id":"bd-1","actor":"..."}
{"type":"delete","id":"bd-1","deleted_at":"...","actor":"..."}
{"type":"comment","comment":{...}}
{"type":"dep_add","dependency":{...}}
{"type":"dep_remove","dependency":{...}}
```

## Configuration

### Config Commands

```bash
# View current config
bd config list

# Set values
bd config set prefix myapp
bd config set default_priority 2
bd config set default_type task

# Git settings
bd config set git.auto_sync true
bd config set git.remote origin
bd config set git.sync_branch main

# Daemon settings
bd config set daemon.enabled true
bd config set daemon.sync_interval 300
```

### Config File

Location: `.beads/config.json` (per-repo) or `~/.config/bd/config.json` (global)

```json
{
  "prefix": "myapp",
  "default_priority": 2,
  "default_type": "task",
  "daemon": {
    "enabled": true,
    "port": 9876,
    "sync_interval": 300
  },
  "git": {
    "auto_sync": true,
    "sync_branch": "main",
    "remote": "origin"
  },
  "repos": {
    "backend": {
      "path": "/Users/user/repos/backend",
      "prefix": "api",
      "auto_route": true
    },
    "frontend": {
      "path": "/Users/user/repos/frontend",
      "prefix": "ui",
      "auto_route": true
    }
  }
}
```

## Statistics & Reporting

```bash
# Overall stats
bd stats

# Count issues
bd count
bd count --status open
bd count --label urgent

# Stale issues
bd stale --older-than 30d

# Export stats
bd list --json | \
  jq '{
    total: length,
    by_status: group_by(.status) | map({(.[0].status): length}) | add,
    by_type: group_by(.type) | map({(.[0].type): length}) | add,
    by_priority: group_by(.priority) | map({("\(.priority)"): length}) | add
  }'
```

## Global Flags

```bash
--json              # JSON output for all commands
--db <path>         # Specify database path
--no-daemon         # Force direct mode (bypass daemon)
--no-db             # JSONL-only mode (no SQLite)
--no-auto-flush     # Disable auto-sync to JSONL
--no-auto-import    # Disable auto-import from JSONL
--sandbox           # Sandbox mode (no daemon, no auto-sync)
--quiet             # Suppress output
--verbose           # Debug output
--actor <name>      # Override actor name (audit trail)
--allow-stale       # Skip staleness check
```

## Best Practices

### 1. Commit Issues with Code

```bash
git checkout -b feature/new-auth
bd create "Implement new auth" --type feature
# ... write code ...
bd update bd-1 --status in_progress
git add .
git commit -m "Implement new auth (bd-1)"
bd close bd-1
git add .beads/
git commit -m "Close bd-1"
git push
```

### 2. Use Dependencies Liberally

Model real work dependencies—it unlocks:
- Critical path analysis
- Parallel work identification
- Automatic ready/blocked tracking

### 3. Label Consistently

Establish taxonomy early:
- `backend`, `frontend`, `infra`
- `urgent`, `high`, `medium`, `low`
- `sprint-N` for sprint tracking
- `tech-debt`, `security`, `performance`

### 4. Comment Frequently

Context decays over time. Comments preserve:
- Why decisions were made
- What was tried and failed
- Links to resources
- Status updates

### 5. Sync Daily

```bash
# Pull in morning
git pull

# Push at end of day
git add .beads/
git commit -m "Daily issue updates"
git push
```

### 6. Clean Up Regularly

```bash
# Weekly: review stale issues
bd stale --older-than 30d

# Monthly: compact old closed issues
bd compact --older-than 90d

# Quarterly: cleanup deleted issues
bd cleanup --older-than 90d
```

### 7. Validate Health

```bash
# Weekly: run validation
bd validate

# Fix issues immediately
bd repair-deps
bd dep cycles
```

## Troubleshooting

### Issues Not Appearing

```bash
# Check database exists
ls -la .beads/

# Validate JSONL
cat .beads/beads.jsonl | jq '.' > /dev/null

# Rebuild SQLite from JSONL
bd migrate
```

### Daemon Not Starting

```bash
# Check daemon status
bd daemon status

# View logs
bd daemon logs

# Stop and restart
bd daemon stop
bd daemon start
```

### Merge Conflicts

```bash
# After git pull with conflicts in .beads/beads.jsonl
git status

# bd's merge driver should handle automatically
# If not, rebuild from JSONL
rm .beads/*.db
bd migrate

# Validate
bd validate
```

### Performance Issues

```bash
# Use daemon mode (default)
bd daemon status

# Compact old issues
bd compact --older-than 90d

# Check database size
du -sh .beads/

# Profile operations
bd --profile list
```

## Related Tools

- **git**: Version control (bd integrates natively)
- **bv**: Interactive graph visualization for bd issues
- **sqlite3**: Direct database queries if needed
- **jq**: JSON processing for structured output
- **graphviz**: Render dependency graphs (dot, neato, circo)
- **rg** (ripgrep): Fast text search in issues
- **fd**: Fast file search for bd files

## References

For complete details, see:

1. **Type Definitions**: `@bd-codebase/types/core.ts`
2. **Git-Native Principles**: `@bd-codebase/principles/git-native.md`
3. **DAG Dependencies**: `@bd-codebase/principles/dag-dependencies.md`
4. **Task Workflows**: `@bd-codebase/templates/task-workflow.md`
5. **Codebase README**: `@bd-codebase/README.md`

## Quick Reference

See [`assets/cheatsheet.md`](assets/cheatsheet.md) for one-page reference.

---

**Remember:** bd is designed to work *like git* because it *is git*. Think of issues as files, operations as commits, and sync as push/pull. It's that simple.
