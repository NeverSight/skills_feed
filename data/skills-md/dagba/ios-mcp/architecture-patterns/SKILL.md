---
name: architecture-patterns
description: Choose and implement iOS architecture patterns (MVVM, TCA, Clean Architecture) based on feature complexity. Use when designing architecture for new features or refactoring existing code.
---

# Architecture Patterns

## Overview

Quick reference for choosing and implementing iOS architecture patterns. Focused on decision criteria, not tutorials.

## Pattern Selection

| Complexity | Pattern | Use When |
|------------|---------|----------|
| Simple | MV | Single screen, local state only |
| Medium | MVVM | 2-5 screens, business logic, network calls |
| Complex | TCA | State machines, side effects, complex flows |
| Enterprise | Clean | Multiple teams, maximum modularity |

## Decision Tree

```
1. Single screen + local state only?
   → MV (SwiftUI View + @State)

2. Business logic or shared state?
   → MVVM

3. Complex state transitions?
   → TCA

4. Multi-team, high modularity?
   → Clean Architecture
```

## MVVM Pattern (Most Common)

**Structure:**
- ViewModels: `@Observable`, protocol-based DI
- Views: `@State private var viewModel`
- Services: Protocols for testability

**Critical Rules:**
- ✅ Protocol-based DI via init (enables mocking)
- ✅ `@MainActor` for state updates
- ✅ Keep Views dumb (delegate to ViewModel)
- ❌ Never import SwiftUI in ViewModels
- ❌ Never use `@Published` (use `@Observable`)
- ❌ Never make ViewModels optional

**Minimal Example:**
```swift
protocol AuthServiceProtocol {
    func login(_ email: String, _ password: String) async throws -> User
}

@Observable
final class LoginViewModel {
    private let authService: AuthServiceProtocol
    var email = ""
    var password = ""
    var isLoading = false

    init(authService: AuthServiceProtocol = AuthService()) {
        self.authService = authService
    }

    @MainActor
    func login() async {
        isLoading = true
        defer { isLoading = false }
        try? await authService.login(email, password)
    }
}

struct LoginView: View {
    @State private var viewModel = LoginViewModel()
    var body: some View {
        Form {
            TextField("Email", text: $viewModel.email)
            SecureField("Password", text: $viewModel.password)
            Button("Login") { Task { await viewModel.login() } }
                .disabled(viewModel.isLoading)
        }
    }
}
```

## TCA Pattern

**Use for:** Complex state machines, side effects, time-travel debugging

**Key:** Single `Reducer` with State/Action/Dependencies. Exhaustive testing via `TestStore`.

Reference: [TCA documentation](https://github.com/pointfreeco/swift-composable-architecture)

## Clean Architecture

**Use for:** Enterprise apps, multiple teams, maximum testability

**Patterns:**
- **VIP (View-Interactor-Presenter)**: Use `vip-clean-architecture` skill for unidirectional data flow, protocol-based boundaries, and Spy-pattern testing
- **Generic Clean**: Domain (entities, use cases) → Data (repositories, network) → Presentation (ViewModels, Views)

**Key:** Dependency inversion, protocol-based boundaries between layers

## References

For detailed implementation examples and migration guides, see:
- `references/mvvm-patterns.md`
- `references/tca-guide.md`
- `references/clean-architecture.md`

---

**Word count:** ~300 (was 2,863)
**For:** Senior/mid iOS engineers who know how to code
**Focus:** Decision-making, not hand-holding
