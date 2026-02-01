---
name: "jira-assistant"
description: "JIRA automation hub routing to 13 specialized skills for any JIRA task: issues, workflows, agile, search, time tracking, service management, and more."
version: "2.1.0"
# Implements: SKILLS_ROUTER_SKILL_PROPOSAL v2.1
author: "jira-assistant-skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# JIRA Assistant

This hub routes requests to specialized JIRA skills. It does not execute JIRA operations directly—it helps find the right skill.

## Risk Levels

| Operation | Risk | Notes |
|-----------|------|-------|
| Route to skill | `-` | Read-only routing decision |
| Skill discovery | `-` | Lists available skills |
| Context tracking | `-` | In-memory only |

**Risk Legend**: `-` Safe, read-only | `!` Caution, modifiable | `!!` Warning, destructive but recoverable | `!!!` Danger, irreversible

## Quick Reference

| I want to... | Use this skill | Risk |
|--------------|----------------|:----:|
| Create/edit/delete a single issue, view/show issue details | jira-issue | ⚠️ |
| Search with JQL, export results | jira-search | - |
| Change status, assign, resolve, manage versions/components | jira-lifecycle | ⚠️ |
| Manage sprints, epics, subtasks, story points | jira-agile | - |
| Add comments, attachments, watchers | jira-collaborate | - |
| Link issues, view dependencies, blocker chains | jira-relationships | - |
| Log time, manage worklogs, time reports | jira-time | - |
| Handle service desk requests, SLAs, queues, approvals, assets, knowledge base | jira-jsm | - |
| Bulk operations on many issues (50+) with dry-run preview | jira-bulk | ⚠️⚠️ |
| Git branch names, commits, PR descriptions | jira-dev | - |
| Custom field discovery and Agile field configuration | jira-fields | - |
| Project discovery, cache management, diagnostics | jira-ops | - |
| Project settings, permissions, automation rules | jira-admin | ⚠️⚠️ |

**Risk Legend**: `-` Read-only/safe | `⚠️` Has destructive ops (confirm) | `⚠️⚠️` High-risk (confirm + dry-run)

---

## Routing Rules

1. **Explicit skill mention wins** - If user says "use jira-agile", use it
2. **Entity signals** - Issue key present → likely jira-issue or jira-lifecycle
3. **Quantity determines bulk** - 50+ issues → jira-bulk (consider bulk for 10+, required for 50+)
4. **Keywords drive routing**:
   - "show", "view", "display", "get", "retrieve", "see", "details", "look up", "check" (with issue reference) → jira-issue
   - "create", "update", "delete" (single issue) → jira-issue
   - "search", "find", "JQL", "filter" → jira-search
   - "sprint", "epic", "backlog", "story points", "subtask" → jira-agile
   - "transition", "move to", "assign", "close", "version", "release", "component", "resolve", "reopen", "archive" → jira-lifecycle
   - "comment", "attach", "watch", "notify", "notification", "activity", "history", "changelog" → jira-collaborate
   - "link", "blocks", "depends on", "clone", "dependency graph", "blocker chain" → jira-relationships
   - "log time", "worklog", "estimate", "time report", "timesheet" → jira-time
   - "service desk", "SLA", "customer", "request", "queue", "approval", "knowledge base", "asset" → jira-jsm
   - "branch name", "commit", "PR" → jira-dev
   - "custom field", "field ID" → jira-fields
   - "cache", "warm cache", "project discovery", "diagnostics", "performance", "request batching" → jira-ops
   - "permissions", "project settings", "automation", "automation rule", "users", "groups", "notifications", "screens", "issue types", "workflows", "notification scheme", "permission scheme" → jira-admin

---

## Negative Triggers

| Skill | Does NOT handle | Route to instead |
|-------|-----------------|------------------|
| jira-issue | Bulk (50+), transitions, comments, sprints, time | jira-bulk, jira-lifecycle, jira-collaborate, jira-agile, jira-time |
| jira-search | Single issue lookup, issue modifications | jira-issue, jira-bulk |
| jira-lifecycle | Field updates, bulk transitions | jira-issue, jira-bulk |
| jira-agile | Issue CRUD (except epic/subtask), JQL, time tracking | jira-issue, jira-search, jira-time |
| jira-bulk | Single issue ops, sprint management | jira-issue, jira-agile |
| jira-collaborate | Field updates, bulk comments | jira-issue, jira-bulk |
| jira-relationships | Field updates, epic/sprint linking | jira-issue, jira-agile |
| jira-time | SLA tracking, date-based searches | jira-jsm, jira-search |
| jira-jsm | Standard project issues, non-service-desk searches | jira-issue, jira-search |
| jira-dev | Issue field updates, JQL searches | jira-issue, jira-search |
| jira-fields | Field value searching, field value updates | jira-search, jira-issue |
| jira-ops | Project configuration, issue operations | jira-admin, jira-issue |
| jira-admin | Issue CRUD, bulk operations | jira-issue, jira-bulk |

---

## When to Clarify First

Ask the user before routing when:
- Request matches 2+ skills with similar likelihood
- Request is vague or could be interpreted multiple ways
- Destructive operations are implied

### Disambiguation Examples

**"Show me the sprint"**
Could mean:
1. Sprint metadata (dates, goals, capacity) → jira-agile
2. Issues in the current sprint → jira-search

Ask: "Do you want sprint details or the issues in the sprint?"

**"Update the issue"**
Could mean:
1. Change fields on one issue → jira-issue
2. Transition status → jira-lifecycle
3. Update multiple issues → jira-bulk

Ask: "What would you like to update - fields, status, or multiple issues?"

**"Create an issue in the epic"**
Context determines:
- Epic context explicit → jira-agile
- Just issue creation → jira-issue

---

## Context Awareness

### Pronoun Resolution

When user says "it" or "that issue":
- If exactly one issue mentioned in last 3 messages → use it
- If multiple issues mentioned → ask: "Which issue - TES-123 or TES-456?"
- If no issue in last 5 messages → ask: "Which issue are you referring to?"

**After CREATE**:
```
User: "create a bug in TES" → TES-789 created
User: "assign it to me"
→ "it" = TES-789 (the issue just created)

User: "create a bug in DEMO" → DEMO-105 created
User: "show me the details of the bug we just created"
→ "the bug we just created" = DEMO-105 (use jira-issue to retrieve details)
```

**After SEARCH**:
```
User: "find all open bugs" → Found TES-100, TES-101, TES-102
User: "close them"
→ "them" = the search results (use jira-bulk)
```

### Project Scope

When user mentions a project:
- Remember it for subsequent requests in this conversation
- "Create a bug in TES" → TES is now the active project
- "Create another bug" → Use TES implicitly
- Explicit project mention updates the active project

### Context Expiration

After 5+ messages or 5+ minutes since last reference:
- Re-confirm rather than assume: "Do you mean TES-123 from earlier?"
- Don't guess when context is stale

---

## Common Workflows

### Create Epic with Stories
1. Use jira-agile to create the epic → Note epic key (e.g., TES-100)
2. Use jira-issue to create each story with `--epic TES-100` flag to link during creation
   - Alternatively: create stories first, then use `jira-as agile epic add-issues` to link existing issues
3. Confirm: "Created epic TES-100 with N stories"

### Bulk Close from Search
1. Use jira-search to find matching issues
2. Use jira-bulk with --dry-run to preview
3. Confirm count with user before executing

### Data Passing Between Steps
When one skill's output feeds another:
- Capture entity IDs from responses (e.g., epic key from jira-agile)
- State this explicitly: "Created EPIC-123. Now creating stories..."
- Reference captured data in subsequent operations

---

## Error Handling

If a skill fails:
- Report the error clearly
- Suggest recovery options from docs/SAFEGUARDS.md
- Offer alternative approaches

If a skill is not available:
- Acknowledge the limitation
- Suggest alternatives from the Quick Reference table

### Permission Awareness
Before operations that might fail due to access:
- Check if user has mentioned permission issues before
- Suggest `jira-admin` for permission checks when blocked

---

## Discoverability

- `/jira-assistant-skills:browse-skills` - List all skills with descriptions
- `/jira-assistant-skills:skill-info <name>` - Detailed skill information

If user asks "what can you do?" or similar:
- Show the Quick Reference table
- Offer to explain specific skills

---

## What This Hub Does NOT Do

- Execute JIRA operations directly (always delegates)
- Guess when uncertain (asks instead)
- Perform destructive operations without confirmation
- Route to deprecated or unavailable skills without warning
