---
name: UI Design
description: Designing premium user interfaces with egui
---

# Skill: UI Design

## When to use this skill

- Creating new UI views or components
- Modifying existing layouts
- Improving UX/UI aesthetics
- Ensuring consistency with the design system

## Design Philosophy

**"Premium Dark Mode"** is the core aesthetic. The UI should look professional, financial, and sleek.

- **Backgrounds**: Deep, rich dark blues/blacks (not just plain `#000000`).
- **Accents**: Neon blue (`#42A5F5`) for action, Green/Red for financial data.
- **Hierarchy**: Use visual weight, spacing, and font size to guide the eye.
- **Feedback**: Interactive elements must respond to hover/click.

## Color Palette (Reference)

| Role | Color | Hex | usage |
|------|-------|-----|-------|
| **Window Bg** | Dark Blue/Black | `#0A0C10` | Main application background |
| **Panel Bg** | Dark Blue/Black | `#0A0C10` | Sidebars, panels |
| **Card Bg** | Slightly lighter | `#12161D` | Surface for content containers |
| **Button Bg** | Lighter input | `#1C212A` | Standard interactive elements |
| **Hover** | Highlight | `#282E3A` | Hover state |
| **Primary** | Vibrant Blue | `#42A5F5` | Active states, primary actions |
| **Text** | High Contrast | `#F0F0F0` | Primary text |
| **Subtext** | Muted | `#B4B4B4` | Labels, secondary info |
| **Border** | Subtle | `#282C34` | Separators, outlines |

## Component Guidelines

### 1. Structure

All UI components should exist in `src/interfaces/` submodules.

```rust
pub fn render_my_component(ui: &mut egui::Ui, data: &MyData) {
    ui.group(|ui| {
        ui.heading("Title");
        // ... content
    });
}
```

### 2. Layouts

Use `egui` layout helpers effectively:

- `ui.horizontal(|ui| { ... })` for toolbars
- `ui.vertical(|ui| { ... })` for lists
- `egui::Grid` for aligned forms or data
- `ui.allocate_ui` for custom sizing

### 3. "Card" Pattern

To create distinct sections, use a coherent card style:

```rust
// Helper for consistent card styling (implement if not exists or use frame)
egui::Frame::none()
    .fill(egui::Color32::from_rgb(18, 22, 29))
    .rounding(4.0)
    .stroke(egui::Stroke::new(1.0, egui::Color32::from_rgb(40, 44, 52)))
    .inner_margin(12.0)
    .show(ui, |ui| {
        ui.heading("Card Title");
        ui.label("Card content...");
    });
```

## Best Practices (egui)

### ❌ Don't
- **Hardcode colors everywhere**: Use the `ctx.style().visuals` or defined constants where possible (though custom colors are allowed for the specific theming).
- **Block the UI thread**: No long computations in `update()`. Use channels to generic agents.
- **Over-nest layouts**: Too many nested `ui.horizontal`/`vertical` calls can kill performance and readability.

### ✅ Do
- **Use `ui.add_enabled(bool, widget)`** for conditional interactivity.
- **Use `ui.push_id`** loops to avoid ID clashes.
- **Separate logic from rendering**: The render function should typically take a reference to data, not the whole application state if possible.

## Checklist for UI Changes

- [ ] Does it respect the Dark Mode palette?
- [ ] Are texts readable (contrast)?
- [ ] Is the layout responsive (resizing window)?
- [ ] Do buttons/inputs have hover states?
- [ ] Are icons using the correct emoji font fallback?
- [ ] Is padding/margin consistent (standard: 8.0, 12.0, 24.0)?

## Updates

When updating the theme, modify `UserAgent::update` in `src/interfaces/ui.rs`.
