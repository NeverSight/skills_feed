---
name: arkit-visionos-developer
description: Build and debug ARKit features for visionOS, including ARKitSession setup, authorization, data providers (world tracking, plane detection, scene reconstruction, hand tracking), anchor processing, and RealityKit integration. Use when implementing ARKit workflows in immersive spaces or troubleshooting ARKit data access and provider behavior on visionOS.
---

# ARKit visionOS Developer

## Description and Goals

This skill provides comprehensive guidance for implementing ARKit-powered features on visionOS. ARKit on visionOS uses `ARKitSession` with data providers to access world tracking, hand tracking, plane detection, scene reconstruction, and other spatial data, which can then be bridged into RealityKit content.

### Goals

- Enable developers to set up and manage ARKitSession on visionOS
- Guide proper authorization handling for ARKit data providers
- Help developers choose and configure appropriate data providers
- Support anchor processing and RealityKit integration
- Ensure proper lifecycle management of ARKit sessions

## What This Skill Should Do

When implementing ARKit features on visionOS, this skill should:

1. **Guide ARKitSession setup** - Help you create and manage long-lived ARKitSession instances
2. **Handle authorization** - Show how to request and check authorization for required data types
3. **Select data providers** - Help you choose the right providers (world tracking, hand tracking, plane detection, etc.)
4. **Process anchors** - Demonstrate how to consume anchor updates and map them to RealityKit entities
5. **Manage lifecycle** - Ensure proper session start/stop and task cancellation
6. **Bridge to RealityKit** - Show how to integrate ARKit anchors with RealityKit content

Load the appropriate reference file from the tables below for detailed usage, code examples, and best practices.

### Quick Start Workflow

1. Add `NSWorldSensingUsageDescription` and `NSHandsTrackingUsageDescription` to `Info.plist` as needed.
2. Ensure the experience runs in a Full Space (ARKit data is unavailable in Shared Space).
3. Create a long-lived `ARKitSession` and the data providers you need.
4. Request authorization for provider-required data types before running the session.
5. Run the session with your providers and observe `anchorUpdates` streams.
6. Map anchors to RealityKit entities and keep state in a model layer.
7. Observe `ARKitSession.events` for authorization changes and errors.
8. Stop the session and cancel tasks when leaving the immersive space.

## Information About the Skill

### Core Concepts

#### ARKitSession Lifecycle

- Keep a strong reference to the session; call `run(_:)` with providers, stop on teardown.
- Sessions stop automatically on deinit, so maintain references throughout the immersive experience.

#### Authorization

- Use `requestAuthorization(for:)` or `queryAuthorization(for:)` and handle denied states gracefully.
- Request authorization before running the session with providers that require it.

#### Data Providers

- Choose providers for world tracking, plane detection, scene reconstruction, and hand tracking based on the feature set.
- Providers expose `anchorUpdates` streams that you consume to process anchors.

#### Anchors and Updates

- Consume provider `anchorUpdates` and reconcile added, updated, and removed anchors.
- Normalize anchor IDs to your own state model for reliable entity updates.

#### RealityKit Bridge

- Use `ARKitAnchorComponent` to inspect backing ARKit data on entities when needed.
- Treat ARKit streams as authoritative and keep rendering logic in RealityKit.

### Implementation Patterns

- Prefer one session per immersive experience and reuse providers when possible.
- Normalize anchor IDs to your own state model for reliable entity updates.
- Treat ARKit streams as authoritative and keep rendering logic in RealityKit.

### Provider References

| Provider | When to Use |
|----------|-------------|
| [`WorldTrackingProvider`](references/world-tracking-provider.md) | When tracking device position and orientation in 3D space. |
| [`HandTrackingProvider`](references/hand-tracking-provider.md) | When tracking hand poses and gestures for interaction. |
| [`PlaneDetectionProvider`](references/plane-detection-provider.md) | When detecting horizontal and vertical surfaces (floors, walls, tables). |
| [`SceneReconstructionProvider`](references/scene-reconstruction-provider.md) | When creating detailed 3D mesh reconstructions of the environment. |
| [`ImageTrackingProvider`](references/image-tracking-provider.md) | When tracking known images or reference objects. |
| [`ObjectTrackingProvider`](references/object-tracking-provider.md) | When tracking 3D objects in the environment. |
| [`RoomTrackingProvider`](references/room-tracking-provider.md) | When tracking room boundaries and room-scale experiences. |
| [`AccessoryTrackingProvider`](references/accessory-tracking-provider.md) | When tracking Apple Vision Pro accessories. |
| [`BarcodeDetectionProvider`](references/barcode-detection-provider.md) | When detecting and reading barcodes in the environment. |
| [`CameraFrameProvider`](references/camera-frame-provider.md) | When accessing raw camera frames for custom processing. |
| [`CameraRegionProvider`](references/camera-region-provider.md) | When accessing camera frames from specific regions. |
| [`EnvironmentLightEstimationProvider`](references/environment-light-estimation-provider.md) | When estimating ambient lighting conditions. |
| [`SharedCoordinateSpaceProvider`](references/shared-coordinate-space-provider.md) | When sharing coordinate spaces across multiple sessions. |
| [`StereoPropertiesProvider`](references/stereo-properties-provider.md) | When accessing stereo camera properties. |

### General ARKit Patterns

| Reference | When to Use |
|-----------|-------------|
| [`REFERENCE.md`](references/REFERENCE.md) | When implementing ARKit session setup, authorization, and general provider patterns. |

### Pitfalls and Checks

- Do not use `ARView` on visionOS; use `RealityView` and `ARKitSession` instead.
- Do not expect ARKit data in Shared Space; use Full Space only.
- Do not block the main actor while awaiting provider updates.
- Do not drop session references; ARKit stops sessions on deinit.
