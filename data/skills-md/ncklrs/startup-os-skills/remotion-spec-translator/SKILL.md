---
name: remotion-spec-translator
description: Orchestrates translation of motion designer video specifications into working Remotion code by coordinating specialized agents. Acts as pipeline coordinator that delegates to remotion-scaffold, remotion-animation, remotion-composition, and remotion-component-gen. Use when you have a complete VIDEO_SPEC.md and need full Remotion implementation.
---

# Remotion Spec Translator

Orchestrates the complete translation pipeline from motion design specifications to working Remotion code. This skill acts as a coordinator that delegates work to specialized skills for each aspect of the translation.

## What This Skill Does

Orchestrates the translation by:

1. **Coordinating pipeline** — Calls specialized skills in correct order
2. **Parsing specs** — Extracts requirements for each skill
3. **Managing handoffs** — Ensures output from one skill feeds into next
4. **Validating completeness** — Confirms all scenes implemented
5. **Documenting workflow** — Tracks pipeline progress

## Scope Boundaries

**IN SCOPE:**
- Pipeline orchestration and coordination
- Spec parsing and requirement extraction
- Skill delegation and sequencing
- Progress tracking and validation
- Workflow documentation

**OUT OF SCOPE:**
- Direct code generation (delegated to specialist skills)
- Implementation details (handled by component/animation skills)
- Manual file creation (handled by scaffold skill)

## Input/Output Formats

### Input Format: VIDEO_SPEC.md

Expects complete motion design specification (from `/motion-designer`):

```markdown
# Video Title: ProductDemo

## Overview
- Duration: 30 seconds
- Frame Rate: 30 fps
- Aspect Ratio: 16:9 (1920x1080)
- Total Scenes: 4

## Color Palette
Primary: #FF6B35 - Ember Orange
Secondary: #4ECDC4 - Teal
Background: #0A0A0A - Black
Text: #FFFFFF - White

## Scene 1: Intro (0s - 5s)
Visual Description: Centered logo with smooth entrance
Animation Details:
- Logo: Scale 0.8 → 1.0, Spring (damping: 200)
- Subtitle: Fade in with upward slide

## Scene 2: Features (5s - 15s)
Visual Description: Three feature cards stagger in
Animation Details:
- Cards: Stagger delay 10 frames, slide from left

## Scene 3: Demo (15s - 25s)
Visual Description: Product screenshot with highlights
Animation Details:
- Screenshot: Fade in, scale 0.95 → 1.0
- Highlights: Sequential pulse effect

## Scene 4: CTA (25s - 30s)
Visual Description: Call-to-action with button
Animation Details:
- Text: Fade in
- Button: Scale bounce effect

## Assets
- Logo: public/images/logo.svg (400x400)
- Product screenshot: public/images/product.png (1200x800)
```

### Output Format: TRANSLATION_COMPLETE.md

Generates orchestration summary document:

```markdown
# Translation Complete: ProductDemo

## Status
✅ Pipeline execution complete
✅ All scenes implemented
⏳ Ready for render

## Pipeline Execution Summary

### Step 1: Scaffold Generation (/remotion-scaffold)
✅ Complete
- Created: Project structure
- Output: SCAFFOLD_MANIFEST.md
- Files: index.tsx, constants.ts, types.ts, 4 scene templates

### Step 2: Animation Configuration (/remotion-animation)
✅ Complete
- Created: Animation parameters
- Output: ANIMATION_CONFIG.md
- Configs: Spring settings, interpolations, timing

### Step 3: Composition Structure (/remotion-composition)
✅ Complete
- Created: Sequence layout
- Output: COMPOSITION_STRUCTURE.md
- Timing: All scene durations calculated

### Step 4: Scene Implementation (/remotion-component-gen)
✅ Complete - 4/4 scenes
- Scene 1 (Intro): SCENE_COMPONENT.md → Scene1Intro.tsx
- Scene 2 (Features): SCENE_COMPONENT.md → Scene2Features.tsx
- Scene 3 (Demo): SCENE_COMPONENT.md → Scene3Demo.tsx
- Scene 4 (CTA): SCENE_COMPONENT.md → Scene4CTA.tsx

### Step 5: Render Configuration (/remotion-render-config)
✅ Complete
- Created: Render settings
- Output: RENDER_CONFIG.md
- Target: YouTube (H.264, CRF 18)

## Generated Files

```
src/remotion/compositions/ProductDemo/
├── index.tsx                  # ✅ Composition with all scenes
├── constants.ts               # ✅ Colors, springs, timing
├── types.ts                   # ✅ TypeScript interfaces
└── scenes/
    ├── Scene1Intro.tsx        # ✅ Implemented
    ├── Scene2Features.tsx     # ✅ Implemented
    ├── Scene3Demo.tsx         # ✅ Implemented
    └── Scene4CTA.tsx          # ✅ Implemented
```

## Next Steps

1. **Add assets** to public/ folders
   - Logo: public/images/logo.svg
   - Product screenshot: public/images/product.png

2. **Test in preview**
   ```bash
   npm run dev
   ```

3. **Verify timing** matches spec exactly

4. **Run render** when ready
   ```bash
   npm run render:youtube
   ```

5. **Review and iterate** if adjustments needed

## Asset Checklist

Required assets from spec:
- [ ] public/images/logo.svg (400x400)
- [ ] public/images/product.png (1200x800)

Use `/remotion-asset-coordinator` for asset sourcing guidance.

## Quality Checklist

- [x] All scenes implemented
- [x] Timing matches spec
- [x] Animations configured
- [x] Colors from palette applied
- [x] Composition structure complete
- [ ] Assets added
- [ ] Preview tested
- [ ] Final render complete

## Translation Summary

**Input:** VIDEO_SPEC.md (motion design specification)
**Pipeline:** 5 specialized skills executed in sequence
**Output:** Complete, working Remotion composition
**Status:** Implementation complete, assets and testing pending
```

## Orchestration Workflow

The pipeline executes in this sequence:

```
VIDEO_SPEC.md (Input)
    ↓
Step 1: /remotion-scaffold
    ↓ outputs: SCAFFOLD_MANIFEST.md + folder structure
Step 2: /remotion-animation
    ↓ outputs: ANIMATION_CONFIG.md + animation constants
Step 3: /remotion-composition
    ↓ outputs: COMPOSITION_STRUCTURE.md + Sequence layout
Step 4: /remotion-component-gen (per scene)
    ↓ outputs: SCENE_COMPONENT.md × N scenes
Step 5: /remotion-render-config
    ↓ outputs: RENDER_CONFIG.md + render commands
    ↓
TRANSLATION_COMPLETE.md (Output)
```

## Skill Delegation Strategy

### When to Delegate

1. **Parse spec** → Extract requirements for each skill
2. **Check dependencies** → Ensure prerequisites met
3. **Call skill** → Provide focused input
4. **Capture output** → Store for next skill
5. **Validate** → Confirm output quality
6. **Proceed** → Move to next step

### Delegation Examples

```typescript
// Step 1: Scaffold
const scaffoldInput = {
  projectName: "ProductDemo",
  duration: 30,
  fps: 30,
  dimensions: "1920x1080",
  scenes: ["Intro", "Features", "Demo", "CTA"]
};
// Call: /remotion-scaffold

// Step 2: Animation
const animationInput = {
  springConfigs: extractSpringConfigs(spec),
  interpolations: extractInterpolations(spec),
  timing: extractAnimationTiming(spec)
};
// Call: /remotion-animation

// Step 3: Composition
const compositionInput = {
  scenes: [
    { name: "intro", durationSeconds: 5 },
    { name: "features", durationSeconds: 10 },
    { name: "demo", durationSeconds: 10 },
    { name: "cta", durationSeconds: 5 }
  ],
  fps: 30
};
// Call: /remotion-composition

// Step 4: Component Gen (per scene)
for (const scene of spec.scenes) {
  const componentInput = {
    sceneName: scene.name,
    visualDescription: scene.visual,
    animationDetails: scene.animation,
    assets: scene.assets
  };
  // Call: /remotion-component-gen
}

// Step 5: Render Config
const renderInput = {
  platform: "YouTube",
  quality: "high",
  format: "MP4"
};
// Call: /remotion-render-config
```

## Spec Parsing Helpers

### Extract Spring Configs

```typescript
function extractSpringConfigs(spec: string) {
  // Parse animation details for spring parameters
  // Look for: damping, stiffness, mass values
  // Return: SPRING_CONFIGS object
}
```

### Extract Scene Timing

```typescript
function extractSceneTiming(spec: string) {
  // Parse scene headers for timing (0s - 5s)
  // Calculate frame numbers
  // Return: Scene timing array
}
```

### Extract Color Palette

```typescript
function extractColorPalette(spec: string) {
  // Parse Color Palette section
  // Extract hex codes and names
  // Return: COLORS object
}
```

### Extract Asset List

```typescript
function extractAssets(spec: string) {
  // Parse Assets sections per scene
  // Collect all required assets
  // Return: Asset checklist
}
```

## Progress Tracking

The orchestrator tracks pipeline progress:

```
Pipeline Progress: ProductDemo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Step 1/5: Scaffold (remotion-scaffold)
✅ Step 2/5: Animation (remotion-animation)
✅ Step 3/5: Composition (remotion-composition)
⏳ Step 4/5: Scenes (remotion-component-gen) - 2/4 complete
⬜ Step 5/5: Render Config (remotion-render-config)

Current: Implementing Scene 3 (Demo)
Next: Scene 4 (CTA)
```

## Error Handling

### Missing Information

If spec lacks required information:
- **Identify gap** (e.g., missing spring config)
- **Use sensible defaults** where possible
- **Document assumption** in output
- **Flag for review** by user

### Skill Failures

If a delegated skill fails:
- **Log error** with context
- **Attempt recovery** if possible
- **Skip to next step** if non-blocking
- **Report issue** in final summary

### Incomplete Specs

If spec is incomplete:
- **Parse what's available**
- **Generate with TODO markers**
- **List missing requirements**
- **Suggest spec improvements**

## Validation Checklist

Before marking translation complete:

- [ ] All scenes from spec have components
- [ ] Animation configs match spec parameters
- [ ] Scene timing adds up to total duration
- [ ] Color palette extracted and applied
- [ ] Asset list generated
- [ ] Render config targets correct platform
- [ ] No TODO markers in critical sections

## Best Practices

1. **Parse thoroughly** — Extract all details from spec
2. **Delegate appropriately** — Use right skill for each task
3. **Maintain context** — Pass relevant info between skills
4. **Validate outputs** — Check each skill's result
5. **Document clearly** — Explain what was done
6. **Track progress** — Show pipeline status
7. **Handle errors** — Gracefully manage failures

## Integration with Other Skills

This skill orchestrates the pipeline:

```
remotion-spec-translator (this skill - ORCHESTRATOR)
    ↓ coordinates
remotion-scaffold → remotion-animation → remotion-composition → remotion-component-gen → remotion-render-config
```

**Works with:**
- `/motion-designer` — Consumes VIDEO_SPEC.md from this skill
- `/remotion-scaffold` — Delegates scaffolding
- `/remotion-animation` — Delegates animation config
- `/remotion-composition` — Delegates composition structure
- `/remotion-component-gen` — Delegates scene implementation (per scene)
- `/remotion-render-config` — Delegates render settings

**Triggers:**
- "Translate spec to code"
- "Implement video spec"
- "Generate Remotion from spec"
- "Build Remotion project from design"

---

This skill ensures motion design specs translate systematically into complete, working Remotion projects through intelligent orchestration and delegation.
