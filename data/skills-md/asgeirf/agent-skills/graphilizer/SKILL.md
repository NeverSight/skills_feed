---
name: graphilizer
description: Generate interactive graph visualizations in the browser from any data - codebases, infrastructure, relationships, knowledge maps
triggers:
  - interactive graph
  - explore graph
  - visualize relationships
  - knowledge graph
  - dependency graph
  - network diagram
  - graphilizer
---

# Graphilizer Skill

Generate interactive graph visualizations that open in the browser for live exploration. You describe a domain — codebases, infrastructure, relationships, knowledge maps, anything — and this skill produces a React Flow app with search, filtering, and detail inspection. Unlike flow-graph which records videos, graphilizer keeps a live dev server running so the user can pan, zoom, click nodes, and explore.

## Workflow

### 1. Understand the Request

Parse the user's description to identify:
- **Domain** — what kind of data is being visualized (codebase, infrastructure, relationships, etc.)
- **Node types** — categories of entities (e.g. `service`, `database`, `user` for infrastructure)
- **Edge types** — categories of relationships (e.g. `depends-on`, `calls`, `reads-from`)
- **Grouping** — logical clusters of related nodes

### 2. Define Node and Edge Types

Create domain-specific type definitions in `settings.nodeTypes` and `settings.edgeTypes`. Each type gets a color, optional icon (emoji or image URL), optional border/line style, and a **shape** that controls how the node is rendered visually. Types are fully custom — define whatever makes sense for the domain.

**Choose the right shape for each entity type:**

| Shape     | Best for                                    | Visual                                        |
|-----------|---------------------------------------------|-----------------------------------------------|
| `default` | Services, entities, generic items           | Icon + label + type badge (horizontal)        |
| `card`    | People, products, detailed entities         | Large icon/image, title, description, tags    |
| `table`   | Databases, configs, specs, inventories      | Header + visible key-value rows               |
| `pill`    | Milestones, statuses, tags, phases          | Compact inline rounded label                  |

Mix shapes freely — a single graph can have card nodes for team members, table nodes for databases, default nodes for services, and pill nodes for deployment phases, all connected with edges.

### 3. Generate Graph JSON

Create the graph data JSON following the schema in [references/graphilizer-schema.md](references/graphilizer-schema.md).

```json
{
  "settings": {
    "title": "My Service Map",
    "description": "Production microservices and their dependencies",
    "layout": { "direction": "LR", "nodeSpacing": 80, "rankSpacing": 120 },
    "nodeTypes": {
      "service":  { "color": "#4A90D9", "icon": "🔧" },
      "database": { "color": "#E8A838", "icon": "🗄️", "shape": "table" },
      "person":   { "color": "#53d769", "icon": "👤", "shape": "card" },
      "phase":    { "color": "#a855f7", "icon": "🏁", "shape": "pill" }
    },
    "edgeTypes": {
      "calls": { "color": "#4A90D9", "style": "solid", "animated": true },
      "reads": { "color": "#E8A838", "style": "dashed" }
    }
  },
  "groups": [
    { "id": "backend", "label": "Backend Services" }
  ],
  "nodes": [
    { "id": "api", "label": "API Gateway", "type": "service", "group": "backend", "metadata": { "language": "Go", "team": "platform" } },
    { "id": "db", "label": "PostgreSQL", "type": "database", "metadata": { "version": "15", "size": "200GB", "tables": "42" } },
    { "id": "sarah", "label": "Sarah Chen", "type": "person", "description": "Tech Lead", "tags": ["Go", "Kubernetes"] },
    { "id": "beta", "label": "Beta Launch", "type": "phase" }
  ],
  "edges": [
    { "id": "e1", "source": "api", "target": "db", "label": "queries", "type": "reads" },
    { "id": "e2", "source": "sarah", "target": "api", "label": "leads" },
    { "id": "e3", "source": "beta", "target": "api", "label": "deploys" }
  ]
}
```

### 4. Write the JSON File

Write the graph JSON to a temporary file, e.g. `/tmp/graphilizer-data.json`.

### 5. Setup (first run only)

Install the skill's dependencies if not yet done:

```bash
cd <skill-dir> && npm install --prefer-offline --no-audit --no-fund
cd <skill-dir>/assets/graphilizer-template && npm install --prefer-offline --no-audit --no-fund
```

Where `<skill-dir>` is the directory containing this SKILL.md file.

### 6. Launch the Interactive Visualization

Run the serve script:

```bash
node <skill-dir>/scripts/serve.mjs /tmp/graphilizer-data.json --open
```

This starts a Vite dev server and opens the visualization in the user's default browser. The server stays running until the user is done exploring.

## Key Points

- **Node and edge types are domain-agnostic** — define whatever types make sense for the use case
- **Shapes** control how each type renders: `default` (box), `card` (vertical with image/tags), `table` (key-value rows), `pill` (compact inline). Mix freely in one graph
- **Icons** can be emojis, image URLs, or omitted entirely (shows a colored dot)
- **Positions are optional** — dagre auto-layout handles positioning when positions are not specified
- **Metadata** on nodes and edges is freeform key-value data that appears in the detail panel when clicked
- **Groups** cluster related nodes visually with a labeled container
- **Search** filters across labels and metadata values
- **Types not in the definitions** get auto-assigned colors from a default palette
- **Card-specific fields**: `description` (text), `tags` (array of strings), `image` (URL) — set directly on the node
- **Table-specific fields**: `rows` (array of `{key, value}`) — or omit and metadata is auto-displayed as rows
- **Layers** assign nodes and edges to logical sections (e.g. "Team", "Architecture", "Rollout") with toggle pills in the sidebar

## Layers

Layers let you partition a graph into logical sections that users can toggle on and off. This is essential for complex graphs that combine multiple concerns — e.g. an infrastructure graph with team responsibilities, architecture diagrams, and rollout phases all in the same view.

### How It Works

- Add a `layer` field (string) to any node or edge
- When more than one layer exists, the sidebar shows toggle pills for each layer
- Toggling a layer off **dims** (not removes) its nodes and edges to ~8% opacity
- Edges are dimmed if their explicit layer is disabled, or if both endpoints are dimmed
- Layers work alongside type and group filters — all filters compose

### Usage Guidelines

- Use layers to separate **conceptual domains** that exist in the same graph (e.g. "Team" vs "Architecture" vs "Rollout")
- Use groups to cluster **related items within a layer** (e.g. "Backend Services" group within the "Architecture" layer)
- Use types to distinguish **entity kinds** across layers (e.g. `service`, `database`, `person` can appear in any layer)
- Nodes and edges without a `layer` field are always visible

### Example

```json
{
  "nodes": [
    { "id": "sarah", "label": "Sarah Chen", "type": "lead", "layer": "Team" },
    { "id": "api", "label": "API Gateway", "type": "service", "layer": "Architecture" },
    { "id": "m-beta", "label": "Private Beta", "type": "milestone", "layer": "Rollout" }
  ],
  "edges": [
    { "id": "e1", "source": "sarah", "target": "api", "label": "leads", "layer": "Team" },
    { "id": "e2", "source": "api", "target": "auth", "label": "validates", "layer": "Architecture" },
    { "id": "e3", "source": "m-beta", "target": "webapp", "label": "ships", "layer": "Rollout" }
  ]
}
```

## Timeline Animation

When edges have an `order` field (integer), a timeline player appears with play/pause, a scrubber slider, and a reset button. This is useful for showing sequences: transfers over a window, build steps, event chains, deployment order, etc.

### How It Works

- Edges with `order` values are animated in sequence — 3 seconds per step
- **Future edges** (order > current step) render translucent so the full graph structure is visible
- **Active edges** (order === current step) are highlighted with a glow and an animated dot traveling along the path. Connected nodes also glow
- **Past edges** (order < current step) render at full opacity, normal style
- The slider scrubs smoothly during playback and can be dragged manually
- When a node is selected (focus mode), the timeline scopes to only the edges visible in that subgraph

### Subtitles

Edges can include a `subtitle` field — a short descriptive line displayed teletext-style at the bottom of the canvas during that edge's animation step. When multiple edges share the same order, their subtitles stack on separate lines.

### Edge Fields for Timeline

| Property   | Type    | Required | Description                                    |
|------------|---------|----------|------------------------------------------------|
| `order`    | integer | no       | Sequence position for timeline animation       |
| `subtitle` | string  | no       | Text shown at bottom of canvas during this step |

### Example: Animated Transfer Timeline

```json
{
  "edges": [
    { "id": "e1", "source": "a", "target": "b", "label": "Step 1", "type": "big", "order": 1, "subtitle": "First transfer completes" },
    { "id": "e2", "source": "b", "target": "c", "label": "Step 2a", "type": "medium", "order": 2, "subtitle": "Two things happen at once" },
    { "id": "e3", "source": "d", "target": "e", "label": "Step 2b", "type": "small", "order": 2, "subtitle": "This runs in parallel with 2a" },
    { "id": "e4", "source": "c", "target": "f", "label": "Step 3", "type": "big", "order": 3, "subtitle": "Final step wraps up" }
  ]
}
```

## Example: Breaking Bad Character Network

```json
{
  "settings": {
    "title": "Breaking Bad",
    "description": "Character relationships",
    "layout": { "direction": "TB", "nodeSpacing": 100, "rankSpacing": 150 },
    "nodeTypes": {
      "protagonist": { "color": "#4CAF50", "icon": "🧪" },
      "antagonist": { "color": "#F44336", "icon": "💀" },
      "family": { "color": "#2196F3", "icon": "👨‍👩‍👦" },
      "dea": { "color": "#FF9800", "icon": "🔫" }
    },
    "edgeTypes": {
      "family": { "color": "#2196F3", "style": "solid" },
      "business": { "color": "#4CAF50", "style": "dashed", "animated": true },
      "conflict": { "color": "#F44336", "style": "dotted" }
    }
  },
  "groups": [
    { "id": "white-family", "label": "White Family" },
    { "id": "cartel", "label": "Drug Trade" }
  ],
  "nodes": [
    { "id": "walt", "label": "Walter White", "type": "protagonist", "group": "white-family", "metadata": { "alias": "Heisenberg", "occupation": "Chemistry Teacher" } },
    { "id": "jesse", "label": "Jesse Pinkman", "type": "protagonist", "group": "cartel", "metadata": { "role": "Cook", "catchphrase": "Yeah, science!" } },
    { "id": "skyler", "label": "Skyler White", "type": "family", "group": "white-family" },
    { "id": "hank", "label": "Hank Schrader", "type": "dea", "metadata": { "role": "DEA Agent" } },
    { "id": "gus", "label": "Gus Fring", "type": "antagonist", "group": "cartel", "metadata": { "front": "Los Pollos Hermanos" } }
  ],
  "edges": [
    { "id": "e1", "source": "walt", "target": "jesse", "label": "partners", "type": "business" },
    { "id": "e2", "source": "walt", "target": "skyler", "label": "married", "type": "family" },
    { "id": "e3", "source": "hank", "target": "skyler", "label": "in-laws", "type": "family" },
    { "id": "e4", "source": "walt", "target": "gus", "label": "rivals", "type": "conflict" },
    { "id": "e5", "source": "gus", "target": "jesse", "label": "employer", "type": "business" }
  ]
}
```

## Schema Reference

See [references/graphilizer-schema.md](references/graphilizer-schema.md) for the complete JSON format specification.
