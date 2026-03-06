---
name: "flutter-caching"
description: "Cache data in a Flutter app"
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Wed, 04 Mar 2026 18:37:11 GMT"

---
# flutter-caching-and-performance

## Goal
Implements advanced caching, offline-first data persistence, and performance optimization strategies in Flutter applications. Evaluates application requirements to select and integrate the appropriate local caching mechanism (in-memory, persistent, file system, or on-device databases). Configures Android-specific FlutterEngine caching to minimize initialization latency. Optimizes widget rendering, image caching, and scrolling performance while adhering to current Flutter API standards and avoiding expensive rendering operations.

## Instructions

### 1. Evaluate and Select Caching Strategy (Decision Logic)
Analyze the user's data retention requirements using the following decision tree to select the appropriate caching mechanism:
*   **Is the data temporary and only needed for the current session?**
    *   *Yes:* Use **In-memory caching**.
*   **Is the data small, simple key-value pairs (e.g., user preferences)?**
    *   *Yes:* Use **`shared_preferences`**.
*   **Is the data large, relational, or requires complex querying?**
    *   *Yes:* Use **On-device databases** (e.g., `sqflite`). Proceed to Step 3.
*   **Is the data large binary files, custom documents, or JSON blobs?**
    *   *Yes:* Use **File system caching** (`path_provider`). Proceed to Step 2.
*   **Is the data network images?**
    *   *Yes:* Use **Image caching** (`cached_network_image` or custom `ImageCache`). Proceed to Step 6.
*   **Is the goal to reduce Android Flutter UI warm-up time?**
    *   *Yes:* Use **FlutterEngine caching**. Proceed to Step 5.

**STOP AND ASK THE USER:** "Based on your requirements, which data type and size are we handling? Should I implement SQLite, File System caching, or a different strategy?"

### 2. Implement File System Caching
When `shared_preferences` is insufficient for larger data, use `path_provider` and `dart:io` to persist data to the device's hard drive.

```dart
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class FileCacheService {
  Future<String> get _localPath async {
    // Use getTemporaryDirectory() for system-cleared cache
    // Use getApplicationDocumentsDirectory() for persistent data
    final directory = await getApplicationDocumentsDirectory();
    return directory.path;
  }

  Future<File> get _localFile async {
    final path = await _localPath;
    return File('$path/cached_data.json');
  }

  Future<File> writeData(String data) async {
    final file = await _localFile;
    return file.writeAsString(data);
  }

  Future<String?> readData() async {
    try {
      final file = await _localFile;
      return await file.readAsString();
    } catch (e) {
      return null; // Cache miss
    }
  }
}
```

### 3. Implement SQLite Persistence
For large datasets requiring improved performance over simple files, implement an on-device database using `sqflite`.

```dart
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

class DatabaseService {
  late Database _database;

  Future<void> initDB() async {
    _database = await openDatabase(
      join(await getDatabasesPath(), 'app_cache.db'),
      onCreate: (db, version) {
        return db.execute(
          'CREATE TABLE cache_data(id INTEGER PRIMARY KEY, key TEXT, payload TEXT)',
        );
      },
      version: 1,
    );
  }

  Future<void> insertCache(String key, String payload) async {
    await _database.insert(
      'cache_data',
      {'key': key, 'payload': payload},
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<String?> getCache(String key) async {
    final List<Map<String, Object?>> maps = await _database.query(
      'cache_data',
      where: 'key = ?',
      whereArgs: [key], // MUST use whereArgs to prevent SQL injection
    );
    if (maps.isNotEmpty) {
      return maps.first['payload'] as String;
    }
    return null;
  }
}
```

### 4. Implement Offline-First Repository (Stream-based)
Combine local caching and remote fetching. Yield the cached data first (cache hit), then fetch from the network, update the cache, and yield the fresh data.

```dart
Stream<UserProfile> getUserProfile() async* {
  // 1. Check local cache
  final localData = await _databaseService.getCache('user_profile');
  if (localData != null) {
    yield UserProfile.fromJson(localData);
  }

  // 2. Fetch remote data
  try {
    final remoteData = await _apiClient.fetchUserProfile();
    // 3. Update cache
    await _databaseService.insertCache('user_profile', remoteData.toJson());
    // 4. Yield fresh data
    yield remoteData;
  } catch (e) {
    // Handle network failure; local data has already been yielded
  }
}
```

### 5. Implement FlutterEngine Caching (Android)
To minimize Flutter's initialization time when adding Flutter screens to an Android app, pre-warm and cache the `FlutterEngine`.

**Pre-warm in Application class (Kotlin):**
```kotlin
class MyApplication : Application() {
  lateinit var flutterEngine : FlutterEngine
  override fun onCreate() {
    super.onCreate()
    flutterEngine = FlutterEngine(this)
    // Optional: Configure initial route before executing entrypoint
    flutterEngine.navigationChannel.setInitialRoute("/cached_route");
    flutterEngine.dartExecutor.executeDartEntrypoint(
      DartExecutor.DartEntrypoint.createDefault()
    )
    FlutterEngineCache.getInstance().put("my_engine_id", flutterEngine)
  }
}
```

**Consume in Activity/Fragment (Kotlin):**
```kotlin
// For Activity
startActivity(
  FlutterActivity
    .withCachedEngine("my_engine_id")
    .backgroundMode(FlutterActivityLaunchConfigs.BackgroundMode.transparent)
    .build(this)
)

// For Fragment
val flutterFragment = FlutterFragment.withCachedEngine("my_engine_id")
    .renderMode(FlutterView.RenderMode.texture)
    .shouldAttachEngineToActivity(false)
    .build()
```

### 6. Optimize Image and Scroll Caching
Apply strict constraints to image caching and scrolling to prevent GPU memory bloat and layout passes.

**ImageCache Validation:**
Verify cache hits without triggering loads using `containsKey`.
```dart
class CustomImageCache extends ImageCache {
  @override
  bool containsKey(Object key) {
    // Check if cache is tracking this key
    return super.containsKey(key); 
  }
}
```

**ScrollCacheExtent Implementation:**
Use the strongly-typed `ScrollCacheExtent` object for scrolling widgets (replaces deprecated `cacheExtent` and `cacheExtentStyle`).
```dart
ListView(
  // Use ScrollCacheExtent.pixels for pixel-based caching
  scrollCacheExtent: const ScrollCacheExtent.pixels(500.0),
  children: [ ... ],
)

Viewport(
  // Use ScrollCacheExtent.viewport for fraction-based caching
  scrollCacheExtent: const ScrollCacheExtent.viewport(0.5),
  slivers: [ ... ],
)
```

### 7. Validate-and-Fix Performance
Review the generated UI code for performance pitfalls.
1.  **Check for `saveLayer()` triggers:** Ensure `Opacity`, `ShaderMask`, `ColorFilter`, and `Clip.antiAliasWithSaveLayer` are only used when absolutely necessary. Replace `Opacity` with semitransparent colors or `FadeInImage` where possible.
2.  **Check `operator ==` overrides:** Ensure `operator ==` is NOT overridden on `Widget` objects unless they are leaf widgets whose properties rarely change.
3.  **Check Intrinsic Passes:** Ensure `ListView` and `GridView` use lazy builder methods (`ListView.builder`) and avoid intrinsic layout passes by setting fixed sizes where possible.

## Constraints
*   **SQL Injection Prevention:** ALWAYS use `whereArgs` in `sqflite` queries. NEVER use string interpolation for SQL `where` clauses.
*   **Engine Lifecycle:** When using a cached `FlutterEngine` in Android, remember it outlives the `Activity`/`Fragment`. Explicitly call `FlutterEngine.destroy()` when it is no longer needed to clear resources.
*   **Image Caching Limits:** Raster cache entries are expensive to construct and use significant GPU memory. Only cache images when absolutely necessary. Do not artificially inflate `ImageCache.maxByteSize`.
*   **Widget Equality:** Do not override `operator ==` on widgets to force caching, as this degrades performance to O(N²). Rely on `const` constructors instead.
*   **Scroll Extents:** NEVER use the deprecated `cacheExtent` (double) or `cacheExtentStyle`. ALWAYS use the `ScrollCacheExtent` object.
*   **Web Workers:** If targeting Flutter Web, remember that Dart `isolates` are not supported. Do not generate isolate-based background parsing for web targets.
