---
name: baoyu-infographic
description: Generate professional infographics with 20 layout types and 17 visual styles. Analyzes content, recommends layout×style combinations, and generates publication-ready infographics. Use when user asks to create "infographic", "信息图", or "visual summary".
---

# Infographic Generator

Generate professional infographics with two dimensions: layout (information structure) and style (visual aesthetics).

## Usage

```bash
# Auto-recommend combinations based on content
/baoyu-infographic path/to/content.md

# Specify layout
/baoyu-infographic path/to/content.md --layout hierarchical-layers

# Specify style (default: craft-handmade)
/baoyu-infographic path/to/content.md --style technical-schematic

# Specify both
/baoyu-infographic path/to/content.md --layout funnel --style corporate-memphis

# With aspect ratio
/baoyu-infographic path/to/content.md --aspect portrait

# Direct content input
/baoyu-infographic
[paste content]

# Direct input with options
/baoyu-infographic --layout linear-progression --style aged-academia
[paste content]
```

## Options

| Option | Description |
|--------|-------------|
| `--layout <name>` | Information layout (20 options, see Layout Gallery) |
| `--style <name>` | Visual style (17 options, default: craft-handmade) |
| `--aspect <ratio>` | landscape (16:9), portrait (9:16), square (1:1) |
| `--lang <code>` | Output language (en, zh, ja, etc.) |

## Two Dimensions

| Dimension | Controls | Count |
|-----------|----------|-------|
| **Layout** | Information structure: hierarchy, flow, relationships | 20 types |
| **Style** | Visual aesthetics: colors, textures, artistic treatment | 17 types |

Layout × Style can be freely combined. Example: `--layout hierarchical-layers --style craft-handmade` creates a hierarchy with playful hand-drawn aesthetics.

## Layout Gallery

| Layout | Best For |
|--------|----------|
| `linear-progression` | Timelines, step-by-step processes, tutorials |
| `binary-comparison` | A vs B, before-after, pros-cons |
| `comparison-matrix` | Multi-factor comparisons |
| `hierarchical-layers` | Pyramids, concentric circles, priority levels |
| `tree-branching` | Categories, taxonomies |
| `hub-spoke` | Central concept with related items |
| `structural-breakdown` | Exploded views, cross-sections, part labeling |
| `bento-grid` | Multiple topics, overview (default) |
| `iceberg` | Surface vs hidden aspects |
| `bridge` | Problem-solution, gap-crossing |
| `funnel` | Conversion processes, filtering |
| `isometric-map` | Spatial relationships, locations |
| `dashboard` | Metrics, KPIs, data display |
| `periodic-table` | Categorized collections |
| `comic-strip` | Narratives, sequences |
| `story-mountain` | Plot structure, tension arcs |
| `jigsaw` | Interconnected parts |
| `venn-diagram` | Overlapping concepts |
| `winding-roadmap` | Journey, milestones |
| `circular-flow` | Cycles, recurring processes |

Detailed layout definitions: `references/layouts/<layout>.md`

## Style Gallery

| Style | Description |
|-------|-------------|
| `craft-handmade` (Default) | Hand-drawn illustration, paper craft aesthetic |
| `claymation` | 3D clay figures, playful stop-motion |
| `kawaii` | Japanese cute, big eyes, pastel colors |
| `storybook-watercolor` | Soft painted illustrations, whimsical |
| `chalkboard` | Colorful chalk on black board |
| `cyberpunk-neon` | Neon glow on dark, futuristic |
| `bold-graphic` | Comic style, halftone dots, high contrast |
| `aged-academia` | Vintage science, sepia sketches |
| `corporate-memphis` | Flat vector people, vibrant fills |
| `technical-schematic` | Blueprint, isometric 3D, engineering |
| `origami` | Folded paper forms, geometric |
| `pixel-art` | Retro 8-bit, nostalgic gaming |
| `ui-wireframe` | Grayscale boxes, interface mockup |
| `subway-map` | Transit diagram, colored lines |
| `ikea-manual` | Minimal line art, assembly style |
| `knolling` | Organized flat-lay, top-down |
| `lego-brick` | Toy brick construction, playful |

Detailed style definitions: `references/styles/<style>.md`

## Recommended Combinations

Based on content analysis, the system recommends 3-5 layout×style combinations:

| Content Type | Recommended Combination |
|--------------|------------------------|
| Timeline/History | `linear-progression` + `craft-handmade` |
| Step-by-step Process | `linear-progression` + `ikea-manual` |
| Comparison (A vs B) | `binary-comparison` + `corporate-memphis` |
| Hierarchy/Levels | `hierarchical-layers` + `craft-handmade` |
| Relationships/Overlap | `venn-diagram` + `craft-handmade` |
| Conversion/Sales | `funnel` + `corporate-memphis` |
| Recurring Process | `circular-flow` + `craft-handmade` |
| Technical/System | `structural-breakdown` + `technical-schematic` |
| Data/Metrics | `dashboard` + `corporate-memphis` |
| Educational/Overview | `bento-grid` + `chalkboard` |
| Journey/Roadmap | `winding-roadmap` + `storybook-watercolor` |
| Categories/Types | `periodic-table` + `bold-graphic` |

**Default combination**: `bento-grid` + `craft-handmade`

## File Structure

Each session creates an independent directory:

```
infographic/{topic-slug}/
├── source-{slug}.{ext}             # Source files
├── analysis.md                     # Deep content analysis
├── structured-content.md           # Instructional content structure
├── prompts/
│   └── infographic.md              # Generated prompt
└── infographic.png                 # Output image
```

**Slug Generation**:
1. Extract main topic from content (2-4 words, kebab-case)
2. Example: "Machine Learning Basics" → `ml-basics`

**Conflict Resolution**:
If `infographic/{topic-slug}/` already exists:
- Append timestamp: `{topic-slug}-YYYYMMDD-HHMMSS`
- Example: `ml-basics` exists → `ml-basics-20260120-103052`

## Instructional Design Approach

This skill applies a **world-class instructional designer** mindset to infographic creation:

1. **Deep Understanding**: Read and comprehend the source material thoroughly
2. **Learning Objectives**: Identify what the viewer should understand after seeing the infographic
3. **Information Architecture**: Structure content for maximum clarity and retention
4. **Visual Storytelling**: Use visuals to communicate complex ideas accessibly
5. **Verbatim Data**: Preserve all source data exactly as written—no summarization or rephrasing of facts

## Workflow

### Step 1: Analyze Content → `analysis.md`

Read source content and perform deep instructional analysis.

**Actions**:
1. **Save source content** (if not already a file):
   - If user provides a file path: use as-is
   - If user pastes content: save to `source.md` in target directory

2. **Deep reading**:
   - Read the entire document thoroughly
   - Develop deep understanding before proceeding
   - Identify the core message and purpose

3. **Content analysis**:
   | Aspect | Questions to Answer |
   |--------|---------------------|
   | **Main Topic** | What is this content fundamentally about? |
   | **Data Type** | Timeline? Hierarchy? Comparison? Process? Relationships? |
   | **Complexity** | Simple (3-5 points) or complex (6-10+ points)? |
   | **Tone** | Technical, educational, playful, serious, persuasive? |
   | **Audience** | Who is the intended viewer? What do they already know? |

4. **Language detection**:
   - Detect **source language** from content
   - Detect **user language** from conversation
   - Note if source_language ≠ user_language (will ask in Step 4)

5. **Extract design instructions** from user input:
   - Style preferences (colors, mood, aesthetic)
   - Layout preferences (structure, organization)
   - Any specific visual requirements
   - Separate these from content—they go in the Design Instructions section

6. **Save to `analysis.md`**

**Analysis Output Format**:
```yaml
---
title: "[Main topic title]"
topic: "[Category: educational/technical/business/etc.]"
data_type: "[timeline/hierarchy/comparison/process/etc.]"
complexity: "[simple/moderate/complex]"
source_language: "[detected language]"
user_language: "[user's language]"
---

## Main Topic
[1-2 sentence summary of what this content is about]

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. [Primary objective]
2. [Secondary objective]
3. [Tertiary objective if applicable]

## Target Audience
- **Knowledge Level**: [Beginner/Intermediate/Expert]
- **Context**: [Why they're viewing this]
- **Expectations**: [What they hope to learn]

## Content Type Analysis
- **Data Structure**: [How information relates to itself]
- **Key Relationships**: [What connects to what]
- **Visual Opportunities**: [What can be shown rather than told]

## Design Instructions (from user input)
[Any style, color, layout, or visual preferences extracted from user's steering prompt]
```

### Step 2: Generate Structured Content → `structured-content.md`

Transform analyzed content into a structured format for the infographic designer.

**Instructional Design Process**:

1. **Create high-level outline**:
   - Title that captures the essence
   - List all main learning objectives
   - Identify the logical flow

2. **Flesh out each section**:
   - For each learning objective, create a section
   - Mix conceptual explanations with practical elements
   - Preserve all source data **verbatim**—do not summarize or rephrase

3. **Structure for visual communication**:
   - Identify what becomes a headline
   - Identify what becomes supporting text
   - Identify what becomes a visual element
   - Identify data points, statistics, or quotes

**Critical Rules**:
| Rule | Requirement |
|------|-------------|
| **Output format** | Markdown only |
| **Tone** | Expert trainer: knowledgeable, clear, encouraging |
| **No new information** | Do not add anything not in the source |
| **Verbatim data** | All statistics, quotes, and facts copied exactly |

**Structured Content Format**:
```markdown
# [Infographic Title]

## Overview
[Brief description of what this infographic conveys]

## Learning Objectives
The viewer will understand:
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

---

## Section 1: [Section Title]

**Key Concept**: [One-sentence summary]

**Content**:
- [Point 1 - verbatim from source]
- [Point 2 - verbatim from source]
- [Point 3 - verbatim from source]

**Visual Element**: [What to show visually]

**Text Labels**:
- Headline: "[Exact text for headline]"
- Subhead: "[Exact text for subhead]"
- Labels: "[Label 1]", "[Label 2]", ...

---

## Section 2: [Section Title]
[Continue pattern...]

---

## Data Points (Verbatim)
[All statistics, numbers, quotes exactly as they appear in source]
- "[Exact quote or statistic 1]"
- "[Exact quote or statistic 2]"

---

## Design Instructions
[Extracted from user's steering prompt]
- Style: [preferences]
- Colors: [preferences]
- Layout: [preferences]
- Other: [any other visual requirements]
```

### Step 3: Generate Layout×Style Recommendations

Based on analysis and structured content, recommend 3-5 combinations.

**Selection Criteria**:
| Factor | How to Match |
|--------|--------------|
| **Data structure** | Timeline→linear-progression, Hierarchy→hierarchical-layers, etc. |
| **Content tone** | Technical→technical-schematic, Playful→kawaii, etc. |
| **Audience** | Business→corporate-memphis, Educational→chalkboard, etc. |
| **Complexity** | Simple→sparse layouts, Complex→dense layouts |
| **User preferences** | Honor any design instructions from Step 1 |

**Format each recommendation**:
```
[Layout] + [Style]: [Brief rationale based on content analysis]
```

### Step 4: Confirm Options

**IMPORTANT**: Present ALL options in a single confirmation step using AskUserQuestion.

**Questions to ask**:

| Question | When to Ask |
|----------|-------------|
| Combination | Always (required) |
| Aspect ratio | Always |
| Language | Only if `source_language ≠ user_language` |

**AskUserQuestion format**:

**Question 1 (Combination)** - always:
- Option A (Recommended): [layout] + [style] - [brief rationale]
- Option B: [layout] + [style] - [brief rationale]
- Option C: [layout] + [style] - [brief rationale]
- Custom: Specify your own layout and/or style

**Question 2 (Aspect)** - always:
- landscape (16:9, Recommended) - standard presentation
- portrait (9:16) - mobile/social media
- square (1:1) - social media posts

**Question 3 (Language)** - only if source ≠ user language:
- [Source language] (matches content)
- [User language] (your preference)

**Language handling**:
- If source language = user language: Just inform user
- If different: Ask which language to use for all text

### Step 5: Generate Prompt → `prompts/infographic.md`

Create the image generation prompt.

**Process**:
1. Read layout definition from `references/layouts/<layout>.md`
2. Read style definition from `references/styles/<style>.md`
3. Read base prompt template from `references/base-prompt.md`
4. Combine with structured content from Step 2
5. **All text in prompt uses confirmed language**

**Prompt Structure**:
```markdown
Topic: [main topic from analysis]
Layout: [selected layout]
Style: [selected style]
Aspect: [confirmed ratio]
Language: [confirmed language]

## Layout Guidelines
[From layout definition file]

## Style Guidelines
[From style definition file]

## Content to Visualize

### Learning Objectives
[From structured-content.md]

### Sections
[From structured-content.md - each section with its visual elements]

### Data Points (Verbatim)
[All exact statistics, quotes, and facts from source]

## Text Labels (in [language])
[All text that appears in the infographic, organized by section]

## Design Instructions
[Any specific visual requirements from user's steering prompt]
```

### Step 6: Generate Image

**Image Generation Skill Selection**:
1. Check available image generation skills
2. If multiple skills available, ask user to choose

**Generation**:
Call selected image generation skill with:
- Prompt file path: `prompts/infographic.md`
- Output path: `infographic.png`
- Aspect ratio parameter if supported

**Error handling**:
- On failure, auto-retry once before reporting error
- If retry fails, inform user with error details

### Step 7: Output Summary

```
Infographic Generated!

Topic: [topic from analysis]
Layout: [layout name]
Style: [style name]
Aspect: [aspect ratio]
Language: [confirmed language]
Location: [output directory path]

Learning Objectives Covered:
1. [Objective 1] ✓
2. [Objective 2] ✓
3. [Objective 3] ✓

Files:
✓ analysis.md
✓ structured-content.md
✓ prompts/infographic.md
✓ infographic.png

Preview the image to verify it matches your expectations.
```

## Quality Checklist

Before generating the final image, verify:

- [ ] All source data preserved verbatim (no summarization)
- [ ] Learning objectives clearly represented
- [ ] Layout matches information structure
- [ ] Style matches content tone and audience
- [ ] All text labels in correct language
- [ ] Design instructions from user honored
- [ ] Visual hierarchy supports comprehension

## References

Detailed templates and guidelines in `references/` directory:
- `analysis-framework.md` - Instructional design analysis methodology
- `structured-content-template.md` - Structured content format and examples
- `base-prompt.md` - Base prompt template for image generation
- `layouts/<layout>.md` - Detailed layout definitions (20 files)
- `styles/<style>.md` - Detailed style definitions (17 files)

## Notes

- Layout determines information architecture; style determines visual treatment
- Default style `craft-handmade` works well with most layouts
- Technical content benefits from `technical-schematic` or `ui-wireframe`
- Educational content works well with `chalkboard`, `storybook-watercolor`
- Business content pairs with `corporate-memphis`, `dashboard`
- All text in the infographic uses the confirmed language
- **Never add information not present in the source document**
- **Statistics and quotes must be copied exactly—no paraphrasing**

## Extension Support

Custom styles and configurations via EXTEND.md.

**Check paths** (priority order):
1. `.baoyu-skills/baoyu-infographic/EXTEND.md` (project)
2. `~/.baoyu-skills/baoyu-infographic/EXTEND.md` (user)

If found, load before Step 1. Extension content overrides defaults.
