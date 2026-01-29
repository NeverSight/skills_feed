---
name: ai-video-creator
description: End-to-end AI video production with avatar narration (HeyGen) and programmatic composition (Remotion). Use for creating tutorials, explainers, product demos, and narrated videos. Supports multi-language, custom branding, screen recordings, and batch clip generation.
---

# AI Video Creator

Complete video production pipeline: Audio → Visual composition → Optional avatar overlay.

## ⚠️ Best Practice: Audio-First Workflow

**Don't start with full avatar videos!** This wastes money and time.

### Recommended Approach for Tutorials:

```
Phase 1: Audio only (TTS) → Iterate on script timing
Phase 2: Compose visuals (code + browser) → Test layout
Phase 3: Add avatar overlay (optional) → Final polish
```

### Layout for Technical Tutorials:

```
┌────────────────────────────────────────────┐
│  🏰 Openfort React SDK          01-intro   │  ← Top bar
├─────────────────────┬──────────────────────┤
│                     │                      │
│       CODE          │      BROWSER         │
│      (55%)          │       (45%)          │
│                     │                      │
│                     │                      │
│                     │    [localhost:3000]  │
│                     │                      │
│                     │                      │
│                ╭────┴──╮                   │
│                │ 👤    │  ← Avatar circle  │
│                │avatar │    (optional,     │
│                ╰───────╯     added last)   │
└────────────────────────────────────────────┘
```

## Quick Reference

```bash
# 1. Generate AUDIO only (cheap, fast)
node scripts/generate-audio.js --config clips.json --output ./audio

# 2. Compose video with audio + visuals (no avatar)
npx remotion render Prototype ./output/prototype.mp4

# 3. Review and iterate (repeat 1-2 until happy)

# 4. ONLY THEN: Generate avatar clips (expensive)
HEYGEN_API_KEY=xxx node scripts/generate-clips.js --config clips.json --output ./clips

# 5. Final render with avatar overlay
npx remotion render TutorialWithAvatar ./output/final.mp4
```

## Workflow

### Phase 1: Audio-First (Iterate Cheap)

Generate just the audio narration:
```bash
# Option A: HeyGen audio-only (uses voice without avatar)
node scripts/generate-audio.js --config clips.json --voice VOICE_ID

# Option B: ElevenLabs (often cheaper)
node scripts/generate-audio-eleven.js --config clips.json --voice "Rachel"

# Option C: OpenAI TTS (cheapest)
node scripts/generate-audio-openai.js --config clips.json --voice "nova"
```

### Phase 2: Visual Composition

Create the split-screen layout without avatar:
```javascript
// Remotion component structure
<SplitLayout>
  <CodePanel width="55%">
    <SyntaxHighlightedCode />
  </CodePanel>
  <BrowserPanel width="45%">
    <BrowserChrome url="localhost:3000">
      <AppScreenshot />
    </BrowserChrome>
  </BrowserPanel>
  <Audio src={narrationAudio} />
</SplitLayout>
```

Render prototype:
```bash
npx remotion render Prototype ./output/prototype.mp4
```

**Review the prototype before spending on avatar!**

### Phase 3: Avatar Generation (Only When Satisfied)

Now that the content is finalized, generate avatar clips:
```bash
HEYGEN_API_KEY=xxx node scripts/generate-clips.js \
  --config clips.json \
  --output ./clips \
  --resolution 720p  # Use 720p unless plan supports 1080p
```

### Phase 4: Final Composition

Add avatar as circular overlay (picture-in-picture):
```javascript
// Avatar overlay style
<AvatarOverlay
  position="bottom-right"  // or "bottom-center"
  size={280}
  style="circle"
  border="4px solid rgba(255,255,255,0.2)"
>
  <OffthreadVideo src={avatarClip} />
</AvatarOverlay>
```

## HeyGen Resolution & Plans

| Plan | Max Resolution | Notes |
|------|---------------|-------|
| Free/Basic | 720p (1280x720) | Most accounts |
| Pro | 1080p (1920x1080) | Requires subscription |
| Enterprise | 4K | Custom plans |

**Always check your plan before generating!** Using unsupported resolution = failed jobs + wasted queue time.

## Cost Optimization

| Approach | Cost | Use When |
|----------|------|----------|
| Audio-only TTS | $0.01-0.05/min | Prototyping, iteration |
| HeyGen 720p | ~$1/min | Final avatar |
| HeyGen 1080p | ~$1.50/min | High-quality final |

**Rule: Iterate with audio-only, render avatar once.**

## Script Best Practices

- **Length**: 35-45 words per clip (ideal for 15-20 seconds)
- **Max**: 100 words (longer = audio sync issues)
- **Tech terms**: Write phonetically for Spanish
  - "npm" → "ene pe eme"
  - ".tsx" → "punto tee ese equis"
  - "localhost" → "localhost" (usually ok)
- **Pauses**: `<break time="0.5s"/>` for natural rhythm

## Multi-Language Workflow

```bash
# 1. Audio prototype in target language
node scripts/generate-audio.js --config clips-es.json --voice "es-ES-female"

# 2. Compose & review
npx remotion render Prototype-ES ./output/prototype-es.mp4

# 3. Generate Spanish avatar only when satisfied
node scripts/generate-clips.js --config clips-es.json --voice "1eca26cb..."
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "RESOLUTION_NOT_ALLOWED" | Use 720p (1280x720) |
| Clips stuck "waiting" | Check credits/subscription |
| Avatar desync | Keep clips under 100 words |
| Expensive iteration | Use audio-only for prototypes! |

## See Also

- `references/heygen-api.md` — Full HeyGen API docs
- `references/remotion-templates.md` — Ready-to-use layouts
- `references/tts-comparison.md` — TTS providers comparison
