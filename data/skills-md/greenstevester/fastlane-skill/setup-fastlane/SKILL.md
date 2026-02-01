---
name: setup-fastlane
description: Set up Fastlane for iOS/macOS app automation
argument-hint: [project-path]
allowed-tools: Bash, Read, Write, Edit, Glob
---

## Fastlane Setup (One-Time)

```
┌─────────────────────────────────────────────────────────────────┐
│  ONE-TIME SETUP                                                 │
│  ══════════════                                                 │
│  After this, you'll have:                                       │
│                                                                 │
│    fastlane ios test    → Run tests                             │
│    fastlane ios beta    → Upload to TestFlight                  │
│    fastlane ios release → Submit to App Store                   │
│                                                                 │
│  Do this once per project. Takes ~10 minutes.                   │
└─────────────────────────────────────────────────────────────────┘
```

### Environment Check
- Xcode CLI: !`xcode-select -p 2>/dev/null && echo "✓" || echo "✗ Run: xcode-select --install"`
- Homebrew: !`brew --version 2>/dev/null | head -1 || echo "✗ Run: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""`
- Fastlane: !`fastlane --version 2>/dev/null | grep -o "fastlane [0-9.]*" | head -1 || echo "✗ Run: brew install fastlane"`

### Your Project
- Project: !`find . -maxdepth 2 -name "*.xcodeproj" 2>/dev/null | head -1 || echo "None found"`
- Workspace: !`find . -maxdepth 2 -name "*.xcworkspace" ! -path "*/.build/*" ! -path "*/xcodeproj/*" 2>/dev/null | head -1 || echo "None"`
- Bundle ID: !`grep -r "PRODUCT_BUNDLE_IDENTIFIER" --include="*.pbxproj" . 2>/dev/null | head -1 | sed 's/.*= //' | tr -d '";' || echo "Not found"`
- Team ID: !`grep -r "DEVELOPMENT_TEAM" --include="*.pbxproj" . 2>/dev/null | head -1 | sed 's/.*= //' | tr -d '";' || echo "Not found"`

### Target: ${ARGUMENTS:-current directory}

---

## Step 1: Install Fastlane

```bash
brew install fastlane
```

> **Why Homebrew?** Bundler 4.x broke Fastlane's Ruby dependencies. Homebrew avoids all version conflicts.

---

## Step 2: Create Configuration Files

### `fastlane/Appfile`
```ruby
app_identifier("{{BUNDLE_ID}}")  # Your bundle ID
apple_id("{{APPLE_ID}}")         # Your Apple ID email
team_id("{{TEAM_ID}}")           # Your team ID
```

### `fastlane/Fastfile`
```ruby
default_platform(:ios)

platform :ios do
  desc "Run tests"
  lane :test do
    scan(scheme: "{{SCHEME}}")
  end

  desc "Upload to TestFlight"
  lane :beta do
    increment_build_number
    gym(scheme: "{{SCHEME}}", export_method: "app-store")
    pilot(skip_waiting_for_build_processing: true)
  end

  desc "Submit to App Store"
  lane :release do
    increment_build_number
    gym(scheme: "{{SCHEME}}", export_method: "app-store")
    deliver(submit_for_review: false, force: true)
  end
end
```

Replace `{{SCHEME}}` with your app's scheme name (usually the app name).

---

## Step 3: Set Up Metadata (Optional)

Download your existing App Store listing:
```bash
fastlane deliver download_metadata
fastlane deliver download_screenshots
```

This creates `fastlane/metadata/` with editable text files for your app description, keywords, etc.

---

## You're Done!

```bash
# Verify setup
fastlane lanes

# Run your first lane
fastlane ios test
```

### Quick Reference
| Command | What it does |
|---------|--------------|
| `fastlane ios test` | Run tests |
| `fastlane ios beta` | Build + TestFlight |
| `fastlane ios release` | Build + App Store |
| `fastlane deliver download_metadata` | Fetch App Store listing |

---

## Next Steps

- **Code signing issues?** Ask: "Set up Match for code signing"
- **Need screenshots?** Ask: "Automate my App Store screenshots"
- **CI/CD setup?** See [Xcode Cloud guide](../../docs/xcode-cloud.md)
