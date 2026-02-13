---
name: navigation-patterns
description: "Expert navigation decisions for iOS/tvOS: when NavigationStack vs Coordinator patterns, NavigationPath state management trade-offs, deep link architecture choices, and tab+navigation coordination strategies. Use when designing app navigation, implementing deep links, or debugging navigation state issues. Trigger keywords: NavigationStack, NavigationPath, deep link, routing, tab bar, navigation, programmatic navigation, universal link, URL scheme, navigation state"
version: "3.0.0"
---

# Navigation Patterns — Expert Decisions

Expert decision frameworks for SwiftUI navigation choices. Claude knows NavigationStack syntax — this skill provides judgment calls for architecture decisions and state management trade-offs.

---

## Decision Trees

### Navigation Architecture Selection

```
How complex is your navigation?
├─ Simple (linear flows, 1-3 screens)
│  └─ NavigationStack with inline NavigationLink
│     No Router needed
│
├─ Medium (multiple flows, deep linking required)
│  └─ NavigationStack + Router (ObservableObject)
│     Centralized navigation state
│
└─ Complex (tabs with independent stacks, cross-tab navigation)
   └─ Tab Coordinator + per-tab Routers
      Each tab maintains own NavigationPath
```

### NavigationPath vs Typed Array

```
Do you need heterogeneous routes?
├─ YES (different types in same stack)
│  └─ NavigationPath (type-erased)
│     path.append(User(...))
│     path.append(Product(...))
│
└─ NO (single route enum)
   └─ @State var path: [Route] = []
      Type-safe, debuggable, serializable
```

**Rule**: Prefer typed arrays unless you genuinely need mixed types. NavigationPath's type erasure makes debugging harder.

### Deep Link Handling Strategy

```
When does deep link arrive?
├─ App already running (warm start)
│  └─ Direct navigation via Router
│
└─ App launches from deep link (cold start)
   └─ Is view hierarchy ready?
      ├─ YES → Navigate immediately
      └─ NO → Queue pending deep link
         Handle in root view's .onAppear
```

### Modal vs Push Selection

```
Is the destination a self-contained flow?
├─ YES (can complete/cancel independently)
│  └─ Modal (.sheet or .fullScreenCover)
│     Examples: Settings, Compose, Login
│
└─ NO (part of current navigation hierarchy)
   └─ Push (NavigationLink or path.append)
      Examples: Detail views, drill-down
```

---

## NEVER Do

### NavigationPath State

**NEVER** store NavigationPath in ViewModel without careful consideration:
```swift
// ❌ ViewModel owns navigation — couples business logic to navigation
@MainActor
final class HomeViewModel: ObservableObject {
    @Published var path = NavigationPath()  // Wrong layer!
}

// ✅ Router/Coordinator owns navigation, ViewModel owns data
@MainActor
final class Router: ObservableObject {
    @Published var path = NavigationPath()
}

@MainActor
final class HomeViewModel: ObservableObject {
    @Published var items: [Item] = []  // Data only
}
```

**NEVER** use NavigationPath across tabs:
```swift
// ❌ Shared path across tabs — navigation becomes unpredictable
struct MainTabView: View {
    @StateObject var router = Router()  // Single router!

    var body: some View {
        TabView {
            // Both tabs share same path — chaos
        }
    }
}

// ✅ Each tab has independent navigation stack
struct MainTabView: View {
    @StateObject var homeRouter = Router()
    @StateObject var searchRouter = Router()

    var body: some View {
        TabView {
            NavigationStack(path: $homeRouter.path) { ... }
            NavigationStack(path: $searchRouter.path) { ... }
        }
    }
}
```

**NEVER** forget to handle deep links arriving before view hierarchy:
```swift
// ❌ Race condition — navigation may fail silently
@main
struct MyApp: App {
    @StateObject var router = Router()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .onOpenURL { url in
                    router.handle(url)  // View may not exist yet!
                }
        }
    }
}

// ✅ Queue deep link for deferred handling
@main
struct MyApp: App {
    @StateObject var router = Router()
    @State private var pendingDeepLink: URL?

    var body: some Scene {
        WindowGroup {
            ContentView()
                .onAppear {
                    if let url = pendingDeepLink {
                        router.handle(url)
                        pendingDeepLink = nil
                    }
                }
                .onOpenURL { url in
                    pendingDeepLink = url
                }
        }
    }
}
```

### Route Design

**NEVER** use stringly-typed routes:
```swift
// ❌ No compile-time safety, typos cause runtime failures
func navigate(to screen: String) {
    switch screen {
    case "profile": ...
    case "setings": ...  // Typo — silent failure
    }
}

// ✅ Enum routes with associated values
enum Route: Hashable {
    case profile(userId: String)
    case settings
}
```

**NEVER** put navigation logic in Views:
```swift
// ❌ View knows too much about app structure
struct ItemRow: View {
    var body: some View {
        NavigationLink {
            ItemDetailView(item: item)  // View creates destination
        } label: {
            Text(item.name)
        }
    }
}

// ✅ Delegate navigation to Router
struct ItemRow: View {
    @EnvironmentObject var router: Router

    var body: some View {
        Button(item.name) {
            router.navigate(to: .itemDetail(item.id))
        }
    }
}
```

### Navigation State Persistence

**NEVER** lose navigation state on app termination without consideration:
```swift
// ❌ User loses their place when app is killed
@StateObject var router = Router()  // State lost on terminate

// ✅ Persist for important flows (optional based on UX needs)
@SceneStorage("navigationPath") private var pathData: Data?

var body: some View {
    NavigationStack(path: $router.path) { ... }
        .onAppear { router.restore(from: pathData) }
        .onChange(of: router.path) { pathData = router.serialize() }
}
```

---

## Essential Patterns

### Type-Safe Router

```swift
@MainActor
final class Router: ObservableObject {
    enum Route: Hashable {
        case userList
        case userDetail(userId: String)
        case settings
        case settingsSection(SettingsSection)
    }

    @Published var path: [Route] = []

    func navigate(to route: Route) {
        path.append(route)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    func popToRoot() {
        path.removeAll()
    }

    func replaceStack(with routes: [Route]) {
        path = routes
    }

    @ViewBuilder
    func destination(for route: Route) -> some View {
        switch route {
        case .userList:
            UserListView()
        case .userDetail(let userId):
            UserDetailView(userId: userId)
        case .settings:
            SettingsView()
        case .settingsSection(let section):
            SettingsSectionView(section: section)
        }
    }
}
```

### Deep Link Handler

```swift
enum DeepLink {
    case user(id: String)
    case product(id: String)
    case settings

    init?(url: URL) {
        guard let scheme = url.scheme,
              ["myapp", "https"].contains(scheme) else { return nil }

        let path = url.path.trimmingCharacters(in: CharacterSet(charactersIn: "/"))
        let components = path.components(separatedBy: "/")

        switch components.first {
        case "user":
            guard components.count > 1 else { return nil }
            self = .user(id: components[1])
        case "product":
            guard components.count > 1 else { return nil }
            self = .product(id: components[1])
        case "settings":
            self = .settings
        default:
            return nil
        }
    }
}

extension Router {
    func handle(_ deepLink: DeepLink) {
        popToRoot()

        switch deepLink {
        case .user(let id):
            navigate(to: .userList)
            navigate(to: .userDetail(userId: id))
        case .product(let id):
            navigate(to: .productDetail(productId: id))
        case .settings:
            navigate(to: .settings)
        }
    }
}
```

### Tab + Navigation Coordination

```swift
struct MainTabView: View {
    @State private var selectedTab: Tab = .home
    @StateObject private var homeRouter = Router()
    @StateObject private var profileRouter = Router()

    enum Tab { case home, search, profile }

    var body: some View {
        TabView(selection: $selectedTab) {
            NavigationStack(path: $homeRouter.path) {
                HomeView()
                    .navigationDestination(for: Router.Route.self) { route in
                        homeRouter.destination(for: route)
                    }
            }
            .tag(Tab.home)
            .environmentObject(homeRouter)

            NavigationStack(path: $profileRouter.path) {
                ProfileView()
                    .navigationDestination(for: Router.Route.self) { route in
                        profileRouter.destination(for: route)
                    }
            }
            .tag(Tab.profile)
            .environmentObject(profileRouter)
        }
    }

    // Pop to root on tab re-selection
    func tabSelected(_ tab: Tab) {
        if selectedTab == tab {
            switch tab {
            case .home: homeRouter.popToRoot()
            case .profile: profileRouter.popToRoot()
            case .search: break
            }
        }
        selectedTab = tab
    }
}
```

---

## Quick Reference

### Navigation Architecture Comparison

| Pattern | Complexity | Deep Link Support | Testability |
|---------|------------|-------------------|-------------|
| Inline NavigationLink | Low | Manual | Low |
| Router with typed array | Medium | Good | High |
| NavigationPath | Medium | Good | Medium |
| Coordinator Pattern | High | Excellent | Excellent |

### When to Use Each Modal Type

| Modal Type | Use For |
|------------|---------|
| `.sheet` | Secondary tasks, can dismiss |
| `.fullScreenCover` | Immersive flows (onboarding, login) |
| `.alert` | Critical decisions |
| `.confirmationDialog` | Action choices |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| NavigationPath across tabs | State confusion | Per-tab routers |
| View creates destination directly | Tight coupling | Router pattern |
| String-based routing | No compile safety | Enum routes |
| Deep link ignored on cold start | Race condition | Pending URL queue |
| ViewModel owns NavigationPath | Layer violation | Router owns navigation |
| No popToRoot on tab re-tap | UX expectation | Handle tab selection |
