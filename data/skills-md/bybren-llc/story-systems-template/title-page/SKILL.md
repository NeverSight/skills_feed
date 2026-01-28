---
name: title-page
wtfbId: wtfb:title-page
description: |
  This skill provides Fountain title page formatting and metadata setup.
  Covers required fields (title, author, contact), optional fields
  (copyright, draft date, notes), and submission-ready formatting.

  Use when: creating new screenplays, setting up title page metadata,
  updating screenplay information, or preparing scripts for submission.
---

# Title Page Skill

## Invocation Triggers
Apply this skill when:
- Creating new screenplays
- Setting up title page metadata
- Updating screenplay information
- Preparing scripts for submission

## Title Page Format

### Fountain Title Page Syntax
Key-value pairs at the very beginning of the document:

```fountain
Title:
    **Seoul Identity**
Credit: Written by
Author: Scott Graham
Draft date: December 27, 2025
Contact:
    scott@wordstofilmby.com
    (555) 123-4567
```

### Standard Keys

| Key | Purpose | Required |
|-----|---------|----------|
| `Title` | Screenplay title | Yes |
| `Credit` | Credit type | Yes |
| `Author` | Writer name(s) | Yes |
| `Source` | Source material | If adapted |
| `Draft date` | Current draft date | Recommended |
| `Contact` | Contact information | Yes |
| `Copyright` | Copyright notice | Optional |
| `Notes` | Additional notes | Optional |

### Multi-Line Values
Indent continuation lines:
```fountain
Title:
    **The Long and Winding
    Road to Nowhere**
Contact:
    Jane Smith
    jane@email.com
    (555) 123-4567
    123 Main Street
    Los Angeles, CA 90001
```

### Formatting in Titles
```fountain
Title:
    **Bold Title**
    _Underlined Subtitle_
    *Italic tagline*
```

## Credit Types

### Single Writer
```fountain
Credit: Written by
Author: Scott Graham
```

### Writing Team (Collaborators)
```fountain
Credit: Written by
Author: Scott Graham & Jane Smith
```
Note: `&` indicates a writing team who wrote together.

### Multiple Writers (Sequential)
```fountain
Credit: Screenplay by
Author: Scott Graham and Jane Smith
```
Note: `and` indicates writers who worked separately.

### Adapted Work
```fountain
Credit: Screenplay by
Author: Scott Graham
Source: Based on the novel by Jane Smith
```

### Multiple Credits
```fountain
Credit: Screenplay by
Author: Scott Graham
Credit: Story by
Author: Jane Smith & John Doe
```

## Industry Standards

### Spec Script Title Page
```fountain
Title:
    **SEOUL IDENTITY**
Credit: Written by
Author: Scott Graham
Contact:
    scott@wordstofilmby.com
```

**Do NOT include on spec scripts:**
- Draft numbers
- WGA registration numbers (prominently)
- Date revisions

### Production Script Title Page
```fountain
Title:
    **SEOUL IDENTITY**
Credit: Written by
Author: Scott Graham
Draft date: REVISED - December 27, 2025
Contact:
    Production Company Name
    Address
```

## Contact Information

### What to Include
```fountain
Contact:
    Your Name
    your.email@domain.com
    (555) 123-4567
```

Or your representation:
```fountain
Contact:
    Represented by
    Agent Name
    Agency Name
    agent@agency.com
    (555) 123-4567
```

### Positioning
In final PDF output:
- Title: Centered, 1/3 down page
- Credit/Author: Centered, below title
- Contact: Lower right (or lower left)

## Copyright Notice

### Optional Copyright
```fountain
Copyright: (c) 2025 Scott Graham
```

### WGA Registration
If including (not recommended on specs):
```fountain
Notes: WGAw Registered
```

## Complete Examples

### Feature Film Spec
```fountain
Title:
    **SEOUL IDENTITY**
Credit: Written by
Author: Scott Graham
Draft date: December 2025
Contact:
    scott@wordstofilmby.com
```

### Television Spec
```fountain
Title:
    **"The One Where Everything Changes"**
Credit: Spec episode of
Author: BREAKING BAD
Credit: Written by
Author: Scott Graham
Contact:
    scott@wordstofilmby.com
```

### Adaptation
```fountain
Title:
    **THE GREAT GATSBY**
Credit: Screenplay by
Author: Scott Graham
Source: Based on the novel by F. Scott Fitzgerald
Draft date: December 2025
Contact:
    scott@wordstofilmby.com
```

### Writing Team
```fountain
Title:
    **BUDDY COP MOVIE**
Credit: Written by
Author: Scott Graham & Jane Smith
Draft date: December 2025
Contact:
    Represented by
    Super Agent
    Big Agency
    agent@bigagency.com
```

## Validation Checklist
- [ ] Title is present
- [ ] Credit type is correct
- [ ] Author name(s) formatted correctly
- [ ] Contact information included
- [ ] Draft date current (if included)
- [ ] Source credited (if adaptation)
- [ ] No WGA number on spec scripts
- [ ] No draft numbers on spec scripts
- [ ] Multi-line values properly indented
