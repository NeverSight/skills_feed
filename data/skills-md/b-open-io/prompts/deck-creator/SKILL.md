---
name: Deck Creator
version: 1.0.0
description: This skill should be used when the user asks to "create a deck", "make a presentation", "build slides", "proposal deck", "pitch deck", "investor deck", "sales presentation", "design a deck", or needs to generate a complete slide deck with consistent visual style. Handles theme selection, copywriting, content planning, and parallel slide generation.
---

# Deck Creator

Create professional presentation decks with consistent visual style, compelling copy, and AI-generated slide images.

## When to Use

Use this skill when the user asks to:
- Create a presentation or slide deck
- Build a pitch deck, proposal, or sales presentation
- Design slides for a product launch, company overview, or partnership
- Generate a complete deck from a document, requirements, or brief

## Process Overview

The deck creation process follows 5 phases:

1. **Discovery** - Gather context, examples, and references
2. **Theme** - Establish visual style and color palette
3. **Copy** - Plan and write slide content using marketing principles
4. **Generation** - Create all slides in parallel with consistent style
5. **Assembly** - Optimize images and stitch into PDF

## Phase 1: Discovery

Before creating any slides, gather comprehensive information:

### Required Information

Ask these questions to understand the project:

```
1. AUDIENCE: Who is the primary audience? (investors, clients, internal team, partners)
2. PURPOSE: What is the goal? (persuade, inform, propose, sell, educate)
3. CONTEXT: What's the setting? (boardroom, conference, email attachment, webinar)
4. BRAND: Is there existing brand guidelines? (colors, fonts, logos)
5. REFERENCES: Any example decks you like the style of?
6. CONTENT: What documents/materials should inform the content?
   - PDFs, docs, or files to reference
   - Key messages that must be included
   - Topics to cover or avoid
7. LENGTH: How many slides? (recommend 10-16 for most presentations)
8. ASSETS: Any images, logos, or graphics to include?
```

### Reference Analysis

If user provides example decks or references:
- Analyze visual style, layout patterns, and color usage
- Note typography choices and hierarchy
- Identify recurring design elements
- Extract key messaging patterns

## Phase 2: Theme Selection

Establish a consistent visual system before generating slides.

### Option A: Use Theme Factory (Recommended)

Install and use the theme-factory skill for professional color schemes:

```bash
npx skills add anthropics/theme-factory
```

Then invoke to get a cohesive palette:
- Primary color (headlines, accents)
- Secondary color (supporting elements)
- Background color (slide base)
- Text colors (high contrast for readability)
- Accent colors (highlights, CTAs)

### Option B: Manual Theme Definition

If user has brand guidelines, define:

```
Background: #XXXXXX (dark backgrounds work best for projection)
Primary:    #XXXXXX (headlines, key accents)
Secondary:  #XXXXXX (supporting elements)
Text:       #FFFFFF / #000000 (high contrast)
Accent:     #XXXXXX (highlights, CTAs)
```

### Style Parameters

Define consistent visual style:

```yaml
Aspect Ratio: 16:9 (1920x1080)
Typography:
  Headlines: Bold, 48-64px
  Body: Regular, 18-24px
  Stats: Extra Bold, 72-96px
Iconography: Flat, 2px stroke, rounded corners
Layout: Card-based with generous whitespace
```

Document the complete theme in a THEME.md file for reference during generation.

## Phase 3: Copy & Content Planning

### Marketing Principles

Apply these copywriting principles:

1. **One Message Per Slide** - Each slide has a single clear takeaway
2. **Headlines Tell the Story** - Someone should understand the deck from headlines alone
3. **Show Don't Tell** - Use visuals, stats, and diagrams over text walls
4. **Problem → Solution → Proof** - Classic persuasion structure
5. **Concrete > Abstract** - Specific numbers beat vague claims
6. **End with Action** - Clear next steps and CTA

### Optional: Marketing Skills

For enhanced copywriting, install:

```bash
npx skills add coreyhaines31/marketingskills
```

### Content Planning Template

Create a DECK-PLAN.md with:

```markdown
# [Deck Title]

## Deck Overview
- Audience:
- Goal:
- Key Message:
- Slides: [10-16]

## Slide Plan

### Slide 1: [Title]
- Type: Title
- Headline:
- Subhead:
- Visual:
- Key Message:

### Slide 2: [Problem/Opportunity]
- Type: Problem Statement
- Headline:
- Content Points:
- Visual:
- Key Message:

[Continue for all slides...]
```

### Content Gathering Loop

**Continue prompting the user until you have enough content for 10-16 slides:**

If information is missing, ask:
- "What specific problem does this solve?"
- "What are the 3-4 key benefits?"
- "What data or proof points support this?"
- "Who are the competitors and how do you differentiate?"
- "What's the timeline or next steps?"
- "What objections might the audience have?"

Do not proceed to generation until the content plan is complete.

## Phase 4: Slide Generation

### Pre-Generation Checklist

Before generating, confirm:
- [ ] Theme defined (colors, typography, style)
- [ ] All slides planned (10-16 slides)
- [ ] Each slide has: headline, content, visual concept
- [ ] Consistent terminology and messaging
- [ ] Output directory created

### Generation Prompts

Each slide prompt should include:

```
Create a professional presentation slide.

**Slide [N]: [Title]**

Specifications:
- Dimensions: 1920x1080 pixels (16:9 aspect ratio)
- Background: [background color]
- Style: [defined style - flat, modern, infographic, etc.]

Visual elements:
[Describe the visual layout, icons, diagrams, charts]

Text to include:
- Title: "[Headline]" ([primary color], bold)
- [Content elements with positioning]
- Footer: "[Company/Contact]" (small, bottom)

Save to: [output path]/[NN]-[slug].png
```

### Parallel Generation

**Launch all slide generation agents simultaneously** for efficiency:

```
Use Task tool with subagent_type=gemskills:content-specialist
Run all slide generations in parallel in a single message
```

Each agent receives:
- The complete theme specification
- The slide-specific prompt
- The output path

### Post-Generation

After all slides are generated:

1. **Verify Files** - Check all slides exist at correct paths
2. **Optimize Images** - Run optimization to reduce file sizes:
   ```bash
   # Use the optimize-images skill on the slides directory
   /optimize-images ./slides
   ```
3. **Stitch PDF** - Combine slides into single PDF:
   ```bash
   # Use kebab-case filename derived from deck title
   # Example: "Scribe Product Overview" → deck-scribe-product-overview.pdf
   bun run ~/code/prompts/skills/deck-creator/scripts/stitch-to-pdf.ts ./slides ./deck-{title-in-kebab-case}.pdf
   ```
4. **Create Index** - Generate DECK-INDEX.md with slide inventory + PDF path
5. **Provide Summary** - List all slides with file paths and PDF location

## Phase 5: PDF Assembly

After all slides are generated, optimized, and verified, combine them into a single PDF:

### Prerequisites

Ensure `pdf-lib` is available:
```bash
bun add pdf-lib
```

### Run the Stitch Script

```bash
# Derive filename from deck title using kebab-case with "deck-" prefix
# Examples:
#   "Investor Pitch 2024" → deck-investor-pitch-2024.pdf
#   "Scribe Product Overview" → deck-scribe-product-overview.pdf
bun run ~/code/prompts/skills/deck-creator/scripts/stitch-to-pdf.ts ./slides ./deck-{title}.pdf
```

The script will:
- Find all PNG files in the slides directory
- Sort them by numeric prefix (01-, 02-, etc.)
- Embed each as a full-page image in the PDF
- Create a PDF with pages sized to match slide dimensions (1920x1080)

### Verification

After stitching:
- Open the PDF and verify all slides are present
- Check correct order (should match numeric prefixes)
- Confirm full resolution with no quality loss

## Output Structure

```
project/deck/
├── THEME.md                        # Visual style definition
├── DECK-PLAN.md                    # Content planning document
├── DECK-INDEX.md                   # Final deck inventory
├── deck-{title-kebab-case}.pdf     # Combined presentation PDF
└── slides/
    ├── 01-title.png
    ├── 02-problem.png
    ├── 03-solution.png
    ...
    └── 14-closing.png
```

**PDF Naming**: Derive from deck title, kebab-case, prefixed with `deck-`. Example: "Q1 Sales Review" → `deck-q1-sales-review.pdf`

## Slide Type Templates

### Title Slide
- Company/project name
- Tagline or value proposition
- Visual: Abstract or product imagery
- Presenter info (optional)

### Problem/Opportunity
- Pain points or market gap
- Statistics that demonstrate scale
- Visual: Icons, comparison chart

### Solution
- What you're proposing
- Key differentiators
- Visual: Product screenshot or diagram

### How It Works
- Process flow (3-5 steps)
- Visual: Flowchart or numbered steps

### Benefits/Value
- 3-6 key benefits
- Visual: Icon grid or cards

### Social Proof
- Testimonials, logos, case studies
- Visual: Quote cards, logo grid

### Team/About
- Key team members or company info
- Visual: Photos or company timeline

### Metrics/Traction
- Key numbers and growth
- Visual: Charts, gauges, stats

### Competitive Advantage
- Comparison or positioning
- Visual: Matrix, comparison table

### Roadmap/Timeline
- Phases or milestones
- Visual: Horizontal timeline

### Pricing/Plans
- Options and what's included
- Visual: Pricing cards

### Next Steps/CTA
- Clear action items
- Contact information
- Visual: Minimal, focused

### Closing
- Memorable quote or summary
- Contact details
- Visual: Elegant, minimal

## Best Practices

1. **Uniform Style** - Every slide uses the same theme parameters
2. **Consistent Terminology** - Use the same words for concepts throughout
3. **Visual Hierarchy** - Headlines largest, supporting text smaller
4. **Generous Whitespace** - Don't overcrowd slides
5. **Center-Weight Important Elements** - Account for cropping
6. **High Contrast** - Ensure readability on projectors
7. **No Orphan Slides** - Every slide connects to the narrative

## Reference Files

For detailed guidance:
- **`references/slide-types.md`** - Expanded templates for each slide type
- **`references/copywriting.md`** - Marketing copy principles
- **`examples/`** - Example deck plans and outputs
