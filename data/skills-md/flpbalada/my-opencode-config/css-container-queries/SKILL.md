---
name: css-container-queries
description: Apply CSS container queries for component-based responsive design. Use when implementing responsive components that adapt to their container size rather than viewport size.
---

# CSS Container Queries

A guide for implementing container-based responsive design using CSS container queries and Tailwind CSS.

## What

### What are Container Queries?

Container queries enable styling elements based on their **container's size** rather than the viewport size. Unlike media queries that respond to the browser window, container queries make components self-contained and truly reusable.

**Key Concept:**
```css
/* Define a container */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Query the container */
@container card (min-width: 400px) {
  .card-title {
    font-size: 2rem;
  }
}
```

**Tailwind Approach:**
```html
<!-- Define a container -->
<div class="@container">
  <!-- Query the container -->
  <div class="@lg:grid-cols-2">
    <!-- Content adapts to container, not viewport -->
  </div>
</div>
```

### Container Query vs Media Query

| Feature | Media Query | Container Query |
|---------|-------------|-----------------|
| Responds to | Viewport size | Container size |
| Reusability | Layout-dependent | Fully portable |
| Use case | Page layouts | Component styling |
| Syntax | `@media` | `@container` |

---

## Why

### 💡 Why Use Container Queries?

**1. Component Portability**
- Components adapt to their context, not the viewport
- Same component works in sidebar (narrow) or main area (wide)
- No need for different component variants

**2. Simpler Component Logic**
- Components don't need to know about page layout
- Follows single responsibility principle
- Reduces coupling between components and layouts

**3. Better for Design Systems**
- Components are truly self-contained
- Works in any layout context (grid, flex, sidebar)
- Easier to maintain and test in isolation

**4. Modern Web Architecture**
- Aligns with component-based frameworks (React, Vue, Svelte)
- Better for micro-frontends
- More predictable behavior

### When to Use Container Queries vs Media Queries

🤔 **Use Container Queries when:**
- Styling reusable components (cards, widgets, forms)
- Component appears in multiple contexts
- Component needs to adapt to its parent's size
- Building a component library

🤔 **Use Media Queries when:**
- Changing overall page layout
- Adjusting navigation structure
- Modifying font sizes globally
- Viewport-specific features (like mobile-first approach)

---

## Requirements

### What to Do

Review and refactor responsive components to use container queries where appropriate.

### Implementation Checklist

#### 1. CSS Implementation

**Step 1: Define the container**
```css
.component-wrapper {
  container-type: inline-size; /* or 'size' for both dimensions */
  container-name: myComponent; /* optional but recommended */
}
```

**Step 2: Add container queries**
```css
/* Use the container name */
@container myComponent (min-width: 400px) {
  .component-title {
    font-size: 2rem;
  }
}

/* Or query nearest container */
@container (min-width: 400px) {
  .component-title {
    font-size: 2rem;
  }
}
```

**Step 3: Use modern range syntax (optional)**
```css
@container (400px <= width <= 800px) {
  .component-content {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}
```

#### 3. Tailwind CSS Implementation

**Step 1: Define container with `@container` class**
```html
<div class="@container">
  <!-- This is now a container context -->
</div>
```

**Step 2: Use container query variants**
```html
<div class="@container">
  <div class="grid @lg:grid-cols-2 @xl:grid-cols-3">
    <!-- Responds to container size, not viewport -->
  </div>
</div>
```

**Available Tailwind Container Breakpoints:**
- `@3xs` - `@container (width >= 16rem)` (256px)
- `@2xs` - `@container (width >= 18rem)` (288px)
- `@xs` - `@container (width >= 20rem)` (320px)
- `@sm` - `@container (width >= 24rem)` (384px)
- `@md` - `@container (width >= 28rem)` (448px)
- `@lg` - `@container (width >= 32rem)` (512px)
- `@xl` - `@container (width >= 36rem)` (576px)
- `@2xl` - `@container (width >= 42rem)` (672px)
- `@3xl` - `@container (width >= 48rem)` (768px)
- `@4xl` - `@container (width >= 56rem)` (896px)
- `@5xl` - `@container (width >= 64rem)` (1024px)
- `@6xl` - `@container (width >= 72rem)` (1152px)
- `@7xl` - `@container (width >= 80rem)` (1280px)

**📝 Note:** These are Tailwind's default breakpoints. You can customize them in `globals.css` (Tailwind v4) using CSS variables or use arbitrary values like `@min-[500px]:grid` for custom container widths.

**Step 3: Named containers (Tailwind)**
```html
<!-- Define named container -->
<div class="@container/main">
  <!-- Query specific container -->
  <div class="@lg/main:grid-cols-3">
    <!-- Content -->
  </div>
</div>
```

#### 4. Common Patterns

**Pattern 1: Card Component**
```html
<!-- Tailwind -->
<div class="@container">
  <article class="@lg:flex @lg:gap-4">
    <img class="@lg:w-48" src="..." alt="..." />
    <div class="@lg:flex-1">
      <h2 class="text-xl @lg:text-2xl">Title</h2>
      <p class="@lg:text-base">Description</p>
    </div>
  </article>
</div>
```

**Pattern 2: Responsive Grid**
```html
<!-- Tailwind -->
<div class="@container">
  <div class="grid @sm:grid-cols-2 @lg:grid-cols-3 @2xl:grid-cols-4 gap-4">
    <!-- Items adapt to container width -->
  </div>
</div>
```

**Pattern 3: Mixed Container + Media Queries**
```html
<!-- Use media queries for layout, container queries for components -->
<main class="max-w-7xl mx-auto md:grid md:grid-cols-3">
  <!-- Sidebar: narrow container -->
  <aside class="md:col-span-1">
    <div class="@container">
      <div class="@lg:hidden">Compact view</div>
    </div>
  </aside>

  <!-- Main: wide container -->
  <div class="md:col-span-2">
    <div class="@container">
      <div class="@2xl:grid-cols-3">Full width view</div>
    </div>
  </div>
</main>
```

### 5. Review Process

✅ **Focus on:**
- Recently modified components
- Components using media queries for internal layout
- Reusable component patterns

⚠️ **Watch out for:**
- Overusing container queries (media queries are still needed for layouts)
- Nesting too many containers (can cause confusion)
- Not naming containers when multiple are present
- Fixed heights (let content flow naturally)

❌ **Avoid:**
- Replacing all media queries with container queries
- Container queries for page-level layouts
- Complex nesting without clear container names

### 6. Testing Checklist

After implementing container queries:

- [ ] Component works in narrow containers (sidebar)
- [ ] Component works in wide containers (main content)
- [ ] Component works in medium containers (grid cells)
- [ ] No layout breaks at container breakpoints
- [ ] Content doesn't overflow fixed heights
- [ ] Performance is acceptable (container queries are efficient)

### 7. Browser Support

✅ **Supported:**
- Chrome 106+
- Edge 106+
- Safari 16+
- Firefox 110+

💡 **Tip:** For older browsers, use `@supports` or progressive enhancement:

```css
/* Fallback for older browsers */
.component {
  padding: 1rem;
}

/* Enhanced with container queries */
@supports (container-type: inline-size) {
  @container (min-width: 400px) {
    .component {
      padding: 2rem;
    }
  }
}
```

---

## Examples

### ✅ Good: Component-Based Container Query

```html
<!-- Tailwind: Reusable card adapts to any container -->
<div class="@container">
  <article class="p-4 @md:p-6 @lg:flex @lg:gap-6">
    <img class="w-full @lg:w-64 rounded" src="card.jpg" alt="" />
    <div>
      <h2 class="text-lg @md:text-xl @lg:text-2xl font-bold">
        Card Title
      </h2>
      <p class="text-sm @md:text-base @lg:text-lg">
        Card description that adapts to container width.
      </p>
      <button class="mt-4 @md:mt-6">Action</button>
    </div>
  </article>
</div>
```

**Why it's good:** Card is self-contained and works in any layout context.

### ❌ Bad: Using Media Queries for Component Internals

```html
<!-- Tailwind: Component depends on viewport, not container -->
<article class="p-4 md:p-6 lg:flex lg:gap-6">
  <img class="w-full lg:w-64 rounded" src="card.jpg" alt="" />
  <div>
    <h2 class="text-lg md:text-xl lg:text-2xl font-bold">
      Card Title
    </h2>
  </div>
</article>
```

**Why it's bad:** Card assumes it's always full width at `md` breakpoint. Breaks when placed in a sidebar.

### ✅ Good: Named Containers for Clarity

```html
<!-- Tailwind: Multiple containers with clear names -->
<div class="@container/sidebar">
  <nav class="@lg/sidebar:grid-cols-1">
    <!-- Sidebar navigation -->
  </nav>
</div>

<div class="@container/main">
  <div class="@lg/main:grid-cols-3">
    <!-- Main content grid -->
  </div>
</div>
```

**Why it's good:** Clear which container each query refers to.

---

## Common Mistakes

❌ **Mistake 1: Using container queries for page layouts**
```html
<!-- Don't do this -->
<body class="@container">
  <main class="@lg:grid @lg:grid-cols-3">
```
**Fix:** Use media queries for page-level layouts.

❌ **Mistake 2: Forgetting to define the container**
```html
<!-- Don't do this -->
<div>
  <div class="@lg:grid-cols-2"><!-- Won't work! --></div>
</div>
```
**Fix:** Always add `@container` to the parent.

❌ **Mistake 3: Fixed heights with responsive content**
```css
/* Don't do this */
.container {
  height: 400px; /* Fixed height */
}

@container (min-width: 600px) {
  .content {
    columns: 2; /* Text will overflow! */
  }
}
```
**Fix:** Use `min-height` or let content determine height.

❌ **Mistake 4: Too many nested containers**
```html
<!-- Don't do this -->
<div class="@container">
  <div class="@container">
    <div class="@container">
      <div class="@lg:..."><!-- Confusing! --></div>
    </div>
  </div>
</div>
```
**Fix:** Use named containers and keep nesting shallow.

---

## Quick Reference

### Vanilla CSS

```css
/* Define container */
.wrapper {
  container-type: inline-size; /* or 'size' */
  container-name: myContainer; /* optional */
}

/* Query container */
@container myContainer (min-width: 400px) {
  /* styles */
}

/* Modern range syntax */
@container (400px <= width <= 800px) {
  /* styles */
}
```

### Tailwind CSS

```html
<!-- Define container -->
<div class="@container">
  <!-- Use container variants -->
  <div class="@sm:text-lg @md:grid-cols-2">
</div>

<!-- Named container -->
<div class="@container/name">
  <div class="@lg/name:grid-cols-3">
</div>
```

---

## Resources

- [MDN: CSS Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Container_Queries)
- [Tailwind: Container Queries](https://tailwindcss.com/docs/hover-focus-and-other-states#container-queries)
- [CSS Tricks: Container Queries Guide](https://css-tricks.com/a-primer-on-css-container-queries/)
- [Can I Use: Container Queries](https://caniuse.com/css-container-queries)
