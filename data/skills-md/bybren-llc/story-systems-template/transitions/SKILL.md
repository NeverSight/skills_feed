---
name: transitions
wtfbId: wtfb:transitions
description: |
  This skill provides screenplay transition formatting and conventions.
  Covers CUT TO, DISSOLVE TO, FADE IN/OUT, SMASH CUT, and when to use
  (or avoid) transitions for pacing and story effect.

  Use when: adding scene transitions, formatting transition elements,
  understanding transition conventions, or controlling pacing.
---

# Transitions Skill

## Invocation Triggers
Apply this skill when:
- Adding scene transitions
- Formatting transition elements
- Understanding transition conventions
- Controlling pacing through transitions

## Transition Format

### Standard Transitions
Transitions are uppercase, ending in `TO:`, with blank lines before and after:

```fountain
INT. OFFICE - DAY

Sarah sets down the phone.

                                                      CUT TO:

EXT. STREET - NIGHT

Rain falls on empty sidewalks.
```

### Forced Transitions
Force any line as a transition with `>`:
```fountain
>FADE TO BLACK.

>SMASH CUT TO:

>MATCH CUT TO:
```

## Common Transitions

### Standard Cuts
| Transition | Usage |
|------------|-------|
| `CUT TO:` | Standard scene change |
| `SMASH CUT TO:` | Abrupt, jarring cut |
| `MATCH CUT TO:` | Visual match between scenes |
| `JUMP CUT TO:` | Time jump, same location |
| `INTERCUT:` | Alternating between locations |

### Fade Transitions
| Transition | Usage |
|------------|-------|
| `FADE IN:` | Opening of script |
| `FADE OUT.` | End of script/act |
| `FADE TO:` | Slow transition |
| `FADE TO BLACK.` | Fade to darkness |
| `FADE TO WHITE.` | Fade to white |

### Dissolve Transitions
| Transition | Usage |
|------------|-------|
| `DISSOLVE TO:` | Soft transition, time passage |
| `RIPPLE DISSOLVE TO:` | Dream/memory transition |
| `CROSS DISSOLVE TO:` | Overlapping dissolve |

### Time Transitions
| Transition | Usage |
|------------|-------|
| `TIME CUT:` | Same location, time jump |
| `LATER:` | Time passage indication |
| `CONTINUOUS:` | No time break |

## When to Use Transitions

### Modern Convention: Less is More
In modern screenwriting, most transitions are **implied**. A new scene heading creates a cut automatically.

**Use transitions sparingly:**
- End of major sequences or acts
- Deliberate stylistic choice
- When the type of cut matters to the story

### When Transitions Add Value

**End of Acts:**
```fountain
Sarah stares at the evidence. Everything she believed was a lie.

                                                      FADE OUT.

                                                      END OF ACT ONE
```

**Jarring Juxtaposition:**
```fountain
JOHN
I'll never leave you.

                                                      SMASH CUT TO:

INT. DIVORCE COURT - DAY

John signs the papers.
```

**Visual Matching:**
```fountain
Sarah's eye fills the frame.

                                                      MATCH CUT TO:

The moon, full and pale, hangs over the city.
```

**Dream/Memory Sequence:**
```fountain
Sarah closes her eyes.

                                                      RIPPLE DISSOLVE TO:

INT. CHILDHOOD HOME - DAY (FLASHBACK)
```

### When NOT to Use Transitions

**Between normal scenes:**
```fountain
// Wrong - unnecessary
INT. OFFICE - DAY

Sarah works at her desk.

                                                      CUT TO:

INT. COFFEE SHOP - DAY

She meets John for lunch.
```

```fountain
// Right - implied cut
INT. OFFICE - DAY

Sarah works at her desk.

INT. COFFEE SHOP - DAY

She meets John for lunch.
```

## Special Transition Patterns

### Intercut
```fountain
INT. SARAH'S APARTMENT - NIGHT

Sarah paces with her phone.

INT. JOHN'S OFFICE - SAME

John answers.

INTERCUT - PHONE CONVERSATION

SARAH
We need to talk.

JOHN
I'm listening.
```

### Pre-lap
Audio from next scene starts before we cut:
```fountain
JOHN (PRE-LAP)
Sarah? Sarah, can you hear me?

                                                      CUT TO:

INT. HOSPITAL ROOM - DAY

Sarah's eyes flutter open.
```

### Flash Cut
Very brief shots:
```fountain
FLASH CUT:

- A face in the crowd
- The gun
- Sarah's hands, shaking

BACK TO SCENE
```

## Opening and Closing

### Script Opening
```fountain
FADE IN:

EXT. SEOUL - NIGHT

The city glitters in the rain.
```

### Script Closing
```fountain
Sarah walks into the light.

                                                      FADE OUT.

                                                      THE END
```

### Act Breaks (Television)
```fountain
Sarah discovers the body.

                                                      FADE OUT.

                                                      END OF ACT TWO

                                                      ACT THREE

FADE IN:

INT. POLICE STATION - DAY
```

## Validation Checklist
- [ ] Transitions are uppercase
- [ ] Standard transitions end in `TO:` or `.`
- [ ] Blank line before transition
- [ ] Transitions are right-aligned (handled by Fountain)
- [ ] Used sparingly, only when necessary
- [ ] FADE IN: at script start
- [ ] FADE OUT. at script/act end
- [ ] Forced transitions use `>` prefix
