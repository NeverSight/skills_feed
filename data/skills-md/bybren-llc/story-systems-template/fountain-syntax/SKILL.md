---
name: fountain-syntax
wtfbId: wtfb:fountain-syntax
description: |
  This skill provides complete Fountain screenplay format syntax reference.
  Covers title page, scene headings, action, character names, dialogue,
  transitions, notes, sections, and all special formatting elements.

  Use when: writing or editing .fountain files, validating screenplay format,
  converting between formats, or teaching Fountain syntax.
---

# Fountain Syntax Skill

## Invocation Triggers
Apply this skill when:
- Writing or editing .fountain files
- Validating screenplay format
- Converting between formats
- Teaching Fountain syntax

## Complete Fountain Syntax Reference

### Title Page
Key-value pairs at the start of the document:
```fountain
Title:
    **Seoul Identity**
Credit: Written by
Author: Scott Graham
Draft date: December 27, 2025
Contact: scott@wordstofilmby.com
```

Standard keys: `Title`, `Credit`, `Author`, `Source`, `Draft date`, `Contact`, `Copyright`, `Notes`

### Scene Headings
```fountain
INT. COFFEE SHOP - DAY
EXT. MOUNTAIN ROAD - NIGHT
INT./EXT. CAR (MOVING) - CONTINUOUS
```

Must begin with: `INT`, `EXT`, `EST`, `INT./EXT`, `INT/EXT`, or `I/E`
Force any line as scene heading with `.` prefix:
```fountain
.FLASHBACK - TWENTY YEARS EARLIER
```

Optional scene numbers:
```fountain
INT. HOUSE - DAY #1#
INT. HOUSE - DAY #1A#
```

### Action (Description)
Plain paragraphs are action. Line breaks are preserved.
```fountain
The room is dark. A FIGURE moves in the shadows.

Sarah enters, hesitant. She looks around.
```

Force uppercase lines as action with `!`:
```fountain
!MONTAGE - SARAH'S MORNING ROUTINE
```

### Character Names
All UPPERCASE on own line, blank line before:
```fountain

SARAH
I don't understand.
```

With extensions:
```fountain
MOM (V.O.)
When I was your age...

JOHN (O.S.)
I'm in the kitchen!

SARAH (CONT'D)
And another thing...
```

Force mixed-case with `@`:
```fountain
@McCLANE
Yippee ki-yay.
```

### Dialogue
Text following Character or Parenthetical:
```fountain
JOHN
This is dialogue. It can span
multiple lines without a problem.
```

### Parentheticals
Wrapped in parentheses, after Character or within Dialogue:
```fountain
SARAH
(looking away)
I never said that.
(beat)
Not exactly.
```

### Dual Dialogue (Simultaneous)
Add `^` after second character:
```fountain
JACK
I love you!

JILL ^
I hate you!
```

### Transitions
Uppercase ending in `TO:`, or forced with `>`:
```fountain
CUT TO:

DISSOLVE TO:

>FADE TO BLACK.
```

### Centered Text
Bracket with `>` and `<`:
```fountain
>THE END<

>TITLE CARD: "THREE YEARS LATER"<
```

### Emphasis (Formatting)
```fountain
*italics*
**bold**
***bold italics***
_underline_
```

Escape with backslash: `\*not italic\*`

### Lyrics
Prefix with `~`:
```fountain
~Somewhere over the rainbow
~Way up high
```

### Page Breaks
Three or more `=` on own line:
```fountain
===
```

### Notes (Writer Comments)
Double brackets, won't appear in output:
```fountain
[[This is a note to myself about the scene.]]
```

### Boneyard (Archived Content)
Content between `/*` and `*/` is ignored:
```fountain
/*
CUT SCENE - keeping for reference

INT. DINER - NIGHT
...
*/
```

### Sections (Structural, Hidden)
Pound signs for outline hierarchy:
```fountain
# Act One
## Sequence 1
### Scene Group
```

### Synopses (Scene Summaries, Hidden)
Prefix with `=`:
```fountain
= Sarah discovers the truth about her father.

INT. SARAH'S APARTMENT - NIGHT
```

## Validation Rules

### Required Elements
- Title page (for complete scripts)
- Scene headings with location and time
- Proper character/dialogue structure

### Common Errors
1. Missing blank line before character names
2. Scene heading missing time of day
3. Parenthetical not on own line
4. Unescaped special characters triggering wrong format

### Syntax Validation Checklist
- [ ] Title page has required fields
- [ ] Scene headings start with INT/EXT
- [ ] Character names are UPPERCASE
- [ ] Parentheticals are in (parentheses)
- [ ] Dual dialogue uses ^ correctly
- [ ] Notes use [[double brackets]]
- [ ] Boneyard uses /* */ correctly
