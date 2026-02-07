---
name: distributing-tauri-for-windows
description: Guides users through distributing Tauri applications on Windows, including creating MSI and NSIS installers, customizing installer behavior, configuring WebView2 installation modes, and submitting apps to the Microsoft Store.
---

# Distributing Tauri Applications for Windows

This skill covers Windows distribution for Tauri v2 applications, including MSI/NSIS installer creation, customization, and Microsoft Store submission.

## Installer Formats Overview

Tauri supports two Windows installer formats:

| Format | Extension | Build Platform | Notes |
|--------|-----------|----------------|-------|
| WiX MSI | `.msi` | Windows only | Traditional Windows installer |
| NSIS | `-setup.exe` | Cross-platform | Can build on Linux/macOS |

## Building Installers

### Standard Build (Windows)

```bash
npm run tauri build
# or
yarn tauri build
# or
pnpm tauri build
# or
cargo tauri build
```

### Target Architectures

```bash
# 64-bit (default)
npm run tauri build -- --target x86_64-pc-windows-msvc

# 32-bit
npm run tauri build -- --target i686-pc-windows-msvc

# ARM64 (requires additional VS build tools)
npm run tauri build -- --target aarch64-pc-windows-msvc
```

### Cross-Platform NSIS Build (Linux/macOS)

NSIS installers can be built on non-Windows systems:

**Prerequisites (Linux):**
```bash
# Install NSIS and build tools (Debian/Ubuntu)
sudo apt install nsis lld llvm clang

# Install Windows Rust target
rustup target add x86_64-pc-windows-msvc

# Install cargo-xwin
cargo install --locked cargo-xwin
```

**Prerequisites (macOS):**
```bash
# Install via Homebrew
brew install nsis llvm

# Add LLVM to PATH
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"

# Install Windows Rust target
rustup target add x86_64-pc-windows-msvc

# Install cargo-xwin
cargo install --locked cargo-xwin
```

**Build command:**
```bash
npm run tauri build -- --runner cargo-xwin --target x86_64-pc-windows-msvc
```

## WebView2 Installation Modes

Configure how WebView2 runtime is installed on end-user machines:

| Mode | Internet Required | Size Impact | Best For |
|------|-------------------|-------------|----------|
| `downloadBootstrapper` | Yes | 0 MB | Default, smallest installer |
| `embedBootstrapper` | Yes | ~1.8 MB | Better Windows 7 support |
| `offlineInstaller` | No | ~127 MB | Offline/air-gapped environments |
| `fixedVersion` | No | ~180 MB | Controlled enterprise deployment |
| `skip` | No | 0 MB | Not recommended |

### Configuration

```json
{
  "bundle": {
    "windows": {
      "webviewInstallMode": {
        "type": "embedBootstrapper"  // or: downloadBootstrapper, offlineInstaller, fixedVersion
      }
    }
  }
}
```

For `fixedVersion`, add the path: `"path": "./WebView2Runtime"`

## WiX MSI Customization

### Custom WiX Template

Replace the default template:

```json
{
  "bundle": {
    "windows": {
      "wix": {
        "template": "./windows/custom-template.wxs"
      }
    }
  }
}
```

### WiX Fragments

Add custom functionality via XML fragments:

**1. Create fragment file** (`src-tauri/windows/fragments/registry.wxs`):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Fragment>
    <ComponentGroup Id="MyFragmentRegistryEntries">
      <Component Id="MyRegistryEntry" Directory="INSTALLDIR">
        <RegistryKey Root="HKCU" Key="Software\MyApp">
          <RegistryValue Type="string" Name="InstallPath" Value="[INSTALLDIR]" KeyPath="yes"/>
        </RegistryKey>
      </Component>
    </ComponentGroup>
  </Fragment>
</Wix>
```

**2. Reference in configuration:**
```json
{
  "bundle": {
    "windows": {
      "wix": {
        "fragmentPaths": ["./windows/fragments/registry.wxs"],
        "componentRefs": ["MyFragmentRegistryEntries"]
      }
    }
  }
}
```

### Internationalization (WiX)

```json
{
  "bundle": {
    "windows": {
      "wix": {
        "language": ["en-US", "fr-FR", "de-DE"],  // Single: "fr-FR"
        "localePath": "./windows/locales"  // Optional: custom locale files
      }
    }
  }
}
```

## NSIS Installer Customization

### Install Modes

| Mode | Admin Required | Install Location | Use Case |
|------|----------------|------------------|----------|
| `perUser` | No | `%LOCALAPPDATA%` | Default, no elevation |
| `perMachine` | Yes | `%PROGRAMFILES%` | System-wide install |
| `both` | Yes | User choice | Flexible deployment |

```json
{
  "bundle": {
    "windows": {
      "nsis": {
        "installMode": "perMachine"
      }
    }
  }
}
```

### Installer Hooks

Extend installation with custom NSIS scripts:

**1. Create hooks file** (`src-tauri/windows/hooks.nsh`):
```nsis
!macro NSIS_HOOK_PREINSTALL
  ; Run before file installation
  DetailPrint "Preparing installation..."
!macroend

!macro NSIS_HOOK_POSTINSTALL
  ; Run after installation completes
  DetailPrint "Configuring application..."
  ; Example: Install VC++ Redistributable
  ReadRegStr $0 HKLM "SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" "Installed"
  ${If} $0 != "1"
    ExecWait '"$INSTDIR\vc_redist.x64.exe" /quiet /norestart'
  ${EndIf}
!macroend

!macro NSIS_HOOK_PREUNINSTALL
  ; Run before uninstallation
  DetailPrint "Cleaning up..."
!macroend

!macro NSIS_HOOK_POSTUNINSTALL
  ; Run after uninstallation
  DetailPrint "Removal complete"
!macroend
```

**2. Reference in configuration:**
```json
{
  "bundle": {
    "windows": {
      "nsis": {
        "installerHooks": "./windows/hooks.nsh"
      }
    }
  }
}
```

### Internationalization (NSIS)

NSIS installers support multiple languages in a single file:

```json
{
  "bundle": {
    "windows": {
      "nsis": {
        "languages": ["English", "French", "German", "Spanish"],
        "displayLanguageSelector": true
      }
    }
  }
}
```

### Minimum WebView2 Version

Require a specific WebView2 version:

```json
{
  "bundle": {
    "windows": {
      "nsis": {
        "minimumWebview2Version": "110.0.1531.0"
      }
    }
  }
}
```

## Complete Configuration Example

```json
{
  "bundle": {
    "active": true,
    "targets": ["msi", "nsis"],
    "icon": ["icons/icon.ico"],
    "windows": {
      "certificateThumbprint": "YOUR_CERTIFICATE_THUMBPRINT",
      "timestampUrl": "http://timestamp.digicert.com",
      "webviewInstallMode": {
        "type": "embedBootstrapper"
      },
      "wix": {
        "language": ["en-US", "de-DE"],
        "fragmentPaths": ["./windows/fragments/registry.wxs"],
        "componentRefs": ["MyRegistryEntries"]
      },
      "nsis": {
        "installMode": "both",
        "installerHooks": "./windows/hooks.nsh",
        "languages": ["English", "German"],
        "displayLanguageSelector": true,
        "minimumWebview2Version": "110.0.1531.0"
      }
    }
  }
}
```

## Special Configurations

### Windows 7 Support

```json
{
  "bundle": {
    "windows": {
      "webviewInstallMode": {
        "type": "embedBootstrapper"
      }
    }
  }
}
```

Enable Windows 7 notification support in `Cargo.toml`:
```toml
[dependencies]
tauri = { version = "2", features = ["windows7-compat"] }
```

### FIPS Compliance

Set environment variable before building:

**PowerShell:**
```powershell
$env:TAURI_BUNDLER_WIX_FIPS_COMPLIANT = "true"
npm run tauri build
```

**Command Prompt:**
```cmd
set TAURI_BUNDLER_WIX_FIPS_COMPLIANT=true
npm run tauri build
```

## Microsoft Store Distribution

### Requirements

1. Microsoft account with developer enrollment
2. Offline installer WebView2 mode (required by Store policy)
3. Publisher name different from product name

### Store-Specific Configuration

Create `tauri.microsoftstore.conf.json`:
```json
{
  "bundle": {
    "windows": {
      "webviewInstallMode": {
        "type": "offlineInstaller"
      }
    }
  },
  "identifier": "com.yourcompany.yourapp",
  "publisher": "Your Company Name"
}
```

### Generate Store Icons

```bash
npm run tauri icon /path/to/app-icon.png
```

This generates all required icon sizes including Microsoft Store assets.

### Build for Store

```bash
npm run tauri build -- --config tauri.microsoftstore.conf.json
```

### Submission Process

1. Build with offline installer configuration
2. Sign installer with valid code signing certificate
3. Create app listing in Partner Center (Apps and Games)
4. Reserve unique app name
5. Upload installer to distribution service
6. Link installer URL in Store listing
7. Submit for certification

### Publisher Name Constraint

Your publisher name cannot match your product name. If your bundle identifier is `com.myapp.myapp`, explicitly set a different publisher:

```json
{
  "identifier": "com.myapp.myapp",
  "publisher": "MyApp Software Inc"
}
```

## Code Signing

### Using Certificate Thumbprint

```json
{
  "bundle": {
    "windows": {
      "certificateThumbprint": "YOUR_CERTIFICATE_THUMBPRINT",
      "timestampUrl": "http://timestamp.digicert.com"
    }
  }
}
```

### Environment Variables

```bash
# Certificate path
export TAURI_SIGNING_PRIVATE_KEY_PASSWORD="your-password"

# Or via tauri.conf.json
```

### Timestamp Servers

Common timestamp servers:
- DigiCert: `http://timestamp.digicert.com`
- Sectigo: `http://timestamp.sectigo.com`
- GlobalSign: `http://timestamp.globalsign.com/tsa/r6advanced1`

## Troubleshooting

### MSI Build Fails on Non-Windows

MSI files can only be built on Windows using WiX Toolset. Use NSIS for cross-platform builds.

### WebView2 Not Installing

1. Check webview install mode configuration
2. Verify internet connectivity for bootstrapper modes
3. For offline mode, ensure installer size is acceptable

### NSIS Cross-Compilation Errors

1. Verify NSIS is installed and in PATH
2. Check LLVM/clang installation
3. Ensure Windows Rust target is installed
4. Verify cargo-xwin is installed

### Certificate Not Found

1. Verify certificate is installed in Windows certificate store
2. Check thumbprint matches exactly (no spaces)
3. Ensure certificate has private key access
