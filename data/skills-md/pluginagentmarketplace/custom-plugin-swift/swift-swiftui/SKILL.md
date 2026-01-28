---
name: swift-swiftui
description: Build modern UIs with SwiftUI - views, state management, animations, navigation
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 03-swift-swiftui
bond_type: PRIMARY_BOND
---

# SwiftUI Skill

Declarative UI framework knowledge for building modern Apple platform interfaces.

## Prerequisites

- Xcode 15+ installed
- iOS 16+ / macOS 13+ deployment target recommended
- Understanding of reactive programming concepts

## Parameters

```yaml
parameters:
  min_ios_version:
    type: string
    default: "16.0"
    description: Minimum iOS version
  platforms:
    type: array
    items: [iOS, macOS, watchOS, tvOS, visionOS]
    default: [iOS]
  observation_framework:
    type: string
    enum: [observation, combine, observable_object]
    default: observation
    description: State management approach
```

## Topics Covered

### Property Wrappers
| Wrapper | Ownership | Use Case |
|---------|-----------|----------|
| `@State` | View owns | Local, private state |
| `@Binding` | Parent owns | Two-way child connection |
| `@StateObject` | View creates/owns | Observable object lifecycle |
| `@ObservedObject` | External owns | Passed observable |
| `@EnvironmentObject` | Environment owns | Dependency injection |
| `@Environment` | System provides | System values (colorScheme, etc) |

### Observation (iOS 17+)
| Feature | Description |
|---------|-------------|
| `@Observable` | Macro for observable classes |
| `@Bindable` | Create bindings from Observable |
| Automatic tracking | No need for @Published |

### Layout System
| Container | Purpose |
|-----------|---------|
| `VStack` | Vertical arrangement |
| `HStack` | Horizontal arrangement |
| `ZStack` | Overlapping views |
| `LazyVStack/HStack` | Lazy loading for lists |
| `Grid` | 2D grid layout |
| `GeometryReader` | Access to size/position |

## Code Examples

### Observation Pattern (iOS 17+)
```swift
import SwiftUI

@Observable
final class ShoppingCart {
    var items: [CartItem] = []
    var couponCode: String = ""

    var subtotal: Decimal {
        items.reduce(0) { $0 + $1.price * Decimal($1.quantity) }
    }

    var total: Decimal {
        let discount = applyCoupon(to: subtotal)
        return subtotal - discount
    }

    func add(_ product: Product, quantity: Int = 1) {
        if let index = items.firstIndex(where: { $0.product.id == product.id }) {
            items[index].quantity += quantity
        } else {
            items.append(CartItem(product: product, quantity: quantity))
        }
    }

    func remove(_ item: CartItem) {
        items.removeAll { $0.id == item.id }
    }

    private func applyCoupon(to amount: Decimal) -> Decimal {
        guard !couponCode.isEmpty else { return 0 }
        // Apply coupon logic
        return amount * 0.1
    }
}

struct CartView: View {
    @Bindable var cart: ShoppingCart

    var body: some View {
        List {
            ForEach(cart.items) { item in
                CartItemRow(item: item)
            }
            .onDelete { indexSet in
                cart.items.remove(atOffsets: indexSet)
            }

            Section {
                HStack {
                    TextField("Coupon code", text: $cart.couponCode)
                    Button("Apply") { }
                }

                LabeledContent("Subtotal", value: cart.subtotal, format: .currency(code: "USD"))
                LabeledContent("Total", value: cart.total, format: .currency(code: "USD"))
                    .fontWeight(.bold)
            }
        }
        .navigationTitle("Cart (\(cart.items.count))")
    }
}
```

### Custom View Modifier
```swift
struct CardStyle: ViewModifier {
    let cornerRadius: CGFloat
    let shadowRadius: CGFloat

    func body(content: Content) -> some View {
        content
            .background(.background)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
            .shadow(color: .black.opacity(0.1), radius: shadowRadius, y: 2)
    }
}

extension View {
    func cardStyle(cornerRadius: CGFloat = 12, shadowRadius: CGFloat = 4) -> some View {
        modifier(CardStyle(cornerRadius: cornerRadius, shadowRadius: shadowRadius))
    }
}

// Usage
struct ProductCard: View {
    let product: Product

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            AsyncImage(url: product.imageURL) { image in
                image.resizable().aspectRatio(contentMode: .fill)
            } placeholder: {
                ProgressView()
            }
            .frame(height: 150)
            .clipped()

            Text(product.name)
                .font(.headline)

            Text(product.price, format: .currency(code: "USD"))
                .foregroundStyle(.secondary)
        }
        .cardStyle()
    }
}
```

### Custom Animations
```swift
struct PulsingButton: View {
    let title: String
    let action: () -> Void

    @State private var isPulsing = false

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.headline)
                .foregroundStyle(.white)
                .padding(.horizontal, 24)
                .padding(.vertical, 12)
                .background(.blue)
                .clipShape(Capsule())
                .scaleEffect(isPulsing ? 1.05 : 1.0)
        }
        .onAppear {
            withAnimation(.easeInOut(duration: 0.8).repeatForever(autoreverses: true)) {
                isPulsing = true
            }
        }
    }
}

struct MatchedGeometryExample: View {
    @Namespace private var animation
    @State private var isExpanded = false

    var body: some View {
        VStack {
            if isExpanded {
                RoundedRectangle(cornerRadius: 20)
                    .fill(.blue)
                    .matchedGeometryEffect(id: "shape", in: animation)
                    .frame(height: 300)
            } else {
                RoundedRectangle(cornerRadius: 10)
                    .fill(.blue)
                    .matchedGeometryEffect(id: "shape", in: animation)
                    .frame(width: 100, height: 100)
            }
        }
        .onTapGesture {
            withAnimation(.spring(response: 0.5, dampingFraction: 0.7)) {
                isExpanded.toggle()
            }
        }
    }
}
```

### Navigation Stack (iOS 16+)
```swift
struct NavigationExample: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List(products) { product in
                NavigationLink(value: product) {
                    ProductRow(product: product)
                }
            }
            .navigationTitle("Products")
            .navigationDestination(for: Product.self) { product in
                ProductDetailView(product: product)
            }
            .navigationDestination(for: Category.self) { category in
                CategoryView(category: category)
            }
        }
    }

    func navigateToProduct(_ product: Product) {
        path.append(product)
    }

    func popToRoot() {
        path.removeLast(path.count)
    }
}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| View not updating | Wrong property wrapper | Check ownership: @State vs @StateObject |
| Preview crash | Missing mock data | Provide preview with sample data |
| Animation stutters | Expensive body | Extract subviews, avoid complex calculations |
| Navigation broken | Missing NavigationStack | Ensure view is inside NavigationStack |
| List slow | Complex cells | Use LazyVStack, simplify cell views |

### Debug Tips
```swift
// Trace view updates
var body: some View {
    let _ = Self._printChanges()
    // ... view content
}

// Check if preview
#if DEBUG
struct MyView_Previews: PreviewProvider {
    static var previews: some View {
        MyView(data: .preview)
    }
}
#endif
```

## Validation Rules

```yaml
validation:
  - rule: state_ownership
    severity: error
    check: @StateObject for views that create, @ObservedObject for passed
  - rule: body_purity
    severity: warning
    check: No side effects in body computed property
  - rule: lazy_for_lists
    severity: info
    check: Use LazyVStack/LazyHStack for long scrolling content
```

## Usage

```
Skill("swift-swiftui")
```

## Related Skills

- `swift-combine` - Reactive programming
- `swift-uikit` - UIKit interop
- `swift-architecture` - MVVM patterns
