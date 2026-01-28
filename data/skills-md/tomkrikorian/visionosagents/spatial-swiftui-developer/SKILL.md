---
name: spatial-swiftui-developer
description: Design and implement visionOS SwiftUI scenes that integrate RealityKit content. Use when building spatial UI with RealityView, Model3D, attachments, volumetric windows, ImmersiveSpace, or spatial gestures, or when choosing SwiftUI vs RealityKit APIs for 3D presentation.
---

# Spatial SwiftUI Developer

## Description and Goals

This skill provides guidance for designing and implementing visionOS SwiftUI scenes that integrate RealityKit content. It helps you choose between SwiftUI and RealityKit APIs for 3D presentation and shows how to bridge between the two frameworks effectively.

### Goals

- Enable developers to build spatial UI experiences on visionOS
- Guide selection between SwiftUI and RealityKit APIs for 3D content
- Show how to integrate RealityKit content into SwiftUI scenes
- Demonstrate spatial interaction patterns with gestures
- Support proper windowing and immersion patterns

## What This Skill Should Do

When building spatial UI with SwiftUI on visionOS, this skill should:

1. **Guide presentation surface selection** - Help you choose between WindowGroup, volumetric windows, and ImmersiveSpace
2. **Select 3D APIs** - Show when to use Model3D vs RealityView for different use cases
3. **Integrate RealityKit** - Demonstrate how to load and embed RealityKit content in SwiftUI
4. **Handle spatial interaction** - Provide patterns for spatial gestures and entity-targeted interactions
5. **Manage lifecycle** - Ensure proper async loading and state management

Load the appropriate reference file from the tables below for detailed usage, code examples, and best practices.

### Quick Start Workflow

1. Identify the presentation surface: `WindowGroup`, volumetric window, or `ImmersiveSpace`.
2. Choose a 3D API: `Model3D` for simple models, `RealityView` for full RealityKit scenes.
3. Load RealityKit content asynchronously and add entities in the `RealityView` make closure.
4. Use RealityView attachments to place SwiftUI UI in 3D space when needed.
5. Add spatial interaction with `SpatialTapGesture` or entity-targeted gestures.
6. Update RealityKit content in the `RealityView` update closure, not in SwiftUI body.
7. Validate scale using `defaultSize` for volumes and `immersionStyle` for immersive spaces.

## Information About the Skill

### Core Concepts

#### Scene and Spatial Presentation

- Use `WindowGroup` with `windowStyle(.volumetric)` and `defaultSize` for volumes.
- Use `ImmersiveSpace` for unbounded spatial scenes and `immersionStyle` selection.
- Use `openImmersiveSpace` and `dismissImmersiveSpace` for transitions.

#### RealityKit Embedding in SwiftUI

- Use `RealityView` for full RealityKit scenes and per-frame updates.
- Use `Attachment` and RealityView attachments to embed SwiftUI views in 3D.
- Use `ViewAttachmentEntity` and `ViewAttachmentComponent` for attachment entities.

#### 3D Model Presentation

- Use `Model3D` for async model loading with SwiftUI layout.
- Use `Model3DPhase` and `Model3DAsset` for loading phases and animation choices.

#### Spatial Input

- Use `SpatialTapGesture` for spatial tap locations in 2D/3D coordinate spaces.

### Reference Files

| Reference | When to Use |
|-----------|-------------|
| [`REFERENCE.md`](references/REFERENCE.md) | When looking for feature-focused code patterns and general guidance. |
| [`model3d.md`](references/model3d.md) | When using Model3D for async model loading, assets, animation, and manipulation. |
| [`realityview.md`](references/realityview.md) | When setting up RealityView, attachments, and RealityKit integration patterns. |
| [`interaction.md`](references/interaction.md) | When implementing gestures and manipulation patterns for spatial input. |
| [`windowing-immersion.md`](references/windowing-immersion.md) | When managing windows and immersive space patterns. |
| [`spatial-layout.md`](references/spatial-layout.md) | When using SwiftUI spatial layout APIs and debug tools. |
| [`charts-3d.md`](references/charts-3d.md) | When implementing Chart3D and surface plot patterns. |

### Implementation Patterns

- Use `Model3D` when you only need display and layout; use `RealityView` for custom entity graphs and systems.
- Keep RealityKit mutations inside `RealityView` make/update closures.
- Prefer attachments for UI that should remain SwiftUI-driven but positioned in 3D.
- Treat `ImmersiveSpace` as a separate scene with its own lifecycle and environment actions.

### Pitfalls and Checks

- Do not block the main actor with synchronous model or entity loading.
- Do not update RealityKit entities inside SwiftUI body computation.
- Do not use volumetric window style with `Window` instead of `WindowGroup`.
- Do not omit `defaultSize` for volumes; physical scale will be inconsistent.
- Prefer `.glassBackgroundEffect()` for backgrounds instead of custom blur/material backgrounds.
