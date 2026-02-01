---
name: quality-speed
description: Decides when quality matters vs move fast, based on Dylan Field (Figma) craft philosophy and Brian Chesky (Airbnb) details obsession. Use when balancing shipping speed with excellence, deciding if refactoring is needed, or determining which details create moats vs which to skip.
---

# Quality vs Speed Framework

## When This Skill Activates

Claude uses this skill when:
- Deciding "should I refactor this before shipping?"
- Balancing craft quality vs speed
- Evaluating if details matter for this feature
- Choosing between polish and iteration

## Core Frameworks

### 1. Craft Creates Moats (Source: Dylan Field, Figma)

**When Quality Matters:**
- Core product experience
- Competitive differentiators
- Brand touchpoints
- High-frequency use

**When Speed Matters:**
- Internal tools
- Experiments
- Non-core features

### 2. The Details Decision Matrix

```
                    │ USER-FACING │ INTERNAL
────────────────────┼─────────────┼──────────
CORE PRODUCT        │ HIGH CRAFT  │ MEDIUM
NON-CORE FEATURE    │ MEDIUM      │ LOW
EXPERIMENT          │ LOW         │ LOW
```

---

## Action Templates

### Template: Quality Assessment

```markdown
# Feature: [Name]

## Context
- User-facing: [yes/no]
- Core product loop: [yes/no]
- Frequency of use: [daily/weekly/monthly]
- Competitive advantage: [yes/no]

## Quality Level Decision

**HIGH CRAFT:**
- Time investment: [X days]
- Polish areas: [list]

**MOVE FAST:**
- Ship threshold: [works, looks okay]
- Time budget: [X days]

## Decision: [HIGH/MEDIUM/LOW craft]
```

---

## Quick Reference

### ⚡ Quality-Speed Checklist

**High Craft Signals:**
- [ ] Core product loop
- [ ] User-facing and frequent
- [ ] Competitive differentiator
- [ ] Brand moment

**Move Fast Signals:**
- [ ] Internal tool
- [ ] One-time use
- [ ] Experiment
- [ ] Behind the scenes

---

## Key Quotes

**Dylan Field:**
> "AI makes design, craft, and quality the new moat for startups."

**Brian Chesky:**
> "Leaders are in the details, but only the details that matter."

