---
name: elevated-design
description: Create sophisticated, Apple-inspired web interfaces with refined aesthetics and corporate elegance. Emphasizes generous whitespace, ultra-precise typography, asymmetric layouts, and purposeful interactions. Combines minimalist design philosophy with premium brand execution. Use when building premium landing pages, marketing sections, product showcases, or corporate interfaces that demand visual sophistication beyond standard business UI.
---

# Elevated Design System

A sophisticated design philosophy inspired by Apple's corporate design language—creating web interfaces that feel crafted by experts at the top of their field. This approach combines minimalist precision with emotional resonance, transforming standard web components into refined, gallery-worthy experiences that command attention and inspire confidence.

## When to Use This Skill

Activate this skill when users request:
- Premium landing pages or hero sections
- Corporate marketing websites that command authority
- Product showcases with sophisticated aesthetics
- Feature sections that feel editorial yet professional
- Interfaces that evoke quality, precision, and confidence
- Apple-style minimalist corporate design
- High-end SaaS product pages
- Brand experiences that need to inspire trust

**Trigger phrases:**
- "Make it more sophisticated"
- "Create an Apple-style design"
- "Design something that looks premium/expensive"
- "Make it feel like a luxury tech brand"
- "Use the elevated/Apple design approach"
## Design Philosophy

### The Pillars of Elevated Design (Apple-Inspired)

1. **Generous Whitespace as a Strategic Tool**
   - Space is not empty—it's intentional, communicative, and confident
   - Large margins and padding create breathing room and hierarchy
   - Elements float in space, commanding individual attention
   - Whitespace guides the eye with purposeful rhythm
   - **Apple principle:** Less is exponentially more

2. **Ultra-Precise Typography**
   - San Francisco-inspired system fonts with exceptional legibility
   - Light to regular weights (300-400) for sophistication
   - Dramatic scale contrasts (72px headlines, 48px subheads)
   - Tight tracking (-0.02em) for headlines, optical spacing for body
   - Text color in subtle grays (never #000000, always #1d1d1f or similar)
   - **Apple principle:** Typography is the interface

3. **Grid-Based Asymmetry**
   - Apple's 12-column grid with intentional breaks
   - Use 7-5 or 8-4 splits for visual tension
   - Alternate scale: large hero images, compact supporting content
   - Balance asymmetry with perfect alignment
   - Create compositions that feel both free and precise
   - **Apple principle:** Controlled chaos breeds sophistication

4. **Restrained Color Palettes**
   - Near-monochromatic with surgical color accents
   - Neutral foundation: white, off-white (#f5f5f7), cool gray (#1d1d1f)
   - Brand accent used for CTAs only (1-2% of design)
   - Gradients are subtle and purpose-driven
   - Photography and product imagery provide color, not UI
   - **Apple principle:** Color is a tool, not decoration

5. **Purposeful Interactions**
   - Micro-interactions that feel inevitable, not surprising
   - Smooth 400-600ms transitions (slower = more premium)
   - Hover states that shift weight, not color
   - Scroll-triggered reveals with momentum
   - Touch targets are generous (44x44px minimum)
   - **Apple principle:** Motion with meaning

6. **Obsessive Attention to Detail**
   - Sub-pixel alignment wherever possible
   - Consistent 8px baseline grid
   - Typography with optical adjustments (not just math)
   - Glass morphism and depth through layering
   - Perfect icon-to-text alignment
### Typography (Apple System)

**Font Stack (San Francisco-Inspired):**
```css
/* Tailwind Default (closest to SF Pro) */
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

**Font Weights:**
```html
font-light     → 300  /* Body copy, descriptions - Apple's go-to */
font-normal    → 400  /* Standard text, balanced */
font-medium    → 500  /* Subtle emphasis, nav items */
font-semibold  → 600  /* Headlines, but use sparingly */
font-bold      → 700  /* Avoid - too heavy for elevated design */
```

**Type Scale (Apple-Inspired Dramatic Hierarchy):**
```html
text-xs    → 12px   /* Fine print, footnotes, legal */
text-sm    → 14px   /* Supporting text, captions */
text-base  → 16px   /* Body text (Apple's minimum) */
text-lg    → 18px   /* Large body, comfortable reading */
text-xl    → 20px   /* Small headings, emphasized text */
text-2xl   → 24px   /* Card titles, section labels */
text-3xl   → 30px   /* Subsection headings */
text-4xl   → 36px   /* Page titles */
text-5xl   → 48px   /* Hero headlines */
text-6xl   → 60px   /* Large hero text */
text-7xl   → 72px   /* Statement headlines (Apple events) */
text-8xl   → 96px   /* Ultra-dramatic (use with extreme restraint) */
text-9xl   → 128px  /* iPhone reveal style (hero images only) */
```

**Letter Spacing (Optical Precision):**
```html
tracking-tighter  → -0.05em   /* Massive headlines (text-8xl+) */
tracking-tight    → -0.025em  /* Large headlines (text-5xl+) */
tracking-normal   → 0em       /* Body text, natural spacing */
tracking-wide     → 0.025em   /* Small text for legibility */
tracking-wider    → 0.05em    /* Uppercase labels */
tracking-widest   → 0.1em     /* Micro labels (11px uppercase) */
```

**Line Height (Apple Standard):**
```html
leading-none      → 1       /* Massive display type only */
leading-tight     → 1.1     /* Large headlines (text-5xl+) */
leading-snug      → 1.2     /* Headlines (text-2xl to text-4xl) */
leading-normal    → 1.5     /* Body text - Apple's preferred */
leading-relaxed   → 1.625   /* Long-form reading */
```html
text-xs    → 12px   /* Metadata, copyright */
text-sm    → 14px   /* Small body text */
text-base  → 16px   /* Standard body */
text-lg    → 18px   /* Large body */
text-xl    → 20px   /* Small headings */
text-2xl   → 24px   /* Card titles */
text-3xl   → 30px   /* Section headings */
text-4xl   → 36px   /* Page titles */
text-5xl   → 48px   /* Hero headlines */
text-6xl   → 60px   /* Large hero text */
```

**Letter Spacing:**
```html
tracking-tight    → -0.025em  /* Large headlines */
tracking-normal   → 0em       /* Body text */
tracking-wide     → 0.025em   /* Small labels */
tracking-wider    → 0.05em    /* Uppercase labels */
tracking-widest   → 0.1em     /* Ultra-wide labels */
```

### Color Philosophy

**Sophisticated Neutrals:**
```html
<!-- Text (Never pure black) -->
text-slate-900  → #0f172a  /* Primary text */
text-slate-600  → #475569  /* Secondary text */
text-slate-500  → #64748b  /* Tertiary text */
text-slate-400  → #94a3b8  /* Subtle text, labels */

### Spacing System (Apple's 8px Grid)

**The 8px Baseline (Apple's Standard):**
Every measurement should be divisible by 8px for perfect rhythm.

**Component Spacing:**
```html
p-4   → 16px   /* Compact elements (badges, pills) */
p-6   → 24px   /* Small cards, tight content */
p-8   → 32px   /* Standard card padding (minimum) */
p-10  → 40px   /* Comfortable card padding */
p-12  → 48px   /* Large cards, feature sections */
p-16  → 64px   /* Extra-large padding, hero sections */
p-20  → 80px   /* Apple event-style spacing */
p-24  → 96px   /* Statement sections */
```

**Section Spacing (Generous, like Apple):**
```html
py-12  → 48px   /* Compact sections */
py-16  → 64px   /* Standard sections */
py-20  → 80px   /* Comfortable sections */
py-24  → 96px   /* Large sections */
py-32  → 128px  /* Hero sections, dramatic reveals */
py-40  → 160px  /* Apple event-style spacing */
py-48  → 192px  /* Ultra-premium sections */
```

**Gap & Margins (8px increments):**
```html
gap-4   → 16px   /* Tight groups */
gap-6   → 24px   /* Related elements */
gap-8   → 32px   /* Standard separation */
gap-12  → 48px   /* Section boundaries */
gap-16  → 64px   /* Large separation */
gap-20  → 80px   /* Dramatic separation */
gap-24  → 96px   /* Hero to content transition */

mb-4   → 16px    /* Paragraph spacing */
mb-6   → 24px    /* Subsection spacing */
mb-8   → 32px    /* Element separation */
mb-12  → 48px    /* Section separation */
mb-16  → 64px    /* Large separation */
mb-20  → 80px    /* Dramatic separation */
mb-24  → 96px    /* Hero to section */
```

**Layout Containers (Apple's Approach):**
```html
max-w-screen-2xl → 1536px  /* Ultra-wide (product grids) */
max-w-7xl        → 1280px  /* Wide layouts (Apple default) */
max-w-6xl        → 1152px  /* Standard editorial */
max-w-5xl        → 1024px  /* Narrow, focused content */
max-w-4xl        → 896px   /* Article-style layouts */
max-w-3xl        → 768px   /* Long-form reading */
max-w-2xl        → 672px   /* Comfortable reading width */
```

**Responsive Padding (Apple's breakpoint strategy):**
```html
px-6 sm:px-8 lg:px-12     /* Standard responsive padding */
px-8 sm:px-12 lg:px-20    /* Generous responsive padding */
py-12 sm:py-16 lg:py-24   /* Section responsive padding */
py-16 sm:py-24 lg:py-32   /* Hero responsive padding */
```2  → 48px   /* Extra large padding */
p-16  → 64px   /* Section padding */

<!-- Section Spacing -->
py-16  → 64px   /* Minimum section */
py-24  → 96px   /* Standard section */
py-32  → 128px  /* Large section */

<!-- Margins -->
mb-8   → 32px   /* Element separation */
mb-12  → 48px   /* Section separation */
mb-16  → 64px   /* Large separation */
mb-24  → 96px   /* Dramatic separation */
```

**Layout Containers:**
```html
max-w-7xl  → 1280px  /* Wide layouts */
max-w-6xl  → 1152px  /* Standard */
max-w-5xl  → 1024px  /* Narrow, focused */
```

### Border Radius (Larger)

```html
rounded-xl   → 12px   /* Minimum for cards */
rounded-2xl  → 16px   /* Standard cards */
rounded-3xl  → 24px   /* Large images */
```

---

## Apple-Inspired Button System

**Primary CTA (Apple Blue):**
```html
<a href="#" class="inline-flex items-center justify-center gap-2 px-5 py-3 bg-[#0071e3] text-white text-[15px] font-normal rounded-xl hover:bg-[#0077ED] transition-all duration-400">
  <span>Buy now</span>
</a>
```

**Secondary Button (Outlined):**
```html
<button class="inline-flex items-center justify-center gap-2 px-5 py-3 border-2 border-[#0071e3] text-[#0071e3] text-[15px] font-normal rounded-xl hover:bg-[#0071e3]/5 transition-all duration-400">
  <span>Learn more</span>
</button>
```

**Tertiary Text Link (Apple style):**
```html
<a href="#" class="inline-flex items-center gap-1.5 text-[#0071e3] text-[15px] font-normal hover:underline">
  <span>Learn more</span>
  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
  </svg>
</a>
```

**Large CTA (Hero Section):**
```html
<a href="#" class="inline-flex items-center justify-center gap-2 px-7 py-4 bg-[#0071e3] text-white text-base font-normal rounded-xl hover:bg-[#0077ED] transition-all duration-400 shadow-lg hover:shadow-xl">
  <span>Get started</span>
</a>
```

**Design Rules:**
- Padding: `px-5 py-3` for standard, `px-7 py-4` for large
- Border radius: `rounded-xl` (12px)
- Font size: 15px (Apple's preferred button size)
- Transitions: `duration-400` for premium feel
- Hover: Subtle color shift, never dramatic transformations

---

## Component Patterns

### Feature Card (Elevated Style)

**Asymmetric Large Card:**
```html
<div class="col-span-12 lg:col-span-7 group">
  <div class="relative h-full bg-slate-50 border border-slate-100 rounded-2xl p-10 hover:bg-white hover:border-slate-200 transition-all duration-300">
    
    <!-- Icon with refined treatment -->
    <div class="mb-8">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-xl border border-blue-200 bg-blue-50">
        <i class="ri-icon-name text-3xl text-[#1b75bc]"></i>
      </div>
    </div>
    
    <!-- Light typography -->
    <h3 class="text-2xl font-light text-slate-900 mb-4 tracking-tight">
      Feature Title
    </h3>
    
    <p class="text-base text-slate-500 leading-relaxed mb-8 max-w-xl">
      Description with refined tone and generous spacing.
    </p>
    
    <!-- Minimal list with dots -->
    <div class="space-y-3 pt-6 border-t border-slate-200">
      <div class="flex items-center gap-3 text-sm text-slate-600">
        <div class="w-1 h-1 rounded-full bg-[#1b75bc]"></div>
        <span class="font-light">Feature item</span>
      </div>
    </div>
  </div>
</div>
```

**Asymmetric Compact Card:**
```html
<div class="col-span-12 lg:col-span-5 group">
  <div class="relative h-full bg-slate-50 border border-slate-100 rounded-2xl p-8 hover:bg-white hover:border-slate-200 transition-all duration-300">
    
    <div class="mb-6">
      <div class="inline-flex items-center justify-center w-14 h-14 rounded-xl border border-purple-200 bg-purple-50">
        <i class="ri-icon-name text-2xl text-purple-600"></i>
      </div>
    </div>
    
    <h3 class="text-xl font-light text-slate-900 mb-3 tracking-tight">
      Feature Title
    </h3>
    
    <p class="text-sm text-slate-500 leading-relaxed mb-6">
      Refined description.
    </p>
    
    <div class="space-y-2.5 pt-4 border-t border-slate-200">
      <div class="flex items-center gap-2.5 text-xs text-slate-600">
        <div class="w-1 h-1 rounded-full bg-[#1b75bc]"></div>
        <span class="font-light">Feature item</span>
      </div>
    </div>
  </div>
</div>
```

### Section Header (Elevated)

**Minimal with Uppercase Label:**
```html
<div class="mb-24">
  <p class="text-[11px] font-medium tracking-[0.2em] text-slate-400 uppercase mb-6">
    Section Label
  </p>
  <h2 class="text-5xl sm:text-6xl font-light text-slate-900 tracking-tight leading-[1.1] max-w-3xl">
    Primary headline with dramatic scale.
    <span class="text-slate-400">Optional subtle accent.</span>
  </h2>
</div>
```

**With Description:**
```html
<div class="mb-20">
  <p class="text-xs font-medium tracking-wider text-slate-400 uppercase mb-4">
    Features
  </p>
  <h2 class="text-4xl sm:text-5xl font-light text-slate-900 tracking-tight leading-tight mb-6">
    Everything your garage needs.
    <br/>
    <span class="text-slate-400">Nothing it doesn't.</span>
  </h2>
  <p class="text-lg text-slate-500 max-w-2xl">
    Refined description with generous spacing and thoughtful typography.
  </p>
</div>
```

### Asymmetric Grid Layout

**7-5 Split Pattern:**
```html
<div class="grid grid-cols-12 gap-8">
  <!-- Large card (7 columns) -->
  <div class="col-span-12 lg:col-span-7">
    <!-- Large content -->
  </div>
  
  <!-- Compact card (5 columns) -->
  <div class="col-span-12 lg:col-span-5">
    <!-- Compact content -->
  </div>
  
  <!-- Compact card (5 columns) -->
  <div class="col-span-12 lg:col-span-5">
    <!-- Compact content -->
  </div>
  
  <!-- Large card (7 columns) -->
  <div class="col-span-12 lg:col-span-7">
    <!-- Large content -->
  </div>
</div>
```

### Background Elements (Subtle)

**Layered Backgrounds:**
```html
<section class="relative py-32 bg-white overflow-hidden">
  <!-- Ultra-subtle background -->
  <div class="absolute inset-0 opacity-[0.03]">
    <div class="absolute top-20 left-10 w-96 h-96 rounded-full bg-[#1b75bc]"></div>
    <div class="absolute bottom-20 right-10 w-96 h-96 rounded-full bg-slate-900"></div>
  </div>
  
  <div class="relative">
    <!-- Content -->
  </div>
</section>
```

### Closing Elements (Refined)

**Subtle Divider:**
```html
<div class="mt-24 text-center">
  <div class="inline-flex items-center gap-2 text-xs text-slate-400 tracking-wider">
    <div class="w-12 h-px bg-slate-200"></div>
    <span class="uppercase">Crafted for excellence</span>
    <div class="w-12 h-px bg-slate-200"></div>
  </div>
</div>
```

---

## Design Rules (Apple Edition)

### Do's ✓

- **Use generous spacing** - Follow the 8px grid religiously
- **Embrace light font weights** - font-light (300) for almost everything
- **Create intentional asymmetry** - 7-5 splits, alternating scales
- **Surgical color use** - Near-monochrome with one accent color
- **Dramatic type scales** - text-7xl for heroes, text-base minimum for body
- **Minimal bullets** - 1px dots (w-1 h-1) or subtle checkmarks
- **Refined borders** - Use Apple's #d2d2d7 or border-slate-200
- **Slow, smooth transitions** - duration-400 to duration-600
- **Glass morphism** - backdrop-blur with opacity for depth
- **Perfect optical alignment** - Not just mathematical, but visual balance
- **Generous touch targets** - Minimum 44x44px for all interactive elements
- **Editorial photography** - High-res, professional, generous sizing
- **Natural shadows** - Subtle, directional, mimicking light from above

### Don'ts ✗

- **Avoid tight spacing** - Never break the 8px grid
- **Skip heavy fonts** - Never use font-bold (700+)
- **No rigid symmetry** - Avoid 6-6, 4-4-4, 3-3-3-3 grids
- **No color chaos** - Stick to neutrals + ONE accent
- **Small type** - Never go below 16px for body text
- **Icon overload** - Icons should whisper, not shout
- **Thick borders** - Never use 2px+ borders except on buttons
- **Fast transitions** - Avoid duration-150 or less
- **Flat design** - Always add subtle depth through shadows or glass
- **Cluttered layouts** - When in doubt, remove elements
- **Small touch targets** - Never smaller than 44x44px
- **Stock photography** - No generic business people smiling at laptops
- **Heavy drop shadows** - Avoid pure black shadows

---

## Typography Hierarchy

### Landing Page Example

```html
<!-- Hero Section -->
<h1 class="text-6xl sm:text-7xl font-light text-slate-900 tracking-tight leading-[1.05]">
  Primary Headline
</h1>
<p class="text-xl text-slate-500 font-light mt-6 max-w-2xl leading-relaxed">
  Supporting description with generous sizing.
</p>

<!-- Section Heading -->
<h2 class="text-5xl font-light text-slate-900 tracking-tight mb-16">
  Section Title
</h2>

<!-- Subsection -->
<h3 class="text-2xl font-light text-slate-900 mb-4">
  Subsection Heading
</h3>

<!-- Body Text -->
<p class="text-base text-slate-500 leading-relaxed">
  Body copy with comfortable line height.
</p>

<!-- Small Labels -->
<span class="text-xs font-medium tracking-wider text-slate-400 uppercase">
  Label
</span>
```

---

## Color Usage Guidelines

### Primary Content
- Headlines: `text-slate-900`
- Body text: `text-slate-500` or `text-slate-600`
- Labels: `text-slate-400`
- Subtle text: `text-slate-400`

### Backgrounds
- Page: `bg-white` or `bg-slate-50`
- Cards: `bg-slate-50` on white, or `bg-white` on slate-50
- Hover states: Shift from slate-50 to white

### Accents
- Primary brand: Use for tiny elements only (dots, small icons)
- Borders: `border-slate-100` or `border-slate-200`
- Never use accent color for large areas

---

## Animation Philosophy

**Smooth & Purposeful:**
```html
<!-- Standard transition -->
transition-all duration-300

<!-- Subtle hover states -->
hover:bg-white hover:border-slate-200

<!-- Refined color shifts -->
group-hover:bg-blue-100 transition-colors duration-300
```

**Principles:**
- Transitions should feel like water, not electricity
- Use 300ms as standard duration
- Avoid sudden changes
- Hover states should whisper, not shout

---

## Responsive Approach

**Mobile First with Generous Breakpoints:**
```html
<!-- Scale down gracefully -->
<h1 class="text-4xl sm:text-5xl lg:text-6xl font-light">
  Headline
</h1>

<!-- Padding scales -->
<div class="px-6 py-16 sm:px-8 sm:py-24 lg:px-12 lg:py-32">

<!-- Grid adapts -->
<div class="grid grid-cols-12 gap-6 lg:gap-8">
  <div class="col-span-12 lg:col-span-7">
```

---

## Complete Section Example

```html
<section class="relative py-32 bg-white overflow-hidden">
  <!-- Subtle background -->
  <div class="absolute inset-0 opacity-[0.03]">
    <div class="absolute top-20 left-10 w-96 h-96 rounded-full bg-[#1b75bc]"></div>
    <div class="absolute bottom-20 right-10 w-96 h-96 rounded-full bg-slate-900"></div>
  </div>

  <div class="relative max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      
    <!-- Section Header -->
    <div class="mb-24">
      <p class="text-[11px] font-medium tracking-[0.2em] text-slate-400 uppercase mb-6">
        Features
      </p>
      <h2 class="text-5xl sm:text-6xl font-light text-slate-900 tracking-tight leading-[1.1] max-w-3xl">
        Everything your garage needs.
        <br/>
        <span class="text-slate-400">Nothing it doesn't.</span>
      </h2>
    </div>

    <!-- Asymmetric Grid -->
    <div class="grid grid-cols-12 gap-8">
      
      <!-- Large Card -->
      <div class="col-span-12 lg:col-span-7 group">
        <div class="relative h-full bg-slate-50 border border-slate-100 rounded-2xl p-10 hover:bg-white hover:border-slate-200 transition-all duration-300">
          <div class="mb-8">
            <div class="inline-flex items-center justify-center w-16 h-16 rounded-xl border border-blue-200 bg-blue-50">
              <i class="ri-calendar-event-line text-3xl text-[#1b75bc]"></i>
            </div>
          </div>
          
          <h3 class="text-2xl font-light text-slate-900 mb-4 tracking-tight">
            Never miss an appointment
          </h3>
          
          <p class="text-base text-slate-500 leading-relaxed mb-8 max-w-xl">
            Customers book online 24/7 while automatic reminders keep your schedule full and your team productive.
          </p>
          
          <div class="space-y-3 pt-6 border-t border-slate-200">
            <div class="flex items-center gap-3 text-sm text-slate-600">
              <div class="w-1 h-1 rounded-full bg-[#1b75bc]"></div>
              <span class="font-light">24/7 online booking</span>
            </div>
            <div class="flex items-center gap-3 text-sm text-slate-600">
              <div class="w-1 h-1 rounded-full bg-[#1b75bc]"></div>
              <span class="font-light">Auto SMS/email reminders</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Compact Card -->
      <div class="col-span-12 lg:col-span-5 group">
        <div class="relative h-full bg-slate-50 border border-slate-100 rounded-2xl p-8 hover:bg-white hover:border-slate-200 transition-all duration-300">
          <div class="mb-6">
            <div class="inline-flex items-center justify-center w-14 h-14 rounded-xl border border-purple-200 bg-purple-50">
              <i class="ri-file-list-3-line text-2xl text-purple-600"></i>
            </div>
          </div>
          
          <h3 class="text-xl font-light text-slate-900 mb-3 tracking-tight">
            Digital job tracking
          </h3>
          
          <p class="text-sm text-slate-500 leading-relaxed mb-6">
            Replace paper trails with real-time updates customers can follow.
          </p>
          
          <div class="space-y-2.5 pt-4 border-t border-slate-200">
            <div class="flex items-center gap-2.5 text-xs text-slate-600">
              <div class="w-1 h-1 rounded-full bg-[#1b75bc]"></div>
              <span class="font-light">Instant estimates</span>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Closing Element -->
    <div class="mt-24 text-center">
      <div class="inline-flex items-center gap-2 text-xs text-slate-400 tracking-wider">
        <div class="w-12 h-px bg-slate-200"></div>
        <span class="uppercase">Crafted for automotive excellence</span>
        <div class="w-12 h-px bg-slate-200"></div>
      </div>
    </div>

  </div>
</section>
```

---

## When to Use vs. Standard Design

### Use Elevated/Apple Design For:
- 🎯 Landing pages and marketing sites
- 🎯 Product showcases and launch pages
- 🎯 Premium feature sections
- 🎯 Brand experiences and "About" pages
- 🎯 Corporate websites that need authority
- 🎯 High-end e-commerce product pages
- 🎯 Portfolio presentations
- 🎯 Event/conference websites
- 🎯 SaaS pricing and features pages

### Use Standard Gixat Design For:
- 📊 Application dashboards
- 📊 Data tables and complex forms
- 📊 Administrative interfaces
- 📊 Internal tools and utilities
- 📊 High-density information displays
- 📊 Real-time monitoring interfaces

### Hybrid Approach:
Combine both systems—use Elevated Design for marketing sections and Standard Design for functional app areas. The transition should feel natural:
- Marketing pages → Elevated Design
- Dashboard/App → Standard Design
- Settings/Profile → Standard Design with elevated touches

---

## Accessibility (Apple Standard)

**Touch Targets (44x44px Minimum):**
```html
<!-- All interactive elements -->
<button class="min-w-[44px] min-h-[44px]">

<!-- Generous padding ensures touch target -->
<a class="inline-flex items-center px-5 py-3">  <!-- Results in 44px+ height -->
```

**Contrast Ratios (WCAG AAA when possible):**
```html
<!-- Apple's text colors pass AAA contrast on white -->
text-[#1d1d1f] on bg-white → 15.8:1 (AAA ✓)
text-[#424245] on bg-white → 10.2:1 (AAA ✓)
text-[#6e6e73] on bg-white → 5.4:1 (AA ✓)
```

**Reduced Motion:**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Screen Reader Optimizations:**
```html
<!-- Proper semantic structure -->
<nav aria-label="Main navigation">
<main aria-label="Main content">
<button aria-label="Close menu" aria-expanded="false">

<!-- Hide decorative elements -->
<div aria-hidden="true">

<!-- Skip to content link -->
<a href="#main-content" class="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

---

## Checklist for Apple-Style Design

Before finalizing any component, verify:

- [ ] **8px Grid**: All spacing divisible by 8
- [ ] **Typography**: Using font-light (300) for most text
- [ ] **Type Scale**: Dramatic hierarchy (text-7xl heroes, text-base+ body)
- [ ] **Colors**: Near-monochrome with one surgical accent
- [ ] **Spacing**: Generous padding (minimum p-8 for cards, py-24 for sections)
- [ ] **Border Radius**: Using rounded-2xl (16px) for cards
- [ ] **Shadows**: Subtle, natural direction (light from above)
- [ ] **Transitions**: Slow (duration-400 to duration-600)
- [ ] **Glass Morphism**: backdrop-blur with opacity where appropriate
- [ ] **Asymmetry**: Using 7-5 or 8-4 grid splits
- [ ] **Touch Targets**: Minimum 44x44px for all interactive elements
- [ ] **Contrast**: Meeting WCAG AA at minimum
- [ ] **Reduced Motion**: Respecting user preferences
- [ ] **Semantics**: Proper HTML5 and ARIA labels
- [ ] **Responsive**: Mobile-first with graceful scaling

---

*This elevated design system brings Apple's corporate design excellence to web interfaces—combining minimalist precision with emotional resonance to create experiences that feel both authoritative and approachable.*
