---
name: book-installer
description: Installs and configures project infrastructure including MkDocs Material intelligent textbook templates, learning graph viewers, and skill tracking systems. Routes to the appropriate installation guide based on what the user needs to set up.
---

# Book Installer

## Overview

This meta-skill handles installation and setup tasks for intelligent textbook projects. It consolidates three installation skills into a single entry point with on-demand loading of specific installation guides.

## When to Use This Skill

Use this skill when users request:

- Setting up a new MkDocs Material project
- Creating a new intelligent textbook from scratch
- Installing a learning graph viewer
- Setting up skill usage tracking with hooks
- Bootstrapping project infrastructure

## Step 1: Handle Help Requests

If the user asks for "help", "what can you do", or "list features", display this numbered list directly (do not load a reference file):

```
Book Installer Features (most → least common):

 1. Simple mkdocs.yml template - Minimal starter config for new projects
 2. Site logo - Add custom logo to header
 3. Favicon - Browser tab/bookmark icon
 4. Cover image & social preview - Home page image + og:image metadata
 5. Math equations - KaTeX (recommended) or MathJax
 6. Code syntax highlighting - Language-aware code blocks
 7. Code copy button - One-click copy for code blocks
 8. Mermaid diagrams - Flowcharts, sequence diagrams from text
 9. Content tabs - Tabbed sections for alternatives
10. Image zoom (GLightbox) - Click to enlarge images
11. Custom admonitions - Prompt boxes with copy button
12. Interactive quizzes - Self-assessment questions
13. Abbreviations & tooltips - Glossary hover definitions
14. Task lists - Checkbox lists
15. Simple feedback - Thumbs up/down per page
16. Detailed comments (Giscus) - GitHub Discussions integration
17. Tags & categorization - Page tagging system
18. Search enhancements - Suggestions and highlighting
19. Table of contents config - TOC sidebar options
20. Blog support - Add blog section
21. Announcement bar - Dismissible top banner
22. Privacy & cookie consent - GDPR compliance
23. Learning graph viewer - Interactive concept visualization
24. Skill usage tracker - Claude Code analytics hooks
25. Google Analytics - requires a Google Analytics property ID G-*
26. .gitignore installer - make sure that `site` and `.cache` are not in the main branch
27. extra CSS installer for iframe and customer prompt admonition
28. extra JavaScript installer - for prompt admonition copy button

Type a number or feature name to install.

Note: If you see `navigation.tabs` in mkdocs.yml, remove it. These books
use side navigation optimized for wide landscape screens.
```

After displaying the list, wait for user to specify which feature they want.

---

## Step 1b: Check for Navigation Tabs (Existing Projects)

When working with an existing mkdocs.yml, always check for and remove navigation tabs:

```yaml
# REMOVE these lines if present in mkdocs.yml:
theme:
  features:
    - navigation.tabs        # DELETE
    - navigation.tabs.sticky # DELETE
```

These books use side navigation optimized for wide landscape screens. Top navigation tabs waste vertical space and are not appropriate for this format.

---

## Step 2: Identify Installation Type

Match the user's request to the appropriate installation guide:

### Routing Table

| Trigger Keywords | Action | Purpose |
|------------------|--------|---------|
| help, what can you do, features, capabilities, list features | Display numbered list (Step 1) | Show quick feature overview |
| 1, simple mkdocs, minimal template, starter config | `references/mkdocs-template.md` (minimal section) | Create simple mkdocs.yml starter |
| enrich, add feature, number 2-24, specific feature name | `references/mkdocs-features.md` | Install specific feature |
| new project, mkdocs, textbook, bootstrap, setup, template, new book | `references/mkdocs-template.md` | Create new MkDocs Material project |
| graph viewer, learning graph, visualization, interactive graph, concept viewer | `references/learning-graph-viewer.md` | Add learning graph viewer to existing project |
| track skills, skill usage, activity tracking, hooks, usage analytics | `references/skill-tracker.md` | Set up skill tracking with hooks |
| cover image, home page, social media, og:image, montage, book cover, index page | `references/home-page-template.md` | Create home page with cover image and social metadata |
| logo, site logo, branding, upper left, header icon | `references/mkdocs-features.md` | Add custom logo with AI prompt examples |
| favicon, browser tab, bookmark icon, .ico | `references/mkdocs-features.md` | Add favicon with AI prompt examples |
| math, equations, latex, mathjax, katex | `references/mkdocs-features.md` | Add math equation support |
| quiz, quizzes, assessment, multiple choice | `references/mkdocs-features.md` | Add interactive quizzes |
| feedback, thumbs up, thumbs down, was this helpful | `references/mkdocs-features.md` | Add page feedback widget |
| comments, giscus, discussions | `references/mkdocs-features.md` | Add comment system |
| image zoom, lightbox, glightbox, click to enlarge | `references/mkdocs-features.md` | Add image zoom on click |
| code highlighting, syntax, copy button | `references/mkdocs-features.md` | Add code syntax highlighting |
| mermaid, diagrams, flowchart | `references/mkdocs-features.md` | Add Mermaid diagram support |
| admonition, callout, prompt box, copy prompt | `references/mkdocs-features.md` | Add custom admonitions with copy |

### Decision Tree

```
Asking for help or what book-installer can do?
  → YES: Display numbered list directly (Step 1)

Creating a new project/textbook from scratch?
  → YES: mkdocs-template.md

Adding a learning graph viewer to existing project?
  → YES: learning-graph-viewer.md

Setting up skill usage tracking?
  → YES: skill-tracker.md

Creating a cover image or setting up home page with social metadata?
  → YES: home-page-template.md

Want to add branding (logo, favicon, cover image)?
  → YES: mkdocs-features.md (Branding Features section)

Want to add a specific feature (equations, quizzes, feedback, etc.)?
  → YES: mkdocs-features.md (then follow specific feature instructions)
```

## Step 2: Load the Matched Guide

Read the corresponding guide file from `references/` and follow its installation workflow.

## Step 3: Execute Installation

Each guide contains:
1. Prerequisites and requirements
2. Step-by-step installation commands
3. Configuration options
4. Verification steps
5. Troubleshooting tips

## Available Installation Guides

### mkdocs-features.md

**Purpose:** Detailed configuration for all MkDocs feature enhancements

**Contains:** Full configuration snippets for features 2-24 listed in the help output, including:
- YAML for mkdocs.yml
- JavaScript files to create
- CSS files to create
- Usage examples

**Use when:**
- User selects a feature by number or name
- User wants detailed configuration for a specific feature
- User has a minimal mkdocs.yml and wants to enrich it

### mkdocs-template.md

**Purpose:** Bootstrap a complete MkDocs Material intelligent textbook project

**Creates:**
- Conda virtual environment named 'mkdocs'
- Full MkDocs Material project structure
- Custom CSS for branding
- Social media card plugins
- GitHub Pages deployment configuration

**Prerequisites:**
- Conda installed
- Git installed
- GitHub repository created

### learning-graph-viewer.md

**Purpose:** Add interactive learning graph exploration to existing textbook

**Creates:**
- Interactive vis-network graph viewer
- Search, filtering, and statistics features
- Integration with existing learning-graph.json

**Prerequisites:**
- Existing MkDocs project
- learning-graph.json file present

### skill-tracker.md

**Purpose:** Set up Claude Code skill usage tracking

**Creates:**
- Hook scripts for tracking skill invocations
- Activity log directory structure
- Reporting scripts for usage analysis

**Prerequisites:**
- Claude Code installed
- ~/.claude directory exists

### home-page-template.md

**Purpose:** Create professional home page with cover image and social media optimization

**Creates:**
- docs/index.md with proper frontmatter metadata
- AI image generation prompts for cover with montage background
- Open Graph and Twitter Card configuration

**Features:**
- Cover image design guidance (1.91:1 aspect ratio)
- Montage element suggestions by topic
- Social media preview optimization
- Example prompts for various book themes

**Prerequisites:**
- Existing MkDocs project
- Access to AI image generator (DALL-E, Midjourney, etc.)

## Examples

### Example 1: Ask for Help
**User:** "book-installer help"
**Routing:** Keyword "help" → Display numbered list
**Action:** Show the numbered feature list (Step 1), then wait for user to select a feature

### Example 2: Add a Specific Feature
**User:** "Add math equation support to my book"
**Routing:** Keyword "math" → `references/mkdocs-features.md`
**Action:** Load mkdocs-features.md, find the Math Equations section, and apply the configuration

### Example 2b: Select by Number
**User:** "5"
**Routing:** Number selection after help list → `references/mkdocs-features.md`
**Action:** Load mkdocs-features.md, find Math Equations (item 5), and apply the configuration

### Example 2c: Simple Template
**User:** "1"
**Routing:** Number 1 → `references/mkdocs-template.md` (minimal section)
**Action:** Load mkdocs-template.md and create a simple mkdocs.yml starter config

### Example 3: New Textbook Project
**User:** "I want to create a new intelligent textbook about machine learning"
**Routing:** Keywords "create", "new", "textbook" → `references/mkdocs-template.md`
**Action:** Read mkdocs-template.md and follow its workflow

### Example 4: Add Graph Viewer
**User:** "Add an interactive viewer for the learning graph"
**Routing:** Keywords "viewer", "learning graph", "interactive" → `references/learning-graph-viewer.md`
**Action:** Read learning-graph-viewer.md and follow its workflow

### Example 5: Track Skill Usage
**User:** "I want to track which skills I use most often"
**Routing:** Keywords "track", "skills", "usage" → `references/skill-tracker.md`
**Action:** Read skill-tracker.md and follow its workflow

### Example 6: Create Cover Image
**User:** "Help me create a cover image for my textbook"
**Routing:** Keywords "cover image", "textbook" → `references/home-page-template.md`
**Action:** Read home-page-template.md and follow its workflow

### Example 7: Set Up Home Page with Social Sharing
**User:** "I need to add og:image metadata to my home page"
**Routing:** Keywords "og:image", "home page" → `references/home-page-template.md`
**Action:** Read home-page-template.md and follow its workflow

## Common Workflows

### Full Project Setup
For a complete new project, users typically run these installations in order:
1. `mkdocs-template.md` - Create the project structure
2. `home-page-template.md` - Create cover image and configure home page
3. `learning-graph-viewer.md` - Add graph visualization (after learning graph exists)
4. `skill-tracker.md` - Enable usage analytics (optional)

### Verification Commands

After any installation, verify with:
```bash
# For MkDocs projects
mkdocs serve
# Visit http://127.0.0.1:8000/[project-name]/

# For skill tracker
cat ~/.claude/activity-logs/skill-usage.jsonl | tail -5
```
