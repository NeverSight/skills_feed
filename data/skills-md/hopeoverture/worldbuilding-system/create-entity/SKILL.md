---
name: create-entity
description: Generate a fully populated worldbuilding entity from a template and save it to a world. Use when the user wants to create a specific entity like "create a dwarven city called Ironhold" or "make a fire deity named Pyraxis".
argument-hint: "[type] called [name] for [world] (e.g., 'dwarven city called Ironhold for Eldermyr')"
---

# Create Entity

Create a new entity: $ARGUMENTS

## Instructions

You are creating a new worldbuilding entity by filling out a template with generated content.

### Step 1: Parse the Request

The user's request should include:
1. **Entity type** - What kind of entity (e.g., "city", "deity", "weapon", "NPC")
2. **Entity name** - The name for this entity
3. **World** (optional) - Which world to place it in (check `Worlds/` for existing worlds)
4. **Additional context** - Any specific details the user wants included

If the world is not specified and multiple worlds exist, ask which world to use.
If no worlds exist, ask if they want to create one first with `/create-world`.

### Step 2: Match to Template

Map the entity type to the appropriate template:

**Characters:**
| User Says | Template |
|-----------|----------|
| protagonist, player character, PC, hero | Protagonist.md |
| antagonist, villain, BBEG, enemy | Antagonist.md |
| NPC, ally, companion, support | Support Character.md |
| commoner, background, minor NPC | Background Character.md |
| angel, avatar, divine servant, celestial agent | Divine Servant.md |
| familiar, companion creature, bonded creature | Familiar.md |

**Settlements:**
| User Says | Template |
|-----------|----------|
| village, hamlet | Village.md |
| town | Town.md |
| city, metropolis | City.md |
| stronghold, fortress, castle, keep | Stronghold.md |
| tavern, inn, pub, alehouse | Tavern.md |
| shop, store, merchant | Shop.md |
| temple, shrine, church, sanctuary | Temple.md |
| library, archive, repository | Library.md |

**Items:**
| User Says | Template |
|-----------|----------|
| weapon, sword, axe, bow | Weapon.md |
| armor, shield | Armor.md |
| magic item, wondrous item | Wondrous Magic Item.md |
| artifact, legendary item, relic | Artifact.md |
| potion, elixir | Potion.md |
| tool, gear, equipment | Gear.md |
| food, meal, dish | Food.md |
| drink, beverage, ale, wine | Drink.md |
| container, bag, chest, box | Container.md |
| vehicle, ship, wagon, airship, cart | Vehicle.md |
| book, tome, grimoire, manual, scripture | Book.md |

**Creatures:**
| User Says | Template |
|-----------|----------|
| monster, creature, enemy creature | Monster.md |
| animal, beast, wildlife | Animal.md |
| insect, bug, swarm | Insect.md |
| species, race, people | Species.md |
| plant, flora, herb, tree, flower | Plant.md |

**Organizations:**
| User Says | Template |
|-----------|----------|
| guild, trade guild | Guild.md |
| government, kingdom, empire, nation | Government.md |
| religious order, church, temple order | Religious Order.md |
| cult, secret cult | Cult.md |
| military, army, navy, legion | Military.md |
| criminal, thieves guild, gang, mafia | Criminal Organization.md |
| business, company, merchant house | Business.md |
| organization, faction, group | Organization (General).md |
| academy, school, college, university | Academy.md |

**Concepts:**
| User Says | Template |
|-----------|----------|
| religion, faith | Religion.md |
| pantheon, gods | Pantheon.md |
| deity, god, goddess | Deity.md |
| magic system, magic, arcane | Magic System.md |
| technology, invention, tech | Technology.md |
| language, tongue, script | Language.md |
| prophecy, prediction, foretelling, vision | Prophecy.md |
| plane, plane of existence, realm, dimension | Plane of Existence.md |
| currency, money, coins, economy | Currency.md |
| calendar, timekeeping, year, months | Calendar.md |

**History:**
| User Says | Template |
|-----------|----------|
| event, historical event | Event.md |
| war, conflict | War.md |
| battle, siege | Battle.md |
| treaty, peace treaty, alliance | Treaty.md |
| trade agreement, trade deal | Trade Agreement.md |
| tragedy, disaster, catastrophe | Tragedy.md |
| dynasty, royal house, lineage, bloodline | Dynasty.md |
| age, era, epoch, period | Age.md |

**Geography:**
| User Says | Template |
|-----------|----------|
| continent | Continent.md |
| region, territory, land | Region.md |
| mountain, mountain range | Mountain Range.md |
| forest, woods, jungle | Forest.md |
| river, stream | River.md |
| road, highway, path, trade route | Road.md |
| desert, wasteland | Desert.md |
| tundra, arctic, frozen land | Tundra.md |
| plains, grassland, prairie | Plains.md |
| hills, highlands | Hills.md |
| steppes, steppe | Steppes.md |
| ocean, sea | Ocean.md |
| lake, pond | Lake.md |
| coast, coastline, shore | Coast.md |
| pass, mountain pass | Pass.md |
| island, isle | Island.md |
| cave, cavern, grotto | Cave.md |
| dungeon, lair, ruins, tomb | Dungeon.md |

**Character Options:**
| User Says | Template |
|-----------|----------|
| background, origin, character background | Character Background.md |
| class, character class, custom class | Character Class.md |
| subclass, archetype, specialization | Character Subclass.md |

**Encounters:**
| User Says | Template |
|-----------|----------|
| combat encounter, fight, battle encounter | Combat Encounter.md |
| social encounter, negotiation, roleplay encounter | Social Encounter.md |
| exploration encounter, puzzle, skill challenge | Exploration Encounter.md |
| trap, hazard, mechanical trap | Trap.md |

**Maps:**
| User Says | Template |
|-----------|----------|
| world map, global map | World Map.md |
| continent map, landmass map | Continent Map.md |
| region map, area map, territory map | Region Map.md |
| settlement map, city map, town map | Settlement Map.md |

**Adventures:**
| User Says | Template |
|-----------|----------|
| adventure, quest, campaign arc, module | Adventure.md |

### Step 3: Read the Template

Read the appropriate template from `Templates/[Category]/[Template].md`

**Category Folder Mappings:**
| Template Category | Save to Folder |
|-------------------|----------------|
| Characters, Character Options | Characters/ |
| Settlements | Settlements/ |
| Items | Items/ |
| Creatures | Creatures/ |
| Organizations | Organizations/ |
| Concepts | Concepts/ |
| History, Adventures | History/ |
| Geography | Geography/ |
| Encounters | Encounters/ |
| Maps | Maps/ |

### Step 4: Generate Content

**Naming Conventions Reference:**
When generating names for entities, consult these reference files:

| Reference File | Use For |
|----------------|---------|
| `Templates/Reference/D&D Species Naming Conventions.md` | Species-specific naming patterns (Dwarves, Elves, Halflings, Orcs, etc.) |
| `Templates/Reference/Tolkien Naming Conventions.md` | High fantasy linguistic patterns (Sindarin, Quenya, Khuzdul, etc.) |

**Matching Names to Context:**
- **Characters:** Match names to species (Dwarven names for dwarves, Elvish for elves, etc.)
- **Settlements:** Use linguistic conventions for the dominant culture
- **Geography:** Use Tolkien patterns for rivers (-duin), mountains (-gor), forests (-taur)
- **Organizations:** Match naming style to the organization's cultural origin

Fill out the template completely with coherent, interconnected content:

1. **YAML Frontmatter**: Fill all fields with appropriate values
   - Set `name:` to the entity name
   - Set `status: draft`
   - Fill category-specific fields

2. **Replace `{{title}}`**: Use the entity name

3. **Fill All Sections**: Generate content for every section following the directive prompts
   - Use specific names, numbers, and details
   - Create internal consistency
   - Reference other entities that could exist in this world using `[[Entity Name]]`
   - Include plot hooks that tie to the broader world

4. **Image Prompts**: Fill in both prompt sections with detailed, specific descriptions based on the generated content

5. **Connections**: Populate with `[[Entity Name]]` links to related entities (these can be entities that don't exist yet but should)

**D&D 5e Stat Block Mode Selection:**
For characters (Protagonist, Antagonist, Support Character), choose ONE mode:

| Mode | When to Use | Fill Field | Leave Blank |
|------|-------------|------------|-------------|
| **Level-based** | PC-style with class features, spell slots | `level:` | `challenge_rating:` |
| **CR-based** | NPC-style, simple combat stats, boss monsters | `challenge_rating:` | `level:` |

**Examples:**
- "Level 10 Wizard villain" → Use `level: 10`, leave `challenge_rating:` blank
- "CR 8 Warlord boss" → Use `challenge_rating: 8`, leave `level:` blank
- "CR 5 Bandit Captain" → Use `challenge_rating: 5`

**D&D 5e Stat Block Validation:**
When generating creatures or characters with stat blocks:
1. Verify CR matches XP (see [[D&D 5e Stat Block Validation]] for tables)
2. Calculate proficiency bonus from level/CR (+2 for levels 1-4, +3 for 5-8, etc.)
3. Verify ability modifiers = (score - 10) / 2 rounded down
4. Verify attack bonus = proficiency + STR/DEX modifier
5. Verify spell save DC = 8 + proficiency + spellcasting ability modifier
6. Verify HP correlates with hit dice and CON modifier
7. For CR 5+ creatures, consider Legendary Resistance and Legendary Actions

### Step 5: Save the Entity

Save the completed entity to:
`Worlds/[World Name]/[Category]/[Entity Name].md`

Use the entity's name as the filename with Title Case and spaces.

### Step 5B: Update Related Entities (Reciprocal Links)

After creating the new entity, check if any entities referenced in its Connections section already exist. If they do, add a reciprocal link back to the new entity.

**Process:**
1. For each `[[Entity Name]]` in the new entity's Connections section
2. Check if that entity file already exists in the world
3. If it exists, read the file and add the new entity to the appropriate Connections category
4. Save the updated file

**Reciprocal Link Patterns:**
See [[Connection Matrix]] for complete bidirectional linking rules.

| New Entity Links To... | Add New Entity To Target's Section |
|-----------------------|-----------------------------------|
| Settlement (as location) | Characters > Residents or Notable NPCs |
| Organization (as member) | Characters > Members |
| Region (as parent geography) | Settlements or Geography > Contains |
| Deity (as patron) | Characters > Worshippers or Followers |
| Character (as ally) | Characters > Allies |
| Character (as enemy) | Characters > Rivals/Enemies |
| Government (as ruler) | Characters > Ruler or Leadership |
| Settlement (as headquarters) | Organizations > Based Here |

**Example:**
- You create "Grom the Blacksmith" who works in "[[Ironforge City]]"
- Check if `Worlds/[World]/Settlements/Ironforge City.md` exists
- If yes, open it and add `[[Grom the Blacksmith]]` to Characters > Notable NPCs
- Save the updated Ironforge City.md

This ensures bidirectional connections and prevents orphaned entities.

### Step 6: Summary

After creating, provide:
1. Confirmation of where the file was saved
2. A brief 2-3 sentence summary of the entity
3. Suggested related entities to create next (from the Connections section)

### Step 7: Offer Image Generation

After presenting the summary, ask the user:

> "Would you like me to generate an image for this entity?"

If yes, use the `/generate-image` skill to:
1. Read the entity file you just created
2. Extract the filled image prompt from the Image Prompts section
3. Generate the image using OpenAI's gpt-image-1.5 model
4. Save the image in the same folder as the entity
5. Update the entity file with the image reference

**Prompt selection for common entity types:**
- **Characters:** Default to "Portrait (Bust)" unless user requests full body
- **Settlements:** Default to "Exterior View"
- **Items:** Default to "Display View"
- **Creatures:** Default to "Natural Habitat"
- **Geography:** Default to "Landscape View"
