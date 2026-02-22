---
name: webconsulting-create-documentation
description: Create product documentation with help pages, AI-generated screenshots, Remotion product videos with TTS narration and background music, and GitHub README visual documentation. Use when asked to create documentation, a help page, product tour video, generate screenshots, add user guides, or enrich a GitHub README.
---

# webconsulting — Create Documentation

End-to-end workflow for building product documentation: help pages, AI-generated illustrations, narrated product tour videos (Remotion + ElevenLabs TTS + Suno AI music), and GitHub README visual documentation.

## Prerequisites

### Required

| Dependency | Install | Purpose |
|------------|---------|---------|
| Node.js 20+ | Pre-installed | Runtime |
| Remotion | `npm install remotion @remotion/cli @remotion/player` | Video composition |
| qrcode.react | `npm install qrcode.react` | QR codes in end card |
| tsx | `npm install -D tsx` | Run TypeScript scripts |

### Optional (for production quality)

| Dependency | Install | Purpose |
|------------|---------|---------|
| ElevenLabs API key | [elevenlabs.io](https://elevenlabs.io) | Premium TTS narration (Jony Ive voice) |
| ffmpeg | `brew install ffmpeg` | Convert audio to MP3 (smaller files) |
| macOS `say` + `afconvert` | Built-in on macOS | Fallback TTS (Daniel voice, outputs WAV) |
| Suno API key | [api.box](https://www.api.box) | AI-generated background music |

### ElevenLabs Setup

1. Create a free account at [elevenlabs.io](https://elevenlabs.io)
2. Navigate to **Profile + API key** in the sidebar
3. Copy your API key
4. Add to your `.env` file:

```bash
ELEVENLABS_API_KEY=your-api-key-here
```

Also add to `.env.example` (commented out) for team documentation:

```bash
# ELEVENLABS_API_KEY=your-elevenlabs-api-key
```

**Voice selection**: The default voice is "Daniel" (`onwK4e9ZLuTAKqWW03F9`) — British, calm.
Browse [elevenlabs.io/voice-library](https://elevenlabs.io/voice-library) and update
the `VOICE_ID` in `scripts/generate-narration.ts` if a better match is found.

**Free tier limits**: ~10,000 characters/month. The full narration script is ~600 characters,
so you can regenerate ~16 times per month on the free tier.

## Workflow Overview

```
1. Create help page       → React component with collapsible sections
2. Generate illustrations → AI image generation tool (GenerateImage)
3. Build Remotion video   → Animated scenes with narration subtitles
4. Generate TTS audio     → ElevenLabs API or macOS `say` fallback
5. Generate music         → Suno AI background music (optional)
6. Render final video     → npm run remotion:render
7. GitHub README          → Embed screenshots + video in README.md
```

## Phase 1: Help Page

Create an in-app help page at `src/app/(dashboard)/help/page.tsx`.

### Structure pattern

```tsx
// Collapsible section wrapper
function HelpSection({ id, icon, title, description, children, defaultOpen }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <Card id={id}>
      <button onClick={() => setOpen(o => !o)}>
        {/* Header with icon, title, description, chevron */}
      </button>
      {open && <CardContent>{children}</CardContent>}
    </Card>
  );
}

// Step-by-step instruction
function Step({ number, title, children }) { /* numbered step */ }

// Pro tip callout
function Tip({ children }) { /* highlighted tip box */ }

// Screenshot placeholder
function Screenshot({ src, alt, caption }) { /* Next/Image with caption */ }
```

### Key sections to include

1. **Table of Contents** — auto-generated from section data with anchor links
2. **Getting Started** — first-time user orientation (default open)
3. **Feature sections** — one per major feature (Dashboard, Clients, Extensions, etc.)
4. **Product Video** — embedded `<video>` element pointing to rendered MP4
5. **FAQ / Troubleshooting** — common questions

### Writing guidelines

- Target audience: users with **low technical knowledge**
- Write as a **senior technical writer** — clear, friendly, no jargon
- Every section has numbered steps with screenshots
- Include "Tip" callouts for pro tips
- Use Tailwind v4 syntax (`mt-3!` not `!mt-3`)

## Phase 2: Screenshots / Illustrations

Since browser automation for screenshots can be unreliable, use AI-generated illustrations.

### Using the GenerateImage tool

```
GenerateImage({
  description: "Modern flat illustration of a monitoring dashboard with
    stat cards showing Total Clients, Extensions, Security Issues.
    Dark theme, clean UI, subtle orange accents.",
  filename: "dashboard.png"
})
```

Place generated images in `public/help/`:

```
public/help/
├── dashboard.png
├── clients.png
├── wizard.png
└── product-tour.mp4   (rendered later)
```

Reference in the help page:

```tsx
<Screenshot src="/help/dashboard.png" alt="Dashboard overview" caption="The main dashboard" />
```

## Phase 3: Remotion Product Video

### Directory structure

```
remotion/
├── index.ts          # registerRoot entry point
├── Root.tsx          # Composition definitions
└── ProductTour.tsx   # All scenes + narration script
```

### Composition setup (`Root.tsx`)

```tsx
import { Composition } from "remotion";
import { ProductTour } from "./ProductTour";

export const RemotionRoot = () => (
  <Composition
    id="ProductTour"
    component={ProductTour}
    durationInFrames={30 * 45}  // 45 seconds at 30fps
    fps={30}
    width={1920}
    height={1080}
  />
);
```

### Scene pattern

Each scene follows this structure:

```tsx
function SceneComponent() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: DARK_BG, padding: 80 }}>
      <SceneAudio scene="scene-name" />           {/* TTS audio */}
      <FadeInText fontSize={56}>Title</FadeInText> {/* Animated heading */}
      {/* Scene-specific content with spring/interpolate animations */}
      <NarrationSubtitle text={NARRATION_SCRIPT.sceneName} />  {/* Subtitles */}
    </AbsoluteFill>
  );
}
```

### Recommended scenes (7 total, ~75 seconds)

Durations are **dynamic** — driven by narration audio length (see Phase 5).
The video includes a **1.5s lead-in** (dark + exponential volume ramp) and
a **4s end card** with social links that fades to black.

| # | Scene | ~Duration | Content |
|---|-------|-----------|---------|
| — | Lead-in | 1.5s | Dark screen, music fades in (exponential t^2.5) |
| 1 | Intro | 13s | Logo + tagline + brand identity |
| 2 | Dashboard | 12s | Stat cards with spring animations |
| 3 | Clients | 12s | Client list with slide-in rows |
| 4 | Wizard | 11s | Step indicator with progressive activation |
| 5 | Security | 11s | Feature grid with staggered fade-in |
| 6 | Outro | 11s | Logo + CTA + credits + website (highlight blog) |
| 7 | End Card | 7s | 4 QR codes (website, GitHub, YouTube, X) + scale-up finale |

### Lead-in and end card

The lead-in uses an **exponential volume curve** (`Math.pow(t, 2.5)`) because
human hearing follows a logarithmic scale (Weber-Fechner law). A linear ramp
sounds "sudden" in the middle; the power curve feels perceptually smooth.

The end card shows 4 QR codes with social/website links (staggered slide-up).
**No fade-to-black** — the QR codes stay fully visible so viewers can scan them.
In the **final 2 seconds**, the entire card scales up dramatically (1.0 → 1.5)
with the T3 Monitoring logo, creating a confident, cinematic close.
The "Find us on" heading scales up in sync but also **moves upward** (-120px)
so it doesn't get covered by the expanding QR code row.

QR codes are rendered inline using `qrcode.react` (`npm install qrcode.react`).

```tsx
export const LEAD_IN_FRAMES = Math.round(30 * 1.5); // 45 frames
export const END_CARD_FRAMES = Math.round(30 * 7);   // 210 frames
```

These are added to `TOTAL_FRAMES` in `Root.tsx` for the composition duration.

#### End card links

| # | Platform | Handle | Highlight |
|---|----------|--------|-----------|
| 1 | Website | webconsulting.at | Orange border, `/blog` callout with description |
| 2 | GitHub | @dirnbauer | — |
| 3 | YouTube | @webconsulting-curt | — |
| 4 | X | @KDirnbauer | — |

The website card is **emphasized**: orange handle text, orange QR border,
and a `/blog` pill badge below — glass-style container with orange border,
glow shadow, and "Tutorials & deep dives" label.

#### QR code pattern

```tsx
import { QRCodeSVG } from "qrcode.react";

<QRCodeSVG value="https://webconsulting.at" size={140}
  bgColor="#ffffff" fgColor="#0f172a" level="M" />
```

Each social card shows: platform icon + handle, QR code (white bg, dark fg,
rounded container), URL text, and optional highlight callout.

### Animation toolkit

```tsx
// Fade + slide up
const opacity = interpolate(frame - delay, [0, fps * 0.6], [0, 1], {
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});

// Spring bounce for cards
const scale = spring({ fps, frame: frame - i * 8, config: { damping: 80 } });

// Staggered slide-in for list items
const slideX = interpolate(frame - i * 10, [0, fps * 0.5], [100, 0], {
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});
```

## Phase 4: Narration (Jony Ive Style)

### Voice characteristics

- **Tone**: Calm, deliberate, aspirational
- **Pace**: ~140 words per minute (slow, measured)
- **Style**: Short declarative sentences. Dramatic pauses. Marketing-punchy.
- **Influence**: Sir Jonathan Ive — think Apple product launch presentations

### Writing narration copy

```
BAD:  "This is a dashboard that shows you statistics about your clients."
GOOD: "Your dashboard. Beautifully considered. Every metric, thoughtfully
       placed, to give you immediate clarity."
```

### Export the narration script (single source of truth)

Define all narration text in `ProductTour.tsx` as an **exported** constant.
This is the single source of truth for both subtitles and audio generation:

```tsx
// remotion/ProductTour.tsx
export const NARRATION_SCRIPT: Record<string, string> = {
  intro: "Imagine seeing every TYPO3 installation you manage...",
  dashboard: "Your dashboard gives you the full picture...",
  // ... one entry per scene
};
```

**Critical**: The generate script **imports** this constant — never duplicate the text:

```tsx
// scripts/generate-narration.ts
import { NARRATION_SCRIPT } from "../remotion/ProductTour.js";
const NARRATION = NARRATION_SCRIPT; // Same text for audio + subtitles
```

This guarantees spoken audio always matches the on-screen subtitles.
If you edit `NARRATION_SCRIPT`, just re-run `npm run narration:generate` and
`npm run remotion:render` — both audio and subtitles update automatically.

### NarrationSubtitle component

Cinematic lower-third with word-by-word reveal, slide-up entrance, and active-word glow.
**Always reads from `NARRATION_SCRIPT`** — update the script and subtitles auto-sync.

```tsx
function NarrationSubtitle({ text }: { text: string }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Slide-up + fade entrance (0.4s → 0.9s)
  const fadeIn = interpolate(frame, [fps * 0.4, fps * 0.9], [0, 1], { ... });
  const slideUp = interpolate(frame, [fps * 0.4, fps * 0.9], [20, 0], { ... });

  const words = text.split(" ");
  const framesPerWord = fps / 2.8; // calm pace, ~2.8 words/sec

  return (
    <div style={{ position: "absolute", bottom: 60, opacity: fadeIn,
                  transform: `translateY(${slideUp}px)` }}>
      <div style={{
        maxWidth: 1100, padding: "24px 56px",
        background: "linear-gradient(135deg, rgba(0,0,0,0.72), rgba(20,20,30,0.68))",
        borderRadius: 20, border: "1px solid rgba(255,255,255,0.08)",
        boxShadow: "0 8px 32px rgba(0,0,0,0.4), 0 0 80px rgba(255,120,50,0.04)",
      }}>
        {/* Subtle top accent line */}
        <div style={{ position: "absolute", top: 0, left: 40, right: 40, height: 1,
          background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent)" }} />
        {words.map((word, i) => {
          const wordDelay = fps * 0.5 + i * framesPerWord;
          const wordOpacity = interpolate(frame, [wordDelay, wordDelay + framesPerWord * 0.5],
            [0.25, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const isActive = frame >= wordDelay && frame < wordDelay + framesPerWord * 1.2;
          return (
            <span key={i} style={{
              fontSize: 30, fontWeight: 300, color: "#fff",
              fontFamily: "'SF Pro Display', 'Inter', system-ui",
              opacity: isActive ? 1 : wordOpacity, letterSpacing: "0.02em",
              textShadow: isActive ? "0 0 20px rgba(255,255,255,0.15)" : "none",
            }}>{word}</span>
          );
        })}
      </div>
    </div>
  );
}
```

### Subtitle styling principles

- **Auto-sync**: Component reads `NARRATION_SCRIPT[scene]` directly — change the
  script text and the subtitles update automatically on next render
- **Slide-up entrance**: Subtitles slide up 20px while fading in (0.4s–0.9s), feels organic
- **Glass morphism container**: Dark gradient background with subtle border and box-shadow,
  plus a thin accent line at the top for depth
- **Word-by-word reveal**: Each word fades from 0.25 to 1.0 opacity at ~2.8 words/second
- **Active word glow**: The currently spoken word gets full opacity + a soft white `text-shadow`
- **Typography**: SF Pro Display / Inter, weight 300 (light), 30px, generous letter-spacing
- **Positioning**: 60px from bottom, centered, max-width 1100px

### When to update subtitles

Subtitles auto-update whenever you change `NARRATION_SCRIPT` in `ProductTour.tsx`.
The full pipeline after editing narration text:

```bash
# 1. Edit NARRATION_SCRIPT in remotion/ProductTour.tsx
# 2. Regenerate audio (subtitles already match the new text)
npm run narration:generate
# 3. Re-render video
npm run remotion:render
```

## Phase 5: TTS Audio Generation

### Script: `scripts/generate-narration.ts`

The script supports two backends and auto-generates `remotion/narration-format.ts`
so the video composition always uses the correct file extension.

| Backend | Trigger | Output | Quality |
|---------|---------|--------|---------|
| ElevenLabs | `ELEVENLABS_API_KEY` set in `.env` | `.mp3` | Production |
| macOS `say` + `afconvert` | No API key, macOS detected | `.wav` | Development preview |

```bash
# Production: use ElevenLabs (add key to .env first)
npm run narration:generate

# Development: macOS fallback (no key needed)
npm run narration:generate
```

The script automatically:
1. Cleans old audio files (prevents mixing formats)
2. Generates audio files in `public/narration/`
3. Probes each file's duration using `afinfo` (macOS) or `ffprobe`
4. Writes `remotion/narration-format.ts` with the correct extension (`"mp3"` or `"wav"`)
5. Writes `remotion/narration-durations.ts` with per-scene frame counts (audio + 2s padding)
6. The Remotion composition imports both configs for synced playback

### ElevenLabs voice settings for Jony Ive style

```json
{
  "voice_id": "onwK4e9ZLuTAKqWW03F9",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.75,
    "similarity_boost": 0.70,
    "style": 0.35,
    "use_speaker_boost": true
  }
}
```

### Audio file location

```
public/narration/
├── intro.mp3 (or .wav)
├── dashboard.mp3
├── clients.mp3
├── wizard.mp3
├── security.mp3
└── outro.mp3

remotion/
├── narration-format.ts      ← auto-generated, audio extension ("mp3" | "wav")
└── narration-durations.ts   ← auto-generated, per-scene frame counts + total
```

### Audio-video sync (critical)

Scene durations are driven by audio length, not hardcoded. The generate script:
1. Probes each audio file's duration (e.g., intro = 8.5s)
2. Adds 2s padding for visual animation breathing room
3. Writes frame count: `ceil((8.5 + 2) * 30) = 317 frames`
4. `ProductTour.tsx` imports these and uses them for `Sequence` durations

Each scene also has:
- **Audio fade-out** (last 1s) — prevents abrupt cut-off between scenes
- **Visual fade-to-black** (last 0.5s) — smooth scene transitions
- **Total video duration** is computed from sum of all scene frames

### Important: format config

`staticFile()` in Remotion does NOT throw when a file is missing — it returns a URL
that 404s at render time. That's why the generate script writes `narration-format.ts`
to ensure the video only references files that actually exist. Always run
`npm run narration:generate` before `npm run remotion:render`.

### Full narration script (prompt)

This is the exact text sent to ElevenLabs. Copy and adapt for your product:

The narration text lives in `remotion/ProductTour.tsx` as `NARRATION_SCRIPT`.
The generate script imports it — **never edit narration text in two places**.

To see the current script, read `NARRATION_SCRIPT` in `ProductTour.tsx`.
To change it, edit only that file, then re-run:

```bash
npm run narration:generate   # Regenerates audio from the updated text
npm run remotion:render      # Subtitles already read from the same source
```

## Phase 5b: Background Music (Suno AI)

### Setup

1. Get a Suno API key at [api.box](https://www.api.box) (Suno API provider)
2. Add to `.env`: `SUNO_API_KEY=your-key`

### Generate music

```bash
npm run music:generate
# Output: public/music/background.mp3
# Config: remotion/music-config.ts (HAS_BACKGROUND_MUSIC = true)
```

The script:
1. Sends a prompt to Suno's API (model V4_5ALL, instrumental only)
2. Polls for completion (typically 30-60 seconds)
3. Downloads the MP3 to `public/music/background.mp3`
4. Writes `remotion/music-config.ts` so the video knows music exists

### Music prompt (adapt for your product)

```
Uplifting neoclassical underscore for a modern technology product video.
Bright piano arpeggios in a major key over gentle pizzicato strings and
a soft cello melody. Light, optimistic, and forward-moving — like a TED
talk opening or an Apple product reveal. Subtle modern electronic texture
underneath the classical instruments. No heavy drums, no vocals, no sudden
drops. Tempo around 100 BPM. Engaging but never distracting — true
background music that lifts the mood without competing with narration.
Think Max Richter meets Ólafur Arnalds with a hint of Nils Frahm.
Duration should be around 90 seconds.
```

**Key prompt principles:**
- Specify **major key** to avoid melancholic/minor tonality
- Name **classic instruments** (piano, strings, cello) for warmth and sophistication
- Add **modern electronic texture** to keep it contemporary
- Reference **real composers** (Max Richter, Ólafur Arnalds, Nils Frahm) for style anchoring
- Emphasize **"background music"** and **"never distracting"** — Suno tends to overpower otherwise
- Set **tempo** (100 BPM) — too slow feels sad, too fast feels hectic

### Volume ducking

The `BackgroundMusic` component in `ProductTour.tsx` handles automatic
volume ducking — music plays at 0.15 volume between scenes and ducks to
0.06 when narration is active. Transitions are smooth 0.5s ramps.

- Fade in: first 2s of video
- Fade out: last 3s of video
- Loop: music loops if shorter than the video

### Without Suno API key

If no key is set, the video renders without background music (narration only).
You can also manually place any MP3 at `public/music/background.mp3` and set
`HAS_BACKGROUND_MUSIC = true` in `remotion/music-config.ts`.

## Phase 6: Render & Deploy

```bash
# Full pipeline: narration → music → render
npm run narration:generate   # ElevenLabs narration (or macOS fallback)
npm run music:generate       # Suno background music (optional)
npm run remotion:render      # Final MP4 with both audio layers

# Preview in Remotion Studio
npm run remotion:studio

# Output: public/help/product-tour.mp4
# The help page references the video:
# <video src="/help/product-tour.mp4" controls />
```

### package.json scripts

```json
{
  "remotion:studio": "npx remotion studio remotion/index.ts",
  "remotion:render": "npx remotion render remotion/index.ts ProductTour public/help/product-tour.mp4",
  "narration:generate": "tsx scripts/generate-narration.ts",
  "music:generate": "tsx scripts/generate-music.ts"
}
```

## Phase 7: GitHub README Documentation

Use the same assets (illustrations, video) to enrich your GitHub `README.md` with
visual documentation. This makes the repository professional and immediately
communicates value to contributors and potential users.

### Strategy

```
README.md documentation flow:
1. Re-use existing illustrations from public/help/
2. Generate additional screenshots/GIFs specific to README sections
3. Upload video to GitHub release or external host (too large for git)
4. Embed everything with standard Markdown + HTML
```

### Embedding screenshots in README

GitHub renders standard Markdown images. Place screenshots in a `docs/` or
`.github/` directory and reference them with relative paths:

```markdown
## Dashboard

![Dashboard overview](docs/screenshots/dashboard.png)

The main dashboard shows all monitored TYPO3 installations at a glance,
with health scores and security alerts.
```

**Best practices for README screenshots:**
- Use 1200px width (GitHub caps display at ~900px, 2× for retina)
- Prefer light theme or show both with `<picture>` for dark mode support
- Add a 1px border or subtle shadow so screenshots don't bleed into the page
- Keep file sizes under 500KB (PNG with compression or JPEG at 85%)

### Dark/light theme images

GitHub supports `<picture>` with `prefers-color-scheme` media queries:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/dashboard-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/screenshots/dashboard-light.png">
  <img alt="Dashboard overview" src="docs/screenshots/dashboard-light.png" width="800">
</picture>
```

### Generating screenshots for README

You have two approaches:

**1. AI-generated illustrations (fast, always available):**

```
GenerateImage({
  description: "Clean screenshot-style illustration of a TYPO3 monitoring
    dashboard. Dark theme, stat cards showing Total Clients: 42,
    Healthy: 38, Warning: 3, Critical: 1. Sidebar navigation visible.
    Modern, polished UI. 1200×675px, 16:9 aspect ratio.",
  filename: "docs/screenshots/dashboard.png"
})
```

**2. Real screenshots via Playwright (pixel-perfect):**

```typescript
// scripts/capture-screenshots.ts
import { chromium } from "playwright";

async function captureScreenshots() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 675 } });

  // Login if needed
  await page.goto("http://localhost:3001");

  // Capture each page
  const pages = [
    { url: "/", name: "dashboard" },
    { url: "/clients", name: "clients" },
    { url: "/extensions", name: "extensions" },
    { url: "/help", name: "help" },
  ];

  for (const p of pages) {
    await page.goto(`http://localhost:3001${p.url}`);
    await page.waitForTimeout(2000); // Let animations settle
    await page.screenshot({ path: `docs/screenshots/${p.name}.png` });
    // Also capture dark mode
    await page.emulateMedia({ colorScheme: "dark" });
    await page.screenshot({ path: `docs/screenshots/${p.name}-dark.png` });
    await page.emulateMedia({ colorScheme: "light" });
  }

  await browser.close();
}

captureScreenshots();
```

Add to `package.json`:
```json
"screenshots:capture": "tsx scripts/capture-screenshots.ts"
```

### Animated GIFs for README

Short GIFs are more engaging than static screenshots for interactive features
(wizard, sorting, filtering). Use Playwright to record and `ffmpeg` to convert:

```bash
# Record a video clip with Playwright (outputs .webm)
# Then convert to GIF:
ffmpeg -i recording.webm -vf "fps=12,scale=800:-1:flags=lanczos" -loop 0 docs/screenshots/wizard.gif
```

Keep GIFs under 5MB. For larger animations, use MP4 with GitHub's video support.

### Embedding the product tour video

GitHub Markdown supports video since 2021. You have three options:

**Option A: Upload to GitHub Release (recommended for open source)**

```bash
# Create a release and attach the video
gh release create v1.0.0 public/help/product-tour.mp4 \
  --title "v1.0.0" --notes "Initial release"
```

Then link in README:

```markdown
## Product Tour

https://github.com/your-org/your-repo/releases/download/v1.0.0/product-tour.mp4
```

GitHub auto-embeds the video player when the URL is on its own line.

**Option B: Drag-and-drop into GitHub Issue/PR**

1. Create a GitHub issue or PR
2. Drag the MP4 into the comment editor
3. Copy the resulting `user-attachments` URL
4. Paste into README

```markdown
## Product Tour

https://github.com/user-attachments/assets/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**Option C: External host (YouTube, Vimeo)**

If the video is large (>25MB) or you want analytics, upload to YouTube/Vimeo
and embed a thumbnail with a play button:

```markdown
## Product Tour

[![Watch the product tour](docs/screenshots/video-thumbnail.png)](https://youtu.be/your-video-id)
```

### Full README template with documentation

Here's a recommended structure integrating all visual assets:

```markdown
# Project Name

> One-line description — aspirational, concise.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/hero-dark.png">
  <img alt="Project screenshot" src="docs/screenshots/hero-light.png" width="800">
</picture>

## Product Tour

https://github.com/your-org/repo/releases/download/v1.0.0/product-tour.mp4

## Features

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)
Description of the dashboard...

### Client Management
![Clients](docs/screenshots/clients.gif)
Description of client features...

## Quick Start
...installation instructions...
```

### Updating documentation on changes

When the UI changes, re-run the documentation pipeline:

```bash
# 1. Capture fresh screenshots (if using Playwright)
npm run screenshots:capture

# 2. Regenerate illustrations (if using AI)
# → Use GenerateImage tool with updated descriptions

# 3. Update narration if features changed
# → Edit NARRATION_SCRIPT in remotion/ProductTour.tsx
npm run narration:generate

# 4. Re-render the product tour video
npm run remotion:render

# 5. Upload new video to GitHub release
gh release upload v1.x.x public/help/product-tour.mp4 --clobber

# 6. Commit updated screenshots
git add docs/screenshots/ README.md
git commit -m "docs: update screenshots and video for vX.Y.Z"
```

### Directory structure for README documentation

```
project/
├── README.md                          ← Main documentation with embedded visuals
├── docs/
│   ├── screenshots/
│   │   ├── dashboard.png              ← Light theme screenshot
│   │   ├── dashboard-dark.png         ← Dark theme screenshot
│   │   ├── clients.png
│   │   ├── wizard.gif                 ← Animated walkthrough
│   │   ├── hero-light.png             ← Hero image (light)
│   │   ├── hero-dark.png              ← Hero image (dark)
│   │   └── video-thumbnail.png        ← Video poster frame
│   └── SECURITY.md
├── public/help/
│   └── product-tour.mp4              ← Rendered Remotion video
└── scripts/
    ├── capture-screenshots.ts         ← Playwright screenshot automation
    ├── generate-narration.ts          ← TTS generation
    └── generate-music.ts             ← Background music generation
```

## Checklist

```
Documentation Creation:
- [ ] Help page component created at src/app/(dashboard)/help/page.tsx
- [ ] Sidebar navigation updated with Help link
- [ ] AI-generated illustrations in public/help/
- [ ] Remotion project set up in remotion/
- [ ] Narration script written (Jony Ive style)
- [ ] NarrationSubtitle component added to video
- [ ] TTS audio generated (ElevenLabs or macOS fallback)
- [ ] Video rendered to public/help/product-tour.mp4
- [ ] Video embedded in help page
- [ ] All content reviewed by technical writer persona

GitHub README Documentation:
- [ ] Screenshots captured (AI-generated or Playwright)
- [ ] Dark/light variants created with <picture> tags
- [ ] Product tour video uploaded to GitHub release
- [ ] README.md updated with embedded visuals
- [ ] Animated GIFs created for interactive features (optional)
- [ ] Documentation update pipeline documented in scripts
```

## Additional resources

- For narration examples and full script, see [narration-examples.md](narration-examples.md)
- Remotion docs: [remotion.dev/docs](https://remotion.dev/docs)
- ElevenLabs docs: [elevenlabs.io/docs](https://elevenlabs.io/docs)
- GitHub Markdown reference: [docs.github.com/en/get-started/writing-on-github](https://docs.github.com/en/get-started/writing-on-github)
- GitHub `<picture>` dark mode: [github.blog/changelog/2022-05-19-specify-theme-context-for-images-in-markdown](https://github.blog/changelog/2022-05-19-specify-theme-context-for-images-in-markdown/)

## Video & Animation for Documentation (Remotion + GSAP)

When generating visual documentation, integrating **Remotion** with **GSAP** allows for complex, sequenced, and dynamic visual storytelling.

### Prerequisites

GSAP must be installed alongside your existing Remotion setup. GSAP's core is free for all use cases; premium plugins require a paid license.

**Install GSAP core:**

```bash
npm install gsap
```

**Optional premium plugins** (require [GSAP Club](https://gsap.com/pricing/) license):

```bash
# Install from GSAP's private registry (requires auth token)
npm install gsap@npm:@gsap/shockingly
```

Premium plugins used in this guide:
- `MorphSVGPlugin` -- morph between SVG shapes (chart transitions)
- `SplitText` -- split text into characters/words for kinetic typography
- `Flip` -- animate layout changes (code diff walkthroughs)
- `MotionPathPlugin` -- animate along SVG paths (included free since GSAP 3.x)

**Register plugins** in your Remotion entry point (e.g., `src/Root.tsx` or the component file):

```tsx
import gsap from "gsap";
import { MotionPathPlugin } from "gsap/MotionPathPlugin";

gsap.registerPlugin(MotionPathPlugin);
// Add other plugins as needed:
// gsap.registerPlugin(Flip, MorphSVGPlugin, SplitText);
```

**Remotion compatibility notes:**
- GSAP works in Remotion's rendering pipeline because it manipulates DOM elements directly, which Remotion captures frame-by-frame.
- Always use `gsap.context()` for proper React cleanup on unmount.
- Never use GSAP's `ScrollTrigger` in Remotion -- there is no scroll context during rendering.

### Core Concept: Deterministic Syncing
Remotion is frame-based; GSAP is time-based. To ensure videos render correctly without tearing or skipping during export, **never let GSAP run on its own timer**. Map Remotion's `useCurrentFrame()` to a strictly paused GSAP timeline.

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useEffect, useMemo, useRef } from "react";
import gsap from "gsap";

export const GsapSequence = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  
  // 1. Create a strictly paused timeline
  const timeline = useMemo(() => gsap.timeline({ paused: true }), []);

  // 2. Build your animation sequence (use GSAP seconds)
  useEffect(() => {
    let ctx = gsap.context(() => {
      timeline.to(".box", { x: 200, rotation: 360, duration: 2, stagger: 0.2 });
    }, containerRef);
    
    return () => ctx.revert(); // React cleanup
  }, [timeline]);

  // 3. THE MAGIC: Sync GSAP playhead to Remotion frame
  useEffect(() => {
    timeline.seek(frame / fps); 
  }, [frame, fps, timeline]);

  return (
    <div ref={containerRef} className="box-container">
      <div className="box">Item 1</div>
      <div className="box">Item 2</div>
    </div>
  );
};
```

### Creative Directives for AI Agents

When prompted to create visual documentation, utilize the following animation patterns:

#### 1. Diagram Animations
- **Data Flow Tracing:** Use GSAP `MotionPathPlugin` or animate `stroke-dashoffset` to show data packets moving along SVG lines between architecture nodes (e.g., Load Balancer → DB).
- **Node Pulses:** Add glowing/pulsing loops (`box-shadow` and `scale`) to servers/components when they become "active" in the explanation.
- **Elastic Reveals:** Animate nodes popping into existence with `ease: "back.out(1.5)"` and a `stagger: 0.1`.

#### 2. Animation of Screenshots
- **3D Exploded View:** Separate UI components into layers (background, modal, button) and rotate the parent container in 3D (`rotateX: 60deg`, `rotateZ: -45deg`). Animate the `translateZ` of inner layers to pull the interface apart conceptually.
- **Glass Morph Spotlight:** Smoothly zoom into an active UI area using a `clip-path` circle, while dimming and applying a CSS blur (`backdrop-filter: blur(10px)`) to the rest of the screenshot.
- **Simulated User Journeys:** Animate a custom SVG cursor moving across the UI, synchronizing button scaling and ripple effects to simulate clicks.

#### 3. Infographics & Tables
- **Staggered Row Reveals:** Slide and fade in table rows one-by-one (`stagger: 0.1`, `x: -20`, `opacity: 0`) to pace the viewer's reading.
- **Data Odometers:** Animate a numeric object's value from 0 to target (using `onUpdate` to format text), making financial or performance numbers tick up dynamically.
- **Cell Highlighting:** Animate a floating background div that smoothly translates its `y` coordinate from row to row to highlight active talking points.

#### 4. Animations of Charts
- **Spring-loaded Bar Charts:** Set CSS `transform-origin: bottom`. Animate SVG `<rect>` `scaleY` from 0 to target with GSAP's `elastic.out` easing for a playful reveal.
- **Progressive Charts:** Animate SVG circles with `stroke-dasharray` and `stroke-dashoffset` to draw out pie chart segments proportionally over time.
- **Morphing Data:** Use `MorphSVGPlugin` to seamlessly transition a bar chart into a line chart, visually connecting two different ways of looking at the same data.

#### 5. Code & Text
- **Code Diff Walkthroughs:** Use GSAP's `Flip` plugin. When code changes, removed lines shrink and glow red, new lines expand and glow green, and unchanged lines glide to their new line numbers smoothly.
- **Kinetic Typography:** Use GSAP `SplitText` to stagger headers character-by-character.

---

### Concrete Code Examples (Remotion + GSAP Patterns)

Use these blueprints as starting points when generating Remotion + GSAP code to ensure correct CSS contexts, React lifecycle management, and frame syncing.

#### Example 1: 3D Exploded Screenshot (UI Layers)
Requires a strict CSS 3D context. The parent needs `perspective`, and the container needs `transformStyle: "preserve-3d"`.

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useEffect, useMemo, useRef } from "react";
import gsap from "gsap";

export const ExplodedScreenshot = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  const tl = useMemo(() => gsap.timeline({ paused: true }), []);

  useEffect(() => {
    let ctx = gsap.context(() => {
      // 1. Tilt the whole container into isometric space
      tl.to(".wrapper", { rotateX: 60, rotateZ: -45, duration: 1, ease: "power2.inOut" })
        // 2. Explode the layers upward on the Z-axis (Using "<" to sync with rotation end)
        .to(".ui-layer", {
          z: (index) => (index + 1) * 80, // Stagger height based on index
          boxShadow: "0px 20px 40px rgba(0,0,0,0.4)",
          duration: 1.5,
          ease: "back.out(1.2)",
          stagger: 0.2
        }, "-=0.2"); 
    }, containerRef);
    
    return () => ctx.revert(); // Crucial for React StrictMode cleanup
  }, [tl]);

  // Deterministic Frame Sync
  useEffect(() => { tl.seek(frame / fps); }, [frame, fps, tl]);

  return (
    <div ref={containerRef} style={{ perspective: 1000, width: "100%", height: "100%" }}>
      <div className="wrapper" style={{ transformStyle: "preserve-3d", position: "relative", width: 800, height: 600 }}>
        <img src="/bg-layer.png" className="ui-layer" style={{ position: "absolute", inset: 0 }} />
        <img src="/modal-layer.png" className="ui-layer" style={{ position: "absolute", inset: 0 }} />
        <img src="/dropdown-layer.png" className="ui-layer" style={{ position: "absolute", inset: 0 }} />
      </div>
    </div>
  );
};
```

#### Example 2: SVG Architecture Diagram (Drawing Data Flows)
Use native SVG `strokeDasharray` and GSAP `strokeDashoffset` to draw connection lines between nodes without needing external plugins.

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useEffect, useMemo, useRef } from "react";
import gsap from "gsap";

export const ArchitectureFlow = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const svgRef = useRef<SVGSVGElement>(null);
  const tl = useMemo(() => gsap.timeline({ paused: true }), []);

  useEffect(() => {
    let ctx = gsap.context(() => {
      // Setup: ensure path is hidden initially (Assuming path length ~500)
      gsap.set(".connection-line", { strokeDasharray: 500, strokeDashoffset: 500 });

      // 1. Pop the nodes in
      tl.from(".node", { scale: 0, transformOrigin: "center", duration: 0.5, stagger: 0.3, ease: "back.out(1.5)" })
      // 2. Draw the line between them
        .to(".connection-line", { strokeDashoffset: 0, duration: 1.2, ease: "power2.inOut" })
      // 3. Pulse the receiving node to indicate data arrival
        .to(".node-db", { scale: 1.15, repeat: 1, yoyo: true, duration: 0.2, fill: "#10b981" });
    }, svgRef);
    
    return () => ctx.revert();
  }, [tl]);

  useEffect(() => { tl.seek(frame / fps); }, [frame, fps, tl]);

  return (
    <svg ref={svgRef} width="800" height="400" viewBox="0 0 800 400">
      {/* Connecting Line */}
      <path className="connection-line" d="M 100 200 C 300 200, 500 200, 700 200" stroke="#cbd5e1" strokeWidth="6" fill="none" />
      {/* Nodes */}
      <circle className="node node-client" cx="100" cy="200" r="40" fill="#3b82f6" />
      <rect className="node node-db" x="660" y="160" width="80" height="80" rx="12" fill="#6366f1" />
    </svg>
  );
};
```

#### Example 3: Number Odometer (For Infographics & Tables)
To animate a number counting up (e.g., "0" to "10,000") smoothly, animate a dummy object and use `onUpdate` to safely set React state synchronously with the frame.

```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useEffect, useMemo, useState } from "react";
import gsap from "gsap";

export const AnimatedNumber = ({ targetValue = 10000 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const [displayValue, setDisplayValue] = useState(0);
  
  const tl = useMemo(() => gsap.timeline({ paused: true }), []);

  useEffect(() => {
    const counter = { val: 0 };
    
    // gsap.context isn't strictly necessary for JS objects, but good for consistency
    let ctx = gsap.context(() => {
      tl.to(counter, {
        val: targetValue,
        duration: 2,
        ease: "power2.out",
        onUpdate: () => {
          // Update React state safely as GSAP manipulates the dummy object
          setDisplayValue(Math.round(counter.val));
        }
      });
    });
    
    return () => ctx.revert();
  }, [tl, targetValue]);

  useEffect(() => { tl.seek(frame / fps); }, [frame, fps, tl]);

  return (
    <div style={{ fontSize: "64px", fontFamily: "monospace", fontWeight: "bold" }}>
      ${displayValue.toLocaleString()}
    </div>
  );
};
```
