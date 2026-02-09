---
name: frontend-magic-ui
description: Polished SaaS landing page components. Use for number tickers/stats animations, logo marquees, bento grids, device mockups (iPhone, Safari), shimmer/rainbow buttons, typing effects. Professional marketing polish built on Framer Motion + Tailwind. For dramatic hero effects use Aceternity, for basic UI use shadcn.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Magic UI

150+ animated components for SaaS landing pages. Professional polish, production-ready.

## When to Use

- Number/stat animations (tickers, counters)
- Logo walls (marquee)
- Bento grid layouts
- Device mockups (iPhone, Safari)
- Text animations (typing, word rotate)
- Shimmer/rainbow buttons

## When NOT to Use

- Basic UI → shadcn/ui
- Dramatic hero effects → Aceternity
- State-driven animations → Rive

## Process

**NEED → ADD → CUSTOMIZE**

1. Identify component type
2. Install: `npx magicui-cli@latest add [component]`
3. Customize props/styles

## Dependencies

```bash
npm install framer-motion clsx tailwind-merge
```

## Component Categories

```yaml
Text:       number-ticker, typing-animation, word-rotate, flip-text, morphing-text
Buttons:    shimmer-button, rainbow-button, pulsating-button, shiny-button
Patterns:   dot-pattern, grid-pattern, retro-grid, particles, meteors
Mockups:    iphone-15-pro, safari, android
Layout:     bento-grid, marquee, dock, animated-list, file-tree
Effects:    orbiting-circles, animated-beam, border-beam, confetti, globe
```

## Decision Tree

```yaml
Need animated component?
  ├─ Stats/numbers → number-ticker
  ├─ Logo carousel → marquee
  ├─ Feature grid → bento-grid
  ├─ CTA button → shimmer-button, rainbow-button
  ├─ App screenshot → safari, iphone-15-pro
  ├─ Dynamic headline → word-rotate, typing-animation
  └─ Integration diagram → orbiting-circles, animated-beam
```

## Quick Patterns

```tsx
// Number Ticker
<div className="flex gap-12">
  <NumberTicker value={10000} className="text-4xl font-bold" />
  <span className="text-4xl">+</span>
</div>

// Marquee (logo wall)
<Marquee pauseOnHover className="[--duration:20s]">
  {logos.map(logo => <img key={logo.name} src={logo.img} />)}
</Marquee>

// Word Rotate
<h1>Build <WordRotate words={["faster", "better"]} /> apps</h1>

// Safari Mockup
<Safari url="yourapp.com" src="/screenshot.png" />
```

## Customization

```tsx
// Speed via CSS variables
<Marquee className="[--duration:40s]">...</Marquee>
<NumberTicker className="[--duration:3s]" value={1000} />

// Colors
<ShimmerButton
  shimmerColor="#a855f7"
  background="linear-gradient(to right, #6366f1, #8b5cf6)"
>
  Custom
</ShimmerButton>

// Marquee gap
<Marquee className="[--gap:2rem]">...</Marquee>
```

## SSR & Hydration

```tsx
// Always 'use client'
'use client'

// Heavy components: dynamic import
import dynamic from 'next/dynamic'
const Globe = dynamic(() => import('@/components/magicui/globe'), { ssr: false })

// Mounted check pattern
const [mounted, setMounted] = useState(false)
useEffect(() => setMounted(true), [])
if (!mounted) return <Skeleton />
```

## Magic UI vs Aceternity

| Use Case | Magic UI | Aceternity |
|----------|----------|------------|
| Number animation | ✓ NumberTicker | ✗ |
| Logo carousel | ✓ Marquee | ✓ InfiniteMovingCards |
| Hero spotlight | ✗ | ✓ Spotlight |
| Device mockup | ✓ Safari/iPhone | ✗ |
| 3D card tilt | ✗ | ✓ 3D Card |

**Rule:** Magic UI = polished SaaS, Aceternity = dramatic effects

## Troubleshooting

```yaml
"Component not found":
  → npx magicui-cli@latest add [name]
  → Check components/magicui/[name].tsx

"Animation not playing":
  → Add 'use client'
  → Check framer-motion installed

"Hydration mismatch":
  → dynamic(() => ..., { ssr: false })

"Marquee stuttering":
  → Increase [--duration:Xs]
  → Use pauseOnHover
```

## References

- **[components.md](references/components.md)** — Full component API with all props

## External Resources

- https://magicui.design/docs — Documentation
- For latest API → use context7 skill
