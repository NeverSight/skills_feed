---
name: generate-economy
description: Generate economic systems including trade routes, resource nodes, merchant guilds, black markets, price variations, and commercial relationships. Use when user wants to add "trade routes", "economy", "commerce", or "merchant networks" to a world.
argument-hint: "[world name]"
---

# Generate Economy

Generate economic systems for: $ARGUMENTS

## Overview

Creates comprehensive economic infrastructure for a world including:
1. Trade routes connecting settlements
2. Resource extraction and production sites
3. Merchant guilds and trading companies
4. Black markets and smuggling networks
5. Price variations by region
6. Commercial relationships and trade agreements
7. Currency flow and economic powers
8. Market hubs and trade fairs

## Instructions

### Step 1: Survey the World

1. **Parse `$ARGUMENTS`** for world name
2. **Read World Overview** for:
   - Technology level
   - Geography layout
   - Major powers
   - Existing currencies
   - Known trade goods

3. **Scan Settlements:**
   - List all cities and towns
   - Note coastal vs. inland
   - Identify capitals and trade hubs

4. **Scan Geography:**
   - List regions and terrain
   - Identify natural resources implied
   - Note mountain passes, rivers, coasts

5. **Scan Organizations:**
   - Existing guilds
   - Governments (tax and trade policies)
   - Criminal organizations (smuggling)

### Step 2: Present Economic Development Plan

```
=== ECONOMY GENERATION: [World Name] ===

World Survey:
- Settlements: [X] cities, [Y] towns, [Z] villages
- Regions: [X] distinct areas
- Existing Trade Entities: [list]
- Currency: [[Currency Name]]

Proposed Economic System:

1. RESOURCE NODES ([X] to create)
   - [Region]: [Resource type]
   - [Region]: [Resource type]

2. TRADE ROUTES ([X] to create)
   Major:
   - [City A] ↔ [City B]: [Primary goods]
   - [City C] ↔ [City D]: [Primary goods]
   Minor:
   - [Town] → [City]: [Goods]

3. MERCHANT ORGANIZATIONS ([X] to create/expand)
   - [Guild/Company 1]: [Specialty]
   - [Guild/Company 2]: [Specialty]

4. TRADE HUBS ([X] to designate)
   - [[City 1]]: [Type of hub]
   - [[City 2]]: [Type of hub]

5. BLACK MARKETS ([X] if appropriate)
   - [Location 1]: [Illegal goods]
   - [Location 2]: [Illegal goods]

6. PRICE VARIATIONS
   - Regional differences explained
   - Seasonal fluctuations

7. TRADE RELATIONSHIPS
   - [[Nation A]] ↔ [[Nation B]]: [Terms]

Proceed? (yes/customize)
```

### Step 3: Identify and Create Resource Nodes

Map resources by region:

**Common Resource Types:**
| Category | Resources | Found In |
|----------|-----------|----------|
| **Metals** | Iron, copper, gold, silver, mithril | Mountains, hills |
| **Gems** | Diamonds, rubies, emeralds, opals | Mountains, caves |
| **Stone** | Marble, granite, limestone | Mountains, quarries |
| **Timber** | Oak, pine, exotic woods | Forests |
| **Agriculture** | Grain, vegetables, fruits | Plains, valleys |
| **Livestock** | Cattle, sheep, horses, exotic | Plains, hills |
| **Textiles** | Wool, silk, cotton, linen | Various |
| **Fish/Sea** | Fish, pearls, coral, salt | Coasts, rivers |
| **Exotic** | Spices, dyes, magical components | Jungles, specific |

**For each region, create resource section:**
```markdown
## Economic Resources: [[Region Name]]

### Primary Exports
| Resource | Extraction Site | Quality | Annual Output | Value |
|----------|-----------------|---------|---------------|-------|
| [Resource 1] | [[Location]] | [High/Med/Low] | [Amount] | [GP/unit] |
| [Resource 2] | [[Location]] | [High/Med/Low] | [Amount] | [GP/unit] |

### Secondary Resources
- [Resource]: [Notes on availability]

### Resource Control
- [[Organization/Government]]: Controls [resources]
- Rights disputes: [Contested resources]

### Extraction Sites
**[[Mine/Farm/etc. Name]]:**
- Location: [Specific place in region]
- Resource: [What's extracted]
- Workers: [Number, type]
- Controlled by: [[Entity]]
- Output: [Amount per season]
- Challenges: [Dangers, difficulties]
```

### Step 4: Create Trade Routes

Connect settlements with logical trade flows:

**Trade Route Principles:**
- Follow rivers where possible
- Pass through minimum mountain passes
- Connect production to consumption
- Build on existing roads

**For each major route:**
```markdown
### [Route Name] Trade Road

**Connects:** [[City A]] ↔ [[City B]]
**Distance:** [X] miles
**Travel Time:** [X] days by horse, [Y] days by wagon
**Route Type:** [Road/River/Sea/Caravan trail]

**Path:**
```
[[City A]] → [[Waypoint 1]] → [[Waypoint 2]] → [[City B]]
       (2 days)        (3 days)         (2 days)
```

**Primary Goods:**
| Direction | Goods | Volume | Season |
|-----------|-------|--------|--------|
| A → B | [Goods from A] | [Heavy/Moderate/Light] | [Year-round/Seasonal] |
| B → A | [Goods from B] | [Heavy/Moderate/Light] | [Year-round/Seasonal] |

**Route Control:**
- [[Government/Guild]]: Maintains and taxes
- Toll stations: [[Location 1]], [[Location 2]]
- Patrol frequency: [Description]

**Hazards:**
- [Hazard 1]: [Location, danger level]
- [Hazard 2]: [Location, danger level]
- Bandit activity: [Description]

**Services Along Route:**
| Waypoint | Services | Notable |
|----------|----------|---------|
| [[Stop 1]] | Inn, stables, smithy | [Hook/detail] |
| [[Stop 2]] | Caravansary | [Hook/detail] |

**Seasonal Variations:**
- Spring: [Conditions]
- Summer: [Conditions]
- Autumn: [Conditions]
- Winter: [Conditions - passable?]

**Adventure Hooks:**
- [Hook related to route]
```

**Sea Routes (if applicable):**
```markdown
### [Sea Route Name]

**Connects:** [[Port A]] ↔ [[Port B]]
**Distance:** [X] nautical miles
**Voyage Time:** [X] days favorable, [Y] days typical
**Season:** [When safe to sail]

**Navigation:**
- Follow coast / Open sea crossing
- Key landmarks: [Navigation points]
- Dangerous waters: [[Hazard area]]

**Common Cargo:**
[Same format as land routes]

**Vessels:**
- Typical ships: [Ship types]
- Fleet size: [Estimate]
- Notable ships: [[Ship Name]]

**Pirates/Threats:**
- [[Pirate Group]]: Active in [area]
- Sea monsters: [[Creature]] reported
```

### Step 5: Create/Expand Merchant Organizations

**Merchant Guild Types:**
1. **General Merchants' Guild** - All traders, broad power
2. **Specialty Guilds** - Single trade (goldsmiths, weavers, etc.)
3. **Trading Companies** - Long-distance trade, quasi-governmental
4. **Cartels** - Price-fixing groups
5. **Merchant Houses** - Family businesses with reach

**For each organization:**
1. Read `Templates/Organizations/Guild.md` or `Business.md`
2. Generate with:
   - Trade specialty
   - Territory/routes controlled
   - Key NPCs (3-5)
   - Relationship with government
   - Rivals and allies
   - Secret operations
3. Save to Organizations folder

**Economic Organization Section:**
```markdown
## Trade Operations

### Routes Controlled
- [[Route 1]]: [Monopoly/Major presence/Minor presence]
- [[Route 2]]: [Control level]

### Trade Posts
| Location | Type | Staff | Function |
|----------|------|-------|----------|
| [[City A]] | Headquarters | [X] | Main operations |
| [[City B]] | Warehouse | [X] | Storage/distribution |
| [[City C]] | Factor's office | [X] | Local trading |

### Annual Revenue
- Estimated: [X] gold pieces
- Primary source: [Trade type]
- Growth: [Increasing/Stable/Declining]

### Trade Agreements
- [[Organization 1]]: [Nature of agreement]
- [[Government]]: [Licenses, monopolies]

### Rivals
- [[Competitor]]: [Nature of competition]

### Illegal Activities
[If applicable - smuggling, price fixing, etc.]
```

### Step 6: Designate Trade Hubs

Identify and detail major commercial centers:

**Hub Types:**
- **Entrepôt** - Transshipment center, goods pass through
- **Production Hub** - Manufacturing center
- **Consumption Hub** - Wealthy buyer market
- **Market Town** - Regional distribution
- **Port** - Sea/river trade gateway

**For each hub, add to settlement file:**
```markdown
## Commerce & Trade

### Trade Hub Status: [Type]

**Economic Role:**
[2-3 sentences on the settlement's commercial importance]

### Markets

**The [[Market Name]]** (Main Market)
- Location: [District]
- Days: [When active]
- Size: [Stalls/capacity]
- Specialty: [What's primarily traded]
- Atmosphere: [Description]

**[[Secondary Market]]**
- Type: [Specialty market]
- Notable for: [Unique goods/services]

### Trade Facilities

| Facility | Location | Capacity | Operator |
|----------|----------|----------|----------|
| Main Warehouse District | [Area] | [Tons] | [[Guild]] |
| Customs House | [Location] | - | [[Government]] |
| Money Changers | [Location] | - | Various |
| Auction House | [Location] | - | [[Operator]] |

### Merchant Presence
| Organization | Office | Interests |
|--------------|--------|-----------|
| [[Guild 1]] | [[Building]] | [Trade focus] |
| [[Company 1]] | [[Building]] | [Trade focus] |

### Trade Laws
- Tariffs: [Rate on goods]
- Forbidden goods: [List]
- Market regulations: [Key rules]
- Dispute resolution: [How handled]

### Trade Calendar
| Event | When | Description |
|-------|------|-------------|
| [[Trade Fair]] | [Season] | [Major commercial event] |
| [Market Day] | [Weekly] | [Regular market] |
| [Auction] | [Frequency] | [What's sold] |
```

### Step 7: Create Black Markets

**If world has illegal goods, create underground economy:**

```markdown
## Black Market: [[Location]]

### The [Nickname/Name]

**Location:** [Where hidden]
**Operator:** [[Criminal Organization]]
**Access:** [How to find it, who knows]

### Illegal Goods Available
| Good | Source | Price | Risk |
|------|--------|-------|------|
| [Contraband 1] | [Origin] | [X gp] | [Danger level] |
| [Contraband 2] | [Origin] | [X gp] | [Danger level] |
| [Stolen goods] | Various | [% of value] | [Danger level] |

### Services
- Fencing stolen goods
- Forged documents
- Smuggling arrangements
- Information brokering
- [Other illegal services]

### Key Figures
- [[Fence NPC]]: Primary goods handler
- [[Broker NPC]]: Information and connections
- [[Muscle NPC]]: Security and enforcement

### Law Enforcement
- Awareness: [Unknown/Suspected/Known but tolerated/Actively hunted]
- [[Guard/Official]]: [Their involvement - corrupt, hunting, etc.]
- Raids: [Frequency, results]

### Smuggling Routes
- Into city: [Methods, routes]
- Out of city: [Methods, routes]
- Key chokepoints: [Where contraband is vulnerable]
```

### Step 8: Calculate Price Variations

Create regional pricing differences:

```markdown
## Regional Price Variations

### Base Prices
[Use standard D&D equipment prices as baseline]

### Regional Modifiers

| Region | Modifier | Reason |
|--------|----------|--------|
| [[Region 1]] | -20% on [goods] | Production center |
| [[Region 2]] | +50% on [goods] | Remote, imported |
| [[Region 3]] | +30% on all | Trade blockade |
| [[Region 4]] | -10% on food | Agricultural surplus |

### Specific Goods

**[[Resource/Good]]**
| Location | Price | Notes |
|----------|-------|-------|
| [[Production area]] | X gp (-30%) | Source |
| [[Trade hub]] | X gp (base) | Standard |
| [[Remote area]] | X gp (+50%) | Transport costs |
| [[Restricted area]] | X gp (+100%) | Illegal/taxed |

### Seasonal Variations
| Good | Season | Change | Reason |
|------|--------|--------|--------|
| Grain | Harvest | -30% | Abundance |
| Grain | Spring | +40% | Pre-harvest scarcity |
| Furs | Winter | -20% | Peak hunting |
| Furs | Summer | +30% | Off-season |

### Supply Disruption Scenarios
| Event | Affected Goods | Price Change | Duration |
|-------|----------------|--------------|----------|
| War | All | +20-50% | Duration of conflict |
| Drought | Food, animals | +50-100% | 1-2 years |
| Trade route blocked | Route goods | +100%+ | Until resolved |
| Monster infestation | Local goods | +30-50% | Until cleared |

### Adventure Hooks
- [Price spike as adventure hook]
- [Smuggling opportunity]
- [Trade war scenario]
```

### Step 9: Map Trade Relationships

Document inter-power commerce:

```markdown
## International Trade

### [[Nation A]] ↔ [[Nation B]]

**Trade Balance:** [A favored / B favored / Balanced]

**A Exports to B:**
| Good | Volume | Value | Notes |
|------|--------|-------|-------|
| [Good 1] | [Amount] | [GP/year] | [Details] |

**B Exports to A:**
| Good | Volume | Value | Notes |
|------|--------|-------|-------|
| [Good 1] | [Amount] | [GP/year] | [Details] |

**Trade Agreement:** [[Treaty Name]] (if exists)
- Terms: [Key provisions]
- Tariffs: [Rates]
- Disputes: [How resolved]

**Trade History:**
- [Historical context]
- [Past conflicts or cooperation]

**Current Tensions:**
- [Economic friction points]

---

### Trade Dependency Map

| Nation | Depends On | For | Vulnerability |
|--------|------------|-----|---------------|
| [[A]] | [[B]] | [Goods] | [High/Med/Low] |
| [[B]] | [[C]] | [Goods] | [High/Med/Low] |

### Embargo Scenarios
[What happens if trade is cut off between powers]
```

### Step 10: Create Trade Fairs & Markets

```markdown
## Major Trade Events

### [[Fair Name]] Fair

**Location:** [[City/Town]]
**Timing:** [Season/Month]
**Duration:** [X] days
**Frequency:** [Annual/Biannual/etc.]

**History:**
[Origin and significance]

**Attendance:**
- Merchants: [Estimate]
- Visitors: [Estimate]
- From: [Regions represented]

**Goods Traded:**
- Primary: [Main commodities]
- Specialty: [Unique offerings]
- Forbidden: [What's not allowed]

**Events & Activities:**
- [Trading event 1]
- [Competition/show]
- [Entertainment]
- [Ceremony]

**Fair Courts:**
- Disputes resolved by: [[Official/Guild]]
- Special fair laws: [Protections, rules]

**Fair Grounds:**
| Area | Purpose | Notable |
|------|---------|---------|
| [Area 1] | [Type of trading] | [Detail] |
| [Area 2] | [Type of trading] | [Detail] |

**Adventure Hooks:**
- [Hook 1]
- [Hook 2]
```

### Step 11: Update World Files

1. **Update World Overview** with economic summary
2. **Add trade sections** to each settlement
3. **Update region files** with resources
4. **Create new organization files** for guilds/companies
5. **Add trade route entities** as Road entities
6. **Update existing organizations** with economic roles
7. **Connect NPCs** to trade activities

### Step 12: Summary Report

```
=== ECONOMY GENERATION COMPLETE: [World Name] ===

RESOURCE NODES: [X]
Regions mapped with resources:
- [[Region 1]]: [Primary resources]
- [[Region 2]]: [Primary resources]

TRADE ROUTES: [X]
Major Routes:
- [[Route 1]]: [[City A]] ↔ [[City B]]
- [[Route 2]]: [[City C]] ↔ [[City D]]

Minor Routes: [Y] created

Sea Routes: [Z] created

MERCHANT ORGANIZATIONS: [X]
- [[Guild/Company 1]] - [Specialty]
- [[Guild/Company 2]] - [Specialty]

TRADE HUBS: [X] designated
- [[City 1]] - [Hub type]
- [[City 2]] - [Hub type]

BLACK MARKETS: [X] (if created)
- [[Location]] - [Contraband type]

TRADE FAIRS: [X]
- [[Fair 1]] at [[Location]]

PRICE VARIATIONS:
- [X] regional modifiers documented
- [Y] seasonal variations noted

TRADE RELATIONSHIPS:
- [X] international relationships mapped
- [Y] treaties/agreements referenced

NPCs CREATED: [X]
- Merchants: [X]
- Guild leaders: [X]
- Smugglers: [X]

Files Created: [X]
Files Updated: [X]

Economic Complexity Rating: [Simple/Moderate/Complex]

Suggested Next Steps:
- Create adventure around [[Trade Route]] dangers
- Develop [[Guild]] faction conflict
- Use [[Trade Fair]] as session setting
- Explore [[Black Market]] criminal network
- Create price disruption adventure hook
```

## Quality Guidelines

1. **Geographic Logic** - Trade follows terrain and water
2. **Economic Realism** - Supply and demand make sense
3. **Power Integration** - Economy ties to politics
4. **Adventure Potential** - Every element can be a quest
5. **NPC Connections** - Real people drive trade
6. **Historical Basis** - Economy reflects world history
7. **Conflict Sources** - Economic tensions create drama

## Examples

```
# Generate economy for a world
/generate-economy "Eldermyr"

# Focus on specific aspect
/generate-economy "Valdros" --focus "black markets"

# Expand existing trade
/generate-economy "The Northern Kingdoms" --focus "trade routes"
```
