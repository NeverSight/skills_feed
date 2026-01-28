---
name: valdi
description: This skill should be used when working on Valdi framework projects. Valdi is Snapchat's cross-platform UI framework that compiles TypeScript/TSX components into native views for iOS, Android, and macOS. It provides specialized knowledge for component architecture, Bazel build system, native bindings, TSX elements, and cross-platform development. Use this skill when implementing Valdi components, debugging build issues, or creating new Valdi projects.
---

# Valdi Framework Development Skill

Specialized guidance for developing cross-platform applications with Valdi, Snapchat's native UI framework that compiles TypeScript/TSX to native iOS, Android, and macOS views.

## Overview

Valdi is NOT a WebView-based framework. It compiles TypeScript components directly into native platform code, delivering native performance without JavaScript bridges. The framework has been used in Snap's production apps for over 8 years.

## When to Use This Skill

Invoke this skill when:

- Working on any Valdi framework project
- Creating new Valdi components or modules
- Configuring Bazel build files for Valdi
- Implementing native bindings (CppModule, NativeModule)
- Debugging cross-platform rendering issues
- Setting up Valdi development environment
- Understanding Valdi's TSX element system

## Key Principles

### 1. Bazel is Mandatory

Valdi uses Bazel exclusively for builds. Never suggest alternative build systems.

**Common commands:**
```bash
# Install CLI globally
pnpm install -g @snap/valdi

# Setup development environment
valdi dev_setup

# Check environment health
valdi doctor

# Bootstrap new project
valdi bootstrap

# Install platform dependencies
valdi install ios
valdi install android

# Enable hot reload during development
valdi hotreload

# Sync project configuration
valdi projectsync
```

### 2. Component Architecture

Valdi components are class-based with lifecycle methods:

```tsx
import { Component, ComponentContext } from 'valdi_core';

interface ViewModel {
  title: string;
  count: number;
}

class MyComponent extends Component<ViewModel, ComponentContext> {
  onCreate(): void {
    // Initialize component
    console.log('Component created');
  }

  onMount(): void {
    // Component mounted to view hierarchy
  }

  onUnmount(): void {
    // Cleanup before removal
  }

  onRender() {
    return (
      <view style={styles.container}>
        <label style={styles.title}>{this.viewModel.title}</label>
      </view>
    );
  }
}
```

### 3. Native TSX Elements

Valdi provides native UI elements (NOT HTML):

| Element | Purpose |
|---------|---------|
| `<view>` | Container view (like div) |
| `<layout>` | Flexbox layout container |
| `<scroll>` | Scrollable container |
| `<label>` | Text display |
| `<image>` | Image display |
| `<video>` | Video player |
| `<slot>` | Content projection |

**Element attributes use native styling, not CSS:**
```tsx
const styles = {
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFFFFF',
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000000',
  },
};
```

### 4. Project Structure

Standard Valdi project layout:

```
my_project/
├── BUILD.bazel              # Main Bazel build file
├── package.json             # Node dependencies (use pnpm)
├── .eslintrc.js            # ESLint configuration
├── app_assets/             # Application assets
│   └── images/
├── src/
│   ├── android/            # Android-specific code
│   ├── cpp/                # C++ native modules
│   ├── ios/                # iOS-specific code
│   └── valdi/              # Valdi TypeScript/TSX
│       ├── _configs/       # Valdi configs
│       ├── tsconfig.json
│       ├── .terserrc.json
│       └── my_module/      # Your module
│           ├── BUILD.bazel
│           ├── tsconfig.json
│           ├── res/        # Module resources
│           └── src/
│               ├── index.ts
│               └── MyComponent.tsx
└── standalone_app/         # Standalone app config
```

### 5. Bazel Build Configuration

**Application BUILD.bazel:**
```python
load("//bzl:valdi.bzl", "valdi_application", "valdi_exported_library")

valdi_application(
    name = "my_app",
    title = "My Valdi App",
    version = "1.0.0",
    ios_bundle_id = "com.example.myapp",
    ios_device_families = ["iphone"],
    android_theme = "Theme.MyApp.Launch",
    android_app_icon = "app_icon",
    root_component = "App@my_module/src/MyApp",
    assets = glob(["app_assets/**/*"]),
    deps = ["//path/to/src/valdi/my_module"],
)

valdi_exported_library(
    name = "my_app_export",
    ios_bundle_id = "com.example.myapp.lib",
    bundle_name = "MyApp",
    deps = ["//path/to/src/valdi/my_module"],
)
```

**Module BUILD.bazel:**
```python
load("//bzl:valdi.bzl", "valdi_module")

valdi_module(
    name = "my_module",
    srcs = glob(["src/**/*.ts", "src/**/*.tsx"]) + ["tsconfig.json"],
    assets = glob(["res/**/*.{jpeg,jpg,png,svg,webp}"]),
    android = struct(
        class_path = "com.example.valdi.modules.my_module",
        native_deps = ["//path/to/android:native_module"],
        release = True,
    ),
    ios = struct(
        module_name = "SCCMyModule",
        native_deps = ["//path/to/ios:native_module"],
        release = True,
    ),
    native = struct(
        deps = ["//path/to/cpp:native_module_cpp"],
    ),
    deps = [
        "//src/valdi_modules/valdi_core",
        "//src/valdi_modules/valdi_tsx",
    ],
    visibility = ["//visibility:public"],
)
```

### 6. Native Bindings

Valdi supports type-safe bindings to native code:

**CppModule.d.ts:**
```typescript
declare module 'CppModule' {
  export function performCalculation(value: number): number;
  export function getNativeString(): string;
}
```

**NativeModule.d.ts:**
```typescript
declare module 'NativeModule' {
  export function showNativeAlert(message: string): void;
  export function getPlatformInfo(): { os: string; version: string };
}
```

**Usage in component:**
```tsx
import * as CppModule from 'CppModule';
import * as NativeModule from 'NativeModule';

class MyComponent extends Component<ViewModel, ComponentContext> {
  onMount() {
    const result = CppModule.performCalculation(42);
    const platform = NativeModule.getPlatformInfo();
  }
}
```

### 7. Cross-Platform Best Practices

**All changes must work across iOS, Android, and macOS:**

- Test on multiple platforms before committing
- Platform-specific code goes in dedicated directories (src/ios/, src/android/)
- Use Valdi's abstraction layer for platform differences
- Check AGENTS.md in repository for platform-specific guidance

**Performance is critical:**
- Valdi emphasizes rendering efficiency
- Use view recycling through Valdi's pooling systems
- Components render independently (no parent re-renders)
- Viewport-aware rendering for efficient scrolling

### 8. Development Workflow

**Initial setup:**
```bash
# Install Valdi CLI
pnpm install -g @snap/valdi

# Setup development environment (takes 10-20 minutes first time)
valdi dev_setup

# Verify installation
valdi doctor
```

**Creating a new project:**
```bash
mkdir my_project && cd my_project
valdi bootstrap
valdi install ios  # or android
```

**Development cycle:**
```bash
# Start hot reload for live updates
valdi hotreload

# After changing dependencies or resources
valdi projectsync
```

**Editor setup (VSCode/Cursor):**
1. Install shell commands from editor
2. Install extensions from Valdi release:
   - `valdi-vivaldi.vsix` (device logs, language support)
   - `valdi-debug.vsix` (JavaScript debugger)
3. Configure TypeScript workspace version

## Common Pitfalls

### 1. Using Web/React Patterns

**Problem:** Treating Valdi like React or web development.

```tsx
// WRONG - HTML elements don't exist
<div className="container">
  <span>Hello</span>
</div>

// CORRECT - Use Valdi native elements
<view style={styles.container}>
  <label>Hello</label>
</view>
```

### 2. CSS-Style Styling

**Problem:** Using CSS syntax for styles.

```tsx
// WRONG - CSS syntax
const styles = {
  container: {
    'background-color': '#fff',
    'font-size': '16px',
  }
};

// CORRECT - Camel case, numeric values
const styles = {
  container: {
    backgroundColor: '#FFFFFF',
    fontSize: 16,
  }
};
```

### 3. Modifying Auto-Generated Code

**Problem:** Editing Djinni-generated native bindings directly.

**Solution:** Always modify source files, never generated code. Regenerate bindings after source changes.

### 4. Wrong Build System

**Problem:** Using npm/yarn scripts, webpack, or other bundlers.

**Solution:** Valdi uses Bazel exclusively. Use `valdi` CLI commands.

### 5. Missing Platform Testing

**Problem:** Only testing on one platform.

**Solution:** Always verify changes work on iOS, Android, and macOS where applicable.

## ESLint Configuration

Standard Valdi ESLint setup:

```javascript
// .eslintrc.js
module.exports = {
  parser: '@typescript-eslint/parser',
  parserOptions: {
    project: './tsconfig.json',
    ecmaVersion: 2020,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  plugins: [
    '@typescript-eslint',
    'eslint-plugin-valdi',
    'rxjs',
    'import',
    'unused-imports',
  ],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  rules: {
    // Valdi-specific rules
  },
};
```

## TypeScript Configuration

Standard tsconfig.json for Valdi modules:

```json
{
  "extends": "../../_configs/tsconfig.json",
  "compilerOptions": {
    "jsx": "react",
    "jsxFactory": "Valdi.createElement",
    "strict": true,
    "moduleResolution": "node",
    "esModuleInterop": true
  },
  "include": ["src/**/*"]
}
```

## Available Libraries

Valdi provides these core modules:

| Module | Purpose |
|--------|---------|
| `valdi_core` | Core component system, lifecycle |
| `valdi_tsx` | TSX/JSX support |
| `valdi_protobuf` | Protobuf serialization |
| `valdi_http` | HTTP client |
| `valdi_storage` | Persistent encrypted storage |
| `valdi_navigation` | Navigation system |
| `valdi_rxjs` | RxJS integration |

## Debugging

**Using Hermes Debugger:**
- Available for JavaScript debugging
- Set breakpoints in VSCode with valdi-debug extension

**Using Valdi Inspector:**
- Inspect UI hierarchy
- View component state
- Performance profiling

## Quick Reference

### CLI Commands
| Command | Purpose |
|---------|---------|
| `valdi dev_setup` | Setup development environment |
| `valdi doctor` | Check environment health |
| `valdi bootstrap` | Create new project |
| `valdi install [platform]` | Install platform dependencies |
| `valdi hotreload` | Enable live updates |
| `valdi projectsync` | Sync project configuration |

### Lifecycle Methods
| Method | When Called |
|--------|-------------|
| `onCreate()` | Component initialization |
| `onMount()` | Added to view hierarchy |
| `onUnmount()` | Before removal from hierarchy |
| `onRender()` | Render component UI |

### Native Elements
| Element | HTML Equivalent |
|---------|-----------------|
| `<view>` | `<div>` |
| `<layout>` | Flexbox container |
| `<scroll>` | Scrollable div |
| `<label>` | `<span>` / `<p>` |
| `<image>` | `<img>` |
| `<video>` | `<video>` |

## References

For more details:
- `references/component-patterns.md` - Advanced component patterns
- `references/bazel-configuration.md` - Detailed Bazel setup
- `references/native-bindings.md` - Native code integration

## Additional Resources

- Valdi GitHub: https://github.com/Snapchat/Valdi
- AGENTS.md in repository for AI coding guidelines
- Discord community for support
- Codelabs in docs/ for guided tutorials

---

**Remember:** Valdi compiles to native code - think native, not web. Use Bazel for builds, pnpm for Node dependencies, and test on all target platforms.
