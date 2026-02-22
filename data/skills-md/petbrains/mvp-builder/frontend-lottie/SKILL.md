---
name: frontend-lottie
description: Decorative JSON animations for UI feedback and polish. Use for loading spinners, success/error checkmarks, empty state illustrations, animated icons. Just plays and loops - no interactivity. For reactive/stateful animations use Rive instead. Lightweight and SSR-compatible.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Lottie

Lightweight vector animations. Just plays and loops — no complex logic.

## When to Use

- Loading spinners
- Success/error checkmarks
- Empty state illustrations
- Decorative micro-animations
- Animated icons

## When NOT to Use

- Animation reacts to input → Rive
- Multiple states/transitions → Rive
- Complex interactivity → Rive

## Process

**FIND → ADD → INTEGRATE**

1. Find animation: https://lottiefiles.com
2. Download .lottie or .json
3. Place in `public/animations/`
4. Use component

## Quick Start

```bash
npm install @lottiefiles/dotlottie-react
```

```tsx
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

// Simple autoplay
<DotLottieReact
  src="/animations/loading.lottie"
  autoplay
  loop
  style={{ width: 200, height: 200 }}
/>
```

## Common Patterns

```tsx
// Loading spinner
<DotLottieReact src="/spinner.lottie" autoplay loop style={{ width: 48 }} />

// Success feedback (plays once)
<DotLottieReact src="/success.lottie" autoplay loop={false} />

// Empty state
<div className="flex flex-col items-center py-16">
  <DotLottieReact src="/empty.lottie" autoplay loop style={{ width: 200 }} />
  <h3>No results found</h3>
</div>

// Loading button
{isLoading ? (
  <DotLottieReact src="/button-loader.lottie" autoplay loop style={{ width: 24 }} />
) : (
  "Submit"
)}
```

## Decision: Lottie vs Rive

| Animation Type | Use |
|----------------|-----|
| Just plays/loops | Lottie ✓ |
| Reacts to hover/click | Rive |
| State machine | Rive |
| Data-driven | Rive |
| Simple loader | Lottie ✓ |

## Finding Animations

```yaml
LottieFiles:   https://lottiefiles.com/free-animations
Lordicon:      https://lordicon.com (animated icons)
useAnimations: https://useanimations.com (micro-interactions)
```

## Playback Control

```tsx
'use client'
import { useState, useCallback } from 'react'
import { DotLottieReact, DotLottie } from '@lottiefiles/dotlottie-react'

function ControlledLottie() {
  const [dotLottie, setDotLottie] = useState<DotLottie | null>(null)

  return (
    <div
      onMouseEnter={() => dotLottie?.play()}
      onMouseLeave={() => dotLottie?.pause()}
    >
      <DotLottieReact
        src="/animation.lottie"
        loop
        dotLottieRefCallback={setDotLottie}
      />
    </div>
  )
}

// Methods: play(), pause(), stop(), setSpeed(n), goToAndPlay(frame)
```

## SSR & Hydration

```tsx
// Always 'use client'
'use client'

// Dynamic import
const DotLottieReact = dynamic(
  () => import('@lottiefiles/dotlottie-react').then(m => m.DotLottieReact),
  { ssr: false }
)

// Or mounted check
const [mounted, setMounted] = useState(false)
useEffect(() => setMounted(true), [])
if (!mounted) return <Skeleton />
```

## Performance

```tsx
// Pause when not visible
import { useInView } from 'react-intersection-observer'

const { ref, inView } = useInView({ threshold: 0.1 })

useEffect(() => {
  inView ? dotLottie?.play() : dotLottie?.pause()
}, [inView, dotLottie])
```

## File Structure

```
public/animations/
  loaders/spinner.lottie
  feedback/success.lottie, error.lottie
  empty-states/no-data.lottie
  illustrations/hero.lottie
```

## Troubleshooting

```yaml
"Animation not loading":
  → Check file path in public/
  → Verify .lottie or .json extension

"Animation not playing":
  → Add autoplay={true}
  → Add loop={true}

"Hydration mismatch":
  → Add 'use client'
  → Use dynamic(() => ..., { ssr: false })

"Too fast/slow":
  → speed={0.5} for slower
  → speed={2} for faster
```

## References

- **[patterns.md](references/patterns.md)** — Controlled playback, events, visibility pause, hover/click triggers

## External Resources

- https://lottiefiles.com/free-animations — Free animations
- https://useanimations.com — Micro-interactions
- https://lordicon.com — Animated icons
- For latest API → use context7 skill
