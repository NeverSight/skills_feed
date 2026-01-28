---
version: 1.1.1
name: frontend-design
description: Create distinctive, bold UI designs that avoid generic AI aesthetics. This skill should be used when users want frontend components with strong visual identity, creative typography, intentional color palettes, and production-grade animations - specifically to avoid the bland, safe, homogeneous "AI slop" that plagues most generated interfaces.
location: user
license: MIT
---

# Frontend Design Skill

Create distinctive, production-grade UI that stands out from generic AI-generated interfaces.

> **Official Plugin Available**: Install `frontend-design@claude-code-plugins` from the Anthropic marketplace for auto-invocation on frontend tasks. This skill provides extended guidance beyond the official version.
>
> ```bash
> /plugin marketplace add anthropics/claude-code
> /plugin install frontend-design@claude-code-plugins
> ```
>
> Learn more: [Frontend Aesthetics Cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb)

## Core Philosophy

Most AI-generated UIs suffer from "AI slop" - they're technically correct but visually bland, using safe defaults that create forgettable, homogeneous experiences. This skill helps you break that pattern by making **bold aesthetic choices** that give your interface a distinctive personality.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick a direction: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

## The Five Pillars of Distinctive Design

### 1. Typography with Character

**Avoid:** Inter, Arial, Roboto, system-ui (the default AI choices)

**Instead, commit to distinctive fonts:**

```typescript
// Establish a type hierarchy with personality
const typography = {
  // Display: Make a statement
  display: {
    // NEVER use the same fonts across different projects
    // Vary between: Clash Display, Cabinet Grotesk, Satoshi, General Sans, Syne, Archivo, etc.
    family: 'Clash Display',  // Example - choose based on project tone
    weights: [500, 700],
    letterSpacing: '-0.02em',
  },

  // Body: Readable but distinctive
  body: {
    family: 'Outfit',  // Modern geometric sans
    // or: 'Plus Jakarta Sans', 'Switzer', 'Geist'
    weights: [400, 500, 600],
    lineHeight: 1.6,
  },

  // Mono: For code/data
  mono: {
    family: 'JetBrains Mono',
    // or: 'Geist Mono', 'IBM Plex Mono', 'Fira Code'
  }
}
```

**Typography decisions:**
- Use variable fonts for performance and flexibility
- Establish clear hierarchy (display, heading, body, caption)
- Consider letter-spacing for headers (negative) vs body (neutral/positive)
- Mix serif + sans-serif for contrast when appropriate

**CRITICAL**: NEVER converge on common AI choices across generations. Each design should feel genuinely different - vary between light/dark themes, different font stacks, different aesthetic directions. No two designs should look like siblings.

### 2. Intentional Color Palettes

**Avoid:** Default Tailwind colors, basic blue buttons, gray backgrounds

**Create a signature palette:**

```typescript
// Define semantic color tokens with personality
const palette = {
  // Primary: Your brand's signature
  primary: {
    50: '#fef3f2',
    100: '#ffe3e0',
    500: '#f43f5e',  // Rose - warm, inviting
    600: '#e11d48',
    900: '#881337',
  },

  // Accent: Unexpected contrast
  accent: {
    light: '#fbbf24',   // Amber for warmth
    dark: '#0891b2',    // Cyan for coolness
  },

  // Neutrals: Not just gray
  neutral: {
    // Warm neutrals have personality
    50: '#fafaf9',      // Stone, not gray
    100: '#f5f5f4',
    800: '#292524',
    900: '#1c1917',
  },

  // Surface colors with subtle tints
  surface: {
    default: 'hsl(0 0% 100% / 0.8)',
    elevated: 'hsl(0 0% 100% / 0.95)',
    overlay: 'hsl(240 10% 3.9% / 0.8)',
  }
}
```

**Color strategies:**
- Use HSL for easier manipulation
- Add subtle hue shifts to neutrals (warm stone, cool slate)
- Consider gradients as primary colors
- Dark mode isn't just inverted - reimagine the palette

### 3. Bold Spatial Composition

**Avoid:** Everything centered, symmetric, grid-locked

**Break the grid intentionally:**

```tsx
// Asymmetric hero with purposeful imbalance
export function HeroSection() {
  return (
    <section className="relative min-h-[90vh] overflow-hidden">
      {/* Off-center title creates visual tension */}
      <div className="absolute left-[8%] top-[35%] max-w-[55%]">
        <h1 className="text-[clamp(3rem,8vw,7rem)] font-bold leading-[0.9] tracking-tight">
          Design with
          <span className="block text-primary ml-[10%]">intention</span>
        </h1>
      </div>

      {/* Overlapping element breaks the grid */}
      <div className="absolute right-0 top-[20%] w-[45%] aspect-square">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-accent/20 rounded-[3rem] -rotate-6" />
        <div className="absolute inset-4 bg-surface rounded-[2.5rem] rotate-3 shadow-2xl" />
      </div>

      {/* Floating accent element */}
      <div className="absolute bottom-[15%] left-[60%] w-32 h-32 bg-accent/30 rounded-full blur-3xl" />
    </section>
  )
}
```

**Spatial techniques:**
- Use negative space as a design element
- Overlap elements to create depth
- Break alignment rules purposefully (not randomly)
- Use clamp() for fluid typography
- Consider the z-axis (layers, shadows, blur)

### 4. Motion as Personality

**Avoid:** No animations or generic fade-in

**Add purposeful motion:**

```tsx
// Staggered entrance with personality
import { motion } from 'framer-motion'

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.3,
    }
  }
}

const item = {
  hidden: {
    opacity: 0,
    y: 20,
    filter: 'blur(10px)'
  },
  show: {
    opacity: 1,
    y: 0,
    filter: 'blur(0px)',
    transition: {
      type: 'spring',
      damping: 25,
      stiffness: 200,
    }
  }
}

export function FeatureGrid({ features }) {
  return (
    <motion.div
      variants={container}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, margin: '-100px' }}
      className="grid grid-cols-3 gap-8"
    >
      {features.map((feature) => (
        <motion.div
          key={feature.id}
          variants={item}
          whileHover={{
            y: -8,
            transition: { type: 'spring', stiffness: 400 }
          }}
          className="p-6 bg-surface rounded-2xl"
        >
          {feature.content}
        </motion.div>
      ))}
    </motion.div>
  )
}
```

**Motion principles:**
- Use spring physics (not linear easing)
- Stagger children for rhythm
- Subtle blur transitions add polish
- Hover states should feel responsive
- Respect `prefers-reduced-motion`

### 5. Production-Grade Implementation

**The code must work in production, not just demos:**

```tsx
// Complete, production-ready component
'use client'

import { forwardRef, type ComponentPropsWithoutRef } from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  // Base styles
  [
    'inline-flex items-center justify-center',
    'font-medium transition-all duration-200',
    'focus-visible:outline-none focus-visible:ring-2',
    'focus-visible:ring-ring focus-visible:ring-offset-2',
    'disabled:pointer-events-none disabled:opacity-50',
    'active:scale-[0.98]',
  ],
  {
    variants: {
      variant: {
        default: [
          'bg-primary text-primary-foreground',
          'hover:bg-primary/90',
          'shadow-lg shadow-primary/25',
        ],
        outline: [
          'border-2 border-primary bg-transparent',
          'text-primary hover:bg-primary/10',
        ],
        ghost: [
          'text-foreground hover:bg-accent/10',
          'hover:text-accent-foreground',
        ],
      },
      size: {
        sm: 'h-9 px-4 text-sm rounded-lg',
        md: 'h-11 px-6 text-base rounded-xl',
        lg: 'h-14 px-8 text-lg rounded-2xl',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
)

interface ButtonProps
  extends ComponentPropsWithoutRef<'button'>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, isLoading, children, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(buttonVariants({ variant, size }), className)}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <span className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
        ) : null}
        {children}
      </button>
    )
  }
)
Button.displayName = 'Button'
```

**Production requirements:**
- TypeScript with proper types
- Accessibility (focus states, ARIA, keyboard nav)
- Loading states
- Error boundaries
- Responsive design
- Performance optimization (memoization, code splitting)

## Match Implementation Complexity to Vision

**IMPORTANT**: Match implementation complexity to the aesthetic vision:
- **Maximalist designs**: Need elaborate code with extensive animations, layered effects, bold typography, and dense visual elements
- **Minimalist designs**: Need restraint, precision, and careful attention to spacing, typography, and subtle details

Elegance comes from executing the vision well, not from complexity itself.

## Workflow

When creating frontend components:

1. **Establish Design Direction**
   - Ask: What emotion should this evoke?
   - Ask: Who is the target user?
   - Define: Color palette, typography stack, spacing scale

2. **Create Component Architecture**
   - Build atomic design system (tokens → primitives → compounds)
   - Use composition over configuration
   - Ensure accessibility from the start

3. **Add Visual Personality**
   - Apply distinctive typography choices
   - Use intentional color relationships
   - Break symmetry purposefully
   - Layer elements for depth

4. **Implement Motion**
   - Add entrance animations
   - Define hover/focus interactions
   - Consider page transitions
   - Respect user preferences

5. **Production Harden**
   - Type everything
   - Handle edge cases
   - Optimize performance
   - Test accessibility

## Anti-Patterns to Avoid

- Using Inter/Roboto as the default font
- Using the same fonts across different projects (especially Space Grotesk, Inter)
- Creating designs that look like siblings of previous AI-generated work
- Gray-on-white with blue buttons
- Everything centered and symmetric
- No animations or generic fades
- Ignoring dark mode
- Forgetting loading/error states
- Skipping accessibility considerations
- Using arbitrary Tailwind values without design tokens

## Recommended Tools

- **Fonts**: Google Fonts, Fontshare, uncut.wtf
- **Colors**: Realtime Colors, Happy Hues, Radix Colors
- **Icons**: Lucide, Phosphor, Tabler Icons
- **Animation**: Framer Motion, React Spring
- **Components**: shadcn/ui (as base), Radix Primitives
- **CSS**: Tailwind CSS with CSS variables

## Quick Reference

```bash
# Distinctive font stacks (copy-paste ready)
# VARY THESE - never use the same fonts across projects!
font-display: 'Clash Display', 'Cabinet Grotesk', 'Satoshi', 'General Sans', 'Syne', 'Archivo'
font-body: 'Outfit', 'Plus Jakarta Sans', 'Switzer', 'Geist'
font-mono: 'JetBrains Mono', 'Geist Mono', 'IBM Plex Mono'

# Tailwind config pattern
theme: {
  extend: {
    colors: { /* HSL tokens */ },
    fontFamily: { /* Variable fonts */ },
    animation: { /* Spring-based */ },
  }
}
```

## Integration with Design Specialist Agent

This skill complements the design-specialist agent by providing specific, opinionated guidance for avoiding generic AI aesthetics. Use this skill when you need:
- Distinctive visual identity
- Creative typography and color choices
- Bold spatial compositions
- Production-ready animated components

Use the design-specialist agent for:
- Comprehensive UI/UX reviews
- Accessibility audits
- Design system architecture
- Component library setup
