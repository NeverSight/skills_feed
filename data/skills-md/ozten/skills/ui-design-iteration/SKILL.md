---
name: ui-design-iteration
description: Iterates on data-intensive UI designs to improve scannability, hierarchy, accessibility, and systematization. Use when improving an existing UI, reviewing a design for UX issues, or transforming a functional-but-flat interface into a polished product.
---

# UI Design Iteration

Transform functional-but-flat interfaces into scannable, actionable, accessible designs.

## Core Principles

### 1. Align labels with user intent
- Page titles and nav labels should reflect the user's job, not internal terminology
- Group navigation by intent (Create, Review, Analyze, Manage)
- Ensure naming consistency across title, nav, tabs, and empty states

### 2. Make primary actions unmistakable
- One primary CTA per screen with consistent placement
- Provide contextual "next step" affordances near where attention already is
- Secondary actions visible but subordinate; tertiary actions in overflow menus

### 3. Improve scannability through hierarchy
- Strengthen typographic hierarchy: title → section headers → row primary → metadata
- Consistent row heights, spacing, and alignment
- Use whitespace and dividers to encode structure, not decoration

### 4. Make state explicit everywhere
- Represent modes with tabs/segmented controls
- Selection needs multiple cues: indicator + weight + background (not color alone)
- Summarize active automation/filters where relevant

### 5. Systematize the visual design
- Standardize spacing, typography, and color via tokens
- Use accent color for priority and state, not decoration
- Build reusable components rather than one-off styles

## Iteration Playbook

### A. Reframe the page
Define the job statement: "User comes here to ____."
- Update page title and nav selection to reflect that job
- Remove ambiguous or overlapping labels

### B. Establish action hierarchy
Identify primary (most common), secondary (common but not main path), and tertiary (rare, collapse to overflow) actions.
- Only one primary button style per screen
- Place contextual next-step affordance near the data surface

### C. Chunk dense controls
Replace walls of toggles/fields with:
- Group headers + short descriptions
- Progressive disclosure for advanced settings
- Aligned labels and descriptions for quick scanning

### D. Increase scan speed for data surfaces
- Consistent columns and alignment
- Primary value bold, metadata muted
- Row actions right-aligned with overflow
- Truncation that preserves meaning (with tooltip/detail access)

### E. Clarify modes and location
- Top-level modes via tabs/segmented control
- Active filters shown as chips with clear remove affordance
- Context line under headers showing scope when needed

## Quick References

**Accessibility requirements**: See [CHECKLIST.md](CHECKLIST.md)
**Reusable component patterns**: See [COMPONENTS.md](COMPONENTS.md)

## Output Format

When completing an iteration, produce:

1. **Design intent** — 1-2 sentences on what job is supported and what changed
2. **Key UX changes** — Bulleted, mapped to the principles above
3. **Component updates** — What was created or standardized
4. **A11y verification** — Contrast, focus, labels, targets, truncation
5. **Known risks** — Only if materially impacting usability