---
name: android-use
description: This skill enables control of Android devices via ADB and the accessibility API. Use this skill when users want to automate Android phone tasks, control apps remotely, tap buttons, type text, navigate UI, or perform any action on a connected Android device. Requires ADB and a connected device with USB debugging enabled.
---

# Android Use

## Overview

This skill enables Claude to control Android devices using ADB (Android Debug Bridge) and the Android Accessibility API (uiautomator). It works by capturing the device's UI hierarchy as structured XML text, parsing interactive elements with their coordinates, and executing actions like tapping, typing, swiping, and navigation.

**IMPORTANT: This skill uses TEXT-BASED UI automation, NOT image/screenshot processing.**

### Why Text-Based (Not Screenshots)?

| Approach | Cost | Speed | Accuracy |
|----------|------|-------|----------|
| Screenshots + Vision | ~$0.15/action | 3-5s | 70-80% |
| **Text UI Dump** | ~$0.01/action | <1s | 99%+ |

The Android Accessibility API provides **structured XML** with:
- Element text content (exact, no OCR errors)
- Precise coordinates (deterministic)
- Clickable/focusable state
- Resource IDs for identification

**Only use screenshots as a LAST RESORT** when:
- UI text is ambiguous or unclear
- You need to verify visual state (colours, images)
- Text dump is empty but screen clearly has content

## Prerequisites

Before using this skill, ensure:

1. **ADB installed**: `brew install android-platform-tools` (macOS) or equivalent
2. **Device connected**: Via USB with "USB debugging" enabled in Developer Options
3. **Device authorised**: Accept the RSA key prompt on the device when first connecting

To verify connection:
```bash
adb devices -l
```

## Quick Start Workflow

To control an Android device:

1. **Get screen state** - Dump UI hierarchy as text
2. **Parse elements** - Extract interactive components with coordinates
3. **Decide action** - Based on text content, find target element
4. **Execute action** - Tap, type, swipe, back, home
5. **Wait & repeat** - Allow UI to update, then reassess

## Core Commands

### Device Management

```bash
# List all connected devices
adb devices -l

# Target specific device (when multiple connected)
adb -s <DEVICE_ID> <command>
```

### UI Inspection (Text-Based)

```bash
# Dump UI hierarchy to device
adb -s <DEVICE_ID> shell uiautomator dump /sdcard/window_dump.xml

# Pull to local machine
adb -s <DEVICE_ID> pull /sdcard/window_dump.xml /tmp/screen.xml

# Parse and extract interactive elements
python3 scripts/parse_ui.py /tmp/screen.xml
```

**One-liner for convenience:**
```bash
adb -s <DEVICE_ID> shell uiautomator dump /sdcard/window_dump.xml && \
adb -s <DEVICE_ID> pull /sdcard/window_dump.xml /tmp/screen.xml && \
python3 scripts/parse_ui.py /tmp/screen.xml
```

The parser outputs interactive elements like:
```
TAPPABLE:
  👆 "Submit" @ (540, 1200)
  👆 "Cancel" @ (200, 1200)
  👆 [search_button] @ (980, 156)

INPUT FIELDS:
  ⌨️ "Enter email" @ (540, 600)

TEXT/INFO:
  👁️ "Welcome back, John" @ (540, 300)
```

### Actions

```bash
# Tap at coordinates
adb shell input tap <x> <y>

# Type text (use %s for spaces)
adb shell input text "hello%sworld"

# Press keys
adb shell input keyevent KEYCODE_HOME      # Home button
adb shell input keyevent KEYCODE_BACK      # Back button
adb shell input keyevent KEYCODE_ENTER     # Enter key
adb shell input keyevent KEYCODE_DEL       # Backspace

# Swipe (x1, y1 to x2, y2 over duration_ms)
adb shell input swipe <x1> <y1> <x2> <y2> <duration_ms>

# Long press (swipe with same start/end)
adb shell input swipe <x> <y> <x> <y> 1000
```

### App Management

```bash
# Launch app by package name (simplest)
adb shell monkey -p <package> -c android.intent.category.LAUNCHER 1

# Launch app with specific activity
adb shell am start -n <package>/<activity>

# List installed packages
adb shell pm list packages | grep <search>

# Force stop app
adb shell am force-stop <package>
```

## Standard Workflow

### Step 1: Get Current Screen State (TEXT ONLY)

```bash
adb -s <DEVICE_ID> shell uiautomator dump /sdcard/window_dump.xml && \
adb -s <DEVICE_ID> pull /sdcard/window_dump.xml /tmp/screen.xml && \
python3 scripts/parse_ui.py /tmp/screen.xml
```

This gives you a text list of all interactive elements with coordinates.

### Step 2: Find Target Element

From the parsed output, identify the element you need:
- Match by **text content**: `"Submit"`, `"Login"`, `"Search"`
- Match by **resource ID**: `[login_button]`, `[search_field]`
- Match by **type**: Button, EditText, TextView

### Step 3: Execute Action

```bash
# To tap "Submit" button at (540, 1200)
adb -s <DEVICE_ID> shell input tap 540 1200

# To type in a field - first tap it, then type
adb -s <DEVICE_ID> shell input tap 540 600
adb -s <DEVICE_ID> shell input text "user@email.com"
```

### Step 4: Wait and Repeat

```bash
# Wait 1-2 seconds for UI to update
sleep 2

# Dump again and reassess
adb -s <DEVICE_ID> shell uiautomator dump /sdcard/window_dump.xml && \
adb -s <DEVICE_ID> pull /sdcard/window_dump.xml /tmp/screen.xml && \
python3 scripts/parse_ui.py /tmp/screen.xml
```

## When to Use Screenshots (LAST RESORT ONLY)

**Only take a screenshot if:**
1. UI dump returns empty/incomplete but you know the screen has content
2. You need to verify something visual (image loaded, colour state)
3. Text elements are ambiguous and you need visual context
4. User explicitly asks to "see" the screen

```bash
# Screenshot command (USE SPARINGLY - costs ~15x more to process)
adb -s <DEVICE_ID> shell screencap -p /sdcard/screen.png && \
adb -s <DEVICE_ID> pull /sdcard/screen.png /tmp/screen.png
```

## Common Patterns

### Opening an App and Navigating

```bash
# 1. Launch app
adb -s DEVICE shell monkey -p com.example.app -c android.intent.category.LAUNCHER 1

# 2. Wait for launch
sleep 2

# 3. Get UI state (text)
adb -s DEVICE shell uiautomator dump /sdcard/window_dump.xml
adb -s DEVICE pull /sdcard/window_dump.xml /tmp/screen.xml
python3 scripts/parse_ui.py /tmp/screen.xml

# 4. Find and tap target element based on text output
adb -s DEVICE shell input tap <x> <y>
```

### Searching in an App

```bash
# 1. Find search field in UI dump
# Output shows: ⌨️ "Search" @ (540, 200)

# 2. Tap search field
adb shell input tap 540 200

# 3. Type search query
adb shell input text "cheesecake"

# 4. Press enter
adb shell input keyevent KEYCODE_ENTER
```

### Scrolling to Find Elements

If an element isn't visible in the UI dump, scroll and re-dump:

```bash
# Scroll down
adb shell input swipe 540 1500 540 500 300

# Wait and re-dump
sleep 1
adb shell uiautomator dump /sdcard/window_dump.xml
# ... parse again
```

### Handling Popups/Dialogs

Popups appear in UI dump with their own elements:
```
👆 "Allow" @ (700, 1200)
👆 "Deny" @ (300, 1200)
```

Just tap the appropriate button coordinates.

## Parser Output Reference

The `parse_ui.py` script outputs elements grouped by action type:

### TAPPABLE (clickable=true)
Elements that respond to taps: buttons, links, icons
```
👆 "Button Text" @ (x, y)
👆 [resource_id] @ (x, y)
```

### INPUT FIELDS (EditText)
Text input fields
```
⌨️ "Placeholder text" @ (x, y)
```

### TEXT/INFO (readable)
Non-interactive text elements (limited to 10)
```
👁️ "Display text" @ (x, y)
```

### JSON Output

For programmatic use:
```bash
python3 scripts/parse_ui.py /tmp/screen.xml --json
```

Returns:
```json
[
  {
    "id": "com.app:id/submit_btn",
    "text": "Submit",
    "type": "Button",
    "bounds": "[400,1100][680,1300]",
    "center": [540, 1200],
    "clickable": true,
    "action": "tap"
  }
]
```

## Troubleshooting

### "error: device not found"
- Check USB connection
- Run `adb devices` to verify
- Try `adb kill-server && adb start-server`

### UI dump returns empty/incomplete
- Screen may be loading - wait and retry
- Some apps have accessibility restrictions
- **Only then** consider a screenshot to diagnose

### Taps not registering
- Verify coordinates are within screen bounds
- Check if element is actually clickable
- Some overlays may intercept touches

### Text input issues
- Replace spaces with `%s`
- Special characters may need escaping
- For passwords, some apps block programmatic input

### Element not found in dump
- It may be off-screen - try scrolling
- It may be in a WebView (limited accessibility)
- It may be loading - wait and retry

## Reference

### Common Package Names

| App | Package |
|-----|---------|
| Uber Eats | com.ubercab.eats |
| DoorDash | com.dd.dasher |
| Chrome | com.android.chrome |
| Settings | com.android.settings |
| Messages | com.google.android.apps.messaging |

### Common Keycodes

| Key | Code |
|-----|------|
| Home | KEYCODE_HOME |
| Back | KEYCODE_BACK |
| Enter | KEYCODE_ENTER |
| Delete | KEYCODE_DEL |
| Tab | KEYCODE_TAB |
| Escape | KEYCODE_ESCAPE |

## Resources

- `scripts/parse_ui.py` - Parses Android UI XML and outputs interactive elements
- Based on [android-action-kernel](https://github.com/anthropics/android-action-kernel) approach
