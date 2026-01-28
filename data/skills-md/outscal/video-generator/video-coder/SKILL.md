---
name: video-coder
description: Expert React video scene component creator for educational content. Builds production-grade, visually distinctive components using framer-motion animations, pixel-precise positioning, and optimized performance patterns. Follows strict component format with React.memo, threshold-based state updates, and module-level definitions. Outputs self-contained TSX components with proper timing sync, 60fps performance, and comprehensive reference-based implementation.
---

# Video Coder

<overview>
This skill guides creation of distinctive, production-grade React video scene components that avoid generic "AI slop" aesthetics and follow the aesthetics and style given. Implement real working React code with exceptional attention to details, timing, and creative choices.
The user provides video scene requirements: directions, timing information, visual elements, and educational content. They may include context about the purpose, audience, or technical constraints.
</overview>
<critical-requirements>
<design-execution>
**CRITICAL**: Follow the design and execute it with precision. Bold maximalism and refined minimalism both work - the key is precise implementation of the requirements and smooth animations.
</design-execution>
<asset-handling>
**Assets**: The design may reference assets from the `asset_manifest`. For elements with `type: "asset"`:
- The element's `id` matches an asset name in the manifest
- Read the SVG code from the `path` specified in the manifest
- Copy the SVG code directly into your React component
- For assets with follow-path, use the `orientation` field from the design spec (numeric degrees: 0°=up, 90°=right, 180°=down, 270°=left)
- Apply transforms from the design spec on a **wrapper div** (not on motion.div):
  - `rotation`: Rotate in degrees
  - `flipX`: Horizontal mirror (true = apply `scaleX(-1)`)
  - `flipY`: Vertical mirror (true = apply `scaleY(-1)`)
  - Combined: `style={{ transform: 'rotate(${rotation || 0}deg) scaleX(${flipX ? -1 : 1}) scaleY(${flipY ? -1 : 1})' }}`
- These values are pre-calculated by the designer. Do NOT perform any math on them.
- **IMPORTANT**: The `orientation` field is NOT a CSS transform. Never apply `orientation` as a CSS rotation. If no `rotation` field exists in the design, apply no rotation.
- Apply styles (position, size, fill, stroke) from the design spec to the SVG element

**Parent div vs motion.div example:**
```tsx
{/* PARENT DIV: positioning, static transforms (rotation, flip), z-index */}
<div
  className="absolute top-[300px] left-[500px] -translate-x-1/2 -translate-y-1/2 z-[10]"
  style={{ transform: 'rotate(45deg) scaleX(-1)' }}
>
  {/* MOTION.DIV: animations only (opacity, scale, movement) */}
  <motion.div
    initial={{ opacity: 0, scale: 0.8 }}
    animate={{ opacity: 1, scale: 1 }}
    transition={{ duration: 0.5 }}
  >
    <svg>...</svg>
  </motion.div>
</div>
```

| Property | Where to Apply |
|----------|----------------|
| `top`, `left`, `z-index` | Parent div (className) |
| `rotation`, `flipX`, `flipY` | Parent div (style.transform) |
| `opacity`, `scale` animations | motion.div |
| `x`, `y` movement animations | motion.div |
</asset-handling>
<implementation-requirements>
Then implement working React code following the component format that is:
- Production-grade and functional
- Properly structured with required props and timing patterns
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail
</implementation-requirements>
</critical-requirements>
<frontend-aesthetics>
<aesthetics-focus>
- **Color & Theme**: Follow the color theme as required
- **Motion**: Use framer-motion for all animations in React video components. Focus on high-impact moments: one well-orchestrated scene entry with staggered reveals (using delay) creates more delight than scattered micro-animations. Sync animations with the given timing in the given design.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays and etc. But make sure you follow the given color theme. You can be creative artist following the given design.
</aesthetics-focus>
<creative-interpretation>
Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same.
</creative-interpretation>
<complexity-matching>
**IMPORTANT**: Match implementation complexity to the given vision/design. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the design/vision well.
</complexity-matching>
</frontend-aesthetics>
<working-with-assets>
When the design includes elements with `type: "asset"`, you'll receive an `asset_manifest` with entries like:
<asset-manifest-example>
```json
{
  "name": "hypersonic_missile_main",
  "path": "Outputs/Assets/v20/hypersonic_missile_main.svg"
}
```
</asset-manifest-example>
<how-to-use-assets>
1. Read the SVG file from the `path` in the manifest
2. Copy the complete SVG code directly into your React component
3. Apply styles (position, size, fill, stroke) from the design spec to the SVG element (transforms go on wrapper div, not SVG)
4. The designer has already calculated all transforms (`rotation`, `flipX`, `flipY`) - use values as-is
5. Wrapper div transform: `rotate(${rotation || 0}deg) scaleX(${flipX ? -1 : 1}) scaleY(${flipY ? -1 : 1})`
6. Assets can be styled/colored using fill and stroke attributes if needed for the design
</how-to-use-assets>
</working-with-assets>
<react-component-format>
This document defines the required format for React video scene components.
<required-structure>
<imports>
```typescript
import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
```
</imports>
<props-interface>
```typescript
interface SceneProps {
  currentTime: number;
}
```
</props-interface>
<export-pattern>
```typescript
const Scene{N} = React.memo(function Scene{N}({ currentTime }: SceneProps) {
  // Component implementation
});

export default Scene{N};
```

Where `{N}` is the scene number (e.g., `Scene0`, `Scene1`, `Scene2`)

`currentTime` is the global value of time with respect to the video start.
</export-pattern>

</required-structure>

---

<sub-components>

### Sub-Components (CRITICAL)

**All sub-components MUST use `React.memo`** and be defined at module level (outside the main Scene component).

<react-memo>
#### Why React.memo is Required
- Video components re-render 60 times per second as `currentTime` changes
- Without `React.memo`, sub-components re-render unnecessarily causing animation jitter
- Module-level definitions ensure stable references across renders
</react-memo>

<sub-component-pattern>
// CORRECT: Module-level with React.memo + wrapper div for positioning
const TreeNode = React.memo(({
  value,
  position,
  isVisible
}: {
  value: string;
  position: { x: number; y: number };
  isVisible: boolean;
}) => (
  <div
    className="absolute -translate-x-1/2 -translate-y-1/2"
    style={{ left: `${position.x}px`, top: `${position.y}px` }}
  >
    <motion.div
      animate={isVisible ? "visible" : "hidden"}>
      {value}
    </motion.div>
  </div>
));
// WRONG: Defined inside component (causes jitter)
export default function Scene0({ currentTime }: SceneProps) {
  // ❌ Never define components here
  const TreeNode = ({ value }) => <div>{value}</div>;
}
</sub-component-pattern>

<module-level-definitions>
#### What Goes at Module Level (Outside Component)
1. **Sub-components** - Always wrapped with `React.memo`
2. **Wrapper div** - For positioning and other (absolute, translate, left/top style, etc.)
3. **Animation variants** - Objects defining animation states
4. **Static data** - Positions, configurations that don't change

```typescript
// Animation variants at module level
const fadeVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.5 } }
};

// Static positions at module level
const nodePositions = {
  node1: { x: 576, y: 540 },
  node2: { x: 1344, y: 540 }
};

// Sub-component at module level with React.memo + wrapper div
const InfoCard = React.memo(({ title, position, isVisible }: { title: string; position: { x: number; y: number }; isVisible: boolean }) => (
  <div
    className="absolute -translate-x-1/2 -translate-y-1/2"
    style={{ left: `${position.x}px`, top: `${position.y}px` }}
  >
    <motion.div variants={fadeVariants} animate={isVisible ? "visible" : "hidden"}>
      {title}
    </motion.div>
  </div>
));
```
</module-level-definitions>
</sub-components>
<complete-example>

```typescript
import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

interface SceneProps {
  currentTime: number;
}

// Animation variants at module level
const nodeVariants = {
  hidden: { scale: 0, opacity: 0 },
  visible: { scale: 1, opacity: 1, transition: { duration: 0.4 } }
};

// Static data at module level
const nodePositions = {
  node1: { x: 576, y: 540 },
  node2: { x: 1344, y: 540 }
};

// Sub-component at module level with React.memo
const TreeNode = React.memo(({
  value,
  position,
  isVisible
}: {
  value: string;
  position: { x: number; y: number };
  isVisible: boolean;
}) => (
  <div
    className="absolute -translate-x-1/2 -translate-y-1/2"
    style={{ left: `${position.x}px`, top: `${position.y}px` }}
  >
    <motion.div
      variants={nodeVariants}
      initial="hidden"
      animate={isVisible ? "visible" : "hidden"}
      className="w-20 h-20 rounded-full bg-white flex items-center justify-center"
    >
      {value}
    </motion.div>
  </div>
));

// Main Scene component with React.memo
const Scene0 = React.memo(function Scene0({ currentTime }: SceneProps) {
  // Threshold-based state updates
  const states = useMemo(() => ({
    showNode1: currentTime >= 1000,
    showNode2: currentTime >= 2000,
  }), [Math.floor(currentTime / 42)]);

  return (
    <div className="relative w-full h-full bg-gray-900">
      <TreeNode value="A" position={nodePositions.node1} isVisible={states.showNode1} />
      <TreeNode value="B" position={nodePositions.node2} isVisible={states.showNode2} />
    </div>
  );
});

export default Scene0;
```

</complete-example>
</react-component-format>
<tailwind-arbitrary-values>
Arbitrary values let you insert **any exact CSS value** inside a Tailwind class using **square brackets**, giving you full freedom beyond Tailwind's default scales.

### What They Do
Let you set **custom sizes, spacing, colors, borders, radii, typography, and positioning** instantly.
<tailwind-examples>
### Examples
- `w-[37px]`
- `h-[3.5rem]`
- `p-[18px]`
- `m-[2.75rem]`
- `bg-[#1a73e8]`
- `text-[22px]`
- `border-[3px]`
- `rounded-[14px]`
- `gap-[22px]`
- `top-[42px]`
- `z-[25]`
</tailwind-examples>
<tailwind-when-to-use>
Use arbitrary values for **one-off, precise custom values** without editing your Tailwind config.
</tailwind-when-to-use>
</tailwind-arbitrary-values>
<performance-optimizations>

**CRITICAL**: Follow these patterns to prevent animation jittering and re-rendering issues.

<performance-optimization-core-problem>

React video components re-render up to 60 times per second. Unstable references cause animations to restart, creating visual jitter.
</performance-optimization-core-problem>
<pattern-module-level-definitions>

Define sub-components, animation variants, and static data **outside** the parent component for stable references.

```tsx
// Animation variants at module level
const nodeVariants = { hidden: { scale: 0 }, visible: { scale: 1 } };

// Static data at module level
const nodePositions = { node1: { x: 576, y: 540 }, node2: { x: 740, y: 540 } };

// Sub-component at module level (see <complete-example> for full pattern)
const TreeNode = React.memo(({ value, position, isVisible }) => (
  <div style={{ left: `${position.x}px`, top: `${position.y}px` }}>
    <motion.div animate={isVisible ? "visible" : "hidden"}>{value}</motion.div>
  </div>
));
```

See `<complete-example>` above for the full implementation pattern.
</pattern-module-level-definitions>
<pattern-threshold-state-updates>
Update states every 42ms using `Math.floor(currentTime / 42)` to prevent excessive re-renders while matching 24fps video output.

```tsx
// State updates inside components
const states = useMemo(() => ({
  showTitle: currentTime >= 1000,
  showGrid: currentTime >= 2000,
  fadeOut: currentTime >= 9000
}), [Math.floor(currentTime / 42)]);

// Computed collections inside components
const visibleItems = useMemo(() => {
  const visible = new Set<string>();
  if (currentTime >= 1000) visible.add('item1');
  if (currentTime >= 2000) visible.add('item2');
  return visible;
}, [Math.floor(currentTime / 42)]);

// Static data created once at mount
const particles = useMemo(() =>
  Array.from({ length: 40 }, () => ({
    x: Math.random() * 100,
    y: Math.random() * 100
  })),
  [] // Empty deps = created once
);
```

<threshold-guidelines>
- `42ms` (24 updates/sec): Default for all animations (matches video output fps)
- `84ms` (12 updates/sec): Slow transitions
</threshold-guidelines>
</pattern-threshold-state-updates>
<pattern-explicit-props>

Pass all dependencies as explicit props for `React.memo` to work correctly.

```tsx
const TreeNode = React.memo(({
  value,
  position,
  showTree  // Explicit prop, not derived from currentTime inside
}: {
  value: string;
  position: { x: number; y: number };
  showTree: boolean;
}) => (
  <div
    className="absolute -translate-x-1/2 -translate-y-1/2"
    style={{ left: `${position.x}px`, top: `${position.y}px` }}
  >
    <motion.div animate={showTree ? "visible" : "hidden"}>
      {value}
    </motion.div>
  </div>
));

// In parent: derive state, pass as prop
<TreeNode value="50" position={{ x: 960, y: 540 }} showTree={states.showTree} />
```
</pattern-explicit-props>

---

<performance-summary>
Always use useMemo inside React components to prevent animation jitter caused by frequent re-renders—define static data and sub-components at module level, use threshold-based state updates (42ms intervals for 24fps), and pass explicit props for memoization.
</performance-summary>
</performance-optimizations>
<component-positioning>
Positioning elements in video scenes using Tailwind CSS and framer-motion.
<positioning-critical>
**CRITICAL**: Always use pixel values (px) as mentioned for positioning, This ensures precise, predictable positioning across all canvas sizes.
</positioning-critical>
<positioning-fundamentals>
<universal-pattern>
For ALL positioning in video scenes, use this consistent pattern with **pixel values**:
A motion.div cannot have absolute positioning, it should be wrapped inside an absolute div that is properly positioned as shown.
<example-universal-positioning>
```tsx
{/* Outer div: handles positioning with Tailwind using PIXELS */}
<div className="absolute top-[108px] left-[192px] -translate-x-1/2 -translate-y-1/2">
  {/* Inner div: content and animations */}
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
  >
    {/* Your content here */}
  </motion.div>
</div>
```
</example-universal-positioning>
<key-principles>
**Key principles:**
- Outer `div`: Uses `absolute` + pixel positioning classes + full centering transforms
- Inner `motion.div`: Handles animations and content
- **Always use BOTH** `-translate-x-1/2` AND `-translate-y-1/2` for consistent centering
- **Always use pixel values** (e.g., `top-[540px]`) NOT percentages
</key-principles>
</universal-pattern>
<cordinate-system>
COORDINATE SYSTEM
Origin: Top-left corner (0, 0)
X-axis: Increases rightward →
Y-axis: Increases downward ↓

FOR SHAPES/TEXT/ICONS:
  Position: Always refers to element's CENTER point

FOR PATHS:
  All coordinates are ABSOLUTE screen positions
  No position/size fields needed (implied by path coordinates)

ROTATION
0° = pointing up (↑)
90° = pointing right (→)
180° = pointing down (↓)
270° = pointing left (←)

Positive values = clockwise rotation
Negative values = counter-clockwise (-90° same as 270°)

EXAMPLE (1920×1080 viewport)
Screen center:        x = 960,  y = 540
Top-center:           x = 960,  y = 100
Bottom-left quadrant: x = 480,  y = 810
Right edge center:    x = 1820, y = 540
</cordinate-system>
</positioning-fundamentals>
<custom-positioning>
Position at any pixel value using the same pattern:

<example-custom-positioning>
{/* Landscape example: position at x=1440px, y=270px */}
<div className="absolute top-[270px] left-[1440px] -translate-x-1/2 -translate-y-1/2">
  <motion.div>{/* content */}</motion.div>
</div>
</example-custom-positioning>
</custom-positioning>
<full-centering-explanation>
Without `-translate-y-1/2`, the element's **top edge** sits at the pixel value, causing overlaps when elements have varying heights. Full centering positions the element's **center** at the pixel coordinate, ensuring safe spacing.
</full-centering-explanation>
<z-index-layering>
Layer elements using Tailwind's z-[index] utilities:
<example-z-index-layering>
{/* Background layer */}
<div className="absolute inset-0 z-[0]">...</div>

{/* Content layer - Landscape center: 540px, 960px */}
<div className="absolute top-[540px] left-[960px] -translate-x-1/2 -translate-y-1/2 z-[10]">
  <motion.div>...</motion.div>
</div>
{/* Overlay layer - Landscape: 216px from top, 1536px from left */}
<div className="absolute top-[216px] left-[1536px] -translate-x-1/2 -translate-y-1/2 z-[20]">
  <motion.div>...</motion.div>
</div>
</example-z-index-layering>
<z-index-scale>
**Standard z-index scale:**
- `z-[0]`: Background
- `z-[10]`: Main content
- `z-[20]`: Overlays/floating elements
- `z-[30]`: UI controls
- `z-[40]`: Modals/dialogs
- `z-[50]`: Top layer
</z-index-scale>
</z-index-layering>
</component-positioning>
<animation-patterns>

Be thorough in studying any animation pattern you're using in your scene.
<transition-types>

| Type | Description | Use Case |
|------|-------------|----------|
| **Tween** | Duration-based, precise timing | Coordinated animations, sync with audio |
| **Spring** | Physics-based, bounce/elasticity | Interactive UI, natural motion |
| **Inertia** | Momentum-based deceleration | Drag interactions, swipe gestures |
</transition-types>
<tween-transition>

```tsx
transition={{
  duration?: number,        // Seconds (default: 0.3)
  ease?: string | array,    // Easing function (default: "easeInOut")
  delay?: number,           // Delay in seconds
  repeat?: number,          // Number of repeats (Infinity for loop)
  repeatType?: "loop" | "reverse" | "mirror",
  times?: number[],         // Keyframe timing [0, 0.5, 1]
}}
```
<easing-functions>

| Ease | Behavior | Use Case |
|------|----------|----------|
| `linear` | Constant speed | Mechanical motion, loading indicators |
| `easeIn` | Slow → fast | Exit animations, falling objects |
| `easeOut` | Fast → slow | Entrances, coming to rest |
| `easeInOut` | Slow → fast → slow | Default for most UI animations |
| `circIn/Out/InOut` | Sharper circular curve | Snappy, aggressive motion |
| `backIn` | Pulls back, then forward | Anticipation effects |
| `backOut` | Overshoots, then settles | Bouncy clicks, attention-grabbing |
| `backInOut` | Both effects combined | Playful, game UI |
| `anticipate` | Dramatic pullback | Hero entrances, launch effects |
| `steps(n)` | Discrete steps | Pixel art, frame-by-frame |
</easing-functions>
<example-tween>
<motion.circle
  animate={{ cy: 200 }}
  transition={{ duration: 1.5, ease: "easeOut" }}
/>
</example-tween>
</tween-transition>
<spring-transition>
Only supports 2 keyframes (from → to).
<spring-physics-based>
**Option 1: Physics-based**
```tsx
transition={{
  type: "spring",
  stiffness?: number,  // Tightness (1-100: soft, 150-300: standard, 400-600: snappy)
  damping?: number,    // Resistance (higher = less bounce, 0 = infinite oscillation)
  mass?: number,       // Weight (higher = more lethargic)
}}
```
</spring-physics-based>
<spring-duration-based>
**Option 2: Duration-based**
```tsx
transition={{
  type: "spring",
  bounce?: number,     // 0-1 bounciness
  duration?: number,   // Seconds
}}
```
</spring-duration-based>

**Note:** Cannot mix `bounce` with `stiffness`/`damping`/`mass`.

<example-spring>
// Bouncy
transition={{ type: "spring", bounce: 0.6 }}

// Snappy
transition={{ type: "spring", stiffness: 400, damping: 30 }}

// Soft
transition={{ type: "spring", stiffness: 60, damping: 10 }}
</example-spring>
</spring-transition>
<inertia-transition>
<example-inertia>
```tsx
<motion.div
  drag
  dragConstraints={{ left: 0, right: 400 }}
  dragTransition={{
    power?: number,           // Deceleration rate (default: 0.8)
    timeConstant?: number,    // Duration in ms (default: 700)
    bounceStiffness?: number, // Boundary spring (default: 500)
    bounceDamping?: number,   // Boundary damping (default: 10)
  }}
/>
```
</example-inertia>
</inertia-transition>
<rotation-animation>
<example-rotation>

// Static orientation (asset facing a direction) - use wrapper div
<div style={{ transform: 'rotate(45deg)' }}>
  <motion.div>{/* content */}</motion.div>
</div>

// Static orientation with flip
<div style={{ transform: 'rotate(90deg) scaleX(-1)' }}>
  <motion.div>{/* content */}</motion.div>
</div>

**Animated rotation** (rotation that changes over time):

// Clockwise rotation (positive degrees)
<motion.div animate={{ rotate: 90 }} transition={{ duration: 1 }} />

// Anti-clockwise rotation (negative degrees)
<motion.div animate={{ rotate: -90 }} transition={{ duration: 1 }} />

// Continuous clockwise spin
<motion.div
  animate={{ rotate: 360 }}
  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
/>

// Continuous anti-clockwise spin
<motion.div
  animate={{ rotate: -360 }}
  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
/>

// Custom pivot point
<motion.div
  style={{ transformOrigin: "top left" }}
  animate={{ rotate: 45 }}
/>
</example-rotation>
<rotation-properties>
- `rotate` - 2D rotation in degrees (positive = clockwise, negative = anti-clockwise)
- `rotateX`, `rotateY` - 2D axis rotation
- `transformOrigin` - pivot point (default: `"center"`)
</rotation-properties>
</rotation-animation>
</animation-patterns>
<path-following>

For animating elements along SVG paths, see the dedicated **[path-following.md](./references/path-following.md)**.

**Important:** When a path has both `path-draw` and `follow-path` animations, apply the same easing to both to keep them synchronized.

---

<property-specific-transitions>

```tsx
transition={{
  x: { type: "spring", stiffness: 200 },
  opacity: { duration: 0.5, ease: "easeOut" },
  scale: { type: "spring", bounce: 0.6 }
}}
```
</property-specific-transitions>
</path-following>
<text-creation>
<text-important-notes>
- All text elements MUST be wrapped in a container div with `w-fit h-fit` and padding. The container div also handles positioning using classes from Component Positioning.
- Always use z-index values to control layering.
- Never set fontFamily to a specific font. Either omit it or use 'inherit'.
- **lineHeight MUST match the design**: If design specifies lineHeight, use that exact value. If not specified, browser default is 1.5.
- **textAlign is CSS only, NOT positioning**: The `textAlign` field from design applies to CSS `text-left`/`text-center`/`text-right` classes for multi-line text flow within the container. It does NOT affect container positioning. Always use `-translate-x-1/2 -translate-y-1/2` to center the container on x,y coordinates regardless of textAlign.
- **NEVER add `whitespace-nowrap`**: Do not add `whitespace-nowrap` to text elements unless explicitly specified in the design. Text should wrap naturally based on available width. Adding `whitespace-nowrap` can cause text to overflow outside the viewport.
</text-important-notes>
<example-container-pattern>
{/* Container: positioning + fit dimensions + padding */}
<div className="absolute -translate-x-1/2 -translate-y-1/2 top-[100px] left-[50px] w-fit h-fit p-[24px] z-[5]">
  <motion.span className="relative z-[6] ...">Your Text</motion.span>
</div>
</example-container-pattern>
<text-key-requirements>
**Key requirements:**
- `w-fit h-fit` - Container fits content exactly
- `p-[Npx]` - Padding must use pixel values in brackets (e.g., `p-[24px]`, `p-[16px]`)
</text-key-requirements>
<example-filled-background-reveal>
<div className="absolute -translate-x-1/2 -translate-y-1/2 top-[80px] left-[60px] w-fit h-fit p-[24px] z-[5]">
  <motion.div className="relative inline-block z-[6]">
    <motion.div
      className="absolute inset-0 bg-amber-500 z-[0]"
      initial={{ scaleX: 0 }}
      animate={{ scaleX: 1 }}
      style={{ transformOrigin: "left" }}
      transition={{ duration: 0.8, ease: "easeOut" }}
    />
    <motion.span
      className="relative z-[10] px-[16px] py-[8px] text-[48px] font-bold text-white block"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.4 }}
    >
      Revealed Text
    </motion.span>
  </motion.div>
</div>
</example-filled-background-reveal>
<example-frosted-glass>
<div className="absolute -translate-x-1/2 -translate-y-1/2 top-[150px] left-[80px] w-fit h-fit p-[24px] z-[5]">
  <motion.div
    className="inline-block bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl z-[6]"
    initial={{ opacity: 0, scale: 0.9 }}
    animate={{ opacity: 1, scale: 1 }}
  >
    <span className="block px-[32px] py-[20px] text-[40px] text-white/90 z-[7]">Frosted</span>
  </motion.div>
</div>
</example-frosted-glass>
<example-letter-by-letter-text>
<div className="absolute -translate-x-1/2 -translate-y-1/2 top-[100px] left-[80px] w-fit h-fit p-[24px] flex z-[5]">
  {"TEXT".split("").map((char, i) => (
    <motion.span
      key={i}
      className="text-[52px] font-black text-emerald-400 px-[4px] z-[8]"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: i * 0.08, duration: 0.4 }}
    >
      {char}
    </motion.span>
  ))}
</div>
</example-letter-by-letter-text>
<example-highlight-marker>
<div className="absolute -translate-x-1/2 -translate-y-1/2 top-[100px] left-[80px] w-fit h-fit p-[24px] z-[5]">
  <div className="relative inline-block -rotate-1 z-[6]">
    <motion.div
      className="absolute inset-0 bg-yellow-300/70 rounded-sm z-[0]"
      initial={{ scaleX: 0 }}
      animate={{ scaleX: 1 }}
      style={{ transformOrigin: "left" }}
    />
    <span className="relative z-[10] px-[12px] py-[4px] text-[38px] font-bold text-gray-900">Highlighted</span>
  </div>
</div>
</example-highlight-marker>
<example-gradient-text>
<div className="absolute -translate-x-1/2 -translate-y-1/2 top-[100px] left-[60px] w-fit h-fit p-[24px] z-[5]">
  <motion.span
    className="block px-[16px] py-[8px] text-[52px] font-black bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500 bg-clip-text text-transparent z-[9]"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
  >
    Gradient Text
  </motion.span>
</div>
</example-gradient-text>
<example-text-outline>
<div className="absolute -translate-x-1/2 -translate-y-1/2 top-[120px] left-[80px] w-fit h-fit p-[24px] z-[5]">
  <motion.span
    className="block text-[56px] font-black z-[8]"
    style={{ color: "transparent", WebkitTextStroke: "2px #fff" }}
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
  >
    OUTLINE
  </motion.span>
</div>
</example-text-outline>
<text-rules>
1. Always wrap text in a positioned container div with `w-fit h-fit` and padding
2. Padding must use pixel values: `p-[Npx]` (e.g., `p-[24px]`, `px-[16px]`, `py-[8px]`)
3. Use `inline-block` for backgrounds that fit text content
4. Use `block` on inner spans for proper padding
5. Use `overflow-hidden` when animating backgrounds
6. Set `relative z-[10]` on text layers over animated backgrounds
</text-rules>
</text-creation>
<path-elements>
<path-elements-reference>
Read [path-elements.md](./references/path-elements.md)
</path-elements-reference>
<path-elements-rules>
All path elements MUST be generated using the Python script - never manually approximate paths.
</path-elements-rules>
<creative-reminder>
Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
</creative-reminder>
</path-elements>
<reference-map>
<reference-path-elements>
`./references/path-elements.md` — Generating SVG paths from design specs using Python script, path rendering, composite paths
</reference-path-elements>
<reference-path-following>
`./references/path-following.md` — Animating elements along paths with getPathPoint, element orientation, static path-aligned elements
</reference-path-following>
</reference-map>