---
name: building-apple-platform-products
description: Builds, tests, and archives Swift packages and Xcode projects for Apple platforms. Use when running xcodebuild, swift build, or swift test commands, discovering schemes and targets, or selecting simulator destinations for iOS, macOS, tvOS, watchOS, or visionOS.
---

# Building Apple Platform Products

Build, test, and archive Swift packages and Xcode projects for Apple platforms.

## When to Use This Skill

Use this skill when you need to:
- Build an iOS, macOS, tvOS, watchOS, or visionOS app
- Build a Swift package
- Run unit tests or UI tests
- Create an archive for distribution
- Discover project structure (schemes, targets, configurations)

## Tool Selection

| Project Type | Primary Tool | When to Use |
|--------------|--------------|-------------|
| Standalone `Package.swift` | `swift build` | Libraries, CLI tools, cross-platform Swift (no .xcodeproj) |
| `.xcworkspace` | `xcodebuild -workspace` | CocoaPods or multi-project setups |
| `.xcodeproj` | `xcodebuild` | Standard Xcode projects (including those with SPM dependencies) |

**Important**: The `swift build` / `swift test` commands only work for **standalone Swift packages**. If a Swift package is embedded as a submodule within an Xcode project, you must use `xcodebuild` with the appropriate scheme—the Swift CLI cannot orchestrate builds in that context.

## Project Discovery

Before building, discover the project structure:

```bash
# Find what project files exist
ls Package.swift *.xcworkspace *.xcodeproj 2>/dev/null

# List schemes and targets (auto-detects project)
xcodebuild -list

# Describe package (standalone SPM only)
swift package describe
```

**Note**: When an Xcode project references a local Swift package, each package **target** gets its own scheme (named after the target, not the package). Use these schemes to build individual targets without building the entire app.

For mixed projects, shared schemes, or detailed output parsing, see [project-discovery.md](references/project-discovery.md).

## Swift Package Manager Commands

**Important**: These commands only work for standalone Swift packages, not Swift Package Manager submodules in Xcode projects.

| Goal | Command |
|------|---------|
| Build (debug) | `swift build` |
| Build (release) | `swift build -c release` |
| Run executable | `swift run [<target>]` |
| Run tests | `swift test` |
| Run specific test | `swift test --filter <TestClass.testMethod>` |
| Show binary path | `swift build --show-bin-path` |
| Clean | `swift package clean` |
| Initialize | `swift package init [--type library\|executable]` |

For cross-compilation, Package.swift syntax, or dependency management, see [swift-package-manager.md](references/swift-package-manager.md).

## xcodebuild Commands

**Command structure**: `xcodebuild [action] -scheme <name> [-workspace|-project] [options] [BUILD_SETTING=value]`

| Goal | Command |
|------|---------|
| List schemes | `xcodebuild -list` |
| Build | `xcodebuild build -scheme <name>` |
| Test | `xcodebuild test -scheme <name> -destination '<spec>'` |
| Build for testing | `xcodebuild build-for-testing -scheme <name> -destination '<spec>'` |
| Test without build | `xcodebuild test-without-building -scheme <name> -destination '<spec>'` |
| Archive | `xcodebuild archive -scheme <name> -archivePath <path>.xcarchive` |
| Clean | `xcodebuild clean -scheme <name>` |

**Required**: `-scheme` is always required. Add `-workspace` or `-project` when multiple exist.
**For tests**: `-destination` is required for iOS/tvOS/watchOS/visionOS targets.

For build settings, SDK selection, or CI configuration, see [xcodebuild-basics.md](references/xcodebuild-basics.md).

## Common Destinations

| Platform | Destination Specifier |
|----------|----------------------|
| macOS | `'platform=macOS'` |
| iOS Simulator | `'platform=iOS Simulator,name=iPhone 17'` |
| iOS Device | `'platform=iOS,id=<UDID>'` |
| tvOS Simulator | `'platform=tvOS Simulator,name=Apple TV'` |
| watchOS Simulator | `'platform=watchOS Simulator,name=Apple Watch Series 11 (46mm)'` |
| visionOS Simulator | `'platform=visionOS Simulator,name=Apple Vision Pro'` |
| Generic (build only) | `'generic/platform=iOS'` |

**Note**: Simulator names change with each Xcode release. Always verify available simulators:
```bash
xcrun simctl list devices available
```

For all platforms, multiple destinations, or troubleshooting destination errors, see [destinations.md](references/destinations.md).

## Reference Files

| Topic | File | When to Read |
|-------|------|--------------|
| Project Discovery | [project-discovery.md](references/project-discovery.md) | Mixed projects, shared schemes |
| Swift Package Manager | [swift-package-manager.md](references/swift-package-manager.md) | Cross-compilation, Package.swift syntax |
| xcodebuild Basics | [xcodebuild-basics.md](references/xcodebuild-basics.md) | Build settings, SDK selection |
| Destinations | [destinations.md](references/destinations.md) | All platforms, multiple destinations |
| Testing | [testing.md](references/testing.md) | Test filtering, parallel execution, coverage |
| Archiving | [archiving.md](references/archiving.md) | Archive creation |
| Troubleshooting | [troubleshooting.md](references/troubleshooting.md) | Build/test failures, error recovery |

## Common Pitfalls

1. **swift build with Xcode submodules**: Only works for standalone packages. Use `xcodebuild` with the package's scheme instead.
2. **Missing destination for iOS**: Use `-destination 'generic/platform=iOS'` for builds, or specify a simulator for tests.
3. **Unnecessary workspace flag**: Only use `-workspace` for CocoaPods or multi-project setups. Standard projects with SPM dependencies just use `.xcodeproj`.
4. **Case-sensitive scheme names**: Run `xcodebuild -list` to see exact scheme names.
5. **Outdated simulator names**: Names change with Xcode versions. Run `xcrun simctl list devices available`.
6. **Code signing errors**: Add `CODE_SIGNING_ALLOWED=NO` for builds that don't require signing.
