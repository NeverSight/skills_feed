---
name: gpui-styling
description: GPUI styling system including theme design, responsive layouts, visual design patterns, and style composition. Use when user needs help with styling, theming, or visual design in GPUI.
---

# GPUI Styling

## Metadata

This skill provides comprehensive guidance on GPUI's styling system, theme management, and visual design patterns for creating beautiful, consistent user interfaces.

## Instructions

### Styling API Fundamentals

#### Basic Styling

```rust
use gpui::*;

div()
    // Colors
    .bg(rgb(0x2563eb))           // Background
    .text_color(white())          // Text color
    .border_color(rgb(0xe5e7eb)) // Border color

    // Spacing
    .p_4()                        // Padding: 1rem
    .px_6()                       // Padding horizontal
    .py_2()                       // Padding vertical
    .m_4()                        // Margin
    .gap_3()                      // Gap between children

    // Sizing
    .w_64()                       // Width: 16rem
    .h_32()                       // Height: 8rem
    .w_full()                     // Width: 100%
    .h_full()                     // Height: 100%

    // Borders
    .border_1()                   // Border: 1px
    .rounded_lg()                 // Border radius: large
```

#### Color Types

```rust
// RGB from hex
let blue = rgb(0x2563eb);

// RGBA with alpha
let transparent_blue = rgba(0x2563eb, 0.5);

// HSLA (hue, saturation, lightness, alpha)
let hsla_color = hsla(0.6, 0.8, 0.5, 1.0);

// Named colors
let white = white();
let black = black();
```

#### Layout with Flexbox

```rust
div()
    .flex()                      // Enable flexbox
    .flex_row()                  // Horizontal layout
    .flex_col()                  // Vertical layout
    .items_center()              // Align items center
    .justify_between()           // Space between
    .gap_4()                     // Gap between items
    .child(/* ... */)
    .child(/* ... */)
```

### Theme System

#### Basic Theme Structure

```rust
use gpui::*;

#[derive(Clone)]
pub struct AppTheme {
    pub colors: ThemeColors,
    pub typography: Typography,
    pub spacing: Spacing,
    pub shadows: Shadows,
}

#[derive(Clone)]
pub struct ThemeColors {
    // Base colors
    pub background: Hsla,
    pub foreground: Hsla,

    // UI colors
    pub primary: Hsla,
    pub primary_foreground: Hsla,
    pub primary_hover: Hsla,

    pub secondary: Hsla,
    pub secondary_foreground: Hsla,
    pub secondary_hover: Hsla,

    pub accent: Hsla,
    pub accent_foreground: Hsla,

    pub destructive: Hsla,
    pub destructive_foreground: Hsla,

    // Neutral colors
    pub muted: Hsla,
    pub muted_foreground: Hsla,

    pub border: Hsla,
    pub input: Hsla,
    pub ring: Hsla,
}

#[derive(Clone)]
pub struct Typography {
    pub font_sans: Vec<String>,
    pub font_mono: Vec<String>,

    pub text_xs: Pixels,
    pub text_sm: Pixels,
    pub text_base: Pixels,
    pub text_lg: Pixels,
    pub text_xl: Pixels,
    pub text_2xl: Pixels,
}

#[derive(Clone)]
pub struct Spacing {
    pub xs: Pixels,
    pub sm: Pixels,
    pub md: Pixels,
    pub lg: Pixels,
    pub xl: Pixels,
}
```

#### Light Theme Implementation

```rust
impl AppTheme {
    pub fn light() -> Self {
        Self {
            colors: ThemeColors {
                background: rgb(0xffffff),
                foreground: rgb(0x0a0a0a),

                primary: rgb(0x2563eb),
                primary_foreground: rgb(0xffffff),
                primary_hover: rgb(0x1d4ed8),

                secondary: rgb(0xf1f5f9),
                secondary_foreground: rgb(0x0f172a),
                secondary_hover: rgb(0xe2e8f0),

                accent: rgb(0xf1f5f9),
                accent_foreground: rgb(0x0f172a),

                destructive: rgb(0xef4444),
                destructive_foreground: rgb(0xffffff),

                muted: rgb(0xf1f5f9),
                muted_foreground: rgb(0x64748b),

                border: rgb(0xe2e8f0),
                input: rgb(0xe2e8f0),
                ring: rgb(0x2563eb),
            },
            typography: Typography {
                font_sans: vec![
                    "Inter".to_string(),
                    "system-ui".to_string(),
                    "sans-serif".to_string(),
                ],
                font_mono: vec![
                    "JetBrains Mono".to_string(),
                    "monospace".to_string(),
                ],
                text_xs: px(12.0),
                text_sm: px(14.0),
                text_base: px(16.0),
                text_lg: px(18.0),
                text_xl: px(20.0),
                text_2xl: px(24.0),
            },
            spacing: Spacing {
                xs: px(4.0),
                sm: px(8.0),
                md: px(16.0),
                lg: px(24.0),
                xl: px(32.0),
            },
            shadows: Shadows {
                sm: Shadow::new(px(1.0), rgba(0x000000, 0.05)),
                md: Shadow::new(px(4.0), rgba(0x000000, 0.1)),
                lg: Shadow::new(px(8.0), rgba(0x000000, 0.15)),
            },
        }
    }
}
```

#### Dark Theme Implementation

```rust
impl AppTheme {
    pub fn dark() -> Self {
        Self {
            colors: ThemeColors {
                background: rgb(0x0a0a0a),
                foreground: rgb(0xfafafa),

                primary: rgb(0x3b82f6),
                primary_foreground: rgb(0xffffff),
                primary_hover: rgb(0x2563eb),

                secondary: rgb(0x1e293b),
                secondary_foreground: rgb(0xf1f5f9),
                secondary_hover: rgb(0x334155),

                accent: rgb(0x1e293b),
                accent_foreground: rgb(0xf1f5f9),

                destructive: rgb(0xef4444),
                destructive_foreground: rgb(0xffffff),

                muted: rgb(0x1e293b),
                muted_foreground: rgb(0x94a3b8),

                border: rgb(0x334155),
                input: rgb(0x334155),
                ring: rgb(0x3b82f6),
            },
            typography: Typography {
                font_sans: vec![
                    "Inter".to_string(),
                    "system-ui".to_string(),
                    "sans-serif".to_string(),
                ],
                font_mono: vec![
                    "JetBrains Mono".to_string(),
                    "monospace".to_string(),
                ],
                text_xs: px(12.0),
                text_sm: px(14.0),
                text_base: px(16.0),
                text_lg: px(18.0),
                text_xl: px(20.0),
                text_2xl: px(24.0),
            },
            spacing: Spacing {
                xs: px(4.0),
                sm: px(8.0),
                md: px(16.0),
                lg: px(24.0),
                xl: px(32.0),
            },
            shadows: Shadows {
                sm: Shadow::new(px(1.0), rgba(0x000000, 0.2)),
                md: Shadow::new(px(4.0), rgba(0x000000, 0.3)),
                lg: Shadow::new(px(8.0), rgba(0x000000, 0.4)),
            },
        }
    }
}
```

#### Using Themes in Components

```rust
impl Render for ThemedComponent {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let theme = cx.global::<AppTheme>();

        div()
            .bg(theme.colors.background)
            .text_color(theme.colors.foreground)
            .p(theme.spacing.md)
            .border_1()
            .border_color(theme.colors.border)
            .child("Themed content")
    }
}
```

#### Theme Switching

```rust
pub fn toggle_theme(cx: &mut AppContext) {
    let current = cx.global::<AppTheme>().clone();

    let new_theme = match current.mode {
        ThemeMode::Light => AppTheme::dark(),
        ThemeMode::Dark => AppTheme::light(),
    };

    cx.set_global(new_theme);
    cx.refresh();
}
```

### Responsive Design

#### Window Size Detection

```rust
impl Render for ResponsiveView {
    fn render(&mut self, cx: &mut ViewContext<Self>) -> impl IntoElement {
        let window_size = cx.window_bounds().get_bounds().size;
        let is_mobile = window_size.width < px(768.0);
        let is_tablet = window_size.width >= px(768.0) && window_size.width < px(1024.0);
        let is_desktop = window_size.width >= px(1024.0);

        div()
            .flex()
            .when(is_mobile, |this| {
                this.flex_col().gap_2()
            })
            .when(is_desktop, |this| {
                this.flex_row().gap_6()
            })
            .child(sidebar())
            .child(main_content())
    }
}
```

#### Breakpoint-Based Styling

```rust
pub struct Breakpoints;

impl Breakpoints {
    pub const SM: f32 = 640.0;
    pub const MD: f32 = 768.0;
    pub const LG: f32 = 1024.0;
    pub const XL: f32 = 1280.0;
    pub const XXL: f32 = 1536.0;
}

fn responsive_grid(width: Pixels) -> impl IntoElement {
    div()
        .grid()
        .when(width.0 < Breakpoints::SM, |this| this.grid_cols_1())
        .when(width.0 >= Breakpoints::SM && width.0 < Breakpoints::LG, |this| {
            this.grid_cols_2()
        })
        .when(width.0 >= Breakpoints::LG, |this| this.grid_cols_3())
        .gap_4()
}
```

### Visual Design Patterns

#### Card Component

```rust
pub fn card(
    title: impl Into<String>,
    description: impl Into<String>,
    content: impl IntoElement,
) -> impl IntoElement {
    let theme = cx.global::<AppTheme>();

    div()
        .bg(theme.colors.background)
        .border_1()
        .border_color(theme.colors.border)
        .rounded_lg()
        .shadow_sm()
        .overflow_hidden()
        .child(
            div()
                .p_6()
                .border_b_1()
                .border_color(theme.colors.border)
                .child(
                    div()
                        .text_lg()
                        .font_semibold()
                        .child(title.into())
                )
                .child(
                    div()
                        .text_sm()
                        .text_color(theme.colors.muted_foreground)
                        .child(description.into())
                )
        )
        .child(
            div()
                .p_6()
                .child(content)
        )
}
```

#### Button Variants

```rust
pub enum ButtonVariant {
    Primary,
    Secondary,
    Outline,
    Ghost,
    Destructive,
}

pub fn button(
    label: &str,
    variant: ButtonVariant,
) -> impl IntoElement {
    let theme = cx.global::<AppTheme>();

    let (bg, fg, hover_bg) = match variant {
        ButtonVariant::Primary => (
            theme.colors.primary,
            theme.colors.primary_foreground,
            theme.colors.primary_hover,
        ),
        ButtonVariant::Secondary => (
            theme.colors.secondary,
            theme.colors.secondary_foreground,
            theme.colors.secondary_hover,
        ),
        ButtonVariant::Outline => (
            hsla(0.0, 0.0, 0.0, 0.0),
            theme.colors.foreground,
            theme.colors.accent,
        ),
        ButtonVariant::Ghost => (
            hsla(0.0, 0.0, 0.0, 0.0),
            theme.colors.foreground,
            theme.colors.accent,
        ),
        ButtonVariant::Destructive => (
            theme.colors.destructive,
            theme.colors.destructive_foreground,
            theme.colors.destructive,
        ),
    };

    div()
        .px_4()
        .py_2()
        .bg(bg)
        .text_color(fg)
        .rounded_md()
        .font_medium()
        .cursor_pointer()
        .when(matches!(variant, ButtonVariant::Outline), |this| {
            this.border_1().border_color(theme.colors.border)
        })
        .hover(|this| this.bg(hover_bg))
        .transition_colors()
        .duration_150()
        .child(label)
}
```

#### Input Fields

```rust
pub fn text_input(
    value: &str,
    placeholder: &str,
) -> impl IntoElement {
    let theme = cx.global::<AppTheme>();

    div()
        .flex()
        .items_center()
        .w_full()
        .px_3()
        .py_2()
        .bg(theme.colors.background)
        .border_1()
        .border_color(theme.colors.input)
        .rounded_md()
        .text_color(theme.colors.foreground)
        .focus(|this| {
            this.border_color(theme.colors.ring)
                .ring_2()
                .ring_color(rgba(theme.colors.ring, 0.2))
        })
        .child(
            input()
                .w_full()
                .bg(hsla(0.0, 0.0, 0.0, 0.0))
                .placeholder(placeholder)
                .value(value)
        )
}
```

### Style Composition

#### Reusable Style Functions

```rust
pub fn focus_ring(theme: &AppTheme) -> StyleRefinement {
    StyleRefinement::default()
        .ring_2()
        .ring_color(rgba(theme.colors.ring, 0.2))
        .border_color(theme.colors.ring)
}

pub fn shadow_sm(theme: &AppTheme) -> StyleRefinement {
    StyleRefinement::default()
        .shadow(theme.shadows.sm)
}

// Usage
div()
    .apply(focus_ring(&theme))
    .apply(shadow_sm(&theme))
    .child("Styled element")
```

#### Conditional Styles

```rust
fn dynamic_button(
    label: &str,
    is_loading: bool,
    is_disabled: bool,
) -> impl IntoElement {
    let theme = cx.global::<AppTheme>();

    div()
        .px_4()
        .py_2()
        .bg(theme.colors.primary)
        .text_color(theme.colors.primary_foreground)
        .rounded_md()
        .when(is_disabled || is_loading, |this| {
            this.opacity(0.5).cursor_not_allowed()
        })
        .when(!is_disabled && !is_loading, |this| {
            this.cursor_pointer()
                .hover(|this| this.bg(theme.colors.primary_hover))
        })
        .child(
            if is_loading {
                "Loading..."
            } else {
                label
            }
        )
}
```

### Animation and Transitions

#### Hover Transitions

```rust
div()
    .transition_all()           // Transition all properties
    .duration_200()             // 200ms duration
    .bg(blue_500())
    .hover(|this| {
        this.bg(blue_600())
            .scale_105()        // Scale to 105%
    })
    .child("Hover me")
```

#### Transform Animations

```rust
div()
    .transition_transform()
    .duration_300()
    .ease_in_out()
    .hover(|this| {
        this.rotate(5.0)        // Rotate 5 degrees
            .translate_y(px(-2.0))  // Move up 2px
    })
    .child("Animated element")
```

## Resources

### Color Systems
- Use HSL for color manipulation
- Maintain consistent color contrast ratios
- Define semantic color names (primary, secondary, etc.)
- Support both light and dark themes

### Typography Scale
- Base: 16px (1rem)
- Scale: 1.125 (Major Second) or 1.2 (Minor Third)
- Sizes: xs, sm, base, lg, xl, 2xl, etc.
- Weights: normal, medium, semibold, bold

### Spacing Scale
- Base unit: 4px or 8px
- Multipliers: 0.5, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32
- Consistent throughout application
- Used for padding, margin, gap

### Best Practices
- Define theme at app level
- Use semantic color names
- Implement both light and dark themes
- Support responsive design
- Maintain consistent spacing
- Use transitions for smooth interactions
- Ensure accessibility (contrast, focus indicators)
- Document theme structure
