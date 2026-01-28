---
name: expand-region
description: Fill a region with villages, landmarks, encounters, local legends, travel hazards, and points of interest. Use when user wants to "flesh out a region", "populate an area", or "detail a territory".
argument-hint: "[region name or path]"
---

# Expand Region

Expand this region: $ARGUMENTS

## Overview

Takes an existing geographic region and fills it with:
1. Small settlements (villages, hamlets, outposts)
2. Landmarks and points of interest
3. Travel routes with hazards and encounters
4. Local legends and mysteries
5. Flora, fauna, and monsters
6. Hidden locations and dungeons
7. Regional culture and customs

## Instructions

### Step 1: Locate and Analyze the Region

1. **Parse `$ARGUMENTS`** for region name or path
2. **Search in `Worlds/[World]/Geography/`**
3. **Read the region file** and extract:
   - Region type (forest, plains, mountains, coast, etc.)
   - Climate and terrain
   - Parent continent
   - Existing settlements
   - Bordering regions
   - Known hazards
   - Controlling government/faction

4. **Determine expansion scope** by region type:

| Region Type | Settlements | Landmarks | Hazards | Dungeons |
|-------------|-------------|-----------|---------|----------|
| Forest | 3-5 | 4-6 | 4-5 | 2-3 |
| Plains | 5-8 | 3-4 | 2-3 | 1-2 |
| Mountains | 2-4 | 5-7 | 5-6 | 3-4 |
| Coast | 4-6 | 4-5 | 3-4 | 2-3 |
| Desert | 1-3 | 4-5 | 5-6 | 2-3 |
| Swamp | 1-3 | 3-4 | 5-6 | 2-3 |
| Tundra | 1-2 | 3-4 | 4-5 | 1-2 |

### Step 2: Present Expansion Plan

```
=== REGION EXPANSION: [Region Name] ===

Current State:
- Type: [Forest/Plains/Mountains/etc.]
- Terrain: [Description]
- Climate: [Description]
- Controlling Power: [[Government/Faction]]
- Existing Settlements: [count]
- Known Features: [list]

Proposed Expansion:

1. SETTLEMENTS ([X] new)
   - [Village 1]: [Concept - purpose/character]
   - [Village 2]: [Concept]
   - [Outpost]: [Concept]

2. LANDMARKS ([X] new)
   - [Landmark 1]: [Type - natural/artificial]
   - [Landmark 2]: [Type]
   - [Landmark 3]: [Type]

3. TRAVEL ROUTES ([X] defined)
   - [Route 1]: [From] to [To] - [Character]
   - [Route 2]: [From] to [To] - [Character]

4. HAZARDS & ENCOUNTERS ([X] defined)
   - [Hazard 1]: [Location/Route]
   - [Monster Lair]: [Creature type]

5. DUNGEONS & ADVENTURE SITES ([X] new)
   - [Dungeon 1]: [Type - ruin/cave/etc.]
   - [Dungeon 2]: [Type]

6. LOCAL LEGENDS ([X] stories)
   - [Legend 1]: [Brief hook]
   - [Legend 2]: [Brief hook]

7. FLORA & FAUNA
   - Notable creatures: [list]
   - Notable plants: [list]
   - Unique resources: [list]

Proceed? (yes/customize/skip sections)
```

### Step 3: Generate Settlements

Create small settlements throughout the region:

**Village Types by Region:**

| Region Type | Village Types |
|-------------|--------------|
| Forest | Lumber camp, Druid grove, Hunting village, Charcoal burners |
| Plains | Farming village, Herding community, Crossroads hamlet |
| Mountains | Mining village, Monastery, Mountain pass guard post |
| Coast | Fishing village, Smuggler's cove, Lighthouse hamlet |
| Desert | Oasis settlement, Nomad gathering point, Trade post |
| Swamp | Fishing hamlet, Herbalist community, Exile settlement |

**For each settlement:**
1. Read `Templates/Settlements/Village.md`
2. Generate with:
   - Name matching regional culture
   - Population (20-200)
   - Primary industry/purpose
   - 2-3 notable NPCs
   - Connection to region's features
   - One local problem or hook
3. Save to Settlements folder
4. Create key NPCs in Characters folder

**Settlement Distribution:**
- Cluster near water sources
- Place along trade routes
- Position near valuable resources
- Keep logical travel distances (1-2 days between)

### Step 4: Create Landmarks

Generate points of interest throughout the region:

**Natural Landmarks:**
- Ancient tree or grove
- Unusual rock formation
- Waterfall or hot spring
- Canyon or ravine
- Natural cave system
- Unique vista point

**Artificial Landmarks:**
- Ruined tower or keep
- Standing stones or monument
- Abandoned mine
- Old battlefield
- Ancient bridge
- Wayshrine or roadside temple

**Mysterious Landmarks:**
- Fairy circle or enchanted glade
- Cursed ground
- Portal or planar thin spot
- Prophetic site
- Elemental manifestation

**For each landmark:**
```markdown
### [Landmark Name]

**Type:** [Natural/Artificial/Mysterious]
**Location:** [Relative to settlements/routes]
**Description:** [2-3 sentences of visual detail]
**History:** [How it came to be, who knows about it]
**Current State:** [Condition, inhabitants if any]
**Secrets:** [Hidden aspects, buried treasure, etc.]
**Adventure Hook:** [Why adventurers would come here]
**Connections:** [[Related entities]]
```

### Step 5: Define Travel Routes

Map the ways through the region:

**Major Routes:**
- Connect to neighboring regions
- Pass through or near major settlements
- Well-maintained, regularly patrolled

**Minor Routes:**
- Connect villages to each other
- Less maintained, more dangerous
- Locals know shortcuts

**Secret Paths:**
- Known only to locals, criminals, or rangers
- Bypass hazards or checkpoints
- Lead to hidden locations

**For each route:**
```markdown
### [Route Name]

**Type:** [Major road/Minor path/Secret trail]
**From:** [[Starting Point]]
**To:** [[Destination]]
**Distance:** [X] miles / [X] days travel
**Terrain:** [What travelers encounter]
**Condition:** [Well-maintained/Overgrown/Treacherous]
**Traffic:** [Busy/Moderate/Rare]

**Waypoints:**
1. [Mile X]: [Feature or landmark]
2. [Mile X]: [Feature or landmark]
3. [Mile X]: [Feature or landmark]

**Hazards:**
- [Hazard 1]: [Description and frequency]
- [Hazard 2]: [Description and frequency]

**Encounters:**
| d6 | Encounter |
|----|-----------|
| 1 | [Encounter] |
| 2 | [Encounter] |
| 3 | [Encounter] |
| 4 | [Encounter] |
| 5 | [Encounter] |
| 6 | [Encounter] |

**Services:**
- [Mile X]: [[Inn/Waystation Name]]
- [Mile X]: [Other service]
```

### Step 6: Generate Hazards & Encounters

**Environmental Hazards by Region:**

| Region | Hazards |
|--------|---------|
| Forest | Quicksand, falling trees, wildfires, thick underbrush, predator territory |
| Plains | Flash floods, tornadoes, stampedes, grass fires, exposure |
| Mountains | Avalanches, rockslides, altitude sickness, sudden storms, narrow ledges |
| Coast | Riptides, high tides, sea caves, cliff erosion, fog |
| Desert | Sandstorms, dehydration, heat stroke, sinkholes, mirages |
| Swamp | Quicksand, disease, toxic plants, flooding, difficult navigation |

**Monster Lairs:**
Create 2-4 monster lairs appropriate to terrain:
1. Read `Templates/Creatures/Monster.md`
2. Generate creatures appropriate to region
3. Define lair location and territory
4. Create encounter parameters (CR, numbers)
5. Note treasure and hooks

**Bandit/Hostile Camps:**
- Outlaw hideouts
- Rival faction outposts
- Hostile tribe territories
- Cultist gathering sites

**For each hazard/lair:**
```markdown
### [Hazard/Lair Name]

**Type:** [Environmental/Monster/Humanoid]
**Location:** [Specific area within region]
**Threat Level:** [Low/Moderate/High/Deadly]
**Description:** [What it looks like, how to spot it]
**Inhabitants:** [Creatures, CR, numbers]
**Territory:** [How far they range]
**Behavior:** [Patrol patterns, hunting times]
**Treasure:** [What can be found]
**Adventure Hook:** [Why deal with this]
```

### Step 7: Create Dungeons & Adventure Sites

Generate detailed adventure locations:

**Dungeon Types by Region:**
- **Forest:** Druid temple ruins, fey court, giant's lair, witch's hut
- **Plains:** Burial mound, sunken temple, underground complex, monster nest
- **Mountains:** Dwarven ruins, dragon lair, mountain temple, mine complex
- **Coast:** Sea caves, shipwreck, underwater temple, smuggler's den
- **Desert:** Buried pyramid, tomb complex, oasis temple, sand-buried city
- **Swamp:** Sunken temple, hag's lair, lizardfolk warren, lost village

**For each dungeon:**
1. Read `Templates/Geography/Dungeon.md` or `Cave.md`
2. Generate with:
   - Evocative name
   - Origin/history
   - Current inhabitants
   - Rumored treasure
   - Challenge rating range
   - Connection to regional history
3. Include brief room/area overview (5-10 areas)
4. Note connections to other entities

### Step 8: Develop Local Legends

Create stories that locals tell:

**Legend Types:**
1. **Origin Legend** - How the region/landmark was created
2. **Hero Legend** - A great deed done here
3. **Tragedy Legend** - A terrible event that occurred
4. **Monster Legend** - A beast that haunts the area
5. **Treasure Legend** - Hidden riches waiting to be found
6. **Ghost Legend** - Spirits that linger
7. **Warning Legend** - Places to avoid and why

**For each legend:**
```markdown
### The Legend of [Name]

**Type:** [Origin/Hero/Tragedy/Monster/Treasure/Ghost/Warning]
**Told By:** [Who tells this story - everyone, elders, children]
**Summary:** [2-3 sentence version locals would share]

**The Full Tale:**
[Paragraph telling the complete legend as a local elder might]

**Truth Level:**
- [What's actually true]
- [What's exaggerated]
- [What's completely false]

**Related Locations:** [[Landmark or dungeon this connects to]]
**Adventure Hook:** [How PCs might investigate]
```

### Step 9: Catalog Flora & Fauna

**Regional Wildlife:**
Create 3-5 notable creatures:
1. Read creature templates
2. Generate animals appropriate to terrain
3. Note hunting/gathering value
4. Include behavioral notes

**Regional Plants:**
Create 3-5 notable plants:
1. Read `Templates/Creatures/Plant.md`
2. Generate flora appropriate to terrain
3. Note uses (food, medicine, poison, materials)
4. Include harvesting notes

**Resources:**
```markdown
## Regional Resources

### Harvestable
| Resource | Location | Value | Notes |
|----------|----------|-------|-------|
| [Resource 1] | [Where found] | [GP value] | [How to harvest] |
| [Resource 2] | [Where found] | [GP value] | [How to harvest] |

### Huntable
| Creature | Frequency | Value | Danger |
|----------|-----------|-------|--------|
| [Animal 1] | [Common/Uncommon/Rare] | [Parts value] | [CR] |
| [Animal 2] | [Common/Uncommon/Rare] | [Parts value] | [CR] |

### Unique to Region
- [Unique resource]: [Description and significance]
```

### Step 10: Define Regional Culture

Add cultural detail for settlements in this region:

```markdown
## Regional Culture

### The People
- **Common Ancestry:** [Human ethnicities, demi-human populations]
- **Typical Occupations:** [Farmer, hunter, miner, etc.]
- **Social Structure:** [Egalitarian, hierarchical, etc.]

### Customs
- **Greeting:** [How locals greet strangers]
- **Hospitality:** [How guests are treated]
- **Trade:** [Bartering customs, fair prices]
- **Taboos:** [What not to do]

### Local Beliefs
- **Primary Deity:** [[Deity]] - [How worshipped locally]
- **Superstitions:** [Local folk beliefs]
- **Omens:** [What they watch for]

### Festivals
| Festival | Time | Purpose | Activities |
|----------|------|---------|------------|
| [Festival 1] | [Season/Date] | [Reason] | [What happens] |
| [Festival 2] | [Season/Date] | [Reason] | [What happens] |

### Local Fare
- **Signature Dish:** [Description]
- **Common Drink:** [Description]
- **Special Delicacy:** [Description]
```

### Step 11: Update All Connections

1. **Update region file** with all new content
2. **Update parent continent** with region details
3. **Update each new settlement** with region link
4. **Update bordering regions** with shared features
5. **Connect dungeons** to historical events
6. **Link creatures** to their territories
7. **Update World Overview** with major new locations

### Step 12: Create Regional Map Notes

Add a section to help with mapping:

```markdown
## Map Notes

### Key Locations
| Symbol | Name | Type | Grid Ref |
|--------|------|------|----------|
| ▲ | [Mountain] | Peak | [A1] |
| ● | [[Village]] | Settlement | [B3] |
| ★ | [[Landmark]] | Point of Interest | [C2] |
| ☠ | [[Dungeon]] | Adventure Site | [D4] |

### Travel Times (by horse)
| From | To | Days | Route |
|------|-----|------|-------|
| [[A]] | [[B]] | 2 | [Route name] |
| [[B]] | [[C]] | 1 | [Route name] |

### Territorial Boundaries
- [Faction/Creature] controls [area description]
- [Faction/Creature] controls [area description]
```

### Step 13: Summary Report

```
=== REGION EXPANSION COMPLETE: [Name] ===

New Entities Created:

SETTLEMENTS ([X]):
- [[Village 1]] - [Type, Population]
- [[Village 2]] - [Type, Population]

LANDMARKS ([X]):
- [[Landmark 1]] - [Type]
- [[Landmark 2]] - [Type]

DUNGEONS ([X]):
- [[Dungeon 1]] - [Type, CR range]
- [[Dungeon 2]] - [Type, CR range]

CREATURES ([X]):
- [[Creature 1]] - [Type]
- [[Creature 2]] - [Type]

PLANTS ([X]):
- [[Plant 1]] - [Use]
- [[Plant 2]] - [Use]

ROUTES DEFINED: [X]
- [Route 1]: [From] to [To]
- [Route 2]: [From] to [To]

LEGENDS CREATED: [X]
- [Legend 1] - [Type]
- [Legend 2] - [Type]

HAZARDS DOCUMENTED: [X]
- [Hazard 1] - [Threat level]
- [Hazard 2] - [Threat level]

Regional Culture: Defined
- Customs, festivals, local fare documented

Suggested Next Steps:
- Expand [[Village]] into full detail
- Create encounters for [[Route]]
- Develop [[Dungeon]] into full adventure
- Generate regional map with /create-entity Map
```

## Quality Guidelines

1. **Geographic Logic** - Features follow terrain (rivers from mountains, etc.)
2. **Economic Sense** - Settlements exist for reasons (resources, trade, defense)
3. **Travel Realism** - Distances and times make sense
4. **Danger Gradient** - Wilderness gets more dangerous away from civilization
5. **Cultural Coherence** - Local customs fit the environment
6. **Historical Layers** - Ruins and legends reflect world history
7. **Adventure Density** - Something interesting every travel day

## Examples

```
# Expand a forest region
/expand-region "The Thornwood"

# Expand with path
/expand-region Worlds/Eldermyr/Geography/The Ashlands.md

# Focus on specific aspect
/expand-region "Northern Reaches" --focus dungeons
```
