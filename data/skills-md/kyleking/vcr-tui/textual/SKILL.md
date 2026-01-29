---
name: textual
description: Expert guidance for building TUI (Text User Interface) applications with the Textual framework. Invoke when user asks about Textual development, TUI apps, widgets, screens, CSS styling, reactive programming, or testing Textual applications.
---

# Textual - Python TUI Framework Expert

You are an expert in building Text User Interface (TUI) applications using **Textual**, a modern Python framework for creating sophisticated terminal applications. This skill provides comprehensive guidance on Textual's architecture, best practices, and common patterns.

## What is Textual?

Textual is a TUI framework by Textualize.io that enables developers to build:

- Beautiful, responsive terminal applications
- Rich, interactive command-line tools
- Cross-platform TUIs with modern UX patterns
- Applications with CSS-like styling and reactive programming

## When to Use This Skill

Invoke this skill when the user:

- Wants to build or modify a TUI application
- Asks about Textual framework features
- Needs help with widgets, screens, or layouts
- Has questions about CSS styling in Textual
- Wants to implement reactive programming patterns
- Needs testing guidance for Textual apps
- Encounters errors or issues with Textual code
- Asks about TUI design patterns or best practices

## Core Concepts

### Application Architecture

Textual applications follow an **event-driven architecture**:

- The `App` class is the entry point and foundation
- **Screens** contain widgets and occupy the full terminal
- **Widgets** are reusable UI components managing rectangular regions
- **Messages** enable communication between components
- **CSS (TCSS)** provides styling separate from logic

### Key Components

**App Class:**
- Entry point via `app.run()`
- Manages screens, modes, and global state
- Handles key bindings and actions
- Configures CSS via `CSS_PATH` or inline `CSS`

**Screens:**
- Full-terminal containers for widgets
- Support push/pop navigation stack
- Can be modal for dialogs
- Define their own key bindings and CSS

**Widgets:**
- Rectangular UI components
- Support composition via `compose()`
- Handle events via `on_*` methods
- Can be focused and styled with CSS

### Reactive Programming

Textual's reactive system automatically updates the UI when data changes:

```python
from textual.reactive import reactive

class Counter(Widget):
    count = reactive(0)  # Auto-refreshes on change

    def render(self) -> str:
        return f"Count: {self.count}"
```

Features:
- **Validation**: `validate_<attr>()` methods constrain values
- **Watchers**: `watch_<attr>()` methods react to changes
- **Computed properties**: `compute_<attr>()` for derived values
- **Recompose**: Rebuild widget tree when data changes

### CSS Styling (TCSS)

Textual uses CSS-like syntax for styling:

```css
Button {
    background: $primary;
    margin: 1;
}

#submit-button {
    background: $success;
}

.danger {
    background: $error;
}
```

Benefits:
- Separation of concerns (style vs logic)
- Live reload during development
- Theme system with semantic colors
- Responsive layout with FR units

## Common Patterns

### Basic App Template

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class MyApp(App):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Hello, Textual!")
        yield Footer()

    def on_mount(self) -> None:
        """Called after app starts."""
        pass

if __name__ == "__main__":
    MyApp().run()
```

### Widget Communication

Follow **"Attributes down, messages up"**:

```python
# Parent sets child attributes (down)
child.value = 10

# Child posts messages to parent (up)
class ChildWidget(Widget):
    class Updated(Message):
        def __init__(self, value: int) -> None:
            super().__init__()
            self.value = value

    def update_value(self) -> None:
        self.post_message(self.Updated(self.value))

# Parent handles child messages
class ParentWidget(Widget):
    def on_child_widget_updated(self, message: ChildWidget.Updated) -> None:
        self.log(f"Child updated: {message.value}")
```

### Testing Pattern

```python
import pytest
from my_app import MyApp

@pytest.mark.asyncio
async def test_button_click():
    app = MyApp()
    async with app.run_test() as pilot:
        # Simulate user interaction
        await pilot.click("#submit-button")

        # CRITICAL: Wait for message processing
        await pilot.pause()

        # Assert state changed
        result = app.query_one("#status")
        assert "Success" in str(result.renderable)
```

## Best Practices

### Design Process

1. **Sketch First**: Draw UI layout on paper before coding
2. **Work Outside-In**: Implement fixed elements (header/footer) first, then flexible content
3. **Use Docking**: Fix elements with `dock: top/bottom/left/right`
4. **FR Units**: Use `1fr` for flexible sizing that fills available space
5. **Container Widgets**: Leverage `Vertical`, `Horizontal`, `Grid` for layouts

### Code Organization

**Prefer composition over inheritance:**

```python
# Good: Compose from smaller widgets
class UserCard(Widget):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Avatar()
            yield UserName()
            yield UserEmail()
```

**Separate concerns:**

```python
# UI in widgets/
class UserPanel(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.service = UserService()  # Business logic

# Business logic in business_logic/
class UserService:
    async def fetch_user(self, user_id: int) -> User:
        # API calls, data processing
        pass
```

**External CSS for apps:**

```python
class MyApp(App):
    CSS_PATH = "app.tcss"  # Enables live reload
```

### Performance

1. **Target 60fps** for smooth terminal rendering
2. **Use `Static` widget** for cached rendering
3. **Cache expensive operations** with `@lru_cache`
4. **Use immutable objects** for data structures
5. **Workers for async operations** to avoid blocking UI

### Accessibility

- Full keyboard navigation support
- Set `can_focus = True` on interactive widgets
- Provide meaningful key bindings
- Use semantic color variables (`$primary`, `$error`)
- Test with different terminal sizes

## Common Errors & Solutions

### 1. Forgetting async/await

```python
# WRONG
def on_button_pressed(self):
    self.mount(Widget())

# RIGHT
async def on_button_pressed(self):
    await self.mount(Widget())
```

### 2. Missing pilot.pause() in tests

```python
# WRONG - race condition
async def test_feature():
    await pilot.click("#button")
    assert app.query_one("#status").text == "Done"

# RIGHT
async def test_feature():
    await pilot.click("#button")
    await pilot.pause()  # Wait for processing
    assert app.query_one("#status").text == "Done"
```

### 3. Modifying reactives in __init__

```python
# WRONG - triggers watchers too early
def __init__(self):
    super().__init__()
    self.count = 10

# RIGHT - use set_reactive or on_mount
def __init__(self):
    super().__init__()
    self.set_reactive(MyWidget.count, 10)
```

### 4. Blocking the event loop

```python
# WRONG
def on_button_pressed(self):
    response = requests.get("https://api.example.com")  # Blocks UI!

# RIGHT - use workers
from textual.worker import work

@work(exclusive=True)
async def on_button_pressed(self):
    response = await httpx.get("https://api.example.com")
```

## Development Tools

### Development Console

Terminal 1:
```bash
textual console
```

Terminal 2:
```bash
textual run --dev my_app.py
```

In code:
```python
from textual import log
log("Debug message", locals())
```

### Screenshots & Live Editing

```bash
# Screenshot after 5 seconds
textual run --screenshot 5 my_app.py

# Dev mode with live CSS reload
textual run --dev my_app.py
```

## Project Structure

**Medium/Large Apps:**

```
project/
├── src/
│   ├── app.py              # Main App class
│   ├── screens/
│   │   ├── main_screen.py
│   │   └── settings_screen.py
│   ├── widgets/
│   │   ├── status_bar.py
│   │   └── data_grid.py
│   └── business_logic/
│       ├── models.py
│       └── services.py
├── static/
│   └── app.tcss           # External CSS
├── tests/
│   ├── test_app.py
│   └── test_widgets/
└── pyproject.toml
```

## Instructions for Assistance

When helping users with Textual:

1. **Assess Context**: Understand their app structure and goals
2. **Check Basics**: Verify imports, async/await, and lifecycle methods
3. **Provide Examples**: Show concrete, runnable code
4. **Explain Patterns**: Describe why a pattern is recommended
5. **Test Guidance**: Include testing code when implementing features
6. **Debug Support**: Use console logging and visual debugging tips
7. **Best Practices**: Suggest improvements for maintainability

Always consider:
- App complexity (simple vs multi-screen)
- State management needs (local vs global)
- Performance requirements
- Testing strategy
- Code organization and maintainability

## Additional Resources

For detailed reference information:

- **[quick-reference.md](quick-reference.md)**: Concise templates, patterns, and cheat sheets
- **[guide.md](guide.md)**: Comprehensive architecture, design principles, and best practices
- **Official Documentation**: https://textual.textualize.io

## Quick Reference Highlights

### Useful Built-in Widgets

**Input & Selection:**
- `Button`, `Checkbox`, `Input`, `RadioButton`, `Select`, `Switch`, `TextArea`

**Display:**
- `Label`, `Static`, `Pretty`, `Markdown`, `MarkdownViewer`

**Data:**
- `DataTable`, `ListView`, `Tree`, `DirectoryTree`

**Containers:**
- `Header`, `Footer`, `Tabs`, `TabbedContent`, `Vertical`, `Horizontal`, `Grid`

### Key Lifecycle Methods

```python
def __init__(self) -> None:
    """Widget created - don't modify reactives here."""
    super().__init__()

def compose(self) -> ComposeResult:
    """Build child widgets."""
    yield ChildWidget()

def on_mount(self) -> None:
    """After mounted - safe to modify reactives."""
    self.set_interval(1, self.update)

def on_unmount(self) -> None:
    """Before removal - cleanup resources."""
    pass
```

### Common CSS Patterns

```css
/* Docking */
#header { dock: top; height: 3; }
#sidebar { dock: left; width: 30; }

/* Flexible sizing */
#content { width: 1fr; height: 1fr; }

/* Grid layout */
#container {
    layout: grid;
    grid-size: 3 2;
    grid-columns: 1fr 2fr 1fr;
}

/* Theme colors */
Button {
    background: $primary;
    color: $text;
}

Button:hover {
    background: $primary-lighten-1;
}
```

## Summary

This skill provides expert-level guidance for building Textual applications. Use it to help users understand architecture, implement features, debug issues, write tests, and follow best practices for maintainable TUI development.
