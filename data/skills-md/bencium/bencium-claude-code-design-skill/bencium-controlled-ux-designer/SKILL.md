---
name: bencium-controlled-ux-designer
description: Expert UI/UX design guidance for unique, accessible interfaces. Use for visual decisions, colors, typography, layouts. Always ask before making design decisions. Use this skill when the user asks to build web components, pages, or applications.
metadata:
  version: 1.0.0
---

# UX Designer

Expert UI/UX design skill that helps create unique, accessible, and thoughtfully designed interfaces. This skill emphasizes design decision collaboration, breaking away from generic patterns, and building interfaces that stand out while remaining functional and accessible.

## Core Philosophy

**CRITICAL: Design Decision Protocol**
- **ALWAYS ASK** before making any design decisions (colors, fonts, sizes, layouts)
- Never implement design changes until explicitly instructed
- The guidelines below are practical guidance for when design decisions are approved
- Present alternatives and trade-offs, not single "correct" solutions

## Foundational Design Principles

### Stand Out From Generic Patterns

**Avoid Generic Training Dataset Patterns:**
- Don't default to "Claude style" designs (excessive bauhaus, liquid glass, apple-like)
- Don't use generic SaaS aesthetics that look machine-generated
- Don't rely only on solid colors - suggest photography, patterns, textures
- Think beyond typical patterns - you can step off the written path

**Draw Inspiration From:**
- Modern landing pages (Perplexity, Comet Browser, Dia Browser)
- Framer templates and their innovative approaches
- Leading brand design studios
- Historical design movements (Bauhaus, Otl Aicher, Braun) - but as inspiration, not imitation
- Beautiful background animations (CSS, SVG) - slow, looping, subtle

**Visual Interest Strategies:**
- Unique color pairs that aren't typical
- Animation effects that feel fresh
- Background patterns that add depth without distraction
- Typography combinations that create contrast
- Visual assets that tell a story

### Core Design Philosophy

1. **Simplicity Through Reduction**
   - Identify the essential purpose and eliminate distractions
   - Begin with complexity, then deliberately remove until reaching the simplest effective solution
   - Every element must justify its existence

2. **Material Honesty**
   - Digital materials have unique properties - embrace them
   - Buttons should communicate affordance through color, spacing, and typography (not shadows)
   - Cards use borders and background differentiation (not depth effects)
   - Animations follow real-world physics principles adapted to digital responsiveness

   **Examples:**
   - Clickable: Use distinct colors, hover state changes, cursor feedback
   - Containers: Use subtle borders (1px), background color shifts, or generous padding
   - Hierarchy: Use scale, weight, and spacing rather than elevation

3. **Functional Layering (Not Visual Depth)**
   - Create hierarchy through typography scale, color contrast, and spatial relationships
   - Layer information conceptually (primary → secondary → tertiary)
   - Reject skeuomorphic shadows/gradients that imitate physical depth
   - Embrace functional depth: modals over content, dropdowns over UI

4. **Obsessive Detail**
   - Consider every pixel, interaction, and transition
   - Excellence emerges from hundreds of small, intentional decisions
   - Balance: Details should serve simplicity, not complexity
   - When detail conflicts with clarity, clarity wins

5. **Coherent Design Language**
   - Every element should visually communicate its function
   - Elements should feel part of a unified system
   - Nothing should feel arbitrary

6. **Invisibility of Technology**
   - The best technology disappears
   - Users should focus on content and goals, not on understanding the interface

### What This Means in Practice

**Color Usage:**
- Base palette: 4-5 neutral shades (backgrounds, borders, text)
- Accent palette: 1-3 bold colors (CTAs, status, emphasis)
- Neutrals are slightly desaturated, warm or cool based on brand intent
- Accents are saturated enough to create clear contrast

**Typography:**
- Headlines: Emotional, attention-grabbing (personality over pure legibility)
- Body/UI: Functional, highly legible (clarity over expression)
- 2-3 typefaces maximum
- Clear mathematical scale (e.g., 1.25x between sizes)

**Animation:**
- Purposeful: Guides attention, establishes relationships, provides feedback
- Subtle: Felt rather than seen (100-300ms for most interactions)
- Physics-informed: Natural easing, appropriate mass/momentum

**Spacing:**
- Generous negative space creates clarity and breathing room
- Mathematical relationships (e.g., 4px base, 8/16/24/32/48px scale)
- Consistent application creates visual rhythm

### Design Decision Checklist

Before presenting any design, verify:

1. **Purpose**: Does every element serve a clear function?
2. **Hierarchy**: Is visual importance aligned with content importance?
3. **Consistency**: Do similar elements look and behave similarly?
4. **Accessibility**: Does it meet WCAG AA standards? (contrast, touch targets, keyboard nav)
5. **Responsiveness**: Does it work on mobile, tablet, desktop?
6. **Uniqueness**: Does this break from generic SaaS patterns?
7. **Approval**: Have I asked before implementing colors, fonts, sizes, layouts?

**Design System Framework:**

For understanding what's fixed (universal rules), project-specific (brand personality), and adaptable (context-dependent) in your design system, see DESIGN-SYSTEM-TEMPLATE.md (meta-framework, project templates, decision trees).

## Visual Design Standards

### Color & Contrast

**Color System Architecture:**

Every interface needs two color roles:

1. **Base/Neutral Palette (4-5 colors):**
   - Backgrounds (lightest)
   - Surface colors (cards, inputs)
   - Borders and dividers
   - Text (darkest)
   - Use slightly desaturated, warm or cool greys based on brand

2. **Accent Palette (1-3 colors):**
   - Primary action (CTA buttons)
   - Status indicators (success, warning, error, info)
   - Focus/hover states
   - Use saturated colors for clear contrast against neutrals

**Palette Structure Example:**
```
Neutrals: slate-50, slate-100, slate-300, slate-700, slate-900
Accents: teal-500 (primary), amber-500 (warning), red-500 (error)
```

**Color Application Rules:**

- **Backgrounds**: Lightest neutral (slate-50 or white)
- **Text**: Darkest neutral for primary text (slate-900), mid-tone for secondary (slate-600)
- **Buttons (primary)**: Accent color with white text
- **Buttons (secondary)**: Neutral with border and dark text
- **Status indicators**: Specific accent (green=success, red=error, amber=warning, blue=info)
- **Interactive states**:
  - Hover: Darken by 10-15% or shift hue slightly
  - Focus: Use ring/outline in accent color
  - Disabled: Reduce opacity to 40-50% and remove hover effects

**Color Relationships:**

Choose warm or cool intentionally based on brand:
- **Warm greys** (beige/brown undertones): Organic, approachable, trustworthy
- **Cool greys** (blue undertones): Modern, tech-forward, professional

Accent colors should have clear contrast with both:
- Light backgrounds (for buttons on white)
- Dark text (if used as backgrounds for white text)

**Intentional Color Usage:**
- Every color must serve a purpose (hierarchy, function, status, or action)
- Avoid decorative colors that don't communicate meaning
- Maintain consistency: same color = same meaning throughout

**Accessibility:**
- Ensure sufficient contrast for color-blind users
- Follow WCAG 2.1 AA: minimum 4.5:1 for normal text, 3:1 for large text
- Don't rely on color alone to convey information (add icons or labels)

**Unique Color Strategy:**

To stand out from generic patterns:
- Avoid default SaaS blue (#3B82F6) unless it fits your brand
- Consider unexpected neutrals: warm greys, soft off-whites, deep charcoals
- Pair neutrals with distinctive accents: terracotta + charcoal, sage + navy, coral + slate
- Test combinations against "does this look AI-generated?" filter

### Typography Excellence

**Typography Philosophy:**

Typography is a primary design element that conveys personality and hierarchy.

**Functional vs Emotional Typography:**
- **Headlines/Display**: Prioritize emotion, personality, attention (legibility secondary)
- **Body Text**: Prioritize legibility, reading comfort, accessibility
- **UI/Labels**: Prioritize clarity, scannability, consistency

**Font Selection:**
- Use 2-3 typefaces maximum
- Limit to 3 weights per typeface (e.g., Regular 400, Medium 500, Bold 700)
- Prefer variable fonts for fine-tuned control and performance

**Font Version Usage:**
- **Display version**: Headlines and hero text only
- **Text version**: Paragraphs and long-form content
- **Caption/Micro**: Small UI labels (1-2 lines, non-critical info)

**Recommended Sources:**
- Google Fonts for web (free, well-optimized, reliable)
- System fonts for performance-critical apps (-apple-system, BlinkMacSystemFont, Segoe UI)
- Choose fonts that serve your brand's purpose (not "trending" lists)

**Typographic Scale:**

Use mathematical relationships for size hierarchy:
- **Ratio**: Major third (1.25x) for moderate contrast, Perfect fourth (1.333x) for dramatic
- **Base size**: 16px (1rem) for body text
- **Example scale (1.25x)**:
  ```
  xs:   0.64rem (10px)
  sm:   0.8rem  (13px)
  base: 1rem    (16px)
  lg:   1.25rem (20px)
  xl:   1.563rem (25px)
  2xl:  1.953rem (31px)
  3xl:  2.441rem (39px)
  4xl:  3.052rem (49px)
  5xl:  3.815rem (61px)
  ```

**Typographic Hierarchy:**
- Create clear visual distinction between levels
- Headlines, subheadings, body, captions should each have distinct size/weight
- Use combination of size, weight, and color for hierarchy

**Spacing & Readability:**
- **Line height**: 1.5x font size for body text (e.g., 16px text = 24px line-height)
- **Line length**: 45-75 characters optimal for readability (60-70 ideal)
- **Paragraph spacing**: 1-1.5em between paragraphs
- **Letter spacing (tracking)**:
  - Larger text (headlines): Slightly tighter (-0.02em to -0.05em)
  - Normal text (body): Default (0)
  - Small text (captions): Slightly looser (+0.01em to +0.03em)
  - General rule: As size increases, reduce tracking; as size decreases, increase tracking

**Font Pairing Logic:**

When using multiple typefaces, create contrast through:
- **Category contrast**: Serif + Sans-serif (classic, clear distinction)
- **Weight contrast**: Light + Bold (dynamic, energetic)
- **Personality contrast**: Geometric + Humanist (modern + warm)

Examples:
- Serif headlines + Sans body (editorial, trustworthy)
- Display headlines + System body (distinctive + efficient)
- Bold sans headlines + Light sans body (modern, clean)

**UI Typography:**

Specific guidance for interface elements:
- **Button text**: Semi-Bold (600), 14-16px, consistent casing (all-caps OR title case)
- **Form labels**: Regular (400), 14px, positioned above input
- **Form input text**: Regular (400), 16px minimum (prevents iOS zoom on focus)
- **Placeholder text**: Light (300) or desaturated color, same size as input
- **Error messages**: Regular (400), 12-14px, color-coded (red-ish)

**Responsive Typography:**

Scale type sizes across breakpoints:
```tsx
// Example with Tailwind
<h1 className="text-3xl md:text-4xl lg:text-5xl">
  Responsive Headline
</h1>

// Or with CSS clamp (fluid)
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
}
```

Reduce sizes on mobile (20-30% smaller than desktop)
Reduce hierarchy levels on small screens (fewer distinct sizes)

### Layout & Spatial Design

**Compositional Balance:**
- Every screen should feel balanced
- Pay attention to visual weight and negative space
- Use generous negative space to focus attention
- Add sufficient margins and paddings for professional, spacious look

**Grid Discipline:**
- Maintain consistent underlying grid system
- Create sense of order while allowing meaningful exceptions
- Use grid/flex wrappers with `gap` for spacing
- Prioritize wrappers over direct margins/padding on children

**Spatial Relationships:**
- Group related elements through proximity, alignment, and shared attributes
- Use size, color, and spacing to highlight important elements
- Guide user focus through visual hierarchy

**Attention Guidance:**
- Design interfaces that guide user attention effectively
- Avoid cluttered interfaces where elements compete
- Create clear paths through the content

## Interaction Design

### Motion & Animation

**Purposeful Animation:**

Every animation must serve a functional purpose:
- **Orient users**: Smooth transitions during navigation changes
- **Establish relationships**: Show how elements connect (expand from source, slide between states)
- **Provide feedback**: Confirm interactions (button press, form submission)
- **Guide attention**: Direct focus to important changes (new messages, errors)

**Animation & Gestalt Principles:**

Motion should reinforce visual relationships:
- **Proximity**: Elements near each other move together (grouped cards animating)
- **Similarity**: Similar elements animate similarly (all buttons have same hover timing)
- **Continuity**: Movement follows natural paths (smooth curves, not jumpy angles)
- **Figure-ground**: Important elements animate while backgrounds stay stable

**Natural Physics:**

Animations should feel organic, not mechanical:
- **Easing**: Use ease-out for entrances (fast start, slow end)
- **Easing**: Use ease-in for exits (slow start, fast end)
- **Easing**: Use ease-in-out for transitions (smooth both ends)
- Avoid linear easing (feels robotic) except for continuous loops
- Apply appropriate mass/momentum (lightweight UI vs weighty modals)

**Subtle Restraint:**
- Animations should be felt rather than seen
- Don't delay user actions unnecessarily (keep under 300ms for interactive feedback)
- Never block critical actions with decorative animations
- Respect `prefers-reduced-motion` media query

**Timing Guidelines:**

- **Micro-interactions** (button press, checkbox toggle): 100-150ms
- **State changes** (expanding accordion, tab switch): 200-300ms
- **Page transitions** (route changes, modal open/close): 300-500ms
- **Attention-directing** (notification appearance, error highlight): 200-400ms

**Physics Profiles:**

Define consistent durations for element types:
- **Lightweight** (icons, small UI): 150ms
- **Standard** (cards, panels): 300ms
- **Weighty** (modals, page transitions): 500ms

**Performance Optimization:**

- Animate `transform` and `opacity` only (GPU-accelerated, smooth 60fps)
- Avoid animating `width`, `height`, `top`, `left`, `margin` (causes reflow/repaint)
- Use `will-change` sparingly for complex animations (pre-allocates GPU resources)
- Test on low-end devices (60fps on powerful hardware ≠ 60fps on mobile)

**Implementation:**
- Use `framer-motion` sparingly and purposefully
- Prefer CSS animations over JavaScript when possible (better performance)
- Use CSS transitions for simple hover/focus states
- Implement `@media (prefers-reduced-motion: reduce)` to disable/reduce animations

**Example:**
```tsx
// Simple hover transition
<button className="
  transition-colors duration-200 ease-out
  bg-blue-600 hover:bg-blue-700
">
  Click me
</button>

// Framer Motion for complex interaction
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.3, ease: "easeOut" }}
>
  Content
</motion.div>
```

**Motion Specification:**

For detailed motion specs, see MOTION-SPEC.md (easing curves, duration tables, state-specific animations, implementation patterns).

### User Experience Patterns

**Core UX Principles:**

1. **Direct Manipulation**
   - Users interact directly with content, not through abstract controls
   - Examples:
     - Drag & drop to reorder items (not up/down buttons)
     - Inline editing (click to edit, not separate form)
     - Sliders for ranges (not numeric input with +/-)
     - Pinch/zoom gestures on mobile (not +/- buttons)

2. **Immediate Feedback**
   - Every interaction provides instantaneous visual feedback (within 100ms)
   - Types of feedback:
     - **Visual**: Button pressed state, hover effects, color changes
     - **Haptic**: Vibration on mobile (submit, error, success)
     - **Audio**: Subtle sounds for critical actions (optional, user-controlled)
     - **Loading**: Skeleton screens, spinners for >300ms operations
     - **Success**: Checkmarks, green highlights, toast notifications
     - **Error**: Red highlights, inline error messages, shake animations

3. **Consistent Behavior**
   - Similar-looking elements behave similarly
   - Examples:
     - **Visual consistency**: All primary buttons have same colors, sizes, hover states
     - **Behavioral consistency**: All modals close via X button, ESC key, and outside click
     - **Interaction consistency**: All drag targets have same hover state and drop feedback
     - **Pattern consistency**: All forms validate on blur and submit

4. **Forgiveness**
   - Make errors difficult, but recovery easy
   - **Prevention strategies**:
     - Disable invalid actions (grey out unavailable buttons)
     - Validate inputs inline (before submission)
     - Confirm destructive actions (delete, overwrite)
     - Auto-save in background (drafts, progress)
   - **Recovery strategies**:
     - Undo/redo for all state changes
     - Soft deletes (trash/archive before permanent delete)
     - Clear error messages with actionable fixes
     - Preserve user input on errors (don't clear forms)

5. **Progressive Disclosure**
   - Reveal details as needed rather than overwhelming users
   - Levels of disclosure:
     - **Summary**: Show essential info by default (card title, price, rating)
     - **Details**: Expand to show more info (description, specs, reviews)
     - **Advanced**: Hide complex options behind "Advanced settings" toggle
   - Examples:
     - Accordion: Start collapsed, expand on click
     - Search filters: Show 3-5 common filters, hide rest behind "More filters"
     - Settings: Basic settings visible, advanced behind "Show advanced"

**Modern UX Patterns:**

1. **Conversational Interfaces**

   Prioritize natural language interaction where appropriate:

   **Four types:**
   - **Pure chat**: Full conversation (AI assistants, support bots)
   - **Command palette**: Text-based shortcuts (Cmd+K, search everywhere)
   - **Smart search**: Natural language queries (search "meetings next week" vs filtering)
   - **Form alternatives**: Conversational data collection ("What's your name?" vs form fields)

   **When to use:**
   - Complex searches with multiple variables
   - Task guidance (wizards, onboarding)
   - Contextual help
   - Quick actions (command palette)

   **When NOT to use:**
   - Simple forms (just use inputs)
   - Precise control interfaces (design tools, dashboards)
   - High-frequency repetitive tasks

2. **Adaptive Layouts**

   Respond to user context automatically:
   - **Time-based**: Dark mode at night, light during day
   - **Device-based**: Simplified UI on mobile, full features on desktop
   - **Connection-based**: Reduce images/video on slow connections
   - **Usage-based**: Prioritize frequent actions, hide rarely-used features

   Examples:
   - Auto dark/light mode based on time or system preference
   - Simplified mobile navigation (hamburger menu) vs full desktop nav
   - Collapsed sidebar on small screens, expanded on large

3. **Minimal, Flat Design**

   Current aesthetic preference:
   - No drop shadows (except subtle ones for modals/dropdowns)
   - No gradients for depth (use for accents/backgrounds if desired)
   - No glass morphism effects
   - Focus on typography, color, and spacing to create hierarchy
   - Functional depth: Layers of content (modals, sheets) use positioning, not visual depth

**Navigation:**
- Clear structure with intuitive navigation menus
- Implement breadcrumbs for deep hierarchies (more than 2 levels)
- Use standard UI patterns to reduce learning curve (hamburger menu, tab bars)
- Ensure predictable behavior (back button works, links look clickable)
- Maintain navigation context (highlight current page, preserve scroll position)

## Styling Implementation

### Component Library & Tools

**Component Library:**
- Strongly prefer shadcn components (v4, pre-installed in `@/components/ui`)
- Import individually: `import { Button } from "@/components/ui/button";`
- Use over plain HTML elements (`<Button>` over `<button>`)
- Avoid creating custom components with names that clash with shadcn

**Styling Engine:**
- Use Tailwind utility classes exclusively
- Adhere to theme variables in `index.css` via CSS custom properties
- Map variables in `@theme` (see `tailwind.config.js`)
- Use inline styles or CSS modules only when absolutely necessary

**Icons:**
- Use `@phosphor-icons/react` for buttons and inputs
- Example: `import { Plus } from "@phosphor-icons/react"; <Plus />`
- Use color for plain icon buttons
- Don't override default `size` or `weight` unless requested

**Notifications:**
- Use `sonner` for toasts
- Example: `import { toast } from 'sonner'`

**Loading States:**
- Always add loading states, spinners, placeholder animations
- Use skeletons until content renders

### Layout Implementation

**Spacing Strategy:**
- Use grid/flex wrappers with `gap` for spacing
- Prioritize wrappers over direct margins/padding on children
- Nest wrappers as needed for complex layouts

**Conditional Styling:**
- Use ternary operators or clsx/classnames utilities
- Example: `className={clsx('base-class', { 'active-class': isActive })}`

### Responsive Design

**Fluid Layouts:**
- Use relative units (%, em, rem) instead of fixed pixels
- Implement CSS Grid and Flexbox for flexible layouts
- Design mobile-first, then scale up

**Media Queries:**
- Use breakpoints based on content needs, not specific devices
- Test across range of devices and orientations

**Touch Targets:**
- Minimum 44x44 pixels for interactive elements
- Provide adequate spacing between touch targets
- Consider hover states for desktop, focus states for touch/keyboard

**Performance:**
- Optimize assets for mobile networks
- Use CSS animations over JavaScript
- Implement lazy loading for images and videos

## Accessibility Standards

**Core Requirements:**
- Follow WCAG 2.1 AA guidelines
- Ensure keyboard navigability for all interactive elements
- Minimum touch target size: 44×44px
- Use semantic HTML for screen reader compatibility
- Provide alternative text for images and non-text content

**Implementation Details:**
- Use descriptive variable and function names
- Event functions: prefix with "handle" (handleClick, handleKeyDown)
- Add accessibility attributes:
  - `tabindex="0"` for custom interactive elements
  - `aria-label` for buttons without text
  - `role` attributes when semantic HTML isn't sufficient
- Ensure logical tab order
- Provide visible focus states

## Design Process & Testing

### Design Workflow

1. **Understand Context:**
   - What problem are we solving?
   - Who are the users and when will they use this?
   - What are the success criteria?

2. **Explore Options:**
   - Present 2-3 alternative approaches
   - Explain trade-offs of each option
   - Ask which direction resonates

3. **Implement Iteratively:**
   - Start with structure and hierarchy
   - Add visual polish progressively
   - Test at each stage

4. **Validate:**
   - Use playwright MCP to test visual changes
   - Check across different screen sizes
   - Verify accessibility

### Testing Checklist

**Visual Testing:**
- Use playwright MCP when available for automated testing
- Check responsive behavior at common breakpoints
- Verify touch targets on mobile
- Test with different content lengths (short, long, edge cases)

**Accessibility Testing:**
- Test keyboard navigation
- Verify screen reader compatibility
- Check color contrast ratios
- Ensure focus states are visible

**Cross-Device Testing:**
- Test on actual devices, not just emulators
- Check different browsers (Chrome, Firefox, Safari)
- Verify touch interactions on mobile
- Test landscape and portrait orientations

## Examples

### Example 1: Designing a Button

**Initial Question to Ask:**
```
Before I implement this button, I have a few design questions:
1. What's the primary action you want to emphasize?
2. Do you have brand colors in mind, or should I suggest options?
3. What emotion should this button convey? (urgent, calm, playful, professional)
```

**After Getting Approval, Implementation:**
```tsx
import { Button } from "@/components/ui/button";
import { ArrowRight } from "@phosphor-icons/react";

<Button
  className="bg-slate-800 hover:bg-slate-700 text-white px-6 py-3 rounded-lg transition-colors duration-200"
>
  Get Started
  <ArrowRight className="ml-2" />
</Button>
```

### Example 2: Typography Hierarchy

**Question First:**
```
For this content hierarchy, I'm thinking:
- Headline: Large, bold, attention-grabbing
- Subheading: Medium, regular weight
- Body: Smaller, optimized for reading

Should we go bold and contemporary, or subtle and refined?
```

**Implementation After Approval:**
```tsx
<div className="space-y-4">
  <h1 className="text-5xl font-bold tracking-tight text-slate-900">
    Headline Here
  </h1>
  <h2 className="text-2xl text-slate-600">
    Supporting subheading
  </h2>
  <p className="text-base leading-relaxed text-slate-700">
    Body text optimized for readability with proper line height.
  </p>
</div>
```

### Example 3: Unique Color Palette Suggestion

**Presenting Options:**
```
I'd like to suggest three color directions that break from typical SaaS patterns:

1. **Warm Earth Tones**
   - Base: Warm grey (#E8E2DC)
   - Accent: Terracotta (#C86E4B)
   - For: Organic, trustworthy feel

2. **Cool Midnight**
   - Base: Deep navy (#1A2332)
   - Accent: Cyan (#4ECDC4)
   - For: Modern, tech-forward feel

3. **Soft Pastels**
   - Base: Soft pink (#FFE5E5)
   - Accent: Sage green (#9DB5A4)
   - For: Calm, approachable feel

Which direction feels right for your brand?
```

## Common Patterns to Avoid

❌ **Don't:**
- Use generic SaaS blue (#3B82F6) without considering alternatives
- Default to shadows and gradients for depth
- Copy Apple's design language
- Use glass morphism effects
- Make design decisions without asking
- Implement typography without considering the font version
- Use animations that delay user actions
- Create cluttered interfaces with competing elements

✅ **Do:**
- Ask before making design decisions
- Suggest unique, contextually appropriate color pairs
- Use flat, minimal design
- Consider unconventional typography choices
- Provide immediate feedback for interactions
- Create generous white space
- Test with real devices
- Validate accessibility

## Version History

- v1.0.0 (2025-10-18): Initial release with comprehensive UI/UX design guidance

## References

For additional context, see:
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Google Fonts: https://fonts.google.com/
- Tailwind CSS Docs: https://tailwindcss.com/docs
- Shadcn UI Components: https://ui.shadcn.com/
