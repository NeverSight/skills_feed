---
name: expand-entity
description: Expand an existing entity with additional detail, create related sub-entities, or generate deeper connections. Use when user wants to "flesh out", "expand", "add more detail to", or "develop" an existing entity like a city, character, or organization.
argument-hint: "[entity path or name]"
---

# Expand Entity

Expand this entity: $ARGUMENTS

## Overview

Takes an existing worldbuilding entity and expands it by:
1. Adding richer detail to existing sections
2. Creating related sub-entities (NPCs for a city, lieutenants for a villain, etc.)
3. Generating deeper connections to other existing entities
4. Filling in image prompts if empty

## Instructions

### Step 1: Locate the Entity

1. Parse `$ARGUMENTS` for entity name or path
2. If path provided, read directly
3. If name provided, search in `Worlds/` directories:
   - Try exact match first
   - Then fuzzy match on filename and YAML `name:` field
4. If not found or ambiguous, list matches and ask user to clarify

### Step 2: Analyze Current State

Read the entity and assess:

1. **Section Completeness:**
   - Which sections are minimal (1-2 sentences)?
   - Which sections are empty?
   - Are image prompts filled?

2. **Connection Density:**
   - Count `[[wikilinks]]` in Connections section
   - Target: 5-8 connections minimum
   - Identify categories with no connections

3. **Related Entities:**
   - What related entities SHOULD exist but don't?
   - What sub-entities make sense (tavern in city, lieutenant for villain)?

4. **Cross-Reference Check:**
   - Do entities this one links to link back?

### Step 3: Present Expansion Options

Show the user what can be expanded:

```
=== EXPANSION OPTIONS: [Entity Name] ===

Current State:
- Sections: X/Y filled (Z minimal)
- Connections: X wikilinks
- Image Prompts: [Filled/Empty]

Recommended Expansions:

1. DEEPEN DETAIL
   - [Section A] - Currently 2 sentences, could expand to full paragraph
   - [Section B] - Empty, needs content
   - History section needs more specific events

2. CREATE SUB-ENTITIES
   - [Tavern] - The city needs a memorable inn
   - [Shop] - A notable merchant establishment
   - [NPC] - The mentioned "captain of the guard" deserves their own file

3. ADD CONNECTIONS
   - No connection to nearby [Region X]
   - Should link to [Organization Y] mentioned in text
   - Missing reciprocal link from [Entity Z]

4. FILL IMAGE PROMPTS
   - Portrait prompt is empty
   - Scene prompt needs entity-specific details

Which would you like to do? (1-4, or 'all', or describe specific needs)
```

### Step 4: Execute Expansion

#### 4A: Deepen Detail

For each section to expand:
1. Read current content
2. Generate 2-3x more detail maintaining consistency
3. Add specific names, numbers, sensory details
4. Show preview before applying
5. Use Edit tool to update section

**Section Expansion Targets:**
| Section Type | Minimum | Target |
|--------------|---------|--------|
| Overview | 3 sentences | 5-7 sentences |
| Personality | 2-3 traits | 4-5 traits with examples |
| History | 1 event | 3-4 key moments |
| Description | Brief | Full sensory details |

#### 4B: Create Sub-Entities

Based on entity type, offer relevant sub-entities:

**For Settlements (City/Town):**
- Tavern(s) - at least 1 per settlement
- Shop(s) - 2-3 notable merchants
- Temple - if deities exist in world
- Notable NPCs - leaders, quest-givers
- District details - if city

**For Characters (Antagonist/Protagonist):**
- Lieutenants/Allies - supporting characters
- Familiar - if magic user
- Signature Items - weapons, artifacts
- Lair/Headquarters - if villain

**For Organizations:**
- Leadership NPCs
- Headquarters settlement details
- Signature items/artifacts
- Rival organizations

**For Geography (Region):**
- Settlements within
- Geographic features
- Notable creatures
- Adventure sites

For each sub-entity:
1. Read appropriate template
2. Generate content linked to parent entity
3. Show preview, get approval
4. Save to appropriate folder
5. Update parent entity with link to new sub-entity

#### 4C: Add Connections

1. **Scan World:**
   - Read World Overview for major entities
   - Scan entity's category folder
   - Scan related category folders

2. **Identify Logical Connections:**
   - Geographic proximity
   - Organizational membership
   - Historical involvement
   - Trade/political relationships

3. **Add Bidirectional Links:**
   - Update current entity's Connections section
   - Update each connected entity to link back

**Connection Categories by Entity Type:**
| Entity Type | Connection Categories |
|-------------|----------------------|
| Character | Allies, Rivals, Organizations, Locations |
| Settlement | Region, Government, Organizations, Notable NPCs |
| Organization | Headquarters, Members, Allies, Rivals |
| Geography | Contains, Borders, Notable Locations |

#### 4D: Fill Image Prompts

1. Read entity content thoroughly
2. Extract key visual details:
   - Physical appearance
   - Setting/environment
   - Mood/atmosphere
   - Distinctive features
3. Generate specific prompts using template format:
   ```
   **Prompt:** [Art style from template], [specific subject], [key details], [setting], [mood/lighting], [notable features]
   ```
4. Update both prompt sections

### Step 5: Update World Overview

If significant content was added:
1. Read `World Overview.md`
2. Check if entity is referenced in Quick Reference
3. Add if missing and entity is significant
4. Update relevant category sections

### Step 6: Summary Report

```
=== EXPANSION COMPLETE: [Entity Name] ===

Changes Made:
- Expanded [X] sections with additional detail
- Created [Y] new sub-entities:
  - [[Sub-Entity 1]] (Type)
  - [[Sub-Entity 2]] (Type)
- Added [Z] new connections
- Filled [N] image prompts

Connection Density: [Before] → [After] wikilinks

New Related Entities:
- [[Entity 1]] - [brief description]
- [[Entity 2]] - [brief description]

Suggested Next Steps:
- Expand [[Related Entity]] for consistency
- Create encounter at this location
- Generate images with /generate-image
```

### Step 7: Offer Follow-up

After expansion:
> "Would you like me to:
> 1. Expand another entity
> 2. Generate an image for this entity
> 3. Create an encounter set here
> 4. Audit connections with /audit-world"

## Expansion Quality Guidelines

1. **Maintain Voice:** Match the existing tone and style
2. **Be Specific:** Use names, numbers, concrete details
3. **Connect Everything:** New content should reference existing entities
4. **Avoid Contradiction:** Don't contradict established facts
5. **Add Plot Hooks:** Include adventure opportunities
6. **Fill Gaps:** Address any logical gaps (ruler without advisors, etc.)

## Examples

```
# Expand a city
/expand-entity Ironhold City

# Expand by path
/expand-entity Worlds/Eldoria/Characters/Grom the Blacksmith.md

# Expand with specific focus
/expand-entity "Ironhold City" --focus npcs
```
