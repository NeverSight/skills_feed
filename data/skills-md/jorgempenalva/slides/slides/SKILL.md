---
name: slides
description: Generates branded presentations as PDF using Slidev. Auto-detects brand colors from the repo's Tailwind config, CSS variables, or design tokens. Use when asked to create a presentation, make slides, generate a deck, or prepare a slide deck on any topic.
---

# Slidev Presentations Skill

Generate branded presentations from natural language. Auto-detects brand colors from your repo configuration, generates Slidev markdown, and exports to PDF.

## Prerequisites

- Node.js >= 18
- If `presentations/` does not exist, run `bash scripts/init.sh` (path relative to this skill's directory) to scaffold the project

## Brand Discovery

On every presentation request, resolve brand colors before generating slides.

### Resolution Flow

1. **Check `presentations/brand.json`** — if it exists, read and use those colors. Skip to slide generation.
2. **Search the repo** for brand colors in this order:
   a. `tailwind.config.{js,ts,mjs,cjs}` — look in `theme.extend.colors` or `theme.colors` for primary/brand keys
   b. CSS/SCSS files — `:root` blocks with `--brand-*`, `--color-*`, or `--primary-*` custom properties
   c. Design token files — `tokens.json`, `design-tokens.json`, `theme.json`
   d. `package.json` — `theme` or `brand` fields
   e. Any `.claude/skills/*.md` files mentioning hex color codes
3. **If colors found** — generate `presentations/brand.json` and confirm with the user: "I found these brand colors in [source]. Should I use them?"
4. **If NOT found** — ask the user: "I couldn't find brand colors in your repo. Where should I get them? (company website, design file, specific file, or just give me a hex code)"
5. **Save** the resolved palette to `presentations/brand.json`

### brand.json Format

```json
{
  "name": "Company Name",
  "colors": {
    "primary-light": "#e8f4fd",
    "primary-medium": "#7fb8e0",
    "primary": "#2196f3",
    "primary-dark": "#1565c0",
    "heading": "#1a237e",
    "subheading": "#283593",
    "border": "#e0e0e0"
  }
}
```

### Deriving a Full Palette from a Single Color

When the user provides just one primary hex, derive the full palette by generating light/medium/dark/heading/subheading variants plus a neutral border (`#e0e0e0`).

---

## Slide Generation Workflow

### Step 1 — Gather Content

Ask the user (via AskUserQuestion) if not already clear: title, key content/topics, and optional slide count (default 6–8).

### Step 2 — Generate Slidev Markdown

Create the file at `presentations/output/<title-slug>.md` with:

1. **Frontmatter** — Slidev configuration
2. **`<style>` block** — Brand colors mapped to CSS variables (see Styling Rules)
3. **Slides** — Content formatted using Layout Patterns, separated by `---`

### Step 3 — Export to PDF

```bash
cd presentations && npx slidev export output/<title-slug>.md --output ./output/<title-slug>.pdf
```

Report the output path to the user when done.

---

## Frontmatter Template

Every generated presentation starts with:

```yaml
---
theme: default
title: "<user-title>"
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
---
```

---

## Styling Rules

Map `brand.json` colors to the `<style>` block inserted after the frontmatter:

```html
<style>
:root {
  --brand-primary-light: <colors.primary-light>;
  --brand-primary-medium: <colors.primary-medium>;
  --brand-primary: <colors.primary>;
  --brand-primary-dark: <colors.primary-dark>;
  --brand-heading: <colors.heading>;
  --brand-subheading: <colors.subheading>;
  --brand-border: <colors.border>;
}
.slidev-layout h1 {
  color: var(--brand-heading) !important;
  border-bottom: 3px solid var(--brand-primary);
  padding-bottom: 0.3rem;
}
.slidev-layout h2 {
  color: var(--brand-primary-dark) !important;
}
.slidev-layout h3 {
  color: var(--brand-subheading) !important;
}
.slidev-layout table th {
  background-color: var(--brand-heading) !important;
  color: white !important;
  padding: 0.5rem 0.75rem;
}
.slidev-layout table td {
  padding: 0.4rem 0.75rem;
  border-bottom: 1px solid var(--brand-border);
}
.slidev-layout table tr:nth-child(even) {
  background-color: var(--brand-primary-light);
}
.slidev-layout blockquote {
  border-left: 4px solid var(--brand-primary);
  background-color: var(--brand-primary-light);
  padding: 0.5rem 1rem;
  border-radius: 0 0.25rem 0.25rem 0;
}
.slidev-layout strong {
  color: var(--brand-heading);
}
</style>
```

---

## Layout Patterns

Use these 5 patterns when composing slides. Mix them based on content type.

### Title Slide

```markdown
# Presentation Title

## Subtitle or context

<div class="pt-12">
  <span class="px-2 py-1 rounded text-sm">Date or tagline</span>
</div>
```

### Bullet List

```markdown
# Slide Title

- Point one with **emphasis**
- Point two with supporting detail
- Point three
```

### Two-Column Layout

```markdown
# Slide Title

<div class="grid grid-cols-2 gap-8">
<div>

### Left Column
- Content here

</div>
<div>

### Right Column
- Content here

</div>
</div>
```

### Table

```markdown
# Slide Title

| Column A | Column B | Column C |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
```

### Blockquote / Highlight

```markdown
# Slide Title

> Key insight or quote that deserves emphasis.
> Can span multiple lines.

Supporting context below the quote.
```

---

## Export Instructions

### Standard Export

```bash
cd presentations && npx slidev export output/<slug>.md --output ./output/<slug>.pdf
```

### Output Files

- Markdown source: `presentations/output/<slug>.md`
- PDF export: `presentations/output/<slug>.pdf`

---

## Example Usage

**Simple topic:**
> "Create a presentation about our engineering team's 2024 accomplishments"

**Structured content:**
> "Make slides for the board meeting covering: revenue growth, customer acquisition, product roadmap, and hiring plan"

**With specifics:**
> "Generate a deck on microservices migration — 8 slides, cover current architecture, target state, timeline, risks, and team allocation"

---

## Notes

- Brand discovery runs only once per project (persisted in `brand.json`)
- Subsequent requests reuse existing `brand.json` without re-prompting
- If the user wants to change brand colors, delete `presentations/brand.json` and request a new presentation
- The `presentations/` directory is project-local (not committed to this skill's repo)
- This skill does NOT include any fixed templates — all content is generated dynamically from user input
