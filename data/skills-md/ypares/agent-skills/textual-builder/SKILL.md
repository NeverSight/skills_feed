---
name: textual-builder
description: Build Text User Interface (TUI) applications using the Textual Python framework (v0.86.0+). Use when creating terminal-based applications, prototyping card games or interactive CLIs, or when the user mentions Textual, TUI, or terminal UI. Includes comprehensive reference documentation, card game starter template, and styling guides.
---

# Textual Builder

## Overview

This skill helps you build sophisticated Text User Interfaces (TUIs) using Textual, a Python framework for creating terminal and browser-based applications with a modern web-inspired API. It includes reference documentation, a card game template, and best practices for Textual development.

## Quick Start

### Basic Textual App

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Hello, Textual!")
        yield Footer()

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

### Card Game Template

For card game prototyping, copy the template:

```bash
cp -r assets/card-game-template/* ./my-game/
cd my-game
python app.py
```

The template includes:
- Interactive Card widget with face-up/down states
- Hand containers for player cards
- Play area with turn management
- Key bindings for card selection and playing
- Customizable styling

See `assets/card-game-template/README.md` for customization guide.

## When to Read Reference Documentation

This skill includes comprehensive reference files. Load them based on your task:

### references/basics.md
**Read when:** Setting up app structure, using reactive attributes, handling mounting, querying widgets, or working with messages/events.

**Covers:**
- App structure and compose method
- Reactive attributes and watchers
- Mounting and dynamic widget creation
- Widget querying
- Messages, events, and custom messages

### references/widgets.md
**Read when:** Adding UI elements like buttons, inputs, labels, data tables, or creating custom widgets.

**Covers:**
- Display widgets (Label, Static, Placeholder)
- Input widgets (Button, Input, TextArea, Switch)
- DataTable for tabular data
- Layout containers (Container, Grid, Horizontal, Vertical)
- Custom widget creation
- Header/Footer

### references/layout.md
**Read when:** Designing layouts, positioning widgets, using grid systems, or handling responsive sizing.

**Covers:**
- Layout types (vertical, horizontal, grid)
- Grid configuration (cell spanning, row/column sizing)
- Alignment and content positioning
- Docking widgets to screen edges
- Sizing (fixed, relative, fractional, auto)
- Spacing (margin, padding)
- Scrolling

### references/styling.md
**Read when:** Applying CSS styles, theming, adding borders, or customizing widget appearance.

**Covers:**
- CSS files and selectors
- Colors (named, hex, RGB, theme variables)
- Borders and border styling
- Text styling and alignment
- Opacity and tinting
- Rich markup for styled text
- Pseudo-classes (:hover, :focus, etc.)

### references/interactivity.md
**Read when:** Implementing keyboard shortcuts, handling mouse events, responding to user actions, or creating interactive behaviors.

**Covers:**
- Key bindings and actions
- Dynamic binding updates
- Mouse events (click, hover, enter, leave)
- Keyboard events
- Focus management
- Widget-specific messages
- Custom messages
- Notifications and timers

## Common Workflows

### Creating a New TUI App

1. Start with basic app structure (see Quick Start)
2. Design layout (read `references/layout.md`)
3. Add widgets (read `references/widgets.md`)
4. Style with CSS (read `references/styling.md`)
5. Add interactivity (read `references/interactivity.md`)

### Prototyping a Card Game

1. Copy the card game template
2. Customize the Card widget for your game's card properties
3. Modify game logic in action methods
4. Add game-specific rules in message handlers
5. Style cards and layout in `app.tcss`

### Adding Interactive Features

1. Define key bindings in `BINDINGS`
2. Implement action methods (`action_*`)
3. Handle widget messages (`on_button_pressed`, etc.)
4. Use reactive attributes for state management
5. Update UI in watchers

## Best Practices

- **Progressive Development**: Start simple, add complexity incrementally
- **Reactive State**: Use `reactive()` for state that affects UI
- **CSS Separation**: Keep styling in `.tcss` files, not inline
- **Widget Reuse**: Create custom widgets for repeated components
- **Message Bubbling**: Use `event.stop()` to control message propagation
- **Type Hints**: Use proper type hints for better IDE support
- **IDs and Classes**: Use semantic IDs/classes for querying and styling

## Installation

```bash
pip install textual
# or
uv pip install textual
```

Current version: v0.86.0+ (as of November 2025, latest is v6.6.0)

## Resources

### references/
Comprehensive documentation loaded on-demand:
- `basics.md` - Core concepts and app structure
- `widgets.md` - Widget catalog and usage
- `layout.md` - Layout systems and positioning
- `styling.md` - CSS and theming
- `interactivity.md` - Events, bindings, and actions

### assets/
- `card-game-template/` - Complete starter template for card games with interactive cards, hands, and turn management

## Official Documentation

For topics not covered in this skill, consult:
- https://textual.textualize.io/ (official docs)
- https://github.com/Textualize/textual (GitHub repo)
