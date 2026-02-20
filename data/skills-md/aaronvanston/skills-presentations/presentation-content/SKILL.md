---
name: presentation-content
description: Write bold, minimal slide content with punchy headlines, concise body text, and impactful bullet points. Use when writing slides, asking "write content for...", "draft slides about...", or "help me phrase this slide...". Transforms ideas into presentation-ready copy designed for speaking to, not reading from.
---

# Presentation Content

Write slide content that is bold, minimal, and designed for speaking to — not reading from.

## Writing Principles

- **Headlines that land** — statements, not descriptions. "AI has no memory" not "Discussion of AI context limitations"
- **Minimal text** — if it takes more than 5 seconds to read, cut it
- **Emphasis through scale** — big words at light weight, not small words in bold
- **Conversation starters** — each slide prompts what you'll say, not what the audience reads

## Headline Patterns

### Statement headlines
Bold declarations that take a position:
- "Speed is a feature"
- "AI has no memory"
- "Context is everything"
- "Passive beats active"

### Question headlines
Create tension and invite reflection:
- "What would we do differently if we started today?"
- "What does this mean for you?"
- "So does any of this actually work?"

### Action headlines
Drive toward outcomes:
- "Building blocks over modules"
- "Always be gardening"
- "Let agents write their own rules"

### Framing headlines
Set context for what follows:
- "How we got here"
- "Where we're going"
- "The real results"

## Body Text Patterns

### Bold lead-in + explanation
```
**Retention is the real metric**
Acquisition gets attention, but retention builds the business.

**Speed compounds**
Ship fast, learn fast, win fast — momentum is the moat.
```

### Key phrase emphasis
Highlight critical words within sentences:
- "Give the **right people**, the **right amount** of information, at the **right time**"
- "We don't compete on **features** — we compete on **speed** and **focus**"

### Minimal bullets
3-4 points maximum, each earning its place:
```
- Focus over breadth — Do one thing better than anyone.
- Platform, not tool — Customers run their whole operation here.
- Speed is the moat — Ship weekly, learn daily, compound forever.
```

### Inline code
Use `backticks` for technical terms, file names, and commands within slides:
- "Start with `AGENTS.md` in your project root"
- "Run `npx skills add` to install"

## Slide Templates

### Statement slide
```markdown
**Section label:** WHAT WORKS
**Section color:** green
**Headline:** Passive context beats active retrieval
**Subtitle:** AGENTS.md is always loaded — skills only trigger when matched
```

### Big statement slide
```markdown
**Section label:** THE PROBLEM
**Section color:** red
**Headline:** AI has no memory
```

### Quote slide
```markdown
**Quote:** "What got you here, won't get you there"
**Attribution:** Marshall Goldsmith
```

### Data slide
```markdown
**Section label:** THE DATA
**Section color:** amber
**Headline:** 10% MoM Growth, $10M ARR
**Subtitle:** Scaling globally with strong traction

**Metrics:**
- ARR: $10M
- MoM Growth: 10%
- NPS: 90
```

### Code slide
```markdown
**Section label:** IMPLEMENTATION
**Section color:** blue
**Headline:** Install the skills
**Subtitle:** One command to add all recommended skills

` ` `bash
npx skills add vercel-labs/agent-skills
` ` `
```

### Goals slide
```markdown
**Section label:** WHY WE'RE HERE
**Section color:** teal
**Headline:** Goals for today
**Points:**
- **Get aligned** — One plan, one direction, no ambiguity.
- **Make decisions** — Resolve the open questions today, not next week.
- **Leave with actions** — Everyone knows what they're doing Monday.
```

### Recap slide
```markdown
**Headline:** Recap

**Sections:**
- **The problem** — AI has no memory, context rots, output is generic
- **The fix** — Invest in AGENTS.md, use skills for domain knowledge
- **The practice** — Always be gardening your project context
```

## Transformation Examples

**Before (verbose):**
> "The fundamental issue with AI coding assistants is that they don't retain any context between sessions, leading to repetitive and generic outputs"

**After (bold):**
> **Headline:** AI has no memory
> **Subtitle:** Every session starts from zero

**Before (explanation):**
> "Our product strategy going forward will be based on building reusable components"

**After (statement):**
> **Headline:** Building blocks over modules
> **Supporting:** A platform built on configurable building blocks. Think "Notion for [your domain]."

## Workflow

1. **Identify the one thing** — what must the audience remember from this slide?
2. **Write the headline first** — bold statement or question
3. **Add only what earns its place** — cut anything the speaker will say anyway
4. **Read it at arm's length** — if you can't parse it in 3 seconds, simplify
