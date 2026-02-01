---
name: responsive-design
description: Responsive web design patterns for mobile-first development. Use for creating fluid layouts, breakpoint systems, responsive typography, flexible grids, and adaptive components. Triggers on requests for responsive layouts, mobile-first CSS, breakpoints, media queries, fluid design, or multi-device support.
---

# Responsive Design

## Mobile-First Breakpoints

```css
/* Base: Mobile (0-639px) - no media query needed */

/* sm: Large phones / Small tablets */
@media (min-width: 640px) { }

/* md: Tablets */
@media (min-width: 768px) { }

/* lg: Small laptops */
@media (min-width: 1024px) { }

/* xl: Desktops */
@media (min-width: 1280px) { }

/* 2xl: Large screens */
@media (min-width: 1536px) { }
```

## CSS Token Integration

```css
:root {
  /* Breakpoint tokens */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  
  /* Container max-widths */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  
  /* Fluid spacing */
  --space-responsive: clamp(1rem, 4vw, 2rem);
  --space-section: clamp(2rem, 8vw, 6rem);
}
```

## Fluid Typography

```css
:root {
  /* Fluid type scale */
  --text-fluid-sm: clamp(0.875rem, 0.8rem + 0.25vw, 1rem);
  --text-fluid-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-fluid-lg: clamp(1.125rem, 1rem + 0.75vw, 1.5rem);
  --text-fluid-xl: clamp(1.5rem, 1.2rem + 1.5vw, 2.5rem);
  --text-fluid-2xl: clamp(2rem, 1.5rem + 2.5vw, 4rem);
  --text-fluid-hero: clamp(2.5rem, 2rem + 4vw, 6rem);
}

h1 { font-size: var(--text-fluid-2xl); }
h2 { font-size: var(--text-fluid-xl); }
p { font-size: var(--text-fluid-base); }
```

## Layout Patterns

### Fluid Grid

```css
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
  gap: var(--space-4);
}
```

### Responsive Stack

```css
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

@media (min-width: 768px) {
  .stack--row-md {
    flex-direction: row;
  }
}
```

### Container Query Ready

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    flex-direction: row;
  }
}
```

## React Pattern

```tsx
// useMediaQuery.ts
export const useMediaQuery = (query: string): boolean => {
  const [matches, setMatches] = useState(
    () => window.matchMedia(query).matches
  );

  useEffect(() => {
    const mq = window.matchMedia(query);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, [query]);

  return matches;
};

// useBreakpoint.ts
export const useBreakpoint = () => {
  const isMobile = useMediaQuery('(max-width: 639px)');
  const isTablet = useMediaQuery('(min-width: 640px) and (max-width: 1023px)');
  const isDesktop = useMediaQuery('(min-width: 1024px)');
  
  return { isMobile, isTablet, isDesktop };
};
```

## Responsive Component Pattern

```tsx
interface ResponsiveProps {
  mobile?: ReactNode;
  tablet?: ReactNode;
  desktop: ReactNode;
}

export const Responsive: FC<ResponsiveProps> = ({ mobile, tablet, desktop }) => {
  const { isMobile, isTablet } = useBreakpoint();
  
  if (isMobile && mobile) return <>{mobile}</>;
  if (isTablet && tablet) return <>{tablet}</>;
  return <>{desktop}</>;
};
```

## Key Principles

| Principle | Implementation |
|-----------|----------------|
| Mobile-first | Base styles = mobile, enhance with min-width |
| Fluid over fixed | Use clamp(), %, vw instead of fixed px |
| Content breakpoints | Break when content breaks, not at devices |
| Touch targets | Minimum 44×44px on mobile |
| Readable line length | Max 65-75 characters |

## Common Mistakes

❌ Using max-width (desktop-first)
✅ Using min-width (mobile-first)

❌ Fixed pixel values everywhere
✅ Fluid units (rem, %, vw, clamp)

❌ Hiding content on mobile
✅ Prioritizing and reorganizing content

❌ Breakpoints for specific devices
✅ Breakpoints where design breaks
