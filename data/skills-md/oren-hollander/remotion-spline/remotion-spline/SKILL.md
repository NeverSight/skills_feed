---
name: remotion-spline
description: Smooth spline path animations for Remotion compositions — linear and Catmull-Rom splines with SVG path generation
---

# Remotion Spline Skill

Use the `remotion-spline` package's standalone spline functions to create smooth path animations in Remotion compositions.

## Available Functions

```typescript
import {
  evaluateLinearSpline,
  linearSplineToSVGPath,
  evaluateCatmullRom,
  catmullRomToSVGPath,
  type Point2D,
} from "remotion-spline";
```

### Point2D

```typescript
interface Point2D {
  readonly x: number;
  readonly y: number;
}
```

### Linear Spline

- `evaluateLinearSpline(points: Point2D[], t: number): [number, number]` — Evaluate position at parameter `t` (clamped to [0,1]) along a piecewise-linear path through `points`.
- `linearSplineToSVGPath(points: Point2D[]): string` — Convert points to an SVG `M ... L ...` path string.

### Catmull-Rom Spline

- `evaluateCatmullRom(points: Point2D[], t: number): [number, number]` — Evaluate position at parameter `t` (clamped to [0,1]) along a centripetal Catmull-Rom spline through `points`. Produces a smooth curve that passes through all control points.
- `catmullRomToSVGPath(points: Point2D[]): string` — Convert points to an SVG cubic Bezier path (`M ... C ...`) that matches the Catmull-Rom curve.

All functions require at least 2 points.

## Pattern: Animated Position Along a Spline

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { evaluateCatmullRom, catmullRomToSVGPath, type Point2D } from "remotion-spline";

const points: Point2D[] = [
  { x: 100, y: 500 },
  { x: 300, y: 200 },
  { x: 600, y: 400 },
];

export const MyAnimation: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const t = frame / (durationInFrames - 1);
  const [x, y] = evaluateCatmullRom(points, t);
  const pathD = catmullRomToSVGPath(points);

  return (
    <svg viewBox="0 0 800 800">
      {/* Static path */}
      <path d={pathD} stroke="blue" strokeWidth="2" fill="none" />
      {/* Animated dot */}
      <circle cx={x} cy={y} r="10" fill="red" />
    </svg>
  );
};
```

## Tips

- `t=0` returns the first point, `t=1` returns the last point.
- Values outside [0,1] are clamped automatically.
- Catmull-Rom splines produce smooth curves through all control points — no need to manually compute Bezier handles.
- Use `linearSplineToSVGPath` / `catmullRomToSVGPath` for static path rendering (racing lines, trails, guides).
- Use `evaluateLinearSpline` / `evaluateCatmullRom` with a time-varying `t` for animated position.
