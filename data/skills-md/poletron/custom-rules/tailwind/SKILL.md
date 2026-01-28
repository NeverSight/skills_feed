---
name: tailwind
description: >
  Tailwind CSS utility-first patterns and best practices.
  Trigger: When styling with Tailwind CSS utility classes.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with tailwind"

## When to Use

Use this skill when:
- Styling with Tailwind CSS
- Building responsive layouts
- Creating component variants
- Optimizing CSS bundle size

---

## Critical Patterns

### Responsive Design (REQUIRED)

```html
<!-- ✅ ALWAYS: Mobile-first approach -->
<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- Full width on mobile, half on medium, third on large -->
</div>
```

### Component Extraction (REQUIRED)

```jsx
// ✅ ALWAYS: Extract repeated patterns to components
function Button({ variant = "primary", children }) {
  const base = "px-4 py-2 rounded font-medium transition";
  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
  };
  
  return (
    <button className={`${base} ${variants[variant]}`}>
      {children}
    </button>
  );
}
```

### Dark Mode (REQUIRED)

```html
<!-- ✅ Use dark: prefix for dark mode -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Content
</div>
```

---

## Decision Tree

```
Need spacing?              → Use p-*, m-*, gap-*
Need sizing?               → Use w-*, h-*, max-w-*
Need colors?               → Use bg-*, text-*, border-*
Need responsive?           → Use sm:, md:, lg:, xl:
Need states?               → Use hover:, focus:, active:
Need animations?           → Use animate-*, transition-*
```

---

## Commands

```bash
npx tailwindcss init -p    # Initialize with PostCSS
npx tailwindcss -o output.css --minify  # Build for production
```
