---
name: generate-world
description: Generate an entire world with interconnected entities. Creates 80-120 entities including continents, regions, settlements, NPCs, organizations, history, and more. Use when the user wants a complete world generated automatically.
argument-hint: "[world name]"
---

# Generate Complete World

Generate a complete world: $ARGUMENTS

## Overview

This skill creates an entire interconnected world through a multi-phase workflow. It generates approximately **80-120 entities** using the 75 core worldbuilding templates (87 total templates exist including DM tools like Encounters and Maps), organized in the proper folder structure with `[[wikilinks]]` connecting everything together.

**Important:** This is a long-running workflow. Progress updates will be provided between phases, and the workflow will pause at key checkpoints for your approval.

## Instructions

---

### Phase 1: World Foundation

**Goal:** Create the world directory and establish core identity.

1. **Parse the world name** from arguments. If not provided, ask the user.

2. **Ask for world concept** (if not provided):
   - Genre/tone (epic fantasy, dark fantasy, etc.)
   - Magic level (none, rare, common, pervasive)
   - Technology level (primitive, medieval, renaissance, etc.)
   - Any specific themes or inspirations

3. **Create directory structure:**
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

4. **Generate World Overview.md** with filled content:
   - Premise (2-3 sentences establishing the world's hook)
   - Tone and central themes
   - Magic and technology levels
   - Initial cosmology notes
   - Placeholder sections for entities to come

5. **CHECKPOINT:** Present the world premise to user for approval before continuing.

---

### Phase 2: Cosmology & Concepts

**Goal:** Establish the metaphysical foundations of the world.

**Templates used:** Pantheon, Deity, Religion, Magic System, Technology, Language, Prophecy, Plane of Existence, Currency, Calendar (10 templates)

Create the following entities:

1. **Planes of Existence** (2-3 entities)
   - Read `Templates/Concepts/Plane of Existence.md`
   - Create the Material Plane, an Upper Plane (divine realm), and a Lower Plane or Shadowfell equivalent
   - Establish how planes interact

2. **Pantheon** (1 entity)
   - Read `Templates/Concepts/Pantheon.md`
   - Generate a pantheon with 5-6 deity slots
   - Establish divine hierarchy and relationships
   - Connect to planes via `[[Plane Name]]`

3. **Deities** (5-6 entities)
   - Read `Templates/Concepts/Deity.md`
   - Create diverse domains covering:
     - Sun/Light/Life deity
     - War/Strength deity
     - Nature/Harvest deity
     - Death/Underworld deity
     - Magic/Knowledge deity
     - Trickery/Shadow deity (optional)
   - Ensure deities have relationships with each other
   - Connect each to pantheon and appropriate plane

4. **Religion** (1-2 entities)
   - Read `Templates/Concepts/Religion.md`
   - Create primary organized religion (monotheistic focus or pantheon worship)
   - If world has conflict, create a secondary/rival religion
   - Connect to pantheon and relevant deities

5. **Magic System** (1 entity, if magic exists)
   - Read `Templates/Concepts/Magic System.md`
   - Define how magic works in this world
   - Reference deities if magic is divine
   - Establish schools, sources, limitations

6. **Technology** (1 entity)
   - Read `Templates/Concepts/Technology.md`
   - Define the world's technological baseline
   - Note any magitech or unique innovations
   - Connect to relevant organizations

7. **Language** (2-3 entities)
   - Read `Templates/Concepts/Language.md`
   - Create Common tongue
   - Create 1-2 regional/racial languages
   - Note scripts and linguistic families

8. **Calendar** (1 entity)
   - Read `Templates/Concepts/Calendar.md`
   - Create months, seasons, important dates
   - Reference deities in holy days
   - Include seasonal festivals

9. **Currency** (1-2 entities)
   - Read `Templates/Concepts/Currency.md`
   - Create primary monetary system
   - Optional: rival nation's currency

10. **Prophecy** (1 entity)
    - Read `Templates/Concepts/Prophecy.md`
    - Create a central prophecy that drives world events
    - Connect to deities, history, current conflicts

**Save all to:** `Worlds/[World Name]/Concepts/`

**Phase 2 Total: 16-22 entities**

---

### Phase 3: Geography - Continents & Oceans

**Goal:** Establish the world's major landmasses and waters.

**Templates used:** Continent, Ocean, Coast, Island (4 templates)

1. **Create Continents** (2 entities)
   - Read `Templates/Geography/Continent.md`
   - Create main continent and a secondary landmass
   - Define climate zones, major features
   - Establish 3-4 regions per continent
   - Note bordering oceans/seas

2. **Create Oceans** (1-2 entities)
   - Read `Templates/Geography/Ocean.md`
   - Create primary ocean separating/bordering continents
   - Include sea routes and dangers

3. **Create Coasts** (2 entities)
   - Read `Templates/Geography/Coast.md`
   - Create notable coastlines (trading coast, pirate waters, etc.)
   - Connect to continents and ocean

4. **Create Islands** (1-2 entities)
   - Read `Templates/Geography/Island.md`
   - Create mysterious or strategic islands
   - Connect to nearest continent and ocean

**Save to:** `Worlds/[World Name]/Geography/`

**CHECKPOINT:** Present continent layout to user for approval.

**Phase 3 Total: 6-8 entities**

---

### Phase 4: Geography - Regions & Features

**Goal:** Fill continents with distinct regions and terrain.

**Templates used:** Region, Mountain Range, Forest, River, Road, Desert, Tundra, Plains, Hills, Steppes, Lake, Pass, Cave, Dungeon (14 templates)

For each continent, create:

1. **Regions** (6-8 entities total)
   - Read `Templates/Geography/Region.md`
   - Vary terrain types across regions
   - Define borders, climate, resources
   - Connect to parent continent
   - Connect to neighboring regions

2. **Mountain Ranges** (2-3 entities)
   - Read `Templates/Geography/Mountain Range.md`
   - Create natural borders between regions
   - Include notable peaks, passes, dangers

3. **Forests** (2-3 entities)
   - Read `Templates/Geography/Forest.md`
   - Vary types (ancient, haunted, cultivated)
   - Include inhabitants and dangers

4. **Rivers** (2-3 entities)
   - Read `Templates/Geography/River.md`
   - Flow from mountains to coasts/lakes
   - Connect settlements along their length

5. **Lakes** (1-2 entities)
   - Read `Templates/Geography/Lake.md`
   - Create significant bodies of water
   - Include legends or inhabitants

6. **Plains/Grasslands** (1-2 entities)
   - Read `Templates/Geography/Plains.md`
   - Create agricultural or nomadic regions

7. **Desert** (1 entity, if climate appropriate)
   - Read `Templates/Geography/Desert.md`
   - Create harsh wasteland with secrets

8. **Tundra** (1 entity, if climate appropriate)
   - Read `Templates/Geography/Tundra.md`
   - Create frozen northern/southern reaches

9. **Hills** (1-2 entities)
   - Read `Templates/Geography/Hills.md`
   - Create transitional terrain

10. **Steppes** (1 entity, if appropriate)
    - Read `Templates/Geography/Steppes.md`
    - Create nomadic horse-lord territory

11. **Mountain Passes** (1-2 entities)
    - Read `Templates/Geography/Pass.md`
    - Create strategic chokepoints
    - Connect to roads and trade routes

12. **Roads** (3-4 entities)
    - Read `Templates/Geography/Road.md`
    - Create major trade routes
    - Connect settlements and regions
    - Reference terrain they traverse

13. **Caves** (2-3 entities)
    - Read `Templates/Geography/Cave.md`
    - Create natural dungeon sites
    - Include inhabitants and treasures

14. **Dungeons** (2-3 entities)
    - Read `Templates/Geography/Dungeon.md`
    - Create adventure sites (ruins, tombs, lairs)
    - Connect to history and current threats

**Save to:** `Worlds/[World Name]/Geography/`

**Phase 4 Total: 22-32 entities**

---

### Phase 5: Civilizations & Organizations

**Goal:** Populate regions with political entities and power structures.

**Templates used:** Government, Military, Guild, Religious Order, Cult, Criminal Organization, Business, Organization (General), Academy (9 templates)

1. **Governments** (4-6 entities)
   - Read `Templates/Organizations/Government.md`
   - Create variety:
     - Hereditary Kingdom
     - Theocratic State
     - Merchant Republic
     - Tribal Confederation
     - Magocracy (if magic is common)
   - Connect to regions, deities, history
   - Establish rivalries and alliances

2. **Military Organizations** (4-6 entities)
   - Read `Templates/Organizations/Military.md`
   - Create for each major government:
     - Royal Army/Legion
     - Naval Fleet
     - Elite Guard/Knights
   - Connect to parent government

3. **Guilds** (2-3 entities)
   - Read `Templates/Organizations/Guild.md`
   - Create economic powers:
     - Merchants' Guild
     - Craftsmen's Guild
     - Adventurers' Guild
   - Connect to settlements, governments

4. **Religious Orders** (2-3 entities)
   - Read `Templates/Organizations/Religious Order.md`
   - Create for major deities:
     - Militant holy order
     - Monastic tradition
     - Healing order
   - Connect to religion, deities, temples

5. **Cults** (1-2 entities)
   - Read `Templates/Organizations/Cult.md`
   - Create secret or forbidden groups
   - Connect to darker deities or prophecy

6. **Criminal Organizations** (1-2 entities)
   - Read `Templates/Organizations/Criminal Organization.md`
   - Create underworld powers:
     - Thieves' Guild
     - Smuggling Ring
   - Connect to cities, rival organizations

7. **Businesses** (1-2 entities)
   - Read `Templates/Organizations/Business.md`
   - Create powerful merchant houses
   - Connect to trade routes, cities

8. **Academies** (1-2 entities)
   - Read `Templates/Organizations/Academy.md`
   - Create centers of learning:
     - Mage College (if magic exists)
     - Bardic College
     - Military Academy
   - Connect to magic system, governments

9. **General Organizations** (1-2 entities)
   - Read `Templates/Organizations/Organization (General).md`
   - Create miscellaneous factions:
     - Secret Society
     - Explorer's League
     - Druid Circle
   - Connect to various entities

**Save to:** `Worlds/[World Name]/Organizations/`

**CHECKPOINT:** Present civilization structure to user for approval.

**Phase 5 Total: 17-28 entities**

---

### Phase 6: Settlements

**Goal:** Create settlements throughout the regions.

**Templates used:** City, Town, Village, Stronghold, Library (5 templates)

For each region:

1. **Cities** (1 per major region, 4-6 total)
   - Read `Templates/Settlements/City.md`
   - Make regional capitals
   - Connect to region, government, organizations
   - Reference geographic features

2. **Towns** (1-2 per region, 6-10 total)
   - Read `Templates/Settlements/Town.md`
   - Vary purposes:
     - Trade hub
     - Mining town
     - Port town
     - Border town
     - Pilgrimage site
   - Connect to parent region and nearest city

3. **Villages** (2-3 per region, 10-15 total)
   - Read `Templates/Settlements/Village.md`
   - Create variety:
     - Farming village
     - Fishing village
     - Logging camp
     - Mining hamlet
   - Connect to parent region

4. **Strongholds** (2-3 entities)
   - Read `Templates/Settlements/Stronghold.md`
   - Create military fortifications:
     - Border fortress
     - Mountain keep
     - Coastal citadel
   - Connect to military, government, strategic locations

5. **Libraries** (1-2 entities)
   - Read `Templates/Settlements/Library.md`
   - Create centers of knowledge:
     - Grand Archive
     - Forbidden Collection
   - Connect to academies, magic system, history

**Save to:** `Worlds/[World Name]/Settlements/`

**Phase 6 Total: 23-36 entities**

---

### Phase 7: Settlement Details

**Goal:** Populate major settlements with establishments and NPCs.

**Templates used:** Tavern, Shop, Temple (3 templates from Settlements), Support Character, Background Character, Antagonist (3 templates from Characters)

For each city and major town:

1. **Taverns** (1-2 per major settlement, 8-12 total)
   - Read `Templates/Settlements/Tavern.md`
   - Create memorable establishments with:
     - Unique atmosphere
     - Colorful proprietor
     - Regular patrons
     - Plot hooks

2. **Shops** (2-3 per major settlement, 12-18 total)
   - Read `Templates/Settlements/Shop.md`
   - Vary types:
     - Blacksmith/Armorer
     - Apothecary/Alchemist
     - General Store
     - Exotic Imports
     - Magic Shop (if appropriate)

3. **Temples** (1 per major settlement, 5-8 total)
   - Read `Templates/Settlements/Temple.md`
   - Connect to established religion and deities
   - Vary deity focus per region

4. **Support Characters - Leaders** (1 per major settlement, 6-10 total)
   - Read `Templates/Characters/Support Character.md`
   - Create settlement rulers:
     - City Lord/Mayor
     - Governor
     - Council Head

5. **Support Characters - Proprietors** (1-2 per major settlement, 8-15 total)
   - Read `Templates/Characters/Support Character.md`
   - Create memorable shopkeepers and innkeepers
   - Give each secrets and connections

6. **Support Characters - Quest-givers** (1 per major settlement, 5-8 total)
   - Read `Templates/Characters/Support Character.md`
   - Create adventure hooks:
     - Mysterious stranger
     - Desperate merchant
     - Haunted noble

7. **Background Characters** (2-3 per city, 8-12 total)
   - Read `Templates/Characters/Background Character.md`
   - Create local color:
     - Town crier
     - Street vendor
     - Gossip
     - Guard captain

8. **Local Antagonists** (1 per major city, 4-6 total)
   - Read `Templates/Characters/Antagonist.md`
   - Create regional villains:
     - Crime boss
     - Corrupt official
     - Cult leader
     - Rival merchant
   - Connect to criminal organizations, cults

**Save Characters to:** `Worlds/[World Name]/Characters/`
**Save Settlements to:** `Worlds/[World Name]/Settlements/`

**Phase 7 Total: 56-89 entities (cumulative establishment + character count)**

---

### Phase 8: History

**Goal:** Create the world's historical timeline.

**Templates used:** Age, Event, War, Battle, Treaty, Trade Agreement, Tragedy, Dynasty (8 templates)

1. **Ages** (4 entities)
   - Read `Templates/History/Age.md`
   - Create chronological eras:
     - **Age of Creation/Myth** - Gods shape the world
     - **Age of Expansion** - Civilizations grow
     - **Age of Conflict** - Great wars reshape borders
     - **Current Age** - Present tensions
   - Connect ages to each other

2. **Major Events** (3-4 entities)
   - Read `Templates/History/Event.md`
   - Create world-shaping moments:
     - The Sundering/Cataclysm
     - Discovery of Magic
     - First Contact between peoples
     - Fall of an Empire
   - Connect to ages, regions, governments

3. **Wars** (2 entities)
   - Read `Templates/History/War.md`
   - Create conflicts that shaped politics:
     - Ancient war (mythic scale)
     - Recent war (living memory)
   - Connect to governments, regions, ages

4. **Battles** (2-3 entities)
   - Read `Templates/History/Battle.md`
   - Create decisive moments:
     - Battle that ended a war
     - Last stand of a hero
     - Siege of a great city
   - Connect to wars, locations, characters

5. **Treaties** (1-2 entities)
   - Read `Templates/History/Treaty.md`
   - Create peace agreements:
     - Treaty ending major war
     - Alliance pact
   - Connect to governments, wars

6. **Trade Agreements** (1 entity)
   - Read `Templates/History/Trade Agreement.md`
   - Create economic pacts between nations
   - Connect to governments, guilds, roads

7. **Tragedies** (1-2 entities)
   - Read `Templates/History/Tragedy.md`
   - Create disasters:
     - Plague
     - Natural disaster
     - Magical catastrophe
   - Connect to regions, ages, current conditions

8. **Dynasties** (2-3 entities)
   - Read `Templates/History/Dynasty.md`
   - Create ruling bloodlines:
     - Current ruling dynasty
     - Fallen dynasty
     - Rising house
   - Connect to governments, characters

**Save to:** `Worlds/[World Name]/History/`

**CHECKPOINT:** Present historical timeline to user for approval.

**Phase 8 Total: 16-21 entities**

---

### Phase 9: Creatures & Flora

**Goal:** Populate the world with unique life forms.

**Templates used:** Species, Monster, Animal, Insect, Plant (5 templates)

1. **Species/Races** (3-4 entities)
   - Read `Templates/Creatures/Species.md`
   - Create unique peoples:
     - Native/ancient race
     - Reclusive/mysterious people
     - Hostile/misunderstood species
     - Recently discovered people
   - Connect to regions, history, governments

2. **Monsters** (4-5 entities)
   - Read `Templates/Creatures/Monster.md`
   - Create regional threats:
     - Apex predator (dragon-type)
     - Undead menace
     - Aberration/eldritch horror
     - Regional beast (unique to one area)
     - Legendary creature (tied to prophecy)
   - Connect to dungeons, regions, history

3. **Animals** (3-4 entities)
   - Read `Templates/Creatures/Animal.md`
   - Create notable wildlife:
     - Mount/beast of burden
     - Hunted game
     - Dangerous predator
     - Exotic/rare creature
   - Connect to regions, cultures

4. **Insects** (1-2 entities)
   - Read `Templates/Creatures/Insect.md`
   - Create notable bugs:
     - Swarming menace
     - Useful/farmed insect
   - Connect to regions, ecology

5. **Plants** (2-3 entities)
   - Read `Templates/Creatures/Plant.md`
   - Create notable flora:
     - Healing herb
     - Dangerous plant
     - Sacred tree/flower
     - Magical reagent
   - Connect to regions, magic system, alchemy

**Save to:** `Worlds/[World Name]/Creatures/`

**Phase 9 Total: 13-18 entities**

---

### Phase 10: Items & Equipment

**Goal:** Create notable items throughout the world.

**Templates used:** Weapon, Armor, Wondrous Magic Item, Artifact, Potion, Gear, Food, Drink, Container, Vehicle, Book (11 templates)

1. **Artifacts** (2-3 entities)
   - Read `Templates/Items/Artifact.md`
   - Create legendary items:
     - Divine relic (tied to deity)
     - Royal regalia (tied to dynasty)
     - Lost weapon of a hero
   - Connect to history, characters, prophecy

2. **Weapons** (2-3 entities)
   - Read `Templates/Items/Weapon.md`
   - Create notable weapons:
     - Signature weapon of a nation
     - Rare material weapon
     - Cursed blade
   - Connect to military, history

3. **Armor** (1-2 entities)
   - Read `Templates/Items/Armor.md`
   - Create notable armor:
     - Royal/ceremonial armor
     - Legendary hero's mail
   - Connect to military, history

4. **Wondrous Magic Items** (2-3 entities)
   - Read `Templates/Items/Wondrous Magic Item.md`
   - Create useful magic items:
     - Navigation tool
     - Communication device
     - Protective charm
   - Connect to magic system, academies

5. **Potions** (2-3 entities)
   - Read `Templates/Items/Potion.md`
   - Create regional brews:
     - Healing potion variant
     - Performance enhancer
     - Dangerous/forbidden elixir
   - Connect to plants, shops, magic

6. **Gear** (1-2 entities)
   - Read `Templates/Items/Gear.md`
   - Create specialized equipment:
     - Explorer's kit
     - Climber's tools
   - Connect to guilds, regions

7. **Food** (2-3 entities)
   - Read `Templates/Items/Food.md`
   - Create regional cuisine:
     - National dish
     - Festival food
     - Travel rations
   - Connect to cultures, settlements

8. **Drinks** (2-3 entities)
   - Read `Templates/Items/Drink.md`
   - Create regional beverages:
     - Famous ale/wine
     - Exotic spirit
     - Ceremonial drink
   - Connect to taverns, cultures

9. **Containers** (1 entity)
   - Read `Templates/Items/Container.md`
   - Create notable container:
     - Bag of holding variant
     - Sacred vessel
   - Connect to magic, religion

10. **Vehicles** (2-3 entities)
    - Read `Templates/Items/Vehicle.md`
    - Create transportation:
      - Trading vessel
      - War machine
      - Exotic mount/vehicle
    - Connect to military, guilds, technology

11. **Books** (2-3 entities)
    - Read `Templates/Items/Book.md`
    - Create important texts:
      - Holy scripture
      - Historical chronicle
      - Forbidden grimoire
      - Map/atlas
    - Connect to libraries, religion, magic, history

**Save to:** `Worlds/[World Name]/Items/`

**Phase 10 Total: 19-29 entities**

---

### Phase 11: Key Characters

**Goal:** Create world-shaping characters beyond settlement NPCs.

**Templates used:** Protagonist, Divine Servant, Familiar (3 remaining templates)

1. **Protagonists/Heroes** (2-3 entities)
   - Read `Templates/Characters/Protagonist.md`
   - Create legendary figures:
     - Living hero (current age)
     - Historical hero (founder/savior)
     - Rising hero (prophecy candidate)
   - Connect to prophecy, history, organizations

2. **Divine Servants** (2-3 entities)
   - Read `Templates/Characters/Divine Servant.md`
   - Create celestial/infernal agents:
     - Angel of primary deity
     - Messenger of the gods
     - Fallen servant
   - Connect to deities, planes, prophecy

3. **Familiars** (1-2 entities)
   - Read `Templates/Characters/Familiar.md`
   - Create notable bonded creatures:
     - Archmage's companion
     - Sacred beast
   - Connect to characters, magic system

**Save to:** `Worlds/[World Name]/Characters/`

**Phase 11 Total: 5-8 entities**

---

### Phase 12: Final Connections & World Overview

**Goal:** Ensure all connections are bidirectional and complete the World Overview.

1. **Update World Overview.md**
   Fill all sections with links to created entities:

   - **Geography Overview:** Link to continents, major regions
   - **Major Powers table:** Link to governments
   - **Timeline table:** Link to ages and key events
   - **Magic System(s):** Link to magic system entity
   - **The Divine:** Link to pantheon, deities
   - **Planes of Existence:** Link to planes
   - **Major Conflicts:** Link to current tensions
   - **Quick Reference:**
     - Key Locations: Capitals, dungeons, landmarks
     - Key Characters: Rulers, heroes, villains
     - Key Organizations: Major powers
     - Key Concepts: Pantheon, magic, prophecy

2. **Connection Audit**
   Review all created entities and ensure:
   - Every entity has at least 3-5 `[[wikilinks]]` in Connections
   - Parent-child relationships are bidirectional
   - Plot hooks reference other entities
   - No orphaned entities exist
   - Historical entities connect to current ones

   **Validation Checklist:**
   - [ ] Every character links to their home settlement, AND that settlement links back to the character
   - [ ] Every organization links to its headquarters, AND that settlement links back to the organization
   - [ ] Every deity in the pantheon links to the pantheon, AND the pantheon links to all deities
   - [ ] Every settlement links to its parent region, AND the region links to all settlements within it
   - [ ] Every historical event links to its location, AND the location links to the event
   - [ ] Every artifact links to its current owner/location, AND they link back to the artifact
   - [ ] Flag any entity with 0 incoming links as "orphaned" - add at least 2 references to it

   **Bidirectional Link Patterns:**
   | If A links to B as... | B must link to A as... |
   |----------------------|------------------------|
   | Homeland/Location | Notable Person/Resident |
   | Member of Organization | Members/Notable Members |
   | Worships Deity | Followers/Worshippers |
   | Parent Region | Subregions/Settlements |
   | Ruler of Settlement | Current Ruler |
   | Creator of Item | Created Items/Notable Works |
   | Participant in Event | Key Figures |

3. **Cross-Category Links**
   Ensure connections span categories:
   - Characters → Organizations they belong to → back-link to Characters
   - Settlements → Geographic features nearby → back-link to Settlements
   - Items → Characters who own/seek them → back-link to Items
   - History → Locations where events occurred → back-link to History
   - Creatures → Regions where they live → back-link to Creatures
   - Organizations → Settlements where they operate → back-link to Organizations

4. **Connection Density Targets:**
   - **Minimum:** 3 outgoing wikilinks per entity
   - **Target:** 5-8 connections per entity
   - **Incoming:** Every entity should have 2+ other entities linking TO it
   - **Fix orphans:** If an entity has <2 incoming links, add references in related entities

---

### Phase 13: Summary Report

Provide a final summary:

1. **Entity Count by Category:**
   ```
   Category        | Count | Templates Used
   ----------------|-------|---------------
   Geography       | X     | 18/18
   Concepts        | X     | 10/10
   Organizations   | X     | 9/9
   Settlements     | X     | 8/8
   Characters      | X     | 6/9 (9 total, 6 for NPCs)
   History         | X     | 8/9 (9 total, includes Adventure)
   Creatures       | X     | 5/5
   Items           | X     | 11/11
   ----------------|-------|---------------
   TOTAL           | X     | 75 core templates

   (Additional DM tool templates available: Encounters 4, Maps 4)
   ```

2. **World Structure Overview:**
   - Continents and their regions
   - Major powers and their relationships
   - Timeline of ages
   - Divine hierarchy

3. **Connection Density:**
   - Total `[[wikilinks]]` created
   - Average connections per entity
   - Most connected entities

4. **Suggested Next Steps:**
   - Areas to expand further
   - Plot hooks ready to develop
   - Character arcs to explore
   - Dungeons ready to detail

5. **File Location:**
   `Worlds/[World Name]/` - ready for use in Obsidian

---

## Naming Conventions Reference

When generating names for entities, consult these reference files:

| Reference File | Use For |
|----------------|---------|
| `Templates/Reference/D&D Species Naming Conventions.md` | Species-specific naming patterns (Dwarves, Elves, Halflings, Orcs, etc.) |
| `Templates/Reference/Tolkien Naming Conventions.md` | High fantasy linguistic patterns (Sindarin, Quenya, Khuzdul, etc.) |

### When to Apply

- **During entity generation:** Use naming patterns that match the entity's species, culture, or region
- **For settlements:** Name cities/towns using appropriate linguistic conventions for their dominant culture
- **For characters:** Match names to species (Dwarven names for dwarves, Elvish for elves, etc.)
- **For geography:** Use Tolkien patterns for rivers (-duin), mountains (-gor), forests (-taur), etc.

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

## Consistency Guidelines

Throughout all phases, maintain:

1. **Naming Conventions:**
   - Extract cultural naming from region/species
   - Use consistent linguistic patterns for related entities
   - Reference `Templates/Reference/D&D Species Naming Conventions.md` for standard races
   - Reference `Templates/Reference/Tolkien Naming Conventions.md` for elvish/dwarvish names

2. **Religious Consistency:**
   - Temples worship established deities
   - Religious orders serve specific gods
   - Holy days appear on the calendar
   - Divine servants match deity domains

3. **Political Logic:**
   - Settlements reference their governing nation
   - Borders follow geographic features
   - Military serves the government
   - Trade agreements match actual routes

4. **Geographic Coherence:**
   - Rivers flow from mountains to seas/lakes
   - Roads connect actual settlements
   - Climate matches latitude/terrain
   - Creatures live in appropriate habitats

5. **Historical Integration:**
   - Current entities reference historical events
   - Wars explain current rivalries
   - Dynasties connect to governments
   - Artifacts tie to historical figures
   - Tragedies explain current conditions

6. **Economic Consistency:**
   - Currency matches issuing government
   - Trade routes connect trading partners
   - Guilds operate in relevant settlements
   - Shops sell regionally appropriate goods

7. **Magical Consistency:**
   - Academies teach the established magic system
   - Magic items follow world's magical rules
   - Potions use established plants/ingredients
   - Prophecy integrates with divine system

8. **Cross-References:**
   - Always use `[[Entity Name]]` syntax
   - Fill the Connections section of every entity
   - Update older entities when new connections emerge
   - Ensure bidirectional links

---

## Template Reference (All 75)

| Category | Templates (Count) |
|----------|-------------------|
| **Geography** | Continent, Region, Mountain Range, Forest, River, Road, Desert, Tundra, Plains, Hills, Steppes, Ocean, Lake, Coast, Pass, Island, Cave, Dungeon (18) |
| **Concepts** | Religion, Pantheon, Deity, Magic System, Technology, Language, Prophecy, Plane of Existence, Currency, Calendar (10) |
| **Organizations** | Guild, Government, Religious Order, Cult, Military, Criminal Organization, Business, Organization (General), Academy (9) |
| **Settlements** | Village, Town, City, Stronghold, Tavern, Shop, Temple, Library (8) |
| **Characters** | Protagonist, Antagonist, Support Character, Background Character, Divine Servant, Familiar (6) |
| **History** | Event, War, Battle, Treaty, Trade Agreement, Tragedy, Dynasty, Age (8) |
| **Creatures** | Monster, Animal, Insect, Species, Plant (5) |
| **Items** | Weapon, Armor, Wondrous Magic Item, Artifact, Potion, Gear, Food, Drink, Container, Vehicle, Book (11) |

**Total: 75 templates across 8 categories**
