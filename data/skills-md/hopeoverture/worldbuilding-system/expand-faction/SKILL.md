---
name: expand-faction
description: Build out an organization with member hierarchy, internal politics, resources, secret plots, rivals, and operational details. Use when user wants to "flesh out a guild", "expand an organization", or "detail a faction".
argument-hint: "[organization name or path]"
---

# Expand Faction

Expand this faction/organization: $ARGUMENTS

## Overview

Takes an existing organization (Guild, Government, Military, Cult, Religious Order, Criminal Organization, Academy, or Business) and expands it with:
1. Complete leadership hierarchy with named NPCs
2. Rank structure and advancement paths
3. Internal factions and politics
4. Resources, assets, and operations
5. Secret plots and hidden agendas
6. Rivals, allies, and external relationships
7. Recruitment and initiation processes

## Instructions

### Step 1: Locate and Analyze the Organization

1. **Parse `$ARGUMENTS`** for organization name or path
2. **Search in `Worlds/[World]/Organizations/`**
3. **Read the organization file** and extract:
   - Organization type (Guild, Military, Cult, etc.)
   - Purpose and goals
   - Current leadership mentioned
   - Headquarters location
   - Known members
   - Existing rivals/allies
   - Scope (local, regional, continental)

4. **Determine expansion scope** by type:

| Org Type | Leaders | Ranks | Members | Cells/Chapters |
|----------|---------|-------|---------|----------------|
| Guild | 3-5 | 4-5 | 10-15 | 2-4 |
| Government | 5-8 | 5-7 | 15-20 | N/A (departments) |
| Military | 5-7 | 6-8 | 12-18 | 3-5 (units) |
| Cult | 3-5 | 4-6 | 8-12 | 2-4 (cells) |
| Religious Order | 4-6 | 5-7 | 12-15 | 3-5 (monasteries) |
| Criminal Org | 3-5 | 4-5 | 10-15 | 3-6 (crews) |
| Academy | 4-6 | 4-5 | 10-12 | N/A (departments) |
| Business | 3-5 | 4-5 | 8-12 | 2-4 (branches) |

### Step 2: Present Expansion Plan

```
=== FACTION EXPANSION: [Organization Name] ===

Current State:
- Type: [Guild/Military/Cult/etc.]
- Scope: [Local/Regional/Continental]
- Headquarters: [[Location]]
- Known Members: [count]
- Known Rivals: [list]

Proposed Expansion:

1. LEADERSHIP COUNCIL ([X] NPCs)
   - [Title]: [Role in organization]
   - [Title]: [Role in organization]

2. RANK STRUCTURE
   - [Rank 1]: Requirements and privileges
   - [Rank 2]: Requirements and privileges
   ...

3. INTERNAL FACTIONS ([X] groups)
   - [Faction A]: Philosophy/goal
   - [Faction B]: Philosophy/goal

4. NOTABLE MEMBERS ([X] NPCs by rank)
   - [High-ranking members]
   - [Mid-level operatives]
   - [Notable initiates]

5. RESOURCES & ASSETS
   - [Headquarters details]
   - [Secondary locations]
   - [Financial resources]
   - [Unique assets]

6. SECRET PLOTS ([X] ongoing schemes)
   - [Plot 1]
   - [Plot 2]

7. EXTERNAL RELATIONSHIPS
   - Allies: [Organizations]
   - Rivals: [Organizations]
   - Neutral contacts: [Organizations]

Proceed? (yes/customize/skip sections)
```

### Step 3: Generate Leadership Hierarchy

Create the ruling body of the organization:

**For Guilds:**
- Guildmaster (Support/Antagonist Character)
- Vice Master or Second (Support Character)
- Treasurer (Background Character)
- Master of Apprentices (Background Character)
- Notable Masters (2-3 Background Characters)

**For Governments:**
- Ruler/Leader (Support/Antagonist Character)
- Heir Apparent (Support Character)
- Chief Advisor (Support Character)
- Spymaster (Support/Antagonist Character)
- Military Commander (Support Character)
- Court Mage (if magical world)
- High Priest (if theocratic elements)
- Treasury Minister (Background Character)

**For Military:**
- Commander/General (Support Character)
- Second-in-Command (Support Character)
- Intelligence Officer (Support Character)
- Quartermaster (Background Character)
- Unit Commanders (2-3 Support Characters)
- Notable Veterans (Background Characters)

**For Cults:**
- High Priest/Prophet (Antagonist Character)
- Inner Circle (2-3 Support/Antagonist)
- Enforcer/Inquisitor (Antagonist Character)
- Recruiter/Face (Support Character)
- Hidden Patron (if applicable)

**For Religious Orders:**
- Grandmaster/High Priest (Support Character)
- Council of Elders (2-3 Support Characters)
- Master of Novices (Support Character)
- Keeper of Sacred Relics (Background Character)
- Champion/Exemplar (Support Character)

**For Criminal Organizations:**
- Boss/Kingpin (Antagonist Character)
- Underboss (Support/Antagonist Character)
- Consigliere/Advisor (Support Character)
- Enforcer (Antagonist Character)
- Crew Leaders (2-3 Support Characters)
- Fence/Money Handler (Background Character)

**For Academies:**
- Headmaster/Archmage (Support Character)
- Department Heads (2-3 Support Characters)
- Dean of Students (Support Character)
- Librarian/Keeper of Knowledge (Background Character)
- Notable Professors (Background Characters)

**For Businesses:**
- Owner/Patriarch (Support Character)
- Heir/Successor (Support Character)
- Operations Manager (Background Character)
- Trade Master (Support Character)
- Notable Agents (Background Characters)

**For each leader:**
1. Read appropriate character template
2. Generate with:
   - Their path to power
   - Key relationships within organization
   - Personal agenda (may conflict with org goals)
   - At least one secret
   - Distinctive leadership style
3. Save to Characters folder

### Step 4: Define Rank Structure

Create a detailed hierarchy section in the organization file:

```markdown
## Rank Structure

| Rank | Title | Requirements | Privileges | Count |
|------|-------|--------------|------------|-------|
| 1 | [Initiate] | [Entry requirements] | [Basic access] | ~[X] |
| 2 | [Journeyman] | [Time + tests] | [More privileges] | ~[X] |
| 3 | [Adept] | [Achievement] | [Authority level] | ~[X] |
| 4 | [Master] | [Mastery proof] | [Leadership roles] | ~[X] |
| 5 | [Elder/Council] | [Selection] | [Voting rights] | [X] |

### Advancement Rituals
- **Initiate to Journeyman:** [Description of test/ceremony]
- **Journeyman to Adept:** [Description]
- **Adept to Master:** [Description]
- **Master to Elder:** [Selection process]

### Insignia & Recognition
- **Initiate:** [Badge/mark/uniform element]
- **Journeyman:** [Badge/mark/uniform element]
- **Adept:** [Badge/mark/uniform element]
- **Master:** [Badge/mark/uniform element]
- **Elder:** [Badge/mark/uniform element]
```

### Step 5: Create Internal Factions

Every organization has internal politics. Create 2-4 internal factions:

**Faction Template:**
```markdown
### [Faction Name]

**Philosophy:** [Core belief or goal that differs from mainstream]
**Leader:** [[NPC Name]] - [Their position in main hierarchy]
**Members:** Approximately [X]% of organization
**Goals:**
- [Short-term goal]
- [Long-term goal]
**Methods:** [How they operate - openly, secretly, through influence]
**Rivals Within:** [[Other Faction]] - [Nature of conflict]
```

**Common Faction Archetypes:**
1. **Traditionalists** - Preserve old ways, resist change
2. **Reformers** - Modernize, expand scope
3. **Militants** - More aggressive action
4. **Moderates** - Diplomatic approach
5. **Purists** - Strict adherence to original purpose
6. **Pragmatists** - Ends justify means
7. **Loyalists** - Support current leadership
8. **Conspirators** - Seek to replace leadership

### Step 6: Generate Notable Members

Create NPCs at various rank levels:

**High-Ranking (3-4 NPCs):**
- Use Support Character template
- Give significant responsibilities
- Each has ambitions and secrets
- Connect to internal factions

**Mid-Level (4-6 NPCs):**
- Mix of Support and Background Characters
- Specialists and department heads
- Field operatives or representatives
- Connect to headquarters and external contacts

**Low-Ranking/Initiates (3-4 NPCs):**
- Background Characters
- Fresh recruits with potential
- Provide ground-level perspective
- May be spies or plants from rivals

**For each member:**
1. Generate with appropriate template
2. Assign to a rank and internal faction
3. Define their specialty or role
4. Create relationships with other members
5. Include one hook or secret

### Step 7: Detail Resources & Assets

Expand the organization's resource section:

**Headquarters (detailed):**
```markdown
### Headquarters: [[Location Name]]

**Location:** [Description of where within settlement]
**Description:** [Physical description - size, architecture, defenses]
**Key Rooms/Areas:**
- [Room 1]: [Purpose and notable contents]
- [Room 2]: [Purpose and notable contents]
- [Secret Area]: [Hidden purpose]

**Security:**
- [Guard complement]
- [Magical protections if any]
- [Secret defenses]

**Staff:** [Non-member employees]
```

**Secondary Locations:**
- Branch offices or chapters
- Safe houses
- Training grounds
- Resource extraction sites
- Meeting locations

**Financial Resources:**
- Primary income sources
- Treasury estimate
- Investments and assets
- Debts or obligations

**Unique Assets:**
- Magical items owned
- Important documents or secrets
- Unique resources (rare materials, special contacts)
- Vehicles or transport

### Step 8: Develop Secret Plots

Create 2-4 ongoing schemes:

**Plot Template:**
```markdown
### [Codename or Description]

**Objective:** [What the organization wants to achieve]
**Mastermind:** [[NPC Name]] - [Why they're driving this]
**Stage:** [Planning/Active/Near Completion]
**Resources Committed:** [What's being used]
**Obstacles:** [What stands in the way]
**Timeline:** [When they expect completion]
**Consequences if Successful:** [World impact]
**Consequences if Discovered:** [Fallout]
**Adventure Hook:** [How PCs might encounter this]
```

**Plot Types by Organization:**
- **Guilds:** Market manipulation, competitor sabotage, political influence
- **Governments:** Annexation, assassination, treaty manipulation
- **Military:** Coup, secret weapon, preemptive strike
- **Cults:** Summoning, mass conversion, artifact retrieval
- **Religious Orders:** Heretic hunting, relic recovery, crusade
- **Criminal:** Heist, territory expansion, corrupting officials
- **Academy:** Forbidden research, magical experiment, artifact study
- **Business:** Hostile takeover, smuggling, monopoly scheme

### Step 9: Map External Relationships

Create a relationship web:

```markdown
## External Relationships

### Allies
| Organization | Relationship | Nature | Contact |
|--------------|--------------|--------|---------|
| [[Ally 1]] | [Strong/Moderate/Weak] | [Why allied] | [[NPC]] |
| [[Ally 2]] | [Strong/Moderate/Weak] | [Why allied] | [[NPC]] |

### Rivals
| Organization | Hostility | Cause | Contact |
|--------------|-----------|-------|---------|
| [[Rival 1]] | [Open war/Cold war/Competition] | [Origin of conflict] | [[NPC]] |
| [[Rival 2]] | [Open war/Cold war/Competition] | [Origin of conflict] | [[NPC]] |

### Neutral Contacts
| Organization | Relationship | Purpose |
|--------------|--------------|---------|
| [[Contact 1]] | [Business/Information/Other] | [What they provide] |

### Government Relations
- **Legal Status:** [Legal/Tolerated/Illegal/Secret]
- **Official Contact:** [[Government NPC]]
- **Bribes/Taxes:** [Financial arrangement]
- **Known to Authorities:** [What officials know]
```

### Step 10: Define Recruitment & Initiation

```markdown
## Membership

### Recruitment
**Who They Seek:**
- [Ideal candidate profile]
- [Required skills or backgrounds]
- [Forbidden backgrounds]

**How They Recruit:**
- [Method 1: e.g., talent scouts]
- [Method 2: e.g., family connections]
- [Method 3: e.g., desperate outcasts]

**Recruitment Locations:**
- [[Location 1]] - [Why here]
- [[Location 2]] - [Why here]

### Initiation
**Process:**
1. [Step 1: e.g., sponsor introduction]
2. [Step 2: e.g., probationary period]
3. [Step 3: e.g., loyalty test]
4. [Step 4: e.g., formal ceremony]

**The Final Test:**
[Description of the defining initiation ritual or test]

**Oaths & Obligations:**
- [Primary oath or commitment]
- [Ongoing obligations]
- [Penalty for betrayal]

### Leaving the Organization
**Voluntary Departure:** [How it's handled - possible? consequences?]
**Expulsion:** [What causes it, what happens]
**Betrayal:** [How traitors are dealt with]
```

### Step 11: Update All Connections

1. **Update organization file** with all new sections
2. **Update each new NPC** with organization membership
3. **Update headquarters settlement** with organization presence
4. **Update rival organizations** with relationship notes
5. **Update allied organizations** with relationship notes
6. **Cross-reference** internal faction leaders

### Step 12: Summary Report

```
=== FACTION EXPANSION COMPLETE: [Name] ===

New Entities Created:

LEADERSHIP ([X] NPCs):
- [[Leader 1]] - [Title]
- [[Leader 2]] - [Title]

NOTABLE MEMBERS ([X] NPCs):
High Rank:
- [[Member 1]] - [Rank, Role]
Mid Rank:
- [[Member 2]] - [Rank, Role]
Initiates:
- [[Member 3]] - [Role]

LOCATIONS:
- [[Headquarters]] - Detailed expansion
- [[Secondary 1]] - New chapter/safehouse
- [[Secondary 2]] - New location

INTERNAL STRUCTURE:
- [X] Ranks defined with advancement paths
- [X] Internal factions with leaders
- Insignia and recognition system

SECRET PLOTS:
- [Plot 1] - [Stage]
- [Plot 2] - [Stage]

RELATIONSHIPS:
- [X] Allies defined with contacts
- [X] Rivals defined with conflicts
- [X] Neutral contacts listed

Suggested Next Steps:
- Expand rival [[Organization]] for comparison
- Create encounter with [[NPC]]
- Develop [[Plot Name]] into adventure
- Generate images for leadership
```

## Quality Guidelines

1. **Realistic Power Structure** - Clear chain of command
2. **Internal Tension** - Factions create drama without destroying org
3. **External Pressure** - Rivals and threats create urgency
4. **Advancement Motivation** - Clear benefits to rising in ranks
5. **Secrets at Every Level** - Leaders and members have hidden agendas
6. **Resource Constraints** - Organization has limits and needs
7. **Adventure Integration** - Every element offers gameplay hooks

## Examples

```
# Expand a thieves' guild
/expand-faction "The Shadow Hand"

# Expand with path
/expand-faction Worlds/Eldermyr/Organizations/Order of the Silver Dawn.md

# Focus on specific aspect
/expand-faction "Royal Army" --focus hierarchy
```
