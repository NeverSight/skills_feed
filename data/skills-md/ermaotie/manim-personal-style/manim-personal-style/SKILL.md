---
name: manim-personal-style
description: "Plan and implement Manim Community (ManimCE) animations: use when users want 3Blue1Brown-style explainer videos, need scene-by-scene planning, or ask for ManimCE code/visualizations. Must gather requirements, produce a scenes.md plan before any Manim code, then implement with ManimCE best practices using the provided rules, examples, and templates."
---

# Manim Personal Style

Combine scene composition (narrative-first planning) with ManimCE implementation best practices.

## Workflow

### Phase 0: Understand the request
- Ask targeted questions to capture **audience**, **scope**, **length**, **style**, **assets**, **math depth**, **visual metaphors**, **narration**, **delivery format** (mp4/gif), **resolution/quality**, and **constraints** (timeline, render limits).
- If the topic is specialized or likely outdated, do quick research before planning.
- Confirm any required brand or color palette.

### Phase 1: Draft scenes.md (required before code)
- Always create `scenes.md` first (use `templates/scenes-template.md`).
- Break the video into clear scenes with purpose, visuals, narration notes, and technical notes.
- Include transitions, recurring motifs, and a color palette.
- If the user wants to skip planning, still provide a **minimal** scenes.md and ask for approval.
- After generating `scenes.md`, provide a concise overall summary plus per-scene highlights so the user can adjust.

### Phase 1.5: Draft scene_with_position.md (required before code)
- After `scenes.md`, create `scene_with_position.md` (use `templates/scene-with-position-template.md`).
- For every scene, enumerate **all objects**, their **sizes** and **positions** in frame coordinates.
- Perform a **layout validation**: confirm every object stays within the frame bounds and does not overlap others unless explicitly intended.
- If bounds or overlaps fail, adjust positions/sizes and document the changes.
- Ask for approval on the layout plan before coding.

### Phase 2: Review and lock the plan
- Ask the user to approve or edit the plan.
- Validate the plan against user requirements (length, style, audience, delivery format, constraints) and explicitly confirm fit or list mismatches for correction.
- Only proceed to code after explicit approval or clear confirmation to continue.

### Phase 3: Implement with ManimCE best practices
- Translate each scene into ManimCE code using `from manim import *`.
- Prefer one Python file per scene or grouped logically; keep scene names aligned to the plan.
- Use templates in `templates/` to start each scene.
- Follow the rules in `rules/` for animations, timing, text/LaTeX, camera, and styling.
- Reuse and transform mobjects for continuity; avoid abrupt replacements.
- If rendering produces multiple video segments, merge them into a single final video without asking.

## scenes.md Requirements
- Must be generated before any code.
- Must include: overview, narrative arc, scene list with durations, visual elements, narration notes, technical notes, transitions, palette, math content, and implementation order.
- Save at `scenes.md` in the working directory unless the user specifies another path.

## scene_with_position.md Requirements
- Must be generated after `scenes.md` and before any code.
- Must include for each scene: object list, sizes, positions, anchors, z-order (if relevant), and layout checks.
- Must include explicit **boundary checks** (frame width/height or safe margins) and **overlap checks**.
- If any conflicts exist, record the adjustments made to resolve them.
- Save at `scene_with_position.md` in the working directory unless the user specifies another path.

## References (use as needed)

### Composition (3b1b-style planning)
- `references/narrative-patterns.md` - Narrative arcs and hooks
- `references/visual-techniques.md` - Visualization techniques
- `references/scene-examples.md` - Example scenes.md fragments
- `templates/scenes-template.md` - scenes.md template
- `templates/scene-with-position-template.md` - scene_with_position.md template

### ManimCE Best Practices
- `rules/scenes.md`, `rules/animations.md`, `rules/mobjects.md` - core usage
- `rules/text.md`, `rules/latex.md`, `rules/text-animations.md` - typography/math
- `rules/positioning.md`, `rules/grouping.md` - layout
- `rules/axes.md`, `rules/graphing.md`, `rules/3d.md` - plotting and 3D
- `rules/camera.md`, `rules/timing.md`, `rules/updaters.md` - motion control
- `rules/styling.md`, `rules/colors.md`, `rules/shapes.md`, `rules/lines.md` - look & feel
- `rules/cli.md`, `rules/config.md` - rendering & config

### Examples & Templates
- `examples/` - working ManimCE examples
- `templates/basic_scene.py` - standard scene
- `templates/camera_scene.py` - MovingCameraScene
- `templates/threed_scene.py` - ThreeDScene

## Output Expectations
- Start with `scenes.md` and request approval.
- After `scenes.md`, create `scene_with_position.md` and request approval.
- After approval, provide ManimCE implementation with clear scene mapping.
- After `scenes.md`, include a short summary + scene-by-scene detail, and invite adjustments.
- Validate the total video plan and each scene against user requirements (e.g., duration, style, assets) before coding.
- If output is split across multiple video files, merge into one final video for delivery.
- Keep code modular and readable; prefer constants for colors and timing.
