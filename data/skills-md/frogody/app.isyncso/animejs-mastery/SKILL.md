---
name: animejs-mastery
description: Autonomous agent for systematically upgrading applications with polished anime.js animations. Use when asked to add animations, improve UI polish, upgrade visual experience, or make an app feel more alive. Triggers on requests like "add animations", "make it feel polished", "upgrade the UX", "animate the app", "make transitions smooth".
---

# Anime.js Animation Upgrade Agent

Autonomous agent that analyzes codebases and systematically implements polished, performant animations using anime.js.

## Agent Workflow

Execute these phases sequentially. Work autonomously—don't ask for permission between steps.

### Phase 1: Codebase Analysis

```bash
# 1. Identify framework and structure
find . -name "package.json" -o -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" | head -20

# 2. Check if anime.js is installed
grep -r "animejs\|anime.js" package.json 2>/dev/null || echo "NOT_INSTALLED"

# 3. Map component structure
find . -type f \( -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" \) -path "*/components/*" | head -50
```

**Install anime.js if missing:**
```bash
npm install animejs
# For TypeScript projects:
npm install --save-dev @types/animejs
```

### Phase 2: Opportunity Identification

Scan the codebase for these high-impact animation opportunities:

| Priority | Pattern to Find | Animation Type |
|----------|-----------------|----------------|
| **P0** | Page/route transitions | Fade + slide sequences |
| **P0** | Loading states, spinners | Smooth pulsing/rotation |
| **P1** | Lists rendering data | Staggered entrance |
| **P1** | Modals/dialogs/drawers | Scale + fade entrance |
| **P1** | Form submissions | Success/error feedback |
| **P2** | Buttons, CTAs | Hover/press micro-interactions |
| **P2** | Cards, tiles | Hover lift effects |
| **P2** | Data visualizations | Number counting, chart reveals |
| **P3** | Icons, badges | Attention pulses |
| **P3** | Tooltips, popovers | Soft entrance |

**Search patterns:**
```bash
# Find loading states
grep -rn "loading\|isLoading\|skeleton\|Spinner" --include="*.tsx" --include="*.jsx"

# Find modals/dialogs
grep -rn "Modal\|Dialog\|Drawer\|Sheet" --include="*.tsx" --include="*.jsx"

# Find lists with map
grep -rn "\.map(" --include="*.tsx" --include="*.jsx" | grep -i "item\|card\|row"

# Find buttons
grep -rn "<button\|<Button\|onClick" --include="*.tsx" --include="*.jsx"

# Find route transitions
grep -rn "Route\|router\|navigate\|Link" --include="*.tsx" --include="*.jsx"
```

### Phase 3: Create Animation Utilities

Create a shared animation utilities file first:

```typescript
// src/lib/animations.ts (or utils/animations.ts)
import anime from 'animejs';

// Respect user preferences
export const prefersReducedMotion = () =>
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Safe animate wrapper
export const safeAnimate = (
  targets: anime.AnimeParams['targets'],
  params: Omit<anime.AnimeParams, 'targets'>
) => {
  if (prefersReducedMotion()) {
    return anime({ targets, ...params, duration: 0 });
  }
  return anime({ targets, ...params });
};

// Staggered list entrance
export const staggerIn = (selector: string, delay = 50) =>
  safeAnimate(selector, {
    translateY: [20, 0],
    opacity: [0, 1],
    delay: anime.stagger(delay),
    duration: 400,
    easing: 'easeOutQuad',
  });

// Modal entrance
export const modalIn = (selector: string) =>
  safeAnimate(selector, {
    scale: [0.95, 1],
    opacity: [0, 1],
    duration: 200,
    easing: 'easeOutQuad',
  });

// Button press feedback
export const buttonPress = (element: HTMLElement) =>
  safeAnimate(element, {
    scale: [1, 0.97, 1],
    duration: 150,
    easing: 'easeInOutQuad',
  });

// Success animation
export const successPop = (selector: string) =>
  safeAnimate(selector, {
    scale: [0, 1.1, 1],
    opacity: [0, 1],
    duration: 400,
    easing: 'easeOutBack',
  });

// Error shake
export const errorShake = (selector: string) =>
  safeAnimate(selector, {
    translateX: [0, -8, 8, -8, 8, -4, 4, 0],
    duration: 400,
    easing: 'easeInOutQuad',
  });

// Fade out (for exits)
export const fadeOut = (selector: string) =>
  safeAnimate(selector, {
    opacity: [1, 0],
    translateY: [0, -10],
    duration: 200,
    easing: 'easeInQuad',
  });

// Number counter
export const countUp = (
  element: HTMLElement,
  endValue: number,
  duration = 1000
) => {
  const obj = { value: 0 };
  return anime({
    targets: obj,
    value: endValue,
    round: 1,
    duration,
    easing: 'easeOutExpo',
    update: () => {
      element.textContent = obj.value.toLocaleString();
    },
  });
};

// Skeleton pulse
export const skeletonPulse = (selector: string) =>
  safeAnimate(selector, {
    opacity: [0.5, 1, 0.5],
    duration: 1500,
    loop: true,
    easing: 'easeInOutSine',
  });
```

### Phase 4: React Hook Pattern

Create reusable hooks for React projects:

```typescript
// src/hooks/useAnimation.ts
import { useEffect, useRef, useCallback } from 'react';
import anime from 'animejs';
import { prefersReducedMotion } from '@/lib/animations';

export function useStaggeredEntrance<T extends HTMLElement>(
  deps: unknown[] = []
) {
  const containerRef = useRef<T>(null);

  useEffect(() => {
    if (!containerRef.current || prefersReducedMotion()) return;

    const children = containerRef.current.children;
    anime({
      targets: children,
      translateY: [20, 0],
      opacity: [0, 1],
      delay: anime.stagger(50),
      duration: 400,
      easing: 'easeOutQuad',
    });
  }, deps);

  return containerRef;
}

export function useButtonFeedback() {
  const handlePress = useCallback((e: React.MouseEvent<HTMLElement>) => {
    if (prefersReducedMotion()) return;
    
    anime({
      targets: e.currentTarget,
      scale: [1, 0.97, 1],
      duration: 150,
      easing: 'easeInOutQuad',
    });
  }, []);

  return { onMouseDown: handlePress };
}

export function useHoverLift<T extends HTMLElement>() {
  const ref = useRef<T>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el || prefersReducedMotion()) return;

    const enter = () => {
      anime.remove(el);
      anime({
        targets: el,
        translateY: -4,
        boxShadow: '0 8px 30px rgba(0,0,0,0.12)',
        duration: 200,
        easing: 'easeOutQuad',
      });
    };

    const leave = () => {
      anime.remove(el);
      anime({
        targets: el,
        translateY: 0,
        boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
        duration: 200,
        easing: 'easeOutQuad',
      });
    };

    el.addEventListener('mouseenter', enter);
    el.addEventListener('mouseleave', leave);
    return () => {
      el.removeEventListener('mouseenter', enter);
      el.removeEventListener('mouseleave', leave);
    };
  }, []);

  return ref;
}

export function useCountUp(endValue: number, duration = 1000) {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    
    const obj = { value: 0 };
    anime({
      targets: obj,
      value: endValue,
      round: 1,
      duration: prefersReducedMotion() ? 0 : duration,
      easing: 'easeOutExpo',
      update: () => {
        if (ref.current) {
          ref.current.textContent = obj.value.toLocaleString();
        }
      },
    });
  }, [endValue, duration]);

  return ref;
}
```

### Phase 5: Implementation Checklist

Work through components systematically. For each component:

1. **Identify the animation opportunity** (entrance, interaction, feedback)
2. **Add necessary imports**
3. **Implement using utilities/hooks**
4. **Test reduced-motion behavior**
5. **Verify 60fps performance**

**Implementation order:**
1. Animation utilities file
2. React hooks (if React project)
3. P0: Page transitions, loading states
4. P1: Lists, modals, form feedback
5. P2: Buttons, cards
6. P3: Icons, tooltips

### Phase 6: Common Implementation Patterns

**List component with staggered entrance:**
```tsx
function ItemList({ items }) {
  const listRef = useStaggeredEntrance<HTMLUListElement>([items]);
  
  return (
    <ul ref={listRef}>
      {items.map(item => (
        <li key={item.id} style={{ opacity: 0 }}>
          {item.name}
        </li>
      ))}
    </ul>
  );
}
```

**Button with press feedback:**
```tsx
function AnimatedButton({ children, onClick, ...props }) {
  const feedbackProps = useButtonFeedback();
  
  return (
    <button {...props} {...feedbackProps} onClick={onClick}>
      {children}
    </button>
  );
}
```

**Card with hover lift:**
```tsx
function Card({ children }) {
  const cardRef = useHoverLift<HTMLDivElement>();
  
  return (
    <div ref={cardRef} className="card">
      {children}
    </div>
  );
}
```

**Modal with entrance animation:**
```tsx
function Modal({ isOpen, children }) {
  const modalRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (isOpen && modalRef.current) {
      modalIn(modalRef.current);
    }
  }, [isOpen]);
  
  if (!isOpen) return null;
  
  return (
    <div ref={modalRef} className="modal" style={{ opacity: 0 }}>
      {children}
    </div>
  );
}
```

## Performance Rules

**ALWAYS animate (GPU-accelerated):**
- `translateX`, `translateY`, `translateZ`
- `scale`, `rotate`
- `opacity`

**NEVER animate (triggers layout):**
- `width`, `height`
- `padding`, `margin`
- `top`, `left`, `right`, `bottom`

**Timing guidelines:**
| Type | Duration | Easing |
|------|----------|--------|
| Micro-interaction | 100-200ms | `easeOutQuad` |
| Button feedback | 150ms | `easeInOutQuad` |
| Modal entrance | 200-250ms | `easeOutQuad` |
| List stagger | 50-100ms between | `easeOutQuad` |
| Page transition | 300ms | `easeOutQuint` |

## Output Format

After implementation, provide a summary:

```markdown
## Animation Upgrade Summary

### Files Created
- `src/lib/animations.ts` - Core utilities
- `src/hooks/useAnimation.ts` - React hooks

### Components Updated
| Component | Animation Added | Priority |
|-----------|-----------------|----------|
| ItemList | Staggered entrance | P1 |
| Modal | Scale + fade in | P1 |
| Button | Press feedback | P2 |

### Performance Notes
- All animations use transform/opacity only
- Reduced motion respected globally
- Average animation duration: 200ms
```

## Reference Files

For detailed API documentation: `references/api-reference.md`
For additional patterns: `references/patterns.md`
