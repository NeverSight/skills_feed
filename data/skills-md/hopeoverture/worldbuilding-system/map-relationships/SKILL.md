---
name: map-relationships
description: Visualize and expand the relationship network around an entity - allies, enemies, debts, secrets, romantic connections, and power dynamics. Use when user wants to "map connections", "show relationships", or "visualize the network" around a character or organization.
argument-hint: "[entity name or path]"
---

# Map Relationships

Map relationships for: $ARGUMENTS

## Overview

Analyzes an entity and its connections, then:
1. Visualizes existing relationships as a network
2. Identifies missing or underdeveloped connections
3. Suggests new relationships to add depth
4. Creates relationship detail for existing links
5. Generates NPCs to fill network gaps
6. Documents secrets, debts, and hidden dynamics

## Instructions

### Step 1: Locate the Entity

1. **Parse `$ARGUMENTS`** for entity name or path
2. **Search across world folders:**
   - Characters
   - Organizations
   - Settlements
   - Any entity type can have relationships
3. **Read the entity file** completely
4. **Identify the world** it belongs to

### Step 2: Scan for Existing Connections

1. **Extract all wikilinks** from the entity file
2. **Read each linked entity** to understand the relationship
3. **Check for reciprocal links** (does the linked entity link back?)
4. **Categorize relationships** by type

**Relationship Types:**
- **Family:** Parent, child, sibling, spouse, extended
- **Professional:** Employer, employee, colleague, rival
- **Social:** Friend, acquaintance, enemy
- **Romantic:** Partner, lover, ex, unrequited
- **Political:** Ally, rival, vassal, lord
- **Economic:** Debtor, creditor, business partner
- **Religious:** Mentor, follower, heretic
- **Secret:** Hidden connection, blackmailer, conspirator

### Step 3: Build Relationship Map

Present the current network:

```
=== RELATIONSHIP MAP: [Entity Name] ===

Type: [Character/Organization/Settlement]
World: [[World Name]]

CURRENT CONNECTIONS: [X] entities

┌─────────────────────────────────────────┐
│           RELATIONSHIP WEB              │
├─────────────────────────────────────────┤
│                                         │
│           ┌──────────────┐              │
│           │              │              │
│   [[A]]───┤  [ENTITY]    ├───[[B]]      │
│   (ally)  │              │   (enemy)    │
│           └──────┬───────┘              │
│                  │                      │
│             [[C]] (family)              │
│                                         │
└─────────────────────────────────────────┘

CATEGORIZED CONNECTIONS:

Family & Blood:
- [[Name]] - [Relationship] [↔ reciprocal / → one-way]

Professional & Political:
- [[Name]] - [Relationship] [↔ / →]

Social & Personal:
- [[Name]] - [Relationship] [↔ / →]

Enemies & Rivals:
- [[Name]] - [Relationship] [↔ / →]

Organizations:
- [[Org]] - [Member/Leader/etc.] [↔ / →]

Locations:
- [[Place]] - [Connection type] [↔ / →]

NETWORK ANALYSIS:

Strengths:
- [Well-connected to organizations]
- [Strong family network]

Gaps Identified:
- No romantic connections defined
- Missing enemy/rival relationships
- Lacks connection to [[Important Entity]]
- One-way links need reciprocation

Suggested Expansions:
1. Add [relationship type] to [entity/new NPC]
2. Create [type] NPC to fill [gap]
3. Develop existing connection to [[Entity]]
```

### Step 4: Relationship Detail Template

For each significant relationship, create or expand detail:

```markdown
### [[Related Entity Name]]

**Relationship Type:** [Category from above]
**Status:** [Active/Strained/Broken/Complicated/Secret]
**Duration:** [How long this has existed]
**Origin:** [How the relationship started]

**From [Entity]'s Perspective:**
- [How they view the other]
- [What they want from the relationship]
- [What they'd do for/against them]

**From [[Related Entity]]'s Perspective:**
- [How they view the entity]
- [What they want]
- [Their commitment level]

**History:**
- [Key moment 1 that shaped the relationship]
- [Key moment 2]
- [Recent development]

**Secrets:**
- [What [Entity] hides from them]
- [What they hide from [Entity]]
- [What neither knows]

**Tension Points:**
- [Source of conflict 1]
- [Potential future conflict]

**Adventure Hooks:**
- [How PCs might encounter this relationship]
- [How this could become a quest]
```

### Step 5: Generate Missing Connections

Based on entity type, suggest and create appropriate relationships:

**For Characters:**

| Gap Type | Suggested NPC | Relationship |
|----------|---------------|--------------|
| No family | Parent/Sibling | Blood relation |
| No mentor | Older professional | Taught them skills |
| No rival | Peer competitor | Professional jealousy |
| No enemy | Wronged party | Seeks revenge |
| No love interest | Appropriate match | Romantic potential |
| No friend | Trusted confidant | Personal support |
| No secret | Hidden contact | Clandestine dealings |

**For Organizations:**

| Gap Type | Suggested Entity | Relationship |
|----------|------------------|--------------|
| No rival | Competing org | Same space, different approach |
| No ally | Complementary org | Mutual benefit |
| No enemy | Opposing org | Fundamental conflict |
| No patron | Powerful backer | Funding/protection |
| No front | Legitimate cover | For illegal activities |
| No target | Victim org | Object of schemes |

**For Settlements:**

| Gap Type | Suggested Entity | Relationship |
|----------|------------------|--------------|
| No rival city | Nearby settlement | Competition for resources |
| No ally | Trading partner | Economic interdependence |
| No threat | Enemy power | External danger |
| No protector | Military force | Defense relationship |

### Step 6: Relationship Intensity Scale

Document the strength of each relationship:

```markdown
## Relationship Intensity

| Entity | Type | Intensity | Direction | Notes |
|--------|------|-----------|-----------|-------|
| [[A]] | Ally | ████░ (4/5) | Mutual | Would die for each other |
| [[B]] | Rival | ███░░ (3/5) | Mutual | Competitive but respectful |
| [[C]] | Enemy | █████ (5/5) | One-way | C doesn't know they're hated |
| [[D]] | Family | ██░░░ (2/5) | Mutual | Estranged, rarely speak |
| [[E]] | Lover | ████░ (4/5) | Uncertain | E's feelings unknown |

### Intensity Scale:
- █░░░░ (1/5): Acquaintance, minimal investment
- ██░░░ (2/5): Casual, some interaction
- ███░░ (3/5): Significant, regular interaction
- ████░ (4/5): Deep, major life influence
- █████ (5/5): Defining, would kill/die for
```

### Step 7: Power Dynamics

Analyze who has power over whom:

```markdown
## Power Dynamics

### [Entity] Has Power Over:
| Target | Type of Power | Leverage |
|--------|---------------|----------|
| [[A]] | Economic | Owes significant debt |
| [[B]] | Political | Controls their appointment |
| [[C]] | Secret | Knows compromising information |
| [[D]] | Emotional | Loved one's loyalty |

### Others Have Power Over [Entity]:
| Source | Type of Power | Leverage |
|--------|---------------|----------|
| [[X]] | Economic | Controls their income |
| [[Y]] | Political | Could expose crimes |
| [[Z]] | Social | Reputation depends on them |

### Mutual Power Balance:
| Entity | Their Power | [Entity]'s Power | Balance |
|--------|-------------|------------------|---------|
| [[M]] | [Leverage] | [Counter-leverage] | Even |
| [[N]] | [Leverage] | [Counter-leverage] | N favored |
```

### Step 8: Secrets & Hidden Relationships

Document what's not publicly known:

```markdown
## Hidden Relationships

### Secret Allies
- [[Hidden Ally]]: [Why it's secret, what they do]

### Secret Enemies
- [[Hidden Enemy]]: [Why it's secret, their plot]

### Secret Connections
- [[Secret Contact]]: [Nature of secret relationship]

### Things [Entity] Knows
| About | Secret | Would Use? |
|-------|--------|------------|
| [[A]] | [What they know] | [Yes/No - why] |
| [[B]] | [What they know] | [Yes/No - why] |

### Things Others Know About [Entity]
| Who Knows | Secret | Threat Level |
|-----------|--------|--------------|
| [[X]] | [The secret] | [High/Medium/Low] |
| [[Y]] | [The secret] | [High/Medium/Low] |

### Unknown Connections
Things no one knows yet that could be revealed:
- [Potential reveal 1]
- [Potential reveal 2]
```

### Step 9: Debts & Obligations

Track what's owed:

```markdown
## Debts & Obligations

### [Entity] Owes
| To Whom | Type | Details | Due |
|---------|------|---------|-----|
| [[A]] | Gold | [Amount] | [When] |
| [[B]] | Favor | [Description] | [Open] |
| [[C]] | Life debt | [Circumstance] | [Never paid] |
| [[D]] | Promise | [What was promised] | [Condition] |

### Owed to [Entity]
| From Whom | Type | Details | Collectible? |
|-----------|------|---------|--------------|
| [[X]] | Gold | [Amount] | [Yes/No] |
| [[Y]] | Service | [Description] | [When convenient] |
| [[Z]] | Honor debt | [Circumstance] | [Must respond if called] |

### Contested Debts
- [[Party]]: [What's disputed and why]
```

### Step 10: Relationship History Timeline

```markdown
## Relationship Timeline

| Year/Age | Event | With | Impact |
|----------|-------|------|--------|
| [Early] | [First meeting with [[A]]] | [[A]] | Began friendship |
| [Time] | [Conflict with [[B]]] | [[B]] | Created rivalry |
| [Time] | [Married [[C]]] | [[C]] | Gained family connections |
| [Time] | [Betrayed by [[D]]] | [[D]] | Trust broken |
| [Recent] | [Alliance with [[E]]] | [[E]] | New ally |
| [Current] | [Tension with [[F]]] | [[F]] | Relationship strained |

### Turning Points
- **[Event 1]:** Changed relationship with [[Entity]] from [before] to [after]
- **[Event 2]:** Changed relationship with [[Entity]] from [before] to [after]
```

### Step 11: Generate New NPCs

For each identified gap, create NPCs:

1. **Read appropriate character template**
2. **Generate with:**
   - Relationship to central entity clearly defined
   - Their own goals and personality (not just a relationship prop)
   - At least one other connection in the world
   - Potential for story development
3. **Save to Characters folder**
4. **Update both entity files** with bidirectional links

### Step 12: Create Relationship Diagram File

For complex webs, create a dedicated file:

```markdown
# Relationships of [Entity Name]

*This file maps the social network around [[Entity Name]].*

## Visual Map
[Text-based diagram or description for Obsidian graph view]

## Primary Circle
[5-8 most important relationships]

## Secondary Circle
[Extended network]

## Hostile Network
[Enemies and their allies]

## Hidden Network
[Secret connections]

## Historical Connections
[Past relationships, deceased or estranged]
```

### Step 13: Update All Connected Entities

1. **Add relationship sections** to entity file
2. **Update each linked entity** with reciprocal information
3. **Create new NPC files** for generated characters
4. **Add relationship notes** to relevant organization files
5. **Cross-reference** in settlement files where relevant

### Step 14: Summary Report

```
=== RELATIONSHIP MAPPING COMPLETE: [Entity Name] ===

Network Analysis:

EXISTING CONNECTIONS: [X]
- Family: [X]
- Professional: [X]
- Social: [X]
- Political: [X]
- Romantic: [X]
- Secret: [X]

RECIPROCAL LINKS: [X/Y] fixed

NEW CONNECTIONS CREATED: [X]
- [[NPC 1]] - [Relationship type]
- [[NPC 2]] - [Relationship type]
- [[NPC 3]] - [Relationship type]

RELATIONSHIP DETAILS ADDED:
- [[Entity A]] - History and dynamics documented
- [[Entity B]] - History and dynamics documented

POWER DYNAMICS MAPPED:
- [Entity] has leverage over [X] entities
- [Y] entities have leverage over [Entity]
- [Z] mutual relationships

SECRETS DOCUMENTED:
- [X] secret relationships
- [Y] hidden knowledge entries
- [Z] blackmail opportunities

DEBTS TRACKED:
- [X] owed by Entity
- [Y] owed to Entity

Timeline: [X] events documented

Files Updated: [X]
Files Created: [X]

Network Density:
- Before: [X] connections
- After: [Y] connections
- Increase: [Z]%

Suggested Next Steps:
- Develop [[NPC]]'s story further
- Create encounter using [[Enemy]] relationship
- Explore [[Secret]] as adventure hook
- Map relationships for [[Connected Entity]]
```

## Quality Guidelines

1. **Bidirectionality** - Every relationship links both ways
2. **Asymmetry** - People often feel differently about each other
3. **History** - Relationships have origins and evolution
4. **Secrets** - Most relationships have hidden elements
5. **Tension** - Even allies have friction points
6. **Stakes** - Relationships matter to the characters
7. **Playability** - Relationships create adventure hooks

## Examples

```
# Map a character's relationships
/map-relationships "Lord Varic Valdren"

# Map with path
/map-relationships Worlds/Eldermyr/Characters/Lady Seren.md

# Map an organization's relationships
/map-relationships "The Merchant's Guild"

# Focus on specific relationship type
/map-relationships "Captain Thorne" --focus enemies
```
