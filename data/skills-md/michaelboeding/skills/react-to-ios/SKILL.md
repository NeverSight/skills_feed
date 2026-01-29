---
name: react-to-ios
description: Use React/React Native code as the source of truth and implement the equivalent feature in iOS/Swift. Understands the feature behavior, components, state management, and logic from React, then creates idiomatic iOS code that matches the target codebase's existing patterns. Use when porting features from React/React Native to native iOS or building native alternatives to web components.
---

# React to iOS: Feature Parity Implementation

Use React/React Native code as the reference to implement the equivalent native iOS feature. Not a literal translation - understand what the React code does, then implement it idiomatically for iOS.

**Use this when:**
- Porting a feature from React/React Native to native iOS
- React is the "source of truth" for a feature
- Building native iOS alternatives to web components
- Migrating from React Native to native Swift

## Key Principle

```
React Code → Understand Feature → Match iOS Codebase Patterns → Implement
                 (what)                  (how it's done here)
```

**Preserved:** Feature behavior, data structure shapes, business logic, user flows, API contracts
**Adapted:** Language idioms, frameworks, UI patterns to match the iOS codebase

---

## Common Mappings Reference

| React/React Native | iOS/Swift Equivalent |
|--------------------|---------------------|
| `useState` | `@State` / `@Published` |
| `useEffect` | `.onAppear` / `.task` / `viewDidLoad` |
| `useContext` | Environment objects / Dependency injection |
| `useMemo` / `useCallback` | Computed properties / lazy vars |
| `useReducer` | State machine / Combine |
| Props | Init parameters / Bindings |
| `View` / `div` | SwiftUI `View` / UIKit `UIView` |
| `Text` | `Text` / `UILabel` |
| `Image` | `Image` / `UIImageView` |
| `ScrollView` | `ScrollView` / `UIScrollView` |
| `FlatList` | `List` / `LazyVStack` / `UITableView` |
| `TouchableOpacity` | `Button` / tap gestures |
| `TextInput` | `TextField` / `UITextField` |
| `StyleSheet` | SwiftUI modifiers / UIKit constraints |
| `fetch` / `axios` | `URLSession` / async-await |
| Redux / Zustand | Combine / SwiftUI state / TCA |
| React Navigation | `NavigationStack` / `UINavigationController` |
| React Query / SWR | Async/await patterns / Combine |
| Styled Components | View modifiers / custom ViewModifiers |
| Context Providers | `@EnvironmentObject` / DI containers |

---

## Workflow

### Step 0: Gather Context

**Ask the user for both pieces of information:**

```
To port a feature from React to iOS, I need:

1. PATH TO REACT CODEBASE (source of truth)
   Where is the React/React Native project located?
   Example: /path/to/react-app or ../react-native-app

2. FEATURE TO IMPLEMENT
   What feature or component should I port?
   Example: "UserProfile component" or "the checkout flow" or "src/components/Dashboard"
```

**Assumptions:**
- Current working directory = iOS codebase (target)
- User provides path to React codebase (source)

If the user already provided this info, proceed. Otherwise, ask.

### Step 1: Locate the React Feature

Navigate to the React codebase path and find the relevant files:

1. Go to the React path provided
2. Find files related to the feature (components, hooks, stores, utils)
3. Read and understand the implementation

**Files to look for:**
- Component files (`.tsx`, `.jsx`, `.js`)
- Custom hooks (`use*.ts`)
- State management (Redux slices, Zustand stores, Context)
- API services
- Types/interfaces (`.ts`, `.d.ts`)
- Styles (CSS modules, styled-components, StyleSheet)

### Step 2: Analyze the React Code

Thoroughly understand:

| Aspect | What to Extract |
|--------|-----------------|
| **Feature Behavior** | What does this feature do? User-facing functionality |
| **Component Structure** | Component hierarchy, props, composition patterns |
| **State Management** | useState, useReducer, Redux, Context usage |
| **Side Effects** | useEffect patterns, data fetching, subscriptions |
| **Business Logic** | Validations, transformations, calculations |
| **API Contracts** | Network calls, request/response shapes |
| **UI Flow** | Screens, navigation, user interactions |
| **Edge Cases** | Error handling, loading states, empty states |

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                  REACT FEATURE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Feature: [Name]

### What It Does
[User-facing description]

### Component Structure
[Component hierarchy and relationships]

### Props & State
[Key props, state variables, their purposes]

### Side Effects
[What useEffect/data fetching does]

### Business Logic
[Core logic summary]

### API Calls
[Endpoints, request/response shapes]

### UI Flow
[Screens, navigation, interactions]

### Edge Cases Handled
- [Case 1]
- [Case 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 3: Analyze iOS Codebase Patterns

**Before implementing, understand how THIS iOS codebase does things:**

1. **Check if `.claude/codebase-style.md` exists** - If yes, use it and skip manual analysis
2. Find similar features in the codebase
3. Note the patterns used:
   - Architecture pattern (MVVM, MVC, TCA, VIPER)
   - UI framework (SwiftUI vs UIKit)
   - State management approach
   - Networking approach
   - Dependency injection
   - File/folder organization
   - Naming conventions

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                 iOS CODEBASE PATTERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Style Guide: [Found / Not found]

Patterns observed from existing code:
- Architecture: [MVVM / MVC / TCA / VIPER / etc.]
- UI Framework: [SwiftUI / UIKit / Mixed]
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

Map the React feature to iOS equivalents **using the patterns from Step 3**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                  IMPLEMENTATION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Files to Create

| # | File | Purpose | React Equivalent |
|---|------|---------|------------------|
| 1 | [path matching codebase conventions] | [purpose] | [React file] |
| 2 | ... | ... | ... |

## Key Mappings

| React Concept | iOS Equivalent (matching codebase patterns) |
|---------------|---------------------------------------------|
| [React thing] | [iOS equivalent as done in this codebase] |
| ... | ... |

## State Migration

| React State | iOS State Management |
|-------------|---------------------|
| [useState/Redux/etc.] | [How it maps to iOS patterns] |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5: Implement

Create the iOS implementation:

- **Match the codebase's existing patterns exactly**
- Use the same architecture, UI patterns, state management as other features
- Follow the same naming conventions
- Keep data structure shapes equivalent for API compatibility
- Translate React patterns to idiomatic Swift/SwiftUI

**Pattern Translation Tips:**

| React Pattern | iOS Implementation |
|---------------|-------------------|
| Component with props | `View` with init parameters or `@Binding` |
| useState + setState | `@State` property with direct mutation |
| useEffect on mount | `.onAppear` or `.task` modifier |
| useEffect with deps | `.onChange(of:)` modifier |
| useEffect cleanup | `.onDisappear` or `task` cancellation |
| Conditional rendering | `if/else` or `@ViewBuilder` |
| List mapping | `ForEach` |
| Event handlers | Action closures or Bindings |
| CSS/StyleSheet | SwiftUI modifiers or custom `ViewModifier` |

**⚠️ IMPORTANT: After creating each `.swift` file, register it with Xcode:**

```bash
ruby ${CLAUDE_PLUGIN_ROOT}/skills/add-to-xcode/scripts/add_to_xcode.rb <filepath>
```

Without this step, files won't appear in Xcode or compile. See the `add-to-xcode` skill.

### Step 6: Copy Assets (if needed)

**If the feature uses assets, offer to copy them:**

Assets that may need to be copied:
- Images, icons (convert to Asset Catalog format)
- Colors (convert to Color Sets)
- Fonts
- Lottie animations
- Sounds

If assets are needed and the user wants them copied, use file operations to transfer and convert them appropriately for iOS.

### Step 7: Report Results

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                 REACT → iOS COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Feature: [Name]

### Files Created

| File | Purpose |
|------|---------|
| [path] | [description] |

### Feature Parity Checklist

- [x] Core functionality matches React
- [x] Data structures equivalent
- [x] State management properly translated
- [x] Side effects handled
- [x] Error handling preserved
- [x] Loading states preserved
- [x] Edge cases handled
- [x] Matches iOS codebase patterns

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Triggers

```
"react to ios"
"react native to ios"
"convert from react"
"port this react component to swift"
"implement this react feature for ios"
"ios version of this react code"
"native ios from react native"
"migrate react native to swift"
```

---

## Integration with style-guide

**Recommended:** Run the `style-guide` skill on the iOS codebase first.

```
style guide    ← Run this first on iOS codebase
react to ios   ← Then run this
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
2. **Match the codebase** - Use the same patterns as existing iOS code
3. **Keep data shapes equivalent** - API compatibility matters
4. **Handle paradigm differences** - React is declarative but different from SwiftUI
5. **Verify feature parity** - Same behavior, not same code
6. **Consider lifecycle differences** - React component lifecycle ≠ SwiftUI view lifecycle
7. **State is different** - React re-renders on state change; SwiftUI uses property wrappers
8. **Navigation differs** - React Router/Navigation vs NavigationStack patterns
