---
name: swift-testing
description: Test Swift applications - XCTest, Swift Testing, UI tests, mocking, TDD, CI/CD
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 06-swift-testing
bond_type: PRIMARY_BOND
---

# Swift Testing Skill

Comprehensive testing strategies for Swift applications using XCTest and Swift Testing framework.

## Prerequisites

- Xcode 15+ installed
- Understanding of dependency injection
- Familiarity with async/await

## Parameters

```yaml
parameters:
  framework:
    type: string
    enum: [xctest, swift_testing]
    default: swift_testing
  test_type:
    type: string
    enum: [unit, integration, ui, snapshot]
    default: unit
  coverage_target:
    type: number
    default: 80
    description: Target code coverage percentage
  ci_platform:
    type: string
    enum: [xcode_cloud, github_actions, gitlab_ci, none]
    default: github_actions
```

## Topics Covered

### Test Frameworks
| Framework | Min Version | Key Features |
|-----------|-------------|--------------|
| XCTest | iOS 2.0+ | XCTestCase, expectations |
| Swift Testing | iOS 17+ / Swift 5.9+ | @Test, #expect, traits |

### Test Types
| Type | Scope | Speed |
|------|-------|-------|
| Unit | Single function/class | Fastest |
| Integration | Multiple components | Medium |
| UI | Full user flows | Slowest |
| Snapshot | Visual regression | Medium |

### Testing Patterns
| Pattern | Purpose |
|---------|---------|
| AAA | Arrange, Act, Assert |
| Given-When-Then | BDD style |
| Test Doubles | Mock, Stub, Spy, Fake |

## Code Examples

### Swift Testing (iOS 17+ / Swift 5.9+)
```swift
import Testing
@testable import MyApp

@Suite("ShoppingCart Tests")
struct ShoppingCartTests {
    var cart: ShoppingCart
    var mockRepository: MockProductRepository

    init() {
        mockRepository = MockProductRepository()
        cart = ShoppingCart(repository: mockRepository)
    }

    @Test("adding product increases count")
    func addProduct() async throws {
        let product = Product(id: "1", name: "Widget", price: 9.99)

        cart.add(product)

        #expect(cart.items.count == 1)
        #expect(cart.items.first?.product == product)
    }

    @Test("adding same product increases quantity")
    func addSameProductTwice() {
        let product = Product(id: "1", name: "Widget", price: 9.99)

        cart.add(product)
        cart.add(product)

        #expect(cart.items.count == 1)
        #expect(cart.items.first?.quantity == 2)
    }

    @Test("total calculates correctly")
    func calculateTotal() {
        cart.add(Product(id: "1", name: "A", price: 10.00))
        cart.add(Product(id: "2", name: "B", price: 20.00))

        #expect(cart.total == 30.00)
    }

    @Test("checkout requires non-empty cart", .tags(.checkout))
    func checkoutEmptyCart() async {
        await #expect(throws: CartError.empty) {
            try await cart.checkout()
        }
    }

    @Test("checkout with valid cart", .tags(.checkout))
    func checkoutSuccess() async throws {
        cart.add(Product(id: "1", name: "Widget", price: 9.99))
        mockRepository.checkoutResult = .success(Order(id: "order-1"))

        let order = try await cart.checkout()

        #expect(order.id == "order-1")
        #expect(cart.items.isEmpty)
    }

    @Test(arguments: [0, 1, 5, 10])
    func discountTiers(quantity: Int) {
        let discount = cart.calculateDiscount(forQuantity: quantity)

        switch quantity {
        case 0..<5: #expect(discount == 0)
        case 5..<10: #expect(discount == 0.05)
        default: #expect(discount == 0.10)
        }
    }
}
```

### XCTest with Async
```swift
import XCTest
@testable import MyApp

final class ProductServiceTests: XCTestCase {
    var sut: ProductService!
    var mockAPI: MockAPIClient!

    override func setUp() {
        super.setUp()
        mockAPI = MockAPIClient()
        sut = ProductService(api: mockAPI)
    }

    override func tearDown() {
        sut = nil
        mockAPI = nil
        super.tearDown()
    }

    func test_fetchProducts_success() async throws {
        // Arrange
        let expectedProducts = [Product(id: "1", name: "Test", price: 9.99)]
        mockAPI.productsResult = .success(expectedProducts)

        // Act
        let products = try await sut.fetchProducts()

        // Assert
        XCTAssertEqual(products, expectedProducts)
        XCTAssertTrue(mockAPI.fetchProductsCalled)
    }

    func test_fetchProducts_networkError_throws() async {
        // Arrange
        mockAPI.productsResult = .failure(NetworkError.noConnection)

        // Act & Assert
        do {
            _ = try await sut.fetchProducts()
            XCTFail("Expected error to be thrown")
        } catch {
            XCTAssertTrue(error is NetworkError)
        }
    }

    func test_fetchProducts_retries_onTransientError() async throws {
        // Arrange
        var attempts = 0
        mockAPI.onFetchProducts = {
            attempts += 1
            if attempts < 3 {
                throw NetworkError.timeout
            }
            return [Product(id: "1", name: "Test", price: 9.99)]
        }

        // Act
        _ = try await sut.fetchProductsWithRetry(maxAttempts: 3)

        // Assert
        XCTAssertEqual(attempts, 3)
    }
}
```

### Mock Implementation
```swift
// Protocol for abstraction
protocol APIClientProtocol {
    func fetchProducts() async throws -> [Product]
    func createOrder(_ order: CreateOrderRequest) async throws -> Order
}

// Production implementation
final class APIClient: APIClientProtocol {
    func fetchProducts() async throws -> [Product] {
        // Real implementation
    }

    func createOrder(_ order: CreateOrderRequest) async throws -> Order {
        // Real implementation
    }
}

// Test mock
final class MockAPIClient: APIClientProtocol {
    var productsResult: Result<[Product], Error> = .success([])
    var orderResult: Result<Order, Error> = .success(Order(id: "mock"))

    var fetchProductsCalled = false
    var fetchProductsCallCount = 0
    var createOrderCalled = false
    var lastOrderRequest: CreateOrderRequest?

    var onFetchProducts: (() async throws -> [Product])?

    func fetchProducts() async throws -> [Product] {
        fetchProductsCalled = true
        fetchProductsCallCount += 1

        if let handler = onFetchProducts {
            return try await handler()
        }

        return try productsResult.get()
    }

    func createOrder(_ order: CreateOrderRequest) async throws -> Order {
        createOrderCalled = true
        lastOrderRequest = order
        return try orderResult.get()
    }

    func reset() {
        productsResult = .success([])
        orderResult = .success(Order(id: "mock"))
        fetchProductsCalled = false
        fetchProductsCallCount = 0
        createOrderCalled = false
        lastOrderRequest = nil
        onFetchProducts = nil
    }
}
```

### UI Testing with Page Object Pattern
```swift
import XCTest

// Page Object
struct LoginPage {
    let app: XCUIApplication

    var usernameField: XCUIElement {
        app.textFields["username"]
    }

    var passwordField: XCUIElement {
        app.secureTextFields["password"]
    }

    var loginButton: XCUIElement {
        app.buttons["login"]
    }

    var errorMessage: XCUIElement {
        app.staticTexts["errorMessage"]
    }

    func login(username: String, password: String) {
        usernameField.tap()
        usernameField.typeText(username)

        passwordField.tap()
        passwordField.typeText(password)

        loginButton.tap()
    }

    func waitForLogin(timeout: TimeInterval = 5) -> Bool {
        !usernameField.waitForExistence(timeout: timeout)
    }
}

// UI Test
final class LoginUITests: XCTestCase {
    var app: XCUIApplication!
    var loginPage: LoginPage!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false

        app = XCUIApplication()
        app.launchArguments = ["--uitesting", "--reset-state"]
        app.launch()

        loginPage = LoginPage(app: app)
    }

    func test_login_withValidCredentials_navigatesToHome() {
        loginPage.login(username: "testuser", password: "password123")

        XCTAssertTrue(loginPage.waitForLogin())
        XCTAssertTrue(app.tabBars["mainTabBar"].exists)
    }

    func test_login_withInvalidCredentials_showsError() {
        loginPage.login(username: "wrong", password: "wrong")

        XCTAssertTrue(loginPage.errorMessage.waitForExistence(timeout: 5))
        XCTAssertEqual(loginPage.errorMessage.label, "Invalid credentials")
    }
}
```

### GitHub Actions CI
```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_15.2.app

      - name: Build and Test
        run: |
          xcodebuild test \
            -scheme MyApp \
            -destination 'platform=iOS Simulator,name=iPhone 15,OS=17.2' \
            -resultBundlePath TestResults.xcresult \
            -enableCodeCoverage YES \
            CODE_SIGNING_ALLOWED=NO

      - name: Upload Results
        uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: test-results
          path: TestResults.xcresult

      - name: Coverage Report
        run: |
          xcrun xccov view --report TestResults.xcresult
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Flaky tests | Shared state | Add setUp/tearDown cleanup |
| Async timeout | Missing fulfillment | Call fulfill() or increase timeout |
| UI element not found | Wrong identifier | Check accessibilityIdentifier |
| Mock not working | Wrong initialization | Verify dependency injection |
| Coverage low | Untested paths | Add edge case tests |

### Debug Tips
```swift
// Print XCUIElement hierarchy
print(app.debugDescription)

// Wait for condition
let exists = element.waitForExistence(timeout: 5)

// Take screenshot on failure
let screenshot = XCUIScreen.main.screenshot()
let attachment = XCTAttachment(screenshot: screenshot)
attachment.lifetime = .keepAlways
add(attachment)
```

## Validation Rules

```yaml
validation:
  - rule: test_naming
    severity: info
    check: Use descriptive test names (test_method_condition_result)
  - rule: one_assertion
    severity: info
    check: Prefer one logical assertion per test
  - rule: no_test_interdependence
    severity: error
    check: Tests must not depend on each other
```

## Usage

```
Skill("swift-testing")
```

## Related Skills

- `swift-fundamentals` - Code to test
- `swift-concurrency` - Testing async code
- `swift-architecture` - Testable architecture
