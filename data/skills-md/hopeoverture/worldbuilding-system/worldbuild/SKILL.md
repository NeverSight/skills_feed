---
name: worldbuild
description: Interactive guided worldbuilding with questions, choices, and incremental creation. Creates worlds collaboratively through a question-and-answer workflow rather than automatic generation. Use when the user wants to thoughtfully build a world step-by-step.
argument-hint: "[world name] or 'resume'"
---

# Interactive Worldbuilding

Build a world collaboratively: $ARGUMENTS

## Overview

This skill guides users through worldbuilding via an interactive question-and-answer workflow. Unlike `/generate-world` which auto-generates 80-120 entities, this skill collaborates with the user at every step—asking questions, offering choices, and creating entities one at a time with approval.

**Philosophy:**
- Start small, expand gradually
- Establish tone and theme first—everything flows from core identity
- Ask the right questions at the right time
- Skip irrelevant sections based on user choices
- Show previews before creating; user approves each entity
- Use culturally-appropriate naming conventions

**9 Interactive Phases:**
1. World Identity (tone, theme, inspirations, naming culture)
2. Metaphysical Foundation (magic, gods, cosmology, planes)
3. The Land (geography, terrain, ecology, resources, travel)
4. Powers & People (nations, species, social structure, laws, economy)
5. History & Conflict (ages, events, legends, mysteries, cycles)
6. Places of Interest (settlements, dungeons, landmarks, routes)
7. Characters & Relationships (NPCs, relationship webs, factions)
8. Society & Daily Life (culture, customs, festivals, arts, death rites)
9. Campaign & Adventure Setup (starting scenarios, arcs, session zero)

---

## Cultural Naming Conventions Reference

When generating names, match the cultural aesthetic the user has chosen. Read and apply patterns from:
- `Templates/Reference/D&D Species Naming Conventions.md`
- `Templates/Reference/Tolkien Naming Conventions.md`

### Historical Culture Naming Patterns

| Culture | Name Examples | Characteristics |
|---------|---------------|-----------------|
| **Celtic/Gaelic** | Brennan, Caelum, Aisling, Niamh, Cormac | Soft consonants, -an/-in endings, Gaelic sounds (ae, oi, ui) |
| **Anglo-Saxon** | Aelfric, Godwin, Eadmund, Wulfstan, Hild | -ric, -win, -mund, -stan endings; Aelf-, Ead-, Wulf- prefixes |
| **Norse/Viking** | Bjorn, Sigrid, Ragnar, Astrid, Thorvald | Thor-/Sig-/Rag- prefixes; -son/-dottir patronymics; -heim/-gard places |
| **Germanic** | Friedrich, Heinrich, Adelheid, Brunhilde | -rich/-helm/-wald endings; compound meaningful names |
| **Slavic** | Vladislav, Miroslav, Svetlana, Yaroslav | -slav/-mir suffixes; patronymics (-ovich/-ovna) |
| **Byzantine/Greek** | Alexios, Theodora, Konstantinos, Irene | -ios/-os endings; Theo-/Alex-/Konst- prefixes |
| **Arabic/Moorish** | Rashid, Fatima, Khalid, Zahra, Tariq | Al- prefix; -id/-iq endings; meaning-based names |
| **Persian** | Darius, Cyrus, Xerxes, Roxana, Ardashir | -us/-es endings; royal connotations |
| **East Asian** | Kenji, Mei, Hiro, Lian, Takeshi | Family name first; nature/virtue meanings |
| **Mediterranean** | Marco, Isabella, Lorenzo, Lucia, Giovanni | -o/-a endings; saint names common |
| **Turkic/Steppe** | Temujin, Borte, Kublai, Toghrul | Harsh consonants; -khan/-beg titles |
| **West African** | Kofi, Amara, Kwame, Nneka, Jabari | Day-names; virtue meanings; -a/-i endings |
| **Indian** | Arjun, Priya, Vikram, Lakshmi, Rajan | Sanskrit roots; -a/-i endings; deity connections |

### Place Name Patterns by Culture

| Culture | Suffixes/Patterns | Examples |
|---------|-------------------|----------|
| **Celtic** | -dun (fort), -mag (plain), -loch (lake), -glen | Dunderry, Magrath, Lochmere |
| **Anglo-Saxon** | -ton (settlement), -ham (home), -ford, -bury | Ashford, Thornbury, Westham |
| **Norse** | -heim (home), -gard (enclosure), -fjord, -by | Ironheim, Stormgard, Ravenby |
| **Germanic** | -burg (fortress), -wald (forest), -stein | Grauburg, Schwarzwald, Falkenstein |
| **Slavic** | -grad (city), -ov/-ev, -sk | Novgorod, Petrokov, Volsk |
| **Greek** | -polis (city), -thea, -os | Heliópolis, Althea, Demos |
| **Arabic** | Al- (the), -abad (city), Dar- (house) | Al-Qadir, Sultanabad, Dar-al-Hikma |

---

## Instructions

### Getting Started

1. **Parse the argument:**
   - If `$ARGUMENTS` is a world name → start new worldbuilding session
   - If `$ARGUMENTS` is "resume" → check for existing sessions
   - If blank → ask user for world name or if they want to resume

2. **Check for existing session:**
   - Look for `Worlds/[World Name]/.worldbuild-state.json`
   - If found, offer to resume or start fresh

3. **Session state tracking:**
   Store decisions and progress in a state file at `Worlds/[World Name]/.worldbuild-state.json`:
   ```json
   {
     "version": "2.0",
     "world_name": "World Name",
     "current_phase": 1,
     "current_section": "tone",
     "completed_phases": [],
     "decisions": {
       "naming_culture": "norse",
       "tone": "dark_fantasy",
       "inspirations": []
     },
     "entities_created": [],
     "skipped_sections": [],
     "relationship_map": {},
     "faction_goals": {},
     "last_updated": "ISO timestamp"
   }
   ```

4. **Commands available to user:**
   - `continue` - Proceed to next question
   - `back` - Go back one question
   - `skip` - Skip current section
   - `pause` - Save state and exit
   - `summary` - Show progress dashboard
   - `review [entity]` - View a created entity
   - `relationships` - Show NPC relationship web
   - `factions` - Show faction goals and conflicts

---

## Phase 1: World Identity

**Goal:** Establish the core identity that everything else flows from.

### Step 1.1: World Name

Ask the user:
> "What would you like to name your world?"

If they're unsure, offer to suggest 5 names based on their tone preferences (ask tone first if needed).

### Step 1.2: Primary Naming Culture

Ask the user:
> "What real-world culture should inspire the naming conventions for your world? This affects how places, people, and things are named. Choose one primary culture, or select 'Mixed' for regional variety:"
>
> 1. **Celtic/Gaelic** - Soft, melodic names with Gaelic sounds (Brennan, Caelum, Aisling, Cormac)
> 2. **Anglo-Saxon** - Old English compound names (Aelfric, Godwin, Eadmund, Wulfstan)
> 3. **Norse/Viking** - Scandinavian warrior culture (Bjorn, Sigrid, Ragnar, Thorvald)
> 4. **Germanic** - Central European medieval (Friedrich, Heinrich, Adelheid, Brunhilde)
> 5. **Slavic** - Eastern European (Vladislav, Miroslav, Svetlana, Yaroslav)
> 6. **Byzantine/Greek** - Eastern Roman Empire (Alexios, Theodora, Konstantinos, Irene)
> 7. **Arabic/Moorish** - Middle Eastern medieval (Rashid, Fatima, Khalid, Zahra)
> 8. **Persian** - Ancient empire aesthetic (Darius, Cyrus, Roxana, Ardashir)
> 9. **Mediterranean/Italian** - Southern European (Marco, Isabella, Lorenzo, Lucia)
> 10. **East Asian** - Chinese/Japanese inspired (Kenji, Mei, Lian, Takeshi)
> 11. **Turkic/Steppe** - Central Asian nomad (Temujin, Borte, Toghrul, Kublai)
> 12. **West African** - Sub-Saharan kingdoms (Kofi, Amara, Kwame, Nneka)
> 13. **Indian/Sanskrit** - South Asian (Arjun, Priya, Vikram, Lakshmi)
> 14. **Tolkien Elvish** - High fantasy linguistic (Sindarin, Quenya patterns)
> 15. **Tolkien Dwarvish** - Norse-influenced Khuzdul patterns
> 16. **Mixed Regional** - Different cultures for different regions (I'll ask per region)
> 17. **Custom Blend** - Describe the aesthetic you want

Store the answer in `decisions.naming_culture`.

### Step 1.3: Tone & Genre

Ask the user:
> "What tone and genre are you going for? Choose one or describe your own:"
>
> 1. **High/Epic Fantasy** - Heroic adventures, clear good vs evil, grand scale, noble quests (Lord of the Rings, Wheel of Time, Dragonlance)
> 2. **Dark Fantasy** - Grim, morally gray, dangerous magic, consequences matter (Dark Souls, Warhammer, The Witcher, Berserk)
> 3. **Sword & Sorcery** - Personal stakes, adventure-focused, pulpy action, morally flexible heroes (Conan, Fafhrd & Gray Mouser)
> 4. **Mythic Fantasy** - Gods walk among mortals, legendary heroes, fate and prophecy (Greek myths, Exalted, Mythic Greece)
> 5. **Low Fantasy** - Subtle magic, realistic politics, grounded world, human-focused (Game of Thrones early seasons, The First Law)
> 6. **Grimdark** - Bleak, cynical, no true heroes, violence and corruption (Joe Abercrombie, Mark Lawrence)
> 7. **Heroic Fantasy** - Larger-than-life heroes, clear villains, triumph of good (Forgotten Realms, classic D&D)
> 8. **Gothic Fantasy** - Horror elements, dark romance, decaying grandeur, curses (Ravenloft, Castlevania)
> 9. **Fairy Tale Fantasy** - Whimsical, folkloric, talking animals, moral lessons (The Witcher's fairy tales, Stardust)
> 10. **Romantic Fantasy** - Relationships central, political intrigue, emotional stakes (A Court of Thorns and Roses)
> 11. **Dying Earth** - World in twilight, ancient mysteries, melancholy beauty (Jack Vance, Numenera)
> 12. **Weird Fantasy** - Strange, unsettling, cosmic horror undertones (Perdido Street Station, Bas-Lag)
> 13. **Historical Fantasy** - Real history with magic added (Jonathan Strange, Guy Gavriel Kay)
> 14. **Military Fantasy** - Wars, tactics, soldiers, chain of command (Black Company, Malazan)
> 15. **Pirate/Nautical Fantasy** - Sea adventures, island hopping, treasure (Pirates of the Caribbean, Liveship Traders)
> 16. **Political Fantasy** - Intrigue, scheming, houses and factions, power games (Dune, Game of Thrones)
> 17. **Comedic/Satirical** - Humor, parody, absurdity welcome (Discworld, Princess Bride)
> 18. **Wuxia/Martial Fantasy** - Martial arts, honor codes, legendary techniques (Crouching Tiger, Avatar: TLA)
> 19. **Arabian Nights** - Desert kingdoms, djinn, thousand-and-one-nights aesthetic
> 20. **Other** - Describe your vision

Store in `decisions.tone`.

### Step 1.4: Inspirations

Ask:
> "What are 1-5 inspirations for this world? These could be books, games, TV shows, movies, historical periods, art styles, or vibes."
>
> Some prompts to help:
> - Any books or series? (Fantasy novels, historical fiction, mythology)
> - Any games? (Video games, tabletop, board games)
> - Any TV shows or movies?
> - Any historical periods? (Medieval Europe, Ancient Rome, Feudal Japan, etc.)
> - Any art styles or aesthetics? (Gothic, Renaissance, Art Nouveau, etc.)
> - Any music or soundtracks that evoke the feeling?

Store in `decisions.inspirations` as an array.

### Step 1.5: Content Rating

Ask:
> "What content rating works for your world?"
>
> 1. **Family-friendly (PG)** - Suitable for all ages, violence is abstract, no mature themes, death happens off-screen
> 2. **Light Adventure (PG-10)** - Mild peril, some scary moments, but nothing too intense
> 3. **Standard Fantasy (PG-13)** - Typical D&D fare, combat violence, mild dark themes, some horror elements
> 4. **Teen+ (TV-14)** - More intense violence, some disturbing imagery, complex moral situations
> 5. **Mature (R)** - Adult themes welcome, graphic violence possible, darker elements fully explored
> 6. **Very Dark (NC-17)** - No restrictions, extreme content possible, explicit themes
> 7. **Varies by Region** - Some areas are darker than others (I'll ask per region)

Store in `decisions.rating`.

### Step 1.6: Themes to Explore

Ask:
> "What themes do you want this world to explore? Select 2-5:"
>
> 1. **Power and Corruption** - What happens when people gain power
> 2. **Redemption** - Can people change? Can evil be forgiven?
> 3. **Legacy and Heritage** - The weight of the past on the present
> 4. **Freedom vs Security** - What do we sacrifice for safety?
> 5. **Nature vs Civilization** - The tension between wild and tamed
> 6. **Faith and Doubt** - Belief, religion, and questioning
> 7. **War and Peace** - The costs and causes of conflict
> 8. **Identity and Belonging** - Who am I? Where do I fit?
> 9. **Love and Loss** - Relationships, grief, connection
> 10. **Duty vs Desire** - Obligation versus personal wants
> 11. **Knowledge and Ignorance** - The dangers and blessings of knowing
> 12. **Mortality and Immortality** - What does it mean to die? To live forever?
> 13. **Justice and Vengeance** - Is revenge ever justified?
> 14. **Colonialism and Empire** - Conquest, resistance, cultural erasure
> 15. **Class and Inequality** - The divide between rich and poor
> 16. **Environmentalism** - The world is dying/healing/changing
> 17. **Technology and Progress** - Is change good? What do we lose?
> 18. **Monsters and Humanity** - Who are the real monsters?
> 19. **Prophecy and Free Will** - Is the future fixed?
> 20. **Other** - Describe your themes

Store in `decisions.themes` as array.

### Step 1.7: Sensitive Topics

Ask:
> "Are there any topics you'd like to avoid or handle carefully in this world? This helps me create appropriate content."
>
> Common topics to consider:
> - Slavery and human trafficking
> - Sexual violence
> - Child endangerment
> - Real-world religions
> - Mental illness
> - Suicide
> - Torture
> - Genocide
> - Addiction
> - Domestic abuse
> - Body horror
> - Animal cruelty
>
> You can say "none" if you have no restrictions, or list specific topics.

Store in `decisions.avoid_topics` if provided.

### Step 1.8: The Hook

Ask:
> "In one sentence, what makes this world unique or interesting? What's the first thing you want players to discover?"
>
> Examples:
> - "Magic is dying, and the last mages are hunted as heretics"
> - "Three empires vie for control of the only river in a vast desert"
> - "The gods went silent fifty years ago, and cults have risen in the void"
> - "An ancient prison-realm is failing, and forgotten horrors are escaping"
> - "The sun is dying, and each generation is colder than the last"
> - "The dead don't stay dead—everyone returns as spirits, for good or ill"
> - "Dragons rule openly, and humans are their servants and cattle"
> - "A great war ended a century ago, and the veterans are all cursed"
> - "The world is a giant corpse of a dead god, and we live on its bones"
> - "Two moons govern fate—when they align, reality breaks"

Store in `decisions.hook`.

### Step 1.9: Central Conflict

Ask:
> "What's the main problem, tension, or struggle in this world right now? Select one or describe your own:"
>
> **Political Conflicts:**
> 1. **Succession Crisis** - A ruler died without clear heir; factions war for the throne
> 2. **Civil War** - A kingdom is tearing itself apart from within
> 3. **Imperial Expansion** - An empire is conquering neighbors
> 4. **Independence Movement** - Provinces seek freedom from overlords
> 5. **Cold War** - Two powers in tense standoff, proxy conflicts everywhere
>
> **Supernatural Threats:**
> 6. **Ancient Evil Awakening** - Something sealed long ago is breaking free
> 7. **Divine Abandonment** - The gods have gone silent or died
> 8. **Planar Invasion** - Forces from another realm are breaking through
> 9. **Magical Catastrophe** - A spell went wrong; reality is unstable
> 10. **Undead Uprising** - The dead are rising in unprecedented numbers
>
> **Natural/Environmental:**
> 11. **Plague/Pestilence** - A disease is spreading with no cure
> 12. **Famine** - Crops are failing; people are starving
> 13. **Climate Shift** - The world is getting hotter/colder/stranger
> 14. **Resource Depletion** - Something vital is running out
> 15. **Monster Migration** - Creatures are fleeing something worse
>
> **Social/Economic:**
> 16. **Class Revolution** - The poor are rising against the rich
> 17. **Religious Schism** - The church has split; holy war looms
> 18. **Trade War** - Economic warfare threatening to become real war
> 19. **Criminal Ascendance** - Organized crime is taking over
> 20. **Other** - Describe your conflict

Store in `decisions.central_conflict`.

### Step 1.10: Conflict Complexity

Follow up based on their choice:
> "Let's add depth to this conflict. Answer briefly:"
>
> 1. **Who started it?** (Or what triggered it?)
> 2. **Who are the major factions?** (At least 2-3 sides)
> 3. **What does each side want?** (Their stated goals)
> 4. **What do they secretly want?** (Hidden agendas)
> 5. **Who's right?** (Is there a "good" side, or is it complicated?)
> 6. **What happens if nothing changes?** (The ticking clock)

Store in `decisions.conflict_details`.

### Step 1.11: Intended Feeling

Ask:
> "What do you want players to feel when exploring this world? Select 3-5:"
>
> 1. **Wonder and Discovery** - Awe at the unknown, excitement to explore
> 2. **Dread and Tension** - Unease, fear of what lurks
> 3. **Political Intrigue** - Suspicion, scheming, "who can I trust?"
> 4. **Heroic Triumph** - Satisfaction of overcoming great odds
> 5. **Mystery and Secrets** - Curiosity, the thrill of uncovering truth
> 6. **Melancholy and Loss** - Bittersweet beauty, mourning what's gone
> 7. **Adventure and Excitement** - Pulpy fun, action, momentum
> 8. **Horror and Revulsion** - Fear, disgust, the uncanny
> 9. **Humor and Levity** - Laughter, absurdity, not taking things too seriously
> 10. **Righteous Anger** - Injustice that demands action
> 11. **Moral Complexity** - Difficult choices, no easy answers
> 12. **Camaraderie** - Friendship, found family, loyalty
> 13. **Romance and Passion** - Love, desire, emotional intensity
> 14. **Paranoia** - Everyone might be an enemy
> 15. **Hope** - Things can get better, light in darkness
> 16. **Despair** - Things are bleak, survival is the goal
> 17. **Reverence** - Sacred spaces, ancient wisdom, respect for tradition
> 18. **Rebellion** - Defiance, fighting the system
> 19. **Nostalgia** - Longing for a golden age past
> 20. **Other** - Describe the feeling

Store in `decisions.intended_feelings`.

### Step 1.12: World Age & State

Ask:
> "How old is civilization in this world, and what state is it in?"
>
> **Age:**
> 1. **Dawn of Civilization** - First cities, first writing, everything is new
> 2. **Ancient Era** - Old kingdoms, established traditions, but much is still wild
> 3. **Classical Period** - Great empires, philosophy, arts flourishing
> 4. **Dark Age** - Civilization has collapsed, rebuilding from ruins
> 5. **Medieval Peak** - Feudal kingdoms, established religions, stable (relatively)
> 6. **Late Medieval** - Change is coming, old orders crumbling
> 7. **Renaissance** - Rediscovery, innovation, questioning old ways
> 8. **Decline and Fall** - Great powers are dying, end of an era
> 9. **Post-Apocalyptic** - Something destroyed the old world
> 10. **Cyclic** - Civilizations rise and fall; this is another cycle
>
> **State:**
> 11. **Golden Age** - Peace, prosperity, art and culture flourishing
> 12. **Tension** - Things seem fine but storm clouds gather
> 13. **Open Conflict** - Wars are ongoing, borders shifting
> 14. **Recovery** - Healing from recent disaster or war
> 15. **Stagnation** - Nothing changes, old powers cling to control
> 16. **Transformation** - Rapid change, old orders falling
> 17. **Fragmentation** - No central power, many small realms
> 18. **Expansion** - Frontiers being pushed, new lands discovered
> 19. **Isolation** - Realms have withdrawn, contact rare
> 20. **Other** - Describe

Store in `decisions.world_age` and `decisions.world_state`.

### Step 1.13: Create World Overview

Based on all answers, create the World Overview document:

1. **Create directory structure:**
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

2. **Generate World Overview.md** with YAML frontmatter and filled sections:
   - Use tone and inspirations to guide writing style
   - Apply naming conventions from chosen culture
   - Fill Premise with the hook expanded to 2-3 sentences
   - Fill Tone & Themes from decisions
   - Fill Central Conflict with the detailed conflict
   - Leave placeholders for sections to be filled in later phases

3. **Show preview to user:**
   > "Here's your World Overview. Does this capture your vision? I can adjust anything before we save it."

4. **Save upon approval** to `Worlds/[World Name]/World Overview.md`

5. **Update state file** with Phase 1 complete.

### Step 1.14: Phase 1 Summary

Display progress dashboard:
```
╔══════════════════════════════════════════════════════════════╗
║           WORLDBUILDING PROGRESS: [World Name]               ║
╠══════════════════════════════════════════════════════════════╣
║ Phase 1: World Identity        [COMPLETE]                    ║
║ Phase 2: Metaphysical          [NOT STARTED]                 ║
║ Phase 3: The Land              [NOT STARTED]                 ║
║ Phase 4: Powers & People       [NOT STARTED]                 ║
║ Phase 5: History & Conflict    [NOT STARTED]                 ║
║ Phase 6: Places of Interest    [NOT STARTED]                 ║
║ Phase 7: Characters            [NOT STARTED]                 ║
║ Phase 8: Society & Daily Life  [NOT STARTED]                 ║
║ Phase 9: Campaign Setup        [NOT STARTED]                 ║
╠══════════════════════════════════════════════════════════════╣
║ Entities Created: 1                                          ║
║ - World Overview                                             ║
╠══════════════════════════════════════════════════════════════╣
║ Key Decisions:                                               ║
║ - Naming Culture: [culture]                                  ║
║ - Tone: [tone]                                               ║
║ - Rating: [rating]                                           ║
║ - Hook: "[hook]"                                             ║
║ - Central Conflict: [conflict]                               ║
╠══════════════════════════════════════════════════════════════╣
║ Commands: continue | back | skip | pause | summary           ║
╚══════════════════════════════════════════════════════════════╝

Ready to continue to Phase 2: Metaphysical Foundation?
```

---

## Phase 2: Metaphysical Foundation

**Goal:** Establish magic, divinity, cosmology, and the "rules" of reality.

### Section 2A: Magic

**Adaptive Skip:** If user indicated "no magic" or "low fantasy" in Phase 1, ask:
> "Your tone suggests a low-magic or no-magic world. Do you want to skip the magic section, or would you like to define what little magic exists?"

If skipping, add "magic" to `skipped_sections` and proceed to Section 2B.

#### Step 2A.1: Magic Prevalence

Ask:
> "How common is magic in this world?"
>
> 1. **Nonexistent** - Magic is myth; it doesn't actually exist (skip remaining magic questions)
> 2. **Legendary Only** - Magic existed in the past but is gone now; only artifacts remain
> 3. **Extremely Rare** - One in 100,000 might have a spark; most never see real magic in their lifetime
> 4. **Very Rare** - One in 10,000; magic users are legendary figures, often feared
> 5. **Rare** - One in 1,000; magic exists but most villages have never seen a spell cast
> 6. **Uncommon** - One in 100; every town has heard of a hedge wizard or wise woman
> 7. **Notable** - One in 50; magic users are known figures, some in positions of power
> 8. **Common** - One in 20; magical services are available in cities, magic is part of commerce
> 9. **Widespread** - One in 10; magic touches most aspects of daily life
> 10. **Pervasive** - Nearly everyone has some magical ability; the world runs on magic
> 11. **Universal** - Everyone can use magic to some degree; it's as natural as speech
> 12. **Oversaturated** - Magic is everywhere, wild, and often out of control

Store in `decisions.magic_level`. If "Nonexistent", skip to Section 2B.

#### Step 2A.2: Magic Source

Ask:
> "Where does magical power come from? Select all that apply:"
>
> **External Sources:**
> 1. **Divine Grant** - Power flows from gods to their faithful; requires devotion
> 2. **Demonic Pact** - Power bargained from dark entities; always has a price
> 3. **Fey Bargains** - Power from the otherworld; unpredictable and whimsical
> 4. **Elemental Forces** - Raw power from fire, water, earth, air, etc.
> 5. **Ley Lines** - Currents of power flowing through the earth
> 6. **Planar Bleed** - Energy seeping from other dimensions
> 7. **Celestial Alignment** - Power from stars, moons, and cosmic events
> 8. **Ancestral Spirits** - Power from the honored dead
>
> **Internal Sources:**
> 9. **Bloodlines** - Inherited magical potential; sorcerous ancestry
> 10. **Life Force** - Magic drawn from one's own vitality
> 11. **Emotional Energy** - Strong feelings manifest as power
> 12. **Willpower** - Pure mental discipline shapes reality
> 13. **Soul Resonance** - The soul itself generates magical potential
>
> **Learned/Acquired:**
> 14. **Academic Study** - Magic as a science; learned through rigorous education
> 15. **Material Components** - Power extracted from magical substances
> 16. **True Names** - Knowing the secret names of things grants power over them
> 17. **Runic/Symbolic** - Power encoded in symbols, words, and patterns
> 18. **Musical/Bardic** - Magic woven through song, poetry, and performance
> 19. **Alchemical** - Magic through transformation of substances
> 20. **Other** - Describe your magic source

Store in `decisions.magic_source` as array.

#### Step 2A.3: Who Can Use Magic

Ask:
> "Who can use magic in this world?"
>
> 1. **Anyone** - Magic is a skill anyone can learn with enough dedication
> 2. **Anyone with Training** - Requires formal education, but no innate requirement
> 3. **Those with Talent** - Must be born with potential, then train to develop it
> 4. **Specific Bloodlines** - Only certain families carry magical ability
> 5. **Chosen by Power** - Gods, spirits, or fate select who receives magic
> 6. **Specific Species** - Only certain races have magical ability
> 7. **Initiated** - Must undergo a ritual, transformation, or awakening
> 8. **Touched by Events** - Exposure to magical phenomena grants ability
> 9. **Purchased/Bargained** - Magic can be bought, traded, or stolen
> 10. **Varies by Type** - Different magics have different requirements
> 11. **Cursed/Afflicted** - Magic comes with a price, condition, or transformation
> 12. **Randomly Manifests** - No pattern; magic appears unpredictably
> 13. **Gender-Specific** - Only certain genders can access certain magic
> 14. **Age-Dependent** - Only manifests at certain life stages
> 15. **Condition-Based** - Requires specific state (virgin, mad, dying, etc.)

Store in `decisions.magic_users`.

#### Step 2A.4: Magic Learning & Training

Ask:
> "How do people learn to use magic?"
>
> 1. **Formal Academies** - Universities of magic with structured curricula
> 2. **Master-Apprentice** - Traditional one-on-one mentorship
> 3. **Temple Training** - Religious institutions teach divine magic
> 4. **Self-Taught** - Trial and error, ancient texts, experimentation
> 5. **Guild System** - Trade guild structure with journeymen and masters
> 6. **Oral Traditions** - Knowledge passed through stories and songs
> 7. **Dream Instruction** - Spirits or gods teach through visions
> 8. **Instinctive** - Magic users just know; it comes naturally
> 9. **Military Training** - Magic taught as weapon of war
> 10. **Secret Societies** - Hidden orders preserve and teach magic
> 11. **Inherited Memory** - Ancestors' knowledge passes with the blood
> 12. **Forbidden Libraries** - Self-study from dangerous texts
> 13. **Direct Communion** - Learn by connecting with magical sources
> 14. **Competitive Schools** - Rival traditions compete for students
> 15. **No Training Exists** - Magic cannot be taught, only discovered

Store in `decisions.magic_training`.

#### Step 2A.5: Costs and Risks

Ask:
> "What are the costs or risks of using magic? Select all that apply:"
>
> **Physical Costs:**
> 1. **Physical Exhaustion** - Magic drains stamina; overuse causes collapse
> 2. **Aging** - Each spell costs days, months, or years of life
> 3. **Pain** - Casting hurts; power comes through suffering
> 4. **Blood** - Requires literal blood sacrifice (self or others)
> 5. **Mutation** - Prolonged use causes physical changes
> 6. **Disease/Decay** - Magic rots the body over time
>
> **Mental Costs:**
> 7. **Mental Strain** - Magic taxes the mind; overuse causes madness
> 8. **Memory Loss** - Spells consume memories to power themselves
> 9. **Personality Shift** - Magic use changes who you are
> 10. **Addiction** - Magic use is psychologically addictive
> 11. **Nightmares** - Magic users suffer terrible dreams
> 12. **Emotional Blunting** - Extended use numbs feelings
>
> **External Risks:**
> 13. **Attracts Attention** - Using magic draws predators, demons, or authorities
> 14. **Environmental Damage** - Magic warps the land, causes dead zones
> 15. **Wild Magic** - Failure causes unpredictable effects
> 16. **Spiritual Debt** - Entities expect payment for borrowed power
> 17. **Paradox/Reality Backlash** - Reality resists and punishes mages
> 18. **Social Persecution** - Magic users are hunted, feared, controlled
>
> **Material Costs:**
> 19. **Expensive Components** - Requires rare, costly ingredients
> 20. **Sacrifice Required** - Living beings must be sacrificed
> 21. **Minimal Risks** - Magic is relatively safe when used properly

Store in `decisions.magic_costs` as array.

#### Step 2A.6: Society's View of Magic

Ask:
> "How does society view magic and its users?"
>
> 1. **Worshipped** - Mages are living gods, revered and obeyed
> 2. **Venerated** - Mages are honored sages, sought for wisdom
> 3. **Respected** - Magic users hold high status, like nobles or priests
> 4. **Valued** - Mages are useful professionals, like doctors or lawyers
> 5. **Accepted** - Magic is normal, neither special nor feared
> 6. **Tolerated** - Magic is allowed but viewed with mild suspicion
> 7. **Regulated** - Magic is legal but strictly controlled by authorities
> 8. **Distrusted** - Common people fear and avoid magic users
> 9. **Hated** - Magic users are despised, blamed for problems
> 10. **Persecuted** - Magic is illegal; users are arrested or killed
> 11. **Hunted** - Organized efforts exist to find and destroy mages
> 12. **Enslaved** - Magic users are forced to serve the state
> 13. **Hidden** - Magic exists but is kept secret from common folk
> 14. **Varies by Type** - Different magic has different status
> 15. **Varies by Region** - Different areas treat mages differently

Store in `decisions.magic_society_view`.

#### Step 2A.7: Forbidden Magic

Ask:
> "Are there forbidden or taboo forms of magic? Select all that exist:"
>
> **Death Magic:**
> 1. **Necromancy** - Animating or communicating with the dead
> 2. **Soul Magic** - Trapping, destroying, or manipulating souls
> 3. **Life Drain** - Stealing life force from the living
>
> **Mind Magic:**
> 4. **Mind Control** - Dominating another's will
> 5. **Memory Manipulation** - Erasing or altering memories
> 6. **Mind Reading** - Invading another's thoughts without consent
>
> **Blood Magic:**
> 7. **Blood Sacrifice** - Power through ritual killing
> 8. **Bloodline Curses** - Afflicting entire family lines
> 9. **Blood Binding** - Enslaving through blood rituals
>
> **Reality Magic:**
> 10. **Time Magic** - Manipulating the flow of time
> 11. **Dimensional Magic** - Opening portals to other realms
> 12. **Creation Magic** - Making life from nothing
>
> **Summoning:**
> 13. **Demon Summoning** - Calling entities from lower planes
> 14. **Binding** - Enslaving summoned creatures
> 15. **Possession Invitation** - Allowing entities to inhabit bodies
>
> **Other:**
> 16. **Prophecy/Divination** - Seeing the future (considered dangerous)
> 17. **Weather Control** - Manipulating climate (affects everyone)
> 18. **Transformation** - Changing one's form permanently
> 19. **None Forbidden** - All magic is acceptable if used responsibly
> 20. **All Magic Forbidden** - Magic itself is the crime

Store in `decisions.forbidden_magic` as array.

#### Step 2A.8: Magic Limitations

Ask:
> "What can magic NOT do in this world? Select all that apply:"
>
> 1. **True Resurrection** - Once truly dead, no magic can bring you back
> 2. **Immortality** - Magic cannot grant eternal life
> 3. **Time Travel** - The past cannot be changed
> 4. **Create Permanent Life** - Golems fade, constructs fail, true creation is impossible
> 5. **Perfect Mind Reading** - Thoughts can always be hidden or protected
> 6. **Perfect Prediction** - The future is never certain
> 7. **Free Teleportation** - Long-distance travel requires time, resources, or risk
> 8. **Override Free Will** - Domination always fades; the will cannot be truly broken
> 9. **Destroy Souls** - Souls persist regardless of magic
> 10. **Affect the Gods** - Divine beings are beyond mortal magic
> 11. **Affect True Names** - Once known, a true name cannot be changed
> 12. **Create Gold/Wealth** - Transmutation has limits
> 13. **Heal Everything** - Some wounds, curses, or conditions resist magic
> 14. **Work Without Components** - Magic always requires something
> 15. **Work Silently** - Magic requires words, gestures, or visible effects
> 16. **Cross Running Water** - Certain boundaries block magic
> 17. **Affect Iron/Silver** - Certain materials resist or block magic
> 18. **Work in Daylight/Darkness** - Time of day affects magic
> 19. **Affect Believers** - Strong faith provides protection
> 20. **Other Limitations** - Describe your limits

Store in `decisions.magic_limitations` as array.

#### Step 2A.9: Schools/Traditions

Ask:
> "What schools or traditions of magic exist? Select all that apply:"
>
> **Elemental:**
> 1. **Pyromancy** - Fire magic
> 2. **Hydromancy** - Water magic
> 3. **Aeromancy** - Air/wind magic
> 4. **Geomancy** - Earth magic
> 5. **Cryomancy** - Ice/cold magic
> 6. **Electromancy** - Lightning/storm magic
>
> **Life:**
> 7. **Healing/Restoration** - Mending wounds and curing illness
> 8. **Druidism/Nature Magic** - Communion with plants and animals
> 9. **Necromancy** - Death and undeath (if allowed)
> 10. **Biomancy** - Shaping and altering living flesh
>
> **Mind:**
> 11. **Enchantment** - Affecting emotions and thoughts
> 12. **Illusion** - Creating false sensory experiences
> 13. **Divination** - Seeing truth, past, future, and hidden things
> 14. **Telepathy** - Mental communication and sensing
>
> **Matter:**
> 15. **Transmutation** - Changing one thing into another
> 16. **Alchemy** - Magical chemistry and potion-making
> 17. **Enchanting/Artifice** - Imbuing objects with magic
> 18. **Conjuration** - Creating objects from nothing
>
> **Space/Time:**
> 19. **Teleportation** - Moving through space instantly
> 20. **Chronomancy** - Time manipulation (if allowed)
> 21. **Portal Magic** - Creating doorways between places
>
> **Spirit:**
> 22. **Summoning** - Calling creatures from elsewhere
> 23. **Binding** - Trapping spirits in objects or places
> 24. **Warding** - Protective barriers and abjurations
> 25. **Other** - Describe your traditions

Store in `decisions.magic_schools` as array.

#### Step 2A.10: Create Magic System Entity

Based on answers, generate a Magic System entity:

1. Read template: `Templates/Concepts/Magic System.md`
2. Fill all sections using decisions
3. Apply world's naming conventions to any named traditions
4. Show preview to user:
   > "Here's the Magic System for [World Name]. Does this capture how magic works? I can adjust anything before saving."
5. Upon approval, save to `Worlds/[World Name]/Concepts/Magic of [World Name].md`
6. Add to `entities_created` in state
7. Update World Overview with link to magic system

---

### Section 2B: The Divine

#### Step 2B.1: Do Gods Exist

Ask:
> "Do gods exist in this world?"
>
> 1. **Definitely Real** - Gods are provably real; they answer prayers, grant power, and sometimes appear
> 2. **Almost Certainly Real** - Divine magic works, miracles happen, but direct proof is rare
> 3. **Probably Real** - Something grants divine power, but its nature is debated
> 4. **Ambiguously Real** - Faith has power, but is it gods or belief itself?
> 5. **Philosophically Unclear** - Different cultures have different answers; none is proven
> 6. **Once Real, Now Gone** - Gods existed but died, left, or went silent
> 7. **Once Real, Now Sleeping** - Gods slumber and may wake
> 8. **Once Real, Now Trapped** - Gods are imprisoned somewhere
> 9. **False Gods** - Beings claim to be gods but are something else (demons, spirits, etc.)
> 10. **No Gods** - Gods don't exist; "divine" magic is something else entirely
> 11. **Unknown** - The truth about gods is a central mystery
> 12. **Varies by Deity** - Some gods are real, others are myths

Store in `decisions.gods_exist`.

If "No Gods", ask if they want to skip divine sections and proceed to Section 2C.

#### Step 2B.2: Divine Interaction

Ask:
> "How do gods interact with mortals?"
>
> 1. **Walking Among Us** - Gods regularly take mortal form and walk the world
> 2. **Frequent Manifestation** - Gods appear in visions, dreams, and sometimes physical form
> 3. **Active Through Champions** - Gods choose mortal agents and grant them great power
> 4. **Regular Miracles** - Gods answer prayers with obvious supernatural intervention
> 5. **Subtle Signs** - Gods communicate through omens, coincidences, and feelings
> 6. **Only Through Priests** - Gods speak only to their chosen clergy
> 7. **Only in Sacred Places** - Divine presence is limited to temples and holy sites
> 8. **Only in Sacred Times** - Gods are accessible only during festivals or rituals
> 9. **Distant Observers** - Gods watch but rarely intervene
> 10. **Cosmic Clockmakers** - Gods set things in motion but don't interfere
> 11. **Absent/Unreachable** - Gods exist but don't answer; faith is blind
> 12. **Currently Silent** - Gods used to respond but have stopped
> 13. **Bound by Rules** - Gods can only act in specific, limited ways
> 14. **Actively Meddlesome** - Gods constantly interfere, often causing problems
> 15. **Varies by Deity** - Different gods have different levels of involvement

Store in `decisions.divine_interaction`.

#### Step 2B.3: Divine Structure

Ask:
> "How are the gods organized?"
>
> 1. **Single Creator Deity** - One supreme god created everything; may have servants
> 2. **Divine Couple** - Two gods (often male/female) created and rule together
> 3. **Divine Trinity** - Three gods form a unified divine presence
> 4. **Dualistic Opposition** - Two opposing cosmic forces (good/evil, order/chaos)
> 5. **Small Pantheon (3-5)** - A tight circle of major deities with clear roles
> 6. **Medium Pantheon (6-10)** - A divine court with varied domains
> 7. **Large Pantheon (11-20)** - Many gods with overlapping and competing interests
> 8. **Vast Pantheon (20+)** - Countless gods, major and minor
> 9. **Divine Hierarchy** - One supreme god rules over lesser deities
> 10. **Divine Council** - Gods govern collectively, debating and voting
> 11. **Divine Families** - Gods organized into family structures (like Greek/Norse)
> 12. **Divine Factions** - Gods divided into competing groups
> 13. **Animistic Spirits** - Countless spirits in everything; no "major" gods
> 14. **Ancestor Worship** - The dead become divine; living worship ancestors
> 15. **Regional Pantheons** - Different cultures worship entirely different gods
> 16. **All Aspects of One** - Many gods are actually faces of a single deity
> 17. **No Organization** - Gods are independent, with no structure
> 18. **Unknown Structure** - Mortals don't understand how gods relate

Store in `decisions.divine_structure`.

#### Step 2B.4: Important Domains

If pantheon exists, ask:
> "What aspects of life do the gods represent? Select 8-12 domains that matter most:"
>
> **Life & Death:**
> 1. **Life, Birth, and Fertility**
> 2. **Death and the Afterlife**
> 3. **Healing and Medicine**
> 4. **Disease and Plague**
>
> **Nature:**
> 5. **Sun, Light, and Day**
> 6. **Moon, Night, and Dreams**
> 7. **Stars and Fate**
> 8. **Storms, Sky, and Weather**
> 9. **Sea, Rivers, and Water**
> 10. **Earth, Mountains, and Stone**
> 11. **Nature, Animals, and the Wild**
> 12. **Harvest, Agriculture, and Plenty**
> 13. **Seasons and Cycles**
>
> **Civilization:**
> 14. **War, Battle, and Valor**
> 15. **Peace, Diplomacy, and Civilization**
> 16. **Justice, Law, and Order**
> 17. **Forge, Craft, and Creation**
> 18. **Commerce, Wealth, and Trade**
> 19. **Home, Hearth, and Family**
> 20. **Travel, Roads, and Journeys**
>
> **Mind & Spirit:**
> 21. **Knowledge, Wisdom, and Learning**
> 22. **Magic and Secrets**
> 23. **Art, Beauty, and Inspiration**
> 24. **Love, Passion, and Desire**
> 25. **Trickery, Luck, and Thieves**
> 26. **Prophecy and Visions**
>
> **Abstract:**
> 27. **Time and Memory**
> 28. **Chaos and Change**
> 29. **Order and Stability**
> 30. **Vengeance and Retribution**

Store in `decisions.divine_domains` as array.

#### Step 2B.5: Divine Morality

Ask:
> "Do gods have clear moral alignments?"
>
> 1. **Absolute Good vs Evil** - Clear sides; some gods are good, some evil
> 2. **Order vs Chaos** - The divine divide is about control, not morality
> 3. **Life vs Death** - The fundamental divide is existence vs ending
> 4. **Mostly Good** - Most gods are benevolent; evil gods are rare aberrations
> 5. **Mostly Neutral** - Gods represent forces; morality doesn't apply to them
> 6. **Complex/Human** - Gods have virtues and flaws, like people
> 7. **Inscrutable** - Divine morality is beyond human understanding
> 8. **Contextual** - What's good for one god may be evil to another
> 9. **Hypocritical** - Gods claim morality but don't always follow it
> 10. **Indifferent** - Gods don't care about mortal concepts of good and evil
> 11. **Actively Cruel** - Gods are mostly malevolent or uncaring
> 12. **Domain-Dependent** - A god of war is violent; a god of love is kind

Store in `decisions.divine_morality`.

#### Step 2B.6: Divine Conflicts

Ask:
> "Are there conflicts among the gods?"
>
> 1. **Perfect Harmony** - Gods cooperate seamlessly
> 2. **Peaceful Coexistence** - Gods stay in their lanes; minimal interaction
> 3. **Friendly Rivalry** - Competition exists but is good-natured
> 4. **Political Factions** - Gods form alliances and oppose other factions
> 5. **Open Rivalry** - Gods actively compete for followers and power
> 6. **Cold War** - Divine factions are hostile but not openly fighting
> 7. **Active Divine War** - Gods are at war; it affects the mortal world
> 8. **Ancient War Ended** - A divine war happened long ago; scars remain
> 9. **Recurring Conflict** - Divine wars happen cyclically
> 10. **One Defeated Side** - A group of gods lost and were imprisoned/diminished
> 11. **Usurper Situation** - Current gods overthrew previous ones
> 12. **Constant Betrayal** - Gods routinely scheme against each other

Store in `decisions.divine_conflicts`.

#### Step 2B.7: Apotheosis

Ask:
> "Can mortals become gods?"
>
> 1. **Impossible** - The divine is unreachable; mortals can never ascend
> 2. **One Legend** - It happened once in myth; none since
> 3. **Ancient Occurrence** - It happened in the past; no one knows how anymore
> 4. **Theoretically Possible** - Sages believe a path exists but it's lost
> 5. **Rare but Known** - A handful of mortals have achieved godhood
> 6. **Difficult Path** - There's a known but incredibly difficult road to divinity
> 7. **Multiple Paths** - Several methods exist to become a god
> 8. **All Gods Were Mortal** - Every god was once a mortal who ascended
> 9. **Demigod Status** - Mortals can become lesser divine beings
> 10. **Temporary Divinity** - Mortals can briefly touch godhood
> 11. **False Apotheosis** - Some claim godhood but aren't truly divine
> 12. **Actively Prevented** - Gods stop mortals from ascending

Store in `decisions.apotheosis`.

#### Step 2B.8: The Afterlife

Ask:
> "What happens when mortals die?"
>
> 1. **Single Destination** - All souls go to the same place
> 2. **Deity-Claimed** - Each god takes their faithful to their own realm
> 3. **Moral Judgment** - Souls are judged and sorted by their deeds
> 4. **Reincarnation** - Souls are reborn in new bodies
> 5. **Ancestor Realm** - The dead join their ancestors
> 6. **Shadow Existence** - Souls become pale echoes, gradually fading
> 7. **Merger with Divine** - Souls join the cosmic essence of their god
> 8. **Eternal Service** - Souls serve their god in the afterlife
> 9. **Reward or Punishment** - Heaven/hell based on life choices
> 10. **Nothing** - Death is the end; no afterlife exists
> 11. **Unknown** - What happens after death is a mystery
> 12. **Complex System** - Multiple outcomes based on many factors
> 13. **Soul Economy** - Souls are a resource; something collects or uses them
> 14. **Unlife** - The dead return as spirits, ghosts, or undead naturally
> 15. **Varies by Culture** - Different peoples have genuinely different afterlives

Store in `decisions.afterlife`.

#### Step 2B.9: Deities to Create

Ask:
> "Based on your domains and structure, I'll create deities. Do you have any specific gods in mind, or should I generate them?"
>
> If you have ideas, for each deity provide:
> 1. **Name** (or I'll generate one using [naming_culture] conventions)
> 2. **Primary Domain** (from the list you selected)
> 3. **Secondary Domain** (optional)
> 4. **Personality in 3 words**
> 5. **One interesting quirk or trait**
>
> Otherwise, I'll create appropriate deities based on your selections.

Store in `decisions.planned_deities` if provided.

#### Step 2B.10: Create Pantheon Entity

If applicable:
1. Read template: `Templates/Concepts/Pantheon.md`
2. Generate pantheon using decisions and naming conventions
3. Show preview, get approval
4. Save to `Worlds/[World Name]/Concepts/The [Pantheon Name].md`
5. Update state

#### Step 2B.11: Create Deity Entities

For each deity (planned or generated):

1. Read template: `Templates/Concepts/Deity.md`
2. Generate deity details using world tone and decisions
3. Apply naming conventions from chosen culture
4. Show preview:
   > "Here's [Deity Name], god/goddess of [domains]. Does this work?"
5. Upon approval, save to `Worlds/[World Name]/Concepts/[Deity Name].md`
6. After each deity, ask: "Ready for the next deity, or would you like to adjust this one?"
7. Continue until all planned deities are created

---

### Section 2C: Cosmology

#### Step 2C.1: Planes Matter?

Ask:
> "Do other planes of existence matter for your world?"
>
> 1. **Not Really** - The material world is all that matters; skip this section
> 2. **Background Lore** - Other planes exist in myth but rarely matter in play
> 3. **Occasional Importance** - Planar entities or travel comes up sometimes
> 4. **Regular Feature** - Planes are a normal part of the world's magic
> 5. **Central to Setting** - Planar interaction is a major theme
> 6. **The World IS a Plane** - The setting is on a non-material plane
> 7. **Planes Are Dying** - Planar boundaries are failing; this is a problem
> 8. **Planes Are New** - The planes were recently discovered or created
> 9. **Planes Are Dangerous** - Contact with other planes is forbidden/deadly
> 10. **Planes Are Everywhere** - Pocket dimensions and portals are common

If "Not Really", skip to Phase 2 Summary.

#### Step 2C.2: Planar Structure

Ask:
> "How is the cosmos structured?"
>
> 1. **Great Wheel** - Traditional D&D cosmology; inner/outer planes, alignment-based
> 2. **World Tree** - Planes connected by branches of a cosmic tree (Yggdrasil-style)
> 3. **Layered Cake** - Planes stacked vertically (heavens above, hells below)
> 4. **Nested Spheres** - Planes as concentric shells around the material world
> 5. **Parallel Mirrors** - Echo planes reflecting the material (Feywild/Shadowfell)
> 6. **Floating Islands** - Planes as separate realms in an infinite void
> 7. **Dream Logic** - Planes are mental/spiritual realms, not physical places
> 8. **Dimensional Pockets** - Planes are small, artificial, created spaces
> 9. **Quantum Multiverse** - Infinite parallel material worlds
> 10. **Single Membrane** - One reality with thin spots where other things leak through
> 11. **Corpse of a God** - The cosmos is built from divine remains
> 12. **Dying Star** - The cosmos is a single entity slowly collapsing
> 13. **Unique Structure** - Describe your cosmology

Store in `decisions.planar_structure`.

#### Step 2C.3: Which Planes Exist

Ask:
> "What planes or realms exist? Select all that apply:"
>
> **Echo Planes:**
> 1. **Feywild/Faerie** - A wild, magical mirror realm of nature and emotion
> 2. **Shadowfell/Shadow Plane** - A dark, dreary echo realm of death and despair
> 3. **Ethereal Plane** - A ghostly overlap with the material world
> 4. **Mirror Realm** - An opposite reflection of reality
>
> **Elemental Planes:**
> 5. **Plane of Fire** - Realm of flame, heat, and destruction
> 6. **Plane of Water** - Infinite ocean, crushing depths
> 7. **Plane of Earth** - Endless stone, crystals, and darkness
> 8. **Plane of Air** - Boundless sky, floating islands
> 9. **Elemental Chaos** - All elements mixed in primordial turmoil
> 10. **Para-Elemental Planes** - Ice, Magma, Ooze, Smoke, etc.
>
> **Divine Realms:**
> 11. **Individual God Realms** - Each deity has their own plane
> 12. **Shared Heavens** - Good gods share an upper realm
> 13. **Shared Hells** - Evil entities share a lower realm
> 14. **The Astral Plane** - Realm of thought, travel, and dead gods
>
> **Other:**
> 15. **The Far Realm** - Alien dimension of madness beyond reality
> 16. **Positive Energy Plane** - Source of life force and healing
> 17. **Negative Energy Plane** - Source of undeath and entropy
> 18. **Temporal Plane** - Where time is a physical dimension
> 19. **Dream Plane** - Where dreams are real places
> 20. **Other Unique Planes** - Describe

Store in `decisions.planes` as array.

#### Step 2C.4: Planar Accessibility

Ask:
> "How do mortals interact with other planes?"
>
> 1. **They Can't** - Other planes are completely inaccessible to mortals
> 2. **Only in Death** - Souls travel to afterlife planes, but the living cannot
> 3. **Rare High Magic** - Only the most powerful mages can breach barriers
> 4. **Natural Portals** - Some locations permanently connect to other planes
> 5. **Thin Spots** - Certain times/places allow easier crossing
> 6. **Ritual Access** - Proper ceremonies can open temporary doors
> 7. **Dreaming** - Sleep allows consciousness to enter other realms
> 8. **Summoning Only** - Things can be brought here, but mortals can't go there
> 9. **One-Way Only** - Easy to go, hard to return
> 10. **Regular Travel** - Planar travel is known and sometimes common
> 11. **Commercial Travel** - You can buy passage to other planes
> 12. **Accidental Only** - People fall through by accident; no controlled travel

Store in `decisions.planar_access`.

#### Step 2C.5: Create Plane Entities

For each important plane selected, offer:
> "Would you like me to detail [Plane Name] now, or save it for later?"

If yes:
1. Read template: `Templates/Concepts/Plane of Existence.md`
2. Generate based on decisions and tone
3. Apply naming conventions
4. Show preview, get approval
5. Save to `Worlds/[World Name]/Concepts/[Plane Name].md`

---

### Phase 2 Summary

Display progress:
```
╔══════════════════════════════════════════════════════════════╗
║           WORLDBUILDING PROGRESS: [World Name]               ║
╠══════════════════════════════════════════════════════════════╣
║ Phase 1: World Identity        [COMPLETE]                    ║
║ Phase 2: Metaphysical          [COMPLETE]                    ║
║ Phase 3: The Land              [NOT STARTED]                 ║
║ Phase 4: Powers & People       [NOT STARTED]                 ║
║ Phase 5: History & Conflict    [NOT STARTED]                 ║
║ Phase 6: Places of Interest    [NOT STARTED]                 ║
║ Phase 7: Characters            [NOT STARTED]                 ║
║ Phase 8: Society & Daily Life  [NOT STARTED]                 ║
║ Phase 9: Campaign Setup        [NOT STARTED]                 ║
╠══════════════════════════════════════════════════════════════╣
║ Entities Created: X                                          ║
║ - World Overview                                             ║
║ - [Magic System Name] (Magic System)                         ║
║ - [Pantheon Name] (Pantheon)                                 ║
║ - [Deity 1], [Deity 2], ... (Deities)                        ║
║ - [Plane Names] (Planes, if any)                             ║
╠══════════════════════════════════════════════════════════════╣
║ Key Decisions:                                               ║
║ - Magic: [level], [sources]                                  ║
║ - Gods: [structure], [interaction level]                     ║
║ - Planes: [list or "minimal"]                                ║
║ - Afterlife: [summary]                                       ║
╠══════════════════════════════════════════════════════════════╣
║ Commands: continue | back | skip | pause | summary           ║
╚══════════════════════════════════════════════════════════════╝

Ready to continue to Phase 3: The Land?
```

---

## Phase 3: The Land

**Goal:** Create the physical world—geography, ecology, climate, resources, and travel.

### Section 3A: Scale & Focus

#### Step 3A.1: Geographic Scope

Ask:
> "How much of the world do you want to detail?"
>
> 1. **Single Location** - One city, dungeon, or specific place
> 2. **City and Surroundings** - An urban center with nearby countryside
> 3. **Small Region** - A single duchy, province, or county
> 4. **Large Region** - A kingdom or significant territory
> 5. **Multiple Regions** - Several interconnected territories
> 6. **One Continent** - A full landmass with many regions
> 7. **Multiple Continents** - Several major landmasses
> 8. **Entire World** - Comprehensive global geography
> 9. **Island Chain** - An archipelago setting
> 10. **Underworld/Underground** - Focus on subterranean realms
> 11. **Planar** - The "land" is another plane of existence
> 12. **Mobile** - The setting moves (ships, caravans, floating city)

Store in `decisions.geographic_scale`.

**Adaptive Logic:**
- If "Single Location", skip continent/region questions; focus on that location
- If "City and Surroundings", skip broader geography; detail one urban area

#### Step 3A.2: Adventure Location

Ask:
> "Where will most adventures take place?"
>
> 1. **Urban** - Primarily within a single large city (intrigue, crime, politics)
> 2. **Suburban/Settled** - Towns and villages in civilized lands
> 3. **Rural/Agricultural** - Farmland, countryside, pastoral settings
> 4. **Wilderness** - Untamed forests, mountains, wild places
> 5. **Frontier** - Edge of civilization, newly explored lands
> 6. **Borderlands** - Contested areas between realms or cultures
> 7. **Coastal/Maritime** - Seas, ships, ports, and islands
> 8. **River-Based** - Travel and trade along waterways
> 9. **Mountain** - High peaks, passes, and valleys
> 10. **Desert** - Arid wastes, oases, sandstorms
> 11. **Frozen/Arctic** - Ice, snow, and cold survival
> 12. **Jungle/Tropical** - Dense vegetation, humidity, exotic dangers
> 13. **Underground** - Caves, dungeons, Underdark
> 14. **Swamp/Marsh** - Wetlands, bogs, murky waters
> 15. **Ruins/Wastelands** - Post-apocalyptic or cursed terrain
> 16. **Mixed/Traveling** - Moving across many terrain types

Store in `decisions.adventure_focus`.

#### Step 3A.3: Exploration State

Ask:
> "How explored is the world?"
>
> 1. **Fully Mapped** - Every corner is known and documented
> 2. **Well Known** - Major features mapped; minor areas unexplored
> 3. **Mostly Known** - Civilized areas mapped; wilderness mysterious
> 4. **Partially Explored** - Major regions known; vast areas unknown
> 5. **Frontier Era** - Much is being discovered for the first time
> 6. **Largely Unknown** - Only local areas are well known
> 7. **Terra Incognita** - Almost everything beyond home is mystery
> 8. **Recently Revealed** - Something opened up previously unknown lands
> 9. **Actively Hidden** - Someone is keeping areas secret
> 10. **Shifting/Unstable** - Geography itself changes, making mapping hard
> 11. **Magically Obscured** - Divination can't map certain areas
> 12. **Different for Different Peoples** - Some cultures know more than others

Store in `decisions.exploration_state`.

#### Step 3A.4: Supernatural Geography

Ask:
> "Does geography have supernatural elements? Select any that apply:"
>
> 1. **None** - Geography follows real-world logic entirely
> 2. **Floating Islands** - Landmasses suspended in the sky
> 3. **Hollow World** - Inhabited interior beneath the surface
> 4. **Flat World** - The world is flat with edges
> 5. **Infinite Plane** - The world extends forever in all directions
> 6. **World Tree** - A massive tree connects realms
> 7. **World Serpent** - A creature encircles or supports the world
> 8. **World Turtle** - The world rests on a cosmic creature
> 9. **Living Geography** - Mountains walk, forests migrate
> 10. **Magical Zones** - Areas where reality is warped
> 11. **Ley Lines** - Currents of magical energy cross the land
> 12. **Thin Spots** - Places where other planes bleed through
> 13. **Cursed Lands** - Regions twisted by magic or divine wrath
> 14. **Blessed Lands** - Regions protected by divine favor
> 15. **Time Distortions** - Areas where time flows differently
> 16. **Elemental Intrusions** - Raw elemental energy manifests physically
> 17. **Dream Geography** - Places that exist partially in dreams
> 18. **Dead God's Remains** - Landforms are divine corpses
> 19. **Artificial Continent** - Some land was magically created
> 20. **Other** - Describe your supernatural geography

Store in `decisions.supernatural_geography` as array.

---

### Section 3B: Climate & Environment

#### Step 3B.1: Primary Climate

Ask:
> "What's the primary climate of the main region?"
>
> 1. **Temperate Oceanic** - Mild, wet, four seasons (British Isles, Pacific Northwest)
> 2. **Temperate Continental** - Hot summers, cold winters (Central Europe, Midwest)
> 3. **Mediterranean** - Warm, dry summers; mild, wet winters (Greece, California)
> 4. **Subtropical** - Hot, humid summers; mild winters (American South, Southern China)
> 5. **Tropical Rainforest** - Hot and wet year-round (Amazon, Congo)
> 6. **Tropical Monsoon** - Wet and dry seasons (India, Southeast Asia)
> 7. **Arid Desert** - Hot and dry year-round (Sahara, Arabian Peninsula)
> 8. **Cold Desert** - Dry with extreme temperature swings (Gobi, Central Asia)
> 9. **Semi-Arid/Steppe** - Grasslands, moderate rainfall (Great Plains, Mongolia)
> 10. **Subarctic** - Long, cold winters; short summers (Siberia, Alaska)
> 11. **Arctic/Polar** - Frozen most or all of the year (Antarctica, Arctic)
> 12. **Alpine/Highland** - Varies with elevation, generally cold (Alps, Himalayas)
> 13. **Varied** - Multiple climate zones in the main region
> 14. **Magically Controlled** - Climate is artificially maintained
> 15. **Unnatural** - Climate doesn't follow normal rules (eternal twilight, etc.)

Store in `decisions.primary_climate`.

#### Step 3B.2: Weather Patterns

Ask:
> "What notable weather phenomena occur? Select any that apply:"
>
> 1. **Normal/Earthlike** - Weather follows familiar patterns
> 2. **Frequent Storms** - Thunderstorms, lightning, heavy rain common
> 3. **Monsoon Seasons** - Predictable heavy rain periods
> 4. **Blizzards** - Severe winter storms
> 5. **Hurricanes/Typhoons** - Major coastal storms
> 6. **Tornadoes** - Frequent violent windstorms
> 7. **Dust Storms** - Blinding sand/dust clouds
> 8. **Fog Banks** - Dense, persistent mists
> 9. **Drought Cycles** - Regular periods of no rain
> 10. **Flash Floods** - Sudden, dangerous water surges
> 11. **Magical Storms** - Weather with supernatural effects
> 12. **Wild Magic Weather** - Spells can trigger weather events
> 13. **Planar Weather** - Elements from other planes manifest
> 14. **Prophetic Weather** - Weather predicts events
> 15. **Weaponized Weather** - Someone controls the weather
> 16. **Unnatural Stillness** - Weather never changes in some areas
> 17. **Seasonal Extremes** - Winters are deadly cold, summers scorching
> 18. **Unpredictable** - Weather changes without warning
> 19. **Ash/Volcanic** - Volcanic activity affects climate
> 20. **Other** - Describe unusual weather

Store in `decisions.weather_patterns` as array.

#### Step 3B.3: Seasons

Ask:
> "How do seasons work in this world?"
>
> 1. **Four Standard Seasons** - Spring, summer, autumn, winter
> 2. **Two Seasons** - Wet/dry or warm/cold
> 3. **Three Seasons** - Common in tropical/subtropical areas
> 4. **Six Seasons** - More detailed annual cycle
> 5. **Irregular Seasons** - Seasons vary in length unpredictably
> 6. **Eternal Season** - One season dominates (always winter, etc.)
> 7. **Magical Seasons** - Seasons tied to magical cycles
> 8. **God-Controlled** - Deities determine seasonal changes
> 9. **Moons Govern Seasons** - Lunar cycles control weather
> 10. **No Seasons** - Climate is constant year-round
> 11. **Regional Variation** - Different areas have different seasonal patterns
> 12. **Fading Seasons** - Seasons are weakening or changing
> 13. **Harsh Transitions** - Season changes are violent/dangerous
> 14. **Named/Cultural Seasons** - Unique seasonal calendar
> 15. **Other** - Describe your seasonal system

Store in `decisions.seasons`.

---

### Section 3C: Major Landmasses

**Skip if scale is "Single Location" or "City and Surroundings".**

#### Step 3C.1: Main Continent/Region Name

Ask:
> "What's the main landmass or region called?"
>
> Using your [naming_culture] conventions, I can suggest names, or you can provide one.

If user is unsure, generate 5 suggestions based on naming culture and tone.

Store in `decisions.main_landmass_name`.

#### Step 3C.2: Landmass Character

Ask:
> "Describe the character of [Landmass Name] in a few phrases. What's the overall feel?"
>
> Examples by tone:
> - **Epic Fantasy:** "Ancient forests and soaring mountains, dotted with elven spires and dwarven halls"
> - **Dark Fantasy:** "Blighted lands where shadows pool, ruined kingdoms, and forests that whisper"
> - **Low Fantasy:** "War-torn plains, strategic river valleys, fortified hilltops"
> - **Nautical:** "Jagged coastlines, hidden coves, storm-wracked islands"

Store in `decisions.landmass_character`.

#### Step 3C.3: Notable Geographic Features

Ask:
> "What major geographic features define [Landmass Name]? Select 5-10:"
>
> **Mountains:**
> 1. **Major Mountain Range** - Continental spine, natural border
> 2. **Isolated Peak** - Legendary single mountain
> 3. **Volcanic Range** - Active or dormant fire mountains
> 4. **Sacred Mountain** - Holy site, pilgrimage destination
>
> **Water:**
> 5. **Great River** - Major trade artery, life of the region
> 6. **River Delta** - Fertile, densely populated
> 7. **Massive Lake** - Inland sea, unique ecosystem
> 8. **Wetlands/Marshes** - Treacherous, mysterious
> 9. **Major Coastline** - Cliffs, beaches, harbors
> 10. **Inland Sea** - Enclosed body of water
>
> **Forests:**
> 11. **Ancient Forest** - Old-growth, possibly magical
> 12. **Haunted Wood** - Cursed, dangerous, avoided
> 13. **Managed Woodlands** - Cultivated, resource-producing
> 14. **Jungle/Rainforest** - Dense, tropical, exotic
>
> **Plains:**
> 15. **Fertile Farmland** - Agricultural heartland
> 16. **Rolling Hills** - Pastoral, transitional terrain
> 17. **Vast Grasslands** - Steppe, prairie, savanna
> 18. **Moorland/Heath** - Windswept, sparse vegetation
>
> **Harsh Terrain:**
> 19. **Major Desert** - Sand sea, rocky waste
> 20. **Frozen Wastes** - Tundra, ice fields
> 21. **Badlands** - Eroded, broken terrain
> 22. **Volcanic Wasteland** - Lava fields, ash plains
>
> **Other:**
> 23. **Underground Realm** - Vast cave networks
> 24. **Island Chain** - Archipelago off the coast
> 25. **Magical Anomaly** - Reality-warped zone
> 26. **Ancient Ruins Region** - Area dominated by remnants of fallen civilizations

Store in `decisions.major_features` as array.

#### Step 3C.4: Create Continent Entity

1. Read template: `Templates/Geography/Continent.md`
2. Generate based on all decisions
3. Apply naming conventions from chosen culture
4. Show preview:
   > "Here's [Continent Name]. Does this geography work for your vision?"
5. Upon approval, save to `Worlds/[World Name]/Geography/[Continent Name].md`
6. Update state

---

### Section 3D: Regions

#### Step 3D.1: Number of Regions

Ask:
> "How many distinct regions exist in [Main Landmass]?"
>
> 1. **1-2 Regions** - Very focused setting
> 2. **3-4 Regions** - Typical for a single-kingdom campaign
> 3. **5-6 Regions** - Good variety without overwhelming
> 4. **7-8 Regions** - A continent with diverse lands
> 5. **9-10 Regions** - Comprehensive geography
> 6. **11+ Regions** - Very detailed, expansive world
>
> Recommendation: 4-6 regions provides variety without being overwhelming.

Store in `decisions.region_count`.

#### Step 3D.2: Define Each Region

For each region, ask:
> "Tell me about Region [X]:"
>
> 1. **Name:** What's this region called? (I'll apply [naming_culture] conventions)
> 2. **Terrain Type:** What dominates? Choose from:
>    - Mountains | Hills | Forest | Plains/Grassland | Coast | Desert
>    - Swamp/Marsh | Tundra | Jungle | Volcanic | Badlands | River Valley
> 3. **Climate:** Warmer/colder/wetter/drier than average?
> 4. **Who Lives Here:** Primary inhabitants?
> 5. **Known For:** What is this region famous for?
> 6. **Resources:** What valuable things come from here?
> 7. **Dangers:** What threats exist?
> 8. **Character:** In 2-3 words, what's the vibe?

Store each region in `decisions.regions` array.

#### Step 3D.3: Regional Naming Cultures

If user selected "Mixed Regional" for naming culture:
> "Which naming culture applies to [Region Name]?"
>
> [Present the culture options from Step 1.2]

Store regional cultures in `decisions.regional_cultures`.

#### Step 3D.4: Create Region Entities

For each region:
1. Read template: `Templates/Geography/Region.md`
2. Generate using decisions and maintaining consistency
3. Apply appropriate naming conventions
4. Show preview for each:
   > "Here's [Region Name]. Does this work?"
5. Upon approval, save to `Worlds/[World Name]/Geography/[Region Name].md`
6. Ensure wikilinks connect: Regions → Continent

---

### Section 3E: Natural Resources & Ecology

#### Step 3E.1: Valuable Resources

Ask:
> "What resources are valuable and where are they found? Select all that apply:"
>
> **Mining:**
> 1. **Iron/Steel** - Industrial backbone
> 2. **Copper/Bronze** - Ancient metals, still valuable
> 3. **Silver** - Currency, anti-undead, magical uses
> 4. **Gold** - Wealth, jewelry, some magical uses
> 5. **Precious Gems** - Diamonds, rubies, sapphires
> 6. **Mithril/Adamantine** - Magical metals (if fantasy)
> 7. **Coal** - Fuel for industry
> 8. **Salt** - Preservation, essential for life
> 9. **Marble/Stone** - Building material
>
> **Agriculture:**
> 10. **Grain/Wheat** - Food staple
> 11. **Wine/Grapes** - Luxury beverage
> 12. **Spices** - Flavor, preservation, medicine
> 13. **Silk** - Luxury textile
> 14. **Cotton/Linen** - Common textile
> 15. **Timber** - Building, ships, fuel
> 16. **Medicinal Herbs** - Healing plants
>
> **Exotic:**
> 17. **Magical Plants** - Potion ingredients
> 18. **Monster Parts** - Dragon scales, phoenix feathers
> 19. **Magical Minerals** - Glowing crystals, elemental ore
> 20. **Rare Creatures** - Exotic mounts, familiars
> 21. **Arcane Substances** - Residuum, essence, mana crystals
> 22. **Ancient Artifacts** - Salvage from ruins

For each selected, note which region it comes from.

Store in `decisions.resources` as object mapping resource to region.

#### Step 3E.2: Scarce Resources

Ask:
> "What resources are scarce or fought over?"
>
> (List the selected resources)
>
> Which are rare enough to cause conflict?

Store in `decisions.scarce_resources`.

#### Step 3E.3: Common Flora

Ask:
> "What notable plants exist? For each region, what grows there?"
>
> I'll generate appropriate flora based on climate and terrain, or you can specify particular plants.
>
> Any unique or magical plants you want to include?

Store in `decisions.notable_flora`.

#### Step 3E.4: Common Fauna

Ask:
> "What animals are common? Select categories present in your world:"
>
> **Domestic:**
> 1. **Horses** - Cavalry and transport
> 2. **Cattle** - Meat, leather, dairy
> 3. **Sheep/Goats** - Wool, meat, milk
> 4. **Pigs** - Meat
> 5. **Chickens/Poultry** - Eggs, meat
> 6. **Dogs** - Companions, hunting, herding
> 7. **Cats** - Pest control, companions
> 8. **Exotic Mounts** - Unusual riding animals
>
> **Wild:**
> 9. **Deer/Elk** - Hunting game
> 10. **Boar** - Dangerous game
> 11. **Wolves** - Predators, pack hunters
> 12. **Bears** - Territorial predators
> 13. **Big Cats** - Lions, tigers, panthers
> 14. **Raptors** - Eagles, hawks, falcons
> 15. **Songbirds** - Environment detail
>
> **Aquatic:**
> 16. **Fish** - Food source
> 17. **Whales** - Hunting, mystical
> 18. **Sharks** - Ocean predators
> 19. **Crustaceans** - Food, pest
>
> **Fantasy:**
> 20. **Wyverns** - Smaller dragon-kin
> 21. **Griffons** - Eagle-lion hybrids
> 22. **Giant Insects** - Oversized bugs
> 23. **Dire Animals** - Larger, fiercer versions
> 24. **Magical Beasts** - Unique fantasy creatures

Store in `decisions.common_fauna`.

---

### Section 3F: Travel & Trade

#### Step 3F.1: Travel Times

Ask:
> "How long does travel take in this world?"
>
> **On Foot:**
> 1. **Realistic Medieval** - 15-25 miles/day on roads; less cross-country
> 2. **Slightly Faster** - 25-35 miles/day (heroic pace)
> 3. **Much Faster** - 40+ miles/day (cinematic)
> 4. **Varies by Terrain** - Detailed system based on ground
>
> **Mounted:**
> 5. **Realistic** - 30-40 miles/day, horses need rest
> 6. **Fast** - 50+ miles/day
> 7. **Fantasy Mounts** - Flying or magical creatures change everything
>
> **Magical Travel:**
> 8. **Nonexistent** - No magical transportation
> 9. **Rare** - Teleportation exists but is very rare
> 10. **Available for Wealthy** - Magical transit can be purchased
> 11. **Common** - Teleportation circles, flying mounts are normal
>
> **Infrastructure:**
> 12. **Poor Roads** - Most travel is difficult
> 13. **Good Roads** - Major routes are well-maintained
> 14. **Excellent Roads** - Roman-style road network
> 15. **River/Canal System** - Water travel is fastest

Store in `decisions.travel_system`.

#### Step 3F.2: Trade Routes

Ask:
> "What major trade routes exist?"
>
> For each route, describe:
> 1. **Start and End Points**
> 2. **What's Traded**
> 3. **Dangers Along the Way**
>
> Or I can generate trade routes based on your regions and resources.

Store in `decisions.trade_routes`.

#### Step 3F.3: Dangerous Areas

Ask:
> "What areas are dangerous to travel through? Select hazards:"
>
> **Natural Hazards:**
> 1. **Bandit Territory** - Outlaws prey on travelers
> 2. **Monster-Infested** - Creatures attack travelers
> 3. **Harsh Terrain** - Deserts, mountains, swamps
> 4. **Severe Weather** - Storms, blizzards, flash floods
> 5. **Diseased Area** - Plague, miasma, corruption
>
> **Supernatural Hazards:**
> 6. **Haunted Roads** - Ghosts, spirits, undead
> 7. **Cursed Lands** - Dark magic affects travelers
> 8. **Wild Magic Zones** - Unpredictable magical effects
> 9. **Planar Thin Spots** - Other realms bleed through
> 10. **Fey Territory** - The fair folk are dangerous
>
> **Political Hazards:**
> 11. **Contested Borders** - Armies clash
> 12. **Toll Roads** - Heavy fees to pass
> 13. **Hostile Territory** - Locals attack outsiders
> 14. **Forbidden Zones** - Travel is illegal
> 15. **No-Man's-Land** - Unclaimed, lawless areas

Store in `decisions.dangerous_areas` as array.

---

### Phase 3 Summary

Display progress:
```
╔══════════════════════════════════════════════════════════════╗
║           WORLDBUILDING PROGRESS: [World Name]               ║
╠══════════════════════════════════════════════════════════════╣
║ Phase 1: World Identity        [COMPLETE]                    ║
║ Phase 2: Metaphysical          [COMPLETE]                    ║
║ Phase 3: The Land              [COMPLETE]                    ║
║ Phase 4: Powers & People       [NOT STARTED]                 ║
║ Phase 5: History & Conflict    [NOT STARTED]                 ║
║ Phase 6: Places of Interest    [NOT STARTED]                 ║
║ Phase 7: Characters            [NOT STARTED]                 ║
║ Phase 8: Society & Daily Life  [NOT STARTED]                 ║
║ Phase 9: Campaign Setup        [NOT STARTED]                 ║
╠══════════════════════════════════════════════════════════════╣
║ Entities Created: X                                          ║
║ - Geography:                                                 ║
║   - [Continent Name] (Continent)                             ║
║   - [Region 1], [Region 2], ... (Regions)                    ║
║   - [Feature entities if created]                            ║
╠══════════════════════════════════════════════════════════════╣
║ Key Decisions:                                               ║
║ - Scale: [scope]                                             ║
║ - Climate: [climate]                                         ║
║ - Regions: [count]                                           ║
║ - Resources: [key resources]                                 ║
╠══════════════════════════════════════════════════════════════╣
║ Commands: continue | back | skip | pause | summary           ║
╚══════════════════════════════════════════════════════════════╝

Ready to continue to Phase 4: Powers & People?
```

---

## Phase 4: Powers & People

**Goal:** Establish who lives here, how they're organized, and the systems that govern them.

### Section 4A: Peoples & Species

#### Step 4A.1: Intelligent Species

Ask:
> "What intelligent species inhabit this world?"
>
> 1. **Humans Only** - Only humans exist (skip species questions)
> 2. **Humans Dominant** - Other species exist but are rare
> 3. **Standard D&D Races** - Humans, elves, dwarves, halflings, gnomes, common others
> 4. **Limited Selection** - A few specific species only
> 5. **Expanded D&D** - Standard plus dragonborn, tieflings, orcs, etc.
> 6. **Custom Only** - Only unique species you design
> 7. **Mix of Standard and Custom** - D&D basics plus unique species
> 8. **Monstrous Focus** - "Monster" races are playable and common
> 9. **All Species Equal** - No species is more common than others
> 10. **One Non-Human** - Humans plus one other significant species
> 11. **Fey-Touched** - Species have connections to otherworlds
> 12. **Extinct Species** - Some races used to exist but are gone

Store in `decisions.species_approach`.

#### Step 4A.2: Species Distribution

If using multiple species:
> "For each species, indicate their status:"
>
> **Commonality:**
> 1. **Dominant** - This species rules/leads civilization
> 2. **Common** - Found everywhere, fully integrated
> 3. **Regional** - Common in specific areas
> 4. **Uncommon** - Present but notable
> 5. **Rare** - Few exist, often remarkable
> 6. **Very Rare** - Legends, most never meet one
> 7. **Unique** - Only one or a handful exist
> 8. **Extinct** - Gone, only ruins remain
> 9. **Hidden** - Exist but conceal themselves
> 10. **New Arrivals** - Recently appeared
> 11. **Declining** - Dying out
> 12. **Ascending** - Growing in power/numbers

Store in `decisions.species_distribution`.

#### Step 4A.3: Species Relations

Ask:
> "How do different species relate to each other?"
>
> 1. **Utopian Integration** - All species live together harmoniously
> 2. **Peaceful Coexistence** - Different but cooperative
> 3. **Separate but Equal** - Species have their own territories, respect borders
> 4. **Trade Partners** - Primarily economic relationships
> 5. **Wary Tolerance** - Coexist but with suspicion
> 6. **Historical Tensions** - Old conflicts, current peace
> 7. **Active Prejudice** - Discrimination is common
> 8. **Segregation** - Species don't mix, contact is rare
> 9. **Hierarchy** - Some species are "superior" to others
> 10. **Master/Servant** - One species enslaves or dominates others
> 11. **Open Conflict** - Species are at war
> 12. **Varies by Region** - Different areas have different relations
> 13. **Varies by Species** - Some get along, others don't
> 14. **Class-Based** - Species correlates with social class
> 15. **Complex Web** - Different relationships between each pair

Store in `decisions.species_relations`.

#### Step 4A.4: Custom Species

If creating custom species:
> "For each unique species, tell me:"
>
> 1. **Name:** What are they called?
> 2. **Appearance:** Brief physical description
> 3. **Origin:** Where did they come from?
> 4. **Homeland:** Where do they live?
> 5. **Culture Hook:** One defining cultural trait
> 6. **Reputation:** How do others see them?
> 7. **Special Ability:** Any unique capability?
> 8. **Weakness:** Any vulnerability?

Create Species entities for each custom species.

---

### Section 4B: Nations & Governments

#### Step 4B.1: Number of Powers

Ask:
> "How many major political powers exist in the main region?"
>
> 1. **One Unified Empire** - A single power dominates
> 2. **Two Rivals** - Binary opposition (cold war, etc.)
> 3. **Three Powers** - Triangular politics
> 4. **4-5 Major Powers** - Classic multi-state system
> 5. **6-8 Kingdoms** - Many competing realms
> 6. **Dozens of City-States** - Fragmented like Greek poleis
> 7. **Hundreds of Petty Lords** - Extreme fragmentation
> 8. **Tribal Confederacies** - Loose alliances, no central power
> 9. **Theocratic Zones** - Religion defines borders
> 10. **Corporate/Guild Territories** - Economic powers rule
> 11. **Anarchy/No Nations** - No organized government
> 12. **Post-Imperial Fragments** - An empire recently collapsed

Store in `decisions.power_count`.

#### Step 4B.2: Government Types

For each major power, ask:
> "What kind of government rules [Nation X]?"
>
> **Monarchies:**
> 1. **Absolute Monarchy** - King's word is law
> 2. **Constitutional Monarchy** - King limited by laws/council
> 3. **Elective Monarchy** - Nobles choose the king
> 4. **Feudal Monarchy** - King rules through vassal lords
> 5. **Sacred Monarchy** - King is divine or semi-divine
>
> **Aristocracies:**
> 6. **Oligarchy** - Council of noble families rules
> 7. **Plutocracy** - Wealthy families control government
> 8. **Meritocracy** - Power based on ability/achievement
> 9. **Gerontocracy** - Elders rule
> 10. **Stratocracy** - Military leaders govern
>
> **Republics:**
> 11. **Republic** - Elected representatives govern
> 12. **Democracy** - Citizens vote directly on issues
> 13. **Merchant Republic** - Traders elect leaders
>
> **Theocracies:**
> 14. **Theocracy** - Religious leaders govern
> 15. **Divine Rule** - God-king, living deity rules
> 16. **Temple-State** - Temple is the government
>
> **Other:**
> 17. **Magocracy** - Mages rule
> 18. **Kritarchy** - Judges/law-speakers rule
> 19. **Anarchy** - No formal government
> 20. **Occupied Territory** - Ruled by foreign power

Store in `decisions.government_types`.

#### Step 4B.3: Define Major Nations

For each major power, ask:
> "Tell me about [Nation X]:"
>
> 1. **Name:** Using [naming_culture] conventions
> 2. **Government Type:** From above
> 3. **Current Ruler:** Name, title, 2-3 word personality
> 4. **Capital City:** Name and brief description
> 5. **Territory:** Which region(s) do they control?
> 6. **Population:** Rough size and composition
> 7. **Known For:** What is this nation famous for?
> 8. **Military Strength:** Weak | Average | Strong | Dominant
> 9. **Economic Strength:** Poor | Developing | Prosperous | Wealthy
> 10. **Greatest Strength:** What advantage do they have?
> 11. **Greatest Weakness:** What vulnerability?
> 12. **Current Goal:** What does leadership want?
> 13. **Secret Agenda:** What are they really after?

Store in `decisions.nations` as array.

#### Step 4B.4: International Relations

Ask:
> "How do these powers relate to each other? For each pair:"
>
> 1. **Allied** - Formal alliance, mutual defense
> 2. **Friendly** - Good relations, no formal treaty
> 3. **Trade Partners** - Economic ties, neutral otherwise
> 4. **Neutral** - No significant relationship
> 5. **Cool/Distant** - Minimal contact, mild distrust
> 6. **Rivals** - Competition but not war
> 7. **Cold War** - Hostile but not openly fighting
> 8. **Border Skirmishes** - Low-level conflict
> 9. **At War** - Open warfare
> 10. **Vassal/Overlord** - One serves the other
> 11. **Blood Feud** - Historical hatred
> 12. **Recently Changed** - Status is in flux

Store in `decisions.nation_relations`.

---

### Section 4C: Social Structure

#### Step 4C.1: Social Classes

Ask:
> "What social classes exist? Select the structure:"
>
> 1. **Classless Society** - No formal distinctions
> 2. **Two Classes** - Nobles and commoners
> 3. **Three Estates** - Clergy, nobles, commoners
> 4. **Four Classes** - Nobles, merchants, artisans, peasants
> 5. **Complex Hierarchy** - Many ranks and distinctions
> 6. **Caste System** - Birth determines role, no mobility
> 7. **Meritocratic** - Class based on achievement
> 8. **Wealth-Based** - Money determines status
> 9. **Professional** - Guilds/occupations define status
> 10. **Species-Based** - Race determines class
> 11. **Magical** - Magical ability determines status
> 12. **Religious** - Piety determines standing
> 13. **Military** - Service record determines rank
> 14. **Varies by Region** - Different systems in different places

Store in `decisions.social_structure`.

#### Step 4C.2: Social Mobility

Ask:
> "How easy is it to change social class?"
>
> 1. **Impossible** - Born into your place, die there
> 2. **Nearly Impossible** - Rare exceptions, usually through violence
> 3. **Very Difficult** - Possible but requires extraordinary circumstances
> 4. **Difficult** - Possible through great achievement or wealth
> 5. **Challenging** - Requires effort but achievable
> 6. **Moderate** - Common to move up or down
> 7. **Easy** - Social fluidity is normal
> 8. **Very Easy** - Class barely matters
> 9. **One-Way Up** - Can rise, rarely fall
> 10. **One-Way Down** - Easy to fall, hard to rise
> 11. **Varies by Class** - Some barriers harder than others
> 12. **Varies by Region** - Different areas have different mobility

Store in `decisions.social_mobility`.

#### Step 4C.3: Rights and Freedoms

Ask:
> "What rights do common people have?"
>
> 1. **None** - Peasants are property
> 2. **Minimal** - Right to life (barely), nothing else
> 3. **Basic** - Right to life, property, and family
> 4. **Moderate** - Basic rights plus limited legal protections
> 5. **Significant** - Rights to trade, travel, appeal to courts
> 6. **Extensive** - Near-modern rights for commoners
> 7. **Equal** - Same rights as nobility
> 8. **Varies by Class** - Different rights for different classes
> 9. **Varies by Species** - Different species have different rights
> 10. **Varies by Gender** - Different rights based on gender
> 11. **Varies by Religion** - Followers of state religion have more rights
> 12. **Varies by Region** - Different areas grant different rights

Store in `decisions.common_rights`.

---

### Section 4D: Law & Justice

#### Step 4D.1: Legal System

Ask:
> "How does law work?"
>
> 1. **No Formal Law** - Custom and strength rule
> 2. **Oral Tradition** - Laws passed down verbally
> 3. **Written Code** - Laws are recorded and standardized
> 4. **Case Law** - Precedent from past judgments
> 5. **Divine Law** - Religious texts are the law
> 6. **Royal Decree** - The ruler's word is law
> 7. **Council Law** - Laws made by deliberation
> 8. **Ancient Law** - Old laws still in force, rarely updated
> 9. **Complex/Layered** - Multiple legal systems overlap
> 10. **Magical Law** - Magic is used to enforce or determine law
> 11. **Trial by Ordeal** - Gods/nature determine guilt
> 12. **Trial by Combat** - Might makes right

Store in `decisions.legal_system`.

#### Step 4D.2: Justice Administration

Ask:
> "Who administers justice?"
>
> 1. **Local Lord** - Feudal lord judges
> 2. **Appointed Judges** - Crown-appointed officials
> 3. **Elected Judges** - Community chooses judges
> 4. **Religious Courts** - Priests judge
> 5. **Elder Council** - Elders decide
> 6. **Jury System** - Peers judge
> 7. **Military Tribunals** - Soldiers judge
> 8. **Guild Courts** - Professional organizations judge their own
> 9. **Traveling Judges** - Circuit courts
> 10. **Vigilante Justice** - No formal system
> 11. **Magical Inquisition** - Mages investigate and judge
> 12. **Multiple Systems** - Different courts for different matters

Store in `decisions.justice_system`.

#### Step 4D.3: Punishments

Ask:
> "What punishments are common? Select all used:"
>
> 1. **Fines** - Monetary penalties
> 2. **Restitution** - Pay the victim
> 3. **Stocks/Pillory** - Public humiliation
> 4. **Flogging/Beating** - Corporal punishment
> 5. **Branding** - Permanent marking
> 6. **Mutilation** - Removal of body parts
> 7. **Imprisonment** - Dungeons and jails
> 8. **Hard Labor** - Forced work
> 9. **Exile/Banishment** - Forced to leave
> 10. **Slavery** - Sold as punishment
> 11. **Execution** - Death penalty
> 12. **Public Execution** - Spectacle of death
> 13. **Torture** - Pain as punishment
> 14. **Magical Punishment** - Curses, transformations
> 15. **Blood Price** - Family can pay to avoid punishment
> 16. **Trial by Combat** - Fight for freedom
> 17. **Rehabilitation** - Reform attempts
> 18. **Outlawry** - Stripped of legal protection

Store in `decisions.punishments`.

---

### Section 4E: Economy

#### Step 4E.1: Economic System

Ask:
> "What's the economic system?"
>
> 1. **Subsistence** - People produce what they need
> 2. **Barter** - Trade goods for goods
> 3. **Simple Money Economy** - Coins and markets
> 4. **Complex Commerce** - Banks, credit, contracts
> 5. **Feudal Economy** - Lords control production
> 6. **Guild Economy** - Craft guilds control trades
> 7. **Command Economy** - State controls production
> 8. **Mercantile** - Trade and profit focused
> 9. **Slave Economy** - Labor is enslaved
> 10. **Magical Economy** - Magic production is key
> 11. **Mixed Systems** - Different regions vary
> 12. **Transitioning** - Economy is changing

Store in `decisions.economic_system`.

#### Step 4E.2: Currency

Ask:
> "What currency is used?"
>
> 1. **No Currency** - Barter only
> 2. **Commodity Money** - Salt, cattle, grain
> 3. **Simple Coins** - One metal, one denomination
> 4. **Multiple Denominations** - Gold, silver, copper
> 5. **Multiple Currencies** - Each nation has its own
> 6. **Universal Currency** - One currency everywhere
> 7. **Trade Bars** - Standardized metal bars
> 8. **Paper Money** - Notes and bills
> 9. **Magical Currency** - Enchanted tokens or crystals
> 10. **Credit System** - Debt-based, letters of credit
> 11. **Mixed** - Different systems in different places
> 12. **Guild Scrip** - Organizations issue their own currency

Store in `decisions.currency_type`.

#### Step 4E.3: Trade & Commerce

Ask:
> "How is trade organized?"
>
> 1. **Minimal Trade** - Self-sufficient communities
> 2. **Local Markets** - Trade within regions
> 3. **Long-Distance Trade** - Caravan routes, merchant ships
> 4. **Merchant Companies** - Organized trading ventures
> 5. **Guild Control** - Trade guilds regulate commerce
> 6. **State Monopolies** - Government controls key trades
> 7. **Free Trade** - Minimal regulation
> 8. **Smuggling Culture** - Much trade is illegal
> 9. **Magical Trade** - Teleportation, magical goods
> 10. **Colonial Trade** - Resources extracted from periphery
> 11. **Fair System** - Seasonal markets and fairs
> 12. **Mixed** - Different approaches in different places

Store in `decisions.trade_organization`.

---

### Section 4F: Military

#### Step 4F.1: Military Organization

Ask:
> "How are militaries organized?"
>
> 1. **No Standing Army** - Militias when needed
> 2. **Feudal Levies** - Lords bring their men
> 3. **Conscript Army** - All citizens serve
> 4. **Professional Army** - Paid, trained soldiers
> 5. **Mercenary Forces** - Hired companies
> 6. **Religious Warriors** - Holy orders fight
> 7. **Mage Corps** - Magic-using military
> 8. **Naval Power** - Sea forces dominate
> 9. **Cavalry Dominant** - Horse warriors supreme
> 10. **Tribal Warriors** - Individual fighters, loose organization
> 11. **Monster Corps** - Trained monsters serve
> 12. **Mixed Forces** - Combination of types

Store in `decisions.military_organization`.

#### Step 4F.2: Warfare Style

Ask:
> "How is war conducted?"
>
> 1. **Ritualized Combat** - Formal, limited warfare
> 2. **Siege Warfare** - Castles and sieges
> 3. **Open Battle** - Field armies clash
> 4. **Raiding/Skirmishing** - Hit-and-run tactics
> 5. **Guerrilla Warfare** - Insurgent tactics
> 6. **Naval Warfare** - Sea battles dominate
> 7. **Total War** - No distinction between military and civilian
> 8. **Magical Warfare** - Spells and enchantments are weapons
> 9. **Aerial Combat** - Flying mounts/creatures
> 10. **Underground War** - Tunnel fighting
> 11. **Champion Combat** - Single combat decides battles
> 12. **Diplomatic War** - Assassination, subterfuge

Store in `decisions.warfare_style`.

---

### Section 4G: Organizations

#### Step 4G.1: Organization Types

Ask:
> "What types of organizations exist? Select all that apply:"
>
> **Professional:**
> 1. **Adventurers' Guild** - Hires and supports adventuring parties
> 2. **Merchants' Guild** - Controls trade and commerce
> 3. **Craft Guilds** - Smiths, weavers, carpenters, etc.
> 4. **Bardic College** - Performers, historians, spies
>
> **Religious:**
> 5. **Temple Hierarchy** - Organized priesthood
> 6. **Monastic Orders** - Contemplative communities
> 7. **Militant Orders** - Religious warriors
> 8. **Inquisition** - Enforcers of religious law
>
> **Criminal:**
> 9. **Thieves' Guild** - Organized theft and burglary
> 10. **Assassins' Guild** - Professional killers
> 11. **Smuggling Ring** - Illegal trade
> 12. **Criminal Syndicate** - Organized crime empire
>
> **Magical:**
> 13. **Mage Academy** - Training wizards
> 14. **Arcane Council** - Regulating magic
> 15. **Druid Circle** - Nature guardians
> 16. **Warlock Coven** - Pact-bound mages
>
> **Political:**
> 17. **Knightly Order** - Chivalric warriors
> 18. **Secret Society** - Hidden agenda
> 19. **Noble Houses** - Aristocratic families
> 20. **Spy Network** - Intelligence gathering
>
> **Other:**
> 21. **Monster Hunters** - Specialists in dangerous prey
> 22. **Explorer's League** - Mapping the unknown
> 23. **Healer's Circle** - Medical organization
> 24. **Revolutionary Movement** - Seeking change

Store in `decisions.organization_types` as array.

#### Step 4G.2: Detail Major Organizations

For each selected type, ask:
> "Tell me about the [organization type]:"
>
> 1. **Name:** What are they called?
> 2. **Headquarters:** Where are they based?
> 3. **Leader:** Who's in charge?
> 4. **Public Purpose:** What do people think they do?
> 5. **True Purpose:** What are they really after?
> 6. **Membership:** Who can join? How?
> 7. **Influence:** Local | Regional | National | International
> 8. **Resources:** Poor | Moderate | Wealthy | Vast
> 9. **Relationship to Power:** Friend | Foe | Independent
> 10. **Secret:** What does the organization hide?

Create Organization entities for each.

---

### Phase 4 Summary

Display progress:
```
╔══════════════════════════════════════════════════════════════╗
║           WORLDBUILDING PROGRESS: [World Name]               ║
╠══════════════════════════════════════════════════════════════╣
║ Phase 1: World Identity        [COMPLETE]                    ║
║ Phase 2: Metaphysical          [COMPLETE]                    ║
║ Phase 3: The Land              [COMPLETE]                    ║
║ Phase 4: Powers & People       [COMPLETE]                    ║
║ Phase 5: History & Conflict    [NOT STARTED]                 ║
║ Phase 6: Places of Interest    [NOT STARTED]                 ║
║ Phase 7: Characters            [NOT STARTED]                 ║
║ Phase 8: Society & Daily Life  [NOT STARTED]                 ║
║ Phase 9: Campaign Setup        [NOT STARTED]                 ║
╠══════════════════════════════════════════════════════════════╣
║ Entities Created: X                                          ║
║ - Governments: [list]                                        ║
║ - Organizations: [list]                                      ║
║ - Species (if custom): [list]                                ║
╠══════════════════════════════════════════════════════════════╣
║ Key Decisions:                                               ║
║ - Nations: [count] major powers                              ║
║ - Social Structure: [type]                                   ║
║ - Legal System: [type]                                       ║
║ - Economy: [type]                                            ║
╠══════════════════════════════════════════════════════════════╣
║ Commands: continue | back | skip | pause | summary           ║
╚══════════════════════════════════════════════════════════════╝

Ready to continue to Phase 5: History & Conflict?
```

---

## Phase 5: History & Conflict

**Goal:** Establish what happened, what's legend, and what tensions drive the present.

### Section 5A: Historical Structure

#### Step 5A.1: Historical Divisions

Ask:
> "How do people in this world divide their history?"
>
> 1. **Linear** - Before/after a single defining event
> 2. **Two Ages** - Before and after a major change
> 3. **Three Ages** - Ancient, middle, and modern eras
> 4. **Four Ages** - Detailed chronological divisions
> 5. **Five+ Ages** - Very detailed historical periods
> 6. **Cyclical** - History repeats in patterns
> 7. **Dynastic** - Measured by ruling houses
> 8. **Religious** - Marked by prophets or divine events
> 9. **Cataclysmic** - Measured by disasters
> 10. **Forgotten** - The past is unknown or lost
> 11. **Mythic Blur** - Past and legend are inseparable
> 12. **Multiple Systems** - Different cultures count differently

Store in `decisions.history_structure`.

#### Step 5A.2: Historical Depth

Ask:
> "How deep does recorded history go?"
>
> 1. **Living Memory** - Only a few generations
> 2. **Centuries** - Several hundred years
> 3. **Millennia** - Thousands of years
> 4. **Tens of Millennia** - Vast ages of history
> 5. **Hundreds of Millennia** - Almost unimaginable time
> 6. **Unknown** - Nobody knows how old things are
> 7. **Varies by Culture** - Some remember more than others
> 8. **Recently Discovered** - Old history was lost, now being recovered
> 9. **Deliberately Obscured** - Someone hides the past
> 10. **Magically Preserved** - Perfect records exist
> 11. **Completely Lost** - Only fragments remain
> 12. **Cycles Mean Nothing** - Time works differently

Store in `decisions.history_depth`.

#### Step 5A.3: Define Ages

For each age (based on historical divisions), ask:
> "Tell me about [Age X]:"
>
> 1. **Name:** What is this era called?
> 2. **Duration:** When did it start/end? How long?
> 3. **Defining Trait:** What characterized this era?
> 4. **Beginning:** What started this age?
> 5. **End:** What ended this age? (if not current)
> 6. **Technology:** What was the tech level?
> 7. **Magic:** How did magic work/differ?
> 8. **Major Powers:** Who ruled?
> 9. **Legacy:** What did this age leave behind?

Store in `decisions.ages` array.

---

### Section 5B: Defining Events

#### Step 5B.1: Major Historical Events

Ask:
> "What 5-10 events most shaped the current world? Select or describe:"
>
> **Creation & Cosmology:**
> 1. **World Creation** - How everything began
> 2. **Divine War** - Gods battled each other
> 3. **First Dawn** - The first sunrise or beginning of time
> 4. **Planar Separation** - Worlds became distinct
>
> **Rise & Fall:**
> 5. **Rise of First Civilization** - The first great culture
> 6. **Golden Age Beginning** - An era of prosperity began
> 7. **Empire at Its Height** - A power reached its peak
> 8. **Fall of an Empire** - A great power collapsed
> 9. **Dynasty End** - A ruling line ended
>
> **Wars & Conflicts:**
> 10. **Great War** - A conflict that reshaped everything
> 11. **Betrayal** - A treachery that echoes through time
> 12. **Conquest** - One power conquered many
> 13. **Revolution** - The common people rose
> 14. **Civil War** - A nation tore itself apart
>
> **Disasters:**
> 15. **Cataclysm** - Natural or magical devastation
> 16. **Plague** - Disease swept the land
> 17. **Famine** - Starvation killed millions
> 18. **Magical Catastrophe** - A spell went terribly wrong
> 19. **Divine Punishment** - Gods struck the world
>
> **Supernatural:**
> 20. **Divine Intervention** - Gods directly changed things
> 21. **First Magic** - Magic was discovered or created
> 22. **Awakening** - Something ancient stirred
> 23. **Sealing/Binding** - Something terrible was imprisoned
> 24. **Prophecy Given** - A foretelling shaped history
>
> **Discovery:**
> 25. **First Contact** - Different peoples met
> 26. **Discovery** - Something important was found
> 27. **Invention** - Technology changed everything
> 28. **Lost Knowledge Found** - Ancient secrets recovered

Store in `decisions.major_events` as array.

#### Step 5B.2: Detail Each Event

For each selected event, ask:
> "Tell me about [Event Name]:"
>
> 1. **Full Name:** What is it called?
> 2. **When:** Which age? How long ago?
> 3. **Location:** Where did it happen?
> 4. **Cause:** What led to this?
> 5. **Key Figures:** Who were the major players?
> 6. **What Happened:** Brief description
> 7. **Immediate Consequence:** What changed right away?
> 8. **Long-Term Impact:** How does it affect today?
> 9. **Evidence:** What remains? (Ruins, artifacts, scars)
> 10. **Memory:** How is it remembered?

Create History entities for major events.

---

### Section 5C: Legends & Mysteries

#### Step 5C.1: Historical Mysteries

Ask:
> "What mysteries surround history? Select any that apply:"
>
> **Lost Things:**
> 1. **Lost Civilization** - A people vanished, leaving only ruins
> 2. **Lost City** - A legendary place no one can find
> 3. **Lost Artifact** - A powerful item is missing
> 4. **Lost Knowledge** - Ancient wisdom is forgotten
> 5. **Lost Heir** - A bloodline disappeared
> 6. **Lost Continent** - A landmass sank or vanished
>
> **Unknown Events:**
> 7. **Unexplained Disaster** - Something terrible happened, cause unknown
> 8. **Mysterious Disappearance** - People or things vanished
> 9. **Impossible Structure** - Something was built that shouldn't exist
> 10. **Time Gap** - A period no one remembers
>
> **Disputed History:**
> 11. **Conflicting Accounts** - Different cultures tell it differently
> 12. **Deliberate Falsification** - History was rewritten
> 13. **Prophecy Interpretation** - What does the prophecy really mean?
> 14. **True Origins** - The real origin of something is unknown
>
> **Ongoing Mysteries:**
> 15. **Recurring Phenomenon** - Something happens regularly, inexplicably
> 16. **Ancient Guardian** - Something or someone watches
> 17. **Sealed Evil** - Something is imprisoned, but what?
> 18. **Coming Event** - Something is prophesied but unclear
> 19. **Hidden Player** - Someone has manipulated events
> 20. **Cosmic Mystery** - Something about reality itself

Store in `decisions.historical_mysteries` as array.

#### Step 5C.2: Legends vs. Truth

Ask:
> "For each mystery or major event, is the common belief true?"
>
> For each:
> 1. **Common Belief:** What do most people think?
> 2. **Truth:** What really happened?
> 3. **Who Knows:** Does anyone know the truth?
> 4. **Evidence:** What clues exist?
> 5. **Consequence if Revealed:** What would happen if truth came out?

Store in `decisions.legends_truth`.

#### Step 5C.3: Prophecies

Ask:
> "What prophecies shape the world? For each:"
>
> 1. **The Prophecy:** What does it say? (Be vague or specific)
> 2. **Source:** Who gave this prophecy?
> 3. **Age:** When was it given?
> 4. **Interpretation:** What do people think it means?
> 5. **True Meaning:** What does it really mean? (Can be uncertain)
> 6. **Fulfillment Status:** Has any of it come true?
> 7. **Key Figures:** Who is mentioned or involved?
> 8. **Seekers:** Who is trying to fulfill or prevent it?

Create Prophecy entities if applicable.

---

### Section 5D: Current Tensions

#### Step 5D.1: Expand Central Conflict

Return to the central conflict from Phase 1:
> "You established the central tension as: '[central_conflict]'. Let's develop it further:"
>
> **Origins:**
> 1. **Root Cause:** What originally started this?
> 2. **Triggering Event:** What made it immediate/urgent?
> 3. **Timeline:** How long has this been going on?
>
> **Factions:**
> 4. **Side A:** Who are they? What do they want?
> 5. **Side B:** Who are they? What do they want?
> 6. **Side C (if any):** Third party?
> 7. **Uncommitted:** Who's neutral? Why?
> 8. **Hidden Players:** Anyone manipulating events?
>
> **Stakes:**
> 9. **If A Wins:** What happens?
> 10. **If B Wins:** What happens?
> 11. **If Status Quo:** What happens if nothing changes?
> 12. **Worst Case:** What's the absolute worst outcome?
> 13. **Best Case:** Is there a way everyone wins?

Store in `decisions.conflict_expanded`.

#### Step 5D.2: Ticking Clocks

Ask:
> "What are the 'ticking clocks'—things that will happen if no one intervenes?"
>
> 1. **Immediate (Days):** What happens soon?
> 2. **Short-Term (Weeks):** What develops next?
> 3. **Medium-Term (Months):** Where is this heading?
> 4. **Long-Term (Years):** What's the ultimate trajectory?
> 5. **Point of No Return:** When is it too late?

Store in `decisions.ticking_clocks`.

#### Step 5D.3: Secondary Conflicts

Ask:
> "What other tensions simmer beneath the main conflict? Select 2-5:"
>
> **Political:**
> 1. **Border Dispute** - Two powers claim the same territory
> 2. **Succession Question** - Who's the rightful heir?
> 3. **Treaty Violation** - Someone broke an agreement
> 4. **Independence Movement** - A region wants freedom
> 5. **Annexed Territory** - Conquered people resist
>
> **Religious:**
> 6. **Heresy** - A splinter faith spreads
> 7. **Holy Site Dispute** - Multiple faiths claim the same place
> 8. **Inquisition** - Religious persecution
> 9. **New Cult** - A dangerous religion grows
> 10. **Divine Silence** - A god stopped answering
>
> **Economic:**
> 11. **Trade War** - Economic conflict
> 12. **Resource Scarcity** - Something is running out
> 13. **Merchant Feud** - Powerful houses battle
> 14. **Guild Dispute** - Organizations fight for control
> 15. **Debt Crisis** - Someone owes too much
>
> **Social:**
> 16. **Class Tension** - Rich vs. poor
> 17. **Species Conflict** - Racial tensions
> 18. **Generational Divide** - Old vs. young
> 19. **Rural vs. Urban** - Countryside vs. city
> 20. **Criminal Ascent** - Organized crime growing

Store in `decisions.secondary_conflicts` as array.

---

### Section 5E: Historical Cycles

#### Step 5E.1: Recurring Patterns

Ask:
> "Does history repeat in this world? Select any patterns:"
>
> 1. **No Patterns** - History is linear and unique
> 2. **Seasonal Cycle** - Events tied to celestial events
> 3. **Generational Cycle** - Similar events every few generations
> 4. **Dynastic Cycle** - Empires rise and fall predictably
> 5. **Magic Cycle** - Magic waxes and wanes
> 6. **Divine Cycle** - Gods sleep and wake
> 7. **Catastrophe Cycle** - Disasters recur
> 8. **Prophetic Cycle** - Prophecies repeat in variations
> 9. **Cosmic Cycle** - Universal patterns
> 10. **Unknown Cycle** - Patterns exist but aren't understood
> 11. **Breaking Cycle** - A cycle is ending or being broken
> 12. **Imposed Cycle** - Something or someone enforces repetition

Store in `decisions.historical_cycles`.

#### Step 5E.2: Where Are We in the Cycle

If cycles exist:
> "Where is the world in its current cycle?"
>
> 1. **Beginning** - A new age is dawning
> 2. **Rising** - Things are building toward a peak
> 3. **Peak** - At the height
> 4. **Declining** - Things are winding down
> 5. **End** - The cycle is concluding
> 6. **Transition** - Between cycles
> 7. **Breaking Point** - The cycle might not repeat
> 8. **Unknown** - No one knows

Store in `decisions.cycle_position`.

---

### Phase 5 Summary

Display progress:
```
╔══════════════════════════════════════════════════════════════╗
║           WORLDBUILDING PROGRESS: [World Name]               ║
╠══════════════════════════════════════════════════════════════╣
║ Phase 1: World Identity        [COMPLETE]                    ║
║ Phase 2: Metaphysical          [COMPLETE]                    ║
║ Phase 3: The Land              [COMPLETE]                    ║
║ Phase 4: Powers & People       [COMPLETE]                    ║
║ Phase 5: History & Conflict    [COMPLETE]                    ║
║ Phase 6: Places of Interest    [NOT STARTED]                 ║
║ Phase 7: Characters            [NOT STARTED]                 ║
║ Phase 8: Society & Daily Life  [NOT STARTED]                 ║
║ Phase 9: Campaign Setup        [NOT STARTED]                 ║
╠══════════════════════════════════════════════════════════════╣
║ Entities Created: X                                          ║
║ - History:                                                   ║
║   - [Age 1], [Age 2], ... (Ages)                            ║
║   - [Event 1], [Event 2], ... (Events)                      ║
║   - [Prophecy] (if any)                                      ║
╠══════════════════════════════════════════════════════════════╣
║ Key Decisions:                                               ║
║ - Ages: [count] historical periods                           ║
║ - Major Events: [list]                                       ║
║ - Current Tensions: [summary]                                ║
║ - Ticking Clocks: [list]                                     ║
╠══════════════════════════════════════════════════════════════╣
║ Commands: continue | back | skip | pause | summary           ║
╚══════════════════════════════════════════════════════════════╝

Ready to continue to Phase 6: Places of Interest?
```

---

## Phase 6: Places of Interest

**Goal:** Create the locations adventurers will visit—settlements, dungeons, landmarks, and routes.

### Section 6A: Major Settlements

#### Step 6A.1: Primary City

Ask:
> "What's the most important city in your main region? (This is probably where adventures start.)"
>
> 1. **Name:** What is it called?
> 2. **Role:** What makes it important?
>    - Capital | Trade Hub | Religious Center | Military Stronghold
>    - Academic Center | Port City | Frontier Outpost | Ancient Seat
> 3. **Size:** Village (<1K) | Town (1-10K) | City (10-50K) | Large City (50-100K) | Metropolis (100K+)
> 4. **Population Mix:** Who lives there?
> 5. **Founded:** When and by whom?
> 6. **Known For:** What's famous about it?

Store in `decisions.primary_city`.

#### Step 6A.2: City Details

For the primary city, ask deeper questions:
> "Tell me more about [City Name]:"
>
> **Geography:**
> 1. **Location:** River | Coast | Mountain | Plain | Island | Underground
> 2. **Defenses:** Walls | Castle | Natural | Magical | None
> 3. **Districts:** Name 3-5 distinctive neighborhoods
>
> **Character:**
> 4. **Atmosphere:** What's the vibe?
>    - Bustling | Quiet | Dangerous | Prosperous | Decaying | Mysterious
> 5. **Architecture:** What style?
>    - Ancient Stone | Timber Frame | Brick | Mixed | Unique
> 6. **Unusual Feature:** What's most interesting or strange?
>
> **Problems:**
> 7. **Current Crisis:** What's the immediate problem?
> 8. **Ongoing Issue:** What chronic problem exists?
> 9. **Secret:** What does the city hide?
>
> **Power:**
> 10. **Ruler:** Who governs?
> 11. **True Power:** Who really controls things?
> 12. **Criminal Element:** What underworld exists?

Create City entity.

#### Step 6A.3: Districts

For each major district, ask:
> "Tell me about [District Name]:"
>
> 1. **Character:** What's this area like?
> 2. **Residents:** Who lives/works here?
> 3. **Notable Location:** What's the most interesting place?
> 4. **Danger:** What risks exist here?
> 5. **Secret:** What's hidden here?

#### Step 6A.4: Secondary Settlements

Ask:
> "How many other settlements matter for your game?"
>
> For each settlement type, how many exist:
> - Towns (1-10K): [number]
> - Villages (<1K): [number]
> - Strongholds: [number]
> - Special locations: [number]
>
> For each, I'll ask for:
> 1. **Name** (using naming conventions)
> 2. **Type** (market town, mining village, border fort, etc.)
> 3. **Location** (which region)
> 4. **One Notable Feature**
> 5. **One Problem or Secret**

Create settlement entities for each.

---

### Section 6B: Key Establishments

#### Step 6B.1: Taverns & Inns

For each major settlement, ask:
> "What tavern or inn is most notable in [Settlement]?"
>
> 1. **Name:** Something memorable
> 2. **Type:** Upscale | Working Class | Shady | Themed | Ancient
> 3. **Proprietor:** Name and brief description
> 4. **Specialty:** What are they known for?
> 5. **Regular Patrons:** Who comes here?
> 6. **Rumors:** What gossip circulates?
> 7. **Secret:** What's hidden?
> 8. **Adventure Hook:** What job might be offered here?

Create Tavern entities.

#### Step 6B.2: Shops & Services

Ask:
> "What notable shops exist? Select types for your main city:"
>
> **Equipment:**
> 1. **Blacksmith/Armorer** - Weapons and armor
> 2. **General Store** - Basic supplies
> 3. **Fletcher/Bowyer** - Ranged weapons
> 4. **Leather Worker** - Armor, bags, gear
>
> **Magic:**
> 5. **Alchemist/Apothecary** - Potions and components
> 6. **Magic Shop** - Enchanted items
> 7. **Scroll Merchant** - Spells for sale
> 8. **Curio Dealer** - Strange artifacts
>
> **Services:**
> 9. **Healer** - Medical services
> 10. **Sage/Scholar** - Information for sale
> 11. **Cartographer** - Maps and navigation
> 12. **Stable** - Mounts and transport
>
> **Specialty:**
> 13. **Exotic Imports** - Rare goods from far lands
> 14. **Pawnbroker** - Buys and sells anything
> 15. **Black Market** - Illegal goods
> 16. **Specialty Craft** - Unique to your world

For each selected shop:
> 1. **Name**
> 2. **Proprietor:** Name and quirk
> 3. **Specialty:** What sets them apart?
> 4. **Secret:** What do they hide?

Create Shop entities.

#### Step 6B.3: Temples & Holy Sites

Ask:
> "What temples exist in [Settlement]?"
>
> For each deity with a presence:
> 1. **Temple Name**
> 2. **Deity Worshipped**
> 3. **Size:** Shrine | Chapel | Temple | Cathedral | Complex
> 4. **Head Priest:** Name and personality
> 5. **Services Offered:** Healing? Blessings? Divination?
> 6. **Tensions:** Any conflicts with other faiths?
> 7. **Secret:** What's hidden in the temple?

Create Temple entities.

---

### Section 6C: Adventure Sites

#### Step 6C.1: Dungeon Types

Ask:
> "What types of adventure sites exist? Select all that interest you:"
>
> **Ancient:**
> 1. **Ruined City** - Fallen civilization, multiple levels
> 2. **Ancient Temple** - Abandoned holy site
> 3. **Buried Vault** - Underground treasure store
> 4. **Forgotten Tomb** - Burial of someone important
> 5. **Collapsed Tower** - Fallen wizard's sanctum
>
> **Natural:**
> 6. **Cave Network** - Natural tunnels, possibly inhabited
> 7. **Underground Lake** - Subterranean water feature
> 8. **Crystal Caverns** - Magical mineral formations
> 9. **Volcanic Vent** - Fire and danger
> 10. **Underwater Ruins** - Sunken structures
>
> **Active:**
> 11. **Monster Lair** - Home of dangerous creatures
> 12. **Bandit Stronghold** - Criminal hideout
> 13. **Cult Sanctum** - Secret worship site
> 14. **Enemy Fortress** - Hostile military installation
> 15. **Slave Camp** - Captives held here
>
> **Supernatural:**
> 16. **Haunted Manor** - Ghost-infested building
> 17. **Cursed Ground** - Magically tainted area
> 18. **Planar Rift** - Gateway to another dimension
> 19. **Wild Magic Zone** - Reality is unstable
> 20. **Sealed Evil** - Prison of something terrible
>
> **Special:**
> 21. **Mobile Dungeon** - It moves (ship, creature, flying)
> 22. **Living Dungeon** - The dungeon itself is alive
> 23. **Temporal Anomaly** - Time works differently
> 24. **Demiplane** - Pocket dimension

Store in `decisions.dungeon_types` as array.

#### Step 6C.2: Create Adventure Sites

For each type selected, ask:
> "Tell me about a [dungeon type]:"
>
> 1. **Name:** What's it called?
> 2. **Location:** Which region? Near what settlement?
> 3. **Origin:** How did it come to be?
> 4. **Original Purpose:** What was it for?
> 5. **Current Occupants:** Who/what lives there now?
> 6. **Notable Features:** What stands out? (3-5 features)
> 7. **Dangers:** What threatens explorers?
> 8. **Treasures:** What rewards might be found?
> 9. **Boss/Guardian:** What's the main threat?
> 10. **Secret:** What's the hidden truth?
> 11. **Difficulty:** What level range is appropriate?
> 12. **Hook:** Why would adventurers go here?

Create Dungeon/Cave entities.

#### Step 6C.3: The Most Dangerous Place

Ask:
> "What's the most dangerous location in the region—the place everyone fears?"
>
> 1. **Name**
> 2. **Location**
> 3. **Why So Dangerous**
> 4. **What Happened There**
> 5. **What Guards It**
> 6. **What Reward Lies Within**
> 7. **What Level Would Be Needed**
> 8. **Is Anyone Seeking It**

---

### Section 6D: Landmarks & Routes

#### Step 6D.1: Natural Landmarks

Ask:
> "What natural landmarks are famous or significant?"
>
> For each:
> 1. **Name**
> 2. **Type:** Mountain | Lake | Waterfall | Canyon | Tree | Cave | Other
> 3. **Significance:** Why does it matter?
> 4. **Legend:** What stories surround it?
> 5. **Danger:** Is it safe to visit?
> 6. **Secret:** What's hidden there?

Create Geography entities.

#### Step 6D.2: Constructed Landmarks

Ask:
> "What built structures are famous landmarks?"
>
> Types to consider:
> 1. **Great Bridge** - Spanning a natural barrier
> 2. **Massive Wall** - Defensive or boundary marker
> 3. **Ancient Monument** - Memorial or marker
> 4. **Lighthouse/Beacon** - Navigation aid
> 5. **Statue/Colossus** - Giant figure
> 6. **Dam** - Water control
> 7. **Road Marker** - Famous milestone
> 8. **Abandoned Structure** - Mysterious building
> 9. **Magical Construct** - Something made by magic
> 10. **Foreign Architecture** - Built by another culture

For each:
> 1. **Name**
> 2. **Builder:** Who made it?
> 3. **Purpose:** Original use?
> 4. **Current State:** Maintained | Decaying | Ruined | Enhanced
> 5. **Significance:** Why is it famous?

#### Step 6D.3: Major Roads & Routes

Ask:
> "What are the major travel routes?"
>
> For each route:
> 1. **Name:** (e.g., "The King's Road," "The Amber Way")
> 2. **Connects:** Start point to end point
> 3. **Type:** Road | River | Sea Route | Mountain Pass | Other
> 4. **Condition:** Excellent | Good | Fair | Poor | Dangerous
> 5. **Controlled By:** Who maintains/patrols it?
> 6. **Dangers:** What threats exist?
> 7. **Notable Stops:** What's along the way?
> 8. **Travel Time:** How long does it take?

Create Road entities.

---

### Phase 6 Summary

Display progress:
```
╔══════════════════════════════════════════════════════════════╗
║           WORLDBUILDING PROGRESS: [World Name]               ║
╠══════════════════════════════════════════════════════════════╣
║ Phase 1: World Identity        [COMPLETE]                    ║
║ Phase 2: Metaphysical          [COMPLETE]                    ║
║ Phase 3: The Land              [COMPLETE]                    ║
║ Phase 4: Powers & People       [COMPLETE]                    ║
║ Phase 5: History & Conflict    [COMPLETE]                    ║
║ Phase 6: Places of Interest    [COMPLETE]                    ║
║ Phase 7: Characters            [NOT STARTED]                 ║
║ Phase 8: Society & Daily Life  [NOT STARTED]                 ║
║ Phase 9: Campaign Setup        [NOT STARTED]                 ║
╠══════════════════════════════════════════════════════════════╣
║ Entities Created: X                                          ║
║ - Settlements:                                               ║
║   - [City], [Town 1], [Village 1], ...                      ║
║   - [Tavern 1], [Shop 1], [Temple 1], ...                   ║
║ - Adventure Sites:                                           ║
║   - [Dungeon 1], [Ruin 1], [Lair 1], ...                    ║
║ - Landmarks: [list]                                          ║
║ - Routes: [list]                                             ║
╠══════════════════════════════════════════════════════════════╣
║ Key Decisions:                                               ║
║ - Primary City: [name]                                       ║
║ - Settlements: [count]                                       ║
║ - Adventure Sites: [count]                                   ║
╠══════════════════════════════════════════════════════════════╣
║ Commands: continue | back | skip | pause | summary           ║
╚══════════════════════════════════════════════════════════════╝

Ready to continue to Phase 7: Characters?
```

---

## Phase 7: Characters & Relationships

**Goal:** Create the NPCs who populate the world and map their relationships.

### Section 7A: Rulers & Leaders

#### Step 7A.1: National Leaders

For each government created in Phase 4, ask:
> "Tell me about the ruler of [Nation]:"
>
> **Identity:**
> 1. **Full Name and Titles**
> 2. **Species/Race**
> 3. **Age**
> 4. **Appearance:** 2-3 sentences
>
> **Personality:**
> 5. **Three Key Traits** (e.g., ambitious, paranoid, just)
> 6. **Greatest Virtue**
> 7. **Fatal Flaw**
> 8. **Secret Desire**
> 9. **Greatest Fear**
>
> **Public Life:**
> 10. **Public Reputation:** What do people think of them?
> 11. **How They Rule:** Hands-on? Distant? Cruel? Just?
> 12. **Key Policies:** What are they known for?
> 13. **Controversies:** What do critics say?
>
> **Private Life:**
> 14. **Family:** Spouse? Children? Heirs?
> 15. **Inner Circle:** Who do they trust?
> 16. **Enemies:** Who opposes them?
> 17. **Secret:** What do they hide?
> 18. **True Motivation:** What really drives them?

Create Character entities for each ruler.

#### Step 7A.2: Advisors & Court

For major rulers, ask:
> "Who are [Ruler]'s key advisors? For each:"
>
> 1. **Role:** Chancellor | General | Spymaster | Priest | Mage | Other
> 2. **Name**
> 3. **Relationship to Ruler:** Loyal | Opportunist | Manipulator | True Friend
> 4. **Secret Agenda:** What do they really want?
> 5. **One Quirk**

Create Character entities for significant advisors.

#### Step 7A.3: Heirs & Succession

Ask:
> "Are there succession issues? For each major nation:"
>
> 1. **Clear Heir:** Is the succession settled?
> 2. **Heir's Personality:** If there's an heir, what are they like?
> 3. **Rivals:** Anyone else claiming the throne?
> 4. **Dangers:** What threatens the succession?
> 5. **Secret:** Any hidden heirs or pretenders?

---

### Section 7B: Quest-Givers & Allies

#### Step 7B.1: Quest-Giver Types

Ask:
> "What types of NPCs will give adventurers quests? Select 5-10:"
>
> **Authority Figures:**
> 1. **Nobleman/Lady** - Power, resources, political problems
> 2. **Military Commander** - War, defense, tactical needs
> 3. **Religious Leader** - Divine missions, holy tasks
> 4. **Guild Master** - Professional needs, trade problems
> 5. **Mayor/Elder** - Community problems
>
> **Knowledge Seekers:**
> 6. **Scholar/Sage** - Research, lost knowledge
> 7. **Wizard** - Magical needs, component gathering
> 8. **Explorer** - Mapping, discovery
> 9. **Collector** - Acquiring specific items
> 10. **Historian** - Uncovering the past
>
> **Common Folk:**
> 11. **Desperate Merchant** - Goods stolen, routes threatened
> 12. **Grieving Parent** - Missing child, revenge
> 13. **Haunted Survivor** - Something terrible happened
> 14. **Simple Farmer** - Monster problems
> 15. **Worried Spouse** - Partner in danger
>
> **Mysterious Figures:**
> 16. **Mysterious Stranger** - Unknown agenda
> 17. **Dying Oracle** - Prophecy to fulfill
> 18. **Hidden Noble** - Disguised aristocrat
> 19. **Reformed Villain** - Seeking redemption
> 20. **Immortal Being** - Ancient perspective

Store in `decisions.quest_giver_types`.

#### Step 7B.2: Create Quest-Givers

For each type selected, create a specific NPC:
> "Tell me about the [quest-giver type]:"
>
> 1. **Name** (using naming conventions)
> 2. **Location:** Where are they found?
> 3. **Appearance:** 2 sentences
> 4. **Personality:** 3 words
> 5. **Voice/Mannerism:** How do they speak/act?
> 6. **Wants:** What do they need from adventurers?
> 7. **Offers:** What can they provide in return?
> 8. **Secret:** What are they hiding?
> 9. **Connection:** How do they relate to the main conflict?
> 10. **Hook:** What's their opening line or request?

Create Character entities.

---

### Section 7C: Villains & Antagonists

#### Step 7C.1: Main Villain

Ask:
> "Who is the main villain or antagonist of the current conflict?"
>
> **Identity:**
> 1. **Name and Title**
> 2. **Species**
> 3. **Age**
> 4. **Appearance:** What makes them memorable?
>
> **Motivation:**
> 5. **What They Want:** Their stated goal
> 6. **Why They Want It:** What drives them?
> 7. **Origin:** What made them this way?
> 8. **Justification:** How do they see themselves?
> 9. **Tragic Element:** Is there anything sympathetic?
>
> **Threat:**
> 10. **Powers/Abilities:** What makes them dangerous?
> 11. **Resources:** Followers? Wealth? Magic items?
> 12. **Methods:** How do they operate?
> 13. **Base of Operations:** Where are they?
> 14. **Timeline:** What's their plan?
>
> **Weakness:**
> 15. **Fatal Flaw:** What could be their undoing?
> 16. **Blind Spot:** What do they fail to see?
> 17. **Vulnerability:** Physical, emotional, or magical?
> 18. **Redeemable?:** Could they be turned?

Create Antagonist entity.

#### Step 7C.2: Lieutenants

Ask:
> "Who serves the main villain? Create 2-4 lieutenants:"
>
> For each:
> 1. **Name**
> 2. **Role:** Enforcer | Spy | Mage | Priest | General | Assassin
> 3. **Personality:** 3 words
> 4. **Loyalty:** Fanatic | Mercenary | Fearful | Complicated
> 5. **Special Ability:** What makes them dangerous?
> 6. **Weakness:** How might they be defeated or turned?
> 7. **Relationship to Boss:** How do they feel about the villain?

Create Character entities.

#### Step 7C.3: Gray Area Antagonists

Ask:
> "Who opposes the heroes but isn't truly evil? Select any that exist:"
>
> 1. **Rival Adventurers** - Competition for the same goals
> 2. **Misguided Official** - Doing wrong for right reasons
> 3. **Protective Guardian** - Defending something they shouldn't
> 4. **Desperate Criminal** - Breaking laws to survive
> 5. **Zealous Priest** - Religious extremism, not evil gods
> 6. **Territorial Monster** - Protecting home, not malicious
> 7. **Cursed Individual** - Not in control of their actions
> 8. **Manipulated Pawn** - Being used by the real villain
> 9. **Different Faction** - Good people with conflicting goals
> 10. **Past Version** - An ally who became opposed
> 11. **Family Member** - Someone the hero cares about
> 12. **Wronged Party** - They have legitimate grievances

For each, create brief character profiles.

---

### Section 7D: Relationship Mapping

#### Step 7D.1: Power Networks

Ask:
> "How are major NPCs connected? For each relationship pair:"
>
> **Relationship Types:**
> 1. **Allied** - Working together
> 2. **Friendly** - Positive relationship
> 3. **Neutral** - No significant connection
> 4. **Rivals** - Competition
> 5. **Enemies** - Open hostility
> 6. **Family** - Blood or marriage
> 7. **Romance** - Current or past lovers
> 8. **Mentor/Student** - Teaching relationship
> 9. **Master/Servant** - Power imbalance
> 10. **Debtor/Creditor** - One owes the other
> 11. **Blackmail** - Secret leverage
> 12. **Unknown** - One doesn't know about the other

Track relationships in `relationship_map` in state file:
```json
"relationship_map": {
  "NPC1-NPC2": {"type": "rivals", "secret": "former friends", "tension": "high"},
  "NPC1-NPC3": {"type": "family", "secret": "estranged", "tension": "medium"}
}
```

#### Step 7D.2: Faction Goals

For each major faction or organization, track:
> "What does [Faction] want, and how do they pursue it?"
>
> 1. **Public Goal:** What they claim to want
> 2. **Secret Goal:** What they really want
> 3. **Current Action:** What are they doing now?
> 4. **Resources:** What do they have?
> 5. **Obstacles:** What blocks them?
> 6. **Timeline:** When do they act?

Store in `faction_goals` in state file.

#### Step 7D.3: Secret Connections

Ask:
> "What secret relationships exist that could be revealed?"
>
> For each secret:
> 1. **Who Knows:** Which NPCs are involved?
> 2. **The Secret:** What's hidden?
> 3. **Evidence:** How could it be discovered?
> 4. **Consequences:** What happens if revealed?
> 5. **Who Benefits:** Who gains from revelation?
> 6. **Who Suffers:** Who's harmed?

---

### Section 7E: Common Folk

#### Step 7E.1: Background Characters

Ask:
> "What types of common folk provide flavor and information? For your main city, create 5-10:"
>
> Types to consider:
> 1. **Town Crier** - News and rumors
> 2. **Street Vendor** - Local color
> 3. **Beggar** - Sees everything, knows secrets
> 4. **Guard** - Law and order perspective
> 5. **Servant** - Knows their employer's secrets
> 6. **Craftsperson** - Specific trade knowledge
> 7. **Entertainer** - Bard, musician, performer
> 8. **Child/Urchin** - Innocent perspective, sneaky
> 9. **Drunk** - Loose lips
> 10. **Foreigner** - Outside perspective
> 11. **Old Timer** - Historical knowledge
> 12. **Gossip** - Knows everyone's business

For each:
> 1. **Name**
> 2. **Appearance:** One sentence
> 3. **Personality:** 2 words
> 4. **What They Know**
> 5. **What They Want**
> 6. **Quirk or Catchphrase**

Create Background Character entities.

#### Step 7E.2: Recurring NPCs

Ask:
> "Which background characters might become important? Select 2-3 to develop further:"
>
> Provide full character development for selected NPCs.

---

### Phase 7 Summary

Display progress and relationship web:
```
╔══════════════════════════════════════════════════════════════╗
║           WORLDBUILDING PROGRESS: [World Name]               ║
╠══════════════════════════════════════════════════════════════╣
║ Phase 1-6: [COMPLETE]                                        ║
║ Phase 7: Characters            [COMPLETE]                    ║
║ Phase 8: Society & Daily Life  [NOT STARTED]                 ║
║ Phase 9: Campaign Setup        [NOT STARTED]                 ║
╠══════════════════════════════════════════════════════════════╣
║ Characters Created: X                                        ║
║ - Rulers: [list]                                             ║
║ - Villains: [main villain] + [lieutenants]                   ║
║ - Quest-Givers: [list]                                       ║
║ - Supporting: [list]                                         ║
╠══════════════════════════════════════════════════════════════╣
║ RELATIONSHIP WEB:                                            ║
║ [Ruler A] ←rivals→ [Ruler B]                                ║
║ [Villain] ←serves→ [Hidden Master]                           ║
║ [Quest-Giver] ←loves→ [NPC] ←hates→ [Villain]               ║
║ (Use 'relationships' command for full map)                   ║
╠══════════════════════════════════════════════════════════════╣
║ Commands: continue | relationships | factions | summary      ║
╚══════════════════════════════════════════════════════════════╝

Ready to continue to Phase 8: Society & Daily Life?
```

---

## Phase 8: Society & Daily Life

**Goal:** Add cultural depth—customs, festivals, arts, daily routines, and the texture of lived experience.

### Section 8A: Time & Calendar

#### Step 8A.1: Calendar System

Ask:
> "How is time measured in this world?"
>
> 1. **Standard Year** - 12 months, 365 days (like Earth)
> 2. **Lunar Calendar** - Based on moon cycles
> 3. **Multiple Moons** - Complex lunar calendar
> 4. **Seasonal Calendar** - Divided by seasons, not months
> 5. **Religious Calendar** - Based on holy days
> 6. **Reign-Based** - Years of current ruler's reign
> 7. **Era-Based** - Counted from major events
> 8. **Unique System** - Different number of days/months
> 9. **Regional Variation** - Different cultures count differently
> 10. **Lost/Unknown** - No standard calendar exists

Store in `decisions.calendar_type`.

#### Step 8A.2: Month Names

If using months:
> "What are the months called? (I'll suggest names based on [naming_culture]):"
>
> For each month:
> 1. **Name** (using cultural conventions)
> 2. **Season**
> 3. **Associated With** (deity, harvest, weather, etc.)
> 4. **Major Holiday** (if any)

Create Calendar entity.

#### Step 8A.3: Days & Hours

Ask:
> "How are days organized?"
>
> 1. **24-Hour Day** - Standard Earth time
> 2. **Different Hour Count** - More or fewer hours
> 3. **Named Hours** - Each hour has a name
> 4. **Watches** - Divided into watches (military/naval)
> 5. **Prayer Times** - Divided by religious observance
> 6. **Sun-Based** - Marked by sun position only
> 7. **Variable Days** - Day length varies significantly

---

### Section 8B: Festivals & Holy Days

#### Step 8B.1: Major Festivals

Ask:
> "What major festivals does [Culture/Nation] celebrate? Select or create 4-8:"
>
> **Seasonal:**
> 1. **Spring Festival** - New beginnings, planting, fertility
> 2. **Summer Solstice** - Height of the sun, celebration
> 3. **Harvest Festival** - Gratitude for crops, plenty
> 4. **Winter Solstice** - Darkest day, light returning
> 5. **Equinox Celebrations** - Balance of light and dark
>
> **Religious:**
> 6. **Deity's Day** - Major god's celebration
> 7. **Remembrance Day** - Honoring the dead
> 8. **Founding Day** - Religion's origin
> 9. **Miracle Anniversary** - Commemorating divine event
> 10. **Pilgrimage Season** - Time to visit holy sites
>
> **Secular:**
> 11. **National Day** - Kingdom's founding
> 12. **Victory Day** - Commemorating a battle
> 13. **Market Fair** - Major trading event
> 14. **Tournament** - Martial competition
> 15. **Coronation Anniversary** - Ruler's celebration
>
> **Cultural:**
> 16. **Coming of Age** - Adulthood ceremonies
> 17. **Lovers' Day** - Romance and partnerships
> 18. **Fools' Festival** - Rules reversed, chaos allowed
> 19. **Light Festival** - Candles, lanterns, fire
> 20. **Night of the Dead** - Ancestors honored, spirits close

For each festival:
> 1. **Name** (using naming conventions)
> 2. **Date** (month/season)
> 3. **Duration** (1 day, 3 days, a week)
> 4. **Activities** (what do people do?)
> 5. **Traditions** (specific customs)
> 6. **Food & Drink** (special treats)
> 7. **Meaning** (what does it commemorate?)
> 8. **Adventure Hook** (what could go wrong?)

---

### Section 8C: Daily Life

#### Step 8C.1: Common Occupations

Ask:
> "What do ordinary people do for a living?"
>
> **Agriculture (if applicable):**
> 1. **Farmers** - Grain, vegetables
> 2. **Herders** - Cattle, sheep, goats
> 3. **Fishermen** - Coastal/river communities
> 4. **Hunters** - Wild game, furs
> 5. **Foresters** - Timber, gathering
>
> **Crafts:**
> 6. **Smiths** - Metal workers
> 7. **Weavers** - Cloth production
> 8. **Potters** - Ceramics
> 9. **Carpenters** - Woodworking
> 10. **Tanners** - Leather working
> 11. **Brewers** - Beer, ale production
>
> **Services:**
> 12. **Merchants** - Trade and commerce
> 13. **Servants** - Domestic labor
> 14. **Innkeepers** - Hospitality
> 15. **Healers** - Medical care
> 16. **Scribes** - Writing, records
>
> **Other:**
> 17. **Soldiers** - Military service
> 18. **Sailors** - Maritime work
> 19. **Miners** - Extraction
> 20. **Entertainers** - Performance

#### Step 8C.2: Daily Routines

Ask:
> "What does a typical day look like for common folk?"
>
> 1. **Wake Time:** When do people rise?
> 2. **Meals:** How many? When? What?
> 3. **Work Hours:** How long? How hard?
> 4. **Leisure:** What free time exists?
> 5. **Evening:** What happens after work?
> 6. **Sleep:** When? Where? With whom?
> 7. **Weekly Rhythm:** Rest days? Market days?

Store in `decisions.daily_life`.

#### Step 8C.3: Food & Drink

Ask:
> "What do people eat and drink?"
>
> **Staples:**
> 1. **Grain:** Wheat, barley, rice, corn?
> 2. **Protein:** Meat, fish, legumes?
> 3. **Vegetables:** What grows here?
> 4. **Preservation:** Salted, dried, smoked, pickled?
>
> **Special Foods:**
> 5. **Nobility Eats:** Rich foods, imports
> 6. **Poor Eat:** Simple fare, scraps
> 7. **Festival Food:** Celebratory dishes
> 8. **Travel Rations:** What adventurers carry
>
> **Drinks:**
> 9. **Common Drink:** Water, small beer, tea?
> 10. **Alcohol:** What's brewed locally?
> 11. **Luxury Drinks:** Wine, spirits, imports
> 12. **Magical Drinks:** Potions, enchanted beverages

Create Food/Drink entities for notable items.

---

### Section 8D: Customs & Etiquette

#### Step 8D.1: Greetings & Forms of Address

Ask:
> "How do people greet each other and show respect?"
>
> 1. **Common Greeting:** How do equals meet?
> 2. **Formal Greeting:** How do people address superiors?
> 3. **Titles:** What honorifics are used?
> 4. **Physical Contact:** Handshakes? Bows? Kisses?
> 5. **Gender Differences:** Do men and women greet differently?
> 6. **Species Differences:** Do different species have different customs?
> 7. **Taboos:** What's rude or offensive?
> 8. **Regional Variation:** Do different areas differ?

Store in `decisions.greetings`.

#### Step 8D.2: Hospitality

Ask:
> "What are the rules of hospitality?"
>
> 1. **Guest Rights:** What protection do guests receive?
> 2. **Host Obligations:** What must a host provide?
> 3. **Duration:** How long can a guest stay?
> 4. **Gift-Giving:** What's expected?
> 5. **Taboos:** What violates hospitality?
> 6. **Sacred Hospitality:** Is it religiously enforced?
> 7. **Enemy as Guest:** What if you host an enemy?
> 8. **Breaking Hospitality:** What are the consequences?

#### Step 8D.3: Honor & Reputation

Ask:
> "How does honor and reputation work?"
>
> 1. **What Gives Honor:** Deeds, birth, wealth, piety?
> 2. **What Loses Honor:** Cowardice, lies, other?
> 3. **Insults:** What's considered an insult?
> 4. **Dueling:** Is it legal? Common?
> 5. **Vendettas:** Do families carry grudges?
> 6. **Redemption:** Can lost honor be regained?
> 7. **Outlaws:** What happens to the dishonorable?
> 8. **Gender & Honor:** Are standards different?

---

### Section 8E: Life Passages

#### Step 8E.1: Birth & Naming

Ask:
> "What customs surround birth and naming?"
>
> 1. **Birth Customs:** What happens when a child is born?
> 2. **Naming Time:** When is a child named?
> 3. **Name Givers:** Who chooses the name?
> 4. **Name Sources:** Where do names come from?
> 5. **Blessing:** Is there a religious ceremony?
> 6. **Protection:** Charms, rituals against evil?
> 7. **Recording:** How are births recorded?
> 8. **Illegitimacy:** How are bastards treated?

#### Step 8E.2: Coming of Age

Ask:
> "How do children become adults?"
>
> 1. **Age:** When does adulthood begin?
> 2. **Ceremony:** Is there a ritual?
> 3. **Tests:** Must they prove themselves?
> 4. **Rights Gained:** What can adults do?
> 5. **Responsibilities:** What must adults do?
> 6. **Gender Differences:** Different for boys and girls?
> 7. **Species Differences:** Different for non-humans?
> 8. **Class Differences:** Different for nobles vs. commoners?

#### Step 8E.3: Marriage & Family

Ask:
> "What customs surround marriage?"
>
> 1. **Marriage Types:** Monogamy, polygamy, other?
> 2. **Arranged vs. Choice:** Who decides?
> 3. **Dowry/Bride Price:** Are payments involved?
> 4. **Ceremony:** What's the wedding like?
> 5. **Religious Role:** Is marriage sacred?
> 6. **Divorce:** Is it possible? How?
> 7. **Same-Sex Unions:** Are they recognized?
> 8. **Inter-Species Marriage:** Is it accepted?
> 9. **Children:** How are they raised?
> 10. **Inheritance:** Who inherits? How?

#### Step 8E.4: Death & Mourning

Ask:
> "What customs surround death?"
>
> 1. **Body Treatment:** Burial, cremation, other?
> 2. **Funeral Rites:** What happens at funerals?
> 3. **Mourning Period:** How long? What restrictions?
> 4. **Mourning Dress:** Special clothing?
> 5. **Afterlife Prep:** Grave goods, rituals?
> 6. **Remembrance:** How are dead honored?
> 7. **Necromancy Issues:** What about undead?
> 8. **Murder/Suicide:** Special treatment?
> 9. **War Dead:** Different customs for soldiers?
> 10. **Ancestor Worship:** Ongoing relationship with dead?

---

### Section 8F: Arts & Entertainment

#### Step 8F.1: Music & Performance

Ask:
> "What arts exist in this world?"
>
> **Music:**
> 1. **Common Instruments** (drums, flutes, strings?)
> 2. **Musical Styles** (folk, court, religious?)
> 3. **Famous Songs** (anthems, ballads, drinking songs)
> 4. **Bardic Traditions** (storytelling, magic?)
>
> **Performance:**
> 5. **Theater** (does it exist? What forms?)
> 6. **Dance** (what styles? When performed?)
> 7. **Storytelling** (oral tradition important?)
> 8. **Acrobatics/Circus** (traveling performers?)
>
> **Games:**
> 9. **Board Games** (chess-like, dice games?)
> 10. **Card Games** (gambling? Fortune-telling?)
> 11. **Sports** (team games, individual competitions?)
> 12. **Blood Sports** (gladiatorial combat? Animal fights?)

#### Step 8F.2: Visual Arts

Ask:
> "What visual arts are valued?"
>
> 1. **Painting** (frescos, portraits, religious art?)
> 2. **Sculpture** (stone, metal, styles?)
> 3. **Architecture** (styles, famous buildings?)
> 4. **Textile Arts** (tapestry, embroidery?)
> 5. **Jewelry** (styles, meanings?)
> 6. **Magic in Art** (enchanted art? Moving paintings?)
> 7. **Forbidden Art** (what's taboo to depict?)
> 8. **Artists' Status** (respected? Distrusted?)

---

### Section 8G: Common Sayings & Superstitions

#### Step 8G.1: Proverbs & Sayings

Ask:
> "What sayings and proverbs do people use? Generate 5-10 based on world details:"
>
> Examples (adapt to world):
> - "[God's name] willing" - Religious invocation
> - "Like [local danger] at the door" - Imminent threat
> - "Worth a [currency name]" - Value comparison
> - "[Historical event] repeating" - Warning of cycles
> - "[Species] promise" - Reference to species stereotype

Generate sayings that reflect world culture.

#### Step 8G.2: Superstitions

Ask:
> "What superstitions exist? Select or create:"
>
> 1. **Lucky Things** (colors, numbers, items?)
> 2. **Unlucky Things** (actions to avoid?)
> 3. **Protective Charms** (what keeps evil away?)
> 4. **Weather Signs** (how do people predict weather?)
> 5. **Death Omens** (what predicts death?)
> 6. **Fey/Spirit Rules** (what invites supernatural trouble?)
> 7. **Magic Fears** (what do non-mages fear about magic?)
> 8. **True Superstitions** (which ones are actually real?)

---

### Phase 8 Summary

Display progress:
```
╔══════════════════════════════════════════════════════════════╗
║           WORLDBUILDING PROGRESS: [World Name]               ║
╠══════════════════════════════════════════════════════════════╣
║ Phase 1-7: [COMPLETE]                                        ║
║ Phase 8: Society & Daily Life  [COMPLETE]                    ║
║ Phase 9: Campaign Setup        [NOT STARTED]                 ║
╠══════════════════════════════════════════════════════════════╣
║ Cultural Elements Created:                                   ║
║ - Calendar with [X] months and [Y] festivals                ║
║ - Food & Drink: [notable items]                              ║
║ - Customs: greetings, hospitality, life passages            ║
║ - Arts: music, performance, games                            ║
║ - Sayings and superstitions                                  ║
╠══════════════════════════════════════════════════════════════╣
║ Key Decisions:                                               ║
║ - Calendar: [type]                                           ║
║ - Major Festivals: [list]                                    ║
║ - Marriage: [type]                                           ║
║ - Death Customs: [burial type]                               ║
╠══════════════════════════════════════════════════════════════╣
║ Commands: continue | back | skip | pause | summary           ║
╚══════════════════════════════════════════════════════════════╝

Ready to continue to Phase 9: Campaign Setup?
```

---

## Phase 9: Campaign & Adventure Setup

**Goal:** Prepare for actual play—starting scenarios, campaign arcs, session zero guidance, and adventure hooks.

### Section 9A: Campaign Framework

#### Step 9A.1: Campaign Type

Ask:
> "What type of campaign are you planning?"
>
> 1. **Open World/Sandbox** - Players choose their own direction
> 2. **Adventure Path** - Structured story with milestones
> 3. **Episodic** - Self-contained adventures loosely connected
> 4. **Mystery** - Central mystery to unravel
> 5. **War Campaign** - Large-scale conflict focus
> 6. **Political Intrigue** - Schemes and machinations
> 7. **Exploration** - Discovering new lands
> 8. **Survival** - Harsh conditions, resource management
> 9. **Heist/Caper** - Complex plans and execution
> 10. **Monster Hunters** - Tracking and slaying creatures
> 11. **Guild Campaign** - Faction-based advancement
> 12. **Kingdom Building** - Establishing and ruling territory
> 13. **Planar Travel** - Journeying to other worlds
> 14. **Mixed** - Combination of types
> 15. **Player-Directed** - Determined by player choices

Store in `decisions.campaign_type`.

#### Step 9A.2: Level Range

Ask:
> "What level range is this campaign designed for?"
>
> 1. **Levels 1-5** - Local heroes, village problems
> 2. **Levels 1-10** - Regional heroes, kingdom threats
> 3. **Levels 1-15** - National heroes, continental threats
> 4. **Levels 1-20** - World heroes, planar threats
> 5. **Levels 5-15** - Start experienced, avoid early slog
> 6. **Levels 10-20** - High power, epic threats
> 7. **Tier 1 Only (1-4)** - Short, focused campaign
> 8. **Tier 2 Focus (5-10)** - Sweet spot of play
> 9. **Tier 3 Focus (11-16)** - High fantasy
> 10. **Tier 4 Focus (17-20)** - Legendary power
> 11. **No Levels** - Milestone or narrative advancement
> 12. **Undecided** - Let it develop naturally

Store in `decisions.level_range`.

#### Step 9A.3: Campaign Length

Ask:
> "How long do you expect this campaign to run?"
>
> 1. **One-Shot** - Single session
> 2. **Mini-Campaign** - 3-6 sessions
> 3. **Short Campaign** - 10-20 sessions
> 4. **Standard Campaign** - 20-50 sessions
> 5. **Long Campaign** - 50-100 sessions
> 6. **Indefinite** - Ongoing until natural end
> 7. **Modular** - Multiple short arcs
> 8. **Unknown** - See how it develops

Store in `decisions.campaign_length`.

---

### Section 9B: Starting Scenario

#### Step 9B.1: Starting Location

Ask:
> "Where does the campaign begin?"
>
> 1. **Major City** - Urban adventure hub
> 2. **Small Town** - Classic starting point
> 3. **Village** - Humble beginnings
> 4. **Frontier Settlement** - Edge of civilization
> 5. **Tavern** - Classic "you meet in a tavern"
> 6. **Prison** - Start captured, need to escape
> 7. **Caravan/Ship** - Already traveling
> 8. **Ruins** - Start in media res
> 9. **Noble Estate** - Start with connections
> 10. **Temple/Church** - Religious beginning
> 11. **Wilderness** - Start lost or stranded
> 12. **Unique Location** - [Specify based on world]

Store in `decisions.starting_location`.

#### Step 9B.2: Party Origin

Ask:
> "How do the player characters know each other?"
>
> 1. **Strangers Meeting** - Classic cold open
> 2. **Already Friends** - Established relationships
> 3. **Same Organization** - Guild, military, church
> 4. **Same Background** - Shared origin
> 5. **Family/Clan** - Blood or adopted ties
> 6. **Former Adventurers** - Reuniting after time apart
> 7. **Hired Together** - Same employer
> 8. **Prisoners Together** - Shared captivity
> 9. **Survivors Together** - Shared disaster
> 10. **Destiny/Prophecy** - Fated to meet
> 11. **Mixed** - Some know each other, some don't
> 12. **Player Choice** - Let players decide

Store in `decisions.party_origin`.

#### Step 9B.3: Opening Hook

Ask:
> "What draws the party into adventure?"
>
> 1. **Job Offer** - Someone hires them
> 2. **Call for Help** - Someone needs rescue
> 3. **Attack** - Violence comes to them
> 4. **Mystery** - Something strange happens
> 5. **Rumor** - They hear about opportunity
> 6. **Obligation** - Duty calls
> 7. **Survival** - They must act to live
> 8. **Competition** - Race against rivals
> 9. **Discovery** - They find something important
> 10. **Revenge** - Personal stakes drive action
> 11. **Prophecy** - They're named in prediction
> 12. **Coincidence** - Wrong place, right time
> 13. **Curiosity** - Something intriguing appears
> 14. **Desperation** - No other options
> 15. **Player-Generated** - Let players create stakes

Store in `decisions.opening_hook`.

#### Step 9B.4: First Adventure

Ask:
> "What's the first adventure or mission?"
>
> 1. **Dungeon Crawl** - Explore dangerous site
> 2. **Monster Hunt** - Track and slay creature
> 3. **Rescue Mission** - Save someone
> 4. **Investigation** - Solve a mystery
> 5. **Escort Mission** - Protect traveler(s)
> 6. **Heist** - Steal something
> 7. **Defense** - Protect a location
> 8. **Delivery** - Transport something important
> 9. **Exploration** - Map unknown area
> 10. **Negotiation** - Diplomatic mission
> 11. **Sabotage** - Destroy enemy resources
> 12. **Competition** - Win a contest
> 13. **Survival** - Escape danger
> 14. **Recovery** - Find lost item/person
> 15. **Revolution** - Overthrow local power

Detail the first adventure:
> 1. **Goal:** What must they accomplish?
> 2. **Location:** Where does it take place?
> 3. **Opposition:** Who/what stands in their way?
> 4. **Complication:** What makes it harder?
> 5. **Reward:** What do they gain?
> 6. **Connection:** How does it tie to larger story?

---

### Section 9C: Campaign Arcs

#### Step 9C.1: Major Story Arc

Ask:
> "What's the overarching campaign story?"
>
> 1. **Defeat Great Evil** - Classic heroic arc
> 2. **Save the World** - Prevent catastrophe
> 3. **Uncover Truth** - Reveal hidden conspiracy
> 4. **Unite the Realm** - Bring peace to warring factions
> 5. **Find the MacGuffin** - Quest for powerful item
> 6. **Fulfill Prophecy** - Complete destined task
> 7. **Build an Empire** - Establish power
> 8. **Survive Apocalypse** - Live through disaster
> 9. **Escape Trap** - Get out of bad situation
> 10. **Revenge Quest** - Hunt those responsible
> 11. **Coming of Age** - Characters grow into heroes
> 12. **Redemption** - Atone for past wrongs
> 13. **Exploration** - Map the unknown
> 14. **No Arc** - Emergent from play
> 15. **Player-Driven** - Their goals become arc

Store in `decisions.main_arc`.

#### Step 9C.2: Arc Structure

Ask:
> "How is the main arc structured?"
>
> 1. **Three Acts** - Setup, Confrontation, Resolution
> 2. **Five Acts** - Rising action, climaxes, denouement
> 3. **Quest Chain** - Linked objectives
> 4. **Mystery Layers** - Peeling back truth
> 5. **Faction War** - Shifting allegiances
> 6. **Countdown** - Racing against time
> 7. **Hero's Journey** - Classic mythic structure
> 8. **Episodic** - Self-contained adventures building
> 9. **Sandbox** - Emergent from player choice
> 10. **Mixed** - Different structures at different times

#### Step 9C.3: Key Milestones

Ask:
> "What are the major milestones in this campaign?"
>
> For a typical campaign, define 4-6 major turning points:
>
> **Act 1 (Levels 1-5):**
> 1. **Inciting Incident:** What launches the story?
> 2. **First Victory:** What early success proves their worth?
> 3. **First Setback:** What early failure raises stakes?
>
> **Act 2 (Levels 6-12):**
> 4. **Midpoint Revelation:** What changes everything?
> 5. **Dark Night:** What brings them lowest?
> 6. **Rallying Point:** What gives them hope?
>
> **Act 3 (Levels 13-20):**
> 7. **Final Challenge:** What ultimate test awaits?
> 8. **Climax:** How does it end?
> 9. **Resolution:** What's the aftermath?

Store in `decisions.milestones`.

---

### Section 9D: Player Integration

#### Step 9D.1: Character Hooks

Ask:
> "What hooks exist for player character backgrounds?"
>
> For each player type/background, provide connections:
>
> 1. **The Warrior** - Military conflicts, enemies, old commanders
> 2. **The Rogue** - Criminal contacts, marks, past heists
> 3. **The Scholar** - Lost knowledge, academic rivals, research
> 4. **The Faithful** - Temple politics, divine visions, heresy
> 5. **The Noble** - Family intrigue, inheritance, obligations
> 6. **The Orphan** - Missing parents, found family, origin mystery
> 7. **The Foreigner** - Cultural clash, homeland threats, ambassadors
> 8. **The Monster** - Prejudice, acceptance, nature vs. nurture
> 9. **The Chosen** - Prophecy, destiny, burden of fate
> 10. **The Refugee** - Lost home, revenge, rebuilding

For each:
> 1. **NPC Connection:** Who do they know?
> 2. **Location Tie:** Where have they been?
> 3. **Historical Link:** What past events affected them?
> 4. **Organization Tie:** What groups matter to them?
> 5. **Personal Quest:** What do they want?

#### Step 9D.2: Session Zero Guide

Ask:
> "What should be covered in Session Zero?"
>
> Generate a Session Zero checklist:
>
> **World Introduction:**
> - World premise and hook
> - Tone and themes
> - Content boundaries
> - Starting location
>
> **Character Creation:**
> - Allowed species/classes
> - Backstory requirements
> - Party composition
> - Connections between characters
>
> **Table Rules:**
> - Scheduling expectations
> - Communication preferences
> - PvP and inter-party conflict
> - Character death handling
>
> **Campaign Expectations:**
> - Combat vs. roleplay balance
> - Exploration vs. narrative
> - Player agency level
> - Homebrew rules (if any)

---

### Section 9E: Adventure Hooks

#### Step 9E.1: Generate Adventure Hooks

Based on all world-building decisions, generate 20+ adventure hooks:
> "Here are adventure hooks based on your world:"
>
> **From Current Conflict:**
> 1. [Hook tied to central conflict]
> 2. [Hook tied to ticking clocks]
> 3. [Hook tied to faction goals]
>
> **From History:**
> 4. [Hook tied to historical mystery]
> 5. [Hook tied to ancient event]
> 6. [Hook tied to prophecy]
>
> **From Geography:**
> 7. [Hook tied to dangerous area]
> 8. [Hook tied to dungeon/ruin]
> 9. [Hook tied to travel route]
>
> **From Characters:**
> 10. [Hook from quest-giver]
> 11. [Hook from villain activity]
> 12. [Hook from NPC relationship]
>
> **From Organizations:**
> 13. [Hook from guild/faction]
> 14. [Hook from religious order]
> 15. [Hook from criminal element]
>
> **From Society:**
> 16. [Hook from festival/holiday]
> 17. [Hook from cultural conflict]
> 18. [Hook from superstition/belief]
>
> **Random Encounters:**
> 19. [Wilderness encounter seed]
> 20. [Urban encounter seed]

Store hooks in World Overview or separate document.

#### Step 9E.2: Random Encounter Tables

Ask:
> "Would you like me to generate random encounter tables for each region?"
>
> For each region, generate:
> - Travel encounters (d12 or d20 table)
> - Urban encounters (if settlement exists)
> - Dungeon encounters (for adventure sites)
>
> Include mix of:
> - Combat encounters
> - Social encounters
> - Environmental hazards
> - Discovery opportunities
> - Plot-relevant events

---

### Section 9F: Quick Reference

#### Step 9F.1: Generate DM Reference Sheet

Create a quick reference document:
> "Generating DM Quick Reference for [World Name]..."
>
> **World at a Glance:**
> - Hook: [one sentence]
> - Tone: [tone]
> - Current Conflict: [conflict]
> - Ticking Clock: [urgency]
>
> **Key NPCs:**
> - [Ruler 1]: [2 words] - [location]
> - [Villain]: [2 words] - [goal]
> - [Quest-Giver 1]: [2 words] - [location]
>
> **Key Locations:**
> - [Starting City]: [key feature]
> - [Danger Zone]: [threat]
> - [Dungeon 1]: [hook]
>
> **Key Factions:**
> - [Faction 1]: [goal] - [current action]
> - [Faction 2]: [goal] - [current action]
>
> **Common Knowledge:**
> - [What everyone knows 1]
> - [What everyone knows 2]
> - [What everyone knows 3]
>
> **Rumors (True/False):**
> - [Rumor 1] - [T/F]
> - [Rumor 2] - [T/F]
> - [Rumor 3] - [T/F]

Save to `Worlds/[World Name]/DM Quick Reference.md`

---

### Phase 9 Summary & Completion

Display final progress:
```
╔══════════════════════════════════════════════════════════════╗
║        WORLDBUILDING COMPLETE: [World Name]                  ║
╠══════════════════════════════════════════════════════════════╣
║ All 9 Phases Complete!                                       ║
╠══════════════════════════════════════════════════════════════╣
║ ENTITY COUNT:                                                ║
║ - World Overview: 1                                          ║
║ - Concepts: [X] (Magic, Pantheon, Deities, Calendar, etc.)  ║
║ - Geography: [X] (Continent, Regions, Features)              ║
║ - Organizations: [X] (Governments, Guilds, etc.)             ║
║ - Settlements: [X] (Cities, Towns, Villages, Buildings)      ║
║ - Characters: [X] (Rulers, NPCs, Villains)                   ║
║ - History: [X] (Ages, Events, Prophecies)                    ║
║ - Adventure Sites: [X] (Dungeons, Ruins, Lairs)              ║
║ - Items: [X] (if any)                                        ║
║ - Creatures: [X] (if any)                                    ║
║ ─────────────────────────────────────────────────────────────║
║ TOTAL: [X] entities                                          ║
╠══════════════════════════════════════════════════════════════╣
║ WORLD READY FOR:                                             ║
║ ✓ Campaign: [type] for levels [range]                        ║
║ ✓ Starting Location: [location]                              ║
║ ✓ First Adventure: [hook]                                    ║
║ ✓ Session Zero materials available                           ║
║ ✓ [X] adventure hooks generated                              ║
╠══════════════════════════════════════════════════════════════╣
║ NEXT STEPS:                                                  ║
║ 1. Run /session-prep for game night preparation              ║
║ 2. Use /create-entity to add more content                    ║
║ 3. Use /expand-entity to detail existing entities            ║
║ 4. Use /generate-image for visual content                    ║
║ 5. Use /audit-world to check consistency                     ║
╠══════════════════════════════════════════════════════════════╣
║ FILES CREATED:                                               ║
║ Location: Worlds/[World Name]/                               ║
║ State: .worldbuild-state.json (for future resume)            ║
║ Reference: DM Quick Reference.md                             ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Resumption Logic

When user invokes `/worldbuild resume` or `/worldbuild [existing world name]`:

1. **Check for state file:**
   Look for `Worlds/[World Name]/.worldbuild-state.json`

2. **If found, display:**
   ```
   ╔══════════════════════════════════════════════════════════════╗
   ║           RESUMING: [World Name]                             ║
   ╠══════════════════════════════════════════════════════════════╣
   ║ Last Session: Phase [X], Section [Y]                        ║
   ║ Last Question: "[question text]"                            ║
   ║ Entities Created: [count]                                   ║
   ║ Session Started: [date]                                     ║
   ║ Last Updated: [date]                                        ║
   ╠══════════════════════════════════════════════════════════════╣
   ║ OPTIONS:                                                    ║
   ║ 1. Continue where you left off                              ║
   ║ 2. Jump to beginning of Phase [X]                           ║
   ║ 3. Jump to a specific phase (1-9)                           ║
   ║ 4. Review completed phases                                  ║
   ║ 5. Show all created entities                                ║
   ║ 6. Show relationship map                                    ║
   ║ 7. Start completely fresh                                   ║
   ╚══════════════════════════════════════════════════════════════╝
   ```

3. **Load all decisions** and continue from stored position.

4. **Preserve context:** All previous decisions remain available for reference.

---

## Adaptive Skip Logic

Track in state and automatically skip irrelevant sections:

| If user chose... | Skip or Modify... |
|------------------|-------------------|
| No magic | Magic System, Mage Academy, magical costs, potion shops |
| Gods don't exist | Pantheon, Deities, Temples, Religious Orders, divine afterlife |
| Humans only | Species creation, inter-species relations, species-specific customs |
| Single city scope | Continents, regions, extensive geography |
| Low fantasy tone | High magic, direct divine intervention, planar travel |
| Grimdark tone | Comedic elements, fairy tale aspects |
| Short campaign | Extensive faction development, complex arcs |
| Sandbox campaign | Detailed arc structure, milestone planning |

Always inform user when skipping:
> "Since you indicated [reason], I'll skip [section]. Say 'wait' if you want to cover this anyway."

---

## Entity Creation Standards

When generating any entity:

1. **Read the template first** from `Templates/[Category]/[Type].md`
2. **Apply naming conventions** from `decisions.naming_culture`
3. **Use all stored decisions** for consistency
4. **Fill ALL sections** completely—no placeholders
5. **Create wikilinks** to all related entities
6. **Generate image prompts** specific to the entity
7. **Match the tone** from Phase 1 decisions
8. **Show preview** and wait for user approval
9. **Offer modifications** before saving
10. **Update relationship map** if character
11. **Update faction goals** if organization
12. **Ensure bidirectional links** - if A links to B, B links to A

---

## Progress Dashboard Format

After each completed phase or on `summary` command:

```
╔══════════════════════════════════════════════════════════════╗
║           WORLDBUILDING PROGRESS: [World Name]               ║
╠══════════════════════════════════════════════════════════════╣
║ Phase 1: World Identity        [COMPLETE]                    ║
║ Phase 2: Metaphysical          [COMPLETE]                    ║
║ Phase 3: The Land              [COMPLETE]                    ║
║ Phase 4: Powers & People       [IN PROGRESS - 4C.2]          ║
║ Phase 5: History & Conflict    [NOT STARTED]                 ║
║ Phase 6: Places of Interest    [NOT STARTED]                 ║
║ Phase 7: Characters            [NOT STARTED]                 ║
║ Phase 8: Society & Daily Life  [NOT STARTED]                 ║
║ Phase 9: Campaign Setup        [NOT STARTED]                 ║
╠══════════════════════════════════════════════════════════════╣
║ Entities Created: [count]                                    ║
║ - [Category]: [list]                                         ║
╠══════════════════════════════════════════════════════════════╣
║ Key Decisions:                                               ║
║ - Naming Culture: [culture]                                  ║
║ - Tone: [tone]                                               ║
║ - Magic: [level]                                             ║
║ - Gods: [structure]                                          ║
╠══════════════════════════════════════════════════════════════╣
║ Commands: continue | back | skip | pause | summary | review  ║
║           relationships | factions | hooks                    ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Template Reference

All templates used in worldbuilding:

| Category | Templates |
|----------|-----------|
| **Concepts** | Pantheon, Deity, Magic System, Calendar, Currency, Language, Prophecy, Plane of Existence, Religion, Technology |
| **Geography** | Continent, Region, Mountain Range, Forest, River, Desert, Tundra, Plains, Hills, Steppes, Ocean, Lake, Coast, Pass, Island, Cave, Dungeon, Road |
| **Organizations** | Government, Guild, Religious Order, Cult, Military, Criminal Organization, Business, Academy, Organization (General) |
| **Settlements** | City, Town, Village, Stronghold, Tavern, Shop, Temple, Library |
| **Characters** | Protagonist, Antagonist, Support Character, Background Character, Divine Servant, Familiar |
| **History** | Age, Event, War, Battle, Treaty, Trade Agreement, Tragedy, Dynasty, Adventure |
| **Creatures** | Monster, Animal, Insect, Species, Plant |
| **Items** | Weapon, Armor, Wondrous Magic Item, Artifact, Potion, Gear, Food, Drink, Container, Vehicle, Book |
