---
name: typography
description: Apply professional typography principles to create readable, hierarchical, and aesthetically refined interfaces. Use when setting type scales, choosing fonts, adjusting spacing, designing text-heavy layouts, implementing dark mode typography, or when asked about readability, font pairing, line height, measure, typographic hierarchy, variable fonts, font loading, or OpenType features.
---

# Typography

Professional typography for user interfaces, grounded in principles from the masters.

> "Typography exists to honor content." — Robert Bringhurst

## Reference Files

For detailed guidance on specific topics, consult these references:

| Topic | When to Read |
|-------|--------------|
| [masters.md](references/masters.md) | Seeking authoritative backing, making nuanced judgments, understanding "why" |
| [variable-fonts.md](references/variable-fonts.md) | Using variable fonts, fluid weight, performance optimization |
| [font-loading.md](references/font-loading.md) | FOIT/FOUT issues, preloading, Core Web Vitals, self-hosting |
| [opentype-features.md](references/opentype-features.md) | Ligatures, tabular numbers, stylistic sets, slashed zero |
| [fluid-typography.md](references/fluid-typography.md) | clamp(), text-wrap, truncation, vertical rhythm, font smoothing |
| [tailwind-integration.md](references/tailwind-integration.md) | Tailwind typography utilities, prose plugin, customization |
| [internationalization.md](references/internationalization.md) | RTL languages, Arabic/Hebrew, CJK, bidirectional text |

## Output Formats

### Type System Recommendations

```markdown
## Type System

### Scale
- Base: [size, e.g., 16px]
- Ratio: [e.g., Minor Third 1.200]
- Rationale: [why this ratio]

### Hierarchy
| Level | Size | Weight | Line Height | Letter Spacing | Use |
|-------|------|--------|-------------|----------------|-----|
| Display | ... | ... | ... | ... | Hero, marketing |
| H1 | ... | ... | ... | ... | Page titles |
| H2 | ... | ... | ... | ... | Section heads |
| Body | ... | ... | ... | ... | Paragraphs |
| Small | ... | ... | ... | ... | Captions, labels |

### Fonts
- Primary: [font] — [rationale]
- Secondary: [font, if applicable]
- Mono: [font, if applicable]

### Implementation
[Ready-to-use CSS/Tailwind]
```

### Typography Audits

```markdown
## Typography Audit

### Issues
| Element | Problem | Recommendation |
|---------|---------|----------------|
| ... | ... | ... |

### Quick Wins
- [Immediate improvement 1]
- [Immediate improvement 2]
```

---

## Core Principles

### The Four Fundamentals (Bringhurst)

The most important typographic considerations for body text:

1. **Point size** — 16px minimum for body; 14px absolute floor for secondary text
2. **Line spacing** — 1.5-1.7 for body; 1.1-1.3 for headings
3. **Line length** — 45-75 characters (66 ideal); use `max-w-prose` (~65ch)
4. **Font choice** — Match typeface to content and context

### Hierarchy Through Contrast

Establish hierarchy using multiple dimensions:

| Dimension | Low Contrast | High Contrast |
|-----------|--------------|---------------|
| Size | 14px → 16px | 16px → 48px |
| Weight | 400 → 500 | 400 → 700 |
| Color | Gray-600 → Gray-900 | Gray-400 → Black |
| Case | Normal | UPPERCASE |

> "Use one typeface per design. Avoid italics and bold—rely on gradations of scale instead." — Massimo Vignelli

### Restraint

- **1-2 font families maximum** — One serif, one sans if pairing
- **3-4 heading levels in practice** — Deeper nesting usually signals structure problems
- **Stick to your type scale** — Resist arbitrary sizes
- **Let whitespace work** — Don't fill every gap

> "In the new computer age, the proliferation of typefaces represents a new level of visual pollution." — Massimo Vignelli

---

## Type Scales

### Modular Scale Ratios

| Name | Ratio | Character |
|------|-------|-----------|
| Minor Second | 1.067 | Subtle, conservative |
| Major Second | 1.125 | Gentle, professional |
| Minor Third | 1.200 | Balanced, versatile |
| Major Third | 1.250 | Bold, impactful |
| Perfect Fourth | 1.333 | Strong hierarchy |
| Golden Ratio | 1.618 | Dramatic, editorial |

### Practical Scale (Minor Third @ 16px)

```css
--text-xs:   12px;  /* 0.75rem */
--text-sm:   14px;  /* 0.875rem */
--text-base: 16px;  /* 1rem */
--text-lg:   18px;  /* 1.125rem — not in pure scale */
--text-xl:   20px;  /* 1.25rem */
--text-2xl:  24px;  /* 1.5rem */
--text-3xl:  30px;  /* 1.875rem */
--text-4xl:  36px;  /* 2.25rem */
--text-5xl:  48px;  /* 3rem */
```

### When to Deviate

- **Marketing/hero:** Larger jumps allowed
- **Dense data interfaces:** Tighter scale
- **Mobile:** Slightly larger base (17-18px)

---

## Spacing Guidelines

### Line Height by Context

| Context | Line Height | Rationale |
|---------|-------------|-----------|
| Body text | 1.5-1.7 | Generous for readability |
| Headings | 1.1-1.3 | Tighter, especially large sizes |
| UI labels | 1.2-1.4 | Compact but legible |
| Buttons | 1.0-1.25 | Single line, tight |

> "The eye does not read letters, but the space between them." — Adrian Frutiger

### Letter Spacing

| Context | Tracking | CSS |
|---------|----------|-----|
| Body text | Default or +0.01em | `tracking-normal` |
| All caps | +0.05em to +0.1em | `tracking-wide` / `tracking-wider` |
| Large headings | -0.01em to -0.02em | `tracking-tight` |
| Small text (<14px) | +0.01em to +0.02em | `tracking-wide` |

**All-caps rule:** Always add tracking. Keep short (1-3 words).

### Paragraph Spacing

- **Between paragraphs:** 1em to 1.5em (equal to or slightly more than line-height)
- **After headings:** Reduced top margin on first paragraph
- **Between sections:** 2-3× paragraph spacing

---

## Font Selection

### System Font Stacks

```css
/* Sans-serif (modern) */
font-family: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";

/* Serif */
font-family: ui-serif, Georgia, Cambria, "Times New Roman", serif;

/* Monospace */
font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
```

### Safe Web Font Recommendations

| Category | Fonts | Use Case |
|----------|-------|----------|
| Sans-serif | Inter, Source Sans 3, Work Sans, DM Sans | UI, body text |
| Serif | Source Serif 4, Lora, Merriweather, Literata | Editorial, long-form |
| Monospace | JetBrains Mono, Fira Code, Source Code Pro | Code, data |
| Display | Fraunces, Epilogue, Outfit | Headlines |

### Pairing Principles

- **Pair by contrast** — Serif + sans-serif
- **Match x-height** — For visual harmony when mixed
- **Ensure weight availability** — Both need needed weights/styles

> "A father should not have a favorite among his daughters." — Hermann Zapf (on his typefaces)

---

## Modern CSS Typography

### Text Wrapping

```css
/* Balanced line lengths for headings (≤6 lines) */
h1, h2, h3, blockquote, figcaption {
  text-wrap: balance;
}

/* Prevent orphans in body text */
p, li {
  text-wrap: pretty;
}
```

**Caveat:** Don't use `balance` inside bordered containers—creates visual imbalance.

### Fluid Typography

```css
/* Font scales smoothly between breakpoints */
h1 {
  font-size: clamp(2rem, 1rem + 4vw, 4rem);
  line-height: clamp(1.1, 1.3 - 0.1vw, 1.3);
}

body {
  font-size: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
}
```

See [fluid-typography.md](references/fluid-typography.md) for complete scale.

### Text Truncation

```css
/* Single line */
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Multi-line (2 lines) */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

---

## Dark Mode Typography

### Weight Adjustment

Text appears heavier on dark backgrounds. Reduce weight slightly:

```css
@media (prefers-color-scheme: dark) {
  body {
    font-weight: 350; /* Instead of 400 */
  }
  h1, h2, h3 {
    font-weight: 600; /* Instead of 700 */
  }
}
```

### Font Smoothing

Apply antialiasing on dark backgrounds to counter perceived boldness:

```css
.dark-bg {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### Color Contrast

- Avoid pure white (#fff) on pure black (#000)—too harsh
- Use off-white (#f5f5f5) and near-black (#1a1a1a)
- Aim for 10:1 to 15:1 contrast in dark mode

---

## Typographic Details

### Quotation Marks

Use curly quotes, not straight:
- Correct: "Hello" and 'world'
- Incorrect: "Hello" and 'world'

### Dashes

| Type | Character | Use |
|------|-----------|-----|
| Hyphen | - | Word breaks, compounds |
| En dash | – | Ranges (2020–2024), relationships |
| Em dash | — | Parenthetical statements |

### Numbers

| Type | Use Case | CSS |
|------|----------|-----|
| Tabular | Tables, prices, alignment | `font-variant-numeric: tabular-nums` |
| Proportional | Body text | `font-variant-numeric: proportional-nums` |
| Old-style | Editorial content | `font-variant-numeric: oldstyle-nums` |
| Slashed zero | Code, data | `font-feature-settings: "zero" 1` |

See [opentype-features.md](references/opentype-features.md) for complete reference.

---

## Accessibility

### Minimums

| Element | Minimum | Preferred |
|---------|---------|-----------|
| Body text | 16px | 16-18px |
| Secondary text | 14px | 14-16px |
| Legal/caption | 12px | 12px + increased tracking |
| Contrast ratio | 4.5:1 | 7:1 |

### User Preferences

```css
/* Use relative units so users can scale */
body {
  font-size: 1rem; /* Not 16px */
}

/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  * {
    transition: none !important;
  }
}
```

### Dyslexia Considerations

- Avoid justified text
- Prefer sans-serif with distinct letterforms (a vs α, l vs 1 vs I)
- Generous line height and paragraph spacing
- Consider offering OpenDyslexic as option

---

## Common Mistakes

### Avoid

- All-caps body text or long headings
- Centered body paragraphs
- Line length over 80 characters
- Insufficient contrast for "aesthetic" reasons
- Mixing too many font families (>2)
- Decorative fonts for UI text
- Justified text on the web
- Tiny gray text on white backgrounds
- Letter-spacing on Arabic text

### Watch For

- Orphans and widows in prominent text
- Inconsistent heading hierarchy
- Missing font fallbacks
- Layout shift from web font loading
- Underlined text that isn't a link

---

## Quick Implementation

### Minimal Professional Setup

```css
:root {
  --font-sans: Inter, ui-sans-serif, system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;
}

body {
  font-family: var(--font-sans);
  font-size: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  line-height: 1.6;
  font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
}

h1, h2, h3 {
  line-height: 1.2;
  text-wrap: balance;
  letter-spacing: -0.02em;
}

p {
  text-wrap: pretty;
  max-width: 65ch;
}

code {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums slashed-zero;
}

@media (prefers-color-scheme: dark) {
  body {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
}
```

### Tailwind Quick Start

```html
<article class="
  prose prose-gray lg:prose-lg
  prose-headings:text-balance
  prose-p:text-pretty
  dark:prose-invert
  max-w-prose mx-auto
">
  <!-- Content -->
</article>
```

See [tailwind-integration.md](references/tailwind-integration.md) for complete patterns.
