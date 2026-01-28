---
name: realitykit-visionos-developer
description: Build, debug, and optimize RealityKit scenes for visionOS, including entity/component setup, rendering, animation, physics, audio, input, attachments, and custom systems. Use when implementing RealityKit features or troubleshooting ECS behavior on visionOS.
---

# RealityKit visionOS Developer

## Description and Goals

This skill provides comprehensive guidance for implementing RealityKit-based spatial experiences on visionOS. RealityKit uses an Entity Component System (ECS) architecture where entities are lightweight containers, behavior comes from components, and systems drive per-frame updates.

### Goals

- Enable developers to build immersive 3D experiences on visionOS using RealityKit
- Provide clear guidance on when to use each component and system
- Help developers understand ECS patterns and best practices
- Support debugging and optimization of RealityKit scenes
- Ensure proper integration with SwiftUI via RealityView

## What This Skill Should Do

When implementing RealityKit features on visionOS, this skill should:

1. **Guide component selection** - Help you choose the right components for rendering, interaction, physics, audio, and animation needs
2. **Provide system implementation patterns** - Show how to create custom systems for continuous behavior
3. **Offer code examples** - Demonstrate common patterns like async asset loading, interactive entities, and custom systems
4. **Highlight best practices** - Emphasize proper async loading, component registration, and performance considerations
5. **Warn about pitfalls** - Identify common mistakes like using ARView on visionOS or blocking the main actor

Load the appropriate component or system reference file from the tables below for detailed usage, code examples, and best practices.


## Information About the Skill

### Core Concepts

#### Entities and Components

- Entities are lightweight containers; behavior comes from components.
- Prefer composition over inheritance and use custom `Component` + `Codable` when you need per-entity state.
- Register custom components once with `Component.registerComponent()` before use.
- Keep entity transforms and component updates on the main actor.

#### RealityView and Attachments

- Use `RealityView` to bridge SwiftUI and RealityKit.
- Load assets with `Entity(named:)` or `Entity(contentsOf:)` asynchronously and handle errors.
- Always use `ViewAttachmentComponent` for SwiftUI overlays in 3D and avoid the `RealityView` attachments closure.

#### Systems and Queries

- Use a custom `System` for continuous, per-frame behavior.
- Query entities with `EntityQuery` + `QueryPredicate` and process them in `update(context:)`.
- Use `SystemDependency` to control update order when multiple systems interact.

### Components Reference

Use this table to decide which component reference file to load when implementing RealityKit features:

#### Rendering and Appearance

| Component | When to Use |
|-----------|-------------|
| [`ModelComponent`](references/modelcomponent.md) | When rendering 3D geometry with meshes and materials on entities. |
| [`ModelSortGroupComponent`](references/modelsortgroupcomponent.md) | When experiencing depth fighting (z-fighting) issues with overlapping geometry or need to control draw order. |
| [`OpacityComponent`](references/opacitycomponent.md) | When creating fade effects, making entities semi-transparent, or implementing visibility transitions. |
| [`AdaptiveResolutionComponent`](references/adaptiveresolutioncomponent.md) | When optimizing performance in large scenes by reducing render quality for distant objects. |
| [`ModelDebugOptionsComponent`](references/modeldebugoptionscomponent.md) | When debugging rendering issues, visualizing model geometry, or inspecting bounding boxes during development. |
| [`MeshInstancesComponent`](references/meshinstancescomponent.md) | When rendering many copies of the same mesh efficiently (trees, crowds, particle-like objects). |
| [`BlendShapeWeightsComponent`](references/blendshapeweightscomponent.md) | When implementing facial animation, character expressions, or morphing mesh deformations. |

#### User Interaction

| Component | When to Use |
|-----------|-------------|
| [`InputTargetComponent`](references/inputtargetcomponent.md) | When making entities interactive (tappable, draggable) or handling user input events. |
| [`ManipulationComponent`](references/manipulationcomponent.md) | When implementing built-in drag, rotate, and scale interactions with hand gestures or trackpad. |
| [`GestureComponent`](references/gesturecomponent.md) | When implementing custom gesture recognition beyond what ManipulationComponent provides. |
| [`HoverEffectComponent`](references/hovereffectcomponent.md) | When providing visual feedback when users look at or hover over interactive entities. |
| [`AccessibilityComponent`](references/accessibilitycomponent.md) | When making entities accessible to screen readers, VoiceOver, or other assistive technologies. |
| [`BillboardComponent`](references/billboardcomponent.md) | When creating 2D sprites, text labels, or UI elements that should always face the viewer. |

#### Anchoring and Spatial

| Component | When to Use |
|-----------|-------------|
| [`AnchoringComponent`](references/anchoringcomponent.md) | When anchoring virtual content to detected planes, tracked images, hand locations, or world targets. |
| [`ARKitAnchorComponent`](references/arkitanchorcomponent.md) | When accessing the underlying ARKit anchor data for an anchored entity. |
| [`SceneUnderstandingComponent`](references/sceneunderstandingcomponent.md) | When accessing scene understanding data like detected objects or room reconstruction. |
| [`DockingRegionComponent`](references/dockingregioncomponent.md) | When defining regions where content can automatically dock or snap into place. |
| [`ReferenceComponent`](references/referencecomponent.md) | When implementing lazy loading of external entity assets or referencing entities in other files. |
| [`AttachedTransformComponent`](references/attachedtransformcomponent.md) | When attaching an entity's transform to another entity for hierarchical positioning. |

#### Cameras

| Component | When to Use |
|-----------|-------------|
| [`PerspectiveCameraComponent`](references/perspectivecameracomponent.md) | When configuring a perspective camera with depth and field of view for 3D scenes. |
| [`OrthographicCameraComponent`](references/orthographiccameracomponent.md) | When configuring an orthographic camera without perspective distortion for 2D-like views. |
| [`ProjectiveTransformCameraComponent`](references/projectivetransformcameracomponent.md) | When implementing custom camera projection transforms for specialized rendering needs. |

#### Lighting and Shadows

| Component | When to Use |
|-----------|-------------|
| [`PointLightComponent`](references/pointlightcomponent.md) | When adding an omnidirectional point light that radiates in all directions from a position. |
| [`DirectionalLightComponent`](references/directionallightcomponent.md) | When adding a directional light with parallel rays (like sunlight) for consistent scene lighting. |
| [`SpotLightComponent`](references/spotlightcomponent.md) | When adding a cone-shaped spotlight for focused, directional lighting effects. |
| [`ImageBasedLightComponent`](references/imagebasedlightcomponent.md) | When applying environment lighting from HDR textures for realistic reflections and ambient lighting. |
| [`ImageBasedLightReceiverComponent`](references/imagebasedlightreceivercomponent.md) | When enabling entities to receive and respond to image-based lighting in the scene. |
| [`GroundingShadowComponent`](references/groundingshadowcomponent.md) | When adding grounding shadows to visually anchor floating content to surfaces. |
| [`DynamicLightShadowComponent`](references/dynamiclightshadowcomponent.md) | When enabling real-time dynamic shadows cast by light sources onto entities. |
| [`EnvironmentLightingConfigurationComponent`](references/environmentlightingconfigurationcomponent.md) | When configuring environment lighting behavior, intensity, or blending modes. |
| [`VirtualEnvironmentProbeComponent`](references/virtualenvironmentprobecomponent.md) | When implementing reflection probes for accurate reflections in virtual environments. |

#### Audio

| Component | When to Use |
|-----------|-------------|
| [`SpatialAudioComponent`](references/spatialaudiocomponent.md) | When playing 3D positioned audio that changes based on listener position and orientation. |
| [`AmbientAudioComponent`](references/ambientaudiocomponent.md) | When playing non-directional ambient audio that doesn't change with listener position. |
| [`ChannelAudioComponent`](references/channelaudiocomponent.md) | When playing channel-based audio content (stereo, surround, etc.) without spatialization. |
| [`AudioLibraryComponent`](references/audiolibrarycomponent.md) | When storing and managing multiple audio resources for reuse across entities. |
| [`ReverbComponent`](references/reverbcomponent.md) | When applying reverb effects to an entity's audio for spatial acoustic simulation. |
| [`AudioMixGroupsComponent`](references/audiomixgroupscomponent.md) | When grouping audio sources for centralized mixing control and volume management. |

#### Animation and Character

| Component | When to Use |
|-----------|-------------|
| [`AnimationLibraryComponent`](references/animationlibrarycomponent.md) | When storing multiple animations (idle, walk, run) on a single entity for character animation. |
| [`CharacterControllerComponent`](references/charactercontrollercomponent.md) | When implementing character movement with physics, collision, and ground detection. |
| [`CharacterControllerStateComponent`](references/charactercontrollerstatecomponent.md) | When storing runtime state (velocity, grounded status) for a character controller. |
| [`SkeletalPosesComponent`](references/skeletalposescomponent.md) | When providing skeletal pose data for skeletal animation and bone transformations. |
| [`IKComponent`](references/ikcomponent.md) | When implementing inverse kinematics for procedural animation (e.g., reaching, pointing). |
| [`BodyTrackingComponent`](references/bodytrackingcomponent.md) | When integrating ARKit body tracking data to animate entities based on real-world body poses. |

#### Physics and Collision

| Component | When to Use |
|-----------|-------------|
| [`CollisionComponent`](references/collisioncomponent.md) | When defining collision shapes for hit testing, raycasting, or physics interactions. |
| [`PhysicsBodyComponent`](references/physicsbodycomponent.md) | When adding physical behavior (mass, gravity, forces) to entities for physics simulation. |
| [`PhysicsMotionComponent`](references/physicsmotioncomponent.md) | When controlling linear and angular velocity of physics bodies programmatically. |
| [`PhysicsSimulationComponent`](references/physicssimulationcomponent.md) | When configuring global physics simulation parameters like gravity or timestep. |
| [`ParticleEmitterComponent`](references/particleemittercomponent.md) | When emitting particle effects (smoke, sparks, debris) from an entity position. |
| [`ForceEffectComponent`](references/forceeffectcomponent.md) | When applying force fields (gravity wells, explosions) that affect multiple physics bodies. |
| [`PhysicsJointsComponent`](references/physicsjointscomponent.md) | When creating joints (hinges, springs) between physics bodies for articulated structures. |
| [`GeometricPinsComponent`](references/geometricpinscomponent.md) | When defining geometric attachment points for connecting entities at specific locations. |

#### Portals and Environments

| Component | When to Use |
|-----------|-------------|
| [`PortalComponent`](references/portalcomponent.md) | When creating portals that render a separate world or scene through an opening. |
| [`WorldComponent`](references/worldcomponent.md) | When designating an entity hierarchy as a separate renderable world for portal rendering. |
| [`PortalCrossingComponent`](references/portalcrossingcomponent.md) | When controlling behavior (teleportation, scene switching) when entities cross portal boundaries. |
| [`EnvironmentBlendingComponent`](references/environmentblendingcomponent.md) | When blending virtual content with the real environment for mixed reality experiences. |

#### Presentation and UI

| Component | When to Use |
|-----------|-------------|
| [`ViewAttachmentComponent`](references/viewattachmentcomponent.md) | When embedding SwiftUI views into 3D space for interactive UI elements or labels. |
| [`PresentationComponent`](references/presentationcomponent.md) | When presenting SwiftUI modals, sheets, or system UI from an entity interaction. |
| [`TextComponent`](references/textcomponent.md) | When rendering 3D text directly on entities without using SwiftUI views. |
| [`ImagePresentationComponent`](references/imagepresentationcomponent.md) | When displaying images or textures on entities in 3D space. |
| [`VideoPlayerComponent`](references/videoplayercomponent.md) | When playing video content on entity surfaces using AVPlayer. |

#### Networking and Sync

| Component | When to Use |
|-----------|-------------|
| [`SynchronizationComponent`](references/synchronizationcomponent.md) | When synchronizing entity state, transforms, and components across networked multiplayer sessions. |
| [`TransientComponent`](references/transientcomponent.md) | When marking entities as temporary, non-persistent, and excluded from network synchronization. |

### Systems Reference

Use this reference when implementing custom ECS behavior:

| System/API | When to Use |
|-----------|-------------|
| [`System and Component Creation`](references/systemandcomponentcreation.md) | When creating custom systems for continuous, per-frame behavior or custom components for per-entity state. |

### Implementation Patterns

#### RealityView Async Load

```swift
RealityView { content in
    do {
        let entity = try await Entity(named: "Scene")
        content.add(entity)
    } catch {
        print("Failed to load entity: \(error)")
    }
}
```

#### Interactive Entity Setup

```swift
let entity = ModelEntity(mesh: .generateBox(size: 0.1))
entity.components.set(CollisionComponent(shapes: [.generateBox(size: [0.1, 0.1, 0.1])]))
entity.components.set(InputTargetComponent())
entity.components.set(ManipulationComponent())
```

#### Custom System Skeleton

```swift
import RealityKit

struct SpinComponent: Component, Codable {
    var speed: Float
}

struct SpinSystem: System {
    static let query = EntityQuery(where: .has(SpinComponent.self))

    init(scene: Scene) {}

    func update(context: SceneUpdateContext) {
        for entity in context.entities(matching: Self.query, updatingSystemWhen: .rendering) {
            guard let spin = entity.components[SpinComponent.self] else { continue }
            entity.transform.rotation *= simd_quatf(angle: spin.speed * Float(context.deltaTime), axis: [0, 1, 0])
        }
    }
}

SpinSystem.registerSystem()
```

### Pitfalls and Checks

- Always load assets asynchronously; avoid blocking the main actor.
- Avoid `ARView` on visionOS; use `RealityView`.
- Add `CollisionComponent` + `InputTargetComponent` for draggable or tappable entities.
- Never use the `RealityView` update closure; use a custom `System` for continuous behavior instead.
- Mesh generation is limited to `box`, `sphere`, `plane`, `cylinder`, and `cone`.
