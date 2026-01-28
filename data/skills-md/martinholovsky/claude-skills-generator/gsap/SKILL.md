---
name: gsap
description: GSAP animations for JARVIS HUD transitions and effects
model: sonnet
risk_level: LOW
version: 1.0.0
---

# GSAP Animation Skill

> **File Organization**: This skill uses split structure. See `references/` for advanced patterns.

## 1. Overview

This skill provides GSAP (GreenSock Animation Platform) expertise for creating smooth, professional animations in the JARVIS AI Assistant HUD.

**Risk Level**: LOW - Animation library with minimal security surface

**Primary Use Cases**:
- HUD panel entrance/exit animations
- Status indicator transitions
- Data visualization animations
- Scroll-triggered effects
- Complex timeline sequences

## 2. Core Responsibilities

### 2.1 Fundamental Principles

1. **TDD First**: Write animation tests before implementation
2. **Performance Aware**: Use transforms/opacity for GPU acceleration, avoid layout thrashing
3. **Cleanup Required**: Always kill animations on component unmount
4. **Timeline Organization**: Use timelines for complex sequences
5. **Easing Selection**: Choose appropriate easing for HUD feel
6. **Accessibility**: Respect reduced motion preferences
7. **Memory Management**: Avoid memory leaks with proper cleanup

## 2.5 Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```typescript
// tests/animations/panel-animation.test.ts
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { gsap } from 'gsap'
import HUDPanel from '~/components/HUDPanel.vue'

describe('HUDPanel Animation', () => {
  beforeEach(() => {
    // Mock reduced motion
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: vi.fn().mockImplementation(query => ({
        matches: false,
        media: query
      }))
    })
  })

  afterEach(() => {
    // Verify cleanup
    gsap.globalTimeline.clear()
  })

  it('animates panel entrance with correct properties', async () => {
    const wrapper = mount(HUDPanel)

    // Wait for animation to complete
    await new Promise(resolve => setTimeout(resolve, 600))

    const panel = wrapper.find('.hud-panel')
    expect(panel.exists()).toBe(true)
  })

  it('cleans up animations on unmount', async () => {
    const wrapper = mount(HUDPanel)
    const childCount = gsap.globalTimeline.getChildren().length

    await wrapper.unmount()

    // All animations should be killed
    expect(gsap.globalTimeline.getChildren().length).toBeLessThan(childCount)
  })

  it('respects reduced motion preference', async () => {
    // Mock reduced motion enabled
    window.matchMedia = vi.fn().mockImplementation(() => ({
      matches: true
    }))

    const wrapper = mount(HUDPanel)
    const panel = wrapper.find('.hud-panel').element

    // Should set final state immediately without animation
    expect(gsap.getProperty(panel, 'opacity')).toBe(1)
  })
})
```

### Step 2: Implement Minimum to Pass

```typescript
// components/HUDPanel.vue - implement animation logic
const animation = ref<gsap.core.Tween | null>(null)

onMounted(() => {
  if (!panelRef.value) return

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    gsap.set(panelRef.value, { opacity: 1 })
    return
  }

  animation.value = gsap.from(panelRef.value, {
    opacity: 0,
    y: 20,
    duration: 0.5
  })
})

onUnmounted(() => {
  animation.value?.kill()
})
```

### Step 3: Refactor Following Patterns

```typescript
// Extract to composable for reusability
export function usePanelAnimation(elementRef: Ref<HTMLElement | null>) {
  const animation = ref<gsap.core.Tween | null>(null)

  const animate = () => {
    if (!elementRef.value) return

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      gsap.set(elementRef.value, { opacity: 1 })
      return
    }

    animation.value = gsap.from(elementRef.value, {
      opacity: 0,
      y: 20,
      duration: 0.5,
      ease: 'power2.out'
    })
  }

  onMounted(animate)
  onUnmounted(() => animation.value?.kill())

  return { animation }
}
```

### Step 4: Run Full Verification

```bash
# Run animation tests
npm test -- --grep "Animation"

# Check for memory leaks
npm run test:memory

# Verify 60fps performance
npm run test:performance
```

## 3. Technology Stack & Versions

### 3.1 Recommended Versions

| Package | Version | Notes |
|---------|---------|-------|
| gsap | ^3.12.0 | Core library |
| @gsap/vue | ^3.12.0 | Vue integration |
| ScrollTrigger | included | Scroll effects |

### 3.2 Vue Integration

```typescript
// plugins/gsap.ts
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

export default defineNuxtPlugin(() => {
  gsap.registerPlugin(ScrollTrigger)

  return {
    provide: {
      gsap,
      ScrollTrigger
    }
  }
})
```

## 4. Implementation Patterns

### 4.1 Panel Entrance Animation

```vue
<script setup lang="ts">
import { gsap } from 'gsap'
import { onMounted, onUnmounted, ref } from 'vue'

const panelRef = ref<HTMLElement | null>(null)
let animation: gsap.core.Tween | null = null

onMounted(() => {
  if (!panelRef.value) return

  // ✅ Check reduced motion preference
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    gsap.set(panelRef.value, { opacity: 1 })
    return
  }

  animation = gsap.from(panelRef.value, {
    opacity: 0,
    y: 20,
    scale: 0.95,
    duration: 0.5,
    ease: 'power2.out'
  })
})

// ✅ Cleanup on unmount
onUnmounted(() => {
  animation?.kill()
})
</script>

<template>
  <div ref="panelRef" class="hud-panel">
    <slot />
  </div>
</template>
```

### 4.2 Status Indicator Animation

```typescript
// composables/useStatusAnimation.ts
import { gsap } from 'gsap'

export function useStatusAnimation(element: Ref<HTMLElement | null>) {
  const timeline = ref<gsap.core.Timeline | null>(null)

  const animateStatus = (status: string) => {
    if (!element.value) return

    timeline.value?.kill()

    timeline.value = gsap.timeline()

    switch (status) {
      case 'active':
        timeline.value
          .to(element.value, {
            scale: 1.2,
            duration: 0.2,
            ease: 'power2.out'
          })
          .to(element.value, {
            scale: 1,
            duration: 0.3,
            ease: 'elastic.out(1, 0.3)'
          })
        break

      case 'warning':
        timeline.value.to(element.value, {
          backgroundColor: '#f59e0b',
          boxShadow: '0 0 10px #f59e0b',
          duration: 0.3,
          repeat: 2,
          yoyo: true
        })
        break

      case 'error':
        timeline.value.to(element.value, {
          x: -5,
          duration: 0.05,
          repeat: 5,
          yoyo: true
        })
        break
    }
  }

  onUnmounted(() => {
    timeline.value?.kill()
  })

  return { animateStatus }
}
```

### 4.3 Data Visualization Animation

```vue
<script setup lang="ts">
import { gsap } from 'gsap'

const props = defineProps<{
  data: number[]
}>()

const barsRef = ref<HTMLElement[]>([])
let animations: gsap.core.Tween[] = []

watch(() => props.data, (newData) => {
  // Kill previous animations
  animations.forEach(a => a.kill())
  animations = []

  // Animate each bar
  newData.forEach((value, index) => {
    const bar = barsRef.value[index]
    if (!bar) return

    const tween = gsap.to(bar, {
      height: `${value}%`,
      duration: 0.5,
      delay: index * 0.05,
      ease: 'power2.out'
    })

    animations.push(tween)
  })
}, { immediate: true })

onUnmounted(() => {
  animations.forEach(a => a.kill())
})
</script>

<template>
  <div class="flex items-end h-40 gap-1">
    <div
      v-for="(_, index) in data"
      :key="index"
      ref="barsRef"
      class="w-4 bg-jarvis-primary"
    />
  </div>
</template>
```

### 4.4 Timeline Sequence

```typescript
// Create complex HUD startup sequence
export function createStartupSequence(elements: {
  logo: HTMLElement
  panels: HTMLElement[]
  status: HTMLElement
}): gsap.core.Timeline {
  const tl = gsap.timeline({
    defaults: { ease: 'power2.out' }
  })

  // Logo reveal
  tl.from(elements.logo, {
    opacity: 0,
    scale: 0,
    duration: 0.8,
    ease: 'back.out(1.7)'
  })

  // Panels stagger in
  tl.from(elements.panels, {
    opacity: 0,
    x: -30,
    stagger: 0.1,
    duration: 0.5
  }, '-=0.3')

  // Status indicator
  tl.from(elements.status, {
    opacity: 0,
    y: 10,
    duration: 0.3
  }, '-=0.2')

  return tl
}
```

### 4.5 Scroll-Triggered Animation

```vue
<script setup lang="ts">
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

const sectionRef = ref<HTMLElement | null>(null)

onMounted(() => {
  if (!sectionRef.value) return

  gsap.from(sectionRef.value.querySelectorAll('.animate-item'), {
    scrollTrigger: {
      trigger: sectionRef.value,
      start: 'top 80%',
      end: 'bottom 20%',
      toggleActions: 'play none none reverse'
    },
    opacity: 0,
    y: 30,
    stagger: 0.1,
    duration: 0.5
  })
})

onUnmounted(() => {
  ScrollTrigger.getAll().forEach(trigger => trigger.kill())
})
</script>
```

## 5. Quality Standards

### 5.1 Performance

```typescript
// ✅ GOOD - Use transforms for GPU acceleration
gsap.to(element, {
  x: 100,
  y: 50,
  rotation: 45,
  scale: 1.2
})

// ❌ BAD - Triggers layout recalculation
gsap.to(element, {
  left: 100,
  top: 50,
  width: '120%'
})
```

### 5.2 Accessibility

```typescript
// ✅ Respect reduced motion
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches

if (prefersReducedMotion) {
  gsap.set(element, { opacity: 1 })
} else {
  gsap.from(element, { opacity: 0, duration: 0.5 })
}
```

## 6. Performance Patterns

### 6.1 will-change Property Usage

```typescript
// Good: Apply will-change before animation
const animatePanel = (element: HTMLElement) => {
  element.style.willChange = 'transform, opacity'

  gsap.to(element, {
    x: 100,
    opacity: 0.8,
    duration: 0.5,
    onComplete: () => {
      element.style.willChange = 'auto'
    }
  })
}

// Bad: Never removing will-change
const animatePanelBad = (element: HTMLElement) => {
  element.style.willChange = 'transform, opacity' // Memory leak!
  gsap.to(element, { x: 100, opacity: 0.8 })
}
```

### 6.2 Transform vs Layout Properties

```typescript
// Good: Use transforms (GPU accelerated)
gsap.to(element, {
  x: 100,           // translateX
  y: 50,            // translateY
  scale: 1.2,       // scale
  rotation: 45,     // rotate
  opacity: 0.5      // opacity
})

// Bad: Layout-triggering properties (CPU, causes reflow)
gsap.to(element, {
  left: 100,        // Triggers layout
  top: 50,          // Triggers layout
  width: '120%',    // Triggers layout
  height: 200,      // Triggers layout
  margin: 10        // Triggers layout
})
```

### 6.3 Timeline Reuse

```typescript
// Good: Reuse timeline instance
const timeline = gsap.timeline({ paused: true })
timeline
  .to(element, { opacity: 1, duration: 0.3 })
  .to(element, { y: -20, duration: 0.5 })

// Play/reverse as needed
const show = () => timeline.play()
const hide = () => timeline.reverse()

// Bad: Creating new timeline each time
const showBad = () => {
  gsap.timeline()
    .to(element, { opacity: 1, duration: 0.3 })
    .to(element, { y: -20, duration: 0.5 })
}
```

### 6.4 ScrollTrigger Batching

```typescript
// Good: Batch ScrollTrigger animations
ScrollTrigger.batch('.animate-item', {
  onEnter: (elements) => {
    gsap.to(elements, {
      opacity: 1,
      y: 0,
      stagger: 0.1,
      overwrite: true
    })
  },
  onLeave: (elements) => {
    gsap.to(elements, {
      opacity: 0,
      y: -20,
      overwrite: true
    })
  }
})

// Bad: Individual ScrollTrigger per element
document.querySelectorAll('.animate-item').forEach(item => {
  gsap.to(item, {
    scrollTrigger: {
      trigger: item,
      start: 'top 80%'
    },
    opacity: 1,
    y: 0
  })
})
```

### 6.5 Lazy Initialization

```typescript
// Good: Initialize animations only when needed
let panelAnimation: gsap.core.Timeline | null = null

const getPanelAnimation = () => {
  if (!panelAnimation) {
    panelAnimation = gsap.timeline({ paused: true })
      .from('.panel', { opacity: 0, y: 20 })
      .from('.panel-content', { opacity: 0, stagger: 0.1 })
  }
  return panelAnimation
}

const showPanel = () => getPanelAnimation().play()
const hidePanel = () => getPanelAnimation().reverse()

// Bad: Initialize all animations on mount
onMounted(() => {
  // Creates timeline even if never used
  const animation1 = gsap.timeline().to('.panel1', { x: 100 })
  const animation2 = gsap.timeline().to('.panel2', { y: 100 })
  const animation3 = gsap.timeline().to('.panel3', { scale: 1.2 })
})
```

## 7. Testing & Quality

### 7.1 Animation Testing

```typescript
describe('Panel Animation', () => {
  it('cleans up on unmount', async () => {
    const wrapper = mount(HUDPanel)
    await wrapper.unmount()

    // No active GSAP animations should remain
    expect(gsap.globalTimeline.getChildren().length).toBe(0)
  })
})
```

## 8. Common Mistakes & Anti-Patterns

### 8.1 Critical Anti-Patterns

#### Never: Skip Cleanup

```typescript
// ❌ MEMORY LEAK
onMounted(() => {
  gsap.to(element, { x: 100, duration: 1 })
})

// ✅ PROPER CLEANUP
let tween: gsap.core.Tween

onMounted(() => {
  tween = gsap.to(element, { x: 100, duration: 1 })
})

onUnmounted(() => {
  tween?.kill()
})
```

#### Never: Animate Layout Properties

```typescript
// ❌ BAD - Causes layout thrashing
gsap.to(element, { width: 200, height: 100 })

// ✅ GOOD - Use transforms
gsap.to(element, { scaleX: 2, scaleY: 1 })
```

## 13. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Write failing tests for animation behavior
- [ ] Define animation timing and easing requirements
- [ ] Identify elements that need will-change hints
- [ ] Plan cleanup strategy for all animations
- [ ] Check if reduced motion support is needed

### Phase 2: During Implementation

- [ ] Use transforms/opacity only (no layout properties)
- [ ] Store animation references for cleanup
- [ ] Apply will-change before, remove after animation
- [ ] Use timelines for sequences
- [ ] Batch ScrollTrigger animations
- [ ] Implement lazy initialization for complex animations

### Phase 3: Before Committing

- [ ] All tests pass (npm test -- --grep "Animation")
- [ ] All animations cleaned up on unmount
- [ ] Reduced motion preference respected
- [ ] No memory leaks (check with DevTools)
- [ ] 60fps maintained (test with performance monitor)
- [ ] ScrollTrigger instances properly killed

## 14. Summary

GSAP provides professional animations for JARVIS HUD:

1. **Cleanup**: Always kill animations on unmount
2. **Performance**: Use transforms and opacity only
3. **Accessibility**: Respect reduced motion preference
4. **Organization**: Use timelines for sequences

**Remember**: Every animation must be cleaned up to prevent memory leaks.

---

**References**:
- `references/advanced-patterns.md` - Complex animation patterns
