---
name: remotion-render-config
description: Generates render and output configuration for Remotion videos. Focuses ONLY on output settings, codec, format, quality, resolution. Input is target platform/quality requirements. Output is RENDER_CONFIG.md with Remotion render settings.
---

# Remotion Render Config

Generates render configuration documents that define video output settings, codec parameters, format options, and quality settings for Remotion video renders. This skill focuses exclusively on render/export configuration.

## What This Skill Does

Generates render configurations for:

1. **Output format** — MP4, WebM, ProRes, etc.
2. **Codec settings** — H.264, H.265, VP9 parameters
3. **Quality settings** — CRF, bitrate, compression level
4. **Resolution** — Output dimensions and scaling
5. **Platform optimization** — YouTube, Twitter, Instagram presets

## Scope Boundaries

**IN SCOPE:**
- Render command configuration
- Codec and format selection
- Quality and compression settings
- Platform-specific optimizations
- Output file parameters

**OUT OF SCOPE:**
- Composition implementation (use `/remotion-composition`)
- Scene logic (use `/remotion-component-gen`)
- Animation parameters (use `/remotion-animation`)
- Asset management (use `/remotion-asset-coordinator`)

## Input/Output Formats

### Input Format: Target Platform/Quality Requirements

Accepts render target specifications:

**Natural Language:**
```
Render for YouTube at high quality with H.264 codec
```

**Structured Format:**
```markdown
## Render Requirements

**Target Platform:** YouTube
**Quality Level:** High
**Format:** MP4 (H.264)
**Resolution:** 1920x1080
**Frame Rate:** 30 fps
**Additional:** Upload-ready, optimized file size
```

### Output Format: RENDER_CONFIG.md

Generates complete render configuration document:

```markdown
# Render Configuration: ProductDemo

## Status
✅ Render settings defined
⏳ Ready for video render

## Render Command

```bash
npx remotion render \
  src/index.tsx \
  ProductDemo \
  output.mp4 \
  --codec=h264 \
  --crf=18 \
  --pixel-format=yuv420p \
  --audio-codec=aac \
  --audio-bitrate=320k
```

## Configuration Details

### Output Format
- **Container:** MP4
- **Video Codec:** H.264 (x264)
- **Audio Codec:** AAC
- **Pixel Format:** yuv420p (for maximum compatibility)

### Quality Settings
- **CRF:** 18 (high quality, ~15-20 MB/min)
- **Audio Bitrate:** 320 kbps (high quality)
- **Preset:** medium (balanced speed/quality)

### Resolution
- **Output:** 1920x1080 (16:9)
- **Frame Rate:** 30 fps
- **Duration:** 30 seconds (900 frames)

## Platform: YouTube

Optimized for YouTube upload:
- ✅ H.264 codec (widely supported)
- ✅ yuv420p pixel format (required)
- ✅ AAC audio (recommended)
- ✅ CRF 18 (high quality, good file size)
- ✅ Metadata compatible

**Estimated File Size:** ~45-60 MB

## Alternative Render Options

### Web Delivery (Smaller File)
```bash
npx remotion render \
  src/index.tsx \
  ProductDemo \
  output.mp4 \
  --codec=h264 \
  --crf=23 \
  --audio-bitrate=192k
```
File size: ~25-35 MB

### Maximum Quality (Archive)
```bash
npx remotion render \
  src/index.tsx \
  ProductDemo \
  output.mp4 \
  --codec=h264 \
  --crf=15 \
  --audio-bitrate=320k \
  --preset=slower
```
File size: ~80-100 MB

### Fast Preview Render
```bash
npx remotion render \
  src/index.tsx \
  ProductDemo \
  preview.mp4 \
  --crf=28 \
  --preset=ultrafast
```
File size: ~15-20 MB

## Render Workflow

1. **Test render** (first 3 seconds):
   ```bash
   npx remotion render src/index.tsx ProductDemo test.mp4 --frames=0-90
   ```

2. **Full render** with progress:
   ```bash
   npx remotion render src/index.tsx ProductDemo output.mp4 --codec=h264 --crf=18
   ```

3. **Verify output**:
   - Check file size
   - Play in video player
   - Verify audio sync
   - Check quality

4. **Upload to platform** (YouTube, etc.)

## Next Steps

1. **Run test render** to verify timing and quality
2. **Adjust CRF** if file size too large/small
3. **Full render** when ready
4. **Upload to target platform**

## Troubleshooting

**File too large:**
- Increase CRF (23-28 for web)
- Lower audio bitrate (192k or 128k)

**Quality issues:**
- Decrease CRF (15-17 for higher quality)
- Use slower preset (slow, slower)

**Rendering slow:**
- Use faster preset (fast, veryfast)
- Reduce resolution temporarily for testing

## Checklist

- [x] Codec selected
- [x] Quality settings defined
- [x] Platform optimized
- [x] Render command generated
- [ ] Test render completed
- [ ] Full render completed
- [ ] Output verified
```

## Codec Reference

### H.264 (Most Compatible)

Best for: YouTube, web delivery, social media

```bash
--codec=h264
--crf=18          # Quality (lower = better, 15-28 typical)
--pixel-format=yuv420p
--audio-codec=aac
--audio-bitrate=320k
```

**Quality Levels:**
- CRF 15-17: Excellent (large files)
- CRF 18-20: High (recommended)
- CRF 21-23: Good (web delivery)
- CRF 24-28: Acceptable (preview/draft)

### H.265 (HEVC) - Better Compression

Best for: Modern platforms, smaller files, 4K video

```bash
--codec=h265
--crf=23
--pixel-format=yuv420p10le
```

**Note:** Not universally supported, but ~50% smaller files at same quality

### VP9 (Open Source)

Best for: WebM format, web delivery, Chrome/Firefox

```bash
--codec=vp9
--crf=30
--pixel-format=yuv420p
```

### ProRes (Professional)

Best for: Video editing, maximum quality, no compression

```bash
--codec=prores
--prores-profile=3  # HQ profile
```

**Warning:** Very large files (~1-2 GB/minute)

## Quality vs File Size Reference

For 30-second 1080p video at 30fps:

| CRF | Quality | File Size | Use Case |
|-----|---------|-----------|----------|
| 15 | Excellent | 80-100 MB | Archive, editing |
| 18 | High | 45-60 MB | YouTube, high quality |
| 21 | Good | 30-40 MB | Web, social media |
| 23 | Acceptable | 20-30 MB | Web delivery |
| 28 | Preview | 10-15 MB | Draft, testing |

## Platform-Specific Presets

### YouTube

```bash
npx remotion render src/index.tsx VideoName output.mp4 \
  --codec=h264 \
  --crf=18 \
  --pixel-format=yuv420p \
  --audio-codec=aac \
  --audio-bitrate=320k
```

**Specifications:**
- Resolution: 1920x1080 or higher
- Frame rate: 24, 25, 30, 48, 50, or 60 fps
- Codec: H.264 or H.265
- Audio: AAC-LC, 320 kbps

### Twitter/X

```bash
npx remotion render src/index.tsx VideoName output.mp4 \
  --codec=h264 \
  --crf=20 \
  --audio-bitrate=192k
```

**Specifications:**
- Max duration: 2:20 (140 seconds)
- Max file size: 512 MB
- Resolution: Up to 1920x1200 or 1200x1920

### Instagram Feed

```bash
npx remotion render src/index.tsx VideoName output.mp4 \
  --codec=h264 \
  --crf=20 \
  --audio-bitrate=192k
```

**Specifications:**
- Max duration: 60 seconds
- Resolution: 1080x1080 (1:1) or 1080x1350 (4:5)
- Frame rate: 30 fps
- Codec: H.264

### Instagram Reels/Stories

```bash
npx remotion render src/index.tsx VideoName output.mp4 \
  --codec=h264 \
  --crf=20 \
  --audio-bitrate=192k
```

**Specifications:**
- Resolution: 1080x1920 (9:16)
- Max duration: 90 seconds (Reels), 15 seconds (Stories)
- Frame rate: 30 fps

### TikTok

```bash
npx remotion render src/index.tsx VideoName output.mp4 \
  --codec=h264 \
  --crf=20 \
  --audio-bitrate=192k
```

**Specifications:**
- Resolution: 1080x1920 (9:16)
- Max duration: 10 minutes
- Max file size: 287.6 MB
- Frame rate: 30 or 60 fps

### LinkedIn

```bash
npx remotion render src/index.tsx VideoName output.mp4 \
  --codec=h264 \
  --crf=20 \
  --audio-bitrate=192k
```

**Specifications:**
- Max file size: 5 GB
- Resolution: 256x144 to 4096x2304
- Frame rate: 10-60 fps

## Advanced Render Options

### Concurrency (Faster Renders)

```bash
--concurrency=8  # Use 8 CPU cores
```

### Image Sequence (for Post-Processing)

```bash
--sequence
--image-format=png
```

Outputs PNG sequence for After Effects, Premiere, etc.

### Specific Frame Range

```bash
--frames=30-90  # Render frames 30-90 only
```

### Scale Output

```bash
--scale=0.5  # Render at 50% resolution (960x540)
```

Useful for quick previews.

### Overwrite Existing File

```bash
--overwrite
```

### Custom Output Name

```bash
npx remotion render src/index.tsx VideoName "output/final-video.mp4"
```

## Environment Variables

```bash
# Number of CPU cores to use
export REMOTION_CONCURRENCY=8

# Disable browser sandbox (Docker)
export REMOTION_DISABLE_CHROMIUM_SANDBOX=true

# Set custom Chromium path
export REMOTION_CHROMIUM_PATH=/path/to/chromium
```

## Render Configuration File

Create `remotion.config.ts`:

```typescript
import { Config } from "@remotion/cli/config";

Config.setCodec("h264");
Config.setCrf(18);
Config.setPixelFormat("yuv420p");
Config.setAudioBitrate("320k");
Config.setAudioCodec("aac");
Config.setConcurrency(8);
Config.setOverwriteOutput(true);
```

Then render with:
```bash
npx remotion render
```

## Render Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "render:preview": "remotion render src/index.tsx VideoName preview.mp4 --crf=28 --preset=ultrafast",
    "render:draft": "remotion render src/index.tsx VideoName draft.mp4 --crf=23",
    "render:final": "remotion render src/index.tsx VideoName output.mp4 --codec=h264 --crf=18",
    "render:youtube": "remotion render src/index.tsx VideoName youtube.mp4 --codec=h264 --crf=18 --audio-bitrate=320k"
  }
}
```

Usage:
```bash
npm run render:youtube
```

## Render Performance Tips

1. **Use concurrency** to utilize all CPU cores
2. **Close other applications** during render
3. **Use SSD** for faster file I/O
4. **Reduce composition complexity** if render is too slow
5. **Test render small ranges** before full render
6. **Use image-format prop** if you need transparency

## Quality Verification Checklist

After rendering:

- [ ] File plays without errors
- [ ] Audio is in sync with video
- [ ] Visual quality meets expectations
- [ ] File size is reasonable for platform
- [ ] No encoding artifacts visible
- [ ] Colors look correct
- [ ] Text is readable
- [ ] Animations are smooth

## Integration Workflow

1. **Complete composition** via other skills
2. **Generate render config** using this skill → RENDER_CONFIG.md
3. **Run test render** (first few seconds)
4. **Verify quality and timing**
5. **Run full render**
6. **Upload to target platform**

## Integration with Other Skills

This skill is the FINAL STEP in the pipeline:

```
remotion-render-config (this skill)
    ↓ outputs: RENDER_CONFIG.md
    ↓ used after: All implementation is complete
    ↓ produces: Final video file
```

**Works with:**
- `/remotion-scaffold` — Render outputs completed project
- `/remotion-composition` — Renders structured composition
- `/remotion-component-gen` — Renders implemented scenes
- `/remotion-spec-translator` — Orchestrates this as final step

---

This skill provides production-ready render configurations that ensure high-quality video output optimized for target platforms.
