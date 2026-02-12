---
name: maestro-e2e
description: E2E UI testing with Maestro for iOS, Android, Flutter, React Native, and Web
metadata:
  tags: maestro, e2e, testing, ui, automation, flutter, react-native, ios, android, web
---

## When to use

Use this skill whenever you are:

- Creating E2E, UI, or integration tests
- Testing login, registration, or navigation flows
- Handling permission dialogs (camera, location, notifications)
- Debugging test failures or exploring UI hierarchy
- Working with Maestro test files (.yaml)

## Captions

When dealing with native permission dialogs, load the [./rules/permissions.md](./rules/permissions.md) file for platform-specific information.

When working with Flutter apps, load the [./rules/platforms/flutter.md](./rules/platforms/flutter.md) file for Semantics patterns.

## How to use

Read individual rule files for detailed explanations and code examples:

### Core

- [rules/installation.md](rules/installation.md) - Installing Maestro on macOS, Linux, and Windows
- [rules/test-structure.md](rules/test-structure.md) - YAML test structure, appId, env variables, and flow definition
- [rules/commands.md](rules/commands.md) - Complete reference of 40+ Maestro commands
- [rules/selectors.md](rules/selectors.md) - Element targeting with id, text, index, and matchers
- [rules/assertions.md](rules/assertions.md) - assertVisible, assertNotVisible, assertTrue, and AI assertions
- [rules/interactions.md](rules/interactions.md) - tapOn, inputText, scroll, swipe, and gesture commands
- [rules/permissions.md](rules/permissions.md) - iOS vs Android permission configuration and dialog handling

### Platforms

- [rules/platforms/android.md](rules/platforms/android.md) - Android-specific: ADB, permission dialogs, emulators
- [rules/platforms/ios.md](rules/platforms/ios.md) - iOS-specific: auto-dismiss dialogs, simulators, limitations
- [rules/platforms/flutter.md](rules/platforms/flutter.md) - Flutter integration using Semantics and identifier
- [rules/platforms/react-native.md](rules/platforms/react-native.md) - React Native with testID and accessibilityLabel
- [rules/platforms/web.md](rules/platforms/web.md) - Desktop browser testing with Chromium

### Advanced

- [rules/advanced/parameters.md](rules/advanced/parameters.md) - Environment variables, external params, ${} syntax
- [rules/advanced/conditions.md](rules/advanced/conditions.md) - Conditional execution with when: visible, platform
- [rules/advanced/nested-flows.md](rules/advanced/nested-flows.md) - Reusable subflows with runFlow command
- [rules/advanced/javascript.md](rules/advanced/javascript.md) - evalScript, runScript, and GraalJS support
- [rules/advanced/waiting.md](rules/advanced/waiting.md) - extendedWaitUntil, waitForAnimationToEnd
- [rules/advanced/repeat-retry.md](rules/advanced/repeat-retry.md) - Repeat and retry patterns for flaky tests

### Additional

- [rules/debugging.md](rules/debugging.md) - Maestro Studio, hierarchy inspection, troubleshooting
- [rules/screenshots.md](rules/screenshots.md) - Screenshots, video recording, and visual evidence
- [rules/ci-integration.md](rules/ci-integration.md) - GitHub Actions, GitLab CI, Maestro Cloud
- [rules/best-practices.md](rules/best-practices.md) - Semantic identifiers, atomic tests, project structure
