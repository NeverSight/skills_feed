---
name: opentui-projects
description: Expert assistance for OpenTUI project scaffolding, templates, examples, and learning paths. Use for quick start, project templates, component library, and best practices.
---

# OpenTUI Projects

Expert assistance for scaffolding OpenTUI projects and exploring examples.

## Quick Start (create-tui)

The fastest way to create an OpenTUI project:

```bash
# Using create-tui (recommended)
bun create tui my-app

# Or with npm
npm create tui my-app
```

### Template Selection

```bash
# Choose from available templates:
# - minimal: Minimal setup
# - basic-cli: Basic CLI tool
# - dashboard: Dashboard layout
# - form-app: Form-based application
# - editor: Text editor template
# - game: Simple game template

bun create tui my-app --template dashboard
```

## Manual Project Setup

### Core Project Structure

```
my-opentui-app/
├── package.json
├── tsconfig.json
├── src/
│   ├── main.tsx
│   ├── components/
│   └── utils/
└── README.md
```

### package.json

```json
{
  "name": "my-opentui-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "bun run src/main.tsx",
    "build": "tsc",
    "start": "bun run dist/main.js"
  },
  "dependencies": {
    "@opentui/core": "latest",
    "@opentui/react": "latest",
    "react": "^18.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.3.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "types": ["node"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

### Basic Entry Point

```tsx
// src/main.tsx
import { createCliRenderer } from "@opentui/core"
import { createRoot } from "@opentui/react"

function App() {
  return <text>Hello, OpenTUI!</text>
}

async function main() {
  const renderer = await createCliRenderer()
  createRoot(renderer).render(<App />)
}

main()
```

## Project Templates

### Minimal Template

**Use case:** Simple hello world, learning basics

```tsx
import { createCliRenderer } from "@opentui/core"
import { TextRenderable } from "@opentui/core"

async function main() {
  const renderer = await createCliRenderer()

  const text = new TextRenderable("Hello, World!")
  renderer.getRoot().add(text)

  renderer.start()
}

main()
```

### CLI Tool Template

**Use case:** Command-line tools with menus

```tsx
import { createCliRenderer } from "@opentui/core"
import { BoxRenderable, TextRenderable } from "@opentui/core"

async function main() {
  const renderer = await createCliRenderer()

  const container = new BoxRenderable()
  container.setStyle({
    borderStyle: "double",
    padding: 1,
  })

  const title = new TextRenderable("My CLI Tool")
  title.setStyle({ textDecoration: "bold" })

  container.add(title)
  renderer.getRoot().add(container)

  renderer.start()
}

main()
```

### Dashboard Template

**Use case:** Multi-panel dashboard applications

```tsx
import { createCliRenderer } from "@opentui/core"
import { GroupRenderable, BoxRenderable, TextRenderable } from "@opentui/core"

async function main() {
  const renderer = await createCliRenderer()
  const root = renderer.getRoot()

  const app = new GroupRenderable()
  app.setStyle({
    flexDirection: "row",
    width: 80,
    height: 30,
  })

  // Sidebar
  const sidebar = new BoxRenderable()
  sidebar.setStyle({
    width: 20,
    borderStyle: "single",
  })
  sidebar.add(new TextRenderable("Sidebar"))

  // Main content
  const main = new BoxRenderable()
  main.setStyle({
    flexGrow: 1,
    borderStyle: "single",
  })
  main.add(new TextRenderable("Main Content"))

  app.add(sidebar)
  app.add(main)
  root.add(app)

  renderer.start()
}

main()
```

### Form App Template

**Use case:** Data entry applications

```tsx
import { createCliRenderer } from "@opentui/core"
import {
  GroupRenderable,
  BoxRenderable,
  TextRenderable,
  InputRenderable,
} from "@opentui/core"

async function main() {
  const renderer = await createCliRenderer()
  const root = renderer.getRoot()

  const form = new GroupRenderable()
  form.setStyle({
    flexDirection: "column",
    gap: 1,
    width: 60,
  })

  const title = new TextRenderable("User Registration")
  title.setStyle({ textDecoration: "bold" })

  const nameInput = new InputRenderable()
  nameInput.setPlaceholder("Name")

  const emailInput = new InputRenderable()
  emailInput.setPlaceholder("Email")

  const submitButton = new BoxRenderable()
  submitButton.setStyle({ borderStyle: "single" })
  submitButton.add(new TextRenderable("Submit"))

  form.add(title)
  form.add(nameInput)
  form.add(emailInput)
  form.add(submitButton)
  root.add(form)

  renderer.start()
}

main()
```

## Component Library

### Button Component

```tsx
// components/Button.ts
import { BoxRenderable, TextRenderable } from "@opentui/core"

export interface ButtonOptions {
  label: string
  onClick?: () => void
  variant?: "primary" | "secondary" | "danger"
}

export class Button {
  private box: BoxRenderable

  constructor(options: ButtonOptions) {
    this.box = new BoxRenderable()
    this.setupStyles(options.variant)
    this.setupContent(options.label)
    this.setupEvents(options.onClick)
  }

  private setupStyles(variant: string = "primary") {
    const styles = {
      primary: {
        borderStyle: "single" as const,
        backgroundColor: new Color(100, 149, 237),
        foregroundColor: new Color(255, 255, 255),
      },
      secondary: {
        borderStyle: "single" as const,
        backgroundColor: new Color(50, 50, 50),
        foregroundColor: new Color(255, 255, 255),
      },
      danger: {
        borderStyle: "single" as const,
        backgroundColor: new Color(231, 76, 60),
        foregroundColor: new Color(255, 255, 255),
      },
    }

    const style = styles[variant as keyof typeof styles] || styles.primary
    this.box.setStyle(style)
  }

  private setupContent(label: string) {
    const text = new TextRenderable(label)
    this.box.add(text)
  }

  private setupEvents(onClick?: () => void) {
    if (onClick) {
      this.box.on("click", onClick)
    }
  }

  getRenderable() {
    return this.box
  }
}
```

### Modal Component

```tsx
// components/Modal.ts
import { BoxRenderable, TextRenderable, GroupRenderable } from "@opentui/core"

export class Modal {
  private overlay: BoxRenderable
  private content: BoxRenderable

  constructor() {
    this.overlay = new BoxRenderable()
    this.overlay.setStyle({
      position: "absolute",
      top: 0,
      left: 0,
      width: 80,
      height: 30,
      backgroundColor: new Color(0, 0, 0, 0.5),
    })

    this.content = new BoxRenderable()
    this.content.setStyle({
      borderStyle: "double",
      backgroundColor: new Color(30, 30, 30),
      padding: 2,
    })

    this.overlay.add(this.content)
  }

  setContent(component: any) {
    this.content.clear()
    this.content.add(component)
  }

  show() {
    this.overlay.setStyle({ display: "flex" })
  }

  hide() {
    this.overlay.setStyle({ display: "none" })
  }

  getRenderable() {
    return this.overlay
  }
}
```

## Learning Paths

### Beginner Path (1-2 weeks)

**Week 1: Basics**
1. Set up minimal project
2. Learn basic components (Text, Box)
3. Understand Yoga layout
4. Handle keyboard input
5. Style with colors

**Week 2: Interactive**
1. Use Input and Select components
2. Manage focus
3. Create simple forms
4. Handle events
5. Debug with console overlay

**Projects:**
- Hello World app
- Simple menu
- Basic form
- Counter app

### Intermediate Path (2-4 weeks)

**Week 3-4: Advanced**
1. ScrollBox for lists
2. Animations with Timeline
2. Component composition
3. State management
4. Testing basics

**Projects:**
- Todo list
- File explorer
- Simple game (tic-tac-toe)
- Dashboard with multiple panels

### Advanced Path (4-8 weeks)

**Week 5-8: Production**
1. Performance optimization
2. Advanced patterns
3. Error handling
4. Production deployment
5. Advanced testing

**Projects:**
- Text editor
- Terminal emulator
- Database viewer
- Complex dashboard

## Examples Explorer

### Available Examples

See `.search-data/research/opentui/resources.md` for a complete list of examples.

**Key Examples:**
1. **OpenCode** - AI coding agent (https://opencode.ai)
2. **cftop** - CloudFlare dashboard
3. **critique** - Git review tool
4. **opentui-examples** - Community examples

### Running Examples

```bash
# Clone OpenTUI repo
git clone https://github.com/sst/opentui.git
cd opentui

# Install dependencies
bun install

# Run core examples
cd packages/core
bun run src/examples/index.ts

# Run React examples
cd packages/react
bun run dev
```

## Best Practices

### Project Organization

```
src/
├── main.tsx              # Entry point
├── app/                  # App components
│   ├── App.tsx
│   └── layout/
├── components/           # Reusable components
│   ├── ui/
│   └── features/
├── hooks/               # Custom hooks (React/SolidJS)
├── stores/              # State management
├── utils/               # Helper functions
└── types/               # TypeScript types
```

### Component Design

1. **Single Responsibility:** Each component does one thing
2. **Composition:** Build complex UIs from simple components
3. **Props Interface:** Define clear props with TypeScript
4. **Styling Consistency:** Use themes and style utilities
5. **Error Handling:** Add error boundaries

### Performance

1. **Memoize expensive computations**
2. **Use efficient list rendering**
3. **Optimize re-renders**
4. **Profile performance**
5. **Test with realistic data**

## When to Use This Skill

Use `/opentui-projects` for:
- Creating new OpenTUI projects
- Choosing project templates
- Exploring examples
- Learning OpenTUI patterns
- Finding component libraries
- Best practices guidance

For core development help, use `/opentui`
For React-specific help, use `/opentui-react`
For SolidJS-specific help, use `/opentui-solid`

## Resources

- [Templates](references/TEMPLATES.md) - Complete template catalog
- [Examples](references/EXAMPLES.md) - Curated example collection
- [Learning Paths](references/LEARNING.md) - Structured learning guides
- [Best Practices](references/PRACTICES.md) - Production guidelines

## Key Knowledge Sources

- create-tui: https://github.com/msmps/create-tui
- Awesome OpenTUI: https://github.com/msmps/awesome-opentui
- OpenTUI Examples: https://github.com/sst/opentui/tree/main/packages/core/src/examples
- Research: `.search-data/research/opentui/`
