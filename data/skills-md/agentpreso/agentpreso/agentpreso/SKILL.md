---
name: agentpreso
description: Create professional presentations from markdown. Use when users want to create slides, decks, presentations, or pitch decks. Supports charts, diagrams, themes, and export to PDF/PPTX.
---

# AgentPreso — AI-Native Presentations

Create professional slide decks from markdown with charts, diagrams, AI-generated graphics, and 10 built-in themes.

## Quick Start

```bash
# 1. Install the CLI
curl -fsSL https://agentpreso.com/install.sh | sh

# 2. Authenticate
agentpreso login

# 3. Create a deck (generates a markdown file from the theme scaffold)
agentpreso create my-deck --theme glacier

# 4. Push to cloud
agentpreso push my-deck.md

# 5. Render to PDF
agentpreso render my-deck.md --format pdf
```

## When to Use

Activate this skill when the user wants to:
- Create slides, presentations, decks, or pitch decks
- Add charts or diagrams to slides
- Export slides to PDF or PPTX
- Work with Marp markdown
- Mentions AgentPreso by name
- Needs a visual summary, report, or briefing in slide format

## Markdown Format

Decks are single `.md` files. Frontmatter sets metadata and theme:

```markdown
---
marp: true
theme: glacier
title: My Presentation
---

<!-- _class: title-hero -->

# Presentation Title

Subtitle or tagline

---

<!-- _class: bullets -->

# Key Points

- First insight with supporting detail
- Second insight with data
- Third insight with takeaway

---

<!-- _class: two-col -->

# Comparison

::: left

**Option A**
Description of the first option.

::: right

**Option B**
Description of the second option.
```

**Key syntax:**
- `---` separates slides
- `<!-- _class: layout-name -->` sets a slide layout
- `::: left`, `::: right`, `::: center` mark columns
- `<!-- _class: invert -->` enables dark mode on a slide
- `{{variable}}` template variables replaced at render time
- `asset://filename.png` references uploaded images
- Chart blocks: `` ```chart `` with YAML (type, data with labels/values or x/series)
- Diagram blocks: `` ```mermaid `` with Mermaid syntax
- AI images: `` ```generated_image `` with a text prompt

## Available Themes

| Theme | Description |
|-------|-------------|
| `agentpreso` | Navy & tangerine on warm ivory — the signature theme |
| `blueprint` | Technical, precise, engineering-focused |
| `botanica` | Nature-inspired, organic, warm greens |
| `chalk` | Blackboard-style, handwritten feel |
| `ember` | Warm, bold, fire-inspired gradients |
| `glacier` | Cool blues, icy, clean, corporate |
| `ink` | High-contrast black & white, editorial |
| `maison` | Elegant, luxury, sophisticated serif |
| `neon` | Vibrant, futuristic, dark with bright accents |
| `terminal` | Monospace, developer-focused, green on black |

## Available Layouts

| Layout | Description |
|--------|-------------|
| `title-hero` | Opening slide with large title and optional subtitle |
| `chapter` | Section divider with chapter title |
| `full-bleed-title` | Title over a full-bleed background image |
| `focus` | Single statement or key number, centered |
| `bullets` | Bullet list with automatic text fitting |
| `steps` | Numbered process or workflow steps |
| `stats-grid` | Grid of key metrics or statistics |
| `two-col` | Two equal columns side by side |
| `two-col-wide-right` | Two columns, right column wider |
| `three-col` | Three equal columns |
| `img-right` | Content left, image right |
| `img-left` | Image left, content right |
| `full-bleed` | Full-bleed image with overlaid text |
| `quote` | Blockquote with attribution |
| `summary` | Closing slide with key takeaways |

## Slide Design Principles

- **Every slide needs a visual** — use charts, diagrams, images, or icons. Walls of text lose the audience.
- **Vary your layouts** — alternate between bullets, two-col, img-right, stats-grid. Repetition is boring.
- **One idea per slide** — if you have two points, make two slides. Density kills clarity.
- **Preview before you are done** — render and review. Adjust text fitting, check image placement, verify chart readability.

## Review Strategy

After creating a deck, preview every slide and review for quality. Two approaches:

**Parallel (recommended when subagents are available):** Spawn read-only subagents to review slide PNGs in parallel — one per slide or batch of 2-3. Each subagent checks the 3-second test, title quality, text density, visual presence, and layout fit, then reports findings as text. The parent agent collects findings, edits the `.md` file once, and re-previews only changed slides. See `commands/create-deck.md` for the full protocol.

**Sequential (default):** Review each slide preview yourself, fix issues, re-push, re-preview until satisfied.

## Reference Files

Read these on demand for detailed guidance:

| File | Contents |
|------|----------|
| `references/cli-reference.md` | Full CLI command reference |
| `references/mcp-tools.md` | MCP tool reference |
| `references/slide-layouts.md` | Layout examples and usage |
| `references/themes.md` | Theme details and customization |
| `references/charts-diagrams.md` | Chart and diagram syntax |
| `references/custom-themes.md` | Creating custom themes |
| `references/markdown-format.md` | Complete markdown syntax |
| `references/export-formats.md` | Export format details |
| `references/presentation-craft.md` | Slide design best practices |
| `references/brand-logos.md` | Logo placement and branding |

## Examples

See the `examples/` directory for complete, valid AgentPreso markdown files demonstrating themes, layouts, charts, and diagrams.
