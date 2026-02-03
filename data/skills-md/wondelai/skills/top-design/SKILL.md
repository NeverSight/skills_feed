---
name: top-design
description: >
  Create award-winning websites and applications with design and typography rated 10/10.
  Use this skill when building premium digital experiences that match the quality of elite
  agencies like Locomotive, Studio Freight, AREA 17, Active Theory, Hello Monday, Dogstudio,
  Tonik, Instrument, Resn, and Awwwards winners. Triggers include premium design, award-winning,
  agency-level, Awwwards quality, exceptional typography, immersive experience, 10/10 design,
  portfolio site, brand website, creative agency style, top-tier web design, or when building
  sites for luxury brands, tech companies, cultural institutions, or startups requiring
  exceptional visual craft.
license: MIT
metadata:
  author: wondelai
  version: "1.3.0"
---

# Top-Design: Award-Winning Digital Experiences

Create websites and applications at the level of world-class digital agencies. This skill embodies the craft of studios that consistently win FWA, Awwwards, CSS Design Awards, and Webby Awards.

## Core Philosophy

**The agencies you're emulating share these traits:**
- Every pixel is intentional — nothing default, nothing accidental
- Typography IS the design — not decoration, but architecture
- Motion creates emotion — animation serves narrative, not novelty
- White space is a weapon — tension through restraint
- Performance is non-negotiable — 60fps or nothing

**What separates 10/10 from 8/10:**
- 8/10: Good typography, nice colors, smooth animations
- 10/10: Typography that makes you gasp, colors that feel invented, animations that tell stories

## Scoring

**Goal: 10/10.** When reviewing or creating digital experiences, rate them 0-10 using the rubric below. A 10/10 means the design would be featured on Awwwards. Always provide the current score and specific improvements needed to reach 10/10.

### Scoring Rubric

| Score | Level | Description |
|-------|-------|-------------|
| **0-2** | Amateur | Default fonts, no hierarchy, generic layout, template feel |
| **3-4** | Basic | Decent typography, some hierarchy, but forgettable |
| **5-6** | Competent | Good fundamentals, clean execution, but lacks soul |
| **7-8** | Professional | Strong typography, intentional motion, clear POV |
| **9** | Exceptional | Signature moments, memorable details, near-flawless craft |
| **10** | World-class | Would win Awwwards SOTD, defines new standards |

### Category Scoring (Each 0-10)

**TYPOGRAPHY (Weight: 25%)**
| Score | Criteria |
|-------|----------|
| 0-3 | System fonts, uniform scale, default tracking |
| 4-6 | Premium fonts, some scale contrast, basic hierarchy |
| 7-8 | Dramatic scale contrast (10:1+), perfect tracking, optical alignment |
| 9-10 | Typography IS the design—gasping moments, custom/variable fonts, type as architecture |

**VISUAL COMPOSITION (Weight: 25%)**
| Score | Criteria |
|-------|----------|
| 0-3 | Centered everything, equal spacing, rigid grid, no tension |
| 4-6 | Some asymmetry, decent spacing rhythm, basic depth |
| 7-8 | Intentional grid breaks, layered elements, strong negative space |
| 9-10 | Magnetic compositions, unexpected scale shifts, elements that breathe and surprise |

**MOTION & INTERACTION (Weight: 20%)**
| Score | Criteria |
|-------|----------|
| 0-3 | No animation or default/linear motion |
| 4-6 | Basic transitions, some scroll effects |
| 7-8 | Custom easing, orchestrated reveals, purposeful parallax |
| 9-10 | Motion that tells stories, perfectly timed choreography, scroll feels invented |

**COLOR & ATMOSPHERE (Weight: 15%)**
| Score | Criteria |
|-------|----------|
| 0-3 | Random colors, pure black/white, no mood |
| 4-6 | Cohesive palette, some atmosphere |
| 7-8 | Colors feel owned, contextual shifts, intentional contrast |
| 9-10 | Colors feel invented for this project, atmosphere you can feel |

**DETAILS & CRAFT (Weight: 15%)**
| Score | Criteria |
|-------|----------|
| 0-3 | Default cursors, no hover states, generic everything |
| 4-6 | Basic hover states, some custom elements |
| 7-8 | Custom cursor, magnetic buttons, branded selection colors |
| 9-10 | Every micro-detail considered—focus states, loading, empty states, scroll indicators |

### Quick Score Formula
```
Total = (Typography × 0.25) + (Composition × 0.25) + (Motion × 0.20) + (Color × 0.15) + (Details × 0.15)
```

---

## The 10/10 Difference: What Makes Design Exceptional

### Typography That Commands Attention

**The Gasping Moment Test:** If someone scrolls past your hero and doesn't pause, your typography isn't working.

**Scale Contrast That Shocks:**
```
WEAK:    48px headline / 16px body (3:1 ratio)
GOOD:    96px headline / 16px body (6:1 ratio)
GREAT:   180px headline / 14px body (13:1 ratio)
10/10:   Viewport-filling type that makes body text feel intimate
```

**Font Selection Hierarchy:**
```
DISPLAY/HERO: The statement maker
├── Custom/Variable fonts (preferred)
├── Foundry fonts: Pangram Pangram, Dinamo, Grilli Type, Klim, Commercial Type
├── Premium Google: Space Grotesk, Instrument Serif, Fraunces
└── NEVER: Inter, Roboto, Arial, system-ui (these are for apps, not experiences)

BODY: The workhorse
├── Match personality to display font
├── Legibility at 16-18px minimum
└── Consider: Söhne, GT America, Suisse, Neue Montreal
```

**Typography Principles:**
- Massive scale contrast: 200px hero + 14px body
- Negative tracking on large type (-0.02em to -0.05em)
- Generous line-height for body (1.5-1.7)
- Tight line-height for display (0.85-1.0)
- Optical alignment over mathematical alignment
- Text that breaks beautifully—control every line break on headlines
- Variable fonts for weight animation on hover

**The Typography Stare Test:** Blur your eyes. Does the type hierarchy still read? If everything looks the same importance when blurred, you've failed.

### Composition That Creates Tension

**The Grid Paradox:** Master the grid so you can break it with intention. Every violation should feel deliberate, not accidental.

**White Space as a Weapon:**
- Amateur: Fills every gap with content
- Pro: Uses padding liberally
- 10/10: White space creates tension, makes you lean in, controls pacing

**Asymmetric Balance:**
```css
/* Don't center—create visual tension */
.hero-title {
  /* Offset from center, aligned to grid but not centered */
  margin-left: 8.33%; /* One column offset */
  max-width: 83.33%; /* 10 of 12 columns */
}

/* Let images bleed and overlap */
.hero-image {
  margin-right: -5vw; /* Extend beyond container */
  width: calc(100% + 5vw);
}
```

**Unexpected Scale Shifts:**
- Full-viewport hero → intimate text section → massive single word → dense grid
- The rhythm of density and breathing room creates a reading experience

**The Screenshot Test:** Would someone screenshot this section and share it? If not, you're missing signature moments.

### Motion That Creates Emotion

**The Three Laws of Elite Motion:**
1. **Purpose Over Decoration**: Every animation answers "Why does this move?"
2. **Custom Curves, Never Linear**: `ease` and `linear` are banned
3. **Orchestration Over Isolation**: Elements animate in relationship, not independently

**Custom Easing (Agency Standards):**
```css
:root {
  /* These are your only easings */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
  --ease-in-out-expo: cubic-bezier(0.87, 0, 0.13, 1);

  /* NEVER use: ease, ease-in, ease-out, linear */
}
```

**Page Load Choreography:**
```
Frame 0-200ms:   Background/structure fades in
Frame 200-600ms: Hero title words slide up (staggered 80ms)
Frame 400-800ms: Hero subtitle fades up
Frame 600-900ms: Navigation items cascade down
Frame 800-1200ms: Supporting elements reveal
```

**Scroll-Triggered Sequences:**
- Elements reveal as they enter viewport (not all at once)
- Parallax used sparingly and only on non-essential elements
- Pinned sections for storytelling moments
- Horizontal scroll for galleries (with clear affordance)

**The Smooth Scroll Standard:** Default browser scroll is unacceptable. Use Lenis or Locomotive Scroll.

### Color That Feels Invented

**Approach Types:**
```
MONOCHROMATIC TENSION
├── 95% one dominant color/neutral
├── 5% accent that POPS
└── Example: Locomotive (cream + black + orange spark)

BOLD SIGNATURE
├── Own a color combination
├── Make it unmistakable
└── Example: Studio Freight (black + cream + rust)

CONTEXTUAL SHIFTING
├── Color responds to content
├── Sections have distinct palettes
└── Example: AREA 17 (adapts to each client case study)
```

**Technical Implementation:**
```css
:root {
  /* Never just 'black' or 'white' */
  --color-dark: #0a0a0a;      /* Slightly warm black */
  --color-light: #fafaf9;     /* Slightly warm white */
  --color-accent: #ff4d00;    /* A color you OWN */

  /* Functional hierarchy */
  --color-text-primary: var(--color-dark);
  --color-text-secondary: rgba(10, 10, 10, 0.6);
  --color-text-tertiary: rgba(10, 10, 10, 0.4);
  --color-surface: var(--color-light);
  --color-border: rgba(10, 10, 10, 0.1);
}
```

**The Squint Test:** Squint at your design. Do the important things stand out through contrast alone?

### Details That Signal Craft

**The Details Checklist (All Required for 10/10):**

```
CURSOR
☐ Custom cursor that reflects brand personality
☐ Cursor changes on interactive elements
☐ Magnetic effect on buttons (subtle)

SELECTION
☐ Custom ::selection color that's on-brand
☐ Selection works well on all backgrounds

HOVER STATES
☐ Every link has a considered hover state
☐ Images have scale or overlay treatment
☐ Cards transform meaningfully

FOCUS STATES
☐ Focus states are visible and beautiful
☐ Focus indicators match brand aesthetic
☐ Tab order is logical

LOADING STATES
☐ Custom skeleton/loading animation
☐ Progress indicators are designed
☐ First contentful paint is instant

EMPTY STATES
☐ Empty states are designed, not default
☐ Error states are helpful and branded
☐ 404 pages are memorable

MICRO-TYPOGRAPHY
☐ Smart quotes (" " not " ")
☐ Proper apostrophes (' not ')
☐ En/em dashes where appropriate
☐ No orphans on headlines
☐ text-wrap: balance on key text
```

### The Signature Moment

Every 10/10 project has at least one moment that makes people stop and share. Design this first.

**Types of Signature Moments:**
- A hero animation that's never been seen before
- Typography so bold it becomes the visual
- An interaction that delights unexpectedly
- A scroll sequence that tells a story
- A transition that feels like magic

**Questions to Identify Your Signature:**
1. What will people screenshot?
2. What will they describe to colleagues?
3. What will they try to reverse-engineer?
4. What makes this unmistakably THIS project?

---

## Design Process

### 1. Concept First, Code Second

Before any code, define:
```
BRAND ESSENCE: What single word captures the soul?
VISUAL TENSION: What opposing forces create interest?
SIGNATURE MOMENT: What will people screenshot and share?
TECHNICAL AMBITION: What pushes the browser's limits?
```

### 2. Design the Signature Moment First

Don't start with the header. Start with the thing that defines the experience. The header can be solved later.

### 3. Typography Sets Everything

Choose your display typeface first. Let it dictate:
- The color palette mood
- The animation style
- The spacing rhythm
- The overall personality

### 4. Motion Is Not Polish

Prototype animations early. Motion design happens alongside visual design, not after.

### 5. Ship With Restraint

3 things perfect beats 10 things mediocre. Cut ruthlessly.

---

## Reference Files

Consult these for detailed implementation:

- **[references/typography.md](references/typography.md)**: Font pairing strategies, type scale systems, advanced CSS typography
- **[references/animation-patterns.md](references/animation-patterns.md)**: Scroll animations, page transitions, micro-interactions with code
- **[references/layout-systems.md](references/layout-systems.md)**: Grid frameworks, breakpoints, responsive patterns
- **[references/technical-stack.md](references/technical-stack.md)**: Libraries, tools, performance optimization
- **[references/case-studies.md](references/case-studies.md)**: Agency technique breakdowns (Locomotive, Studio Freight, AREA 17, Hello Monday, etc.)

---

## Quality Checklist

Before considering any design complete:

```
TYPOGRAPHY
□ Display font makes a statement (not Inter/Roboto/Arial)
□ Scale contrast is dramatic (min 10:1 ratio)
□ Tracking adjusted for size (-0.02em to -0.05em on large type)
□ Line-height optimized per use case (0.9 display, 1.6 body)
□ No orphans/widows on key headlines
□ Variable font with weight animation (if applicable)

COMPOSITION
□ Grid exists but is strategically broken
□ White space creates tension and pacing
□ Hierarchy is instantly clear from across the room
□ Asymmetric balance creates visual interest
□ Elements overlap, bleed, or extend with intention
□ Unexpected scale shifts create rhythm

MOTION
□ Page load has choreographed reveal (not all at once)
□ Scroll feels custom (Lenis/Locomotive level)
□ Custom easing on everything (expo.out, power4.out)
□ Staggered animations create depth
□ 60fps verified on target devices

COLOR & ATMOSPHERE
□ No pure black (#000) or pure white (#fff)
□ Colors feel owned by this project
□ Accent color creates moments of surprise
□ Works in both light and dark contexts
□ Contextual color shifts between sections (if applicable)

DETAILS
□ Custom cursor (if appropriate for the project)
□ Selection colors are branded
□ Focus states are beautiful AND accessible
□ Loading states are designed
□ Error/empty states are crafted
□ Micro-typography is correct (smart quotes, proper dashes)

SIGNATURE
□ There is at least one screenshot-worthy moment
□ Something would make another designer stop and inspect
□ The project has a clear point of view

PERFORMANCE
□ Fonts subset and preloaded
□ Images optimized (WebP/AVIF with fallbacks)
□ Animations GPU-accelerated (transform/opacity only)
□ No layout shifts (CLS near zero)
□ LCP under 2.5s
```

---

## Anti-Patterns to Avoid

```
TYPOGRAPHY CRIMES
✗ Inter, Roboto, Arial, or system-ui as primary typeface
✗ Uniform type scale (everything within 2x of each other)
✗ Default letter-spacing on headlines
✗ Line-height: 1.5 applied universally
✗ Type that doesn't command attention

ANIMATION SINS
✗ Linear or ease easing anywhere
✗ Everything animated simultaneously
✗ Animations blocking interaction
✗ Parallax without clear purpose
✗ Default browser scroll
✗ Animations longer than 1.2s without reason

COMPOSITION FAILURES
✗ Center-aligned everything
✗ Equal spacing everywhere
✗ Grid followed rigidly without breaks
✗ Mobile as afterthought
✗ No signature moments

COLOR CRIMES
✗ Pure #000000 black
✗ Pure #ffffff white
✗ Random colors without system
✗ No clear accent
✗ Palette that could be any brand

GENERIC TELLS (Instant 10/10 Disqualification)
✗ Purple/blue gradient hero sections
✗ "Hi, I'm [Name]" portfolio intros
✗ Floating cards with drop shadows
✗ Stock photography (unedited)
✗ Visible lorem ipsum
✗ Default form styles
✗ Generic 404 pages
✗ Cookie-cutter layouts
✗ Font Awesome icons (unmodified)

AI SLOP (Immediate Rejection)
✗ ANY emoji in professional interfaces
✗ Purple-to-blue or purple-to-pink gradients (the "AI gradient")
✗ Generic "futuristic" glassmorphism everywhere
✗ Overly smooth, soulless illustrations (the "corporate Memphis" successor)
✗ Teal + coral + purple color schemes (every AI startup ever)
✗ "Clean and modern" that means "generic and forgettable"
✗ Gradients on everything because "it looks techy"
✗ Neon accents on dark backgrounds (cyberpunk cliché)
✗ Abstract blob shapes as decoration
✗ Particle effects without purpose
✗ "Magical" sparkle animations
✗ The same Figma community hero section everyone uses
```

---

## Implementation Notes

1. **Start with the signature moment** — design the thing that defines the experience first
2. **Conceptualize desktop-first, build mobile-first** — dream big, implement progressively
3. **Prototype animations early** — motion is not a polish step, it's core to the design
4. **Test on real devices** — simulators lie about performance and feel
5. **Ship with restraint** — 3 things perfect beats 10 things mediocre
6. **Sweat the micro-details** — craft lives in the 1% others skip
7. **Design the states** — hover, focus, loading, empty, error all matter
8. **Own your constraints** — every limitation is a design opportunity
9. **Use project conventions** — if Tailwind 4+ and/or shadcn/ui are available, build on top of them rather than fighting them. Extend their design tokens, customize their components, and use their patterns as a foundation for 10/10 craft
