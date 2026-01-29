---
name: launch-assets
description: |
  Generate complete launch asset package by composing primitives.
  Runs: /product-hunt-kit, /og-hero-image, /announce, /app-screenshots (if mobile).
  Use when: preparing full launch, generating all marketing assets at once.
  Keywords: launch, assets, marketing, bundle, all assets.
argument-hint: "[product name]"
---

# /launch-assets

All launch assets. One command.

## What This Orchestrates
1. /brand-builder - if no brand-profile.yaml exists
2. /product-hunt-kit - PH launch copy + checklist
3. /og-hero-image - AI hero image for social
4. /announce - Multi-platform launch posts
5. /app-screenshots - if apps/mobile exists
Usage:
- `/launch-assets heartbeat`
- `/launch-assets caesar without screenshots`
Output:
```text
launch-assets/
  product-hunt-kit.md
  og-hero-[name].png
  announcements/
  screenshots/ (if mobile)
```
Order Matters:
Brand profile → Copy → Images → Distribution
Each step informs the next.
