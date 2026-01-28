---
name: session-prep
description: Prepare materials for a D&D game session. Generates session notes, NPC cheat sheets, encounter summaries, and location briefs from world entities. Use when DM wants to "prep for session", "prepare for game night", or "create session notes".
argument-hint: "[world] [location or adventure focus]"
---

# Session Prep

Prepare session: $ARGUMENTS

## Overview

Creates DM-ready materials for running a game session by:
1. Compiling relevant world information into quick-reference format
2. Generating NPC cheat sheets with personality and stat summaries
3. Creating location briefs with key details
4. Suggesting encounters appropriate to the area
5. Preparing plot hooks and contingencies

## Instructions

### Step 1: Gather Context

Parse arguments for:
- **World name** - Required
- **Session focus** - Location, adventure, or narrative arc
- **Party level** - For encounter scaling

Ask clarifying questions:
> "To prepare your session, I need to know:
> 1. What world are we working with?
> 2. Where will the session take place? (location/region)
> 3. What's the party's average level?
> 4. Any specific plot threads to advance?"

### Step 2: Read Relevant Entities

Based on session focus, read:
- **Location entities** - Settlement, dungeon, region
- **NPC entities** - Characters likely to appear
- **Organization entities** - Active factions
- **Current plot entities** - Adventures, prophecies, conflicts

### Step 3: Generate Session Notes Document

Create a comprehensive but scannable prep document:

```markdown
# Session Prep: [Session Title/Location]
**World:** [[World Name]]
**Date:** [Prep date]
**Party Level:** [X]
**Estimated Duration:** [X hours]

---

## Quick Reference

### Key NPCs This Session
| NPC | Role | Personality | Want | Secret |
|-----|------|-------------|------|--------|
| [[NPC 1]] | [role] | [2-3 words] | [goal] | [hidden] |
| [[NPC 2]] | [role] | [2-3 words] | [goal] | [hidden] |

### Active Factions
| Faction | Goal | Disposition | Agent |
|---------|------|-------------|-------|
| [[Faction 1]] | [objective] | [friendly/hostile/neutral] | [[Agent NPC]] |

### Locations
| Location | Key Feature | Danger | Opportunity |
|----------|-------------|--------|-------------|
| [[Location 1]] | [notable thing] | [threat] | [hook] |

---

## Session Outline

### Opening Scene
**Location:** [[Start Location]]
**Setup:** [2-3 sentences describing how session begins]
**Read-Aloud Text:**
> "[Atmospheric description for players]"

### Possible Scenes

#### Scene A: [Name]
**Trigger:** [What leads here]
**Location:** [[Location]]
**NPCs:** [[NPC 1]], [[NPC 2]]
**Purpose:** [What this scene accomplishes]
**Key Information:** [What players can learn]
**Complications:** [What could go wrong]

#### Scene B: [Name]
[Same structure]

#### Scene C: [Name]
[Same structure]

### Climax Options
[2-3 possible climactic moments based on player choices]

### Ending Hooks
[How to end on a cliffhanger or setup next session]

---

## NPC Cheat Sheets

### [[NPC Name]]
**Quick Stats:** AC [X], HP [X], Attack +[X] ([damage])
**Voice/Mannerism:** [How to portray them]
**Key Phrases:**
- "[Something they'd say]"
- "[Another characteristic line]"
**Knows:** [Information they have]
**Wants:** [Their immediate goal]
**Fears:** [What threatens them]
**Will Trade:** [What they offer for help]

[Repeat for each major NPC]

---

## Location Briefs

### [[Location Name]]

**At a Glance:** [1 sentence summary]

**Sensory Details:**
- **See:** [Visual description]
- **Hear:** [Sounds]
- **Smell:** [Scents]

**Key Features:**
1. [Notable feature with mechanical relevance]
2. [Another feature]
3. [Interactive element]

**Hidden Elements:**
- **DC [X] Perception:** [What they notice]
- **DC [X] Investigation:** [What they find]

**Inhabitants:** [[Creature/NPC]]

**Exits:** [Where paths lead]

---

## Encounter Summaries

### Combat: [Encounter Name]
**Difficulty:** [Easy/Medium/Hard/Deadly]
**Enemies:** [X] [[Creature]] (CR [Y])
**Tactics:** [How they fight]
**Trigger:** [What starts combat]
**Terrain:** [Battle map notes]
**Treasure:** [Loot]

### Social: [Encounter Name]
**NPC:** [[NPC Name]]
**Stakes:** [What's at risk]
**Success:** [What they gain]
**Failure:** [Consequences]
**Key DCs:** Persuasion [X], Insight [X]

---

## Treasure & Rewards

### Planned Treasure
| Item | Location/Source | Value |
|------|-----------------|-------|
| [[Item 1]] | [where found] | [gp/rarity] |
| [Gold amount] | [where found] | [X gp] |

### Information Rewards
| Clue | Source | Reveals |
|------|--------|---------|
| [Clue description] | [[NPC/Location]] | [Plot advancement] |

---

## Contingencies

### If Players...
- **Go left instead of right:** [How to adapt]
- **Attack the friendly NPC:** [Consequences]
- **Skip the dungeon entirely:** [Alternative path]
- **Ask about [topic]:** [Prepared answer]

### Random Encounters
[3-4 encounters ready if needed, scaled to party]

### Emergency NPCs
[2-3 generic NPCs ready to drop in]

---

## Session Checklist

### Before Session
- [ ] Review NPC voices
- [ ] Prepare battle maps for: [locations]
- [ ] Queue music for: [scenes]
- [ ] Print/prepare: [handouts]

### During Session Track
- [ ] XP earned: ___
- [ ] Gold found: ___
- [ ] Items acquired: ___
- [ ] NPCs met: ___
- [ ] Plot points revealed: ___

### Notes for Next Session
[Space for during-session notes]
```

### Step 4: Generate Supporting Materials

Based on session needs, also create:

#### NPC Voice Cards
```
┌─────────────────────────────────────┐
│ NPC NAME                            │
├─────────────────────────────────────┤
│ Voice: [accent/pattern]             │
│ Gesture: [physical habit]           │
│ Catchphrase: "[phrase]"             │
│ Motivation: [single word]           │
├─────────────────────────────────────┤
│ Stats: AC [X] HP [X] +[X] to hit    │
│ Spell DC [X] if caster              │
└─────────────────────────────────────┘
```

#### Location Maps Key
If location has rooms/areas:
```
LOCATION MAP KEY

A. [Area name] - [1 line description]
B. [Area name] - [1 line description]
C. [Area name] - [1 line description]

Trap: Room [X]
Treasure: Room [X]
Boss: Room [X]
```

### Step 5: Plot Thread Tracking

If world has ongoing plots:
```
## Active Plot Threads

### Thread: [Plot Name]
**Status:** [current state]
**Last Session:** [what happened]
**This Session:** [how to advance]
**Foreshadowing:** [hints to drop]

### Thread: [Plot Name]
[Repeat]
```

### Step 6: Save and Organize

Offer to save prep document:
> "Would you like me to save this session prep?"

If yes:
1. Save to `Worlds/[World Name]/Sessions/Session [Date] - [Title].md`
2. Create Sessions folder if needed

### Step 7: Offer Additional Prep

> "Session prep complete! Would you also like me to:
> 1. Generate detailed battle maps descriptions
> 2. Create handout text for players
> 3. Write read-aloud descriptions for key moments
> 4. Generate backup random encounters
> 5. Create a player-facing session summary from last time"

## Examples

```
# Basic session prep
/session-prep Eldoria "Ironhold City"

# With specific focus
/session-prep Eldoria "The Sunken Temple" level 8

# Adventure-focused
/session-prep Eldoria "Confronting the Cult" climax session
```
