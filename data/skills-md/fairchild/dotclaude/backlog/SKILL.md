---
name: backlog
description: Capture explored work as a backlog item for future implementation. Use when you've explored an enhancement, alternative approach, or feature but decided to defer it. Creates comprehensive plan files in backlog/ directory with enough context for a future session to execute efficiently.
license: Apache-2.0
---

# Backlog

Create a comprehensive backlog item for work we've explored but decided not to implement now.

## Instructions

### Step 1: Gather Context

Ask these questions to understand what we're deferring:

1. **What feature/enhancement are we deferring?** (brief name)
2. **Why did we explore it?** (what problem does it solve)
3. **Why are we deferring?** (out of scope, lower priority, needs more info, etc.)
4. **What did we learn?** (key findings from exploration)

### Step 2: Determine Category

Based on the work, select the appropriate category per `backlog/AGENTS.md`:

- **plan**: Comprehensive design for new features (most common for /backlog)
- **followup**: Post-merge improvements and tech debt
- **task-list**: Collection of related items
- **ideas**: Ideas to explore, not yet developed into actionable plans

### Step 3: Create Backlog File

Create a file at `backlog/{feature}-{category}.md` with this structure:

```markdown
---
status: pending
category: {plan|followup|task-list|ideas}
pr: null
branch: null
score: null
retro_summary: null
completed: null
---

# {Feature Name}

## Problem Statement

{1-2 paragraphs explaining why this work matters and what problem it solves}

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| {decision point} | {what we'd choose} | {why} |

## Architecture

{ASCII diagram if helpful}

## Implementation Phases

### Phase 1: {Name}

**Files to modify:**
- `path/to/file.ts` - {what changes}

**Files to create:**
- `path/to/new-file.ts` - {purpose}

**Acceptance criteria:**
- [ ] {testable outcome}
- [ ] {testable outcome}

### Phase 2: {Name}
...

## Verification Commands

```bash
# Commands to verify the implementation works
```

## Rollback Plan

{How to undo if things go wrong}

## References

- {Related files, PRs, docs, or external resources}
```

### Step 4: Include Research Artifacts

Incorporate what we learned during exploration:
- Code snippets we prototyped or found
- Configuration examples
- API patterns from existing code
- External documentation links

### Step 5: Commit

Commit the backlog file with message:
```
chore: add {feature} to backlog

{One sentence on what this enables}
```

## Quality Checklist

Before finishing, verify the backlog file:

- [ ] Has enough context that a fresh session can understand without the original conversation
- [ ] Includes specific file paths (with line numbers when relevant)
- [ ] Has verification commands or acceptance criteria
- [ ] References related code patterns in the codebase
- [ ] Follows the frontmatter schema from `backlog/AGENTS.md`

## List Backlog Items

To see all backlog items, run:

```bash
~/.claude/skills/backlog/scripts/status.sh
```

## Grooming

Detect stale or likely-completed backlog items that were never moved to `done/`.

```bash
~/.claude/skills/backlog/scripts/groom.sh [path/to/backlog]
```

The script cross-references pending items against git history (PR numbers, branch names, keyword matches) and the filesystem (files that were supposed to be created). It flags items that look done so you can review and close them.

See `references/grooming.md` for the full grooming workflow and checklist.

## Example Usage

```
User: /backlog
Claude: I'll help capture the work we explored for future implementation.

What feature/enhancement are we deferring?
> R2 storage for docs assets

Why did we explore it?
> Docs screenshots are gitignored, wanted persistent storage without git bloat

Why are we deferring?
> Works fine locally for now, R2 adds complexity we don't need yet

What did we learn?
> R2 bindings in wrangler.jsonc, Worker route pattern, wrangler CLI for uploads

[Creates backlog/docs-r2-storage-plan.md with full implementation plan]
```

## Setting Up backlog/ Directory

See `references/agents-schema.md` for the full directory setup and frontmatter schema.

## References

- `references/agents-schema.md` — Frontmatter schema, categories, lifecycle, directory setup
- `references/grooming.md` — Backlog maintenance workflow and checklist
- `references/README.md` — Background, design philosophy, and related projects
