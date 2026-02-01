---
name: mapbox-android-patterns
description: Integration patterns for Mapbox Maps SDK on Android with Kotlin, Jetpack Compose, lifecycle management, and mobile optimization best practices.
---

# Mapbox Android Integration Patterns

Official integration patterns for Mapbox Maps SDK on Android. Covers Kotlin, Jetpack Compose, View system, proper lifecycle management, token handling, offline maps, and mobile-specific optimizations.

**Use this skill when:**
- Setting up Mapbox Maps SDK for Android in a new or existing project
- Integrating maps with Jetpack Compose or View system
- Implementing proper lifecycle management and cleanup
- Managing tokens securely in Android apps
- Working with offline maps and caching
- Integrating Navigation SDK
- Optimizing for battery life and memory usage
- Debugging crashes, memory leaks, or performance issues

---

## Core Integration Patterns

### Jetpack Compose Pattern (Modern)

**Modern approach using Jetpack Compose and Kotlin**

```kotlin
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import com.mapbox.maps.MapView
import com.mapbox.maps.Style
import com.mapbox.maps.plugin.animation.camera
import com.mapbox.geojson.Point

@Composable
fun MapboxMap(
    modifier: Modifier = Modifier,
    center: Point,
    zoom: Double,
    onMapReady: (MapView) -> Unit = {}
) {
    val mapView = rememberMapViewWithLifecycle()

    AndroidView(
        modifier = modifier,
        factory = { mapView },
        update = { view ->
            // Update camera when state changes
            view.getMapboxMap().apply {
                setCamera(
                    CameraOptions.Builder()
                        .center(center)
                        .zoom(zoom)
                        .build()
                )
            }
        }
    )

    LaunchedEffect(mapView) {
        mapView.getMapboxMap().loadStyleUri(Style.MAPBOX_STREETS) {
            onMapReady(mapView)
        }
    }
}

@Composable
fun rememberMapViewWithLifecycle(): MapView {
    val context = LocalContext.current
    val mapView = remember {
        MapView(context).apply {
            id = View.generateViewId()
        }
    }

    // Lifecycle-aware cleanup
    DisposableEffect(mapView) {
        onDispose {
            mapView.onDestroy()
        }
    }

    return mapView
}

// Usage in Composable
@Composable
fun MapScreen() {
    var center by remember { mutableStateOf(Point.fromLngLat(-122.4194, 37.7749)) }
    var zoom by remember { mutableStateOf(12.0) }

    MapboxMap(
        modifier = Modifier.fillMaxSize(),
        center = center,
        zoom = zoom,
        onMapReady = { mapView ->
            // Add sources and layers
        }
    )
}
```

**Key points:**
- Use `AndroidView` to integrate MapView in Compose
- Use `remember` to preserve MapView across recompositions
- Use `DisposableEffect` for proper lifecycle cleanup
- Handle state updates in `update` block

### View System Pattern (Classic)

**Traditional Android View system with proper lifecycle**

```kotlin
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.mapbox.maps.MapView
import com.mapbox.maps.Style
import com.mapbox.maps.plugin.gestures.addOnMapClickListener
import com.mapbox.geojson.Point

class MapActivity : AppCompatActivity() {
    private lateinit var mapView: MapView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_map)

        mapView = findViewById(R.id.mapView)

        mapView.getMapboxMap().loadStyleUri(Style.MAPBOX_STREETS) { style ->
            // Map loaded, add sources and layers
            setupMap(style)
        }

        // Add click listener
        mapView.getMapboxMap().addOnMapClickListener { point ->
            handleMapClick(point)
            true
        }
    }

    private fun setupMap(style: Style) {
        // Add your custom sources and layers
    }

    private fun handleMapClick(point: Point) {
        // Handle map clicks
    }

    // CRITICAL: Lifecycle methods for proper cleanup
    override fun onStart() {
        super.onStart()
        mapView.onStart()
    }

    override fun onStop() {
        super.onStop()
        mapView.onStop()
    }

    override fun onDestroy() {
        super.onDestroy()
        mapView.onDestroy()
    }

    override fun onLowMemory() {
        super.onLowMemory()
        mapView.onLowMemory()
    }
}
```

**XML layout (activity_map.xml):**

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <com.mapbox.maps.MapView
        android:id="@+id/mapView"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
```

**Key points:**
- Call `mapView.onStart()`, `onStop()`, `onDestroy()`, `onLowMemory()` in corresponding Activity methods
- Wait for style to load before adding layers
- Store MapView reference as lateinit var (will be initialized in onCreate)

### Fragment Pattern

```kotlin
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.mapbox.maps.MapView
import com.mapbox.maps.Style

class MapFragment : Fragment() {
    private var mapView: MapView? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val view = inflater.inflate(R.layout.fragment_map, container, false)
        mapView = view.findViewById(R.id.mapView)

        mapView?.getMapboxMap()?.loadStyleUri(Style.MAPBOX_STREETS) { style ->
            setupMap(style)
        }

        return view
    }

    private fun setupMap(style: Style) {
        // Add sources and layers
    }

    override fun onStart() {
        super.onStart()
        mapView?.onStart()
    }

    override fun onStop() {
        super.onStop()
        mapView?.onStop()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        mapView?.onDestroy()
        mapView = null
    }

    override fun onLowMemory() {
        super.onLowMemory()
        mapView?.onLowMemory()
    }
}
```

**Key points:**
- Set `mapView` to null in `onDestroyView()` to prevent leaks
- Use nullable `mapView?` for safety
- Call lifecycle methods appropriately

---

## Token Management

### ✅ Recommended: String Resources with BuildConfig

**1. Add to `local.properties` (DO NOT commit):**

```properties
# local.properties (add to .gitignore)
MAPBOX_ACCESS_TOKEN=pk.your_token_here
```

**2. Configure in `build.gradle.kts` (Module):**

```kotlin
android {
    defaultConfig {
        // Read from local.properties
        val properties = Properties()
        properties.load(project.rootProject.file("local.properties").inputStream())

        buildConfigField(
            "String",
            "MAPBOX_ACCESS_TOKEN",
            "\"${properties.getProperty("MAPBOX_ACCESS_TOKEN", "")}\""
        )

        // Also add to resources for SDK
        resValue(
            "string",
            "mapbox_access_token",
            properties.getProperty("MAPBOX_ACCESS_TOKEN", "")
        )
    }

    buildFeatures {
        buildConfig = true
    }
}
```

**3. Add to `.gitignore`:**

```gitignore
local.properties
```

**4. Usage in code:**

```kotlin
import com.yourapp.BuildConfig

// Access token automatically picked up from resources
// No need to set manually if in string resources

// Or access programmatically:
val token = BuildConfig.MAPBOX_ACCESS_TOKEN
```

**Why this pattern:**
- Token not in source code or version control
- Works in local development and CI/CD (via environment variables)
- Automatically injected at build time
- No hardcoded secrets

### ❌ Anti-Pattern: Hardcoded Tokens

```kotlin
// ❌ NEVER DO THIS - Token in source code
MapboxOptions.accessToken = "pk.YOUR_MAPBOX_TOKEN_HERE"
```

---

## Memory Management and Lifecycle

### ✅ Proper Lifecycle Management

```kotlin
import androidx.lifecycle.DefaultLifecycleObserver
import androidx.lifecycle.LifecycleOwner
import com.mapbox.maps.MapView

class MapLifecycleObserver(
    private val mapView: MapView
) : DefaultLifecycleObserver {

    override fun onStart(owner: LifecycleOwner) {
        mapView.onStart()
    }

    override fun onStop(owner: LifecycleOwner) {
        mapView.onStop()
    }

    override fun onDestroy(owner: LifecycleOwner) {
        mapView.onDestroy()
    }

    fun onLowMemory() {
        mapView.onLowMemory()
    }
}

// Usage in Activity/Fragment
class MapActivity : AppCompatActivity() {
    private lateinit var mapView: MapView
    private lateinit var lifecycleObserver: MapLifecycleObserver

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_map)

        mapView = findViewById(R.id.mapView)
        lifecycleObserver = MapLifecycleObserver(mapView)

        // Automatically handle lifecycle
        lifecycle.addObserver(lifecycleObserver)
    }

    override fun onLowMemory() {
        super.onLowMemory()
        lifecycleObserver.onLowMemory()
    }
}
```

### ✅ ViewModel Pattern

```kotlin
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mapbox.geojson.Point
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class MapState(
    val center: Point = Point.fromLngLat(-122.4194, 37.7749),
    val zoom: Double = 12.0,
    val markers: List<Point> = emptyList()
)

class MapViewModel : ViewModel() {
    private val _mapState = MutableStateFlow(MapState())
    val mapState: StateFlow<MapState> = _mapState

    fun updateCenter(point: Point) {
        _mapState.value = _mapState.value.copy(center = point)
    }

    fun addMarker(point: Point) {
        val currentMarkers = _mapState.value.markers
        _mapState.value = _mapState.value.copy(
            markers = currentMarkers + point
        )
    }

    fun loadData() {
        viewModelScope.launch {
            // Load data from repository
            // Update state when ready
        }
    }
}
```

**Benefits:**
- State survives configuration changes
- Separates business logic from UI
- Lifecycle-aware
- Easy to test

---

## Offline Maps

### Download Region for Offline Use

```kotlin
import com.mapbox.maps.TileStore
import com.mapbox.maps.TileRegionLoadOptions
import com.mapbox.common.TileRegion
import com.mapbox.geojson.Point
import com.mapbox.bindgen.Expected

class OfflineManager(private val context: Context) {
    private val tileStore = TileStore.create()

    fun downloadRegion(
        regionId: String,
        bounds: CoordinateBounds,
        minZoom: Int = 0,
        maxZoom: Int = 16,
        onProgress: (Float) -> Unit,
        onComplete: (Result<Unit>) -> Unit
    ) {
        val tilesetDescriptor = tileStore.createDescriptor(
            TilesetDescriptorOptions.Builder()
                .styleURI(Style.MAPBOX_STREETS)
                .minZoom(minZoom.toByte())
                .maxZoom(maxZoom.toByte())
                .build()
        )

        val loadOptions = TileRegionLoadOptions.Builder()
            .geometry(bounds.toGeometry())
            .descriptors(listOf(tilesetDescriptor))
            .acceptExpired(false)
            .build()

        val cancelable = tileStore.loadTileRegion(
            regionId,
            loadOptions,
            { progress ->
                val percent = (progress.completedResourceCount.toFloat() /
                              progress.requiredResourceCount.toFloat()) * 100
                onProgress(percent)
            }
        ) { expected ->
            if (expected.isValue) {
                onComplete(Result.success(Unit))
            } else {
                onComplete(Result.failure(Exception(expected.error?.message)))
            }
        }
    }

    fun getTileRegions(callback: (List<TileRegion>) -> Unit) {
        tileStore.getAllTileRegions { expected ->
            if (expected.isValue) {
                callback(expected.value ?: emptyList())
            } else {
                callback(emptyList())
            }
        }
    }

    fun removeTileRegion(regionId: String, callback: (Boolean) -> Unit) {
        tileStore.removeTileRegion(regionId)
        callback(true)
    }

    fun estimateStorageSize(
        bounds: CoordinateBounds,
        minZoom: Int,
        maxZoom: Int
    ): Long {
        // Rough estimate: 50 KB per tile average
        val tileCount = estimateTileCount(bounds, minZoom, maxZoom)
        return tileCount * 50_000L // bytes
    }

    private fun estimateTileCount(
        bounds: CoordinateBounds,
        minZoom: Int,
        maxZoom: Int
    ): Long {
        // Simplified tile count estimation
        var count = 0L
        for (zoom in minZoom..maxZoom) {
            val tilesAtZoom = Math.pow(4.0, zoom.toDouble()).toLong()
            count += tilesAtZoom
        }
        return count
    }
}
```

**Key considerations:**
- **Battery impact:** Downloading uses significant battery
- **Storage limits:** Monitor available disk space
- **Zoom levels:** Higher zoom = more tiles = more storage
- **Network type:** WiFi vs cellular

### Check Available Storage

```kotlin
import android.os.StatFs
import android.os.Environment

fun getAvailableStorageBytes(): Long {
    val stat = StatFs(Environment.getDataDirectory().path)
    return stat.availableBlocksLong * stat.blockSizeLong
}

fun hasEnoughStorage(requiredBytes: Long): Boolean {
    val available = getAvailableStorageBytes()
    return available > requiredBytes * 2 // 2x buffer
}
```

---

## Navigation SDK Integration

### Basic Navigation Setup

```kotlin
import com.mapbox.navigation.core.MapboxNavigation
import com.mapbox.navigation.core.MapboxNavigationProvider
import com.mapbox.navigation.core.directions.session.RoutesObserver
import com.mapbox.navigation.core.trip.session.RouteProgressObserver
import com.mapbox.navigation.core.trip.session.TripSessionState
import com.mapbox.api.directions.v5.models.DirectionsRoute
import com.mapbox.geojson.Point

class NavigationActivity : AppCompatActivity() {
    private lateinit var mapboxNavigation: MapboxNavigation
    private lateinit var mapView: MapView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_navigation)

        mapView = findViewById(R.id.mapView)

        // Initialize Navigation SDK
        mapboxNavigation = MapboxNavigationProvider.create(
            NavigationOptions.Builder(this)
                .accessToken(getString(R.string.mapbox_access_token))
                .build()
        )

        setupObservers()
    }

    private fun setupObservers() {
        // Observe route updates
        mapboxNavigation.registerRoutesObserver(object : RoutesObserver {
            override fun onRoutesChanged(result: RoutesUpdatedResult) {
                val routes = result.navigationRoutes
                if (routes.isNotEmpty()) {
                    // Show route on map
                    showRouteOnMap(routes.first())
                }
            }
        })

        // Observe navigation progress
        mapboxNavigation.registerRouteProgressObserver(object : RouteProgressObserver {
            override fun onRouteProgressChanged(routeProgress: RouteProgress) {
                // Update UI with progress
                val distanceRemaining = routeProgress.distanceRemaining
                val durationRemaining = routeProgress.durationRemaining
            }
        })
    }

    fun startNavigation(destination: Point) {
        // Request route
        val origin = mapboxNavigation.navigationOptions.locationEngine
            .getLastLocation { location ->
                location?.let {
                    val originPoint = Point.fromLngLat(it.longitude, it.latitude)
                    requestRoute(originPoint, destination)
                }
            }
    }

    private fun requestRoute(origin: Point, destination: Point) {
        val routeOptions = RouteOptions.builder()
            .applyDefaultNavigationOptions()
            .coordinates(listOf(origin, destination))
            .build()

        mapboxNavigation.requestRoutes(
            routeOptions,
            object : NavigationRouterCallback {
                override fun onRoutesReady(
                    routes: List<NavigationRoute>,
                    routerOrigin: RouterOrigin
                ) {
                    mapboxNavigation.setNavigationRoutes(routes)
                    mapboxNavigation.startTripSession()
                }

                override fun onFailure(
                    reasons: List<RouterFailure>,
                    routeOptions: RouteOptions
                ) {
                    // Handle error
                }

                override fun onCanceled(
                    routeOptions: RouteOptions,
                    routerOrigin: RouterOrigin
                ) {
                    // Handle cancellation
                }
            }
        )
    }

    private fun showRouteOnMap(route: NavigationRoute) {
        // Draw route on map
    }

    override fun onDestroy() {
        super.onDestroy()
        mapboxNavigation.onDestroy()
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

```kotlin
import android.content.Context
import android.os.PowerManager

class BatteryAwareMapActivity : AppCompatActivity() {
    private lateinit var mapView: MapView
    private lateinit var powerManager: PowerManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_map)

        mapView = findViewById(R.id.mapView)
        powerManager = getSystemService(Context.POWER_SERVICE) as PowerManager

        observeBatteryState()
    }

    private fun observeBatteryState() {
        if (powerManager.isPowerSaveMode) {
            enableLowPowerMode()
        }

        // Register broadcast receiver for power save mode changes
        registerReceiver(
            object : BroadcastReceiver() {
                override fun onReceive(context: Context?, intent: Intent?) {
                    if (powerManager.isPowerSaveMode) {
                        enableLowPowerMode()
                    } else {
                        enableNormalMode()
                    }
                }
            },
            IntentFilter(PowerManager.ACTION_POWER_SAVE_MODE_CHANGED)
        )
    }

    private fun enableLowPowerMode() {
        // Reduce frame rate
        mapView.getMapboxMap().setMaximumFps(30)

        // Disable 3D features
        // Reduce tile quality
    }

    private fun enableNormalMode() {
        mapView.getMapboxMap().setMaximumFps(60)
    }
}
```

### Memory Optimization

```kotlin
override fun onLowMemory() {
    super.onLowMemory()
    mapView.onLowMemory()

    // Clear map cache
    mapView.getMapboxMap().clearData { result ->
        if (result.isValue) {
            Log.d("Map", "Cache cleared")
        }
    }
}

override fun onTrimMemory(level: Int) {
    super.onTrimMemory(level)

    when (level) {
        ComponentCallbacks2.TRIM_MEMORY_RUNNING_LOW,
        ComponentCallbacks2.TRIM_MEMORY_RUNNING_CRITICAL -> {
            // Clear non-essential data
            mapView.getMapboxMap().clearData { }
        }
    }
}
```

### Network Optimization

```kotlin
import android.net.ConnectivityManager
import android.net.NetworkCapabilities

class NetworkAwareMapActivity : AppCompatActivity() {
    private lateinit var connectivityManager: ConnectivityManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        connectivityManager = getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager

        observeNetworkState()
    }

    private fun observeNetworkState() {
        val networkCallback = object : ConnectivityManager.NetworkCallback() {
            override fun onCapabilitiesChanged(
                network: Network,
                capabilities: NetworkCapabilities
            ) {
                when {
                    capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> {
                        // WiFi - use full quality
                        enableHighQuality()
                    }
                    capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> {
                        // Cellular - reduce data usage
                        enableLowDataMode()
                    }
                }
            }
        }

        connectivityManager.registerDefaultNetworkCallback(networkCallback)
    }

    private fun enableHighQuality() {
        // Use full resolution tiles
    }

    private fun enableLowDataMode() {
        // Reduce tile resolution
        // Limit prefetching
    }
}
```

---

## Common Mistakes and Solutions

### ❌ Mistake 1: Not Calling Lifecycle Methods

```kotlin
// ❌ BAD: MapView lifecycle not managed
class MapActivity : AppCompatActivity() {
    private lateinit var mapView: MapView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mapView = findViewById(R.id.mapView)
        // No lifecycle methods called!
    }
}

// ✅ GOOD: Proper lifecycle management
class MapActivity : AppCompatActivity() {
    private lateinit var mapView: MapView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mapView = findViewById(R.id.mapView)
    }

    override fun onStart() {
        super.onStart()
        mapView.onStart()
    }

    override fun onStop() {
        super.onStop()
        mapView.onStop()
    }

    override fun onDestroy() {
        super.onDestroy()
        mapView.onDestroy()
    }

    override fun onLowMemory() {
        super.onLowMemory()
        mapView.onLowMemory()
    }
}
```

### ❌ Mistake 2: Memory Leaks in Fragments

```kotlin
// ❌ BAD: MapView not cleaned up in Fragment
class MapFragment : Fragment() {
    private lateinit var mapView: MapView

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val view = inflater.inflate(R.layout.fragment_map, container, false)
        mapView = view.findViewById(R.id.mapView)
        return view
    }
    // No cleanup!
}

// ✅ GOOD: Proper cleanup
class MapFragment : Fragment() {
    private var mapView: MapView? = null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val view = inflater.inflate(R.layout.fragment_map, container, false)
        mapView = view.findViewById(R.id.mapView)
        return view
    }

    override fun onDestroyView() {
        super.onDestroyView()
        mapView?.onDestroy()
        mapView = null // Prevent leaks
    }
}
```

### ❌ Mistake 3: Ignoring Location Permissions

```kotlin
// ❌ BAD: Enabling location without checking permissions
mapView.location.enabled = true

// ✅ GOOD: Request and check permissions
import androidx.activity.result.contract.ActivityResultContracts

class MapActivity : AppCompatActivity() {
    private val locationPermissionRequest = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        when {
            permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true -> {
                enableLocationTracking()
            }
            permissions[Manifest.permission.ACCESS_COARSE_LOCATION] == true -> {
                enableLocationTracking()
            }
            else -> {
                // Handle denied
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestLocationPermissions()
    }

    private fun requestLocationPermissions() {
        when {
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED -> {
                enableLocationTracking()
            }
            else -> {
                locationPermissionRequest.launch(
                    arrayOf(
                        Manifest.permission.ACCESS_FINE_LOCATION,
                        Manifest.permission.ACCESS_COARSE_LOCATION
                    )
                )
            }
        }
    }

    private fun enableLocationTracking() {
        mapView.location.enabled = true
    }
}
```

**Add to AndroidManifest.xml:**

```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

### ❌ Mistake 4: Adding Layers Before Map Loads

```kotlin
// ❌ BAD: Adding layers immediately
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    mapView = findViewById(R.id.mapView)
    addCustomLayers() // Map not loaded yet!
}

// ✅ GOOD: Wait for style to load
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    mapView = findViewById(R.id.mapView)

    mapView.getMapboxMap().loadStyleUri(Style.MAPBOX_STREETS) { style ->
        addCustomLayers(style)
    }
}
```

---

## Testing Patterns

### Unit Testing Map Logic

```kotlin
import org.junit.Test
import org.junit.Assert.*
import com.mapbox.geojson.Point

class MapLogicTest {
    @Test
    fun testCoordinateConversion() {
        val point = Point.fromLngLat(-122.4194, 37.7749)

        // Test your map logic without creating actual MapView
        val converted = MapLogic.convert(point)

        assertEquals(-122.4194, converted.longitude(), 0.001)
        assertEquals(37.7749, converted.latitude(), 0.001)
    }
}
```

### Instrumented Testing with Maps

```kotlin
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class MapActivityTest {
    @get:Rule
    val activityRule = ActivityScenarioRule(MapActivity::class.java)

    @Test
    fun testMapLoads() {
        activityRule.scenario.onActivity { activity ->
            val mapView = activity.findViewById<MapView>(R.id.mapView)
            assertNotNull(mapView)
        }
    }
}
```

---

## Troubleshooting

### Map Not Displaying

**Checklist:**
1. ✅ Token configured in string resources?
2. ✅ Correct package name in token restrictions?
3. ✅ MapboxMaps dependency added to build.gradle?
4. ✅ MapView lifecycle methods called?
5. ✅ Internet permission in AndroidManifest.xml?

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

### Memory Leaks

**Use Android Studio Profiler:**
1. Run → Profile 'app' → Memory
2. Look for MapView instances not being garbage collected
3. Ensure `mapView.onDestroy()` is called
4. Set `mapView = null` in Fragments after destroy

### Slow Performance

**Common causes:**
- Too many markers (use clustering or symbols)
- Large GeoJSON sources (use vector tiles)
- Not handling lifecycle properly
- Not calling `onLowMemory()`
- Running on emulator (use device for accurate testing)

---

## Platform-Specific Considerations

### Android Version Support

- **Android 6.0+ (API 23+)**: Minimum supported version
- **Android 12+ (API 31+)**: New permission handling
- **Android 13+ (API 33+)**: Runtime notification permissions

### Device Optimization

```kotlin
import android.app.ActivityManager
import android.content.Context

fun isLowRamDevice(): Boolean {
    val activityManager = getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
    return activityManager.isLowRamDevice
}

// Adjust map quality based on device
if (isLowRamDevice()) {
    // Reduce detail, limit features
}
```

### Screen Density

```kotlin
val density = resources.displayMetrics.density
when {
    density >= 4.0 -> {
        // xxxhdpi displays
        // Use highest quality
    }
    density >= 3.0 -> {
        // xxhdpi displays
        // High quality
    }
    density >= 2.0 -> {
        // xhdpi displays
        // Standard quality
    }
}
```

---

## Reference

- [Mapbox Maps SDK for Android](https://docs.mapbox.com/android/maps/guides/)
- [API Reference](https://docs.mapbox.com/android/maps/api-reference/)
- [Examples](https://docs.mapbox.com/android/maps/examples/)
- [Navigation SDK](https://docs.mapbox.com/android/navigation/guides/)
- [Gradle Installation](https://docs.mapbox.com/android/maps/guides/install/)
- [Migration Guides](https://docs.mapbox.com/android/maps/guides/migrate-to-v10/)
