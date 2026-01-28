---
name: generate-politics
description: Generate political systems including alliance webs, active conflicts, treaties, succession crises, and power brokers. Use when user wants to add "political intrigue", "alliances", "faction conflict", or "power dynamics" to a world.
argument-hint: "[world name]"
---

# Generate Politics

Generate political systems for: $ARGUMENTS

## Overview

Creates comprehensive political infrastructure for a world including:
1. Alliance webs between powers
2. Active conflicts and cold wars
3. Treaties and agreements
4. Succession lines and crises
5. Power brokers and kingmakers
6. Diplomatic relationships
7. Political factions within powers
8. Flashpoints and tensions

## Instructions

### Step 1: Survey the World's Powers

1. **Parse `$ARGUMENTS`** for world name
2. **Read World Overview** for:
   - Major governments
   - Known conflicts
   - Historical context

3. **Scan Organizations folder:**
   - All Governments
   - All Military organizations
   - Religious orders with political power
   - Guilds with political influence

4. **Identify key leaders** from Characters
5. **Note existing treaties** from History

### Step 2: Present Political Development Plan

```
=== POLITICS GENERATION: [World Name] ===

Current Political Landscape:
- Major Powers: [X] governments
- Military Forces: [X] organizations
- Religious Influences: [X] orders
- Existing Treaties: [X] documented

Power Assessment:
| Power | Strength | Stability | Aggression |
|-------|----------|-----------|------------|
| [[Gov 1]] | [1-5] | [1-5] | [1-5] |
| [[Gov 2]] | [1-5] | [1-5] | [1-5] |

Proposed Political System:

1. ALLIANCE WEB
   - [[A]] + [[B]]: [Basis]
   - [[C]] + [[D]]: [Basis]

2. RIVALRIES & CONFLICTS
   - [[X]] vs [[Y]]: [Nature]
   - Cold wars: [Count]

3. TREATIES & AGREEMENTS ([X] to create/detail)
   - [[Treaty 1]]: [Parties]

4. SUCCESSION SITUATIONS
   - [[Power 1]]: [Crisis/Stable]
   - [[Power 2]]: [Crisis/Stable]

5. POWER BROKERS ([X] NPCs)
   - [Type 1]: [Role]
   - [Type 2]: [Role]

6. FLASHPOINTS
   - [Location/Issue 1]
   - [Location/Issue 2]

Proceed? (yes/customize)
```

### Step 3: Create Alliance Web

Map formal and informal alliances:

```markdown
## Alliance Network

### Formal Alliances

#### The [[Alliance Name]]
**Members:** [[Power A]], [[Power B]], [[Power C]]
**Formed:** [Year] after [[Event]]
**Purpose:** [Mutual defense / Trade bloc / Religious unity]

**Terms:**
- [Obligation 1]
- [Obligation 2]
- [Conditions for activation]

**Strength:** [Strong/Moderate/Weak]
**Cracks:** [Internal tensions]

**Coordinating Body:** [If any]
**Key Figure:** [[NPC]] - [Role in alliance]

---

### Informal Alignments

#### [[Power A]] - [[Power B]] Axis
**Nature:** [Friendship/Convenience/Secret]
**Basis:**
- [Shared interest 1]
- [Shared interest 2]

**Not Formalized Because:**
[Why there's no treaty]

**Known To:** [Who knows about this alignment]

---

### Alliance Diagram

```
        [[Power A]]
           /    \
    ally  /      \  ally
         /        \
  [[Power B]]----[[Power C]]
       |           |
  rival|           |rival
       |           |
  [[Power D]]----[[Power E]]
           enemy
```

### Alliance Obligations Table

| If [[X]] is Attacked | [[Y]] Must | [[Z]] Must |
|---------------------|------------|------------|
| [[Power A]] | Defend | Support |
| [[Power B]] | Neutral | Defend |
```

### Step 4: Map Rivalries & Conflicts

**Conflict Types:**
1. **Hot War** - Active military conflict
2. **Cold War** - Hostile but not fighting
3. **Rivalry** - Competition without hostility
4. **Proxy Conflict** - Fighting through others
5. **Border Tension** - Localized friction
6. **Trade War** - Economic conflict

**For each major conflict:**
```markdown
### [[Power A]] vs [[Power B]]

**Status:** [Hot War/Cold War/Rivalry/etc.]
**Duration:** Since [Year/Event]

**Root Causes:**
1. [Historical grievance]
2. [Current dispute]
3. [Ideological difference]

**Current Situation:**
[2-3 sentences on present state]

**Flashpoints:**
- [[Location 1]]: [Why contested]
- [[Issue 1]]: [Why disputed]

**Recent Incidents:**
- [Year]: [Incident description]
- [Year]: [Incident description]

**War Likelihood:** [Imminent/Likely/Possible/Unlikely]

**If War Breaks Out:**
- [[A]]'s allies: [Who joins]
- [[B]]'s allies: [Who joins]
- Neutral powers: [Reactions]
- Likely theater: [[Region]]

**Peace Possibilities:**
- [What could resolve this]
- [Who's working for peace]

**Adventure Hooks:**
- [PC involvement opportunity]
```

### Step 5: Detail Treaties & Agreements

**Treaty Types:**
1. **Peace Treaty** - Ending a war
2. **Defensive Pact** - Mutual defense
3. **Trade Agreement** - Economic terms
4. **Non-Aggression Pact** - Promise not to fight
5. **Vassalage** - Subordinate relationship
6. **Marriage Alliance** - Dynastic tie
7. **Border Agreement** - Territorial settlement

**For each treaty:**
```markdown
### [[Treaty Name]]

**Type:** [Treaty type]
**Signed:** [Year] at [[Location]]
**Parties:** [[Power A]], [[Power B]], [others]

**Background:**
[How this came to be negotiated]

**Key Terms:**
1. [Term 1]
2. [Term 2]
3. [Term 3]

**Secret Clauses:** (if any)
[Known only to signatories]

**Duration:** [Perpetual/X years/Until condition]
**Renewal:** [Automatic/Requires negotiation]

**Enforcement:**
- [How violations are handled]
- [Who arbitrates disputes]

**Current Status:**
- Compliance: [Full/Partial/Violated]
- Tensions: [Issues with treaty]
- Renegotiation: [Any ongoing]

**Guarantor:** [[Power/Organization]] (if any)

**Signatories:**
| Party | Signed By | Ratified |
|-------|-----------|----------|
| [[Power A]] | [[NPC]] | [Year] |
| [[Power B]] | [[NPC]] | [Year] |

**Historical Significance:**
[What this treaty meant for the world]

**Adventure Hooks:**
- [Treaty-related quest opportunity]
```

### Step 6: Analyze Succession Situations

For each major power:

```markdown
## Succession: [[Power Name]]

### Current Ruler
**[[Ruler Name]]**
- Age: [X] years
- Health: [Robust/Declining/Critical]
- Reign: [X] years
- Legitimacy: [Unquestioned/Challenged/Weak]

### Line of Succession

| Order | Claimant | Claim Basis | Support | Obstacles |
|-------|----------|-------------|---------|-----------|
| 1st | [[Heir 1]] | [Birthright/etc.] | [Strong/Moderate/Weak] | [Issues] |
| 2nd | [[Heir 2]] | [Basis] | [Support level] | [Issues] |
| 3rd | [[Heir 3]] | [Basis] | [Support level] | [Issues] |

### Succession Law
- System: [Primogeniture/Elective/etc.]
- Gender: [Male-only/Equal/etc.]
- Legitimacy: [Requirements]
- Council role: [If any]

### Factions

**[[Faction A]] - Supports [[Heir 1]]**
- Leader: [[NPC]]
- Power base: [Military/Noble/Religious/etc.]
- Goals beyond succession: [What they want]
- Methods: [Legitimate/Underhanded]

**[[Faction B]] - Supports [[Heir 2]]**
[Same structure]

### Crisis Potential
**Likelihood:** [Imminent/High/Moderate/Low]

**If Ruler Dies Today:**
- Peaceful transition: [% chance]
- Civil war: [% chance]
- External intervention: [Who might involve themselves]

**Potential Outcomes:**
1. [Scenario 1]: [Consequences]
2. [Scenario 2]: [Consequences]
3. [Scenario 3]: [Consequences]

### Adventure Hooks
- [PC involvement in succession politics]
```

### Step 7: Create Power Brokers

NPCs who influence politics without ruling:

**Power Broker Types:**
1. **Spymaster** - Controls information
2. **Treasurer** - Controls wealth
3. **General** - Controls military
4. **High Priest** - Controls faith
5. **Guildmaster** - Controls commerce
6. **Dowager** - Controls through family
7. **Advisor** - Controls through counsel
8. **Fixer** - Controls through connections

**For each power broker:**
1. Read Support Character or Antagonist template
2. Generate with:
   - Source of power
   - Network of influence
   - Goals and methods
   - Relationships with rulers
   - Secrets and vulnerabilities
3. Save to Characters folder

```markdown
### [[Power Broker Name]]

**Title:** [Official position]
**True Role:** [How they actually wield power]
**Based in:** [[Location]]

**Power Sources:**
- [Source 1]: [How it gives them power]
- [Source 2]: [How it gives them power]

**Network:**
- Controls: [[Organization/people]]
- Influences: [[Rulers/decisions]]
- Information on: [What they know]

**Goals:**
- Short-term: [Current objective]
- Long-term: [Ultimate aim]

**Methods:**
- [How they operate]
- Willing to: [Lines they'll cross]
- Won't do: [Lines they won't cross]

**Relationships:**
| With | Nature | Notes |
|------|--------|-------|
| [[Ruler]] | [Relationship] | [Details] |
| [[Rival]] | [Relationship] | [Details] |

**Vulnerabilities:**
- [Weakness 1]
- [Weakness 2]

**If Removed:**
[What changes in political landscape]

**Adventure Hooks:**
- [How PCs might encounter them]
```

### Step 8: Map Internal Political Factions

For each major power, detail internal divisions:

```markdown
## Internal Politics: [[Power Name]]

### Court Factions

#### [[Faction Name 1]]
**Philosophy:** [Core political belief]
**Leader:** [[NPC]]
**Members:** [Key supporters]
**Power Base:** [Noble houses/Military/Church/etc.]

**Policies They Support:**
- [Policy 1]
- [Policy 2]

**Policies They Oppose:**
- [Policy 1]
- [Policy 2]

**Current Influence:** [High/Moderate/Low]
**Relationship with Ruler:** [Favored/Neutral/Disfavored]

**Rivals:** [[Other Faction]]
**Methods:** [How they pursue power]

---

### Current Political Issues

| Issue | [[Faction A]] | [[Faction B]] | Ruler's Position |
|-------|---------------|---------------|------------------|
| [Issue 1] | [Stance] | [Stance] | [Stance] |
| [Issue 2] | [Stance] | [Stance] | [Stance] |
| [Issue 3] | [Stance] | [Stance] | [Stance] |

### Power Balance

```
Current Council/Court Composition:

[[Faction A]]: ████████░░ (40%)
[[Faction B]]: ██████░░░░ (30%)
[[Faction C]]: ████░░░░░░ (20%)
Independents: ██░░░░░░░░ (10%)
```

### Upcoming Decisions
- [Decision 1]: [Stakes and positions]
- [Decision 2]: [Stakes and positions]
```

### Step 9: Identify Flashpoints

Locations and issues that could spark conflict:

```markdown
## Political Flashpoints

### [[Flashpoint 1 Name]]

**Type:** [Territorial/Religious/Economic/Ethnic]
**Location:** [[Region/Settlement]]
**Parties:** [[Power A]], [[Power B]]

**The Issue:**
[Clear description of the dispute]

**Current Status:**
[Tense peace/Minor skirmishes/Diplomatic standoff]

**Historical Context:**
[Why this is contentious]

**Recent Developments:**
- [Event 1]
- [Event 2]

**Escalation Triggers:**
- [What could start a war]
- [What could start a war]

**De-escalation Possibilities:**
- [What could resolve this peacefully]

**If Violence Erupts:**
- First moves: [What happens]
- Likely spread: [How it expands]
- Duration: [How long it might last]

**Key Figures:**
- [[NPC 1]]: [Their role - hawk/dove/profiteer]
- [[NPC 2]]: [Their role]

**Adventure Hooks:**
- [Prevention mission]
- [Escalation mission]
- [Profiteering opportunity]
```

### Step 10: Create Diplomatic Infrastructure

```markdown
## Diplomatic Systems

### Neutral Meeting Grounds

**[[Location Name]]**
- Status: [Sacred neutral / Treaty-designated / Traditional]
- Controlled by: [[Neutral party]]
- Used for: [Negotiations, summits, etc.]
- Rules: [Conduct requirements]

### Diplomatic Conventions

**Ambassador Rights:**
- [Immunity, privileges]
- [Violations and consequences]

**Declaration of War:**
- [Traditional method]
- [Required notifications]

**Peace Negotiations:**
- [Traditional mediators]
- [Customary processes]

### Active Embassies

| Power | In [[Capital A]] | In [[Capital B]] | In [[Capital C]] |
|-------|------------------|------------------|------------------|
| [[A]] | - | [[Ambassador]] | [[Ambassador]] |
| [[B]] | [[Ambassador]] | - | None |
| [[C]] | [[Ambassador]] | None | - |

### Current Diplomatic Missions

**[[Mission Name]]**
- Objective: [What's being negotiated]
- Parties: [[Involved powers]]
- Lead Negotiator: [[NPC]]
- Progress: [Stalled/Advancing/Near completion]
- Obstacles: [What's blocking agreement]
```

### Step 11: Document Recent Political History

```markdown
## Recent Political Timeline

### Last 10 Years

| Year | Event | Powers Affected | Consequence |
|------|-------|-----------------|-------------|
| [Y-10] | [Event] | [[Powers]] | [What changed] |
| [Y-8] | [Event] | [[Powers]] | [What changed] |
| [Y-5] | [Event] | [[Powers]] | [What changed] |
| [Y-2] | [Event] | [[Powers]] | [What changed] |
| [Y-1] | [Event] | [[Powers]] | [What changed] |
| [Now] | [Current situation] | - | - |

### Trend Analysis

**Rising Powers:**
- [[Power]]: [Why they're ascending]

**Declining Powers:**
- [[Power]]: [Why they're falling]

**Emerging Threats:**
- [Threat]: [Nature and timeline]

**Shifting Alliances:**
- [Description of realignment]
```

### Step 12: Update World Files

1. **Update World Overview** with political summary
2. **Add politics sections** to each government
3. **Create new NPC files** for power brokers
4. **Update or create treaty entities** in History
5. **Add succession info** to dynasties
6. **Connect NPCs** to political roles
7. **Update settlements** with political significance

### Step 13: Summary Report

```
=== POLITICS GENERATION COMPLETE: [World Name] ===

ALLIANCE WEB:
- [X] formal alliances documented
- [Y] informal alignments noted
- [Z] powers mapped in network

CONFLICTS:
- Hot Wars: [X]
- Cold Wars: [Y]
- Rivalries: [Z]
- Flashpoints: [W]

TREATIES: [X]
- [[Treaty 1]] - [Type]
- [[Treaty 2]] - [Type]

SUCCESSION ANALYSIS:
| Power | Stability | Crisis Risk |
|-------|-----------|-------------|
| [[A]] | [Stable/Unstable] | [High/Med/Low] |
| [[B]] | [Stable/Unstable] | [High/Med/Low] |

POWER BROKERS CREATED: [X]
- [[NPC 1]] - [Type]
- [[NPC 2]] - [Type]

INTERNAL FACTIONS:
- [X] governments analyzed
- [Y] factions documented

DIPLOMATIC INFRASTRUCTURE:
- Embassies mapped
- Conventions documented
- Neutral grounds identified

Files Created: [X]
Files Updated: [Y]

Political Complexity: [Simple/Moderate/Complex/Byzantine]

Suggested Next Steps:
- Develop [[Flashpoint]] into adventure
- Create intrigue around [[Succession]]
- Use [[Power Broker]] as patron/antagonist
- Explore [[Faction]] conflict as backdrop
- Stage [[Treaty]] negotiation session
```

## Quality Guidelines

1. **Balance of Power** - No single overwhelming force (unless intentional)
2. **Historical Logic** - Alliances/enmities have reasons
3. **Character-Driven** - Politics happens through people
4. **Dynamic Potential** - Situations can change
5. **Adventure Integration** - PCs can affect outcomes
6. **Multiple Scales** - International to court intrigue
7. **Realistic Complexity** - Not too simple, not too tangled

## Examples

```
# Generate politics for a world
/generate-politics "Eldermyr"

# Focus on specific aspect
/generate-politics "The Crownlands" --focus "succession"

# Analyze specific relationship
/generate-politics "Valdros" --focus "[[Kingdom A]] vs [[Kingdom B]]"
```
