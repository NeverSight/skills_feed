---
name: pwa
description: Progressive Web App development guidelines covering manifest configuration, service workers, offline-first strategies, mobile optimization, and safe-area handling. Triggers on "PWA", "progressive web app", "installable app", "offline app", "service worker", "web manifest".
---

# Progressive Web App (PWA) Skill

Build installable, offline-capable web apps optimized for mobile with desktop compatibility.

## Essential HTML Head

```html
<head>
  <!-- Viewport with safe area support -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="theme-color" content="#000000">

  <!-- PWA capable -->
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="App Name">

  <!-- Manifest & Icons -->
  <link rel="manifest" href="/manifest.webmanifest">
  <link rel="apple-touch-icon" href="/apple-touch-icon-180x180.png">
</head>
```

## Web App Manifest

```json
{
  "name": "My Progressive Web App",
  "short_name": "MyPWA",
  "description": "App description",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```

### Display Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `standalone` | Native app look, no browser UI | Most apps (recommended) |
| `fullscreen` | Entire screen, no status bar | Games, immersive, VR/AR |
| `minimal-ui` | Minimal browser controls | Content needing navigation |
| `browser` | Standard browser tab | Not recommended for PWAs |

### Detect Display Mode

```css
@media (display-mode: standalone) {
  .browser-nav { display: none; }
}
```

```javascript
const isInstalled = window.matchMedia('(display-mode: standalone)').matches
  || window.navigator.standalone; // iOS
```

---

## Safe Area Handling

**Required:** `viewport-fit=cover` in viewport meta tag.

Handles notches, Dynamic Island, rounded corners on modern devices.

```css
:root {
  --safe-top: env(safe-area-inset-top, 0px);
  --safe-right: env(safe-area-inset-right, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);
  --safe-left: env(safe-area-inset-left, 0px);
}

body {
  padding: var(--safe-top) var(--safe-right) var(--safe-bottom) var(--safe-left);
}

/* Fixed header */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: calc(1rem + var(--safe-top)) calc(1rem + var(--safe-right)) 1rem calc(1rem + var(--safe-left));
}

/* Fixed bottom navigation */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.5rem var(--safe-right) calc(0.5rem + var(--safe-bottom)) var(--safe-left);
}

/* Landscape notch handling */
@media (orientation: landscape) {
  .content {
    padding-left: max(1rem, var(--safe-left));
    padding-right: max(1rem, var(--safe-right));
  }
}
```

### iOS Status Bar Styles

| Value | Effect |
|-------|--------|
| `default` | White bar, black text |
| `black` | Black bar, white text |
| `black-translucent` | Transparent, content flows behind |

---

## Service Worker

### Registration

```javascript
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(reg => console.log('SW registered:', reg.scope))
    .catch(err => console.error('SW failed:', err));
}
```

### Basic Service Worker (sw.js)

```javascript
const CACHE_NAME = 'app-v1';
const ASSETS = ['/', '/index.html', '/styles.css', '/app.js'];

// Install: cache assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate: clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch: cache-first for assets, network-first for API
self.addEventListener('fetch', event => {
  const { request } = event;

  if (request.url.includes('/api/')) {
    // Network first for API
    event.respondWith(
      fetch(request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(c => c.put(request, clone));
          return res;
        })
        .catch(() => caches.match(request))
    );
  } else {
    // Cache first for static assets
    event.respondWith(
      caches.match(request).then(cached => cached || fetch(request))
    );
  }
});
```

### Caching Strategies

| Strategy | Use Case | Behavior |
|----------|----------|----------|
| Cache First | Static assets, fonts, images | Fast, may be stale |
| Network First | API data, dynamic content | Fresh, slower |
| Stale While Revalidate | Semi-dynamic content | Fast + background update |
| Network Only | Auth, real-time data | Always fresh |

---

## Mobile Optimization

### Touch Targets

```css
/* Apple HIG: minimum 44x44px */
button, a, [role="button"] {
  min-width: 44px;
  min-height: 44px;
}
```

### Prevent iOS Input Zoom

```css
/* Font size >= 16px prevents zoom on focus */
input, select, textarea {
  font-size: 16px;
}
```

### Disable Pull-to-Refresh

```css
html {
  overscroll-behavior-y: contain;
}
```

### Native-like Touch Feedback

```css
button, a {
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation; /* Disable double-tap zoom */
}

/* Disable text selection on UI elements */
.nav, .toolbar {
  -webkit-user-select: none;
  user-select: none;
}
```

### Smooth Scrolling

```css
.scroll-container {
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior: contain;
}
```

---

## Responsive Layout

```css
/* Mobile-first */
.container {
  padding: 1rem;
  max-width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .container { max-width: 720px; margin: 0 auto; }
  .mobile-only { display: none; }
}

/* Desktop */
@media (min-width: 1024px) {
  .container { max-width: 960px; }
  .bottom-nav { display: none; }
  .sidebar { display: block; }
}
```

---

## Installation Prompt

```javascript
let deferredPrompt;

window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault();
  deferredPrompt = e;
  showInstallButton();
});

function installApp() {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  deferredPrompt.userChoice.then(result => {
    console.log('Install:', result.outcome);
    deferredPrompt = null;
  });
}

window.addEventListener('appinstalled', () => {
  console.log('App installed');
  hideInstallButton();
});
```

---

## PWA Checklist

### Required for Installation

- [ ] HTTPS (localhost allowed for dev)
- [ ] Valid manifest with `name`, `icons`, `start_url`, `display`
- [ ] 192x192 PNG icon
- [ ] 512x512 PNG icon
- [ ] Service worker with fetch handler

### Recommended

- [ ] `viewport-fit=cover` meta tag
- [ ] Safe area inset handling
- [ ] `theme_color` in manifest and meta tag
- [ ] Maskable icon (512x512 with 20% safe zone)
- [ ] Apple touch icon (180x180)
- [ ] `apple-mobile-web-app-status-bar-style` meta tag
- [ ] Offline fallback page
- [ ] Install prompt UI

### Performance

- [ ] Precache critical assets
- [ ] Lazy load non-critical resources
- [ ] Use WebP/AVIF images
- [ ] Code splitting

---

## Testing

### Lighthouse

Chrome DevTools > Lighthouse > Progressive Web App

### Manual Checks

```javascript
// Is installed?
window.matchMedia('(display-mode: standalone)').matches

// Service worker status
navigator.serviceWorker.getRegistrations()
  .then(regs => console.log('SW:', regs));

// Cache contents
caches.keys().then(names => console.log('Caches:', names));
```

### Clear PWA State

```javascript
// Unregister all service workers
navigator.serviceWorker.getRegistrations()
  .then(regs => regs.forEach(r => r.unregister()));

// Clear all caches
caches.keys().then(names => names.forEach(n => caches.delete(n)));
```

---

## Reference Files

- [reference/build-tools.md](reference/build-tools.md) - Vite, Webpack, framework-specific setup
- [reference/caching-strategies.md](reference/caching-strategies.md) - Advanced Workbox patterns
- [reference/mobile-optimization.md](reference/mobile-optimization.md) - iOS quirks, responsive patterns
