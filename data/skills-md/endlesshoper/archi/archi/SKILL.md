---
name: archi
description: |
  Project scaffolding and management for vibe coding. Initializes opinionated
  documentation structure, tracks features, and keeps agent context updated.

  Use when: setting up a new project, tracking features, viewing project status,
  or managing documentation. Works with Claude Code, OpenCode, Codex CLI, and
  other skills-compatible agents.
argument-hint: "[init|feature|status|docs]"
---

# Archi

Project scaffolding and management for AI-assisted development ("vibe coding").

## Workflows

| Command | What it does |
|---------|--------------|
| `/archi` | Detect context and choose appropriate workflow, or show menu |
| `/archi init` | Initialize new project with docs structure |
| `/archi feature` | Manage features (add/start/complete/update) |
| `/archi status` | Show project overview |
| `/archi docs` | Sync and update documentation |

**Users can just run `/archi`** - you'll figure out what they need based on context. If it's a new project with no docs structure, offer to initialize. If they're mid-conversation about a feature, offer to track it. When unclear, use AskUserQuestion to let them choose.

Parse `$ARGUMENTS` to route to specific workflows, or detect from context.

---

## Initialize Project

**Trigger:** `/archi init`, `/archi start`, or when project has no docs structure

**Goal:** Create SPEC.md and docs folder structure through a conversational interview.

### Interview the user to understand:
- Project name (detect from directory/package.json if possible)
- What they're building (one sentence)
- Who it's for
- What problem it solves
- Key features (3-5 things it should do)

If there are existing files (README, package.json, etc.), read them to gather context before asking questions. Don't ask permission to read - just read them.

Use AskUserQuestion throughout to gather info interactively. Keep questions simple and beginner-friendly.

### Create this structure:

```
project/
├── SPEC.md
└── docs/
    ├── features/
    │   ├── todo/
    │   ├── doing/
    │   └── done/
    ├── research/
    │   ├── spikes/
    │   └── references/
    └── bugs/
```

### SPEC.md template:

```markdown
# {Project Name}

> {One-sentence description}

## Problem
{What problem does this solve}

## Users
{Who is this for}

## Features
1. {Feature}
2. {Feature}
...

## Out of Scope
- TBD

## Success Criteria
- TBD
```

After creating, suggest next steps like adding their first feature.

---

## Feature Management

**Trigger:** `/archi feature`, or when user mentions working on/completing something

**Goal:** Track features through todo → doing → done lifecycle.

### Capabilities:
- **Add new feature** → create file in `docs/features/todo/`
- **Start feature** → move from `todo/` to `doing/`, add started date
- **Complete feature** → move from `doing/` to `done/`, add completed date
- **Update progress** → edit existing feature file

Detect intent from conversation context. If user says "I just finished the auth system", offer to mark it done. If they say "I'm going to work on payments", offer to start that feature or create it if it doesn't exist.

### Feature file format:

**Todo:**
```yaml
---
title: Feature Name
priority: high | medium | low
---
# Feature Name

Description and requirements...
```

**Doing:**
```yaml
---
title: Feature Name
priority: high
started: 2026-01-23
---
# Feature Name

## Progress
- What's been done
- What's next
```

**Done:**
```yaml
---
title: Feature Name
category: Core | Enhancement | Fix | Infrastructure
completed: 2026-01-23
---
# Feature Name

Summary of what was built.
```

Use kebab-case for filenames: `user-authentication.md`

---

## Project Status

**Trigger:** `/archi status`, or when user asks about project state

**Goal:** Give a quick overview of where the project stands.

Read the docs structure and summarize:
- Features in progress (from `doing/`)
- Backlog count and priorities (from `todo/`)
- Recently completed (from `done/`)
- Any research or bugs

Keep it concise and actionable.

---

## Documentation Sync

**Trigger:** `/archi docs`, or when docs seem out of sync

**Goal:** Keep project documentation current.

Check for:
- SPEC.md reflects current scope
- Features mentioned but not tracked
- Stale information

Offer to update what's outdated. Don't over-ask - if something clearly needs updating, just suggest the specific changes.

---

## Behavior Guidelines

1. **Be contextual** - detect what the user needs from conversation flow
2. **Be beginner-friendly** - no jargon, explain what's happening
3. **Just do it** - read files, check structure, don't ask permission for basic operations
4. **Use AskUserQuestion** - for choices and gathering info, not for confirmation of obvious actions
5. **Kebab-case filenames** - `user-authentication.md` not `UserAuthentication.md`
6. **Date format** - YYYY-MM-DD

---

## Handling Existing Documentation

**IMPORTANT:** Never overwrite existing documentation without explicit user permission.

When initializing a project that already has documentation (README.md, docs/, SPEC.md, etc.):

1. **Read existing docs first** - understand what's already there
2. **Preserve all content** - never summarize or condense existing documentation
3. **Adapt to archi format** - restructure into the archi structure while keeping ALL original content
4. **Ask before overwriting** - if a file would be replaced, ask the user first
5. **Copy when needed** - if existing content fits elsewhere, use `cp` to preserve it before reorganizing

### Migration approach:

- Existing README → Extract relevant sections into SPEC.md, keep README for public-facing info
- Existing docs/ folder → Move files into appropriate archi subdirectories (features/, research/, etc.)
- Existing feature docs → Adapt to feature file format, preserving full content
- Existing specs → Merge into SPEC.md sections, keeping all detail

**Never lose user content.** If unsure where something belongs, ask. If content is substantial, copy the file rather than moving it until the user confirms the new structure works for them.
