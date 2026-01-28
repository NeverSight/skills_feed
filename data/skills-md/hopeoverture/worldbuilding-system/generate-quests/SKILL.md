---
name: generate-quests
description: Generate adventure hooks, quest lines, and story seeds tied to existing world entities. Creates bounties, mysteries, faction missions, and personal quests. Use when user wants "quest ideas", "adventure hooks", "story seeds", or "mission board" content.
argument-hint: "[world or scope] [optional: type or theme]"
---

# Generate Quests

Generate quests for: $ARGUMENTS

## Overview

Creates adventure content tied to existing world entities:
1. Bounty board postings (monster hunts, wanted criminals)
2. Mystery hooks (investigations, unexplained events)
3. Faction missions (organization-specific tasks)
4. Personal quests (character-driven stories)
5. Political intrigue (espionage, diplomacy)
6. Dungeon delves (exploration, treasure hunting)
7. Rescue/escort missions
8. Moral dilemmas (no easy answers)

## Instructions

### Step 1: Determine Scope

1. **Parse `$ARGUMENTS`** for:
   - World name (generate world-wide hooks)
   - Region name (regional adventures)
   - Settlement name (local quests)
   - Organization name (faction missions)
   - Character name (personal quests)
   - Type filter (bounties, mysteries, etc.)

2. **Read relevant entities:**
   - World Overview for themes
   - Location entities for setting
   - Organization entities for factions
   - Character entities for NPCs
   - History for background

3. **Identify quest-worthy elements:**
   - Unresolved conflicts
   - Mentioned threats
   - NPC goals and problems
   - Geographic mysteries
   - Historical secrets

### Step 2: Present Quest Generation Plan

```
=== QUEST GENERATION: [Scope] ===

Scope: [World/Region/Settlement/Faction]
Existing Hooks Found: [X] in current entities
Recommended Level Range: [Based on area threats]

Proposed Quest Types:

1. BOUNTIES ([X] quests)
   - Monster hunts
   - Wanted criminals
   - Dangerous beasts

2. MYSTERIES ([X] quests)
   - Investigations
   - Disappearances
   - Strange occurrences

3. FACTION MISSIONS ([X] quests)
   - [[Faction A]] needs...
   - [[Faction B]] needs...

4. DUNGEONS & EXPLORATION ([X] quests)
   - [[Site A]]: [Hook]
   - [[Site B]]: [Hook]

5. POLITICAL INTRIGUE ([X] quests)
   - Espionage
   - Diplomacy
   - Succession

6. MORAL DILEMMAS ([X] quests)
   - No easy answers

7. PERSONAL QUESTS ([X] quests)
   - For [[NPC A]]
   - For [[NPC B]]

Target Total: [20-30] quest hooks

Proceed? (yes/customize/focus on type)
```

### Step 3: Generate Bounty Board Quests

**Bounty Types:**
1. **Monster Hunt** - Kill a dangerous creature
2. **Wanted Criminal** - Capture/kill an outlaw
3. **Beast Control** - Clear an infestation
4. **Dangerous Terrain** - Make an area safe
5. **Creature Capture** - Bring back alive

**For each bounty:**
```markdown
### [Bounty Title]

**Type:** [Monster Hunt/Wanted/etc.]
**Posted By:** [[NPC or Organization]]
**Location:** [[Area]]
**Reward:** [GP amount] / [Other rewards]

**The Posting:**
> *[Flavor text as it appears on board]*
> *WANTED: [Target]. [Reason]. [Reward].*
> *—[[Poster]]*

**The Target:**
- Name/Type: [[Creature or NPC]]
- Threat Level: [CR or danger assessment]
- Last Seen: [[Location]]
- Distinguishing Features: [Identification details]

**The Truth:**
[What's actually going on - complications]

**Investigation Leads:**
1. [[NPC]] knows [information]
2. [[Location]] has [evidence]
3. [Other lead]

**Confrontation:**
- Location: [[Lair/Hideout]]
- Defenses: [What protects target]
- Allies: [Who aids target]

**Complications:**
- [Twist 1]
- [Twist 2]

**Outcomes:**
- Kill target: [Consequences]
- Capture alive: [Consequences + bonus]
- Let go: [Consequences]
- Discover truth: [New opportunities]

**Level Range:** [X-Y]
**Estimated Sessions:** [1-3]
```

### Step 4: Generate Mystery Quests

**Mystery Types:**
1. **Missing Person** - Someone vanished
2. **Murder Investigation** - Someone died
3. **Strange Phenomenon** - Unexplained events
4. **Stolen Item** - Something was taken
5. **Hidden Conspiracy** - Deeper plot
6. **Ancient Secret** - Historical mystery

**For each mystery:**
```markdown
### [Mystery Title]

**Type:** [Missing Person/Murder/etc.]
**Hook:** [[NPC]] approaches party or [how they learn]
**Location:** [[Area]]
**Reward:** [Payment/Favor/Information]

**The Hook:**
[2-3 sentences - what the party learns initially]

**What Happened:**
[The actual truth - for GM only]

**The Victim(s):**
- [[NPC]]: [Their role, connection to events]

**The Perpetrator:**
- [[NPC or Entity]]: [Motive and method]

**The Clues:**
| Location | Clue | Leads To |
|----------|------|----------|
| [[Scene 1]] | [Evidence] | [Next lead] |
| [[Scene 2]] | [Evidence] | [Next lead] |
| [[Scene 3]] | [Evidence] | [Next lead] |

**Red Herrings:**
- [False lead 1]
- [False lead 2]

**Key Witnesses:**
- [[NPC 1]]: Knows [information], will share if [condition]
- [[NPC 2]]: Knows [information], hiding because [reason]

**Breakthrough Moment:**
[When/how the truth becomes clear]

**Confrontation:**
- Where: [[Location]]
- The reveal: [How perpetrator is exposed/confronted]
- Their response: [Fight/Flee/Confess/etc.]

**Complications:**
- [Twist 1]
- [Twist 2]

**Resolution Options:**
- Justice: [Legal consequences]
- Vengeance: [Violent resolution]
- Mercy: [Let them go - consequences]
- Cover-up: [Hide the truth - consequences]

**Level Range:** [X-Y]
**Estimated Sessions:** [2-4]
```

### Step 5: Generate Faction Missions

For each major organization, create missions:

**Mission Types by Faction:**
| Faction Type | Mission Types |
|--------------|---------------|
| Government | Tax collection, law enforcement, diplomacy, reconnaissance |
| Guild | Trade escort, rival sabotage, resource acquisition, debt collection |
| Military | Patrol, strike mission, rescue, intelligence gathering |
| Religious | Pilgrimage escort, relic recovery, heretic hunting, miracle investigation |
| Criminal | Heist, smuggling, intimidation, territory expansion |
| Academy | Specimen collection, ruins exploration, experiment assistance |

**For each faction mission:**
```markdown
### [Mission Title]

**Faction:** [[Organization]]
**Mission Giver:** [[NPC]] - [Their role in org]
**Type:** [Mission type]
**Urgency:** [Immediate/Soon/When convenient]

**Briefing:**
> *"[NPC's actual words giving the mission]"*

**Objectives:**
- Primary: [Must accomplish]
- Secondary: [Bonus objective]
- Hidden: [What faction really wants]

**Background:**
[Why this mission matters to the faction]

**Resources Provided:**
- [Equipment/information/contacts]
- [Authority/documentation]

**Complications:**
- [Expected difficulty 1]
- [Unexpected complication]
- [Moral dimension]

**The Mission:**

1. **Phase 1: [Name]**
   - Location: [[Place]]
   - Task: [What to do]
   - Challenge: [Obstacle]

2. **Phase 2: [Name]**
   - Location: [[Place]]
   - Task: [What to do]
   - Challenge: [Obstacle]

3. **Phase 3: [Name]**
   - Location: [[Place]]
   - Task: [What to do]
   - Challenge: [Obstacle]

**Opposition:**
- [[Enemy 1]]: [Their interest]
- [[Enemy 2]]: [Their interest]

**Success Rewards:**
- Payment: [GP/items]
- Reputation: [Standing increase]
- Access: [New opportunities]
- [[Contact]]: [New relationship]

**Failure Consequences:**
- Faction: [How they respond]
- Personal: [Effect on party]
- World: [Broader impact]

**Follow-up Missions:**
- If successful: [Next mission possibility]
- If failed: [Recovery mission possibility]

**Level Range:** [X-Y]
**Estimated Sessions:** [1-3]
```

### Step 6: Generate Dungeon/Exploration Quests

Tie to existing geographic features:

```markdown
### [Quest Title]

**Site:** [[Dungeon/Ruin/Cave]]
**Hook:** [How party learns of it]
**Reward:** [Treasure/knowledge/favor]

**The Legend:**
[What people say about this place]

**The Truth:**
[What's actually there]

**Why Now:**
[Recent event that makes exploration timely]

**Getting There:**
- Route: [Travel requirements]
- Hazards: [Journey dangers]
- Guide: [[NPC]] available if [condition]

**Site Overview:**

| Area | Challenge | Treasure | Lore |
|------|-----------|----------|------|
| [Area 1] | [Danger] | [Reward] | [Discovery] |
| [Area 2] | [Danger] | [Reward] | [Discovery] |
| [Area 3] | [Danger] | [Reward] | [Discovery] |
| [Boss Area] | [Final challenge] | [Major reward] | [Key revelation] |

**Inhabitants:**
- [[Creature type]]: [Numbers, behavior]
- [[NPC faction]]: [Why they're here]

**The Prize:**
- [[Artifact/Treasure]]: [What it is]
- Location: [Where in dungeon]
- Guardian: [What protects it]

**Complications:**
- [Twist 1]
- [Rival party/faction also seeking]

**Aftermath:**
- Cleared: [What changes]
- Partially cleared: [What remains]
- Failed: [Consequences]

**Level Range:** [X-Y]
**Estimated Sessions:** [2-5]
```

### Step 7: Generate Political Intrigue Quests

```markdown
### [Quest Title]

**Type:** [Espionage/Diplomacy/Assassination/Sabotage]
**Patron:** [[NPC or Faction]]
**Target:** [[NPC or Faction]]
**Stakes:** [What's at risk]

**The Situation:**
[Political context in 2-3 sentences]

**The Mission:**
[What the patron wants done]

**Why the Party:**
[Why they need adventurers, not professionals]

**The Approach:**
Option A: [Subtle method]
Option B: [Direct method]
Option C: [Alternative approach]

**Key NPCs:**
- [[Target NPC]]: [Their situation, vulnerabilities]
- [[Allied NPC]]: [How they can help]
- [[Opposing NPC]]: [Their counter-moves]

**Locations:**
- [[Location 1]]: [Role in mission]
- [[Location 2]]: [Role in mission]

**Information to Gather:**
- [Secret 1]: Found at [location] from [source]
- [Secret 2]: Found at [location] from [source]

**Obstacles:**
- [Security measure 1]
- [Political complication]
- [Unexpected factor]

**Moral Dimensions:**
- [Ethical concern 1]
- [Ethical concern 2]
- What if the target is [sympathetic revelation]?

**Success Outcomes:**
- For patron: [What they gain]
- For party: [Rewards and consequences]
- For world: [Political shift]

**Failure Outcomes:**
- Caught: [Consequences]
- Exposed: [Consequences]
- Betrayed: [Consequences]

**Level Range:** [X-Y]
**Estimated Sessions:** [2-4]
```

### Step 8: Generate Moral Dilemma Quests

```markdown
### [Quest Title]

**The Dilemma:** [Core moral question]
**No Easy Answer:** [Why both choices have costs]

**Setup:**
[How the party encounters this situation]

**Side A: [Position Name]**
- Represented by: [[NPC A]]
- Their argument: [Why they're right]
- What they want: [Their goal]
- If they win: [Consequences]

**Side B: [Position Name]**
- Represented by: [[NPC B]]
- Their argument: [Why they're right]
- What they want: [Their goal]
- If they win: [Consequences]

**The Complication:**
[Why the party can't just walk away]

**Hidden Factors:**
- [Something neither side knows]
- [Secret that changes the equation]

**Possible Resolutions:**
1. Support Side A: [Full consequences]
2. Support Side B: [Full consequences]
3. Compromise: [What it looks like, costs to both]
4. Third option: [Creative solution, what it requires]
5. Walk away: [Why it's hard, what happens]

**No Right Answer:**
[Acknowledge that players may disagree - that's the point]

**Aftermath Seeds:**
- [How this decision echoes later]

**Level Range:** [Any - moral weight matters more]
**Estimated Sessions:** [1-2]
```

### Step 9: Generate Personal Quests

Tie to existing NPCs:

```markdown
### [Quest Title]: [[NPC Name]]'s Story

**NPC:** [[Character Name]]
**Relationship:** [How party knows them]
**Their Need:** [What they want]

**Background:**
[NPC's relevant history]

**The Revelation:**
[How party learns of their need]

**What They Ask:**
> *"[NPC's actual request in their voice]"*

**Why It Matters:**
- To NPC: [Personal stakes]
- To party: [Relationship/reward stakes]
- To world: [Broader implications if any]

**The Journey:**

1. **[Step 1]**
   - Go to: [[Location]]
   - Do: [Task]
   - Learn: [Information]

2. **[Step 2]**
   - Go to: [[Location]]
   - Do: [Task]
   - Overcome: [Challenge]

3. **[Resolution]**
   - Confront: [[Adversary or situation]]
   - Choice: [Decision to make]
   - Outcome: [Result]

**NPC During Quest:**
- Accompanies party: [Yes/No]
- If yes: [Their role, combat ability]
- If no: [Where they wait, their anxiety]

**Rewards:**
- [[NPC]]'s gratitude: [What they offer]
- Relationship: [How bond changes]
- Revelation: [What party learns about NPC]

**If Refused:**
- NPC attempts alone: [What happens]
- Relationship damage: [How it affects things]

**Level Range:** [X-Y]
**Estimated Sessions:** [1-3]
```

### Step 10: Create Quest Board Summary

Compile quests into usable format:

```markdown
## Quest Board: [[Location]]

*Posted notices, word-of-mouth opportunities, and pressing needs.*

### Active Bounties

| Bounty | Target | Reward | Posted By | Difficulty |
|--------|--------|--------|-----------|------------|
| [Name] | [Target] | [GP] | [[NPC]] | ★★☆☆☆ |
| [Name] | [Target] | [GP] | [[NPC]] | ★★★☆☆ |
| [Name] | [Target] | [GP] | [[NPC]] | ★★★★☆ |

### Rumors & Hooks

| Heard From | Rumor | Actually |
|------------|-------|----------|
| [[NPC]] | "[Rumor]" | [Truth/Hook it leads to] |
| Street talk | "[Rumor]" | [Truth/Hook it leads to] |
| [[Tavern]] | "[Rumor]" | [Truth/Hook it leads to] |

### Faction Opportunities

| Faction | Contact | Mission Available | Standing Required |
|---------|---------|-------------------|-------------------|
| [[Org 1]] | [[NPC]] | [Brief mission] | [None/Friendly/etc.] |
| [[Org 2]] | [[NPC]] | [Brief mission] | [None/Friendly/etc.] |

### Urgent Matters

*Time-sensitive opportunities*

1. **[Urgent Quest]** - [Deadline], [Consequence if missed]
2. **[Urgent Quest]** - [Deadline], [Consequence if missed]

### Long-term Opportunities

*Quests that can wait but offer substantial reward*

1. **[Quest]** - [Brief description]
2. **[Quest]** - [Brief description]
```

### Step 11: Link Quests to Entities

1. **Update NPC files** with quest-giving roles
2. **Update location files** with quest associations
3. **Update organization files** with mission types
4. **Update dungeon files** with treasure/danger details
5. **Create new quest document** or add to settlement files

### Step 12: Summary Report

```
=== QUEST GENERATION COMPLETE: [Scope] ===

Total Quests Created: [X]

BY TYPE:
- Bounties: [X]
- Mysteries: [X]
- Faction Missions: [X]
- Dungeon Delves: [X]
- Political Intrigue: [X]
- Moral Dilemmas: [X]
- Personal Quests: [X]

BY LEVEL RANGE:
- Tier 1 (1-4): [X] quests
- Tier 2 (5-10): [X] quests
- Tier 3 (11-16): [X] quests
- Tier 4 (17-20): [X] quests

QUEST CHAINS CREATED:
- [Chain 1]: [Quest A] → [Quest B] → [Quest C]
- [Chain 2]: [Quest A] → [Quest B]

KEY NPCs IN QUESTS:
- [[NPC 1]]: Quest-giver for [X] quests
- [[NPC 2]]: Target/subject of [X] quests
- [[NPC 3]]: Antagonist in [X] quests

FACTIONS REPRESENTED:
- [[Faction 1]]: [X] missions
- [[Faction 2]]: [X] missions

LOCATIONS FEATURED:
- [[Location 1]]: [X] quests
- [[Location 2]]: [X] quests

Files Created: [X]
Files Updated: [X]

Suggested Next Steps:
- Prepare [[Quest]] for next session
- Expand [[Dungeon]] for delve quest
- Develop [[NPC]] for personal quest
- Create handout for [[Bounty]]
```

## Quest Quality Guidelines

1. **Entity Integration** - Quests use existing world elements
2. **Player Agency** - Multiple approaches and outcomes
3. **Moral Complexity** - Not just good vs. evil
4. **Scalable Difficulty** - Adjustable to party level
5. **Lasting Consequences** - Actions matter to the world
6. **NPC Involvement** - Real people, not just quest-givers
7. **Variety** - Different types for different sessions

## Examples

```
# Generate quests for a world
/generate-quests "Eldermyr"

# Generate for a settlement
/generate-quests "City of Thornhaven"

# Generate for a faction
/generate-quests "The Shadow Hand" --type faction

# Generate specific type
/generate-quests "Ashlands Region" --type bounties

# Generate for level range
/generate-quests "Eldermyr" --levels 5-10
```
