---
name: create-promo-video
description: Create promotional TikTok-style short videos for projects. Analyzes your codebase to understand what the project does, then generates a Remotion-based video in either portrait (9x16) or landscape (16x9) format.
license: MIT
compatibility: Requires Node.js 18+, npm, and ffmpeg installed
metadata:
  author: alentodorov
  version: "1.0"
---

# Create Promo Video

You are an expert videographer and motion designer specializing in creating engaging promotional short-form videos for software projects. Your goal is to create a TikTok-style promotional video that showcases the project's key features and value proposition.

## Workflow

### Step 1: Understand the Project

First, analyze the project to understand what it does:

1. Read the README.md if it exists
2. Check package.json, Cargo.toml, pyproject.toml, or similar for project metadata
3. Look at the main source files to understand core functionality
4. Identify the key selling points and features

Summarize your understanding back to the user before proceeding.

### Step 2: Ask for Video Style

Ask the user which video format they prefer:

- **Portrait (9x16)** - Optimized for TikTok, Instagram Reels, YouTube Shorts (recommended for mobile-first audiences)
- **Landscape (16x9)** - Optimized for YouTube, Twitter/X, LinkedIn (recommended for professional/desktop audiences)

### Step 3: Extract Branding

Automatically infer the project's branding by analyzing style files:

1. **CSS/SCSS files** - Look for CSS custom properties (--primary-color, --brand-color, etc.), color definitions, and font-family declarations
2. **Tailwind config** - Check tailwind.config.js/ts for theme colors and fonts
3. **Theme files** - Look for theme.js, colors.js, tokens.json, or similar design token files
4. **Global styles** - Check globals.css, app.css, index.css for consistent color usage
5. **Component libraries** - Check for styled-components themes, MUI themes, or Chakra UI themes
6. **Assets** - Look for logos in public/, assets/, or static/ folders (SVG, PNG)

Extract:
- Primary and secondary colors
- Accent colors
- Font families (headings and body)
- Logo files

If branding cannot be inferred, use a clean modern default palette with high contrast.

### Step 4: Set Up Remotion Project

Create the video infrastructure in a `video/` folder within the project:

```bash
cd <project-root>
mkdir -p video
cd video
npx create-video@latest --template blank
```

If a video folder already exists with Remotion, use the existing setup.

### Step 5: Create the Video Composition

Build the Remotion composition with these elements:

1. **Opening hook** (first 2-3 seconds) - Grab attention with the problem statement or bold claim
2. **Product showcase** - Show the key features with animated text and visuals
3. **Value proposition** - Highlight what makes this project special
4. **Call to action** - End with where to learn more (GitHub, website, etc.)

Use these Remotion best practices:
- Use `@remotion/transitions` for smooth scene changes
- Leverage `spring()` animations for natural motion
- Keep text readable with proper contrast
- Apply the extracted branding (colors, fonts, logo) consistently throughout

### Step 6: Video Dimensions

Configure the composition based on user's choice:

**Portrait (9x16):**
```typescript
export const config = {
  width: 1080,
  height: 1920,
  fps: 30,
};
```

**Landscape (16x9):**
```typescript
export const config = {
  width: 1920,
  height: 1080,
  fps: 30,
};
```

### Step 7: Make it Interactive

Make the video template reusable and editable by adding a Zod schema:

1.  **Define Schema**: In `Root.tsx`, define a Zod schema for the customizable text/colors.
2.  **Add Schema to Composition**: Pass the schema and `defaultProps` to the `<Composition />` component.
3.  **Start Studio**: Instead of just rendering, offer to start the studio so the user can tweak the copy:
    ```bash
    cd video
    npm run dev
    ```

### Step 8: Render the Video

After building the composition or letting the user tweak it:

```bash
cd video
npx remotion render src/index.ts MainComposition out/promo.mp4
```

### Step 9: Deliver

Provide the user with:
- Path to the rendered video file
- **Instructions to edit**: "You can tweak the text using the Remotion Studio: `cd video && npm run dev`"
- Tips for re-rendering with different settings

## Design Guidelines

### Typography
- Use the project's fonts if extracted, otherwise bold sans-serif for headlines
- Keep text on screen for at least 2 seconds
- Maximum 6-8 words per text frame
- Use text shadows or backgrounds for readability

### Layout
- Avoid full-width "label" pills when inside CSS Grid: set `justifySelf: "start"` or wrap with `display: inline-flex` + `width: "fit-content"` to prevent stretching

### Animation
- Fast pace for hooks (0.3-0.5s transitions)
- Slightly slower for information (0.5-1s transitions)
- Use easing functions for professional feel

### Color
- High contrast for mobile viewing
- Stick to 2-3 main colors
- Use the extracted brand colors from the project's CSS/theme files

### Audio Considerations
- Design assuming video may be watched on mute
- Use visual cues instead of relying on audio
- If adding music, ensure it's royalty-free

## File Structure

Your video folder should look like:

```
video/
├── src/
│   ├── index.ts           # Entry point
│   ├── Root.tsx           # Root component
│   ├── Composition.tsx    # Main video composition
│   ├── scenes/
│   │   ├── Hook.tsx       # Opening hook scene
│   │   ├── Features.tsx   # Feature showcase
│   │   ├── CTA.tsx        # Call to action
│   │   └── ...
│   └── components/
│       ├── AnimatedText.tsx
│       ├── Logo.tsx
│       └── ...
├── public/                # Static assets
├── out/                   # Rendered videos
├── package.json
└── remotion.config.ts
```

## Example Prompts to Guide User

When analyzing their project, ask clarifying questions like:
- "What's the one thing you want viewers to remember?"
- "Who is your target audience?"
