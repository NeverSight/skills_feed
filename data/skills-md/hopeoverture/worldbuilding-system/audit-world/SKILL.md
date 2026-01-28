---
name: audit-world
description: Audit a world for consistency, D&D 5e 2024 rule compliance, broken links, orphaned entities, and connection gaps. Provides detailed reports and can auto-fix issues.
argument-hint: "[world] [--fix] [--check links|stats|orphans|images|circular] [--category Type]"
---

# Audit World

Audit world: $ARGUMENTS

## Overview

This skill performs comprehensive audits on worldbuilding projects to ensure:
- **Entity Linking:** All `[[wikilinks]]` point to real entities
- **Bidirectional Connections:** If A links to B, B should link back to A
- **D&D 5e 2024 Compliance:** Stat blocks are mechanically correct
- **Template Compliance:** Entities use correct templates for their type
- **Orphan Detection:** No entities exist without incoming links
- **Consistency:** Cross-entity references make logical sense

## Instructions

### Step 1: Parse Arguments

Extract from arguments:
1. **World name** - Required. Check `Worlds/` for existing worlds.
2. **--fix flag** - Optional. If present, automatically fix issues where possible.
3. **--category [type]** - Optional. Only audit specific category (Characters, Settlements, etc.)
4. **--check [type]** - Optional. Run specific check only (links, stats, orphans, connections, templates, images, circular)

If world name not provided, list available worlds and ask which to audit.

### Step 2: Scan World Structure

1. **Verify directory structure:**
   ```
   Worlds/[World Name]/
   ├── World Overview.md
   ├── Characters/
   ├── Settlements/
   ├── Items/
   ├── Creatures/
   ├── Organizations/
   ├── Concepts/
   ├── History/
   └── Geography/
   ```

2. **Build entity index:**
   - Scan all `.md` files in the world
   - Extract entity names from filenames
   - Extract entity names from YAML `name:` field
   - Build lookup table: `{entity_name: file_path}`

3. **Count entities by category:**
   ```
   Category        | Count
   ----------------|------
   Characters      | X
   Settlements     | X
   Items           | X
   Creatures       | X
   Organizations   | X
   Concepts        | X
   History         | X
   Geography       | X
   ----------------|------
   TOTAL           | X
   ```

---

## Audit Checks

### Check 1: Wikilink Validation

**Goal:** Verify all `[[Entity Name]]` links point to real entities.

**Process:**
1. For each entity file:
   - Extract all `[[...]]` patterns using regex: `\[\[([^\]]+)\]\]`
   - For each link, check if target exists in entity index
   - Track: `{source_file, broken_link, line_number}`

2. **Ignore false positives:**
   - Links to D&D rules: `[[D&D 5e...]]`, `[[Stat Block...]]`
   - Links to images: `[[...png]]`, `[[...jpg]]`
   - Obsidian system links

3. **Report:**
   ```
   ## Broken Links Report

   Found X broken links across Y entities.

   ### [Entity Name]
   - Line XX: [[Missing Entity 1]]
   - Line XX: [[Missing Entity 2]]

   ### [Entity Name 2]
   ...
   ```

4. **Auto-fix options (if --fix):**
   - Offer to create stub entities for missing links
   - Offer to remove broken links
   - Offer fuzzy match suggestions for typos

---

### Check 2: Bidirectional Connection Audit

**Goal:** Ensure connections are reciprocal.

**Process:**
1. For each entity, extract its `## Connections` section
2. Parse all outgoing links
3. For each outgoing link, check if target links back
4. Track one-way connections

**Reciprocal Relationship Matrix:**

See [[Connection Matrix]] for complete bidirectional linking rules.

| Source Links To | Target Should Have |
|-----------------|-------------------|
| Settlement (as location) | Characters > Residents/Notable NPCs |
| Organization (as member) | Characters > Members |
| Region (as parent) | Settlements/Geography > Contains |
| Deity (as patron) | Characters > Worshippers |
| Character (as ally) | Characters > Allies |
| Character (as enemy) | Characters > Rivals/Enemies |
| Government (as ruler) | Characters > Leadership |
| Settlement (as HQ) | Organizations > Based Here |
| Parent Geography | Child Geography > Part Of |
| Historical Event | Locations > Site Of |
| Military (as army) | Government > Armed Forces |
| Criminal Organization (as operating) | Government > Criminal Elements |
| Creature (as habitat) | Geography > Native Wildlife/Monsters |

**Report:**
```
## One-Way Connection Report

Found X connections missing reciprocal links.

### [Entity A] → [Entity B]
- A links to B in: Connections > Organizations > Member
- B should link back in: Characters > Members
- Status: MISSING

### [Entity C] → [Entity D]
...
```

**Auto-fix (if --fix):**
- Add reciprocal links to target entities
- Use appropriate section based on relationship type

---

### Check 3: D&D 5e 2024 Stat Block Validation

**Goal:** Verify all stat blocks are mechanically correct.

**Applies to:** Characters (Protagonist, Antagonist, Support Character), Creatures (Monster, Animal, Insect)

#### 3-Pre: Stat Block Mode Detection (Characters Only)

Before validating characters, detect which stat block mode they use:

| Condition | Mode | Validation |
|-----------|------|------------|
| `level:` filled, `challenge_rating:` empty | **PC-style** | Use level-based proficiency, class features |
| `challenge_rating:` filled, `level:` empty | **NPC-style** | Use CR-based proficiency, monster rules |
| Both filled | **WARNING** | Ambiguous mode - flag for manual review |
| Neither filled | **WARNING** | Missing stat block info - flag for manual review |

**PC-style validation applies:**
- Proficiency from level (Check 3B)
- HP from class hit dice + CON (Check 3F)
- Spell slots from class progression
- Features match class/subclass

**NPC-style validation applies:**
- Proficiency from CR (Check 3A)
- HP from size hit dice + CON (Check 3F)
- CR/XP correlation (Check 3A)
- Legendary features for high CR (Check 3G)

**Note:** Creatures (Monster, Animal, Insect) always use NPC-style validation with `challenge_rating:`.

---

#### 3A: Challenge Rating & XP

Verify CR matches XP using official table:

| CR | XP | Proficiency |
|----|-----|-------------|
| 0 | 0 or 10 | +2 |
| 1/8 | 25 | +2 |
| 1/4 | 50 | +2 |
| 1/2 | 100 | +2 |
| 1 | 200 | +2 |
| 2 | 450 | +2 |
| 3 | 700 | +2 |
| 4 | 1,100 | +2 |
| 5 | 1,800 | +3 |
| 6 | 2,300 | +3 |
| 7 | 2,900 | +3 |
| 8 | 3,900 | +3 |
| 9 | 5,000 | +4 |
| 10 | 5,900 | +4 |
| 11 | 7,200 | +4 |
| 12 | 8,400 | +4 |
| 13 | 10,000 | +5 |
| 14 | 11,500 | +5 |
| 15 | 13,000 | +5 |
| 16 | 15,000 | +5 |
| 17 | 18,000 | +6 |
| 18 | 20,000 | +6 |
| 19 | 22,000 | +6 |
| 20 | 25,000 | +6 |
| 21 | 33,000 | +7 |
| 22 | 41,000 | +7 |
| 23 | 50,000 | +7 |
| 24 | 62,000 | +7 |
| 25 | 75,000 | +8 |
| 26 | 90,000 | +8 |
| 27 | 105,000 | +8 |
| 28 | 120,000 | +8 |
| 29 | 135,000 | +9 |
| 30 | 155,000 | +9 |

**Check:** `experience_points` in YAML matches CR from table.

#### 3B: Proficiency Bonus

**By Level (Characters):**
| Level | Proficiency |
|-------|-------------|
| 1-4 | +2 |
| 5-8 | +3 |
| 9-12 | +4 |
| 13-16 | +5 |
| 17-20 | +6 |

**By CR (Monsters):** Use CR table above.

**Check:** `proficiency_bonus` matches level/CR.

#### 3C: Ability Modifiers

**Formula:** `modifier = floor((score - 10) / 2)`

| Score | Modifier |
|-------|----------|
| 1 | -5 |
| 2-3 | -4 |
| 4-5 | -3 |
| 6-7 | -2 |
| 8-9 | -1 |
| 10-11 | +0 |
| 12-13 | +1 |
| 14-15 | +2 |
| 16-17 | +3 |
| 18-19 | +4 |
| 20-21 | +5 |
| 22-23 | +6 |
| 24-25 | +7 |
| 26-27 | +8 |
| 28-29 | +9 |
| 30 | +10 |

**Check:** Modifiers in ability score tables are calculated correctly.

#### 3D: Attack Bonuses

**Formula:** `attack_bonus = proficiency_bonus + ability_modifier`
- Melee: Usually STR (or DEX for finesse)
- Ranged: Usually DEX (or STR for thrown)

**Check:** Attack bonus in action descriptions matches formula.

#### 3E: Spell Save DC

**Formula:** `spell_save_DC = 8 + proficiency_bonus + spellcasting_ability_modifier`

| Class | Spellcasting Ability |
|-------|---------------------|
| Bard | Charisma |
| Cleric | Wisdom |
| Druid | Wisdom |
| Paladin | Charisma |
| Ranger | Wisdom |
| Sorcerer | Charisma |
| Warlock | Charisma |
| Wizard | Intelligence |

**Check:** Spell save DC in spellcasting section matches formula.

#### 3F: Hit Points

**Formula for Characters:**
```
HP = (hit_die_max + CON_mod) + ((level - 1) × (hit_die_avg + CON_mod))
```

**Hit Die by Class:**
| Class | Hit Die | Average |
|-------|---------|---------|
| Barbarian | d12 | 7 |
| Fighter, Paladin, Ranger | d10 | 6 |
| Bard, Cleric, Druid, Monk, Rogue, Warlock | d8 | 5 |
| Sorcerer, Wizard | d6 | 4 |

**Formula for Monsters:**
```
HP = hit_dice_count × hit_die_average + (hit_dice_count × CON_mod)
```

**Hit Die by Size:**
| Size | Hit Die | Average |
|------|---------|---------|
| Tiny | d4 | 2.5 |
| Small | d6 | 3.5 |
| Medium | d8 | 4.5 |
| Large | d10 | 5.5 |
| Huge | d12 | 6.5 |
| Gargantuan | d20 | 10.5 |

**Check:** HP matches hit dice formula with CON modifier.

#### 3G: Legendary Features (CR 5+)

For creatures CR 5 and above, check for:
- Legendary Resistance (3/Day) for CR 10+
- Legendary Actions for bosses
- Lair Actions if lair is defined

**Report:**
```
## D&D 5e Stat Block Errors

Found X errors across Y entities.

### [Monster Name] (CR 5)
- ERROR: XP is 1500, should be 1800 for CR 5
- ERROR: Proficiency bonus is +2, should be +3 for CR 5
- WARNING: CR 5+ creature missing Legendary Actions (optional but recommended)

### [Character Name] (Level 8)
- ERROR: Proficiency bonus is +2, should be +3 for level 8
- ERROR: Spell Save DC is 14, should be 15 (8 + 3 + 4)
- ERROR: Attack bonus is +5, should be +7 (proficiency 3 + STR 4)
```

**Auto-fix (if --fix):**
- Recalculate and update XP, proficiency, modifiers
- Update attack bonuses and spell save DCs
- Flag HP for manual review (hit dice formula)

---

### Check 4: Orphan Entity Detection

**Goal:** Find entities with no incoming links.

**Process:**
1. Build incoming link count for each entity
2. Entities with 0 incoming links are orphans
3. Exception: World Overview.md (always root)

**Report:**
```
## Orphan Entities

Found X entities with no incoming links.

### Characters
- [[Forgotten NPC]] - 0 incoming links

### Geography
- [[Unnamed Valley]] - 0 incoming links
```

**Auto-fix (if --fix):**
- Suggest parent entities to link from
- Offer to add to World Overview Quick Reference
- Offer to delete if truly orphaned

---

### Check 5: Template Compliance

**Goal:** Verify entities match their templates.

**Process:**
1. Determine entity type from:
   - File location (folder)
   - YAML tags
   - Content structure

2. Compare against expected template structure:
   - Required YAML fields present
   - Required sections present
   - Section ordering correct

**Template Requirements by Category:**

**Characters (All):**
- YAML: `name`, `status`, `tags` containing character type
- Sections: Overview, Connections

**Characters (Protagonist/Antagonist/Support Character):**
- YAML: `species`, `class`, `armor_class`, `hit_points`
- YAML (Stat Block Mode): `level` OR `challenge_rating` (one required, not both)
- Sections: Stat Block, Ability Scores, Combat Statistics, Personality, Background

**Creatures (Monster):**
- YAML: `size`, `creature_type`, `challenge_rating`, `experience_points`
- Sections: Stat Block, Classification, Ability Scores, Traits, Actions

**Settlements:**
- YAML: `settlement_type`, `population`, `government_type`
- Sections: Overview, Districts/Areas, Notable Locations

**Organizations:**
- YAML: `organization_type` or appropriate tag
- Sections: Overview, Leadership, Goals, Resources

**Geography:**
- YAML: `terrain_type` or geographic tag
- Sections: Overview, Features, Inhabitants

**Report:**
```
## Template Compliance Issues

Found X compliance issues across Y entities.

### [Entity Name] (Characters/Protagonist.md)
- AMBIGUOUS YAML: Both `level` and `challenge_rating` are filled (use only one)
- MISSING SECTION: ## Ability Scores
- WRONG FOLDER: Located in Items/, should be Characters/

### [Entity Name] (Characters/Antagonist.md)
- MISSING YAML: Neither `level` nor `challenge_rating` (one required for stat block)
- WARNING: Cannot validate proficiency bonus without level/CR

### [Entity Name] (Settlements/City.md)
- MISSING YAML: `population`
- EMPTY SECTION: ## Districts
```

**Auto-fix (if --fix):**
- Add missing YAML fields with placeholder values
- Add missing section headers
- Suggest moving misplaced files

---

### Check 6: Cross-Entity Consistency

**Goal:** Verify logical consistency across entities.

**Checks:**

1. **Religious Consistency:**
   - Temples reference deities that exist
   - Religious orders serve established deities
   - Characters with deity patrons link to real deities

2. **Political Consistency:**
   - Settlements reference governments that exist
   - Military organizations belong to real governments
   - Rulers are linked to their domains

3. **Geographic Consistency:**
   - Settlements are in regions that exist
   - Rivers flow from mountains to bodies of water
   - Roads connect real settlements
   - Terrain types match climate of parent region

4. **Historical Consistency:**
   - Events reference locations that exist
   - Battles are part of wars that exist
   - Dynasties connect to governments
   - Characters in historical events existed at that time

5. **Economic Consistency:**
   - Currency matches issuing government
   - Trade agreements connect trading partners
   - Shops sell goods appropriate to region

**Report:**
```
## Cross-Entity Consistency Issues

### Religious Inconsistencies
- Temple of [[Nonexistent God]] references deity not in pantheon
- Religious Order [[Knights of X]] serves [[Y]] but Y's domain doesn't match order purpose

### Political Inconsistencies
- [[City A]] claims to be capital of [[Kingdom B]] but B lists different capital
- [[Military X]] serves [[Government Y]] but Y doesn't list X in armed forces

### Geographic Inconsistencies
- [[River A]] claims to flow from [[Desert B]] (deserts don't have river sources)
- [[Settlement A]] is in [[Region B]] but B's climate is tundra, A's description is tropical
```

---

### Check 7: Image Prompt Validation

**Goal:** Verify image prompt sections are properly filled for `/generate-image` readiness.

**Process:**
1. For each entity file, locate the Image Prompts section (usually near the end)
2. Find all `**Prompt:**` fields
3. Check if they contain actual content vs template placeholders

**Template Placeholder Patterns to Detect:**
- Empty field: `**Prompt:**` followed by nothing or whitespace
- Unfilled brackets: `**Prompt:** [describe scene here]`
- Generic text: `**Prompt:** Describe the scene...`
- Template instructions: `**Prompt:** Write a detailed prompt for...`

**Valid Prompt Patterns:**
- Specific descriptions: `**Prompt:** A weathered dwarven blacksmith...`
- Detailed scenes: `**Prompt:** Interior of a dimly lit tavern...`
- Minimum 20 characters of descriptive content

**Report:**
```
## Image Prompt Status

### Ready for Image Generation
| Entity | Prompts Filled | Status |
|--------|----------------|--------|
| [[Lord Varic]] | 2/2 | ✓ Ready |
| [[Ironhold City]] | 2/2 | ✓ Ready |

### Missing or Incomplete Prompts
| Entity | Issue | Line |
|--------|-------|------|
| [[The Sunken Palace]] | Empty prompt field | 245 |
| [[Captain Alonzo]] | Placeholder text only | 189 |
| [[Mountain Pass]] | Missing Image Prompts section | - |

Summary:
- Entities with complete prompts: X
- Entities with incomplete prompts: Y
- Entities missing Image Prompts section: Z
```

**Auto-fix (if --fix):**
- Cannot auto-fill image prompts (requires creative content)
- Flag entities needing attention
- Suggest running `/create-entity` to regenerate Image Prompts section

---

### Check 8: Circular Reference Detection

**Goal:** Detect potentially problematic circular reference chains.

**Process:**
1. Build a directed graph of entity relationships
2. For each relationship type, check for cycles
3. Categorize cycles as valid (expected) or warning (potential error)

**Valid Circular Patterns:**
| Pattern | Example | Why Valid |
|---------|---------|-----------|
| Mutual relationship | A → B (ally), B → A (ally) | Symmetric relationship |
| Parent-child | Region → City (contains), City → Region (part of) | Bidirectional by design |
| Organization loop | Org → Member, Member → Org | Membership is bidirectional |

**Warning Patterns:**
| Pattern | Example | Why Problematic |
|---------|---------|-----------------|
| Geographic containment loop | A contains B contains C contains A | Impossible geography |
| Temporal causation loop | Event A caused B caused C caused A | Paradox |
| Hierarchical loop | God A serves B serves C serves A | Impossible hierarchy |
| "Part of" chain loop | Region A part of B part of C part of A | Invalid nesting |

**Detection Algorithm:**
```
1. Extract relationships by type:
   - containment: "contains", "part of", "in"
   - hierarchy: "serves", "reports to", "rules"
   - causation: "caused", "led to", "resulted in"
   - temporal: "before", "after", "during"

2. For each relationship type:
   - Build directed graph
   - Run cycle detection (DFS-based)
   - Classify each cycle found

3. Report cycles by severity
```

**Report:**
```
## Circular Reference Analysis

### Valid Bidirectional Links: X
(These are expected and correct)

### Warning: Potential Problematic Cycles

#### Geographic Containment Loop
[[Region A]] → contains → [[Region B]] → contains → [[Region C]] → contains → [[Region A]]
Severity: HIGH - Geographic impossibility
Suggestion: Review containment relationships; one link is likely incorrect

#### Hierarchical Loop
[[Organization X]] → parent of → [[Organization Y]] → parent of → [[Organization X]]
Severity: MEDIUM - Circular hierarchy
Suggestion: Determine which org is truly the parent

No auto-fix available for circular references - requires manual review.
```

---

## Summary Report

After all checks, provide comprehensive summary:

```
# World Audit Report: [World Name]

## Overview
- **Total Entities:** X
- **Audit Date:** YYYY-MM-DD
- **Issues Found:** X (Y critical, Z warnings)

## Entity Count
| Category | Count | Issues |
|----------|-------|--------|
| Characters | X | Y |
| Settlements | X | Y |
| Items | X | Y |
| Creatures | X | Y |
| Organizations | X | Y |
| Concepts | X | Y |
| History | X | Y |
| Geography | X | Y |
| **TOTAL** | **X** | **Y** |

## Issue Summary

### Critical Issues (Must Fix)
| Issue Type | Count | Example |
|------------|-------|---------|
| Broken Links | X | [[Missing Entity]] in Entity.md |
| Stat Block Errors | X | Wrong XP for CR in Monster.md |
| Orphan Entities | X | Forgotten NPC.md |

### Warnings (Should Review)
| Issue Type | Count | Example |
|------------|-------|---------|
| One-Way Links | X | A→B without B→A |
| Missing Sections | X | No Connections in Entity.md |
| Consistency Issues | X | Temple references wrong deity |

## Connection Statistics
- **Total Wikilinks:** X
- **Average Links Per Entity:** X.X
- **Most Connected Entity:** [[Entity]] (X links)
- **Least Connected Entity:** [[Entity]] (X links)

## Recommendations

### High Priority
1. Fix X broken links in Y entities
2. Add reciprocal links for Z one-way connections
3. Correct stat block errors in W creatures

### Medium Priority
1. Review X orphan entities for relevance
2. Fill missing sections in Y entities
3. Resolve Z consistency issues

### Low Priority
1. Increase connections in sparse entities
2. Add missing optional YAML fields
3. Consider additional entities for coverage gaps

## Next Steps
- Run `/audit-world [world] --fix` to auto-repair issues
- Use `/create-entity` to fill coverage gaps
- Review orphan entities for deletion or integration
```

---

## Auto-Fix Mode (--fix)

When `--fix` is specified:

1. **Ask before each fix category:**
   - "Found X broken links. Fix by creating stubs? (y/n)"
   - "Found X one-way connections. Add reciprocal links? (y/n)"
   - "Found X stat errors. Auto-correct calculations? (y/n)"

2. **Create backup before modifying:**
   - Copy modified files to `.audit-backup/` folder
   - Log all changes made

3. **Report changes:**
   ```
   ## Auto-Fix Results

   ### Files Modified: X
   - Entity1.md: Added 3 reciprocal links
   - Entity2.md: Corrected XP (1500 → 1800)
   - Entity3.md: Added missing YAML fields

   ### Files Created: X
   - Missing Entity (stub).md: Created from broken link

   ### Backup Location: .audit-backup/[timestamp]/
   ```

---

## Rollback & Restore Procedure

If auto-fix made unwanted changes, you can restore from backup:

### Backup Structure

```
Worlds/[World Name]/.audit-backup/
└── [YYYY-MM-DD_HH-MM-SS]/
    ├── manifest.json         # List of all modified files
    ├── Characters/
    │   └── [backed up files]
    ├── Settlements/
    │   └── [backed up files]
    └── ...
```

### Manual Restore Steps

1. **Find the backup timestamp:**
   ```bash
   ls Worlds/[World Name]/.audit-backup/
   ```

2. **Review what was changed:**
   Read the manifest file to see what was modified:
   ```bash
   cat Worlds/[World Name]/.audit-backup/[timestamp]/manifest.json
   ```

3. **Restore specific files:**
   ```bash
   # Copy backed up file over current version
   cp "Worlds/[World Name]/.audit-backup/[timestamp]/Characters/Lord Varic.md" \
      "Worlds/[World Name]/Characters/Lord Varic.md"
   ```

4. **Restore all files from a backup:**
   ```bash
   # Restore entire backup (overwrite current files)
   cp -r "Worlds/[World Name]/.audit-backup/[timestamp]/"* "Worlds/[World Name]/"
   ```

### Backup Retention

- Backups are kept for 7 days by default
- Each `--fix` run creates a new timestamped backup
- Old backups can be manually deleted from `.audit-backup/`

### Partial Restore

To restore only certain changes:

1. Open the backed-up file
2. Compare with current file (use diff tool or Obsidian)
3. Manually copy specific sections you want to restore

---

## Integration with Other Skills

### After `/generate-world`
Run `/audit-world [world]` to:
- Verify all generated entities are linked
- Check stat blocks on generated monsters
- Ensure no orphans from generation

### After `/create-entity`
Reciprocal link logic in create-entity should prevent most issues, but audit can catch edge cases.

### Before `/generate-image`
Audit can verify image prompt sections are filled before batch image generation.

---

## Usage Examples

```
# Full audit
/audit-world Eldoria

# Audit with auto-fix
/audit-world Eldoria --fix

# Only check links
/audit-world Eldoria --check links

# Only check D&D stats
/audit-world Eldoria --check stats

# Only audit Characters
/audit-world Eldoria --category Characters

# Combination
/audit-world Eldoria --category Creatures --check stats --fix
```
