---
name: gplay-submission-checks
description: Pre-submission validation for Google Play releases covering metadata, screenshots, bundle integrity, data safety, and policy compliance. Use when preparing a release to avoid rejections and catch issues before submitting.
---

# Google Play Submission Checks

Use this skill to validate everything before submitting a release to Google Play, reducing rejections and failed edits.

## Preconditions
- Auth configured (`gplay auth login` or `GPLAY_SERVICE_ACCOUNT` env var).
- Package name known (`--package` or `GPLAY_PACKAGE`).
- AAB/APK built and signed.
- Service account has at least "Release Manager" permission.

## Pre-submission Checklist

### 1. Validate Bundle Integrity

```bash
gplay validate bundle --file app-release.aab
```

Checks:
- File exists and is readable
- File has `.aab` extension
- Valid ZIP archive structure
- Contains required bundle components (manifest, resources, dex)

If using APK instead:
```bash
gplay validate bundle --file app-release.apk
```

### 2. Validate Store Listing Metadata

```bash
gplay validate listing --dir ./metadata
```

Checks:
- **Title**: max 30 characters
- **Short description**: max 80 characters
- **Full description**: max 4000 characters
- Required fields present
- Valid UTF-8 encoding

Validate a specific locale:
```bash
gplay validate listing --dir ./metadata --locale en-US
```

For JSON format metadata:
```bash
gplay validate listing --dir ./metadata --format json
```

### 3. Validate Screenshots

```bash
gplay validate screenshots --dir ./metadata
```

Checks:
- Minimum 2 screenshots per device type
- Maximum 8 screenshots per device type
- Valid image formats (PNG, JPEG)
- Files are readable

Validate for a specific locale:
```bash
gplay validate screenshots --dir ./metadata --locale en-US
```

### 4. Verify Existing Listings on Play Store

Compare local metadata against what is live:
```bash
gplay sync diff-listings \
  --package com.example.app \
  --dir ./metadata
```

Check all configured locales:
```bash
EDIT_ID=$(gplay edits create --package com.example.app | jq -r '.id')
gplay listings list --package com.example.app --edit $EDIT_ID --output table
```

### 5. Data Safety Declaration

Ensure the data safety form is complete. Missing or inaccurate data safety declarations are a common rejection reason.

```bash
gplay data-safety update \
  --package com.example.app \
  --json @data-safety.json
```

### 6. Version Code Check

The version code must be strictly higher than all previous releases on every track. Check current track status:

```bash
gplay tracks list --package com.example.app --output table
```

Get details for a specific track:
```bash
EDIT_ID=$(gplay edits create --package com.example.app | jq -r '.id')
gplay tracks get --package com.example.app --edit $EDIT_ID --track production --output table
```

### 7. Deobfuscation / Mapping File

Upload ProGuard/R8 mapping files so crash reports in Play Console are readable:

```bash
gplay deobfuscation upload \
  --package com.example.app \
  --version-code 42 \
  --file mapping.txt
```

Without mapping files, crash stack traces in Android Vitals will be obfuscated and unusable.

### 8. Dry Run the Release

The safest pre-submission check. Performs the full release pipeline without committing:

```bash
gplay release \
  --package com.example.app \
  --track production \
  --bundle app-release.aab \
  --release-notes @release-notes.json \
  --dry-run
```

This will:
- Create an edit
- Upload the bundle
- Configure the track
- **Validate** the edit (catches API-level errors)
- Discard the edit without committing

If the dry run succeeds, the real release will succeed.

### 9. Edit Validation (Manual Sequence)

When using the manual edit workflow, always validate before committing:

```bash
EDIT_ID=$(gplay edits create --package com.example.app | jq -r '.id')

# ... upload bundle, update tracks, etc. ...

# Validate the edit (catches all server-side issues)
gplay edits validate --package com.example.app --edit $EDIT_ID

# Only commit if validation passes
gplay edits commit --package com.example.app --edit $EDIT_ID
```

## Content Policy Compliance

### Target API Level
Google Play requires apps to target a recent Android API level. As of 2025:
- New apps: must target API level 34 (Android 14) or higher
- App updates: must target API level 34 or higher

Check your `build.gradle` or `build.gradle.kts`:
```
android {
    defaultConfig {
        targetSdkVersion 34  // or targetSdk = 34
    }
}
```

Builds targeting older API levels will be rejected by the Play Console.

### Permissions Declarations
Sensitive permissions require justification in the Play Console:
- `ACCESS_FINE_LOCATION` / `ACCESS_BACKGROUND_LOCATION`
- `READ_CONTACTS`, `READ_CALL_LOG`, `READ_SMS`
- `CAMERA`, `RECORD_AUDIO`
- `REQUEST_INSTALL_PACKAGES`
- `QUERY_ALL_PACKAGES`

Remove any permissions your app does not actually need. Unused sensitive permissions are a top rejection reason.

### Data Safety Form
All apps must have a complete data safety section. Common data types to declare:
- Personal info (name, email, phone)
- Location (approximate, precise)
- Financial info (purchase history)
- App activity (in-app search, other user-generated content)
- Device identifiers (advertising ID)

### App Content Ratings
Ensure your content rating questionnaire is completed in Play Console. Missing ratings block distribution.

## Screenshot Requirements by Device Type

| Device Type | Image Type | Min | Max | Min Resolution |
|-------------|-----------|-----|-----|----------------|
| Phone | `phoneScreenshots` | 2 | 8 | 320px (min side) |
| 7-inch Tablet | `sevenInchScreenshots` | 0 | 8 | 320px (min side) |
| 10-inch Tablet | `tenInchScreenshots` | 0 | 8 | 320px (min side) |
| Android TV | `tvScreenshots` | 0 | 8 | 1280x720 |
| Wear OS | `wearScreenshots` | 0 | 8 | 320px (min side) |

Additional image assets:
| Asset | Type | Required |
|-------|------|----------|
| Feature Graphic | `featureGraphic` | Yes (for featuring) |
| Promo Graphic | `promoGraphic` | No |
| Icon | `icon` | Set via Play Console |
| TV Banner | `tvBanner` | Required for TV apps |

## Common Rejection Reasons and Fixes

### 1. "Version code already exists"
**Cause**: The version code in your bundle matches an existing release.
**Fix**: Increment `versionCode` in `build.gradle` and rebuild.

### 2. "APK/Bundle targets an SDK below the required level"
**Cause**: `targetSdkVersion` is too low.
**Fix**: Update `targetSdkVersion` to 34 or higher and rebuild.

### 3. "Data safety form incomplete"
**Cause**: The data safety declaration is missing or incomplete.
**Fix**: Complete the data safety form in Play Console or update via CLI:
```bash
gplay data-safety update --package com.example.app --json @data-safety.json
```

### 4. "Screenshots missing for required device type"
**Cause**: Phone screenshots are required for all apps.
**Fix**: Add at least 2 phone screenshots:
```bash
EDIT_ID=$(gplay edits create --package com.example.app | jq -r '.id')
gplay images upload \
  --package com.example.app \
  --edit $EDIT_ID \
  --locale en-US \
  --type phoneScreenshots \
  --file screenshot1.png
```

### 5. "Release notes missing for default locale"
**Cause**: No "What's New" text for the default language.
**Fix**: Include release notes in the release command:
```bash
gplay release \
  --package com.example.app \
  --track production \
  --bundle app.aab \
  --release-notes '{"en-US": "Bug fixes and improvements"}'
```

### 6. "Signing key mismatch"
**Cause**: The bundle is signed with a different key than what Play Console expects.
**Fix**: Use the same upload key configured in Play App Signing. Check your keystore configuration.

### 7. "Deobfuscation file too large"
**Cause**: Mapping file exceeds 300 MB limit.
**Fix**: Strip unused mappings or compress the file.

## Pre-launch Report

Google Play runs automated tests on your app before review (pre-launch report). Common issues surfaced:
- **Crashes on launch**: App crashes on one or more test devices
- **Security vulnerabilities**: Known CVEs in dependencies
- **Accessibility issues**: Missing content descriptions, small touch targets
- **Performance warnings**: Slow startup, excessive wake locks

Check pre-launch reports in Play Console after uploading to any track. Address critical issues before promoting to production.

## Full Pre-submission Pipeline

```bash
#!/bin/bash
# pre-submission-checks.sh

PACKAGE="com.example.app"
BUNDLE="app-release.aab"
METADATA_DIR="./metadata"
RELEASE_NOTES="release-notes.json"
MAPPING="app/build/outputs/mapping/release/mapping.txt"

echo "=== Step 1: Validate bundle ==="
gplay validate bundle --file "$BUNDLE" --output table

echo "=== Step 2: Validate listings ==="
gplay validate listing --dir "$METADATA_DIR" --output table

echo "=== Step 3: Validate screenshots ==="
gplay validate screenshots --dir "$METADATA_DIR" --output table

echo "=== Step 4: Diff listings against Play Store ==="
gplay sync diff-listings --package "$PACKAGE" --dir "$METADATA_DIR" --output table

echo "=== Step 5: Dry run release ==="
gplay release \
  --package "$PACKAGE" \
  --track production \
  --bundle "$BUNDLE" \
  --release-notes "@$RELEASE_NOTES" \
  --listings-dir "$METADATA_DIR" \
  --screenshots-dir "$METADATA_DIR" \
  --dry-run \
  --output table

echo "=== Step 6: Upload mapping file ==="
gplay deobfuscation upload \
  --package "$PACKAGE" \
  --version-code 42 \
  --file "$MAPPING"

echo "=== All checks passed. Ready to release. ==="
```

## CI/CD Integration

Add these checks to your CI pipeline to catch issues before they reach Play Console:

```yaml
# GitHub Actions example
- name: Validate bundle
  run: gplay validate bundle --file app/build/outputs/bundle/release/app-release.aab

- name: Validate metadata
  run: gplay validate listing --dir metadata/

- name: Validate screenshots
  run: gplay validate screenshots --dir metadata/

- name: Dry run release
  run: |
    gplay release \
      --package ${{ secrets.PACKAGE_NAME }} \
      --track internal \
      --bundle app/build/outputs/bundle/release/app-release.aab \
      --dry-run
  env:
    GPLAY_SERVICE_ACCOUNT: ${{ secrets.GPLAY_SERVICE_ACCOUNT_PATH }}
```

## Agent Behavior
- Always run `gplay validate` commands before attempting a release.
- Use `--dry-run` as the final gate before real releases.
- Always confirm exact flags with `--help` before running commands.
- Use `--output table` for human-readable validation output.
- When multiple validation steps fail, report all failures together rather than stopping at the first one.
- Check version code conflicts by listing tracks before releasing.
- Remind the user about data safety declarations if they have not mentioned them.

## Notes
- `gplay validate` commands run locally and do not require API calls.
- `gplay release --dry-run` creates a real edit session but discards it after validation.
- `gplay edits validate` is the server-side equivalent, catching issues that local validation cannot.
- Always use `--help` to verify flags for the exact command.
- Use `--output table` for human-readable output; default is JSON.
