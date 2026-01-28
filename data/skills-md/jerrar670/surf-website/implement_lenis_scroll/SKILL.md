---
name: implement_lenis_scroll
description: Instructions for implementing Lenis smooth scrolling in a Next.js or React application.
---

# Implement Lenis Smooth Scroll

This skill guides you through adding buttery smooth scrolling to a React/Next.js application using `@studio-freight/lenis` (or the newer `lenis` package).

## Prerequisites
- A React or Next.js project.

## Steps

### 1. Install Dependencies
Install the Lenis package.
```bash
npm install lenis
# OR depending on version preference
npm install @studio-freight/lenis
```

### 2. Create the Lenis Hook/Component
It's best to encapsulate Lenis in a reusable component or hook.

**Option A: Global Component (Recommended for Next.js App Router)**
Create `src/lib/lenis.ts` or `src/components/SmoothScroll.tsx`.

```typescript
// src/components/SmoothScroll.tsx
'use client'

import { ReactNode, useEffect } from 'react'
import Lenis from 'lenis'

export default function SmoothScroll({ children }: { children: ReactNode }) {
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
    })

    function raf(time: number) {
      lenis.raf(time)
      requestAnimationFrame(raf)
    }

    requestAnimationFrame(raf)

    return () => {
      lenis.destroy()
    }
  }, [])

  return <>{children}</>
}
```

### 3. Integrate into Layout
Wrap your main application or layout content with the component.

**Next.js App Router (`layout.tsx`):**
```typescript
import SmoothScroll from '@/components/SmoothScroll'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <SmoothScroll>
          {children}
        </SmoothScroll>
      </body>
    </html>
  )
}
```

## Best Practices
- **Performance**: Ensure `requestAnimationFrame` is optimized.
- **Scroll Restoration**: Lenis usually handles this, but verify `scrollRestoration` works as expected in Next.js.
- **GSAP Integration**: If using ScrollTrigger, ensure you update ScrollTrigger on Lenis scroll.
  ```typescript
  // Inside useEffect
  // lenis.on('scroll', ScrollTrigger.update)
  // gsap.ticker.add((time)=>{lenis.raf(time * 1000)})
  // gsap.ticker.lagSmoothing(0)
  ```
