---
name: create-template
description: Create a new worldbuilding template for the Obsidian vault. Use when the user wants to add a new entity type template like "tavern template", "spell template", or "dungeon template".
argument-hint: "[template type]"
---

# Create Worldbuilding Template

Create a new worldbuilding template for: $ARGUMENTS

## Instructions

You are creating a new Obsidian template for a fantasy worldbuilding vault. Follow the established conventions exactly.

### Step 1: Determine Category and Filename

Based on the user's request, determine:
1. **Category folder**: Characters, Settlements, Items, Creatures, Organizations, Concepts, History, or Geography
2. **Filename**: Use Title Case with spaces (e.g., "Haunted House.md", "Trade Guild.md")

### Step 2: Template Structure

Every template MUST follow this exact structure:

```markdown
---
tags:
  - [category]
  - [subcategory]
name:
aliases: []
status: draft
# [Category]-Specific Fields
field_name:
another_field:
---

# {{title}}

> [!info] Generation Instructions
> When generating a [entity type], [guidance on what to create and focus areas]. [What makes this entity type interesting]. [Key aspects to include].

## Overview
> Write [X] sentences establishing [what the overview should cover].

## Classification
[Type and categorization options]

## [Domain-Specific Sections]
[Multiple sections with subsections, tables, and directive prompts]

## History
[Origin, major events, current situation]

## Key Figures
[Important associated characters]

## Secrets
1.
2.

## Plot Hooks
1.
2.
3.

## Image Prompts

### Art Style
**Hyper-realistic digital art, photorealistic rendering, cinematic lighting, rich textures, intricate detail on [relevant elements], dramatic atmosphere, depth of field, volumetric lighting, 8K quality, masterful composition.**

### [Scene Type 1]
**Template:**
> [Detailed scene description with placeholders in brackets]. Hyper-realistic digital art, photorealistic rendering, cinematic lighting, rich textures, dramatic atmosphere, depth of field, volumetric lighting, 8K quality, masterful composition. Fantasy [scene type] illustration.

**Prompt:**

### [Scene Type 2]
**Template:**
> [Second scene description with placeholders]. Hyper-realistic digital art, photorealistic rendering, cinematic lighting, rich textures, dramatic atmosphere, depth of field, volumetric lighting, 8K quality, masterful composition. Fantasy [scene type] illustration.

**Prompt:**

## Notes
Additional details and references.

## Connections
Link to related entities using `[[Entity Name]]` syntax.

### [Category]
- **[Relationship]:** [[]], [[]]
```

### Step 3: Writing Style Requirements

- **Directive language**: Use "Write 2-3 sentences...", "List 3-4...", "Describe in..."
- **Classification options**: Use parenthetical choices like "(Type A / Type B / Type C)"
- **Tables**: Use for structured data with clear headers
- **YAML fields**: Include relevant metadata for filtering (status always starts as "draft")
- **Two image prompt scenes**: Always include exactly 2 scene templates
- **Wikilinks**: Use `[[Entity Name]]` syntax in Connections section

### Step 4: Reference Existing Templates

Before creating, look at similar templates in the same category folder for:
- Appropriate YAML fields
- Section structure and depth
- Table formats used
- Connection categories

### Step 5: Create the Template

Write the complete template file to `Templates/[Category]/[Filename].md`

After creating, update CLAUDE.md:
1. Update the Project Structure comment for the category if needed
2. Update the Template Categories table with the new count and name
