---
name: document
description: Update project documentation after feature approval. Creates/updates feature docs and user guides. Use after /test passes and user approves. Supports task IDs for easier invocation.
model: haiku
---

# /document - Documentation Agent

> **Model:** haiku (templated documentation work)

## Command Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--help` | `-h` | Show available commands and options |
| `--version` | `-v` | Show workflow skills version |

### Flag Handling

**On `-h` or `--help`:**
```
/document - Documentation Agent

Usage:
  /document {ID}                     Update docs for a task
  /document -h, --help               Show this help message
  /document -v, --version            Show version

Arguments:
  {ID}    Task ID (number) or task filename (e.g., 001-auth-jwt)

Creates/Updates:
  - docs/features/{feature}.md       Technical documentation
  - docs/guides/{feature}.md         User guides (if user-facing)
  - CLAUDE.md                        Project patterns (if needed)

Examples:
  /document 1                        # Document task #1
  /document 001-auth-jwt             # Using task filename

Next: /ship {ID}
```

**On `-v` or `--version`:**
Display:
```
Workflow Skills v1.4.1
https://github.com/eljun/claude-skills
```

---

## When to Use

Invoke `/document {ID}` when:
- Task has passed testing (`/test` returned PASS)
- User has approved the implementation
- Ready to update project documentation

**Example:** `/document 1` or `/document 001-dashboard-redesign`

## Task ID Resolution

The `{ID}` can be:
- **Numeric ID:** `1`, `2`, `3` → Looks up in TASKS.md, finds matching task document
- **Padded ID:** `001`, `002` → Same as numeric
- **Full filename:** `001-dashboard-redesign` → Direct file reference

## Workflow

```
/document {ID}
       ↓
1. Resolve task ID → find task document
2. Read task document for context
3. Check Automation field (manual | auto)
4. Read test report for verification
5. Update/create feature documentation
6. Update/create user guide (if user-facing)
7. Update CLAUDE.md files if needed
8. Move task to "Approved" in TASKS.md
       ↓
┌─── Automation Mode? ───┐
│                        │
▼ Manual                 ▼ Auto
Notify user              Invoke /ship {ID}
Ready for /ship
```

## Auto Mode Behavior

When task document has `Automation: auto`:

After documentation is complete, use Task tool to spawn ship agent with **model: haiku**:
```
Documentation complete: #{ID} - {Task Title}

Updated files:
- docs/features/{feature}.md
- docs/guides/{feature}.md

[AUTO] Spawning /ship with haiku model...
```
`Task({ subagent_type: "general-purpose", model: "haiku", prompt: "/ship {ID}" })`

## Pre-Documentation Checklist

### 1. Gather Context (Primary Sources Only)

Read these files — they contain all the context you need:
```
docs/task/{ID}-{task-name}.md        - Implementation details
docs/testing/{ID}-{task-name}.md     - Test results & verification
```

**IMPORTANT — Context Efficiency:**
These two documents were created by the `/task`, `/implement`, and `/test` agents which already analyzed the codebase. Do NOT perform broad codebase exploration. Only read specific source files if you need to verify implementation details for documentation accuracy.

### 2. Identify Documentation Needs

| Change Type | Documentation Needed |
|-------------|---------------------|
| New feature | Feature doc + User guide |
| Enhancement | Update existing docs |
| Bug fix | Update troubleshooting sections |
| API change | Update API reference |

### 3. Use Templates

Follow the templates defined in this document:
- **Feature Documentation Structure** - Technical feature docs (see below)
- **User Guide Structure** - User-facing guides (see below)

---

## Documentation Types

### 1. Feature Documentation

**Location:** `docs/features/{FEATURE}.md`
**Audience:** Developers
**Purpose:** Technical implementation details

**When to create/update:**
- New feature → Create new doc
- Enhancement → Update existing doc
- Significant change → Update relevant sections

### 2. User Guide

**Location:** `docs/guides/{feature}.md`
**Audience:** End users (business owners, customers)
**Purpose:** How to use the feature

**When to create/update:**
- User-facing feature → Create/update guide
- UI changes → Update screenshots/steps
- New functionality → Add new sections

### 3. CLAUDE.md Files

**Locations:**
- `/CLAUDE.md` - Root project instructions

**When to update:**
- New patterns discovered
- New "Do Not" rules
- Bug fix patterns
- Tech stack changes

---

## Feature Documentation Structure

```markdown
# Feature: {Feature Name}

> **Status:** PRODUCTION
> **Last Updated:** {Date}

## Overview

{Brief 2-3 sentence description}

---

## User Journey

### For Customers
1. Step 1
2. Step 2

### For Business Owners
1. Step 1
2. Step 2

---

## Architecture

### File Structure
{Accurate file tree - VERIFY paths exist}

### Database Schema
{SQL with comments, if applicable}

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|

---

## Implementation Details

### Key Components
| Component | Location | Purpose |
|-----------|----------|---------|

### Technical Notes
- Important detail 1
- Important detail 2

---

## Related Features
- [Link to related feature]
```

**Target length:** 200-400 lines

---

## User Guide Structure

```markdown
# {Feature Name} Guide

> {Brief intro sentence}

## Quick Start
{1-2 paragraph overview}

---

## For Customers

### How to {Primary Action}
1. Step with context
2. Step with context

### Tips
- Tip 1
- Tip 2

---

## For Business Owners

### How to {Admin Action}
1. Step with context

### Settings
| Setting | Location | What it does |
|---------|----------|--------------|

---

## FAQ

**Q: Question?**
A: Answer.

---

## Troubleshooting

**Issue:** Description
**Solution:** How to fix

---

## Related Guides
- [Link]
```

**Target length:** 100-200 lines

---

## Documentation Checklist

### Feature Doc
- [ ] Follows template structure
- [ ] File paths verified to exist
- [ ] API endpoints are accurate
- [ ] Schema matches database
- [ ] Status set to PRODUCTION
- [ ] Last Updated date set
- [ ] Under 400 lines

### User Guide
- [ ] Follows template structure
- [ ] Clear step-by-step instructions
- [ ] FAQ answers common questions
- [ ] Troubleshooting section included
- [ ] Under 200 lines

### CLAUDE.md Updates
- [ ] New patterns added to relevant file
- [ ] "Do Not" rules added if mistakes were made
- [ ] Tech stack updated if dependencies changed

---

## Update TASKS.md

Move task to "Approved" section:

```markdown
## Approved

| ID | Task | Task Doc | Feature Doc | Test Report | Approved |
|----|------|----------|-------------|-------------|----------|
| 1 | Quick Actions Redesign | [001-quick-actions.md](docs/task/001-quick-actions.md) | [feature](docs/features/...) | [001-quick-actions.md](docs/testing/001-quick-actions.md) | Jan 25 |
```

---

## What to Include

- **Current state only** - Document what exists now
- **Accurate file paths** - Verify paths exist
- **Working examples** - Only code that matches production
- **Clear user journeys** - What users actually do

## What to Exclude

| Remove | Why |
|--------|-----|
| Development logs | Move to changelogs |
| Before/after comparisons | Only document current state |
| "Lessons learned" | Dev notes, not docs |
| Speculative future phases | Keep minimal |
| Full component code | Code lives in codebase |

---

## Handoff to /ship

**Check the task document for `Automation: auto` field.**

### Manual Mode
```
Documentation updated for: #{ID} - {Task Title}

Updated files:
- docs/features/{feature}.md (created/updated)
- docs/guides/{feature}.md (created/updated)
- CLAUDE.md (if updated)

Task moved to "Approved" in TASKS.md

Next Steps:
  /ship {ID}              # e.g., /ship 1
  /ship {ID}-{task-name}  # e.g., /ship 001-auth-jwt
```

### Auto Mode
```
Documentation updated for: #{ID} - {Task Title}

Updated files:
- docs/features/{feature}.md (created/updated)
- docs/guides/{feature}.md (created/updated)
- CLAUDE.md (if updated)

Task moved to "Approved" in TASKS.md

[AUTO] Spawning /ship with haiku model...
```
Use Task tool: `Task({ subagent_type: "general-purpose", model: "haiku", prompt: "/ship {ID}" })`

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `/implement` | If issues found during doc review |
| `/ship` | After documentation complete |

## Recommended Plugins (Install Separately)

These plugins must be installed separately. **Once installed, they MUST be invoked** — do not skip them:

| Plugin | Install From | When to Invoke |
|--------|--------------|----------------|
| `vercel-react-best-practices` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Reference React patterns for docs |
| `supabase-postgres-best-practices` | [supabase/agent-skills](https://github.com/supabase/agent-skills) | Reference database patterns for docs |
