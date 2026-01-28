---
name: linkify
description: Automatically add [[wikilinks]] to all mentions of existing entities within a file or entire world. Scans for entity names, aliases, and partial matches, then wraps them in wikilink syntax. Use when user wants to "linkify", "auto-link", "add links to existing entities", or "wikilink this file".
argument-hint: "[entity or --world WorldName] [--dry-run] [--category Type]"
---

# Linkify Entity

Linkify: $ARGUMENTS

## Overview

This skill scans an entity file and automatically wraps any mentions of existing entities in `[[wikilink]]` syntax. It's a focused tool that only adds links to entities that already exist—it does NOT create new entities.

## Quick Start

```bash
# Linkify a specific entity
/linkify "Aldersgate"

# Preview changes without modifying
/linkify "Aldersgate" --dry-run

# Linkify by file path
/linkify Worlds/Eldermyr/Settlements/Aldersgate.md

# BULK: Linkify all entities in a world
/linkify --world Eldermyr

# BULK: Linkify only Characters in a world
/linkify --world Eldermyr --category Characters

# BULK: Preview bulk changes
/linkify --world Eldermyr --dry-run
```

## Instructions

### Step 1: Parse Arguments

**Required:**
- Entity path or name

**Optional Flags:**
| Flag | Purpose | Default |
|------|---------|---------|
| `--dry-run` | Show what would be linked without making changes | false |
| `--all-worlds` | Search all worlds for entities, not just the source entity's world | false |
| `--case-sensitive` | Require exact case matching | false |
| `--world [name]` | **BULK MODE:** Process all entities in the specified world | - |
| `--category [type]` | With `--world`: only process entities in this category (Characters, Settlements, etc.) | all |

### Step 2: Locate Entity & Determine World

1. **If path provided** (contains `/` or `.md`):
   - Read the file directly
   - Extract world name from path: `Worlds/[World Name]/...`

2. **If name provided**:
   - Search `Worlds/` directories for matching entity
   - Try exact filename match first
   - Then fuzzy match on filename and YAML `name:` field
   - If multiple matches, list them and ask user to clarify

3. **If not found**:
   - List similar entities and ask for clarification

### Step 3: Build Entity Index

Create a complete index of existing entities:

1. **Scan all files** in `Worlds/[World Name]/` recursively (or all worlds if `--all-worlds`)
2. **For each entity file**, extract:
   - Filename (without .md extension) → primary name
   - YAML `name:` field → canonical name
   - YAML `aliases:` array → alternative names
3. **Build lookup dictionary** (case-insensitive by default):

```
{
  "Lord Varic Valdren": { path: "Characters/Lord Varic Valdren.md", canonical: "Lord Varic Valdren" },
  "Varic": { path: "Characters/Lord Varic Valdren.md", canonical: "Lord Varic Valdren" },
  "The Merchant Lord": { path: "Characters/Lord Varic Valdren.md", canonical: "Lord Varic Valdren" },
  ...
}
```

**Important:** Sort the lookup dictionary by name length (longest first) to ensure longer matches are found before shorter partial matches.

### Step 4: Identify Content to Scan

Read the source entity file and identify sections to scan:

**INCLUDE these sections:**
- Overview
- Geography
- History
- Demographics
- Government & Politics
- Economy
- Defense & Military
- Notable Locations
- Key Figures
- Secrets
- Plot Hooks
- Description
- Any custom content sections

**EXCLUDE these sections:**
- YAML frontmatter (between `---` markers)
- Image Prompts section and everything after it
- Connections section (already has wikilinks)
- Code blocks (between ``` markers)
- Existing wikilinks `[[...]]`
- Block quotes used for image prompts (lines starting with `>` after `**Prompt:**`)

### Step 5: Find Matches

For each entity name/alias in the index (longest first):

1. **Skip if entity is the source file itself** (don't self-link)

2. **Search for the name in content:**
   - Use word-boundary matching to avoid partial matches within words
   - Match: "Lord Varic Valdren" in "talked to Lord Varic Valdren about"
   - Skip: "Lord Varic Valdren" in "[[Lord Varic Valdren]]" (already linked)
   - Skip: "Stone" in "Aldric Stone" if "Aldric Stone" is a separate entity

3. **Record each match:**
   - Line number
   - Exact text matched
   - Canonical entity name (for the wikilink)
   - Surrounding context (5 words before/after)

4. **Handle partial name matches:**
   - If "Lord Varic Valdren" exists but text says "Lord Varic", offer to link as `[[Lord Varic Valdren|Lord Varic]]`
   - If "House Valdren" exists but text says "the Valdren house", consider display text

### Step 6: Present Findings

```
=== LINKIFY ANALYSIS: [Entity Name] ===

World: [World Name]
Source: [path/to/entity.md]
Entities Indexed: X

---

MATCHES FOUND: Y

| # | Text Found | Line | Links To | Context |
|---|------------|------|----------|---------|
| 1 | Lady Serana Valdren | 121 | [[Lady Serana Valdren]] | "...wife, manages court..." |
| 2 | High Confessor Maren | 136 | [[High Confessor Maren]] | "...supporters, seeking..." |
| 3 | Sister Elspeth | 204 | [[Sister Elspeth]] | "...Abbess of the..." |
| 4 | Lord Varic | 117 | [[Lord Varic Valdren|Lord Varic]] | "...ensuring Varic holds..." |

---

PARTIAL MATCHES (display text needed):

| # | Text Found | Line | Suggested Link |
|---|------------|------|----------------|
| 1 | "the Owl" | 123 | [[The Owl|the Owl]] |
| 2 | "young Edric" | 117, 177 | [[Edric Valdren|young Edric]] |

---

AMBIGUOUS (multiple possible matches):

| # | Text Found | Line | Could Match |
|---|------------|------|-------------|
| 1 | "Edric" | 177 | [[Edric Valdren]] or [[Prince Edric the Liberator]] |

---

SUMMARY:
- Exact matches: X
- Partial matches: X
- Ambiguous: X
- Total changes: X

Options:
1. Apply all exact matches
2. Apply exact + partial matches
3. Review each individually
4. Dry run complete (--dry-run flag)
```

If `--dry-run` flag is set, show report and stop.

### Step 7: Apply Changes

For each approved match:

1. **Build replacement text:**
   - Exact match: `EntityName` → `[[EntityName]]`
   - Partial match: `PartialName` → `[[FullEntityName|PartialName]]`

2. **Apply using Edit tool:**
   - Process from bottom of file to top (so line numbers don't shift)
   - Use precise string replacement with surrounding context for uniqueness
   - Verify each replacement succeeded

3. **Handle duplicates:**
   - If the same entity is mentioned multiple times, link ALL occurrences
   - Exception: Don't link the same name twice in the same sentence

### Step 8: Validation

After applying changes:

1. Re-read the file
2. Verify all intended wikilinks are present
3. Check no content was accidentally corrupted
4. Verify wikilinks point to existing files

### Step 9: Summary Report

```
=== LINKIFY COMPLETE: [Entity Name] ===

Changes Applied: X

Links Added:
- [[Lady Serana Valdren]] (line 121)
- [[High Confessor Maren]] (line 136)
- [[Sister Elspeth]] (lines 204, 252)
- [[Lord Varic Valdren|Lord Varic]] (line 117)

Skipped (ambiguous):
- "Edric" (line 177) - multiple matches possible

---

File Updated: [path/to/entity.md]

Suggested Next Steps:
- Review ambiguous matches manually
- Run /audit-world to check bidirectional links
- Use /link-entities to add reciprocal connections
```

## Matching Rules

### Word Boundary Matching

Only match complete words/phrases:

| Text | Entity | Match? | Reason |
|------|--------|--------|--------|
| "spoke to Lord Varic Valdren about" | Lord Varic Valdren | Yes | Complete phrase |
| "the Valdren family" | House Valdren | No | "Valdren" alone, different entity |
| "visited Aldersgate" | Aldersgate | Yes | Complete word |
| "Aldersgates" | Aldersgate | No | Different word |
| "[[Lord Varic Valdren]]" | Lord Varic Valdren | No | Already linked |

### Partial Name Handling

When text contains a shorter form of an entity name:

| Text | Entity | Link Format |
|------|--------|-------------|
| "Lord Varic said" | Lord Varic Valdren | `[[Lord Varic Valdren|Lord Varic]]` |
| "the Owl knows" | The Owl | `[[The Owl|the Owl]]` |
| "young Edric" | Edric Valdren | `[[Edric Valdren|young Edric]]` |

### Case Handling

By default (case-insensitive):
- "lord varic valdren" matches "Lord Varic Valdren"
- Original case is preserved in display text

With `--case-sensitive`:
- Only exact case matches

### Exclusion Patterns

Never link:
- Text inside existing `[[wikilinks]]`
- Text in YAML frontmatter
- Text in code blocks
- Text in Image Prompts section
- The entity's own name (no self-linking)
- Text that's part of a markdown header (`# Name`)
- Text in the Connections section (manage links there separately)

## Bulk Processing Mode

When `--world` flag is provided, the skill processes multiple entities:

### Bulk Mode Workflow

1. **Scan world directory:**
   - List all `.md` files in `Worlds/[World Name]/`
   - If `--category` specified, only scan that folder (e.g., `Characters/`)
   - Exclude `World Overview.md` by default (use `--include-overview` to include)

2. **Build combined entity index:**
   - Same process as single-entity mode
   - Index is built once and reused for all files

3. **Process each entity:**
   - For each file, run Steps 4-7 (Find Matches → Apply Changes)
   - Track cumulative statistics

4. **Batch report:**
   ```
   === BULK LINKIFY COMPLETE: [World Name] ===

   Files Processed: X
   Files Modified: Y
   Files Unchanged: Z

   Total Links Added: N

   By Category:
   - Characters: X files, Y links
   - Settlements: X files, Y links
   - Organizations: X files, Y links
   ...

   Skipped (ambiguous): N references across M files

   Performance: X.X seconds total
   ```

### Bulk Mode Options

```bash
# Process entire world
/linkify --world Eldermyr

# Process only one category
/linkify --world Eldermyr --category Settlements

# Dry run to preview bulk changes
/linkify --world Eldermyr --dry-run

# Process multiple categories
/linkify --world Eldermyr --category Characters --category Organizations
```

### Performance Notes

For large worlds (100+ entities), bulk mode:
- Builds the entity index once (faster than per-file)
- Processes files in parallel where possible
- Reports progress every 10 files
- For very large worlds (300+), consider using `scripts/linkify_world.py` instead

## Examples

```bash
# Basic linkify
/linkify "Aldersgate"

# Preview what would be linked
/linkify "Aldersgate" --dry-run

# Linkify checking all worlds for entities
/linkify "Aldersgate" --all-worlds

# Linkify by path
/linkify Worlds/Eldermyr/Settlements/Aldersgate.md

# Case-sensitive matching
/linkify "Lord Varic Valdren" --case-sensitive
```

## Integration with Other Skills

### After `/create-entity`
Run `/linkify` on newly created entities to link any mentioned existing entities.

### Before `/audit-world`
Run `/linkify` on key entities to add missing links before the audit.

### With `/link-entities`
- `/linkify` adds wikilinks within entity content
- `/link-entities` manages the Connections section relationships
- Use together for comprehensive linking

### With `/populate-entity`
- `/linkify` only links to EXISTING entities
- `/populate-entity --links-only` does the same thing
- `/populate-entity` (full) also CREATES missing entities
- Use `/linkify` when you just want to add links without creating anything

## Error Handling

**File not found:**
```
Error: Could not find entity "[name]"
Similar entities in Worlds/:
- [similar1]
- [similar2]
Please specify the full path or exact name.
```

**No matches found:**
```
=== LINKIFY: [Entity Name] ===

No unlinked entity references found.

This file either:
- Already has all entities properly linked
- Contains no references to other known entities
- References entities that don't exist yet (use /populate-entity to create them)
```

**Write permission error:**
```
Error: Could not write to [path]
The dry-run showed X matches. Please check file permissions.
```
