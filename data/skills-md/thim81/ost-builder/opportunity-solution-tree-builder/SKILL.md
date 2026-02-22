---
name: opportunity-solution-tree-builder
description: Create and edit Opportunity Solution Trees (OST) in ost-builder Markdown. Use when users ask how to create an Opportunity Solution Trees, format OST Markdown, convert a tree to Markdown, validate headings/status/metrics syntax, or troubleshoot why ost-builder is not parsing a tree correctly.
---

# Opportunity Solution Tree Builder

## Overview
Create Opportunity Solution Trees by writing structured Markdown headings with type prefixes, optional status tags, descriptions, and outcome metrics. Use this skill to explain or generate valid  Opportunity Solution Trees Markdown for ost-builder.

## Quick Start
Use these heading levels and prefixes:
- `## [Outcome]` for the main outcome
- `### [Opportunity]` for opportunities
- `#### [Solution]` for solutions
- `##### [Experiment]` for experiments

Optional status suffix (end of heading): `@on-track | @at-risk | @next | @done | @none`

Outcome metrics (only for outcomes):
- `- start: <number>`
- `- current: <number>`
- `- target: <number>`

## Visualize In The Web App
To visualize an OST, open `https://ost-builder.trinixlabs.dev/` and either:
- Paste your Markdown directly into the Markdown editor, or
- Upload your Markdown file if the upload option is available in the UI.
- Use the CLI to generate a share link and open the app:
  - `npx ost-builder your-file.md` (defaults to `--show`)
  - Options: `--show`, `--share`, `--share-base <url>`, `--format <json|markdown>`, `--pretty`, `--name <name>`

## Markdown Rules
- One card per heading line.
- Description text goes on the lines immediately below a heading.
- Keep child cards nested by heading level (Outcome > Opportunity > Solution > Experiment).
- Use blank lines between cards for readability.
- Status must appear at the very end of the heading line.
- Metrics are only read for Outcome cards.

## Example (Minimal)
```markdown
## [Outcome] Grow MAU to 120k @next
- start: 50
- current: 80
- target: 120

### [Opportunity] Improve onboarding
Reduce friction in the flow.

#### [Solution] Add questions to increase motivation

##### [Experiment] Test motivational copy variants
```

## Example (Full Tree)
```markdown
## [Outcome] Improve activation to 40% by Q2 @on-track
Increase successful onboarding completions.
- start: 22
- current: 31
- target: 40

### [Opportunity] Reduce friction in signup
Remove confusing steps and delays.

#### [Solution] Social sign-on
Allow Google and Apple sign-in.

##### [Experiment] Measure conversion lift
Compare social sign-on vs. email-only.

#### [Solution] Better error messaging
Make validation errors clear and actionable.

##### [Experiment] A/B test error copy
Test concise vs. detailed error messages.

### [Opportunity] Improve first-session value
Help users reach an “aha” moment fast.

#### [Solution] Guided checklist
Surface a 3-step activation checklist.

##### [Experiment] Checklist completion rate
Measure completion and activation impact.
```

## References
- For the full syntax and patterns, read `references/ost-markdown.md`.
