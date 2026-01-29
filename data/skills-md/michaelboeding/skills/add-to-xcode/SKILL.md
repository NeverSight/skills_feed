---
name: add-to-xcode
description: >
  REQUIRED: After creating ANY .swift, .m, .mm, .c, .cpp, or .h file in a directory 
  containing a .xcodeproj, you MUST run add_to_xcode.rb to register it with the project.
  Without this step, the file will NOT appear in Xcode and will NOT compile.
triggers:
  - create swift file
  - create objective-c file
  - add file to xcode
  - new ios file
  - new macos file
  - xcode project
  - .swift
  - .xcodeproj
---

# Add to Xcode

## ⚠️ MANDATORY: Run After Creating Source Files

**Every time you create a `.swift`, `.m`, `.mm`, `.c`, `.cpp`, or `.h` file in an Xcode project, you MUST run:**

```bash
ruby ${CLAUDE_PLUGIN_ROOT}/skills/add-to-xcode/scripts/add_to_xcode.rb <filepath>
```

**If you skip this step:**
- ❌ File will NOT appear in Xcode's navigator
- ❌ File will NOT compile with the app
- ❌ User will have to manually add it

---

## Quick Reference

```bash
# ALWAYS do this after creating any source file:
# Use subshell to get latest version (handles multiple cached versions)
ruby "$(ls -1d ~/.claude/plugins/cache/michaelboeding-skills/skills/*/skills/add-to-xcode/scripts/add_to_xcode.rb 2>/dev/null | sort -V | tail -1)" NewFile.swift
```

---

## Supported File Types

| Extension | Added to Compile Sources |
|-----------|-------------------------|
| `.swift` | ✅ Yes |
| `.m` | ✅ Yes |
| `.mm` | ✅ Yes |
| `.c` | ✅ Yes |
| `.cpp` | ✅ Yes |
| `.h` | ❌ No (reference only) |

## Workflow

### Step 1: Create the file normally

```bash
# Example: Create a new Swift file
cat > Sources/Features/MyFeature.swift << 'EOF'
import Foundation

class MyFeature {
    // Implementation
}
EOF
```

### Step 2: Add to Xcode project

```bash
ruby ${CLAUDE_PLUGIN_ROOT}/skills/add-to-xcode/scripts/add_to_xcode.rb Sources/Features/MyFeature.swift
```

**Output:**
```
✓ Added Sources/Features/MyFeature.swift to MyApp.xcodeproj (target: MyApp)
```

## What the Script Does

1. **Finds the `.xcodeproj`** - Searches current directory and parents
2. **Creates group hierarchy** - Matches the file's directory structure
3. **Adds file reference** - Registers with the project
4. **Adds to build target** - Source files (`.swift`, `.m`, `.mm`, `.c`, `.cpp`) are added to the first target's compile sources

## Requirements

Ruby with the `xcodeproj` gem:

```bash
gem install xcodeproj
```

## Examples

### Adding a new Swift file

```bash
# Create the file
cat > MyApp/ViewModels/ProfileViewModel.swift << 'EOF'
import SwiftUI

@Observable
class ProfileViewModel {
    var name: String = ""
    var email: String = ""
}
EOF

# Add to Xcode
ruby ${CLAUDE_PLUGIN_ROOT}/skills/add-to-xcode/scripts/add_to_xcode.rb MyApp/ViewModels/ProfileViewModel.swift
```

### Adding a header file

```bash
# Create header
cat > MyApp/Bridge/MyApp-Bridging-Header.h << 'EOF'
#import <SomeLibrary/SomeLibrary.h>
EOF

# Add to Xcode (headers are added but not to compile sources)
ruby ${CLAUDE_PLUGIN_ROOT}/skills/add-to-xcode/scripts/add_to_xcode.rb MyApp/Bridge/MyApp-Bridging-Header.h
```

### Adding Objective-C files

```bash
# Create implementation
cat > MyApp/Legacy/LegacyManager.m << 'EOF'
#import "LegacyManager.h"

@implementation LegacyManager
// Implementation
@end
EOF

# Add to Xcode
ruby ${CLAUDE_PLUGIN_ROOT}/skills/add-to-xcode/scripts/add_to_xcode.rb MyApp/Legacy/LegacyManager.m
```

## Agent Integration

When working in an Xcode project, agents should:

1. **Check for `.xcodeproj`** before creating source files
2. **Create the file** using standard file creation
3. **Run add_to_xcode.rb** immediately after file creation

```bash
# Pattern for agents:
# 1. Create file
cat > NewFile.swift << 'EOF'
// content
EOF

# 2. Register with Xcode
ruby ${CLAUDE_PLUGIN_ROOT}/skills/add-to-xcode/scripts/add_to_xcode.rb NewFile.swift
```

## Troubleshooting

### "No .xcodeproj found"
- Make sure you're running from within the Xcode project directory or a subdirectory

### "gem not found: xcodeproj"
- Install with: `gem install xcodeproj`
- On macOS with system Ruby, you may need: `sudo gem install xcodeproj`

### File added but not compiling
- Check that the file extension is recognized (`.swift`, `.m`, `.mm`, `.c`, `.cpp`)
- Verify the target exists and has a source build phase
- Header files (`.h`) are not added to compile sources (this is correct)

## Related Skills

| Skill | Use Case |
|-------|----------|
| `ios-to-android` | Convert iOS code to Android |
| `android-to-ios` | Convert Android code to iOS |
