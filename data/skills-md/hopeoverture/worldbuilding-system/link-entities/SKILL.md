---
name: link-entities
description: Create bidirectional wikilinks between existing entities. Use when user wants to "connect", "link", or "relate" two or more entities, or when they mention entities should reference each other.
argument-hint: "[entity1] [entity2] or 'auto [world]'"
---

# Link Entities

Link entities: $ARGUMENTS

## Overview

Creates bidirectional wikilinks between entities to ensure proper interconnection. Can operate in:
1. **Manual mode:** Link two specific entities
2. **Auto mode:** Scan a world and suggest missing connections

## Instructions

### Parse Arguments

- `[entity1] [entity2]` → Manual linking between two entities
- `auto [world name]` → Auto-detect and suggest missing links for a world
- `[entity1] to [entity2]` → Manual with explicit relationship
- `[entity]` alone → Show what this entity could connect to

### Manual Linking Mode

#### Step 1: Locate Both Entities

1. Search `Worlds/` for each entity name
2. If ambiguous, ask for clarification
3. Read both entity files

#### Step 2: Determine Relationship Type

Based on entity types, suggest appropriate relationship:

| Entity A | Entity B | A Links to B As | B Links to A As |
|----------|----------|-----------------|-----------------|
| Character | Settlement | Location/Home | Notable NPCs/Residents |
| Character | Organization | Member Of | Members |
| Character | Character | Ally/Rival/Family | Ally/Rival/Family |
| Settlement | Region | Part Of | Contains/Settlements |
| Settlement | Organization | Hosts | Headquarters/Presence |
| Organization | Organization | Allied With/Rivals | Allied With/Rivals |
| Geography | Geography | Part Of/Borders | Contains/Borders |
| Character | Deity | Worships | Followers |
| Item | Character | Owned By | Equipment/Possessions |
| Creature | Geography | Habitat | Native Creatures |
| Event | Location | Occurred At | Historical Events |

Ask user to confirm or specify the relationship:
> "I'll link [[Entity A]] and [[Entity B]]. Suggested relationship:
> - A references B as: [suggested category]
> - B references A as: [suggested category]
>
> Is this correct, or would you prefer a different relationship?"

#### Step 3: Add Links to Both Entities

1. **Read Entity A:**
   - Find Connections section
   - Identify appropriate subsection
   - Check if link already exists

2. **Add Link to Entity A:**
   - If subsection exists, append `[[Entity B]]`
   - If subsection doesn't exist, create it with link
   - Use Edit tool

3. **Read Entity B:**
   - Find Connections section
   - Identify appropriate subsection (reciprocal)

4. **Add Link to Entity B:**
   - If subsection exists, append `[[Entity A]]`
   - If subsection doesn't exist, create it with link

#### Step 4: Confirm

```
=== LINKS CREATED ===

[[Entity A]] → [[Entity B]]
Added to: Connections > [Category]

[[Entity B]] → [[Entity A]]
Added to: Connections > [Category]

Both entities now reference each other.
```

### Auto Mode

#### Step 1: Scan World

1. Build entity index from `Worlds/[World Name]/`
2. For each entity, extract:
   - All `[[wikilinks]]` in content
   - All `[[wikilinks]]` in Connections section
   - Entity type from YAML or folder

#### Step 2: Build Connection Graph

Create adjacency list:
```
Entity A → [Entity B, Entity C, ...]
Entity B → [Entity D, ...]
...
```

#### Step 3: Identify Missing Links

Check for:

1. **One-way links:** A links to B, but B doesn't link to A
2. **Implied connections:**
   - Two characters in same organization should know each other
   - Settlements in same region should reference region
   - Organization headquarters should reference organization
3. **Orphan entities:** Entities with no incoming links

#### Step 4: Present Suggestions

```
=== CONNECTION ANALYSIS: [World Name] ===

One-Way Links Found: X
Suggested New Links: Y
Orphan Entities: Z

HIGH PRIORITY (One-Way Links):
1. [[Character A]] → [[City B]] but City B doesn't link back
   Suggestion: Add Character A to City B's "Notable NPCs"

2. [[Organization X]] → [[Settlement Y]] but Settlement Y doesn't link back
   Suggestion: Add Organization X to Settlement Y's "Organizations"

SUGGESTED CONNECTIONS:
3. [[Character C]] and [[Character D]] are both in [[Organization Z]]
   Suggestion: Link them as "Associates" or "Fellow Members"

4. [[Settlement E]] and [[Settlement F]] are both in [[Region G]]
   Suggestion: Link them as "Nearby Settlements"

ORPHAN ENTITIES (no incoming links):
- [[Forgotten NPC]] - Consider linking from their location
- [[Lonely Mountain]] - Consider linking from parent region

Would you like me to:
1. Fix all one-way links automatically
2. Add all suggested connections
3. Review each suggestion individually
4. Just fix specific items (enter numbers)
```

#### Step 5: Apply Fixes

For each approved fix:
1. Read source entity
2. Add link in appropriate section
3. Read target entity
4. Add reciprocal link
5. Track changes made

#### Step 6: Summary

```
=== LINKING COMPLETE ===

Changes Made:
- Fixed X one-way links
- Added Y new bidirectional connections
- Orphans addressed: Z

Entities Modified: [list]

Connection Density:
- Before: Average X.X links per entity
- After: Average Y.Y links per entity

Remaining Issues:
- [List any unresolved items]
```

## Connection Section Formats

When adding to Connections section, use these formats:

### Character Connections
```markdown
## Connections

### People
- **Allies:** [[Ally 1]], [[Ally 2]]
- **Rivals:** [[Rival 1]]
- **Family:** [[Family Member]]

### Organizations
- **Member Of:** [[Organization]]
- **Enemies:** [[Enemy Org]]

### Locations
- **Home:** [[Settlement]]
- **Frequents:** [[Tavern]], [[Shop]]
```

### Settlement Connections
```markdown
## Connections

### Geography
- **Region:** [[Parent Region]]
- **Nearby:** [[Nearby Settlement]]

### People
- **Ruler:** [[Ruler Name]]
- **Notable NPCs:** [[NPC 1]], [[NPC 2]]

### Organizations
- **Based Here:** [[Org 1]], [[Org 2]]
- **Influence:** [[Distant Org]]
```

### Organization Connections
```markdown
## Connections

### Structure
- **Headquarters:** [[Settlement]]
- **Branches:** [[Location 1]], [[Location 2]]

### People
- **Leader:** [[Leader Name]]
- **Notable Members:** [[Member 1]], [[Member 2]]

### Relationships
- **Allies:** [[Allied Org]]
- **Rivals:** [[Rival Org]]
```

## Examples

```
# Link two specific entities
/link-entities "Grom the Blacksmith" "Ironhold City"

# Auto-detect missing links
/link-entities auto Eldoria

# Show potential connections for one entity
/link-entities "The Iron Guild"
```
