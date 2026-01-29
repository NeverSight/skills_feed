---
name: mobile-migrate
description: "Add an Expo + EAS React Native mobile app to an existing web project, sharing logic, design tokens, auth, and backend integrations. Use when migrating a web codebase into a web+mobile monorepo."
---

# Mobile Migrate

Main mobile migration skill: add an Expo app to an existing web project while keeping one backend, one auth system, and shared design/logic.

## Purpose

Add a mobile app to an existing web project using:
- Expo (React Native)
- EAS Build/Submit
- Shared packages for logic, types, and design tokens

Outcome: `apps/web` + `apps/mobile` share `packages/shared`, ship to TestFlight/internal tracks fast.

## Prerequisites

- Monorepo structure exists. If not, run `/monorepo-scaffold` first.
- Node.js 22+ installed.
- `pnpm` installed and used as the workspace package manager.
- Apple Developer and Google Play Console accounts ready for store submission.

## 10-Step Workflow

### 1. Prerequisites — Ensure Monorepo Structure

Goal: standard layout before adding mobile.

```bash
pwd
pnpm -v
node -v
rg "^packages:" pnpm-workspace.yaml
ls apps packages
```

If no monorepo, invoke `/monorepo-scaffold`.

### 2. Scaffold — Create Expo App in `apps/mobile/`

Goal: boot a working Expo app inside the monorepo.

```bash
pnpm dlx create-expo-app@latest apps/mobile --template
pnpm --filter ./apps/mobile add -D typescript
pnpm --filter ./apps/mobile exec expo --version
```

Recommend Expo Router:

```bash
pnpm --filter ./apps/mobile exec expo install expo-router react-native-safe-area-context react-native-screens
```

### 3. Share — Extract Shareable Logic to `packages/shared/`

Goal: remove duplication; share types, schemas, utilities, and API clients.

```bash
mkdir -p packages/shared/src
pnpm add -w -D tsup typescript
pnpm add -w zod
```

Create minimal package scaffold, then wire workspace deps:

```bash
pnpm --filter ./apps/web add @acme/shared@workspace:*
pnpm --filter ./apps/mobile add @acme/shared@workspace:*
```

### 4. Design — Set Up NativeWind with Shared Design Tokens

Goal: mobile uses same design language, not a fork.

```bash
pnpm --filter ./apps/mobile add nativewind
pnpm --filter ./apps/mobile exec expo install react-native-reanimated react-native-safe-area-context
pnpm --filter ./apps/mobile add -D tailwindcss
```

Initialize Tailwind config and point it at shared tokens:

```bash
pnpm --filter ./apps/mobile exec tailwindcss init
```

### 5. Screens — Generate Initial Screens Mirroring Web Structure

Goal: mirror information architecture first, pixel perfection later.

```bash
mkdir -p apps/mobile/app
touch apps/mobile/app/_layout.tsx
touch apps/mobile/app/index.tsx
```

If web uses routes, map them:

```bash
rg "app/|pages/" apps/web -S
```

### 6. Auth — Integrate Authentication (Clerk SDK for Expo)

Goal: same identity system across platforms.

```bash
pnpm --filter ./apps/mobile add @clerk/clerk-expo expo-secure-store
pnpm --filter ./apps/mobile exec expo install expo-auth-session expo-web-browser
```

Add required plugins to Expo config, then verify:

```bash
pnpm --filter ./apps/mobile exec expo config --type public
```

### 7. API — Connect to Same Backend (Convex React Native Client)

Goal: mobile hits same backend and data model.

```bash
pnpm --filter ./apps/mobile add convex
pnpm --filter ./apps/mobile exec expo install react-native-get-random-values
```

If backend lives in a workspace package:

```bash
pnpm --filter ./apps/mobile add @acme/backend@workspace:*
```

### 8. Build — Configure EAS Build Profiles

Goal: deterministic builds for dev, preview, production.

```bash
pnpm --filter ./apps/mobile add -D eas-cli
pnpm --filter ./apps/mobile exec eas login
pnpm --filter ./apps/mobile exec eas build:configure
```

Generate or update `apps/mobile/eas.json` with profiles:

```bash
pnpm --filter ./apps/mobile exec eas build --platform ios --profile development
```

### 9. Submit — Generate App Store Assets + Submission Checklist

Goal: unblock store submission early (assets often bottleneck).

```bash
pnpm --filter ./apps/mobile exec expo install expo-application
pnpm --filter ./apps/mobile exec expo config --type public
pnpm --filter ./apps/mobile exec eas submit --platform ios --profile production
```

Also generate a checklist doc:

```bash
mkdir -p docs/mobile
touch docs/mobile/submission-checklist.md
```

### 10. Verify — Test on Simulators + Ship Test Builds

Goal: prove mobile works end-to-end before polishing.

```bash
pnpm --filter ./apps/mobile exec expo start --clear
pnpm --filter ./apps/mobile exec expo run:ios
pnpm --filter ./apps/mobile exec expo run:android
pnpm --filter ./apps/mobile exec eas build --platform all --profile preview
```

Then distribute:
- iOS: TestFlight build
- Android: internal testing track build

## Automation vs Manual

What can be automated:
- Monorepo scaffolding, Expo scaffolding, workspace wiring
- Shared package extraction and dependency alignment
- NativeWind setup and design token plumbing
- EAS configuration, build profiles, preview builds
- Route/screen scaffolding that mirrors web structure
- Basic auth and backend client integration wiring

What must be manual (or human-supervised):
- App naming, bundle identifiers, and store metadata
- Apple/Google account setup, certificates, legal agreements
- Final UX decisions, platform-specific flows, accessibility polish
- Store listings: screenshots, marketing copy, privacy disclosures
- Submission steps, review responses, release coordination

## Verification Strategy (Specific Checks)

Run these checks in order:

1. Workspace integrity:

```bash
pnpm -w install
pnpm -w list --depth 0
```

2. Type safety across shared code:

```bash
pnpm -w typecheck || pnpm -w exec tsc -b --pretty false
```

3. Expo config sanity:

```bash
pnpm --filter ./apps/mobile exec expo config --type public
pnpm --filter ./apps/mobile exec expo doctor
```

4. Runtime smoke tests:

```bash
pnpm --filter ./apps/mobile exec expo start --clear
```

Validate manually:
- App launches on iOS simulator.
- App launches on Android emulator.
- Auth sign-in works end-to-end.
- Core read flows hit backend successfully.
- One write/mutation works.
- Shared validation/types behave same as web.

5. Build pipeline smoke tests:

```bash
pnpm --filter ./apps/mobile exec eas build --platform ios --profile preview
pnpm --filter ./apps/mobile exec eas build --platform android --profile preview
```

## Common Pitfalls

- Adding Expo into a non-monorepo or half-monorepo layout.
- Duplicating logic instead of extracting to `packages/shared`.
- Sharing UI components directly instead of sharing tokens + primitives.
- Web-only dependencies leaking into shared packages.
- Not aligning TypeScript config paths across apps and packages.
- Missing native config/plugins for auth, deep links, or secure storage.
- Treating EAS config as an afterthought; it becomes the release bottleneck.
- Late discovery of store requirements (privacy, assets, identifiers).
- Testing only via Expo Go when a dev client or native build is required.

## Execution Notes

Heuristics:
- Extract logic first, then replicate screens.
- Share schemas, types, and clients; avoid sharing heavy UI.
- Keep `@acme/shared` deep, with a small, intention-revealing API.
- Prefer boring, deterministic build + submission plumbing early.

Definition of done (minimum viable migration):
- Mobile app boots in simulator.
- Uses same auth provider.
- Reads and writes to same backend.
- Shares core types/validation with web.
- Produces preview EAS builds for both platforms.
