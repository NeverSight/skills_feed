---
name: map-docs
description: This skill should be used when the user asks to "map documentation links", "extract docs navigation", "get documentation structure", "scrape docs sidebar", or wants to understand the structure of a documentation website before creating skills.
---

# Documentation Link Mapper

Map the navigation structure of documentation websites to understand their hierarchy before creating Claude Code skills.

## Purpose

Extract the sidebar/navigation structure from documentation sites, producing a hierarchical tree of sections and subsections with their URLs. This enables systematic skill creation covering each documentation area.

## When to Use

- Before creating skills for a library/framework
- When needing to understand docs structure
- When planning comprehensive documentation coverage

## Process

### Step 1: Fetch the Documentation Page

Use WebFetch to retrieve the documentation page and extract navigation links:

```
WebFetch the documentation URL with prompt:
"Extract the sidebar/navigation structure. Return a hierarchical list of all documentation sections and subsections with their URLs. Format as:

Section Name → /path
  - Subsection 1 → /path/subsection1
  - Subsection 2 → /path/subsection2

Include ALL navigation links, preserving parent-child relationships."
```

### Step 2: Format the Output

Present the structure as a tree showing the hierarchy:

```
Getting started
  - Installation → /docs/installation
  - Quick start → /docs/quickstart
API Reference
  - Methods → /docs/api/methods
  - Properties → /docs/api/properties
```

### Step 3: Identify Skill Groupings

Analyze the structure to suggest logical skill groupings:

1. **Core concepts** - Installation, getting started, basics
2. **API sections** - Methods, properties, events
3. **Advanced topics** - Performance, plugins, extensions
4. **Examples/Recipes** - Common patterns, tutorials

## Output Format

Provide both:

1. **Tree view** - Human-readable hierarchical structure
2. **Flat list** - All URLs for systematic crawling

## Tips

- Some sites load navigation dynamically - if WebFetch returns incomplete results, note this limitation
- Focus on the documentation sidebar, not header/footer navigation
- Preserve the exact URL paths for later content fetching
- Group related sections when suggesting skill structure

## Example Usage

User: "Map the animejs documentation structure"

Response:
1. Fetch https://animejs.com/documentation
2. Extract navigation structure
3. Present tree view
4. Suggest skill groupings for comprehensive coverage
