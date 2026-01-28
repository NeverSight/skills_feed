---
name: sentry-react-setup
description: Setup Sentry in React apps. Use when asked to add Sentry to React, install @sentry/react, or configure error monitoring for React applications.
---

# Sentry React Setup

Install and configure Sentry in React projects.

## Invoke This Skill When

- User asks to "add Sentry to React" or "install Sentry" in a React app
- User wants error monitoring, logging, or tracing in React
- User mentions "@sentry/react" or React error boundaries

## Install

```bash
npm install @sentry/react --save
```

## Configure

Create `src/instrument.js` (must be imported first in your app):

```javascript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  sendDefaultPii: true,
  
  // Tracing
  integrations: [Sentry.browserTracingIntegration()],
  tracesSampleRate: 1.0,
  tracePropagationTargets: [/^\//, /^https:\/\/yourserver\.io\/api/],
  
  // Session Replay
  integrations: [Sentry.replayIntegration()],
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  
  // Logs
  enableLogs: true,
});
```

### Import First in Entry Point

```javascript
// src/index.js or src/main.jsx
import "./instrument";  // Must be first!
import App from "./App";
import { createRoot } from "react-dom/client";

const root = createRoot(document.getElementById("app"));
root.render(<App />);
```

## Error Handling

### React 19+

Use error hooks with `createRoot`:

```javascript
import { createRoot } from "react-dom/client";
import * as Sentry from "@sentry/react";

const root = createRoot(document.getElementById("app"), {
  onUncaughtError: Sentry.reactErrorHandler(),
  onCaughtError: Sentry.reactErrorHandler(),
  onRecoverableError: Sentry.reactErrorHandler(),
});
```

### React <19

Use ErrorBoundary component:

```javascript
import * as Sentry from "@sentry/react";

<Sentry.ErrorBoundary fallback={<p>An error occurred</p>}>
  <MyComponent />
</Sentry.ErrorBoundary>
```

## React Router Integration

| Router Version | Integration |
|---------------|-------------|
| v7 (non-framework) | `Sentry.reactRouterV7BrowserTracingIntegration` |
| v6 | `Sentry.reactRouterV6BrowserTracingIntegration` |
| v4/v5 | `Sentry.reactRouterV5BrowserTracingIntegration` |

## Redux Integration (Optional)

```javascript
import * as Sentry from "@sentry/react";
import { configureStore } from "@reduxjs/toolkit";

const store = configureStore({
  reducer,
  enhancers: (getDefaultEnhancers) =>
    getDefaultEnhancers().concat(Sentry.createReduxEnhancer()),
});
```

## Source Maps

Upload source maps for readable stack traces:

```bash
npx @sentry/wizard@latest -i sourcemaps
```

## Environment Variables

```bash
REACT_APP_SENTRY_DSN=https://xxx@o123.ingest.sentry.io/456
SENTRY_AUTH_TOKEN=sntrys_xxx
SENTRY_ORG=my-org
SENTRY_PROJECT=my-project
```

## Verification

Add test button to trigger error:

```javascript
<button onClick={() => { throw new Error("Sentry Test Error"); }}>
  Test Sentry
</button>
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Errors not captured | Ensure `instrument.js` is imported first |
| Source maps not working | Run sourcemaps wizard, verify auth token |
| React Router spans missing | Add correct router integration for your version |
