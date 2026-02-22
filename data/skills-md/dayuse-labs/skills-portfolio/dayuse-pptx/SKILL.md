---
name: dayuse-pptx
description: Creates Dayuse-branded presentations (PPTX) with consistent visual identity and storytelling structure. Use when the user asks to create a presentation, deck, slides, pitch deck, roadmap, reporting, plan d'action, or any PPTX for Dayuse. Also use when user mentions "prez Dayuse", "deck Dayuse", "slides internes", "pitch hotel", or "presentation partenaire". Handles both external pitch decks and internal strategy/reporting presentations. Do NOT use for non-Dayuse presentations.
metadata:
  author: Dayuse
  version: 2.1.0
  category: document-creation
---

# Dayuse PPTX Skill

This skill creates Dayuse-branded presentations following the company's visual identity (sourced from the official Figma brand guidelines), storytelling framework, and slide patterns.

**Before creating any presentation, always also read the main `pptx` skill** for technical guidance on creating PPTX files with PptxGenJS.

### Figma Sources

| Resource | File Key | Content |
|----------|----------|---------|
| **Design System v2.0.3** | `1kQ21QwHaQxQrfR1Ozz7ys` | 187 icons (8 categories), colors, typography, components |
| **ICONS-LIBRARY** | `VYZeBPPWPcilQddvldU8w0` | Réassurance gradient + UI icon sets |
| **Image Bank** | `VU7niZDEMGOhmquJcpAk2P` | 35+ lifestyle photos (photoshoot June 2023) |
| **On-boarding Assets** | `XVlA3zCtO7jJ4GI4oaFLCV` | App screens, splash, UI components |

---

## Asset Catalog

All brand assets are organized in `assets/`. **ALWAYS use these real assets rather than generating placeholders.**

### Logos (assets/logos/)

| File | Description | Usage | Aspect Ratio |
|------|-------------|-------|--------------|
| `logo-gradient.png` | Wordmark "DAYUSE" in expressive gradient (jaune → orange → corail → bleu) | OOH, social, printed merch, expressive presentations. **Requires background removal preprocessing.** | 2:1 |
| `logo-black.png` | Wordmark "DAYUSE" in Evening Blue `292935` | Website, web banners, formal documents, toned-down communications | 2:1 |

### Icons / Symbols (assets/icons/)

| File | Description | Usage |
|------|-------------|-------|
| `icon-gradient.png` | "Y" symbol in sun gradient circle (jaune → orange → corail) | Expressive use: social media favicons, app icon contexts. **Can ONLY be used with the sun gradient.** |
| `icon-black.png` | "Y" symbol in Evening Blue circle | Functional use: slide footers, small placements, formal contexts |
| `icon-app.png` | App icon (Y symbol on rounded-square gradient background) | App references, product mockups |

### Image Bank (Figma — Photoshoot "New Brand June 2023")

**Source**: Figma file `VU7niZDEMGOhmquJcpAk2P`

The Dayuse Image Bank is the official repository of brand photography for all channels (CRM, Social Media, Website, presentations). It contains **35+ retouched, validated lifestyle photos** from the June 2023 brand photoshoot.

#### Photo Categories & Subjects

| Theme | Description | Example IDs | Usage in Slides |
|-------|-------------|-------------|-----------------|
| **Couple en chambre** | Couples in hotel rooms: bed, breakfast, petals, relaxation | DAYUSE0026, DAYUSE0085, DAYUSE0456 | Cover slides, lifestyle backgrounds, "experience" sections |
| **Piscine / Pool** | People in hotel pools, underwater shots, poolside | DAYUSE1876, DAYUSE2375, DAYUSE2059 | Leisure slides, amenities, summer campaigns |
| **Spa & Wellness** | Bathrobes, face masks, spa treatments, skincare | DAYUSE0060, DAYUSE0620, DAYUSE0064 | Wellness proposition, hotel amenities |
| **Sauna** | Couples in sauna, relaxation | DAYUSE0559, DAYUSE0620-2, DAYUSE0620-3 | Relaxation theme, hotel features |
| **Travail / Remote Work** | Business travelers with laptops in hotel settings | DAYUSE0143, DAYUSE0226 | "Work" use case, B2B slides, business travel |
| **Selfie & Fun** | Playful photos, selfies, confetti, rose petals | DAYUSE0801, DAYUSE2138, DAYUSE2202 | Social media references, fun/playful slides |
| **Marché Asie** | Asia-specific imagery (couples, luxury hotels) | Asia A, Asia B variants | APAC market slides, international expansion |

#### Available Photos (assets/photos/)

| File | Theme | Description |
|------|-------|-------------|
| `hero_girl_bed_room.jpg` | Chambre | Femme sur lit d'hôtel — hero/cover slide |
| `bed-1.jpg` | Chambre | Scène de chambre d'hôtel |
| `bath-2-1.jpg` | Spa/Wellness | Scène de salle de bain |
| `couplepool.jpg` | Piscine | Couple à la piscine |
| `girlpool.jpg` | Piscine | Femme à la piscine |
| `coupleontop.jpg` | Couple | Couple en extérieur |
| `frenchcouple_ontop.jpg` | Couple | Couple lifestyle |
| `girl_la_view_swimsuit.jpg` | Lifestyle | Femme avec vue panoramique |
| `dayuse_20_01_251245-1.jpg` | Brand shoot | Photo shoot officiel |
| `dayuse_20_01_251524-1.jpg` | Brand shoot | Photo shoot officiel |
| `dayuse_20_01_251693-2-1.jpg` | Brand shoot | Photo shoot officiel |

> **Note**: `POOL 1.png` (311 MB / 460M pixels) a été exclu car trop volumineux. Ré-exporter depuis Figma à ≤4000px de large.

#### Photo Style Guidelines (for Presentations)
- **Full-bleed**: Use photos as full-slide backgrounds for cover or closing slides
- **Half-bleed**: Photo on one half, content on the other (50/50 split)
- **Card crop**: Crop photos into rounded rectangles (`rectRadius: 0.12`) for cards
- **Overlay**: Photo with gradient text overlay (see `assets/brand-guide/images-best-practice.png`)
- **Always** use brand gradient band at bottom when photo is NOT full-bleed

```javascript
// Example — full-bleed photo background with text overlay:
slide.addImage({ path: "assets/photos/hero_girl_bed_room.jpg", x: 0, y: 0, w: 10, h: 5.625 });
// Add semi-transparent overlay for text readability:
slide.addShape(pptx.shapes.RECTANGLE, { x: 0, y: 3.5, w: 10, h: 2.125, fill: { color: "292935", transparency: 40 } });
slide.addText("Room to daydream.", { x: 0.6, y: 3.8, w: 8.8, fontSize: 36, fontFace: "Manrope", color: "FFFFFF", bold: true });
```

### On-boarding Assets (Figma Reference)

**Source**: Figma file `XVlA3zCtO7jJ4GI4oaFLCV` (node `445:3150`)

Contains mobile app onboarding screens, splash screens, and UI component variations. Useful as reference for:
- **Product mockups** in pitch decks (screenshot the app screens)
- **App UI illustrations** for product slides
- **Onboarding flow diagrams** for internal roadmap presentations

### Marketing Icons — "Réassurance Gradient" (assets/icons/marketing-icons.json)

**Source**: Figma ICONS-LIBRARY (`VYZeBPPWPcilQddvldU8w0`)

19 SVG icons with **brand gradient fills** (orange/coral/yellow). ViewBox 49x49. Used for pitch decks, marketing materials, value propositions. All icons are stored in a single JSON file: `assets/icons/marketing-icons.json` (key = icon name, value = SVG string).

| Key | Description | Usage |
|-----|-------------|-------|
| `business` | Bar chart with gradient bg | Business metrics, revenue |
| `customer` | User silhouette | Customer-related stats |
| `customer-service` | Headset agent | Support, service quality |
| `duo` | Two people | Couples, social |
| `diamond` | Diamond shape | Premium, luxury |
| `free-cancellation` | Calendar with cross | Cancellation policy |
| `gift` | Gift box | Promotions, offers |
| `hotel` | Building | Hotel count, partners |
| `house-traditional` | House | Alternative accommodations |
| `international` | Globe | International presence |
| `keys` | Keys | Access, bookings |
| `leader` | Trophy/medal | Market leadership |
| `location` | Map pin | Geographic coverage |
| `money` | Coins/bills | Revenue, savings |
| `no-card` | Crossed credit card | No card required |
| `rated` | Star rating | Reviews, ratings |
| `stats-lines` | Line chart | Growth trends |
| `stats-pipes` | Bar chart | Comparative data |
| `-75pct` | Discount tag | Discounts, savings |

### UI Icons — Design System (assets/icons/ui-icons.json)

**Source**: Figma Design System v2.0.3 — exported SVGs

184 SVG icons in **flat outline style** (stroke `#292935` Evening Blue). ViewBox 24x24. Used for all presentation contexts. All icons are stored in a single JSON file: `assets/icons/ui-icons.json` (key = icon name, value = SVG string).

**Naming convention** (keys in JSON):
- `nav-xxx` — UI navigation actions (arrows, check, cross, edit, trash, menu, etc.)
- `ind-xxx` — Status & feedback (alert, check, clock, discount, gift, info, lock, star, etc.)
- `xxx` (no prefix) — Amenities & features (wifi, pool, parking, spa, bed, tv, restaurant, etc.)

#### Icon Helper Functions

```javascript
const fs = require("fs");
const sharp = require("sharp");

// Load icon catalogs once
const UI_ICONS = JSON.parse(fs.readFileSync("assets/icons/ui-icons.json", "utf8"));
const MKT_ICONS = JSON.parse(fs.readFileSync("assets/icons/marketing-icons.json", "utf8"));

// UI icon → PNG (with optional recolor)
async function uiIconPng(name, color = "#292935", size = 128) {
  let svg = UI_ICONS[name];
  if (!svg) throw new Error(`UI icon "${name}" not found. Available: ${Object.keys(UI_ICONS).join(", ")}`);
  svg = svg.replace(/stroke="#292935"/g, `stroke="${color}"`);
  const buf = await sharp(Buffer.from(svg)).resize(size).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Marketing icon → PNG (gradient, use as-is)
async function marketingIconPng(name, size = 128) {
  const svg = MKT_ICONS[name];
  if (!svg) throw new Error(`Marketing icon "${name}" not found. Available: ${Object.keys(MKT_ICONS).join(", ")}`);
  const buf = await sharp(Buffer.from(svg)).resize(size).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Examples:
const wifiCoral = await uiIconPng("wifi", "#FDAA9A");          // coral
const starOrange = await uiIconPng("ind-star", "#F66236");     // orange
const checkWhite = await uiIconPng("nav-check", "#FFFFFF");    // white (for dark bg)
const alertPink = await uiIconPng("ind-alert", "#FF003E");     // hot pink
slide.addImage({ data: wifiTeal, x: 1, y: 1, w: 0.4, h: 0.4 });

const hotelIcon = await marketingIconPng("hotel");
slide.addImage({ data: hotelIcon, x: 1, y: 1, w: 0.5, h: 0.5 });
```

> **Recoloring**: UI icons use `stroke="#292935"` — easy to recolor via the `color` param. Marketing icons have **baked-in brand gradients** (linearGradient orange→coral→yellow) — use as-is.

### Brand Guide References (assets/brand-guide/)

These are exported Figma pages for visual reference when designing slides:

| File | Content |
|------|---------|
| `gradients-4types.png` | The 4 brand gradients (Generic, Primary, Complementary 1, Complementary 2) |
| `gradient-text-rules.png` | Rules for applying gradients ON text (direction: top-left → bottom-right) |
| `gradient-background-rules.png` | Rules for applying gradients AS backgrounds (direction: bottom-left → top-right) |
| `hq-gradients.png` | HQ angular gradients with background blur for key visuals |
| `typography-best-practice.png` | Font hierarchy: Maison Neue (H1), Manrope (H2/body), secondary text rules |
| `typography-colors.png` | Color/gradient usage on text with examples |
| `color-spectrum-values.png` | Color spectrum with emotional values (Liberté → Bien-être) |
| `color-inspiration-skies.png` | Sky photography inspiration for the brand palette |
| `layouts-best-practice.png` | Diverse layout examples (portrait, landscape, stories) |
| `images-best-practice.png` | Image + gradient text overlay example |

### Logo Usage Rules (from Figma Brand Guidelines)

**CRITICAL RULES:**
- The **symbol** (Y icon) and **wordmark** (DAYUSE text) each have their own place and time. **NEVER use them as a lock-up together** on the same element. They CAN appear on the same layout, but never combined as one unit.
- **Functional** (Evening Blue versions): for practical uses — website, small sizes, web banners, formal documents
- **Expressive** (Gradient versions): for expressive uses — OOH, social channels, printed merch, hero slides
- The **expressive core symbol** (icon-gradient) can **ONLY** be used with the sun gradient — never recolor it
- Always use the supplied artwork — **never try to recreate the wordmark**

---

## Step 0: Preprocess Assets (MANDATORY)

Run these steps BEFORE writing any slide code.

### Logo — Remove Black Background

The source logos (gradient versions) are RGB with a **black background**. They MUST be converted to transparent PNG before use, or they will display as an ugly black rectangle on slides.

```bash
python scripts/preprocess-logo.py assets/logos/logo-gradient.png /tmp/dayuse-logo-gradient.png
python scripts/preprocess-logo.py assets/icons/icon-gradient.png /tmp/dayuse-icon-gradient.png
```

Also prepare the black versions (which have white backgrounds to remove):
```bash
python scripts/preprocess-logo.py assets/logos/logo-black.png /tmp/dayuse-logo-black.png
python scripts/preprocess-logo.py assets/icons/icon-black.png /tmp/dayuse-icon-black.png
```

Then use `/tmp/dayuse-*.png` everywhere. NEVER use the raw asset files directly.

### ⚠️ CRITICAL — Image & Icon Aspect Ratio (NO DISTORTION)

**ALL images and icons MUST maintain their original aspect ratio.** Never set both `w` and `h` arbitrarily — always compute one from the other.

```javascript
const sharp = require("sharp");

// Helper: get image dimensions and compute correct placement
async function fitImage(imagePath, maxW, maxH) {
  const meta = await sharp(imagePath).metadata();
  const ratio = meta.width / meta.height;
  let w, h;
  if (ratio >= maxW / maxH) {
    // wider than slot → fit to width
    w = maxW;
    h = maxW / ratio;
  } else {
    // taller than slot → fit to height
    h = maxH;
    w = maxH * ratio;
  }
  return { w, h };
}

// For base64 data (icons from JSON), use the SVG viewBox or known ratio:
// UI icons: viewBox 24x24 → ratio 1:1 → ALWAYS use same w and h
// Marketing icons: viewBox 49x49 → ratio 1:1 → ALWAYS use same w and h
// Photos: use fitImage() helper above

// CORRECT — 1:1 icon
slide.addImage({ data: iconData, x: 1, y: 1, w: 0.5, h: 0.5 });

// CORRECT — photo fitted to slot
const { w, h } = await fitImage("assets/photos/couplepool.jpg", 4.5, 3.0);
slide.addImage({ path: "assets/photos/couplepool.jpg", x: 0.5, y: 1, w, h });

// WRONG — arbitrary w/h stretches the image
slide.addImage({ path: "assets/photos/couplepool.jpg", x: 0.5, y: 1, w: 4.5, h: 3.0 }); // DISTORTED!
```

**Rules:**
- **Icons** (UI + Marketing): Always square `w === h` (they are all 1:1 viewBox)
- **Photos**: Always use `fitImage()` helper or manually compute `h = w / ratio`
- **Logos**: Wordmark = 2:1, Symbol = 1:1 (see below)

### Logo — Respect the 2:1 Aspect Ratio (Wordmark Only)

The wordmark logos are 2000x1000px = **exactly 2:1 ratio**. Always maintain this ratio when placing:

```javascript
// CORRECT — 2:1 ratio maintained
const LOGO_W = 1.8;
const LOGO_H = LOGO_W / 2; // = 0.9
slide.addImage({ path: "/tmp/dayuse-logo-gradient.png", x: 0.6, y: 0.4, w: LOGO_W, h: LOGO_H });

// WRONG — distorted logo
slide.addImage({ path: logo, x: 0.6, y: 0.4, w: 1.8, h: 0.5 }); // squished!
```

Common sizes (all 2:1):
- Cover top-left: `w: 1.8, h: 0.9`
- Closing centered: `w: 1.4, h: 0.7`
- Small footer: `w: 1.0, h: 0.5`

### Icon Symbol — 1:1 Aspect Ratio

The symbol icons are circular = **exactly 1:1 ratio**:
- Slide footer symbol: `w: 0.35, h: 0.35`
- Cover accent: `w: 0.5, h: 0.5`

### Gradient Band

Create the Dayuse signature gradient band (jaune → orange → corail → bleu/vert) as a PNG image to place at the bottom of every slide:

```javascript
async function makeGradientBand(width = 2000, height = 12) {
  const svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
    <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FEB900"/>
      <stop offset="33%" stop-color="#FD7030"/>
      <stop offset="67%" stop-color="#FDAA9A"/>
      <stop offset="100%" stop-color="#B7D5D5"/>
    </linearGradient></defs>
    <rect width="${width}" height="${height}" fill="url(#g)"/>
  </svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Place at bottom of every content slide:
slide.addImage({ data: gradientData, x: 0, y: 5.525, w: 10, h: 0.1 });
```

### Gradient Backgrounds (for Section Slides)

The brand supports 4 gradient types for backgrounds. Use these for section divider slides (like WHY? / HOW? transitions):

```javascript
// Generic Gradient (full spectrum — for brand statement slides)
async function makeGenericGradientBg(width = 1920, height = 1080) {
  const svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
    <defs><linearGradient id="g" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FEB900"/>
      <stop offset="33%" stop-color="#FD7030"/>
      <stop offset="67%" stop-color="#FDAA9A"/>
      <stop offset="100%" stop-color="#B7D5D5"/>
    </linearGradient></defs>
    <rect width="${width}" height="${height}" fill="url(#g)"/>
  </svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Primary Gradient (warm tones — for energy/passion slides)
// #FEB900 → #FD7030 → #FDAA9A

// Complementary 1 (blues — for calm/wellness slides)
// #B7D5D5 → #7BBFCF → #3597C8

// Complementary 2 (corail → violet — for creative/experience slides)
// #FDAA9A → #C88AAE → #6E69AC
```

**DIRECTION RULE (from Figma):**
- Gradient on **text**: direction top-left → bottom-right (reading direction)
- Gradient as **background**: direction bottom-left → top-right

### Icons — Dayuse Custom Icon Library (187 icons)

**Full catalog**: See `references/icon-catalog.md` for the complete list of 187 icons with names, descriptions, and react-icons equivalents.

**Source**: Figma Design System v2.0.3 — Icons page (node `40:927`)

#### 8 Categories:

| Category | Count | Usage | Key Icons |
|----------|-------|-------|-----------|
| **Navigation** | 21 | UI chrome, arrows, actions | Chevron, Check, Cross, Menu, Filter, Edit, Trash, Map, Eye |
| **Indicators** | 33 | Status, feedback, badges | Circle check, Alert, Info, Star, Clock, Security, Gift, Sparkle |
| **Access** | 16 | Core app actions | Search, Place, Calendar, Home, Booking, Heart, User, Settings |
| **Search** | 6 | Transport/location types | City, Plane, Metro, Train, Hotel |
| **Interest & Social** | 15 | Sharing, social brands | Share, Copy, Link, Apple, Google, Facebook, Instagram, WhatsApp |
| **Hotel Amenities** | 46 | Hotel features | Pool, Wifi, Parking, Fitness, Spa, Restaurant, Elevator, Rooftop |
| **Hotel Room Amenities** | 38 | In-room features | Bed, TV, AC, Shower, Bathtub, Safe, Mini-bar, Kitchen, Iron |
| **Pool Amenities** | 11 | Pool features | Towels, Locker, Cabana, Sunscreen, Umbrella, Lounge chair |

#### How to use icons:

**Option 1 — Exported Dayuse icons (PREFERRED):**
If Dayuse SVG/PNG icons have been exported from Figma into `assets/icons/{category}/`, use those directly:
```javascript
slide.addImage({ path: "assets/icons/hotel-amenities/wifi.png", x: 1, y: 1, w: 0.4, h: 0.4 });
```

**Option 2 — react-icons fallback:**
When Dayuse icons aren't available as files, use `react-icons/fa` (Font Awesome) with Dayuse brand colors. Check `references/icon-catalog.md` for the react-icons equivalent of each Dayuse icon.

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaWifi, FaSwimmingPool, FaParking } = require("react-icons/fa");

async function iconPng(IconComponent, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// Usage with Dayuse palette colors:
const wifiIcon = await iconPng(FaWifi, "#FDAA9A");     // coral for amenities
const poolIcon = await iconPng(FaSwimmingPool, "#F66236"); // orange for leisure
const parkIcon = await iconPng(FaParking, "#FEB900");   // yellow for functional
slide.addImage({ data: wifiIcon, x: 1, y: 1, w: 0.4, h: 0.4 });
```

Install deps: `npm install -g react-icons react react-dom sharp`

#### Icon styling rules:
- **Style**: Outline/line icons (matching Dayuse custom style). Do NOT use filled/solid icons unless specifically named "Solid" in the catalog.
- **UI icons on slides**: May be placed inside **colored circles** (0.4-0.7" diameter) using Dayuse accent colors, OR used standalone
- **Marketing icons (gradient)**: Use **standalone ONLY** — NO colored circle, NO background shape behind them. They already have their own gradient fill and are self-contained.
- **Color on white bg** (UI icons): Use Evening Blue `292935` or accent colors (`F66236`, `FDAA9A`, `FEB900`, `FF003E`)
- **Color on dark bg** (UI icons): Use White `FFFFFF`
- **All icons are 1:1 ratio** — always use `w === h` when placing

---

## Step 1: Identify the Deck Type

Ask the user (if not clear) which type of deck they need:

| Type | Audience | Language | Tone |
|------|----------|----------|------|
| **Pitch externe** | Hoteliers, partenaires, investisseurs | EN or FR | Inspiring, desirable, business value |
| **Reporting interne** | Equipe, management, board | FR (primarily) | Data-driven, actionable, honest |
| **Roadmap / Plan d'action** | Equipe produit, strat, ops | FR | Vision-first, structured, progressive |
| **Analyse stratégique** | Management, cross-functional | FR | Analytical, insight-led, recommendation-oriented |

---

## Step 2: Apply the Dayuse Storytelling Framework

CRITICAL: Every Dayuse presentation follows a **"Vision-First"** narrative arc. Never start with details — always anchor in the WHY before the WHAT and HOW.

### Narrative Arc (applies to ALL deck types)

```
1. VISION / CONTEXTE  → Pourquoi on est là, la big picture
2. FRAMEWORK / METHODE → Comment on structure le sujet
3. DONNEES / PREUVES   → Les faits, analyses, résultats
4. INSIGHTS / SO WHAT  → Ce que ça veut dire concrètement
5. ACTION PLAN / NEXT  → Ce qu'on fait maintenant
```

### Structures par Type de Deck

**Pitch externe:**
1. Cover (titre + visuel lifestyle)
2. Dayuse in figures (crédibilité)
3. Proposition de valeur
4. Product demo / mockups
5. Business model
6. Marketing support
7. Contact / CTA

**Reporting interne:**
1. Titre + date + scope
2. Rappel vision / objectif
3. Vue synthétique KPIs
4. Deep dives par axe / marché
5. Insights clés
6. Action plan

**Roadmap / Plan d'action:**
1. Vision et ambition
2. Contexte et enjeux
3. Etapes clés + jalons temporels
4. Détail par étape
5. Next steps + ownership

**Analyse stratégique:**
1. Problématique et objectif
2. Framework / méthodologie
3. Données et résultats
4. Synthèse comparative
5. Recommandations

---

## Step 3: Apply Dayuse Visual Identity

### Color Palette

| Role | Color | Hex |
|------|-------|-----|
| **Texte principal / titres** | Evening Blue | `292935` |
| **Texte secondaire** | Gray | `54545D` |
| **Texte tertiaire** | Light Gray | `7F7F86` |
| **Accent principal (titres highlights, CTA)** | Orange | `F66236` |
| **Accent secondaire** | Coral | `FDAA9A` |
| **Accent tertiaire / urgence** | Hot Pink | `FF003E` |
| **CTA / boutons / énergie** | Yellow Gold | `FEB900` |
| **Fond encarts takeaway** | Rose pâle | `FFE5EA` |
| **Fond encarts bloc** | Beige clair | `F5F0E8` |
| **Fond cards** | Off-white | `F8F8F8` |

### Color Coding par Use Case
- Leisure = Coral `FDAA9A`
- Fonctionnel = Orange `F66236`
- Travel = Yellow `FEB900`
- Work = Hot Pink `FF003E`

### Accent Palette (5 couleurs)
Les 5 couleurs d'accent à utiliser pour les graphiques, badges, tags, cercles d'icônes :
- `FDAA9A` — Coral (doux, secondaire)
- `F66236` — Orange (principal, énergie)
- `FEB900` — Yellow Gold (CTA, attention)
- `FF003E` — Hot Pink (urgence, contraste)
- `FFE5EA` — Rose pâle (fonds, encarts)

> **Note** : les anciens bleus (`51B0B0`, `3597C8`) et le violet (`6E69AC`) ne font plus partie de la palette d'accent. Utiliser uniquement la gamme chaude ci-dessus.

### Color Spectrum (Emotional)
Le spectre de couleurs Dayuse représente un voyage émotionnel (de gauche à droite) :
- **Gauche (chaud)**: Liberté, Soleil, Joie, Bonheur, Intensité, Amour
- **Droite (frais)**: Bien-être, Ciel, Paisibilité, Calme, Temps pour soi, Ressource

### Contrast Rule (from Figma)
"Font should always maximise lisibility and strong contrast." Always alternate:
- **Dark text** (`292935`) on light backgrounds (`FFFFFF`, `F8F8F8`, gradients clairs)
- **White text** (`FFFFFF`) on dark backgrounds (`292935`), colored backgrounds (Yellow, Orange, Hot Pink), or gradient backgrounds

### BACKGROUND RULES (CRITICAL)

**Evening Blue (`292935`) is FORBIDDEN as a slide background.** It is a TEXT color only.

Allowed slide backgrounds:
- `FFFFFF` (white) — default for ALL content slides
- `F8F8F8` (off-white) — subtle variation
- **Brand gradient** backgrounds — for section divider slides ONLY (WHY? / HOW? transitions)
- `FEB900` (yellow) — for bold statement slides (e.g. "Only 3% of French people have heard of Dayuse")
- A lifestyle **photo** as full-bleed background (for closing slides)

The only exception where `292935` can be used as a SHAPE fill (not slide bg) is for small accent elements like the "Victor Barnouin" card or data pill badges.

---

### Typography — Manrope Only (Google Slides Compatible)

**IMPORTANT:** The Figma brand guidelines specify Maison Neue Extended Bold for H1 titles, but since Dayuse presentations are delivered via **Google Slides**, Maison Neue is NOT available and NOT editable there. Therefore ALL text uses **Manrope** (Google Font, fully compatible with Google Slides).

The hierarchy below adapts the Figma brand sizing/weight rules to Manrope only.

#### Title Level 1 (Hero): Manrope ExtraBold
For hero titles, section divider text, bold statements. Replaces Maison Neue in PPTX context.

```
Font: Manrope ExtraBold (weight 800)
Size: 36-48pt
Line Height: tight (1.1x)
Letter Spacing: 0%
Color: 292935 (or FFFFFF on dark/gradient backgrounds)
```

#### Title Level 2 (Slide Title): Manrope Bold
For slide titles, section sub-headers. The "insight title" used on most content slides.

```
Font: Manrope Bold (weight 700)
Size: 24-30pt
Line Height: 1.2x
Letter Spacing: 0%
Color: 292935 (key words in F66236)
```

#### Subtitle: Manrope SemiBold
For slide subtitles, chapeau text above titles.

```
Font: Manrope SemiBold (weight 600)
Size: 16-20pt
Line Height: 1.3x
Letter Spacing: 0%
Color: 54545D
```

#### Running Text: Manrope Regular
For body text, descriptions, explanations.

```
Font: Manrope Regular (weight 400)
Size: 12-14pt
Line Height: 22
Letter Spacing: 1%
Color: 54545D
```

#### Secondary Text: Manrope Bold (FULL CAPS)
For CTAs, signatures, chapeau labels, important secondary messages. **Always uppercase with letter spacing.**

```
Font: Manrope Bold (weight 700)
Size: variable (typically 10-14pt)
Letter Spacing: 17%
Transform: UPPERCASE
Color: 292935 or 7F7F86
```

Example: `MADE WITH LOVE AT DAYUSE` / `ROOM TO DAYDREAM` / `VIEW OUR HOTELS`

### Full Typography Reference Table

| Element | fontFace | Size | Weight | Color | Notes |
|---------|----------|------|--------|-------|-------|
| Hero title (H1) | `"Manrope"` | 36-48pt | 800 (ExtraBold) | `292935` | Section dividers, covers. Can use gradient as image mask |
| Slide title (H2) | `"Manrope"` | 24-30pt | 700 (Bold) | `292935` | Key words in `F66236` |
| Subtitle | `"Manrope"` | 16-20pt | 600 (SemiBold) | `54545D` | |
| Body text | `"Manrope"` | 12-14pt | 400 (Regular) | `54545D` | Line height 22, spacing 1% |
| Labels / captions | `"Manrope"` | 10-11pt | 500 (Medium) | `7F7F86` | |
| Big KPI numbers | `"Manrope"` | 36-48pt | 700 (Bold) | `292935` | |
| Label under KPI | `"Manrope"` | 11pt | 400 (Regular) | `7F7F86` | |
| CTA / Signature | `"Manrope"` | 11-12pt | 700 (Bold) | `292935` | FULL CAPS, 17% letter spacing |
| CTA button text | `"Manrope"` | 11-12pt | 700 (Bold) | `FFFFFF` | Inside colored shape |
| Section divider text | `"Manrope"` | 60-80pt | 800 (ExtraBold) | `FFFFFF` | On gradient backgrounds |
| Orange highlight words | `"Manrope"` | same as parent | 700 (Bold) | `F66236` | Within titles only |

### Titre-Insight Pattern (OBLIGATOIRE)

Every slide title MUST be an **insight** (a conclusion), NOT a descriptive label.

```
WRONG: "Analyse USA"
RIGHT: "Les hôtels Travel drivent la dynamique nouveaux clients."

WRONG: "Résultats Q3"
RIGHT: "Le Travel comme générateur de valeur : +59% de croissance."

WRONG: "Distribution hôtel"
RIGHT: "Un parc mondial principalement Fonctionnel aujourd'hui."
```

Implementation: **Title text in Evening Blue bold + key words in Orange bold** to guide the eye.

```javascript
slide.addText([
  { text: "L'IA gère le ", options: { fontSize: 26, fontFace: "Manrope", color: "292935", bold: true } },
  { text: "volume", options: { fontSize: 26, fontFace: "Manrope", color: "F66236", bold: true } },
  { text: ", l'humain gère ", options: { fontSize: 26, fontFace: "Manrope", color: "292935", bold: true } },
  { text: "l'exception.", options: { fontSize: 26, fontFace: "Manrope", color: "F66236", bold: true } },
], { x: 0.6, y: 0.3, w: 8.8, h: 0.8, margin: 0 });
```

---

### The 4 Brand Gradients

Reference: `assets/brand-guide/gradients-4types.png`

| Gradient | Colors | When to Use |
|----------|--------|-------------|
| **Generic** | `#FEB900` → `#FD7030` → `#FDAA9A` → `#B7D5D5` | Brand statements, logo, signature elements. Full spectrum = balance between all polarities |
| **Primary** | `#FEB900` → `#FD7030` → `#FDAA9A` | Affirm brand identity simply. Use when energy/intensity is the message. "Be careful, sometimes it's too hot to be used" |
| **Complementary 1** | Blues/teals spectrum | Balance in an ensemble of visual, webpage, brochure pages |
| **Complementary 2** | Corail → Violet | Balance in an ensemble of visual, webpage, brochure pages |

### Gradient Usage Rules (from Figma)

1. **On text**: Direction top-left → bottom-right (reading direction). Gradients can ONLY be used on **hero titles (Manrope ExtraBold 800)** as a title or main message. **Never apply gradient to body text or secondary elements.**
2. **On backgrounds**: Direction bottom-left → top-right. Should generally NOT be used with an image on top (exception: for balance).
3. **HQ Gradients**: For key visuals, use angular gradients with background blur overlay. These create a more diffuse, organic look suited for non-print, non-functional use.

### Gradient Text in PptxGenJS

Since PptxGenJS doesn't natively support gradient text, simulate it by rendering gradient text as a PNG image:

```javascript
async function makeGradientText(text, fontSize = 80, width = 1920, height = 300) {
  const svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#FEB900"/>
        <stop offset="33%" stop-color="#FD7030"/>
        <stop offset="67%" stop-color="#FDAA9A"/>
        <stop offset="100%" stop-color="#B7D5D5"/>
      </linearGradient>
    </defs>
    <text x="0" y="${fontSize}" font-family="Manrope, Arial Black, sans-serif"
          font-weight="800" font-size="${fontSize}px" fill="url(#textGrad)">
      ${text}
    </text>
  </svg>`;
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
```

---

### Slide Patterns

**1. Slide Cover**
- Fond BLANC
- Logo wordmark (gradient or black) en haut à gauche (2:1 ratio, transparent)
- Titre en **Manrope ExtraBold** 36-48pt, Evening Blue
- Sous-titre et auteur en Manrope Regular gris `54545D`
- Bandeau gradient en bas

**2. Slide Section Divider (Gradient Background)**
- Full-bleed gradient background (Generic or Primary)
- Gros texte centré en **Manrope ExtraBold** 60-80pt, BLANC
- Sous-texte en Manrope SemiBold, BLANC
- NO gradient band at bottom (gradient IS the background)
- Use for WHY? / HOW? / WHAT? transitions

**3. Slide Bold Statement (Yellow Background)**
- Full-bleed `FEB900` yellow background
- Titre en Manrope Bold 14pt noir en chapeau
- Statement en **Manrope ExtraBold** 36-44pt noir
- Description en Manrope Regular 14pt noir
- NO gradient band (colored bg)

**4. Slide Titre de Section**
- Fond gris clair (`E8E8E8`) sur la moitié gauche
- Nom de section en gros, en gradient (utiliser le gradient comme image)
- Contenu sur la moitié droite, fond blanc

**5. Slide KPI / Chiffres Clés**
- Icônes dans des cercles colorés
- Gros chiffre (36-48pt, bold, `292935`)
- Label sous le chiffre (11pt, `7F7F86`)
- Grille 2x3 ou 3x2

**6. Slide Matrice / Tableau**
- Pastilles arrondies foncées (`292935`) avec texte blanc
- Pastilles colorées pour les highlights
- Encart takeaway rose pâle en bas

**7. Slide Graphique**
- Deux graphiques côte à côte quand possible
- Bullets d'insights sous chaque graphique
- Titre-insight en haut

**8. Slide Roadmap / Timeline**
- Etapes numérotées dans des encarts fond léger
- Badges de timing colorés (Q1, Q2-Q3...)
- Ligne verticale de connexion entre les étapes

**9. Slide Cards (3 colonnes)**
- 3 cards `ROUNDED_RECTANGLE` en `F8F8F8`
- Icône dans cercle coloré centré en haut
- Titre bold centré
- Items avec check icons

**10. Slide Vision/Quote (from Brand Platform style)**
- Fond blanc
- Barre gradient verticale gauche (thin, ~0.15" wide, full height)
- Chapeau en Manrope Bold UPPERCASE + small icon: `OUR VISION`, `OUR MISSION`
- Grande citation en **Manrope ExtraBold** 28-36pt
- Description en Manrope Regular 14pt
- Symbol icon (black) en bas à droite footer
- Bandeau gradient en bas

**11. Slide Photo + Text Overlay**
- Lifestyle photo as partial or full background
- Gradient text overlay using Manrope ExtraBold
- CTA button with gradient or white background
- Logo wordmark bottom-center
- Reference: `assets/brand-guide/images-best-practice.png`

**12. Slide Closing**
- Fond BLANC (ou photo lifestyle plein écran)
- Logo centré (2:1 ratio, transparent)
- Message de closing with accent orange
- CTA buttons en orange
- Bandeau gradient en bas

### Elements Visuels Récurrents

- **Bandeau gradient** en bas de CHAQUE slide blanc (0.1" height). NOT on gradient/colored bg slides.
- **Barre gradient verticale gauche** : thin stripe (~0.15") on the left edge for vision/quote slides
- **Encarts takeaway rose** (`FDE8E4`) pour conclusions/punchlines
- **Pastilles données** : rounded rect `292935` avec texte blanc
- **Cercles colorés** autour des icônes (0.4-0.7" diameter)
- **CTA buttons** : rounded rect orange `F66236` avec texte blanc bold
- **Cards** : `ROUNDED_RECTANGLE`, `rectRadius: 0.1-0.12`, fill `F8F8F8`
- **UPPERCASE secondary text** : Manrope Bold, 17% letter spacing, for signatures/CTAs

### Layout Rules

- Marges : minimum 0.5" de chaque côté
- Espacement entre blocs : 0.3-0.4"
- Texte aligné à gauche (sauf titres centrés sur cover/section dividers)
- JAMAIS de ligne d'accent sous les titres (hallmark AI)
- Varier les layouts (pas 3x le même layout consécutif)
- Chaque slide a au moins 1 élément visuel (icône, shape, chart, gradient element)
- "The brand is meant to live with diverse and exploratory layouts" — don't be repetitive

---

## Step 4: Build the Presentation

1. Confirm deck type, audience, content with user
2. Propose structure de slides (titres-insights) pour validation
3. **Preprocess assets** : logo transparency + gradient band + gradient backgrounds
4. Build PPTX via `pptx` skill PptxGenJS workflow
5. Apply ALL Dayuse visual identity rules
6. QA via pptx skill verification process

---

## Step 5: Quality Checklist

Before delivering, verify ALL of these:

- [ ] Titres = insights (pas descriptifs)
- [ ] Mots-clés en orange `F66236`
- [ ] Palette Dayuse respectée
- [ ] **AUCUN fond Evening Blue** — tous blancs, off-white, gradient, ou yellow
- [ ] **Font = Manrope partout** (ExtraBold 800 pour H1, Bold 700 pour H2, Regular pour body)
- [ ] **Secondary text in FULL CAPS** with letter spacing (signatures, CTAs, chapeaux)
- [ ] **Logo transparent** et **ratio respecté** (2:1 wordmark, 1:1 symbol)
- [ ] **Logo and symbol never used as a lock-up** — never combined in one element
- [ ] **Gradient direction correct**: text = top-left→bottom-right, background = bottom-left→top-right
- [ ] Bandeau gradient en bas de chaque slide blanc (NOT on gradient/colored bg slides)
- [ ] Gros chiffres 36pt+ bold
- [ ] Arc narratif Vision-First respecté
- [ ] Pas de slide text-only (every slide has a visual element)
- [ ] Encarts takeaway rose pour conclusions
- [ ] Section dividers use gradient backgrounds with large white Manrope ExtraBold text
- [ ] Slide de fin avec logo + CTA
- [ ] Langue correcte (FR interne, EN/FR externe)
- [ ] Contrast rule applied (dark text on light bg, white text on dark/colored bg)

---

## Troubleshooting

**Logo avec fond noir rectangulaire :**
→ Script preprocessing non exécuté. Lancer `python scripts/preprocess-logo.py assets/logos/logo-gradient.png /tmp/dayuse-logo-gradient.png`

**Logo déformé / écrasé :**
→ Ratio non respecté. Wordmark: `h = w / 2`. Symbol: `h = w`.

**Font ne s'affiche pas :**
→ Manrope non installée sur la machine cible. Installer depuis Google Fonts. Google Slides la supporte nativement.

**Gradient text doesn't render :**
→ PptxGenJS ne supporte pas le texte gradient nativement. Utiliser la fonction `makeGradientText()` pour générer un PNG. Vérifier que `sharp` est installé.

**Icônes invisibles (blanches sur blanc) :**
→ Les icônes blanches doivent être dans un cercle coloré. Ne jamais placer une icône blanche directement sur fond blanc.

**SVG icons depuis JSON :**
→ Les icônes sont dans `ui-icons.json` et `marketing-icons.json`. Utiliser les helpers `uiIconPng(name)` et `marketingIconPng(name)`. Les clés sont sans extension : `"wifi"`, `"nav-check"`, `"ind-star"`, `"hotel"`.

**Photo trop lourde / lente :**
→ Les photos haute-res peuvent ralentir le PPTX. Utiliser `sharp` pour redimensionner avant insertion : `sharp(photo).resize(1920).jpeg({ quality: 80 })`.

**SVG icons invisible sur fond blanc :**
→ Les icônes UI sont en stroke `#292935`. Sur fond blanc elles sont visibles. Si nécessaire, recolorer le stroke dans le SVG avant conversion PNG.

**Deck manque d'impact :**
→ Chaque slide doit avoir un élément visuel
→ Augmenter contraste titre (32pt+) vs corps (14pt)
→ Utiliser encarts colorés pour takeaways
→ Ajouter au moins 1-2 section dividers avec gradient background

**Storytelling plat :**
→ Revérifier arc Vision-First
→ Titres = conclusions, pas sujets
→ Ajouter transitions entre sections (gradient divider slides)
→ Use bold statement slides (yellow bg) for impactful data points
