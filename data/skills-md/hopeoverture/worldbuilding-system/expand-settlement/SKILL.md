---
name: expand-settlement
description: Deep-dive into a settlement, generating NPCs, shops, taverns, districts, local issues, rumors, and daily life details. Use when user wants to "flesh out a city", "populate a town", or "add NPCs to a settlement".
argument-hint: "[settlement name or path]"
---

# Expand Settlement

Expand this settlement: $ARGUMENTS

## Overview

Takes an existing settlement (Village, Town, City, or Stronghold) and populates it with:
1. Named NPCs with roles and personalities
2. Notable establishments (taverns, shops, temples)
3. District/neighborhood definitions (for cities)
4. Local issues, rumors, and plot hooks
5. Daily life and atmosphere details

## Instructions

### Step 1: Locate and Analyze the Settlement

1. **Parse `$ARGUMENTS`** for settlement name or path
2. **Search in `Worlds/`** directories if name provided
3. **Read the settlement file** and extract:
   - Settlement type (Village/Town/City/Stronghold)
   - Population size
   - Government/leadership
   - Primary industries/purpose
   - Existing NPCs mentioned
   - Cultural flavor
   - Parent region and world

4. **Determine expansion scope** based on settlement type:

| Type | NPCs | Establishments | Districts | Rumors |
|------|------|----------------|-----------|--------|
| Village | 5-8 | 2-3 | N/A | 3-4 |
| Town | 10-15 | 5-8 | 2-3 informal | 5-6 |
| City | 15-25 | 10-15 | 4-6 formal | 8-10 |
| Stronghold | 8-12 | 3-5 | N/A (sections) | 4-5 |

### Step 2: Present Expansion Plan

Show the user what will be generated:

```
=== SETTLEMENT EXPANSION: [Settlement Name] ===

Current State:
- Type: [City/Town/Village/Stronghold]
- Population: [X]
- Existing NPCs: [count]
- Existing Establishments: [count]

Proposed Expansion:

1. LEADERSHIP & AUTHORITY ([X] NPCs)
   - [Role 1]: [Brief concept]
   - [Role 2]: [Brief concept]

2. COMMERCE & SERVICES ([X] establishments + NPCs)
   - [Shop type]: [Concept]
   - [Tavern]: [Concept]

3. FAITH & CULTURE ([X] entities)
   - [Temple]: [Deity]
   - [Cultural site]: [Concept]

4. COMMON FOLK ([X] NPCs)
   - [Role]: [Concept]

5. UNDERWORLD ([X] NPCs, if appropriate)
   - [Criminal element]: [Concept]

6. DISTRICTS (if City)
   - [District 1]: [Character]
   - [District 2]: [Character]

7. LOCAL ISSUES & RUMORS ([X] hooks)
   - [Hook 1]
   - [Hook 2]

Proceed with expansion? (yes/customize/skip sections)
```

### Step 3: Generate Leadership & Authority

Based on settlement's government type, create:

**For Hereditary Rule:**
- Lord/Lady of the settlement (Support Character)
- Steward/Seneschal (Background Character)
- Captain of the Guard (Support Character)
- Court Advisor or Spymaster (Support or Antagonist)

**For Elected/Council:**
- Mayor/Burgomeister (Support Character)
- Council Members (2-3 Background Characters)
- Town Sheriff (Support Character)

**For Theocratic:**
- High Priest/Priestess (Support Character)
- Temple Hierarchy (Background Characters)
- Temple Guard Captain (Background Character)

**For Military (Stronghold):**
- Commander (Support Character)
- Lieutenant(s) (Background Characters)
- Quartermaster (Background Character)
- Scout/Intelligence Officer (Support Character)

**For each leader NPC:**
1. Read appropriate character template
2. Generate with connections to:
   - The settlement
   - Parent government/organization
   - Other local NPCs (rivals, allies)
   - At least one secret or plot hook
3. Include personality quirks and mannerisms
4. Save to `Worlds/[World]/Characters/`

### Step 4: Generate Commerce & Services

**Taverns** (1 per village, 2-3 per town, 4-6 per city):

For each tavern:
1. Read `Templates/Settlements/Tavern.md`
2. Generate with:
   - Unique name reflecting local culture
   - Distinctive atmosphere (rowdy, refined, mysterious, cozy)
   - Proprietor NPC (Support Character)
   - 2-3 regular patrons (Background Characters)
   - Signature food/drink
   - One rumor or plot hook
3. Save to `Worlds/[World]/Settlements/`
4. Create proprietor NPC, save to Characters/

**Shops** (scale by settlement size):

| Shop Type | Village | Town | City |
|-----------|---------|------|------|
| General Store | 1 | 1 | 1-2 |
| Blacksmith | 0-1 | 1 | 2-3 |
| Apothecary | 0 | 1 | 1-2 |
| Specialty (jeweler, etc.) | 0 | 0-1 | 2-4 |
| Magic Shop | 0 | 0-1 | 1-2 |

For each shop:
1. Read `Templates/Settlements/Shop.md`
2. Generate with:
   - Unique name
   - Specialty inventory hook
   - Proprietor NPC
   - One interesting customer or supplier connection
3. Save shop and proprietor

**Temples** (1 per town, 2-4 per city):
1. Read `Templates/Settlements/Temple.md`
2. Connect to established world deities
3. Generate head priest NPC
4. Include temple services and local significance

### Step 5: Generate Common Folk

Create NPCs that give the settlement flavor:

**Essential Roles:**
- Town crier or gossip
- Street vendor or market regular
- Local drunk or storyteller
- Craftsperson (not shopkeeper)
- Farmer/fisher/miner (based on local industry)

**For each:**
1. Read `Templates/Characters/Background Character.md`
2. Generate with:
   - Simple but memorable personality trait
   - One piece of local knowledge
   - Connection to at least one other NPC
   - Potential minor quest hook

### Step 6: Generate Underworld (if appropriate)

For Towns and Cities with sufficient population:

**Criminal Elements:**
- Thieves' Guild contact or fence
- Black market dealer
- Corrupt official
- Gang leader (for larger cities)
- Smuggler (for ports/border towns)

**For each:**
1. Use Antagonist or Support Character template
2. Connect to any established Criminal Organizations
3. Include their racket/operation
4. Add conflict with law enforcement NPCs

### Step 7: Define Districts (Cities Only)

Create 4-6 named districts with distinct character:

**Standard District Types:**
1. **Noble/Palace District** - Wealth, guards, exclusive
2. **Market/Merchant District** - Commerce, crowds, diversity
3. **Temple District** - Religious, peaceful, pilgrims
4. **Docks/Harbor** (if coastal) - Rough, foreign, smuggling
5. **Craftsmen's Quarter** - Industry, guilds, pride
6. **Slums/Lower Ward** - Poverty, crime, desperation
7. **Foreign Quarter** - Exotic, cultural, isolated

**For each district:**
1. Write a section in the settlement file describing:
   - General atmosphere and architecture
   - Dominant population
   - Key establishments located there
   - Typical sights, sounds, smells
   - Common encounters
2. Assign previously created establishments to districts
3. Note district boundaries and transitions

### Step 8: Generate Local Issues & Rumors

Create a "Rumors & Hooks" section in the settlement file:

**Rumor Types to Include:**
1. **True Rumor** - Leads to actual adventure
2. **Partially True** - Contains truth but misleading
3. **False Rumor** - Red herring or gossip
4. **Local Politics** - About settlement leadership
5. **Regional Threat** - Connects to wider world
6. **Historical Secret** - About the settlement's past

**Format each as:**
```markdown
### Rumors & Plot Hooks

| # | Rumor | Truth Level | Hook |
|---|-------|-------------|------|
| 1 | "The baker's son..." | True | Missing person quest |
| 2 | "Gold in the old mine..." | Partial | Actually monster lair |
| 3 | "The mayor takes bribes..." | False | Political rival spreading lies |
```

**Local Issues to Address:**
- Resource shortage or trade problem
- Criminal activity or corruption
- External threat (monsters, bandits, rival settlement)
- Internal conflict (factions, guilds, families)
- Mystery or haunting
- Festival or upcoming event

### Step 9: Add Daily Life Details

Enhance the settlement's Description section with:

**Morning:**
- What sounds wake residents
- Who's up earliest and why
- Morning markets or routines

**Midday:**
- Peak activity description
- Common sights in streets
- Where people eat

**Evening:**
- Tavern atmosphere
- Guard patrol patterns
- Entertainment options

**Night:**
- Who's out after dark
- Dangers and patrols
- Secret activities

**Seasonal Variations:**
- Festival days
- Harvest/planting times
- Winter hardships
- Trade season peaks

### Step 10: Update Connections

1. **Update the settlement file** with links to all new entities
2. **Update each new NPC** with connection to settlement
3. **Update each establishment** with:
   - Parent settlement link
   - District location (if city)
   - Connected NPCs
4. **Update World Overview** if settlement is significant
5. **Cross-reference** new NPCs with existing organizations

### Step 11: Summary Report

```
=== SETTLEMENT EXPANSION COMPLETE: [Name] ===

New Entities Created:

CHARACTERS ([X] total):
Leadership:
- [[NPC 1]] - [Role]
- [[NPC 2]] - [Role]

Commerce:
- [[NPC 3]] - Proprietor of [[Tavern]]
- [[NPC 4]] - Owner of [[Shop]]

Common Folk:
- [[NPC 5]] - [Role]
- [[NPC 6]] - [Role]

Underworld:
- [[NPC 7]] - [Role]

ESTABLISHMENTS ([X] total):
Taverns:
- [[Tavern Name]]

Shops:
- [[Shop 1]]
- [[Shop 2]]

Temples:
- [[Temple Name]]

DISTRICTS DEFINED: [X]
- [District 1] - [brief character]
- [District 2] - [brief character]

RUMORS & HOOKS: [X]
- [Hook 1 summary]
- [Hook 2 summary]

Connection Density:
- Settlement now has [X] outgoing wikilinks
- [X] new entities link back to settlement

Suggested Next Steps:
- Generate images for key NPCs
- Create encounter at [[Location]]
- Expand nearby [[Settlement]] for comparison
- Develop [[NPC]]'s secret plot
```

### Step 12: Offer Follow-up

> "Would you like me to:
> 1. Generate portraits for key NPCs (/generate-image)
> 2. Create a random encounter set for this settlement
> 3. Expand a connected settlement
> 4. Develop a specific NPC's storyline
> 5. Create a local dungeon or adventure site"

## Quality Guidelines

1. **Cultural Consistency** - Names, customs, and attitudes match the region
2. **Economic Logic** - Shops and services match population needs
3. **Social Stratification** - Clear class distinctions where appropriate
4. **Internal Conflicts** - NPCs have relationships and tensions
5. **Adventure Potential** - Every section has hooks for gameplay
6. **Sensory Details** - Include sights, sounds, smells throughout
7. **Memorable NPCs** - Each has at least one distinctive trait

## Examples

```
# Expand a city with full detail
/expand-settlement Ironhold

# Expand with path
/expand-settlement Worlds/Eldermyr/Settlements/Thornhaven.md

# Expand focusing on specific aspect
/expand-settlement "Riverside" --focus commerce
```
