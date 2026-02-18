---
name: gplay-gradle-build
description: Build, sign, and package Android apps with Gradle before uploading to Google Play. Use when asked to create an APK or AAB, configure signing, or set up build pipelines.
---

# Gradle Build for Google Play

Use this skill when you need to build an Android app before uploading to Play Store.

## Build Types

### App Bundle (AAB) - Recommended
App Bundles are required for new apps on Google Play:

```bash
./gradlew bundleRelease
```

Output: `app/build/outputs/bundle/release/app-release.aab`

### APK - Legacy
For apps not using bundles:

```bash
./gradlew assembleRelease
```

Output: `app/build/outputs/apk/release/app-release.apk`

## Signing Configuration

### build.gradle (app level)
```groovy
android {
    signingConfigs {
        release {
            storeFile file(System.getenv("KEYSTORE_FILE") ?: "release.keystore")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### Environment Variables
```bash
export KEYSTORE_FILE=/path/to/release.keystore
export KEYSTORE_PASSWORD=your_keystore_password
export KEY_ALIAS=your_key_alias
export KEY_PASSWORD=your_key_password

./gradlew bundleRelease
```

## Version Management

### gradle.properties
```properties
VERSION_NAME=1.2.3
VERSION_CODE=123
```

### build.gradle
```groovy
android {
    defaultConfig {
        versionCode project.property('VERSION_CODE').toInteger()
        versionName project.property('VERSION_NAME')
    }
}
```

### Increment version
```bash
# Read current version
CURRENT_VERSION=$(grep VERSION_CODE gradle.properties | cut -d'=' -f2)
NEW_VERSION=$((CURRENT_VERSION + 1))

# Update gradle.properties
sed -i "" "s/VERSION_CODE=$CURRENT_VERSION/VERSION_CODE=$NEW_VERSION/" gradle.properties

# Build
./gradlew bundleRelease
```

## ProGuard/R8 Configuration

### Enable R8 (default in AGP 3.4+)
```groovy
buildTypes {
    release {
        minifyEnabled true
        shrinkResources true
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
}
```

### Generate mapping file
Mapping file location: `app/build/outputs/mapping/release/mapping.txt`

Upload to Play Console for crash symbolication:
```bash
gplay deobfuscation upload \
  --package com.example.app \
  --edit $EDIT_ID \
  --apk-version 123 \
  --type proguard \
  --file app/build/outputs/mapping/release/mapping.txt
```

## Build Variants

### Product Flavors
```groovy
android {
    flavorDimensions "version"
    productFlavors {
        free {
            dimension "version"
            applicationIdSuffix ".free"
        }
        paid {
            dimension "version"
        }
    }
}
```

### Build specific flavor
```bash
./gradlew bundleFreeRelease
./gradlew bundlePaidRelease
```

## CI/CD Build

### GitHub Actions Example
```yaml
- name: Build Release AAB
  run: |
    echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > release.keystore
    export KEYSTORE_FILE=release.keystore
    export KEYSTORE_PASSWORD="${{ secrets.KEYSTORE_PASSWORD }}"
    export KEY_ALIAS="${{ secrets.KEY_ALIAS }}"
    export KEY_PASSWORD="${{ secrets.KEY_PASSWORD }}"
    ./gradlew bundleRelease

- name: Upload to Play Store
  env:
    GPLAY_SERVICE_ACCOUNT: ${{ secrets.PLAY_SERVICE_ACCOUNT }}
  run: |
    gplay release \
      --package com.example.app \
      --track internal \
      --bundle app/build/outputs/bundle/release/app-release.aab
```

## Common Build Tasks

### Clean build
```bash
./gradlew clean bundleRelease
```

### Build with specific SDK versions
```bash
./gradlew bundleRelease -PminSdkVersion=21 -PtargetSdkVersion=34
```

### Build without tests
```bash
./gradlew bundleRelease -x test -x lint
```

### Build multiple variants
```bash
./gradlew bundle  # Builds all variants
```

## Troubleshooting

### Build fails with signing errors
```bash
# Verify keystore
keytool -list -v -keystore release.keystore
```

### Check AAB contents
```bash
bundletool build-apks \
  --bundle=app-release.aab \
  --output=output.apks \
  --mode=universal

unzip output.apks
```

### Verify version codes
```bash
./gradlew tasks --all | grep Version
```

## Best Practices

1. **Never commit keystores** - Store in secure location
2. **Use environment variables** for credentials
3. **Enable ProGuard/R8** for release builds
4. **Upload mapping files** after each release
5. **Increment version code** for every build
6. **Test release builds** before uploading
7. **Use App Bundles (AAB)** instead of APKs when possible
