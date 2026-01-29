---
name: image-gen
description: Generate compelling cover images and in-article illustrations for technical articles using the imagen CLI tool. Use when asked to "generate images", "create cover image", "make article illustrations", "create visual assets", or "add images to article". Handles both high-impact conceptual cover images and technical diagrams/illustrations for specific concepts. Includes prompt engineering best practices and SEO-friendly image integration.
---

# Image Gen

## Contents

- [Overview](#overview)
- [When to Use This Skill](#when-to-use-this-skill)
- [Workflow](#workflow)
  - [Step 1: Analyze Article Content](#step-1-analyze-article-content)
  - [Step 2: Generate Cover Image](#step-2-generate-cover-image)
  - [Step 3: Generate In-Article Images](#step-3-generate-in-article-images-1-3)
  - [Step 4a: Integrate Images](#step-4a-integrate-images)
  - [Step 4b: Write ALT Text](#step-4b-write-alt-text)
  - [Step 5: Verify and Save](#step-5-verify-and-save)
- [Command Reference](#command-reference)
- [Prompt Engineering Best Practices](#prompt-engineering-best-practices)
- [Common Patterns](#common-patterns)
- [Resources](#resources)

## Overview

Generate high-quality images for technical articles using the `imagen` CLI tool (powered by `gemini-2.5-flash-image`). This skill provides a systematic workflow for creating two types of images:

1. **Cover Images**: High-impact, conceptual images that grab attention on LinkedIn/Medium
2. **In-Article Images**: Technical diagrams and illustrations that explain specific concepts

The skill includes comprehensive prompt engineering guidance and best practices for integrating images with SEO-friendly ALT text.

## When to Use This Skill

Invoke this skill when:
- Creating visual assets for a completed or near-complete article
- User requests "generate images for this article" or similar
- Article needs a cover image for publication
- Technical concepts would benefit from visual explanation
- Breaking up long text sections with relevant imagery
- Optimizing article for LinkedIn/Medium with visual appeal

**Typical workflow position**: After article content is finalized (Phase 8 in the article enhancement workflow), before SEO optimization.

## Workflow

### Step 1: Analyze Article Content

Before generating any images, analyze the article to identify:

1. **Article topic and key themes**: What is the main subject?
2. **Key concepts needing visualization**: Which technical ideas are complex or abstract?
3. **Section breaks**: Where would images improve readability?
4. **Target audience**: Developers? DevOps? Beginners or advanced?

**Output**: List of 2-4 images needed (1 cover + 1-3 in-article)

**Example**:
```
Article: "Mastering Alembic for Database Migrations"
Images needed:
- Cover: Conceptual image representing database evolution/migration
- Image 1: Diagram showing migration workflow
- Image 2: Visual comparing manual SQL vs Alembic automation
```

### Step 2: Generate Cover Image

Cover images should be **high-impact, conceptual, and visually interesting** to grab attention. They are often metaphorical rather than literal.

**Prompt Engineering for Covers**:

- **Style keywords**: `digital art`, `3D render`, `conceptual art`, `abstract`
- **Atmosphere**: `cinematic lighting`, `dramatic`, `futuristic`, `professional`
- **Composition**: Specify angle, focus, and elements
- **Structure**: `[Style] cover image of [Metaphor/Concept] representing [Article Topic], [Atmosphere/Lighting], [Composition]`

**Command**:
```bash
imagen generate "DETAILED PROMPT" --output work/images/[article_name]_cover.png
```

**Example Prompts**:

For a Vertex AI article:
```bash
imagen generate "A stunning digital art cover image showing three glowing pathways converging into a central AI cloud platform. Each pathway is a different color (green, blue, gold) representing different AI models flowing into Google Cloud infrastructure. The scene has dramatic cinematic lighting with a futuristic tech aesthetic. Style: conceptual, 3D render, high-detail, professional." --output work/images/vertex_ai_cover.png
```

For an Alembic article:
```bash
imagen generate "A dramatic 3D render showing a database schema transforming like evolving architecture, with migration files as glowing blueprints guiding the transformation. Dark background with cinematic lighting highlighting the evolution process. Style: conceptual art, digital art, high-detail, professional." --output work/images/alembic_cover.png
```

**Tips**:
- Be specific and detailed (100+ words is fine)
- Use metaphors that resonate with the topic
- Specify lighting/atmosphere for mood
- Include "professional" or "high-detail" for quality

### Step 3: Generate In-Article Images (1-3)

In-article images should **explain or reinforce specific concepts** from the text. They are more direct and educational than cover images.

**Prompt Engineering for In-Article Images**:

- **Style keywords**: `technical diagram`, `blueprint`, `minimalist illustration`, `clean`
- **Clarity**: `clear labels`, `connecting arrows`, `color-coded`, `organized`
- **Purpose**: Focus on explaining one specific concept
- **Structure**: `[Style] showing [Specific Concept], [Visual Elements], [Labels/Clarity]`

**Command**:
```bash
imagen generate "CONCEPT-SPECIFIC PROMPT" --output work/images/[article_name]_[concept].png
```

**Example Prompts**:

For a technical diagram:
```bash
imagen generate "A clean technical diagram showing three distinct client libraries connecting to a central Vertex AI platform. Use color-coded arrows: green for native Google SDK, blue for partner Anthropic SDK, and gold for OpenAI-compatible SDK. Include clear labels for each connection path. Style: blueprint, technical diagram, clear labels, professional." --output work/images/vertex_ai_three_patterns.png
```

For a comparison illustration:
```bash
imagen generate "A minimalist side-by-side comparison showing traditional infrastructure (left) with tangled wires and manual configuration versus modern infrastructure-as-code (right) with clean, organized flow. Use contrasting colors and simple icons. Style: clean, minimalist illustration, symbolic." --output work/images/traditional_vs_iac.png
```

For a workflow diagram:
```bash
imagen generate "A flowchart-style diagram showing the Alembic migration workflow: 1) Model changes → 2) Auto-generate migration → 3) Review migration → 4) Apply to database. Use arrows connecting each step with clear labels. Style: blueprint, technical flowchart, organized, clean." --output work/images/alembic_workflow.png
```

**Tips**:
- Focus on **one concept per image**
- Use color-coding to distinguish elements
- Request "clear labels" or "connecting arrows" for clarity
- Simpler is often better for technical diagrams

### Step 4a: Integrate Images

**CRITICAL**: Integrate generated images into the article at strategic locations.

**Integration Checklist**:
1. Create `work/images/` directory if needed
2. Verify all images generated successfully (cover + in-article)
3. Add cover image immediately after H1 title
4. Add in-article images at strategic section breaks
5. Save updated article as new version (e.g., `v8_with_images.md`)

**Markdown Integration Format**:

```markdown
# Article Title

![Cover image description here](images/article_cover.png)

## Introduction

Text introducing the problem...

![Diagram description here](images/article_diagram.png)
```

### Step 4b: Write ALT Text

Write descriptive ALT text (50-125 characters) for each image to ensure accessibility and SEO.

**Good ALT Text** (descriptive, specific):
- "Architecture diagram showing Cloud Run connecting through VPC Connector to AlloyDB in private subnet"
- "Comparison showing manual infrastructure with tangled wires versus automated infrastructure-as-code"
- "Flowchart illustrating Alembic migration workflow from model changes to database update"

**Bad ALT Text** (vague, non-descriptive):
- "diagram" or "image"
- "architecture" (too vague)
- "image1.png" or "screenshot"

### Step 5: Verify and Save

**Final checks**:
1. All images generated successfully (check file paths)
2. Images linked correctly in markdown
3. ALT text is descriptive and SEO-friendly (50-125 chars)
4. Cover image placed after H1 title
5. In-article images at logical section breaks
6. New version saved (e.g., `work/draft/article_v8_with_images.md`)

**Typical outputs**:
- 1 cover image (`*_cover.png`)
- 1-3 in-article images (`*_concept.png`, `*_workflow.png`, etc.)
- Updated article with integrated images and ALT text

## Command Reference

**Basic Usage**:
```bash
imagen generate "PROMPT" --output FILENAME.png
```

**Directory Setup**:
```bash
mkdir -p work/images
```

**Batch Generation Example**:
```bash
# Cover
imagen generate "COVER PROMPT" --output work/images/article_cover.png

# In-article images
imagen generate "DIAGRAM PROMPT" --output work/images/article_diagram.png
imagen generate "COMPARISON PROMPT" --output work/images/article_comparison.png
```

## Prompt Engineering Best Practices

For comprehensive prompt engineering guidance, refer to `references/prompting_guide.md`.

**Core Principles**:
1. **Be Specific**: Detailed descriptions produce better results
2. **Define Style**: Always specify artistic style (`digital art`, `blueprint`, etc.)
3. **Set Atmosphere**: Use lighting and mood keywords
4. **Use Photography Terms**: `wide-angle`, `close-up`, `depth of field`, etc.

**Cover vs In-Article Summary**:

| Aspect | Cover Images | In-Article Images |
|--------|-------------|-------------------|
| **Goal** | Grab attention, create "wow" factor | Explain concepts, reinforce learning |
| **Style** | `digital art`, `3D render`, `conceptual art` | `technical diagram`, `blueprint`, `minimalist` |
| **Approach** | Metaphorical, abstract | Direct, educational |
| **Keywords** | `cinematic`, `dramatic`, `futuristic` | `clean`, `clear labels`, `organized` |

## Common Patterns

**Pattern 1: Simple Article (1-2 images)**
- Cover image only
- OR Cover + 1 key diagram

**Pattern 2: Standard Article (2-3 images)**
- Cover image (conceptual)
- 1-2 in-article images (technical diagrams)

**Pattern 3: Complex Tutorial (3-4 images)**
- Cover image (conceptual)
- Workflow/architecture diagram
- Comparison illustration
- Example/output visualization

## Resources

### references/prompting_guide.md

Complete guide to prompt engineering for the `imagen` CLI, including:
- Detailed prompt crafting principles
- Style and medium keywords
- Lighting and atmosphere techniques
- Photography/cinematography terms
- Extensive examples for different image types

Load this reference when crafting complex prompts or needing inspiration for visual concepts.

