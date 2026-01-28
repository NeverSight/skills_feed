---
name: react-native-deployment
description: Master deployment - EAS Build, Fastlane, App Store, Play Store, and OTA updates
sasmp_version: "1.3.0"
bonded_agent: 07-react-native-deploy
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-01"
---

# React Native Deployment Skill

> Learn to build, sign, and deploy React Native apps to iOS App Store, Google Play Store, and OTA update systems.

## Prerequisites

- React Native app ready for production
- Apple Developer Account (iOS)
- Google Play Developer Account (Android)
- Basic understanding of CI/CD

## Learning Objectives

After completing this skill, you will be able to:
- [ ] Configure EAS Build for production
- [ ] Set up iOS code signing
- [ ] Generate Android keystores
- [ ] Submit to App Store and Play Store
- [ ] Implement OTA updates with EAS Update

---

## Topics Covered

### 1. EAS Build Setup
```bash
# Install EAS CLI
npm install -g eas-cli

# Login
eas login

# Configure
eas build:configure

# Build
eas build --platform all --profile production
```

### 2. EAS Configuration
```json
// eas.json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "production": {
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {
      "ios": { "appleId": "your@email.com" },
      "android": { "track": "production" }
    }
  }
}
```

### 3. iOS Code Signing
```bash
# With Fastlane Match
fastlane match appstore

# Manual (Xcode)
# 1. Create certificate in Apple Developer
# 2. Create provisioning profile
# 3. Download and install in Xcode
```

### 4. Android Keystore
```bash
# Generate keystore
keytool -genkeypair -v -storetype PKCS12 \
  -keystore release.keystore \
  -alias my-key-alias \
  -keyalg RSA -keysize 2048 -validity 10000

# NEVER commit keystore or passwords
```

### 5. OTA Updates
```typescript
// Check for updates
import * as Updates from 'expo-updates';

async function checkUpdates() {
  const update = await Updates.checkForUpdateAsync();
  if (update.isAvailable) {
    await Updates.fetchUpdateAsync();
    await Updates.reloadAsync();
  }
}
```

### 6. Submission Commands
```bash
# Build and submit in one command
eas build --platform all --profile production --auto-submit

# Submit existing build
eas submit --platform ios --latest
eas submit --platform android --latest
```

---

## Quick Start Example

```bash
# 1. Configure EAS
eas build:configure

# 2. Build for production
eas build --platform all --profile production

# 3. Submit to stores
eas submit --platform all --latest

# 4. Push OTA update
eas update --branch production --message "Bug fixes"
```

---

## Pre-Submission Checklist

### iOS App Store
- [ ] App icon (1024x1024)
- [ ] Screenshots (all sizes)
- [ ] Privacy policy URL
- [ ] App review information
- [ ] Build uploaded to TestFlight

### Google Play Store
- [ ] Hi-res icon (512x512)
- [ ] Feature graphic (1024x500)
- [ ] Screenshots (phone + tablet)
- [ ] Content rating completed
- [ ] Signed AAB uploaded

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Code signing failed | Certificate mismatch | Regenerate certs |
| Build number conflict | Not incremented | Use autoIncrement |
| Upload rejected | Missing metadata | Complete all fields |

---

## Validation Checklist

- [ ] Build succeeds for both platforms
- [ ] App installs from TestFlight/Internal
- [ ] OTA updates apply correctly
- [ ] Store listing is complete

---

## Usage

```
Skill("react-native-deployment")
```

**Bonded Agent**: `07-react-native-deploy`
