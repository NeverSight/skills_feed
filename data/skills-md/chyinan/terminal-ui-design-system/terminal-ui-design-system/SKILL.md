---
name: terminal-ui-design-system
description: Create terminal-inspired UI interfaces with macOS-style window decorations, monospace typography, and a warm color palette. Use this skill when building developer tools, code marketplaces, technical documentation sites, or any interface that benefits from a terminal/command-line aesthetic. Provides complete design system specifications including color palette, typography, spacing, components, and CSS implementation details.
---

# Terminal UI Design System

A comprehensive design system for creating terminal-inspired user interfaces with macOS-style window decorations, monospace typography, and a warm, developer-friendly color palette. This design system is optimized for developer tools, code marketplaces, technical documentation, and any interface that benefits from a command-line aesthetic.

## Design Philosophy

**Core Principles:**
- **Terminal Aesthetic**: Mimics macOS terminal windows with colored dots, monospace fonts, and command-line syntax
- **Developer-First**: Uses syntax highlighting colors, code-like structures, and terminal metaphors
- **Warm & Approachable**: Warm terracotta primary color (#cc7a60) creates a friendly, non-intimidating feel
- **High Contrast**: Clear visual hierarchy with distinct text colors and backgrounds
- **Functional Beauty**: Every design element serves a purpose while maintaining visual appeal

## Color System

### Primary Palette

**Main Brand Color:**
- `--primary: #cc7a60` - Warm terracotta/orange-brown, used for primary actions, accents, and highlights
- `--primary-foreground: #fff` - White text on primary backgrounds
- `--primary-dark: #b56850` - Darker shade for hover states
- `--primary-light: #d8907a` - Lighter shade for subtle accents
- `--ring: #cc7a60` - Focus ring color (same as primary)

**Warm Accent:**
- `--warm-red: #c85a3f` - Used for code block borders and warm accents

### Semantic Colors

**Backgrounds:**
- `--background: #fff` - Pure white for main backgrounds
- `--bg-main: #f8f8f8` - Light gray for page background (with subtle grid pattern)
- `--bg-card: #fff` - White for card components
- `--bg-code: #fafafa` - Very light gray for code blocks and window headers
- `--secondary: #f9fafb` - Light gray for secondary backgrounds
- `--muted: #f3f4f6` - Muted gray for subtle backgrounds

**Text Colors:**
- `--foreground: #111827` - Near-black for primary text (excellent readability)
- `--text-primary: #111827` - Primary text color
- `--text-secondary: #666666` - Medium gray for secondary text
- `--text-muted: #5b6370` - Muted gray for less important text
- `--muted-foreground: #5b6370` - Foreground on muted backgrounds

**Borders:**
- `--border: #8b929e` - Medium gray for main borders
- `--border-light: #e5e7eb` - Light gray for subtle dividers
- `--input: #8b929e` - Input border color

**Status Colors:**
- `--success: #22c55e` - Green for success states
- `--warning: #f59e0b` - Amber for warnings
- `--danger: #ef4444` - Red for errors/destructive actions
- `--accent: #f59e0b` - Amber accent color

### Syntax Highlighting Colors

**Code Syntax:**
- `--syntax-keyword: #cc7a60` - Primary color for keywords (const, export, etc.)
- `--syntax-string: #22c55e` - Green for strings
- `--syntax-number: #cc7a60` - Primary color for numbers
- `--syntax-comment: #6a9955` - Muted green for comments
- `--syntax-function: #dcdcaa` - Light yellow for function names

**Command Prefix:**
- Command prefix (`$`) uses fluorescent green: `#39ff14` - Creates terminal-like appearance

**Code Elements:**
- `--text-comment: #6a9955` - Comment text color

### macOS Window Dots

**Terminal Window Controls:**
- `--dot-red: #ff5f57` - Close button (macOS red)
- `--dot-yellow: #febc2e` - Minimize button (macOS yellow)
- `--dot-green: #28c840` - Maximize button (macOS green)

### Color Usage Guidelines

**Primary Color (#cc7a60) Usage:**
- Command keywords in navigation
- Prompt symbols (`>`)
- Active states and highlights
- Focus rings
- Hover borders
- Primary buttons when active
- Chart lines and data visualization

**Fluorescent Green (#39ff14) Usage:**
- Command prefix (`$`) - creates authentic terminal feel
- Only used for dollar signs, never for other elements

**Green (#22c55e) Usage:**
- Success indicators
- Status dots (online/ready)
- String literals in code
- Positive actions

**Blue (#3b82f6) Usage:**
- Command keywords (cd, watch, man, api)
- Code keywords (const, let, var)
- Links and interactive elements

## Typography System

### Font Families

**Primary Font Stack:**
```css
--font-mono: "JetBrains Mono", "JetBrains Mono Fallback", 'Fira Code', 'Consolas', monospace;
```
- **Primary**: JetBrains Mono (400-800 weights)
- **Fallbacks**: Fira Code, Consolas, system monospace
- Used for: All UI text, navigation, buttons, code blocks

**Sans-serif Fallback:**
```css
--font-sans: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
```
- Used as fallback only, monospace is preferred

### Font Size Scale

**Base Unit System:**
- `--text-xs: 0.75rem` (12px) - Small labels, hints, window status
- `--text-sm: 0.875rem` (14px) - Secondary text, descriptions
- `--text-base: 1rem` (16px) - Body text, default size
- `--text-lg: 1.125rem` (18px) - Slightly emphasized text
- `--text-xl: 1.25rem` (20px) - Subheadings
- `--text-2xl: 1.5rem` (24px) - Section titles
- `--text-3xl: 1.875rem` (30px) - Large numbers, stats
- `--text-4xl: 2.25rem` (36px) - Hero numbers
- `--text-5xl: 3rem` (48px) - Large headings
- `--text-6xl: 3.75rem` (60px) - Extra large headings

**Font Weights:**
- `--font-weight-normal: 400` - Body text
- `--font-weight-medium: 500` - Medium emphasis
- `--font-weight-semibold: 600` - Semibold (keywords, labels)
- `--font-weight-bold: 700` - Bold (headings, important text)
- `--font-weight-extrabold: 800` - Extra bold (hero text)

**Line Heights:**
- `--leading-tight: 1.25` - Tight spacing for headings
- `--leading-relaxed: 1.625` - Relaxed spacing for body text

### Typography Usage

**Headings:**
- Hero titles: 3.5rem, weight 700, line-height 1.1
- Section titles: 2.5rem, weight 700
- FAQ titles: 2rem, weight 700

**Body Text:**
- Default: 1rem, weight 400, line-height 1.5
- Secondary: 0.875rem, color `--text-secondary`
- Muted: 0.75rem, color `--text-muted`

**Code/Command Text:**
- Always use monospace font
- Command prefix: fluorescent green (#39ff14)
- Keywords: primary color (#cc7a60) or blue (#3b82f6)
- Flags/arguments: default foreground color

## Spacing System

**Base Unit:** `--spacing: 0.25rem` (4px)

**Spacing Scale:**
- `--spacing-xs: 4px` (0.25rem) - Tight spacing, icon padding
- `--spacing-sm: 8px` (0.5rem) - Small gaps, button padding
- `--spacing-md: 16px` (1rem) - Standard spacing, card padding
- `--spacing-lg: 24px` (1.5rem) - Large gaps, section spacing
- `--spacing-xl: 32px` (2rem) - Extra large gaps, major sections
- `--spacing-2xl: 48px` (3rem) - Maximum spacing, page sections

**Usage Guidelines:**
- Use consistent spacing multiples (4px base)
- Card padding: `--spacing-md` to `--spacing-lg`
- Section margins: `--spacing-xl` to `--spacing-2xl`
- Button padding: `--spacing-sm` to `--spacing-md`
- Gap between related elements: `--spacing-sm` to `--spacing-md`

## Border Radius System

**Radius Scale:**
- `--radius-xs: 2px` (0.125rem) - Minimal rounding
- `--radius-sm: 4px` (0.25rem) - Small elements
- `--radius-md: 6px` (0.375rem) - Buttons, inputs
- `--radius-lg: 8px` (0.5rem) - Cards, windows (most common)
- `--radius-xl: 12px` (0.75rem) - Large cards
- `--radius-2xl: 16px` (1rem) - Extra large elements
- `--radius: 10px` (0.625rem) - Default radius

**Usage:**
- Terminal windows: `--radius-lg` (8px)
- Buttons: `--radius-lg` (8px)
- Cards: `--radius-lg` (8px)
- Inputs: `--radius-md` (6px)
- Avatar: `9999px` (fully rounded)

## Shadow System

**Shadow Scale:**
- `--shadow-sm: 0 1px 2px rgba(0,0,0,0.05)` - Subtle elevation
- `--shadow-md: 0 4px 6px rgba(0,0,0,0.07)` - Medium elevation (cards on hover)
- `--shadow-lg: 0 10px 25px rgba(0,0,0,0.1)` - Large elevation (floating buttons)

**Usage:**
- Default cards: `--shadow-sm`
- Hover states: `--shadow-md`
- Floating elements: `--shadow-lg`
- Primary-colored shadows: `rgba(204, 122, 96, 0.1)` for primary-themed elements

## Component Specifications

### Terminal Window Component

**Structure:**
```html
<div class="terminal-window">
  <div class="window-header">
    <div class="window-dots">
      <span class="dot red"></span>
      <span class="dot yellow"></span>
      <span class="dot green"></span>
    </div>
    <span class="window-title">filename.ext</span>
    <span class="window-status">ready</span>
  </div>
  <div class="window-content">
    <!-- Content -->
  </div>
</div>
```

**Styling:**
- Background: `--bg-card` (#fff)
- Border: `1px solid --border` (#8b929e)
- Border radius: `--radius-lg` (8px)
- Box shadow: `--shadow-sm`
- Header background: `--bg-code` (#fafafa)
- Header border-bottom: `1px solid --border-light` (#e5e7eb)
- Header padding: `--spacing-sm --spacing-md` (8px 16px)
- Content padding: `--spacing-lg` (24px)

**Window Dots:**
- Size: `12px × 12px`
- Gap: `6px`
- Colors: Red (#ff5f57), Yellow (#febc2e), Green (#28c840)
- Fully rounded (border-radius: 50%)

**Window Title:**
- Font size: `0.85rem`
- Color: `--text-secondary` (#666666)
- Font: Monospace

**Window Status:**
- Font size: `0.75rem`
- Color: `--text-muted` (#5b6370)
- Position: Right side of header

### Navigation Bar

**Structure:**
```html
<nav class="navbar">
  <div class="navbar-container">
    <div class="navbar-content">
      <!-- Logo, commands, actions -->
    </div>
  </div>
</nav>
```

**Styling:**
- Position: `sticky`, `top: 0`
- Background: `rgba(255, 255, 255, 0.8)` with `backdrop-filter: blur(8px)`
- Border-bottom: `1px solid --border`
- Height: `64px` (desktop), `56px` (mobile)
- Max width: `80rem` (1280px), centered

**Logo:**
- Status indicator: Green dot (8px) + "ready" text
- Path prefix: `~/` in primary color (#cc7a60)
- Path name: Bold, foreground color
- Cursor blink: 2px width, primary color, animated

**Navigation Commands:**
- Display: Flex, gap `--spacing-md`
- Button style: Monospace font, small padding (6px 12px)
- Border: `1px solid --border`
- Border radius: `--radius-lg`
- Active state: Primary border color with pulse animation
- Hover: Border color changes to primary with 50% opacity

**Command Button Structure:**
```html
<button class="nav-cmd">
  <span class="cmd-prefix">$</span>
  <span class="cmd-keyword">ai</span>
  <span class="cmd-flag">--search</span>
</button>
```

**Command Colors:**
- Prefix (`$`): Fluorescent green (#39ff14)
- Keyword: Primary color (#cc7a60) or blue (#3b82f6)
- Flag: Default foreground color

### Card Components

**Skill Card:**
- Background: `--bg-card` (#fff in light, #111 in dark)
- Border: `1px solid --border`
- Border radius: `--radius-xl` (12px)
- Height: `100%` with flex column layout
- Hover: Border changes to primary with 50% opacity, shadow increases (`0 25px 50px -12px rgba(204, 122, 96, 0.1)`), `translateY(-4px)`
- Active: `translateY(0) scale(0.99)`
- Transition: `all 0.3s ease`
- **Line Numbers**: Absolute positioned on left, `2rem` width, subtle background
- **Avatar**: 24px × 24px, bordered, scales on hover
- **Star Icon**: 10px × 10px, warning color
- **Like Button**: SVG heart icon, changes color on hover

**Category Card:**
- Same base styling as skill card
- **Color Themes**: Cyan, Blue, Purple, Amber variants
- **Folder Icon**: SVG icon, color varies by theme, scales on hover
- **Category Dot**: Small indicator dot, changes on hover
- **Arrow Icon**: Appears on hover, positioned bottom-right
- **JSON Display**: Key-value pairs with theme-colored hover effects
- **Command Line**: Footer with command-style text

**Mention Card:**
- Same base styling
- Blockquote styling with quotation marks
- Source attribution with border-top separator

### Button Components

**Primary Button (Active):**
- Background: `--primary` (#cc7a60)
- Color: `--primary-foreground` (#fff)
- Border: `1px solid --primary`
- Border radius: `--radius-lg`
- Padding: `6px 12px` (small) or `--spacing-md --spacing-lg` (medium)
- Font: Monospace, `--text-xs` or `--text-sm`

**Secondary Button:**
- Background: `--bg-card`
- Border: `1px solid --border`
- Color: `--foreground`
- Hover: Border color changes to primary with 50% opacity
- Active: `transform: scale(0.95)`

**Icon Button:**
- Square or rounded
- Padding: `6px 12px`
- Icon size: `14px` or `16px`
- Same hover/active states as secondary button

### Input Components

**Search Input:**
- Background: Transparent
- Border: None
- Font: Monospace
- Placeholder: `--text-muted` color
- Focus: No visible border (minimal design)

**Text Input:**
- Background: `--bg-card`
- Border: `1px solid --border`
- Border radius: `--radius-sm` or `--radius-md`
- Padding: `--spacing-sm`
- Font: Monospace

### Code Display Components

**Code Block:**
- Background: `rgba(255, 255, 255, 0.5)` with backdrop blur
- Border: `1px solid --border`
- Border radius: `--radius-lg`
- Padding: `--spacing-md`
- Font: Monospace
- Line height: `--leading-relaxed`

**Code Line:**
- Display: Flex, align baseline
- Gap: `--spacing-sm`
- Syntax colors applied to different elements

**Description Block (Comment Style):**
- Border-left: `4px solid rgba(204, 122, 96, 0.5)`
- Background: `rgba(204, 122, 96, 0.05)`
- Padding-left: `--spacing-md`
- Border-radius: Right side only (`--radius-lg`)
- Font: Monospace

### Grid Layouts

**Skills Grid:**
- Display: Grid
- Columns: `repeat(3, 1fr)` (desktop), `repeat(2, 1fr)` (tablet), `1fr` (mobile)
- Gap: `--spacing-lg` (24px)

**Categories Grid:**
- Display: Grid
- Columns: `repeat(4, 1fr)` (desktop), `repeat(2, 1fr)` (tablet), `1fr` (mobile)
- Gap: `--spacing-lg`

**Mentions Grid:**
- Display: Grid
- Columns: `1fr 1fr` (desktop), `1fr` (mobile)
- Gap: `--spacing-lg`

## Animation System

### Transitions

**Default Transition:**
- Duration: `0.15s` or `0.2s`
- Timing: `cubic-bezier(.4,0,.2,1)` (ease-in-out)
- Properties: `all` or specific properties

**Common Transitions:**
- Hover states: `all 0.2s ease`
- Active states: `transform 0.2s ease`
- Color changes: `color 0.2s ease` or `background-color 0.2s ease`

### Keyframe Animations

**Blink Animation (Cursor):**
```css
@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
```
- Duration: `1s`
- Iteration: `infinite`
- Used for: Cursor blink effect

**Pulse Border Animation:**
```css
@keyframes pulse-border {
  0%, 100% { border-color: rgba(204, 122, 96, 0.5); }
  50% { border-color: var(--ring); }
}
```
- Duration: `2s`
- Timing: `ease-in-out`
- Iteration: `infinite`
- Used for: Active navigation items

**Fade In Up Animation:**
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```
- Duration: `0.5s`
- Timing: `ease`
- Used for: Card entrance animations
- Staggered delays: 0.1s increments for grid items

### Interactive States

**Hover States:**
- Buttons: Border color changes, background lightens
- Cards: Border changes to primary, shadow increases, slight lift
- Links: Color changes to primary
- Scale: No scaling on hover (maintains stability)

**Active States:**
- Buttons: `transform: scale(0.95)` - subtle press effect
- Duration: `0.2s`

**Focus States:**
- Outline: `2px solid --ring` with `2px` offset
- Used for: Accessibility, keyboard navigation

## Background Patterns

### Grid Pattern (Page Background)

```css
background-image: 
  linear-gradient(rgba(0, 0, 0, 0.02) 1px, transparent 1px),
  linear-gradient(90deg, rgba(0, 0, 0, 0.02) 1px, transparent 1px);
background-size: 20px 20px;
```

- Very subtle grid (2% opacity black)
- 20px × 20px grid cells
- Creates texture without distraction
- Applied to `body` background

### Gradient Backgrounds

**Avatar Gradient:**
```css
background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
```
- Warm peach gradient
- 135-degree angle
- Used for: User avatars

**Chart Gradient:**
```css
linearGradient: #cc7a60 with opacity stops (0%: 0.6, 100%: 0)
```
- Primary color gradient
- Used for: Area charts, data visualization

## Responsive Design

### Breakpoints

**Mobile:** `< 640px`
- Single column layouts
- Reduced font sizes
- Simplified navigation
- Stacked grids

**Tablet:** `640px - 1024px`
- Two column layouts
- Medium font sizes
- Collapsed navigation menu

**Desktop:** `1024px - 1200px`
- Three column layouts
- Full navigation visible
- Standard spacing

**Large Desktop:** `> 1200px`
- Four column layouts (where applicable)
- Maximum content width: `1400px`
- Generous spacing

### Responsive Adjustments

**Navigation:**
- Desktop (>1024px): Full command menu visible
- Tablet/Mobile: Hamburger menu, simplified layout
- Status indicator: Hidden on mobile, visible on tablet+

**Hero Section:**
- Desktop: Two column grid (text + chart)
- Mobile: Single column, stacked

**Grids:**
- Skills: 3 → 2 → 1 columns
- Categories: 4 → 2 → 1 columns
- Mentions: 2 → 1 columns

**Typography:**
- Hero title: 3.5rem → 2.5rem (mobile)
- Section titles: 2.5rem → 2rem (mobile)
- Body text: Maintains readability

## Implementation Guidelines

### CSS Variable Usage

**Always use CSS variables** for:
- Colors (never hardcode hex values)
- Spacing (use spacing scale)
- Typography (use text size scale)
- Border radius (use radius scale)
- Shadows (use shadow scale)

**Example:**
```css
.button {
  background: var(--bg-card);
  color: var(--foreground);
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}
```

### Component Structure

**Terminal Window Pattern:**
1. Container with border and radius
2. Header with dots, title, status
3. Content area with padding
4. Consistent spacing throughout

**Command-Line Pattern:**
1. Prefix (`$`) in fluorescent green
2. Keyword in primary or blue
3. Flags/arguments in default color
4. Monospace font throughout

### Color Application Rules

**Primary Color (#cc7a60):**
- Use for: Active states, highlights, keywords, prompts
- Avoid: Large background areas (too intense)
- Opacity variants: Use `rgba(204, 122, 96, 0.5)` for borders, `rgba(204, 122, 96, 0.05)` for backgrounds

**Fluorescent Green (#39ff14):**
- Use ONLY for: Command prefix (`$`)
- Never use for: Other text, backgrounds, or accents

**Green (#22c55e):**
- Use for: Success states, positive indicators, string literals
- Avoid: Primary actions (use primary color instead)

### Typography Rules

**Always use monospace font** for:
- Navigation elements
- Buttons
- Code blocks
- Command-line interfaces
- Window titles
- Status text

**Font weight guidelines:**
- Body text: 400 (normal)
- Labels/keywords: 600 (semibold)
- Headings: 700 (bold)
- Hero text: 700-800 (bold-extrabold)

### Spacing Consistency

**Use spacing scale:**
- Never use arbitrary values (e.g., `13px`, `27px`)
- Stick to: 4px, 8px, 16px, 24px, 32px, 48px
- For gaps between related items: `--spacing-sm` to `--spacing-md`
- For section separation: `--spacing-xl` to `--spacing-2xl`

### Animation Best Practices

**Keep animations subtle:**
- Duration: 0.15s - 0.3s maximum
- Easing: Use provided cubic-bezier curves
- Avoid: Bouncy animations, long durations
- Prefer: Fade, translate, scale (small amounts)

**Performance:**
- Use `transform` and `opacity` for animations (GPU accelerated)
- Avoid animating `width`, `height`, `margin`, `padding`

## Common Patterns

### Terminal Window Card

```html
<div class="terminal-window">
  <div class="window-header">
    <div class="window-dots">
      <span class="dot red"></span>
      <span class="dot yellow"></span>
      <span class="dot green"></span>
    </div>
    <span class="window-title">filename.ext</span>
    <span class="window-status">ready</span>
  </div>
  <div class="window-content">
    <!-- Content here -->
  </div>
</div>
```

### Command Button

```html
<button class="nav-cmd">
  <span class="cmd-prefix">$</span>
  <span class="cmd-keyword">command</span>
  <span class="cmd-flag">--flag</span>
</button>
```

### Code Block Display

```html
<div class="stats-code-block">
  <div class="code-line">
    <span class="keyword">const</span>
    <span class="variable-name">variable</span>
    <span class="operator">=</span>
    <span class="number">123</span>
    <span class="operator">;</span>
  </div>
  <div class="code-comment">
    <span class="comment-symbol">// </span>Comment text
  </div>
</div>
```

### Description Block (Comment Style)

```html
<div class="description-block">
  <div class="comment-start">/**</div>
  <div class="comment-text">
    <span class="comment-asterisk"> * </span>Description text
  </div>
  <div class="comment-end"> */</div>
</div>
```

## Accessibility Considerations

**Color Contrast:**
- Primary text (#111827) on white: WCAG AAA compliant
- Secondary text (#666666) on white: WCAG AA compliant
- Primary color (#cc7a60) on white: WCAG AA compliant for large text

**Focus States:**
- All interactive elements have visible focus indicators
- Focus ring: 2px solid primary color with 2px offset

**Keyboard Navigation:**
- All interactive elements are keyboard accessible
- Tab order follows visual hierarchy
- Enter/Space activate buttons

**Screen Readers:**
- Semantic HTML structure
- ARIA labels where needed
- Status indicators use appropriate roles

## Dark Mode Implementation

The design system includes a complete dark mode implementation using `[data-theme="dark"]` attribute selector. Dark mode is fully integrated with smooth transitions and maintains all design principles.

### Dark Mode Color System

**Primary Colors (Dark Mode):**
- `--primary: #d99178` - Lighter terracotta for better contrast on dark backgrounds
- `--primary-foreground: #0a0a0a` - Dark text on primary backgrounds
- `--primary-dark: #c57f66` - Darker shade for hover states
- `--primary-light: #e5a890` - Lighter shade for subtle accents
- `--ring: #d99178` - Focus ring color (lighter primary)

**Backgrounds (Dark Mode):**
- `--background: #0a0a0a` - Deep black for main backgrounds
- `--bg-main: #0a0a0a` - Dark background with subtle white grid pattern
- `--bg-card: #111` - Slightly lighter black for card components
- `--bg-code: #18181b` - Dark gray for code blocks and window headers
- `--secondary: #1a1a1a` - Dark gray for secondary backgrounds
- `--muted: #262626` - Muted dark gray for subtle backgrounds

**Text Colors (Dark Mode):**
- `--foreground: #ededed` - Light gray for primary text
- `--text-primary: #ededed` - Primary text color
- `--text-secondary: #a3a3a3` - Medium gray for secondary text
- `--text-muted: #a3a3a3` - Muted gray for less important text
- `--muted-foreground: #a3a3a3` - Foreground on muted backgrounds

**Borders (Dark Mode):**
- `--border: #606068` - Lighter gray for visibility on dark backgrounds
- `--border-light: #27272a` - Subtle dark gray for dividers

**Syntax Highlighting (Dark Mode):**
- `--syntax-keyword: #d99178` - Lighter primary for keywords
- `--syntax-string: #22c55e` - Green (same as light mode)
- `--syntax-number: #d99178` - Lighter primary for numbers
- `--syntax-comment: #6a9955` - Muted green (same as light mode)
- Blue keywords: `#60a5fa` (blue-400) - Brighter blue for better contrast
- Purple keywords: `#c084fc` (purple-400) - Brighter purple for better contrast

**Shadows (Dark Mode):**
- `--shadow-sm: 0 1px 2px rgba(0,0,0,0.3)` - Stronger shadows for depth
- `--shadow-md: 0 4px 6px rgba(0,0,0,0.4)` - Medium shadows
- `--shadow-lg: 0 10px 25px rgba(0,0,0,0.5)` - Large shadows

### Dark Mode Background Pattern

Dark mode uses a subtle white grid pattern instead of black:

```css
[data-theme="dark"] body {
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
}
```

### Theme Toggle Implementation

**HTML Structure:**
```html
<button class="theme-toggle-btn theme-toggle" title="切换主题" aria-label="切换主题">
  <svg class="icon-sun theme-icon"><!-- Sun icon --></svg>
  <svg class="icon-moon theme-icon" style="display: none;"><!-- Moon icon --></svg>
</button>
```

**JavaScript Implementation:**
- Uses `localStorage` to persist theme preference
- Detects system preference on first load
- Smoothly transitions between themes
- Updates icon visibility (sun/moon)
- Listens to system theme changes (when no manual preference set)

**Key Features:**
- Automatic system preference detection
- Manual override with localStorage persistence
- Smooth CSS transitions (0.2s ease-in-out)
- Icon state management (sun for light, moon for dark)

### Dark Mode Component Adaptations

**Navigation Bar:**
- Background: `rgba(10, 10, 10, 0.8)` with backdrop blur
- Status indicator: Darker background with adjusted border

**Terminal Windows:**
- Card background: `#111` (slightly lighter than main background)
- Window headers: `rgba(38, 38, 38, 0.3)` for subtle contrast
- All borders use darker mode colors

**Skill Cards:**
- Line numbers background: `rgba(38, 38, 38, 0.2)`
- Footer background: `rgba(38, 38, 38, 0.2)`
- Hover effects maintain same behavior with adjusted colors

**Category Cards:**
- Each category has theme-specific hover colors:
  - Cyan: `#22d3ee` (dark) vs `#06b6d4` (light)
  - Blue: `#60a5fa` (dark) vs `#3b82f6` (light)
  - Purple: `#c084fc` (dark) vs `#a855f7` (light)
  - Amber: `#fbbf24` (dark) vs `#f59e0b` (light)

**Charts:**
- Grid lines: `#27272a` with 0.5 opacity
- Chart container: `rgba(17, 17, 17, 0.3)`
- All text colors adapt to dark mode

**FAB Button:**
- Light mode: Dark background `#1a1a1a` with white icon
- Dark mode: White background with dark icon (inverted)

### Dark Mode Best Practices

**Color Contrast:**
- All text maintains WCAG AA compliance in dark mode
- Primary color is lightened for better visibility
- Borders are lighter for clear definition

**Transitions:**
- All color changes use `transition: color 0.2s ease-in-out`
- Background changes use `transition: background-color 0.2s ease-in-out`
- Smooth theme switching without jarring changes

**Implementation Pattern:**
```css
/* Light mode (default) */
.component {
  background: var(--bg-card);
  color: var(--foreground);
}

/* Dark mode */
[data-theme="dark"] .component {
  background: var(--bg-card); /* Automatically uses dark value */
  color: var(--foreground); /* Automatically uses dark value */
}
```

**Maintains:**
- Same spacing system
- Same typography scale
- Same component structure
- Same animation timing
- Enhanced shadows for depth perception

## Performance Optimization

**CSS Variables:**
- All colors/spacing use CSS variables for easy theming
- Variables defined in `:root` for global access

**Animations:**
- Use `transform` and `opacity` (GPU accelerated)
- Avoid layout-triggering properties
- Keep durations short (0.15s - 0.3s)

**Font Loading:**
- Preconnect to Google Fonts
- Use `font-display: swap` for better performance
- Provide fallback fonts in stack

## Browser Support

**Modern Browsers:**
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support (with `-webkit-` prefixes for backdrop-filter)

**Features Used:**
- CSS Grid: Full support in modern browsers
- CSS Variables: Full support
- Backdrop Filter: Requires `-webkit-` prefix for Safari
- Flexbox: Full support

## Design Tokens Summary

**Quick Reference:**

```css
/* Colors - Light Mode */
Primary: #cc7a60
Fluorescent Green: #39ff14 (command prefix only)
Success: #22c55e
Blue: #3b82f6
Foreground: #111827
Border: #8b929e

/* Colors - Dark Mode */
Primary: #d99178
Foreground: #ededed
Background: #0a0a0a
Card: #111
Border: #606068
Blue: #60a5fa (brighter for contrast)

/* Spacing */
xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, 2xl: 48px

/* Typography */
Font: JetBrains Mono
Sizes: 0.75rem - 3.75rem scale
Weights: 400, 500, 600, 700, 800

/* Radius */
xs: 2px, sm: 4px, md: 6px, lg: 8px, xl: 12px, 2xl: 16px

/* Shadows - Light Mode */
sm: 0 1px 2px rgba(0,0,0,0.05)
md: 0 4px 6px rgba(0,0,0,0.07)
lg: 0 10px 25px rgba(0,0,0,0.1)

/* Shadows - Dark Mode */
sm: 0 1px 2px rgba(0,0,0,0.3)
md: 0 4px 6px rgba(0,0,0,0.4)
lg: 0 10px 25px rgba(0,0,0,0.5)
```

## Theme Toggle JavaScript Implementation

**Complete Implementation:**
```javascript
(function() {
  const themeToggles = document.querySelectorAll('.theme-toggle');
  const html = document.documentElement;
  
  // Get initial theme from localStorage or system preference
  function getInitialTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    // Check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }
  
  // Set theme and update icons
  function setTheme(theme) {
    if (theme === 'dark') {
      html.setAttribute('data-theme', 'dark');
      document.querySelectorAll('.icon-sun').forEach(icon => {
        icon.style.display = 'none';
      });
      document.querySelectorAll('.icon-moon').forEach(icon => {
        icon.style.display = 'block';
      });
    } else {
      html.removeAttribute('data-theme');
      document.querySelectorAll('.icon-sun').forEach(icon => {
        icon.style.display = 'block';
      });
      document.querySelectorAll('.icon-moon').forEach(icon => {
        icon.style.display = 'none';
      });
    }
    localStorage.setItem('theme', theme);
  }
  
  // Toggle theme
  function toggleTheme() {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  }
  
  // Initialize
  const initialTheme = getInitialTheme();
  setTheme(initialTheme);
  
  // Add event listeners
  themeToggles.forEach(button => {
    button.addEventListener('click', toggleTheme);
  });
  
  // Listen to system theme changes (only if no manual preference)
  if (window.matchMedia) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
})();
```

**Key Features:**
- Persists theme preference in localStorage
- Detects system preference on first load
- Smoothly transitions between themes
- Updates icon visibility automatically
- Listens to system theme changes (when no manual override)

## Usage Examples

When implementing this design system:

1. **Start with CSS variables** - Import or define all color/spacing variables (including dark mode)
2. **Use terminal window pattern** - Wrap content in terminal-window component
3. **Apply monospace font** - Use JetBrains Mono for all UI text
4. **Follow spacing scale** - Use defined spacing values consistently
5. **Use semantic colors** - Apply colors based on meaning, not appearance
6. **Implement theme toggle** - Add theme toggle button and JavaScript
7. **Maintain consistency** - Reuse component patterns throughout
8. **Test responsiveness** - Ensure layouts work at all breakpoints
9. **Test both themes** - Verify light and dark modes work correctly
10. **Optimize animations** - Keep transitions smooth and performant

This design system creates a cohesive, developer-friendly interface that feels both modern and familiar to users comfortable with terminal interfaces. The complete dark mode implementation ensures the interface works beautifully in any lighting condition.
