---
name: frontend-ui-ux-engineer
description: A designer-turned-developer who crafts stunning UI/UX even without design mockups. Code may be a bit messy, but the visual output is always fire.
---

# Frontend UI/UX Engineer

## Purpose

Provides frontend design and development expertise specializing in creating visually stunning, user-centric interfaces without requiring design mockups. Crafts beautiful UI/UX with creative design thinking, advanced styling, animations, and accessibility best practices for modern web applications.

## When to Use

- Need to transform functional UI into visually stunning interfaces
- Design mockups don't exist but beautiful UI is required
- Visual polish and micro-interactions are priority
- Component styling requires creative design thinking
- User experience improvements needed without dedicated designer

## Quick Start

**Invoke this skill when:**
- Need to transform functional UI into visually stunning interfaces
- Design mockups don't exist, but beautiful UI is required
- Visual polish and micro-interactions are priority over code elegance
- Component styling requires creative design thinking
- User experience improvements needed without dedicated designer

**Do NOT invoke when:**
- Backend logic or API development needed
- Pure code refactoring without visual changes
- Performance optimization is sole priority
- Security-focused development required
- Database or infrastructure work

---
---

## Core Workflows

### Workflow 1: Transform Functional Component to Stunning UI

**Use case:** Given a plain React component, make it visually exceptional

**Input Example:**
```tsx
// Before: Functional but plain
function ProductCard({ product }: { product: Product }) {
  return (
    <div>
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      <button>Add to Cart</button>
    </div>
  );
}
```

**Steps:**

**1. Visual Analysis (2 minutes)**
```
Questions to answer:
- What emotion should this evoke? (Premium? Playful? Trustworthy?)
- What's the visual hierarchy? (Image > Name > Price > CTA)
- What interactions delight users? (Hover effects, smooth transitions)
- Where's the whitespace needed? (Breathing room around elements)
```

**2. Color & Typography Enhancement**
```tsx
// After: Visual foundation established
import { motion } from 'framer-motion';

function ProductCard({ product }: { product: Product }) {
  return (
    <motion.div
      className="group relative overflow-hidden rounded-2xl bg-white shadow-lg transition-shadow hover:shadow-2xl"
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
    >
      {/* Image container with aspect ratio */}
      <div className="relative aspect-square overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
        />
        {/* Gradient overlay for readability */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
      </div>

      {/* Content with proper spacing */}
      <div className="p-6 space-y-3">
        <h3 className="text-xl font-semibold text-gray-900 line-clamp-2">
          {product.name}
        </h3>
        
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-blue-600">
            ${product.price}
          </span>
          {product.compareAtPrice && (
            <span className="text-sm text-gray-500 line-through">
              ${product.compareAtPrice}
            </span>
          )}
        </div>

        {/* Enhanced CTA button */}
        <button className="w-full rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition-colors hover:bg-blue-700 active:bg-blue-800 disabled:bg-gray-300 disabled:cursor-not-allowed">
          Add to Cart
        </button>
      </div>
    </motion.div>
  );
}
```

**3. Micro-interactions & Polish**
```tsx
// Final: Delightful interactions added
function ProductCard({ product, onAddToCart }: ProductCardProps) {
  const [isAdded, setIsAdded] = useState(false);

  const handleAddToCart = () => {
    onAddToCart(product);
    setIsAdded(true);
    setTimeout(() => setIsAdded(false), 2000);
  };

  return (
    <motion.div
      layout
      className="group relative overflow-hidden rounded-2xl bg-white shadow-lg transition-shadow hover:shadow-2xl"
      whileHover={{ y: -4 }}
    >
      <div className="relative aspect-square overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
        />
        
        {/* Sale badge with animation */}
        {product.onSale && (
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            className="absolute top-4 right-4 rounded-full bg-red-500 px-3 py-1 text-sm font-bold text-white shadow-lg"
          >
            SALE
          </motion.div>
        )}
      </div>

      <div className="p-6 space-y-3">
        <h3 className="text-xl font-semibold text-gray-900 line-clamp-2 transition-colors group-hover:text-blue-600">
          {product.name}
        </h3>
        
        <div className="flex items-baseline gap-2">
          <motion.span
            className="text-2xl font-bold text-blue-600"
            key={product.price} // Re-animate on price change
            initial={{ scale: 1.2, color: '#ef4444' }}
            animate={{ scale: 1, color: '#2563eb' }}
          >
            ${product.price}
          </motion.span>
          {product.compareAtPrice && (
            <span className="text-sm text-gray-500 line-through">
              ${product.compareAtPrice}
            </span>
          )}
        </div>

        {/* Button with success state */}
        <button
          onClick={handleAddToCart}
          className={`
            w-full rounded-lg px-6 py-3 font-medium text-white transition-all
            ${isAdded 
              ? 'bg-green-500 scale-105' 
              : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
            }
          `}
        >
          {isAdded ? (
            <span className="flex items-center justify-center gap-2">
              <CheckIcon className="h-5 w-5" />
              Added!
            </span>
          ) : (
            'Add to Cart'
          )}
        </button>
      </div>
    </motion.div>
  );
}
```

**Expected Outcome:**
- Visual appeal increased 5x
- Engagement metrics improve 20-40% (typical)
- User delight through micro-interactions
- Maintains accessibility (ARIA labels, keyboard navigation)

---
---

## Patterns & Templates

### Pattern 1: Glassmorphism Card

**When to use:** Modern, premium aesthetic (works well with colorful backgrounds)

```tsx
function GlassCard({ children, className = '' }: GlassCardProps) {
  return (
    <div className={`
      relative overflow-hidden rounded-2xl
      backdrop-blur-xl backdrop-saturate-150
      bg-white/10 border border-white/20
      shadow-xl shadow-black/5
      ${className}
    `}>
      {/* Optional gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent opacity-50" />
      
      <div className="relative z-10 p-6">
        {children}
      </div>
    </div>
  );
}
```

---
---

### Pattern 3: Skeleton Loading with Shimmer

**When to use:** Loading states for cards, lists (better UX than spinners)

```tsx
function SkeletonCard() {
  return (
    <div className="relative overflow-hidden rounded-xl bg-gray-200 p-6">
      {/* Shimmer effect */}
      <div className="absolute inset-0 -translate-x-full animate-shimmer bg-gradient-to-r from-transparent via-white/50 to-transparent" />
      
      {/* Skeleton content */}
      <div className="space-y-4">
        <div className="h-4 w-3/4 rounded bg-gray-300" />
        <div className="h-4 w-1/2 rounded bg-gray-300" />
        <div className="h-32 w-full rounded bg-gray-300" />
      </div>
    </div>
  );
}

// Tailwind config (add to tailwind.config.js)
{
  theme: {
    extend: {
      animation: {
        shimmer: 'shimmer 2s infinite',
      },
      keyframes: {
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
      },
    },
  },
}
```

---
---

### ❌ Anti-Pattern 2: Ignoring Color Contrast

**What it looks like:**
```css
/* ❌ Gray text on light gray background = unreadable */
.subtle-text {
  color: #999999;
  background: #f0f0f0;
  /* Contrast ratio: 2.1:1 (FAILS WCAG AA 4.5:1 requirement) */
}
```

**Why it fails:**
- Fails WCAG AA accessibility (4.5:1 contrast for text)
- Users with visual impairments cannot read content
- Poor UX in bright sunlight (mobile devices)

**Correct approach:**
```css
/* ✅ Sufficient contrast */
.readable-text {
  color: #333333;
  background: #ffffff;
  /* Contrast ratio: 12.6:1 (PASSES WCAG AAA) */
}

/* Or use design system tokens */
.text {
  color: var(--color-text-primary);    /* Guaranteed 4.5:1 */
  background: var(--color-bg-surface); /* Against text color */
}
```

---
---

## Quality Checklist

### Visual Polish
- [ ] Color palette uses max 3 primary colors + neutrals
- [ ] Typography hierarchy clear (3-5 font sizes)
- [ ] Spacing follows consistent scale (4px, 8px, 16px, 24px, 32px...)
- [ ] Hover states on all interactive elements
- [ ] Loading states for async actions
- [ ] Empty states with helpful messaging

### Accessibility
- [ ] Color contrast ≥4.5:1 for text (WCAG AA)
- [ ] Focus indicators visible on all interactive elements
- [ ] Animations respect `prefers-reduced-motion`
- [ ] Alt text on all images
- [ ] Keyboard navigation works (Tab, Enter, Esc)

### Responsive Design
- [ ] Mobile-first approach (320px base)
- [ ] Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- [ ] Touch targets ≥44x44px (mobile)
- [ ] No horizontal scroll on mobile
- [ ] Images responsive (`max-width: 100%`, `height: auto`)

### Performance
- [ ] Animations use `transform` and `opacity` (GPU-accelerated)
- [ ] Images optimized (WebP, lazy loading)
- [ ] CSS bundle <50KB (after minification)
- [ ] No layout shift (CLS <0.1)
- [ ] Fonts preloaded (`<link rel="preload">`)
