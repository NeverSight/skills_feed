---
name: excalidraw-ai
description: >
  Create professional Excalidraw diagrams by generating JSON directly.
  This skill provides the Excalidraw JSON schema reference and professional icon libraries
  for AI agents to autonomously create diagrams without templates.
---

# excalidraw-ai

Generate Excalidraw diagrams by writing JSON directly. No templates needed - you have full control over every element.

## When to Use This Skill

Use this skill when you need to:
- Create architecture diagrams, flowcharts, or mind maps
- Visualize system designs, data flows, or processes
- Generate diagrams from code analysis or documentation
- Create custom diagrams with precise control over layout and styling

## Excalidraw JSON Schema

An Excalidraw file is a JSON object with this structure:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ /* array of element objects */ ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

### Element Types

#### Rectangle
```json
{
  "id": "unique-id-1",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 100,
  "strokeColor": "#1971c2",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "angle": 0,
  "seed": 12345,
  "isDeleted": false
}
```

#### Ellipse
```json
{
  "id": "unique-id-2",
  "type": "ellipse",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 100,
  "strokeColor": "#7c3aed",
  "backgroundColor": "#ede9fe",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1
}
```

#### Diamond
```json
{
  "id": "unique-id-3",
  "type": "diamond",
  "x": 100,
  "y": 100,
  "width": 120,
  "height": 120,
  "strokeColor": "#dc2626",
  "backgroundColor": "#fee2e2",
  "fillStyle": "solid"
}
```

#### Text
```json
{
  "id": "unique-id-4",
  "type": "text",
  "x": 110,
  "y": 140,
  "width": 180,
  "height": 25,
  "text": "Your Label Here",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent"
}
```

#### Arrow
```json
{
  "id": "unique-id-5",
  "type": "arrow",
  "x": 300,
  "y": 150,
  "width": 100,
  "height": 50,
  "strokeColor": "#1971c2",
  "strokeWidth": 2,
  "points": [[0, 0], [100, 50]],
  "startBinding": {
    "elementId": "source-element-id",
    "focus": 0.5,
    "gap": 5
  },
  "endBinding": {
    "elementId": "target-element-id",
    "focus": 0.5,
    "gap": 5
  },
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

#### Line
```json
{
  "id": "unique-id-6",
  "type": "line",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 0,
  "strokeColor": "#868e96",
  "strokeWidth": 1,
  "points": [[0, 0], [200, 0]],
  "startArrowhead": null,
  "endArrowhead": null
}
```

### Element Properties Reference

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier (use UUID or similar) |
| `type` | string | `rectangle`, `ellipse`, `diamond`, `text`, `arrow`, `line` |
| `x`, `y` | number | Position coordinates |
| `width`, `height` | number | Dimensions |
| `strokeColor` | string | Border/stroke color (hex) |
| `backgroundColor` | string | Fill color (hex) or `"transparent"` |
| `fillStyle` | string | `"solid"`, `"hachure"`, `"cross-hatch"` |
| `strokeWidth` | number | Line thickness (1, 2, 4) |
| `strokeStyle` | string | `"solid"`, `"dashed"`, `"dotted"` |
| `roughness` | number | 0 = sharp, 1 = normal, 2 = sketchy |
| `opacity` | number | 0-100 |
| `angle` | number | Rotation in radians |
| `groupIds` | array | Group element IDs together |
| `seed` | number | Random seed for hand-drawn effect |

### Text Properties

| Property | Type | Description |
|----------|------|-------------|
| `text` | string | The text content |
| `fontSize` | number | Font size in pixels |
| `fontFamily` | number | 1 = Virgil (hand-drawn), 2 = Helvetica, 3 = Cascadia |
| `textAlign` | string | `"left"`, `"center"`, `"right"` |
| `verticalAlign` | string | `"top"`, `"middle"` |

### Arrow Properties

| Property | Type | Description |
|----------|------|-------------|
| `points` | array | Array of [x, y] coordinates relative to element origin |
| `startBinding` | object | Connection to source element |
| `endBinding` | object | Connection to target element |
| `startArrowhead` | string | `null`, `"arrow"`, `"bar"`, `"dot"`, `"triangle"` |
| `endArrowhead` | string | `null`, `"arrow"`, `"bar"`, `"dot"`, `"triangle"` |

## Color Palette Reference

### Component-Based Colors (Recommended for Architecture Diagrams)

| Component Type | Stroke | Background | Use For |
|----------------|--------|------------|---------|
| **Database** | `#7c3aed` | `#ede9fe` | PostgreSQL, MySQL, MongoDB |
| **Cache** | `#dc2626` | `#fee2e2` | Redis, Memcached |
| **Queue** | `#16a34a` | `#dcfce7` | Kafka, RabbitMQ, SQS |
| **Load Balancer** | `#0891b2` | `#cffafe` | Nginx, HAProxy, ALB |
| **Gateway** | `#475569` | `#f1f5f9` | API Gateway, Kong |
| **CDN** | `#06b6d4` | `#e0f2fe` | CloudFront, Fastly |
| **Auth** | `#e11d48` | `#ffe4e6` | OAuth, IAM, Cognito |
| **Storage** | `#d97706` | `#fef3c7` | S3, Blob Storage |
| **Service** | `#2563eb` | `#dbeafe` | Backend services, APIs |
| **Container** | `#0284c7` | `#bae6fd` | Docker, Kubernetes |
| **Function** | `#f59e0b` | `#fef3c7` | Lambda, Serverless |
| **Monitoring** | `#84cc16` | `#ecfccb` | Prometheus, Grafana |
| **Web App** | `#4f46e5` | `#e0e7ff` | React, Vue, Frontend |
| **Mobile** | `#6366f1` | `#eef2ff` | iOS, Android |

### Theme Colors

**Modern (Default)**
- Primary: `#1971c2` / `#e7f5ff`
- Neutral: `#64748b` / `#f1f5f9`

**Sketchy (Hand-drawn)**
- Primary: `#495057` / `#f8f9fa`
- Use `roughness: 2` and `fontFamily: 3`

**Technical**
- Primary: `#2f9e44` / `#ebfbee`
- Use `strokeStyle: "dashed"` for connections

## Icon Libraries (305 Components Total)

Professional icons are available in `.excalidrawlib` files in the `assets/` directory:

| Library | Components | Content |
|---------|------------|---------|
| `aws-architecture-icons.excalidrawlib` | 248 | AWS service icons (Lambda, S3, EC2, RDS, DynamoDB, SQS, etc.) |
| `system-design.excalidrawlib` | 24 | System design elements (server, database, storage, etc.) |
| `drwnio.excalidrawlib` | 18 | Draw.io style icons |
| `system-design-template.excalidrawlib` | 8 | Pre-built templates (steps, flow, db, etc.) |
| `software-architecture.excalidrawlib` | 7 | Software architecture components |

### Using Library Components

Library files contain element arrays that can be embedded directly into your diagram. Each library item is an array of Excalidraw elements that form a component.

To use: Parse the library JSON, find the component you need, adjust positions, and include in your diagram's elements array.

## Layout Guidelines

### Architecture Diagram Layout

Organize components in layers (top to bottom):

```
Layer 1: Client/External (y: 100)
Layer 2: Edge/CDN (y: 280)
Layer 3: Gateway/Load Balancer (y: 460)
Layer 4: Services (y: 640)
Layer 5: Data/Cache (y: 820)
Layer 6: Infrastructure (y: 1000)
```

**Spacing recommendations:**
- Horizontal spacing between components: 240px
- Vertical spacing between layers: 180px
- Component width: 180-220px
- Component height: 80-100px

### Flowchart Layout

Arrange left-to-right or top-to-bottom:
- Step spacing: 200px
- Use rectangles for processes
- Use diamonds for decisions
- Use ellipses for start/end

### Mind Map Layout

Radial layout from center:
- Center node at (400, 300)
- Child nodes at radius 250px
- Distribute evenly using angle calculations

## Complete Example

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "id": "api-gateway",
      "type": "rectangle",
      "x": 100,
      "y": 100,
      "width": 180,
      "height": 80,
      "strokeColor": "#475569",
      "backgroundColor": "#f1f5f9",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "roughness": 0,
      "opacity": 100,
      "groupIds": ["group-1"],
      "seed": 1234
    },
    {
      "id": "api-gateway-label",
      "type": "text",
      "x": 140,
      "y": 130,
      "width": 100,
      "height": 25,
      "text": "API Gateway",
      "fontSize": 16,
      "fontFamily": 1,
      "textAlign": "center",
      "strokeColor": "#1e1e1e",
      "groupIds": ["group-1"]
    },
    {
      "id": "redis",
      "type": "diamond",
      "x": 100,
      "y": 280,
      "width": 180,
      "height": 100,
      "strokeColor": "#dc2626",
      "backgroundColor": "#fee2e2",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "roughness": 0,
      "seed": 5678
    },
    {
      "id": "redis-label",
      "type": "text",
      "x": 155,
      "y": 320,
      "width": 70,
      "height": 20,
      "text": "Redis",
      "fontSize": 16,
      "fontFamily": 1,
      "textAlign": "center",
      "strokeColor": "#1e1e1e"
    },
    {
      "id": "arrow-1",
      "type": "arrow",
      "x": 190,
      "y": 180,
      "width": 0,
      "height": 100,
      "strokeColor": "#64748b",
      "strokeWidth": 2,
      "points": [[0, 0], [0, 100]],
      "startBinding": {"elementId": "api-gateway", "focus": 0.5, "gap": 5},
      "endBinding": {"elementId": "redis", "focus": 0.5, "gap": 5},
      "endArrowhead": "arrow"
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

## Output

Save your diagram as a `.excalidraw` or `.json` file. It can be:
- Imported directly into [excalidraw.com](https://excalidraw.com)
- Embedded in documentation or web apps
- Converted to PNG/SVG using Excalidraw's export features

## Tips for AI Agents

1. **Generate unique IDs**: Use UUIDs or sequential IDs for each element
2. **Group related elements**: Use `groupIds` to keep shapes and their labels together
3. **Use bindings for arrows**: Connect arrows to elements using `startBinding` and `endBinding`
4. **Apply consistent styling**: Use the color palette for component types
5. **Calculate text positions**: Center text within shapes by adjusting x/y based on text length
6. **Set seed values**: Use `seed: hash(id)` for consistent hand-drawn rendering
