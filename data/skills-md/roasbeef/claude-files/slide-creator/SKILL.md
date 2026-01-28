---
name: slide-creator
description: Transform written content (blog posts, newsletters, articles) into visual slide deck images. This skill should be used when converting text content into presentation format, creating slide graphics from outlines, or generating visual summaries of written material.
allowed-tools: Bash(python:*), Read, Write, Skill
---

# Slide Creator

This skill transforms written content into visual slide deck images using AI image generation. It analyzes text content, extracts key points, and generates presentation-quality slide images.

## Prerequisites

- The `nano-banana` skill must be available for image generation.
- Python 3.10+
- `google-genai` package installed

## Workflow Overview

1. **Input**: Receive content (blog post, article, newsletter, outline)
2. **Analysis**: Extract key points and structure
3. **Outline**: Create slide outline with titles and talking points
4. **Generation**: Create image prompts and generate slide images
5. **Refinement**: Accept feedback and regenerate specific slides

## Creating Slides from Content

### Step 1: Analyze the Content

Read and analyze the source content to identify:
- Main topic/theme
- Key sections or chapters
- Important points to visualize
- Logical flow and transitions

### Step 2: Create Slide Outline

Structure the presentation as:

```
Slide 1: Title slide (topic, subtitle)
Slide 2: Introduction/Problem statement
Slides 3-N: Key points (one concept per slide)
Slide N+1: Conclusion/Summary
Slide N+2: Call to action (optional)
```

### Step 3: Generate Image Prompts

For each slide, create an image prompt that:
- Captures the key concept visually
- Uses consistent style across all slides
- Leaves appropriate space for text overlay
- Matches the desired aspect ratio (typically 16:9)

### Step 4: Generate Slide Images

Use the nano-banana skill to generate images:

```bash
# Single slide
python ~/.claude/skills/nano-banana/scripts/generate_image.py \
    "Professional slide background: [concept], [style], 16:9 aspect, clean with text space" \
    slide_01.png --aspect 16:9

# Batch generation
python ~/.claude/skills/nano-banana/scripts/batch_generate.py \
    slide_prompts.json ./slides/ --aspect 16:9 --parallel 3
```

### Step 5: Refinement

Accept feedback and regenerate specific slides:

```bash
# Edit existing slide
python ~/.claude/skills/nano-banana/scripts/edit_image.py \
    slides/slide_03.png "make the colors more vibrant" slides/slide_03_v2.png
```

## Slide Prompt Patterns

### Title Slide
```
Bold typography-inspired background for [topic] presentation, [style], gradient [colors], modern and professional, 16:9 aspect ratio
```

### Concept Slide
```
Visual metaphor for [concept]: [metaphor description], [style], [brand colors], clean composition with space on [left/right] for text overlay, presentation graphic
```

### Data/Stats Slide
```
Abstract data visualization representing [metric/trend], infographic style, [colors], clean white background, professional presentation graphic
```

### Transition/Section Slide
```
Section divider for [section name], abstract [theme] imagery, gradient [colors], full bleed background, minimal text space
```

### Conclusion Slide
```
Inspiring background for conclusion: [theme], uplifting atmosphere, [colors], professional, space for summary points
```

## Style Presets

See [references/slide-styles.md](references/slide-styles.md) for pre-defined style presets:

- **Corporate**: Professional blues, clean lines, minimal
- **Creative**: Bold colors, dynamic compositions
- **Technical**: Dark theme, code/circuit aesthetics
- **Minimalist**: White space, subtle accents
- **Warm**: Earth tones, organic shapes

## Batch Generation Format

Create a `slide_prompts.json` file:

```json
[
    {
        "prompt": "Title slide for AI presentation, modern tech aesthetic, blue gradient, bold composition",
        "filename": "slide_01_title.png",
        "aspect": "16:9"
    },
    {
        "prompt": "Visual metaphor: neural network as interconnected nodes, tech illustration style, blue and purple",
        "filename": "slide_02_intro.png",
        "aspect": "16:9"
    },
    {
        "prompt": "Growth chart concept, abstract rising bars with glow effect, tech presentation style",
        "filename": "slide_03_growth.png",
        "aspect": "16:9"
    }
]
```

## Example: Blog Post to Slides

### Input Blog Post
```markdown
# The Future of Remote Work

Remote work is transforming how we think about productivity...

## Key Benefits
1. Flexibility
2. Work-life balance
3. Global talent access

## Challenges
- Communication
- Culture building
- Technology needs

## Best Practices
...
```

### Generated Slide Outline
```
1. Title: "The Future of Remote Work"
2. Hook: Remote work transformation visual
3. Benefits: Flexibility metaphor
4. Benefits: Work-life balance visual
5. Benefits: Global connectivity
6. Challenges: Communication barriers
7. Solutions: Best practices overview
8. Conclusion: Future outlook
```

### Generated Prompts
```json
[
    {"prompt": "Title slide: Future of Remote Work, modern office fading into home workspace, professional blue tones", "filename": "slide_01.png"},
    {"prompt": "Remote work transformation: office desk morphing into laptop anywhere, clean illustration style", "filename": "slide_02.png"},
    {"prompt": "Flexibility concept: person working from beach, mountain, city cafe montage, lifestyle photography style", "filename": "slide_03.png"}
]
```

## Tips for Quality Slides

1. **Consistency**: Use same style keywords across all prompts.
2. **Text Space**: Always include "space for text" or "clean area for overlay".
3. **Aspect Ratio**: Use 16:9 for standard presentations.
4. **One Concept**: Each slide should visualize ONE key point.
5. **Color Harmony**: Establish a palette and reference it in each prompt.

## Feedback Handling

When the user requests changes:

1. **Specific slide**: Regenerate just that slide with modified prompt.
2. **Style change**: Create new prompts and batch regenerate all.
3. **Minor edits**: Use edit_image.py for adjustments.
4. **Iterative**: Use chat_session.py for complex refinements.

## Output Structure

```
output_dir/
├── slide_01_title.png
├── slide_02_intro.png
├── slide_03_point1.png
├── slide_04_point2.png
├── slide_05_point3.png
├── slide_06_conclusion.png
└── slide_prompts.json  # Save prompts for reference
```
