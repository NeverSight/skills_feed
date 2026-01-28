---
name: populate-entity
description: Scan an entity file to identify mentions of people, places, organizations, and other entities in the text. Creates missing entities using appropriate templates and adds wikilinks. Use when user wants to "populate", "fill out", "create linked entities", or "auto-generate connections" for an entity.
argument-hint: "[entity or --world WorldName] [--dry-run] [--auto] [--limit N]"
---

# Populate Entity

Populate this entity: $ARGUMENTS

## Overview

This skill analyzes an existing entity file to:
1. Identify plain text that should become wikilinks (names of people, places, organizations)
2. Find existing wikilinks that point to non-existent entities
3. Create all missing entities using appropriate templates
4. Update the source entity with proper wikilinks
5. Ensure bidirectional connections

## Instructions

### Step 1: Parse Arguments

**Required:**
- Entity path or name

**Optional Flags:**
| Flag | Purpose | Default |
|------|---------|---------|
| `--dry-run` | Show what would be created without making changes | false |
| `--auto` | Skip confirmations, use best-guess entity types | false |
| `--limit N` | Maximum number of entities to create | 20 |
| `--broken-only` | Only fix broken wikilinks, skip plain text detection | false |
| `--links-only` | Only add wikilinks to existing entities, don't create new | false |
| `--world [name]` | **BULK MODE:** Process all entities in the specified world | - |
| `--category [type]` | With `--world`: only process entities in this category | all |

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

**The world name is required** for knowing where to save new entities.

### Step 3: Build Entity Index

Before analysis, create a complete index of existing entities in the world:

1. **Scan all files** in `Worlds/[World Name]/` recursively
2. **For each entity file**, extract:
   - Filename (without .md extension)
   - YAML `name:` field
   - YAML `aliases:` array
   - File path
3. **Build lookup dictionary** (case-insensitive):
   ```
   {
     "entity name": "path/to/entity.md",
     "alias1": "path/to/entity.md",
     ...
   }
   ```

This index is used to:
- Avoid creating duplicate entities
- Detect existing entities mentioned as plain text
- Verify wikilinks point to real files

### Step 4: Analyze Source Entity

Read the source entity file and perform three analyses:

#### 4A: Extract Existing Wikilinks

Use regex pattern: `\[\[([^\]|]+)(?:\|[^\]]+)?\]\]`

For each wikilink found:
1. Extract the entity name (handling `[[Name|Display]]` format)
2. Check if it exists in the entity index
3. If not found, mark as **broken link**
4. Track line numbers for reporting

#### 4B: Identify Potential Entity References

Scan the entity content (excluding YAML frontmatter, code blocks, and Image Prompts section) for proper noun patterns:

**High-Confidence Patterns:**

| Pattern | Entity Type | Example |
|---------|-------------|---------|
| Lord/Lady [Name] | Character | "Lord Varic", "Lady Serana" |
| King/Queen [Name] | Character | "King Aldric", "Queen Elara" |
| Prince/Princess [Name] | Character | "Prince Edric" |
| Sir/Dame [Name] | Character | "Sir Galahad" |
| Captain/Commander [Name] | Character | "Captain Alonzo" |
| High Priest/Confessor [Name] | Character | "High Confessor Maren" |
| Elder/Master [Name] | Character | "Elder Thorne" |
| House [Name] | Organization | "House Valdren" |
| Clan [Name] | Organization | "Clan Ironforge" |
| Guild/Order [Name] | Organization | "Guild of Merchants" |
| The [Name] + (River/Sea/Forest/Mountain) | Geography | "The Trader's Sea" |
| [Name] River/Stream | Geography (River) | "Valdris River" |
| [Name] Mountain(s)/Range/Peak(s) | Geography (Mountain) | "Sundered Peaks" |
| [Name] Forest/Wood(s)/Grove | Geography (Forest) | "Whisperwood Forest" |
| [Name] Sea/Ocean | Geography (Ocean) | "The Eastern Sea" |
| [Name] Lake/Pond | Geography (Lake) | "Lake Shimmer" |
| [Name] Fields/Plains | Geography (Plains) | "The Ashen Fields" |
| [Name] Pass/Gap | Geography (Pass) | "Ironhold Pass" |
| [Name] Palace/Ruins/Dungeon | Geography (Dungeon) | "The Sunken Palace" |
| [Name] City/Metropolis | Settlement (City) | "Porto Valdris" |
| [Name] Town | Settlement (Town) | "Oakhaven Town" |
| [Name] Port/Harbor | Settlement | "Porto Valdris" |
| [Name] Fortress/Castle/Keep | Settlement (Stronghold) | "Thornwall Keep" |
| [Name] Village/Hamlet | Settlement (Village) | "Millbrook Village" |

**Medium-Confidence Patterns:**

| Pattern | Entity Type | Context Needed |
|---------|-------------|----------------|
| The [Capitalized Name] (standalone) | Geography/Organization | Check surrounding text |
| [Two-Three Capitalized Words] in People section | Character | "Marco Fortunato" |
| [Capitalized Name] near "guild/order/temple" | Organization | Check context |
| [Capitalized Name] near "river/mountain/forest" | Geography | Check context |

**Detection Algorithm:**

```
1. Split content into lines
2. Skip YAML frontmatter (between --- markers)
3. Skip Image Prompts section and below
4. Skip content inside code blocks (``` markers)
5. Skip existing wikilinks

6. For each line:
   a. Find capitalized multi-word phrases (2-4 words)
   b. Check against high-confidence patterns first
   c. If no pattern match, check context clues
   d. Skip common phrases that aren't entities:
      - "The [Direction]" (The North, The East)
      - Generic descriptors (The Great, The Ancient)
      - Section headers

7. For each detected phrase:
   a. Check if already in entity index -> mark as "needs wikilink"
   b. Check if not in index -> mark as "potential new entity"
   c. Record line numbers for all occurrences
   d. Extract surrounding context (10 words before/after)
```

#### 4C: Classify Detected References

Sort all detected references into categories:

| Category | Description | Action |
|----------|-------------|--------|
| **Existing (Unlinked)** | Name matches an existing entity but isn't a wikilink | Convert to `[[wikilink]]` |
| **Broken Link** | `[[wikilink]]` exists but no entity file found | Create entity |
| **Inferred New** | Proper noun with confident type guess | Create entity (confirm type) |
| **Ambiguous New** | Proper noun but type unclear | Ask user for type |

### Step 5: Present Analysis Report

Display findings before taking action:

```
=== ENTITY ANALYSIS: [Source Entity Name] ===

World: [World Name]
Source Path: [path/to/source.md]

---

## EXISTING ENTITIES (Should Become Links)

Found X names matching existing entities but not wikilinked:

| # | Name | Line(s) | Matches Entity |
|---|------|---------|----------------|
| 1 | "Lady Serana Valdren" | 150 | [[Lady Serana Valdren]] |
| 2 | "Captain Alonzo" | 178, 192 | [[Captain Alonzo the Bold]] |

---

## BROKEN WIKILINKS (Need New Entities)

Found X wikilinks pointing to non-existent entities:

| # | Wikilink | Line(s) | Suggested Type | Template |
|---|----------|---------|----------------|----------|
| 1 | [[The Merchant Guilds]] | 286 | Organization | Guild.md |
| 2 | [[Marevento]] | 69, 278 | Settlement | Town.md |
| 3 | [[Serenzia]] | 72, 278 | Settlement | Town.md |

---

## DETECTED REFERENCES (Potential New Entities)

Found X capitalized names that may be entities:

| # | Name | Line(s) | Suggested Type | Context |
|---|------|---------|----------------|---------|
| 1 | "Marco Fortunato" | 171, 283 | Character | "wealthiest merchant", "key retainer" |
| 2 | "Adriano Valdren" | 165 | Character | "Varic's brother", "overseas trade" |
| 3 | "The Sunken Palace" | 166, 252 | Geography (Dungeon) | "underwater ruins", "pre-Faith secrets" |

---

## AMBIGUOUS REFERENCES (Need Confirmation)

| # | Name | Line(s) | Could Be | Please Specify |
|---|------|---------|----------|----------------|
| 1 | "The Reckoning" | 184, 253 | Event OR Tradition | history/concept? |

---

## SUMMARY

| Category | Count |
|----------|-------|
| Existing to link | X |
| Broken links to create | X |
| New entities detected | X |
| Ambiguous (need input) | X |
| **Total potential creations** | **X** |

---

**Options:**
1. Create all suggested entities (uses best-guess types)
2. Review each entity individually
3. Only fix broken wikilinks
4. Only add links to existing entities
5. Show dry-run (no changes)
```

If `--auto` flag is set, skip this step and proceed with best-guess types.
If `--dry-run` flag is set, show report and stop.

### Step 6: Determine Entity Types

For each entity to create, use pattern matching to determine the template:

**Template Mapping (from create-entity):**

**Characters:**
| Pattern | Template |
|---------|----------|
| Lord/Lady/King/Queen/Prince/Princess + name | Support Character.md (or Antagonist.md if negative context) |
| Sir/Dame/Captain/Commander + name | Support Character.md |
| High Priest/Confessor/Elder + name | Support Character.md |
| Personal name in "Members" or "Allies" context | Support Character.md |
| Personal name with villain/enemy context | Antagonist.md |

**Settlements:**
| Pattern | Template |
|---------|----------|
| [Name] + City/Metropolis | City.md |
| [Name] + Port/Harbor (large) | City.md |
| [Name] + Town | Town.md |
| [Name] + Port/Harbor (small) | Town.md |
| [Name] + Village/Hamlet | Village.md |
| [Name] + Fortress/Castle/Keep/Stronghold | Stronghold.md |
| Context mentions "capital", "great city" | City.md |

**Organizations:**
| Pattern | Template |
|---------|----------|
| House + [Name] (noble context) | Government.md |
| Guild/Guilds + [Name] | Guild.md |
| Order + [Name] (religious context) | Religious Order.md |
| Order + [Name] (martial context) | Military.md |
| Clan/Tribe + [Name] | Organization (General).md |
| Army/Legion/Navy + [Name] | Military.md |
| Cult + [Name] | Cult.md |
| Company + [Name] (trade context) | Business.md |
| Default organization | Organization (General).md |

**Geography:**
| Pattern | Template |
|---------|----------|
| [Name] + River/Stream | River.md |
| [Name] + Mountain(s)/Range/Peak(s) | Mountain Range.md |
| [Name] + Forest/Wood(s)/Grove/Jungle | Forest.md |
| [Name] + Sea/Ocean | Ocean.md |
| [Name] + Lake/Pond | Lake.md |
| [Name] + Fields/Plains/Grassland | Plains.md |
| [Name] + Pass/Gap | Pass.md |
| [Name] + Desert/Wasteland | Desert.md |
| [Name] + Coast/Shore | Coast.md |
| [Name] + Island/Isle | Island.md |
| [Name] + Palace/Ruins/Dungeon/Tomb | Dungeon.md |
| [Name] + Cave/Cavern | Cave.md |
| The [Name] (generic geography) | Region.md |

**History:**
| Pattern | Template |
|---------|----------|
| The [Name] + War/Conflict | War.md |
| The [Name] + Battle/Siege | Battle.md |
| The [Name] (event context: "years ago", "when") | Event.md |
| [Name] + Age/Era/Epoch | Age.md |
| [Name] + Treaty/Accord | Treaty.md |

**Category Folder Mappings:**
| Template Category | Save to Folder |
|-------------------|----------------|
| Characters | Characters/ |
| Settlements | Settlements/ |
| Organizations | Organizations/ |
| Geography | Geography/ |
| History | History/ |
| Concepts | Concepts/ |
| Items | Items/ |
| Creatures | Creatures/ |

### Step 7: Confirm Creation Plan

Before creating entities, present the plan:

```
=== CREATION PLAN ===

Will create X new entities:

CHARACTERS (X):
| Entity | Template | Context from Source |
|--------|----------|---------------------|
| Marco Fortunato | Support Character.md | "wealthiest merchant" |
| Adriano Valdren | Support Character.md | "Varic's brother" |

SETTLEMENTS (X):
| Entity | Template | Context from Source |
|--------|----------|---------------------|
| Marevento | Town.md | "secondary port", "shipbuilding" |
| Serenzia | Town.md | "agricultural center" |

ORGANIZATIONS (X):
| Entity | Template | Context from Source |
|--------|----------|---------------------|
| The Merchant Guilds | Guild.md | "allied with House Valdren" |

GEOGRAPHY (X):
| Entity | Template | Context from Source |
|--------|----------|---------------------|
| The Sunken Palace | Dungeon.md | "underwater ruins", "pre-Faith" |

---

Proceed with creation? (yes/no/modify)
```

If `--auto` flag is set, skip confirmation and proceed.

### Step 8: Create Entities

For each confirmed entity:

#### 8A: Read Template

Read the appropriate template from `Templates/[Category]/[Template].md`

#### 8B: Generate Content

Generate content based on:
1. **Context from source entity** - What does the source say about this entity?
2. **World Overview** - Read for tone, themes, naming conventions
3. **Template requirements** - Fill required sections

**Content Generation Guidelines:**

Since these are auto-generated entities, create **minimal but coherent** content:

1. **YAML Frontmatter:**
   - Set `name:` to the entity name
   - Set `status: draft` (marked for user review)
   - Fill category-specific fields with reasonable defaults
   - Leave `image:` empty

2. **Overview Section:**
   - 2-3 sentences based on context from source entity
   - Reference the source entity using `[[wikilink]]`

3. **Core Identity Sections:**
   - Fill minimally based on available context
   - Mark sections needing expansion with `<!-- TODO: Expand -->`

4. **Connections Section:**
   - Add `[[Source Entity]]` as primary connection
   - Use appropriate relationship category based on entity types

5. **Image Prompts:**
   - Leave as template placeholders or fill with basic descriptions

**Naming Conventions:**

Consult naming reference files when generating names:
- `Templates/Reference/D&D Species Naming Conventions.md`
- `Templates/Reference/Tolkien Naming Conventions.md`

Match naming style to the world's established conventions.

#### 8C: Save Entity

Save to: `Worlds/[World Name]/[Category]/[Entity Name].md`

Use Title Case with spaces for filenames.

#### 8D: Add Reciprocal Link

After saving the new entity, add a connection back to the source entity:

**Reciprocal Link Patterns:**

| New Entity Type | Source Entity Type | New Entity Links To Source As |
|-----------------|-------------------|-------------------------------|
| Character | Settlement | Home/Location |
| Character | Organization | Member Of |
| Character | Character | Associate/Ally |
| Settlement | Region | Part Of |
| Settlement | Organization | Headquarters |
| Organization | Settlement | Based Here |
| Organization | Character | Leadership/Members |
| Geography | Geography | Part Of/Contains |

### Step 9: Update Source Entity

After creating all new entities:

#### 9A: Convert Plain Text to Wikilinks

For each detected reference that now has an entity:
1. Find occurrences in source entity
2. Replace `Entity Name` with `[[Entity Name]]`
3. Handle partial name matches (e.g., "Lady Serana" → `[[Lady Serana Valdren|Lady Serana]]`)

Use Edit tool for precise replacements.

#### 9B: Ensure Connections Section is Updated

For each new entity created:
1. Determine appropriate connection category based on entity type
2. Check if source entity's Connections section has this category
3. Add wikilink to appropriate subsection

**Connection Section Formats:**

```markdown
## Connections

### People
- **Family:** [[Family Member]]
- **Allies:** [[Ally 1]], [[Ally 2]]
- **Associates:** [[Associate 1]]

### Organizations
- **Member Of:** [[Organization]]
- **Allied With:** [[Allied Org]]

### Locations
- **Headquarters:** [[Settlement]]
- **Territory:** [[Region]]

### Geography
- **Contains:** [[Location 1]], [[Location 2]]
- **Borders:** [[Neighboring Region]]
```

#### 9C: Validate All Links

After updates, verify:
1. All new wikilinks resolve to existing entity files
2. No duplicate links in Connections section
3. Source entity frontmatter is intact

### Step 10: Summary Report

```
=== POPULATE COMPLETE: [Source Entity Name] ===

Created X new entities:

CHARACTERS:
- [[Marco Fortunato]] - Wealthy merchant, Valdren ally (draft)
- [[Adriano Valdren]] - Varic's brother, trade manager (draft)

SETTLEMENTS:
- [[Marevento]] - Secondary port, shipbuilding center (draft)
- [[Serenzia]] - Agricultural town (draft)

ORGANIZATIONS:
- [[The Merchant Guilds]] - Allied trading organizations (draft)

GEOGRAPHY:
- [[The Sunken Palace]] - Underwater ruins with ancient secrets (draft)

---

Source Entity Updated:
- Added X wikilinks (previously plain text)
- Added X items to Connections section

Reciprocal Links Added:
- Marco Fortunato → [[Source Entity]] (employer)
- Marevento → [[The Western Shore]] (region)
- etc.

---

All new entities marked as 'draft' for review.

Suggested Next Steps:
1. Review and expand created entities with /expand-entity
2. Run /audit-world [World Name] to verify all connections
3. Generate images with /generate-image [Entity]
```

## Bulk Processing Mode

When `--world` flag is provided, the skill processes multiple entities:

### Bulk Mode Workflow

1. **Scan world directory:**
   - List all `.md` files in `Worlds/[World Name]/`
   - If `--category` specified, only scan that folder
   - Build a master entity index for the entire world

2. **Analyze all entities:**
   - Run detection on each entity file
   - Compile a master list of potential new entities
   - De-duplicate across files (same reference in multiple files = one entity)

3. **Present consolidated plan:**
   ```
   === BULK POPULATE: [World Name] ===

   Files Analyzed: X
   Files with Detections: Y

   ENTITIES TO CREATE (de-duplicated):

   | Entity | Type | Referenced In | Times |
   |--------|------|---------------|-------|
   | Marco Fortunato | Character | 3 files | 7 mentions |
   | The Iron Guild | Organization | 2 files | 4 mentions |
   ...

   Total: N new entities across M source files

   Options:
   1. Create all (uses best-guess types)
   2. Review by category
   3. Review each individually
   4. Dry run complete
   ```

4. **Process with de-duplication:**
   - Create each entity once
   - Update ALL source files that reference it
   - Add reciprocal links from new entity to all referencing entities

5. **Bulk summary report:**
   ```
   === BULK POPULATE COMPLETE ===

   Entities Created: N
   Source Files Updated: M
   Total Wikilinks Added: X
   Reciprocal Links Created: Y

   By Category:
   - Characters: N created
   - Settlements: N created
   ...
   ```

### Bulk Mode Options

```bash
# Process entire world (with confirmations)
/populate-entity --world Eldermyr

# Fully automated (no confirmations)
/populate-entity --world Eldermyr --auto

# Only fix broken links across world
/populate-entity --world Eldermyr --broken-only

# Limit total entities created in bulk
/populate-entity --world Eldermyr --limit 50

# Preview bulk changes
/populate-entity --world Eldermyr --dry-run
```

### Performance Notes

- Bulk mode builds entity index once (more efficient)
- De-duplication prevents creating duplicate entities
- For very large operations, use `--limit` to process in batches
- Consider running `/audit-world --check links` afterward to verify

## Examples

```bash
# Populate a specific entity by name
/populate-entity "House Valdren"

# Populate by file path
/populate-entity Worlds/Eldermyr/Organizations/House Valdren.md

# Preview what would be created (no changes)
/populate-entity "Porto Valdris" --dry-run

# Auto-populate without prompts (for batch processing)
/populate-entity "Lord Varic Valdren" --auto

# Only fix broken wikilinks, skip text detection
/populate-entity "World Overview" --broken-only

# Only add wikilinks to existing entities, don't create new
/populate-entity "The Great War" --links-only

# Limit number of entities to create
/populate-entity "The Great War" --limit 5

# Combine flags
/populate-entity "House Valdren" --auto --limit 10
```

## Integration with Other Skills

### After `/create-entity`
Run `/populate-entity` on newly created entities to automatically flesh out referenced names.

### Before `/audit-world`
Run `/populate-entity` on key entities to reduce broken link count before audit.

### With `/expand-entity`
- `/expand-entity` adds depth to a single entity
- `/populate-entity` creates the network of related entities
- Use together: populate first, then expand key entities

### With `/link-entities`
- `/populate-entity` creates entities from detected references
- `/link-entities` can refine the relationships afterward

## Quality Guidelines

1. **Conservative Creation:** Only create entities with high-confidence type detection
2. **Minimal Content:** New entities get basic content marked as `draft`
3. **Preserve Context:** Use context from source to inform new entity content
4. **Bidirectional:** Always add reciprocal links
5. **No Duplicates:** Check entity index before creating
6. **User Control:** Confirmation prompts unless `--auto` flag
