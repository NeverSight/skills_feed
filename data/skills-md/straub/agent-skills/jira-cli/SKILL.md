---
name: jira-cli
description: Interact with Jira using the jira-cli command-line tool to manage issues, sprints, epics, and boards. Use when working with Jira tickets, sprint planning, issue tracking, or when the user mentions Jira, tickets, sprints, epics, or issue management.
compatibility: Requires jira-cli installed and configured (jira init)
---

# Jira CLI

Use [jira-cli](https://github.com/ankitpokhrel/jira-cli) to interact with Jira from the command line.

## Prerequisites

- Jira CLI installed and configured with `jira init`
- Config: `~/.config/.jira/.config.yml` (override with `JIRA_CONFIG_FILE`)

## Critical Usage Patterns

**Always use `--plain` for listing and `--no-input` for creation** to avoid interactive mode:

```bash
jira issue list --plain              # ✓ Parseable output
jira issue create --no-input         # ✓ Skip prompts
jira issue view KEY --raw            # ✓ JSON output
```

## Creating Issues: Template-First Workflow

**IMPORTANT**: Always use a template file for issue creation to avoid shell escaping and formatting issues with bullets, quotes, and special characters.

### Recommended Workflow

1. **Research style first** - Query recent issues of the same type to match team conventions:
   ```bash
   jira issue list -p PROJECT -t"Spike" --created month --plain --columns key,summary,status
   jira issue view KEY --plain  # View a few to understand description style
   ```

2. **Draft in a template file** - Create `/tmp/issue-template.md` with the description body only (no frontmatter needed). Let user review and edit before proceeding.

3. **Create using `--template`** - This avoids all shell escaping issues:
   ```bash
   jira issue create -p PROJECT -t TYPE -s "Summary" -P "PARENT-KEY" \
     --template /tmp/issue-template.md --no-input
   ```

### Template File Format

The template file contains **only the description body** in Jira-flavored markdown:

```markdown
As a [role], I want [what], so that [benefit].

* First action item
  - Sub-item with detail
  - Another sub-item
* Second action item
* Third action item
```

### Quick Create (simple descriptions only)

For single-line or very simple descriptions without special characters:

```bash
jira issue create -p PROJECT -t Task -s "Summary" -b "Simple description" --no-input
```

### Common Options

```bash
-p PROJECT          # Project key
-t TYPE             # Issue type (Bug, Story, Task, Spike, etc.)
-s "Summary"        # Issue title
-P "PARENT-KEY"     # Parent epic or issue
-y PRIORITY         # Priority (High, Critical, etc.)
-a "user@email"     # Assignee
-l label            # Labels (repeat for multiple)
--template FILE     # Description from file (RECOMMENDED)
--no-input          # Skip interactive prompts
--web               # Open in browser after creation
```

## Listing and Viewing Issues

```bash
# View single issue
jira issue view KEY --plain
jira issue view KEY --raw                   # JSON output
jira issue view KEY --comments 10           # Include comments

# List with filters
jira issue list -p PROJECT --plain
jira issue list -t TYPE --plain             # By type
jira issue list -s "In Progress" --plain    # By status
jira issue list -a "user@email" --plain     # By assignee
jira issue list -y High --plain             # By priority
jira issue list -P "PARENT-KEY" --plain     # By parent
jira issue list -l label --plain            # By label

# Date filters
jira issue list --created month --plain
jira issue list --updated "-7d" --plain

# Custom columns and output
jira issue list --plain --columns key,summary,status,assignee

# JQL for complex queries
jira issue list -q "project = MPD AND status = 'In Progress'" --plain
```

## Updating Issues

```bash
jira issue edit KEY -s "New summary"
jira issue edit KEY --priority Critical
jira issue edit KEY --assignee "user@email"
jira issue edit KEY --label newlabel
jira issue assign KEY "user@email"
jira issue assign KEY -x                    # Unassign
jira issue move KEY "In Progress"           # Transition status
jira issue comment add KEY -m "Comment"
jira issue link KEY1 KEY2 "relates to"
```

## Sprints and Epics

```bash
# Sprints
jira sprint list --table --plain
jira sprint list --state active --plain
jira sprint list --current --plain          # Current sprint issues

# Epics
jira epic list --table --plain
jira epic list EPIC-KEY --plain             # Issues in epic
jira epic add EPIC-KEY ISSUE-KEY            # Add issue to epic
```

## Other Operations

```bash
jira open KEY                               # Open in browser
jira me --plain                             # Current user
jira project list --plain
jira board list --plain
```

## JQL Quick Reference

```jql
assignee = currentUser()
assignee is EMPTY
status not in ("Done", "Closed")
updated >= -7d
project = MPD AND priority in (High, Highest)
parent = EPIC-KEY
ORDER BY created DESC
```

## Notes

- Default pagination is 100 items; use `--paginate N` for more
- Custom fields require field ID: `--custom field-id=value`
- Debug with `jira --debug`
