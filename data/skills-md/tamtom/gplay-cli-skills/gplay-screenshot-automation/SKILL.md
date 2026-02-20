---
name: gplay-screenshot-automation
description: Automate Android screenshot capture across devices and locales using adb, Espresso/UI Automator, device framing, and gplay CLI upload. Use when building screenshot pipelines for Google Play listings.
---

# Google Play Screenshot Automation

Use this skill for agent-driven screenshot workflows where Android screenshots are captured via emulators or connected devices, organized by locale and device type, and uploaded to Google Play via `gplay`.

## Current Scope
- Screenshot capture via `adb shell screencap` and Android test frameworks (Espresso, UI Automator).
- Multi-device capture: phone, tablet, TV, Wear OS.
- Multi-locale capture with emulator locale switching.
- Device framing with third-party tools.
- Upload via `gplay images upload` or `gplay sync import-images`.
- CI/CD integration for fully automated pipelines.

## Defaults
- Raw screenshots dir: `./screenshots/raw`
- Framed screenshots dir: `./screenshots/framed`
- Metadata dir (FastLane format): `./metadata`

## 1) Emulator Setup

### Create emulators for each device type

```bash
# Phone (Pixel 7, API 34)
sdkmanager "system-images;android-34;google_apis;x86_64"
avdmanager create avd \
  --name "pixel7_api34" \
  --device "pixel_7" \
  --package "system-images;android-34;google_apis;x86_64"

# 10-inch Tablet
avdmanager create avd \
  --name "tablet10_api34" \
  --device "pixel_tablet" \
  --package "system-images;android-34;google_apis;x86_64"

# 7-inch Tablet
avdmanager create avd \
  --name "tablet7_api34" \
  --device "Nexus 7" \
  --package "system-images;android-34;google_apis;x86_64"
```

### Boot emulators

```bash
emulator -avd pixel7_api34 -no-audio -no-window -gpu swiftshader_indirect &
adb wait-for-device
adb shell getprop sys.boot_completed  # Wait until "1"
```

For headless CI environments, always use `-no-window -no-audio -gpu swiftshader_indirect`.

## 2) Basic Capture with adb

### Single screenshot

```bash
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png ./screenshots/raw/en-US/phone/home.png
adb shell rm /sdcard/screenshot.png
```

### Helper function for repeated captures

```bash
capture() {
  local NAME="$1"
  local LOCALE="$2"
  local DEVICE_TYPE="$3"
  local SERIAL="$4"
  local OUTPUT_DIR="./screenshots/raw/$LOCALE/$DEVICE_TYPE"

  mkdir -p "$OUTPUT_DIR"
  adb -s "$SERIAL" shell screencap -p "/sdcard/$NAME.png"
  adb -s "$SERIAL" pull "/sdcard/$NAME.png" "$OUTPUT_DIR/$NAME.png"
  adb -s "$SERIAL" shell rm "/sdcard/$NAME.png"
  echo "Captured $OUTPUT_DIR/$NAME.png"
}

# Usage
capture "home" "en-US" "phoneScreenshots" "emulator-5554"
capture "settings" "en-US" "phoneScreenshots" "emulator-5554"
capture "home" "en-US" "tenInchScreenshots" "emulator-5556"
```

## 3) Test Framework Capture (Espresso / UI Automator)

For repeatable, state-driven screenshots, use Android instrumentation tests.

### Espresso screenshot test

```kotlin
// app/src/androidTest/java/com/example/app/ScreenshotTest.kt
@RunWith(AndroidJUnit4::class)
class ScreenshotTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    @Test
    fun captureHomeScreen() {
        // Wait for content to load
        onView(withId(R.id.main_content))
            .check(matches(isDisplayed()))

        takeScreenshot("home")
    }

    @Test
    fun captureSearchScreen() {
        onView(withId(R.id.search_button)).perform(click())
        onView(withId(R.id.search_input)).perform(typeText("example"))

        takeScreenshot("search")
    }

    private fun takeScreenshot(name: String) {
        val bitmap = InstrumentationRegistry.getInstrumentation()
            .uiAutomation.takeScreenshot()
        val dir = File(
            InstrumentationRegistry.getInstrumentation()
                .targetContext.getExternalFilesDir(null),
            "screenshots"
        )
        dir.mkdirs()
        val file = File(dir, "$name.png")
        file.outputStream().use {
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, it)
        }
    }
}
```

### Run tests and pull screenshots

```bash
# Build and run instrumented tests
./gradlew connectedAndroidTest \
  -Pandroid.testInstrumentationRunnerArguments.class=com.example.app.ScreenshotTest

# Pull screenshots from device
adb pull /sdcard/Android/data/com.example.app/files/screenshots/ ./screenshots/raw/en-US/phoneScreenshots/
```

### UI Automator for cross-app flows

```kotlin
@RunWith(AndroidJUnit4::class)
class UiAutomatorScreenshotTest {

    private lateinit var device: UiDevice

    @Before
    fun setup() {
        device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())
    }

    @Test
    fun captureNotificationScreen() {
        device.openNotification()
        device.wait(Until.hasObject(By.pkg("com.android.systemui")), 3000)
        takeScreenshot("notifications")
    }

    private fun takeScreenshot(name: String) {
        val file = File(
            InstrumentationRegistry.getInstrumentation()
                .targetContext.getExternalFilesDir(null),
            "screenshots/$name.png"
        )
        file.parentFile?.mkdirs()
        device.takeScreenshot(file)
    }
}
```

## 4) Multi-locale Capture

### Switch emulator locale via adb

```bash
set_locale() {
  local SERIAL="$1"
  local LOCALE="$2"   # e.g. "de-DE"
  local LANG="${LOCALE%%-*}"  # e.g. "de"
  local REGION="${LOCALE##*-}" # e.g. "DE"

  adb -s "$SERIAL" shell "setprop persist.sys.locale ${LANG}-${REGION}"
  adb -s "$SERIAL" shell "setprop persist.sys.language ${LANG}"
  adb -s "$SERIAL" shell "setprop persist.sys.country ${REGION}"
  adb -s "$SERIAL" shell "settings put system system_locales ${LANG}-${REGION}"
  # Restart the app to pick up locale change
  adb -s "$SERIAL" shell am force-stop com.example.app
  adb -s "$SERIAL" shell am start -n com.example.app/.MainActivity
  sleep 3
}
```

### Capture across multiple locales

```bash
#!/bin/bash
# multi-locale-capture.sh

SERIAL="emulator-5554"
PACKAGE="com.example.app"
LOCALES=("en-US" "de-DE" "fr-FR" "es-ES" "ja" "ko" "pt-BR" "zh-CN")

for LOCALE in "${LOCALES[@]}"; do
  echo "Capturing locale: $LOCALE"
  set_locale "$SERIAL" "$LOCALE"

  mkdir -p "./screenshots/raw/$LOCALE/phoneScreenshots"

  # Capture each screen
  for SCREEN in "home" "search" "settings" "profile"; do
    adb -s "$SERIAL" shell screencap -p "/sdcard/$SCREEN.png"
    adb -s "$SERIAL" pull "/sdcard/$SCREEN.png" \
      "./screenshots/raw/$LOCALE/phoneScreenshots/$SCREEN.png"
    adb -s "$SERIAL" shell rm "/sdcard/$SCREEN.png"

    # Navigate to next screen (app-specific logic)
    # adb -s "$SERIAL" shell input tap X Y
  done

  echo "Done: $LOCALE"
done
```

### Using Espresso test arguments for locale

```bash
# Run screenshot tests with a specific locale
./gradlew connectedAndroidTest \
  -Pandroid.testInstrumentationRunnerArguments.class=com.example.app.ScreenshotTest \
  -Pandroid.testInstrumentationRunnerArguments.locale=de-DE
```

## 5) Multi-device Capture

### Capture across phone, tablet, TV, and Wear

```bash
#!/bin/bash
# multi-device-capture.sh

declare -A DEVICES=(
  ["phoneScreenshots"]="emulator-5554"       # Pixel 7
  ["tenInchScreenshots"]="emulator-5556"     # Pixel Tablet
  ["sevenInchScreenshots"]="emulator-5558"   # Nexus 7
  ["tvScreenshots"]="emulator-5560"          # Android TV
  ["wearScreenshots"]="emulator-5562"        # Wear OS
)

LOCALE="en-US"

for DEVICE_TYPE in "${!DEVICES[@]}"; do
  SERIAL="${DEVICES[$DEVICE_TYPE]}"
  echo "Capturing $DEVICE_TYPE on $SERIAL"

  mkdir -p "./screenshots/raw/$LOCALE/$DEVICE_TYPE"

  for SCREEN in "home" "search" "settings"; do
    adb -s "$SERIAL" shell screencap -p "/sdcard/$SCREEN.png"
    adb -s "$SERIAL" pull "/sdcard/$SCREEN.png" \
      "./screenshots/raw/$LOCALE/$DEVICE_TYPE/$SCREEN.png"
    adb -s "$SERIAL" shell rm "/sdcard/$SCREEN.png"
  done

  echo "Done: $DEVICE_TYPE"
done
```

## 6) Device Framing

Use third-party tools to wrap raw screenshots in device frames for polished store listings.

### Using frameit (from fastlane)

```bash
gem install fastlane

# Place Framefile.json alongside screenshots
cat > ./screenshots/raw/Framefile.json << 'EOF'
{
  "device_frame_version": "latest",
  "default": {
    "keyword": { "font": "./fonts/SF-Pro-Display-Bold.otf" },
    "title": { "font": "./fonts/SF-Pro-Display-Regular.otf" }
  }
}
EOF

cd ./screenshots/raw && fastlane frameit
```

### Using a custom framing script

```bash
#!/bin/bash
# frame-screenshots.sh
# Requires ImageMagick

FRAME_IMAGE="./frames/pixel7_frame.png"
RAW_DIR="./screenshots/raw"
FRAMED_DIR="./screenshots/framed"

for LOCALE_DIR in "$RAW_DIR"/*/; do
  LOCALE=$(basename "$LOCALE_DIR")
  for TYPE_DIR in "$LOCALE_DIR"*/; do
    TYPE=$(basename "$TYPE_DIR")
    mkdir -p "$FRAMED_DIR/$LOCALE/$TYPE"
    for IMG in "$TYPE_DIR"*.png; do
      NAME=$(basename "$IMG")
      convert "$FRAME_IMAGE" "$IMG" \
        -gravity center -geometry +0+0 -composite \
        "$FRAMED_DIR/$LOCALE/$TYPE/$NAME"
      echo "Framed: $FRAMED_DIR/$LOCALE/$TYPE/$NAME"
    done
  done
done
```

## 7) Validate Before Upload

Always validate screenshots before uploading:

```bash
gplay validate screenshots --dir ./screenshots/framed --output table
```

Check specific locale:
```bash
gplay validate screenshots --dir ./screenshots/framed --locale en-US --output table
```

## 8) Upload to Google Play

### Option A: Upload via sync (FastLane directory structure)

Organize screenshots in FastLane format:
```
metadata/
  en-US/
    images/
      phoneScreenshots/
        1_home.png
        2_search.png
      tenInchScreenshots/
        1_home.png
  de-DE/
    images/
      phoneScreenshots/
        1_home.png
        2_search.png
```

Then import:
```bash
gplay sync import-images \
  --package com.example.app \
  --dir ./metadata
```

### Option B: Upload individual images

```bash
EDIT_ID=$(gplay edits create --package com.example.app | jq -r '.id')

# Upload phone screenshots
gplay images upload \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type phoneScreenshots \
  --file ./screenshots/framed/en-US/phoneScreenshots/home.png

gplay images upload \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type phoneScreenshots \
  --file ./screenshots/framed/en-US/phoneScreenshots/search.png

# Upload tablet screenshots
gplay images upload \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type tenInchScreenshots \
  --file ./screenshots/framed/en-US/tenInchScreenshots/home.png

# Upload feature graphic
gplay images upload \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type featureGraphic \
  --file ./screenshots/framed/en-US/featureGraphic.png

# Validate and commit
gplay edits validate --package com.example.app --edit $EDIT_ID
gplay edits commit --package com.example.app --edit $EDIT_ID
```

### Option C: Upload as part of a release

```bash
gplay release \
  --package com.example.app \
  --track production \
  --bundle app-release.aab \
  --screenshots-dir ./metadata \
  --release-notes @release-notes.json
```

### Replace existing screenshots

Delete before uploading to replace:
```bash
EDIT_ID=$(gplay edits create --package com.example.app | jq -r '.id')

# Delete all existing phone screenshots for a locale
gplay images delete-all \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type phoneScreenshots

# Upload new ones
gplay images upload \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type phoneScreenshots \
  --file ./screenshots/framed/en-US/phoneScreenshots/home.png

gplay edits validate --package com.example.app --edit $EDIT_ID
gplay edits commit --package com.example.app --edit $EDIT_ID
```

## 9) Full Automation Pipeline

```bash
#!/bin/bash
# screenshot-pipeline.sh
# End-to-end: boot emulators, capture, frame, validate, upload

PACKAGE="com.example.app"
SERIAL="emulator-5554"
LOCALES=("en-US" "de-DE" "fr-FR" "es-ES" "ja")
RAW_DIR="./screenshots/raw"
METADATA_DIR="./metadata"

# Step 1: Boot emulator
emulator -avd pixel7_api34 -no-audio -no-window -gpu swiftshader_indirect &
adb wait-for-device
adb -s "$SERIAL" shell "while [[ \$(getprop sys.boot_completed) != '1' ]]; do sleep 1; done"

# Step 2: Build and install app
./gradlew assembleRelease
adb -s "$SERIAL" install -r app/build/outputs/apk/release/app-release.apk

# Step 3: Capture per locale
for LOCALE in "${LOCALES[@]}"; do
  set_locale "$SERIAL" "$LOCALE"
  mkdir -p "$RAW_DIR/$LOCALE/phoneScreenshots"

  for SCREEN in "home" "search" "settings" "profile"; do
    adb -s "$SERIAL" shell screencap -p "/sdcard/$SCREEN.png"
    adb -s "$SERIAL" pull "/sdcard/$SCREEN.png" "$RAW_DIR/$LOCALE/phoneScreenshots/$SCREEN.png"
    adb -s "$SERIAL" shell rm "/sdcard/$SCREEN.png"
  done
done

# Step 4: Organize into FastLane metadata structure
for LOCALE in "${LOCALES[@]}"; do
  mkdir -p "$METADATA_DIR/$LOCALE/images/phoneScreenshots"
  cp "$RAW_DIR/$LOCALE/phoneScreenshots/"*.png "$METADATA_DIR/$LOCALE/images/phoneScreenshots/"
done

# Step 5: Validate
gplay validate screenshots --dir "$METADATA_DIR" --output table

# Step 6: Upload
gplay sync import-images --package "$PACKAGE" --dir "$METADATA_DIR"

# Step 7: Kill emulator
adb -s "$SERIAL" emu kill

echo "Screenshot pipeline complete."
```

## 10) CI/CD Integration

### GitHub Actions

```yaml
name: Screenshot Pipeline
on:
  workflow_dispatch:
  schedule:
    - cron: '0 4 * * 1'  # Weekly Monday 4am

jobs:
  screenshots:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Enable KVM
        run: |
          echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules
          sudo udevadm control --reload-rules
          sudo udevadm trigger --name-match=kvm

      - name: AVD cache
        uses: actions/cache@v4
        with:
          path: |
            ~/.android/avd/*
            ~/.android/adb*
          key: avd-api-34

      - name: Create AVD
        run: |
          sdkmanager "system-images;android-34;google_apis;x86_64"
          avdmanager create avd -n pixel7_api34 -d pixel_7 \
            --package "system-images;android-34;google_apis;x86_64" --force

      - name: Build app
        run: ./gradlew assembleRelease

      - name: Capture screenshots
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          target: google_apis
          arch: x86_64
          profile: pixel_7
          script: ./scripts/capture-screenshots.sh

      - name: Validate screenshots
        run: gplay validate screenshots --dir ./metadata --output table

      - name: Upload to Play Store
        run: |
          gplay sync import-images \
            --package ${{ secrets.PACKAGE_NAME }} \
            --dir ./metadata
        env:
          GPLAY_SERVICE_ACCOUNT: ${{ secrets.GPLAY_SERVICE_ACCOUNT_PATH }}

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: screenshots
          path: ./screenshots/
```

## Google Play Image Type Reference

| Type | Usage |
|------|-------|
| `phoneScreenshots` | Phone screenshots (required, 2-8) |
| `sevenInchScreenshots` | 7-inch tablet screenshots |
| `tenInchScreenshots` | 10-inch tablet screenshots |
| `tvScreenshots` | Android TV screenshots |
| `wearScreenshots` | Wear OS screenshots |
| `featureGraphic` | Feature graphic (1024x500) |
| `promoGraphic` | Promo graphic (180x120) |
| `icon` | App icon (512x512, usually set in Console) |
| `tvBanner` | TV banner (1280x720) |

## Agent Behavior
- Always confirm exact flags with `--help` before running commands.
- Use `gplay validate screenshots` before uploading.
- Prefer `gplay sync import-images` for bulk uploads over individual `gplay images upload` calls.
- When using individual uploads, always create an edit, upload, validate, then commit.
- Keep outputs deterministic: default to JSON for machine steps, `--output table` for user review.
- Use explicit long flags (`--package`, `--edit`, `--locale`, `--type`, `--file`).
- Verify emulator is fully booted (`sys.boot_completed == 1`) before capturing.
- For multi-locale workflows, always force-stop and relaunch the app after locale change.
- Validate screenshot counts (min 2 phone screenshots) before attempting upload.

## Notes
- Google Play requires PNG or JPEG format; PNG is recommended for quality.
- Maximum image file size is 8 MB per screenshot.
- Screenshot ordering on Play Store matches upload order.
- Use `gplay images list` to verify uploaded images.
- Use `gplay images delete-all` to clear screenshots before re-uploading.
- Always use `--help` to verify flags for the exact command.
