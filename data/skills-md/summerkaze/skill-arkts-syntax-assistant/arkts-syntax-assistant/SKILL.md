---
name: arkts-syntax-assistant
description: |-
  ArkTS syntax, migration, and optimization guide for HarmonyOS/OpenHarmony development.
  Triggers on: .ets files, ArkTS keywords, HarmonyOS/OpenHarmony context, @ohos packages.
  Help with syntax reference, TypeScript migration, performance optimization,
  compile errors, state management, component development, and language-specific questions.
license: MIT
tags:
  - arkts
  - harmonyos
  - typescript
  - migration
  - development
  - syntax
---

# ArkTS Syntax Assistant

[中文文档](SKILL.zh.md)

---

## Overview

ArkTS is the default development language for OpenHarmony applications. It builds
upon TypeScript with enhanced static typing to improve program stability and
performance.

## Core Features

- **Static Typing**: All types determined at compile time, reducing runtime checks
- **No Dynamic Object Layout**: Object structure fixed at compile time, cannot be
  modified at runtime
- **Restricted Operators**: Some operator behaviors are restricted to encourage
  clearer code semantics
- **No Structural Typing**: Structural typing is currently not supported

## Reference Documentation

| Scenario | Document |
|----------|----------|
| Syntax Learning | [references/en/introduction-to-arkts.md](references/en/introduction-to-arkts.md) |
| Quick Overview | [references/en/arkts-get-started.md](references/en/arkts-get-started.md) |
| TS Migration | [references/en/typescript-to-arkts-migration-guide.md](references/en/typescript-to-arkts-migration-guide.md) |
| Migration Background | [references/en/arkts-migration-background.md](references/en/arkts-migration-background.md) |
| Performance | [references/en/arkts-high-performance-programming.md](references/en/arkts-high-performance-programming.md) |
| More Cases | [references/en/arkts-more-cases.md](references/en/arkts-more-cases.md) |

## Workflows

### 1. Syntax Questions

```
User Question -> Identify Question Type -> Consult Documentation -> Provide Code Example
```

**Common Syntax Questions**:
- Variable declaration -> Use `let`/`const` with explicit type or inference
- Function definition -> Supports optional parameters, defaults, rest parameters,
  arrow functions
- Classes and interfaces -> Must initialize fields, supports inheritance and
  implementation
- Generics -> Supports constraints and default values
- Null safety -> Nullable types `T | null`, non-null assertion `!`, optional
  chaining `?.`

### 2. TypeScript Migration

```
Identify TS Code -> Check Incompatible Features -> Consult Migration Rules -> Provide ArkTS Alternative
```

**Key Migration Rules Quick Reference**:

| TypeScript | ArkTS Alternative |
|------------|-------------------|
| `var x` | `let x` |
| `any`/`unknown` | Specific types |
| `{n: 42}` object literal | Define class/interface first |
| `[index: T]: U` index signature | `Record<T, U>` |
| `A & B` intersection type | `interface C extends A, B` |
| `function(){}` function expression | `() => {}` arrow function |
| `<Type>value` type assertion | `value as Type` |
| Destructuring `[a, b] = arr` | Individual access `arr[0]`, `arr[1]` |
| `for..in` | `for` loop or `for..of` |
| Constructor parameter properties | Explicit field declaration |

### 3. Performance Optimization

```
Analyze Code -> Identify Performance Issues -> Consult Optimization Guide -> Provide Solutions
```

**High-Performance Programming Key Points**:

- **Declarations**: Use `const` for invariants; avoid mixing integer and float
- **Loops**: Extract loop invariants; avoid numeric overflow
- **Functions**: Parameter passing preferred over closures; avoid optional
  parameters
- **Arrays**: Use TypedArray for numeric values; avoid sparse arrays and union
  type arrays
- **Exceptions**: Avoid throwing in loops; use return values instead

### 4. Compile Error Resolution

```
Get Error Message -> Search Migration Rules -> Find Related Case -> Provide Fix
```

## Common Questions

### Q: How to handle JSON.parse return value?

```typescript
// Error
let data = JSON.parse(str);

// Correct
let data: Record<string, Object> = JSON.parse(str);
```

### Q: How to define object types?

```typescript
// TypeScript syntax (not supported in ArkTS)
type Person = { name: string, age: number }

// ArkTS syntax
interface Person {
  name: string;
  age: number;
}

// Using object literal
let p: Person = { name: 'John', age: 25 };
```

### Q: How to replace globalThis?

```typescript
// Error
globalThis.value = 'xxx';

// Use singleton pattern
export class GlobalContext {
  private constructor() {}
  private static instance: GlobalContext;
  private _objects = new Map<string, Object>();

  public static getContext(): GlobalContext {
    if (!GlobalContext.instance) {
      GlobalContext.instance = new GlobalContext();
    }
    return GlobalContext.instance;
  }

  getObject(key: string): Object | undefined {
    return this._objects.get(key);
  }

  setObject(key: string, value: Object): void {
    this._objects.set(key, value);
  }
}
```

### Q: How to handle error types in catch?

```typescript
// Error
try {} catch (e: BusinessError) {}

// Correct
try {} catch (error) {
  let e: BusinessError = error as BusinessError;
}
```

### Q: How to use Record type?

```typescript
// TypeScript index signature
function foo(data: { [key: string]: string }) {}

// ArkTS Record
function foo(data: Record<string, string>) {}

// Usage example
let map: Record<string, number> = {
  'John': 25,
  'Mary': 21,
};
```

### Q: How to replace constructor signatures with factory functions?

```typescript
// TypeScript constructor signature
type ControllerCtor = {
  new (value: string): Controller;
}

// ArkTS factory function
type ControllerFactory = () => Controller;

class Menu {
  createController: ControllerFactory = () => {
    return new Controller('default');
  }
}
```

## Prohibited Standard Library APIs

The following are prohibited in ArkTS:

- **Global**: `eval`
- **Object**: `__proto__`, `defineProperty`, `freeze`, `getPrototypeOf`, etc.
- **Reflect**: `apply`, `construct`, `defineProperty`, etc.
- **Proxy**: All handler methods

## Build Scripts

The scripts directory provides quick compilation scripts for ArkTS projects
(including dependency installation):

| Platform | Script | Purpose |
|----------|--------|---------|
| macOS/Linux | `scripts/run.sh` | Execute `ohpm install` + `hvigorw assembleApp` |
| Windows | `scripts/run.ps1` | Execute `ohpm install` + `hvigorw assembleApp` |

Usage:
```bash
# macOS/Linux
bash scripts/run.sh

# Windows PowerShell
.\scripts\run.ps1
```

Script execution steps:
1. Install dependencies (`ohpm install --all`)
2. Build project (`hvigorw assembleApp`)

## Mandatory Requirements

**CRITICAL**: When this skill generates ArkTS code, the following workflow MUST be followed:

1. **Compilation Verification**: After generating code, you MUST compile the project using the build scripts:
   - macOS/Linux: `bash scripts/run.sh`
   - Windows: `.\scripts\run.ps1`

2. **Retry Strategy**: If compilation fails:
   - Analyze the error output
   - Fix the issue and retry compilation
   - Maximum of **3 compilation attempts**

3. **User Intervention**: After 3 failed compilation attempts, use `AskUserQuestion`:
   ```
   Question: Compilation failed after 3 attempts. How would you like to proceed?
   Options:
   - Continue retrying (attempt another fix)
   - Manual intervention (I'll wait for your guidance)
   - Skip compilation (proceed without verification)
   ```

4. **Error Reporting**: Always show the full compilation error output when failures occur.

## Answer Guidelines

1. **Prioritize code examples**: Show correct vs incorrect syntax comparison
2. **Reference official documentation**: For detailed explanations, guide users to
   consult corresponding documents in references/
3. **Explain reasons**: Explain why ArkTS has this restriction (performance,
   stability)
4. **Provide alternatives**: For unsupported features, provide feasible
  alternatives

## License

MIT License - see [LICENSE.txt](LICENSE.txt)
