---
name: swift-architecture
description: Master iOS/macOS app architecture - MVVM, Clean Architecture, Coordinator, DI, Repository
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 05-swift-macos
bond_type: SECONDARY_BOND
---

# Swift Architecture Skill

Design patterns and architectural approaches for scalable, testable Swift applications.

## Prerequisites

- Understanding of SOLID principles
- Familiarity with dependency injection
- Experience with protocol-oriented programming

## Parameters

```yaml
parameters:
  architecture_pattern:
    type: string
    enum: [mvvm, mvc, tca, viper, clean]
    default: mvvm
  navigation_pattern:
    type: string
    enum: [coordinator, router, navigation_stack]
    default: coordinator
  di_approach:
    type: string
    enum: [manual, container, property_wrapper]
    default: manual
```

## Topics Covered

### Architecture Patterns
| Pattern | Complexity | Testability | Best For |
|---------|------------|-------------|----------|
| MVC | Low | Low | Simple apps |
| MVVM | Medium | High | Most apps |
| Clean | High | Very High | Large teams |
| TCA | High | Very High | Complex state |
| VIPER | Very High | Very High | Enterprise |

### Key Principles
| Principle | Description |
|-----------|-------------|
| Separation of Concerns | Each layer has one job |
| Dependency Inversion | Depend on abstractions |
| Single Source of Truth | One place for state |
| Unidirectional Data Flow | State → View → Action → State |

### Layer Responsibilities
| Layer | Responsibility |
|-------|----------------|
| View | UI rendering only |
| ViewModel | Presentation logic |
| UseCase | Business logic |
| Repository | Data access |
| Service | External integrations |

## Code Examples

### MVVM with Coordinator
```swift
// MARK: - Coordinator Protocol

protocol Coordinator: AnyObject {
    var navigationController: UINavigationController { get }
    var childCoordinators: [Coordinator] { get set }
    func start()
}

extension Coordinator {
    func addChild(_ coordinator: Coordinator) {
        childCoordinators.append(coordinator)
    }

    func removeChild(_ coordinator: Coordinator) {
        childCoordinators.removeAll { $0 === coordinator }
    }
}

// MARK: - App Coordinator

final class AppCoordinator: Coordinator {
    let navigationController: UINavigationController
    var childCoordinators: [Coordinator] = []
    private let dependencies: AppDependencies

    init(navigationController: UINavigationController, dependencies: AppDependencies) {
        self.navigationController = navigationController
        self.dependencies = dependencies
    }

    func start() {
        if dependencies.authService.isLoggedIn {
            showMain()
        } else {
            showLogin()
        }
    }

    private func showLogin() {
        let coordinator = LoginCoordinator(
            navigationController: navigationController,
            dependencies: dependencies
        )
        coordinator.delegate = self
        addChild(coordinator)
        coordinator.start()
    }

    private func showMain() {
        let coordinator = MainCoordinator(
            navigationController: navigationController,
            dependencies: dependencies
        )
        addChild(coordinator)
        coordinator.start()
    }
}

extension AppCoordinator: LoginCoordinatorDelegate {
    func loginDidComplete(_ coordinator: LoginCoordinator) {
        removeChild(coordinator)
        showMain()
    }
}

// MARK: - ViewModel

@MainActor
protocol ProductListViewModelProtocol: ObservableObject {
    var products: [Product] { get }
    var isLoading: Bool { get }
    var error: Error? { get }

    func loadProducts() async
    func selectProduct(_ product: Product)
}

@MainActor
final class ProductListViewModel: ProductListViewModelProtocol {
    @Published private(set) var products: [Product] = []
    @Published private(set) var isLoading = false
    @Published private(set) var error: Error?

    private let getProductsUseCase: GetProductsUseCaseProtocol
    private weak var coordinator: ProductCoordinator?

    init(getProductsUseCase: GetProductsUseCaseProtocol, coordinator: ProductCoordinator) {
        self.getProductsUseCase = getProductsUseCase
        self.coordinator = coordinator
    }

    func loadProducts() async {
        isLoading = true
        error = nil

        do {
            products = try await getProductsUseCase.execute()
        } catch {
            self.error = error
        }

        isLoading = false
    }

    func selectProduct(_ product: Product) {
        coordinator?.showProductDetail(product)
    }
}
```

### Clean Architecture Layers
```swift
// MARK: - Domain Layer (Use Cases)

protocol GetProductsUseCaseProtocol {
    func execute() async throws -> [Product]
}

final class GetProductsUseCase: GetProductsUseCaseProtocol {
    private let repository: ProductRepositoryProtocol

    init(repository: ProductRepositoryProtocol) {
        self.repository = repository
    }

    func execute() async throws -> [Product] {
        let products = try await repository.getProducts()
        // Business logic: filter, sort, validate
        return products.filter { $0.isAvailable }.sorted { $0.name < $1.name }
    }
}

// MARK: - Data Layer (Repository)

protocol ProductRepositoryProtocol {
    func getProducts() async throws -> [Product]
    func getProduct(id: String) async throws -> Product
    func saveProduct(_ product: Product) async throws
}

final class ProductRepository: ProductRepositoryProtocol {
    private let remoteDataSource: ProductRemoteDataSourceProtocol
    private let localDataSource: ProductLocalDataSourceProtocol

    init(remoteDataSource: ProductRemoteDataSourceProtocol,
         localDataSource: ProductLocalDataSourceProtocol) {
        self.remoteDataSource = remoteDataSource
        self.localDataSource = localDataSource
    }

    func getProducts() async throws -> [Product] {
        // Try cache first
        if let cached = try? await localDataSource.getProducts(), !cached.isEmpty {
            // Refresh in background
            Task {
                if let remote = try? await remoteDataSource.fetchProducts() {
                    try? await localDataSource.saveProducts(remote)
                }
            }
            return cached
        }

        // Fetch from remote
        let products = try await remoteDataSource.fetchProducts()
        try? await localDataSource.saveProducts(products)
        return products
    }

    func getProduct(id: String) async throws -> Product {
        try await remoteDataSource.fetchProduct(id: id)
    }

    func saveProduct(_ product: Product) async throws {
        try await remoteDataSource.createProduct(product)
        try await localDataSource.saveProduct(product)
    }
}
```

### Dependency Injection Container
```swift
// MARK: - Dependencies Protocol

protocol HasAuthService {
    var authService: AuthServiceProtocol { get }
}

protocol HasProductRepository {
    var productRepository: ProductRepositoryProtocol { get }
}

typealias AppDependencies = HasAuthService & HasProductRepository

// MARK: - DI Container

final class DependencyContainer: AppDependencies {
    // Singletons
    lazy var authService: AuthServiceProtocol = AuthService()

    // Factories
    lazy var productRepository: ProductRepositoryProtocol = {
        ProductRepository(
            remoteDataSource: ProductRemoteDataSource(apiClient: apiClient),
            localDataSource: ProductLocalDataSource(database: database)
        )
    }()

    private lazy var apiClient: APIClientProtocol = APIClient()
    private lazy var database: DatabaseProtocol = Database()

    // Factory methods for ViewModels
    func makeProductListViewModel(coordinator: ProductCoordinator) -> ProductListViewModel {
        ProductListViewModel(
            getProductsUseCase: GetProductsUseCase(repository: productRepository),
            coordinator: coordinator
        )
    }
}

// MARK: - Property Wrapper Approach

@propertyWrapper
struct Injected<T> {
    private let keyPath: KeyPath<DependencyContainer, T>

    var wrappedValue: T {
        DependencyContainer.shared[keyPath: keyPath]
    }

    init(_ keyPath: KeyPath<DependencyContainer, T>) {
        self.keyPath = keyPath
    }
}

// Usage
final class SomeService {
    @Injected(\.authService) private var authService
}
```

### SwiftUI MVVM
```swift
// MARK: - View

struct ProductListView: View {
    @StateObject private var viewModel: ProductListViewModel

    init(viewModel: @autoclosure @escaping () -> ProductListViewModel) {
        _viewModel = StateObject(wrappedValue: viewModel())
    }

    var body: some View {
        Group {
            if viewModel.isLoading {
                ProgressView()
            } else if let error = viewModel.error {
                ErrorView(error: error) {
                    Task { await viewModel.loadProducts() }
                }
            } else {
                productList
            }
        }
        .navigationTitle("Products")
        .task {
            await viewModel.loadProducts()
        }
    }

    private var productList: some View {
        List(viewModel.products) { product in
            ProductRow(product: product)
                .onTapGesture {
                    viewModel.selectProduct(product)
                }
        }
    }
}

// MARK: - SwiftUI Coordinator (Router)

@MainActor
final class Router: ObservableObject {
    @Published var path = NavigationPath()

    func push<T: Hashable>(_ value: T) {
        path.append(value)
    }

    func pop() {
        path.removeLast()
    }

    func popToRoot() {
        path.removeLast(path.count)
    }
}

struct ContentView: View {
    @StateObject private var router = Router()
    @StateObject private var dependencies = DependencyContainer()

    var body: some View {
        NavigationStack(path: $router.path) {
            ProductListView(viewModel: dependencies.makeProductListViewModel(router: router))
                .navigationDestination(for: Product.self) { product in
                    ProductDetailView(product: product)
                }
        }
        .environmentObject(router)
    }
}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Massive ViewModel | Too many responsibilities | Split into smaller VMs or use UseCases |
| Tight coupling | Direct dependencies | Use protocols and DI |
| Hard to test | Static/singleton dependencies | Inject dependencies |
| Memory leaks | Strong coordinator references | Use weak delegates |
| State sync issues | Multiple sources of truth | Single source + binding |

### Debug Tips
```swift
// Check retain cycles
deinit {
    print("\(Self.self) deinit")
}

// Trace view updates
var body: some View {
    let _ = Self._printChanges()
    // ...
}

// Validate architecture
// Run: swift package diagnose-api-breaking-changes
```

## Validation Rules

```yaml
validation:
  - rule: layer_separation
    severity: error
    check: Views should not import data layer
  - rule: protocol_abstractions
    severity: warning
    check: Dependencies should be protocols
  - rule: unidirectional_flow
    severity: info
    check: State changes flow in one direction
```

## Usage

```
Skill("swift-architecture")
```

## Related Skills

- `swift-fundamentals` - Protocol-oriented design
- `swift-swiftui` - SwiftUI patterns
- `swift-testing` - Testing architecture
