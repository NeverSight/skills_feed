---
name: remotion-editor
description: Best practices for building video editors with Remotion
metadata:
  tags: remotion, editor, timeline, state-management, canvas, undo-redo
---

## When to use

Use this skill when you are building a video editor or an interactive creation tool on top of Remotion. It provides patterns for high-performance state management, timeline interactions, and canvas manipulation.

## How to use

Read individual rule files for detailed explanations and code examples:

### Core Architecture
- [rules/state-optimization.md](rules/state-optimization.md) - Using the "Many Contexts" pattern to optimize editor performance.
- [rules/undo-redo.md](rules/undo-redo.md) - Implementing an efficient undo/redo stack for video project states.
- [rules/feature-flags.md](rules/feature-flags.md) - Scaling an editor codebase with togglable features.

### Interaction & Math
- [rules/timeline-math.md](rules/timeline-math.md) - Best practices for frame-to-pixel translation, dragging, and snapping.
- [rules/timeline-interactions.md](rules/timeline-interactions.md) - Implementing smooth zooming and scroll restoration.
- [rules/canvas-logic.md](rules/canvas-logic.md) - Handling interactive elements, UV coordinates, and spatial transforms.
- [rules/keyboard-shortcuts.md](rules/keyboard-shortcuts.md) - Managing global hotkeys and focus-aware listeners.

### Lifecycle & Assets
- [rules/asset-lifecycle.md](rules/asset-lifecycle.md) - Local-first caching with IndexedDB and blob URL persistence.
- [rules/rendering-pipeline.md](rules/rendering-pipeline.md) - Implementing a robust state machine and polling for video exports.
- [rules/captioning-workflow.md](rules/captioning-workflow.md) - Managing multi-stage background tasks for AI-generated captions.
- [rules/editor-remotion-sync.md](rules/editor-remotion-sync.md) - Synchronizing editor state with Remotion compositions and the Player.
