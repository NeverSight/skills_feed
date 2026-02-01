---
name: mapbox-ios-patterns
description: Integration patterns for Mapbox Maps SDK on iOS with Swift, SwiftUI, UIKit, lifecycle management, and mobile optimization best practices.
---

# Mapbox iOS Integration Patterns

Official integration patterns for Mapbox Maps SDK on iOS. Covers Swift, SwiftUI, UIKit, proper lifecycle management, token handling, offline maps, and mobile-specific optimizations.

**Use this skill when:**
- Setting up Mapbox Maps SDK for iOS in a new or existing project
- Integrating maps with SwiftUI or UIKit
- Implementing proper lifecycle management and cleanup
- Managing tokens securely in iOS apps
- Working with offline maps and caching
- Integrating Navigation SDK
- Optimizing for battery life and memory usage
- Debugging crashes, memory leaks, or performance issues

---

## Core Integration Patterns

### SwiftUI Pattern (iOS 13+)

**Modern approach using SwiftUI and Combine**

```swift
import SwiftUI
import MapboxMaps

struct MapView: UIViewRepresentable {
    @Binding var coordinate: CLLocationCoordinate2D
    @Binding var zoom: CGFloat

    func makeUIView(context: Context) -> MapboxMap.MapView {
        let mapView = MapboxMap.MapView(frame: .zero)

        // Configure map
        mapView.mapboxMap.setCamera(
            to: CameraOptions(
                center: coordinate,
                zoom: zoom
            )
        )

        return mapView
    }

    func updateUIView(_ mapView: MapboxMap.MapView, context: Context) {
        // Update camera when SwiftUI state changes
        mapView.mapboxMap.setCamera(
            to: CameraOptions(
                center: coordinate,
                zoom: zoom
            )
        )
    }
}

// Usage in SwiftUI view
struct ContentView: View {
    @State private var coordinate = CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194)
    @State private var zoom: CGFloat = 12

    var body: some View {
        MapView(coordinate: $coordinate, zoom: $zoom)
            .edgesIgnoringSafeArea(.all)
    }
}
```

**Key points:**
- Use `UIViewRepresentable` to wrap MapView
- Bind SwiftUI state to map properties
- Handle updates in `updateUIView`
- No manual cleanup needed (SwiftUI handles it)

### UIKit Pattern (Classic)

**Traditional UIKit integration with proper lifecycle**

```swift
import UIKit
import MapboxMaps

class MapViewController: UIViewController {
    private var mapView: MapboxMap.MapView!

    override func viewDidLoad() {
        super.viewDidLoad()

        // Initialize map
        mapView = MapboxMap.MapView(frame: view.bounds)
        mapView.autoresizingMask = [.flexibleWidth, .flexibleHeight]

        // Configure map
        mapView.mapboxMap.setCamera(
            to: CameraOptions(
                center: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194),
                zoom: 12
            )
        )

        view.addSubview(mapView)

        // Add map loaded handler
        mapView.mapboxMap.onNext(.mapLoaded) { [weak self] _ in
            self?.mapDidLoad()
        }
    }

    private func mapDidLoad() {
        // Add sources and layers after map loads
        addCustomLayers()
    }

    private func addCustomLayers() {
        // Add your custom sources and layers
    }

    deinit {
        // MapView cleanup happens automatically
        // No manual cleanup needed with SDK v10+
    }
}
```

**Key points:**
- Initialize in `viewDidLoad()`
- Use `weak self` in closures to prevent retain cycles
- Wait for `.mapLoaded` event before adding layers
- No manual cleanup needed (SDK v10+ handles it)

---

## Token Management

### ✅ Recommended: Info.plist Configuration

```xml
<!-- Info.plist -->
<key>MBXAccessToken</key>
<string>$(MAPBOX_ACCESS_TOKEN)</string>
```

**Xcode Build Configuration:**

1. Create `.xcconfig` file:

```bash
# Config/Secrets.xcconfig (add to .gitignore)
MAPBOX_ACCESS_TOKEN = pk.your_token_here
```

2. Set in Xcode project settings:
   - Select project → Info tab
   - Add Configuration Set: Secrets.xcconfig

3. Add to `.gitignore`:

```gitignore
Config/Secrets.xcconfig
*.xcconfig
```

**Why this pattern:**
- Token not in source code
- Automatically injected at build time
- Works with Xcode Cloud and CI/CD
- No hardcoded secrets

### ❌ Anti-Pattern: Hardcoded Tokens

```swift
// ❌ NEVER DO THIS - Token in source code
MapboxOptions.accessToken = "pk.YOUR_MAPBOX_TOKEN_HERE"
```

---

## Memory Management and Lifecycle

### ✅ Proper Retain Cycle Prevention

```swift
class MapViewController: UIViewController {
    private var mapView: MapboxMap.MapView!
    private var cancelables = Set<AnyCancelable>()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupMap()
    }

    private func setupMap() {
        mapView = MapboxMap.MapView(frame: view.bounds)
        view.addSubview(mapView)

        // ✅ GOOD: Use weak self to prevent retain cycles
        mapView.mapboxMap.onEvery(.cameraChanged) { [weak self] event in
            self?.handleCameraChange(event)
        }

        // ✅ GOOD: Store cancelables for proper cleanup
        mapView.gestures.onMapTap
            .sink { [weak self] coordinate in
                self?.handleTap(at: coordinate)
            }
            .store(in: &cancelables)
    }

    private func handleCameraChange(_ event: MapboxCoreMaps.Event) {
        // Handle camera changes
    }

    private func handleTap(at coordinate: CLLocationCoordinate2D) {
        // Handle tap
    }

    deinit {
        // Cancelables automatically cleaned up
        print("MapViewController deallocated")
    }
}
```

### ❌ Anti-Pattern: Retain Cycles

```swift
// ❌ BAD: Strong reference cycle
mapView.mapboxMap.onEvery(.cameraChanged) { event in
    self.handleCameraChange(event) // Retains self!
}

// ❌ BAD: Not storing cancelables
mapView.gestures.onMapTap
    .sink { coordinate in
        self.handleTap(at: coordinate)
    }
    // Immediately deallocated!
```

---

## Offline Maps

### Download Region for Offline Use

```swift
import MapboxMaps

class OfflineManager {
    private let offlineManager: OfflineRegionManager

    init() {
        offlineManager = OfflineRegionManager()
    }

    func downloadRegion(
        name: String,
        bounds: CoordinateBounds,
        minZoom: Double = 0,
        maxZoom: Double = 16,
        completion: @escaping (Result<Void, Error>) -> Void
    ) {
        // Create tile pyramid definition
        let tilePyramid = TilePyramidOfflineRegionDefinition(
            styleURL: StyleURI.streets.rawValue,
            bounds: bounds,
            minZoom: minZoom,
            maxZoom: maxZoom
        )

        // Create offline region
        offlineManager.createOfflineRegion(
            for: tilePyramid,
            metadata: ["name": name]
        ) { result in
            switch result {
            case .success(let region):
                // Download tiles
                region.setOfflineRegionDownloadState(to: .active)

                // Monitor progress
                region.observeOfflineRegionDownloadStatus { status in
                    print("Downloaded: \(status.completedResourceCount)/\(status.requiredResourceCount)")
                }

                completion(.success(()))

            case .failure(let error):
                completion(.failure(error))
            }
        }
    }

    func listOfflineRegions() -> [OfflineRegion] {
        return offlineManager.offlineRegions
    }

    func deleteRegion(_ region: OfflineRegion, completion: @escaping (Result<Void, Error>) -> Void) {
        offlineManager.removeOfflineRegion(for: region) { result in
            completion(result.map { _ in () })
        }
    }
}
```

**Key considerations:**
- **Battery impact:** Downloading uses significant battery
- **Storage limits:** Monitor available disk space
- **Zoom levels:** Higher zoom = more tiles = more storage
- **Style updates:** Offline regions don't auto-update styles

### Storage Calculations

```swift
// Estimate offline region size before downloading
func estimateSize(bounds: CoordinateBounds, maxZoom: Double) -> Int64 {
    let tilePyramid = TilePyramidOfflineRegionDefinition(
        styleURL: StyleURI.streets.rawValue,
        bounds: bounds,
        minZoom: 0,
        maxZoom: maxZoom
    )

    // Rough estimate: 50 KB per tile average
    let tileCount = tilePyramid.tileCount
    return tileCount * 50_000 // bytes
}

// Check available storage
func hasEnoughStorage(requiredBytes: Int64) -> Bool {
    let fileURL = URL(fileURLWithPath: NSHomeDirectory())
    guard let values = try? fileURL.resourceValues(forKeys: [.volumeAvailableCapacityKey]),
          let capacity = values.volumeAvailableCapacity else {
        return false
    }
    return Int64(capacity) > requiredBytes * 2 // 2x buffer
}
```

---

## Navigation SDK Integration

### Basic Navigation Setup

```swift
import MapboxMaps
import MapboxNavigation
import MapboxDirections
import MapboxCoreNavigation

class NavigationViewController: UIViewController {
    private var navigationMapView: NavigationMapView!
    private var routeController: RouteController?

    override func viewDidLoad() {
        super.viewDidLoad()
        setupNavigationMap()
    }

    private func setupNavigationMap() {
        navigationMapView = NavigationMapView(frame: view.bounds)
        navigationMapView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(navigationMapView)
    }

    func startNavigation(to destination: CLLocationCoordinate2D) {
        guard let origin = navigationMapView.mapView.location.latestLocation?.coordinate else {
            return
        }

        // Request route
        let waypoints = [
            Waypoint(coordinate: origin),
            Waypoint(coordinate: destination)
        ]

        let options = NavigationRouteOptions(waypoints: waypoints)

        Directions.shared.calculate(options) { [weak self] session, result in
            guard let self = self else { return }

            switch result {
            case .success(let response):
                guard let route = response.routes?.first else { return }

                // Show route on map
                self.navigationMapView.show([route])
                self.navigationMapView.showWaypoints(on: route)

                // Start navigation
                self.startActiveNavigation(with: route)

            case .failure(let error):
                print("Route calculation failed: \(error)")
            }
        }
    }

    private func startActiveNavigation(with route: Route) {
        let navigationService = MapboxNavigationService(
            route: route,
            routeOptions: route.routeOptions,
            simulating: .never
        )

        routeController = RouteController(
            navigationService: navigationService
        )

        // Listen to navigation events
        routeController?.delegate = self
    }
}

extension NavigationViewController: RouteControllerDelegate {
    func routeController(
        _ routeController: RouteController,
        didUpdate locations: [CLLocation]
    ) {
        // Update user location
    }

    func routeController(
        _ routeController: RouteController,
        didArriveAt waypoint: Waypoint
    ) {
        print("Arrived at destination!")
    }
}
```

**Navigation SDK features:**
- Turn-by-turn guidance
- Voice instructions
- Route progress tracking
- Rerouting
- Traffic-aware routing
- Offline navigation (with offline regions)

---

## Mobile Performance Optimization

### Battery Optimization

```swift
// ✅ Reduce frame rate when app is in background
class BatteryAwareMapViewController: UIViewController {
    private var mapView: MapboxMap.MapView!

    override func viewDidLoad() {
        super.viewDidLoad()
        setupMap()
        observeAppState()
    }

    private func observeAppState() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(appDidEnterBackground),
            name: UIApplication.didEnterBackgroundNotification,
            object: nil
        )

        NotificationCenter.default.addObserver(
            self,
            selector: #selector(appWillEnterForeground),
            name: UIApplication.willEnterForegroundNotification,
            object: nil
        )
    }

    @objc private func appDidEnterBackground() {
        // Reduce rendering when in background
        mapView.mapboxMap.setRenderCacheSize(to: 0)

        // Pause expensive operations
        mapView.location.options.activityType = .otherNavigation
    }

    @objc private func appWillEnterForeground() {
        // Resume normal rendering
        mapView.mapboxMap.setRenderCacheSize(to: nil) // Default

        // Resume location updates
        mapView.location.options.activityType = .fitness
    }
}
```

### Memory Optimization

```swift
// ✅ Handle memory warnings
override func didReceiveMemoryWarning() {
    super.didReceiveMemoryWarning()

    // Clear map cache
    mapView?.mapboxMap.clearData { result in
        switch result {
        case .success:
            print("Map cache cleared")
        case .failure(let error):
            print("Failed to clear cache: \(error)")
        }
    }
}

// ✅ Limit cached tiles
let resourceOptions = ResourceOptions(
    accessToken: accessToken,
    tileStoreUsageMode: .readOnly
)

// ✅ Use appropriate map scale for device
if UIScreen.main.scale > 2.0 {
    // Retina displays, can use higher detail
} else {
    // Lower DPI, reduce detail
}
```

### Network Optimization

```swift
// ✅ Detect network conditions and adjust
import Network

class NetworkAwareMapViewController: UIViewController {
    private let monitor = NWPathMonitor()
    private let queue = DispatchQueue.global(qos: .background)

    override func viewDidLoad() {
        super.viewDidLoad()
        setupNetworkMonitoring()
    }

    private func setupNetworkMonitoring() {
        monitor.pathUpdateHandler = { [weak self] path in
            if path.status == .satisfied {
                if path.isExpensive {
                    // Cellular connection - reduce data usage
                    self?.enableLowDataMode()
                } else {
                    // WiFi - normal quality
                    self?.enableNormalMode()
                }
            }
        }
        monitor.start(queue: queue)
    }

    private func enableLowDataMode() {
        // Use lower resolution tiles on cellular
        // Reduce tile prefetching
    }

    private func enableNormalMode() {
        // Use full resolution
    }
}
```

---

## Common Mistakes and Solutions

### ❌ Mistake 1: Not Using Weak Self

```swift
// ❌ BAD: Creates retain cycle
mapView.mapboxMap.onNext(.mapLoaded) { _ in
    self.setupLayers() // Retains self!
}

// ✅ GOOD: Use weak self
mapView.mapboxMap.onNext(.mapLoaded) { [weak self] _ in
    self?.setupLayers()
}
```

### ❌ Mistake 2: Adding Layers Before Map Loads

```swift
// ❌ BAD: Adding layers immediately
override func viewDidLoad() {
    super.viewDidLoad()
    mapView = MapboxMap.MapView(frame: view.bounds)
    view.addSubview(mapView)

    addCustomLayers() // Map not loaded yet!
}

// ✅ GOOD: Wait for map loaded event
override func viewDidLoad() {
    super.viewDidLoad()
    mapView = MapboxMap.MapView(frame: view.bounds)
    view.addSubview(mapView)

    mapView.mapboxMap.onNext(.mapLoaded) { [weak self] _ in
        self?.addCustomLayers()
    }
}
```

### ❌ Mistake 3: Ignoring Location Permissions

```swift
// ❌ BAD: Enabling location without checking permissions
mapView.location.options.puckType = .puck2D()

// ✅ GOOD: Request and check permissions
import CoreLocation

class MapViewController: UIViewController, CLLocationManagerDelegate {
    private let locationManager = CLLocationManager()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupLocation()
    }

    private func setupLocation() {
        locationManager.delegate = self

        switch locationManager.authorizationStatus {
        case .notDetermined:
            locationManager.requestWhenInUseAuthorization()
        case .authorizedWhenInUse, .authorizedAlways:
            enableLocationTracking()
        default:
            // Handle denied/restricted
            break
        }
    }

    private func enableLocationTracking() {
        mapView.location.options.puckType = .puck2D()
    }

    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        if manager.authorizationStatus == .authorizedWhenInUse ||
           manager.authorizationStatus == .authorizedAlways {
            enableLocationTracking()
        }
    }
}
```

**Add to Info.plist:**

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>We need your location to show you on the map</string>
```

### ❌ Mistake 4: Not Handling Camera State in SwiftUI

```swift
// ❌ BAD: No way to read camera state changes
struct MapView: UIViewRepresentable {
    @Binding var coordinate: CLLocationCoordinate2D

    func makeUIView(context: Context) -> MapboxMap.MapView {
        let mapView = MapboxMap.MapView(frame: .zero)
        // User pans map, but coordinate binding never updates!
        return mapView
    }
}

// ✅ GOOD: Use Coordinator to sync camera state
struct MapView: UIViewRepresentable {
    @Binding var coordinate: CLLocationCoordinate2D
    @Binding var zoom: CGFloat

    func makeCoordinator() -> Coordinator {
        Coordinator(coordinate: $coordinate, zoom: $zoom)
    }

    func makeUIView(context: Context) -> MapboxMap.MapView {
        let mapView = MapboxMap.MapView(frame: .zero)

        // Listen to camera changes
        mapView.mapboxMap.onEvery(.cameraChanged) { _ in
            context.coordinator.updateFromMap(mapView.mapboxMap)
        }

        return mapView
    }

    class Coordinator {
        @Binding var coordinate: CLLocationCoordinate2D
        @Binding var zoom: CGFloat

        init(coordinate: Binding<CLLocationCoordinate2D>, zoom: Binding<CGFloat>) {
            _coordinate = coordinate
            _zoom = zoom
        }

        func updateFromMap(_ map: MapboxMap) {
            coordinate = map.cameraState.center
            zoom = CGFloat(map.cameraState.zoom)
        }
    }
}
```

---

## Testing Patterns

### Unit Testing Map Logic

```swift
import XCTest
@testable import YourApp
import MapboxMaps

class MapLogicTests: XCTestCase {
    func testCoordinateConversion() {
        let coordinate = CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194)

        // Test your map logic without creating actual MapView
        let converted = YourMapLogic.convert(coordinate: coordinate)

        XCTAssertEqual(converted.latitude, 37.7749, accuracy: 0.001)
    }
}
```

### UI Testing with Maps

```swift
import XCTest

class MapUITests: XCTestCase {
    func testMapViewLoads() {
        let app = XCUIApplication()
        app.launch()

        // Wait for map to load
        let mapView = app.otherElements["mapView"]
        XCTAssertTrue(mapView.waitForExistence(timeout: 5))
    }
}
```

**Set accessibility identifier:**

```swift
mapView.accessibilityIdentifier = "mapView"
```

---

## Troubleshooting

### Map Not Displaying

**Checklist:**
1. ✅ Token configured in Info.plist?
2. ✅ Bundle ID matches token restrictions?
3. ✅ MapboxMaps framework imported?
4. ✅ MapView added to view hierarchy?
5. ✅ Internet connection available? (for non-cached tiles)

### Memory Leaks

**Use Instruments:**
1. Xcode → Product → Profile → Leaks
2. Look for retain cycles in map event handlers
3. Ensure `[weak self]` in all closures
4. Check that cancelables are stored and cleaned up

### Slow Performance

**Common causes:**
- Too many markers (use clustering or symbols)
- Large GeoJSON sources (use vector tiles)
- High-frequency camera updates
- Not handling memory warnings
- Running on simulator (use device for accurate testing)

---

## Platform-Specific Considerations

### iOS Version Support

- **iOS 13+**: Full SwiftUI support
- **iOS 12**: UIKit only
- **iOS 11**: Limited features

### Device Optimization

```swift
// Adjust quality based on device
if UIDevice.current.userInterfaceIdiom == .pad {
    // iPad - can handle higher detail
} else if ProcessInfo.processInfo.isLowPowerModeEnabled {
    // iPhone in low power mode - reduce detail
}
```

### Screen Resolution

```swift
let scale = UIScreen.main.scale
if scale >= 3.0 {
    // @3x displays (iPhone Pro models)
    // Use highest quality
} else if scale >= 2.0 {
    // @2x displays
    // Standard quality
}
```

---

## Reference

- [Mapbox Maps SDK for iOS](https://docs.mapbox.com/ios/maps/guides/)
- [API Reference](https://docs.mapbox.com/ios/maps/api-reference/)
- [Examples](https://docs.mapbox.com/ios/maps/examples/)
- [Navigation SDK](https://docs.mapbox.com/ios/navigation/guides/)
- [Swift Package Manager Installation](https://docs.mapbox.com/ios/maps/guides/install/)
- [Migration Guides](https://docs.mapbox.com/ios/maps/guides/migrate-to-v10/)
