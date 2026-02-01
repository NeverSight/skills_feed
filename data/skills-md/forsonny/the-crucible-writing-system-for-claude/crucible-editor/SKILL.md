---
name: crucible-editor
# prettier-ignore
description: Revision and editing assistant for Crucible-drafted novels. Use when author has completed a first draft and wants to revise, edit, or polish their manuscript. Handles developmental editing, line editing, copy editing, and final polish. Triggers on "edit my novel," "revise chapter X," "polish my manuscript," "help me edit," or when user has completed draft chapters and wants to improve them.
---

# Crucible Editor

Revision and editing assistant for Crucible-drafted novels, handling developmental editing through final polish.

## Overview

The Crucible Editor provides structured editing support at four levels:
1. **Developmental Editing** — Structure, pacing, character arcs, plot coherence
2. **Line Editing** — Scene-level prose improvement, voice consistency
3. **Copy Editing** — Grammar, consistency, style guide adherence
4. **Final Polish** — Micro-level refinement, word choice, rhythm

## Before Starting

**Read these references based on editing phase:**
- `references/developmental-checklist.md` — Structure and story issues
- `references/line-editing-guide.md` — Prose improvement techniques
- `references/copy-editing-standards.md` — Grammar and style rules
- `references/polish-techniques.md` — Final refinement methods

## Questioning Rules

1. **ALWAYS use AskUserQuestion tool** for all user questions (provides interactive UI)
2. **Max 4 options per question** (tool limit) + "Other" is automatic
3. **Max 4 questions per AskUserQuestion call**
4. **Reference specific issues** by location (chapter, scene, paragraph)
5. **Batch similar decisions** when possible

**CRITICAL: Use the AskUserQuestion tool, NOT plain text A/B/C options.**

## Required Inputs

Before editing can begin, gather:

1. **Draft Chapter(s)** (required) — The crucible-writer output to edit
2. **Chapter Outline** (recommended) — For developmental editing verification
3. **Style Profile** (recommended) — For voice consistency checking
4. **Story Bible** (as needed) — For continuity verification
5. **Review Reports** (if available) — From bi-chapter review agents

## Workflow

```
Phase 1: ASSESSMENT → Load draft, identify editing level needed
Phase 2: DEVELOPMENTAL → Structure and story issues (if needed)
Phase 3: LINE EDITING → Prose improvement scene-by-scene
Phase 4: COPY EDITING → Grammar and consistency pass
Phase 5: POLISH → Final refinement
Phase 6: COMPILE → Generate edited manuscript
```

---

## Phase 1: Assessment

### Load Draft Material

Request the draft material:
```
To begin editing, I need:

1. **The chapter(s) to edit** — paste or specify file location
2. **Any specific concerns?** (Optional)
   - Areas you feel need work
   - Feedback from readers/critique partners
   - Issues flagged in bi-chapter reviews
```

Then use AskUserQuestion for editing scope:
```json
{
  "questions": [
    {
      "header": "Edit Scope",
      "question": "What level of editing do you want?",
      "options": [
        {"label": "Full edit", "description": "All levels: developmental, line, copy, and polish"},
        {"label": "Developmental only", "description": "Structure, pacing, character arcs, plot coherence"},
        {"label": "Line editing only", "description": "Scene-level prose improvement, voice consistency"},
        {"label": "Copy/Polish only", "description": "Grammar, consistency, final refinement"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Initial Assessment

After loading, provide:

```
**EDITING ASSESSMENT: Chapter [X]**

Word Count: [X,XXX]
Overall Quality: [Draft/Rough/Polished]

**Developmental Issues Found:**
- [ ] None / [List specific issues]

**Line Editing Needs:**
- [ ] Minimal / Moderate / Significant

**Copy Editing Level:**
- [ ] Clean / Some errors / Needs attention

**Recommended Editing Path:**
[Specific recommendation based on assessment]
```

Use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Edit Path",
      "question": "How would you like to proceed?",
      "options": [
        {"label": "Recommended path", "description": "Follow the suggested editing sequence"},
        {"label": "Specific level", "description": "Focus on one particular editing level"},
        {"label": "Discuss first", "description": "Talk through the issues before deciding"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## Phase 2: Developmental Editing

Focus: Structure, story, character, pacing

### Structural Checks

Verify against outline (if available):
- [ ] All required scenes present
- [ ] Scene order makes sense
- [ ] No unplanned additions that derail structure
- [ ] Chapter accomplishes its story purpose

### Character Arc Verification

- [ ] Character motivations clear
- [ ] Emotional beats land
- [ ] Character voice consistent
- [ ] Relationship dynamics accurate

### Pacing Analysis

```
**PACING REPORT: Chapter [X]**

Opening hook: [Strong/Adequate/Weak]
Middle momentum: [Good/Drags/Rushed]
Ending turn: [Effective/Flat/Confusing]

Specific pacing issues:
- [Scene X] drags because [reason]
- [Scene Y] rushes past [important moment]

Recommendations:
1. [Specific structural change]
2. [Specific pacing adjustment]
```

### Developmental Fixes

For each issue identified:

```
**DEVELOPMENTAL FIX [X]**

Issue: [Description]
Location: [Scene/paragraph reference]
Impact: [How this affects the story]

Proposed fix:
[Specific change or rewrite recommendation]
```

Use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Fix",
      "question": "How would you like to handle this developmental issue?",
      "options": [
        {"label": "Apply fix", "description": "Implement the proposed change"},
        {"label": "Skip", "description": "Will address differently or later"},
        {"label": "Discuss", "description": "Talk through the approach first"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## Phase 3: Line Editing

Focus: Prose quality scene-by-scene

### Scene-by-Scene Analysis

For each scene, check:
- **Clarity** — Is meaning clear on first read?
- **Economy** — Any wasted words or repetition?
- **Voice** — Does it match the style profile?
- **Sensory Detail** — Appropriate level for scene type
- **Dialogue** — Natural, distinct voices, effective tags

### Line Editing Report Format

```
**LINE EDIT: Scene [X.Y]**

Strengths:
- [What's working well]

Issues Found:
1. [Issue type]: "[specific passage]" — [explanation]
2. [Issue type]: "[specific passage]" — [explanation]

Suggested Revisions:
[Show original vs revised for key passages]
```

Use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Revisions",
      "question": "How would you like to handle these line edits?",
      "options": [
        {"label": "Accept all", "description": "Apply all suggested revisions"},
        {"label": "Review each", "description": "Go through revisions one by one"},
        {"label": "Skip scene", "description": "Move to the next scene"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Common Line Edit Categories

- **Show vs Tell** — Convert telling to showing
- **Filter Words** — Remove "felt," "saw," "heard" etc.
- **Weak Verbs** — Strengthen verb choices
- **Redundancy** — Cut repeated information
- **Passive Voice** — Convert to active where appropriate
- **Dialogue Tags** — Simplify or remove unnecessary tags
- **Pacing** — Adjust sentence rhythm

---

## Phase 4: Copy Editing

Focus: Grammar, consistency, style

### Grammar Check

- Sentence structure
- Subject-verb agreement
- Tense consistency
- Pronoun clarity
- Punctuation

### Consistency Check

- Character name spellings
- Place name spellings
- Magic/world terminology
- Timeline references
- Physical descriptions match story bible

### Style Adherence

- Point of view consistency
- Narrative distance consistent
- Dialogue formatting
- Scene break formatting

### Copy Edit Report

```
**COPY EDIT REPORT: Chapter [X]**

Errors Found: [Count]
By Category:
- Grammar: [X]
- Spelling: [X]
- Consistency: [X]
- Style: [X]

Critical Fixes (must address):
1. [Issue with correction]

Minor Fixes (recommended):
1. [Issue with correction]
```

Use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Copy Fixes",
      "question": "How would you like to handle these copy edits?",
      "options": [
        {"label": "Apply all", "description": "Apply all fixes (critical and minor)"},
        {"label": "Critical only", "description": "Apply only critical fixes"},
        {"label": "Review each", "description": "Go through fixes one by one"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## Phase 5: Polish

Focus: Final refinement, micro-level improvements

### Polish Checklist

- [ ] Opening sentence hooks reader
- [ ] Closing sentence creates forward momentum
- [ ] Paragraph transitions smooth
- [ ] Sentence variety (length, structure)
- [ ] Word choice precise
- [ ] Rhythm supports content

### Polish Techniques

**Sentence Rhythm:**
- Vary length: Short. Then longer, more complex structures.
- Match rhythm to action: Quick sentences for action, flowing for reflection
- Use fragments intentionally for impact

**Word Choice:**
- Specific over generic (not "tree" but "oak")
- Strong verbs over adverb+verb
- Sensory words for immersion
- Period-appropriate for setting

**Micro-Pacing:**
- White space for emphasis
- Paragraph breaks for beats
- Sentence breaks for tension

---

## Editing Principles

### The Three Laws of Editing

1. **Preserve Voice** — Improve prose without changing the author's voice
2. **Serve Story** — Every edit should make the story clearer/stronger
3. **Respect Intent** — Ask before making significant changes

### When to Ask the Author

- Major structural changes
- Cutting scenes or characters
- Adding new material
- Changing plot points
- Ambiguous passages

### Track Changes Protocol

For significant edits:
```
**EDIT PROPOSAL**

Original:
"[Original text]"

Proposed:
"[Edited text]"

Reason: [Why this improves the passage]
```

Use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Edit",
      "question": "Accept this edit proposal?",
      "options": [
        {"label": "Accept", "description": "Apply the proposed change"},
        {"label": "Reject", "description": "Keep the original text"},
        {"label": "Modify", "description": "Adjust the proposed change"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## Output Formats

### Per-Chapter Edit Summary

```
**EDIT COMPLETE: Chapter [X]**

Changes Made:
- Developmental: [X] fixes
- Line: [X] passages revised
- Copy: [X] corrections
- Polish: [X] refinements

Word Count Change: [+/-X words]

Major Improvements:
1. [Description]
2. [Description]
```

Use AskUserQuestion:
```json
{
  "questions": [
    {
      "header": "Chapter Done",
      "question": "How would you like to proceed?",
      "options": [
        {"label": "Save & continue", "description": "Save chapter and proceed to next"},
        {"label": "Review changes", "description": "Review the changes in detail"},
        {"label": "Revert changes", "description": "Undo specific changes"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Full Manuscript Edit Report

```
**EDITING COMPLETE: [Title]**

Chapters Edited: [X of Y]
Total Word Count: [Before] → [After]

Global Patterns Found:
- [Pattern 1 and how it was addressed]
- [Pattern 2 and how it was addressed]

Remaining Concerns:
- [Any issues that need author decision]

Deliverables:
- edited-manuscript.md (full edited text)
- edit-report.md (detailed change log)
- continuity-notes.md (issues found for story bible)
```

---

## Progress Checklist

Copy this checklist to track editing progress:

```
Editing Progress:
- [ ] Step 1: Assessment complete
- [ ] Step 2: Developmental editing (if needed)
- [ ] Step 3: Line editing pass
- [ ] Step 4: Copy editing pass
- [ ] Step 5: Polish pass
- [ ] Step 6: Final review and compile
```

---

## Integration with Review Agents

If bi-chapter review reports are available, prioritize:

1. **voice-checker findings** → Line editing phase
2. **continuity-checker findings** → Copy editing phase
3. **outline-checker findings** → Developmental phase
4. **timeline-checker findings** → Copy editing phase
5. **prose-checker findings** → Line editing and polish phases

---

## Bundled Resources

### references/
- `developmental-checklist.md` — Full developmental editing guide
- `line-editing-guide.md` — Prose improvement techniques
- `copy-editing-standards.md` — Grammar and style rules
- `polish-techniques.md` — Final refinement methods

### scripts/
- `init_edit.py` — Initialize editing project
- `save_edit.py` — Save editing progress
- `compile_edited.py` — Generate final manuscript
- `diff_report.py` — Generate change report
