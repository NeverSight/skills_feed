---
name: personal-brand-video
description: Create or upgrade a personal branding/marketing video (e.g., founder intro, portfolio reel, LinkedIn/website hero) with a premium, modern aesthetic. Use when the user needs a Remotion-based personal brand video, wants a story/scene plan, visual system, motion design, or a full implementation. Always pair with the remotion-best-practices skill for Remotion rules and rendering constraints.
---

# Personal Brand Video

## Overview
Design and implement high‑quality personal brand videos that feel premium, concise, and conversion‑oriented, typically built in Remotion.

## Prerequisite: Remotion Skill
Install the Remotion best practices skill before using this skill:

```bash
npx skills add https://github.com/remotion-dev/skills --skill remotion-best-practices
```

## Workflow Decision Tree

1) **New build** → use the full workflow below.  
2) **Existing Remotion project** → jump to “Upgrade Pass” and “Implementation”.  
3) **Only script/storyboard requested** → use “Script & Structure” + “Storyboard Template” reference.

## Golden Rules

- **Use Remotion rules**: Always load and follow `remotion-best-practices` (no CSS animations, no CSS transitions; use `useCurrentFrame()` + `useVideoConfig()`).
- **Premium over busy**: Fewer elements, stronger hierarchy, precise motion, intentional spacing.
- **One message per scene**: Every scene should answer one question or show one proof point.
- **Brand consistency**: Typography, color, and icon style must be consistent across scenes.

## Step 1 — Intake & Goals

Collect these before coding (ask succinctly):
- Audience & platform: LinkedIn, website hero, email, keynote?
- Length target: 20–30s, 30–45s, or 45–60s?
- CTA: hire, book a call, join waitlist, view portfolio?
- Visual style: minimal, dark, light, tech‑lux, etc.
- Assets: headshot, logo, brand colors, product UI, screenshots.

If details are missing, **assume**: 26–35s, vertical 1080×1920, premium dark theme, founder/engineer voice.

## Step 2 — Script & Structure (Story Spine)

Default 6‑scene structure:
1. **Hook** (identity + domain)
2. **What I build** (capability)
3. **Proof** (metrics, case study, logos)
4. **How** (stack / workflow)
5. **Impact** (outcomes)
6. **CTA** (next step)

See `references/storyboard-template.md` for a concrete template.

## Step 3 — Visual System (Design Tokens)

Define:
- Typography scale (display → body → meta)
- Color tokens (bg, surface, accent, success)
- Gradients, glows, shadows, depth rules
- Icon system style (stroke width, corner radius, palette)

If a design system exists, **reuse it**. Otherwise create a small token set and use everywhere.

## Step 4 — Motion System

Use a small set of motion primitives:
- **Reveal**: opacity + translateY (ease out)
- **Scale‑in**: spring for hero elements
- **Stagger**: lists and badges
- **Pulse**: subtle for status/metrics

Document timing in frames (e.g., “hero reveal 0–18f”, “stagger 4f intervals”).

## Step 5 — Implementation (Remotion)

Always:
- Drive animations via `useCurrentFrame()` and `useVideoConfig()`.
- Use `interpolate()` or `spring()`, not CSS animations.
- Use `staticFile()` for assets.
- Keep each scene self‑contained and predictable.

Create shared components when repeating:
- `Typography`, `Icons`, `Metric`, `Badge`, `Card`, `SceneTitle`.

## Step 6 — Upgrade Pass (Existing Project)

Look for these upgrades:
- Emoji → SVG icons
- Linear → eased motion
- Flat → depth (shadows, gradients)
- Numbers → formatted/tabular
- Inconsistent text → tokenized typography

Use `references/quality-checklist.md` to validate.

## References

Load these only when needed:
- `references/workflow.md` for full step‑by‑step delivery
- `references/storyboard-template.md` for script/scene templates
- `references/scene-patterns.md` for reusable scene ideas
- `references/remotion-integration.md` for explicit Remotion constraints
- `references/quality-checklist.md` for final QA
