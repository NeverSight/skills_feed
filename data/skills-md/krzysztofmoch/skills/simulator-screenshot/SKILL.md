---
name: simulator-screenshot
description: Capture screenshots from iOS Simulator or Android Emulator using the bundled simulator-screenshot.sh script. Use when asked to take simulator/emulator screenshots, list available devices, select a specific simulator or emulator by ID/name, or return JSON output for automation.
license: MIT
metadata:
  author: Krzysztof Moch
---

# Simulator Screenshot

## Overview

Use this skill to capture screenshots from iOS Simulator or Android Emulator via a single script with consistent JSON output. It supports listing devices, selecting by name or ID, and saving screenshots to a chosen path.
Useful for verifying UI changes, debugging layouts, or documenting app states during development.

If user is working on iOS/Android App use this tool to verify visual aspects by capturing simulator/emulator screenshots on demand.

## Quick Start

Use `scripts/simulator-screenshot.sh` from this skill folder.

```bash
# List iOS simulators (JSON)
scripts/simulator-screenshot.sh ios --list --json

# Capture from the booted iOS simulator
scripts/simulator-screenshot.sh ios ./screenshot.png --json

# Capture from a specific iOS simulator by name
scripts/simulator-screenshot.sh ios ./screenshot.png --id "iPhone 15 Pro" --json

# List Android emulators/devices (JSON)
scripts/simulator-screenshot.sh android --list --json

# Capture from a specific Android emulator by serial
scripts/simulator-screenshot.sh android ./screenshot.png --id emulator-5554 --json
```

## Workflow

Pre steps:
1. If user have not specified location to save screenshot, create `agent_screenshots` folder in the current directory.
2. Generate names for screenshots basing on context of usage eg. `login_screen-ios.png`, `settings_page-ios.png`.
3. Use `--max-size 1024` unless the user specifies another size.

Main steps:
1. Choose platform: `ios` or `android`.
2. If device is unknown, run `--list --json` and pick a device:
   - iOS: use device name or UDID.
   - Android: use running device serial (e.g., `emulator-5554`).
3. Capture with optional `--id` and an output path, including `--max-size 1024` unless specified otherwise.
4. Parse JSON output and check `status` for `success` or `error`.

## Output Notes

- Always pass `--json` for machine-readable output.
- Success JSON includes `path`, `platform`, `device_id` (if provided), and `timestamp`.
- Error JSON includes `message`, `platform`, and `timestamp`.

## Requirements

- iOS: macOS with Xcode Command Line Tools and `jq`.
- Android: Android SDK `adb` in PATH and `jq`. Optional `emulator` for listing AVDs.
