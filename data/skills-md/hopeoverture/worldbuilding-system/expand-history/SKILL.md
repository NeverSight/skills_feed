---
name: expand-history
description: Expand a historical era or event with detailed timeline, key figures, artifacts, witnesses still living, and consequences that echo to the present. Use when user wants to "detail this war", "expand this age", or "develop this event's history".
argument-hint: "[era/event name or path]"
---

# Expand History

Expand this historical period or event: $ARGUMENTS

## Overview

Takes an existing historical entity (Age, Event, War, Battle, Treaty, Tragedy, Dynasty) and expands it with:
1. Detailed chronological timeline
2. Key figures who shaped events (with NPC files)
3. Artifacts and relics from the period
4. Witnesses who survived (still living NPCs)
5. Locations where events occurred
6. Consequences that affect the present
7. Legends and distorted accounts
8. Lost knowledge and mysteries

## Instructions

### Step 1: Locate and Analyze the Historical Entity

1. **Parse `$ARGUMENTS`** for history name or path
2. **Search in `Worlds/[World]/History/`**
3. **Read the entity file** and determine type:
   - **Age:** An era spanning generations
   - **Event:** A specific occurrence
   - **War:** Extended conflict
   - **Battle:** Single engagement
   - **Treaty:** Agreement between powers
   - **Tragedy:** Disaster or catastrophe
   - **Dynasty:** Ruling lineage

4. **Extract existing information:**
   - Time period
   - Key participants mentioned
   - Locations involved
   - Causes and consequences
   - Connection to other history

5. **Determine expansion scope:**

| Type | Timeline Detail | Figures | Artifacts | Living Witnesses |
|------|-----------------|---------|-----------|------------------|
| Age | Phases & epochs | 8-12 | 3-5 | If recent |
| Event | Days/weeks | 5-8 | 1-3 | If <100 years |
| War | Campaigns | 8-12 | 3-5 | If <100 years |
| Battle | Hours | 5-8 | 2-3 | If <100 years |
| Treaty | Negotiations | 4-6 | 1-2 | If <100 years |
| Tragedy | Phases | 3-5 | 1-3 | If <100 years |
| Dynasty | Generations | 6-10 | 2-4 | Current members |

### Step 2: Present Expansion Plan

```
=== HISTORY EXPANSION: [Name] ===

Type: [Age/Event/War/Battle/Treaty/Tragedy/Dynasty]
Period: [When it occurred]
Duration: [How long it lasted]

Current Information:
- Causes: [Summarized]
- Key Events: [Listed]
- Outcome: [Summarized]
- Known Figures: [X] mentioned

Proposed Expansion:

1. DETAILED TIMELINE
   - [Phase 1]: [Key events]
   - [Phase 2]: [Key events]
   - [Phase 3]: [Key events]

2. KEY FIGURES ([X] to create)
   Leaders:
   - [Figure 1]: [Role]
   - [Figure 2]: [Role]
   Heroes/Villains:
   - [Figure 3]: [Role]
   - [Figure 4]: [Role]

3. ARTIFACTS & RELICS ([X] to create)
   - [Artifact 1]: [Significance]
   - [Artifact 2]: [Significance]

4. LIVING WITNESSES ([X] if applicable)
   - [Witness 1]: [Their experience]
   - [Witness 2]: [Their experience]

5. LOCATIONS ([X] to detail)
   - [[Location 1]]: [Role in events]
   - [[Location 2]]: [Role in events]

6. CONSEQUENCES
   - Political changes still felt
   - Cultural impacts
   - Grudges and tensions
   - Lost knowledge

7. LEGENDS & MYSTERIES
   - [Distorted account 1]
   - [Unsolved mystery 1]

Proceed? (yes/customize)
```

### Step 3: Create Detailed Timeline

Expand the historical entity with a comprehensive timeline:

**For Ages (generation-spanning eras):**
```markdown
## Detailed Timeline

### Dawn of the [Age Name] (Years [X] - [Y])
**Defining Moment:** [Event that marked the beginning]

| Year | Event | Key Figures | Location | Impact |
|------|-------|-------------|----------|--------|
| [Year] | [Event] | [[Figure]] | [[Place]] | [Consequence] |
| [Year] | [Event] | [[Figure]] | [[Place]] | [Consequence] |

**Cultural Developments:**
- [Change in society, art, religion]
- [Technological advancement]

**Political Landscape:**
- [Who held power]
- [Major conflicts]

### Height of the [Age Name] (Years [X] - [Y])
[Similar structure]

### Decline of the [Age Name] (Years [X] - [Y])
[Similar structure]

### Transition to [[Next Age]]
**Defining Moment:** [Event that marked the end]
[How one age became another]
```

**For Wars (extended conflicts):**
```markdown
## Detailed Timeline

### Causes & Build-up (Years [X] - [Y])
**Root Causes:**
- [Long-term cause 1]
- [Long-term cause 2]

**Immediate Triggers:**
- [Event that started hostilities]

**Declaration:**
- [When/how war was declared]
- [Initial positions of powers]

### The [First/Name] Campaign (Years [X] - [Y])
**Objective:** [What this phase aimed to achieve]
**Belligerents:**
- [[Faction A]]: [Commander], [forces]
- [[Faction B]]: [Commander], [forces]

| Date | Action | Location | Outcome |
|------|--------|----------|---------|
| [Date] | [[Battle Name]] | [[Location]] | [Victor] |
| [Date] | [Siege of [[City]]] | [[Location]] | [Result] |
| [Date] | [Diplomatic event] | [[Location]] | [Impact] |

**Turning Point:** [Key moment that shifted momentum]

### The [Second/Name] Campaign (Years [X] - [Y])
[Similar structure]

### War's End (Year [X])
**Final Engagement:** [[Battle/Event]]
**Peace Process:** [How negotiations began]
**The [[Treaty Name]]:** [Terms and signatories]

### Aftermath
**Immediate:** [Months after end]
**Long-term:** [Years after end]
**Legacy:** [What changed forever]
```

**For Events/Battles (specific occurrences):**
```markdown
## Detailed Timeline

### Prelude ([Time period before])
**Setting:** [Context and conditions]
**Key Tensions:** [What was building]
**Warning Signs:** [What should have been noticed]

### Day/Phase 1: [Title]
| Time | Event | Key Actors | Consequence |
|------|-------|------------|-------------|
| [Time] | [Action] | [[Figure]] | [Result] |
| [Time] | [Action] | [[Figure]] | [Result] |

**Critical Moment:** [The pivot point of this phase]

### Day/Phase 2: [Title]
[Similar structure]

### Climax: [Title]
**The Decisive Moment:**
[Detailed description of the key event]

**Who Was There:**
- [[Figure 1]]: [Their role]
- [[Figure 2]]: [Their role]

### Immediate Aftermath
**Casualties:** [Human cost]
**Physical Impact:** [Destruction, changes]
**Initial Reactions:** [How people responded]

### Long-term Consequences
**[X] Years Later:** [State of affairs]
**[X] Decades Later:** [Lasting changes]
**In the Present:** [What remains]
```

### Step 4: Generate Key Historical Figures

Create NPCs who shaped these events:

**Categories of Figures:**
1. **Leaders** - Rulers, generals, high priests
2. **Heroes** - Those who saved others or turned the tide
3. **Villains** - Those who caused harm or betrayed
4. **Witnesses** - Common people who saw events
5. **Chroniclers** - Those who recorded history
6. **Victims** - Those who suffered
7. **Survivors** - Those who endured

**For each major figure:**
1. Read appropriate character template
2. Generate with:
   - Role in the historical events
   - Fate (died during, survived, unknown)
   - Legacy (how remembered)
   - Connections to current entities
3. Save to Characters folder

**Historical Figure Entry Template:**
```markdown
### Role in [Historical Event]

**Position:** [Their role during events]
**Actions:**
- [Key action 1]
- [Key action 2]
- [Decisive moment]

**Fate:** [What happened to them]
**Legacy:** [How they're remembered]
**Monuments:** [Statues, named places, etc.]

**What History Records:**
[The official/common version]

**What Really Happened:**
[The truth, if different]
```

### Step 5: Create Historical Artifacts

Generate items from the period:

**Artifact Types:**
- **Weapons** used in battles
- **Regalia** of fallen rulers
- **Documents** (treaties, orders, journals)
- **Relics** (religious or magical)
- **Art** depicting events
- **Personal Effects** of key figures

**For each artifact:**
1. Read appropriate item template
2. Generate with:
   - Historical significance
   - Current location (known, lost, contested)
   - Who seeks it
   - Powers or value
3. Save to Items folder

**Artifact Entry Template:**
```markdown
### Historical Significance

**Created:** [When and by whom]
**Role in Events:** [How it mattered]
**Last Known Location:** [[Location]] or "Unknown"
**Current Status:** [In collection/Lost/Contested/Destroyed]

**Seekers:**
- [[Entity 1]]: [Why they want it]
- [[Entity 2]]: [Why they want it]

**Legends About It:**
[What people believe about the artifact]

**Adventure Hook:**
[How PCs might become involved]
```

### Step 6: Identify Living Witnesses

If events occurred within living memory (varies by species):

**Species Lifespans for Reference:**
| Species | Average Lifespan | "Living Memory" |
|---------|------------------|-----------------|
| Human | 70-80 years | ~60 years |
| Dwarf | 350 years | ~300 years |
| Elf | 700+ years | ~600 years |
| Half-Elf | 180 years | ~150 years |
| Gnome | 400 years | ~350 years |
| Halfling | 150 years | ~120 years |

**For each witness:**
1. Calculate if they could be alive
2. Generate as NPC (usually Background Character)
3. Include:
   - What they saw
   - How it affected them
   - What they tell others
   - What they hide
   - Where they are now

**Witness Entry Template:**
```markdown
### Witness to [Historical Event]

**What They Witnessed:**
[Specific experiences]

**Age at Time:** [X] years old
**Current Age:** [X] years old
**Current Location:** [[Settlement]]

**How It Changed Them:**
[Psychological impact, life changes]

**Their Account:**
"[Quote - what they tell people]"

**What They Don't Tell:**
[Hidden trauma or secrets]

**Why They Matter Now:**
[Information they hold, role they could play]
```

### Step 7: Detail Historical Locations

Expand locations where events occurred:

1. **Read existing location files** if they exist
2. **Add historical sections:**
```markdown
### Historical Significance: [Event/Age Name]

**What Happened Here:**
[Description of events at this location]

**Physical Evidence:**
- [Ruins, monuments, scars on landscape]
- [Artifacts that might be found]

**Local Memory:**
- [How locals remember/discuss it]
- [Taboos or traditions related to it]

**Haunted/Magical Effects:**
[If applicable - echoes of violence, sacred ground, etc.]
```

3. **Create new locations** if events happened somewhere undetailed

### Step 8: Map Present-Day Consequences

Document how history affects the current world:

```markdown
## Living Consequences

### Political Impact
**Power Shifts:**
- [[Government A]] rose because of [event]
- [[Government B]] fell because of [event]
- Current borders reflect [consequence]

**Ongoing Tensions:**
- [[Faction A]] vs [[Faction B]]: [Grudge from events]
- [[Region]] still resents [[Region]] for [reason]

### Social Impact
**Changed Customs:**
- [Practice that began because of events]
- [Taboo that emerged from events]

**Demographic Changes:**
- [Population shifts, migrations, extinctions]
- [Mixed populations from aftermath]

### Cultural Impact
**Holidays & Observances:**
- [[Festival]] commemorates [aspect of events]
- Day of Mourning for [tragedy]

**Art & Literature:**
- [Famous works about the events]
- [Banned or controversial depictions]

**Sayings & Proverbs:**
- "[Phrase]" - refers to [event aspect]

### Economic Impact
**Trade Changes:**
- [Routes that opened/closed]
- [Resources that became valuable/worthless]

**Debts & Reparations:**
- [[Entity]] still pays [[Entity]] for [reason]
- Disputed claims over [resource/territory]

### Magical/Religious Impact
**Divine Involvement:**
- [[Deity]] is credited with [intervention]
- [[Religion]] gained/lost followers because [reason]

**Magical Consequences:**
- [Cursed lands, blessed sites]
- [Magic that was lost/discovered]
```

### Step 9: Create Legends & Distorted Accounts

History is told differently by different groups:

```markdown
## Competing Narratives

### Official History
**According to [[Government/Religion]]:**
[The sanctioned version of events]

**Why This Version:**
[What it serves, what it hides]

### Folk Memory
**Common People Believe:**
[The popular version, often simplified]

**Distortions:**
- [Exaggeration 1]
- [Missing element 1]
- [Added myth element]

### [[Faction A]]'s Version
**They Claim:**
[Their biased account]

**Their Evidence:**
[What they point to]

### [[Faction B]]'s Version
**They Claim:**
[Their different account]

**Their Evidence:**
[What they point to]

### The Truth
**What Actually Happened:**
[The real account, known only to few or none]

**Who Knows:**
- [[Character]] knows because [reason]
- [[Document]] contains truth, located at [[Location]]
- No one living knows [aspect]
```

### Step 10: Document Mysteries & Lost Knowledge

```markdown
## Unsolved Mysteries

### [Mystery 1 Name]
**The Question:** [What's unknown]
**What's Known:** [Established facts]
**Theories:**
- Theory 1: [Explanation]
- Theory 2: [Explanation]
**The Truth:** [For GM's eyes - actual answer]
**Investigation Hooks:** [How PCs might investigate]

### [Mystery 2 Name]
[Similar structure]

## Lost Knowledge

### [Lost Knowledge 1]
**What Was Lost:** [Description]
**Why It Matters:** [Significance]
**Where It Might Be Found:**
- [[Location 1]]: [Likelihood]
- [[Location 2]]: [Likelihood]
**Who Seeks It:** [[Seeker]] - [their motive]

### Forgotten Truths
[Things that were once known but forgotten]
- [Truth 1]: Only [[Character type]] remembers
- [Truth 2]: Recorded in [[Book]] at [[Library]]
```

### Step 11: Update Connected Entities

1. **Update the history file** with all new sections
2. **Update or create NPC files** for historical figures
3. **Update or create artifact files** for relics
4. **Update location files** with historical significance
5. **Update World Overview** timeline
6. **Add references** in government, religion, and organization files
7. **Connect to current NPCs** who might know history or be descendants

### Step 12: Summary Report

```
=== HISTORY EXPANSION COMPLETE: [Name] ===

Historical Entity Type: [Age/Event/War/etc.]
Period Covered: [Time span]

TIMELINE DETAIL:
- [X] phases/periods documented
- [Y] specific events dated
- [Z] turning points identified

KEY FIGURES CREATED/EXPANDED: [X]
Leaders:
- [[Figure 1]] - [Role, Fate]
- [[Figure 2]] - [Role, Fate]

Heroes:
- [[Figure 3]] - [Role, Fate]

Villains:
- [[Figure 4]] - [Role, Fate]

ARTIFACTS CREATED: [X]
- [[Artifact 1]] - [Location/Status]
- [[Artifact 2]] - [Location/Status]

LIVING WITNESSES: [X]
- [[Witness 1]] - [Current location]
- [[Witness 2]] - [Current location]

LOCATIONS DETAILED: [X]
- [[Location 1]] - Historical significance added
- [[Location 2]] - Created new location

PRESENT-DAY CONSEQUENCES:
- [X] political impacts documented
- [Y] cultural changes noted
- [Z] ongoing tensions mapped

MYSTERIES & LOST KNOWLEDGE:
- [X] unsolved mysteries
- [Y] items of lost knowledge

COMPETING NARRATIVES:
- [X] different versions documented

Connected Entities Updated: [X]
Files Created: [X]
Files Modified: [X]

Suggested Next Steps:
- Create adventure around [[Artifact]]
- Use [[Witness]] as quest-giver
- Explore [[Mystery]] as investigation
- Develop [[Figure]]'s descendants
- Map [[Location]] as dungeon
```

## Quality Guidelines

1. **Cause and Effect** - Events have logical causes and consequences
2. **Multiple Perspectives** - History is remembered differently
3. **Living Impact** - Past affects present
4. **Mystery Preservation** - Not everything is known
5. **Character-Driven** - People shaped events
6. **Physical Evidence** - History left marks on the world
7. **Adventure Hooks** - Every element can become a quest

## Examples

```
# Expand a war
/expand-history "The War of Broken Crowns"

# Expand an age
/expand-history "The Second Age of Magic"

# Expand with path
/expand-history Worlds/Eldermyr/History/The Sundering.md

# Focus on specific aspect
/expand-history "The Great Plague" --focus witnesses
```
