---
name: rulebook-writing
description: Expert guidance for writing UP SHIP! rulebook content following Euro-style board game best practices. Use when drafting rules sections, reviewing rules clarity, restructuring content, or ensuring consistency. Covers section ordering, terminology, formatting, cross-referencing, and audience design.
---

# UP SHIP! Rulebook Writing Skill

## Overview

This skill provides expert guidance for writing and maintaining the UP SHIP! rulebook, applying proven Euro-style board game rulebook best practices. It covers section ordering, writing style, terminology consistency, formatting conventions, and techniques for serving multiple reader audiences.

## Core Philosophy

### The Three Rules of Rulebook Writing

1. **Clarity Over Brevity**: A longer, clearer explanation beats a shorter, confusing one
2. **Sequential Disclosure**: Introduce concepts in the order players encounter them
3. **Consistent Terminology**: Use the same term for the same concept every time

### Three Audiences to Serve

Every rulebook section must work for three types of readers:

| Audience | Need | Design Approach |
|----------|------|-----------------|
| **First-time Players** | Learn from scratch | Sequential flow, define terms before using |
| **Active Players** | Quick reference during play | Bold keywords, scannable structure, clear headings |
| **Returning Players** | Memory refresh | Glossary, quick reference, section summaries |

## UP SHIP! Rulebook Structure

### Recommended Section Order

The UP SHIP! rulebook follows this structure, informed by best practices:

1. **Title & Overview** (§1)
   - Game theme (Golden Age of Airships)
   - Player count, play time
   - Victory condition stated early
   - Game end triggers

2. **Glossary** (Front matter)
   - Quick reference for all key terms
   - Cross-references to detailed sections
   - Alphabetical for quick lookup

3. **Components** (§2)
   - Per-player components listed first
   - Shared components second
   - Include quantities and visual descriptions

4. **Player Board** (§3)
   - The Factory Interface zones
   - Blueprint mechanics (critical to understanding)
   - Crew tokens (Officers, Engineers)
   - Economy tracks

5. **Core Systems** (§4)
   - Technology acquisition (R&D)
   - Upgrade installation
   - Lifting gas system (Hydrogen vs Helium)

6. **Routes & Network** (§5)
   - Route types and requirements
   - Claiming routes
   - Income and scoring from routes

7. **The Game Loop** (§6)
   - Round structure overview
   - Worker Placement phase
   - Reveal phase

8. **Building & Launching** (§7)
   - Construction Hall actions
   - Launch requirements (Physics Check)
   - Hazard Check system
   - Fire and damage

9. **Deck Building** (§8)
   - Starting deck
   - Market Row purchases
   - Card icons and effects

10. **Age Transitions** (§9)
    - What carries over
    - What resets
    - Blueprint replacement

11. **Faction Rules** (§10)
    - Germany, Britain, USA, Italy
    - Unique abilities and constraints

12. **Advanced Rules** (§11)
    - Optional variants
    - Solo mode (if any)

13. **Detailed Procedures** (§12)
    - Edge cases
    - Specific action procedures
    - Timing windows

14. **Appendices**
    - A: Design Notes / TODO
    - B: Quick Reference
    - C: Technology Tiles
    - D: Upgrade Tiles
    - E: Hazard Deck
    - F: Market Deck

### Key UP SHIP! Cross-References

These interconnected systems require consistent cross-referencing:

| System | Cross-References To |
|--------|---------------------|
| Blueprint (§3.2) | Technology (§4), Upgrade (§4.2), Launch (§7) |
| Physics Check (§3.2, §7.2) | Gas Cubes (§4.4), Weight (§3.7), Lift (§4.4) |
| Hazard Checks (§7.3) | Ship Stats (§3.7), Appendix E |
| Age Transitions (§9) | Blueprint (§3.2), Technology (§4), Routes (§5) |
| Progress Track (§1.3) | Launch (§7), Game End (§1) |

## Writing Style Guide

### Verb-First Instructions

Start instructions with the action verb:

```markdown
# Good
Draw 2 cards from your deck.
Place 1 Agent on an empty Ground Board location.
Compare your ship's Speed to the Hazard difficulty.

# Avoid
You should draw 2 cards from your deck.
The player places 1 Agent on a Ground Board location.
Your ship's Speed is compared to the Hazard difficulty.
```

### Consistent Terminology

UP SHIP! uses specific terms that must be consistent:

| Use This | Not This |
|----------|----------|
| Agent | worker, meeple |
| Blueprint | ship design, schematic |
| Gas Cube | gas token, lifting gas |
| Hazard Check | danger roll, risk test |
| Install | attach, place (for upgrades) |
| Claim (route) | take, capture, control |
| Acquire (technology) | buy, purchase, research |
| Launch | deploy, send, fly |
| Physics Check | lift check, weight check |

### Capitalization Rules

| Capitalize | Don't Capitalize |
|------------|------------------|
| Game terms: Agent, Blueprint, Hazard Check | Generic words: route, card, token |
| Phase names: Worker Placement, Reveal Phase | Common verbs: draw, place, move |
| Zone names: Drawing Office, Launch Hangar | Directions: left, right, top |
| Upgrade types: Frame, Fabric, Drive, Payload | Stats unless specific: speed, range |
| Age names: Age I, Pioneer Era | General time: early game, late game |

### Bold Usage

Use **bold** for:
- First mention of a defined game term
- Key warnings or reminders
- Cross-section references: "See **Section 7.3 Hazard Checks**"

### Numbers and Quantities

- Spell out numbers one through nine
- Use numerals for 10 and above
- Always use numerals with units: 5 Lift, £3, 2 Research
- Use numerals in tables and stat blocks

### Example Format

Use callout boxes for examples:

```markdown
> **Example:** Anna launches her airship with Speed 3 and Range 4.
> She draws a Hazard Card showing Engine Failure (Reliability 3).
> Her ship has Reliability 2, so she fails by 1. The Hazard takes effect.
```

## Formatting Best Practices

### Section Headers

Use hierarchical headers consistently:

```markdown
# 7. BUILDING AND LAUNCHING SHIPS

## 7.1 Ship Construction

### Construction Hall Actions

#### Building from Blueprint
```

### Tables for Stats and Options

Use tables when comparing options:

```markdown
| Gas Type | Cost | Lift | Fire Vulnerability |
|----------|------|------|--------------------|
| Hydrogen | £1/cube | +5 | Vulnerable |
| Helium | £2-15/cube | +5 | Immune |
```

### Lists for Sequential Steps

Use numbered lists for procedures:

```markdown
**To Launch a Ship:**
1. Verify Physics Check passes (Lift ≥ Weight)
2. Pay Officer cost (1 per Age number)
3. Spend gas cubes from Gas Reserve
4. Draw Hazard Card and resolve
5. If successful, claim route and move ship token
```

### Cross-References

Format cross-references consistently:

```markdown
See Section 7.3 for Hazard Check procedures.
(See §3.2 Blueprint for slot types.)
Refer to Appendix E: Hazard Deck.
```

## Common Mistakes to Avoid

### 1. Forward References Without Definition

**Bad:** "Place gas cubes (see Section 4.4) on your Blueprint."
**Good:** "Place **Gas Cubes**—tokens providing +5 Lift each—on your Blueprint. See Section 4.4 for the complete gas system rules."

### 2. Inconsistent Terminology

**Bad:** "Your workers... your agents... your meeples..."
**Good:** "Your Agents" (consistently throughout)

### 3. Passive Voice

**Bad:** "Cards are drawn by each player."
**Good:** "Each player draws cards."

### 4. Ambiguous Pronouns

**Bad:** "When it reaches the threshold, it ends."
**Good:** "When the Progress Track reaches the threshold, the Age ends."

### 5. Mixing Rules with Examples

**Bad:** "Install an Upgrade tile. For example, if you install a Diesel Engine..."
**Good:**
```
Install an Upgrade tile in a matching empty slot.

> **Example:** You install a Diesel Engine in your Drive slot.
```

### 6. Burying Critical Information

**Bad:** Long paragraph with "Note: Ships cannot launch if..." in the middle
**Good:** Bold callout or dedicated subsection for critical rules

## Quick Reference Design

Create quick reference materials that:
- Fit on one page or card
- Use icons consistently
- Include turn sequence
- List all Ground Board locations
- Summarize key costs and limits

### UP SHIP! Quick Reference Elements

- Turn sequence (Worker Placement → Reveal → Income/Cleanup)
- Physics formula (Lift ≥ Weight)
- Ground Board locations and their symbols
- Technology track discounts
- Age transition summary
- Hazard Check procedure

## When This Skill Activates

Use this skill when:
- Writing new rules sections for UP SHIP!
- Reviewing existing sections for clarity
- Reorganizing content for better flow
- Checking terminology consistency
- Adding examples or edge case clarifications
- Creating quick reference materials
- Preparing rules for playtest feedback

## Supporting Resources

This skill includes reference files in `references/`:

- `section-templates.md` - Templates for each rulebook section with UP SHIP! examples
- `writing-checklist.md` - Validation checklist for rules completeness and clarity

## Sources

Best practices synthesized from:
- [Meeple Mountain - Top Six Rules for Writing Rulebooks](https://www.meeplemountain.com/top-six/top-six-rules-for-writing-rulebooks/)
- [Resonym - Writing Rulebooks](https://resonym.com/writing-rulebooks/)
- [Brandon the Game Dev - Perfect Board Game Rule Book](https://brandonthegamedev.com/how-to-make-the-perfect-board-game-rule-book/)
- [Board Game Design Lab - Writing Rules](https://boardgamedesignlab.com/rules/)
