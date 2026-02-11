---
name: android-adb
description: Android device control and UI automation via ADB using a TypeScript helper CLI. Use for device/emulator discovery, USB or Wi-Fi connection, app launch/force-stop, tap/swipe/keyevent/text input, screenshots, APK install handling, device reset for app, and ADB troubleshooting. Use with ai-vision for screenshot-based UI recognition and coordinate decisions.
---

# Android ADB Automation

Execute Android operations with `scripts/adb_helpers.ts` in the `android-adb` skill directory.

## Path Convention

Canonical install and execution directory: `~/.agents/skills/android-adb/`. Run commands from this directory:

```bash
cd ~/.agents/skills/android-adb
```

One-off (safe in scripts/loops from any working directory):

```bash
(cd ~/.agents/skills/android-adb && npx tsx scripts/adb_helpers.ts --help)
```

## Core Capabilities

- Device discovery and connection management.
- App lifecycle control (`launch`, `force-stop`).
- Input primitives (`tap`, `swipe`, `long-press`, `keyevent`, `text`).
- Screenshot and UI dump utilities (`screenshot`, `dump-ui --parse`).
- Install automation with UI assistance (`install-smart`).
- Device reset workflow for app (`device-reset`).

## Execution Constraints

- Use `-s <device_id>` whenever more than one device is connected.
- Confirm resolution before coordinate actions: `npx tsx scripts/adb_helpers.ts -s SERIAL wm-size`.
- Run each `npx` command in its owning skill directory (`android-adb` or `ai-vision`).
- Prefer helper subcommands before raw `adb` calls.
- Prefer `text --adb-keyboard` when ADB Keyboard exists; otherwise use plain `text`.
- Ask for missing required inputs before executing (serial, package/activity/schema, coordinates, APK path).
- Surface actionable stderr on failure (authorization, cable/network, tcpip state, missing env vars).

## Reference Map

- Command catalog and examples: `references/adb-reference.md`
- Vision-first UI recognition flow: `references/ui-recognition.md`
- Installer dialog handling details: `references/install-smart.md`
- Generic verification handling: `references/handle-verification.md`
- Device reset flow for app: `references/device-reset.md`

Load only the file needed for the current task.

## Minimal Commands

```bash
npx tsx scripts/adb_helpers.ts --help
npx tsx scripts/adb_helpers.ts devices
npx tsx scripts/adb_helpers.ts -s SERIAL wm-size
npx tsx scripts/adb_helpers.ts -s SERIAL screenshot --out ~/.eval/screenshots/shot.png
```
