---
name: crucible-outliner
# prettier-ignore
description: Chapter-by-chapter outline generator for stories planned with the Crucible Structure. Use when a user has completed Crucible planning documents (thesis, strand maps, forge points, etc.) and wants to create detailed chapter outlines. Triggers on requests like "outline my book," "create chapter outline," "outline Book 1," "turn my Crucible plan into chapters," or when user has Crucible planning docs and wants to start writing. Works for single books or multi-book series.
---

# Crucible Outliner

Transform Crucible planning documents into detailed chapter-by-chapter outlines with proper narrative craft.

## Before Starting

**Read these references based on the outlining phase:**
- `references/beat-to-chapter-mapping.md` — How 36 beats map to chapters
- `references/narrative-craft.md` — Foreshadowing, pacing, scene structure
- `references/outline-templates.md` — Chapter and scene outline formats

## Questioning Rules

1. **ALWAYS use AskUserQuestion tool** for all user questions (provides interactive UI)
2. **Max 4 options per question** (tool limit) + "Other" is automatic
3. **Max 4 questions per AskUserQuestion call**
4. **Reference user's story elements** by name (characters, places, etc.)
5. **Save state after each chapter outline**

**CRITICAL: Use the AskUserQuestion tool, NOT plain text A/B/C options.**

## Required Inputs

The user must have completed Crucible planning. Request uploads of:

1. **Crucible Thesis** (required first) — Core elements: burden, fire, constellation, theme
2. **Strand Maps** (required) — Quest, Fire, Constellation arcs
3. **Forge Point Blueprints** (required) — The convergence crises
4. **Constellation Bible** (as needed) — Character details
5. **Mercy Ledger** (as needed) — Setup/payoff tracking
6. **World Forge** (as needed) — Setting details

## Workflow

```
Phase 1: SETUP → Load planning docs, confirm scope, establish parameters
Phase 2: STRUCTURE → Map beats to chapters, identify act breaks
Phase 3: CHAPTERS → Outline each chapter through questions
Phase 4: CRAFT → Add foreshadowing threads, verify payoffs
Phase 5: COMPILE → Generate final outline documents
```

## Phase 1: Setup

### Load Planning Documents

Request the Crucible Thesis first:
```
To begin outlining, I need your Crucible planning documents.

Please upload your **Crucible Thesis** (or paste its contents).
This contains your core elements: burden, fire, constellation, theme, etc.
```

After receiving, extract and confirm:
- Theme
- Burden type
- Fire nature  
- Core bond
- Dark mirror connection
- Surrender moment
- Blade's purpose

### Confirm Scope

Use AskUserQuestion to confirm scope:
```json
{
  "questions": [
    {
      "header": "Book Type",
      "question": "Which book are we outlining?",
      "options": [
        {"label": "Standalone novel", "description": "A single, complete novel"},
        {"label": "Book in series", "description": "Part of a larger series (specify which book)"},
        {"label": "Series overview", "description": "Full series overview first, then individual books"}
      ],
      "multiSelect": false
    },
    {
      "header": "Chapter Count",
      "question": "What is your target chapter count?",
      "options": [
        {"label": "Standard (20-25)", "description": "Typical novel length"},
        {"label": "Compact (15-20)", "description": "Tighter, faster-paced structure"},
        {"label": "Extended (25-35)", "description": "More room for subplot development"},
        {"label": "Story dictates", "description": "Let the narrative determine chapter count"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Initialize Project

```bash
python scripts/init_outline.py "./outline-project" "Title" "Book X of Y"
```

## Phase 2: Structure

### Map Beats to Chapters

Using `references/beat-to-chapter-mapping.md`, establish the chapter skeleton:

**For standard 20-25 chapter book:**

| Movement | Beats | Chapters | % of Book |
|----------|-------|----------|-----------|
| I. Ignition | 1-6 | 1-5 | 10% |
| II. First Tempering | 7-14 | 6-10 | 20% |
| III. Scattering | 15-22 | 11-16 | 25% |
| IV. Brightest Burning | 23-28 | 17-21 | 25% |
| V. Final Forging | 29-34 | 22-24 | 15% |
| Coda | 35-36 | 25 | 5% |

Present the proposed structure:
```
**Proposed Chapter Structure for [Title]**

MOVEMENT I — IGNITION (Chapters 1-5)
• Ch 1: [Beat 1 - The Unlit Forge]
• Ch 2: [Beats 2-3 - Dual Arrival + First Spark]
• Ch 3: [Beat 4 - The Burden Chosen]
• Ch 4: [Beat 5 - First Constellation]
• Ch 5: [Beat 6 - IGNITION FORGE POINT]

[Continue for all movements...]

Use AskUserQuestion to confirm:
```json
{
  "questions": [
    {
      "header": "Structure",
      "question": "Does this chapter structure work for your story?",
      "options": [
        {"label": "Approve structure", "description": "Proceed with this chapter layout"},
        {"label": "Adjust count", "description": "Modify the number of chapters"},
        {"label": "Discuss sections", "description": "Talk through specific movements or chapters"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Request Additional Documents

Based on which movement is being outlined, request relevant docs:
- Movements I-II: Request Forge Point 0 and 1 blueprints
- Movement III: Request Forge Point 2, Mercy Ledger
- Movement IV: Request Forge Point 3, Dark Mirror Profile
- Movement V: Request Forge Point Apex, full Constellation Bible

## Phase 3: Chapter Outlining

### Question Format for Each Chapter

For each chapter, work through:

```
**CHAPTER [X]: [Working Title]**
Beat(s): [Which Crucible beats this covers]
Strand Focus: [Quest/Fire/Constellation]
POV: [If dual/multiple POV]

**1. OPENING**
Where does the reader enter this chapter?
A) Immediate action/tension
B) Character reflection/interiority  
C) World/setting establishment
D) Dialogue/interaction
E) Time skip from previous chapter
F) Other (describe)

**2. CORE SCENES**
What must happen in this chapter? (Select all that apply)
A) [Beat-specific requirement from Crucible]
B) [Beat-specific requirement]
C) Foreshadowing plant for [future payoff]
D) Character development moment
E) World-building revelation
F) Other (describe)

**3. CHAPTER TURN**
How does this chapter end?
A) Cliffhanger — immediate tension
B) Revelation — new information changes everything
C) Decision point — character commits to action
D) Emotional beat — feeling resonates into next chapter
E) Question raised — reader needs to know what's next
F) Other (describe)
```

### Scene-Level Detail

For each scene within a chapter:

```
**SCENE [X.Y]**

**Goal:** What must this scene accomplish?
**Conflict:** What opposes the goal?
**Disaster/Turn:** How does it shift?

**Characters present:** 
**Location:**
**Tone/Mood:**
**Key dialogue/moments:**
**Plants/Payoffs:** 
  - Sets up: [future scene]
  - Pays off: [previous setup]
```

### Save Progress After Each Chapter

```bash
python scripts/save_outline.py "./outline-project"
```

## Phase 4: Narrative Craft Layer

After completing chapter skeletons, add craft elements:

### Foreshadowing Threads

Using `references/narrative-craft.md`, track:

```
**FORESHADOWING TRACKER**

Thread: [Description]
├── Plant: Chapter [X], Scene [Y] — [How it's planted]
├── Water: Chapter [X] — [How it's reinforced]  
└── Payoff: Chapter [X], Scene [Y] — [How it resolves]
```

Required threads for Crucible stories:
1. Mercy → Unexpected Agents (each mercy must plant, payoff in finale)
2. Dark Mirror reveals (antagonist philosophy shown before confrontation)
3. Fire mastery path (surrender lesson foreshadowed before mastery moment)
4. Constellation fracture/repair (betrayal foreshadowed, bond-holds foreshadowed)

### Pacing Verification

Check chapter-by-chapter:
- Tension curve (rising overall with valleys for rest)
- Strand rotation (no strand absent 3+ chapters)
- Emotional variety (not all dark, not all light)

### Verify Forge Points

Each Forge Point chapter must have:
- [ ] All three strands in crisis
- [ ] Clear sacrifice made
- [ ] Irreversible change
- [ ] Forward momentum into next movement

## Phase 5: Compile

### Generate Outline Documents

```bash
python scripts/compile_outline.py "./outline-project"
```

Creates:
```
outline/
├── master-outline.md          # Full book outline
├── chapter-summaries.md       # Quick reference
├── scene-breakdown.md         # Detailed scene list
├── foreshadowing-tracker.md   # Plant/payoff tracking
├── character-threads.md       # Per-character arcs
└── by-chapter/
    ├── ch01-outline.md
    ├── ch02-outline.md
    └── ...
```

### Present to User

```
✅ **Outline Complete: [Title]**

📄 [View Master Outline](computer:///path/outline/master-outline.md)
📄 [View Chapter Summaries](computer:///path/outline/chapter-summaries.md)
📄 [View Scene Breakdown](computer:///path/outline/scene-breakdown.md)
📄 [View Foreshadowing Tracker](computer:///path/outline/foreshadowing-tracker.md)

Use AskUserQuestion for next steps:
```json
{
  "questions": [
    {
      "header": "Next Steps",
      "question": "What would you like to do next?",
      "options": [
        {"label": "Review chapters", "description": "Review and adjust specific chapters"},
        {"label": "Outline next book", "description": "Continue to next book in series"},
        {"label": "Begin drafting", "description": "Start writing prose from this outline"},
        {"label": "Add scene detail", "description": "Expand detail on specific scenes"}
      ],
      "multiSelect": false
    }
  ]
}
```

## Multi-Book Series Handling

For series, outline books in order. Track:

**Cross-Book Elements:**
- Mercy plants in Book X → Payoffs in Book Y
- Character arcs spanning multiple books
- Foreshadowing threads that span books
- Series-level pacing (which book is darkest, etc.)

Before outlining Book 2+, request:
- Previous book outline(s)
- Updated character states
- Unresolved threads list

## Questioning Principles

1. **Max 2-3 questions per message** — Don't overwhelm
2. **Always offer "Other" option** — User knows their story
3. **Reference their documents** — Use their character names, places, elements
4. **Explain the "why"** — Brief context for why this choice matters
5. **Save state frequently** — After each chapter or major decision
