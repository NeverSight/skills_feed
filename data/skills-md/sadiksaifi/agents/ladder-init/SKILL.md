---
name: ladder-init
description: >-
  Initializes Ladder project structure with OVERVIEW.md and progress tracking.
  Use when starting phased spec-driven development or when the user says
  "ladder init."
compatibility: Requires git, Claude Code with plan mode and Task tool support
---

# Ladder Init

Bootstrap `.ladder/` directory structure with OVERVIEW.md and progress.md.

## When to Use

- User says "ladder init," "initialize ladder," "set up specs," "bootstrap phases," or "/ladder-init"
- Starting phased spec-driven development on a new or existing project
- Run once per project

## When NOT to Use

- `.ladder/OVERVIEW.md` already exists → will exit gracefully (idempotency gate)
- User wants to create a phase spec → use `/ladder-create`
- User wants to fix a malformed spec → use `/ladder-refine`
- User wants to implement a phase → use `/ladder-execute`

## Quick Reference

| Field | Value |
|-------|-------|
| **Input** | Project name, vision, tech stack, architecture (from user) |
| **Output** | `.ladder/OVERVIEW.md`, `.ladder/progress.md`, `.ladder/specs/`, `.ladder/refs/` |
| **Commits** | `chore(ladder): initialize project structure` |
| **Prerequisites** | None — this is the entry point |

## Iron Laws

1. **Specs are immutable** after creation — only `progress.md` is a living document.
2. **Evidence before completion** — never claim a step is done without proof.
3. **`progress.md` is the single source of truth** for execution state.
4. **User approval before persistent actions** — always confirm before writing files or committing.

## Hard Gates

<HARD-GATE>
IDEMPOTENCY: If `.ladder/OVERVIEW.md` exists, print "Ladder already initialized — OVERVIEW.md exists. Nothing to do." and STOP. Do not proceed under any circumstances.
</HARD-GATE>

<HARD-GATE>
ALL ANSWERS REQUIRED: Do not create any files until ALL 4 user answers (project name, vision, tech stack, architecture) have been collected. No partial scaffolding.
</HARD-GATE>

<HARD-GATE>
USER REVIEW: Present OVERVIEW.md content to the user for approval before writing to disk.
</HARD-GATE>

## Workflow

### Phase A: Validation

#### 1. Idempotency Check

If `.ladder/OVERVIEW.md` already exists → STOP (see Hard Gate above).

#### 2. Discover Existing Specs

Scan `.ladder/specs/` for `L-*.md` files. Extract phase number and title from each filename. Store as the discovered phase list for the Phase Registry.

### Phase B: Information Gathering

#### 3. Gather Project Info

Ask the user **one question at a time** (use AskUserQuestion):
1. **Project name** — short name for the product
2. **Vision** — one-line product vision
3. **Tech stack** — languages, frameworks, platforms
4. **Architecture** — 2-3 sentence architecture summary

#### 4. Map Reference Docs

If `.ladder/refs/` contains files, list them and ask the user:
> "Which phases does each reference doc relate to?"

Build a mapping table (document → relevant phase numbers).

#### 5. Brownfield Detection

Ask: "Is this an existing project with prior work?"

**If yes (brownfield):**
- Scan project structure: key directories, package files, README, config files
- Ask user to summarize key components and known technical debt
- Build a Baseline section for progress.md (see `references/progress-format.md`)

**If no (greenfield):** skip baseline.

### Phase C: Scaffold

#### 6. Create Directory Structure

Create `.ladder/specs/` and `.ladder/refs/` if they don't already exist.

#### 7. Write OVERVIEW.md

Create `.ladder/OVERVIEW.md` using this format:

```markdown
# <Name> — Product Overview

## Vision
<one-line vision>

## Tech Stack
- <items>

## Architecture
<2-3 sentences>

## Reference Docs
| Document | Relevant Phases |
|----------|----------------|
| <filename> | L<N>, L<N> |

## Phase Registry
| # | File | Status |
|---|------|--------|
| 0 | L-00-slug.md | pending |
```

#### 8. Write progress.md

Create `.ladder/progress.md`:

```markdown
# Progress
```

If brownfield, add the Baseline section immediately after the heading. See `references/progress-format.md` for the Baseline format.

### Phase D: Finalize

#### 9. Commit

Stage `.ladder/OVERVIEW.md` and `.ladder/progress.md` only.

```
chore(ladder): initialize project structure
```

#### 10. Summary

Print what was created and suggest:
> "Run `/ladder-refine <spec-path>` to bring a spec to canonical format, or `/ladder-create` to add a new phase."

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| Writing files before gathering all user info | Produces incomplete OVERVIEW.md, requires re-editing | Collect all 4 answers first (Hard Gate) |
| Skipping brownfield detection | Misses existing state, phases lack context | Always ask about prior work |
| Ignoring existing specs in `.ladder/specs/` | Phase Registry is incomplete | Scan for `L-*.md` files first |
| Creating `progress.md` with phase entries | Only `/ladder-execute` adds phase entries | Create with just `# Progress` heading |

## Red Flags — STOP

| Thought | Reality |
|---------|---------|
| "I'll create the files and fill in details later" | All info must be gathered BEFORE file creation |
| "The user probably wants greenfield" | Always ask — brownfield detection is mandatory |
| "I can skip the reference docs step" | Missing mappings break phase context |
| "OVERVIEW.md exists but I'll overwrite it" | Idempotency check is a HARD GATE — STOP |
| "I'll just use defaults for tech stack" | Every field must come from the user |

## Integration

| Direction | Skill | Signal |
|-----------|-------|--------|
| **Enables** | `/ladder-create` | OVERVIEW.md exists with Phase Registry |
| **Enables** | `/ladder-refine` | `.ladder/specs/` directory exists |
| **Required by** | All other Ladder skills | OVERVIEW.md is the project root |
