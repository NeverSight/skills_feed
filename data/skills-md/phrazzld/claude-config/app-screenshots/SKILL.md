---
name: app-screenshots
description: |
  Generate App Store and Play Store screenshots with device frames.
  Use when: preparing for app store submission, updating marketing assets,
  localizing screenshots, or automating screenshot generation in CI.
  Uses fastlane (free) not SaaS. Keywords: app store, play store, screenshot,
  device frame, fastlane, snapshot, frameit, localization.
argument-hint: "[app path] [platforms: ios, android] [locales: en, es]"
---

## What This Does
- Configure `Snapfile` for app routes, devices, locales.
- Run `fastlane snapshot` across simulators/emulators.
- Apply device frames via `fastlane frameit`.
- Organize output by platform/locale/device.

## Why fastlane (not Screenshots Pro)
- Free, CLI-first, CI/CD native, handles all device sizes automatically.

## Prerequisites
- `gem install fastlane`
- Xcode (iOS) or Android SDK (Android)

## Usage
- `/app-screenshots apps/mobile for ios in english and spanish`
- `/app-screenshots . for iphone 15 pro only`

## References
- `references/fastlane-config.md`
- `references/device-specs.md`
