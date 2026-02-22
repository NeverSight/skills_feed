---
name: mobile-app-design-mastery
description: "Production-grade mobile application UI design based on Refactoring UI principles. ALWAYS activate for: Flutter app, mobile app, iOS app, Android app, mobile UI, app screens, mobile navigation, bottom sheets, mobile forms, touch targets, mobile typography, app color scheme, mobile cards, list views, mobile modals, tab bars, app bars, floating action buttons. Provides mobile design workflow, touch-optimized spacing, mobile typography scale, platform-aware patterns. Turkish: mobil uygulama tasarımı, Flutter tasarım, uygulama arayüzü, mobil UI, telefon uygulaması, Android tasarım, iOS tasarım. English: app design, mobile interface, touch-friendly, native feel, mobile UX."
---

# Mobile App Design Mastery

Production-grade mobile UI design principles adapted from Refactoring UI for Flutter/native apps.

---

## Core Mobile Design Workflow

### 1. Start with a Screen, Not a Shell

- Design the core functionality of a single screen first
- Don't start with navigation, tab bars, or app chrome
- Work in greyscale first—add color after hierarchy is clear
- Design for the primary device size, then adapt

### 2. Establish Mobile Systems

**Spacing Scale (dp/logical pixels):**

| Token | Size | Use Case |
|-------|------|----------|
| xs | 4 | Micro gaps, icon padding |
| sm | 8 | Tight, within components |
| md | 12 | Related elements |
| base | 16 | Standard padding |
| lg | 24 | Between sections |
| xl | 32 | Major separation |
| 2xl | 48 | Screen margins on tablets |

**Touch Targets:**

| Platform | Minimum Size |
|----------|-------------|
| iOS | 44×44 pt |
| Android | 48×48 dp |
| Comfortable | 56×56 |

**Type Scale (sp/pt):**

| Size | Use Case |
|------|----------|
| 11-12 | Captions, labels |
| 14 | Body text, default |
| 16 | Emphasized body |
| 18-20 | Subheadings |
| 24 | Screen titles |
| 28-34 | Large titles (iOS style) |

**Shadow/Elevation Scale (dp):**

| Level | Elevation | Use Case |
|-------|-----------|----------|
| 0 | 0 | Flat surfaces |
| 1 | 1-2 | Cards, tiles |
| 2 | 4 | Raised buttons, app bar |
| 3 | 8 | Bottom sheets, dialogs |
| 4 | 16 | Navigation drawers |
| 5 | 24 | Modals |

### 3. Build Mobile Hierarchy

Mobile screens have limited space—hierarchy is even more critical.

- **Primary**: Key action/content (one per screen)
- **Secondary**: Supporting info (visible but not competing)
- **Tertiary**: Metadata, timestamps (smallest/lightest)

Key principles:

- Size matters more on mobile—but don't overdo it
- Use weight and color before increasing size
- Emphasize by de-emphasizing competing elements
- Icons need softer colors to balance with text

### 4. Design for Touch

- Generous touch targets (minimum 44pt/48dp)
- Adequate spacing between interactive elements
- Visual feedback on press (ripples, scale, opacity)
- Swipe actions for common operations

### 5. Apply Platform-Aware Depth

- **iOS**: Subtle shadows, blur/frosted glass, less elevation
- **Android**: Material elevation system, layered surfaces
- Use depth to indicate interactivity and focus

---

## Mobile Anti-Patterns

**NEVER do:**

- Touch targets smaller than 44×44
- Text smaller than 11sp (illegible)
- Grey text on colored backgrounds
- Ambiguous spacing between groups
- Full-width buttons edge-to-edge without padding
- Relying on color alone for meaning
- Ignoring safe areas (notch, home indicator)

---

## Reference Files

| Topic | File | When to Read |
|-------|------|--------------|
| Visual hierarchy, labels, emphasis | [mobile-hierarchy.md](references/mobile-hierarchy.md) | Balancing element importance |
| Spacing, touch targets, layout | [mobile-spacing.md](references/mobile-spacing.md) | Layout decisions |
| Typography, fonts, readability | [mobile-typography.md](references/mobile-typography.md) | Text styling |
| Color, themes, dark mode | [mobile-color.md](references/mobile-color.md) | Color system |
| Shadows, elevation, layers | [mobile-depth.md](references/mobile-depth.md) | Adding depth |
| Components, navigation, patterns | [mobile-patterns.md](references/mobile-patterns.md) | Platform-specific patterns |
