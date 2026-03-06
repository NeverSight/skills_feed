---
name: optimise-claude
description: Use when auditing, trimming, or restructuring AI instruction files (CLAUDE.md, SKILL.md, AGENTS.md) to reduce context-window consumption. Trigger whenever CLAUDE.md is bloated or Claude ignores instructions, a SKILL.md exceeds 120 lines, skills share duplicated content, AGENTS.md has large inline blocks, or the user asks to optimize, slim down, or reduce token usage.
---

# Optimise Claude

Audit AI instruction files for size, relevance, and structure. CLAUDE.md loads every session — bloated files cause Claude to ignore your actual instructions. SKILL.md lines cost tokens on every invocation. Keeping both lean reduces latency, cost, and instruction-following failures.

## Scope

All operations scoped to project root (`$PWD`). Never modify files outside the repository.

## When to Use

- CLAUDE.md is long and Claude ignores rules or asks questions already answered in it
- SKILL.md files exceed ~120 lines
- Frontmatter or section order is non-canonical
- Multiple skills contain duplicated content
- AGENTS.md has inline instruction blocks >30 lines that should be skills

## Workflow

Run phases sequentially. Skip any that don't apply.

### Phase 1 — Inventory & Triage

1. List every CLAUDE.md (root, parent dirs, child dirs), SKILL.md under `.agents/skills/`, and AGENTS.md
2. Record: file, line count, has frontmatter (y/n), canonical sections (y/n)
3. Flag violations per file type (see criteria below)
4. Output triage table sorted by line count descending

```
| File | Lines | Type | Violations |
|------|------:|------|------------|
```

### Phase 2 — Audit CLAUDE.md

For each CLAUDE.md, apply the litmus test per line: **"Would removing this cause Claude to make mistakes?"** If not, cut it.

**Keep:**
- Bash commands Claude can't guess
- Code style rules that differ from defaults
- Testing instructions and preferred test runners
- Repo etiquette (branch naming, PR conventions)
- Architectural decisions specific to the project
- Dev environment quirks (required env vars)
- Common gotchas or non-obvious behaviors

**Remove:**
- Anything Claude can figure out by reading code
- Standard language conventions Claude already knows
- Detailed API docs (link instead)
- Information that changes frequently
- Long explanations or tutorials
- File-by-file codebase descriptions
- Self-evident practices like "write clean code"

**Restructure:**
- Migrate domain-specific workflows and on-demand knowledge to skills (SKILL.md)
- Split large CLAUDE.md using `@path/to/import` syntax for logical sections
- Use emphasis (`IMPORTANT`, `YOU MUST`) sparingly — only for rules Claude repeatedly violates
- If a rule is critical with zero exceptions, suggest converting to a hook instead

### Phase 3 — Reduce SKILL.md Token Usage

For each flagged skill:
- Trim prose to imperative bullets
- Collapse verbose examples to minimal code fences
- Remove redundant explanations covered by parent AGENTS.md or CLAUDE.md
- Remove blank lines between list items
- Target <=120 lines; if still over, move detail to `references/` files with clear pointers
- For multi-domain skills, split into variant reference files (read only the relevant one)

### Phase 4 — Fix Structure & Frontmatter

- YAML frontmatter: `name` matches directory (kebab-case), `description` starts with "Use when"
- Section order: H1 title → When to Use → Rules/Instructions → Quick Reference → Validation
- Remove empty or placeholder sections
- Use imperative voice throughout

### Phase 5 — Cross-Skill Deduplication

1. Identify repeated content blocks across skills (>5 similar lines)
2. Move shared content to root CLAUDE.md, AGENTS.md, or a shared skill
3. Replace duplicates with one-line pointer: "See `<skill-name>` for ..."
4. Reword overlapping `description` fields so each skill has a unique trigger

### Phase 6 — Extract Bloated AGENTS.md Blocks

1. Scan AGENTS.md for inline instruction blocks >30 lines
2. Create a new skill at `.agents/skills/<name>/SKILL.md`
3. Replace original block with slim pointer + Quick Reference
4. If a skill sync script exists, run it

## Output Format

```
## Optimisation Report

| File | Before | After | Delta |
|------|-------:|------:|------:|
| ...  |    250 |   110 |  -140 |

Total files audited: N
Total lines saved: N
Content migrated to skills: N
```

## Validation

- Every CLAUDE.md line passes the "would removing cause mistakes?" test
- No SKILL.md exceeds 120 lines
- Every SKILL.md has valid YAML frontmatter with `name` and `description`
- No two skills share >5 identical lines
- No AGENTS.md has inline instruction blocks >30 lines without a skill pointer
- Domain-specific content lives in skills, not CLAUDE.md
