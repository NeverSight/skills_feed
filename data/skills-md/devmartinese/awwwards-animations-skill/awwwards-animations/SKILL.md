---
name: awwwards-animations
description: Professional React animation skill for creating Awwwards/FWA-level animations using GSAP (useGSAP), Motion (Framer Motion), Anime.js, and Lenis. Use when building premium scroll experiences, custom cursors, page transitions, text animations, parallax effects, micro-interactions, or any animation that needs to be 60fps and award-worthy. Triggers on requests for smooth scroll, ScrollTrigger, magnetic effects, reveal animations, horizontal scroll, pin sections, stagger effects, useScroll, useTransform, integration with Three.js/WebGL, algorithmic art, mathematical art, generative art, fractals, L-systems, flow fields, strange attractors, sacred geometry, geometric puzzles, Dudeney dissections, tangram, tessellations, Penrose tiles, kinetic typography, glitch effects, text explosion, morphing text, circular text, brutalist design, minimalist animation, neo-brutalism, or design philosophy mixing. React-first approach with proper cleanup and hooks.
---

# Awwwards Animations

Create premium web animations at Awwwards/FWA quality level. **React-first approach**. 60fps non-negotiable.

## Decision Matrix

| Task | Library | Why |
|------|---------|-----|
| Scroll-driven animations | GSAP + ScrollTrigger + useGSAP | Industry standard, best control |
| Smooth scroll | Lenis + ReactLenis | Best performance, works with ScrollTrigger |
| React-native animations | Motion (Framer Motion) | Native React, useScroll/useTransform |
| Simple/lightweight effects | Anime.js 4.0 | Small footprint, clean API |
| Complex timelines | GSAP | Unmatched timeline control |
| SVG morphing | GSAP MorphSVG or Anime.js | Both excellent |
| 3D + animation | Three.js + GSAP | GSAP controls Three.js objects |
| Page transitions | AnimatePresence or GSAP | Motion for React, GSAP for complex |
| Geometric shapes (vector) | SVG + GSAP/Motion | Native, animable |
| Geometric shapes (canvas) | Canvas 2D API | Programmatic, performant |
| Pseudo-3D shapes | Zdog | Flat design 3D, ~2kb |
| Creative coding/generative | p5.js | Rich ecosystem |
| Audio reactive | Tone.js | Web Audio, synths, effects |
| Physics 2D | Matter.js | Gravity, collisions, constraints |
| Algorithmic/generative art | Canvas 2D + p5.js | Math-driven visuals |
| Fractals/L-systems | Canvas 2D recursivo | Recursive rendering |
| Tessellations/geometric puzzles | SVG + GSAP | Precise animated transforms |
| Kinetic typography advanced | GSAP SplitText + Canvas | Per-char control |
| Glitch effects | CSS + GSAP | Layered RGB split, clip-path |
| Brutalist animation | CSS raw + Motion | Hard cuts, no easing |
| Minimalist animation | Motion springs | Subtle, purposeful motion |

## Installation (Latest Stable - 2025)

```bash
# GSAP + React hook (v3.14.1)
npm install gsap @gsap/react

# Lenis (v1.3.17) - includes React components
npm install lenis

# Motion (Framer Motion)
npm install motion

# Anime.js (v4.0.0)
npm install animejs
```

## React Setup

### 1. GSAP Configuration (app-wide)

```tsx
// lib/gsap.ts
'use client' // Next.js App Router

import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { useGSAP } from '@gsap/react'

// Register plugins once
gsap.registerPlugin(ScrollTrigger, useGSAP)

export { gsap, ScrollTrigger, useGSAP }
```

### 2. Lenis + GSAP ScrollTrigger Integration (Critical)

```tsx
// components/SmoothScroll.tsx
'use client'
import { ReactLenis, useLenis } from 'lenis/react'
import { useEffect } from 'react'
import { gsap, ScrollTrigger } from '@/lib/gsap'

export function SmoothScroll({ children }: { children: React.ReactNode }) {
  const lenis = useLenis()
  useEffect(() => {
    if (!lenis) return
    lenis.on('scroll', ScrollTrigger.update)
    gsap.ticker.add((time) => lenis.raf(time * 1000))
    gsap.ticker.lagSmoothing(0)
    return () => { gsap.ticker.remove(lenis?.raf) }
  }, [lenis])

  return (
    <ReactLenis root options={{ lerp: 0.1, duration: 1.2, smoothWheel: true }}>
      {children}
    </ReactLenis>
  )
}
// Wrap in layout: <SmoothScroll>{children}</SmoothScroll>
```

## Core Patterns (React)

Detailed implementations in references:
- **GSAP + useGSAP**: See [references/gsap-react.md](references/gsap-react.md)
- **Motion (Framer Motion)**: See [references/motion-patterns.md](references/motion-patterns.md)
- **Anime.js 4.0**: See [references/animejs-react.md](references/animejs-react.md)
- **Lenis React**: See [references/lenis-react.md](references/lenis-react.md)
- **Geometric Shapes**: See [references/geometric-shapes.md](references/geometric-shapes.md) (SVG, Canvas, Zdog, p5.js, Tetris-style)
- **Audio Reactive**: See [references/audio-reactive.md](references/audio-reactive.md) (Tone.js, Web Audio, scroll audio)
- **Physics 2D**: See [references/physics-2d.md](references/physics-2d.md) (Matter.js, collisions, constraints)
- **Advanced (Three.js, WebGL)**: See [references/advanced-patterns.md](references/advanced-patterns.md)
- **Algorithmic & Generative Art**: See [references/algorithmic-art.md](references/algorithmic-art.md) (fractals, L-systems, flow fields, attractors, noise, sacred geometry)
- **Advanced Text Effects**: See [references/text-effects.md](references/text-effects.md) (glitch, kinetic typography, morphing, explosion, circular text, scramble)
- **Geometric Puzzles**: See [references/geometric-puzzles.md](references/geometric-puzzles.md) (Dudeney, tangram, tessellations, Penrose, polyominoes)
- **Design Philosophy**: See [references/design-philosophy.md](references/design-philosophy.md) (brutalist, minimalist, abstract, mixing styles, palettes)
- **Performance**: See [references/performance.md](references/performance.md)

## Quick Patterns (React)

### 1. Magnetic Cursor (GSAP + useGSAP)

```tsx
'use client'
import { useRef, useEffect } from 'react'
import { gsap, useGSAP } from '@/lib/gsap'

export function MagneticCursor() {
  const cursorRef = useRef<HTMLDivElement>(null)
  const pos = useRef({ x: 0, y: 0, cx: 0, cy: 0 })
  useEffect(() => {
    const h = (e: MouseEvent) => { pos.current.x = e.clientX; pos.current.y = e.clientY }
    window.addEventListener('mousemove', h)
    return () => window.removeEventListener('mousemove', h)
  }, [])
  useGSAP(() => {
    gsap.ticker.add(() => {
      const p = pos.current
      p.cx += (p.x - p.cx) * 0.15; p.cy += (p.y - p.cy) * 0.15
      gsap.set(cursorRef.current, { x: p.cx, y: p.cy })
    })
  })
  return <div ref={cursorRef} className="fixed w-10 h-10 border border-white rounded-full pointer-events-none mix-blend-difference z-[9999] -translate-x-1/2 -translate-y-1/2" />
}
```

### 2. Magnetic Button (Motion)

```tsx
'use client'
import { useRef, useState } from 'react'
import { motion } from 'motion/react'

export function MagneticButton({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLButtonElement>(null)
  const [pos, setPos] = useState({ x: 0, y: 0 })
  const onMove = (e: React.MouseEvent) => {
    const { left, top, width, height } = ref.current!.getBoundingClientRect()
    setPos({ x: (e.clientX - left - width / 2) * 0.3, y: (e.clientY - top - height / 2) * 0.3 })
  }
  return (
    <motion.button ref={ref} onMouseMove={onMove} onMouseLeave={() => setPos({ x: 0, y: 0 })}
      animate={pos} transition={{ type: 'spring', stiffness: 150, damping: 15 }}
      className="px-8 py-4 bg-white text-black rounded-full">{children}</motion.button>
  )
}
```

### 3. Parallax Hero (GSAP + useGSAP)

```tsx
'use client'
import { useRef } from 'react'
import { gsap, ScrollTrigger, useGSAP } from '@/lib/gsap'

export function ParallaxHero() {
  const containerRef = useRef<HTMLDivElement>(null)

  useGSAP(() => {
    gsap.to('.parallax-bg', {
      yPercent: 50,
      ease: 'none',
      scrollTrigger: {
        trigger: containerRef.current,
        start: 'top top',
        end: 'bottom top',
        scrub: true,
      },
    })

    gsap.to('.hero-title', {
      yPercent: 100,
      opacity: 0,
      scrollTrigger: {
        trigger: containerRef.current,
        start: 'top top',
        end: '50% top',
        scrub: true,
      },
    })
  }, { scope: containerRef })

  return (
    <div ref={containerRef} className="relative h-screen overflow-hidden">
      <div className="parallax-bg absolute inset-0 bg-cover bg-center" />
      <h1 className="hero-title absolute inset-0 flex items-center justify-center text-6xl">
        Hero Title
      </h1>
    </div>
  )
}
```

### 4. Text Character Reveal (Motion)

```tsx
'use client'
import { motion } from 'motion/react'

const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.02 },
  },
}

const child = {
  hidden: { opacity: 0, y: 50, rotateX: -90 },
  visible: {
    opacity: 1,
    y: 0,
    rotateX: 0,
    transition: { type: 'spring', damping: 12 },
  },
}

export function TextReveal({ text }: { text: string }) {
  return (
    <motion.span
      variants={container}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      className="inline-block"
    >
      {text.split('').map((char, i) => (
        <motion.span key={i} variants={child} className="inline-block">
          {char === ' ' ? '\u00A0' : char}
        </motion.span>
      ))}
    </motion.span>
  )
}
```

### 5. Image Reveal (GSAP)

```tsx
'use client'
import { useRef } from 'react'
import { gsap, useGSAP } from '@/lib/gsap'

export function ImageReveal({ src, alt }: { src: string; alt: string }) {
  const containerRef = useRef<HTMLDivElement>(null)

  useGSAP(() => {
    gsap.from(containerRef.current, {
      clipPath: 'inset(100% 0% 0% 0%)',
      duration: 1.2,
      ease: 'power4.inOut',
      scrollTrigger: {
        trigger: containerRef.current,
        start: 'top 80%',
      },
    })

    gsap.from('.reveal-img', {
      scale: 1.3,
      duration: 1.5,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: containerRef.current,
        start: 'top 80%',
      },
    })
  }, { scope: containerRef })

  return (
    <div ref={containerRef} className="overflow-hidden">
      <img src={src} alt={alt} className="reveal-img w-full h-full object-cover" />
    </div>
  )
}
```

### 6. Glitch Text Effect (CSS + GSAP)

```tsx
'use client'
import { useRef, useEffect } from 'react'
import { gsap } from '@/lib/gsap'

export function GlitchText({ text }: { text: string }) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const layers = ref.current!.querySelectorAll('.g-layer')
    const tl = gsap.timeline({ repeat: -1, repeatDelay: 3 })
    tl.to(layers[0], { x: -5, duration: 0.05, ease: 'none' }, 0)
      .to(layers[0], { x: 5, duration: 0.05 }, 0.05)
      .to(layers[0], { x: 0, duration: 0.05 }, 0.1)
      .to(layers[1], { x: 5, duration: 0.05 }, 0.02)
      .to(layers[1], { x: -5, duration: 0.05 }, 0.07)
      .to(layers[1], { x: 0, duration: 0.05 }, 0.12)
    return () => { tl.kill() }
  }, [])

  return (
    <div ref={ref} className="relative font-mono text-5xl font-black">
      <span className="relative z-10">{text}</span>
      <span className="g-layer absolute inset-0 text-cyan-400 mix-blend-multiply" aria-hidden>{text}</span>
      <span className="g-layer absolute inset-0 text-red-400 mix-blend-multiply" aria-hidden>{text}</span>
    </div>
  )
}
```

### 7. Fractal Tree (Canvas 2D)

```tsx
'use client'
import { useRef, useEffect } from 'react'

export function FractalTree({ depth = 10, angle = 25 }: { depth?: number; angle?: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current!
    const ctx = canvas.getContext('2d')!
    canvas.width = canvas.offsetWidth * 2; canvas.height = canvas.offsetHeight * 2; ctx.scale(2, 2)
    let progress = 0, raf = 0

    function branch(x: number, y: number, len: number, a: number, d: number) {
      if (d > depth || len < 2) return
      const dp = Math.max(0, Math.min(1, progress * depth - d))
      if (dp <= 0) return
      const ex = x + Math.cos(a * Math.PI / 180) * len * dp
      const ey = y - Math.sin(a * Math.PI / 180) * len * dp
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(ex, ey)
      ctx.strokeStyle = `hsl(${120 + d * 15}, 60%, ${30 + d * 5}%)`
      ctx.lineWidth = Math.max(1, (depth - d) * 1.5); ctx.stroke()
      branch(ex, ey, len * 0.72, a + angle, d + 1)
      branch(ex, ey, len * 0.72, a - angle, d + 1)
    }
    const animate = () => {
      progress = Math.min(1, progress + 0.008)
      ctx.clearRect(0, 0, canvas.offsetWidth, canvas.offsetHeight)
      branch(canvas.offsetWidth / 2, canvas.offsetHeight, canvas.offsetHeight * 0.28, 90, 0)
      if (progress < 1) raf = requestAnimationFrame(animate)
    }
    animate()
    return () => cancelAnimationFrame(raf)
  }, [depth, angle])
  return <canvas ref={canvasRef} className="w-full h-full bg-gray-950" />
}
```

See [references/algorithmic-art.md](references/algorithmic-art.md) for L-systems, flow fields, attractors, noise, sacred geometry.

### 8. Geometric Dissection (SVG + GSAP)

```tsx
'use client'
import { useRef, useState } from 'react'
import { gsap } from '@/lib/gsap'

const P = [
  { id: 'A', tri: 'M 0,173 L 50,87 L 100,173 Z', sq: 'M 0,0 L 100,0 L 100,87 L 0,87 Z', c: '#f43f5e' },
  { id: 'B', tri: 'M 50,87 L 100,0 L 150,87 Z', sq: 'M 100,0 L 200,0 L 200,87 L 100,87 Z', c: '#8b5cf6' },
  { id: 'C', tri: 'M 100,173 L 150,87 L 200,173 Z', sq: 'M 0,87 L 100,87 L 100,173 L 0,173 Z', c: '#06b6d4' },
  { id: 'D', tri: 'M 50,87 L 100,173 L 150,87 L 100,0 Z', sq: 'M 100,87 L 200,87 L 200,173 L 100,173 Z', c: '#f59e0b' },
]
export function GeometricDissection() {
  const svg = useRef<SVGSVGElement>(null)
  const [isSq, setSq] = useState(false)
  const morph = () => {
    const t = !isSq
    P.forEach((p, i) => {
      const el = svg.current!.querySelector(`#d-${p.id}`)
      if (el) gsap.to(el, { attr: { d: t ? p.sq : p.tri }, duration: 1.5, ease: 'power2.inOut', delay: i * 0.15 })
    }); setSq(t)
  }
  return (
    <div className="flex flex-col items-center gap-4">
      <svg ref={svg} viewBox="-10 -10 220 200" className="w-64 h-64">
        {P.map(p => <path key={p.id} id={`d-${p.id}`} d={p.tri} fill={p.c} stroke="#000" strokeWidth="1.5" />)}
      </svg>
      <button onClick={morph} className="px-6 py-2 bg-white text-black font-mono text-sm">{isSq ? '△' : '□'}</button>
    </div>
  )
}
```

See [references/geometric-puzzles.md](references/geometric-puzzles.md) for tangram, tessellations, Penrose tiles, polyominoes.

### 9. Brutalist Grid (Motion)

```tsx
'use client'
import { motion } from 'motion/react'

export function BrutalistGrid({ items }: { items: string[] }) {
  return (
    <div className="grid grid-cols-3 border-2 border-black">
      {items.map((item, i) => (
        <motion.div key={i}
          className="border-2 border-black p-6 font-mono font-black uppercase text-2xl"
          style={{ mixBlendMode: i % 2 === 0 ? 'normal' : 'difference' }}
          initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }}
          transition={{ duration: 0, delay: i * 0.1 }}
          whileHover={{ backgroundColor: '#000', color: '#BAFF39', transition: { duration: 0 } }}
        >{item}</motion.div>
      ))}
    </div>
  )
}
```

## Design Philosophy (Quick Reference)

| Style | Motion Feel | Easing | Typography | Key Trait |
|-------|------------|--------|------------|-----------|
| Brutalist | Hard, instant, jarring | `none` / `steps()` | Mono, 15-30vw | Raw honesty |
| Minimalist | Smooth, subtle, slow | `power2.out` | Sans-serif light | Purposeful restraint |
| Abstract | Noise-driven, parametric | Organic/sine | Varies | Mathematical beauty |
| Neo-Brutalist | Bold but controlled | `power1.out` | Mono + color | Brutalism + restraint |

See [references/design-philosophy.md](references/design-philosophy.md) for full guide with color palettes and mixing strategies.

## Easing Reference

| Feel | GSAP | Motion |
|------|------|--------|
| Smooth | `power2.out` | `[0.16, 1, 0.3, 1]` |
| Snappy | `power4.out` | `[0.87, 0, 0.13, 1]` |
| Bouncy | `back.out(1.7)` | `{ type: 'spring', stiffness: 300, damping: 20 }` |
| Dramatic | `power4.inOut` | `[0.76, 0, 0.24, 1]` |

## Timing

- Micro-interactions: 150-300ms
- UI transitions: 300-500ms
- Page transitions: 500-800ms
- Stagger: 0.02-0.1s per item

## Accessibility

```tsx
// Motion: useReducedMotion() → conditionally disable/reduce animations
import { useReducedMotion } from 'motion/react'
const reduced = useReducedMotion() // true if prefers-reduced-motion: reduce
```

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

## Performance Rules

1. Only animate `transform` and `opacity`
2. Use `will-change` sparingly
3. Always cleanup: `useGSAP` handles it automatically
4. Scope GSAP selectors to container refs
5. Use `contextSafe()` for event handlers with GSAP
6. Memoize Motion variants objects

## Common Pitfalls

1. Not integrating Lenis with ScrollTrigger
2. Missing `scope` in useGSAP
3. Not using `contextSafe()` for click handlers
4. React 18 Strict Mode calling effects twice
5. Forgetting `'use client'` in Next.js App Router
6. Not calling `ScrollTrigger.refresh()` after dynamic content

## Testing Checklist

- [ ] 60fps on scroll (Chrome DevTools Performance)
- [ ] Keyboard navigation works
- [ ] Respects prefers-reduced-motion
- [ ] No layout shifts (CLS)
- [ ] Mobile touch works
- [ ] ScrollTrigger markers removed in prod
- [ ] No memory leaks on unmount

## Inspiration

Active Theory, Studio Freight, Locomotive, Resn, Aristide Benoist, Immersive Garden
