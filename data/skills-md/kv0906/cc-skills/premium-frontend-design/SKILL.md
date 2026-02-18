---
name: premium-frontend-design
description: Create award-winning, cinematic frontend interfaces that feel ALIVE. Combines 10+ years of creative frontend experience with technical excellence. Specializes in WebGL, custom shaders, premium animations, and distinctive aesthetics that would win on Awwwards. Use when building landing pages, dashboards, platforms, or any interface where "generic AI slop" is unacceptable.
license: MIT
---

# Premium Frontend Design Skill

This skill guides creation of **production-grade frontend interfaces that feel ALIVE** — not generic, not copy-paste, but genuinely crafted experiences that users remember.

> "The difference between a good interface and an unforgettable one is intentionality in every pixel."

---

## Dependencies (Flexible — Choose What Fits)

This skill is **framework-flexible**. Pick packages based on user preference and project needs.

### Core 3D (for WebGL templates)
```bash
pnpm add three @react-three/fiber @react-three/drei
```

### Animation (choose based on user preference)

| Library | Best For | Complexity | Bundle Size |
|---------|----------|------------|-------------|
| **CSS/Tailwind** | Simple transitions, micro-interactions | Low | 0KB |
| **Framer Motion** | React-native feel, layout animations, gestures | Medium | ~30KB |
| **GSAP** | Complex timelines, scroll-triggered, text effects | High | ~60KB |
| **GSAP + Club** | SplitText, ScrollTrigger, MorphSVG | High | ~80KB |

```bash
# Framer Motion (simpler, React-idiomatic)
pnpm add framer-motion

# GSAP (powerful, timeline-based)
pnpm add gsap @gsap/react
# Note: SplitText, ScrollTrigger require GSAP Club license
```

**Decision Guide:**
- User says "simple" or "lightweight" → CSS + Framer Motion
- User says "complex animations" or "scroll effects" → GSAP
- User says "text animations" or "split text" → GSAP + SplitText
- User doesn't specify → Default to Framer Motion (simpler API)

### Optional Enhancements
```bash
# Mesh gradients (for mesh-gradient-hero)
pnpm add @paper-design/shaders-react

# Icons
pnpm add lucide-react

# Charts/Sparklines (for dashboards)
pnpm add recharts
# or lightweight: pnpm add @visx/shape @visx/scale
```

### Browser Compatibility Notes
- `backdrop-filter`: Not supported in Firefox < 103 (add fallback bg)
- WebGL: Provide CSS fallback for older devices
- `@starting-style`: Chrome 117+, Safari 17.4+ (progressive enhancement)

---

## Core Philosophy

### The "Alive" Principle

An interface feels alive when:
- **It breathes**: Subtle ambient animations, particles, or shader effects create constant but non-distracting motion
- **It responds**: Micro-interactions acknowledge every user action with satisfying feedback
- **It has depth**: Layers, parallax, glassmorphism, and shadows create dimensional space
- **It surprises**: At least one element breaks expectations in a delightful way

### Design Thinking (Before ANY Code)

Before writing a single line, answer these:

1. **Purpose**: What problem does this solve? Who uses it?
2. **Tone**: Pick ONE extreme direction (not a blend):
   - Brutally minimal
   - Maximalist chaos
   - Retro-futuristic / Cyberpunk
   - Organic / Natural
   - Luxury / Refined
   - Playful / Toy-like
   - Editorial / Magazine
   - Brutalist / Raw
   - Art Deco / Geometric
   - Industrial / Utilitarian
   - Bio-luminescent / Sci-fi
   - Mission Control / Technical

3. **The One Thing**: What single element will someone remember? Every great interface has a signature moment.

4. **Constraints**: Framework, performance budgets, accessibility requirements.

**CRITICAL**: Bold maximalism and refined minimalism both work. The key is **intentionality, not intensity**. A single, perfectly-executed animation beats 50 mediocre ones.

---

## Wow + Clarity Framework

Use this whenever the brief is vague or when you need to justify design decisions. The goal is **wow factor with purpose**.

### 1. Hierarchy Guardrails

- **1 hero flourish** (shader, particle system, or globe). Everything else supports readability.
- **1 supporting flourish** (micro-interactions, animated stat card, or glowing CTA). No more.
- Layout rule: `Hero (wild) → Content blocks (calm) → Proof (calm) → CTA (highlighted)`.
- If the page has more than one scroll-length of copy, every second section should be mostly static.

### 2. Typography Discipline

- **Max 2 headliner fonts** (display + body). Monospace only for data.
- Headline letter-spacing ≥ -0.04em. Anything tighter kills readability.
- Body width target: 55–75 characters per line on desktop, 35–45 on mobile.
- Always pair big display text with a plain supporting sentence under 80 characters.

### 3. Color & Contrast Rules

- Limit neon usage to **primary CTA + 1 accent**. Everything else stays in zinc/neutral palette.
- If background is busy (shader, gradients, particles), add a `bg-black/70` or `bg-slate-950/70` scrim behind text.
- Keep contrast ratios ≥ 4.5:1 for body copy even if the aesthetic is cyberpunk.
- Add a grayscale preview check before shipping: if it looks muddy, dial the palette back.

### 4. Motion Throttle

- **Default**: CSS or Framer Motion with durations ≤ 400ms, easing `cubic-bezier(0.34, 1.56, 0.64, 1)`.
- **Escalate to GSAP/WebGL** only if the brief explicitly asks for cinematic or interactive experiences.
- Max 1 continuous animation per viewport (e.g., shader OR wave bars, not both).
- Provide a “calm mode”: disable non-essential motion when `prefers-reduced-motion` is on OR when user scrolls past hero.

### 5. When Requirements Are Vague

| Situation | Default | Optional Upgrade |
|-----------|---------|------------------|
| User only says “clean SaaS” | `mesh-gradient-hero` + `bento-grid` | Swap hero background for CPPN if they later ask for “more energy” |
| User says “dashboard” with no flair | `bento-grid` + `dashboard-widgets` + CSS glow pills | Add `digital-liquid` shader only after data viz is signed off |
| User says “hero section” but nothing else | Text-first layout + CSS gradient | Offer shader/globe as a suggestion, never as default |

If the prompt does not explicitly mention WebGL, assume **CSS-first** and opt-in to shaders only when the user embraces the cost.

---

## Anti-Patterns (NEVER Do This)

### Visual Anti-Patterns
❌ White/light backgrounds as default (dark mode is premium)
❌ Generic gradients (purple-to-blue on white is AI slop)
❌ Evenly-distributed, timid color palettes
❌ Static, lifeless backgrounds
❌ Cookie-cutter component layouts
❌ Missing loading/transition states
❌ Jarring, un-eased animations

### Typography Anti-Patterns
❌ Inter, Roboto, Arial, system fonts for headlines
❌ Same font for everything
❌ Default line-heights and letter-spacing
❌ Boring, predictable type scales

### Code Anti-Patterns
❌ Inline styles scattered randomly
❌ No CSS variables for theming
❌ Animations without `will-change` or GPU acceleration
❌ Canvas/WebGL without `requestAnimationFrame`
❌ Missing cleanup in `useEffect`

---

## Design System

### 1. Color Architecture

**Rule: ONE dominant accent, everything else supports it.**

```typescript
// Premium Dark Theme (Default)
const colors = {
  // Backgrounds (layer from darkest to lightest)
  bg: {
    void: '#000000',      // True black for maximum contrast
    primary: '#050505',   // Main background
    elevated: '#0a0a0a',  // Cards, modals
    subtle: '#111111',    // Hover states
  },
  
  // Glass surfaces
  glass: {
    bg: 'rgba(255, 255, 255, 0.03)',
    border: 'rgba(255, 255, 255, 0.08)',
    hover: 'rgba(255, 255, 255, 0.06)',
  },
  
  // Text hierarchy
  text: {
    primary: '#ffffff',
    secondary: '#a1a1aa',   // zinc-400
    muted: '#71717a',       // zinc-500
    ghost: '#3f3f46',       // zinc-700
  },
  
  // Accent (choose ONE per project)
  accent: '#ff4d00',  // Neon Orange
  // accent: '#00f3ff',  // Neon Cyan
  // accent: '#ccff00',  // Neon Lime
  // accent: '#F5E445',  // Premium Yellow
  // accent: '#a855f7',  // Electric Purple
}
```

**Accent Usage Rules**:
- Primary actions: Full accent color
- Secondary elements: Accent at 20% opacity
- Borders/lines: Accent at 30% opacity
- Glows: Accent with blur, 40-60% opacity
- Never use accent for large background areas

### 2. Typography System

**Rule: Display font for impact, Body font for reading, Mono for data.**

```css
/* Tier 1: Display/Headlines - BOLD, characterful */
--font-display: 'Chakra Petch', 'Orbitron', 'Bebas Neue', 'Playfair Display';

/* Tier 2: Headings - Geometric, modern */
--font-heading: 'Manrope', 'Outfit', 'Syne', 'Space Grotesk';

/* Tier 3: Body - Clean, highly legible */
--font-body: 'Plus Jakarta Sans', 'DM Sans', 'Satoshi', 'General Sans';

/* Tier 4: Data/Code - ALWAYS monospace */
--font-mono: 'JetBrains Mono', 'Fira Code', 'IBM Plex Mono';
```

**Typography Patterns**:

```css
/* Hero Headlines: Massive, tight, aggressive */
.headline {
  font-family: var(--font-display);
  font-size: clamp(3rem, 12vw, 10rem);
  font-weight: 800;
  line-height: 0.9;
  letter-spacing: -0.03em;
  text-transform: uppercase;
}

/* Section Titles */
.section-title {
  font-family: var(--font-heading);
  font-size: clamp(1.5rem, 4vw, 3rem);
  font-weight: 700;
  letter-spacing: -0.02em;
}

/* Technical Labels */
.label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
}

/* Data Display */
.data {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}
```

### 3. Spacing & Layout

**Rule: Asymmetry creates interest. Grids are starting points, not prisons.**

```css
/* Spacing scale (use consistently) */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-24: 6rem;     /* 96px */
--space-32: 8rem;     /* 128px */

/* Use generous padding on containers */
.container {
  padding-inline: clamp(1rem, 5vw, 4rem);
}

/* Hero sections need breathing room */
.hero {
  min-height: 100vh;
  padding-block: var(--space-32);
}
```

**Bento Grid Pattern** (for dashboards):
```css
.bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(150px, auto);
  gap: var(--space-4);
}

/* Feature card spans */
.card-hero { grid-column: span 2; grid-row: span 2; }
.card-wide { grid-column: span 2; }
.card-tall { grid-row: span 2; }
```

---

## Visual Effects Library

### 1. Glassmorphism (The Right Way)

```css
.glass {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
}

/* Elevated glass (for modals, dropdowns) */
.glass-elevated {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}
```

### 2. CRT Scanlines Overlay

```css
.scanlines::before {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.1) 0px,
    rgba(0, 0, 0, 0.1) 1px,
    transparent 1px,
    transparent 2px
  );
  pointer-events: none;
  z-index: 9999;
}
```

### 3. Film Grain Texture

```css
.grain::before {
  content: '';
  position: fixed;
  inset: 0;
  opacity: 0.03;
  pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}
```

### 4. Tech Grid Background

```css
.tech-grid {
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 60px 60px;
}
```

### 5. Neon Glow Effects

```css
/* Text glow */
.neon-text {
  text-shadow: 
    0 0 10px currentColor,
    0 0 20px currentColor,
    0 0 40px currentColor,
    0 0 80px currentColor;
}

/* Box glow */
.neon-box {
  box-shadow: 
    0 0 20px var(--accent-alpha-40),
    0 0 40px var(--accent-alpha-20),
    inset 0 0 20px var(--accent-alpha-10);
}

/* Border glow */
.neon-border {
  border: 1px solid var(--accent);
  box-shadow: 
    0 0 10px var(--accent-alpha-50),
    inset 0 0 10px var(--accent-alpha-20);
}
```

---

## Animation Patterns

### Philosophy
- **Entrance animations**: Use once, make them count
- **Micro-interactions**: Subtle, fast (150-300ms)
- **Ambient motion**: Infinite, very slow, non-distracting
- **Page transitions**: Smooth, coordinated

### Choosing the Right Tool

| Need | Use | Why |
|------|-----|-----|
| Hover/focus states | CSS | Zero JS, instant |
| Simple entrance | CSS keyframes | Lightweight |
| Layout animations | Framer Motion | `layout` prop magic |
| Gesture-based | Framer Motion | Built-in drag/pan |
| Scroll-triggered | GSAP ScrollTrigger | Most powerful |
| Text splitting | GSAP SplitText | Industry standard |
| Complex timelines | GSAP | Precise control |
| SVG morphing | GSAP MorphSVG | No alternative |

**Default to simpler solutions. Escalate complexity only when needed.**

### CSS Keyframes Library

```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scale-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes slide-in-right {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse-glow {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes rotate-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes scan-line {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}
```

### Staggered Entrance Pattern

```css
.stagger-container > * {
  opacity: 0;
  animation: fade-up 0.6s ease-out forwards;
}

.stagger-container > *:nth-child(1) { animation-delay: 0.1s; }
.stagger-container > *:nth-child(2) { animation-delay: 0.2s; }
.stagger-container > *:nth-child(3) { animation-delay: 0.3s; }
.stagger-container > *:nth-child(4) { animation-delay: 0.4s; }
.stagger-container > *:nth-child(5) { animation-delay: 0.5s; }
```

### CSS-Only Patterns (Zero Dependencies)

```css
/* View transition entrance (Chrome 111+, Safari 18+) */
@supports (view-transition-name: none) {
  .card {
    view-transition-name: card;
  }
  
  ::view-transition-old(card),
  ::view-transition-new(card) {
    animation-duration: 0.3s;
  }
}

/* Scroll-driven animations (Chrome 115+) */
@supports (animation-timeline: scroll()) {
  .parallax-bg {
    animation: parallax linear;
    animation-timeline: scroll();
  }
  
  @keyframes parallax {
    from { transform: translateY(0); }
    to { transform: translateY(-30%); }
  }
}

/* Hover with spring-like feel */
.spring-hover {
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.spring-hover:hover {
  transform: scale(1.05);
}

/* Glow pulse */
.glow-pulse {
  animation: glow-pulse 2s ease-in-out infinite;
}
@keyframes glow-pulse {
  0%, 100% { box-shadow: 0 0 20px var(--accent-alpha-40); }
  50% { box-shadow: 0 0 40px var(--accent-alpha-60); }
}
```

### GSAP Patterns (When You Need Power)

```typescript
// Stagger entrance on scroll
gsap.from('.card', {
  scrollTrigger: {
    trigger: '.cards-section',
    start: 'top 80%',
  },
  y: 60,
  opacity: 0,
  duration: 0.8,
  stagger: 0.1,
  ease: 'power3.out',
});

// Text scramble effect
const scrambleText = (el: HTMLElement, text: string) => {
  const chars = '!<>-_\\/[]{}—=+*^?#';
  let iteration = 0;
  
  const interval = setInterval(() => {
    el.innerText = text
      .split('')
      .map((char, i) => 
        i < iteration ? char : chars[Math.floor(Math.random() * chars.length)]
      )
      .join('');
    
    if (iteration >= text.length) clearInterval(interval);
    iteration += 1/3;
  }, 30);
};

// Smooth parallax
gsap.to('.parallax-bg', {
  scrollTrigger: {
    scrub: 1,
  },
  y: '-30%',
  ease: 'none',
});
```

### Framer Motion Patterns

```tsx
// Page transitions
<AnimatePresence mode="wait">
  <motion.div
    key={page}
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -20 }}
    transition={{ duration: 0.3 }}
  />
</AnimatePresence>

// Hover glow effect
<motion.div
  whileHover={{ 
    scale: 1.02,
    boxShadow: '0 0 30px rgba(255, 77, 0, 0.4)',
  }}
  transition={{ type: 'spring', stiffness: 300 }}
/>

// Stagger children
<motion.div
  initial="hidden"
  animate="visible"
  variants={{
    hidden: {},
    visible: { transition: { staggerChildren: 0.1 } },
  }}
>
  {items.map(item => (
    <motion.div
      key={item.id}
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 },
      }}
    />
  ))}
</motion.div>
```

---

## 3D & WebGL Patterns

### Tech Stack
```bash
npm install three @react-three/fiber @react-three/drei
```

### Basic Scene Setup

```tsx
import { Canvas } from '@react-three/fiber';
import { Stars, Float, MeshDistortMaterial } from '@react-three/drei';

const Scene = () => (
  <Canvas
    camera={{ position: [0, 0, 5], fov: 75 }}
    style={{ position: 'fixed', inset: 0, zIndex: -1 }}
  >
    <ambientLight intensity={0.2} />
    <pointLight position={[10, 10, 10]} color="#ff4d00" />
    <Stars radius={100} depth={50} count={3000} />
    {/* Your 3D content */}
  </Canvas>
);
```

### Particle Sphere (Data Globe)

```tsx
const ParticleSphere = ({ count = 3000, color = '#ff4d00' }) => {
  const ref = useRef<THREE.Points>(null);
  
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);
      const r = 2;
      pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      pos[i * 3 + 2] = r * Math.cos(phi);
    }
    return pos;
  }, [count]);
  
  useFrame(() => {
    if (ref.current) ref.current.rotation.y += 0.001;
  });
  
  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.02} color={color} transparent opacity={0.8} />
    </points>
  );
};
```

### Sentient Core (AI Brain)

```tsx
const SentientCore = () => (
  <Float speed={2} rotationIntensity={0.5}>
    <mesh>
      <sphereGeometry args={[1.5, 64, 64]} />
      <MeshDistortMaterial
        color="#00f3ff"
        wireframe
        distort={0.4}
        speed={2}
      />
    </mesh>
  </Float>
);
```

### Performance Rules
1. Always use `requestAnimationFrame` via `useFrame`
2. Reduce particle counts on mobile (check `window.innerWidth`)
3. Use `useMemo` for geometry/position calculations
4. Cleanup animations in `useEffect` return
5. Set `transparent` and `opacity` for depth sorting

---

## Component Patterns

### 1. Loading + Page Transitions

**Default (ship this unless user asks otherwise):**
- Skeleton placeholders on cards/sections (see shimmer pattern above)
- Simple fade/slide page transition using CSS or Framer Motion route transitions

**Optional Cinematic Mode (only when the user wants a narrative boot sequence and there's time/budget):**
- GSAP-powered preloader with boot logs, text scramble, shader/WebGL background
- Coordinated timeline that fades into actual content once data is ready

### 2. Glassmorphic Navbar

```tsx
<nav className="fixed top-4 left-1/2 -translate-x-1/2 z-50">
  <div className="glass rounded-full px-6 py-3 flex items-center gap-8">
    <Logo />
    <NavLinks />
    <ThemeToggle />
    <CTA />
  </div>
</nav>
```

### 3. Live Terminal

```tsx
const Terminal = ({ logs }) => {
  const scrollRef = useRef();
  
  useEffect(() => {
    scrollRef.current?.scrollTo(0, scrollRef.current.scrollHeight);
  }, [logs]);
  
  return (
    <div className="glass font-mono text-xs">
      <header className="border-b border-white/10 px-4 py-2">
        <span className="text-accent">&gt;</span> System Logs
        <span className="ml-auto w-2 h-2 bg-green-500 rounded-full animate-pulse" />
      </header>
      <div ref={scrollRef} className="h-64 overflow-y-auto p-4">
        {logs.map(log => (
          <div key={log.id}>
            <span className="text-zinc-600">{log.time}</span>
            <span className={levelColor[log.level]}>[{log.level}]</span>
            <span>{log.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 4. Stat Cards with Sparklines

```tsx
const StatCard = ({ icon, label, value, change, trend }) => (
  <motion.div
    whileHover={{ scale: 1.02, boxShadow: '0 0 30px var(--accent-alpha-30)' }}
    className="glass p-4"
  >
    <div className="flex justify-between">
      <div className="p-2 rounded-lg bg-accent/10 text-accent">{icon}</div>
      <span className={change > 0 ? 'text-green-400' : 'text-red-400'}>
        {change > 0 ? '+' : ''}{change}%
      </span>
    </div>
    <div className="mt-4 font-mono text-2xl font-bold">{value}</div>
    <div className="text-xs text-zinc-500 uppercase">{label}</div>
    <Sparkline data={trend} className="mt-2 h-8" />
  </motion.div>
);
```

---

## Quality Checklist

Before shipping, verify:

### Visual
- [ ] Dark mode is default and premium-feeling
- [ ] ONE dominant accent color used consistently
- [ ] Glass effects have proper blur AND borders
- [ ] Scanlines or grain overlay for texture
- [ ] No pure white text on dark (#f4f4f5 max)

### Typography
- [ ] Display font for headlines (not Inter/Roboto)
- [ ] Monospace for ALL data/code/numbers
- [ ] Proper hierarchy (3-4 distinct levels)
- [ ] Tracking adjusted for large text

### Animation
- [ ] Entrance animations on load (staggered)
- [ ] Hover states with transform AND glow
- [ ] Smooth 60fps for all canvas
- [ ] No animation without purpose

### Code
- [ ] CSS variables for all colors
- [ ] Responsive (mobile-first)
- [ ] Cleanup functions in useEffect
- [ ] Error boundaries for 3D content

---

## Accessibility (Premium ≠ Inaccessible)

Great design is inclusive. These aren't optional.

### Motion Sensitivity

```css
/* ALWAYS respect user preferences */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```tsx
// React hook for motion preference
const usePrefersReducedMotion = () => {
  const [prefersReduced, setPrefersReduced] = useState(false);
  
  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReduced(mq.matches);
    const handler = (e: MediaQueryListEvent) => setPrefersReduced(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);
  
  return prefersReduced;
};

// Usage
const shouldAnimate = !usePrefersReducedMotion();
```

### WebGL Accessibility

```tsx
// Always mark decorative 3D as hidden
<div aria-hidden="true" className="pointer-events-none">
  <Canvas>{/* decorative background */}</Canvas>
</div>

// Provide text alternatives for meaningful 3D
<div role="img" aria-label="3D visualization of global network connections">
  <Canvas>{/* data visualization */}</Canvas>
</div>
```

### Color Contrast

| Element | Minimum Ratio | Target |
|---------|---------------|--------|
| Body text | 4.5:1 | 7:1 |
| Large text (18px+) | 3:1 | 4.5:1 |
| UI components | 3:1 | 4.5:1 |
| Decorative | N/A | N/A |

```css
/* Safe text colors on dark backgrounds */
--text-primary: #ffffff;     /* ✓ 21:1 on #000 */
--text-secondary: #a1a1aa;   /* ✓ 7.2:1 on #000 */
--text-muted: #71717a;       /* ✓ 4.6:1 on #000 */
--text-ghost: #52525b;       /* ⚠ 3.2:1 - decorative only */
```

### Keyboard Navigation

```tsx
// Interactive 3D elements need keyboard support
<mesh
  tabIndex={0}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
  onClick={handleClick}
/>

// Focus indicators for glass components
.glass:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

---

## Mobile & Responsive Strategy

Premium experiences adapt gracefully. Don't just shrink — reimagine.

### WebGL Fallbacks

```tsx
// Detect low-power devices
const useIsLowPowerDevice = () => {
  const [isLowPower, setIsLowPower] = useState(false);
  
  useEffect(() => {
    const isLow = 
      window.innerWidth < 768 ||
      navigator.hardwareConcurrency <= 4 ||
      /Android|iPhone|iPad/.test(navigator.userAgent);
    setIsLowPower(isLow);
  }, []);
  
  return isLowPower;
};

// Usage in hero components
const HeroBackground = () => {
  const isLowPower = useIsLowPowerDevice();
  
  if (isLowPower) {
    return <CSSGradientFallback />; // Lighter alternative
  }
  
  return <WebGLBackground />;
};
```

### Performance Budgets

| Device | JS Budget | Animation Target |
|--------|-----------|------------------|
| Desktop | < 500KB | 60fps WebGL |
| Tablet | < 300KB | 30fps or CSS-only |
| Mobile | < 150KB | CSS-only, no WebGL |

### Touch Interactions

```tsx
// Replace hover with tap/long-press on mobile
<motion.div
  whileHover={{ scale: 1.02 }}  // Desktop
  whileTap={{ scale: 0.98 }}    // Mobile
  onTouchStart={handleTouch}
/>

// Increase touch targets
.button {
  min-height: 44px;  /* Apple HIG */
  min-width: 44px;
  padding: 12px 24px;
}
```

### Responsive Typography

```css
/* Fluid type scale */
--text-hero: clamp(2.5rem, 8vw, 7rem);
--text-h1: clamp(2rem, 5vw, 4rem);
--text-h2: clamp(1.5rem, 3vw, 2.5rem);
--text-body: clamp(1rem, 2vw, 1.125rem);

/* Reduce letter-spacing on mobile */
@media (max-width: 768px) {
  .headline {
    letter-spacing: -0.02em; /* Less aggressive than desktop */
  }
}
```

---

## Loading & Error States

Premium UX handles every state beautifully.

### Skeleton Loaders

```tsx
// Glass skeleton with shimmer
const Skeleton = ({ className }: { className?: string }) => (
  <div 
    className={`relative overflow-hidden rounded-lg bg-white/5 ${className}`}
  >
    <div 
      className="absolute inset-0 -translate-x-full animate-[shimmer_2s_infinite] bg-gradient-to-r from-transparent via-white/10 to-transparent"
    />
  </div>
);

// Usage
<div className="space-y-4">
  <Skeleton className="h-8 w-3/4" />
  <Skeleton className="h-4 w-full" />
  <Skeleton className="h-4 w-5/6" />
</div>
```

```css
@keyframes shimmer {
  100% { transform: translateX(100%); }
}
```

### Error Boundaries (Styled)

```tsx
const ErrorFallback = ({ error, resetErrorBoundary }) => (
  <div className="glass p-8 text-center">
    <div className="mx-auto mb-4 h-16 w-16 rounded-full bg-red-500/10 flex items-center justify-center">
      <AlertTriangle className="h-8 w-8 text-red-400" />
    </div>
    <h2 className="text-xl font-semibold text-white mb-2">
      Something went wrong
    </h2>
    <p className="text-zinc-400 mb-4 font-mono text-sm">
      {error.message}
    </p>
    <button 
      onClick={resetErrorBoundary}
      className="px-4 py-2 bg-white/10 rounded-lg hover:bg-white/20 transition"
    >
      Try again
    </button>
  </div>
);
```

### Empty States

```tsx
const EmptyState = ({ 
  icon: Icon, 
  title, 
  description, 
  action 
}: EmptyStateProps) => (
  <div className="flex flex-col items-center justify-center py-16 text-center">
    <div className="mb-4 rounded-full bg-white/5 p-4">
      <Icon className="h-8 w-8 text-zinc-500" />
    </div>
    <h3 className="text-lg font-medium text-white mb-1">{title}</h3>
    <p className="text-zinc-400 mb-4 max-w-sm">{description}</p>
    {action}
  </div>
);

// Usage
<EmptyState
  icon={Inbox}
  title="No messages yet"
  description="When you receive messages, they'll appear here."
  action={<Button>Send your first message</Button>}
/>
```

### Loading States for Data

```tsx
// Optimistic UI with rollback
const [items, setItems] = useState(data);
const [pending, startTransition] = useTransition();

const addItem = (newItem) => {
  // Optimistic update
  setItems(prev => [...prev, { ...newItem, pending: true }]);
  
  startTransition(async () => {
    try {
      await api.createItem(newItem);
    } catch {
      // Rollback on error
      setItems(prev => prev.filter(i => i.id !== newItem.id));
      toast.error('Failed to add item');
    }
  });
};
```

---

## Framework Integration

### Next.js App Router

```tsx
// Client boundary for WebGL components
// app/components/hero-client.tsx
'use client';

import dynamic from 'next/dynamic';

// Lazy load heavy 3D components
const WebGLHero = dynamic(() => import('./webgl-hero'), {
  ssr: false,
  loading: () => <HeroSkeleton />,
});

export default function HeroClient() {
  return <WebGLHero />;
}
```

```tsx
// Server component wrapper
// app/page.tsx
import HeroClient from './components/hero-client';

export default function Page() {
  return (
    <main>
      {/* Server-rendered SEO content */}
      <h1 className="sr-only">Your SEO Title</h1>
      
      {/* Client-side 3D hero */}
      <HeroClient />
    </main>
  );
}
```

### SEO for WebGL Content

```tsx
// WebGL isn't crawlable - always provide text alternatives
<section aria-labelledby="hero-title">
  {/* Hidden but crawlable */}
  <h1 id="hero-title" className="sr-only">
    AI-Powered Trading Platform
  </h1>
  <p className="sr-only">
    {seoDescription}
  </p>
  
  {/* Visual hero (not crawled) */}
  <div aria-hidden="true">
    <Canvas>...</Canvas>
  </div>
  
  {/* Visible text (crawled) */}
  <div className="relative z-10">
    <span className="text-7xl">{visibleTitle}</span>
  </div>
</section>
```

### Data Fetching with Loading States

```tsx
// Server Component with Suspense
import { Suspense } from 'react';

async function DashboardData() {
  const data = await fetchDashboardData();
  return <DashboardWidgets data={data} />;
}

export default function Dashboard() {
  return (
    <div className="bento-grid">
      <Suspense fallback={<WidgetSkeleton />}>
        <DashboardData />
      </Suspense>
    </div>
  );
}
```

---

## Template Quick Reference

| Template | Props | WebGL | Mobile Fallback | Best Animation Lib |
|----------|-------|-------|-----------------|-------------------|
| `cppn-hero` | `title`, `description`, `ctaButtons`, `microDetails` | Yes | CSS gradient | GSAP (SplitText) |
| `mesh-gradient-hero` | `colors[]`, `speed`, `distortion`, `swirl` | No* | Native | Framer Motion |
| `wave-hero` | `title`, `subtitle`, `placeholder`, `onPromptSubmit` | Yes | Solid bg | GSAP |
| `globe-hero` | `globeImage`, `dashboardImage`, `accentColor` | No | Native | Framer Motion |
| `hero-section` | `title`, `badge`, `primaryCTA`, `accentColor` | Yes | Stars CSS | Either |
| `bento-grid` | `children` (card layout) | No | Native | CSS or Framer |
| `dashboard-widgets` | `value`, `change`, `trend[]` | No | Native | Framer Motion |
| `terminal` | `logs[]`, `title` | No | Native | CSS |
| `preloader` | `onComplete`, `messages[]` | Optional | CSS version | GSAP |
| `glass-components` | Various | No | Native | CSS |

*`mesh-gradient-hero` uses `@paper-design/shaders-react` (Canvas, not WebGL)

---

## Template Playbooks (Start Grounded, Layer Wow Intentionally)

| Goal | Baseline (Clarity-first) | Optional Wow Upgrade | Kill It If |
|------|--------------------------|----------------------|------------|
| Marketing / Waitlist | `mesh-gradient-hero` + `glass-components` + `bento-grid` value props | Swap hero for `cppn-hero` or add `wave-hero` band for social proof | Copy is long-form or the product is compliance-heavy |
| AI / Research Landing | `cppn-hero` + `dashboard-widgets` (metrics) + `terminal` logs | Add `holographic` shader sections or `globe-hero` interlude | User needs print-friendly deliverables |
| Crypto / Finance | `globe-hero` + `bento-grid` KPIs + `dashboard-widgets` + CTA strip | Add `data-grid` shader background or rolling ticker | Performance budget < 200KB or mobile-only |
| Developer Tools | `wave-hero` + `terminal` + `glass-components` cards | Introduce `digital-liquid` shader or 3D device mock | Audience is enterprise buyers needing conservative tone |
| Product Dashboard | `bento-grid` + `dashboard-widgets` + `mesh-gradient-hero` (static) | Add mini WebGL module (sentient core, particle globe) | Data is dense, requires tabular clarity |

### Layout Flow Recipes

1. **Hero (signature flourish)** → Key metrics/value props (calm) → Product proof (screens) → Testimonials/logos → CTA (glow button).
2. **Dashboard page**: Above-the-fold summary (minimal) → Feature grid (asymmetrical) → Live data (terminal/sparkline) → Help/resources (calm).
3. **Docs/Platform**: Clean header (`mesh-gradient-hero` in CSS mode) → Navigation grid → Content area (monospace) → CTA.

Each flow should have at most **two high-saturation panels**. If you need more energy, animate the CTA or accent borders instead of adding another shader.

---

## Template Remix & Adaptation Patterns

| Need | Action | Notes |
|------|--------|-------|
| **Downgrade WebGL → CSS** | Replace `cppn-hero` with `mesh-gradient-hero`, keep same copy. Swap shader backgrounds for `bg-gradient-to-b`. | Use when user mentions “mobile-first,” “performance,” or “lightweight.” |
| **Upgrade CSS → WebGL** | Start from `mesh-gradient-hero`, then inject `ShaderBackground` and reuse props from `cppn-hero`. | Only after confirming the client wants “cinematic” or “experimental.” |
| **Shader swap** | Any hero using shaders can switch to another by swapping imports (e.g., `holographic` ↔ `digital-liquid`). Keep uniform names consistent. | Document the new accent palette alongside the swap. |
| **Content density mode** | When the design needs to carry lots of text, keep hero flourish but make every subsequent section `bg-black` with simple borders. | Example: `cppn-hero` on top, then `bento-grid` in plain glass cards. |
| **Prompt-to-template defaults** | - “Clean SaaS” → Mesh gradient package<br> - “AI platform” → CPPN hero + dashboard metrics<br> - “Crypto trading” → Globe hero + ticker<br> - “Developer CLI” → Wave hero + terminal | Mention these defaults directly in responses so the model doesn’t hallucinate new structures. |

When in doubt: **start with the baseline, ship usable layout, then pitch a single wow upgrade** as a follow-up suggestion (“Optionally we can swap in the CPPN shader if you want a more neural vibe.”).

---

## Template & Shader Selection Guide

Use this guide to pick the right template and shader based on the user's request. **Don't default to the same hero for everything** — match the aesthetic to the domain.

### Industry/Vertical Mapping

| Industry | Hero Template | Shader | Accent Color | Tone |
|----------|--------------|--------|--------------|------|
| **AI/ML/Neural** | `cppn-hero` | `cppn-generative` | Cyan `#00f3ff` / Purple `#a855f7` | Organic, alive, mathematical |
| **Crypto/DeFi/Trading** | `globe-hero` | `data-grid` | Purple `#9b87f5` / Amber `#f59e0b` | Global, technical, financial |
| **Developer Tools/API** | `wave-hero` | `digital-liquid` | Blue `#1f3dbc` / Orange `#ff4d00` | Technical, dynamic, builder |
| **SaaS/B2B/Product** | `mesh-gradient-hero` | *(CSS only)* | Soft pastels | Clean, professional, trustworthy |
| **Creative Agency** | `hero-section` (CyberpunkHero) | `holographic` | Neon colors | Bold, experimental, artistic |
| **Fintech/Dashboard** | `bento-grid` + `dashboard-widgets` | `data-grid` | Green `#10b981` / Blue `#3b82f6` | Data-rich, precise, analytical |

### Keyword-Based Selection

When analyzing user requests, match keywords to templates:

```
User Request Analysis:
├── Contains "AI", "neural", "intelligent", "learning", "model", "GPT"
│   → cppn-hero + cppn-generative shader
│   → Organic, flowing backgrounds that feel "alive"
│
├── Contains "crypto", "blockchain", "trading", "global", "DeFi", "web3"
│   → globe-hero + data-grid shader
│   → Earth imagery, global reach, financial precision
│
├── Contains "developer", "API", "code", "build", "deploy", "ship"
│   → wave-hero + digital-liquid shader
│   → Dynamic bars, typing animations, terminal aesthetic
│
├── Contains "SaaS", "product", "waitlist", "brand", "startup", "launch"
│   → mesh-gradient-hero (no WebGL needed)
│   → Soft, fluid gradients, professional feel
│
├── Contains "futuristic", "cyber", "agency", "creative", "portfolio"
│   → hero-section (CyberpunkHero) + holographic shader
│   → Particle spheres, text scramble, scanlines
│
└── Contains "dashboard", "analytics", "metrics", "data", "monitoring"
    → bento-grid + dashboard-widgets + terminal
    → Stat cards, sparklines, live data feeds
```

### Performance-Based Selection

Choose based on target audience and device constraints:

| Performance Tier | Templates | Best For |
|-----------------|-----------|----------|
| **High-end (WebGL)** | `cppn-hero`, `wave-hero`, `hero-section` | Desktop-first, portfolio sites, creative agencies |
| **Medium (Canvas/Images)** | `globe-hero` | Marketing sites, crypto landing pages |
| **Light (CSS only)** | `mesh-gradient-hero`, `bento-grid` | Mobile-first, SaaS, B2B, accessibility-focused |

### Shader Pairing Guide

| Shader | Aesthetic | Pairs Well With |
|--------|-----------|-----------------|
| `cppn-generative` | Neural, organic, mathematical | AI products, generative art, research tools |
| `data-grid` | Matrix, technical, cyberpunk | Crypto, fintech, developer tools |
| `digital-liquid` | Flowing, dynamic, fluid | Creative tools, media platforms |
| `holographic` | Sci-fi, iridescent, futuristic | Gaming, AR/VR, experimental projects |

### Quick Decision Flowchart

```
Is performance critical (mobile-first)?
├── YES → mesh-gradient-hero (CSS only)
└── NO → Continue...
    │
    Is it AI/ML related?
    ├── YES → cppn-hero
    └── NO → Continue...
        │
        Is it crypto/global/financial?
        ├── YES → globe-hero
        └── NO → Continue...
            │
            Is it developer-focused?
            ├── YES → wave-hero
            └── NO → hero-section (CyberpunkHero)
```

---

## File Structure

```
premium-frontend-skill/
├── SKILL.md                           # This document
├── examples/
│   ├── 01-racing-dashboard.tsx        # Motorsport telemetry
│   ├── 02-cyberpunk-platform.tsx      # Developer platform
│   ├── 03-bioluminescent-landing.tsx  # AI agency landing
│   ├── 04-fintech-protocol.tsx        # DeFi interface
│   └── 05-neural-interface.tsx        # Sentient AI core
├── templates/
│   ├── preloader.tsx                  # Boot sequence loader
│   ├── glass-components.tsx           # Glassmorphic UI elements
│   ├── terminal.tsx                   # Live logs display
│   ├── bento-grid.tsx                 # Dashboard layout system
│   ├── dashboard-widgets.tsx          # Stat cards, charts, metrics
│   ├── hero-section.tsx               # CyberpunkHero + StarfieldScene
│   ├── cppn-hero.tsx                  # Neural network shader hero
│   ├── mesh-gradient-hero.tsx         # Fluid gradient hero (CSS-light)
│   ├── wave-hero.tsx                  # Animated wave bars hero
│   └── globe-hero.tsx                 # 3D globe with dashboard
└── shaders/
    ├── cppn-generative.glsl.ts        # Neural pattern generator
    ├── digital-liquid.glsl.ts         # Flowing noise effect
    ├── data-grid.glsl.ts              # Matrix/grid effect
    └── holographic.glsl.ts            # Hologram interference
```

---

## Remember

> "The goal is to create interfaces that feel **alive**, **cinematic**, and **unforgettable**. Every pixel should be intentional. These aren't just websites—they're experiences."

Don't hold back. Show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
