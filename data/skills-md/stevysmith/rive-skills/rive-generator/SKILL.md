---
name: rive-generator
description: |
  Trigger when: (1) User wants to create a Rive animation programmatically,
  (2) User mentions "generate .riv file" or "create Rive animation",
  (3) User wants to see a visual animation created from code,
  (4) Working with the rive-generator project.

  Generate .riv files programmatically using TypeScript. Creates static shapes
  and animations. Requires npm package @stevysmith/rive-generator.
globs:
  - "**/*.riv"
alwaysApply: false
---

# Rive Generator Skill

Generate Rive animations programmatically using TypeScript.

## Installation

First, install the npm package:

```bash
npm install @stevysmith/rive-generator
```

## Quick Start

```typescript
import { writeFileSync } from 'fs';
import { RiveFile, hex } from '@stevysmith/rive-generator';

const riv = new RiveFile();

// Create artboard
const artboard = riv.addArtboard({
  name: 'My Animation',
  width: 400,
  height: 400,
});

// Add shape at center
const shape = riv.addShape(artboard, {
  name: 'MyShape',
  x: 200,
  y: 200,
});

// Add path (ellipse or rectangle)
riv.addEllipse(shape, { width: 100, height: 100 });

// Add fill with color
const fill = riv.addFill(shape);
riv.addSolidColor(fill, hex('#3498db'));

// Export
writeFileSync('my-animation.riv', riv.export());
```

## Running

```bash
# With TypeScript (Node 22+)
node --experimental-strip-types generate.ts

# Or compile first
npx tsc generate.ts && node generate.js
```

## API Reference

### RiveFile

Main class for building .riv files.

| Method | Description |
|--------|-------------|
| `addArtboard(options)` | Add an artboard (canvas) |
| `addNode(parent, options)` | Add a transform group |
| `addShape(parent, options)` | Add a shape container |
| `addEllipse(shape, options)` | Add an ellipse/circle |
| `addRectangle(shape, options)` | Add a rectangle |
| `addPointsPath(shape, options)` | Add a custom vector path |
| `addVertex(path, options)` | Add a straight vertex |
| `addFill(shape, options)` | Add a fill |
| `addStroke(shape, options)` | Add a stroke |
| `addSolidColor(paint, color)` | Set solid color |
| `addLinearGradient(paint, options)` | Add linear gradient |
| `addRadialGradient(paint, options)` | Add radial gradient |
| `addGradientStop(gradient, options)` | Add gradient color stop |
| `addLinearAnimation(artboard, options)` | Add an animation |
| `addKeyedObject(animation, targetId)` | Link animation to object |
| `addKeyedProperty(keyedObject, propertyKey)` | Specify property to animate |
| `addKeyFrameDouble(keyedProperty, options)` | Add a keyframe |
| `export()` | Returns `Uint8Array` of .riv binary |

## Colors

```typescript
import { hex, rgba } from '@stevysmith/rive-generator';

hex('#ff0000')           // Red
hex('#3498db')           // Nice blue
rgba(255, 0, 0, 255)     // Red with full opacity
rgba(0, 0, 0, 128)       // Semi-transparent black
```

## PropertyKey

```typescript
import { PropertyKey } from '@stevysmith/rive-generator';

PropertyKey.x          // X position
PropertyKey.y          // Y position
PropertyKey.scaleX     // X scale
PropertyKey.scaleY     // Y scale
PropertyKey.rotation   // Rotation (radians)
```

## Important Constraints

1. **Use a single Node container** - All shapes must be children of ONE Node under the Artboard.

2. **Gradient shapes must be LAST** - Add shapes with gradients after solid color shapes.

3. **DO NOT use CubicVertex** - Use `addVertex()` only. Approximate curves with many straight vertices.

4. **DO NOT use cornerRadius** - Use plain rectangles or PointsPath for rounded corners.

5. **First shape position bug** - Add a tiny transparent dummy shape first:
   ```typescript
   const dummy = riv.addShape(container, { name: 'Dummy', x: 0, y: 0 });
   riv.addRectangle(dummy, { width: 1, height: 1 });
   const dummyFill = riv.addFill(dummy);
   riv.addSolidColor(dummyFill, hex('#00000000'));
   ```

## Animation Example

```typescript
import { RiveFile, hex, PropertyKey } from '@stevysmith/rive-generator';
import { writeFileSync } from 'fs';

const riv = new RiveFile();
const artboard = riv.addArtboard({ name: 'Pulse', width: 200, height: 200 });

const shape = riv.addShape(artboard, { name: 'Circle', x: 100, y: 100 });
riv.addEllipse(shape, { width: 50, height: 50 });
const fill = riv.addFill(shape);
riv.addSolidColor(fill, hex('#e74c3c'));

const anim = riv.addLinearAnimation(artboard, {
  name: 'pulse',
  fps: 60,
  duration: 60,
  loop: 'pingPong',
});

const keyed = riv.addKeyedObject(anim, shape);

const scaleX = riv.addKeyedProperty(keyed, PropertyKey.scaleX);
riv.addKeyFrameDouble(scaleX, { frame: 0, value: 1.0, interpolation: 'cubic' });
riv.addKeyFrameDouble(scaleX, { frame: 30, value: 1.2, interpolation: 'cubic' });
riv.addKeyFrameDouble(scaleX, { frame: 60, value: 1.0, interpolation: 'cubic' });

const scaleY = riv.addKeyedProperty(keyed, PropertyKey.scaleY);
riv.addKeyFrameDouble(scaleY, { frame: 0, value: 1.0, interpolation: 'cubic' });
riv.addKeyFrameDouble(scaleY, { frame: 30, value: 1.2, interpolation: 'cubic' });
riv.addKeyFrameDouble(scaleY, { frame: 60, value: 1.0, interpolation: 'cubic' });

writeFileSync('pulse.riv', riv.export());
```

## Viewing Generated .riv Files

- [Rive Editor](https://rive.app) - Import to view/edit
- [rive.app/preview](https://rive.app/preview) - Quick online preview
- Your app using `@rive-app/canvas` or `@rive-app/react-canvas`
