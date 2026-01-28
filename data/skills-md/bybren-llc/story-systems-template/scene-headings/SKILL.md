---
name: scene-headings
wtfbId: wtfb:scene-headings
description: |
  This skill provides Fountain scene heading formatting rules and conventions.
  Covers INT/EXT prefixes, location naming, time of day indicators,
  continuous scenes, and establishing shots.

  Use when: creating new scenes, formatting scene headings, managing
  location consistency, or organizing scene structure in Fountain format.
---

# Scene Headings Skill

## Invocation Triggers
Apply this skill when:
- Creating new scenes
- Formatting scene headings
- Managing location consistency
- Organizing scene structure

## Scene Heading Format

### Standard Structure
```
[INT/EXT]. [LOCATION] - [TIME OF DAY]
```

### Interior/Exterior Prefixes
| Prefix | Meaning | Usage |
|--------|---------|-------|
| `INT.` | Interior | Indoor scenes |
| `EXT.` | Exterior | Outdoor scenes |
| `INT./EXT.` | Both | Moving between (car scenes) |
| `INT/EXT` | Both | Alternate format |
| `I/E` | Both | Abbreviated format |
| `EST.` | Establishing | Establishing shots |

### Time of Day Options
| Time | Usage |
|------|-------|
| `DAY` | Standard daylight |
| `NIGHT` | Standard nighttime |
| `MORNING` | Early day, specific |
| `AFTERNOON` | Mid-day, specific |
| `EVENING` | Late day before dark |
| `DAWN` | Sunrise |
| `DUSK` | Sunset |
| `CONTINUOUS` | No time break from previous |
| `LATER` | Same location, time passed |
| `MOMENTS LATER` | Brief time passage |
| `SAME` | Same time as previous scene |

### Examples
```fountain
INT. COFFEE SHOP - DAY

EXT. MOUNTAIN ROAD - NIGHT

INT./EXT. CAR (MOVING) - CONTINUOUS

INT. SARAH'S APARTMENT - MORNING

EXT. CITY STREET - LATER

INT. HOSPITAL ROOM - SAME
```

## Location Best Practices

### Naming Conventions
- Use consistent names throughout script
- Be specific: "JOHN'S APARTMENT" not just "APARTMENT"
- Include relevant modifiers in parentheses

### Location Modifiers
```fountain
INT. CAR (MOVING) - DAY
INT. CAR (PARKED) - NIGHT
INT. WAREHOUSE (ABANDONED) - DAY
EXT. HOUSE (ESTABLISHING) - DAY
INT. PLANE (IN FLIGHT) - NIGHT
```

### Sub-locations
```fountain
INT. JOHN'S APARTMENT - LIVING ROOM - DAY
INT. JOHN'S APARTMENT - BEDROOM - CONTINUOUS
INT. HOSPITAL - HALLWAY - NIGHT
INT. HOSPITAL - SARAH'S ROOM - CONTINUOUS
```

## Special Scene Headings

### Flashbacks/Flash-forwards
```fountain
INT. CHILDHOOD HOME - DAY (FLASHBACK)

INT. CHILDHOOD HOME - DAY (1985)

EXT. CITY STREET - DAY (TWENTY YEARS EARLIER)

INT. OFFICE - DAY (FLASH-FORWARD)
```

### Dream/Fantasy Sequences
```fountain
INT. SURREAL LANDSCAPE - NIGHT (DREAM)

INT. PALACE - DAY (FANTASY)

INT. SARAH'S MIND - TIMELESS
```

### Forcing Non-Standard Headings
Use `.` prefix to force any line as scene heading:
```fountain
.MONTAGE - SARAH'S TRAINING

.FLASHBACK SEQUENCE

.SERIES OF SHOTS

.INTERCUT - PHONE CONVERSATION
```

## Scene Numbers

### Format
```fountain
INT. HOUSE - DAY #1#
INT. HOUSE - NIGHT #2#
INT. GARDEN - DAY #2A#
```

### Usage Guidelines
- **Spec scripts**: Do NOT include scene numbers
- **Shooting scripts**: Include scene numbers
- Numbers appear at both margins in output
- Use letters for inserted scenes (#2A#, #2B#)

## Common Patterns

### Continuous Action
```fountain
INT. HALLWAY - DAY

Sarah runs down the corridor.

INT. STAIRWELL - CONTINUOUS

She bursts through the door, taking stairs two at a time.

EXT. PARKING LOT - CONTINUOUS

Sarah emerges into bright sunlight.
```

### Intercut Scenes
```fountain
INT. SARAH'S APARTMENT - NIGHT

Sarah paces, phone to ear.

INT. JOHN'S OFFICE - SAME

John sits at his desk, phone in hand.

INTERCUT - PHONE CONVERSATION

SARAH
We need to talk.

JOHN
I'm listening.
```

### Montage
```fountain
.MONTAGE - SARAH'S INVESTIGATION

INT. LIBRARY - DAY
Sarah pores over old newspapers.

EXT. COURTHOUSE - DAY
Sarah photographs documents.

INT. BAR - NIGHT
Sarah interviews an old man.

.END MONTAGE
```

## Validation Checklist
- [ ] Prefix is INT., EXT., or valid variant
- [ ] Location is specific and consistent
- [ ] Time of day is included
- [ ] Special scenes are properly forced with .
- [ ] Scene numbers only on shooting scripts
