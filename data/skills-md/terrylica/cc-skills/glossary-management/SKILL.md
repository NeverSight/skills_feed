---
name: glossary-management
description: Manage terminology glossary with Vale. TRIGGERS - sync terms, glossary validation, add terms, Vale vocabulary.
---

# Glossary Management

## Overview

Manage the global terminology glossary (`~/.claude/docs/GLOSSARY.md`) and its Vale integration. The glossary is the Single Source of Truth (SSoT) for terminology across all projects.

## When to Use This Skill

Use when:

- Manually syncing glossary to Vale vocabulary files
- Validating glossary format and structure
- Checking for duplicate or conflicting terms across projects
- Adding new terms programmatically
- Troubleshooting Vale terminology warnings

## Quick Commands

```bash
# Manual sync to Vale
bun ~/.claude/tools/bin/glossary-sync.ts

# Check for duplicates/conflicts across projects (invokes terminology-sync hook)
bun ~/eon/cc-skills/plugins/itp-hooks/hooks/posttooluse-terminology-sync.ts <<< '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/test-CLAUDE.md"}}'
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    GLOSSARY.md (SSoT)                           │
│                ~/.claude/docs/GLOSSARY.md                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
┌─────────────────┐ ┌───────────┐ ┌────────────────────┐
│ accept.txt      │ │ Term.yml  │ │ Project CLAUDE.md  │
│ (Vale vocab)    │ │ (subs)    │ │ (bidirectional)    │
└─────────────────┘ └───────────┘ └────────────────────┘
```

## SCAN_PATHS Configuration

The terminology sync hook uses `SCAN_PATHS` to discover project CLAUDE.md files. This is configured via an HTML comment in GLOSSARY.md:

```markdown
<!-- SCAN_PATHS:
- ~/eon/*/CLAUDE.md
- ~/eon/*/*/CLAUDE.md
- ~/.claude/docs/GLOSSARY.md
-->
```

**Format rules**:

- Must be an HTML comment starting with `<!-- SCAN_PATHS:`
- Each path on its own line with `-` prefix
- Supports glob patterns (`*`, `**`)
- Paths are relative to home directory (`~`)

**Default paths** (if not specified):

- `~/eon/*/CLAUDE.md` - Top-level project CLAUDE.md files
- `~/eon/*/*/CLAUDE.md` - Package-level CLAUDE.md files

## Table Schema (5 Columns)

Every term in GLOSSARY.md follows this 5-column format:

| Column         | Required | Description                     | Example                        |
| -------------- | -------- | ------------------------------- | ------------------------------ |
| **Term**       | Yes      | Bold term name (`**Term**`)     | `**Time-Weighted Sharpe**`     |
| **Acronym**    | Yes      | Abbreviation (or `-` if none)   | `TWSR`                         |
| **Definition** | Yes      | Clear, concise definition       | `Sharpe ratio for range bars`  |
| **Unit/Range** | Yes      | Measurement unit or valid range | `ratio`, `[0, 1]`, `-`         |
| **Projects**   | Yes      | Comma-separated project names   | `alpha-forge, trading-fitness` |

**Example row**:

```markdown
| **Time-Weighted Sharpe** | TWSR | Sharpe ratio for variable-duration bars using time weights | annualized ratio | alpha-forge |
```

## Automatic Sync (Hooks)

Two PostToolUse hooks handle automatic sync:

| Hook                           | Trigger                           | Action                                      |
| ------------------------------ | --------------------------------- | ------------------------------------------- |
| `posttooluse-glossary-sync`    | Edit `~/.claude/docs/GLOSSARY.md` | Sync to Vale vocabulary                     |
| `posttooluse-terminology-sync` | Edit project `CLAUDE.md`          | Merge terms → GLOSSARY.md, detect conflicts |

## Manual Operations

### Sync Glossary to Vale

When automatic sync fails or you need to force a refresh:

```bash
bun ~/.claude/tools/bin/glossary-sync.ts
```

**Output**:

```
=== Glossary Bidirectional Sync ===
  Source: /Users/you/.claude/docs/GLOSSARY.md
  Found 25 acronyms, 24 substitutions
  Updated: .vale/styles/config/vocabularies/TradingFitness/accept.txt
  Total terms: 27
  Updated: .vale/styles/TradingFitness/Terminology.yml
  Substitution rules: 24
  Updated timestamp: 2026-01-22T00:00:00Z
=== Sync Complete ===
```

### Validate Glossary Format

Check that GLOSSARY.md follows the correct table format:

```bash
# Check required columns
grep -E '^\| \*\*[^|]+\*\* \|' ~/.claude/docs/GLOSSARY.md | head -5

# Verify table structure (should have | Term | Acronym | Definition | Unit/Range | Projects |)
head -25 ~/.claude/docs/GLOSSARY.md
```

**Expected format**:

```markdown
| Term                     | Acronym | Definition                  | Unit/Range | Projects    |
| ------------------------ | ------- | --------------------------- | ---------- | ----------- |
| **Time-Weighted Sharpe** | TWSR    | Sharpe ratio for range bars | ratio      | alpha-forge |
```

### Check for Duplicates

Scan all project CLAUDE.md files for terminology conflicts:

```bash
# Full duplicate check (scans ~/eon/*/CLAUDE.md)
bun ~/eon/cc-skills/plugins/itp-hooks/hooks/posttooluse-terminology-sync.ts <<< '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/test-CLAUDE.md"}}'
```

**Conflict types detected**:

- **Definition conflict**: Same term, different definitions
- **Acronym conflict**: Same term, different acronyms
- **Acronym collision**: Same acronym used for different terms

### Add New Term

To add a new term to the glossary:

1. **Edit GLOSSARY.md directly**:

   ```markdown
   | **New Term** | NT | Definition of the new term | - | project-name |
   ```

2. **Sync will auto-trigger** via `posttooluse-glossary-sync` hook

3. **Verify Vale recognizes it**:

   ```bash
   echo "The NT is important" | vale --config=~/.claude/.vale.ini
   ```

## Vale Integration

### Files Generated

| File                                                                   | Purpose                                      |
| ---------------------------------------------------------------------- | -------------------------------------------- |
| `~/.claude/.vale/styles/config/vocabularies/TradingFitness/accept.txt` | Accepted terms (won't be flagged)            |
| `~/.claude/.vale/styles/TradingFitness/Terminology.yml`                | Substitution rules (suggests canonical form) |

### Running Vale

```bash
# Check a single file (run from file's directory for glob patterns to match)
cd ~/eon/trading-fitness && vale --config=~/.claude/.vale.ini CLAUDE.md

# Check all CLAUDE.md files
find ~/eon -name "CLAUDE.md" -exec sh -c 'cd "$(dirname "$1")" && vale --config=~/.claude/.vale.ini "$(basename "$1")"' _ {} \;
```

**Important**: Vale glob patterns in `.vale.ini` (like `[CLAUDE.md]`) are relative to cwd. Always run Vale from the file's directory or use absolute paths with matching glob patterns.

## Troubleshooting

### Terms Not Being Recognized

1. **Check sync timestamp**:

   ```bash
   grep "Last Sync" ~/.claude/docs/GLOSSARY.md
   ```

2. **Force manual sync**:

   ```bash
   bun ~/.claude/tools/bin/glossary-sync.ts
   ```

3. **Verify Vale config path**:

   ```bash
   cat ~/.claude/.vale.ini | grep StylesPath
   ```

### Hook Not Triggering

1. **Check hook is registered**:

   ```bash
   grep "glossary-sync" ~/.claude/settings.json
   ```

2. **Verify hook file exists**:

   ```bash
   ls -la ~/.claude/plugins/marketplaces/cc-skills/plugins/itp-hooks/hooks/posttooluse-glossary-sync.ts
   ```

### Vale Output Shows "0 files" But File Exists

This happens when Vale's glob patterns don't match the file path. The `posttooluse-vale-claude-md.ts` hook handles this by:

1. Walking up from the file's directory to find `.vale.ini`
2. Changing to the file's directory before running Vale
3. Stripping ANSI escape codes for reliable output parsing

If running Vale manually, ensure you're in the file's directory:

```bash
# Wrong - may show "0 files"
vale --config=/path/to/.vale.ini /absolute/path/to/CLAUDE.md

# Correct - cd first
cd /absolute/path/to && vale --config=/path/to/.vale.ini CLAUDE.md
```

### Duplicate Vocabulary Directories

If you see Vale inconsistencies:

```bash
# Check for duplicate vocab dirs (should only have config/vocabularies/)
ls -la ~/.claude/.vale/styles/

# Remove any stale Vocab/ directory
rm -rf ~/.claude/.vale/styles/Vocab/
```

## References

- [Vale Documentation](https://vale.sh/docs/)
- GLOSSARY.md: `~/.claude/docs/GLOSSARY.md` (local file)
- [itp-hooks CLAUDE.md](/plugins/itp-hooks/CLAUDE.md)
