---
name: rs-ratatui-crate
description: "Build terminal user interfaces (TUIs) in Rust with Ratatui (v0.30). Use this skill whenever working with the ratatui crate for creating interactive terminal applications, including: (1) Setting up a new Ratatui project, (2) Creating or modifying terminal UI layouts, (3) Implementing widgets (lists, tables, charts, text, gauges, etc.), (4) Handling keyboard/mouse input and events, (5) Structuring TUI application architecture (TEA, component-based, or monolithic patterns), (6) Writing custom widgets, (7) Managing application state in a TUI context, (8) Terminal setup/teardown and panic handling, (9) Testing TUI rendering with TestBackend. Also triggers for questions about crossterm event handling in a Ratatui context, tui-input, tui-textarea, or any ratatui-* ecosystem crate."
---

# Ratatui

Ratatui is an immediate-mode Rust library for building terminal UIs. It renders the entire UI each frame from application state — there is no persistent widget tree. The default backend is Crossterm.

- **Crate**: `ratatui = "0.30"`
- **Docs**: <https://docs.rs/ratatui/latest/ratatui/>
- **MSRV**: 1.86.0 (Rust 2024 edition)
- **Widget reference**: Read [references/widgets.md](references/widgets.md) for built-in widget details, styling, and custom widget implementation
- **Architecture patterns**: Read [references/architecture.md](references/architecture.md) for TEA, component, and monolithic patterns, event handling, layout, state management, and testing

## Quick Start

### Minimal app with `ratatui::run()` (v0.30+)

```rust
use ratatui::{widgets::{Block, Paragraph}, style::Stylize};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    ratatui::run(|terminal| {
        loop {
            terminal.draw(|frame| {
                let greeting = Paragraph::new("Hello, Ratatui!")
                    .centered()
                    .yellow()
                    .block(Block::bordered().title("Welcome"));
                frame.render_widget(greeting, frame.area());
            })?;
            if crossterm::event::read()?.is_key_press() {
                break Ok(());
            }
        }
    })
}
```

`ratatui::run()` calls `init()` before and `restore()` after the closure — handles terminal setup/teardown automatically.

### App with `init()`/`restore()` (manual control)

```rust
fn main() -> Result<()> {
    color_eyre::install()?;
    let mut terminal = ratatui::init();
    let result = run(&mut terminal);
    ratatui::restore();
    result
}

fn run(terminal: &mut ratatui::DefaultTerminal) -> Result<()> {
    loop {
        terminal.draw(|frame| { /* render widgets */ })?;
        if let Event::Key(key) = crossterm::event::read()? {
            if key.kind == KeyEventKind::Press && key.code == KeyCode::Char('q') {
                break;
            }
        }
    }
    Ok(())
}
```

### Cargo.toml

```toml
[dependencies]
ratatui = "0.30"
crossterm = "0.29"
color-eyre = "0.6"
```

## Core Concepts

### Rendering

Immediate-mode: call `terminal.draw(|frame| { ... })` each tick. Build widgets from state and render — no retained widget tree.

```rust
terminal.draw(|frame| {
    frame.render_widget(some_widget, frame.area());
    frame.render_stateful_widget(stateful_widget, area, &mut state);
})?;
```

### Layout

Use `Layout` to split areas with constraints. Prefer `areas()` for destructuring (v0.28+):

```rust
let [header, body, footer] = Layout::vertical([
    Constraint::Length(3),
    Constraint::Min(0),
    Constraint::Length(1),
]).areas(frame.area());
```

Centering with `Rect::centered()` (v0.30+):

```rust
let popup_area = frame.area()
    .centered(Constraint::Percentage(60), Constraint::Percentage(40));
```

Or with `Flex::Center`:

```rust
let [area] = Layout::horizontal([Constraint::Length(40)])
    .flex(Flex::Center)
    .areas(frame.area());
```

Constraint types: `Length(n)`, `Min(n)`, `Max(n)`, `Percentage(n)`, `Ratio(a, b)`, `Fill(weight)`.

### Widgets

All widgets implement `Widget` trait (`fn render(self, area: Rect, buf: &mut Buffer)`). Stateful widgets use `StatefulWidget` with an associated `State` type.

Built-in: `Block`, `Paragraph`, `List`, `Table`, `Tabs`, `Gauge`, `LineGauge`, `BarChart`, `Chart`, `Canvas`, `Sparkline`, `Scrollbar`, `Calendar`, `Clear`.

Text primitives: `Span`, `Line`, `Text` — all implement `Widget`.

See [references/widgets.md](references/widgets.md) for full API details.

### Event Handling

Use Crossterm for input. Always check `KeyEventKind::Press`:

```rust
use crossterm::event::{self, Event, KeyCode, KeyEventKind};

if let Event::Key(key) = event::read()? {
    if key.kind == KeyEventKind::Press {
        match key.code {
            KeyCode::Char('q') => should_quit = true,
            KeyCode::Up | KeyCode::Char('k') => scroll_up(),
            KeyCode::Down | KeyCode::Char('j') => scroll_down(),
            _ => {}
        }
    }
}
```

### Terminal Setup & Panic Handling

With `ratatui::run()` (simplest, v0.30+):

```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    ratatui::run(|terminal| { /* app loop */ })
}
```

With `color-eyre` panic hook (recommended for `init()`/`restore()`):

```rust
fn install_hooks() -> Result<()> {
    let (panic_hook, eyre_hook) = color_eyre::config::HookBuilder::default().into_hooks();
    let panic_hook = panic_hook.into_panic_hook();
    std::panic::set_hook(Box::new(move |info| {
        ratatui::restore();
        panic_hook(info);
    }));
    eyre_hook.install()?;
    Ok(())
}
```

## Architecture

Choose based on complexity. See [references/architecture.md](references/architecture.md) for full patterns with code.

| Complexity | Pattern                    | When                                      |
| ---------- | -------------------------- | ----------------------------------------- |
| Simple     | Monolithic                 | Single-screen, few key bindings, no async |
| Medium     | TEA (The Elm Architecture) | Multiple modes, form-like interaction     |
| Complex    | Component                  | Multi-panel, reusable panes, plugin-like  |

### TEA (The Elm Architecture) — Summary

```rust
struct Model { counter: i32, running: bool }

enum Message { Increment, Decrement, Quit }

fn update(model: &mut Model, msg: Message) {
    match msg {
        Message::Increment => model.counter += 1,
        Message::Decrement => model.counter -= 1,
        Message::Quit => model.running = false,
    }
}

fn view(model: &Model, frame: &mut Frame) {
    let text = format!("Counter: {}", model.counter);
    frame.render_widget(Paragraph::new(text), frame.area());
}
```

## Common Patterns

### List Navigation with Selection

```rust
let mut list_state = ListState::default().with_selected(Some(0));

// Update
match key.code {
    KeyCode::Up => list_state.select_previous(),
    KeyCode::Down => list_state.select_next(),
    _ => {}
}

// Render
let list = List::new(items)
    .block(Block::bordered().title("Items"))
    .highlight_style(Style::new().reversed())
    .highlight_symbol(Line::from(">> ").bold());
frame.render_stateful_widget(list, area, &mut list_state);
```

### Popup Overlay

```rust
fn render_popup(frame: &mut Frame, title: &str, content: &str) {
    let area = frame.area()
        .centered(Constraint::Percentage(60), Constraint::Percentage(40));
    frame.render_widget(Clear, area);
    let popup = Paragraph::new(content)
        .block(Block::bordered().title(title).border_type(BorderType::Rounded))
        .wrap(Wrap { trim: true });
    frame.render_widget(popup, area);
}
```

### Tabbed Interface

```rust
let titles = vec!["Tab1", "Tab2", "Tab3"];
let tabs = Tabs::new(titles)
    .block(Block::bordered())
    .select(selected_tab)
    .highlight_style(Style::new().bold().yellow());
frame.render_widget(tabs, tabs_area);
```

### Custom Widget

```rust
struct StatusBar { message: String }

impl Widget for StatusBar {
    fn render(self, area: Rect, buf: &mut Buffer) {
        Line::from(self.message)
            .style(Style::new().bg(Color::DarkGray).fg(Color::White))
            .render(area, buf);
    }
}

// Implement for reference to avoid consuming the widget:
impl Widget for &StatusBar {
    fn render(self, area: Rect, buf: &mut Buffer) {
        Line::from(self.message.as_str())
            .style(Style::new().bg(Color::DarkGray).fg(Color::White))
            .render(area, buf);
    }
}
```

### Text Input with tui-input

```toml
[dependencies]
tui-input = "0.11"
```

```rust
use tui_input::Input;
use tui_input::backend::crossterm::EventHandler;

let mut input = Input::default();

// In event handler:
input.handle_event(&crossterm::event::Event::Key(key));

// In render:
let width = area.width.saturating_sub(2) as usize;
let scroll = input.visual_scroll(width);
let input_widget = Paragraph::new(input.value())
    .scroll((0, scroll as u16))
    .block(Block::bordered().title("Search"));
frame.render_widget(input_widget, area);
frame.set_cursor_position(Position::new(
    area.x + (input.visual_cursor().max(scroll) - scroll) as u16 + 1,
    area.y + 1,
));
```

## Key Conventions

- Always restore terminal — even on panic. Use `ratatui::run()` or install a panic hook
- Check `KeyEventKind::Press` on all key events
- Use `Block::bordered()` as standard container
- Prefer `Layout::vertical/horizontal([...]).areas(rect)` over `.split(rect)`
- Use `Clear` widget before rendering popups/overlays
- Implement `Widget for &MyType` when the widget should not be consumed on render
- Use `ListState`, `TableState`, `ScrollbarState` for scroll/selection tracking
- Prefer `color-eyre` for error handling in TUI apps
- Use `Rect::centered()` (v0.30+) for centering layouts instead of double `Flex::Center`
