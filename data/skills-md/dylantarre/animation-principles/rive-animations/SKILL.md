---
name: rive-animations
description: Use when implementing Disney's 12 animation principles with Rive interactive animations
---

# Rive Animation Principles

Implement all 12 Disney animation principles using Rive's state machine and interactive animations.

## 1. Squash and Stretch

In Rive Editor:
- Create shape with bones
- Animate scale X/Y with inverse relationship
- Key: `scaleX: 1.2` when `scaleY: 0.8`

```javascript
// Trigger from code
rive.play('squash_stretch');
```

## 2. Anticipation

State Machine Setup:
1. Create "Idle" state
2. Create "Anticipate" state (wind-up pose)
3. Create "Action" state
4. Connect: Idle → Anticipate → Action

```javascript
const inputs = rive.stateMachineInputs('State Machine');
const trigger = inputs.find(i => i.name === 'jump');
trigger.fire(); // Plays anticipate → action sequence
```

## 3. Staging

In Rive:
- Use artboard layers for depth
- Apply blur/opacity to background layers
- Use nested artboards for complex scenes

```javascript
// Control visibility
const bgOpacity = inputs.find(i => i.name === 'bgOpacity');
bgOpacity.value = 0.6;
```

## 4. Straight Ahead / Pose to Pose

Pose to Pose in Rive:
- Set key poses on timeline
- Rive interpolates between
- Use easing curves in Graph Editor

## 5. Follow Through and Overlapping Action

In Rive Editor:
- Use bone hierarchy with constraints
- Apply "delay" or "lag" to child bones
- Or offset keyframes by 2-4 frames
- Use spring constraints for natural follow-through

## 6. Slow In and Slow Out

In Rive Graph Editor:
- Select keyframes
- Apply easing: Cubic, Quad, Bounce
- Adjust bezier handles for custom curves

```javascript
// Runtime speed control
rive.play('animation', { speed: 0.5 });
```

## 7. Arc

In Rive:
- Use IK (Inverse Kinematics) for natural arcs
- Apply path constraints
- Animate position with curved interpolation

## 8. Secondary Action

State Machine approach:
```javascript
// Listen for state changes
rive.on('statechange', (event) => {
  if (event.data.includes('button_press')) {
    // Secondary animations auto-trigger via state machine
  }
});

// Or blend multiple animations
rive.play(['main_action', 'secondary_particles']);
```

## 9. Timing

```javascript
// Fast - snappy feedback
rive.play('click', { speed: 1.5 });

// Normal
rive.play('hover');

// Slow - dramatic reveal
rive.play('reveal', { speed: 0.5 });
```

In Rive Editor:
- Adjust animation duration
- Use work area to fine-tune timing
- Graph Editor for precise control

## 10. Exaggeration

In Rive:
- Push bone rotations beyond natural limits
- Exaggerate scale transformations
- Use elastic/bounce interpolation
- Overshoot in Graph Editor curves

## 11. Solid Drawing

In Rive:
- Use multiple bones for volume preservation
- Apply constraints to maintain form
- Use clipping for depth illusion
- Layer shapes for 3D effect

## 12. Appeal

Design in Rive:
- Smooth bezier curves on shapes
- Consistent stroke weights
- Pleasing color palette
- Clean bone structure

```javascript
// Smooth hover interactions
const hover = inputs.find(i => i.name === 'isHovering');
element.addEventListener('mouseenter', () => hover.value = true);
element.addEventListener('mouseleave', () => hover.value = false);
```

## React Implementation

```jsx
import { useRive, useStateMachineInput } from '@rive-app/react-canvas';

function AnimatedButton() {
  const { rive, RiveComponent } = useRive({
    src: 'button.riv',
    stateMachines: 'Button',
    autoplay: true
  });

  const hoverInput = useStateMachineInput(rive, 'Button', 'isHovering');

  return (
    <RiveComponent
      onMouseEnter={() => hoverInput.value = true}
      onMouseLeave={() => hoverInput.value = false}
    />
  );
}
```

## Key Rive Features

- **State Machines** - Logic-driven animation flow
- **Inputs** - Boolean, Number, Trigger types
- **Blend States** - Mix multiple animations
- **Listeners** - Pointer events in editor
- **Constraints** - IK, path, distance, rotation
- **Bones & Meshes** - Skeletal animation
- **Runtime API** - Full control from code
- **Tiny file size** - Optimized binary format
