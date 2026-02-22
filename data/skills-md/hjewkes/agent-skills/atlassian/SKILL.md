---
name: atlassian
description: Jira and Confluence integration for Atlassian Cloud. Use when the user needs to search issues, manage sprints, read Confluence docs, create/update pages, work with epics and backlogs, or any Atlassian workflow. Triggers include "jira", "confluence", "sprint", "backlog", "ticket", "issue", "epic", or references to Atlassian content.
allowed-tools: Bash(jira:*), Bash(confluence:*)
---

# Atlassian — Jira & Confluence

## Setup

Both `jira` and `confluence` wrappers auto-detect first run and launch `scripts/setup`.

## Jira Operations

```bash
# Search issues (JQL)
jira issue list -q "project = PROJ AND status = 'In Progress'" --plain

# View issue details
jira issue view KEY --raw | jq '.fields.summary, .fields.status.name'

# Create issue
jira issue create -t Bug -s "Summary of the issue" --no-input

# Transition issue
jira issue move KEY "In Review"

# Current sprint
jira sprint list --current --plain

# My in-progress issues
jira issue list -a$(jira me) -s"In Progress" --plain
```

## Confluence Operations

```bash
# Search pages (CQL)
confluence search "text ~ 'keyword' AND space = 'KEY'"

# Read a page
confluence get PAGE_ID --format storage

# Create a page
confluence create --space KEY --title "Page Title" --body "Content here"

# List spaces
confluence spaces
```

## Output Conventions

- Use `--plain` for human-readable output when displaying to the user.
- Use `--raw` + `jq` to extract specific fields programmatically.
- The `confluence` script always outputs JSON — pipe through `jq` for display.

## Reference Files

| Reference | When to Load |
|-----------|-------------|
| references/jira-commands.md | Full jira-cli command reference needed |
| references/confluence-commands.md | Confluence script details needed |
| references/jql-patterns.md | Building complex JQL queries |
| references/cql-patterns.md | Building complex CQL queries |
| references/troubleshooting.md | Auth failures, errors, rate limits |
