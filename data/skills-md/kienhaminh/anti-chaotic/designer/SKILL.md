---
name: designer
description: Use when building UI, branding, design systems, or auditing accessibility/UX.
---

# Frontend Design Standards

Expert-level design guidance for creating memorable, production-grade interfaces.

## Core Design Principles

### Intentionality Over Trends

Every design decision must be purposeful:

- **Why this color?** → Brand meaning, accessibility, contrast
- **Why this font?** → Readability, personality, performance
- **Why this animation?** → User feedback, spatial understanding

### Distinctive Over Generic

Avoid "AI slop" aesthetics:

- ❌ Default purple gradients, Inter everywhere, card-with-shadow templates
- ✅ Committed aesthetic vision, unique typography pairs, contextual layouts

### Technical Excellence

High-quality design = high-quality code:

- Semantic HTML first
- CSS custom properties for theming
- Performance-minded animations
- Accessibility as foundation

## Tools

| Tool             | Purpose                                       | Rule                                 |
| ---------------- | --------------------------------------------- | ------------------------------------ |
| `generate_image` | UI icons, avatars, backgrounds, illustrations | Follow `.agent/rules/nano-banana.md` |

## Asset Creation Capability

The designer skill includes a specialized workflow for creating high-quality, transparent assets (icons, avatars, game sprites) using the `generate_image` tool and a custom background removal script.

### Workflow

1.  **Prompt Engineering**:
    - Follow the formula in `.agent/rules/nano-banana.md`: `[Core Subject]` + `[Visual Style]` + `[Lighting/Color]` + `[Technical/Quality specs]`.
    - Ensure the visual style is compatible with extraction (e.g., "clean background", "minimalist").

2.  **Generation**:
    - Use `generate_image` to create the initial asset.
    - Save it with a descriptive name (e.g., `hero_robot_raw`).

3.  **Transparency Processing**:
    - Run the helper script to remove the background:
      ```bash
      python3 .agent/skills/designer/scripts/remove_background.py <input_path> <output_path>
      ```
    - **Parameters**:
      - `<input_path>`: Path to the image file you want to process.
      - `<output_path>`: File path where the result should be saved.

### Example

To create a "Blue Potion Icon":

1.  **Generate**: "Blue glass potion bottle, round shape, cork stopper, flat vector style, soft blue lighting, white background, detailed 4k" -> leads to `blue_potion_raw.png`
2.  **Process**: `python3 .agent/skills/designer/scripts/remove_background.py blue_potion_raw.png blue_potion_final.png`

## Integration

Works with `frontend-developer` skill for implementation handoff:

- **Designer Role**: Creates visual designs, tokens, and Motion Specs.
- **Frontend Role**: Writes the actual CSS/JS code based on these specs.

## References

Load references based on task context:

| Reference      | Path                           | Purpose                                           |
| -------------- | ------------------------------ | ------------------------------------------------- |
| Branding       | `references/branding.md`       | Creating logos, visual identity, brand guidelines |
| Color Theory   | `references/color-theory.md`   | Choosing palettes, dark mode, semantic colors     |
| Typography     | `references/typography.md`     | Font pairing, scales, text rendering              |
| Layout         | `references/layout.md`         | Grids, spacing, responsive design                 |
| Motion         | `references/motion.md`         | Micro-interactions, transitions, performance      |
| Accessibility  | `references/accessibility.md`  | WCAG compliance, keyboard nav, screen readers     |
| Design Systems | `references/design-systems.md` | Design tokens, component patterns, documentation  |
| Trends         | `references/trends.md`         | 2024-2025 trends, emerging CSS features           |
| Creation       | `references/creation.md`       | New components, pages, creative direction         |
| Review         | `references/review.md`         | Code review, compliance checks, quality audit     |

## Concepts

Distinct visual aesthetics to drive design direction:

| Concept             | Path                           | Description                                 |
| ------------------- | ------------------------------ | ------------------------------------------- |
| Apple Glassmorphism | `concepts/apple-glass.md`      | Premium, translucent depth (VisionOS Style) |
| Neo-Brutalism       | `concepts/neo-brutalism.md`    | Raw, high-contrast, bold borders            |
| Claymorphism        | `concepts/claymorphism.md`     | Soft 3D, inflated shapes, tactile feel      |
| Aurora Gradients    | `concepts/aurora-gradients.md` | Ethereal, moving blurred color meshes       |
| Bento Grids         | `concepts/bento-grids.md`      | Modular, grid-based content layout          |

## Templates

| Template    | Path                              | Purpose                                                                                                  |
| ----------- | --------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Motion Spec | `templates/design-motion-spec.md` | Motion Specification - animation timeline, triggers, easing. Use for handoff animation specs to frontend |
