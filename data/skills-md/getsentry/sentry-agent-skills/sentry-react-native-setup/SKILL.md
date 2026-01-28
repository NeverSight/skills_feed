---
name: sentry-react-native-setup
description: Setup Sentry in React Native using the wizard CLI. Use when asked to add Sentry to React Native, install @sentry/react-native, or configure error monitoring for React Native or Expo apps.
---

# Sentry React Native Setup

Install and configure Sentry in React Native projects using the official wizard CLI.

## Invoke This Skill When

- User asks to "add Sentry to React Native" or "install Sentry" in a React Native app
- User wants error monitoring, logging, or tracing in React Native or Expo
- User mentions "@sentry/react-native" or mobile error tracking

## Wizard Setup (Recommended)

```bash
npx @sentry/wizard@latest -i reactNative
```

### What the Wizard Does

| Task | Description |
|------|-------------|
| Install SDK | Adds `@sentry/react-native` package |
| Metro config | Adds `@sentry/react-native/metro` to `metro.config.js` |
| Expo config | Adds `@sentry/react-native/expo` to `app.json` |
| Android setup | Enables Gradle build step for source maps |
| iOS setup | Wraps Xcode build phase, adds debug symbol upload |
| Pod install | Runs `pod install` for iOS |
| Credentials | Stores in `ios/sentry.properties`, `android/sentry.properties`, `.env.local` |
| Init code | Configures Sentry in `App.tsx` or `_layout.tsx` |

## Manual Configuration

If not using wizard, add to your app entry point:

```javascript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  sendDefaultPii: true,
  
  // Tracing
  tracesSampleRate: 1.0,
  
  // Logs
  enableLogs: true,
  
  // Profiling
  profilesSampleRate: 1.0,
  
  // Session Replay
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  integrations: [Sentry.mobileReplayIntegration()],
});
```

### Wrap Your App

```javascript
export default Sentry.wrap(App);
```

## Expo Projects

For Expo, follow the [Expo-specific setup](https://docs.sentry.io/platforms/react-native/manual-setup/expo/):

```bash
npx @sentry/wizard@latest -i reactNative
```

Works for both managed and bare Expo projects.

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `dsn` | Sentry DSN | Required |
| `sendDefaultPii` | Include user data | `false` |
| `tracesSampleRate` | % of transactions traced | `0` |
| `profilesSampleRate` | % of traces profiled | `0` |
| `enableLogs` | Send logs to Sentry | `false` |
| `replaysOnErrorSampleRate` | % of error sessions replayed | `0` |
| `replaysSessionSampleRate` | % of all sessions replayed | `0` |

## Files Created/Modified

| File | Purpose |
|------|---------|
| `App.js` / `_layout.tsx` | Sentry initialization |
| `metro.config.js` | Metro bundler config |
| `app.json` | Expo config (if Expo) |
| `ios/sentry.properties` | iOS build credentials |
| `android/sentry.properties` | Android build credentials |
| `.env.local` | Environment variables |

## Environment Variables

```bash
SENTRY_DSN=https://xxx@o123.ingest.sentry.io/456
SENTRY_AUTH_TOKEN=sntrys_xxx
SENTRY_ORG=my-org
SENTRY_PROJECT=my-project
```

## Verification

Add test error:

```javascript
throw new Error("My first Sentry error!");
```

Or use a test button:

```javascript
<Button title="Test Sentry" onPress={() => { throw new Error("Test"); }} />
```

## Source Maps

Source maps are automatically uploaded during build when wizard configures:
- Android: Gradle plugin
- iOS: Xcode build phase

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wizard fails | Try manual setup, check Node version |
| iOS build fails | Run `cd ios && pod install` |
| Source maps not uploading | Verify `sentry.properties` files have auth token |
| Expo errors | Ensure using compatible Expo SDK version |
| App not wrapped | Add `export default Sentry.wrap(App)` |
