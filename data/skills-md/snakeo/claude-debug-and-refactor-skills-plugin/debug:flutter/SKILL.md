---
name: debug:flutter
description: Debug Flutter applications systematically with this comprehensive troubleshooting skill. Covers RenderFlex overflow errors, setState() after dispose() issues, null check operator failures, platform channel problems, build context errors, and hot reload failures. Provides structured four-phase debugging methodology with Flutter DevTools, widget inspector, performance profiling, and platform-specific debugging for Android, iOS, and web targets.
---

# Flutter Debugging Guide

This skill provides a systematic approach to debugging Flutter applications, covering common error patterns, debugging tools, and best practices for efficient problem resolution.

## Common Error Patterns

### 1. RenderFlex Overflow Error

**Symptoms:**
- Yellow and black stripes appear in the UI indicating overflow area
- Error message: "A RenderFlex overflowed by X pixels"

**Causes:**
- Content exceeds available space in Row/Column
- Fixed-size widgets in constrained containers
- Text without proper overflow handling

**Solutions:**
```dart
// Solution 1: Wrap in SingleChildScrollView
SingleChildScrollView(
  child: Column(
    children: [...],
  ),
)

// Solution 2: Use Flexible or Expanded
Row(
  children: [
    Expanded(
      child: Text('Long text that might overflow...'),
    ),
  ],
)

// Solution 3: Handle text overflow explicitly
Text(
  'Long text...',
  overflow: TextOverflow.ellipsis,
  maxLines: 2,
)
```

### 2. setState() Called After Dispose

**Symptoms:**
- Runtime error: "setState() called after dispose()"
- App crashes after async operations complete

**Causes:**
- Calling setState() after widget is removed from tree
- Async operations completing after navigation away
- Timer callbacks on disposed widgets

**Solutions:**
```dart
// Solution 1: Check mounted before setState
Future<void> fetchData() async {
  final data = await api.getData();
  if (mounted) {
    setState(() {
      _data = data;
    });
  }
}

// Solution 2: Cancel async operations in dispose
late final StreamSubscription _subscription;

@override
void dispose() {
  _subscription.cancel();
  super.dispose();
}

// Solution 3: Use CancelableOperation
CancelableOperation<Data>? _operation;

Future<void> fetchData() async {
  _operation = CancelableOperation.fromFuture(api.getData());
  final data = await _operation!.value;
  if (mounted) {
    setState(() => _data = data);
  }
}

@override
void dispose() {
  _operation?.cancel();
  super.dispose();
}
```

### 3. Null Check Operator Errors

**Symptoms:**
- Error: "Null check operator used on a null value"
- App crashes when accessing nullable values with `!`

**Causes:**
- Using `!` operator on null values
- Not initializing late variables
- Race conditions in async code

**Solutions:**
```dart
// Bad: Using ! without null check
final name = user!.name;

// Good: Use null-aware operators
final name = user?.name ?? 'Unknown';

// Good: Use if-null check
if (user != null) {
  final name = user.name;
}

// Good: Use pattern matching (Dart 3+)
if (user case final u?) {
  final name = u.name;
}

// For late initialization, consider nullable with check
String? _data;

String get data {
  if (_data == null) {
    throw StateError('Data not initialized');
  }
  return _data!;
}
```

### 4. Platform Channel Issues

**Symptoms:**
- MissingPluginException
- PlatformException with native code errors
- Method channel not responding

**Solutions:**
```dart
// Solution 1: Ensure proper platform setup
// Run flutter clean && flutter pub get

// Solution 2: Check method channel registration
const platform = MethodChannel('com.example/channel');

try {
  final result = await platform.invokeMethod('methodName');
} on PlatformException catch (e) {
  debugPrint('Platform error: ${e.message}');
} on MissingPluginException {
  debugPrint('Plugin not registered for this platform');
}

// Solution 3: For plugins, ensure proper initialization
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Initialize plugins here
  runApp(MyApp());
}
```

### 5. Build Context Errors

**Symptoms:**
- "Looking up a deactivated widget's ancestor is unsafe"
- Navigator operations fail
- Theme/MediaQuery not available

**Causes:**
- Using context after widget disposal
- Using context in initState before build
- Storing context references

**Solutions:**
```dart
// Bad: Using context in initState
@override
void initState() {
  super.initState();
  // Theme.of(context); // Error!
}

// Good: Use didChangeDependencies
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  final theme = Theme.of(context);
}

// Good: Use Builder for nested contexts
Scaffold(
  body: Builder(
    builder: (context) {
      // This context has access to Scaffold
      return ElevatedButton(
        onPressed: () {
          Scaffold.of(context).showSnackBar(...);
        },
        child: Text('Show Snackbar'),
      );
    },
  ),
)

// Good: Use GlobalKey for cross-widget access
final scaffoldKey = GlobalKey<ScaffoldState>();
```

### 6. Hot Reload Failures

**Symptoms:**
- Changes not reflecting after save
- App state lost unexpectedly
- "Hot reload not available" message

**Causes:**
- Changing app initialization code
- Modifying const constructors
- Native code changes
- Global variable mutations

**Solutions:**
```bash
# Solution 1: Hot restart instead of hot reload
# Press 'R' (capital) in terminal or Shift+Cmd+\ in VS Code

# Solution 2: Full restart
flutter run --no-hot

# Solution 3: Clean build
flutter clean && flutter pub get && flutter run
```

**Code patterns that require hot restart:**
```dart
// Changes to main() require restart
void main() {
  runApp(MyApp()); // Modification here needs restart
}

// Changes to initState logic often need restart
@override
void initState() {
  super.initState();
  _controller = AnimationController(...); // Changes here need restart
}

// Const constructor changes need restart
const MyWidget({super.key}); // Adding/removing const needs restart
```

### 7. Vertical Viewport Given Unbounded Height

**Symptoms:**
- Error: "Vertical viewport was given unbounded height"
- ListView inside Column fails

**Solutions:**
```dart
// Bad: ListView in Column without constraints
Column(
  children: [
    ListView(...), // Error!
  ],
)

// Good: Use Expanded
Column(
  children: [
    Expanded(
      child: ListView(...),
    ),
  ],
)

// Good: Use shrinkWrap (for small lists only)
Column(
  children: [
    ListView(
      shrinkWrap: true,
      physics: NeverScrollableScrollPhysics(),
      children: [...],
    ),
  ],
)

// Good: Use SizedBox with fixed height
Column(
  children: [
    SizedBox(
      height: 200,
      child: ListView(...),
    ),
  ],
)
```

### 8. RenderBox Was Not Laid Out

**Symptoms:**
- Error: "RenderBox was not laid out"
- Widget fails to render

**Solutions:**
```dart
// Ensure parent provides constraints
SizedBox(
  width: 200,
  height: 200,
  child: CustomPaint(...),
)

// For intrinsic sizing
IntrinsicHeight(
  child: Row(
    children: [
      Container(color: Colors.red),
      Container(color: Colors.blue),
    ],
  ),
)
```

### 9. Incorrect Use of ParentDataWidget

**Symptoms:**
- Error: "Incorrect use of ParentDataWidget"
- Positioned/Expanded used incorrectly

**Solutions:**
```dart
// Bad: Positioned outside Stack
Column(
  children: [
    Positioned(...), // Error!
  ],
)

// Good: Positioned inside Stack
Stack(
  children: [
    Positioned(
      top: 10,
      left: 10,
      child: Text('Hello'),
    ),
  ],
)

// Bad: Expanded outside Flex widget
Container(
  child: Expanded(...), // Error!
)

// Good: Expanded inside Row/Column
Row(
  children: [
    Expanded(child: Text('Hello')),
  ],
)
```

### 10. Red/Grey Screen of Death

**Symptoms:**
- Red screen in debug/profile mode
- Grey screen in release mode
- App appears frozen

**Causes:**
- Uncaught exceptions
- Rendering errors
- Failed assertions

**Solutions:**
```dart
// Global error handling
void main() {
  FlutterError.onError = (details) {
    FlutterError.presentError(details);
    // Log to crash reporting service
    crashReporter.recordFlutterError(details);
  };

  PlatformDispatcher.instance.onError = (error, stack) {
    // Handle async errors
    crashReporter.recordError(error, stack);
    return true;
  };

  runApp(MyApp());
}

// Custom error widget
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    ErrorWidget.builder = (FlutterErrorDetails details) {
      return CustomErrorWidget(details: details);
    };
    return MaterialApp(...);
  }
}
```

## Debugging Tools

### Flutter DevTools

The comprehensive suite for Flutter debugging:

```bash
# Launch DevTools
flutter pub global activate devtools
flutter pub global run devtools

# Or access via VS Code Flutter extension
```

**Key DevTools Features:**
- **Widget Inspector**: Examine widget tree, properties, and render objects
- **Performance View**: Analyze frame rendering and jank
- **Memory View**: Track allocations and detect memory leaks
- **Network View**: Monitor HTTP requests
- **Logging View**: View all debug output
- **CPU Profiler**: Identify performance bottlenecks

### flutter doctor

Diagnose environment issues:

```bash
# Full diagnostic
flutter doctor -v

# Check specific issues
flutter doctor --android-licenses

# Common fixes
flutter clean
flutter pub get
flutter pub upgrade
```

### Dart DevTools Debugger

```dart
// Set breakpoints in code
debugger(when: condition);

// Conditional breakpoints in IDE
// Right-click line number > Add Conditional Breakpoint
```

### Logging Best Practices

```dart
// Basic logging
print('Debug message'); // stdout

// Better: debugPrint for large outputs (prevents dropped logs)
debugPrint('Large debug output...');

// Best: dart:developer log for granular control
import 'dart:developer';

log(
  'User action',
  name: 'UserFlow',
  error: exception,
  stackTrace: stackTrace,
);

// Conditional logging
assert(() {
  debugPrint('Only in debug mode');
  return true;
}());

// Using kDebugMode
import 'package:flutter/foundation.dart';

if (kDebugMode) {
  print('Debug only');
}
```

### Flutter Inspector (Widget Inspector)

```dart
// Enable debug painting
import 'package:flutter/rendering.dart';

debugPaintSizeEnabled = true;
debugPaintBaselinesEnabled = true;
debugPaintLayerBordersEnabled = true;
debugPaintPointersEnabled = true;

// In widget
debugPrint(context.widget.toStringDeep());
```

## The Four Phases of Flutter Debugging

### Phase 1: Identify the Error Type

Categorize the error:

1. **Compile-time errors**: Syntax, type errors (red squiggles)
2. **Runtime errors**: Exceptions during execution
3. **Layout errors**: RenderFlex overflow, unbounded constraints
4. **State errors**: setState after dispose, inconsistent state
5. **Platform errors**: Native plugin issues, permissions
6. **Performance issues**: Jank, memory leaks, slow frames

```bash
# Get detailed error information
flutter analyze
flutter test --reporter expanded
```

### Phase 2: Reproduce and Isolate

```dart
// Create minimal reproduction
class DebugWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Isolate the problematic widget
    return Container(
      child: ProblematicWidget(),
    );
  }
}

// Use assertions to validate state
assert(data != null, 'Data should not be null at this point');
assert(index >= 0 && index < list.length, 'Index out of bounds: $index');
```

### Phase 3: Debug and Fix

```dart
// Add strategic logging
void processData() {
  debugPrint('processData called with: $data');

  try {
    final result = transform(data);
    debugPrint('Transform result: $result');
  } catch (e, stack) {
    debugPrint('Transform failed: $e');
    debugPrint('Stack trace: $stack');
    rethrow;
  }
}

// Use DevTools breakpoints
// Set breakpoints at:
// - Method entry points
// - Before suspected failure points
// - In catch blocks
```

### Phase 4: Verify and Prevent

```dart
// Add tests for the fix
testWidgets('Widget handles null data gracefully', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: MyWidget(data: null),
    ),
  );

  expect(find.text('No data'), findsOneWidget);
  expect(tester.takeException(), isNull);
});

// Add defensive coding
Widget build(BuildContext context) {
  if (data == null) {
    return const EmptyState();
  }
  return DataDisplay(data: data!);
}
```

## Quick Reference Commands

### Diagnostics

```bash
# Environment check
flutter doctor -v

# Analyze code for issues
flutter analyze

# Check for outdated packages
flutter pub outdated

# Upgrade packages
flutter pub upgrade --major-versions
```

### Testing

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/widget_test.dart

# Run with coverage
flutter test --coverage

# Run integration tests
flutter test integration_test/
```

### Build and Run

```bash
# Debug mode (default)
flutter run

# Profile mode (for performance debugging)
flutter run --profile

# Release mode
flutter run --release

# Specific device
flutter run -d <device_id>

# List devices
flutter devices
```

### Clean and Reset

```bash
# Clean build artifacts
flutter clean

# Get dependencies
flutter pub get

# Reset iOS pods
cd ios && pod deintegrate && pod install && cd ..

# Reset Android
cd android && ./gradlew clean && cd ..
```

### DevTools

```bash
# Install DevTools globally
flutter pub global activate devtools

# Run DevTools
flutter pub global run devtools

# Or use dart devtools
dart devtools
```

## Performance Debugging

### Identify Jank

```dart
// Enable performance overlay
MaterialApp(
  showPerformanceOverlay: true,
  ...
)

// Or toggle in DevTools
// Performance > Show Performance Overlay
```

### Common Performance Issues

```dart
// Bad: Building expensive widgets in build()
@override
Widget build(BuildContext context) {
  final expensiveData = computeExpensiveData(); // Called every rebuild!
  return ExpensiveWidget(data: expensiveData);
}

// Good: Cache expensive computations
late final expensiveData = computeExpensiveData();

// Good: Use const constructors
const MyWidget(key: Key('my-widget'));

// Good: Use RepaintBoundary for isolated repaints
RepaintBoundary(
  child: ExpensiveAnimatedWidget(),
)
```

### Memory Debugging

```dart
// Check for leaks in DevTools Memory view

// Common leak patterns:
// 1. Streams not disposed
@override
void dispose() {
  _streamSubscription.cancel();
  super.dispose();
}

// 2. Controllers not disposed
@override
void dispose() {
  _textController.dispose();
  _animationController.dispose();
  super.dispose();
}

// 3. Listeners not removed
@override
void dispose() {
  _focusNode.removeListener(_onFocusChange);
  _focusNode.dispose();
  super.dispose();
}
```

## State Management Debugging

### Provider/Riverpod

```dart
// Debug Provider rebuilds
Consumer<MyModel>(
  builder: (context, model, child) {
    debugPrint('Consumer rebuilding: ${model.value}');
    return Text(model.value);
  },
)

// Use ProviderScope observers
ProviderScope(
  observers: [DebugProviderObserver()],
  child: MyApp(),
)

class DebugProviderObserver extends ProviderObserver {
  @override
  void didUpdateProvider(
    ProviderBase provider,
    Object? previousValue,
    Object? newValue,
    ProviderContainer container,
  ) {
    debugPrint('Provider ${provider.name}: $previousValue -> $newValue');
  }
}
```

### Bloc/Cubit

```dart
// Enable Bloc observer
Bloc.observer = DebugBlocObserver();

class DebugBlocObserver extends BlocObserver {
  @override
  void onChange(BlocBase bloc, Change change) {
    super.onChange(bloc, change);
    debugPrint('${bloc.runtimeType} $change');
  }

  @override
  void onError(BlocBase bloc, Object error, StackTrace stackTrace) {
    debugPrint('${bloc.runtimeType} $error $stackTrace');
    super.onError(bloc, error, stackTrace);
  }
}
```

## Platform-Specific Debugging

### Android

```bash
# View Android logs
flutter logs

# Or use adb
adb logcat | grep flutter

# Debug native crashes
adb logcat -s AndroidRuntime:E
```

### iOS

```bash
# View iOS logs
flutter logs

# Open Xcode console
open ios/Runner.xcworkspace

# Check crash logs
# Xcode > Window > Devices and Simulators > View Device Logs
```

### Web

```dart
// Use browser DevTools console
import 'dart:html' as html;

html.window.console.log('Web debug message');

// Check for CORS issues in Network tab
// Check for CSP issues in Console
```

## Additional Resources

For detailed documentation:
- [Flutter Debugging Documentation](https://docs.flutter.dev/testing/debugging)
- [Flutter DevTools Guide](https://docs.flutter.dev/tools/devtools/debugger)
- [Common Flutter Errors](https://docs.flutter.dev/testing/common-errors)
- [Error Handling in Flutter](https://docs.flutter.dev/testing/errors)
- [Flutter Performance Profiling](https://docs.flutter.dev/perf/ui-performance)
