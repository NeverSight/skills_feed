---
name: remotion-video-reviewer
description: Structured review process for Remotion video implementations. Analyzes spec compliance, detects common timing/easing issues, validates asset quality, and provides prioritized revision lists. Use when reviewing Remotion code against design specs or performing quality assurance on video compositions. Trigger phrases "review video code", "check spec compliance", "audit Remotion implementation".
---

# Remotion Video Reviewer

Provides comprehensive, structured reviews of Remotion video implementations against motion design specifications. Identifies issues, assesses impact, and generates actionable revision lists.

## What This Skill Does

Performs multi-layer review analysis:

1. **Spec compliance** — Verifies implementation matches design spec
2. **Code quality** — Checks patterns, performance, best practices
3. **Timing accuracy** — Validates frame calculations and animation timing
4. **Visual fidelity** — Confirms colors, typography, layout match spec
5. **Asset quality** — Verifies assets are production-ready
6. **Performance** — Identifies render bottlenecks

## Input/Output Formats

### Input Format: VIDEO_SPEC.md + Code Files

Requires both the original specification and implemented code:

**VIDEO_SPEC.md** (from `/motion-designer`)
```markdown
# Video Title

## Overview
- Duration: 30 seconds
- Frame Rate: 30 fps

## Color Palette
Primary: #FF6B35
Background: #0A0A0A

## Scene 1: Opening (0s - 5s)
- Logo scales from 0.8 to 1.0
- Spring config: { damping: 200 }
```

**Code Files** to review:
- `src/remotion/compositions/VideoName/index.tsx`
- `src/remotion/compositions/VideoName/constants.ts`
- `src/remotion/compositions/VideoName/types.ts`
- Asset files in `public/`

### Output Format: REVIEW_REPORT.md

Generates a comprehensive review with prioritized issues:

```markdown
# Video Review Report: [Video Title]

**Date:** 2026-01-23
**Reviewer:** remotion-video-reviewer
**Spec Version:** VIDEO_SPEC.md v1.0
**Code Location:** `src/remotion/compositions/VideoName/`

---

## Executive Summary

**Overall Status:** ✅ APPROVED WITH MINOR REVISIONS

**Quick Stats:**
- Total Issues: 4 (0 critical, 1 high, 2 medium, 1 low)
- Spec Compliance: 95%
- Code Quality: Excellent
- Production Ready: Yes, after addressing HIGH priority items

**Recommendation:** Address high-priority color mismatch before final render. Medium and low priority items are optional improvements.

---

## Compliance Scores

| Category | Score | Status | Notes |
|----------|-------|--------|-------|
| **Spec Compliance** | 95% | 🟢 Pass | 1 color mismatch in Scene 3 |
| **Code Quality** | 98% | 🟢 Pass | Excellent structure, minor optimization opportunity |
| **Timing Accuracy** | 100% | 🟢 Pass | All frame calculations correct |
| **Visual Fidelity** | 95% | 🟢 Pass | Minor color deviation |
| **Asset Quality** | 90% | 🟡 Good | 1 image could be optimized |
| **Performance** | 95% | 🟢 Pass | Excellent render times |

**Overall Compliance:** 95.5% — Production Ready

---

## Issues Found

### CRITICAL (Must Fix Before Production)
_None_ ✅

### HIGH Priority (Should Fix)

#### 1. Scene 3 Background Color Mismatch
**Category:** Visual Fidelity
**Location:** `src/remotion/compositions/VideoName/scenes/Scene3.tsx:15`
**Impact:** Visual inconsistency with brand colors

**Issue:**
```typescript
// Current implementation
backgroundColor: '#0B0B0B'  // ❌ Wrong

// Spec requirement
Primary: #FF6B35
Background: #0A0A0A  // ✅ Correct
```

**Fix:**
```typescript
// Update to use COLORS constant
backgroundColor: COLORS.background  // Now: #0A0A0A
```

**Verification:**
- [ ] Update `constants.ts` if COLORS.background is incorrect
- [ ] Verify Scene 3 uses COLORS.background
- [ ] Visual check against spec color palette

---

### MEDIUM Priority (Consider Fixing)

#### 2. Large Product Image Could Be Optimized
**Category:** Asset Quality
**Location:** `public/images/product.png`
**Impact:** Slower render times, larger output file

**Current:**
- Format: PNG
- Resolution: 4000x3000
- File size: 8.2MB

**Recommendation:**
- Format: JPEG (no transparency needed)
- Resolution: 1920x1440 (2x display size)
- Quality: 90%
- Expected size: ~400KB (95% reduction)

**Fix:**
```bash
# Resize and convert
magick public/images/product.png -resize 1920x1440 -quality 90 public/images/product.jpg

# Update code to use .jpg
<Img src={staticFile('images/product.jpg')} />
```

**Benefits:**
- Faster preview/render times
- Smaller final video file
- No visual quality loss

---

#### 3. Particle System Could Use Memoization
**Category:** Performance
**Location:** `src/remotion/compositions/VideoName/scenes/Scene2.tsx:45`
**Impact:** Minor performance improvement possible

**Current:**
```typescript
// Particle positions recalculated (deterministic but not cached)
const particles = Array.from({ length: 70 }, (_, i) => ({
  x: seededRandom(i * 123) * width,
  y: seededRandom(i * 456) * height,
}));
```

**Recommendation:**
```typescript
import { useMemo } from 'react';

const particles = useMemo(
  () => Array.from({ length: 70 }, (_, i) => ({
    x: seededRandom(i * 123) * width,
    y: seededRandom(i * 456) * height,
  })),
  [width, height]
);
```

**Expected Impact:** 5-10% faster render for Scene 2

---

### LOW Priority (Nice to Have)

#### 4. Add JSDoc Comments to Scene Components
**Category:** Code Quality
**Location:** All scene components
**Impact:** Improved maintainability

**Recommendation:**
```typescript
/**
 * Scene 1: Opening animation with logo reveal
 * Duration: 0s - 5s (frames 0-150)
 * Spec reference: VIDEO_SPEC.md Section "Scene 1"
 */
function Scene1Opening() {
  // ...
}
```

**Benefits:**
- Easier for team members to understand
- Better IDE autocomplete
- Clear spec traceability

---

## Detailed Analysis

### Spec Compliance (95%)

✅ **Passed:**
- All 4 scenes implemented
- Scene timing matches spec exactly (verified frame calculations)
- Typography matches (Inter font, correct weights)
- Audio placement correct (background music + 2 SFX)
- Spring configurations match spec descriptions
- All animations implemented as described

❌ **Failed:**
- Scene 3 background color (#0B0B0B instead of #0A0A0A)

**Verification Steps Completed:**
- [x] Compared scene count: 4 scenes (matches)
- [x] Verified scene durations: All correct
- [x] Checked color palette: 1 mismatch found
- [x] Validated spring configs: All match
- [x] Tested audio timing: Correct

---

### Code Quality (98%)

✅ **Excellent Patterns:**
- Constants properly extracted (COLORS, SPRING_CONFIGS, SCENE_TIMING)
- Consistent naming conventions (Scene1Opening, Scene2Content)
- AbsoluteFill used correctly in all scenes
- Progress variables extracted (not inline spring calls)
- TypeScript types defined for all props
- Clean, readable code structure
- Proper imports from remotion

✅ **Best Practices Followed:**
- useVideoConfig used for responsive positioning
- staticFile() used for all assets
- Sequence timing uses constants
- No magic numbers in code
- Deterministic random in particle system

🟡 **Minor Improvements:**
- Could add useMemo to particle calculation (LOW impact)
- JSDoc comments would improve maintainability

---

### Timing Accuracy (100%)

✅ **All Verified:**
```
Scene 1: 0s - 5s    → frames 0-150    ✓ Correct (5 * 30fps)
Scene 2: 5s - 15s   → frames 150-450  ✓ Correct (10 * 30fps)
Scene 3: 15s - 25s  → frames 450-750  ✓ Correct (10 * 30fps)
Scene 4: 25s - 30s  → frames 750-900  ✓ Correct (5 * 30fps)

Total: 30s = 900 frames ✓ Correct
```

**Validation:**
- [x] All SCENE_TIMING constants match spec
- [x] Sequence components use correct start/duration
- [x] No timing overlap or gaps
- [x] Audio timing matches frame calculations

---

### Asset Quality (90%)

✅ **Good:**
- Logo: 800x800 PNG, optimized, transparent ✓
- Background music: 30s MP3, 192kbps ✓
- Whoosh SFX: MP3, proper duration ✓
- Pop SFX: MP3, proper duration ✓
- Font: Inter loaded correctly via @remotion/google-fonts ✓

🟡 **Could Improve:**
- Product image: 8.2MB PNG → Should be 1920x1440 JPEG (~400KB)

**Asset Checklist:**
- [x] All assets present in `public/`
- [x] Correct formats used (mostly)
- [x] staticFile() imports correct
- [ ] File sizes optimized (1 large image)
- [x] No missing assets

---

### Performance (95%)

**Render Performance:**
- Average: 85ms/frame ✅ Excellent (target: <100ms)
- Scene 1: 65ms/frame ✅
- Scene 2: 105ms/frame 🟡 (particle system, acceptable)
- Scene 3: 75ms/frame ✅
- Scene 4: 70ms/frame ✅

**No Major Issues:**
- ✅ Spring calculations extracted and reused
- ✅ No expensive operations in render path
- ✅ Assets load efficiently (except large PNG)
- ✅ No memory leaks detected

**Minor Optimization Opportunities:**
- Memoize particle calculations (5-10% improvement in Scene 2)
- Optimize product.png (faster asset loading)

---

## Recommendations

### Before Production
1. ✅ **Fix HIGH priority color mismatch** (5 minutes)
2. ⏭️ Consider optimizing product image (10 minutes) - Optional but recommended

### For Future Iterations
1. Add JSDoc comments to scene components
2. Apply memoization to particle system
3. Consider extracting ParticleSystem to reusable component

---

## Testing Checklist

Completed validation:
- [x] Visual inspection of all scenes
- [x] Frame-by-frame timing verification
- [x] Color palette comparison
- [x] Audio synchronization test
- [x] Asset loading verification
- [x] Render performance profiling
- [x] Code pattern review
- [x] Best practices compliance

---

## Next Steps

1. **Address HIGH priority issue:** Fix Scene 3 background color
2. **Optional:** Optimize product.png asset
3. **Final render:** Generate production video
4. **Performance check:** Run `/remotion-performance-optimizer` if render times increase
5. **Archive:** Save REVIEW_REPORT.md with project files

---

## Approval

**Status:** ✅ APPROVED WITH MINOR REVISIONS

This implementation is production-ready after addressing the Scene 3 color mismatch. All critical functionality, timing, and structure are correct. Medium and low priority items are optional improvements that can be addressed in future iterations.

**Signed:** remotion-video-reviewer
**Date:** 2026-01-23
```

**This document provides:**
- Executive summary with quick approval status
- Quantified compliance scores (95%, 98%, etc.)
- Prioritized issues (CRITICAL, HIGH, MEDIUM, LOW)
- Specific code locations and fixes
- Detailed analysis per category
- Testing verification checklist
- Clear next steps
- Official approval status

**Feeds into:**
- Developer: Fix identified issues
- `/remotion-performance-optimizer` if performance issues found
- Final production render after approval

## Review Process

### 1. Spec Comparison

Compare implementation against motion design spec:

**Check:**
- [ ] All scenes from spec are implemented
- [ ] Scene durations match spec timing
- [ ] Color palette matches hex codes exactly
- [ ] Typography (font, size, weight) matches
- [ ] Animation descriptions are accurately translated
- [ ] Audio placement matches timing
- [ ] Spring configurations match spec

### 2. Code Quality Review

Evaluate code structure and patterns:

**Check:**
- [ ] Constants extracted (colors, springs, timing)
- [ ] Scene components follow naming convention
- [ ] AbsoluteFill used for all scenes
- [ ] Progress variables extracted (not inline calculations)
- [ ] useVideoConfig used for responsive positioning
- [ ] TypeScript types defined
- [ ] Proper imports from remotion

### 3. Timing Accuracy

Verify frame calculations:

**Check:**
- [ ] Seconds correctly converted to frames (seconds * fps)
- [ ] Scene timing constants are accurate
- [ ] Delay calculations use frame offsets
- [ ] Transitions account for overlap
- [ ] Total duration matches spec
- [ ] Animation hold times are correct

### 4. Animation Review

Assess animation implementation:

**Check:**
- [ ] Spring configs match spec descriptions
- [ ] Interpolate ranges match spec values
- [ ] Easing functions appropriate for motion type
- [ ] Stagger delays calculated correctly
- [ ] Continuous animations use appropriate patterns
- [ ] Exit animations present where specified

### 5. Visual Fidelity

Confirm visual accuracy:

**Check:**
- [ ] Background colors match spec
- [ ] Element colors use COLORS constants
- [ ] Font sizes match spec exactly
- [ ] Positioning follows spec layout
- [ ] Visual hierarchy maintained
- [ ] Layer organization (background/midground/foreground)

### 6. Asset Quality

Validate asset preparation:

**Check:**
- [ ] All required assets present
- [ ] Assets use staticFile() import
- [ ] Image formats appropriate (PNG for transparency, JPEG for photos)
- [ ] Audio files in supported formats
- [ ] Asset dimensions suitable for composition
- [ ] Fonts loaded correctly

### 7. Performance Check

Identify performance issues:

**Check:**
- [ ] No expensive calculations in render
- [ ] Progress variables reused
- [ ] No unnecessary spring recalculations
- [ ] Memoization used where appropriate
- [ ] Large assets optimized
- [ ] No memory leaks in loops

## Review Output Format

### Summary

```markdown
## Review Summary

**Spec Compliance**: 95% (1 minor deviation)
**Code Quality**: Excellent
**Timing Accuracy**: 100%
**Visual Fidelity**: 98% (color mismatch in Scene 3)
**Asset Quality**: Good (1 optimization needed)
**Performance**: Excellent

**Overall Rating**: READY FOR PRODUCTION (with minor revisions)
```

### Issues List (Prioritized)

```markdown
## Issues Found

### CRITICAL (Must Fix)
None

### HIGH (Should Fix)
1. **Scene 3 background color mismatch**
   - Spec: #0A0A0A
   - Code: #0B0B0B
   - Impact: Visual inconsistency
   - Fix: Update COLORS.background

### MEDIUM (Consider Fixing)
1. **Product image could be optimized**
   - Current: 4000x3000 PNG
   - Recommendation: 1920x1440 JPEG
   - Impact: Faster render times
   - Fix: Resize and convert asset

### LOW (Nice to Have)
1. **Add memoization to particle system**
   - Impact: Negligible performance gain
   - Fix: Wrap in useMemo
```

### Recommendations

```markdown
## Recommendations

### Code Organization
- Extract ParticleSystem to reusable component
- Consider splitting Scene6 (currently 150 lines)

### Performance
- Preload audio files
- Consider lazy loading large assets

### Maintainability
- Add JSDoc comments to scene components
- Consider extracting animation helpers
```

## Common Issues to Check

### Timing Issues

**Issue:** Incorrect frame calculation
```typescript
// Wrong
const duration = 5; // Should be 150 frames, not 5

// Correct
const duration = 5 * fps; // 150 frames
```

**Issue:** Missing delay
```typescript
// Wrong - all elements appear at once
const progress = spring({ frame, fps, config: SMOOTH_SPRING });

// Correct - staggered with delays
const progress = spring({
  frame: frame - (index * STAGGER_DELAY),
  fps,
  config: SMOOTH_SPRING
});
```

### Animation Issues

**Issue:** Inline spring config instead of constant
```typescript
// Wrong
const progress = spring({
  frame,
  fps,
  config: { damping: 200 },
});

// Correct
const progress = spring({
  frame,
  fps,
  config: SPRING_CONFIGS.smooth,
});
```

**Issue:** Repeated calculations
```typescript
// Wrong
<div style={{
  opacity: spring({ frame, fps, config: SMOOTH }),
  transform: `scale(${spring({ frame, fps, config: SMOOTH })})`,
}} />

// Correct
const progress = spring({ frame, fps, config: SMOOTH });
<div style={{
  opacity: progress,
  transform: `scale(${progress})`,
}} />
```

### Visual Issues

**Issue:** Hardcoded colors
```typescript
// Wrong
backgroundColor: '#FF6B35'

// Correct
backgroundColor: COLORS.primary
```

**Issue:** Pixel values instead of responsive
```typescript
// Wrong
left: 960,  // Hardcoded center

// Correct
left: width / 2,  // Responsive center
```

### Asset Issues

**Issue:** Direct import instead of staticFile
```typescript
// Wrong
import logo from './logo.png';

// Correct
import { staticFile } from 'remotion';
const logoSrc = staticFile('logo.png');
```

### Performance Issues

**Issue:** Expensive operation in render
```typescript
// Wrong - recalculated every frame
const particles = Array.from({ length: 1000 }, (_, i) => ({
  x: Math.random() * width,
  y: Math.random() * height,
}));

// Correct - calculate once
const particles = useMemo(
  () => Array.from({ length: 1000 }, (_, i) => ({
    x: seededRandom(i * 123) * width,
    y: seededRandom(i * 456) * height,
  })),
  [width, height]
);
```

## Review Checklist

Complete review checklist:

### Spec Compliance
- [ ] All scenes implemented
- [ ] Timing matches spec
- [ ] Colors match exactly
- [ ] Typography matches
- [ ] Animations match descriptions
- [ ] Audio matches spec

### Code Quality
- [ ] Constants properly extracted
- [ ] Naming conventions followed
- [ ] AbsoluteFill used correctly
- [ ] TypeScript types defined
- [ ] Clean, readable code

### Timing
- [ ] Frame calculations correct
- [ ] Delays calculated properly
- [ ] Total duration accurate
- [ ] Transitions timed correctly

### Visuals
- [ ] Colors use constants
- [ ] Responsive positioning
- [ ] Visual hierarchy clear
- [ ] Layer organization logical

### Assets
- [ ] All assets present
- [ ] staticFile used
- [ ] Formats appropriate
- [ ] Quality sufficient

### Performance
- [ ] No expensive render calculations
- [ ] Progress variables reused
- [ ] Assets optimized
- [ ] Memoization where needed

## Integration with Other Skills

**Works with:**
- `/remotion-spec-translator` — Reviews translated code
- `/remotion-best-practices` — Ensures patterns are followed
- `/motion-designer` — Compares against original spec
- `/remotion-performance-optimizer` — Deep performance analysis

## Rules Directory

For detailed review criteria:

- [rules/spec-compliance.md](rules/spec-compliance.md) — Verifying spec accuracy
- [rules/timing-review.md](rules/timing-review.md) — Frame timing validation
- [rules/animation-quality.md](rules/animation-quality.md) — Animation assessment
- [rules/visual-accuracy.md](rules/visual-accuracy.md) — Visual fidelity checks
- [rules/asset-validation.md](rules/asset-validation.md) — Asset quality review
- [rules/performance-audit.md](rules/performance-audit.md) — Performance checking
- [rules/code-patterns.md](rules/code-patterns.md) — Code quality standards

---

This skill ensures Remotion implementations are production-ready, spec-compliant, and follow best practices before deployment.
