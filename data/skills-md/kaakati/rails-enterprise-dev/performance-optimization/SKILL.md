---
name: performance-optimization
description: "Expert performance decisions for iOS/tvOS: when to optimize vs premature optimization, profiling tool selection, SwiftUI view identity trade-offs, and memory management strategies. Use when debugging performance issues, optimizing slow screens, or reducing memory usage. Trigger keywords: performance, Instruments, Time Profiler, Allocations, memory leak, view identity, lazy loading, @StateObject, retain cycle, image caching, faulting, batch operations"
version: "3.0.0"
---

# Performance Optimization — Expert Decisions

Expert decision frameworks for performance choices. Claude knows lazy loading and async basics — this skill provides judgment calls for when to optimize and which tool to use.

---

## Decision Trees

### Should You Optimize?

```
When should you invest in optimization?
├─ User-facing latency issue (visible stutter/delay)
│  └─ YES — Profile and fix
│     Measure first, optimize second
│
├─ Premature concern ("this might be slow")
│  └─ NO — Wait for evidence
│     Write clean code, profile later
│
├─ Battery drain complaints
│  └─ YES — Use Energy Diagnostics
│     Focus on background work, location, network
│
├─ Memory warnings / crashes
│  └─ YES — Use Allocations + Leaks
│     Find retain cycles, unbounded caches
│
└─ App store reviews mention slowness
   └─ YES — Profile real scenarios
      User perception matters
```

**The trap**: Optimizing based on assumptions. Always profile first. The bottleneck is rarely where you think.

### Profiling Tool Selection

```
What are you measuring?
├─ Slow UI / frame drops
│  └─ Time Profiler + View Debugger
│     Find expensive work on main thread
│
├─ Memory growth / leaks
│  └─ Allocations + Leaks instruments
│     Track object lifetimes, find cycles
│
├─ Network performance
│  └─ Network instrument + Charles/Proxyman
│     Latency, payload size, request count
│
├─ Disk I/O issues
│  └─ File Activity instrument
│     Excessive reads/writes
│
├─ Battery drain
│  └─ Energy Log instrument
│     CPU wake, location, networking
│
└─ GPU / rendering
   └─ Core Animation instrument
      Offscreen rendering, overdraw
```

### SwiftUI View Update Strategy

```
View is re-rendering too often?
├─ Caused by parent state changes
│  └─ Extract to separate view
│     Child doesn't depend on changing state
│
├─ Complex computed body
│  └─ Cache expensive computations
│     Use ViewModel or memoization
│
├─ List items all updating
│  └─ Check view identity
│     Use stable IDs, not indices
│
├─ Observable causing cascading updates
│  └─ Split into multiple @Published
│     Or use computed properties
│
└─ Animation causing constant redraws
   └─ Use drawingGroup() or limit scope
      Rasterize stable content
```

### Memory Management Decision

```
How to fix memory issues?
├─ Steady growth during use
│  └─ Check caches and collections
│     Add eviction, use NSCache
│
├─ Growth tied to navigation
│  └─ Check retain cycles
│     weak self in closures, delegates
│
├─ Large spikes on specific screens
│  └─ Downsample images
│     Load at display size, not full resolution
│
├─ Memory not released after screen dismissal
│  └─ Debug object lifecycle
│     deinit not called = retain cycle
│
└─ Background memory pressure
   └─ Respond to didReceiveMemoryWarning
      Clear caches, release non-essential data
```

---

## NEVER Do

### View Identity

**NEVER** use indices as identifiers:
```swift
// ❌ Identity changes when array mutates
List(items.indices, id: \.self) { index in
    ItemRow(item: items[index])
}
// Insert at index 0 → all views recreated!

// ✅ Use stable identifiers
List(items) { item in
    ItemRow(item: item)
        .id(item.id)  // Stable across mutations
}
```

**NEVER** compute expensive values in body:
```swift
// ❌ Called on every render
var body: some View {
    let sortedItems = items.sorted { $0.date > $1.date }  // O(n log n) per render!
    let filtered = sortedItems.filter { $0.isActive }

    List(filtered) { item in
        ItemRow(item: item)
    }
}

// ✅ Compute in ViewModel or use computed property
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []

    var displayItems: [Item] {
        items.filter(\.isActive).sorted { $0.date > $1.date }
    }
}
```

### State Management

**NEVER** use @StateObject for passed objects:
```swift
// ❌ Creates new instance on every parent update
struct ChildView: View {
    @StateObject var viewModel: ChildViewModel  // Wrong!

    var body: some View { ... }
}

// ✅ Use @ObservedObject for passed objects
struct ChildView: View {
    @ObservedObject var viewModel: ChildViewModel  // Parent owns it

    var body: some View { ... }
}
```

**NEVER** make everything @Published:
```swift
// ❌ Every property change triggers view updates
class ViewModel: ObservableObject {
    @Published var items: [Item] = []
    @Published var internalCache: [String: Data] = [:]  // UI doesn't need this!
    @Published var isProcessing = false  // Maybe internal only
}

// ✅ Only publish what UI observes
class ViewModel: ObservableObject {
    @Published var items: [Item] = []
    @Published var isLoading = false

    private var internalCache: [String: Data] = [:]  // Not @Published
    private var isProcessing = false  // Private state
}
```

### Memory Leaks

**NEVER** capture self strongly in escaping closures:
```swift
// ❌ Retain cycle — never deallocates
class ViewModel {
    var timer: Timer?

    func start() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.tick()  // Strong capture!
        }
    }
}

// ✅ Weak capture + invalidation
class ViewModel {
    var timer: Timer?

    func start() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.tick()
        }
    }

    deinit {
        timer?.invalidate()
    }
}
```

**NEVER** forget to remove observers:
```swift
// ❌ Leaks observer and potentially self
class ViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleNotification),
            name: .userLoggedIn,
            object: nil
        )
        // Never removed!
    }
}

// ✅ Remove in deinit or use modern API
class ViewController: UIViewController {
    private var observer: NSObjectProtocol?

    override func viewDidLoad() {
        super.viewDidLoad()
        observer = NotificationCenter.default.addObserver(
            forName: .userLoggedIn,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.handleNotification()
        }
    }

    deinit {
        if let observer { NotificationCenter.default.removeObserver(observer) }
    }
}
```

### Image Loading

**NEVER** load full resolution for thumbnails:
```swift
// ❌ 4000×3000 image for 80×80 thumbnail
let image = UIImage(contentsOfFile: path)  // Full resolution in memory!
imageView.image = image

// ✅ Downsample to display size
func downsampledImage(at url: URL, to size: CGSize) -> UIImage? {
    let options: [CFString: Any] = [
        kCGImageSourceShouldCache: false,
        kCGImageSourceCreateThumbnailFromImageAlways: true,
        kCGImageSourceThumbnailMaxPixelSize: max(size.width, size.height) * UIScreen.main.scale
    ]

    guard let source = CGImageSourceCreateWithURL(url as CFURL, nil),
          let cgImage = CGImageSourceCreateThumbnailAtIndex(source, 0, options as CFDictionary) else {
        return nil
    }
    return UIImage(cgImage: cgImage)
}
```

**NEVER** cache images without limits:
```swift
// ❌ Unbounded memory growth
class ImageLoader {
    private var cache: [URL: UIImage] = [:]  // Grows forever!

    func image(for url: URL) -> UIImage? {
        if let cached = cache[url] { return cached }
        let image = loadImage(url)
        cache[url] = image  // Never evicted
        return image
    }
}

// ✅ Use NSCache with limits
class ImageLoader {
    private let cache = NSCache<NSURL, UIImage>()

    init() {
        cache.countLimit = 100
        cache.totalCostLimit = 50 * 1024 * 1024  // 50 MB
    }

    func image(for url: URL) -> UIImage? {
        if let cached = cache.object(forKey: url as NSURL) { return cached }
        guard let image = loadImage(url) else { return nil }
        cache.setObject(image, forKey: url as NSURL, cost: image.jpegData(compressionQuality: 1)?.count ?? 0)
        return image
    }
}
```

### Heavy Operations

**NEVER** do heavy work on main thread:
```swift
// ❌ UI frozen during processing
func loadData() {
    let data = try! Data(contentsOf: largeFileURL)  // Blocks main thread!
    let parsed = parseData(data)  // Still blocking!
    self.items = parsed
}

// ✅ Use background thread, update on main
func loadData() async {
    let items = await Task.detached(priority: .userInitiated) {
        let data = try! Data(contentsOf: largeFileURL)
        return parseData(data)
    }.value

    await MainActor.run {
        self.items = items
    }
}
```

---

## Essential Patterns

### Efficient List View

```swift
struct EfficientListView: View {
    let items: [Item]

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {  // Lazy = on-demand creation
                ForEach(items) { item in
                    ItemRow(item: item)
                        .id(item.id)  // Stable identity
                }
            }
        }
    }
}

// Equatable row prevents unnecessary updates
struct ItemRow: View, Equatable {
    let item: Item

    var body: some View {
        HStack {
            AsyncImage(url: item.imageURL) { image in
                image.resizable().aspectRatio(contentMode: .fill)
            } placeholder: {
                Color.gray.opacity(0.3)
            }
            .frame(width: 60, height: 60)
            .clipShape(RoundedRectangle(cornerRadius: 8))

            VStack(alignment: .leading) {
                Text(item.title).font(.headline)
                Text(item.subtitle).font(.caption).foregroundColor(.secondary)
            }
        }
    }

    static func == (lhs: ItemRow, rhs: ItemRow) -> Bool {
        lhs.item.id == rhs.item.id &&
        lhs.item.title == rhs.item.title &&
        lhs.item.subtitle == rhs.item.subtitle
    }
}
```

### Memory-Safe ViewModel

```swift
@MainActor
final class ViewModel: ObservableObject {
    @Published private(set) var items: [Item] = []
    @Published private(set) var isLoading = false

    private var cancellables = Set<AnyCancellable>()
    private var loadTask: Task<Void, Never>?

    func load() {
        loadTask?.cancel()  // Cancel previous

        loadTask = Task {
            guard !Task.isCancelled else { return }

            isLoading = true
            defer { isLoading = false }

            do {
                let items = try await API.fetchItems()
                guard !Task.isCancelled else { return }
                self.items = items
            } catch {
                // Handle error
            }
        }
    }

    deinit {
        loadTask?.cancel()
        cancellables.removeAll()
    }
}
```

### Debounced Search

```swift
@MainActor
final class SearchViewModel: ObservableObject {
    @Published var searchText = ""
    @Published private(set) var results: [Item] = []

    private var searchTask: Task<Void, Never>?

    init() {
        // Debounce search
        $searchText
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .sink { [weak self] text in
                self?.performSearch(text)
            }
            .store(in: &cancellables)
    }

    private func performSearch(_ query: String) {
        searchTask?.cancel()

        guard !query.isEmpty else {
            results = []
            return
        }

        searchTask = Task {
            do {
                let results = try await API.search(query: query)
                guard !Task.isCancelled else { return }
                self.results = results
            } catch {
                // Handle error
            }
        }
    }
}
```

---

## Quick Reference

### Instruments Selection

| Issue | Instrument | What to Look For |
|-------|------------|------------------|
| Slow UI | Time Profiler | Heavy main thread work |
| Memory leak | Leaks | Leaked objects |
| Memory growth | Allocations | Growing categories |
| Battery | Energy Log | Wake frequency |
| Network | Network | Request count, size |
| Disk | File Activity | Excessive I/O |
| GPU | Core Animation | Offscreen renders |

### SwiftUI Performance Checklist

| Issue | Solution |
|-------|----------|
| Slow list scrolling | Use LazyVStack/LazyVGrid |
| All items re-render | Stable IDs, Equatable rows |
| Heavy body computation | Move to ViewModel |
| Cascading @Published updates | Split or use computed |
| Animation jank | Use drawingGroup() |

### Memory Management

| Pattern | Prevent Issue |
|---------|---------------|
| [weak self] in closures | Retain cycles |
| Timer.invalidate() in deinit | Timer leaks |
| Remove observers in deinit | Observer leaks |
| NSCache with limits | Unbounded cache growth |
| Image downsampling | Memory spikes |

### os_signpost for Custom Profiling

```swift
import os.signpost

let log = OSLog(subsystem: "com.app", category: .pointsOfInterest)

os_signpost(.begin, log: log, name: "DataProcessing")
// Expensive work
os_signpost(.end, log: log, name: "DataProcessing")
```

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Indices as List IDs | Views recreated on mutation | Use stable identifiers |
| Expensive body computation | Runs every render | Move to ViewModel |
| @StateObject for passed object | Creates new instance | Use @ObservedObject |
| Strong self in Timer/closure | Retain cycle | Use [weak self] |
| Full-res images for thumbnails | Memory explosion | Downsample to display size |
| Unbounded dictionary cache | Memory growth | Use NSCache with limits |
| Heavy work without Task.detached | Blocks main thread | Use background priority |
