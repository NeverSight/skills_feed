---
name: electrobun-distribution
description: Packaging, code signing, notarization, and distribution for Electrobun desktop applications. This skill covers building production bundles, creating installers and distributable packages, code signing for Windows and macOS, Apple notarization for Gatekeeper, auto-updater implementation, delta updates, update servers, cross-platform build processes, CI/CD integration, app icons and resources, version management, release workflows, Windows SmartScreen requirements, macOS DMG creation, Linux package formats (deb, rpm, AppImage), and distribution best practices. Use when preparing app for production, implementing auto-updates, setting up code signing certificates, troubleshooting distribution issues, creating installers, configuring update servers, building for multiple platforms, or releasing new versions. Triggers include "build", "package", "distribute", "code sign", "notarize", "installer", "auto-update", "release", "production build", "DMG", "updater", "delta update", or "certificate".
license: MIT
metadata:
  author: Blackboard
  version: "1.0.0"
---

# Electrobun Distribution

Complete guide to packaging, signing, and distributing Electrobun applications.

## Production Build

### Basic Build Configuration

**electrobun.config.ts:**
```ts
import { defineConfig } from "electrobun";

export default defineConfig({
  app: {
    name: "My Application",
    version: "1.0.0",
    identifier: "com.mycompany.myapp",
    description: "My desktop application",
    author: "My Company",
  },
  
  build: {
    main: "src/bun/main.ts",
    views: {
      mainview: "src/views/mainview/index.ts",
      settings: "src/views/settings/index.ts",
    },
    output: "dist",
  },
  
  icons: {
    mac: "assets/icon.icns",    // macOS: 1024x1024 .icns
    win: "assets/icon.ico",     // Windows: .ico with multiple sizes
    linux: "assets/icon.png",   // Linux: 512x512 .png
  },
  
  updates: {
    provider: "generic",
    url: "https://updates.myapp.com",
  },
});
```

### Build Commands

```bash
# Development build
bun run dev

# Production build
bun run build

# Build for specific platform
bun run build --platform=mac
bun run build --platform=win
bun run build --platform=linux

# Build for all platforms
bun run build --all
```

## Code Signing

### macOS Code Signing

#### Setup Certificates

```bash
# List available certificates
security find-identity -v -p codesigning

# Import Developer ID certificate
# Get certificate from Apple Developer Portal
# Double-click .p12 file or:
security import cert.p12 -k ~/Library/Keychains/login.keychain
```

#### Sign Application

**electrobun.config.ts:**
```ts
export default defineConfig({
  // ...
  mac: {
    identity: "Developer ID Application: Your Name (TEAM_ID)",
    entitlements: "entitlements.mac.plist",
    entitlementsInherit: "entitlements.mac.plist",
    hardenedRuntime: true,
    gatekeeperAssess: false,
  },
});
```

**entitlements.mac.plist:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <!-- Allow JIT for Bun runtime -->
  <key>com.apple.security.cs.allow-jit</key>
  <true/>
  
  <!-- Allow unsigned executable memory -->
  <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
  <true/>
  
  <!-- Disable library validation -->
  <key>com.apple.security.cs.disable-library-validation</key>
  <true/>
  
  <!-- Network client access -->
  <key>com.apple.security.network.client</key>
  <true/>
  
  <!-- Optional: Network server -->
  <key>com.apple.security.network.server</key>
  <true/>
  
  <!-- Optional: Camera access -->
  <key>com.apple.security.device.camera</key>
  <true/>
  
  <!-- Optional: Microphone access -->
  <key>com.apple.security.device.audio-input</key>
  <true/>
</dict>
</plist>
```

#### Apple Notarization

```bash
# Notarize the app
xcrun notarytool submit dist/MyApp.dmg \
  --apple-id "your@email.com" \
  --team-id "TEAM_ID" \
  --password "app-specific-password" \
  --wait

# Check notarization status
xcrun notarytool log <submission-id> \
  --apple-id "your@email.com" \
  --team-id "TEAM_ID" \
  --password "app-specific-password"

# Staple notarization to DMG
xcrun stapler staple dist/MyApp.dmg

# Verify stapling
xcrun stapler validate dist/MyApp.dmg
```

**Automated notarization:**
```ts
// In electrobun.config.ts
export default defineConfig({
  // ...
  mac: {
    identity: "Developer ID Application: Your Name (TEAM_ID)",
    notarize: {
      teamId: process.env.APPLE_TEAM_ID,
      appleId: process.env.APPLE_ID,
      appleIdPassword: process.env.APPLE_APP_PASSWORD,
    },
  },
});
```

### Windows Code Signing

#### Get Certificate

```powershell
# Import certificate
certutil -importpfx cert.pfx

# Or specify password
certutil -f -p PASSWORD -importpfx cert.pfx
```

#### Sign Application

**electrobun.config.ts:**
```ts
export default defineConfig({
  // ...
  win: {
    certificateFile: "cert.pfx",
    certificatePassword: process.env.WIN_CERT_PASSWORD,
    signWithParams: "/tr http://timestamp.digicert.com /td sha256 /fd sha256",
  },
});
```

**Manual signing:**
```powershell
# Sign executable
signtool sign /f cert.pfx /p PASSWORD /tr http://timestamp.digicert.com /td sha256 /fd sha256 MyApp.exe

# Verify signature
signtool verify /pa MyApp.exe
```

## Auto-Updater

### Update Server Setup

**updates.json:**
```json
{
  "version": "1.0.1",
  "releaseDate": "2026-02-21T00:00:00Z",
  "platforms": {
    "darwin": {
      "url": "https://updates.myapp.com/MyApp-1.0.1-mac.zip",
      "signature": "MC0CFQCf...",
      "size": 15728640
    },
    "win32": {
      "url": "https://updates.myapp.com/MyApp-1.0.1-win.exe",
      "signature": "30820...",
      "size": 12582912
    },
    "linux": {
      "url": "https://updates.myapp.com/MyApp-1.0.1-linux.AppImage",
      "signature": "30440...",
      "size": 18874368
    }
  },
  "releaseNotes": "Bug fixes and performance improvements"
}
```

### Client Implementation

**src/bun/main.ts:**
```ts
import { Updater, dialog } from "electrobun/bun";

class UpdateManager {
  private updater: Updater;
  private updateAvailable = false;
  
  constructor() {
    this.updater = new Updater({
      url: "https://updates.myapp.com/updates.json",
      autoCheck: true,
      interval: 4 * 60 * 60 * 1000, // Check every 4 hours
    });
    
    this.setupHandlers();
  }
  
  private setupHandlers() {
    this.updater.on("update-available", async (info) => {
      this.updateAvailable = true;
      
      const result = await dialog.showMessageBox({
        type: "info",
        title: "Update Available",
        message: `Version ${info.version} is available`,
        detail: info.releaseNotes,
        buttons: ["Download Now", "Later"],
        defaultId: 0,
      });
      
      if (result.response === 0) {
        this.updater.downloadAndInstall();
      }
    });
    
    this.updater.on("update-not-available", () => {
      console.log("App is up to date");
    });
    
    this.updater.on("download-progress", (progress) => {
      console.log(`Download progress: ${progress.percent}%`);
      // Update UI with progress
      mainWindow.rpc.updateDownloadProgress(progress);
    });
    
    this.updater.on("update-downloaded", async () => {
      const result = await dialog.showMessageBox({
        type: "info",
        title: "Update Ready",
        message: "Update has been downloaded",
        detail: "The app will restart to apply the update",
        buttons: ["Restart Now", "Later"],
        defaultId: 0,
      });
      
      if (result.response === 0) {
        this.updater.quitAndInstall();
      }
    });
    
    this.updater.on("error", (error) => {
      console.error("Update error:", error);
      dialog.showMessageBox({
        type: "error",
        title: "Update Error",
        message: "Failed to check for updates",
        detail: error.message,
      });
    });
  }
  
  checkForUpdates() {
    this.updater.checkForUpdates();
  }
  
  isUpdateAvailable() {
    return this.updateAvailable;
  }
}

const updateManager = new UpdateManager();

// Expose to window RPC
win.defineRpc({
  handlers: {
    checkForUpdates: async () => {
      updateManager.checkForUpdates();
    },
    isUpdateAvailable: async () => {
      return updateManager.isUpdateAvailable();
    }
  }
});
```

### Delta Updates

Electrobun uses bsdiff for tiny delta updates (~14KB):

```ts
// Automatically handled by Updater
// Just ensure update server provides:
// - Full package for new installs
// - Delta patches for updates

// Update server structure:
// /updates.json
// /v1.0.0/MyApp-mac.zip (full)
// /v1.0.1/MyApp-mac.zip (full)
// /v1.0.1/delta-1.0.0-to-1.0.1-mac.patch (delta)
```

## Creating Installers

### macOS DMG

```bash
# Create DMG with background and app arrangement
create-dmg dist/MyApp.app dist/ \
  --overwrite \
  --window-size 660 400 \
  --icon-size 160 \
  --icon "MyApp.app" 180 170 \
  --hide-extension "MyApp.app" \
  --app-drop-link 480 170 \
  --background "installer-background.png"

# Result: dist/MyApp-1.0.0.dmg
```

### Windows Installer

**Using NSIS:**
```nsis
; installer.nsi
!include "MUI2.nsh"

Name "My Application"
OutFile "MyApp-Setup.exe"
InstallDir "$PROGRAMFILES\My Application"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  
  File /r "dist\*.*"
  
  CreateDirectory "$SMPROGRAMS\My Application"
  CreateShortcut "$SMPROGRAMS\My Application\My Application.lnk" "$INSTDIR\MyApp.exe"
  CreateShortcut "$DESKTOP\My Application.lnk" "$INSTDIR\MyApp.exe"
  
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyApp" "DisplayName" "My Application"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyApp" "UninstallString" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\*.*"
  RMDir /r "$INSTDIR"
  Delete "$SMPROGRAMS\My Application\*.*"
  RMDir "$SMPROGRAMS\My Application"
  Delete "$DESKTOP\My Application.lnk"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyApp"
SectionEnd
```

### Linux Packages

**AppImage (recommended):**
```bash
# Create AppImage
appimagetool dist/MyApp-linux-x64 dist/MyApp.AppImage

# Make executable
chmod +x dist/MyApp.AppImage
```

**Debian package:**
```bash
# Create .deb structure
mkdir -p myapp_1.0.0/DEBIAN
mkdir -p myapp_1.0.0/usr/bin
mkdir -p myapp_1.0.0/usr/share/applications
mkdir -p myapp_1.0.0/usr/share/icons/hicolor/512x512/apps

# Copy files
cp dist/MyApp myapp_1.0.0/usr/bin/
cp myapp.desktop myapp_1.0.0/usr/share/applications/
cp icon.png myapp_1.0.0/usr/share/icons/hicolor/512x512/apps/

# Create control file
cat > myapp_1.0.0/DEBIAN/control << EOF
Package: myapp
Version: 1.0.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Your Name <you@example.com>
Description: My Application
 A desktop application built with Electrobun
EOF

# Build .deb
dpkg-deb --build myapp_1.0.0
```

## CI/CD Integration

### GitHub Actions

**.github/workflows/build.yml:**
```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-mac:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        
      - name: Install dependencies
        run: bun install
        
      - name: Import signing certificate
        env:
          CERTIFICATE_BASE64: ${{ secrets.MAC_CERTIFICATE }}
          CERTIFICATE_PASSWORD: ${{ secrets.MAC_CERT_PASSWORD }}
        run: |
          echo $CERTIFICATE_BASE64 | base64 --decode > certificate.p12
          security import certificate.p12 -P $CERTIFICATE_PASSWORD
          
      - name: Build app
        env:
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APPLE_APP_PASSWORD: ${{ secrets.APPLE_APP_PASSWORD }}
          APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
        run: bun run build --platform=mac
        
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: mac-build
          path: dist/*.dmg

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        
      - name: Install dependencies
        run: bun install
        
      - name: Build app
        env:
          WIN_CERT_PASSWORD: ${{ secrets.WIN_CERT_PASSWORD }}
        run: bun run build --platform=win
        
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: win-build
          path: dist/*.exe

  release:
    needs: [build-mac, build-windows]
    runs-on: ubuntu-latest
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3
        
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            mac-build/*
            win-build/*
          draft: false
          prerelease: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Best Practices

### Version Management

```ts
// Use semantic versioning
const version = "1.2.3"; // MAJOR.MINOR.PATCH

// Update package.json and electrobun.config.ts together
// Automate with script:
import { writeFileSync, readFileSync } from "fs";

function updateVersion(newVersion: string) {
  // Update package.json
  const pkg = JSON.parse(readFileSync("package.json", "utf-8"));
  pkg.version = newVersion;
  writeFileSync("package.json", JSON.stringify(pkg, null, 2));
  
  // Update config
  const config = readFileSync("electrobun.config.ts", "utf-8");
  const updated = config.replace(
    /version:\s*"[^"]+"/,
    `version: "${newVersion}"`
  );
  writeFileSync("electrobun.config.ts", updated);
}
```

### Testing Before Release

```ts
// Pre-release checklist
const checklist = [
  "All tests passing",
  "No console errors",
  "Auto-updater tested",
  "Code signed and notarized",
  "Installer tested on clean system",
  "Release notes written",
  "Documentation updated",
];
```

## Resources

For more on Electrobun:
- **Core skill**: `electrobun` - Basic build setup
- **Debugging**: `electrobun-debugging` - Build troubleshooting
- **Auto-updater docs**: https://blackboard.sh/electrobun/docs/guides/auto-updates
