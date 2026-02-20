---
name: presentation-outline
description: Generate structured presentation outlines with bold statement slides, section dividers, and clear narrative arcs. Use when starting a new presentation, planning a deck structure, or asking "outline a presentation about...", "structure a deck for...", or "create a presentation flow for...". Outputs markdown outlines ready to translate into slides.
---

# Presentation Outline

Generate presentation structures following a proven flow pattern with bold, minimal slides designed for live presenting.

## Core Principles

- **Slides are conversation starters, not scripts** — each slide prompts discussion
- **Bold statements over explanations** — headlines that land, not sentences that explain
- **Breathing room** — fewer slides with more impact beats many dense slides
- **Clear sections** — the audience should always know where they are
- **Section colors** — each major section gets its own accent color to reinforce structure

## Standard Flow

The base arc adapts to the content. A typical presentation follows 5-7 sections:

```
1. OPENING (color: teal)
   - Title slide (topic + subtitle)
   - Goals/agenda (3 key takeaways max)

2. CONTEXT / THE PROBLEM (color: red)
   - Current state / where we are today
   - The tension or question to resolve

3-5. CORE SECTIONS (colors: purple, amber, green, blue)
   - Section dividers between major topics
   - 3-5 content slides per section
   - Mix of statement, data, code, framework, and quote slides

6. CLOSING (color: teal)
   - Recap (one-liner per section)
   - Resources
   - Q&A
```

Sections can expand or contract — a complex topic might have 4 core sections, a focused talk might have 2.

## Slide Types

| Type | When to use | Example |
|------|-------------|---------|
| **Statement** | Land a key point | "Speed is a feature" |
| **Big statement** | Maximum impact, one idea | "AI has no memory" |
| **Question** | Create tension | "What would we do differently?" |
| **Section divider** | Signal topic shift | "Where we play" |
| **Goals** | Set expectations | "Goals for today" |
| **Data** | Prove with numbers | "3x growth in 6 months" |
| **Code** | Show implementation | Syntax-highlighted code block |
| **Framework** | Show a model or list | Do's and don'ts, comparison |
| **Quote** | Borrow authority | "What got you here won't get you there" |
| **Recap** | Summarize before close | "Recap" |
| **Resources** | Link references | Grouped by section |
| **Next steps** | Drive action | "Where to from here?" |

## Output Format

```markdown
# [Presentation Title]
[One-line purpose]

---

## 1. Opening
**Section color:** teal

### Slide 1: Title
- **Headline:** [Title]
- **Subtitle:** [Context or date]

### Slide 2: Goals for today
- **Headline:** Goals for today
- **Points:**
  - [Takeaway 1] — [Brief explanation]
  - [Takeaway 2] — [Brief explanation]
  - [Takeaway 3] — [Brief explanation]

---

## 2. [Section Name]
**Section color:** [color]

### Slide 3: Section divider
- **Type:** Section divider
- **Headline:** [Section title]

### Slide 4: [Slide purpose]
- **Type:** [Statement/Big statement/Data/Code/etc.]
- **Headline:** [Bold headline]
- **Supporting:** [1-2 sentences or bullets]

---

## X. Closing
**Section color:** teal

### Slide N: Recap
- **Headline:** Recap
- **Points:** [One-liner per section]

### Slide N+1: Resources
- **Type:** Resources
- **References:** [Grouped by section]

### Slide N+2: Q&A
```

## Workflow

1. **Ask about context** — audience, purpose, setting (live vs. async)
2. **Identify key messages** — what 3 things must land?
3. **Map the arc** — Opening → Problem/Context → Core sections → Close
4. **Assign section colors** — one color per major section
5. **Draft outline** — use the format above
6. **Review density** — cut slides that don't earn their place
