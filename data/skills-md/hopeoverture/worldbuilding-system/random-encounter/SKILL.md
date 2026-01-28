---
name: random-encounter
description: Generate random encounters appropriate for a location, party level, or situation. Creates combat, social, or exploration encounters using existing world entities. Use when user wants "random encounter", "encounter table", or "what happens at [location]".
argument-hint: "[location] [party level] [type]"
---

# Random Encounter Generator

Generate encounter: $ARGUMENTS

## Overview

Creates contextually appropriate random encounters by:
1. Using existing world entities (creatures, NPCs, locations)
2. Matching encounter difficulty to party level
3. Generating varied encounter types (combat, social, exploration)
4. Optionally creating encounter tables for locations

## Instructions

### Step 1: Parse Arguments

Extract from `$ARGUMENTS`:
- **Location:** Where the encounter occurs (entity name, region, terrain type)
- **Party Level:** Average party level (1-20) - ask if not provided
- **Encounter Type:** combat, social, exploration, or random
- **World:** Which world to pull entities from

If location is a world entity, read it for context.
If location is a terrain type (forest, road, city), use as context.

### Step 2: Gather World Context

If a specific world is identifiable:
1. Scan `Worlds/[World Name]/Creatures/` for available monsters
2. Scan `Worlds/[World Name]/Characters/` for NPCs
3. Read location entity for specific inhabitants/dangers mentioned
4. Note regional factions, tensions, environmental hazards

### Step 3: Determine Encounter Parameters

#### Difficulty by Party Level

| Party Level | Easy CR | Medium CR | Hard CR | Deadly CR |
|-------------|---------|-----------|---------|-----------|
| 1-4 | 1/4-1/2 | 1-2 | 3-4 | 5+ |
| 5-8 | 1-3 | 4-6 | 7-9 | 10+ |
| 9-12 | 4-6 | 7-10 | 11-13 | 14+ |
| 13-16 | 7-10 | 11-14 | 15-17 | 18+ |
| 17-20 | 10-14 | 15-18 | 19-21 | 22+ |

#### Encounter Types by Location

| Location Type | Combat % | Social % | Exploration % |
|---------------|----------|----------|---------------|
| City/Town | 20% | 60% | 20% |
| Road/Trade Route | 40% | 40% | 20% |
| Wilderness | 60% | 15% | 25% |
| Dungeon | 70% | 10% | 20% |
| Frontier | 50% | 25% | 25% |

### Step 4: Generate Encounter

#### Combat Encounter Format

```markdown
## Combat Encounter: [Evocative Name]

**Location:** [Specific setting within area]
**Difficulty:** [Easy/Medium/Hard/Deadly] for level [X] party

### Setup
[2-3 sentences describing the scene as players encounter it]

### Enemies
| Creature | Count | CR | Notes |
|----------|-------|----|----- |
| [[Creature 1]] | X | Y | Tactics/role |
| [[Creature 2]] | X | Y | Tactics/role |

**Total XP:** [calculated]

### Tactics
[How enemies behave - aggression, retreat conditions, special actions]

### Environment
- **Terrain:** [features that affect combat]
- **Hazards:** [environmental dangers]
- **Cover:** [defensive positions]

### Treasure
[Appropriate loot based on CR and creature type]

### Complications (Optional)
[d4 table of things that could make this more interesting]
1. [Complication 1]
2. [Complication 2]
3. [Complication 3]
4. [Complication 4]

### Aftermath
[What happens after combat - tracks to follow, clues found, etc.]
```

#### Social Encounter Format

```markdown
## Social Encounter: [Evocative Name]

**Location:** [Where this occurs]
**Primary NPC:** [[NPC Name]] or [Generated NPC]

### Setup
[2-3 sentences describing the situation]

### The NPC
- **Appearance:** [Brief description]
- **Demeanor:** [How they come across]
- **Want:** [What they're trying to achieve]
- **Secret:** [What they're hiding]

### The Situation
[What's happening, what the NPC needs or offers]

### Conversation Hooks
- [Opening line or action]
- [Topic they'll bring up]
- [Question they might ask]

### Possible Outcomes
| Approach | DC | Result |
|----------|----|----- |
| Persuasion | [X] | [Outcome] |
| Intimidation | [X] | [Outcome] |
| Deception | [X] | [Outcome] |
| Insight | [X] | [What they learn] |

### Complications
[What could go wrong or make this interesting]

### Connections
[How this ties to larger world events/entities]
```

#### Exploration Encounter Format

```markdown
## Exploration Encounter: [Evocative Name]

**Location:** [Specific area]
**Type:** [Discovery/Hazard/Mystery/Resource]

### Discovery
[What the party finds - describe for players]

### Investigation
| Check | DC | Reveals |
|-------|----|----- |
| Perception | [X] | [Detail] |
| Investigation | [X] | [Detail] |
| History/Arcana/Nature | [X] | [Context] |
| Survival | [X] | [Practical info] |

### Interaction Options
1. **[Option A]:** [What happens]
2. **[Option B]:** [What happens]
3. **[Option C]:** [What happens]

### Hidden Elements
[Things not immediately obvious]

### Treasure/Rewards
[What can be gained]

### Connections
[Links to world lore, plot hooks]
```

### Step 5: Use World Entities

When possible, incorporate existing entities:

1. **Creatures:** Use monsters from `Creatures/` folder
2. **NPCs:** Reference characters from `Characters/` folder
3. **Organizations:** Tie to factions from `Organizations/`
4. **Locations:** Reference specific places from `Geography/` or `Settlements/`
5. **Items:** Include items from `Items/` as treasure
6. **History:** Connect to events from `History/`

Add `[[wikilinks]]` to all referenced entities.

### Step 6: Offer Encounter Table

After generating one encounter, offer:

> "Would you like me to create a full d6 or d12 encounter table for this location?"

#### Encounter Table Format

```markdown
## Encounter Table: [Location Name]

**Terrain:** [Type]
**Recommended Level:** [Range]
**Check Frequency:** [How often to roll]

### d12 Encounters

| Roll | Type | Encounter | Difficulty |
|------|------|-----------|------------|
| 1 | Combat | [Brief description] | Deadly |
| 2 | Combat | [Brief description] | Hard |
| 3-4 | Combat | [Brief description] | Medium |
| 5 | Social | [Brief description] | - |
| 6 | Social | [Brief description] | - |
| 7 | Exploration | [Brief description] | - |
| 8 | Exploration | [Brief description] | - |
| 9 | Environmental | [Brief description] | Varies |
| 10 | Plot Hook | [Brief description] | - |
| 11 | Resource | [Brief description] | - |
| 12 | Special | [Unique event] | Varies |

### Encounter Details
[Expanded details for each entry]
```

### Step 7: Offer to Save

> "Would you like me to save this encounter to the world?"

If yes:
1. Determine appropriate template (Combat, Social, Exploration, Trap)
2. Read template from `Templates/Encounters/`
3. Fill template with generated content
4. Save to `Worlds/[World Name]/Encounters/[Encounter Name].md`
5. Update location entity's Connections if applicable

## Examples

```
# Generate for specific location
/random-encounter "The Blackwood Forest" level 5

# Combat encounter on a road
/random-encounter road combat level 3

# Social encounter in city
/random-encounter "Ironhold City" social level 8

# Let system choose type
/random-encounter wilderness level 6 random

# Create encounter table
/random-encounter "Shadowfell Border" table level 10
```

## Integration Notes

- Reference Connection Matrix for encounter-to-location linking
- Use CR and XP tables from D&D 5e 2024 Rules
- Match creature behavior to stat blocks if using world creatures
- Consider party composition if mentioned in conversation
