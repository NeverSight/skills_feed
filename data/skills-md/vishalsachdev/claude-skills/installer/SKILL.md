---
name: installer
description: Installs and configures project infrastructure including MkDocs Material intelligent textbook templates, learning graph viewers, and skill tracking systems. Routes to the appropriate installation guide based on what the user needs to set up.
---

# Installer

## Overview

This meta-skill handles installation and setup tasks for intelligent textbook projects. It consolidates three installation skills into a single entry point with on-demand loading of specific installation guides.

## When to Use This Skill

Use this skill when users request:

- Setting up a new MkDocs Material project
- Creating a new intelligent textbook from scratch
- Installing a learning graph viewer
- Setting up skill usage tracking with hooks
- Bootstrapping project infrastructure

## Step 1: Identify Installation Type

Match the user's request to the appropriate installation guide:

### Routing Table

| Trigger Keywords | Guide File | Purpose |
|------------------|------------|---------|
| new project, mkdocs, textbook, bootstrap, setup, template, new book | `references/mkdocs-template.md` | Create new MkDocs Material project |
| graph viewer, learning graph, visualization, interactive graph, concept viewer | `references/learning-graph-viewer.md` | Add learning graph viewer to existing project |
| track skills, skill usage, activity tracking, hooks, usage analytics | `references/skill-tracker.md` | Set up skill tracking with hooks |
| cover image, home page, social media, og:image, montage, book cover, index page | `references/home-page-template.md` | Create home page with cover image and social metadata |

### Decision Tree

```
Creating a new project/textbook from scratch?
  → YES: mkdocs-template.md

Adding a learning graph viewer to existing project?
  → YES: learning-graph-viewer.md

Setting up skill usage tracking?
  → YES: skill-tracker.md

Creating a cover image or setting up home page with social metadata?
  → YES: home-page-template.md
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

### Example 1: New Textbook Project
**User:** "I want to create a new intelligent textbook about machine learning"
**Routing:** Keywords "create", "new", "textbook" → `references/mkdocs-template.md`
**Action:** Read mkdocs-template.md and follow its workflow

### Example 2: Add Graph Viewer
**User:** "Add an interactive viewer for the learning graph"
**Routing:** Keywords "viewer", "learning graph", "interactive" → `references/learning-graph-viewer.md`
**Action:** Read learning-graph-viewer.md and follow its workflow

### Example 3: Track Skill Usage
**User:** "I want to track which skills I use most often"
**Routing:** Keywords "track", "skills", "usage" → `references/skill-tracker.md`
**Action:** Read skill-tracker.md and follow its workflow

### Example 4: Create Cover Image
**User:** "Help me create a cover image for my textbook"
**Routing:** Keywords "cover image", "textbook" → `references/home-page-template.md`
**Action:** Read home-page-template.md and follow its workflow

### Example 5: Set Up Home Page with Social Sharing
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
