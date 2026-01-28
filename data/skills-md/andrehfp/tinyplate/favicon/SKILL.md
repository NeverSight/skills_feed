---
name: favicon
description: "Generate favicons and app icons for Next.js projects. Creates all required sizes, formats, and configures metadata."
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, WebFetch
---

# Favicon Generator

Generate complete favicon sets for Next.js projects.

## Workflow

### Step 1: Auto-Detect App Information

**IMPORTANT:** Before asking the user anything, scan the codebase to extract:

```bash
# Check these files in order:
```

#### 1. Package.json
```typescript
// Read package.json for name and description
{
  "name": "my-app",           // App name
  "description": "..."        // App description
}
```

#### 2. Next.js Metadata (app/layout.tsx)
```typescript
// Look for metadata export
export const metadata: Metadata = {
  title: "App Title",         // App name
  description: "...",         // App description
};

// Or metadataBase, applicationName
```

#### 3. README.md
```markdown
# App Name              <- Extract from H1
Description paragraph   <- Extract first paragraph
```

#### 4. Tailwind Config (tailwind.config.ts)
```typescript
// Look for custom colors in theme.extend.colors
theme: {
  extend: {
    colors: {
      primary: "#6366f1",    // Brand color
      brand: { ... }
    }
  }
}
```

#### 5. CSS Variables (app/globals.css)
```css
:root {
  --primary: #6366f1;        /* Brand color */
  --brand-color: ...;
}
```

#### 6. Existing Favicon/Icons
```bash
# Check if icons already exist
public/favicon.ico
public/apple-touch-icon.png
app/icon.tsx
app/icon.png
```

### Step 2: Present Findings & Confirm

After scanning, present what was found:

```
I found the following from your codebase:

App name: Striggo
Description: A study platform for professional certification exams
Brand color: #8b5cf6 (from Tailwind config)
Existing icons: None found

Should I generate a favicon based on this? Or would you like to customize?
```

Only ask questions if:
- App name is missing or unclear
- No brand colors found (suggest based on app type)
- User wants to override detected values

### Step 3: Choose Generation Method

Based on user input, choose one of these approaches:

---

## Option A: Generate from Description (No Source Image)

### A1: Text/Initial-Based Icon

Best for: Professional SaaS apps, clean minimal branding.

```typescript
// app/icon.tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";
export const contentType = "image/png";
export const size = { width: 32, height: 32 };

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          // Use app's primary brand color
          background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          borderRadius: 8,
          color: "white",
          fontSize: 20,
          fontWeight: 700,
          fontFamily: "system-ui, sans-serif",
        }}
      >
        {/* First letter or initials of app name */}
        S
      </div>
    ),
    { ...size }
  );
}
```

Create matching `apple-icon.tsx`:

```typescript
// app/apple-icon.tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";
export const contentType = "image/png";
export const size = { width: 180, height: 180 };

export default function AppleIcon() {
  return new ImageResponse(
    (
      <div
        style={{
          background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          borderRadius: 40,
          color: "white",
          fontSize: 100,
          fontWeight: 700,
          fontFamily: "system-ui, sans-serif",
        }}
      >
        S
      </div>
    ),
    { ...size }
  );
}
```

### A2: Emoji-Based Icon

Best for: Fun apps, MVPs, quick prototypes.

```typescript
// app/icon.tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";
export const contentType = "image/png";
export const size = { width: 32, height: 32 };

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          background: "#f8fafc",
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          borderRadius: 6,
          fontSize: 24,
        }}
      >
        {/* Choose emoji that represents the app */}
        🚀
      </div>
    ),
    { ...size }
  );
}
```

### A3: SVG Icon (Scalable, Dark Mode Support)

Best for: Technical apps, developer tools.

```typescript
// app/icon.tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";
export const contentType = "image/png";
export const size = { width: 32, height: 32 };

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          background: "#0f172a",
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          borderRadius: 6,
        }}
      >
        {/* Simple geometric shape or symbol */}
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="white"
          strokeWidth="2"
        >
          <path d="M12 2L2 7l10 5 10-5-10-5z" />
          <path d="M2 17l10 5 10-5" />
          <path d="M2 12l10 5 10-5" />
        </svg>
      </div>
    ),
    { ...size }
  );
}
```

### Design Guidelines by App Type

| App Type | Style | Colors | Icon Ideas |
|----------|-------|--------|------------|
| Finance/Banking | Minimal, professional | Blue, green, dark | Letter, shield, chart |
| Productivity | Clean, modern | Purple, blue | Checkmark, layers, grid |
| Social/Community | Friendly, warm | Orange, pink | Heart, people, chat |
| Developer Tools | Technical, dark | Dark gray, cyan | Terminal, brackets, code |
| E-commerce | Bold, trustworthy | Orange, blue | Cart, bag, tag |
| Health/Fitness | Energetic, fresh | Green, teal | Heart, leaf, pulse |
| Education | Approachable | Blue, yellow | Book, cap, lightbulb |

### Color Suggestions

Based on app purpose, suggest colors:

```typescript
const colorSchemes = {
  professional: "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)",
  creative: "linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%)",
  growth: "linear-gradient(135deg, #059669 0%, #10b981 100%)",
  energy: "linear-gradient(135deg, #ea580c 0%, #f59e0b 100%)",
  trust: "linear-gradient(135deg, #0284c7 0%, #06b6d4 100%)",
  minimal: "#0f172a", // Solid dark
  light: "#f8fafc",   // Solid light with colored icon
};
```

---

## Option B: Generate from Existing Source Image

### B1: Using Sharp (Recommended)

```bash
bun add sharp
```

```typescript
// scripts/generate-favicons.ts
import sharp from "sharp";
import { join } from "path";

const SOURCE = "source-icon.png";
const OUTPUT_DIR = "public";

const sizes = [
  { name: "favicon-16x16.png", size: 16 },
  { name: "favicon-32x32.png", size: 32 },
  { name: "apple-touch-icon.png", size: 180 },
  { name: "android-chrome-192x192.png", size: 192 },
  { name: "android-chrome-512x512.png", size: 512 },
];

async function generateFavicons() {
  for (const { name, size } of sizes) {
    await sharp(SOURCE)
      .resize(size, size)
      .png()
      .toFile(join(OUTPUT_DIR, name));
    console.log(`Generated: ${name}`);
  }

  // Create ICO
  await sharp(SOURCE)
    .resize(32, 32)
    .toFile(join(OUTPUT_DIR, "favicon.ico"));
}

generateFavicons();
```

### B2: Using ImageMagick

```bash
brew install imagemagick

# Generate all sizes
convert source.png -resize 16x16 public/favicon-16x16.png
convert source.png -resize 32x32 public/favicon-32x32.png
convert source.png -resize 180x180 public/apple-touch-icon.png
convert source.png -resize 192x192 public/android-chrome-192x192.png
convert source.png -resize 512x512 public/android-chrome-512x512.png
convert source.png -resize 32x32 -define icon:auto-resize=32,16 public/favicon.ico
```

---

## Step 3: Create Web Manifest

```json
// public/site.webmanifest
{
  "name": "APP_NAME",
  "short_name": "APP_SHORT",
  "description": "APP_DESCRIPTION",
  "icons": [
    {
      "src": "/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#PRIMARY_COLOR",
  "background_color": "#ffffff",
  "display": "standalone",
  "start_url": "/"
}
```

Or use dynamic manifest:

```typescript
// app/manifest.ts
import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "App Name",
    short_name: "App",
    description: "App description",
    start_url: "/",
    display: "standalone",
    background_color: "#ffffff",
    theme_color: "#6366f1",
    icons: [
      {
        src: "/android-chrome-192x192.png",
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: "/android-chrome-512x512.png",
        sizes: "512x512",
        type: "image/png",
      },
    ],
  };
}
```

## Step 4: Configure Metadata (if using static files)

```typescript
// app/layout.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "App Name",
  description: "App description",
  icons: {
    icon: [
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
    ],
    apple: [
      { url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
  },
  manifest: "/site.webmanifest",
};
```

## Interactive Flow

When running `/favicon`:

### 1. First, scan the codebase (silently):
```bash
# Read these files
cat package.json
cat app/layout.tsx
cat README.md
cat tailwind.config.ts
cat app/globals.css
ls public/favicon* app/icon* 2>/dev/null
```

### 2. Present findings:
```
I scanned your codebase and found:

  App name:     Striggo
  Description:  A study platform for professional certification exams
  Brand color:  #8b5cf6 (from tailwind.config.ts)
  Existing icons: None

I'll generate a favicon with:
- Letter "S" on purple gradient background
- Professional style (matching education/learning apps)

Proceed with this? Or customize (name/color/style)?
```

### 3. If info is missing, ask only what's needed:
```
I couldn't detect a brand color. What color should I use?
1. Purple (education/learning)
2. Blue (trust/professional)
3. Green (growth/success)
4. Custom hex code
> 1
```

### 4. Generate:
- `app/icon.tsx` - Dynamic 32x32 favicon
- `app/apple-icon.tsx` - Dynamic 180x180 Apple icon
- `app/manifest.ts` - PWA manifest
- Update `app/layout.tsx` with theme colors

## Files Checklist

### For Dynamic Icons (Option A)
```
app/
├── icon.tsx           # 32x32 favicon (generated)
├── apple-icon.tsx     # 180x180 Apple icon (generated)
└── manifest.ts        # PWA manifest
```

### For Static Icons (Option B)
```
public/
├── favicon.ico
├── favicon-16x16.png
├── favicon-32x32.png
├── apple-touch-icon.png
├── android-chrome-192x192.png
├── android-chrome-512x512.png
└── site.webmanifest
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Icon not updating | Clear cache, restart dev server |
| Apple icon not showing | Must be exactly 180x180 PNG |
| Dynamic icon 500 error | Check ImageResponse syntax |
| Emoji not rendering | Use system emoji font |
| Gradient looks wrong | Use standard CSS gradient syntax |
