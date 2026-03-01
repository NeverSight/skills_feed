---
name: memory-optimize
description: "Optimizes Claude Code memory files in 4 interactive steps: removes duplicates, migrates rules to CLAUDE.md/rules files, compresses remaining entries, validates with cleanup. Typical reduction: 30-50% on token count."
tags: [auto-memory, claude-code-memory, claude-code-auto-memory]
license: MIT
metadata:
  author: "kochetkov-ma"
  version: "3.1.0"
  source: "claude-brewcode"
user-invocable: true
allowed-tools: Read Write Edit Glob Grep Bash Task AskUserQuestion
model: opus
---

## Memory Optimizer

Optimizes Claude Code **auto-memory** files in **4 interactive steps**: removes duplicates, migrates rules to proper config files, compresses remaining entries, validates the result.
Typical reduction: **30–50%** token count in memory files.

Auto-memory stores context across sessions in `~/.claude/projects/**/memory/MEMORY.md`.
Enable: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=0` · Disable: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`

**Benefits:** faster context loading · no duplicate rules · cleaner instructions · lower API cost

**Usage:**
```bash
/memory-optimize          # no args — starts 4-step interactive workflow
```

> _Skill text is written for LLM consumption and optimized for token efficiency._

---

# Memory Optimizer

Optimizes Claude Code memory files through 4 interactive steps.

> **No `context: fork`** — must run in main conversation to spawn agents.

## Phase 0: Load Context

1. Glob all memory files: `~/.claude/projects/**/memory/*.md`
2. Read `~/.claude/CLAUDE.md` and project `CLAUDE.md` (if exists)
3. Glob `.claude/rules/*.md` — read all project rules
4. Read `~/.claude/rules/*.md` — read all global rules

Build context map:
```
memory_files: [paths]
claude_md_sections: [sections]
rules_files: [paths with content]
```

## Step 1: Analysis — Remove Duplicates (Interactive)

**Goal:** Find memory entries that duplicate content already in CLAUDE.md or rules.

1. Spawn `Explore` agent to cross-reference all loaded files
2. Identify entries where:
   - Same rule already in CLAUDE.md
   - Same pattern already in a rules file
   - Contradicts CLAUDE.md (CLAUDE.md wins)
3. Show analysis:
   ```
   Found X duplicate/redundant entries (Y% of memory):
   | Entry | Memory File | Already In | Action |
   |-------|-------------|------------|--------|
   | "Use grepai first" | MEMORY.md:5 | rules/grepai-first.md | DELETE |
   ...
   ```
4. `AskUserQuestion`: "Delete X duplicate entries (Y% of memory)? This is safe — content exists elsewhere."
   - Options: "Yes, delete all" / "Review each" / "Skip this step"
5. Apply deletion using `Edit` tool if approved

## Step 2: Migration — Move to Rules/CLAUDE.md (Interactive)

**Goal:** Identify remaining memory entries better suited to persistent config files.

Decision tree (per entry):
- Applies to ALL projects + IS a rule/constraint → `~/.claude/rules/`
- Applies to THIS project only + IS a rule → `.claude/rules/`
- IS an architectural decision → project `CLAUDE.md`
- IS a fact/pattern reusable across sessions → KEEP in memory

1. Show categorization:
   ```
   X entries suitable for migration:
   | Entry | Current Location | Target | Reduction |
   |-------|-----------------|--------|-----------|
   | "Always use BD_PLUGIN_ROOT" | MEMORY.md:12 | .claude/rules/brewdoc.md | 15 tokens |
   ...
   Total: X entries → ~Y tokens saved
   ```
2. `AskUserQuestion`: "Migrate X entries to rules/CLAUDE.md?"
   - Options: "Yes, migrate all" / "Review each" / "Skip this step"
3. If approved:
   - Create/append to target rule files via `Edit`
   - Remove migrated entries from memory via `Edit`
   - If target file doesn't exist, create it

## Step 3: Compression (Interactive)

**Goal:** Compress remaining entries using LLM-efficient formatting.

Compression techniques:
- Prose → table row
- Multiple related entries → single table
- Verbose description → imperative one-liner
- List of examples → pattern + one example

1. Show compression preview:
   ```
   Compression opportunities found:
   | Before | After | Savings |
   |--------|-------|---------|
   | "When you need to... always use..." | "Use X for Y" | 8 tokens |
   ...
   Total: ~Y% token reduction (~Z tokens)
   ```
   Show 2-3 specific before/after samples.
2. `AskUserQuestion`: "Compress remaining memory? (~Y% reduction)"
   - Options: "Yes, compress all" / "Skip compression"
3. Apply compression via `Edit` (bottom-up order to preserve line numbers)

## Step 4: Validation (Automatic)

**Goal:** Verify final state and clean orphaned references.

1. Spawn `reviewer` agent to verify:
   - No broken file path references in memory files
   - No contradictions between memory and CLAUDE.md
   - Memory files are well-formed markdown
2. Clean broken references (Edit tool)
3. Check for orphaned memory files (files in `~/.claude/projects/**/memory/` with no MEMORY.md reference)
4. Report orphaned files and ask to delete

**Final Report:**
```markdown
## Memory Optimization Complete

### Summary
| Metric | Before | After | Saved |
|--------|--------|-------|-------|
| Total entries | X | Y | Z |
| Duplicate entries | X | 0 | — |
| Migrated entries | — | — | X |
| Token estimate | ~X | ~Y | ~Z (~P%) |

### Changes Made
- Step 1: Deleted X duplicate entries
- Step 2: Migrated X entries to rules/CLAUDE.md
- Step 3: Compressed X entries (Y% reduction)
- Step 4: Fixed X broken references, removed X orphaned files

### Final Memory Structure
{directory listing of ~/.claude/projects/.../memory/}

---

**Part of brewdoc:** [brewcode](https://github.com/kochetkov-ma/claude-brewcode) — docs tools: memory optimization, auto-sync, Claude installation docs, Markdown to PDF.
Install: `claude plugin marketplace add https://github.com/kochetkov-ma/claude-brewcode && claude plugin install brewdoc@claude-brewcode`
```
