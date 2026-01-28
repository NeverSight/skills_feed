---
name: design-guide
description: Ensures modern, professional UI design across SwiftUI, Android, and web platforms. Use when building ANY user interface components including buttons, forms, cards, layouts, navigation, or complete screens. Enforces clean minimal design, neutral color palettes with one accent color, 8px grid spacing system, proper typography hierarchy, and clear interactive states. Always reference before creating or modifying UI elements.
---

# Design Guide

Comprehensive design system ensuring every UI you build looks modern, professional, and consistent across all platforms (SwiftUI, Android Studio, web applications).

## Bundled Resources

This skill includes additional reference materials:

- **references/color-palettes.md** - Detailed color schemes, accent color options, and platform-specific color implementation examples. Reference when choosing or implementing colors.
- **references/component-templates.md** - Ready-to-use code templates for buttons, cards, forms, and navigation across SwiftUI, Android Compose, and React. Reference when implementing specific components.

## Core Design Principles

### 1. Clean and Minimal
- Embrace white space generously
- Avoid cluttered interfaces
- One primary action per screen/section
- Remove unnecessary decorative elements
- Let content breathe

### 2. Color Palette

**Neutral Base:**
- Use grays and off-whites as foundation
- White: #FFFFFF
- Light gray: #F5F5F5, #EEEEEE
- Medium gray: #9E9E9E, #757575
- Dark gray: #424242, #212121
- True black sparingly: #000000

**Accent Color:**
- Choose ONE accent color for your app
- Use sparingly for CTAs, important actions, and key information
- Good accent options: Emerald (#10B981), Indigo (#6366F1), Rose (#F43F5E), Amber (#F59E0B)
- **NEVER use generic purple/blue gradients**

**Color Usage Rules:**
- 80% neutral, 15% secondary neutral, 5% accent
- Backgrounds: light grays or white
- Text: dark grays on light backgrounds
- Interactive elements: accent color
- Borders/dividers: very light gray (#E5E5E5)

### 3. Spacing System (8px Grid)

**Always use multiples of 8:**
- 8px: Tight spacing (icon padding, inline elements)
- 16px: Standard spacing (button padding, form field gaps)
- 24px: Section spacing (card internal padding)
- 32px: Component spacing (between cards, sections)
- 48px: Major section breaks
- 64px: Screen-level spacing (margins)

**Application:**
- Padding: 16px or 24px for most containers
- Margins: 32px between major sections
- Gap between elements: 16px standard, 8px for tight groups
- Never use arbitrary values like 13px or 27px

### 4. Typography

**Hierarchy:**
- H1: 32px - 40px, bold, rare (page titles only)
- H2: 24px - 28px, semibold (section headers)
- H3: 20px - 24px, semibold (subsections)
- Body: 16px - 18px, regular (MINIMUM 16px for readability)
- Small: 14px, regular (captions, metadata)
- Tiny: 12px, regular (legal text only, use rarely)

**Font Rules:**
- Maximum 2 font families per project
- One for headings (can be display font)
- One for body text (must be highly readable)
- Recommended pairings:
  - Inter + Inter (single family, different weights)
  - SF Pro Display + SF Pro Text (Apple platforms)
  - Roboto + Roboto (Android)
  - System fonts always acceptable

**Line Height:**
- Headings: 1.2 - 1.3
- Body: 1.5 - 1.6
- Small text: 1.4

### 5. Shadows

**Subtle, not heavy:**
- Small shadow: `0 1px 3px rgba(0,0,0,0.12)`
- Medium shadow: `0 4px 6px rgba(0,0,0,0.1)`
- Large shadow: `0 10px 15px rgba(0,0,0,0.1)`
- Floating shadow: `0 20px 25px rgba(0,0,0,0.1)`

**When to use:**
- Cards: subtle shadow or border, not both
- Buttons: very subtle shadow on hover
- Modals/dialogs: medium shadow
- Dropdowns: medium shadow
- **Avoid:** heavy drop shadows, inner shadows, multiple shadows

### 6. Rounded Corners

**Border Radius Guidelines:**
- Small elements (buttons, inputs): 6px - 8px
- Cards, containers: 8px - 12px
- Large panels: 12px - 16px
- Circular (avatars, icon buttons): 50% or 9999px

**Don't overdo it:**
- Not everything needs rounded corners
- Sharp corners acceptable for:
  - Screen edges
  - Full-width sections
  - Data tables
  - Navigation bars

### 7. Interactive States

**Every interactive element MUST have:**

**Buttons:**
- Default: base color, subtle shadow
- Hover: slightly darker (10%), lift shadow
- Active: pressed appearance, darker (20%)
- Disabled: 40% opacity, no hover, no pointer cursor
- Focus: visible outline (2px accent color, 2px offset)

**Form Fields:**
- Default: light gray border (#E5E5E5)
- Focus: accent color border (2px), remove shadow
- Error: red border, error text below
- Disabled: gray background, no interaction
- Valid: subtle green checkmark (optional)

**Links:**
- Default: accent color, underline on hover
- Visited: slightly muted accent
- Never: blue #0000FF (unless that's your accent)

**Cards:**
- Default: subtle shadow or border
- Hover: lift effect, slightly stronger shadow
- Active: immediate feedback

### 8. Mobile-First Thinking

**Always design for mobile first, then scale up:**
- Touch targets minimum 44x44px (iOS), 48x48px (Android)
- Adequate spacing between tappable elements (min 8px)
- Thumb-friendly navigation (bottom of screen)
- Single column layouts on mobile
- Responsive breakpoints:
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px

## Component Patterns

### Buttons

**Primary Button (main action):**
```
Background: Accent color
Text: White
Padding: 12px 24px (vertical, horizontal)
Border radius: 8px
Shadow: 0 1px 3px rgba(0,0,0,0.12)
Font: 16px, semibold
Hover: Darken 10%, lift shadow
```

**Secondary Button (alternative action):**
```
Background: White
Text: Accent color
Border: 1px solid accent color
Padding: 12px 24px
Border radius: 8px
Hover: Light accent background (10% opacity)
```

**Ghost Button (tertiary action):**
```
Background: Transparent
Text: Dark gray
No border
Padding: 12px 24px
Hover: Light gray background
```

**Bad Button Examples:**
- ❌ Gradient backgrounds
- ❌ Multiple colors in one button
- ❌ Tiny padding (looks cramped)
- ❌ No hover state
- ❌ Text too small (< 14px)

### Cards

**Standard Card:**
```
Background: White
Border: 1px solid #E5E5E5 OR subtle shadow (not both)
Border radius: 12px
Padding: 24px
Margin bottom: 16px

OR

Background: White
Shadow: 0 4px 6px rgba(0,0,0,0.1)
Border radius: 12px
Padding: 24px
Margin bottom: 16px
```

**Card Content Spacing:**
- Title to subtitle: 8px
- Subtitle to content: 16px
- Content sections: 24px
- Content to actions: 24px

**Bad Card Examples:**
- ❌ Both border AND shadow
- ❌ Heavy shadows
- ❌ Inconsistent padding
- ❌ Too many colors

### Forms

**Form Field:**
```
Label: 14px, semibold, dark gray, margin bottom 8px
Input: 
  - Height: 44px minimum
  - Padding: 12px 16px
  - Border: 1px solid #E5E5E5
  - Border radius: 8px
  - Background: White
  - Font: 16px
  - Focus: Accent border, no shadow
  
Error state:
  - Border: Red
  - Helper text: Red, 14px, margin top 4px
  
Field spacing: 24px between fields
```

**Form Layout:**
- Labels above inputs (not beside)
- Clear required indicators
- Group related fields
- Adequate spacing (24px minimum)
- Submit button: full width on mobile, auto on desktop

**Bad Form Examples:**
- ❌ Labels inside inputs (placeholder text is not a label)
- ❌ Tiny text (< 16px)
- ❌ Cramped spacing
- ❌ No error states
- ❌ Unclear required fields

### Navigation

**Top Navigation:**
```
Height: 64px
Background: White
Border bottom: 1px solid #E5E5E5
Padding: 0 32px (desktop), 0 16px (mobile)
Logo: 32px height
Links: 16px, medium weight, dark gray
Active link: Accent color
```

**Bottom Navigation (Mobile):**
```
Height: 56px
Background: White
Shadow: 0 -4px 6px rgba(0,0,0,0.1)
Icons: 24px, centered
Labels: 12px (optional)
Active: Accent color
```

## Design Quality Checklist

Before considering any UI complete, verify:

**Layout:**
- [ ] Adequate white space throughout
- [ ] Consistent spacing using 8px grid
- [ ] Not cluttered or cramped
- [ ] Clear visual hierarchy

**Colors:**
- [ ] Neutral base colors (grays/whites)
- [ ] Only ONE accent color
- [ ] NO gradients (unless specifically requested)
- [ ] Sufficient contrast (WCAG AA minimum)

**Typography:**
- [ ] Clear hierarchy (size + weight)
- [ ] Body text minimum 16px
- [ ] Maximum 2 font families
- [ ] Readable line heights

**Interactive Elements:**
- [ ] Clear hover states
- [ ] Clear active states
- [ ] Clear disabled states
- [ ] Clear focus states (keyboard navigation)

**Components:**
- [ ] Buttons have proper padding
- [ ] Forms have clear labels and spacing
- [ ] Cards use border OR shadow, not both
- [ ] Shadows are subtle

**Mobile:**
- [ ] Touch targets minimum 44x44px
- [ ] Works on small screens
- [ ] Adequate spacing for touch

## Platform-Specific Notes

### SwiftUI
- Use `.padding()` with explicit values from 8px grid
- Use `Color` with hex initializers for consistent colors
- Leverage `@Environment(\.colorScheme)` for dark mode
- Use SF Symbols for icons (always consistent)

### Android Studio
- Use `dp` units (1dp ≈ 1px on mdpi)
- Material Design 3 components acceptable but customize colors
- Use `dimens.xml` for spacing constants
- Leverage Compose for modern UI

### Web (HTML/CSS/React)
- Use CSS variables for colors and spacing
- Mobile-first media queries
- Use semantic HTML
- Leverage Tailwind CSS classes following this guide

## Anti-Patterns to Avoid

**NEVER do these:**
- ❌ Rainbow gradients everywhere
- ❌ Different colors on every element
- ❌ Purple/blue gradients by default
- ❌ Tiny unreadable text (< 16px body)
- ❌ Inconsistent spacing (random values)
- ❌ Heavy drop shadows
- ❌ Overly rounded everything
- ❌ Missing interactive states
- ❌ Both borders AND shadows on same element
- ❌ Cluttered layouts with no white space
- ❌ More than 2 font families
- ❌ Touch targets smaller than 44px

## Quick Reference

**Spacing:** 8, 16, 24, 32, 48, 64px
**Typography:** 16px minimum body, max 2 fonts
**Colors:** Neutral base + ONE accent
**Shadows:** Subtle only
**Border radius:** 6-12px most elements
**Interactive states:** Always include hover, active, disabled, focus

Always reference this guide before creating any UI component. Consistency is key to professional design.
