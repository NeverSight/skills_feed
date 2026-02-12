---
name: crafting-effective-readmes
description: Create, update, or review README.md files with templates and checklists matched to audience and project type (open source, internal, personal, config/dotfiles). Use when asked to write/improve a README, add installation/usage, document setup, or audit a README for staleness and missing sections.
---

# Crafting Effective READMEs

## Overview

READMEs answer questions your audience will have. Different audiences need different information: an OSS contributor needs different context than a teammate onboarding, and both differ from future-you opening a config folder.

**Always ask:** Who will read this, and what do they need to know?

## Quick Start
1. Identify the project type (Open Source, Personal, Internal, Config).
2. Start from the matching template in `assets/templates/`.
3. Ensure the minimum sections exist: name/description and usage, plus install/setup if applicable.
4. If reviewing: verify commands against reality (configs, package scripts, CI).

## Process

### Step 1: Identify the Task

**Ask:** "What README task are you working on?"

| Task | When |
|------|------|
| **Creating** | New project, no README yet |
| **Adding** | Need to document something new |
| **Updating** | Capabilities changed, content is stale |
| **Reviewing** | Checking if README is still accurate |

### Step 2: Task-Specific Questions

**Creating initial README:**
1. What type of project? (see Project Types below)
2. What problem does this solve in one sentence?
3. What's the quickest path to "it works"?
4. Anything notable to highlight?

**Adding a section:**
1. What needs documenting?
2. Where should it go in the existing structure?
3. Who needs this info most?

**Updating existing content:**
1. What changed?
2. Read current README, identify stale sections
3. Propose specific edits

**Reviewing/refreshing:**
1. Read current README
2. Check against actual project state (package.json, main files, etc.)
3. Flag outdated sections
4. Update "Last reviewed" date if present

### Step 3: Always Ask

After drafting, ask: **"Anything else to highlight or include that I might have missed?"**

## Project Types

| Type | Audience | Key Sections | Template |
|------|----------|--------------|----------|
| **Open Source** | Contributors, users worldwide | Install, Usage, Contributing, License | `assets/templates/oss.md` |
| **Personal** | Future you, portfolio viewers | What it does, Tech stack, Learnings | `assets/templates/personal.md` |
| **Internal** | Teammates, new hires | Setup, Architecture, Runbooks | `assets/templates/internal.md` |
| **Config** | Future you (confused) | What's here, Why, How to extend, Gotchas | `assets/templates/xdg-config.md` |

**Ask the user** if unclear. Don't assume OSS defaults for everything.

## Essential Sections (All Types)

Every README needs at minimum:

1. **Name** - Self-explanatory title
2. **Description** - What + why in 1-2 sentences  
3. **Usage** - How to use it (examples help)

## References

- `references/section-checklist.md` - Which sections to include by project type
- `references/style-guide.md` - Common README mistakes and prose guidance
- `references/using-references.md` - How and when to use the deeper reference docs
