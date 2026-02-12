---
name: opentui
description: Expert assistance for OpenTUI core development using the imperative API with vanilla TypeScript. Use for component creation, layout management, input handling, styling, animations, and debugging.
---

# OpenTUI Core Development

Expert assistance for building terminal user interfaces with OpenTUI's imperative API.

## Quick Start

```bash
# Install dependencies
bun install @opentui/core

# Zig is required for native modules
# Install from: https://ziglang.org/download/
```

## Core Components

| Component | Purpose | Import |
|-----------|---------|--------|
| `TextRenderable` | Text display with styling | `import { TextRenderable } from "@opentui/core"` |
| `BoxRenderable` | Container with borders/backgrounds | `import { BoxRenderable } from "@opentui/core"` |
| `GroupRenderable` | Layout containers | `import { GroupRenderable } from "@opentui/core"` |
| `InputRenderable` | Single-line text input | `import { InputRenderable } from "@opentui/core"` |
| `SelectRenderable` | Dropdown selection | `import { SelectRenderable } from "@opentui/core"` |
| `ScrollBoxRenderable` | Scrollable content areas | `import { ScrollBoxRenderable } from "@opentui/core"` |
| `CodeRenderable` | Syntax-highlighted code | `import { CodeRenderable } from "@opentui/core"` |

## Basic Pattern

```typescript
import { createCliRenderer } from "@opentui/core"
import { BoxRenderable, TextRenderable } from "@opentui/core"

async function main() {
  const renderer = await createCliRenderer()

  const box = new BoxRenderable()
  const text = new TextRenderable("Hello, OpenTUI!")
  box.add(text)

  renderer.getRoot().add(box)
  renderer.start()

  // Handle Ctrl+C to exit
  renderer.on("key", (key) => {
    if (key.name === "c" && key.ctrl) {
      renderer.destroy()
      process.exit(0)
    }
  })
}

main()
```

## Layout with Yoga (CSS Flexbox)

```typescript
import { Yoga } from "@opentui/core"

const group = new GroupRenderable()
group.setStyle({
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
  width: 80,
  height: 24,
})
```

See [LAYOUT.md](references/LAYOUT.md) for all Yoga properties.

## Input Handling

### Keyboard Events
```typescript
renderer.on("key", (key: KeyEvent) => {
  if (key.name === "escape") process.exit(0)
  if (key.name === "c" && key.ctrl) process.exit(0)
})
```

### Component Input Events
```typescript
const input = new InputRenderable()
input.on("submit", (value: string) => {
  console.log("Submitted:", value)
})
input.on("change", (value: string) => {
  console.log("Changed:", value)
})
```

See [INPUT.md](references/INPUT.md) for complete event handling patterns.

## Styling & Colors

```typescript
import { Color, parseColor } from "@opentui/core"

// Create colors
const red = new Color(255, 0, 0)        // RGB integers
const blue = Color.fromInts(0, 0, 255) // Static method
const green = parseColor("#00FF00")     // Parse hex

// Apply styles
box.setStyle({
  backgroundColor: red,
  foregroundColor: blue,
  borderStyle: "double",
  paddingLeft: 2,
  paddingRight: 2,
})
```

See [STYLING.md](references/STYLING.md) for color system and style properties.

## Animations

```typescript
import { Timeline } from "@opentui/core"

const box = new BoxRenderable()
const timeline = new Timeline({
  duration: 1000,
  easing: (t) => t * (2 - t), // easeOutQuad
})

timeline.to(box, {
  backgroundColor: new Color(255, 0, 0),
}, {
  onUpdate: () => renderer.render()
})

timeline.play()
```

See [ANIMATION.md](references/ANIMATION.md) for animation patterns.

## Debugging

```typescript
// Enable console overlay
import { consoleOverlay } from "@opentui/core"
renderer.attach(consoleOverlay())

// Now console.log() appears in terminal overlay
console.log("Debug: initialized")
```

## When to Use This Skill

Use `/opentui` for:
- Building TUIs with vanilla TypeScript/JavaScript
- Creating custom OpenTUI components
- Understanding core OpenTUI architecture
- Performance optimization
- Low-level debugging

For React-specific development, use `/opentui-react`
For SolidJS-specific development, use `/opentui-solid`
For project scaffolding and examples, use `/opentui-projects`

## Common Tasks

- **Create a form**: Use BoxRenderable + InputRenderable components with Yoga layout
- **Handle keyboard shortcuts**: Listen to renderer "key" events
- **Make scrollable lists**: Use ScrollBoxRenderable with dynamic content
- **Display code**: Use CodeRenderable for syntax highlighting
- **Add borders**: Use BoxRenderable with borderStyle property

## Resources

- [Component API](references/COMPONENTS.md) - Complete component reference
- [Layout Guide](references/LAYOUT.md) - Yoga flexbox properties
- [Event Handling](references/INPUT.md) - Keyboard, mouse, clipboard
- [Styling](references/STYLING.md) - Colors, borders, spacing
- [Animations](references/ANIMATION.md) - Timeline and easing
- [Testing](references/TESTING.md) - Testing utilities

## Key Knowledge Sources

- OpenTUI GitHub: https://github.com/sst/opentui
- Context7: `/sst/opentui` (168 code snippets, High reputation)
- Research: `.search-data/research/opentui/`
