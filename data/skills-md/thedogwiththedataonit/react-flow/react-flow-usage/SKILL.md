---
name: react-flow-usage
description: Comprehensive React Flow (@xyflow/react) patterns and best practices for building node-based UIs, workflow editors, and interactive diagrams. Use when working with React Flow for (1) building flow editors or node-based interfaces, (2) creating custom nodes and edges, (3) implementing drag-and-drop workflows, (4) optimizing performance for large graphs, (5) managing flow state and interactions, (6) implementing auto-layout or positioning, or (7) TypeScript integration with React Flow.
license: MIT
metadata:
  author: xyflow Team
  version: "1.0.0"
  package: "@xyflow/react"
---

# React Flow Usage Guide

Comprehensive patterns and best practices for building production-ready node-based UIs with React Flow (@xyflow/react v12+).

## When to Use This Skill

Apply these guidelines when:
- Building workflow editors, flow diagrams, or node-based interfaces
- Creating custom node or edge components
- Implementing drag-and-drop functionality for visual programming
- Optimizing performance for graphs with 100+ nodes
- Managing flow state, save/restore, or undo/redo
- Implementing auto-layout with dagre, elkjs, or custom algorithms
- Integrating React Flow with TypeScript

## Rule Categories by Priority

| Priority | Category | Focus | Prefix |
|----------|----------|-------|--------|
| 1 | Setup & Configuration | CRITICAL | `setup-` |
| 2 | Performance Optimization | CRITICAL | `perf-` |
| 3 | Node Patterns | HIGH | `node-` |
| 4 | Edge Patterns | HIGH | `edge-` |
| 5 | State Management | HIGH | `state-` |
| 6 | Hooks Usage | MEDIUM | `hook-` |
| 7 | Layout & Positioning | MEDIUM | `layout-` |
| 8 | Interaction Patterns | MEDIUM | `interaction-` |
| 9 | TypeScript Integration | MEDIUM | `typescript-` |

## Quick Start Pattern

```tsx
import { useCallback } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes = [
  { id: '1', position: { x: 0, y: 0 }, data: { label: 'Node 1' } },
];

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2' },
];

// Define outside component or use useMemo
const nodeTypes = { custom: CustomNode };
const edgeTypes = { custom: CustomEdge };

function Flow() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}
```

## Core Concepts Overview

### Node Structure
- `id`: Unique identifier (required)
- `position`: `{ x: number, y: number }` (required)
- `data`: Custom data object (required)
- `type`: Built-in or custom type
- `style`, `className`: Styling
- `draggable`, `selectable`, `connectable`: Interaction controls
- `parentId`: For nested/grouped nodes
- `extent`: Movement boundaries

### Edge Structure
- `id`: Unique identifier (required)
- `source`: Source node id (required)
- `target`: Target node id (required)
- `sourceHandle`, `targetHandle`: Specific handle ids
- `type`: 'default' | 'straight' | 'step' | 'smoothstep' | custom
- `animated`: Boolean for animation
- `label`: String or React component
- `markerStart`, `markerEnd`: Arrow markers

### Handle Usage
- Position: `Position.Top | Bottom | Left | Right`
- Type: `'source' | 'target'`
- Multiple handles per node supported
- Use unique `id` prop for multiple handles

## Essential Patterns

### Custom Nodes
```tsx
import { memo } from 'react';
import { Handle, Position, NodeProps } from '@xyflow/react';

const CustomNode = memo(({ data, selected }: NodeProps) => {
  return (
    <div className={`custom-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      <div>{data.label}</div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
});

// IMPORTANT: Define outside component
const nodeTypes = { custom: CustomNode };
```

### Custom Edges
```tsx
import { BaseEdge, EdgeLabelRenderer, getBezierPath, EdgeProps } from '@xyflow/react';

function CustomEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition }: EdgeProps) {
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition,
  });

  return (
    <>
      <BaseEdge path={edgePath} />
      <EdgeLabelRenderer>
        <div style={{
          position: 'absolute',
          transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
        }}>
          Custom Label
        </div>
      </EdgeLabelRenderer>
    </>
  );
}
```

### Performance Optimization
```tsx
// 1. Memoize node/edge types (define outside component)
const nodeTypes = useMemo(() => ({ custom: CustomNode }), []);

// 2. Memoize callbacks
const onConnect = useCallback((params) =>
  setEdges((eds) => addEdge(params, eds)), [setEdges]
);

// 3. Use simple edge types for large graphs
const edgeType = nodes.length > 100 ? 'straight' : 'smoothstep';

// 4. Avoid unnecessary re-renders in custom components
const CustomNode = memo(({ data }) => <div>{data.label}</div>);
```

## Key Hooks

- `useReactFlow()` - Access flow instance methods (getNodes, setNodes, fitView, etc.)
- `useNodesState()` / `useEdgesState()` - Managed state with change handlers
- `useNodes()` / `useEdges()` - Reactive access to current nodes/edges
- `useNodesData(id)` - Get specific node data (more performant than useNodes)
- `useHandleConnections()` - Get connections for a handle
- `useConnection()` - Track connection in progress
- `useStore()` - Direct store access (use sparingly)

## Common Patterns

### Drag and Drop
```tsx
const onDrop = useCallback((event) => {
  event.preventDefault();
  const type = event.dataTransfer.getData('application/reactflow');
  const position = screenToFlowPosition({
    x: event.clientX,
    y: event.clientY,
  });

  setNodes((nds) => nds.concat({
    id: getId(),
    type,
    position,
    data: { label: `${type} node` },
  }));
}, [screenToFlowPosition]);
```

### Save and Restore
```tsx
const { toObject } = useReactFlow();

// Save
const flow = toObject();
localStorage.setItem('flow', JSON.stringify(flow));

// Restore
const flow = JSON.parse(localStorage.getItem('flow'));
setNodes(flow.nodes || []);
setEdges(flow.edges || []);
setViewport(flow.viewport);
```

### Connection Validation
```tsx
const isValidConnection = useCallback((connection) => {
  // Prevent self-connections
  if (connection.source === connection.target) return false;

  // Custom validation logic
  return true;
}, []);
```

## Detailed Rules

For comprehensive patterns and best practices, see individual rule files in the `rules/` directory organized by category:

```
rules/setup-*.md          - Critical setup patterns
rules/perf-*.md           - Performance optimization
rules/node-*.md           - Node customization patterns
rules/edge-*.md           - Edge handling patterns
rules/state-*.md          - State management
rules/hook-*.md           - Hooks usage
rules/layout-*.md         - Layout and positioning
rules/interaction-*.md    - User interactions
rules/typescript-*.md     - TypeScript integration
```

## Full Compiled Documentation

For the complete guide with all rules and examples expanded: see `AGENTS.md`

## Scraped Documentation Reference

Comprehensive scraped documentation from reactflow.dev is available in `scraped/`:

- **Learn**: `scraped/learn-concepts/`, `scraped/learn-customization/`, `scraped/learn-advanced/`
- **API**: `scraped/api-hooks/`, `scraped/api-types/`, `scraped/api-utils/`, `scraped/api-components/`
- **Examples**: `scraped/examples-nodes/`, `scraped/examples-edges/`, `scraped/examples-interaction/`, `scraped/examples-layout/`
- **UI Components**: `scraped/ui-components/`
- **Tutorials**: `scraped/learn-tutorials/`
- **Troubleshooting**: `scraped/learn-troubleshooting/`

## Common Issues

1. **Couldn't create edge** - Add `onConnect` handler
2. **Nodes not draggable** - Check `nodesDraggable` prop
3. **CSS not loading** - Import `@xyflow/react/dist/style.css`
4. **useReactFlow outside provider** - Wrap with `<ReactFlowProvider>`
5. **Performance issues** - See Performance category rules
6. **TypeScript errors** - Use proper generic types `useReactFlow<NodeType, EdgeType>()`

## References

- Official Documentation: https://reactflow.dev
- GitHub: https://github.com/xyflow/xyflow
- Package: `@xyflow/react` (npm)
- Examples: https://reactflow.dev/examples
- API Reference: https://reactflow.dev/api-reference
