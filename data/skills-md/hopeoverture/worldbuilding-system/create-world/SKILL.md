---
name: create-world
description: Create a new worldbuilding project with full folder structure. Use when the user wants to start a new world, campaign setting, or fantasy setting like "create a world called Eldoria".
argument-hint: "[world name] [--quick]"
---

# Create New World

Create a new worldbuilding project for: $ARGUMENTS

## Overview

Creates a new world directory with full folder structure and an initial World Overview document. Can run in:
- **Interactive mode** (default): Asks questions to generate a customized World Overview
- **Quick mode** (`--quick`): Creates structure with template placeholders only

## Instructions

### Step 1: Parse Arguments

Extract from `$ARGUMENTS`:
- **World name** - Required (ask if not provided)
- **--quick flag** - Optional, skips questionnaire

Check if world already exists at `Worlds/[World Name]/`. If yes:
> "A world named '[World Name]' already exists. Would you like to:
> 1. Open the existing world
> 2. Choose a different name
> 3. Delete and recreate (WARNING: destroys existing content)"

### Step 2: World Name Validation

Ensure the world name is:
- Evocative and memorable
- Title Case with spaces allowed
- Valid as a folder name (no special characters: `/ \ : * ? " < > |`)

If name seems generic (e.g., "Test", "New World", "World 1"), offer suggestions:
> "Would you like a more evocative name? Here are some suggestions based on fantasy naming patterns:
> 1. [Generated name 1]
> 2. [Generated name 2]
> 3. [Generated name 3]
> 4. Keep '[Original Name]'"

---

## Interactive Mode (Default)

### Step 3: Core Identity Questions

Ask these questions to generate customized content. Present as numbered options where applicable.

#### 3A: Genre & Tone

> "What genre and tone fits your world?"
>
> 1. **Epic Fantasy** - Heroic adventures, clear good vs evil, grand scale (Lord of the Rings, Wheel of Time)
> 2. **Dark Fantasy** - Grim, morally gray, dangerous (Dark Souls, Warhammer, Witcher)
> 3. **Sword & Sorcery** - Personal stakes, pulpy action, rogues and warriors (Conan, Lankhmar)
> 4. **Mythic Fantasy** - Gods walk among mortals, legendary heroes, fate-driven (Greek myths, Exalted)
> 5. **Low Fantasy** - Subtle magic, political intrigue, grounded (Game of Thrones, First Law)
> 6. **Whimsical Fantasy** - Lighter tone, humor welcome (Discworld, Princess Bride)
> 7. **Horror Fantasy** - Dread, cosmic terror, survival (Ravenloft, Call of Cthulhu)
> 8. **Other** - Describe your vision

Store response in `world_tone`.

#### 3B: The Hook

> "In one or two sentences, what makes this world unique? What's the first thing you want players to discover?"
>
> Examples:
> - "Magic is dying, and the last mages are hunted as heretics"
> - "Three empires vie for control of the only river in a vast desert"
> - "The gods went silent fifty years ago, and cults have risen in the void"
> - "A floating archipelago above an endless storm-sea"

Store response in `world_hook`.

#### 3C: Magic Level

> "How common is magic in this world?"
>
> 1. **None** - Magic doesn't exist; purely mundane
> 2. **Mythic Only** - Magic existed in legends, maybe traces remain
> 3. **Rare** - Most people never see real magic; practitioners are legendary
> 4. **Uncommon** - Magic exists but is notable; mages are respected/feared
> 5. **Common** - Part of daily life; magical services available in cities
> 6. **Pervasive** - Magic is everywhere; even commoners have cantrips

Store response in `magic_level`.

#### 3D: Technology Level

> "What's the baseline technology level?"
>
> 1. **Primitive** - Stone age, tribal societies
> 2. **Ancient** - Bronze/Iron age, early empires (Egypt, Mesopotamia)
> 3. **Classical** - Greek/Roman equivalent, sophisticated but pre-medieval
> 4. **Medieval** - Feudal kingdoms, castles, knights (standard D&D)
> 5. **Renaissance** - Early gunpowder, printing press, exploration age
> 6. **Industrial** - Steam power, factories, early modern
> 7. **Magitech** - Technology powered or replaced by magic

Store response in `tech_level`.

#### 3E: Scale & Scope

> "How much of the world do you plan to detail?"
>
> 1. **Local** - One city and surroundings; tight focus
> 2. **Regional** - A single kingdom or territory
> 3. **Continental** - One major landmass with multiple nations
> 4. **Global** - Multiple continents, world-spanning scope
> 5. **Planar** - Multiple planes of existence matter

Store response in `world_scale`.

#### 3F: Central Conflict

> "What's the primary tension or conflict driving events?"
>
> Examples:
> - War between nations
> - Ancient evil awakening
> - Political succession crisis
> - Plague with no cure
> - Planar barriers weakening
> - Resource scarcity
> - Religious schism
> - Or describe your own

Store response in `central_conflict`.

#### 3G: Inspirations (Optional)

> "What are 1-3 inspirations for this world? (Books, games, movies, history, aesthetics)"

Store response in `inspirations`.

---

### Step 4: Create Directory Structure

Create the following structure in `Worlds/[World Name]/`:

```
[World Name]/
├── World Overview.md
├── Characters/
├── Settlements/
├── Items/
├── Creatures/
├── Organizations/
├── Concepts/
├── History/
├── Geography/
├── Encounters/
├── Maps/
└── Sessions/
```

**Folder purposes:**
| Folder | Contents |
|--------|----------|
| Characters/ | NPCs, protagonists, antagonists, familiars |
| Settlements/ | Cities, towns, villages, taverns, shops, temples |
| Items/ | Weapons, armor, artifacts, potions, books, vehicles |
| Creatures/ | Monsters, animals, species, plants |
| Organizations/ | Governments, guilds, cults, military, criminal orgs |
| Concepts/ | Deities, pantheons, magic systems, calendars, currencies |
| History/ | Ages, events, wars, battles, dynasties |
| Geography/ | Continents, regions, terrain features, dungeons |
| Encounters/ | Combat, social, exploration encounters |
| Maps/ | World, continent, region, settlement maps |
| Sessions/ | DM session prep notes and logs |

---

### Step 5: Generate World Overview

Create `World Overview.md` with content filled from questionnaire answers:

```markdown
---
tags:
  - world
  - overview
  - [world_name_tag]
name: "[World Name]"
aliases: []
status: draft
# World Details
genre: [derived from tone]
tone: "[world_tone]"
time_period: "[tech_level era name]"
magic_level: "[magic_level]"
technology_level: "[tech_level]"
scale: "[world_scale]"
created: "[current date]"
---

# [World Name]

> [!info] World Overview
> This is the central document for [World Name]. It tracks high-level worldbuilding details, themes, and relationships between major elements. Use `[[wikilinks]]` to connect to entities as you create them.

## Premise

[Expanded version of world_hook - 3-4 sentences elaborating on the unique concept, the current situation, and what makes this world compelling for adventures]

## Tone & Themes

### Tone
**Primary Tone:** [world_tone]

**What This Means:**
[2-3 sentences describing how this tone manifests - violence level, moral complexity, humor appropriateness, stakes]

### Central Themes
1. **[Theme 1]** - [Brief description derived from hook/conflict]
2. **[Theme 2]** - [Second theme]
3. **[Theme 3]** - [Third theme, if applicable]

### Inspirations
[List inspirations if provided, or leave as prompt]
-
-

---

## The World

### Geography Overview
[3-4 sentences describing the world's physical layout appropriate to the scale. For continental: describe the main continent. For local: describe the region.]

**Scale:** [world_scale] - [What this means for play]

### Major Powers
| Power | Type | Region | Status |
|-------|------|--------|--------|
| [Placeholder] | [Government type] | [Location] | [Current state] |
| [Placeholder] | [Government type] | [Location] | [Current state] |
| [Placeholder] | [Government type] | [Location] | [Current state] |

### Timeline
| Era | Approximate Period | Key Events |
|-----|-------------------|------------|
| Age of [Myth/Creation] | Ancient past | [World's origin] |
| Age of [Growth/Expansion] | [Time period] | [Key developments] |
| Current Era | Present | [Current situation from central_conflict] |

---

## Magic & Technology

### Magic
**Magic Level:** [magic_level]

[2-3 sentences describing how magic works in this world, who can use it, and how society views it - derived from magic_level choice]

**Key Questions to Answer:**
- Where does magical power come from?
- Who can use magic and how do they learn?
- What are the costs or limits?
- How does society treat magic users?

**Magic System(s):** (Create with `/create-entity magic system`)
- [[]]

### Technology
**Technology Level:** [tech_level]

[2-3 sentences describing the technological baseline - what exists, what doesn't, any anachronisms or unique innovations]

**Notable Technologies:**
-

---

## Cosmology

### The Divine
[Placeholder text based on tone - for dark fantasy: "The gods are distant or cruel..."; for epic fantasy: "A pantheon of gods watches over mortals..."]

**Pantheon:** (Create with `/create-entity pantheon`)
- [[]]

**Key Questions to Answer:**
- Do gods exist? Are they active?
- How do mortals worship?
- What happens after death?

### Planes of Existence
[Default based on scale - if planar: list expected planes; otherwise: "The material world is the focus of this setting."]

-

### Creation Myth
[2-3 sentence placeholder based on tone]

---

## Current Era

### The State of the World
[4-5 sentences expanding on central_conflict - who's involved, what's at stake, how it affects common people, what's the ticking clock]

### Major Conflicts
1. **[Primary Conflict]:** [central_conflict expanded]
2. **[Secondary Conflict]:** [Related or contrasting tension]

### Opportunities for Adventure
1. [Hook derived from conflict]
2. [Exploration opportunity]
3. [Faction-based opportunity]
4. [Mystery or discovery opportunity]

---

## World-Specific Rules

### House Rules
D&D 5e 2024 modifications for this setting:
- [Based on magic_level - e.g., if magic is rare: "Spellcasting classes require DM approval"]
- [Based on tech_level - e.g., if renaissance: "Firearms exist using DMG rules"]
-

### Unique Mechanics
Setting-specific systems to develop:
- [If magic is unusual: "Magic corruption/cost system"]
- [If appropriate: "Faction reputation tracking"]
-

### Restricted Options
[Based on world - species, classes, or backgrounds that don't fit]
-

---

## Development Notes

### Priorities
What to develop first (recommended based on scale):
1. [If continental/global: "Main continent geography and 2-3 major nations"]
   [If regional: "The primary region and its major settlement"]
   [If local: "The main city and its districts"]
2. Pantheon and/or magic system (if magic exists)
3. Central conflict factions and key NPCs
4. 2-3 adventure sites (dungeons, ruins, dangerous locations)

### Questions to Answer
Unresolved worldbuilding questions:
1. [Derived from gaps in provided info]
2. [Standard question for the tone/scale]
3.

### Session Zero Topics
Discuss with players:
- Appropriate character origins
- Tone expectations (violence, horror, humor levels)
- [Theme-specific topic]
- [Conflict-specific topic]

---

## Quick Reference

### Key Locations
- [[]] - [Description placeholder]
- [[]] - [Description placeholder]
- [[]] - [Description placeholder]

### Key Characters
- [[]] - [Role placeholder]
- [[]] - [Role placeholder]
- [[]] - [Role placeholder]

### Key Organizations
- [[]] - [Type placeholder]
- [[]] - [Type placeholder]
- [[]] - [Type placeholder]

### Key Concepts
- [[]] - [Magic/religion/culture placeholder]
- [[]] - [Placeholder]

---

## Image Prompts

### World Map Concept
**Art Style:** [Derived from tone - e.g., "Hand-drawn parchment map with aged edges" for classic fantasy, "Dark atmospheric satellite view" for dark fantasy]

**Prompt:** [To be filled when geography is established]

### Iconic Scene
**Art Style:** [Tone-appropriate]

**Prompt:** [To be filled - depicting the world's hook visually]
```

---

### Step 6: Create Supporting Files

#### 6A: .gitkeep Files

Add `.gitkeep` to each empty subdirectory for version control:
- Characters/.gitkeep
- Settlements/.gitkeep
- Items/.gitkeep
- Creatures/.gitkeep
- Organizations/.gitkeep
- Concepts/.gitkeep
- History/.gitkeep
- Geography/.gitkeep
- Encounters/.gitkeep
- Maps/.gitkeep
- Sessions/.gitkeep

#### 6B: Create Session Log Template (Optional)

If user seems interested in running games, create `Sessions/Session Log Template.md`:

```markdown
---
tags:
  - session
  - log
session_number:
date_played:
date_ingame:
---

# Session [X]: [Title]

## Summary
[2-3 sentence summary of what happened]

## Events
1.
2.
3.

## NPCs Encountered
- [[NPC Name]] - [What happened]

## Locations Visited
- [[Location]] - [What happened]

## Loot & Rewards
-

## Plot Threads
### Advanced
-
### Introduced
-
### Resolved
-

## Notes for Next Session
-
```

---

### Step 7: Confirmation & Next Steps

Present a summary and clear next steps:

```
╔══════════════════════════════════════════════════════════════╗
║              WORLD CREATED: [World Name]                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Location: Worlds/[World Name]/                              ║
║                                                              ║
║  Tone: [world_tone]                                          ║
║  Magic: [magic_level]                                        ║
║  Tech: [tech_level]                                          ║
║  Scale: [world_scale]                                        ║
║                                                              ║
║  Hook: "[world_hook - truncated]"                            ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  NEXT STEPS                                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1. Review and refine World Overview.md                      ║
║                                                              ║
║  2. Choose your approach:                                    ║
║     • /generate-world [World Name]                           ║
║       Auto-generate 80-120 interconnected entities           ║
║                                                              ║
║     • /worldbuild [World Name]                               ║
║       Interactive guided building with Q&A                   ║
║                                                              ║
║     • /create-entity [description] for [World Name]          ║
║       Create entities one at a time                          ║
║                                                              ║
║  Recommended first entities based on your scale:             ║
║  [Scale-specific recommendations - see below]                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Scale-specific recommendations:**

| Scale | Recommended First Entities |
|-------|---------------------------|
| Local | Main city → Key district → Central tavern → 3-4 NPCs |
| Regional | Region overview → Capital city → 2 other settlements → Government |
| Continental | Continent → 3-4 regions → Major nation → Capital city |
| Global | World geography → 2 continents → Major nations overview |
| Planar | Material plane → 1-2 key planes → Planar connections |

---

## Quick Mode (--quick flag)

If `--quick` is in arguments, skip the questionnaire:

1. Create directory structure (same as interactive)
2. Create World Overview with all placeholder text (no filled content)
3. Create .gitkeep files
4. Brief confirmation:

```
World '[World Name]' created at Worlds/[World Name]/

Start by editing World Overview.md to define your world's identity.

Commands to continue:
- /worldbuild [World Name] - Interactive guided building
- /generate-world [World Name] - Auto-generate full world
- /create-entity [type] for [World Name] - Create individual entities
```

---

## Duplicate World Handling

If `Worlds/[World Name]/` already exists:

```
A world named '[World Name]' already exists.

Options:
1. Open existing - I'll read the World Overview and summarize it
2. New name - Choose a different name for your new world
3. Recreate - Delete existing and start fresh (DESTRUCTIVE)
4. Cancel - Abort world creation

What would you like to do?
```

If user chooses "Open existing":
- Read World Overview.md
- Summarize current state (entities created, status, etc.)
- Offer next steps based on world state

---

## Naming Conventions Reference

When generating names for entities in this world, consult these reference files:

| Reference File | Use For |
|----------------|---------|
| `Templates/Reference/D&D Species Naming Conventions.md` | Species-specific naming patterns (Dwarves, Elves, Halflings, Orcs, etc.) |
| `Templates/Reference/Tolkien Naming Conventions.md` | High fantasy linguistic patterns (Sindarin, Quenya, Khuzdul, etc.) |

### When to Apply

- **During World Overview generation:** Use naming patterns that match the world's tone and inspirations
- **For Major Powers table:** Name kingdoms/empires using appropriate linguistic conventions
- **For placeholder entities:** Suggest names consistent with cultural patterns

### Matching Names to Tone

| World Tone | Recommended Naming Style |
|------------|-------------------------|
| Epic Fantasy | Tolkien patterns (Sindarin/Quenya for elves, Norse-inspired for dwarves) |
| Dark Fantasy | Harsher variants, Black Speech influences for villains |
| Sword & Sorcery | Mixed cultural human names, simpler constructions |
| Mythic Fantasy | Quenya (formal/divine), culture-specific for mortals |
| Low Fantasy | Historical human naming patterns (Germanic, Celtic, Slavic) |
| Whimsical Fantasy | Halfling/Gnome patterns, playful constructions |

---

## Integration Notes

- World Overview uses `[[wikilinks]]` syntax for Obsidian compatibility
- All YAML frontmatter follows template conventions
- Folder structure matches category mappings in create-entity skill
- Sessions/ folder supports session-prep skill output
- Encounters/ folder supports random-encounter skill output
- Maps/ folder ready for map templates

## Examples

```
# Interactive creation
/create-world Eldoria

# Quick creation (no questions)
/create-world Shadowmere --quick

# Will prompt for name
/create-world
```
