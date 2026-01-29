---
name: android-build
description: Use when building Android apps (Gradle CLI) or ROMs (AOSP, LineageOS). Triggers on "gradle build", "assemble", "AOSP", "LineageOS", "lunch", "mka", "breakfast", "brunch", "compile android", "device tree", "kernel build".
---

# Android Build Systems

This skill covers building Android apps via Gradle CLI and building custom ROMs via AOSP/LineageOS.

---

## App Building (Gradle CLI)

### Essential Commands

```bash
./gradlew tasks                     # List available tasks
./gradlew assembleDebug             # Build debug APK
./gradlew assembleRelease           # Build release APK
./gradlew installDebug              # Build + install to device
./gradlew bundleRelease             # Build AAB (App Bundle)

# APK output location
# app/build/outputs/apk/debug/app-debug.apk
# app/build/outputs/apk/release/app-release.apk
```

### Build Variants

```bash
./gradlew assembleFreeDebug         # Flavor + build type
./gradlew assemblePaidRelease
./gradlew assembleDebug --info      # Verbose output
./gradlew assembleRelease -x test   # Skip tests
```

### Testing

```bash
./gradlew test                      # Unit tests
./gradlew testDebugUnitTest         # Debug unit tests only
./gradlew connectedAndroidTest      # Instrumented tests
./gradlew connectedCheck            # All connected tests

# Run specific test
./gradlew test --tests "*.MyTestClass"
```

### Linting & Analysis

```bash
./gradlew lint                      # Run lint
./gradlew lintDebug                 # Debug only (faster)
./gradlew ktlintCheck               # Kotlin style (if configured)
./gradlew detekt                    # Detekt analysis (if configured)
```

### Clean & Refresh

```bash
./gradlew clean                     # Clean build
./gradlew clean assembleDebug       # Clean + build
./gradlew --refresh-dependencies    # Force dependency refresh
./gradlew --stop                    # Stop Gradle daemon
```

### Dependencies

```bash
./gradlew dependencies              # All dependencies
./gradlew app:dependencies          # Module dependencies
./gradlew dependencyInsight --dependency <name>
```

### Signing

Debug keystore location:

- Linux: `~/.android/debug.keystore`
- macOS: `~/.android/debug.keystore`
- Windows: `C:\Users\<user>\.android\debug.keystore`

Password: `android`, Alias: `androiddebugkey`

```bash
# Create release keystore
keytool -genkey -v -keystore release.keystore \
    -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000
```

### Performance

```bash
./gradlew assembleDebug --parallel  # Parallel builds
./gradlew assembleDebug --build-cache  # Use cache
./gradlew assembleDebug --offline   # Offline mode
./gradlew --scan                    # Build scan (uploads data)
./gradlew --profile                 # Local profile report
```

### gradle.properties Optimization

```properties
org.gradle.jvmargs=-Xmx4g -XX:+HeapDumpOnOutOfMemoryError
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true
android.useAndroidX=true
```

---

## SDK Management

### sdkmanager

```bash
sdkmanager --list                   # List available packages
sdkmanager --list | grep system     # Filter system images
sdkmanager "platform-tools"         # Install package
sdkmanager "platforms;android-34"   # Install platform
sdkmanager "system-images;android-34;google_apis;x86_64"
sdkmanager --update                 # Update all
sdkmanager --licenses               # Accept licenses
```

### avdmanager

```bash
avdmanager list device              # List device profiles
avdmanager list avd                 # List created AVDs

# Create AVD
avdmanager create avd -n my_avd \
    -k "system-images;android-34;google_apis;x86_64" \
    -d pixel_6

avdmanager delete avd -n my_avd
```

### Emulator CLI

```bash
emulator -list-avds                 # List AVDs
emulator @my_avd                    # Start AVD
emulator @my_avd -no-snapshot       # Fresh boot
emulator @my_avd -no-window         # Headless
emulator @my_avd -wipe-data         # Factory reset
```

---

## ROM Building (AOSP/LineageOS)

### Environment Setup

```bash
# Install repo tool
mkdir -p ~/.bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/.bin/repo
chmod a+x ~/.bin/repo
export PATH="$HOME/.bin:$PATH"

# Initialize repo
mkdir android && cd android
repo init -u https://github.com/LineageOS/android.git -b lineage-21.0
# Or AOSP: repo init -u https://android.googlesource.com/platform/manifest

# Sync source
repo sync -c -j$(nproc) --force-sync --no-tags --no-clone-bundle
```

### Build Commands

```bash
# Setup environment
source build/envsetup.sh

# Select device
lunch <device>-userdebug           # AOSP
breakfast <device>                  # LineageOS

# Build
m                                   # Full build
mka bacon                           # LineageOS (with flashable zip)
mka bootimage                       # Just boot.img
mka systemimage                     # Just system

# Parallel build
m -j$(nproc)
```

### Build Variants

| Variant     | Purpose                                |
| ----------- | -------------------------------------- |
| `user`      | Production, no root, limited debugging |
| `userdebug` | Like user + root + debugging           |
| `eng`       | Development, all debug tools           |

### Common Targets

```bash
m bootimage                         # Kernel + ramdisk
m systemimage                       # System partition
m vendorimage                       # Vendor partition
m otapackage                        # OTA zip
mka bacon                           # LineageOS flashable zip

# Module-specific
m Settings                          # Just Settings app
mm                                  # Build current directory
mmm packages/apps/Settings          # Build specific path
```

### LineageOS Specifics

```bash
breakfast <device>                  # Setup + sync device deps
brunch <device>                     # breakfast + mka bacon

# Cherry-pick from Gerrit
repopick <change_number>
repopick -t <topic>

# Sync specific project
repo sync packages/apps/Settings
```

### Build Output

```
out/target/product/<device>/
├── boot.img                        # Kernel + ramdisk
├── system.img                      # System partition
├── vendor.img                      # Vendor partition
├── lineage-*.zip                   # Flashable zip (LineageOS)
└── recovery.img                    # Recovery (non-A/B)
```

---

## Device Trees

### Structure

```
device/<vendor>/<device>/
├── AndroidProducts.mk              # Product makefiles list
├── BoardConfig.mk                  # Board configuration
├── device.mk                       # Device makefile
├── lineage_<device>.mk             # LineageOS product
├── extract-files.sh                # Vendor blob extraction
├── proprietary-files.txt           # Blob list
├── sepolicy/                       # SELinux policies
└── overlay/                        # Resource overlays
```

### Key Files

**BoardConfig.mk** - Hardware configuration:

```makefile
TARGET_ARCH := arm64
TARGET_BOARD_PLATFORM := <platform>
TARGET_BOOTLOADER_BOARD_NAME := <device>
BOARD_KERNEL_CMDLINE := ...
BOARD_BOOT_HEADER_VERSION := 4
```

**device.mk** - Device packages:

```makefile
PRODUCT_PACKAGES += \
    android.hardware.audio@7.0-impl \
    audio.primary.$(TARGET_BOARD_PLATFORM)

PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/configs/audio_policy.conf:...
```

---

## Kernel Building

### Standalone

```bash
# Setup
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-
# Or for Clang:
export CC=clang
export CLANG_TRIPLE=aarch64-linux-gnu-

# Configure
make <device>_defconfig

# Build
make -j$(nproc)

# Output
arch/arm64/boot/Image.gz
```

### In AOSP Tree

```makefile
# In BoardConfig.mk
TARGET_KERNEL_SOURCE := kernel/<vendor>/<device>
TARGET_KERNEL_CONFIG := <device>_defconfig
TARGET_KERNEL_CLANG_COMPILE := true
```

---

## Troubleshooting

### Common Gradle Issues

```bash
# OOM
export GRADLE_OPTS="-Xmx4g"

# Daemon issues
./gradlew --stop
rm -rf ~/.gradle/daemon

# Cache issues
./gradlew clean --refresh-dependencies
```

### Common AOSP Issues

```bash
# Ninja error - usually dependency issue
m clean && m

# Jack server (old builds)
./prebuilts/sdk/tools/jack-admin kill-server
./prebuilts/sdk/tools/jack-admin start-server

# SELinux issues
audit2allow -i audit.log
```

### Build Logs

```bash
# Gradle
./gradlew assembleDebug --stacktrace
./gradlew assembleDebug --info

# AOSP
m 2>&1 | tee build.log
```

---

## Quick Reference

### Gradle

| Task          | Command                     |
| ------------- | --------------------------- |
| Build debug   | `./gradlew assembleDebug`   |
| Build release | `./gradlew assembleRelease` |
| Install       | `./gradlew installDebug`    |
| Test          | `./gradlew test`            |
| Lint          | `./gradlew lint`            |
| Clean         | `./gradlew clean`           |
| Dependencies  | `./gradlew dependencies`    |

### AOSP/LineageOS

| Task          | Command                    |
| ------------- | -------------------------- |
| Setup env     | `source build/envsetup.sh` |
| Select device | `lunch <device>-userdebug` |
| Full build    | `m`                        |
| LineageOS zip | `mka bacon`                |
| Just boot     | `mka bootimage`            |
| Sync          | `repo sync -c -j$(nproc)`  |
