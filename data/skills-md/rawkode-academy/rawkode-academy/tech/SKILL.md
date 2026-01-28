---
name: tech
description: Research, validate, and set up technology profiles in content/technologies. Handles both new entries and updates to existing ones.
license: Complete terms in LICENSE.txt
---

This skill helps maintain the `content/technologies` directory by researching, validating, and creating technology profiles.

When the user asks to add or check a technology (e.g., "Add Bun", "Check Kubernetes"), follow this process:

## 1. Research & Discovery

Use `WebSearch` to gather the following information about the technology:

- **Official Name** and **Description** (1-2 paragraphs summary).
- **Official Website** and **Documentation** URLs.
- **Source Code Repository** (GitHub/GitLab) and **License** (e.g., Apache-2.0, MIT).
- **Logos**: Look for official vector logos (SVG preferred). You will need paths for `icon`, `horizontal`, and `stacked`. (Note: You won't be able to download them directly to the specific filenames without `FetchUrl` or `curl`, so for now, just identify if they exist or create placeholders).
- **Key Features**: What are the main selling points?
- **Use Cases**: When should someone use this?
- **Core Concepts**: What are the main building blocks?
- **Ecosystem**: Related tools or integrations.

## 2. Check Existence

Check if `content/technologies/<slug>` exists. The slug should be the kebab-case version of the technology name.

## 3. Action: Create New (If it doesn't exist)

1.  Create the directory: `content/technologies/<slug>`.
2.  Create `index.mdx` with the following structure. **Strictly follow the frontmatter format.**

```yaml
---
name: "Technology Name"
description: |
  A comprehensive description of the technology.
  It can span multiple lines.
logos:
  icon: ./icon.svg
  horizontal: ./horizontal.svg
  stacked: ./stacked.svg
website: "https://official-website.com"
documentation: "https://docs.url"
license: "License-Type"
categories:
  - "category-1"
  - "category-2"
status: "sandbox" # Default to sandbox for new entries, or 'stable' if very mature
radar:
  status: assess # Default to assess
---

Introduction paragraph...

## What is [Technology]?
...

## Why [Technology] Matters in 2025
...

## Core [Technology] Concepts
...

## Getting Started with [Technology]
...

## Common Use Cases
...

## Best Practices for Production
...

## [Technology] Ecosystem and Tools
...

## Conclusion
...
```

3.  **Logos**: Since you cannot browse the web visually to pick the perfect SVG, leave the references in the frontmatter as `./icon.svg`, etc., but explicitly tell the user **"I have created the file structure. You will need to manually add the `icon.svg`, `horizontal.svg`, and `stacked.svg` files to the `content/technologies/<slug>` directory."**

## 4. Action: Validate & Update (If it exists)

1.  Read the existing `index.mdx`.
2.  Compare the `website`, `documentation`, and `license` fields with your research.
3.  If they differ, update them.
4.  Check if the content is outdated (e.g., refers to old versions or years). If so, propose updates to the "Why it matters" or "What is" sections.
5.  Report back to the user with a summary of what was validated and what was updated.

## General Guidelines

- **Tone**: informative, technical, and objective.
- **Formatting**: Use proper Markdown.
- **Files**: Do not create other files unless specifically asked.
