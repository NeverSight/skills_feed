---
name: tca
description: Expert guidance on The Composable Architecture (TCA) for Swift, focusing on ReducerProtocol, macros, and testability.
---

# The Composable Architecture (TCA) Guidelines

You are an expert in Point-Free's Composable Architecture. When writing or refactoring TCA code, adhere to these rules:

## 1. Reducer Structure

- ALWAYS use the `@Reducer` macro.
- State and Action must be nested types within the Reducer struct.
- Use `CasePaths` logic implicitly via the `Bindable` and `Pulsar` patterns where applicable (though `CasePath` is rarely manual now).
- Actions should be named `delegate`, `view`, and `internal` to separate concerns:
  - `case view(ViewAction)`: User interactions.
  - `case delegate(DelegateAction)`: Communication with parent reducers.
  - `case internal(InternalAction)`: Side-effect results.

## 2. Dependencies

- Use the `@Dependency(\.clientName)` pattern.
- NEVER reach out to global singletons.
- Always define a `testValue` and `previewValue` for every custom dependency.

## 3. Effects & Concurrency

- Use `.run { send in ... }` for asynchronous side effects.
- Avoid `Effect.task` unless strictly necessary for simple bridging.
- Ensure all loops in effects handle cancellation properly via `.cancellable(id:)`.

## 4. Testing

- Use `TestStore` for all logic verification.
- Enforce exhaustivity: `store.exhaustivity = .on`.
- Mock all dependencies in tests using `withDependencies`.

## Example

```swift
@Reducer
struct Feature {
    @ObservableState
    struct State: Equatable {
        var count = 0
    }
    enum Action {
        case view(ViewAction)
        case internal(InternalAction)

        enum ViewAction {
            case incrementButtonTapped
        }
        enum InternalAction {
            case loadResponse(Int)
        }
    }

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .view(.incrementButtonTapped):
                state.count += 1
                return .none
            }
        }
    }
}
