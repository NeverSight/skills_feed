---
name: signing-tauri-apps
description: Guides the user through Tauri application code signing and notarization for Android, iOS, Linux, macOS, and Windows platforms including certificate setup and configuration.
---

# Tauri Code Signing Skill

This skill provides comprehensive guidance for code signing Tauri applications across all supported platforms.

## Platform Overview

| Platform | Requirement | Certificate Type |
|----------|-------------|------------------|
| Android | Required for Play Store | Java Keystore (JKS) |
| iOS | Required for distribution | Apple Developer Certificate |
| Linux | Optional (enhances trust) | GPG Key |
| macOS | Required for distribution | Developer ID / Apple Distribution |
| Windows | Required (SmartScreen) | OV or EV Certificate |

---

## Android Signing

### Generate Keystore

**macOS/Linux:**
```bash
keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

**Windows:**
```powershell
keytool -genkey -v -keystore $env:USERPROFILE\upload-keystore.jks -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

### Configuration File

Create `src-tauri/gen/android/keystore.properties`:

```properties
password=<your-password>
keyAlias=upload
storeFile=/path/to/upload-keystore.jks
```

**IMPORTANT:** Never commit `keystore.properties` to version control.

### Gradle Configuration

Modify `src-tauri/gen/android/app/build.gradle.kts`:

```kotlin
import java.io.FileInputStream

// Add before android { } block
val keystorePropertiesFile = rootProject.file("keystore.properties")
val keystoreProperties = java.util.Properties()
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

android {
    // ... existing config ...

    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["password"] as String
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["password"] as String
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            // ... other release config ...
        }
    }
}
```

### CI/CD Environment Variables

| Variable | Description |
|----------|-------------|
| `ANDROID_KEY_ALIAS` | Key alias (e.g., `upload`) |
| `ANDROID_KEY_PASSWORD` | Keystore password |
| `ANDROID_KEY_BASE64` | Base64-encoded keystore file |

**GitHub Actions Example:**

```yaml
- name: Setup Android signing
  run: |
    cd src-tauri/gen/android
    echo "keyAlias=${{ secrets.ANDROID_KEY_ALIAS }}" > keystore.properties
    echo "password=${{ secrets.ANDROID_KEY_PASSWORD }}" >> keystore.properties
    base64 -d <<< "${{ secrets.ANDROID_KEY_BASE64 }}" > $RUNNER_TEMP/keystore.jks
    echo "storeFile=$RUNNER_TEMP/keystore.jks" >> keystore.properties
```

---

## iOS Signing

### Prerequisites

- Apple Developer Program enrollment ($99/year)
- Bundle identifier registered in App Store Connect
- iOS code signing certificate
- Mobile provisioning profile

### Automatic Signing (Recommended)

For local development, authenticate through Xcode Settings > Accounts.

For CI/CD, create an App Store Connect API key and set:

| Variable | Description |
|----------|-------------|
| `APPLE_API_ISSUER` | Issuer ID from App Store Connect |
| `APPLE_API_KEY` | Key ID from App Store Connect |
| `APPLE_API_KEY_PATH` | Path to the `.p8` private key file |

### Manual Signing

| Variable | Description |
|----------|-------------|
| `IOS_CERTIFICATE` | Base64-encoded `.p12` certificate |
| `IOS_CERTIFICATE_PASSWORD` | Password used when exporting certificate |
| `IOS_MOBILE_PROVISION` | Base64-encoded provisioning profile |

### Certificate Types by Distribution Method

| Distribution | Certificate Type |
|--------------|------------------|
| Debugging | Apple Development or iOS App Development |
| App Store | Apple Distribution or iOS Distribution |
| Ad Hoc | Apple Distribution or iOS Distribution |

### Export Certificate

1. Open Keychain Access
2. Find your certificate
3. Right-click the private key
4. Select "Export" and save as `.p12`
5. Convert to base64: `base64 -i certificate.p12`

### Create Provisioning Profile

1. Register App ID with matching bundle identifier
2. Create provisioning profile for your distribution method
3. Link certificate to profile
4. Download and convert: `base64 -i profile.mobileprovision`

---

## Linux Signing (AppImage)

### Generate GPG Key

```bash
gpg2 --full-gen-key
```

Back up the key securely.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `SIGN` | Set to `1` to enable signing |
| `SIGN_KEY` | GPG Key ID (optional, uses default if not set) |
| `APPIMAGETOOL_SIGN_PASSPHRASE` | Key password (required for CI/CD) |
| `APPIMAGETOOL_FORCE_SIGN` | Set to `1` to fail build on signing error |

### Build with Signing

```bash
SIGN=1 APPIMAGETOOL_SIGN_PASSPHRASE="your-passphrase" npm run tauri build
```

### View Embedded Signature

```bash
./src-tauri/target/release/bundle/appimage/app_version_amd64.AppImage --appimage-signature
```

### Validate Signature

Download the validate tool from [AppImageUpdate releases](https://github.com/AppImageCommunity/AppImageUpdate/releases):

```bash
chmod +x validate-x86_64.AppImage
./validate-x86_64.AppImage your-app.AppImage
```

**Note:** AppImage does not auto-validate signatures. Users must manually verify.

---

## macOS Signing and Notarization

### Prerequisites

- Apple Developer Program enrollment ($99/year)
- Mac computer for code signing
- Free accounts cannot notarize applications

### Certificate Types

| Certificate | Use Case |
|-------------|----------|
| Apple Distribution | App Store submissions |
| Developer ID Application | Distribution outside App Store |

### Create Certificate

1. Generate Certificate Signing Request (CSR) from Keychain Access
2. Upload CSR at Apple Developer > Certificates, IDs & Profiles
3. Download and double-click `.cer` to install

### Configuration

**tauri.conf.json:**

```json
{
  "bundle": {
    "macOS": {
      "signingIdentity": "Developer ID Application: Your Name (TEAM_ID)"
    }
  }
}
```

### Environment Variables for CI/CD

**Certificate Variables:**

| Variable | Description |
|----------|-------------|
| `APPLE_CERTIFICATE` | Base64-encoded `.p12` certificate |
| `APPLE_CERTIFICATE_PASSWORD` | Password for exported certificate |
| `APPLE_SIGNING_IDENTITY` | Certificate name in keychain |

**Notarization - Option 1: App Store Connect API (Recommended):**

| Variable | Description |
|----------|-------------|
| `APPLE_API_ISSUER` | Issuer ID |
| `APPLE_API_KEY` | Key ID |
| `APPLE_API_KEY_PATH` | Path to `.p8` private key |

**Notarization - Option 2: Apple ID:**

| Variable | Description |
|----------|-------------|
| `APPLE_ID` | Apple ID email |
| `APPLE_PASSWORD` | App-specific password |
| `APPLE_TEAM_ID` | Team identifier |

### Export Certificate for CI/CD

```bash
# Export from Keychain as .p12, then:
base64 -i certificate.p12 | pbcopy
```

### Ad-Hoc Signing (Testing Only)

For unsigned distribution or testing without Apple credentials:

```json
{
  "bundle": {
    "macOS": {
      "signingIdentity": "-"
    }
  }
}
```

### GitHub Actions Example

```yaml
- name: Import certificate
  env:
    APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
    APPLE_CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
  run: |
    echo $APPLE_CERTIFICATE | base64 --decode > certificate.p12
    security create-keychain -p actions temp.keychain
    security import certificate.p12 -k temp.keychain -P $APPLE_CERTIFICATE_PASSWORD -T /usr/bin/codesign
    security list-keychains -s temp.keychain
    security unlock-keychain -p actions temp.keychain
    security set-key-partition-list -S apple-tool:,apple: -s -k actions temp.keychain
```

---

## Windows Signing

### Certificate Types

| Type | SmartScreen | Availability |
|------|-------------|--------------|
| OV (Organization Validated) | Builds reputation over time | Before June 1, 2023 |
| EV (Extended Validation) | Immediate trust | Required after June 1, 2023 |

**Note:** Certificates obtained after June 1, 2023 require EV certificates for immediate SmartScreen trust.

### Configuration

**tauri.conf.json:**

```json
{
  "bundle": {
    "windows": {
      "certificateThumbprint": "A1B1A2B2A3B3A4B4A5B5A6B6A7B7A8B8A9B9A0B0",
      "digestAlgorithm": "sha256",
      "timestampUrl": "http://timestamp.sectigo.com"
    }
  }
}
```

### Find Certificate Thumbprint

1. Open certificate details
2. Go to Details tab
3. Find "Thumbprint" field
4. Copy the hex string (remove spaces)

### Common Timestamp URLs

- `http://timestamp.sectigo.com`
- `http://timestamp.digicert.com`
- `http://timestamp.globalsign.com`

### Convert Certificate to PFX

```bash
openssl pkcs12 -export -in cert.cer -inkey private-key.key -out certificate.pfx
```

### Environment Variables for CI/CD

| Variable | Description |
|----------|-------------|
| `WINDOWS_CERTIFICATE` | Base64-encoded `.pfx` file |
| `WINDOWS_CERTIFICATE_PASSWORD` | PFX export password |

### GitHub Actions Example

```yaml
- name: Import Windows certificate
  env:
    WINDOWS_CERTIFICATE: ${{ secrets.WINDOWS_CERTIFICATE }}
    WINDOWS_CERTIFICATE_PASSWORD: ${{ secrets.WINDOWS_CERTIFICATE_PASSWORD }}
  run: |
    echo "$WINDOWS_CERTIFICATE" | base64 --decode > certificate.pfx
    Import-PfxCertificate -FilePath certificate.pfx -CertStoreLocation Cert:\CurrentUser\My -Password (ConvertTo-SecureString -String $env:WINDOWS_CERTIFICATE_PASSWORD -AsPlainText -Force)
  shell: pwsh
```

### Azure Key Vault Signing

For cloud-based signing with Azure Key Vault:

| Variable | Description |
|----------|-------------|
| `AZURE_CLIENT_ID` | Azure AD application client ID |
| `AZURE_CLIENT_SECRET` | Azure AD application secret |
| `AZURE_TENANT_ID` | Azure AD tenant ID |

Configure in `tauri.conf.json`:

```json
{
  "bundle": {
    "windows": {
      "signCommand": "relic sign --key azurekeyvault --file %1"
    }
  }
}
```

### Azure Trusted Signing

For Azure Code Signing service:

```json
{
  "bundle": {
    "windows": {
      "signCommand": "trusted-signing-cli -e <endpoint> -a <account> -c <profile> %1"
    }
  }
}
```

### Custom Sign Command

For other signing tools or cross-platform builds:

```json
{
  "bundle": {
    "windows": {
      "signCommand": "your-signing-tool --sign %1"
    }
  }
}
```

The `%1` placeholder is replaced with the executable path.

---

## Quick Reference: All Environment Variables

### Android
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`
- `ANDROID_KEY_BASE64`

### iOS (Manual)
- `IOS_CERTIFICATE`
- `IOS_CERTIFICATE_PASSWORD`
- `IOS_MOBILE_PROVISION`

### iOS/macOS (API Key)
- `APPLE_API_ISSUER`
- `APPLE_API_KEY`
- `APPLE_API_KEY_PATH`

### macOS (Certificate)
- `APPLE_CERTIFICATE`
- `APPLE_CERTIFICATE_PASSWORD`
- `APPLE_SIGNING_IDENTITY`

### macOS (Apple ID Notarization)
- `APPLE_ID`
- `APPLE_PASSWORD`
- `APPLE_TEAM_ID`

### Linux
- `SIGN`
- `SIGN_KEY`
- `APPIMAGETOOL_SIGN_PASSPHRASE`
- `APPIMAGETOOL_FORCE_SIGN`

### Windows
- `WINDOWS_CERTIFICATE`
- `WINDOWS_CERTIFICATE_PASSWORD`

### Azure (Windows)
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_TENANT_ID`
