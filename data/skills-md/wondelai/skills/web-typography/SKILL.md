---
name: web-typography
description: Web typography principles based on "On Web Typography" by Jason Santa Maria (A Book Apart, 2014). Use when selecting typefaces, setting body text, creating type hierarchies, pairing fonts, or implementing typography in CSS. Triggers on requests for font selection, readable text, typographic hierarchy, font pairing, or "making text look better."
license: MIT
metadata:
  author: wondelai
  version: "1.0"
---

# Web Typography

A practical guide to choosing, pairing, and implementing typefaces for the web. Typography serves communication—the best typography is invisible, immersing readers in content rather than calling attention to itself.

## Core Philosophy

**Typography is the voice of your content.** The typeface you choose sets tone before a single word is read. A legal site shouldn't feel playful; a children's app shouldn't feel corporate.

**The "clear goblet" principle:** Typography should be like a crystal-clear wine glass—the focus is on the wine (content), not the glass (type). Readers should absorb meaning, not notice letterforms.

**Readers don't read, they scan.** Eyes jump 7-9 characters at a time (saccades), pausing briefly (fixations). Good typography supports this natural pattern.

## Scoring

**Goal: 10/10.** When reviewing or creating typography implementations, rate them 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## Two Contexts for Type

All typography falls into two categories:

| Context | Purpose | Priorities |
|---------|---------|------------|
| **Type for a moment** | Headlines, buttons, navigation, logos | Personality, impact, distinctiveness |
| **Type to live with** | Body text, articles, documentation | Readability, comfort, endurance |

**Workhorse typefaces** excel at "type to live with"—they're versatile across sizes, weights, and contexts without drawing attention to themselves. Examples: Georgia, Source Sans, Freight Text, FF Meta.

## How We Read

Understanding reading mechanics improves typography decisions:

- **Saccades:** Eyes jump in 7-9 character bursts, not smooth scanning
- **Fixation points:** Eyes pause briefly to absorb content
- **Word shapes:** Experienced readers recognize word silhouettes, not individual letters
- **Bouma:** The overall shape of a word—maintaining distinct boumas aids recognition

**Legibility vs. Readability:**
- **Legibility** = Can individual characters be distinguished? (typeface concern)
- **Readability** = Can text be comfortably read for extended periods? (typography concern—size, spacing, line length)

A typeface can be legible but poorly set, making it unreadable. Both matter.

## Evaluating Typefaces

Quick assessment checklist:

### Technical Quality
- [ ] Consistent stroke weights across characters
- [ ] Even color (visual density) across text blocks
- [ ] Good kerning pairs (AV, To, Ty, etc.)
- [ ] Complete character set (accents, punctuation, figures)
- [ ] Multiple weights (at minimum: regular, bold, italic)

### Structural Assessment
- [ ] Adequate x-height (larger = better screen readability)
- [ ] Open counters and apertures (a, e, c shapes)
- [ ] Distinct letterforms (Il1, O0, rn vs. m)
- [ ] Appropriate contrast (thick/thin stroke variation)

### Practical Needs
- [ ] Works at intended sizes (test at actual use size)
- [ ] Renders well on target screens/browsers
- [ ] Acceptable file size for web loading
- [ ] Appropriate license for project

See [references/evaluating-typefaces.md](references/evaluating-typefaces.md) for detailed criteria.

## Choosing Typefaces

**Start with purpose, not aesthetics.** Ask:

1. What is the content's tone? (formal, casual, technical, friendly)
2. Where will it be read? (phone, desktop, print)
3. How long will people read? (glance vs. extended)
4. What personality should it project?

### Selection Process

1. **Define the job:** Body text? Headlines? UI elements? Each may need different faces
2. **Match tone to content:** A financial report needs different type than a bakery menu
3. **Test at actual sizes:** A face beautiful at 72px may be illegible at 14px
4. **Check the family:** Ensure needed weights, italics, and styles exist
5. **Test with real content:** Lorem ipsum hides problems

### Safe Starting Points

For body text, these reliably work:

| Serif | Sans-Serif |
|-------|------------|
| Georgia | -apple-system, BlinkMacSystemFont |
| Source Serif Pro | Source Sans Pro |
| Freight Text | Inter |
| Charter | IBM Plex Sans |
| Literata | Atkinson Hyperlegible |

## Pairing Typefaces

**One to two typefaces maximum.** More requires exceptional skill. When in doubt, use one family with weight variation.

### Contrast Principle

Successful pairings create **clear contrast**—faces should be obviously different, not confusingly similar.

| Contrast Type | Example |
|---------------|---------|
| Structure | Serif headline + sans-serif body |
| Weight | Light headline + regular body |
| Era | Humanist + geometric |
| Width | Condensed headline + normal body |

### Pairing Strategies

1. **Serif + Sans-serif:** The classic approach. Uses structural contrast.
2. **Same designer:** Faces designed by one person often share DNA that harmonizes (e.g., FF Meta + FF Meta Serif)
3. **Superfamilies:** Designed to work together (e.g., Roboto + Roboto Slab)
4. **Same era:** Typefaces from the same period share proportional assumptions

See [references/pairing-strategies.md](references/pairing-strategies.md) for specific combinations.

### Pairing Mistakes

- **Too similar:** Two serifs or two sans faces that look almost alike
- **Competing personality:** Both faces trying to be distinctive
- **Era clash:** Mixing renaissance and postmodern without intention
- **Weight imbalance:** One face overwhelms the other

## Typographic Measurements

| Property | Optimal Range | Notes |
|----------|---------------|-------|
| **Body font size** | 16-18px | 16px minimum; err larger for reading-heavy sites |
| **Line length (measure)** | 45-75 characters | 66 characters ideal; use `ch` unit or `max-width` |
| **Line height** | 1.4-1.8 | Longer lines need more; shorter need less |
| **Paragraph spacing** | 1em-1.5em | More space = more separation between ideas |
| **Heading scale** | 1.2-1.5 ratio | Establish clear hierarchy without extremes |

### Line Length Rules

```css
/* Optimal: 45-75 characters */
.prose { max-width: 65ch; }

/* If wider, increase line-height to compensate */
.wide-text {
  max-width: 80ch;
  line-height: 1.8;
}
```

### Line Height Adjustments

| Context | Line Height |
|---------|-------------|
| Headlines | 1.1-1.25 |
| Short UI text | 1.3-1.4 |
| Body paragraphs | 1.5-1.7 |
| Wide columns | 1.7-1.8 |

## Building Type Hierarchies

Create distinction through variation in three properties:

| Level | Size | Weight | Color |
|-------|------|--------|-------|
| H1 | 2.5-3rem | 700 | #111 |
| H2 | 1.75-2rem | 600 | #111 |
| H3 | 1.25-1.5rem | 600 | #333 |
| Body | 1rem (16-18px) | 400 | #333 |
| Secondary | 0.875rem | 400 | #666 |
| Caption | 0.75rem | 400 | #888 |

**Don't combine all levers at once.** H1 doesn't need to be largest AND boldest AND darkest. Use enough to create clear hierarchy, no more.

### Hierarchy Checklist

- [ ] Can you tell what's most important at a glance?
- [ ] Does squinting still reveal the hierarchy?
- [ ] Are there clear "levels" or does everything blend?
- [ ] Is there enough contrast between adjacent levels?

## Responsive Typography

Type must adapt to screens and reading contexts.

### Fluid Typography with clamp()

```css
/* Scales between 16px (320px viewport) and 20px (1200px viewport) */
body {
  font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
}

/* Fluid headings */
h1 {
  font-size: clamp(2rem, 1.5rem + 2vw, 3.5rem);
}
```

### Breakpoint Considerations

| Viewport | Adjustments |
|----------|-------------|
| Mobile (<640px) | Increase body size to 17-18px; reduce line-length limits; tighter heading scale |
| Tablet (640-1024px) | Standard sizing; enforce line-length limits |
| Desktop (>1024px) | Can use larger display type; maintain line-length |

See [references/responsive-typography.md](references/responsive-typography.md) for implementation patterns.

## Practical Checklist

Before shipping typography:

- [ ] Body text is 16px or larger
- [ ] Line length doesn't exceed 75 characters
- [ ] Line height is 1.4 or greater for body text
- [ ] Sufficient contrast between type levels
- [ ] Typefaces tested at actual sizes on actual screens
- [ ] Font files loading performantly (< 200KB total)
- [ ] Fallback fonts specified
- [ ] Works with browser zoom (test at 200%)
- [ ] Headings don't orphan single words on lines
- [ ] Links are visually distinct

## Quick Fixes

| Problem | Fix |
|---------|-----|
| Text feels cramped | Increase line-height to 1.6+; add paragraph spacing |
| Lines too long, hard to track | Add `max-width: 65ch` to text containers |
| Headings look disconnected | Reduce space above heading; keep space below |
| Text looks blurry | Check font-smoothing; try different weight; increase size |
| Fonts loading slowly | Subset fonts; use `font-display: swap`; preload critical fonts |
| Body text too small | Increase to 18px; mobile users hold phones farther than you think |
| Hierarchy is unclear | Increase size/weight differences between levels |
| Typefaces clash | Simplify to one face; or ensure clear contrast |
| Text hard to read | Check contrast ratio; increase font weight on light backgrounds |

## CSS Quick Reference

```css
/* Core typography setup */
body {
  font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 1.125rem;      /* 18px */
  line-height: 1.6;
  color: #333;
}

/* Constrain line length */
.prose {
  max-width: 65ch;
}

/* Heading rhythm */
h1, h2, h3 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  line-height: 1.2;
}

/* Fluid type */
h1 {
  font-size: clamp(2rem, 1.5rem + 2vw, 3rem);
}

/* Font loading */
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;
  font-weight: 400;
}
```

See [references/css-implementation.md](references/css-implementation.md) for complete patterns.

## Reference Files

- [typeface-anatomy.md](references/typeface-anatomy.md): Terminology, letterform parts, classification systems
- [evaluating-typefaces.md](references/evaluating-typefaces.md): Quality assessment, structural analysis, technical requirements
- [pairing-strategies.md](references/pairing-strategies.md): Combining typefaces, contrast methods, proven combinations
- [responsive-typography.md](references/responsive-typography.md): Fluid type, viewport units, breakpoint strategies
- [css-implementation.md](references/css-implementation.md): @font-face, loading strategies, variable fonts, performance

## Book Reference

**On Web Typography** by Jason Santa Maria
Publisher: A Book Apart (2014)
ISBN: 978-1937557065
[Amazon](https://www.amazon.com/Web-Typography-Jason-Santa-Maria/dp/1937557065?tag=wondelai-20)
