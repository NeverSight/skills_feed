---
name: telegram-mini-apps-react
description: Comprehensive guide for creating Telegram Mini Apps with React using @tma.js/sdk-react. Covers SDK initialization, component mounting, signals, theming, back button handling, viewport management, init data, deep linking, and environment mocking for development. Use when building or debugging Telegram Mini Apps with React.
metadata:
  author: Courtix Team, NailorSH
  version: "1.0"
  source: https://docs.telegram-mini-apps.com
---

# Telegram Mini Apps with React

This skill provides comprehensive guidance for building Telegram Mini Apps using React and the `@tma.js/sdk-react` package.

## Overview

Telegram Mini Apps are web applications displayed inside Telegram's WebView. They integrate with Telegram's native UI components (Back Button, Main Button) and have access to user data, theme parameters, and platform-specific features.

**Key concepts:**
- Mini Apps are add-ons for Telegram Bots
- They run inside Telegram's WebView
- They communicate with Telegram client via events and methods
- They have access to launch parameters, init data, and theme settings

## Quick Start

### 1. Installation

```bash
# For React projects, install the React-specific package
pnpm i @tma.js/sdk-react

# DO NOT install both @tma.js/sdk and @tma.js/sdk-react - this causes bugs!
```

> **Important:** The `@tma.js/sdk-react` package fully re-exports `@tma.js/sdk`, so you don't need to install them separately.

### 2. Create New Project (Optional)

```bash
pnpm dlx @tma.js/create-mini-app@latest
# or
npx @tma.js/create-mini-app@latest
```

This CLI scaffolds a complete project with proper configuration.

## Project Structure

A typical Telegram Mini App React project structure:

```
src/
├── main.tsx          # Entry point - SDK initialization
├── init.ts           # SDK configuration and component mounting
├── mockEnv.ts        # Development environment mocking
├── App.tsx           # Main React app with routing
├── components/
│   ├── Page.tsx      # Page wrapper with back button handling
│   └── EnvUnsupported.tsx  # Fallback for non-TG environments
├── hooks/
│   └── useDeeplink.ts      # Deep linking handler
└── services/
    └── analytics.ts        # Analytics with user data
```

## Core Concepts

### SDK Initialization

The SDK must be initialized before using any features. See [references/init.md](references/init.md) for detailed implementation.

```typescript
import { 
  init as initSDK,
  setDebug,
  themeParams,
  miniApp,
  viewport,
  backButton,
  swipeBehavior,
  initData
} from '@tma.js/sdk-react';

export async function init(options: {
  debug: boolean;
  eruda: boolean;
  mockForMacOS: boolean;
}): Promise<void> {
  // Enable debug mode for development
  setDebug(options.debug);
  
  // Initialize the SDK (REQUIRED before using any features)
  initSDK();

  // Mount components you'll use in the app
  backButton.mount.ifAvailable();
  initData.restore();

  // Configure swipe behavior
  if (swipeBehavior.isSupported()) {
    swipeBehavior.mount();
    swipeBehavior.disableVertical();
  }

  // Setup Mini App theming
  if (miniApp.mount.isAvailable()) {
    themeParams.mount();
    miniApp.mount();
    themeParams.bindCssVars();  // Binds theme to CSS variables
  }

  // Configure viewport
  if (viewport.mount.isAvailable()) {
    viewport.mount().then(() => {
      viewport.bindCssVars();
      viewport.requestFullscreen();
    });
  }
}
```

### Entry Point (main.tsx)

```typescript
import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { retrieveLaunchParams } from '@tma.js/sdk-react';
import { init } from './init';
import App from "./App";
import { EnvUnsupported } from "./components/EnvUnsupported";

// Mock environment for local development
import './mockEnv';

const root = ReactDOM.createRoot(document.getElementById('root')!);

try {
  const launchParams = retrieveLaunchParams();
  const { tgWebAppPlatform: platform } = launchParams;
  const debug = (launchParams.tgWebAppStartParam || '').includes('debug')
    || import.meta.env.DEV;

  await init({
    debug,
    eruda: debug && ['ios', 'android'].includes(platform),
    mockForMacOS: platform === 'macos',
  }).then(() => {
    root.render(
      <StrictMode>
        <App/>
      </StrictMode>,
    );
  });
} catch (e) {
  // Show fallback UI when not in Telegram
  root.render(<EnvUnsupported/>);
}
```

### Using Back Button

The Back Button is a native Telegram UI element that appears in the header.

```typescript
import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { backButton, miniApp } from '@tma.js/sdk-react';

export function Page({ children, back = true }) {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (back) {
      backButton.show();
      
      // onClick returns a cleanup function
      return backButton.onClick(() => {
        const isDeeplink = location.state?.fromDeeplink;
        const isFirstPage = !window.history.state || window.history.state.idx === 0;

        if (isDeeplink || isFirstPage) {
          miniApp.close();  // Close the Mini App
        } else {
          navigate(-1);     // Go back in history
        }
      });
    }
    
    backButton.hide();
  }, [back, navigate, location]);

  return <>{children}</>;
}
```

### Using Signals (useSignal Hook)

Signals are reactive values that update automatically. Use `useSignal` to subscribe to them in React:

```typescript
import { useEffect } from 'react';
import { backButton, useSignal } from '@tma.js/sdk-react';

function BackButtonStatus() {
  const isVisible = useSignal(backButton.isVisible);

  useEffect(() => {
    console.log('Back button is', isVisible ? 'visible' : 'hidden');
  }, [isVisible]);

  return null;
}
```

### Getting Init Data (User Info)

Init data contains user information and can be used for authentication:

```typescript
import { initData } from '@tma.js/sdk-react';

function getUserId(): number | undefined {
  try {
    const user = initData.user();
    return user?.id;
  } catch (e) {
    return undefined;
  }
}

// Get start parameter (for deep linking)
const startParam = initData.startParam();
```

### Launch Parameters

Launch parameters contain platform info, theme, and app data:

```typescript
import { retrieveLaunchParams, useLaunchParams } from '@tma.js/sdk-react';

// In component
function Component() {
  const launchParams = useLaunchParams();
  // launchParams.tgWebAppPlatform - 'ios', 'android', 'macos', 'tdesktop', 'web', 'weba'
  // launchParams.tgWebAppVersion - SDK version supported by client
  // launchParams.tgWebAppData - init data
  // launchParams.tgWebAppThemeParams - theme colors
  // launchParams.tgWebAppStartParam - custom start parameter
}

// Outside component
const launchParams = retrieveLaunchParams();
```

### Theming

Theme parameters are automatically provided by Telegram. Bind them to CSS variables:

```typescript
import { themeParams, miniApp } from '@tma.js/sdk-react';

// During initialization
if (miniApp.mount.isAvailable()) {
  themeParams.mount();
  miniApp.mount();
  themeParams.bindCssVars();  // Creates CSS variables like --tg-theme-bg-color
}
```

**Available CSS variables after binding:**
- `--tg-theme-bg-color`
- `--tg-theme-text-color`
- `--tg-theme-hint-color`
- `--tg-theme-link-color`
- `--tg-theme-button-color`
- `--tg-theme-button-text-color`
- `--tg-theme-secondary-bg-color`
- `--tg-theme-header-bg-color`
- `--tg-theme-accent-text-color`
- `--tg-theme-section-bg-color`
- `--tg-theme-section-header-text-color`
- `--tg-theme-subtitle-text-color`
- `--tg-theme-destructive-text-color`

### Viewport and Safe Areas

Handle viewport and safe areas for proper layout:

```typescript
import { viewport } from '@tma.js/sdk-react';

if (viewport.mount.isAvailable()) {
  viewport.mount().then(() => {
    viewport.bindCssVars();        // Binds viewport dimensions to CSS
    viewport.requestFullscreen();   // Request fullscreen mode
  });
}
```

**Available CSS variables:**
```css
/* Safe area insets */
padding-top: var(--tg-viewport-safe-area-inset-top, 0);
padding-bottom: var(--tg-viewport-safe-area-inset-bottom, 0);

/* Content safe area (for notch, etc.) */
padding-top: var(--tg-viewport-content-safe-area-inset-top, 0);

/* Viewport dimensions */
height: var(--tg-viewport-height);
width: var(--tg-viewport-width);
```

**Usage in CSS:**
```css
.header {
  padding-top: max(2rem, calc(var(--tg-viewport-content-safe-area-inset-top, 0) + var(--tg-viewport-safe-area-inset-top, 0)));
}

.footer {
  padding-bottom: calc(1rem + var(--tg-viewport-safe-area-inset-bottom, 0));
}
```

## Development Environment Mocking

For local development outside Telegram, mock the environment. See [references/mock-env.md](references/mock-env.md).

```typescript
import { emitEvent, isTMA, mockTelegramEnv } from '@tma.js/sdk-react';

if (import.meta.env.DEV) {
  if (!await isTMA('complete')) {
    const themeParams = {
      accent_text_color: '#6ab2f2',
      bg_color: '#17212b',
      button_color: '#5288c1',
      button_text_color: '#ffffff',
      destructive_text_color: '#ec3942',
      header_bg_color: '#17212b',
      hint_color: '#708499',
      link_color: '#6ab3f3',
      secondary_bg_color: '#232e3c',
      section_bg_color: '#17212b',
      section_header_text_color: '#6ab3f3',
      subtitle_text_color: '#708499',
      text_color: '#f5f5f5',
    };

    mockTelegramEnv({
      onEvent(e) {
        if (e.name === 'web_app_request_theme') {
          return emitEvent('theme_changed', { theme_params: themeParams });
        }
        if (e.name === 'web_app_request_viewport') {
          return emitEvent('viewport_changed', {
            height: window.innerHeight,
            width: window.innerWidth,
            is_expanded: true,
            is_state_stable: true,
          });
        }
        if (e.name === 'web_app_request_safe_area') {
          return emitEvent('safe_area_changed', { left: 0, top: 0, right: 0, bottom: 0 });
        }
      },
      launchParams: new URLSearchParams([
        ['tgWebAppThemeParams', JSON.stringify(themeParams)],
        ['tgWebAppData', new URLSearchParams([
          ['auth_date', (Date.now() / 1000 | 0).toString()],
          ['hash', 'mock-hash'],
          ['signature', 'mock-signature'],
          ['user', JSON.stringify({ id: 1, first_name: 'Developer' })],
        ]).toString()],
        ['tgWebAppVersion', '8.4'],
        ['tgWebAppPlatform', 'tdesktop'],
      ]),
    });

    console.info('⚠️ Running in mocked Telegram environment');
  }
}
```

## Deep Linking

Handle start parameters for deep linking. See [references/deeplink.md](references/deeplink.md).

```typescript
import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { initData } from "@tma.js/sdk-react";

export function useDeeplink() {
  const navigate = useNavigate();
  const processedRef = useRef(false);

  useEffect(() => {
    if (processedRef.current) return;

    const startParam = initData.startParam();
    if (!startParam) return;

    processedRef.current = true;

    try {
      // startParam is base64url encoded
      const base64 = startParam.replace(/-/g, '+').replace(/_/g, '/');
      const decoded = atob(base64);
      const params = new URLSearchParams(decoded);
      
      const route = params.get('route');
      if (route) {
        navigate(route, { replace: true, state: { fromDeeplink: true } });
      }
    } catch (e) {
      console.error("Failed to parse startParam:", e);
    }
  }, [navigate]);
}
```

## Best Practices

### 1. Always Check Availability

Before using any method, check if it's available:

```typescript
import { backButton } from '@tma.js/sdk-react';

// Option 1: Check before calling
if (backButton.show.isAvailable()) {
  backButton.show();
}

// Option 2: Call only if available (safer, no-op if unavailable)
backButton.show.ifAvailable();

// Option 3: Mount only if available
backButton.mount.ifAvailable();
```

### 2. Mount Components Before Use

Components must be mounted before their methods can be used:

```typescript
// ❌ Wrong - will throw error
backButton.show();

// ✅ Correct
backButton.mount();
backButton.show();
```

### 3. Handle macOS Bugs

Telegram for macOS has known issues:

```typescript
if (platform === 'macos') {
  mockTelegramEnv({
    onEvent(event, next) {
      if (event.name === 'web_app_request_theme') {
        const tp = themeParams.state() || retrieveLaunchParams().tgWebAppThemeParams;
        return emitEvent('theme_changed', { theme_params: tp });
      }
      if (event.name === 'web_app_request_safe_area') {
        return emitEvent('safe_area_changed', { left: 0, top: 0, right: 0, bottom: 0 });
      }
      next();
    },
  });
}
```

### 4. Don't Install Duplicate SDKs

Never install both `@tma.js/sdk` and `@tma.js/sdk-react`:

```json
// ❌ Wrong - causes bugs
{
  "dependencies": {
    "@tma.js/sdk": "^3.0.0",
    "@tma.js/sdk-react": "^3.0.8"
  }
}

// ✅ Correct - only the React package
{
  "dependencies": {
    "@tma.js/sdk-react": "^3.0.8"
  }
}
```

### 5. Disable Swipe When Needed

Prevent accidental navigation:

```typescript
if (swipeBehavior.isSupported()) {
  swipeBehavior.mount();
  swipeBehavior.disableVertical();  // Prevents swipe-to-close
}
```

## Sending Init Data to Server

For authentication, send init data to your server:

```typescript
import { retrieveRawInitData } from '@tma.js/sdk-react';

const initDataRaw = retrieveRawInitData();

fetch('https://api.example.com/auth', {
  method: 'POST',
  headers: {
    Authorization: `tma ${initDataRaw}`,
  },
});
```

**Server-side validation:**
- Use `@tma.js/init-data-node` for Node.js
- Validate the hash using your bot token
- Never trust init data without validation

## Supported Platforms

Mini Apps work on:
- **android** - Telegram for Android
- **ios** - Telegram for iOS  
- **macos** - Telegram for macOS (has some bugs)
- **tdesktop** - Telegram Desktop
- **weba** - Telegram Web A
- **web** - Telegram Web K

## Common Issues

### SDK not initialized error
Make sure to call `init()` before using any SDK features.

### Component not mounted error
Mount the component before calling its methods:
```typescript
backButton.mount();
backButton.show();
```

### Method not available error
Check availability before calling:
```typescript
if (backButton.show.isAvailable()) {
  backButton.show();
}
```

### App crashes outside Telegram
Use environment mocking during development and provide a fallback UI.

## Additional Resources

- [Official Documentation](https://docs.telegram-mini-apps.com)
- [@tma.js/sdk-react Package](https://docs.telegram-mini-apps.com/packages/tma-js-sdk-react)
- [@tma.js/sdk Package](https://docs.telegram-mini-apps.com/packages/tma-js-sdk)
- [Platform Overview](https://docs.telegram-mini-apps.com/platform/about)
- [Init Data Validation](https://docs.telegram-mini-apps.com/platform/init-data)
- [Theming](https://docs.telegram-mini-apps.com/platform/theming)

## See Also

- [references/init.md](references/init.md) - Full initialization example
- [references/mock-env.md](references/mock-env.md) - Environment mocking
- [references/deeplink.md](references/deeplink.md) - Deep linking implementation
- [examples/page-component.tsx](examples/page-component.tsx) - Page wrapper with back button
