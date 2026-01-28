---
name: brand-guidelines
description: IdeaForge brand identity - colors, typography, and visual guidelines. Use when styling UI components, creating marketing materials, or ensuring brand consistency.
---

# IdeaForge Brand Guidelines

## Brand Identity

**Name**: IdeaForge
**Tagline**: AI-Powered Idea Generation
**Personality**: Innovative, Inspiring, Data-Driven, Professional

**Target Audience**: Startup founders seeking AI-assisted business idea generation and evaluation.

## Colors

### Primary Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Mint** | `#34D399` | rgb(52, 211, 153) | Primary brand color, CTAs, logo |
| **Mint Dark** | `#10B981` | rgb(16, 185, 129) | Hover states, gradients |
| **Coral** | `#FF6B6B` | rgb(255, 107, 107) | Text accents, highlights, alerts |

### Background Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Dark Base** | `#0f1419` | rgb(15, 20, 25) | Primary dark background |
| **Dark Surface** | `#1c2128` | rgb(28, 33, 40) | Cards, elevated surfaces |
| **Dark Elevated** | `#262c36` | rgb(38, 44, 54) | Hover states, borders |

### Text Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Text Primary** | `#f0f6fc` | rgb(240, 246, 252) | Primary text on dark |
| **Text Secondary** | `#8b949e` | rgb(139, 148, 158) | Secondary text, labels |
| **Text Muted** | `#6e7681` | rgb(110, 118, 129) | Disabled, placeholder |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Success** | `#34D399` | Positive actions, success states |
| **Warning** | `#FBBF24` | Warnings, caution |
| **Error** | `#EF4444` | Errors, destructive actions |
| **Info** | `#67E8F9` | Information, tips |

### Button Colors

| Type | Style |
|------|-------|
| **Primary** | Background: gradient `#34D399` → `#10B981`, Text: `#0f1419` |
| **Secondary** | Background: transparent, Border: `rgba(255,255,255,0.3)`, Text: `#f0f6fc` |
| **Ghost** | Background: transparent, Text: `#34D399` |
| **Danger** | Background: `#EF4444`, Text: `#ffffff` |

## Typography

### Font Stack

```css
/* Headings */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;

/* Body */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;

/* Code/Data */
font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;
```

### Type Scale

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 2.5rem (40px) | 700 | 1.2 |
| H2 | 2rem (32px) | 600 | 1.25 |
| H3 | 1.5rem (24px) | 600 | 1.3 |
| H4 | 1.25rem (20px) | 600 | 1.4 |
| Body | 1rem (16px) | 400 | 1.6 |
| Small | 0.875rem (14px) | 400 | 1.5 |
| Caption | 0.75rem (12px) | 500 | 1.4 |

## Tailwind CSS Classes

### Common Patterns

```tsx
// Primary Button
className="bg-gradient-to-r from-emerald-400 to-emerald-500 text-gray-900 font-semibold px-6 py-3 rounded-lg hover:from-emerald-300 hover:to-emerald-400 transition-all"

// Secondary Button
className="border border-white/30 text-gray-100 px-6 py-3 rounded-lg hover:bg-white/5 transition-all"

// Card
className="bg-gray-800/50 rounded-xl p-6 border border-gray-700/50"

// Text Accent
className="text-red-400" // For coral accent on text

// Stats/Numbers
className="text-emerald-400 font-bold text-2xl"

// Background
className="bg-gradient-to-br from-gray-900 to-gray-800"
```

### Dark Mode (Default)

IdeaForge uses dark mode as the primary theme. All components should be designed dark-first.

```tsx
// Standard background layers
bg-[#0f1419]      // Base
bg-[#1c2128]      // Surface
bg-[#262c36]      // Elevated

// Or using Tailwind
bg-gray-900       // Base
bg-gray-800       // Surface
bg-gray-700       // Elevated
```

## Spacing

Base unit: 4px

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Tight spacing |
| sm | 8px | Between related elements |
| md | 16px | Default padding |
| lg | 24px | Section padding |
| xl | 32px | Major sections |
| 2xl | 48px | Page sections |

## Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| sm | 4px | Buttons, inputs |
| md | 8px | Cards, containers |
| lg | 12px | Modals, large cards |
| xl | 16px | Hero sections |
| full | 9999px | Pills, avatars |

## Shadows

```css
/* Subtle */
box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);

/* Card */
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);

/* Elevated */
box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3);

/* Glow (for primary elements) */
box-shadow: 0 0 20px rgba(52, 211, 153, 0.3);
```

## Component Examples

### Score Badge

```tsx
// High score (80-100)
className="bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded text-sm font-medium"

// Medium score (50-79)
className="bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded text-sm font-medium"

// Low score (0-49)
className="bg-red-500/20 text-red-400 px-2 py-1 rounded text-sm font-medium"
```

### Navigation

```tsx
className="bg-gray-900/95 backdrop-blur border-b border-gray-800"
```

### Input Fields

```tsx
className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-gray-100 placeholder-gray-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
```

## Logo Usage

- Primary color: Mint `#34D399`
- Can be displayed on dark backgrounds only
- Minimum clear space: height of logo on all sides
- Do not distort, rotate, or add effects

## Voice & Tone

- **Professional but approachable** - Not stiff, not casual
- **Action-oriented** - "Generate ideas", "Start exploring"
- **Confident** - Emphasize AI capabilities without overpromising
- **Concise** - Data-dense UI means minimal text

## Anti-Patterns

Avoid:
- Light/white backgrounds as primary
- Generic blue (#007bff) as primary color
- Gradients using coral/red (reserve for text accents only)
- Low contrast text combinations
- Excessive animations
- Purple gradients (overused in AI products)