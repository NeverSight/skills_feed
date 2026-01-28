---
name: the-vm-standard
description: The VM Standard - inviolable covenants governing View Model architecture in this codebase. These covenants SHALL NOT be violated under any circumstance.
---

# TITLE 1: VIEW MODEL ARCHITECTURE CODE

## PREAMBLE

This Code establishes the governing requirements for View Model architecture within this codebase. The View Model pattern serves as the bridge between domain services and user interface. These provisions ensure consistency, maintainability, and proper separation of concerns across all View Model implementations.

---

## CHAPTER 1: STRUCTURAL REQUIREMENTS

### § 1.1 Colocation

A View Model SHALL be defined in a single file bearing the name format `{ComponentName}.vm.ts`. No View Model definition SHALL span multiple files.

The interface, the tag, and the layer SHALL coexist within this single source file.

### § 1.2 Unity of Type and Tag

The interface type and the Context.Tag for any View Model SHALL bear identical names.

```typescript
export interface ChatVM {
  readonly history$: Atom.Atom<Prompt.Prompt>;
  readonly inputValue$: Atom.Atom<string>;
  readonly setInputValue: (value: string) => void;
  readonly sendMessageAtom: Atom.AtomResultFn<void, void, unknown>;
}

export const ChatVM = Context.GenericTag<ChatVM>("ChatVM");
```

When imported as a namespace, this unity SHALL enable both type and runtime tag access through the same identifier.

---

## CHAPTER 2: EXPORT REQUIREMENTS

### § 2.1 Live Layer Export

Every View Model SHALL export a live layer providing full production dependencies.

```typescript
const FullLayer = pipe(
  FullSessionLayer,
  Layer.provide(DependentVMKey.variants.live)
);

const layerLive = pipe(
  layer,
  Layer.provide(FullLayer),
);
```

No View Model SHALL exist without a live layer capable of executing in production.

### § 2.2 Default Key Export

Every View Model file SHALL conclude with a default export via `VMRuntime.key()`.

This export SHALL provide both `live` and `test` variants.

```typescript
export default VMRuntime.key(ChatVM, {
  live: pipe(layer, Layer.provide(FullLayer)),
  test: layer,
});
```

### § 2.3 Namespace Import Requirement

All View Models SHALL be imported as namespaces.

```typescript
// Required form:
import ChatVM from "./Chat.vm";

// Access patterns:
// ChatVM.variants.live  - the production layer
// ChatVM.variants.test  - the test layer
// ChatVM.tag            - the Context.Tag
```

Named imports that fracture the namespace unity are prohibited:

```typescript
// Prohibited:
import { ChatVM } from "./Chat.vm";
```

---

## CHAPTER 3: BEHAVIORAL REQUIREMENTS

### § 3.1 Thin Presentational Bridge

View Models SHALL serve as thin bridges between service layers and the user interface.

View Models SHALL NOT contain business logic. A View Model is required to:

(a) Yield services from the Effect context;
(b) Expose atoms for reactive UI binding;
(c) Provide action functions that delegate to services;
(d) Transform domain values into UI-ready formats.

```typescript
// Compliant: VM delegates to service
const sendMessageAtom = VMRuntime.fn((_: void, get: Atom.FnContext) =>
  Effect.gen(function* () {
    const input = get(inputValue$);
    if (!input.trim()) return;
    get.set(inputValue$, "");
    yield* chatService.handleUserMessage(input);
  }).pipe(Effect.withSpan("Chat.sendMessage"))
);
```

Business logic SHALL reside in service layers. View Models adapt; they must not compute.

### § 3.2 Service Yield Requirement

View Models SHALL yield services from the Effect context. View Models must not construct services directly.

```typescript
// Compliant: Services yielded from context
const layer = Layer.effect(
  ChatVM,
  Effect.gen(function* () {
    const registry = yield* AtomRegistry;
    const chatService = yield* ChatService.ChatService;
    const session = yield* EvaluationSession.tag;

    return { /* ... */ };
  })
);
```

Direct service construction is prohibited:

```typescript
// Prohibited:
const layer = Layer.effect(
  ChatVM,
  Effect.gen(function* () {
    const chatService = new ChatServiceImpl();
    const session = createSession();

    return { /* ... */ };
  })
);
```

---

## CHAPTER 4: ATOM REQUIREMENTS

### § 4.1 Atom Suffix Convention

All atom properties SHALL bear the `$` suffix.

```typescript
export interface SessionSetupVM {
  readonly inputValue$: Atom.Atom<string>;
  readonly history$: Atom.Atom<Prompt.Prompt>;
  readonly isLoading$: Atom.Atom<boolean>;
  readonly streamingMode$: Atom.Atom<StreamingMode>;
  readonly setupState$: Atom.Atom<SetupState>;

  // Non-atom members bear no suffix
  readonly setInputValue: (value: string) => void;
  readonly sendMessageAtom: Atom.AtomResultFn<void, void, unknown>;
}
```

### § 4.2 Confinement of Atoms

Atoms SHALL be defined only inside `Effect.gen` within the layer factory.

Atoms must not be defined at module scope.

```typescript
// Compliant: Atoms confined within Effect.gen
const layer = Layer.effect(
  ChatVM,
  Effect.gen(function* () {
    const registry = yield* AtomRegistry;

    const inputValue$ = Atom.make("");
    const debugMode$ = Atom.make(false);
    const history$ = Atom.subscriptionRef(chat.history);

    return { inputValue$, debugMode$, history$ };
  })
);
```

Module-scope atoms are prohibited:

```typescript
// Prohibited:
const inputValue$ = Atom.make("");

const layer = Layer.effect(
  ChatVM,
  Effect.gen(function* () {
    return { inputValue$ };
  })
);
```

---

## CHAPTER 5: ACTION REQUIREMENTS

### § 5.1 Synchronous Setters

Synchronous setters SHALL use `registry.set()`:

```typescript
const setInputValue = (value: string) => registry.set(inputValue$, value);
const setDebugMode = (enabled: boolean) => registry.set(debugMode$, enabled);
```

### § 5.2 Asynchronous Actions

Asynchronous actions SHALL use `VMRuntime.fn()` returning `AtomResultFn`:

```typescript
const sendMessageAtom = VMRuntime.fn((_: void, get: Atom.FnContext) =>
  Effect.gen(function* () {
    const input = get(inputValue$);
    if (!input.trim()) return;
    get.set(inputValue$, "");
    yield* chatService.handleUserMessage(input);
  }).pipe(Effect.withSpan("Chat.sendMessage"))
);
```

### § 5.3 Observability Span Requirement

All asynchronous actions SHALL be wrapped with `Effect.withSpan()`.

---

## CHAPTER 6: VARIANT REQUIREMENTS

### § 6.1 Dual Variant Structure

Every VMKey SHALL provide both `live` and `test` variants.

```typescript
export default VMRuntime.key(SessionSetupVM, {
  live: layerLive,
  test: layer,
});
```

(a) The `live` variant SHALL provide the complete dependency graph for production execution.

(b) The `test` variant SHALL provide the minimal layer, allowing tests to inject mock dependencies.

---

## CHAPTER 7: TESTING REQUIREMENTS

### § 7.1 Testing Protocol

Tests SHALL use the `live` layer variant with test dependencies injected.

Tests must not test the `test` layer directly.

```typescript
// Compliant:
describe("ChatVM", () => {
  const ChatServiceMock = Layer.succeed(ChatService.ChatService, {
    handleUserMessage: () => Effect.succeed(undefined),
    exportChat: () => Effect.succeed({ json: "{}", filename: "test.json" }),
  });

  const TestLayer = pipe(
    ChatVMKey.variants.live,
    Layer.provide(ChatServiceMock),
    Layer.provide(TestSessionLayer),
  );

  it("sends messages via ChatService", () => /* test with TestLayer */);
});
```

Direct testing of the `test` variant is prohibited:

```typescript
// Prohibited:
describe("ChatVM", () => {
  it("tests nothing of value", () => {
    const vm = buildVM(ChatVMKey.variants.test);
  });
});
```

The `test` variant exists for dependency injection, not for direct testing.

---

## SCHEDULE A: COMPLIANCE CHECKLIST

Before any View Model is considered complete, the following SHALL be verified:

- [ ] **§ 1.1**: VM resides in single `ComponentName.vm.ts` file
- [ ] **§ 1.2**: Interface and tag share identical name
- [ ] **§ 2.1**: Live layer exports with full production dependencies
- [ ] **§ 2.2**: Default export uses `VMRuntime.key()` with live and test variants
- [ ] **§ 2.3**: All imports use namespace pattern
- [ ] **§ 3.1**: No business logic in VM; all logic delegated to services
- [ ] **§ 3.2**: All services yielded from context, none constructed
- [ ] **§ 4.1**: All atoms use `$` suffix
- [ ] **§ 4.2**: All atoms defined inside `Effect.gen` within layer
- [ ] **§ 5.1**: Sync actions use `registry.set()`
- [ ] **§ 5.2**: Async actions use `VMRuntime.fn()`
- [ ] **§ 5.3**: Async actions wrapped with `Effect.withSpan()`
- [ ] **§ 6.1**: Both `live` and `test` variants provided
- [ ] **§ 7.1**: Tests use `live` variant with injected test dependencies

---

## SCHEDULE B: CANONICAL TEMPLATE

```typescript
import * as Atom from "@effect-atom/atom/Atom";
import { AtomRegistry } from "@effect-atom/atom/Registry";
import * as Result from "@effect-atom/atom/Result";
import * as Context from "effect/Context";
import * as Effect from "effect/Effect";
import * as Layer from "effect/Layer";
import { pipe } from "effect/Function";
import { VMRuntime } from "@/lib/VMRuntime.js";
import * as SomeService from "../../services/SomeService.js";
import { FullLayer } from "../../lib/FullLayer.js";

// =============================================================================
// Interface
// =============================================================================

export interface ComponentNameVM {
  readonly data$: Atom.Atom<SomeData>;
  readonly isLoading$: Atom.Atom<boolean>;
  readonly setValue: (value: string) => void;
  readonly submitAtom: Atom.AtomResultFn<void, void, unknown>;
}

export const ComponentNameVM = Context.GenericTag<ComponentNameVM>("ComponentNameVM");

// =============================================================================
// Layer
// =============================================================================

const layer = Layer.effect(
  ComponentNameVM,
  Effect.gen(function* () {
    const registry = yield* AtomRegistry;
    const service = yield* SomeService.SomeService;

    const data$ = Atom.make<SomeData>(initialData);

    const submitAtom = VMRuntime.fn((_: void, get: Atom.FnContext) =>
      Effect.gen(function* () {
        yield* service.submit(get(data$));
      }).pipe(Effect.withSpan("ComponentName.submit"))
    );

    const isLoading$ = pipe(submitAtom, Atom.map(Result.isWaiting));

    return {
      data$,
      isLoading$,
      setValue: (value: string) => registry.set(data$, value),
      submitAtom,
    };
  })
);

// =============================================================================
// Export
// =============================================================================

export default VMRuntime.key(ComponentNameVM, {
  live: pipe(layer, Layer.provide(FullLayer)),
  test: layer,
});
```
