---
name: create-video-start
description: Master orchestrator that chains all Remotion video creation skills together in a single automated pipeline. Takes a creative brief and produces a complete, production-ready Remotion video project. Use when starting a new video from scratch, when asked to "create a video", "make a video", "build a complete video", or "video from idea to code".
argument-hint: <creative-brief>
---

# Create Video Start

Master orchestrator skill that chains the entire Remotion video pipeline together. Takes a single creative brief and automatically invokes each specialized skill in sequence, passing outputs between them.

## What This Skill Does

Orchestrates the complete video creation pipeline:

1. **motion-designer** → Creates VIDEO_SPEC.md from creative brief
2. **remotion-scaffold** → Sets up project structure
3. **remotion-animation** → Generates animation configurations
4. **remotion-composition** → Creates Sequence layout
5. **remotion-component-gen** → Generates each scene component
6. **remotion-render-config** → Configures output settings
7. **remotion-asset-coordinator** → Prepares asset manifest

## Pipeline Execution

When invoked, execute this pipeline in order:

### Step 0: Setup

Create a working directory for pipeline artifacts:

```bash
# Create pipeline working directory
PIPELINE_DIR=".remotion-pipeline/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$PIPELINE_DIR"
echo "Pipeline artifacts: $PIPELINE_DIR"
```

### Step 1: Motion Designer → VIDEO_SPEC.md

Generate the motion design specification from the creative brief:

```bash
# Invoke motion-designer skill
claude -p "You are using the /motion-designer skill.

Create a detailed VIDEO_SPEC.md for this creative brief:

$CREATIVE_BRIEF

Output a complete motion design specification with:
- Overview (duration, fps, dimensions)
- Color palette with hex codes
- Scene-by-scene breakdown with timing
- Animation details for each element
- Audio specifications

Write the spec to: $PIPELINE_DIR/VIDEO_SPEC.md" \
  --allowedTools "Read,Write,Edit,Bash"
```

**Checkpoint:** Verify VIDEO_SPEC.md exists and contains all required sections.

### Step 2: Remotion Scaffold → SCAFFOLD_MANIFEST.md

Create project folder structure:

```bash
# Invoke remotion-scaffold skill
claude -p "You are using the /remotion-scaffold skill.

Based on this VIDEO_SPEC.md:
$(cat $PIPELINE_DIR/VIDEO_SPEC.md)

Create the Remotion project scaffold:
1. Create folder structure for the composition
2. Create empty template files
3. Setup asset directories
4. Register composition in Root.tsx

Write manifest to: $PIPELINE_DIR/SCAFFOLD_MANIFEST.md
Write actual files to the project." \
  --allowedTools "Read,Write,Edit,Bash,Glob"
```

**Checkpoint:** Verify scaffold directories and files exist.

### Step 3: Remotion Animation → ANIMATION_CONFIG.md

Generate animation configurations:

```bash
# Invoke remotion-animation skill
claude -p "You are using the /remotion-animation skill.

Based on this VIDEO_SPEC.md:
$(cat $PIPELINE_DIR/VIDEO_SPEC.md)

Generate animation configurations:
1. Spring configs for each animation type
2. Interpolation mappings
3. Timing constants
4. Stagger delay patterns

Write to: $PIPELINE_DIR/ANIMATION_CONFIG.md

Output TypeScript constants that can be copied to constants.ts" \
  --allowedTools "Read,Write,Edit"
```

**Checkpoint:** Verify ANIMATION_CONFIG.md contains spring configs and timing.

### Step 4: Remotion Composition → COMPOSITION_STRUCTURE.md

Generate Sequence layout:

```bash
# Invoke remotion-composition skill
claude -p "You are using the /remotion-composition skill.

Based on this VIDEO_SPEC.md:
$(cat $PIPELINE_DIR/VIDEO_SPEC.md)

Generate composition structure:
1. Sequence ordering for all scenes
2. Transition timing between scenes
3. Duration calculations
4. Scene timing constants

Write to: $PIPELINE_DIR/COMPOSITION_STRUCTURE.md

Output the main composition JSX structure." \
  --allowedTools "Read,Write,Edit"
```

**Checkpoint:** Verify COMPOSITION_STRUCTURE.md contains Sequence layout.

### Step 5: Remotion Component Gen → SCENE_COMPONENT.md (per scene)

Generate each scene component:

```bash
# For each scene in the spec, invoke remotion-component-gen
for SCENE_NUM in $(seq 1 $TOTAL_SCENES); do
  claude -p "You are using the /remotion-component-gen skill.

Based on Scene $SCENE_NUM from this VIDEO_SPEC.md:
$(cat $PIPELINE_DIR/VIDEO_SPEC.md)

And these animation configs:
$(cat $PIPELINE_DIR/ANIMATION_CONFIG.md)

Generate the complete Scene${SCENE_NUM} component:
1. Full TSX implementation
2. Animation logic using the configs
3. Proper imports and types
4. AbsoluteFill wrapper

Write to: $PIPELINE_DIR/SCENE_${SCENE_NUM}_COMPONENT.md
Also write the actual .tsx file to the scenes/ folder." \
    --allowedTools "Read,Write,Edit,Glob"
done
```

**Checkpoint:** Verify all scene components are generated.

### Step 6: Remotion Render Config → RENDER_CONFIG.md

Generate render settings:

```bash
# Invoke remotion-render-config skill
claude -p "You are using the /remotion-render-config skill.

Based on this VIDEO_SPEC.md:
$(cat $PIPELINE_DIR/VIDEO_SPEC.md)

Generate render configuration:
1. Output format and codec settings
2. Quality settings
3. Resolution confirmation
4. Render command examples

Write to: $PIPELINE_DIR/RENDER_CONFIG.md" \
  --allowedTools "Read,Write,Edit"
```

### Step 7: Remotion Asset Coordinator → ASSET_MANIFEST.md

Generate asset preparation guide:

```bash
# Invoke remotion-asset-coordinator skill
claude -p "You are using the /remotion-asset-coordinator skill.

Based on this VIDEO_SPEC.md:
$(cat $PIPELINE_DIR/VIDEO_SPEC.md)

And this SCAFFOLD_MANIFEST.md:
$(cat $PIPELINE_DIR/SCAFFOLD_MANIFEST.md)

Generate asset manifest:
1. List all required assets
2. Recommend sources for each
3. Provide preparation instructions
4. Generate import code snippets

Write to: $PIPELINE_DIR/ASSET_MANIFEST.md" \
  --allowedTools "Read,Write,Edit,WebSearch"
```

### Step 8: Assemble Final Output

Combine all outputs into final summary:

```bash
# Create final summary
claude -p "Create a PIPELINE_COMPLETE.md summary that:

1. Lists all generated files
2. Provides next steps for the developer
3. Includes quick-start commands
4. Notes any TODOs that need manual attention

Pipeline artifacts:
- VIDEO_SPEC.md: $(cat $PIPELINE_DIR/VIDEO_SPEC.md | head -20)
- SCAFFOLD_MANIFEST.md: $(cat $PIPELINE_DIR/SCAFFOLD_MANIFEST.md | head -20)
- ANIMATION_CONFIG.md: $(cat $PIPELINE_DIR/ANIMATION_CONFIG.md | head -20)
- COMPOSITION_STRUCTURE.md: $(cat $PIPELINE_DIR/COMPOSITION_STRUCTURE.md | head -20)
- Scene components: $(ls $PIPELINE_DIR/SCENE_*_COMPONENT.md)
- RENDER_CONFIG.md: $(cat $PIPELINE_DIR/RENDER_CONFIG.md | head -20)
- ASSET_MANIFEST.md: $(cat $PIPELINE_DIR/ASSET_MANIFEST.md | head -20)

Write to: $PIPELINE_DIR/PIPELINE_COMPLETE.md" \
  --allowedTools "Read,Write,Edit,Glob"
```

## Input Format

### Creative Brief (Natural Language)

```
Create a 30-second product demo video for Vello, an AI task management app.
Show the main features: smart scheduling, team collaboration, and AI suggestions.
Use modern, clean aesthetic with the brand colors (orange #FF6B35, dark background).
Include upbeat background music and subtle sound effects for transitions.
Target platform: YouTube and Twitter.
```

### Structured Brief

```markdown
## Video Brief

**Product:** Vello - AI Task Management
**Duration:** 30 seconds
**Style:** Modern, clean, tech-forward
**Brand Colors:**
  - Primary: #FF6B35 (Orange)
  - Background: #0A0A0A (Dark)
  - Accent: #4ECDC4 (Teal)

**Key Messages:**
1. Smart AI scheduling
2. Team collaboration
3. Instant AI suggestions

**Scenes:**
1. Logo intro (5s)
2. Feature showcase (15s)
3. Social proof (5s)
4. CTA (5s)

**Audio:**
- Background: Upbeat electronic
- SFX: Subtle whooshes, clicks

**Target Platforms:** YouTube, Twitter
```

## Output Format

### PIPELINE_COMPLETE.md

```markdown
# Pipeline Complete: [Video Name]

## Execution Summary

| Step | Skill | Output | Status |
|------|-------|--------|--------|
| 1 | motion-designer | VIDEO_SPEC.md | ✅ |
| 2 | remotion-scaffold | SCAFFOLD_MANIFEST.md | ✅ |
| 3 | remotion-animation | ANIMATION_CONFIG.md | ✅ |
| 4 | remotion-composition | COMPOSITION_STRUCTURE.md | ✅ |
| 5 | remotion-component-gen | SCENE_*_COMPONENT.md | ✅ |
| 6 | remotion-render-config | RENDER_CONFIG.md | ✅ |
| 7 | remotion-asset-coordinator | ASSET_MANIFEST.md | ✅ |

## Generated Files

### Pipeline Artifacts
```
.remotion-pipeline/20240123_143052/
├── VIDEO_SPEC.md
├── SCAFFOLD_MANIFEST.md
├── ANIMATION_CONFIG.md
├── COMPOSITION_STRUCTURE.md
├── SCENE_1_COMPONENT.md
├── SCENE_2_COMPONENT.md
├── SCENE_3_COMPONENT.md
├── SCENE_4_COMPONENT.md
├── RENDER_CONFIG.md
├── ASSET_MANIFEST.md
└── PIPELINE_COMPLETE.md
```

### Project Files Created
```
src/remotion/compositions/VideoName/
├── index.tsx           ✅ Main composition
├── constants.ts        ✅ Colors, springs, timing
├── types.ts            ✅ TypeScript interfaces
└── scenes/
    ├── Scene1Intro.tsx     ✅ Implemented
    ├── Scene2Features.tsx  ✅ Implemented
    ├── Scene3Proof.tsx     ✅ Implemented
    └── Scene4CTA.tsx       ✅ Implemented

public/
├── images/             📁 Ready for assets
├── audio/
│   ├── music/          📁 Ready for music
│   └── sfx/            📁 Ready for sound effects
└── fonts/              📁 Ready for fonts
```

## Quick Start

```bash
# Preview the video
npm run dev

# Open Remotion Studio
# Navigate to http://localhost:3000

# Render final video
npx remotion render src/index.tsx VideoName output.mp4
```

## Next Steps

### Required Actions
1. [ ] Add background music to `public/audio/music/`
2. [ ] Add sound effects to `public/audio/sfx/`
3. [ ] Add product images to `public/images/`
4. [ ] Review and customize colors in `constants.ts`

### Optional Enhancements
- Run `/remotion-video-reviewer` for QA check
- Run `/remotion-performance-optimizer` for render optimization

## Render Commands

From RENDER_CONFIG.md:

```bash
# YouTube (1080p, high quality)
npx remotion render src/index.tsx VideoName youtube-output.mp4 \
  --codec h264 --crf 18

# Twitter (optimized file size)
npx remotion render src/index.tsx VideoName twitter-output.mp4 \
  --codec h264 --crf 23

# Preview frames
npx remotion still src/index.tsx VideoName preview.png --frame=150
```

## Pipeline Timing

- Total execution time: ~3-5 minutes
- Motion design: ~45s
- Scaffold: ~15s
- Animation config: ~20s
- Composition: ~15s
- Scene components: ~30s per scene
- Render config: ~10s
- Asset manifest: ~20s
```

## Execution Instructions

When this skill is invoked:

1. **Parse the creative brief** from the user's input
2. **Create pipeline directory** with timestamp
3. **Execute each step sequentially** using `claude -p` for skill invocation
4. **Validate output** after each step before proceeding
5. **Handle errors gracefully** - if a step fails, report and offer to retry
6. **Assemble final summary** with all artifacts and next steps

### Error Handling

If any step fails:

```bash
# Retry pattern
MAX_RETRIES=2
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  # Attempt skill invocation
  if claude -p "..." --allowedTools "..."; then
    break
  fi
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "Retry $RETRY_COUNT of $MAX_RETRIES"
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "Step failed after $MAX_RETRIES retries"
  # Log error and continue with partial output
fi
```

## Integration Notes

This skill coordinates these sub-skills:

| Skill | Invocation | Output |
|-------|------------|--------|
| `/motion-designer` | `claude -p "..."` | VIDEO_SPEC.md |
| `/remotion-scaffold` | `claude -p "..."` | SCAFFOLD_MANIFEST.md + files |
| `/remotion-animation` | `claude -p "..."` | ANIMATION_CONFIG.md |
| `/remotion-composition` | `claude -p "..."` | COMPOSITION_STRUCTURE.md |
| `/remotion-component-gen` | `claude -p "..."` (×N) | SCENE_*_COMPONENT.md + files |
| `/remotion-render-config` | `claude -p "..."` | RENDER_CONFIG.md |
| `/remotion-asset-coordinator` | `claude -p "..."` | ASSET_MANIFEST.md |

Each `claude -p` invocation includes:
- The skill context/instructions
- Relevant output from previous steps
- Specific output file path
- Allowed tools for that step

## Example Usage

```bash
# Invoke with natural language brief
/create-video-start Create a 30-second demo video for our AI task app Vello

# Invoke with detailed brief
/create-video-start <<EOF
Product: Vello AI Task Manager
Duration: 45 seconds
Style: Modern tech, dark theme
Scenes: Intro, Features (3), Testimonial, CTA
Brand: Orange #FF6B35, Dark #0A0A0A
Target: YouTube, LinkedIn
EOF
```

## Skill Dependencies

Requires these skills to be installed:

- `/motion-designer` - Video specification creation
- `/remotion-scaffold` - Project structure setup
- `/remotion-animation` - Animation configuration
- `/remotion-composition` - Sequence layout
- `/remotion-component-gen` - Scene component generation
- `/remotion-render-config` - Render settings
- `/remotion-asset-coordinator` - Asset preparation

---

This orchestrator eliminates the manual handoff between skills, creating a complete video project from a single creative brief.
