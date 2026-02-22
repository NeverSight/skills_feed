---
name: drag-and-drop
description: Implement drag and drop using @atlaskit/pragmatic-drag-and-drop. Use when implementing sortable lists, reorderable items, kanban boards, or any drag-drop interactions. Covers draggable setup, drop targets, edge detection, drag previews, and critical state management patterns to avoid performance issues.
---

# Drag and Drop with Pragmatic DnD

This project uses `@atlaskit/pragmatic-drag-and-drop` for drag-and-drop functionality.

## Required Imports

```tsx
import { combine } from "@atlaskit/pragmatic-drag-and-drop/combine"
import {
  draggable,
  dropTargetForElements,
  type ElementDropTargetEventBasePayload,
} from "@atlaskit/pragmatic-drag-and-drop/element/adapter"
import { pointerOutsideOfPreview } from "@atlaskit/pragmatic-drag-and-drop/element/pointer-outside-of-preview"
import { setCustomNativeDragPreview } from "@atlaskit/pragmatic-drag-and-drop/element/set-custom-native-drag-preview"
import {
  attachClosestEdge,
  type Edge,
  extractClosestEdge,
} from "@atlaskit/pragmatic-drag-and-drop-hitbox/closest-edge"
import { DropIndicator } from "@atlaskit/pragmatic-drag-and-drop-react-drop-indicator/box"
```

## Critical Pattern: Refs for Volatile State

**NEVER put volatile drag state in useEffect dependencies.** This causes handlers to re-register on every state change.

```tsx
// BAD - re-registers handlers on every edge change
const [closestEdge, setClosestEdge] = useState<Edge | null>(null)
useEffect(() => {
  // ...handlers using closestEdge
}, [closestEdge]) // Re-runs on every drag movement!

// GOOD - use ref + useCallback for volatile state
const [closestEdge, setClosestEdge] = useState<Edge | null>(null)
const closestEdgeRef = useRef<Edge | null>(null)

// Wrap in useCallback for lint compliance (exhaustive-deps)
const updateClosestEdge = useCallback((edge: Edge | null) => {
  closestEdgeRef.current = edge
  setClosestEdge(edge) // Still update state for rendering
}, [])

useEffect(() => {
  // ...handlers read closestEdgeRef.current instead
}, [/* stable deps */, updateClosestEdge]) // Include updateClosestEdge
```

**Import `useCallback`:**
```tsx
import { useCallback, useEffect, useRef, useState } from "react"
```

## Basic Draggable Item Pattern

```tsx
function DraggableItem({ item, index, instanceId, onDrop }) {
  const ref = useRef<HTMLDivElement>(null)
  const dragHandleRef = useRef<HTMLButtonElement>(null)
  const [isDragging, setIsDragging] = useState(false)
  const [closestEdge, setClosestEdge] = useState<Edge | null>(null)
  const closestEdgeRef = useRef<Edge | null>(null)

  const updateClosestEdge = useCallback((edge: Edge | null) => {
    closestEdgeRef.current = edge
    setClosestEdge(edge)
  }, [])

  useEffect(() => {
    const element = ref.current
    const dragHandle = dragHandleRef.current
    if (!element || !dragHandle) return

    const itemData = { id: item.id, index, instanceId }

    return combine(
      draggable({
        element: dragHandle,
        getInitialData: () => itemData,
        onDragStart: () => setIsDragging(true),
        onDrop: () => setIsDragging(false),
        onGenerateDragPreview({ nativeSetDragImage }) {
          setCustomNativeDragPreview({
            nativeSetDragImage,
            getOffset: pointerOutsideOfPreview({ x: "16px", y: "8px" }),
            render({ container }) {
              const preview = document.createElement("div")
              preview.style.cssText = `
                background: hsl(var(--background));
                border: 2px solid hsl(var(--border));
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: hsl(var(--foreground));
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
              `
              preview.textContent = item.label
              container.appendChild(preview)
            },
          })
        },
      }),
      dropTargetForElements({
        element,
        canDrop: ({ source }) =>
          source.data.instanceId === instanceId && source.data.index !== index,
        getData({ input }) {
          return attachClosestEdge(itemData, {
            element,
            input,
            allowedEdges: ["top", "bottom"],
          })
        },
        onDrag({ source, self }: ElementDropTargetEventBasePayload) {
          if (source.data.index === index) {
            updateClosestEdge(null)
            return
          }

          const edge = extractClosestEdge(self.data)
          const sourceIndex = source.data.index
          if (typeof sourceIndex !== "number") return

          // Hide indicator when it would be redundant
          const isItemBeforeSource = index === sourceIndex - 1
          const isItemAfterSource = index === sourceIndex + 1
          const isDropIndicatorHidden =
            (isItemBeforeSource && edge === "bottom") ||
            (isItemAfterSource && edge === "top")

          updateClosestEdge(isDropIndicatorHidden ? null : edge)
        },
        onDragLeave: () => updateClosestEdge(null),
        onDrop({ source }) {
          const sourceIndex = source.data.index
          if (typeof sourceIndex === "number" && sourceIndex !== index) {
            const edge = closestEdgeRef.current // Read from ref!
            const targetIndex = edge === "top" ? index : index + 1
            const adjustedTargetIndex =
              sourceIndex < targetIndex ? targetIndex - 1 : targetIndex
            onDrop(sourceIndex, adjustedTargetIndex)
          }
          updateClosestEdge(null)
        },
      }),
    )
  }, [item.id, item.label, index, instanceId, onDrop, updateClosestEdge])

  return (
    <div ref={ref} className="relative">
      {closestEdge && <DropIndicator edge={closestEdge} gap="2px" />}
      <div className={isDragging ? "opacity-50" : ""}>
        <button ref={dragHandleRef} type="button" aria-label="Drag to reorder">
          <GripVertical />
        </button>
        {/* Item content */}
      </div>
    </div>
  )
}
```

## Instance ID for Multiple Lists

Use `Symbol` to scope drag operations to a single list:

```tsx
function SortableList({ items }) {
  const [instanceId] = useState(() => Symbol("list"))
  // Pass instanceId to each item
}
```

## Reorder Handler

```tsx
const handleDrop = async (sourceIndex: number, targetIndex: number) => {
  const newItems = [...items]
  const [movedItem] = newItems.splice(sourceIndex, 1)
  if (movedItem) {
    newItems.splice(targetIndex, 0, movedItem)
    const updated = newItems.map((item, i) => ({ ...item, position: i }))
    setItems(updated) // Optimistic update
    await saveOrder(updated) // Persist
  }
}
```

## Checklist

- [ ] Refs for volatile state (closestEdge, etc.)
- [ ] Wrap updateClosestEdge in useCallback (lint compliance)
- [ ] Include updateClosestEdge in useEffect deps
- [ ] Instance ID for list scoping
- [ ] Drop indicator with edge detection
- [ ] Custom drag preview
- [ ] Optimistic UI updates
