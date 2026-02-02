---
name: figma-plugin
description: Create Figma plugins with the Plugin API. Covers plugin architecture (sandbox + UI), node manipulation, styles, components, UI development with postMessage communication, and publishing. Use this skill when building Figma plugins, working with the Figma Plugin API, or creating design automation tools.
---

# Figma Plugin Development

Build plugins that extend Figma's functionality.

## Plugin Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FIGMA APPLICATION                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐      ┌─────────────────────────┐  │
│  │    MAIN THREAD      │      │      UI THREAD          │  │
│  │    (Sandbox)        │      │      (iframe)           │  │
│  │                     │      │                         │  │
│  │  • Plugin API       │ ←──→ │  • HTML/CSS/JS          │  │
│  │  • Node access      │ post │  • User interface       │  │
│  │  • figma.*          │ Msg  │  • No Figma API access  │  │
│  │  • Read/write doc   │      │  • Can use npm packages │  │
│  │                     │      │                         │  │
│  └─────────────────────┘      └─────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Constraints:**
- Main thread (sandbox): Access to Figma API, but limited JS environment
- UI thread (iframe): Full browser environment, but no Figma API access
- Communication via `postMessage` / `onmessage`

## Plugin Types

| Type | Use Case | Has UI |
|------|----------|--------|
| Design Plugin | Manipulate design files | Optional |
| FigJam Plugin | Manipulate FigJam files | Optional |
| Widget | Interactive objects in canvas | Always (React-like) |

## Quick Start

### Minimal Plugin (No UI)

```typescript
// code.ts
// Runs in main thread with Figma API access

// Get current selection
const selection = figma.currentPage.selection;

if (selection.length === 0) {
  figma.notify('Please select something');
  figma.closePlugin();
}

// Do something with selection
for (const node of selection) {
  if ('fills' in node) {
    node.fills = [{ type: 'SOLID', color: { r: 1, g: 0, b: 0 } }];
  }
}

figma.notify(`Updated ${selection.length} items`);
figma.closePlugin();
```

### Plugin with UI

```typescript
// code.ts (main thread)
figma.showUI(__html__, { width: 300, height: 200 });

// Receive messages from UI
figma.ui.onmessage = (msg) => {
  if (msg.type === 'create-rectangle') {
    const rect = figma.createRectangle();
    rect.resize(msg.width, msg.height);
    rect.fills = [{ type: 'SOLID', color: { r: 0.5, g: 0.5, b: 1 } }];
    figma.currentPage.appendChild(rect);
    figma.viewport.scrollAndZoomIntoView([rect]);
  }

  if (msg.type === 'cancel') {
    figma.closePlugin();
  }
};
```

```html
<!-- ui.html (UI thread) -->
<div id="app">
  <label>Width: <input id="width" type="number" value="100"></label>
  <label>Height: <input id="height" type="number" value="100"></label>
  <button id="create">Create Rectangle</button>
  <button id="cancel">Cancel</button>
</div>

<script>
  document.getElementById('create').onclick = () => {
    parent.postMessage({
      pluginMessage: {
        type: 'create-rectangle',
        width: Number(document.getElementById('width').value),
        height: Number(document.getElementById('height').value),
      }
    }, '*');
  };

  document.getElementById('cancel').onclick = () => {
    parent.postMessage({ pluginMessage: { type: 'cancel' } }, '*');
  };
</script>
```

## Core Concepts

### Node Types

| Category | Types |
|----------|-------|
| **Containers** | PageNode, FrameNode, GroupNode, SectionNode |
| **Shapes** | RectangleNode, EllipseNode, PolygonNode, StarNode, LineNode, VectorNode |
| **Text** | TextNode |
| **Components** | ComponentNode, ComponentSetNode, InstanceNode |
| **Media** | ImageNode (via fills) |
| **Special** | BooleanOperationNode, SliceNode, ConnectorNode |

### Properties by Mixin

```typescript
// Figma uses mixins for shared properties

// BlendMixin - opacity, blendMode, effects
node.opacity = 0.5;
node.effects = [{ type: 'DROP_SHADOW', ... }];

// GeometryMixin - fills, strokes
node.fills = [{ type: 'SOLID', color: { r: 1, g: 0, b: 0 } }];
node.strokes = [{ type: 'SOLID', color: { r: 0, g: 0, b: 0 } }];
node.strokeWeight = 2;

// LayoutMixin - position, size, constraints
node.x = 100;
node.y = 100;
node.resize(200, 100);
node.constraints = { horizontal: 'SCALE', vertical: 'CENTER' };

// ChildrenMixin - parent/child relationships
node.children; // readonly
node.appendChild(child);
node.insertChild(0, child);
```

### Type Guards

```typescript
// Check node type before accessing properties
function isTextNode(node: SceneNode): node is TextNode {
  return node.type === 'TEXT';
}

function hasChildren(node: SceneNode): node is FrameNode | GroupNode {
  return 'children' in node;
}

function hasFills(node: SceneNode): node is GeometryMixin & SceneNode {
  return 'fills' in node;
}

// Usage
for (const node of figma.currentPage.selection) {
  if (isTextNode(node)) {
    node.characters = 'Updated text';
  }
  if (hasFills(node)) {
    node.fills = [...];
  }
}
```

## Communication Pattern

### Main → UI

```typescript
// code.ts
figma.ui.postMessage({ type: 'selection-changed', count: selection.length });
```

```typescript
// ui.ts
window.onmessage = (event) => {
  const msg = event.data.pluginMessage;
  if (msg.type === 'selection-changed') {
    document.getElementById('count').textContent = msg.count;
  }
};
```

### UI → Main

```typescript
// ui.ts
parent.postMessage({ pluginMessage: { type: 'do-something', data: 'value' } }, '*');
```

```typescript
// code.ts
figma.ui.onmessage = (msg) => {
  if (msg.type === 'do-something') {
    console.log(msg.data);
  }
};
```

### Typed Messages

```typescript
// shared-types.ts
type PluginMessage =
  | { type: 'create-shape'; shape: 'rectangle' | 'ellipse'; size: number }
  | { type: 'update-selection'; color: RGB }
  | { type: 'cancel' };

type UIMessage =
  | { type: 'selection-changed'; count: number; types: string[] }
  | { type: 'error'; message: string };

// code.ts
figma.ui.onmessage = (msg: PluginMessage) => {
  switch (msg.type) {
    case 'create-shape':
      // TypeScript knows msg has shape and size
      break;
    case 'update-selection':
      // TypeScript knows msg has color
      break;
  }
};
```

## Common Operations

### Create Nodes

```typescript
// Shapes
const rect = figma.createRectangle();
const ellipse = figma.createEllipse();
const frame = figma.createFrame();

// Text (must load font first)
const text = figma.createText();
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
text.characters = 'Hello World';

// Component
const component = figma.createComponent();
component.name = 'Button';

// Instance
const instance = component.createInstance();
```

### Modify Selection

```typescript
// Get selection
const selection = figma.currentPage.selection;

// Set selection
figma.currentPage.selection = [node1, node2];

// Listen for changes
figma.on('selectionchange', () => {
  const newSelection = figma.currentPage.selection;
  figma.ui.postMessage({ type: 'selection', nodes: newSelection.map(n => n.name) });
});
```

### Colors

```typescript
// RGB (0-1 range, not 0-255)
const red: RGB = { r: 1, g: 0, b: 0 };
const blue: RGB = { r: 0, g: 0, b: 1 };

// With alpha
const semiTransparent: RGBA = { r: 1, g: 0, b: 0, a: 0.5 };

// Hex to RGB helper
function hexToRgb(hex: string): RGB {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16) / 255,
    g: parseInt(result[2], 16) / 255,
    b: parseInt(result[3], 16) / 255,
  } : { r: 0, g: 0, b: 0 };
}

// Apply solid fill
node.fills = [{ type: 'SOLID', color: hexToRgb('#FF5733') }];
```

### Storage

```typescript
// Per-document storage
await figma.clientStorage.setAsync('key', { data: 'value' });
const data = await figma.clientStorage.getAsync('key');

// Per-node storage (survives copy/paste)
node.setPluginData('key', JSON.stringify({ saved: true }));
const nodeData = JSON.parse(node.getPluginData('key') || '{}');

// Shared across plugins (use namespace)
node.setSharedPluginData('com.myplugin', 'key', 'value');
```

## Anti-Patterns

### ❌ Forgetting Async Font Loading

```typescript
// WRONG: Will fail
const text = figma.createText();
text.characters = 'Hello'; // Error: font not loaded

// RIGHT
const text = figma.createText();
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
text.characters = 'Hello';
```

### ❌ Modifying Readonly Arrays

```typescript
// WRONG: fills is readonly
node.fills.push(newFill); // Error

// RIGHT: Create new array
node.fills = [...node.fills, newFill];
```

### ❌ Not Handling Selection Empty

```typescript
// WRONG: Crashes if nothing selected
const node = figma.currentPage.selection[0];
node.name = 'Renamed'; // Error if selection empty

// RIGHT
const selection = figma.currentPage.selection;
if (selection.length === 0) {
  figma.notify('Please select something');
  return;
}
```

### ❌ Blocking Main Thread

```typescript
// WRONG: Long loop blocks Figma
for (let i = 0; i < 10000; i++) {
  figma.createRectangle();
}

// RIGHT: Batch with setTimeout
async function createManyRectangles(count: number) {
  const batchSize = 100;
  for (let i = 0; i < count; i += batchSize) {
    for (let j = 0; j < Math.min(batchSize, count - i); j++) {
      figma.createRectangle();
    }
    // Yield to Figma
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}
```

### ❌ Not Closing Plugin

```typescript
// WRONG: Plugin hangs
figma.showUI(__html__);
// User can't close if no cancel button

// RIGHT: Always provide exit
figma.showUI(__html__);
figma.ui.onmessage = (msg) => {
  if (msg.type === 'close') {
    figma.closePlugin();
  }
};
```

## Plugin Categories

| Category | Examples | Key APIs |
|----------|----------|----------|
| **Generators** | Lorem ipsum, icons, patterns | `figma.create*`, fills, text |
| **Utilities** | Rename layers, organize, cleanup | Selection, traversal, properties |
| **Importers** | JSON to layers, spreadsheet data | `figma.create*`, positioning |
| **Exporters** | Design tokens, code generation | Traversal, styles, properties |
| **Connectors** | Sync with external tools | `figma.clientStorage`, fetch |
| **Accessibility** | Contrast checker, a11y audit | Colors, text, traversal |

---

**References:**
- [references/plugin-api.md](references/plugin-api.md) — Complete API reference for nodes, properties, and methods
- [references/ui-development.md](references/ui-development.md) — Building plugin UIs with HTML/CSS/JS or React
- [references/common-patterns.md](references/common-patterns.md) — Selection, traversal, batch operations, undo
- [references/project-setup.md](references/project-setup.md) — Manifest, TypeScript, bundling, publishing
