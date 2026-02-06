---
name: debug:react-native
description: Debug React Native issues systematically. Use when encountering native module errors like "Native module cannot be null", Metro bundler issues including port conflicts and cache corruption, platform-specific build failures for iOS CocoaPods or Android Gradle, bridge communication problems, Hermes engine bytecode compilation failures, red screen fatal errors, or New Architecture migration issues with TurboModules and Fabric renderer.
---

# React Native Debugging Guide

You are an expert React Native debugger. When the user encounters React Native issues, follow this systematic four-phase approach to identify, diagnose, and resolve the problem efficiently.

## Common Error Patterns

### Red Screen Errors (Fatal Errors)
- **"Unable to load script"**: Metro bundler connection issues
- **"Invariant Violation"**: React component lifecycle or rendering errors
- **"Module not found"**: Missing or incorrectly linked dependencies
- **"Native module cannot be null"**: Native module linking failures
- **"Text strings must be rendered within a <Text> component"**: JSX structure errors

### Yellow Box Warnings
- Deprecation warnings for outdated APIs
- Performance warnings (excessive re-renders)
- Unhandled promise rejections
- Console.warn statements

### Metro Bundler Issues
- Port 8081 already in use
- Cache corruption causing stale bundles
- Watchman file watching limits exceeded (EMFILE errors)
- Symlink resolution failures
- Module resolution failures

### Native Module Linking Errors
- "RCTBridge required dispatch_sync to load" (iOS)
- "Native module XYZ tried to override" conflicts
- CocoaPods installation failures
- Gradle build failures
- Auto-linking not working properly

### Bridge Communication Failures
- Serialization errors for complex objects
- Async bridge message queue overflow
- Threading violations (UI updates from background thread)
- Turbo Modules migration issues (New Architecture)

### iOS-Specific Build Failures
- Xcode version incompatibility
- CocoaPods cache corruption
- Provisioning profile issues
- Bitcode compilation errors
- M1/M2 architecture issues (Rosetta)

### Android-Specific Build Failures
- Gradle version mismatches
- Android SDK path not configured
- NDK version conflicts
- R8/ProGuard minification errors
- MultiDex issues

### Hermes Engine Issues
- Bytecode compilation failures
- Incompatible native modules with Hermes
- Source map issues for stack traces
- Memory leaks specific to Hermes

## Debugging Tools

### React Native DevTools (Primary - RN 0.76+)
The default debugging tool for React Native. Access via Dev Menu or press "j" from CLI.
- Console panel for JavaScript logs
- React DevTools integration for component inspection
- Network inspection
- Performance profiling

### Flipper (Comprehensive Desktop Debugger)
Meta's desktop debugging platform with plugin architecture:
- **Layout Inspector**: Visualize component hierarchies
- **Network Inspector**: Monitor API requests/responses
- **Database Browser**: View AsyncStorage, SQLite
- **Log Viewer**: Centralized JavaScript and native logs
- **React DevTools Integration**: Inspect component trees and hooks
- **Hermes Debugger**: Debug Hermes bytecode

### Reactotron (State Management Focus)
Free, open-source desktop app by Infinite Red:
- Redux/MobX state tracking
- API request/response logging
- Custom command execution
- Benchmark timing
- Error stack traces

### React Native Debugger (All-in-One)
Combines multiple debugging features:
- Chrome DevTools integration
- React DevTools
- Redux DevTools
- Network inspection

### Native IDE Tools
- **Xcode**: iOS crash logs, memory profiler, Instruments
- **Android Studio**: Logcat, Layout Inspector, Profiler, Memory Analyzer

### Console and Logging
- `console.log()`, `console.warn()`, `console.error()`
- LogBox for structured error/warning display
- Remote debugging via Chrome DevTools
- Structured logging with severity levels

## The Four Phases of React Native Debugging

### Phase 1: Information Gathering

Before attempting any fixes, systematically collect diagnostic information:

```bash
# 1. Check React Native environment health
npx react-native doctor

# 2. Get React Native version info
npx react-native info

# 3. Check Node.js and npm/yarn versions
node --version
npm --version  # or: yarn --version

# 4. Verify Metro bundler status
# Check if port 8081 is in use
lsof -i :8081  # macOS/Linux
netstat -ano | findstr :8081  # Windows

# 5. Check Watchman status (file watching)
watchman version
watchman watch-list

# 6. iOS: Check CocoaPods version
pod --version
cd ios && pod outdated

# 7. Android: Check Gradle and SDK
cd android && ./gradlew --version
echo $ANDROID_HOME
```

**Ask the user:**
1. What is the exact error message (copy full stack trace)?
2. When did the error start occurring?
3. Did you recently update any dependencies or React Native version?
4. Does the error occur on iOS, Android, or both?
5. Is this a development build or production build?
6. Are you using Expo or bare React Native?
7. Is Hermes enabled?

### Phase 2: Error Classification and Diagnosis

Classify the error into one of these categories:

#### JavaScript Errors
**Symptoms**: Red screen with JS stack trace, errors in console
**Diagnosis**:
```bash
# Check for syntax errors
npx eslint src/

# Verify TypeScript compilation (if using TS)
npx tsc --noEmit

# Check for circular dependencies
npx madge --circular src/
```

#### Build/Compilation Errors
**Symptoms**: Build fails before app launches
**Diagnosis**:
```bash
# iOS: Clean and rebuild
cd ios && xcodebuild clean
cd ios && pod deintegrate && pod install

# Android: Clean Gradle
cd android && ./gradlew clean
cd android && ./gradlew --refresh-dependencies
```

#### Runtime/Native Errors
**Symptoms**: Crash after launch, native stack trace
**Diagnosis**:
```bash
# iOS: Check Xcode console and crash logs
# Open Xcode > Window > Devices and Simulators > View Device Logs

# Android: Check Logcat
adb logcat *:E | grep -E "(ReactNative|RN|React)"
```

#### Metro/Bundler Errors
**Symptoms**: "Unable to load script", bundling failures
**Diagnosis**:
```bash
# Check Metro process
ps aux | grep metro

# Verify cache state
ls -la $TMPDIR/metro-*
ls -la node_modules/.cache/
```

#### Dependency/Linking Errors
**Symptoms**: "Module not found", "Native module cannot be null"
**Diagnosis**:
```bash
# Check installed dependencies
npm ls  # or: yarn list

# Verify native module linking (RN < 0.60)
npx react-native link

# Check auto-linking (RN >= 0.60)
npx react-native config
```

### Phase 3: Resolution Strategies

Apply fixes based on error classification:

#### The Nuclear Option (Clean Everything)
When nothing else works, perform a complete clean:

```bash
# 1. Stop all processes
# Kill Metro bundler (Ctrl+C or)
lsof -ti:8081 | xargs kill -9

# 2. Clear JavaScript caches
rm -rf node_modules
rm -rf $TMPDIR/react-*
rm -rf $TMPDIR/metro-*
rm -rf $TMPDIR/haste-map-*
watchman watch-del-all

# 3. Clear iOS caches
cd ios
rm -rf Pods
rm -rf ~/Library/Caches/CocoaPods
rm -rf ~/Library/Developer/Xcode/DerivedData
pod cache clean --all
pod deintegrate
pod setup
pod install
cd ..

# 4. Clear Android caches
cd android
./gradlew clean
rm -rf .gradle
rm -rf app/build
rm -rf ~/.gradle/caches
cd ..

# 5. Reinstall dependencies
npm cache clean --force  # or: yarn cache clean
npm install  # or: yarn install

# 6. Rebuild
npx react-native start --reset-cache
# In another terminal:
npx react-native run-ios  # or: run-android
```

#### Metro Bundler Fixes

```bash
# Reset Metro cache
npx react-native start --reset-cache

# Change Metro port if 8081 is occupied
npx react-native start --port 8082

# Kill process using port 8081
lsof -ti:8081 | xargs kill -9  # macOS/Linux
# Windows: Use Resource Monitor to find and kill process

# Fix Watchman issues (EMFILE: too many open files)
watchman watch-del-all
watchman shutdown-server
# Increase file limit (macOS)
echo kern.maxfiles=10485760 | sudo tee -a /etc/sysctl.conf
echo kern.maxfilesperproc=1048576 | sudo tee -a /etc/sysctl.conf
sudo sysctl -w kern.maxfiles=10485760
sudo sysctl -w kern.maxfilesperproc=1048576
ulimit -n 65536
```

#### iOS-Specific Fixes

```bash
# CocoaPods reinstall
cd ios
pod deintegrate
pod cache clean --all
rm Podfile.lock
pod install --repo-update
cd ..

# Xcode clean build
cd ios
xcodebuild clean -workspace YourApp.xcworkspace -scheme YourApp
cd ..

# M1/M2 Mac issues (run with Rosetta)
# Open Terminal via Rosetta, then:
arch -x86_64 pod install

# Fix provisioning/signing issues
# Open Xcode > Signing & Capabilities > Select team

# Reset iOS Simulator
xcrun simctl shutdown all
xcrun simctl erase all
```

#### Android-Specific Fixes

```bash
# Set Android SDK path
export ANDROID_HOME=~/Library/Android/sdk  # macOS
export ANDROID_HOME=~/Android/Sdk  # Linux
# Add to PATH
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Gradle clean and rebuild
cd android
./gradlew clean
./gradlew assembleDebug --stacktrace
cd ..

# Fix Gradle wrapper issues
cd android
rm -rf .gradle
./gradlew wrapper --gradle-version=8.3
cd ..

# Accept Android SDK licenses
yes | sdkmanager --licenses

# ADB issues
adb kill-server
adb start-server
adb devices
```

#### Native Module Linking Fixes

```bash
# For React Native >= 0.60 (auto-linking)
cd ios && pod install && cd ..
npx react-native run-ios

# For React Native < 0.60 (manual linking)
npx react-native link <package-name>

# Verify linking configuration
npx react-native config

# Rebuild after linking
cd android && ./gradlew clean && cd ..
cd ios && pod install && cd ..
```

#### Hermes Engine Fixes

```bash
# Verify Hermes is enabled (check android/app/build.gradle)
# hermesEnabled: true

# Clean Hermes bytecode cache
cd android && ./gradlew clean && cd ..

# iOS: Reinstall pods with Hermes
cd ios
pod deintegrate
pod install
cd ..

# Disable Hermes temporarily to test
# android/gradle.properties: hermesEnabled=false
# ios/Podfile: :hermes_enabled => false
```

#### Dependency Conflict Resolution

```bash
# Check for duplicate packages
npm ls <package-name>

# Force resolution with npm
# Add to package.json:
# "overrides": { "problematic-package": "desired-version" }
npm install

# Force resolution with yarn
# Add to package.json:
# "resolutions": { "problematic-package": "desired-version" }
yarn install

# Deduplicate dependencies
npm dedupe  # or: yarn dedupe
```

### Phase 4: Verification and Prevention

After applying fixes, verify the solution:

```bash
# 1. Run doctor again
npx react-native doctor

# 2. Start fresh Metro instance
npx react-native start --reset-cache

# 3. Run on both platforms
npx react-native run-ios
npx react-native run-android

# 4. Run tests
npm test  # or: yarn test

# 5. Check for TypeScript errors
npx tsc --noEmit

# 6. Run linter
npx eslint src/ --ext .js,.jsx,.ts,.tsx
```

**Prevention strategies:**
1. Lock dependency versions in package.json
2. Use exact versions for native modules
3. Keep React Native version updated (within major versions)
4. Maintain consistent node_modules across team (use lockfiles)
5. Document native configuration changes
6. Use CI/CD to catch build issues early
7. Enable error boundaries in production
8. Implement crash reporting (Sentry, Crashlytics)

## Quick Reference Commands

```bash
# Environment check
npx react-native doctor
npx react-native info

# Start with cache reset
npx react-native start --reset-cache

# Run on specific platform
npx react-native run-ios
npx react-native run-ios --simulator="iPhone 15 Pro"
npx react-native run-android
npx react-native run-android --deviceId=<device-id>

# iOS specific
cd ios && pod install
cd ios && pod update
cd ios && pod deintegrate && pod install
xcodebuild clean -workspace ios/YourApp.xcworkspace -scheme YourApp

# Android specific
cd android && ./gradlew clean
cd android && ./gradlew assembleDebug --stacktrace
cd android && ./gradlew assembleRelease
adb logcat *:E
adb reverse tcp:8081 tcp:8081

# Process management
lsof -ti:8081 | xargs kill -9  # Kill Metro
watchman watch-del-all
watchman shutdown-server

# Cache clearing
rm -rf node_modules
rm -rf $TMPDIR/react-*
rm -rf $TMPDIR/metro-*
rm -rf ios/Pods
rm -rf android/.gradle
rm -rf android/app/build

# Dependency management
npm cache clean --force
yarn cache clean
npm install
yarn install

# Debugging
npx react-native log-ios
npx react-native log-android
adb shell input keyevent 82  # Open Dev Menu on Android

# Generate release builds
cd android && ./gradlew bundleRelease
cd ios && xcodebuild -workspace YourApp.xcworkspace -scheme YourApp -configuration Release archive
```

## Platform-Specific Debugging

### iOS Debugging Checklist
1. Open Xcode and check Issue Navigator (Cmd+5)
2. Check Console output in Debug area (Cmd+Shift+C)
3. Verify Signing & Capabilities settings
4. Check Podfile and Podfile.lock for version mismatches
5. Review build phases and linked frameworks
6. Use Instruments for memory/CPU profiling
7. Check device logs: Window > Devices and Simulators

### Android Debugging Checklist
1. Open Android Studio and check Build output
2. Check Logcat for errors: View > Tool Windows > Logcat
3. Verify build.gradle dependencies and versions
4. Check AndroidManifest.xml for permissions
5. Review ProGuard rules if using minification
6. Use Android Profiler for performance issues
7. Check `adb devices` for device connectivity

## New Architecture (Fabric + TurboModules)

If using React Native New Architecture:

```bash
# Enable New Architecture (android/gradle.properties)
newArchEnabled=true

# Enable New Architecture (ios/Podfile)
ENV['RCT_NEW_ARCH_ENABLED'] = '1'

# Rebuild after enabling
cd ios && pod install
cd android && ./gradlew clean

# Common New Architecture issues:
# 1. Native modules not compatible - check for TurboModule support
# 2. Fabric renderer issues - verify component compatibility
# 3. Build failures - ensure correct versions of dependencies
```

## Error Handling Best Practices

```typescript
// Implement Error Boundaries
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to error reporting service (Sentry, Crashlytics)
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <FallbackComponent error={this.state.error} />;
    }
    return this.props.children;
  }
}

// Async error handling
const fetchData = async () => {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
    // Report to crash analytics
    throw error;
  }
};
```

## Debugging Workflow Summary

1. **Gather Information**: Run `npx react-native doctor`, collect error messages, identify platform
2. **Classify Error**: JavaScript, Build, Runtime, Metro, or Dependency issue
3. **Apply Targeted Fix**: Use platform-specific commands based on classification
4. **Verify Fix**: Test on both platforms, run tests, check for regressions
5. **Document**: Note what caused the issue and how it was resolved

Remember: Most React Native issues can be resolved by clearing caches and rebuilding. When in doubt, perform the "nuclear option" clean and rebuild.
