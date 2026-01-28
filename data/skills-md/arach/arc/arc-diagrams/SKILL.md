---
name: arc-diagrams
description: Create architecture diagrams using Arc's JSON format. Use when asked to "create an architecture diagram", "draw a system diagram", "visualize the architecture", or "make a diagram of".
---

# Arc Diagrams

Arc is a visual diagram editor for creating architecture diagrams. This skill enables you to generate Arc-compatible diagram configs that can be rendered in React applications.

## When to Use

Activate this skill when the user asks to:
- "Create an architecture diagram"
- "Draw a system diagram"
- "Visualize the architecture"
- "Make a diagram showing..."
- "Design a flow diagram"

## Diagram Format

Arc diagrams are JSON objects with this structure:

```typescript
interface ArcDiagramData {
  layout: { width: number; height: number }
  nodes: Record<string, NodePosition>
  nodeData: Record<string, NodeData>
  connectors: Connector[]
  connectorStyles: Record<string, ConnectorStyle>
}
```

## Creating a Diagram

### 1. Define Layout

Set canvas dimensions (default 1600x900 for editor, smaller for exports):

```json
"layout": { "width": 860, "height": 400 }
```

### 2. Position Nodes

Each node needs an `x`, `y` position and `size`:

```json
"nodes": {
  "frontend": { "x": 50,  "y": 100, "size": "l" },
  "api":      { "x": 300, "y": 100, "size": "m" },
  "database": { "x": 550, "y": 100, "size": "m" }
}
```

**Size options:**
| Size | Key | Dimensions |
|------|-----|------------|
| Extra Small | `xs` | 80 × 36 |
| Small | `s` | 95 × 42 |
| Medium | `m` | 145 × 68 |
| Large | `l` | 210 × 85 |

### 3. Define Node Data

Each node needs an icon, name, and color:

```json
"nodeData": {
  "frontend": {
    "icon": "Monitor",
    "name": "Frontend",
    "subtitle": "React",
    "description": "User interface",
    "color": "violet"
  },
  "api": {
    "icon": "Server",
    "name": "API",
    "subtitle": "Node.js",
    "description": "REST endpoints",
    "color": "emerald"
  },
  "database": {
    "icon": "Database",
    "name": "PostgreSQL",
    "subtitle": "Storage",
    "description": "Persistent data",
    "color": "blue"
  }
}
```

**Available icons (from Lucide):**
- **Devices:** Monitor, Server, Smartphone, Watch, Cloud, Cpu, Database, HardDrive
- **Network:** Wifi, Globe
- **Users:** User, Users
- **Security:** Lock, Key, Shield
- **Media:** Mic, Camera, Speaker, Headphones
- **Code:** Code, Terminal, FileCode, Folder
- **Data:** Zap, Activity, BarChart, PieChart
- **Flow:** ArrowRight, ArrowDown, RefreshCw, Repeat
- **Structure:** Box, Package, Layers, Grid
- **UI:** Settings, Bell, Mail, MessageSquare, Search, Filter
- **Actions:** Download, Upload, Play, Pause, Square, Circle

**Available colors:**
`violet` | `emerald` | `blue` | `amber` | `sky` | `zinc` | `rose` | `orange`

### 4. Connect Nodes

Define connections between nodes:

```json
"connectors": [
  {
    "from": "frontend",
    "to": "api",
    "fromAnchor": "right",
    "toAnchor": "left",
    "style": "http"
  },
  {
    "from": "api",
    "to": "database",
    "fromAnchor": "right",
    "toAnchor": "left",
    "style": "sql"
  }
]
```

**Anchor positions:**
`top` | `bottom` | `left` | `right` | `bottomLeft` | `bottomRight` | `topLeft` | `topRight`

**Optional:** Add `"curve": "natural"` or `"curve": "step"` for curved connectors.

### 5. Style Connectors

Define appearance for each connector style:

```json
"connectorStyles": {
  "http": { "color": "amber", "strokeWidth": 2, "label": "HTTP" },
  "sql": { "color": "blue", "strokeWidth": 2, "label": "SQL" },
  "async": { "color": "zinc", "strokeWidth": 1.5, "dashed": true }
}
```

## Complete Example

Here's a full diagram for a typical web application:

```json
{
  "layout": { "width": 700, "height": 300 },
  "nodes": {
    "client":   { "x": 50,  "y": 100, "size": "l" },
    "api":      { "x": 300, "y": 100, "size": "m" },
    "cache":    { "x": 300, "y": 220, "size": "s" },
    "database": { "x": 520, "y": 100, "size": "m" }
  },
  "nodeData": {
    "client":   { "icon": "Monitor",  "name": "Client",   "subtitle": "React",    "color": "violet" },
    "api":      { "icon": "Server",   "name": "API",      "subtitle": "Express",  "color": "emerald" },
    "cache":    { "icon": "Zap",      "name": "Cache",    "subtitle": "Redis",    "color": "amber" },
    "database": { "icon": "Database", "name": "Database", "subtitle": "Postgres", "color": "blue" }
  },
  "connectors": [
    { "from": "client", "to": "api",      "fromAnchor": "right",  "toAnchor": "left", "style": "http" },
    { "from": "api",    "to": "database", "fromAnchor": "right",  "toAnchor": "left", "style": "sql" },
    { "from": "api",    "to": "cache",    "fromAnchor": "bottom", "toAnchor": "top",  "style": "cache" }
  ],
  "connectorStyles": {
    "http":  { "color": "amber",   "strokeWidth": 2, "label": "HTTP" },
    "sql":   { "color": "blue",    "strokeWidth": 2, "label": "SQL" },
    "cache": { "color": "emerald", "strokeWidth": 2, "label": "cache" }
  }
}
```

## Layout Tips

1. **Grid alignment:** Position nodes on a ~50px grid for clean layouts
2. **Spacing:** Leave ~150-200px between connected nodes horizontally
3. **Flow direction:** Left-to-right or top-to-bottom for data flow
4. **Grouping:** Place related nodes close together
5. **Large nodes:** Use `l` size for primary/entry-point components
6. **Connectors:** Match connector colors to the source or destination node

## Output

When generating a diagram, output:
1. The complete JSON config
2. Brief explanation of the architecture shown
3. Suggest the user save it as a `.arc.json` file or paste into the Arc editor

## TypeScript Export

For React projects, diagrams can be exported as TypeScript:

```typescript
import type { ArcDiagramData } from '@arach/arc'

const diagram: ArcDiagramData = {
  // ... config here
}

export default diagram
```
