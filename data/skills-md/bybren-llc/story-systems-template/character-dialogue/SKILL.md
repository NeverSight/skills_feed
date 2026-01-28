---
name: character-dialogue
wtfbId: wtfb:character-dialogue
description: |
  This skill provides Fountain format character and dialogue formatting rules.
  Covers character name formatting, extensions (V.O., O.S., CONT'D), dual
  dialogue, parentheticals, and proper dialogue block structure.

  Use when: introducing characters, writing dialogue blocks, formatting
  character names, handling dual dialogue, or using character extensions.
---

# Character & Dialogue Skill

## Invocation Triggers
Apply this skill when:
- Introducing characters
- Writing dialogue blocks
- Formatting character names
- Handling dual dialogue
- Using character extensions

## Character Name Format

### Basic Format
Character names must be:
- ALL UPPERCASE
- On their own line
- Preceded by a blank line
- Followed immediately by dialogue (no blank line)

```fountain

SARAH
Hello, John.
```

### Character Extensions
Extensions appear in parentheses after the name:

| Extension | Meaning | When to Use |
|-----------|---------|-------------|
| `(V.O.)` | Voice Over | Character narrating or not in scene |
| `(O.S.)` | Off Screen | Character in scene but not visible |
| `(O.C.)` | Off Camera | Same as O.S. (alternate) |
| `(CONT'D)` | Continued | Same speaker after action interruption |
| `(PRE-LAP)` | Pre-lap | Audio starts before scene |
| `(INTO PHONE)` | Delivery | Speaking into phone |
| `(INTO RADIO)` | Delivery | Speaking into radio |
| `(SUBTITLE)` | Translation | Foreign dialogue translated |

```fountain
SARAH (V.O.)
I never should have trusted him.

JOHN (O.S.)
Sarah? Are you home?

SARAH
In here!

She turns toward the door.

SARAH (CONT'D)
I wasn't expecting you.
```

### Forcing Mixed-Case Names
Use `@` prefix for names that aren't all caps:
```fountain
@McCLANE
Yippee ki-yay.

@DeVITO
Don't start with me.
```

## Dialogue Format

### Basic Dialogue
```fountain
SARAH
This is a line of dialogue. It can
span multiple lines naturally.
```

### Dialogue with Parenthetical
```fountain
SARAH
(hesitant)
I don't think that's a good idea.

JOHN
(laughing)
You always say that.
(serious now)
But this time I agree.
```

### Parenthetical Guidelines
- Use sparingly
- Brief direction only
- Lower case
- On own line within dialogue block
- Don't overuse - trust actors

**Good parentheticals:**
```fountain
(whispering)
(to John)
(beat)
(re: the gun)
(into phone)
```

**Bad parentheticals (avoid):**
```fountain
(angrily, as if she can't believe what she's hearing)
(walking across the room and picking up the vase)
```

## Dual Dialogue (Simultaneous Speech)

Characters speaking at the same time:
```fountain
JACK
I love you!

JILL ^
I hate you!
```

The `^` after the second character name triggers side-by-side formatting.

### Dual Dialogue Guidelines
- Use for overlapping speech
- Second character gets the `^`
- Both should be roughly equal length
- Don't overuse - can be hard to follow

## Character Introduction

### First Appearance Format
When a character first appears, their name is typically CAPITALIZED in action:
```fountain
INT. COFFEE SHOP - DAY

SARAH CHEN (30s, sharp eyes, perpetually exhausted)
sits alone at a corner table.
```

### Introduction Best Practices
- Age range, not exact age
- Brief physical impression
- One character-defining detail
- Active description when possible

**Good introductions:**
```fountain
JOHN MARCUS (40s, ex-military bearing, softened by life)

DETECTIVE PARK (50s, seen too much, says too little)

YOUNG SARAH (8, all skinned knees and fierce determination)
```

**Avoid:**
```fountain
SARAH, a beautiful woman in her 30s, enters.  // "beautiful" is vague

JOHN is tall with brown hair and blue eyes.  // casting details
```

## Character Consistency

### Naming Rules
- Pick one name, use it consistently
- Avoid switching between SARAH/MS. CHEN/SHE
- If character is known differently by different people, pick one for script

### Exception Patterns
```fountain
// Character is introduced under false identity
STRANGER (later revealed as JOHN)
Nice to meet you.

// Later, after reveal
JOHN
Sorry about the deception.
```

## Dialogue Best Practices

### Line Length
- Keep lines speakable (read aloud)
- Break at natural breath points
- One thought per line when possible

### Subtext
- Characters rarely say exactly what they mean
- Let action contradict words
- Use pauses and silence

```fountain
SARAH
I'm fine.

She stares out the window, knuckles white on her coffee cup.
```

### Avoiding "On the Nose"
Instead of:
```fountain
JOHN
I'm angry because you betrayed me and now I can't trust you.
```

Try:
```fountain
JOHN
(quiet)
I think you should leave.
```

## Validation Checklist
- [ ] Character names in UPPERCASE
- [ ] Blank line before character names
- [ ] No blank line between name and dialogue
- [ ] Extensions in (PARENTHESES)
- [ ] Parentheticals are brief and necessary
- [ ] Mixed-case names use @ prefix
- [ ] Dual dialogue uses ^ on second character
- [ ] Character names are consistent throughout
