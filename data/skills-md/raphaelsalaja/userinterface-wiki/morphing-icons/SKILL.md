---
name: morphing-icons
description: Build icon components where any icon morphs into any other through SVG line transformation. Use when asked to "create morphing icons", "build icon transitions", "animate between icons", or "transform icons".
license: MIT
metadata:
  author: raphael-salaja
  version: "1.0.0"
  source: /content/morphing-icons/index.mdx
---

# Morphing Icons

Build icons that transform through actual shape transformation, not crossfades. Any icon can morph into any other because they share the same underlying 3-line structure.

## Core Concept

Every icon is composed of exactly **three SVG lines**. Icons that need fewer lines collapse the extras to invisible center points. This constraint enables seamless morphing between any two icons.

## Architecture

### 1. Line Definition

Each line has coordinates and optional opacity:

```ts
interface IconLine {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  opacity?: number;
}
```

### 2. Collapsed Lines

Icons needing fewer than 3 lines use collapsed lines—zero-length lines at the center:

```ts
const CENTER = 7; // Center of 14x14 viewbox

const collapsed: IconLine = {
  x1: CENTER,
  y1: CENTER,
  x2: CENTER,
  y2: CENTER,
  opacity: 0,
};
```

### 3. Icon Definition

Each icon has exactly 3 lines, optional rotation, and optional group:

```ts
interface IconDefinition {
  lines: [IconLine, IconLine, IconLine];
  rotation?: number;
  group?: string;
}
```

### 4. Rotation Groups

Icons sharing a `group` animate rotation when transitioning between them. Icons without matching groups jump to the new rotation instantly:

```ts
// These rotate smoothly between each other
{ lines: plusLines, rotation: 0, group: "plus-cross" }   // plus
{ lines: plusLines, rotation: 45, group: "plus-cross" }  // cross

// These rotate smoothly between each other
{ lines: arrowLines, rotation: 0, group: "arrow" }       // arrow-right
{ lines: arrowLines, rotation: 90, group: "arrow" }      // arrow-down
{ lines: arrowLines, rotation: 180, group: "arrow" }     // arrow-left
{ lines: arrowLines, rotation: -90, group: "arrow" }     // arrow-up
```

## Implementation Rules

### `morphing-three-lines`
Every icon MUST use exactly 3 lines. No more, no fewer.

**Fail:**
```ts
const checkIcon = {
  lines: [
    { x1: 2, y1: 7.5, x2: 5.5, y2: 11 },
    { x1: 5.5, y1: 11, x2: 12, y2: 3 },
  ], // Only 2 lines
};
```

**Pass:**
```ts
const checkIcon = {
  lines: [
    { x1: 2, y1: 7.5, x2: 5.5, y2: 11 },
    { x1: 5.5, y1: 11, x2: 12, y2: 3 },
    collapsed, // Third line collapsed
  ],
};
```

### `morphing-use-collapsed`
Unused lines must use the collapsed constant, not omission or null.

**Fail:**
```ts
const minusIcon = {
  lines: [
    { x1: 2, y1: 7, x2: 12, y2: 7 },
    null,
    null,
  ],
};
```

**Pass:**
```ts
const minusIcon = {
  lines: [
    { x1: 2, y1: 7, x2: 12, y2: 7 },
    collapsed,
    collapsed,
  ],
};
```

### `morphing-consistent-viewbox`
All icons must use the same viewBox (14x14 recommended).

**Fail:**
```ts
// Mixing viewbox scales
const icon1 = { lines: [{ x1: 2, y1: 7, x2: 12, y2: 7 }, ...] }; // 14x14
const icon2 = { lines: [{ x1: 4, y1: 14, x2: 24, y2: 14 }, ...] }; // 28x28
```

**Pass:**
```ts
const VIEWBOX_SIZE = 14;
const CENTER = 7;
// All coordinates within 0-14 range
```

### `morphing-group-variants`
Icons that are rotational variants MUST share the same group and base lines.

**Fail:**
```ts
// Different line definitions for arrows
const arrowRight = { lines: [{ x1: 2, y1: 7, x2: 12, y2: 7 }, ...] };
const arrowDown = { lines: [{ x1: 7, y1: 2, x2: 7, y2: 12 }, ...] }; // Different!
```

**Pass:**
```ts
const arrowLines: [IconLine, IconLine, IconLine] = [
  { x1: 2, y1: 7, x2: 12, y2: 7 },
  { x1: 7.5, y1: 2.5, x2: 12, y2: 7 },
  { x1: 7.5, y1: 11.5, x2: 12, y2: 7 },
];

const icons = {
  "arrow-right": { lines: arrowLines, rotation: 0, group: "arrow" },
  "arrow-down": { lines: arrowLines, rotation: 90, group: "arrow" },
  "arrow-left": { lines: arrowLines, rotation: 180, group: "arrow" },
  "arrow-up": { lines: arrowLines, rotation: -90, group: "arrow" },
};
```

### `morphing-spring-rotation`
Rotation between grouped icons should use spring physics for natural motion.

**Fail:**
```tsx
<motion.g animate={{ rotate: rotation }} transition={{ duration: 0.3 }} />
```

**Pass:**
```tsx
const rotation = useSpring(definition.rotation ?? 0, activeTransition);

<motion.g style={{ rotate: rotation, transformOrigin: "center" }} />
```

### `morphing-reduced-motion`
Respect `prefers-reduced-motion` by disabling animations.

**Fail:**
```tsx
function MorphingIcon({ icon }: Props) {
  return <motion.line animate={...} transition={{ duration: 0.4 }} />;
}
```

**Pass:**
```tsx
function MorphingIcon({ icon }: Props) {
  const reducedMotion = useReducedMotion() ?? false;
  const activeTransition = reducedMotion ? { duration: 0 } : transition;
  
  return <motion.line animate={...} transition={activeTransition} />;
}
```

### `morphing-jump-non-grouped`
When transitioning between icons NOT in the same group, rotation should jump instantly.

**Fail:**
```tsx
// Always animating rotation regardless of group
useEffect(() => {
  rotation.set(definition.rotation ?? 0);
}, [definition]);
```

**Pass:**
```tsx
useEffect(() => {
  if (shouldRotate) {
    rotation.set(definition.rotation ?? 0); // Animate
  } else {
    rotation.jump(definition.rotation ?? 0); // Instant
  }
}, [definition, shouldRotate]);
```

### `morphing-strokelinecap-round`
Lines should use `strokeLinecap="round"` for polished endpoints.

**Fail:**
```tsx
<motion.line strokeLinecap="butt" />
```

**Pass:**
```tsx
<motion.line strokeLinecap="round" />
```

### `morphing-aria-hidden`
Icon SVGs should be `aria-hidden` since they're decorative.

**Fail:**
```tsx
<svg width={size} height={size}>...</svg>
```

**Pass:**
```tsx
<svg width={size} height={size} aria-hidden="true">...</svg>
```

## Common Icon Patterns

### Two-Line Icons (check, minus, equals, chevron)
Use one or two collapsed lines:

```ts
const check = {
  lines: [
    { x1: 2, y1: 7.5, x2: 5.5, y2: 11 },
    { x1: 5.5, y1: 11, x2: 12, y2: 3 },
    collapsed,
  ],
};
```

### Three-Line Icons (menu, asterisk, play)
Use all three lines:

```ts
const menu = {
  lines: [
    { x1: 2, y1: 3.5, x2: 12, y2: 3.5 },
    { x1: 2, y1: 7, x2: 12, y2: 7 },
    { x1: 2, y1: 10.5, x2: 12, y2: 10.5 },
  ],
};
```

### Point Icons (more, grip)
Use zero-length lines as dots:

```ts
const more = {
  lines: [
    { x1: 3, y1: 7, x2: 3, y2: 7 },
    { x1: 7, y1: 7, x2: 7, y2: 7 },
    { x1: 11, y1: 7, x2: 11, y2: 7 },
  ],
};
```

## Recommended Transition

Use exponential ease-out for smooth morphing:

```ts
const defaultTransition: Transition = {
  ease: [0.19, 1, 0.22, 1],
  duration: 0.4,
};
```

## Output Format

When auditing morphing icon implementations, output findings as:

```
file:line - [rule-id] description of issue

Example:
components/icon/index.tsx:45 - [morphing-three-lines] Icon "check" has only 2 lines, needs collapsed third
components/icon/index.tsx:78 - [morphing-group-variants] arrow-down uses different line definitions than arrow-right
```

## Summary Table

After findings, output a summary:

| Rule | Count | Severity |
|------|-------|----------|
| `morphing-three-lines` | 2 | HIGH |
| `morphing-group-variants` | 1 | HIGH |
| `morphing-reduced-motion` | 1 | MEDIUM |

## References

- [Benji's experiments with Claude](https://benji.org/morphing-icons-with-claude)
- [Motion useSpring](https://motion.dev/docs/react-use-spring)
- [SVG Line Element](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/line)
