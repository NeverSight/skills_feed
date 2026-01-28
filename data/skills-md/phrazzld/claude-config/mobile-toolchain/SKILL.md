---
name: mobile-toolchain
description: "Apply modern mobile development toolchain patterns: Expo (default), React Native, Tauri for iOS/Android apps. Use when building mobile applications, choosing cross-platform frameworks, or discussing mobile architecture."
---

# Mobile Toolchain

Modern cross-platform mobile development with TypeScript, focusing on React Native ecosystem and emerging alternatives.

## Recommended Stack: Expo (Default)

**Why Expo (2025):**
- Fastest setup to production (minutes, not days)
- Managed workflow (no Xcode/Android Studio for most use cases)
- OTA updates (deploy fixes without app store approval)
- EAS Build (cloud builds for iOS/Android)
- Excellent DX with hot reload and debugging
- Large ecosystem of quality libraries

```bash
# Create new Expo app
npx create-expo-app my-app --template

# Start development
cd my-app
npm run ios     # iOS simulator
npm run android # Android emulator
npm run web     # Web (bonus!)
```

### When to Use Expo
✅ MVPs and startups (fastest time-to-market)
✅ Standard mobile features (camera, GPS, notifications)
✅ Teams without native development experience
✅ Projects needing OTA updates
✅ Cross-platform web+mobile

### Expo Limitations
⚠️ Can't use arbitrary native modules (must use Expo SDK or create custom dev client)
⚠️ Reliant on Expo services for builds (EAS)
⚠️ Slightly larger app bundles than pure native

## Alternative: React Native (Bare Workflow)

**When to use:**
- Need custom native modules not in Expo SDK
- Require deep platform-specific customization
- Have native development expertise in-house
- Very large apps where bundle size critical

```bash
# Create React Native app
npx @react-native-community/cli init MyApp --template react-native-template-typescript

# Requires Xcode (Mac) and Android Studio setup
```

### React Native Setup Requirements
- **iOS**: Xcode 16+, CocoaPods, macOS only
- **Android**: Android Studio, Java JDK, Android SDK

## Emerging: Tauri for Mobile

**Experimental (2025) - Very lightweight alternative:**
- Uses OS WebView (extremely small bundles)
- Rust backend (security + performance)
- Web technologies for UI (React, Vue, Svelte, etc.)
- Still maturing for mobile (Tauri 2.0+)

```bash
# Create Tauri mobile app
npm create tauri-app@latest
```

### When to Consider Tauri
✅ Extremely small app size critical (<5MB)
✅ Team has Rust expertise
✅ Web-first app with mobile version
⚠️ Smaller ecosystem than React Native
⚠️ Less battle-tested on mobile

## Toolchain Comparison

| | Expo | React Native | Tauri Mobile |
|---|---|---|---|
| **Setup Time** | Minutes | Hours | Hours |
| **Native Access** | Expo SDK | Full | WebView APIs |
| **Bundle Size** | ~50MB | ~40MB | ~3-5MB |
| **OTA Updates** | Built-in | Manual | Limited |
| **Ecosystem** | Large | Largest | Growing |
| **Learning Curve** | Low | Medium | High (Rust) |
| **Native Skills Required** | None | Some | Some |

## Project Structure (Expo)

```
my-app/
├── app/                  # App Router (file-based routing)
│   ├── (tabs)/          # Tab navigator
│   │   ├── index.tsx    # Home screen
│   │   └── settings.tsx # Settings screen
│   ├── _layout.tsx      # Root layout
│   └── +not-found.tsx   # 404 screen
├── components/          # Reusable components
├── hooks/              # Custom hooks
├── constants/          # Colors, sizes, etc.
├── assets/             # Images, fonts
├── app.json            # Expo configuration
└── package.json
```

## Essential Libraries

```bash
# Navigation (built-in with Expo Router)
# Already included

# State Management
npm install zustand

# Forms
npm install react-hook-form zod

# API Calls
npm install @tanstack/react-query

# Icons
npm install @expo/vector-icons

# Styling
npm install nativewind  # Tailwind for React Native
npx expo install tailwindcss
```

## Testing Strategy

```bash
# Unit Testing
npm install --save-dev jest @testing-library/react-native

# E2E Testing
npm install --save-dev detox
```

**Jest configuration:**
```javascript
// jest.config.js
module.exports = {
  preset: 'jest-expo',
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg)'
  ],
}
```

## Quality Gates Integration

```yaml
# .github/workflows/mobile-ci.yml
name: Mobile CI

on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx expo prebuild --platform ios
      - run: npx expo run:ios --configuration Release

  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx expo prebuild --platform android
      - run: npx expo run:android --variant release
```

## EAS Build & Deploy

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Configure project
eas build:configure

# Build for both platforms
eas build --platform all

# Submit to app stores
eas submit --platform ios
eas submit --platform android
```

**eas.json:**
```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "android": { "buildType": "apk" }
    },
    "production": {
      "distribution": "store"
    }
  }
}
```

## Monorepo Integration

Use monorepo when mobile must share code with web (design system, types, API clients, business logic). Prefer single repo over copy-paste.

**Setup + migration:**
- For greenfield monorepo setup, use `/monorepo-scaffold`
- For existing app migration, use `/mobile-migrate`
- See `/mobile-migrate` skill for complete migration workflow

**Key monorepo considerations:**
- Metro needs workspace visibility:
  - Configure `metro.config.js` `watchFolders` to include repo root and shared packages
  - Ensure Metro resolves workspace symlinks (Expo docs patterns)
- Workspace references must be explicit:
  - Use package manager workspaces (`workspace:*` or equivalent)
  - Avoid relative `../shared` imports between apps
- Standard shared packages layout:
  - `packages/shared` for types, utils, API clients
  - `packages/ui` for cross-platform components/tokens
  - Keep mobile-only modules out of shared packages
- TypeScript must agree with bundler:
  - Add path aliases for shared packages in root `tsconfig`
  - Mirror aliases in Babel/Metro resolver settings
  - Export stable entrypoints from shared packages

## OTA Updates

```bash
# Publish update (no app store review needed for JS/assets)
eas update --branch production --message "Fix login bug"

# Users get update on next app launch
```

## Performance Best Practices

- Use `React.memo()` for expensive components
- Implement `FlatList` with `getItemLayout` for known sizes
- Avoid inline functions in render
- Use Hermes JS engine (default in Expo 50+)
- Lazy load screens with `React.lazy()` + `Suspense`
- Optimize images with `expo-image`

## Native Module Integration

```typescript
// Using Expo Modules API
import * as Camera from 'expo-camera'
import * as Location from 'expo-location'
import * as Notifications from 'expo-notifications'

// Request permissions
const { status } = await Camera.requestCameraPermissionsAsync()
const location = await Location.getCurrentPositionAsync()
await Notifications.scheduleNotificationAsync({
  content: { title: 'Hello!' },
  trigger: { seconds: 60 },
})
```

## Recommendation Flow

```
New mobile project:
├─ Standard features, fast launch → Expo ✅
├─ Need custom native code → React Native (bare)
└─ Tiny bundle size critical → Tauri (experimental)

Existing React Native project:
└─ Consider migrating to Expo (easier than you think!)
```

When agents design mobile apps, they should:
- Default to Expo for new projects (fastest, best DX)
- Use Expo Router for navigation (file-based routing)
- Apply quality-gates skill for testing/CI setup
- Use React Native Paper or NativeBase for UI components
- Integrate structured-logging skill for error tracking
- Plan OTA update strategy from the start
- Support both iOS and Android unless explicitly single-platform
