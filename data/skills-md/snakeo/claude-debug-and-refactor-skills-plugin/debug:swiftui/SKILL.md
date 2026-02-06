---
name: debug:swiftui
description: Debug SwiftUI application issues systematically. This skill helps diagnose and resolve SwiftUI-specific problems including view update failures, state management issues with @State/@Binding/@ObservedObject, NavigationStack problems, memory leaks from retain cycles, preview crashes, Combine publisher issues, and animation glitches. Provides Xcode debugger techniques, Instruments profiling, and LLDB commands for iOS/macOS development.
---

# SwiftUI Debugging Guide

A comprehensive guide for systematically debugging SwiftUI applications, covering common error patterns, debugging tools, and step-by-step resolution strategies.

## Common Error Patterns

### 1. View Not Updating

**Symptoms:**
- UI doesn't reflect state changes
- Data updates but view remains stale
- Animations don't trigger

**Root Causes:**
- Missing `@Published` on ObservableObject properties
- Using wrong property wrapper (@State vs @Binding vs @ObservedObject)
- Mutating state on background thread
- Object reference not triggering SwiftUI's change detection

**Solutions:**
```swift
// Ensure @Published is used for observable properties
class ViewModel: ObservableObject {
    @Published var items: [Item] = []  // Correct
    var count: Int = 0  // Won't trigger updates
}

// Force view refresh with id modifier
List(items) { item in
    ItemRow(item: item)
}
.id(UUID())  // Forces complete rebuild

// Update state on main thread
DispatchQueue.main.async {
    self.viewModel.items = newItems
}
```

### 2. @State/@Binding Issues

**Symptoms:**
- Child view changes don't propagate to parent
- State resets unexpectedly
- Two-way binding doesn't work

**Solutions:**
```swift
// Parent view
struct ParentView: View {
    @State private var isOn = false

    var body: some View {
        ChildView(isOn: $isOn)  // Pass binding with $
    }
}

// Child view
struct ChildView: View {
    @Binding var isOn: Bool  // Use @Binding, not @State

    var body: some View {
        Toggle("Toggle", isOn: $isOn)
    }
}
```

### 3. NavigationStack Problems

**Symptoms:**
- Navigation doesn't work
- Back button missing
- Destination view not appearing
- Deprecated NavigationView warnings

**Solutions:**
```swift
// iOS 16+ use NavigationStack
NavigationStack {
    List(items) { item in
        NavigationLink(value: item) {
            Text(item.name)
        }
    }
    .navigationDestination(for: Item.self) { item in
        DetailView(item: item)
    }
}

// For programmatic navigation
@State private var path = NavigationPath()

NavigationStack(path: $path) {
    // ...
}

// Navigate programmatically
path.append(item)
```

### 4. Memory Leaks with Closures

**Symptoms:**
- Memory usage grows over time
- Deinit never called
- Retain cycles in view models

**Solutions:**
```swift
// Use [weak self] in closures
viewModel.fetchData { [weak self] result in
    guard let self = self else { return }
    self.handleResult(result)
}

// For Combine subscriptions, store cancellables
private var cancellables = Set<AnyCancellable>()

publisher
    .sink { [weak self] value in
        self?.handleValue(value)
    }
    .store(in: &cancellables)
```

### 5. Preview Crashes

**Symptoms:**
- Canvas shows "Preview crashed"
- "Cannot preview in this file"
- Slow or unresponsive previews

**Solutions:**
```swift
// Provide mock data for previews
#Preview {
    ContentView()
        .environmentObject(MockViewModel())
}

// Use @available to exclude preview-incompatible code
#if DEBUG
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .previewDevice("iPhone 15 Pro")
    }
}
#endif

// Simplify preview environment
#Preview {
    ContentView()
        .modelContainer(for: Item.self, inMemory: true)
}
```

### 6. Combine Publisher Issues

**Symptoms:**
- Publisher never emits
- Multiple subscriptions
- Memory leaks
- Values emitted on wrong thread

**Solutions:**
```swift
// Ensure receiving on main thread for UI updates
publisher
    .receive(on: DispatchQueue.main)
    .sink { value in
        self.updateUI(value)
    }
    .store(in: &cancellables)

// Debug publisher chain
publisher
    .print("DEBUG")  // Prints all events
    .handleEvents(
        receiveSubscription: { _ in print("Subscribed") },
        receiveOutput: { print("Output: \($0)") },
        receiveCompletion: { print("Completed: \($0)") },
        receiveCancel: { print("Cancelled") }
    )
    .sink { _ in }
    .store(in: &cancellables)
```

### 7. Compiler Type-Check Errors

**Symptoms:**
- "The compiler is unable to type-check this expression in reasonable time"
- Generic error messages on wrong line
- Build times extremely slow

**Solutions:**
```swift
// Break complex views into smaller components
// BAD: Complex inline logic
var body: some View {
    VStack {
        if condition1 && condition2 || condition3 {
            // Lots of nested views...
        }
    }
}

// GOOD: Extract to computed properties or subviews
var body: some View {
    VStack {
        conditionalContent
    }
}

@ViewBuilder
private var conditionalContent: some View {
    if shouldShowContent {
        ContentSubview()
    }
}
```

### 8. Animation Issues

**Symptoms:**
- Animations not playing
- Jerky or stuttering animations
- Wrong elements animating

**Solutions:**
```swift
// Use withAnimation for explicit control
Button("Toggle") {
    withAnimation(.spring()) {
        isExpanded.toggle()
    }
}

// Apply animation to specific value
Rectangle()
    .frame(width: isExpanded ? 200 : 100)
    .animation(.easeInOut, value: isExpanded)

// Use transaction for fine-grained control
var transaction = Transaction(animation: .easeInOut)
transaction.disablesAnimations = false
withTransaction(transaction) {
    isExpanded.toggle()
}
```

## Debugging Tools

### Xcode Debugger

**Breakpoints:**
```swift
// Conditional breakpoint
// Right-click breakpoint > Edit Breakpoint > Condition: items.count > 10

// Symbolic breakpoint for SwiftUI layout issues
// Debug > Breakpoints > Create Symbolic Breakpoint
// Symbol: UIViewAlertForUnsatisfiableConstraints
```

**LLDB Commands:**
```lldb
# Print view hierarchy
po view.value(forKey: "recursiveDescription")

# Print SwiftUI view
po self

# Examine memory
memory read --size 8 --format x 0x12345678

# Find retain cycles
leaks --outputGraph=/tmp/leaks.memgraph [PID]
```

### Instruments

**Allocations:**
- Track memory usage over time
- Identify objects not being deallocated
- Find retain cycles

**Time Profiler:**
- Identify slow code paths
- Find main thread blocking
- Optimize view rendering

**SwiftUI Instruments (Xcode 15+):**
- View body evaluations
- View identity tracking
- State change tracking

### Print Debugging

```swift
// Track view redraws
var body: some View {
    let _ = Self._printChanges()  // Prints what caused redraw
    Text("Hello")
}

// Conditional debug printing
#if DEBUG
func debugPrint(_ items: Any...) {
    print(items)
}
#else
func debugPrint(_ items: Any...) {}
#endif

// os_log for structured logging
import os.log

let logger = Logger(subsystem: "com.app.name", category: "networking")
logger.debug("Request started: \(url)")
logger.error("Request failed: \(error.localizedDescription)")
```

### View Hierarchy Debugger

1. Run app in simulator/device
2. Click "Debug View Hierarchy" button in Xcode
3. Use 3D view to inspect layer structure
4. Check for overlapping views, incorrect frames

### Environment Inspection

```swift
// Print all environment values
struct DebugEnvironmentView: View {
    @Environment(\.self) var environment

    var body: some View {
        let _ = print(environment)
        Text("Debug")
    }
}
```

## The Four Phases (SwiftUI-Specific)

### Phase 1: Reproduce and Isolate

1. **Create minimal reproduction**
   - Strip away unrelated code
   - Use fresh SwiftUI project if needed
   - Test in Preview vs Simulator vs Device

2. **Identify trigger conditions**
   - When does the bug occur?
   - What user actions trigger it?
   - Is it state-dependent?

3. **Check iOS version specifics**
   - Does it happen on all iOS versions?
   - Is it simulator-only or device-only?

### Phase 2: Diagnose

1. **Use Self._printChanges()**
   ```swift
   var body: some View {
       let _ = Self._printChanges()
       // Your view content
   }
   ```

2. **Add strategic breakpoints**
   - Body property
   - State mutations
   - Network callbacks

3. **Check property wrapper usage**
   - @State for view-local state
   - @Binding for parent-child communication
   - @StateObject for owned ObservableObject
   - @ObservedObject for passed ObservableObject
   - @EnvironmentObject for dependency injection

4. **Verify threading**
   ```swift
   // Check if on main thread
   assert(Thread.isMainThread, "Must be on main thread")
   ```

### Phase 3: Fix

1. **Apply targeted fix**
   - Fix one issue at a time
   - Don't introduce new property wrappers unnecessarily

2. **Test the fix**
   - Verify in Preview
   - Test in Simulator
   - Test on physical device
   - Test edge cases

3. **Check for side effects**
   - Run existing tests
   - Verify related features still work

### Phase 4: Prevent

1. **Add unit tests**
   ```swift
   func testViewModelUpdatesState() async {
       let viewModel = ViewModel()
       await viewModel.fetchData()
       XCTAssertEqual(viewModel.items.count, 10)
   }
   ```

2. **Add UI tests**
   ```swift
   func testNavigationFlow() {
       let app = XCUIApplication()
       app.launch()
       app.buttons["DetailButton"].tap()
       XCTAssertTrue(app.staticTexts["DetailView"].exists)
   }
   ```

3. **Document the fix**
   - Add code comments explaining why
   - Update team documentation

## Quick Reference Commands

### Xcode Shortcuts

| Shortcut | Action |
|----------|--------|
| Cmd + R | Run |
| Cmd + B | Build |
| Cmd + U | Run tests |
| Cmd + Shift + K | Clean build folder |
| Cmd + Option + P | Resume preview |
| Cmd + 7 | Show debug navigator |
| Cmd + 8 | Show breakpoint navigator |

### Common Debug Snippets

```swift
// Force view identity reset
.id(someValue)

// Track view lifecycle
.onAppear { print("View appeared") }
.onDisappear { print("View disappeared") }
.task { print("Task started") }

// Debug layout
.border(Color.red)  // See frame boundaries
.background(Color.blue.opacity(0.3))

// Debug geometry
.background(GeometryReader { geo in
    Color.clear.onAppear {
        print("Size: \(geo.size)")
        print("Frame: \(geo.frame(in: .global))")
    }
})

// Debug state changes
.onChange(of: someState) { oldValue, newValue in
    print("State changed from \(oldValue) to \(newValue)")
}
```

### Build Settings for Debugging

```
// In scheme > Run > Arguments > Environment Variables
OS_ACTIVITY_MODE = disable  // Reduce console noise
DYLD_PRINT_STATISTICS = 1   // Print launch time stats
```

### Memory Debugging

```swift
// Add to class to track deallocation
deinit {
    print("\(Self.self) deinit")
}

// Enable Zombie Objects
// Edit Scheme > Run > Diagnostics > Zombie Objects

// Enable Address Sanitizer
// Edit Scheme > Run > Diagnostics > Address Sanitizer
```

## Resources

- [SwiftUI Debugging - SwiftLee](https://www.avanderlee.com/swiftui/debugging-swiftui-views/)
- [Building SwiftUI Debugging Utilities - Swift by Sundell](https://www.swiftbysundell.com/articles/building-swiftui-debugging-utilities/)
- [Common SwiftUI Errors - Hacking with Swift](https://www.hackingwithswift.com/quick-start/swiftui/common-swiftui-errors-and-how-to-fix-them)
- [8 Common SwiftUI Mistakes - Hacking with Swift](https://www.hackingwithswift.com/articles/224/common-swiftui-mistakes-and-how-to-fix-them)
- [Advanced Debugging Techniques - MoldStud](https://moldstud.com/articles/p-advanced-debugging-techniques-for-swiftui-applications-expert-guide)
- [Debugging SwiftUI with Xcode - Kodeco](https://www.kodeco.com/books/swiftui-cookbook/v1.0/chapters/5-debugging-swiftui-code-with-xcode-s-debugger)
