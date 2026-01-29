---
name: outside-in-testing-ios-apps
description: "Test iOS apps running in Simulator from the outside in. Use PROACTIVELY when you need to verify an iOS app works, run acceptance tests, check UI behavior, perform outside-in testing, end-to-end testing, functional testing, exploratory testing, or smoke testing of iOS apps. Covers launching test flows, verifying screens, interacting with UI elements, and diagnosing failures. Triggers on: test my app, verify the app, check the UI, does this work, acceptance test, outside-in test, e2e test, functional test, smoke test, exploratory test."
---

<objective>
Guide agents through outside-in testing of iOS apps running in Simulator. The agent interacts with the app as a real user would — navigating screens, tapping buttons, entering text, and verifying that the app behaves correctly. When the app misbehaves, the agent diagnoses failures using simulator logs.
</objective>

<tool>
All interactions use the AXe CLI (`axe`), a tool for driving iOS Simulators via accessibility APIs and HID.

**Installation (prerequisite):**
```bash
brew install cameroncooke/axe/axe
```

The iOS Simulator must be running with the app under test.
</tool>

<quick_start>
1. Find the simulator: `axe list-simulators` — look for a Booted simulator, capture its UDID
2. Screenshot current state: `axe screenshot --udid {UDID} --output /tmp/screen.png`
3. Describe the UI: `axe describe-ui --udid {UDID}`
4. Interact: `axe tap --label "Button" --udid {UDID}`
5. Repeat: screenshot → describe → interact → verify
</quick_start>

<process>
Follow an **Observe → Act → Verify** loop for each step of the test flow.

**Observe**
- Take a screenshot: `axe screenshot --udid {UDID} --output /tmp/screen.png`
- Read the accessibility tree: `axe describe-ui --udid {UDID}`
- To inspect a specific point: `axe describe-ui --point 100,200 --udid {UDID}`

**Act** — choose based on what you need to do:

- Tap by accessibility label: `axe tap --label "Login" --udid {UDID}`
- Tap by accessibility identifier: `axe tap --id "loginButton" --udid {UDID}`
- Tap by coordinates (fallback): `axe tap -x 200 -y 400 --udid {UDID}`
- Type text: `axe type 'user@example.com' --udid {UDID}`
- Type from stdin: `echo "text" | axe type --stdin --udid {UDID}`
- Type from file: `axe type --file input.txt --udid {UDID}`
- Scroll: `axe gesture scroll-down --udid {UDID}`
- Swipe: `axe swipe --start-x 200 --start-y 500 --end-x 200 --end-y 200 --duration 0.3 --udid {UDID}`
- Advanced touch (hold): `axe touch -x 150 -y 250 --down --up --delay 1.0 --udid {UDID}`
- Press key: `axe key 40 --udid {UDID}` (Enter)
- Key sequence: `axe key-sequence --keycodes 11,8,15,15,18 --udid {UDID}`
- Home button: `axe button home --udid {UDID}`
- Siri: `axe button siri --udid {UDID}`

**Verify**
After each action, take a screenshot and check whether the expected change occurred. If something is wrong, note the issue and investigate.

**Timing controls** — add delays when animations or loading cause flakiness:
- `--pre-delay 0.5` — wait before acting
- `--post-delay 1.0` — wait after acting
- `--duration 0.3` — control gesture speed
</process>

<gesture_presets>
Available preset gestures (use with `axe gesture {preset} --udid {UDID}`):
- `scroll-up`, `scroll-down`, `scroll-left`, `scroll-right`
- `swipe-from-left-edge`, `swipe-from-right-edge`
- `swipe-from-top-edge`, `swipe-from-bottom-edge`

For specific screen sizes: `axe gesture swipe-from-left-edge --screen-width 430 --screen-height 932 --udid {UDID}`
</gesture_presets>

<recording>
Record video of test sessions for evidence or debugging:
- Record MP4: `axe record-video --udid {UDID} --fps 15 --output recording.mp4`
- Lower quality/size: `axe record-video --udid {UDID} --fps 10 --quality 60 --scale 0.5 --output recording.mp4`
- Stream MJPEG: `axe stream-video --udid {UDID} --fps 10 --format mjpeg > stream.mjpeg`
</recording>

<diagnosing_failures>
When the app is not behaving as expected, fetch simulator logs to diagnose:

```bash
# Stream logs from the booted simulator (Ctrl+C to stop)
xcrun simctl spawn booted log stream --level debug --predicate 'subsystem == "com.apple.UIKit" OR processImagePath CONTAINS "{APP_NAME}"' 2>&1 | head -200

# Get recent log entries
xcrun simctl spawn booted log show --last 5m --predicate 'processImagePath CONTAINS "{APP_NAME}"' --style compact

# Check for crash logs
ls ~/Library/Logs/DiagnosticReports/*{APP_NAME}* 2>/dev/null
```

Replace `{APP_NAME}` with the app's process name (visible in `describe-ui` output or from `xcrun simctl listapps booted`).

**If this is a React Native app**, invoke the `debugging-react-native` skill (https://github.com/mikekelly/debugging-react-native) for React Native-specific diagnosis including Metro bundler issues, JS errors, and red box screens.
</diagnosing_failures>

<gotchas>
- **Labels with special characters fail**: `axe tap --label "Reload (⌘R)"` breaks. Use coordinates from `describe-ui` instead.
- **Tapping input fields may show context menus**: iOS may show "Paste"/"AutoFill" instead of the keyboard. Tap elsewhere to dismiss, then tap the field again or just use `axe type`.
- **Coordinates are in points, not pixels**: Use values from `describe-ui` directly — do not multiply by screen scale.
- **React Native apps need Metro bundler**: If you see "No script URL provided", Metro isn't running. Start it with `npm start` in the app directory.
</gotchas>

<success_criteria>
Testing is complete when:
- App launched and initial screen verified via screenshot
- Core user flows exercised (navigate, interact, verify outcomes)
- Key interactive elements respond correctly
- No crashes or unhandled errors encountered (or failures diagnosed via logs)
- Findings documented: what worked, what failed, and why
</success_criteria>
