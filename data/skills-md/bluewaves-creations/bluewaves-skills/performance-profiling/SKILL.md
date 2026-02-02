---
name: performance-profiling
description: Advanced iOS performance profiling with Xcode Instruments, real-world optimization case studies, memory debugging with ASAN/TSAN, SwiftUI view optimization, and production performance patterns. Use when user asks about profiling, Instruments, memory leaks, performance optimization, ASAN, TSAN, hangs, stutters, or app performance issues.
allowed-tools: Bash, Read, Write, Edit
---

# Performance Profiling & Optimization

Comprehensive guide to iOS performance profiling with Xcode Instruments, real-world optimization case studies, memory debugging, and production-ready performance patterns.

## Prerequisites

- Xcode 26+
- Physical device for accurate profiling (Simulator results differ)
- Instruments.app

---

## Instruments Overview

### Core Profiling Templates

```
┌─────────────────────────────────────────────────────────────┐
│                    INSTRUMENTS TEMPLATES                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  TIME PROFILER         CPU usage, hot paths, slow methods   │
│  ALLOCATIONS           Memory allocations, object lifetime  │
│  LEAKS                 Memory leaks detection               │
│  NETWORK               HTTP requests, bandwidth usage       │
│  CORE ANIMATION        FPS, GPU usage, offscreen renders    │
│  SYSTEM TRACE          Low-level system performance         │
│  HANGS                 Main thread blocks > 250ms           │
│  SWIFT CONCURRENCY     Task scheduling, actor contention    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Quick Profile Commands

```bash
# Profile with Time Profiler
xcrun xctrace record --device "iPhone" --template "Time Profiler" --launch -- /path/to/app

# Profile memory allocations
xcrun xctrace record --template "Allocations" --attach "MyApp"

# Export trace to file
xcrun xctrace export --input trace.trace --output results.json
```

---

## Case Study 1: ListView Scroll Performance

### The Problem

A list with 1000+ items stutters during scroll (drops below 60 FPS).

### Diagnosis with Core Animation Instrument

```
Symptoms:
- FPS drops to 30-40 during fast scroll
- "Color Offscreen-Rendered" shows red highlights
- High GPU utilization

Root Causes Found:
1. Shadow on every cell (offscreen render)
2. Cornerradius + masksToBounds (offscreen render)
3. Large images not downsampled
4. Complex view hierarchy per cell
```

### Before (Problematic Code)

```swift
struct NoteCell: View {
    let note: Note

    var body: some View {
        HStack {
            // Problem 1: AsyncImage without caching
            AsyncImage(url: note.thumbnailURL) { image in
                image.resizable()
            } placeholder: {
                ProgressView()
            }
            .frame(width: 60, height: 60)
            // Problem 2: Offscreen render
            .clipShape(RoundedRectangle(cornerRadius: 8))

            VStack(alignment: .leading) {
                Text(note.title)
                    .font(.headline)
                // Problem 3: Heavy formatting every render
                Text(note.formattedDate)
                    .font(.caption)
            }
        }
        // Problem 4: Shadow causes offscreen render
        .shadow(color: .black.opacity(0.1), radius: 4)
    }
}
```

### After (Optimized Code)

```swift
struct NoteCell: View {
    let note: Note

    // Pre-computed values
    private let formattedDate: String

    init(note: Note) {
        self.note = note
        // Compute once, not on every render
        self.formattedDate = note.createdAt.formatted(date: .abbreviated, time: .omitted)
    }

    var body: some View {
        HStack {
            // Solution 1: Cached image loading
            CachedAsyncImage(url: note.thumbnailURL)
                .frame(width: 60, height: 60)
                // Solution 2: Pre-rendered corner radius
                .cornerRadius(8)

            VStack(alignment: .leading) {
                Text(note.title)
                    .font(.headline)
                // Solution 3: Pre-computed date
                Text(formattedDate)
                    .font(.caption)
            }
        }
        // Solution 4: Remove shadow or use pre-rendered shadow image
        .background(
            RoundedRectangle(cornerRadius: 8)
                .fill(Color(.systemBackground))
        )
    }
}

// Cached image loading
struct CachedAsyncImage: View {
    let url: URL?

    @State private var image: UIImage?

    var body: some View {
        Group {
            if let image {
                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } else {
                Color.gray.opacity(0.2)
            }
        }
        .task(id: url) {
            await loadImage()
        }
    }

    private func loadImage() async {
        guard let url else { return }

        // Check cache first
        if let cached = ImageCache.shared[url] {
            image = cached
            return
        }

        // Load and downsample
        guard let data = try? Data(contentsOf: url),
              let original = UIImage(data: data) else { return }

        // Downsample to target size (60x60 points at 3x = 180px)
        let targetSize = CGSize(width: 180, height: 180)
        let downsampled = await original.downsample(to: targetSize)

        ImageCache.shared[url] = downsampled
        image = downsampled
    }
}

// Image downsampling extension
extension UIImage {
    func downsample(to targetSize: CGSize) async -> UIImage {
        await withCheckedContinuation { continuation in
            DispatchQueue.global(qos: .userInitiated).async {
                let renderer = UIGraphicsImageRenderer(size: targetSize)
                let downsampled = renderer.image { _ in
                    self.draw(in: CGRect(origin: .zero, size: targetSize))
                }
                continuation.resume(returning: downsampled)
            }
        }
    }
}

// Simple in-memory cache
actor ImageCache {
    static let shared = ImageCache()
    private var cache: [URL: UIImage] = [:]

    subscript(url: URL) -> UIImage? {
        get { cache[url] }
        set { cache[url] = newValue }
    }
}
```

### Results

```
Before:
- Scroll FPS: 30-40
- Memory: 250MB (unbounded growth)
- Offscreen renders: 1000+

After:
- Scroll FPS: 60 (smooth)
- Memory: 80MB (stable)
- Offscreen renders: 0
```

---

## Case Study 2: App Launch Time Optimization

### The Problem

App takes 4+ seconds to launch (cold start).

### Diagnosis with App Launch Template

```
Launch Phases Analysis:
1. dylib loading: 1.2s (too many frameworks)
2. +load methods: 0.8s (ObjC initialization)
3. UIApplicationMain: 0.5s
4. First frame: 1.8s (heavy initial view)
```

### Optimization Strategies

```swift
// 1. Defer non-critical initialization
@main
struct MyApp: App {
    init() {
        // Only critical setup here
        configureAppearance()

        // Defer analytics, crash reporting, etc.
        Task.detached(priority: .background) {
            await self.deferredSetup()
        }
    }

    private func deferredSetup() async {
        // Non-critical initialization
        AnalyticsManager.shared.configure()
        CrashReporter.shared.start()
        await RemoteConfig.shared.fetch()
    }

    var body: some Scene {
        WindowGroup {
            // 2. Show lightweight placeholder first
            LaunchView()
                .task {
                    // Load heavy data after first frame
                    await DataStore.shared.load()
                }
        }
    }
}

// 3. Lazy service initialization
@Observable
class ServiceContainer {
    static let shared = ServiceContainer()

    // Lazy: Only initialized when first accessed
    lazy var heavyService: HeavyService = {
        HeavyService()
    }()

    lazy var analyticsService: AnalyticsService = {
        AnalyticsService()
    }()
}

// 4. Split view hierarchy
struct LaunchView: View {
    @State private var isReady = false

    var body: some View {
        if isReady {
            // Heavy main content
            MainTabView()
        } else {
            // Lightweight launch screen
            LaunchPlaceholder()
                .task {
                    // Prepare on background
                    await prepareApp()
                    isReady = true
                }
        }
    }

    private func prepareApp() async {
        // Warm up caches, load initial data
        await DataStore.shared.warmUp()
    }
}
```

### Reducing Binary Size

```swift
// 5. Enable dead code stripping
// In Build Settings:
// DEAD_CODE_STRIPPING = YES
// STRIP_INSTALLED_PRODUCT = YES

// 6. Remove unused assets
// Use Asset Catalog Compiler optimization:
// ASSETCATALOG_COMPILER_OPTIMIZATION = "space"

// 7. Link frameworks dynamically
// Convert static libraries to dynamic where possible
// Reduces launch time at cost of slightly larger binary
```

### Results

```
Before:
- Cold launch: 4.2s
- dylib loading: 1.2s
- First frame: 1.8s

After:
- Cold launch: 1.8s
- dylib loading: 0.6s
- First frame: 0.4s
```

---

## Case Study 3: Memory Leak Detection

### Using Address Sanitizer (ASAN)

Enable in Xcode: Edit Scheme → Run → Diagnostics → Address Sanitizer

```swift
// Common leak patterns

// LEAK 1: Closure capturing self strongly
class ViewModel {
    var data: [String] = []
    var timer: Timer?

    func startPolling() {
        // BUG: Timer retains self, self retains timer
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.fetchData()  // Strong capture
        }
    }

    // FIX: Use weak capture
    func startPollingFixed() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.fetchData()
        }
    }

    deinit {
        timer?.invalidate()
    }
}

// LEAK 2: NotificationCenter observer not removed
class ObserverViewModel {
    var observation: Any?

    init() {
        // BUG: Observer not removed
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleNotification),
            name: .someNotification,
            object: nil
        )
    }

    // FIX: Use modern observation API
    init(fixed: Bool) {
        observation = NotificationCenter.default.addObserver(
            forName: .someNotification,
            object: nil,
            queue: .main
        ) { [weak self] notification in
            self?.handleNotification(notification)
        }
    }

    deinit {
        if let observation {
            NotificationCenter.default.removeObserver(observation)
        }
    }
}

// LEAK 3: Delegate retain cycle
protocol DataDelegate: AnyObject {  // Must be AnyObject for weak reference
    func didReceiveData(_ data: Data)
}

class DataManager {
    // BUG: Strong delegate reference
    // var delegate: DataDelegate?

    // FIX: Weak delegate
    weak var delegate: DataDelegate?
}
```

### Using Thread Sanitizer (TSAN)

Enable in Xcode: Edit Scheme → Run → Diagnostics → Thread Sanitizer

```swift
// DATA RACE: Concurrent access to non-atomic property
class Counter {
    // BUG: Not thread-safe
    var count = 0

    func increment() {
        count += 1  // Data race!
    }
}

// FIX 1: Use actor
actor SafeCounter {
    var count = 0

    func increment() {
        count += 1  // Thread-safe
    }
}

// FIX 2: Use lock
class LockedCounter {
    private var _count = 0
    private let lock = NSLock()

    var count: Int {
        lock.withLock { _count }
    }

    func increment() {
        lock.withLock { _count += 1 }
    }
}

// FIX 3: Use dispatch queue
class QueueCounter {
    private var _count = 0
    private let queue = DispatchQueue(label: "counter")

    var count: Int {
        queue.sync { _count }
    }

    func increment() {
        queue.sync { _count += 1 }
    }
}
```

### Memory Graph Debugger

```swift
// Analyze object graph in Xcode:
// Debug → Debug Memory Graph

// Look for:
// 1. Retain cycles (circular references)
// 2. Zombie objects
// 3. Unexpected object counts

// Annotate weak references for debugging
class DebugWeakRef<T: AnyObject> {
    weak var object: T?
    let description: String

    init(_ object: T, description: String = "") {
        self.object = object
        self.description = description
        print("WeakRef created: \(description)")
    }

    deinit {
        print("WeakRef released: \(description)")
    }
}
```

---

## Case Study 4: SwiftUI View Optimization

### Identifying Excessive View Updates

```swift
// Debug view updates
extension View {
    func debugPrint(_ message: String) -> some View {
        #if DEBUG
        print("[\(Date())] \(message)")
        #endif
        return self
    }

    func countRenders(_ counter: Binding<Int>, label: String = "") -> some View {
        #if DEBUG
        counter.wrappedValue += 1
        print("Render #\(counter.wrappedValue): \(label)")
        #endif
        return self
    }
}

// Problematic: Parent state causes child re-render
struct ParentView: View {
    @State private var parentState = 0
    @State private var unrelatedState = ""

    var body: some View {
        VStack {
            // This re-renders when unrelatedState changes!
            ExpensiveChildView(value: parentState)

            TextField("Unrelated", text: $unrelatedState)
        }
    }
}

// Fix 1: Use @Binding only for needed state
struct ExpensiveChildView: View {
    let value: Int  // Value type, not binding

    var body: some View {
        Text("Value: \(value)")
    }
}

// Fix 2: Equatable conformance
struct OptimizedChildView: View, Equatable {
    let value: Int

    static func == (lhs: Self, rhs: Self) -> Bool {
        lhs.value == rhs.value
    }

    var body: some View {
        Text("Value: \(value)")
    }
}

// Usage with .equatable() modifier
ParentView()
    .equatable()  // Only re-renders when Equatable comparison fails
```

### Optimizing @Observable Updates

```swift
// Problem: Entire model triggers updates
@Observable
class UserProfile {
    var name: String = ""
    var email: String = ""
    var avatar: Data?  // Large data
    var preferences: Preferences = .init()
}

// Every property change re-renders all observing views

// Fix: Split into focused models
@Observable
class UserIdentity {
    var name: String = ""
    var email: String = ""
}

@Observable
class UserAvatar {
    var data: Data?
}

@Observable
class UserPreferences {
    var theme: Theme = .system
    var notifications: Bool = true
}

// Views only observe what they need
struct ProfileHeader: View {
    let identity: UserIdentity  // Only re-renders for name/email changes

    var body: some View {
        Text(identity.name)
    }
}

struct AvatarView: View {
    let avatar: UserAvatar  // Only re-renders for avatar changes

    var body: some View {
        if let data = avatar.data {
            Image(uiImage: UIImage(data: data)!)
        }
    }
}
```

### Lazy Loading Patterns

```swift
// Problem: All items loaded at once
struct BadListView: View {
    let items: [Item]  // 10,000 items

    var body: some View {
        ScrollView {
            VStack {
                ForEach(items) { item in
                    ItemRow(item: item)  // All 10,000 created immediately
                }
            }
        }
    }
}

// Fix: Use LazyVStack
struct GoodListView: View {
    let items: [Item]

    var body: some View {
        ScrollView {
            LazyVStack {
                ForEach(items) { item in
                    ItemRow(item: item)  // Only visible items created
                }
            }
        }
    }
}

// Even better: Paginated loading
struct PaginatedListView: View {
    @State private var items: [Item] = []
    @State private var page = 0
    @State private var hasMore = true

    var body: some View {
        List {
            ForEach(items) { item in
                ItemRow(item: item)
                    .onAppear {
                        loadMoreIfNeeded(currentItem: item)
                    }
            }

            if hasMore {
                ProgressView()
                    .onAppear { loadNextPage() }
            }
        }
    }

    private func loadMoreIfNeeded(currentItem: Item) {
        guard let index = items.firstIndex(where: { $0.id == currentItem.id }),
              index >= items.count - 5 else { return }
        loadNextPage()
    }

    private func loadNextPage() {
        guard hasMore else { return }
        Task {
            let newItems = await DataStore.shared.fetchItems(page: page)
            items.append(contentsOf: newItems)
            page += 1
            hasMore = !newItems.isEmpty
        }
    }
}
```

---

## Performance Monitoring in Production

### MetricKit Integration

```swift
import MetricKit

class PerformanceMonitor: NSObject, MXMetricManagerSubscriber {
    static let shared = PerformanceMonitor()

    override init() {
        super.init()
        MXMetricManager.shared.add(self)
    }

    func didReceive(_ payloads: [MXMetricPayload]) {
        for payload in payloads {
            processPayload(payload)
        }
    }

    func didReceive(_ payloads: [MXDiagnosticPayload]) {
        for payload in payloads {
            processDiagnostic(payload)
        }
    }

    private func processPayload(_ payload: MXMetricPayload) {
        // Launch time
        if let launchMetrics = payload.applicationLaunchMetrics {
            let resumeTime = launchMetrics.histogrammedTimeToFirstDraw
                .bucketEnumerator
            // Log to analytics
        }

        // Hang rate
        if let hangMetrics = payload.applicationResponsivenessMetrics {
            let hangTime = hangMetrics.histogrammedApplicationHangTime
            // Alert if above threshold
        }

        // Memory
        if let memoryMetrics = payload.memoryMetrics {
            let peakMemory = memoryMetrics.peakMemoryUsage
            // Track trends
        }
    }

    private func processDiagnostic(_ payload: MXDiagnosticPayload) {
        // Crash diagnostics
        if let crashes = payload.crashDiagnostics {
            for crash in crashes {
                // Send to crash reporting service
                CrashReporter.shared.report(crash)
            }
        }

        // Hang diagnostics
        if let hangs = payload.hangDiagnostics {
            for hang in hangs {
                // Analyze hang stack traces
            }
        }
    }
}
```

### Custom Signposts for Instruments

```swift
import os.signpost

extension OSLog {
    static let performance = OSLog(subsystem: "com.myapp", category: "Performance")
}

struct PerformanceTracer {
    static func trace<T>(_ name: StaticString, _ operation: () throws -> T) rethrows -> T {
        let signpostID = OSSignpostID(log: .performance)
        os_signpost(.begin, log: .performance, name: name, signpostID: signpostID)
        defer {
            os_signpost(.end, log: .performance, name: name, signpostID: signpostID)
        }
        return try operation()
    }

    static func traceAsync<T>(_ name: StaticString, _ operation: () async throws -> T) async rethrows -> T {
        let signpostID = OSSignpostID(log: .performance)
        os_signpost(.begin, log: .performance, name: name, signpostID: signpostID)
        defer {
            os_signpost(.end, log: .performance, name: name, signpostID: signpostID)
        }
        return try await operation()
    }
}

// Usage
func loadData() async {
    await PerformanceTracer.traceAsync("Load Data") {
        await fetchFromNetwork()
        await processData()
        await saveToCache()
    }
}

// View in Instruments → os_signpost
```

---

## Quick Reference: Common Performance Issues

| Symptom | Likely Cause | Tool | Fix |
|---------|--------------|------|-----|
| Scroll stuttering | Offscreen renders | Core Animation | Remove shadows, clipsToBounds |
| High memory | Image loading | Allocations | Downsample, cache |
| Slow launch | Heavy init | App Launch | Defer non-critical work |
| UI hangs | Main thread work | Hangs | Move to background |
| Memory growth | Leaks/cycles | Leaks + ASAN | Fix retain cycles |
| Data races | Concurrent access | TSAN | Use actors/locks |
| Battery drain | Background activity | Energy Log | Reduce timers, location |

---

## Official Resources

- [Instruments Help](https://help.apple.com/instruments/)
- [WWDC23: Analyze hangs with Instruments](https://developer.apple.com/videos/play/wwdc2023/10248/)
- [WWDC22: Track down hangs with Xcode and on-device detection](https://developer.apple.com/videos/play/wwdc2022/10082/)
- [WWDC21: Detect and diagnose memory issues](https://developer.apple.com/videos/play/wwdc2021/10180/)
- [MetricKit Documentation](https://developer.apple.com/documentation/metrickit)
