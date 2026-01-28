---
name: makepad-router
description: "CRITICAL: Use for ALL Makepad/Robius questions including widgets, layout, events, and shaders.
Triggers on: makepad, robius, live_design, app_main, Widget, View, Button, Label, Image, TextInput,
ScrollView, RoundedView, SolidView, PortalList, Markdown, Html, TextFlow,
layout, Flow, Walk, padding, margin, width, height, Fit, Fill, align, spacing,
event, action, Hit, FingerDown, FingerUp, KeyDown, handle_event, click, tap,
animator, animation, state, transition, hover, pressed, ease,
shader, draw_bg, draw_text, Sdf2d, pixel, gradient, glow, shadow,
font, text_style, font_size, glyph, typography,
tokio, async, spawn, submit_async, SignalToUI, post_action,
apply_over, TextOrImage, modal, collapsible, drag drop,
AppState, persistence, theme, Scope,
deploy, package, APK, IPA, WASM, cargo makepad,
makepad widget, makepad 组件, makepad 按钮, makepad 布局, makepad 事件, makepad 动画, makepad 着色器,
创建组件, 自定义组件, 开发应用, 居中, 对齐, 点击事件, 悬停效果, 渐变, 阴影, 字体大小"
globs: ["**/live_design!*", "**/*.rs"]
---

# Makepad Question Router

> **Version:** 2.0.0 | **Last Updated:** 2026-01-21

## INSTRUCTIONS FOR CLAUDE

When this skill is triggered, you MUST load the appropriate sub-skill(s) based on the question:

### Routing Table

| Keywords | Load Skill |
|----------|------------|
| `live_design!`, `app_main!`, getting started, app structure | **makepad-basics** |
| DSL, inheritance, `<Widget>`, `Foo = { }` | **makepad-dsl** |
| layout, Flow, Walk, padding, width, height, center, align | **makepad-layout** |
| View, Button, Label, Image, TextInput, widget, Markdown, Html | **makepad-widgets** |
| event, action, Hit, FingerDown, handle_event, click | **makepad-event-action** |
| animator, state, transition, hover, pressed | **makepad-animation** |
| shader, draw_bg, Sdf2d, gradient, glow, shadow | **makepad-shaders** |
| font, text_style, font_size, glyph | **makepad-font** |
| platform, macOS, Android, iOS, WASM | **makepad-platform** |
| tokio, async, spawn, submit_async | **robius-app-architecture** |
| apply_over, modal, collapsible, pageflip | **robius-widget-patterns** |
| custom action, MatchEvent, post_action | **robius-event-action** |
| AppState, persistence, theme switch | **robius-state-management** |
| deploy, package, APK, IPA | **makepad-deployment** |
| troubleshoot, error, debug | **makepad-reference** |

### Context Bundle Loading

For complex tasks, load multiple skills:

| Context | Load These Skills |
|---------|-------------------|
| **Create widget/component** | makepad-widgets, makepad-dsl, makepad-layout, makepad-animation, makepad-shaders, makepad-event-action |
| **Build full app** | makepad-basics, makepad-dsl, makepad-layout, makepad-widgets, makepad-event-action, robius-app-architecture |
| **UI design** | makepad-dsl, makepad-layout, makepad-widgets, makepad-animation, makepad-shaders |
| **Production patterns** | robius-app-architecture, robius-widget-patterns, robius-state-management |

### Skill Dependencies

When loading a skill, also load its dependencies:

| Skill | Also Load |
|-------|-----------|
| makepad-widgets | makepad-layout, makepad-dsl |
| makepad-animation | makepad-shaders |
| makepad-shaders | makepad-widgets |
| robius-widget-patterns | makepad-widgets, makepad-layout |

### Example Workflow

```
User: "How do I create a custom button with hover animation?"

Analysis:
1. Keywords: custom, button, hover, animation
2. Context: Widget creation
3. Load: makepad-widgets, makepad-animation, makepad-shaders, makepad-event-action

Answer using patterns from all loaded skills.
```

## Default Project Settings

When creating Makepad projects:

```toml
[package]
edition = "2024"

[dependencies]
makepad-widgets = { git = "https://github.com/makepad/makepad", branch = "dev" }

[features]
default = []
nightly = ["makepad-widgets/nightly"]
```

## Key Patterns Quick Reference

### Widget Definition
```rust
#[derive(Live, LiveHook, Widget)]
pub struct MyWidget {
    #[deref] view: View,
    #[live] property: f64,
    #[rust] state: State,
    #[animator] animator: Animator,
}
```

### Async Pattern (Robius)
```rust
// UI -> Async
submit_async_request(MyRequest { ... });

// Async -> UI
Cx::post_action(MyAction { ... });
SignalToUI::set_ui_signal();
```
