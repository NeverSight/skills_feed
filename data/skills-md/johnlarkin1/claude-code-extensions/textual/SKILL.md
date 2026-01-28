---
name: textual
description: Build terminal user interface (TUI) applications with the Textual framework. Use when creating new Textual apps, adding screens/widgets, styling with TCSS, handling events and reactivity, testing TUI apps, or any task involving "textual", "TUI", or terminal-based Python applications.
---

# Textual TUI Framework

Build terminal applications with Textual's web-inspired architecture: App → Screen → Widget.

## Quick Start

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class MyApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [("q", "quit", "Quit"), ("d", "toggle_dark", "Dark Mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Hello, World!")
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"

if __name__ == "__main__":
    MyApp().run()
```

## Core Concepts

### Widget Lifecycle
1. `__init__()` → `compose()` → `on_mount()` → `on_show()`/`on_hide()` → `on_unmount()`

### Reactivity
```python
from textual.reactive import reactive, var

class MyWidget(Widget):
    count = reactive(0)  # Triggers refresh on change
    internal = var("")   # No automatic refresh

    def watch_count(self, new_value: int) -> None:
        """Called when count changes."""
        self.styles.background = "green" if new_value > 0 else "red"

    def validate_count(self, value: int) -> int:
        """Constrain values."""
        return max(0, min(100, value))
```

### Events and Messages
```python
from textual import on
from textual.message import Message

class MyWidget(Widget):
    class Selected(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    def on_click(self) -> None:
        self.post_message(self.Selected("item"))

class MyApp(App):
    # Handler naming: on_<widget>_<message>
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.log(f"Button {event.button.id} pressed")

    @on(Button.Pressed, "#submit")  # CSS selector filtering
    def handle_submit(self) -> None:
        pass
```

### Data Flow
- **Attributes down**: Parent sets child properties directly
- **Messages up**: Child posts messages to parent via `post_message()`

## Screens

```python
from textual.screen import Screen

class WelcomeScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Static("Welcome!")
        yield Button("Continue", id="continue")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue":
            self.app.push_screen("main")

class MyApp(App):
    SCREENS = {"welcome": WelcomeScreen, "main": MainScreen}

    def on_mount(self) -> None:
        self.push_screen("welcome")
```

## Custom Widgets

### Simple Widget
```python
class Greeting(Widget):
    def render(self) -> RenderResult:
        return "Hello, [bold]World[/bold]!"
```

### Compound Widget
```python
class LabeledButton(Widget):
    DEFAULT_CSS = """
    LabeledButton { layout: horizontal; height: auto; }
    LabeledButton Label { width: 1fr; }
    """

    def __init__(self, label: str, button_text: str) -> None:
        self.label_text = label
        self.button_text = button_text
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.label_text)
        yield Button(self.button_text)
```

### Focusable Widget
```python
class Counter(Widget):
    can_focus = True
    BINDINGS = [("up", "increment", "+"), ("down", "decrement", "-")]
    count = reactive(0)

    def action_increment(self) -> None:
        self.count += 1
```

## Layout Patterns

### Containers
```python
from textual.containers import Horizontal, Vertical, Grid, VerticalScroll

def compose(self) -> ComposeResult:
    with Vertical():
        with Horizontal():
            yield Button("Left")
            yield Button("Right")
        with VerticalScroll():
            for i in range(100):
                yield Label(f"Item {i}")
```

### Grid CSS
```css
Grid {
    layout: grid;
    grid-size: 3 2;           /* columns rows */
    grid-columns: 1fr 2fr 1fr;
    grid-gutter: 1 2;
}
#wide { column-span: 2; }
```

### Docking
```css
#header { dock: top; height: 3; }
#sidebar { dock: left; width: 25; }
#footer { dock: bottom; height: 1; }
```

## Workers (Async)

```python
from textual import work

class MyApp(App):
    @work(exclusive=True)  # Cancels previous
    async def fetch_data(self, url: str) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            self.query_one("#result").update(response.text)

    @work(thread=True)  # For sync APIs
    def sync_operation(self) -> None:
        result = blocking_call()
        self.call_from_thread(self.update_ui, result)
```

## Testing

```python
async def test_app():
    app = MyApp()
    async with app.run_test() as pilot:
        await pilot.press("enter")
        await pilot.click("#button")
        await pilot.pause()  # Wait for messages
        assert app.query_one("#status").render() == "Done"
```

## Common Operations

```python
# Query widgets
self.query_one("#id")
self.query_one(Button)
self.query(".class")

# CSS classes
widget.add_class("active")
widget.toggle_class("visible")
widget.set_class(condition, "active")

# Visibility
widget.display = True/False

# Mount/remove
self.mount(NewWidget())
widget.remove()

# Timers
self.set_interval(1.0, callback)
self.set_timer(5.0, callback)

# Exit
self.exit(return_code=0)
```

## References

- **Widget catalog and messages**: See [references/widgets.md](references/widgets.md)
- **CSS properties and selectors**: See [references/css.md](references/css.md)
- **Complete examples**: See [references/examples.md](references/examples.md)
- **Official docs**: https://textual.textualize.io/
