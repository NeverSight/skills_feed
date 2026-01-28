---
name: continuity-tracking
wtfbId: wtfb:continuity-tracking
description: |
  This skill provides screenplay continuity tracking systems and templates.
  Covers character registry, timeline registry, location registry, prop
  registry, and wardrobe registry for maintaining story consistency.

  Use when: setting up tracking systems, checking consistency, managing
  timelines, or tracking characters, props, and locations across scenes.
---

# Continuity Tracking Skill

## Invocation Triggers
Apply this skill when:
- Setting up tracking systems
- Checking consistency
- Managing timeline
- Tracking characters and props

## Tracking Systems Overview

### Core Tracking Databases
| Database | Tracks |
|----------|--------|
| **Character Registry** | Physical details, knowledge, relationships |
| **Timeline Registry** | Story chronology, scene timing |
| **Location Registry** | Settings, geography, descriptions |
| **Prop Registry** | Important objects, ownership, status |
| **Wardrobe Registry** | Costume tracking per scene |

## Character Registry

### Template
```markdown
## Character Registry: [SCREENPLAY]

### [CHARACTER NAME]

#### Basic Info
- **Full Name:** [name]
- **First Appearance:** Scene [X], Page [Y]
- **Age:** [range]
- **Role:** [protagonist/antagonist/supporting]

#### Physical Description
- **Hair:** [description]
- **Build:** [description]
- **Distinguishing Features:** [list]
- **Notes:** [production-relevant details]

#### Wardrobe Log
| Scene | Page | Costume | Notes |
|-------|------|---------|-------|
| 1 | 1 | Black suit, white shirt | Intro |
| 5 | 12 | Same | Continuous |
| 6 | 15 | Casual jeans, t-shirt | Next day |

#### Knowledge State
Tracks what character knows at each point:
| By Scene | Knows | Doesn't Know |
|----------|-------|--------------|
| 1 | Normal life | The conspiracy |
| 10 | Father is alive | Where he is |
| 20 | Location revealed | True identity |

#### Relationship Map
| Character | Relationship | Evolution |
|-----------|--------------|-----------|
| SARAH | Ex-wife | Hostile → Allied (Sc. 25) |
| JOHN | Partner | Trusted → Betrayed (Sc. 40) |

#### Arc Tracking
| Act | Internal State | Evidence |
|-----|---------------|----------|
| 1 | Distrustful | Refuses help |
| 2 | Opening up | Accepts Sarah's aid |
| 3 | Transformed | Trusts completely |
```

## Timeline Registry

### Template
```markdown
## Timeline Registry: [SCREENPLAY]

### Story Span
- **Begins:** [Day 1, Morning]
- **Ends:** [Day 7, Night]
- **Total Duration:** [7 days]

### Chronological Breakdown

#### Day 1 (Monday)
| Scene | Time | Location | Duration |
|-------|------|----------|----------|
| 1 | Morning | Apartment | 2 min |
| 2 | Morning | Street | 1 min |
| 3 | Midday | Office | 5 min |

#### Day 2 (Tuesday)
| Scene | Time | Location | Duration |
|-------|------|----------|----------|
| 10 | Dawn | Rooftop | 3 min |
| 11 | Morning | Hospital | 5 min |

### Non-Linear Elements

#### Flashbacks
| Scene | Present Day | Flashback To | Purpose |
|-------|------------|--------------|---------|
| 15 | Day 3 | 10 years ago | Reveal wound |
| 30 | Day 5 | Day 1 (new angle) | Revelation |

#### Flash-forwards
| Scene | From | To | Purpose |
|-------|------|-----|---------|
| 1 | Day 1 | Day 7 | Hook |

### Time Validation
- [ ] No impossible jumps
- [ ] Travel times realistic
- [ ] Continuous scenes consistent
- [ ] Day/night matches headings
```

## Location Registry

### Template
```markdown
## Location Registry: [SCREENPLAY]

### [LOCATION NAME]

#### Details
- **First Appearance:** Scene [X], Page [Y]
- **Type:** INT / EXT / INT./EXT.
- **Real or Fictional:** [answer]
- **Time Zone:** [if relevant]

#### Description
[Key visual details established in script]

#### Geography
- **Relative to:** [other locations]
- **Travel time from [X]:** [duration]
- **Access:** [how characters arrive]

#### Scene Usage
| Scene | Time | Characters Present |
|-------|------|-------------------|
| 3 | DAY | Sarah, John |
| 15 | NIGHT | Sarah alone |
| 40 | DAY | Full cast |

#### Continuity Notes
- [Specific details to maintain]
- [Elements established that must persist]
```

## Prop Registry

### Template
```markdown
## Prop Registry: [SCREENPLAY]

### [PROP NAME]

#### Details
- **First Appearance:** Scene [X], Page [Y]
- **Owner:** [CHARACTER]
- **Significance:** [plot/character/thematic]

#### Tracking
| Scene | Page | Status | Location | Notes |
|-------|------|--------|----------|-------|
| 5 | 12 | Introduced | Sarah's pocket | Gift from father |
| 20 | 45 | Used | Office | Opens safe |
| 35 | 78 | Destroyed | Warehouse | Fire |

#### Related Props
- [Other props connected to this one]

### Critical Props List
| Prop | Intro | Status | Significance |
|------|-------|--------|--------------|
| Locket | Sc. 5 | Active | Plot key |
| Gun | Sc. 10 | Fired Sc. 50 | Chekhov's gun |
| Letter | Sc. 1 | Destroyed Sc. 40 | Mcguffin |
```

## Continuity Checklist

### Per Scene
- [ ] Time of day matches heading
- [ ] Characters present have reason to be there
- [ ] Props present were previously established
- [ ] Wardrobe consistent with timeline
- [ ] Character knowledge appropriate
- [ ] Weather consistent (if established)

### Per Sequence
- [ ] CONTINUOUS scenes flow correctly
- [ ] Time passage makes sense
- [ ] Locations reachable in time
- [ ] Character positions track

### Per Act
- [ ] Timeline progresses logically
- [ ] Character arcs advance appropriately
- [ ] No contradictions with earlier acts
- [ ] Subplots maintain consistency

### Full Script
- [ ] Character registry complete
- [ ] Timeline validated
- [ ] All props tracked
- [ ] Locations consistent
- [ ] No orphaned setups (Chekhov's gun)

## Common Continuity Errors

### Timeline Errors
| Error | Example | Fix |
|-------|---------|-----|
| Impossible travel | NYC to LA in 2 hours | Add time passage |
| Wrong time of day | NIGHT after DAY-CONTINUOUS | Correct heading |
| Seasonal jump | Summer to snow, no time | Add time marker |

### Character Errors
| Error | Example | Fix |
|-------|---------|-----|
| Wrong knowledge | Knows before told | Adjust scene order |
| Wardrobe jump | Suit to casual, same time | Add scene for change |
| Location error | Character in wrong place | Fix or explain |

### Prop Errors
| Error | Example | Fix |
|-------|---------|-----|
| Orphaned setup | Gun shown, never used | Use or remove |
| Magic appearance | Prop appears, no intro | Add introduction |
| Wrong status | Destroyed prop reappears | Track status |

## Quick Validation Commands

### Character Check
For each major character:
1. List all scenes they appear in
2. Verify timeline possibility
3. Check knowledge at each point
4. Verify wardrobe changes have opportunity

### Prop Check
For each significant prop:
1. Note introduction scene
2. Track every appearance
3. Verify final status
4. Check for unused setups

### Timeline Check
1. Build linear timeline
2. Plot all scenes
3. Verify no impossibilities
4. Check flashback consistency
