---
name: ios-to-android
description: Use iOS/Swift code as the source of truth and implement the equivalent feature in Android/Kotlin. Understands the feature behavior, data structures, and logic from iOS, then creates idiomatic Android code that matches the target codebase's existing patterns. Use when porting features from iOS to Android or ensuring platform consistency.
---

# iOS to Android: Feature Parity Implementation

Use iOS code as the reference to implement the equivalent Android feature. Not a literal translation - understand what the iOS code does, then implement it idiomatically for Android.

**Use this when:**
- Porting a feature from iOS to Android
- iOS is the "source of truth" for a feature
- Ensuring feature parity between platforms

## Key Principle

```
iOS Code → Understand Feature → Match Android Codebase Patterns → Implement
              (what)                    (how it's done here)
```

**Preserved:** Feature behavior, data structure shapes, business logic, user flows
**Adapted:** Language idioms, frameworks, patterns to match the Android codebase

---

## Workflow

### Step 0: Gather Context

**Ask the user for both pieces of information:**

```
To port a feature from iOS to Android, I need:

1. PATH TO iOS CODEBASE (source of truth)
   Where is the iOS project located?
   Example: /path/to/ios-app or ../ios-app

2. FEATURE TO IMPLEMENT
   What feature or component should I port?
   Example: "UserProfile screen" or "the authentication flow" or "src/Features/Checkout"
```

**Assumptions:**
- Current working directory = Android codebase (target)
- User provides path to iOS codebase (source)

If the user already provided this info, proceed. Otherwise, ask.

### Step 1: Locate the iOS Feature

Navigate to the iOS codebase path and find the relevant files:

1. Go to the iOS path provided
2. Find files related to the feature
3. Read and understand the implementation

### Step 2: Analyze the iOS Code

Thoroughly understand:

| Aspect | What to Extract |
|--------|-----------------|
| **Feature Behavior** | What does this feature do? User-facing functionality |
| **Data Structures** | Models, types, enums - their shapes and relationships |
| **Business Logic** | Core logic, validations, transformations |
| **State Management** | What state exists, how it flows |
| **API Contracts** | Network calls, request/response shapes |
| **UI Flow** | Screens, navigation, user interactions |
| **Edge Cases** | Error handling, loading states, empty states |

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    iOS FEATURE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Feature: [Name]

### What It Does
[User-facing description]

### Data Structures
[Key models and their relationships]

### Business Logic
[Core logic summary]

### State
[What state is managed, how it changes]

### API Calls
[Endpoints, request/response shapes]

### UI Flow
[Screens, navigation]

### Edge Cases Handled
- [Case 1]
- [Case 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 3: Analyze Android Codebase Patterns

**Before implementing, understand how THIS Android codebase does things:**

1. **Check if `.claude/codebase-style.md` exists** - If yes, use it and skip manual analysis
2. Find similar features in the codebase
3. Note the patterns used:
   - Architecture pattern
   - UI framework and patterns
   - State management approach
   - Networking approach
   - Dependency injection
   - File/folder organization
   - Naming conventions

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
               ANDROID CODEBASE PATTERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Style Guide: [Found / Not found]

Patterns observed from existing code:
- Architecture: [what pattern is used]
- UI: [how UI is built]
- State: [how state is managed]
- Networking: [how API calls are made]
- DI: [how dependencies are injected]
- Navigation: [how navigation works]

Similar features to reference:
- [Feature 1]: [path]
- [Feature 2]: [path]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4: Create Implementation Plan

Map the iOS feature to Android equivalents **using the patterns from Step 3**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                  IMPLEMENTATION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Files to Create

| # | File | Purpose | iOS Equivalent |
|---|------|---------|----------------|
| 1 | [path matching codebase conventions] | [purpose] | [iOS file] |
| 2 | ... | ... | ... |

## Key Mappings

| iOS Concept | Android Equivalent (matching codebase patterns) |
|-------------|------------------------------------------------|
| [iOS thing] | [Android equivalent as done in this codebase] |
| ... | ... |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5: Implement

Create the Android implementation:

- **Match the codebase's existing patterns exactly**
- Use the same architecture, UI patterns, state management as other features
- Follow the same naming conventions
- Keep data structure shapes equivalent for API compatibility

### Step 6: Copy Assets (if needed)

**If the feature uses assets, offer to copy them:**

Assets that may need to be copied:
- Images, icons, colors, fonts, Lottie animations, sounds, etc.

If assets are needed and the user wants them copied, use file operations to transfer them from the iOS codebase to the appropriate Android locations.

### Step 7: Report Results

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                 iOS → ANDROID COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Feature: [Name]

### Files Created

| File | Purpose |
|------|---------|
| [path] | [description] |

### Feature Parity Checklist

- [x] Core functionality matches iOS
- [x] Data structures equivalent
- [x] Error handling preserved
- [x] Loading states preserved
- [x] Edge cases handled
- [x] Matches Android codebase patterns

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Triggers

```
"ios to android"
"convert from ios"
"port this swift to kotlin"
"implement this ios feature for android"
"android version of this ios code"
```

---

## Integration with style-guide

**Recommended:** Run the `style-guide` skill on the Android codebase first.

```
style guide     ← Run this first on Android codebase
ios to android  ← Then run this
```

This generates `.claude/codebase-style.md` which this skill will automatically reference.

**If style guide exists:**
- Skip manual pattern analysis (Step 3)
- Reference the documented patterns directly
- Ensure perfect consistency with existing code

**If no style guide:**
- This skill will analyze patterns manually (Step 3)
- Consider running `style-guide` first for better results

---

## Tips

1. **Don't translate literally** - Understand the feature, then implement idiomatically
2. **Match the codebase** - Use the same patterns as existing Android code
3. **Keep data shapes equivalent** - API compatibility matters
4. **Handle platform differences** - Some things work differently (lifecycle, permissions)
5. **Verify feature parity** - Same behavior, not same code
