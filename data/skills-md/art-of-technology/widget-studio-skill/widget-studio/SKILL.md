---
name: widget-studio
description: Integrates Widget Studio SDK into web projects. Supports HTML, React, Next.js, Shopify, and WordPress. Use this skill when the user wants to add Widget Studio, WidgetX, or widget-studio.weez.boo to their project.
---

# Widget Studio Integration

This skill helps you integrate Widget Studio SDK into web projects.

## Prerequisites

Before starting the integration, you MUST ask the user for their **Site Key**. This is a required public key that looks like: `site_01702db01234588145cb48be580d575`

**Always ask:** "What is your Widget Studio site key?"

## ⚠️ CRITICAL: Code Implementation Rules

**DO NOT SUMMARIZE OR PARAPHRASE THE CODE SNIPPETS.**

When implementing Widget Studio integration:

1. **Copy code exactly as shown** - Do not simplify, shorten, or "optimize" the code examples
2. **Include ALL parts** - Every line in the code snippets is intentional and required
3. **Preserve structure** - Keep the exact formatting, variable names, and initialization patterns
4. **No shortcuts** - Do not skip the double-init prevention logic for Shopify/WordPress
5. **No "equivalent" alternatives** - Use the exact patterns provided, not similar approaches

### Why This Matters

- The SDK initialization order is specific and tested
- The `__widgetx_inited` flag prevents real production bugs
- TypeScript declarations must be exact for proper type checking
- Script loading strategies (`async`, `afterInteractive`) are performance-optimized

### ❌ DON'T DO THIS:
- "Here's a simplified version..."
- "You can also just add..."
- "A shorter approach would be..."
- Omitting the cleanup function in React
- Skipping TypeScript type declarations
- Removing the polling logic (`setTimeout(init, 50)`)

### ✅ DO THIS:
- Copy the complete code block for the detected project type
- Replace ONLY `YOUR_SITE_KEY` with the actual key
- Keep all comments and structure intact

## Project Detection

Detect the project type by checking for these files:

| Project Type | Detection Method |
|--------------|------------------|
| **Next.js** | `next.config.js`, `next.config.ts`, or `next.config.mjs` exists |
| **React** | `package.json` contains `react` dependency (but no Next.js) |
| **WordPress** | `functions.php` exists or `wp-content` directory present |
| **Shopify** | `theme.liquid` exists or `.shopify` directory present |
| **HTML** | `.html` files present without framework indicators |

## Integration Instructions

### HTML Projects

Add this code just before the closing `</body>` tag:

```html
<script src="https://widget-studio.weez.boo/sdk/index.global.js"></script>
<script>
  WidgetX.init({
    siteKey: 'YOUR_SITE_KEY'
  })
</script>
```

### React Projects

Add this to your main `App.tsx` or `App.jsx`:

```tsx
import { useEffect } from 'react'

function App() {
  useEffect(() => {
    const script = document.createElement('script')
    script.src = 'https://widget-studio.weez.boo/sdk/index.global.js'
    script.async = true
    script.onload = () => {
      window.WidgetX?.init({
        siteKey: 'YOUR_SITE_KEY',
      })
    }
    document.body.appendChild(script)

    return () => {
      document.body.removeChild(script)
    }
  }, [])

  return <>{/* Your app content */}</>
}

export default App
```

If the project uses TypeScript, also add this type declaration to a `.d.ts` file or at the top of the component:

```typescript
declare global {
  interface Window {
    WidgetX?: {
      init: (config: { siteKey: string }) => void
    }
  }
}
```

### Next.js Projects (App Router)

Add this code to app/layout.tsx. If that file is not a client-side component (doesn't have 'use client' directive), find the first global layout file in your app that is client-side and add the code there instead.

```tsx
'use client'
import Script from 'next/script'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <Script
          src="https://widget-studio.weez.boo/sdk/index.global.js"
          strategy="afterInteractive"
          onLoad={() => {
            window.WidgetX?.init({
              siteKey: 'YOUR_SITE_KEY',
            })
          }}
        />
      </body>
    </html>
  )
}
```

### Next.js Projects (Pages Router)

Add this to `pages/_app.tsx`:

```tsx
import Script from 'next/script'
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Component {...pageProps} />
      <Script
        src="https://widget-studio.weez.boo/sdk/index.global.js"
        strategy="afterInteractive"
        onLoad={() => {
          window.WidgetX?.init({
            siteKey: 'YOUR_SITE_KEY',
          })
        }}
      />
    </>
  )
}
```

### Shopify Projects

Add this code to `theme.liquid`, just before `</body>`:

Location: **Online Store > Themes > Edit code > Layout > theme.liquid**

```html
<script async src="https://widget-studio.weez.boo/sdk/index.global.js"></script>
<script>
  (function () {
    if (window.__widgetx_inited) return;
    window.__widgetx_inited = true;

    function init() {
      if (!window.WidgetX) return setTimeout(init, 50);

      window.WidgetX.init({
        siteKey: 'YOUR_SITE_KEY',
      });
    }

    init();
  })();
</script>
```

### WordPress Projects

Add this code to `functions.php`:

```php
<?php
add_action('wp_enqueue_scripts', function () {
  wp_enqueue_script(
    'widgetx-sdk',
    'https://widget-studio.weez.boo/sdk/index.global.js',
    array(),
    null,
    true
  );

  $inline = <<<JS
(function () {
  if (window.__widgetx_inited) return;
  window.__widgetx_inited = true;

  function init() {
    if (!window.WidgetX) return setTimeout(init, 50);

    window.WidgetX.init({
      siteKey: "YOUR_SITE_KEY",
    });
  }

  init();
})();
JS;

  wp_add_inline_script('widgetx-sdk', $inline, 'after');
});
```

## Important Notes

1. **Replace `YOUR_SITE_KEY`** with the user's actual site key in all code snippets
2. The SDK URL is always: `https://widget-studio.weez.boo/sdk/index.global.js`
3. For Shopify and WordPress, the double-init prevention (`__widgetx_inited`) is important to avoid issues with theme reloads
4. Always load the script with `async` attribute when possible for better performance
