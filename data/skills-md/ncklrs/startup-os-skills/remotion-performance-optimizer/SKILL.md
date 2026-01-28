---
name: remotion-performance-optimizer
description: Analyzes Remotion compositions for performance issues and provides optimization recommendations. Identifies expensive computations, unnecessary re-renders, large assets, memoization opportunities, and architecture improvements. Use when optimizing render times or when asked to "improve performance", "speed up renders", "optimize Remotion video".
---

# Remotion Performance Optimizer

Comprehensive performance analysis and optimization recommendations for Remotion video compositions. Identifies bottlenecks and provides actionable fixes to reduce render times.

## What This Skill Does

Performs deep performance analysis:

1. **Computation analysis** — Identify expensive operations in render path
2. **Re-render detection** — Find unnecessary component re-renders
3. **Asset optimization** — Recommend asset size and format improvements
4. **Memoization opportunities** — Identify cacheable calculations
5. **Architecture review** — Suggest structural improvements
6. **Render profiling** — Analyze frame render times

## Input/Output Formats

### Input Format: Remotion Composition Code

Accepts implemented Remotion composition files:

**Files to analyze:**
```
src/remotion/compositions/VideoName/
├── index.tsx           # Main composition
├── constants.ts        # Color, timing, spring configs
├── types.ts            # TypeScript types
└── scenes/
    ├── Scene1.tsx
    ├── Scene2.tsx
    └── Scene3.tsx
```

**Context needed:**
- Target render time goals (e.g., < 100ms/frame)
- Composition complexity (simple, moderate, complex)
- Any specific performance concerns

**Example request:**
```
Analyze performance of VideoName composition.
Target: < 100ms/frame average render time.
Scene 2 is rendering slowly (200ms/frame).
```

### Output Format: OPTIMIZATION_REPORT.md

Generates detailed performance analysis with actionable fixes:

```markdown
# Performance Optimization Report: [Video Title]

**Date:** 2026-01-23
**Analyzer:** remotion-performance-optimizer
**Composition:** `src/remotion/compositions/VideoName/`

---

## Executive Summary

**Current Performance:** ⚠️ NEEDS OPTIMIZATION

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| **Average Render Time** | 145ms/frame | < 100ms | 🔴 45% over target |
| **Slowest Scene** | Scene 2: 285ms | < 150ms | 🔴 90% over target |
| **Total Render Time (estimated)** | 36 minutes | < 20 minutes | 🔴 80% over target |
| **Memory Usage** | Normal | Normal | 🟢 Good |

**Potential Improvement:** 60-70% faster render times after implementing recommendations

**Priority Actions:**
1. Replace Math.random() with seeded random in Scene 2 (55% improvement)
2. Optimize large product image (20% faster asset loading)
3. Extract repeated spring calculations (15% improvement)

---

## Performance Breakdown by Scene

| Scene | Avg Render Time | Status | Primary Bottleneck |
|-------|----------------|--------|-------------------|
| Scene 1 | 75ms | 🟢 Good | None |
| Scene 2 | 285ms | 🔴 Critical | Non-deterministic particle system |
| Scene 3 | 95ms | 🟡 Acceptable | Large asset loading |
| Scene 4 | 80ms | 🟢 Good | None |

**Overall:** 145ms average (Target: < 100ms)

---

## Issues Found

### CRITICAL (Major Performance Impact)

#### 1. Non-Deterministic Particle System in Scene 2
**Impact:** 🔴 200ms per frame slowdown
**Location:** `src/remotion/compositions/VideoName/scenes/Scene2.tsx:48-65`
**Severity:** Critical - 70% of render time in Scene 2

**Problem:**
```typescript
// ❌ PROBLEM: Math.random() called 70 times per frame
{Array.from({ length: 70 }, (_, i) => {
  const x = Math.random() * width;     // Recalculated every frame!
  const y = Math.random() * height;    // Non-deterministic
  const speed = Math.random() * 2;

  return <Particle key={i} x={x} y={y} speed={speed} />;
})}
```

**Why This Is Slow:**
- Math.random() is non-deterministic (different each frame)
- 70 particles × 3 random calls = 210 random calls per frame
- Remotion can't cache because values change
- Browser must recalculate positions every frame

**Solution:**
```typescript
// ✅ OPTIMIZED: Seeded random, deterministic
const seededRandom = (seed: number): number => {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
};

const particles = useMemo(
  () => Array.from({ length: 70 }, (_, i) => ({
    x: seededRandom(i * 123.456) * width,
    y: seededRandom(i * 789.012) * height,
    speed: seededRandom(i * 456.789) * 2,
  })),
  [width, height]
);

{particles.map((p, i) => (
  <Particle key={i} x={p.x} y={p.y} speed={p.speed} />
))}
```

**Expected Improvement:**
- Scene 2: 285ms → 125ms (55% faster)
- Overall: 145ms → 105ms (28% faster)
- Total render time: 36min → 22min (40% faster)

**Implementation Time:** 15 minutes

---

### HIGH (Significant Performance Impact)

#### 2. Large Unoptimized Product Image
**Impact:** 🟡 50ms asset loading delay
**Location:** `public/images/product.png`
**Severity:** High - Affects loading and memory

**Problem:**
```
Current Asset:
- Format: PNG (unnecessary transparency)
- Resolution: 4000x3000 (2x larger than needed)
- File Size: 8.2MB
- Load Time: ~50ms
```

**Why This Is Slow:**
- 8.2MB file takes time to load and decode
- 4000x3000 is overkill for 1920x1080 display
- PNG format unnecessary (no transparency used)

**Solution:**
```bash
# Resize and convert to JPEG
magick public/images/product.png \
  -resize 1920x1440 \
  -quality 90 \
  public/images/product.jpg

# Update code
<Img src={staticFile('images/product.jpg')} />
```

**Result:**
```
Optimized Asset:
- Format: JPEG
- Resolution: 1920x1440 (2x for retina)
- File Size: ~400KB (95% smaller)
- Load Time: ~5ms (90% faster)
```

**Expected Improvement:**
- Scene 3 load time: 50ms faster
- Overall render: 95ms → 85ms in Scene 3
- Smaller final video file

**Implementation Time:** 5 minutes

---

#### 3. Repeated Spring Calculations
**Impact:** 🟡 30ms per scene
**Location:** Multiple scenes
**Severity:** High - Accumulates across scenes

**Problem in Scene 1:**
```typescript
// ❌ PROBLEM: Spring calculated 3 times
<div style={{
  opacity: spring({ frame, fps, config: SMOOTH }),
  scale: spring({ frame, fps, config: SMOOTH }),
  y: interpolate(spring({ frame, fps, config: SMOOTH }), [0, 1], [0, 100]),
}} />
```

**Why This Is Slow:**
- Spring function has internal calculations
- Called 3 times with identical parameters
- Remotion can't optimize duplicate calls
- Wastes 20-30ms per scene

**Solution:**
```typescript
// ✅ OPTIMIZED: Calculate once, reuse
const progress = spring({ frame, fps, config: SMOOTH });

<div style={{
  opacity: progress,
  scale: progress,
  y: interpolate(progress, [0, 1], [0, 100]),
}} />
```

**Expected Improvement:**
- Per scene: 20-30ms faster
- Overall: 145ms → 125ms (15% faster)
- Affects Scenes 1, 3, 4

**Implementation Time:** 10 minutes

---

### MEDIUM (Moderate Performance Impact)

#### 4. Component Not Memoized
**Impact:** 🟡 10-15ms
**Location:** Scene components
**Severity:** Medium - Minor unnecessary re-renders

**Problem:**
```typescript
// Scene components re-render even when props haven't changed
function Scene1() { ... }
function Scene2() { ... }
```

**Solution:**
```typescript
import { memo } from 'react';

const Scene1 = memo(() => { ... });
const Scene2 = memo(() => { ... });
```

**Expected Improvement:**
- 10-15ms per scene
- Overall: 10% faster in complex compositions

**Implementation Time:** 5 minutes

---

### LOW (Minor Performance Impact)

#### 5. Array Creation in Render
**Impact:** 🟢 2-5ms
**Location:** `Scene4.tsx:23`
**Severity:** Low - Negligible but fixable

**Problem:**
```typescript
// Array recreated every frame
{Array(50).fill(0).map((_, i) => <Element key={i} />)}
```

**Solution:**
```typescript
// Reuse array reference
const ELEMENTS = Array.from({ length: 50 }, (_, i) => i);

{ELEMENTS.map((i) => <Element key={i} />)}
```

**Expected Improvement:** 2-5ms (minimal but good practice)

**Implementation Time:** 2 minutes

---

## Optimization Implementation Plan

### Phase 1: Critical Fixes (15 minutes) — 55% improvement
1. Replace Math.random() with seeded random in Scene 2
   - Expected: 285ms → 125ms

### Phase 2: High Priority (15 minutes) — 20% additional improvement
1. Optimize product.png to JPEG (5 min)
   - Expected: 95ms → 85ms in Scene 3
2. Extract spring calculations (10 min)
   - Expected: 145ms → 125ms overall

### Phase 3: Medium Priority (10 minutes) — 10% additional improvement
1. Memoize scene components
   - Expected: 10-15ms improvement

### Phase 4: Low Priority (5 minutes) — 2-5% improvement
1. Extract array constants
   - Expected: 2-5ms improvement

**Total Implementation Time:** 45 minutes
**Total Expected Improvement:** 60-70% faster renders

---

## Before/After Projections

| Metric | Before | After Phase 1 | After Phase 2 | After All | Target |
|--------|--------|---------------|---------------|-----------|--------|
| Scene 2 | 285ms | 125ms | 115ms | 110ms | < 150ms ✅ |
| Scene 3 | 95ms | 95ms | 85ms | 80ms | < 100ms ✅ |
| Overall Avg | 145ms | 105ms | 90ms | 85ms | < 100ms ✅ |
| Total Render | 36min | 22min | 19min | 18min | < 20min ✅ |

**After all optimizations:** All targets met! 🎉

---

## Performance Validation

### Benchmarking Commands

```bash
# Test single frame render time
npx remotion still src/index.tsx VideoName --frame=150

# Profile specific scene (Scene 2)
npx remotion still src/index.tsx VideoName --frame=225

# Benchmark full render (first 100 frames)
time npx remotion render src/index.tsx VideoName test.mp4 --frames=0-100

# Full production render with timing
time npx remotion render src/index.tsx VideoName output.mp4
```

### Performance Targets

| Composition Type | Target | Current | Status |
|-----------------|--------|---------|--------|
| Simple scenes | < 50ms | 75ms (Scenes 1,4) | 🟡 Acceptable |
| Moderate scenes | < 100ms | 145ms avg | 🔴 Over target |
| Complex scenes | < 150ms | 285ms (Scene 2) | 🔴 Over target |

**After optimizations:** All scenes should meet targets

---

## Code Quality Checks

✅ **Good Patterns Found:**
- Constants extracted (COLORS, SPRING_CONFIGS)
- useVideoConfig used for responsive sizing
- TypeScript types defined
- staticFile() used for assets

⚠️ **Optimization Opportunities:**
- [ ] Replace Math.random() with seeded random
- [ ] Extract repeated spring calculations
- [ ] Memoize scene components
- [ ] Optimize large assets

---

## Asset Optimization Details

### Current Assets

| Asset | Size | Format | Status | Recommendation |
|-------|------|--------|--------|----------------|
| logo.png | 180KB | PNG | 🟢 Good | Keep as-is |
| product.png | 8.2MB | PNG | 🔴 Optimize | → JPEG 400KB |
| background.mp3 | 1.8MB | MP3 | 🟢 Good | Keep as-is |
| whoosh.mp3 | 45KB | MP3 | 🟢 Good | Keep as-is |

### Optimization Commands

```bash
# Product image (95% size reduction)
magick public/images/product.png \
  -resize 1920x1440 \
  -quality 90 \
  public/images/product.jpg
```

---

## Recommendations Summary

### Immediate Actions (Critical)
1. ✅ **Replace Math.random() in Scene 2** — 55% faster
   - Priority: CRITICAL
   - Time: 15 minutes
   - Impact: 160ms per frame improvement

### Short-Term Actions (High Priority)
1. ✅ **Optimize product image** — 20% faster loading
   - Priority: HIGH
   - Time: 5 minutes
   - Impact: 50ms improvement

2. ✅ **Extract spring calculations** — 15% faster
   - Priority: HIGH
   - Time: 10 minutes
   - Impact: 20-30ms per scene

### Long-Term Improvements (Medium/Low)
1. Memoize scene components (10% improvement)
2. Extract array constants (2-5% improvement)
3. Consider lazy loading assets
4. Profile with Chrome DevTools for deeper analysis

---

## Next Steps

1. **Implement Critical Fix:** Replace Math.random() (highest impact)
2. **Benchmark:** Verify Scene 2 improvement (should be 285ms → 125ms)
3. **Implement High Priority:** Optimize assets and springs
4. **Re-run analysis:** Verify all targets met
5. **Final render:** Generate production video with optimizations

---

## Tools & Resources

### Profiling Tools
```bash
# Remotion built-in profiling
npx remotion preview --log=verbose

# Chrome DevTools profiling
# Open preview → DevTools → Performance tab → Record
```

### Optimization References
- Remotion Performance Docs: https://remotion.dev/docs/performance
- React Profiler: https://react.dev/reference/react/Profiler
- Seeded Random Pattern: See `/remotion-component-builder` skill

---

## Approval

**Status:** ⚠️ OPTIMIZATION REQUIRED BEFORE PRODUCTION

After implementing critical and high-priority fixes, this composition will meet all performance targets and be production-ready.

**Estimated Time to Production-Ready:** 30-45 minutes of optimization work

**Signed:** remotion-performance-optimizer
**Date:** 2026-01-23
```

**This document provides:**
- Current vs. target performance metrics
- Prioritized issues by impact (CRITICAL, HIGH, MEDIUM, LOW)
- Before/after projections with concrete numbers
- Specific code locations and fixes
- Implementation time estimates
- Step-by-step optimization plan
- Benchmarking commands for validation
- Asset optimization recommendations

**Feeds into:**
- Developer: Implement fixes
- Re-run `/remotion-video-reviewer` after optimizations
- Final production render

## Performance Analysis Categories

### 1. Expensive Computations

**Issue:** Calculations executed every frame unnecessarily.

**Detection:**
```typescript
// ❌ PROBLEM - Recalculated every frame
function Scene() {
  const frame = useCurrentFrame();

  // Heavy calculation every frame
  const particles = Array.from({ length: 1000 }, () => ({
    x: Math.random() * 1920,
    y: Math.random() * 1080,
  }));

  return /* render particles */;
}
```

**Solution:**
```typescript
// ✓ OPTIMIZED - Deterministic, seeded
function Scene() {
  const frame = useCurrentFrame();

  // Deterministic calculation
  const particles = useMemo(
    () => Array.from({ length: 1000 }, (_, i) => ({
      x: seededRandom(i * 123) * 1920,
      y: seededRandom(i * 456) * 1080,
    })),
    [] // No dependencies, calculate once
  );

  return /* render particles */;
}

// Seeded random for consistency
const seededRandom = (seed: number) => {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
};
```

**Impact:** 30-50% render time reduction for scenes with many elements.

### 2. Repeated Spring Calculations

**Issue:** Same spring calculation multiple times.

**Detection:**
```typescript
// ❌ PROBLEM - Spring calculated 3 times
<div style={{
  opacity: spring({ frame, fps, config: SMOOTH }),
  scale: spring({ frame, fps, config: SMOOTH }),
  y: interpolate(spring({ frame, fps, config: SMOOTH }), [0, 1], [0, 100]),
}} />
```

**Solution:**
```typescript
// ✓ OPTIMIZED - Calculate once, reuse
const progress = spring({ frame, fps, config: SMOOTH });

<div style={{
  opacity: progress,
  scale: progress,
  y: interpolate(progress, [0, 1], [0, 100]),
}} />
```

**Impact:** 10-20% render time reduction per scene.

### 3. Large Asset Sizes

**Issue:** Unoptimized assets slow down loading and rendering.

**Detection:**
```markdown
Product image: 4000x3000 PNG (8.2MB)
Background video: 3840x2160 ProRes (450MB)
Logo: 2000x2000 PNG (1.5MB)
```

**Recommendations:**
```markdown
✓ Product image: 1920x1440 JPEG 90% (400KB) — 95% smaller
✓ Background video: 1920x1080 H.264 (25MB) — 95% smaller
✓ Logo: 800x800 PNG optimized (80KB) — 95% smaller
```

**Impact:** Faster renders, smaller output files, better preview performance.

### 4. Unnecessary Re-renders

**Issue:** Components re-render when dependencies haven't changed.

**Detection:**
```typescript
// ❌ PROBLEM - Re-renders on every frame change
function ExpensiveComponent({ data }) {
  // Heavy calculation
  const processed = data.map(item => /* complex transform */);

  return /* render */;
}

// Parent re-renders every frame
<ExpensiveComponent data={staticData} />
```

**Solution:**
```typescript
// ✓ OPTIMIZED - Memoized component
const ExpensiveComponent = memo(({ data }) => {
  // Heavy calculation
  const processed = useMemo(
    () => data.map(item => /* complex transform */),
    [data]
  );

  return /* render */;
});

// Or: Extract static data outside component
const processedData = staticData.map(item => /* complex transform */);

function Scene() {
  return <Component data={processedData} />;
}
```

**Impact:** 20-40% render time reduction for complex components.

### 5. DOM Thrashing

**Issue:** Excessive DOM reads/writes causing layout thrashing.

**Detection:**
```typescript
// ❌ PROBLEM - Reading and writing in loop
elements.forEach((el) => {
  const width = el.getBoundingClientRect().width; // Read
  el.style.width = `${width * 2}px`; // Write (causes reflow)
});
```

**Solution:**
```typescript
// ✓ OPTIMIZED - Batch reads, then batch writes
const widths = elements.map((el) => el.getBoundingClientRect().width);
elements.forEach((el, i) => {
  el.style.width = `${widths[i] * 2}px`;
});
```

**Impact:** 15-30% improvement in DOM-heavy scenes.

### 6. Unoptimized Loops

**Issue:** Inefficient iteration patterns.

**Detection:**
```typescript
// ❌ PROBLEM - Array creation every frame
{Array(100).fill(0).map((_, i) => (
  <Particle key={i} index={i} />
))}
```

**Solution:**
```typescript
// ✓ OPTIMIZED - Reuse array reference
const PARTICLES = Array.from({ length: 100 }, (_, i) => i);

{PARTICLES.map((i) => (
  <Particle key={i} index={i} />
))}
```

**Impact:** 5-10% improvement in scenes with many elements.

## Performance Optimization Checklist

### Computation Optimizations
- [ ] No Math.random() in render (use seeded random)
- [ ] Heavy calculations use useMemo
- [ ] Spring calculations extracted and reused
- [ ] Static data moved outside components
- [ ] Loops use Array.from instead of Array().fill()

### Component Optimizations
- [ ] Expensive components wrapped in memo()
- [ ] useMemo for derived state
- [ ] useCallback for event handlers passed to children
- [ ] Components split appropriately (not too large)

### Asset Optimizations
- [ ] Images sized to actual display dimensions (2x for retina)
- [ ] JPEG for photos, PNG for transparency, SVG for graphics
- [ ] Videos use H.264 codec with reasonable bitrate
- [ ] Audio files trimmed to exact duration
- [ ] Fonts load only required weights

### Render Optimizations
- [ ] Avoid inline object/array creation in JSX
- [ ] Use key prop correctly in lists
- [ ] Minimize div nesting depth
- [ ] Use CSS transforms over position changes
- [ ] AbsoluteFill instead of complex layouts

### Architecture Optimizations
- [ ] Extract reusable components
- [ ] Scene components under 200 lines
- [ ] Constants extracted to top of file
- [ ] Utility functions outside components
- [ ] Logical component composition

## Performance Benchmarking

### Measuring Render Time

```bash
# Benchmark a specific frame
npx remotion still src/index.tsx VideoName --frame=100

# Benchmark full render (first 100 frames)
time npx remotion render src/index.tsx VideoName output.mp4 --frames=0-100

# Profile with Chrome DevTools
npx remotion preview
# Open Chrome DevTools → Performance tab → Record
```

### Performance Targets

| Composition Type | Target Render Time | Notes |
|-----------------|-------------------|-------|
| Simple (text, shapes) | < 50ms/frame | Minimal computations |
| Moderate (animations, images) | 50-100ms/frame | Standard videos |
| Complex (particles, 3D) | 100-200ms/frame | Heavy effects |
| Very Complex (thousands of elements) | 200-500ms/frame | Acceptable with optimization |

**Red flags:**
- Single frame > 500ms → Major optimization needed
- Render time increases over time → Memory leak

## Common Bottleneck Patterns

### Pattern 1: Particle Explosion

**Issue:**
```typescript
// 1000 particles, each calculating independently
{Array(1000).fill(0).map((_, i) => {
  const x = Math.random() * width;  // Recalculated every frame!
  const y = Math.random() * height;
  return <Particle key={i} x={x} y={y} />;
})}
```

**Fix:**
```typescript
// Deterministic particles, calculated once
const particles = useMemo(
  () => Array.from({ length: 1000 }, (_, i) => ({
    x: seededRandom(i * 123.456) * width,
    y: seededRandom(i * 789.012) * height,
  })),
  [width, height]
);

{particles.map((p, i) => (
  <Particle key={i} x={p.x} y={p.y} />
))}
```

### Pattern 2: Text Processing

**Issue:**
```typescript
// String operations every frame
const words = text.split(' ');
const processed = words.map(w => w.toUpperCase());
```

**Fix:**
```typescript
// Process once outside render
const processedWords = useMemo(
  () => text.split(' ').map(w => w.toUpperCase()),
  [text]
);
```

### Pattern 3: Conditional Rendering

**Issue:**
```typescript
// Component always rendered, visibility toggled
<HeavyComponent style={{ opacity: frame > 100 ? 1 : 0 }} />
```

**Fix:**
```typescript
// Don't render at all when not visible
{frame > 100 && <HeavyComponent />}
```

## Optimization Report Template

```markdown
## Performance Optimization Report

### Current Performance
- Average render time: 180ms/frame
- Slowest scene: Scene 3 (350ms/frame)
- Total video render time: 45 minutes (estimated)

### Identified Issues

**CRITICAL (Major Impact)**
1. Particle system using Math.random()
   - Location: Scene 2, ParticleSystem component
   - Impact: +200ms per frame
   - Fix: Replace with seeded random
   - Estimated improvement: 55% faster

2. 4K product image not optimized
   - Location: Scene 4
   - Current: 8.2MB PNG
   - Impact: Slow loading, memory pressure
   - Fix: Resize to 1920x1440, convert to JPEG
   - Estimated improvement: 95% smaller file

**HIGH (Significant Impact)**
1. Repeated spring calculations
   - Location: Scene 1, Scene 3, Scene 5
   - Impact: +50ms per scene
   - Fix: Extract to progress variable
   - Estimated improvement: 20% faster

**MEDIUM (Moderate Impact)**
1. Components not memoized
   - Location: Scene components
   - Fix: Wrap in React.memo()
   - Estimated improvement: 10% faster

### Optimization Plan

1. Implement seeded random (15 min) — 55% improvement
2. Optimize assets (30 min) — Better loading
3. Extract spring calculations (10 min) — 20% improvement
4. Memoize components (20 min) — 10% improvement

**Expected Result:**
- Render time: 180ms → 80ms per frame (55% faster)
- Total render: 45 min → 20 min
```

## Integration with Other Skills

**Works with:**
- `/remotion-video-reviewer` — Performance audit during review
- `/remotion-best-practices` — Ensures optimized patterns
- `/remotion-spec-translator` — Generates optimized code from start

## Rules Directory

Detailed optimization guides:

- [rules/computation-optimization.md](rules/computation-optimization.md) — Optimizing calculations
- [rules/asset-optimization.md](rules/asset-optimization.md) — Asset size and format
- [rules/memoization-strategies.md](rules/memoization-strategies.md) — When and how to memoize
- [rules/render-optimization.md](rules/render-optimization.md) — Render path improvements

---

This skill ensures Remotion videos render as fast as possible while maintaining quality.
