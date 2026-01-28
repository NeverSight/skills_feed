---
name: react-vm
description: Implement the VM pattern using Effect and Effect-Atom for reactive, testable frontend state management. Use this skill when building React applications with View Models that bridge domain services and UI.
---

# Effectful View Model Architecture Guide

## The Golden Rule: Zero UI Logic

**VMs take domain input → VMs produce UI-ready output → Components are pure renderers**

VM transforms domain to UI-ready:
- `User` entity → `displayName: "John D."`
- `timestamp: 1702425600` → `formattedDate: "Dec 13, 2024"`
- `balance: 1000000n` → `displayBalance: "$1,000,000"`
- `isActive && hasAccess` → `canEdit: true`
- `error.code` → `errorMessage: "Network failed"`

**Components must NEVER:** format strings/dates/numbers, compute derived values, contain business logic, transform entities

**Components ONLY:** subscribe via `useAtomValue`, invoke via `useAtomSet`, pattern match with `$match`, render UI-ready values

**Error handling:** Components CAN pattern match on error states (to render different UI per error type), but MUST render `error.message` as-is—VM is responsible for producing user-friendly messages

---

## File Structure

Every **parent component** needs a VM:

```
components/
  Wallet/
    Wallet.tsx       # Component - pure renderer
    Wallet.vm.ts     # VM - interface, tag, default layer export
    index.ts         # Re-exports
```

Child components used for UI composition receive VM as props—only parent components define their own VM.

---

## VMs vs Regular Layers

**VMs are strictly UI constructs.** A VM only exists if a component for that exact VM exists.

| Pattern | When to Use | Location |
|---------|-------------|----------|
| **VM** | Layer serves a React component | `components/X/X.vm.ts` paired with `X.tsx` |
| **Service Layer** | Non-UI logic, shared business rules | `services/`, `lib/`, etc. |

```typescript
// ❌ WRONG - No component uses this, not a VM
// components/Analytics/Analytics.vm.ts  (but no Analytics.tsx!)

// ✅ CORRECT - Just a service layer
// services/Analytics.ts
export class AnalyticsService extends Context.Tag("AnalyticsService")<
  AnalyticsService,
  { track: (event: string) => Effect.Effect<void> }
>() {}
```

**When VMs share logic**: Use standard Effect layer composition. Shared logic lives in service layers, VMs compose over them:

```typescript
import { Context, Effect, Layer } from "effect"
import { AtomRegistry } from "@effect-atom/atom/Registry"
interface Consent { id: string }
declare var ConsentListVM: Context.Tag<ConsentListVM, ConsentListVM>
interface ConsentListVM {}

// services/ConsentService.ts - shared business logic
export class ConsentService extends Context.Tag("ConsentService")<
  ConsentService,
  { getConsents: Effect.Effect<Consent[]> }
>() {}

// components/ConsentList/ConsentList.vm.ts - UI-specific, uses service
const layer = Layer.effect(
  ConsentListVM,
  Effect.gen(function* () {
    const consentService = yield* ConsentService  // Compose over service
    const registry = yield* AtomRegistry
    // ... VM-specific UI state
  })
)
```

---

## Architecture Flow

- Component calls `useVM(tag, layer)` → VMRuntime lazily builds VM via `Layer.buildWithMemoMap` → VM yields services from infrastructure layers
- VMRuntime provides render-stable scope for all VMs
- User action → VM action (updates atom via registry) → atom notifies → `useAtomValue` re-renders

---

## VM File Pattern

Each VM file contains: interface, tag, and default `{ tag, layer }` export.

```typescript
// components/Wallet/Wallet.vm.ts
import * as Atom from "@effect-atom/atom/Atom"
import { AtomRegistry } from "@effect-atom/atom/Registry"
import { Context, Layer, Effect, pipe, Data } from "effect"

// State machine
export type WalletState = Data.TaggedEnum<{
  Disconnected: {}
  Connecting: {}
  Connected: { displayAddress: string; fullAddress: string }
}>
export const WalletState = Data.taggedEnum<WalletState>()

// 1. Interface - atoms use camelCase with $ suffix
export interface WalletVM {
  readonly state$: Atom.Atom<WalletState>
  readonly isConnected$: Atom.Atom<boolean>  // Derived, UI-ready
  readonly connect: () => void               // Actions return void
  readonly disconnect: () => void
}

// 2. Tag
export const WalletVM = Context.GenericTag<WalletVM>("WalletVM")

// 3. Layer - atoms ONLY defined inside the layer
// VMRuntime provides scope, so Layer.effect is the default
const layer = Layer.effect(
  WalletVM,
  Effect.gen(function* () {
    const registry = yield* AtomRegistry
    const walletService = yield* WalletService

    // Atoms defined here, inside the layer
    const state$ = Atom.make<WalletState>(WalletState.Disconnected())
    const isConnected$ = pipe(state$, Atom.map(WalletState.$is("Connected")))

    const connect = () => {
      registry.set(state$, WalletState.Connecting())
      Effect.runPromise(
        walletService.connect.pipe(
          Effect.match({
            onFailure: () => registry.set(state$, WalletState.Disconnected()),
            onSuccess: (addr) => registry.set(state$, WalletState.Connected({
              displayAddress: `${addr.slice(0,6)}...${addr.slice(-4)}`,
              fullAddress: addr
            }))
          })
        )
      )
    }

    const disconnect = () => {
      registry.set(state$, WalletState.Disconnected())
    }

    return { state$, isConnected$, connect, disconnect }
  })
)

// 4. Default export
export default { tag: WalletVM, layer }
```

---

## Component Pattern

```tsx
// components/Wallet/Wallet.tsx
"use client"
import { useVM } from "@/lib/VMRuntime"
import { useAtomValue } from "@effect-atom/atom-react"
import * as Result from "@effect-atom/atom/Result"
import WalletVM, { WalletState, type WalletVM as WalletVMType } from "./Wallet.vm"

// Child components receive VM as prop - no own VM needed
function WalletStatus({ vm }: { vm: WalletVMType }) {
  const state = useAtomValue(vm.state$)

  return WalletState.$match(state, {
    Disconnected: () => <span>Not connected</span>,
    Connecting: () => <Spinner />,
    Connected: ({ displayAddress }) => <span>{displayAddress}</span>
  })
}

function WalletActions({ vm }: { vm: WalletVMType }) {
  const isConnected = useAtomValue(vm.isConnected$)

  return isConnected
    ? <button onClick={vm.disconnect}>Disconnect</button>
    : <button onClick={vm.connect}>Connect</button>
}

// Parent component owns VM
export default function Wallet() {
  const vmResult = useVM(WalletVM.tag, WalletVM.layer)

  return Result.match(vmResult, {
    onInitial: () => <Spinner />,
    onSuccess: ({ value: vm }) => (
      <div className="wallet">
        <WalletStatus vm={vm} />
        <WalletActions vm={vm} />
      </div>
    ),
    onFailure: ({ cause }) => <Alert>{String(cause)}</Alert>
  })
}
```

---

## Core Pattern: Atom.fn for Async Actions

**Key insight**: Use `Atom.fn` with `Effect.fnUntraced` for effect-based actions. This gives you:
1. Automatic `waiting` flag for loading state
2. `Result<Success, Error>` with Initial/Success/Failure states
3. No manual state management or void wrappers

```tsx
import { Atom, useAtomValue, useAtomSet } from "@effect-atom/atom-react"
import * as Result from "@effect-atom/atom/Result"
import { Effect, Exit } from "effect"

// Define action with Atom.fn + Effect.fnUntraced
const refreshAtom = Atom.fn(
  Effect.fnUntraced(function* () {
    const consents = yield* consentService.getOwnConsents
    return consents
  })
)

// In component - useAtom for result and trigger
function ConsentList() {
  const [result, refresh] = useAtom(refreshAtom)

  // result.waiting is true while the effect runs
  const isLoading = result.waiting

  return (
    <div>
      <button onClick={() => refresh()} disabled={isLoading}>
        {isLoading ? "Loading..." : "Refresh"}
      </button>
      {Result.matchWithWaiting(result, {
        onWaiting: () => <Loading />,
        onSuccess: ({ value }) => <List items={value} />,
        onError: (error) => <Error message={String(error)} />,
        onDefect: (defect) => <Error message={String(defect)} />
      })}
    </div>
  )
}
```

**With services using Atom.runtime:**

```tsx
class ConsentService extends Effect.Service<ConsentService>()("ConsentService", {
  effect: Effect.gen(function* () {
    const getAll = Effect.succeed([{ id: "1", name: "Terms" }])
    return { getAll } as const
  }),
}) {}

const runtimeAtom = Atom.runtime(ConsentService.Default)

const refreshAtom = runtimeAtom.fn(
  Effect.fnUntraced(function* () {
    const service = yield* ConsentService
    return yield* service.getAll
  })
)
```

**With promiseExit for async handlers:**

```tsx
function CreateUser() {
  // mode: "promiseExit" returns Promise<Exit<...>> for await
  const createUser = useAtomSet(createUserAtom, { mode: "promiseExit" })

  return (
    <button onClick={async () => {
      const exit = await createUser("John")
      if (Exit.isSuccess(exit)) {
        console.log(exit.value)
      }
    }}>
      Create
    </button>
  )
}
```

**Anti-pattern: Manual void wrappers**

```typescript
// ❌ DON'T - manual state management loses waiting control
const loading$ = Atom.make(false)
const data$ = Atom.make<Data | null>(null)

const refresh = (): void => {
  registry.set(loading$, true)
  Effect.runPromise(fetchData).then(data => {
    registry.set(data$, data)
    registry.set(loading$, false)
  })
}

// ✅ DO - Atom.fn handles everything
const refreshAtom = Atom.fn(Effect.fnUntraced(function* () {
  return yield* fetchData
}))
// result.waiting, Result.matchWithWaiting - all built-in
```

---

## Building Blocks

### Atoms & Registry

Atoms are ONLY defined inside VM layers:

```typescript
// Inside Layer.effect or Layer.scoped
const registry = yield* AtomRegistry

// Writable atom - camelCase with $ suffix
const count$ = Atom.make(0)

// Derived atom (read-only)
const doubled$ = pipe(count$, Atom.map((n) => n * 2))

// Read/write via registry
registry.get(count$)      // read
registry.set(count$, 42)  // write
```

### Data.TaggedEnum - State Machines

```tsx
export type WalletState = Data.TaggedEnum<{
  Disconnected: {}
  Connecting: {}
  Connected: { displayAddress: string; fullAddress: string }
}>
export const WalletState = Data.taggedEnum<WalletState>()

// Pattern match in UI
WalletState.$match(state, {
  Disconnected: () => <ConnectButton />,
  Connecting: () => <Spinner />,
  Connected: ({ displayAddress }) => <span>{displayAddress}</span>
})
```

### VMs with Lists (Atom.family)

```typescript
const makeConsentItemVM = Atom.family((consent: Consent): ConsentItemVM => {
  const status$ = pipe(consentsState$, Atom.map((either) =>
    Either.match(either, {
      onLeft: () => ConsentStatus.Active(),
      onRight: (consents) => {
        const c = consents.find(x => x.consentId === consent.consentId)
        return c?.isRevoked ? ConsentStatus.Revoked() : ConsentStatus.Active()
      }
    })
  ))

  // Close over consent.consentId - UI never sees it
  const revoke = () => {
    Effect.gen(function* () {
      yield* consentService.revokeById(consent.consentId)
      yield* refresh()
    }).pipe(Effect.runFork)
  }

  return { key: consent.consentId, status$, revoke }
})
```

### Event Listeners → Atom with Finalizer

Instead of `useEffect` for event listeners, use `Atom.make` with `get.addFinalizer`:

```typescript
// Window scroll position - auto-cleanup when atom is no longer used
const scrollY$ = Atom.make((get) => {
  const onScroll = () => get.setSelf(window.scrollY)
  window.addEventListener("scroll", onScroll)
  get.addFinalizer(() => window.removeEventListener("scroll", onScroll))
  return window.scrollY
})

// Resize observer
const windowSize$ = Atom.make((get) => {
  const update = () => get.setSelf({ width: window.innerWidth, height: window.innerHeight })
  window.addEventListener("resize", update)
  get.addFinalizer(() => window.removeEventListener("resize", update))
  return { width: window.innerWidth, height: window.innerHeight }
})
```

### URL Search Params → Atom.searchParam

Instead of `useEffect` + `useSearchParams`, use `Atom.searchParam`:

```typescript
// Simple string param
const filter$ = Atom.searchParam("filter")  // Atom.Writable<string>

// With schema parsing
const page$ = Atom.searchParam("page", {
  schema: Schema.NumberFromString
})  // Atom.Writable<Option<number>>

// Multiple params for a search form
const search$ = Atom.searchParam("q")
const sort$ = Atom.searchParam("sort")
const limit$ = Atom.searchParam("limit", { schema: Schema.NumberFromString })
```

---

## VMRuntime Hook

```typescript
// lib/VMRuntime.ts
const memoMap = Layer.makeMemoMap.pipe(Effect.runSync)

const vmAtom = Atom.family(<Id, Value, E>(key: VmKey<Id, Value, E>) =>
  Atom.make(
    Effect.gen(function* () {
      const scope = yield* Scope.Scope
      const ctx = yield* Layer.buildWithMemoMap(key.layer, memoMap, scope)
      return Context.get(ctx, key.tag)
    })
  )
)

export const useVM = <Id, Value, E>(
  tag: Context.Tag<Id, Value>,
  layer: Layer.Layer<Id, E, Scope.Scope | AtomRegistry>
): Result.Result<Value, E> => useAtomValue(vmAtom(makeVmKey(tag, layer)))
```

---

## React Integration

### Provider Setup

```tsx
// app/providers.tsx
import { RegistryProvider } from "@effect-atom/atom-react"

export function Providers({ children }: { children: React.ReactNode }) {
  return <RegistryProvider>{children}</RegistryProvider>
}
```

### Hooks Reference

| Hook | Purpose |
|------|---------|
| `useAtomValue(atom$)` | Subscribe to value |
| `useAtomSet(atom$)` | Get setter function |
| `useAtom(atom$)` | Get `[value, setter]` |

---

## Testing VMs

```typescript
describe("WalletVM", () => {
  const WalletServiceMock = Layer.succeed(WalletService, WalletService.of({
    connect: Effect.succeed("0x1234..."),
    disconnect: Effect.succeed(undefined)
  }))

  const makeVM = () => {
    const r = Registry.make()
    const vm = Layer.build(WalletVM.layer).pipe(
      Effect.map((ctx) => Context.get(ctx, WalletVM.tag)),
      Effect.scoped,
      Effect.provideService(Registry.AtomRegistry, r),
      Effect.provide(WalletServiceMock),
      Effect.runSync
    )
    return { r, vm }
  }

  it("should start disconnected", () => {
    const { r, vm } = makeVM()
    expect(WalletState.$is("Disconnected")(r.get(vm.state$))).toBe(true)
  })

  it("should connect wallet", async () => {
    const { r, vm } = makeVM()
    vm.connect()
    await new Promise(r => setTimeout(r, 10))
    expect(WalletState.$is("Connected")(r.get(vm.state$))).toBe(true)
  })
})
```

---

## Best Practices

**Core Pattern**
- Use `Atom.fn()` for async actions—gives you `AtomResultFn` with automatic `waiting` flag
- Use `useAtom(action$)` to get `[result, trigger]` tuple
- `Result.matchWithWaiting` for rendering async states (onWaiting/onSuccess/onError/onDefect)
- `Result.match` for one-time builds like VM initialization (onInitial/onSuccess/onFailure)
- Never manually wrap Effects in void functions—you lose `waiting` control

**Naming & Structure**
- Atoms use `camelCase$` suffix
- Every parent component: `Component.tsx` + `Component.vm.ts`
- Child components receive VM as prop (no own VM)
- VM file exports: interface, tag, default `{ tag, layer }`

**Interface Design**
- ALL formatting happens in VM—components receive ready-to-render strings
- Use `key` for React, close over IDs in callbacks

### UI-Ready Output Examples

```tsx
// WRONG - Logic in component
function UserCard({ vm }: { vm: UserVM }) {
  const user = useAtomValue(vm.user$)
  const balance = useAtomValue(vm.balance$)

  // NO! Formatting in component
  const displayName = `${user.firstName} ${user.lastName.charAt(0)}.`
  const formattedBalance = new Intl.NumberFormat('en-US', {
    style: 'currency', currency: 'USD'
  }).format(balance / 100)
  const isVip = balance > 10000 && user.memberSince < Date.now() - 31536000000

  return (
    <div>
      <h2>{displayName}</h2>
      <span>{formattedBalance}</span>
      {isVip && <VipBadge />}  {/* NO! Conditional logic */}
    </div>
  )
}

// CORRECT - VM produces UI-ready values
interface UserVM {
  readonly displayName$: Atom.Atom<string>       // "John D."
  readonly formattedBalance$: Atom.Atom<string>  // "$1,234.56"
  readonly showVipBadge$: Atom.Atom<boolean>     // true/false
}

function UserCard({ vm }: { vm: UserVM }) {
  const displayName = useAtomValue(vm.displayName$)
  const formattedBalance = useAtomValue(vm.formattedBalance$)
  const showVipBadge = useAtomValue(vm.showVipBadge$)

  return (
    <div>
      <h2>{displayName}</h2>
      <span>{formattedBalance}</span>
      {showVipBadge && <VipBadge />}  {/* OK - just reading a boolean */}
    </div>
  )
}
```

**Implementation**
- Atoms ONLY defined inside VM layers
- `Layer.effect` is the default (VMRuntime provides scope)
- Use `Atom.family` for list item sub-VMs
- Use `Effect.forkScoped` for background tasks
- Handle all errors in actions (update atom on failure)

**Testing**
- Test VMs without UI using registry directly
- Create fresh VM per test
- Mock services with `Layer.succeed`
