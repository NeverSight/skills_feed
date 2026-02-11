---
name: arkts-development
description: HarmonyOS ArkTS application development with ArkUI declarative UI framework. Use when building HarmonyOS/OpenHarmony apps, creating ArkUI components, implementing state management with decorators (@State, @Prop, @Link), migrating from TypeScript to ArkTS, or working with HarmonyOS-specific APIs (router, http, preferences). Covers component lifecycle, layout patterns, and ArkTS language constraints.
---

# ArkTS Development

Build HarmonyOS applications using ArkTS and the ArkUI declarative UI framework.

## Quick Start

Create a basic component:

```typescript
@Entry
@Component
struct HelloWorld {
  @State message: string = 'Hello, ArkTS!';

  build() {
    Column() {
      Text(this.message)
        .fontSize(30)
        .fontWeight(FontWeight.Bold)
      Button('Click Me')
        .onClick(() => { this.message = 'Button Clicked!'; })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }
}
```

## State Management Decorators

### V1 (Traditional)

| Decorator | Usage | Description |
|-----------|-------|-------------|
| `@State` | `@State count: number = 0` | Component internal state |
| `@Prop` | `@Prop title: string` | Parent → Child (one-way) |
| `@Link` | `@Link value: number` | Parent ↔ Child (two-way, use `$varName`) |
| `@Provide/@Consume` | Cross-level | Ancestor → Descendant |
| `@Observed/@ObjectLink` | Nested objects | Deep object observation |

### V2 (Recommended - API 12+)

| Decorator | Usage | Description |
|-----------|-------|-------------|
| `@ComponentV2` | `@ComponentV2 struct MyComp` | Enable V2 state management |
| `@Local` | `@Local count: number = 0` | Internal state (no external init) |
| `@Param` | `@Param title: string = ""` | Parent → Child (one-way, efficient) |
| `@Event` | `@Event onChange: () => void` | Child → Parent (callback) |
| `@ObservedV2` | `@ObservedV2 class Data` | Class observation |
| `@Trace` | `@Trace name: string` | Property-level tracking |
| `@Computed` | `@Computed get value()` | Cached computed properties |
| `@Monitor` | `@Monitor('prop') onFn()` | Watch changes with before/after |
| `@Provider/@Consumer` | Cross-level | Two-way sync across tree |

**See [references/state-management-v2.md](references/state-management-v2.md) for complete V2 guide.**

## Common Layouts

```typescript
// Vertical
Column({ space: 10 }) { Text('A'); Text('B'); }
  .alignItems(HorizontalAlign.Center)

// Horizontal
Row({ space: 10 }) { Text('A'); Text('B'); }
  .justifyContent(FlexAlign.SpaceBetween)

// Stack (overlay)
Stack({ alignContent: Alignment.Center }) {
  Image($r('app.media.bg'))
  Text('Overlay')
}

// List with ForEach
List({ space: 10 }) {
  ForEach(this.items, (item: string) => {
    ListItem() { Text(item) }
  }, (item: string) => item)
}
```

## Component Lifecycle

```typescript
@Entry
@Component
struct Page {
  aboutToAppear() { /* Init data */ }
  onPageShow() { /* Page visible */ }
  onPageHide() { /* Page hidden */ }
  aboutToDisappear() { /* Cleanup */ }
  build() { Column() { Text('Page') } }
}
```

## Navigation

```typescript
import { router } from '@kit.ArkUI';

// Push
router.pushUrl({ url: 'pages/Detail', params: { id: 123 } });

// Replace
router.replaceUrl({ url: 'pages/New' });

// Back
router.back();

// Get params
interface RouteParams {
  id: number;
  title?: string;
}
const params = router.getParams() as RouteParams;
```

## Network Request

```typescript
import { http } from '@kit.NetworkKit';

const req = http.createHttp();
const res = await req.request('https://api.example.com/data', {
  method: http.RequestMethod.GET,
  header: { 'Content-Type': 'application/json' }
});
if (res.responseCode === 200) {
  const data = JSON.parse(res.result as string);
}
req.destroy();
```

## Local Storage

```typescript
import { preferences } from '@kit.ArkData';

const prefs = await preferences.getPreferences(this.context, 'store');
await prefs.put('key', 'value');
await prefs.flush();
const val = await prefs.get('key', 'default');
```

## ArkTS Language Constraints

ArkTS enforces stricter rules than TypeScript for performance and safety:

| Prohibited | Use Instead |
|------------|-------------|
| `any`, `unknown` | Explicit types, interfaces |
| `var` | `let`, `const` |
| Dynamic property access `obj['key']` | Fixed object structure |
| `for...in`, `delete`, `with` | `for...of`, array methods |
| `#privateField` | `private` keyword |
| Structural typing | Explicit `implements`/`extends` |

See [references/migration-guide.md](references/migration-guide.md) for complete TypeScript → ArkTS migration details.

## Command Line Build (hvigorw)

hvigorw is the Hvigor wrapper tool for command-line builds.

```bash
# Common build tasks
hvigorw clean                              # Clean build directory
hvigorw assembleHap -p buildMode=debug     # Build Hap (debug)
hvigorw assembleApp -p buildMode=release   # Build App (release)
hvigorw assembleHar                        # Build Har library
hvigorw assembleHsp                        # Build Hsp

# Build specific module
hvigorw assembleHap -p module=entry@default --mode module

# Run tests
hvigorw onDeviceTest -p module=entry -p coverage=true
hvigorw test -p module=entry              # Local test

# CI/CD recommended
hvigorw assembleApp -p buildMode=release --no-daemon
```

Common parameters:

| Parameter | Description |
|-----------|-------------|
| `-p buildMode={debug\|release}` | Build mode |
| `-p product={name}` | Target product (default: default) |
| `-p module={name}@{target}` | Target module (with `--mode module`) |
| `--no-daemon` | Disable daemon (recommended for CI) |
| `--analyze=advanced` | Enable build analysis |
| `--optimization-strategy=memory` | Memory-optimized build |

See [references/hvigor-commandline.md](references/hvigor-commandline.md) for complete command reference.

## Code Linter (codelinter)

codelinter is the code checking and fixing tool for ArkTS/TS files.

```bash
# Basic usage
codelinter                           # Check current project
codelinter /path/to/project          # Check specified project
codelinter -c ./code-linter.json5    # Use custom rules

# Check and auto-fix
codelinter --fix
codelinter -c ./code-linter.json5 --fix

# Output formats
codelinter -f json -o ./report.json  # JSON report
codelinter -f html -o ./report.html  # HTML report

# Incremental check (Git changes only)
codelinter -i

# CI/CD with exit codes
codelinter --exit-on error,warn      # Non-zero exit on error/warn
```

| Parameter | Description |
|-----------|-------------|
| `-c, --config <file>` | Specify rules config file |
| `--fix` | Auto-fix supported issues |
| `-f, --format` | Output format: default/json/xml/html |
| `-o, --output <file>` | Save result to file |
| `-i, --incremental` | Check only Git changed files |
| `-p, --product <name>` | Specify product |
| `-e, --exit-on <levels>` | Exit code levels: error,warn,suggestion |

See [references/codelinter.md](references/codelinter.md) for complete reference.

## Stack Trace Parser (hstack)

hstack parses obfuscated crash stacks from Release builds back to source code locations.

```bash
# Parse crash files directory
hstack -i crashDir -o outputDir -s sourcemapDir -n nameCacheDir

# Parse with C++ symbols
hstack -i crashDir -o outputDir -s sourcemapDir --so soDir -n nameCacheDir

# Parse single crash stack
hstack -c "at func (entry|entry|1.0.0|src/main/ets/pages/Index.ts:58:58)" -s sourcemapDir
```

| Parameter | Description |
|-----------|-------------|
| `-i, --input` | Crash files directory |
| `-c, --crash` | Single crash stack string |
| `-o, --output` | Output directory (or file with `-c`) |
| `-s, --sourcemapDir` | Sourcemap files directory |
| `--so, --soDir` | Shared object (.so) files directory |
| `-n, --nameObfuscation` | NameCache files directory |

Requirements:
- Must provide either `-i` or `-c` (not both)
- Must provide at least `-s` or `--so`
- For method name restoration, provide both `-s` and `-n`

See [references/hstack.md](references/hstack.md) for complete reference.

## Code Obfuscation (ArkGuard)

Enable in `build-profile.json5`:

```json
"arkOptions": {
  "obfuscation": {
    "ruleOptions": {
      "enable": true,
      "files": ["./obfuscation-rules.txt"]
    }
  }
}
```

Common rules in `obfuscation-rules.txt`:

```text
-enable-property-obfuscation      # Property name obfuscation
-enable-toplevel-obfuscation      # Top-level scope obfuscation
-enable-filename-obfuscation      # Filename obfuscation
-keep-property-name apiKey        # Whitelist specific names
```

See [references/arkguard-obfuscation.md](references/arkguard-obfuscation.md) for complete guide.

## Reference Files

- **State Management V2**: [references/state-management-v2.md](references/state-management-v2.md) - Complete guide to V2 state management (@ComponentV2, @Local, @Param, @Event, @ObservedV2, @Trace, @Computed, @Monitor, @Provider, @Consumer)
- **Migration Guide**: [references/migration-guide.md](references/migration-guide.md) - Complete TypeScript to ArkTS migration rules and examples
- **Component Patterns**: [references/component-patterns.md](references/component-patterns.md) - Advanced component patterns and best practices
- **API Reference**: [references/api-reference.md](references/api-reference.md) - Common HarmonyOS APIs
- **ArkGuard Obfuscation**: [references/arkguard-obfuscation.md](references/arkguard-obfuscation.md) - Code obfuscation configuration and troubleshooting
- **Hvigor Command Line**: [references/hvigor-commandline.md](references/hvigor-commandline.md) - Complete hvigorw build tool reference
- **CodeLinter**: [references/codelinter.md](references/codelinter.md) - Code checking and fixing tool
- **Hstack**: [references/hstack.md](references/hstack.md) - Crash stack trace parser for Release builds

## Development Environment

- **IDE**: DevEco Studio
- **SDK**: HarmonyOS SDK
- **Simulator**: Built-in DevEco Studio emulator

## Related Skills

- **Build & Deploy**: See `harmonyos-build-deploy` skill for building, packaging, and device installation
