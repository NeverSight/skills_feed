---
name: start-session
description: Use when user says "let's get started", "where are we", or at beginning of a session. Reads project context from CLAUDE.md, checks git status and recent commits, and provides orientation for the session. Works across all repo types (code, research, mixed).
---

# Session Start

Orient yourself at the beginning of a work session. This skill reads project context, roadmap progress, and provides a summary to get started quickly.

## Steps

### 1. Sync with Remote Machine

Run Unison to pull latest changes from the other machine:

```bash
unison folders -batch -terse
```

- `-batch` — non-interactive, skips conflicts (won't hang waiting for input)
- `-terse` — minimal output

This syncs all @folders and configs (.claude, .codex, .gemini, vault) before reading project context. Conflicts are skipped and left unsynced — review manually if needed.

### 2. Read Project Context

Check for context files in order of priority:
1. `CLAUDE.md` - Primary project context (if exists)
2. `agents.md` - Agent/workflow instructions (if exists)
3. `README.md` - Fallback for project overview
4. `.claude/` directory - Check for local settings

### 3. Detect Repo Type

Look for `type:` declaration in CLAUDE.md, or infer from contents:

| Indicator | Repo Type |
|-----------|-----------|
| `type: code` or `package.json`, `requirements.txt`, `go.mod` | Code |
| `type: research` or mostly `.md` files, no code dependencies | Research/Writing |
| Both code and documents | Mixed |

### 4. Check Git State

Run these commands to understand current state:
```bash
git status --short
git branch --show-current
git log --oneline -5
```

### 4b. Check Remote for New Branches

Fetch from remote and identify branches that exist on origin but have no local counterpart:

```bash
# Fetch and prune stale references
git fetch --prune 2>/dev/null

# Find remote-only branches (exist on origin, not locally)
comm -23 \
  <(git branch -r | grep -v HEAD | sed 's|^ *origin/||' | sort) \
  <(git branch | sed 's|^[* ] ||' | sort)
```

**What to report:**
- If remote-only branches exist, list them with a 🆕 marker
- Show the latest commit on each (one-liner) so user knows what it contains
- Skip `main`/`master` if they appear (these are typically tracked)

**Example output:**
```
**Remote-only branches:**
| Branch | Latest Commit |
|--------|---------------|
| 🆕 `feature/new-auth` | a1b2c3d Add OAuth2 support |
| 🆕 `claude/experiment-xyz` | e4f5g6h Initial setup |
```

**Why this matters:**
- Catches work from other machines or sessions
- Surfaces auto-created `claude/*` branches from Claude Code
- Identifies collaboration branches pushed by teammates

### 5. Parse Project Actions (if present)

Look for `## Project Actions` section in CLAUDE.md or agents.md:

1. Find all `### action-name` headers under `## Project Actions`
2. Extract action name and brief description (first line after header)
3. List them in the output summary

Example parsing:
```markdown
## Project Actions

### new-experiment <name>
Creates a new experiment branch with worktree...
```
→ Action: `new-experiment <name>` - Creates a new experiment branch with worktree

### 6. Parse Roadmap Sections (if present)

Look for these sections in CLAUDE.md and parse them:

**`## Current Focus`** - The single item being worked on right now
- Extract the checkbox item (e.g., `- [ ] Dark mode toggle`)
- This is the suggested starting point for the session

**`## Roadmap`** - The feature checklist
- Count total items and completed items (`[x]` vs `[ ]`)
- Calculate progress: "3/7 items complete"
- List next 2-3 incomplete items as "upcoming"

**`## Session Log`** - Historical record of sessions
- Find the most recent date entry (e.g., `### 2025-12-22`)
- Extract what was completed and what was set as "next"

### 7. Output Orientation Summary

Provide a structured summary based on repo type:

**For Code Repos:**
- Project name and purpose
- Current branch
- Uncommitted changes (if any)
- Recent commits
- **Remote-only branches** (if any exist on origin but not locally)
- **Project Actions** (from `## Project Actions` section, if any)
- **Current Focus** (from `## Current Focus` section)
- **Roadmap Progress** (from `## Roadmap` section)
- **Last Session Summary** (from `## Session Log`)

**For Research/Writing Repos:**
- Project/document name and purpose
- Document structure (chapters, sections)
- Recently edited files
- Word count or progress (if tracked)
- Where writing left off
- **Roadmap Progress** (if present)

**For Mixed Repos:**
- Combine relevant aspects from both

## Example Output

```
## Session Start: helloworld

**Purpose:** Experiment framework for rapid prototyping

**Current State:**
- Branch: `main`
- Status: Clean (no uncommitted changes)

**Recent Commits:**
- 9f139bd Update agents.md with session workflow and worktree docs
- 6b19a1f Reorganize main as experiment framework only

**Remote-only Branches:**
| Branch | Latest Commit |
|--------|---------------|
| 🆕 `feature/dark-mode` | c3d4e5f Add theme toggle component |

**Project Actions:**
- `new-experiment <name>` - Creates a new experiment branch with worktree
- `graduate-experiment <name>` - Promotes an experiment to its own repo

**Current Focus:**
- [ ] Add bulk import from CSV

**Roadmap Progress:** 4/7 items complete
- [ ] Next: Add bulk import from CSV
- [ ] Then: Export to PDF
- [ ] Then: Analytics dashboard

**Last Session (2025-12-21):**
- Completed: Supabase integration, helpful tips for editors
- Next: Bulk import feature
```

## Notes

- This skill is generic and works across all repos
- Repo-specific context comes from CLAUDE.md
- Pairs with `/wrap-up-session` which updates the roadmap sections

## Structure Checks (Guardrails)

After gathering context, check what's missing and prompt the user. This ensures new projects get properly set up.

### Check 1: No CLAUDE.md

If no CLAUDE.md exists:

```
⚠️ **No project context found.** This project is missing CLAUDE.md.

Would you like me to create one? I'll add:
- Project description (I'll ask what this project is for)
- Roadmap sections for session tracking
- Current focus placeholder

This enables `/start-session` orientation and `/wrap-up-session` session logging.
```

If yes, ask: "What is this project for? (one sentence)"

Then create CLAUDE.md with:
```markdown
# Project Name

[User's description]

## Current Focus
- [ ] [Ask user or use "Initial setup"]

## Roadmap
- [ ] [Feature 1]

## Backlog
- [Ideas for later]

## Session Log
### YYYY-MM-DD
- Completed: Initial project setup
- Next: [First focus item]
```

### Check 2: CLAUDE.md exists but missing roadmap sections

If CLAUDE.md exists but lacks `## Current Focus`, `## Roadmap`, or `## Session Log`:

```
⚠️ **Missing roadmap sections.** This project has CLAUDE.md but no session tracking.

Missing:
- [ ] ## Current Focus
- [ ] ## Roadmap
- [ ] ## Session Log

Would you like me to add them? This enables progress tracking and `/wrap-up-session` integration.
```

If yes, append the roadmap template to CLAUDE.md.

### Check 3: Summary of missing items

At the end of the orientation output, if anything is missing, add a **Setup Suggestions** section:

```
**Setup Suggestions:**
- [ ] Add CLAUDE.md with project description
- [ ] Add roadmap sections for session tracking
- [ ] Consider adding `## Project Actions` if this repo has custom workflows

Run these suggestions? [y/n]
```

This serves as the "guardrail" - the system actively tells you what's missing instead of requiring you to remember.
