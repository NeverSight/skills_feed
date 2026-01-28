---
name: validate-template
description: Validate a template or entity file has all required sections, YAML fields, and follows the worldbuilding system conventions. Use when creating new templates or checking if entities are properly structured.
argument-hint: "[template or entity path] [--fix] [--template-type Type]"
---

# Validate Template

Validate: $ARGUMENTS

## Overview

This skill validates that templates and entity files conform to the worldbuilding system standards:
- Required YAML frontmatter fields are present
- Required sections exist
- Image Prompts section is properly formatted
- Connections section has correct structure
- Content follows directive patterns

## Instructions

### Parse Arguments

| Argument | Purpose |
|----------|---------|
| `[path]` | Path to template or entity file |
| `--fix` | Auto-fix simple issues (add missing sections) |
| `--template-type [Type]` | Force validation as specific type |
| `--all-templates` | Validate all templates in Templates/ |
| `--all-entities [world]` | Validate all entities in a world |

---

## Validation Rules

### Universal Requirements (All Files)

#### YAML Frontmatter
Every file must have:

```yaml
---
tags:
  - [category tag]
name: "[Entity Name]"
aliases:
  - [optional aliases]
status: draft | in-progress | complete
image: "" | "[[Entity Name.png]]"
---
```

**Checks:**
- [ ] YAML block exists (between `---` markers)
- [ ] `tags:` field exists and is non-empty array
- [ ] `name:` field exists and is non-empty string
- [ ] `aliases:` field exists (can be empty array)
- [ ] `status:` field exists with valid value
- [ ] `image:` field exists

#### Title Section
```markdown
# {{title}}
```
or
```markdown
# [Entity Name]
```

**Checks:**
- [ ] H1 heading exists as first content line after YAML
- [ ] Only one H1 heading in file

#### Connections Section
```markdown
## Connections

### [Category]
- **[Relationship]:** [[Entity]]
```

**Checks:**
- [ ] `## Connections` section exists
- [ ] At least one subsection with wikilinks
- [ ] Wikilinks use proper format `[[Entity Name]]`

#### Image Prompts Section
```markdown
## Image Prompts

### [Art Style]
[Style description]

### [Scene Type]
[Scene setup]

**Prompt:** [Filled prompt text]
```

**Checks:**
- [ ] `## Image Prompts` section exists (for most entity types)
- [ ] At least one subsection with `**Prompt:**` field
- [ ] `**Prompt:**` field contains actual content (not placeholder)

---

### Category-Specific Requirements

#### Characters (Protagonist, Antagonist, Support Character)

**Additional YAML:**
```yaml
species: "[species]"
class: "[class]"
level: [number]           # OR
challenge_rating: "[CR]"  # (one required, not both)
armor_class: [number]
hit_points: [number]
proficiency_bonus: [number]
```

**Additional Sections:**
- [ ] `## Stat Block`
- [ ] `### Ability Scores`
- [ ] `## Personality`
- [ ] `## Background`
- [ ] `## Combat Statistics`

**Validation Notes:**
- Either `level:` OR `challenge_rating:` must be filled (not both, not neither)
- Proficiency bonus must match level/CR per D&D 5e 2024 rules

#### Settlements (Village, Town, City, Stronghold)

**Additional YAML:**
```yaml
settlement_type: "[type]"
population: "[range]"
government_type: "[type]"
```

**Additional Sections:**
- [ ] `## Overview`
- [ ] `## Districts` or `## Areas`
- [ ] `## Notable Locations`

#### Organizations

**Additional YAML:**
```yaml
organization_type: "[type]"  # or appropriate tag
```

**Additional Sections:**
- [ ] `## Overview`
- [ ] `## Leadership`
- [ ] `## Goals`
- [ ] `## Resources`

#### Creatures (Monster, Animal, Insect)

**Additional YAML:**
```yaml
size: "[size]"
creature_type: "[type]"
challenge_rating: "[CR]"
experience_points: [number]
```

**Additional Sections:**
- [ ] `## Stat Block`
- [ ] `### Classification`
- [ ] `### Ability Scores`
- [ ] `## Traits`
- [ ] `## Actions`

#### Geography

**Additional YAML:**
```yaml
terrain_type: "[type]"  # or appropriate geographic tag
```

**Additional Sections:**
- [ ] `## Overview`
- [ ] `## Features`
- [ ] `## Inhabitants`

#### Items

**Additional YAML:**
```yaml
rarity: "[rarity]"
item_type: "[type]"
```

**Additional Sections:**
- [ ] `## Description`
- [ ] `## Properties`

#### History (Event, Age, War, Battle)

**Additional YAML:**
```yaml
date: "[date or era]"
```

**Additional Sections:**
- [ ] `## Overview`
- [ ] `## Causes`
- [ ] `## Key Figures`
- [ ] `## Consequences`

---

## Validation Report

```
=== VALIDATION REPORT: [File Name] ===

Template Type: [Detected or Specified]
Category: [Category]

YAML FRONTMATTER
─────────────────────────────────────
✓ tags: present (3 tags)
✓ name: present ("Lord Varic Valdren")
✓ aliases: present (2 aliases)
✓ status: present (in-progress)
✓ image: present (empty - needs image)
✓ species: present ("Human")
✓ class: present ("Fighter")
✓ level: present (8)
✗ challenge_rating: N/A (using level-based)
✓ armor_class: present (18)
✓ hit_points: present (75)
✓ proficiency_bonus: present (+3) ✓ Matches level 8

REQUIRED SECTIONS
─────────────────────────────────────
✓ # Title (line 15)
✓ ## Stat Block (line 20)
✓ ### Ability Scores (line 25)
✓ ## Personality (line 60)
✓ ## Background (line 80)
✓ ## Combat Statistics (line 45)
✓ ## Connections (line 200)
✓ ## Image Prompts (line 230)

IMAGE PROMPTS
─────────────────────────────────────
✓ ### Portrait found
  ✓ **Prompt:** filled (45 characters)
✓ ### Action Scene found
  ✗ **Prompt:** EMPTY or placeholder

CONNECTIONS
─────────────────────────────────────
✓ Has wikilinks in Connections section
  - [[Lady Serana Valdren]]
  - [[House Valdren]]
  - [[Aldersgate]]

SUMMARY
─────────────────────────────────────
Checks Passed: 18/20
Checks Failed: 2
Warnings: 1

ISSUES FOUND:
1. [ERROR] Image Prompt for "Action Scene" is empty (line 245)
2. [WARNING] image: field is empty (entity has no generated image)

RECOMMENDATIONS:
- Fill the Action Scene prompt before running /generate-image
- Run /generate-image after filling prompts
```

---

## Auto-Fix Mode (--fix)

When `--fix` is specified, the skill can automatically fix:

| Issue | Auto-Fix Action |
|-------|-----------------|
| Missing YAML field | Add field with placeholder value |
| Missing required section | Add section header with TODO comment |
| Missing Connections section | Add empty Connections section |
| Missing Image Prompts section | Add template Image Prompts section |
| Empty aliases array | Add `aliases: []` |

**Cannot auto-fix:**
- Missing content in sections
- Empty image prompts (requires creative content)
- Incorrect stat block values
- Missing wikilinks

---

## Bulk Validation

### Validate All Templates

```bash
/validate-template --all-templates
```

Report:
```
=== TEMPLATE VALIDATION: Templates/ ===

Category             | Files | Valid | Issues |
---------------------|-------|-------|--------|
Characters           | 6     | 6     | 0      |
Settlements          | 8     | 7     | 1      |
Items                | 11    | 11    | 0      |
Creatures            | 5     | 5     | 0      |
Organizations        | 9     | 9     | 0      |
Concepts             | 10    | 9     | 1      |
History              | 9     | 9     | 0      |
Geography            | 18    | 18    | 0      |
Encounters           | 4     | 4     | 0      |
Maps                 | 4     | 4     | 0      |
---------------------|-------|-------|--------|
TOTAL                | 84    | 82    | 2      |

FILES WITH ISSUES:
- Templates/Settlements/Tavern.md: Missing ## Notable NPCs section
- Templates/Concepts/Religion.md: Empty image prompt
```

### Validate All Entities in World

```bash
/validate-template --all-entities Eldermyr
```

Report:
```
=== ENTITY VALIDATION: Worlds/Eldermyr/ ===

Category             | Files | Valid | Issues |
---------------------|-------|-------|--------|
Characters           | 12    | 10    | 2      |
Settlements          | 8     | 8     | 0      |
...

ENTITIES WITH ISSUES:
- Characters/Old Merchant.md: Missing level OR challenge_rating
- Characters/Guard Captain.md: Proficiency +2 doesn't match level 7
```

---

## Integration with Other Skills

### Before `/create-template`
Run validation on similar templates to understand the expected structure.

### After `/create-entity`
Run validation to ensure generated entity meets all requirements.

### With `/audit-world`
Validation is complementary to audit:
- `/validate-template` checks structure and format
- `/audit-world` checks content consistency and links

---

## Examples

```bash
# Validate a single entity
/validate-template "Worlds/Eldermyr/Characters/Lord Varic Valdren.md"

# Validate and auto-fix issues
/validate-template "Worlds/Eldermyr/Characters/Lord Varic Valdren.md" --fix

# Validate as specific type
/validate-template "some-file.md" --template-type "Support Character"

# Validate all templates
/validate-template --all-templates

# Validate all entities in a world
/validate-template --all-entities Eldermyr

# Validate with auto-fix
/validate-template --all-entities Eldermyr --fix
```
