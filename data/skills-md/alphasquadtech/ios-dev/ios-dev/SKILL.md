---
name: ios-dev
description: >
  iOS development workflow for building, running, testing, debugging, and fixing
  iOS apps using Xcode, Simulator, screenshots, and Maestro UI automation.
  Use when: building an iOS app, running on simulator, taking simulator screenshots,
  navigating app UI, debugging iOS issues, creating Xcode projects, writing SwiftUI
  or UIKit code, running xcodebuild, using xcrun simctl, or any iOS/iPhone/iPad
  development task.
allowed-tools: >
  Bash, Read, Write, Edit, Glob, Grep
user-invocable: true
argument-hint: "[build|run|test|screenshot|debug]"
---

# iOS Development Skill

You are an expert iOS developer with full autonomous control of the Xcode build pipeline, iOS Simulator, screenshot capture, Maestro UI automation, and debug log analysis. Follow these procedures exactly.

## 1. Pre-flight Checks

**On every invocation**, run the preflight script first. Locate this skill's scripts directory:

```bash
SKILL_SCRIPTS=$(find -L .claude/skills .agents/skills -path "*/ios-dev/scripts" -type d 2>/dev/null | head -1)
bash "$SKILL_SCRIPTS/preflight.sh"
```

If it reports BLOCKED, fix the issues before proceeding. If Maestro is missing, the script auto-installs it. Always ensure `~/.maestro/bin` is in PATH:

```bash
export PATH="$HOME/.maestro/bin:$PATH"
```

## 2. Project Discovery

Auto-detect the Xcode project:

```bash
# Prefer workspace (supports CocoaPods)
find . -maxdepth 3 -name "*.xcworkspace" -not -path "*/DerivedData/*" -not -path "*/.build/*" -not -path "*/Pods/*" 2>/dev/null | head -1

# Fall back to project file
find . -maxdepth 3 -name "*.xcodeproj" -not -path "*/DerivedData/*" -not -path "*/Pods/*" 2>/dev/null | head -1
```

If found, discover schemes:
```bash
xcodebuild -list -project <path> 2>/dev/null
# or
xcodebuild -list -workspace <path> 2>/dev/null
```

If no project exists, create one as needed for the task.

## 3. Simulator Management

### Select a simulator

```bash
# Check if one is already booted -- use it
xcrun simctl list devices booted 2>/dev/null

# If none booted, list available iPhone simulators and pick the newest iPhone Pro:
xcrun simctl list devices available 2>/dev/null | grep "iPhone"
```

Selection priority: booted device > newest iPhone Pro > newest iPhone > any available.

### Boot and open

```bash
xcrun simctl boot <UDID>
open -a Simulator
sleep 3  # Wait for simulator to fully boot
```

## 4. Build

```bash
xcodebuild -project <path.xcodeproj> -scheme <scheme> -sdk iphonesimulator -destination 'platform=iOS Simulator,id=<UDID>' -configuration Debug -derivedDataPath .claude-ios/build CODE_SIGNING_ALLOWED=NO build 2>&1
```

> **Note**: The xcodebuild command must be on a **single line** when executed via Bash tool. Backslash line continuations may cause `Unknown build action ''` errors in agent environments.

For workspaces, use `-workspace` instead of `-project`.

**On build failure**: Read the error output, fix the source code, rebuild. Retry up to 3 times.

The built `.app` bundle will be at:
```
.claude-ios/build/Build/Products/Debug-iphonesimulator/<AppName>.app
```

## 5. Install & Launch

```bash
xcrun simctl install booted .claude-ios/build/Build/Products/Debug-iphonesimulator/<AppName>.app
xcrun simctl launch booted <bundle.identifier>
sleep 3  # Wait for app to load
```

Find the bundle identifier:
```bash
defaults read .claude-ios/build/Build/Products/Debug-iphonesimulator/<AppName>.app/Info.plist CFBundleIdentifier
```

## 6. Screenshots (CRITICAL)

**ALWAYS use the screenshot script.** Never take a raw screenshot without resizing.

```bash
SKILL_SCRIPTS=$(find -L .claude/skills .agents/skills -path "*/ios-dev/scripts" -type d 2>/dev/null | head -1)
bash "$SKILL_SCRIPTS/screenshot.sh" <descriptive_name>
```

This captures the simulator screen, resizes to max 1568px (Claude API limit), and saves to `.claude-ios/screenshots/<name>.png`.

**After every screenshot, ALWAYS use the Read tool to view it:**

```
Read tool -> .claude-ios/screenshots/<name>.png
```

This is how you see the app. Analyze what is on screen and decide next actions.

### Screenshot naming convention
Use descriptive names: `home_screen`, `login_form`, `after_submit`, `error_state`, `detail_view`.

## 7. UI Navigation with Maestro

### Quick single actions
Write a temporary Maestro flow file and run it:

```yaml
# .claude-ios/flow.yaml
appId: <bundle.identifier>
---
- tapOn: "Button Text"
- inputText: "Hello"
- assertVisible: "Expected Result"
- takeScreenshot: .claude-ios/screenshots/after_action
```

```bash
export PATH="$HOME/.maestro/bin:$PATH"
MAESTRO_CLI_NO_ANALYTICS=1 maestro test .claude-ios/flow.yaml
```

### After Maestro runs
1. Resize any screenshots Maestro took (it does NOT auto-resize):
   ```bash
   sips --resampleHeightWidthMax 1568 .claude-ios/screenshots/<name>.png
   ```
2. Use the Read tool to view them.

### Key Maestro commands
- `tapOn: "text"` -- tap a button/label by its text
- `tapOn: { id: "accessibilityId" }` -- tap by accessibility identifier
- `inputText: "text"` -- type into focused field
- `assertVisible: "text"` -- verify element exists
- `scroll` / `swipe` -- navigate lists
- `waitForAnimationToEnd` -- wait after transitions
- See `references/maestro-guide.md` for the full command reference.

## 8. Video Recording

```bash
SKILL_SCRIPTS=$(find -L .claude/skills .agents/skills -path "*/ios-dev/scripts" -type d 2>/dev/null | head -1)

# Start recording
bash "$SKILL_SCRIPTS/record.sh" start <name>

# ... perform actions ...

# Stop recording
bash "$SKILL_SCRIPTS/record.sh" stop
```

Videos are saved to `.claude-ios/videos/`.

## 9. Debug Logs

### View recent logs
```bash
xcrun simctl spawn booted log show --last 5m --predicate 'process == "<AppName>"' --style compact
```

### Stream logs in real-time
```bash
xcrun simctl spawn booted log stream --predicate 'process == "<AppName>"' --level debug --timeout 10
```

### Check for crash logs
```bash
xcrun simctl spawn booted log show --last 2m --predicate 'process == "<AppName>" AND messageType == 16' --style compact
```

## 10. The Autonomous Build-Run-Verify Loop

When asked to build, test, or fix an iOS app, follow this exact sequence:

1. **Preflight** -- Run `preflight.sh`, fix any blockers
2. **Discover** -- Find or create the Xcode project
3. **Build** -- `xcodebuild` for simulator
4. **If build fails** -- Read errors, fix code, rebuild (up to 3 retries)
5. **Simulator** -- Boot if needed, select best device
6. **Install** -- Install `.app` on simulator
7. **Launch** -- Start the app
8. **Screenshot** -- Take screenshot via `screenshot.sh`, view with Read tool
9. **Verify** -- Analyze the screenshot. Does the UI look correct?
10. **If UI is wrong** -- Diagnose from screenshot, fix code, rebuild from step 3
11. **Navigate** -- If needed, use Maestro to tap/type/swipe through the app
12. **Screenshot again** -- Capture and view each significant state
13. **Debug** -- If something is off, check logs for errors
14. **Iterate** -- Repeat until the app works correctly

## 11. Rules (Non-negotiable)

1. **NEVER** view a screenshot without resizing first -- always use `screenshot.sh` or `sips --resampleHeightWidthMax 1568`
2. **ALWAYS** use the Read tool to view screenshots after taking them -- this is how you see the app
3. **NEVER** ask the user to manually interact with the simulator -- do everything programmatically
4. **ALWAYS** store artifacts in `.claude-ios/screenshots/` and `.claude-ios/videos/`
5. **ALWAYS** use `CODE_SIGNING_ALLOWED=NO` for simulator builds
6. **ALWAYS** use `-derivedDataPath .claude-ios/build` to keep build artifacts in the project
7. **ALWAYS** run preflight checks at the start of a session
8. For troubleshooting, see `references/troubleshooting.md`
