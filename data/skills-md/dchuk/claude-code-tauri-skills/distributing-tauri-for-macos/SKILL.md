---
name: distributing-tauri-for-macos
description: Guides users through distributing Tauri applications on macOS, including creating DMG installers, configuring app bundles, setting up entitlements, and customizing Info.plist files for proper macOS distribution.
---

# Tauri macOS Distribution

This skill covers distributing Tauri v2 applications on macOS, including DMG installers and application bundle configuration.

## Overview

macOS distribution for Tauri apps involves two primary formats:

1. **Application Bundle (.app)** - The executable directory containing all app components
2. **DMG Installer (.dmg)** - A disk image that wraps the app bundle for easy drag-and-drop installation

## Building for macOS

### Build Commands

Generate specific bundle types using the Tauri CLI:

```bash
# Build app bundle only
npm run tauri build -- --bundles app
yarn tauri build --bundles app
pnpm tauri build --bundles app
cargo tauri build --bundles app

# Build DMG installer only
npm run tauri build -- --bundles dmg
yarn tauri build --bundles dmg
pnpm tauri build --bundles dmg
cargo tauri build --bundles dmg

# Build both
npm run tauri build -- --bundles app,dmg
```

## Application Bundle Structure

The `.app` directory follows macOS conventions:

```
<productName>.app/
Contents/
    Info.plist              # App metadata and configuration
    MacOS/
        <app-name>          # Main executable
    Resources/
        icon.icns           # App icon
        [bundled resources] # Additional resources
    _CodeSignature/         # Code signature files
    Frameworks/             # Bundled frameworks
    PlugIns/                # App plugins
    SharedSupport/          # Support files
```

## DMG Installer Configuration

Configure DMG appearance in `tauri.conf.json`:

### Complete DMG Configuration Example

```json
{
  "bundle": {
    "macOS": {
      "dmg": {
        "background": "./images/dmg-background.png",
        "windowSize": {
          "width": 660,
          "height": 400
        },
        "windowPosition": {
          "x": 400,
          "y": 400
        },
        "appPosition": {
          "x": 180,
          "y": 220
        },
        "applicationFolderPosition": {
          "x": 480,
          "y": 220
        }
      }
    }
  }
}
```

### DMG Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `background` | string | - | Path to background image relative to `src-tauri` |
| `windowSize.width` | number | 660 | DMG window width in pixels |
| `windowSize.height` | number | 400 | DMG window height in pixels |
| `windowPosition.x` | number | - | Initial window X position on screen |
| `windowPosition.y` | number | - | Initial window Y position on screen |
| `appPosition.x` | number | 180 | App icon X position in window |
| `appPosition.y` | number | 220 | App icon Y position in window |
| `applicationFolderPosition.x` | number | 480 | Applications folder X position |
| `applicationFolderPosition.y` | number | 480 | Applications folder Y position |

**Note:** Icon sizes and positions may not apply correctly when building on CI/CD platforms due to a known issue with headless environments.

## Info.plist Customization

### Creating a Custom Info.plist

Create `src-tauri/Info.plist` to extend the default configuration. The Tauri CLI automatically merges this with generated values.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Privacy Usage Descriptions -->
    <key>NSCameraUsageDescription</key>
    <string>This app requires camera access for video calls</string>

    <key>NSMicrophoneUsageDescription</key>
    <string>This app requires microphone access for audio recording</string>

    <key>NSLocationUsageDescription</key>
    <string>This app requires location access for mapping features</string>

    <key>NSPhotoLibraryUsageDescription</key>
    <string>This app requires photo library access to import images</string>

    <!-- Document Types -->
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeName</key>
            <string>My Document</string>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>mydoc</string>
            </array>
            <key>CFBundleTypeRole</key>
            <string>Editor</string>
        </dict>
    </array>

    <!-- URL Schemes -->
    <key>CFBundleURLTypes</key>
    <array>
        <dict>
            <key>CFBundleURLName</key>
            <string>com.example.myapp</string>
            <key>CFBundleURLSchemes</key>
            <array>
                <string>myapp</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
```

### Common Info.plist Keys

| Key | Description |
|-----|-------------|
| `NSCameraUsageDescription` | Camera access explanation |
| `NSMicrophoneUsageDescription` | Microphone access explanation |
| `NSLocationUsageDescription` | Location access explanation |
| `NSPhotoLibraryUsageDescription` | Photo library access explanation |
| `NSAppleEventsUsageDescription` | AppleScript/automation access |
| `CFBundleDocumentTypes` | Supported document types |
| `CFBundleURLTypes` | Custom URL schemes |
| `LSMinimumSystemVersion` | Minimum macOS version (prefer tauri.conf.json) |

### Info.plist Localization

Support multiple languages with localized strings:

**Directory structure:**
```
src-tauri/
    infoplist/
        en.lproj/
            InfoPlist.strings
        de.lproj/
            InfoPlist.strings
        fr.lproj/
            InfoPlist.strings
        es.lproj/
            InfoPlist.strings
```

**Example `InfoPlist.strings` (German):**
```
"NSCameraUsageDescription" = "Diese App benötigt Kamerazugriff für Videoanrufe";
"NSMicrophoneUsageDescription" = "Diese App benötigt Mikrofonzugriff für Audioaufnahmen";
```

**Configure in `tauri.conf.json`:**
```json
{
  "bundle": {
    "resources": {
      "infoplist/**": "./"
    }
  }
}
```

## Entitlements Configuration

Entitlements grant special capabilities when your app is code-signed.

### Creating Entitlements.plist

Create `src-tauri/Entitlements.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- App Sandbox (required for App Store) -->
    <key>com.apple.security.app-sandbox</key>
    <true/>

    <!-- Network Access -->
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.network.server</key>
    <true/>

    <!-- File Access -->
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
    <key>com.apple.security.files.downloads.read-write</key>
    <true/>

    <!-- Hardware Access -->
    <key>com.apple.security.device.camera</key>
    <true/>
    <key>com.apple.security.device.microphone</key>
    <true/>

    <!-- Hardened Runtime -->
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
</dict>
</plist>
```

### Configure Entitlements in tauri.conf.json

```json
{
  "bundle": {
    "macOS": {
      "entitlements": "./Entitlements.plist"
    }
  }
}
```

### Common Entitlements Reference

**Sandbox Entitlements:**
| Entitlement | Description |
|-------------|-------------|
| `com.apple.security.app-sandbox` | Enable app sandbox (required for App Store) |
| `com.apple.security.network.client` | Outbound network connections |
| `com.apple.security.network.server` | Incoming network connections |
| `com.apple.security.files.user-selected.read-write` | Access user-selected files |
| `com.apple.security.files.downloads.read-write` | Access Downloads folder |

**Hardware Entitlements:**
| Entitlement | Description |
|-------------|-------------|
| `com.apple.security.device.camera` | Camera access |
| `com.apple.security.device.microphone` | Microphone access |
| `com.apple.security.device.usb` | USB device access |
| `com.apple.security.device.bluetooth` | Bluetooth access |

**Hardened Runtime Entitlements:**
| Entitlement | Description |
|-------------|-------------|
| `com.apple.security.cs.allow-jit` | Allow JIT compilation |
| `com.apple.security.cs.allow-unsigned-executable-memory` | Allow unsigned executable memory |
| `com.apple.security.cs.disable-library-validation` | Load arbitrary plugins |

## macOS Bundle Configuration

### Complete macOS Configuration Example

```json
{
  "bundle": {
    "icon": ["icons/icon.icns"],
    "macOS": {
      "minimumSystemVersion": "10.13",
      "entitlements": "./Entitlements.plist",
      "frameworks": [
        "CoreAudio",
        "./libs/libcustom.dylib",
        "./frameworks/CustomFramework.framework"
      ],
      "files": {
        "embedded.provisionprofile": "./profiles/distribution.provisionprofile",
        "SharedSupport/README.md": "./docs/README.md"
      },
      "dmg": {
        "background": "./images/dmg-background.png",
        "windowSize": {
          "width": 660,
          "height": 400
        },
        "appPosition": {
          "x": 180,
          "y": 220
        },
        "applicationFolderPosition": {
          "x": 480,
          "y": 220
        }
      }
    }
  }
}
```

### Minimum System Version

Set the minimum supported macOS version:

```json
{
  "bundle": {
    "macOS": {
      "minimumSystemVersion": "12.0"
    }
  }
}
```

Default: macOS 10.13 (High Sierra)

### Including Frameworks and Libraries

Bundle system frameworks or custom dylib files:

```json
{
  "bundle": {
    "macOS": {
      "frameworks": [
        "CoreAudio",
        "AVFoundation",
        "./libs/libmsodbcsql.18.dylib",
        "./frameworks/Sparkle.framework"
      ]
    }
  }
}
```

- **System frameworks:** Specify name only (e.g., `"CoreAudio"`)
- **Custom frameworks/dylibs:** Provide path relative to `src-tauri`

### Adding Custom Files to Bundle

Include additional files in the bundle's Contents directory:

```json
{
  "bundle": {
    "macOS": {
      "files": {
        "embedded.provisionprofile": "./profile.provisionprofile",
        "SharedSupport/docs/guide.pdf": "./assets/guide.pdf",
        "Resources/config.json": "./config/default.json"
      }
    }
  }
}
```

Format: `"destination": "source"` where paths are relative to `tauri.conf.json`

## Troubleshooting

### Common Issues

**DMG icons not positioned correctly on CI/CD:**
- This is a known issue with headless environments
- Consider building DMGs locally or accepting default positioning

**App rejected due to missing usage descriptions:**
- Add all required `NS*UsageDescription` keys to `Info.plist`
- Ensure descriptions clearly explain why access is needed

**Entitlements not applied:**
- Verify the entitlements file path in `tauri.conf.json`
- Ensure the app is properly code-signed

**Framework not found at runtime:**
- Check framework path is correct relative to `src-tauri`
- Verify framework is properly signed

### Verification Commands

```bash
# Check Info.plist contents
plutil -p path/to/App.app/Contents/Info.plist

# Verify entitlements
codesign -d --entitlements - path/to/App.app

# Check code signature
codesign -vvv --deep --strict path/to/App.app

# View bundle structure
find path/to/App.app -type f | head -50
```

## Quick Reference

### File Locations

| File | Location | Purpose |
|------|----------|---------|
| `Info.plist` | `src-tauri/Info.plist` | App metadata extensions |
| `Entitlements.plist` | `src-tauri/Entitlements.plist` | Capability entitlements |
| `DMG Background` | Any path in project | DMG window background |
| `Localized strings` | `src-tauri/infoplist/<lang>.lproj/` | Localized Info.plist values |

### Build Output Locations

```
src-tauri/target/release/bundle/
    macos/
        <ProductName>.app         # Application bundle
    dmg/
        <ProductName>_<version>_<arch>.dmg  # DMG installer
```
