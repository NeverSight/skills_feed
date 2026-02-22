---
name: blitzreels-carousels-instagram
description: Create Instagram feed carousel projects (still slides + text overlays) via the BlitzReels API.
---

# BlitzReels Carousels (Instagram)

This skill is a convenience wrapper around `blitzreels-carousels` with Instagram defaults:

- `platform: "instagram"`
- Recommended aspect ratio: `4:5` (feed portrait)
- Safe area preset: `instagram_4_5`

Use it when the user explicitly wants an Instagram feed carousel.

## Instagram Platform-Specific Guidelines

### Danger Zones (Absolute Pixels)

**For 4:5 Portrait (1080x1350):**
- **Bottom**: Avoid bottom 420px (username, caption preview, like/comment/share buttons)
- **Edges**: Keep text 80px from all edges (safe margins)

**For 1:1 Square (1080x1080):**
- **Bottom**: Avoid bottom 380px (captions, profile link)
- **Edges**: 80px margins on all sides

### Safe Text Positioning

**Normalized Coordinates (0-1 scale):**
- **Top-center safe**: `position_x: 0.5, position_y: 0.15` (titles, hooks)
- **Middle-center safe**: `position_x: 0.5, position_y: 0.45` (body text)
- **Bottom safe (max)**: `position_x: 0.5, position_y: 0.6` (before caption zone)

**Best Practices:**
- **Always center text** (`position_x: 0.5`) — Instagram's feed is symmetrical
- Use consistent vertical positioning across all slides (e.g., always `position_y: 0.18`)
- Leave generous bottom margin (users expect captions below image)

### Caption & Hashtag Strategy

**Captions:**
- First 125 characters visible without "more" tap
- Front-load value: "Swipe to learn..." or "Save this for later..."
- Use line breaks for readability (blank lines between sections)
- Call-to-action on last line: "📌 Save this post" or "👉 Follow for more"

**Hashtags:**
- Max 10-15 hashtags (30 max, but less is more)
- Mix sizes: 3 broad (500K+ posts) + 5 medium (50K-500K) + 2 niche (5K-50K)
- Place in first comment OR at end of caption after line breaks
- Example: `#digitalmarketing #marketingtips #contentcreator #socialmediatips #instagramgrowth`

### Visual Consistency Patterns

**Color Palette:**
- Cohesive feed aesthetic (e.g., all slides use same color scheme)
- Instagram users prefer clean, polished visuals (less chaotic than TikTok)
- Popular styles: minimalist white, pastel gradients, bold brand colors

**Typography:**
- Clean sans-serif fonts (Inter, Poppins, Manrope)
- 64-72px for titles, 48-56px for body
- Always enable text stroke for legibility (6px black/white)

**Slide Timing:**
- 3-4 seconds per slide (Instagram's default auto-advance)
- Keep total carousel under 20 seconds (5 slides max recommended)

**Slide Count Sweet Spot:**
- **3-5 slides**: Optimal for engagement
- **10 slides**: Max allowed, but engagement drops after slide 5

## Quickstart

```bash
export BLITZREELS_API_KEY="br_live_xxxxx"

bash scripts/instagram.sh \
  --aspect 4:5 \
  --name "My Instagram Carousel" \
  --images "https://.../1.jpg|https://.../2.jpg"
```

## Full Workflow Example

**Goal**: Create a 5-slide Instagram feed carousel explaining "How to Start a Podcast."

**Step 1: Prepare slide backgrounds**
- Slide 1: Gradient background (purple → pink) with podcast microphone icon
- Slides 2-4: White backgrounds with colored accent bars (consistent branding)
- Slide 5: Dark background with CTA

**Step 2: Run script**
```bash
bash scripts/instagram.sh \
  --aspect 4:5 \
  --name "How to Start a Podcast" \
  --slide-duration 3 \
  --images "url1|url2|url3|url4|url5" \
  --titles "How to Start a Podcast\n(5 Simple Steps)|Step 1: Choose Your Niche\nPick a topic you know well|Step 2: Get Equipment\nMic + headphones = $200|Step 3: Record & Edit\nUse Audacity (free)|Step 4: Publish\nAnchor, Spotify, Apple|📌 Save this guide!\nFollow @YourBrand for more"
```

**Step 3: Verify layout**
```bash
bash scripts/blitzreels.sh GET "/projects/${PROJECT_ID}/context?mode=timeline"
```

**Step 4: Export slideshow**
```bash
export BLITZREELS_ALLOW_EXPENSIVE=1
bash scripts/blitzreels.sh POST "/projects/${PROJECT_ID}/export" '{"resolution":"1080p","format":"mp4"}'
```

**Step 5: Upload to Instagram**
- Upload as carousel post (not Reel)
- Caption: "Starting a podcast is easier than you think. Swipe to see the 5 steps I used to launch mine →"
- Hashtags (first comment): `#podcasttips #startapodcast #podcasting #contentcreator #podcaster`
- Tag location if relevant (boosts reach)
- Post at peak times (11 AM - 1 PM, 7-9 PM user's timezone)

