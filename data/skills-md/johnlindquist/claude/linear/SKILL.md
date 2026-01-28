---
name: linear
description: Manage Linear issues and workflows. Use for viewing, creating, and updating Linear issues, and integrating with development workflow.
---

# Linear Issue Manager

Manage Linear issues using the `linearis` CLI.

## Prerequisites

Install linearis CLI:
```bash
bun add -g linearis
```

Set your API token:
```bash
export LINEAR_API_KEY=lin_api_xxxxx
```

Get your API key from: Linear Settings > API > Personal API keys

## CLI Reference

### List Issues

```bash
# List issues (default: 25)
linearis issues list

# Limit results
linearis issues list --limit 10
```

### Search Issues

```bash
# Search by query
linearis issues search "bug"

# Filter by team
linearis issues search "authentication" --team ENG

# Filter by assignee
linearis issues search "feature" --assignee user-id

# Filter by project
linearis issues search "api" --project "Backend"

# Filter by status
linearis issues search "bug" --status "In Progress,Todo"

# Combined filters with limit
linearis issues search "urgent" --team ENG --limit 5
```

### Get Issue Details

```bash
# Read issue by ID or identifier
linearis issues read ENG-123
linearis issues read abc123-uuid
```

### Create Issues

```bash
# Basic issue (requires team)
linearis issues create "Fix login bug" --team ENG

# With description
linearis issues create "Add OAuth support" --team ENG -d "Implement Google OAuth"

# With priority (1=Urgent, 2=High, 3=Medium, 4=Low)
linearis issues create "Critical fix" --team ENG -p 1

# With assignee
linearis issues create "Review code" --team ENG --assignee user-id

# With labels
linearis issues create "Security issue" --team ENG --labels "bug,security"

# With project
linearis issues create "New feature" --team ENG --project "Q1 Roadmap"

# With status
linearis issues create "Started task" --team ENG --status "In Progress"

# Full example
linearis issues create "Implement caching" \
  --team ENG \
  -d "Add Redis caching for API responses" \
  -p 2 \
  --labels "feature,performance" \
  --project "Backend" \
  --status "Todo"
```

### Update Issues

```bash
# Update title
linearis issues update ENG-123 -t "New title"

# Update description
linearis issues update ENG-123 -d "Updated description"

# Change status
linearis issues update ENG-123 -s "In Progress"
linearis issues update ENG-123 -s "Done"

# Change priority
linearis issues update ENG-123 -p 1

# Change assignee
linearis issues update ENG-123 --assignee user-id

# Add labels (default mode: adding)
linearis issues update ENG-123 --labels "urgent,blocked"

# Replace all labels
linearis issues update ENG-123 --labels "new-label" --label-by overwriting

# Clear all labels
linearis issues update ENG-123 --clear-labels

# Set parent issue
linearis issues update ENG-123 --parent-ticket ENG-100

# Clear parent
linearis issues update ENG-123 --clear-parent-ticket

# Set cycle
linearis issues update ENG-123 --cycle "Sprint 5"

# Clear cycle
linearis issues update ENG-123 --clear-cycle
```

### Comments

```bash
# Add comment to issue
linearis comments create ENG-123 --body "Working on this now"
```

### Teams

```bash
# List all teams
linearis teams list
```

### Labels

```bash
# List all labels
linearis labels list
```

### Projects

```bash
# List projects
linearis projects list
```

### Cycles

```bash
# List cycles
linearis cycles list
```

### Users

```bash
# List users
linearis users list
```

## Workflow Patterns

### Start Work on Issue

```bash
# 1. Find the issue
linearis issues search "feature name" --team ENG

# 2. Get details
linearis issues read ENG-123

# 3. Update status to In Progress
linearis issues update ENG-123 -s "In Progress"

# 4. Create branch (from issue identifier)
git checkout -b eng-123-feature-name
```

### Complete an Issue

```bash
# 1. Update status
linearis issues update ENG-123 -s "Done"

# 2. Add completion comment
linearis comments create ENG-123 --body "Completed in PR #456"
```

### Daily Standup View

```bash
# My in-progress issues
linearis issues search "assignee:me" --status "In Progress"

# Team's blocked issues
linearis issues search "" --team ENG --status "Blocked"
```

### Bug Triage

```bash
# Find unassigned bugs
linearis issues search "label:bug" --team ENG

# Assign and prioritize
linearis issues update ENG-456 --assignee user-id -p 1
```

## Git Integration

### Link Commits

Mention issue ID in commit message:
```bash
git commit -m "feat: implement caching

Fixes ENG-123"
```

### Create PR with Issue Link

```bash
ISSUE_ID="ENG-123"
gh pr create --title "feat: implement caching" --body "Closes $ISSUE_ID"
```

## Priority Values

| Value | Meaning |
|-------|---------|
| 0 | No priority |
| 1 | Urgent |
| 2 | High |
| 3 | Medium |
| 4 | Low |

## Best Practices

1. **Use issue IDs** - Reference ENG-123 in commits/PRs
2. **Update status** - Move issues through workflow with `linearis issues update`
3. **Add comments** - Track progress with `linearis comments create`
4. **Use labels** - Categorize for filtering
5. **Link PRs** - Connect code to issues
6. **Search effectively** - Combine filters for precise results
