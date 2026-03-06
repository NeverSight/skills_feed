---
name: "flutter-platform-views"
description: "Add a native view into your Flutter app"
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Wed, 04 Mar 2026 18:59:25 GMT"

---
# flutter-platform-views-and-web-embedding

## Goal
Guides developers through implementing Flutter Platform Views for Android, iOS, and macOS, as well as embedding Flutter into existing web applications. Assumes the user has a configured Flutter environment and is comfortable with Dart, JavaScript, and the relevant native platform languages (Kotlin, Swift).

## Instructions

### 1. Determine the Target Platform and Embedding Strategy (Decision Logic)
Before writing code, you must determine the target platform and the specific embedding strategy required by the user.

**STOP AND ASK THE USER:**
"Which platform are you targeting for native view embedding?
1. Android (Requires choosing between Hybrid Composition or Texture Layer)
2. iOS (Hybrid Composition only)
3. macOS (Hybrid Composition only, gesture support limited)
4. Web (Requires choosing between Full Page mode or Embedded/Multi-view mode)"

**Decision Tree:**
*   **If Android:** Ask the user: "Do you prioritize native Android view fidelity (Hybrid Composition) or Flutter rendering performance (Texture Layer)?"
*   **If Web:** Ask the user: "Are you taking over the full page, or embedding Flutter into specific HTML elements (Embedded/Multi-view mode)?"

### 2. Implement Android Platform Views
Based on the user's choice in Step 1, implement the Dart and Kotlin sides.

**Dart Implementation:**
If the user chose **Hybrid Composition** (Best fidelity, lower Flutter FPS):
```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';

Widget buildHybridAndroidView(BuildContext context, String viewType, Map<String, dynamic> creationParams) {
  return PlatformViewLink(
    viewType: viewType,
    surfaceFactory: (context, controller) {
      return AndroidViewSurface(
        controller: controller as AndroidViewController,
        gestureRecognizers: const <Factory<OneSequenceGestureRecognizer>>{},
        hitTestBehavior: PlatformViewHitTestBehavior.opaque,
      );
    },
    onCreatePlatformView: (params) {
      return PlatformViewsService.initSurfaceAndroidView(
        id: params.id,
        viewType: viewType,
        layoutDirection: TextDirection.ltr,
        creationParams: creationParams,
        creationParamsCodec: const StandardMessageCodec(),
        onFocus: () {
          params.onFocusChanged(true);
        },
      )
        ..addOnPlatformViewCreatedListener(params.onPlatformViewCreated)
        ..create();
    },
  );
}
```

If the user chose **Texture Layer** (Best Flutter FPS, janky quick scrolling):
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

Widget buildTextureAndroidView(BuildContext context, String viewType, Map<String, dynamic> creationParams) {
  return AndroidView(
    viewType: viewType,
    layoutDirection: TextDirection.ltr,
    creationParams: creationParams,
    creationParamsCodec: const StandardMessageCodec(),
  );
}
```

**Kotlin Implementation (Platform Side):**
Create the View, the Factory, and register it in the `MainActivity`.
```kotlin
package dev.flutter.example

import android.content.Context
import android.graphics.Color
import android.view.View
import android.widget.TextView
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.StandardMessageCodec
import io.flutter.plugin.platform.PlatformView
import io.flutter.plugin.platform.PlatformViewFactory

// 1. Define the View
internal class NativeView(context: Context, id: Int, creationParams: Map<String?, Any?>?) : PlatformView {
    private val textView: TextView = TextView(context).apply {
        textSize = 72f
        setBackgroundColor(Color.rgb(255, 255, 255))
        text = "Rendered on a native Android view (id: $id)"
    }
    override fun getView(): View = textView
    override fun dispose() {}
}

// 2. Define the Factory
class NativeViewFactory : PlatformViewFactory(StandardMessageCodec.INSTANCE) {
    override fun create(context: Context, viewId: Int, args: Any?): PlatformView {
        val creationParams = args as Map<String?, Any?>?
        return NativeView(context, viewId, creationParams)
    }
}

// 3. Register in MainActivity
class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        flutterEngine
            .platformViewsController
            .registry
            .registerViewFactory("<platform-view-type>", NativeViewFactory())
    }
}
```
*Validate-and-Fix:* If the user is embedding a `SurfaceView` or `SurfaceTexture`, instruct them to manually call `invalidate()` on the view when content changes, as they do not invalidate themselves automatically.

### 3. Implement iOS Platform Views
iOS uses Hybrid Composition exclusively.

**Dart Implementation:**
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

Widget buildIosView(BuildContext context, String viewType, Map<String, dynamic> creationParams) {
  return UiKitView(
    viewType: viewType,
    layoutDirection: TextDirection.ltr,
    creationParams: creationParams,
    creationParamsCodec: const StandardMessageCodec(),
  );
}
```

**Swift Implementation (Platform Side):**
```swift
import Flutter
import UIKit

// 1. Define the View
class FLNativeView: NSObject, FlutterPlatformView {
    private var _view: UIView

    init(frame: CGRect, viewIdentifier viewId: Int64, arguments args: Any?, binaryMessenger messenger: FlutterBinaryMessenger?) {
        _view = UIView()
        super.init()
        createNativeView(view: _view)
    }

    func view() -> UIView { return _view }

    func createNativeView(view _view: UIView){
        _view.backgroundColor = UIColor.blue
        let nativeLabel = UILabel()
        nativeLabel.text = "Native text from iOS"
        nativeLabel.textColor = UIColor.white
        nativeLabel.textAlignment = .center
        nativeLabel.frame = CGRect(x: 0, y: 0, width: 180, height: 48.0)
        _view.addSubview(nativeLabel)
    }
}

// 2. Define the Factory
class FLNativeViewFactory: NSObject, FlutterPlatformViewFactory {
    private var messenger: FlutterBinaryMessenger

    init(messenger: FlutterBinaryMessenger) {
        self.messenger = messenger
        super.init()
    }

    func create(withFrame frame: CGRect, viewIdentifier viewId: Int64, arguments args: Any?) -> FlutterPlatformView {
        return FLNativeView(frame: frame, viewIdentifier: viewId, arguments: args, binaryMessenger: messenger)
    }

    public func createArgsCodec() -> FlutterMessageCodec & NSObjectProtocol {
          return FlutterStandardMessageCodec.sharedInstance()
    }
}

// 3. Register in AppDelegate
@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]?
    ) -> Bool {
        GeneratedPluginRegistrant.register(with: self)
        guard let pluginRegistrar = self.registrar(forPlugin: "plugin-name") else { return false }
        
        let factory = FLNativeViewFactory(messenger: pluginRegistrar.messenger())
        pluginRegistrar.register(factory, withId: "<platform-view-type>")
        
        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }
}
```

### 4. Implement macOS Platform Views
macOS uses Hybrid Composition. Note that gesture support is currently limited.

**Dart Implementation:**
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

Widget buildMacOsView(BuildContext context, String viewType, Map<String, dynamic> creationParams) {
  return AppKitView(
    viewType: viewType,
    layoutDirection: TextDirection.ltr,
    creationParams: creationParams,
    creationParamsCodec: const StandardMessageCodec(),
  );
}
```

**Swift Implementation (Platform Side):**
```swift
import Cocoa
import FlutterMacOS

// 1. Define the View
class NativeView: NSView {
  init(viewIdentifier viewId: Int64, arguments args: Any?, binaryMessenger messenger: FlutterBinaryMessenger?) {
    super.init(frame: CGRect(x: 0, y: 0, width: 200, height: 200))
    wantsLayer = true
    layer?.backgroundColor = NSColor.systemBlue.cgColor
    createNativeView(view: self)
  }
  required init?(coder nsCoder: NSCoder) { super.init(coder: nsCoder) }

  func createNativeView(view _view: NSView) {
    let nativeLabel = NSTextField()
    nativeLabel.frame = CGRect(x: 0, y: 0, width: 180, height: 48.0)
    nativeLabel.stringValue = "Native text from macOS"
    nativeLabel.isEditable = false
    nativeLabel.sizeToFit()
    _view.addSubview(nativeLabel)
  }
}

// 2. Define the Factory
class NativeViewFactory: NSObject, FlutterPlatformViewFactory {
  private var messenger: FlutterBinaryMessenger
  init(messenger: FlutterBinaryMessenger) {
    self.messenger = messenger
    super.init()
  }
  func create(withViewIdentifier viewId: Int64, arguments args: Any?) -> NSView {
    return NativeView(viewIdentifier: viewId, arguments: args, binaryMessenger: messenger)
  }
  public func createArgsCodec() -> (FlutterMessageCodec & NSObjectProtocol)? {
    return FlutterStandardMessageCodec.sharedInstance()
  }
}

// 3. Register in MainFlutterWindow.swift
class MainFlutterWindow: NSWindow {
  override func awakeFromNib() {
    let registrar = flutterViewController.registrar(forPlugin: "plugin-name")
    let factory = NativeViewFactory(messenger: registrar.messenger)
    registrar.register(factory, withId: "<platform-view-type>")
    super.awakeFromNib()
  }
}
```

### 5. Implement Web Embedding
If the user chose **Embedded/Multi-view mode**, implement the JS and Dart configurations.

**JavaScript Implementation (`flutter_bootstrap.js` or HTML script):**
```javascript
_flutter.loader.load({
  onEntrypointLoaded: async function onEntrypointLoaded(engineInitializer) {
    let engine = await engineInitializer.initializeEngine({
      multiViewEnabled: true, // Enables embedded mode.
    });
    let app = await engine.runApp();
    
    // Add a view to a specific host element
    let viewId = app.addView({
      hostElement: document.querySelector('#flutter-host-element'),
      initialData: { greeting: 'Hello from JS!' }
    });
  }
});
```

**Dart Implementation (`main.dart`):**
*Validate-and-Fix:* Ensure `runWidget` is used instead of `runApp`. `runApp` will fail with a null `implicitView` error in multi-view mode.

```dart
import 'dart:ui' show FlutterView;
import 'package:flutter/widgets.dart';

void main() {
  // MUST use runWidget, not runApp, for multi-view web embedding.
  runWidget(
    MultiViewApp(
      viewBuilder: (BuildContext context) => const MyEmbeddedWidget(),
    ),
  );
}

class MultiViewApp extends StatefulWidget {
  const MultiViewApp({super.key, required this.viewBuilder});
  final WidgetBuilder viewBuilder;

  @override
  State<MultiViewApp> createState() => _MultiViewAppState();
}

class _MultiViewAppState extends State<MultiViewApp> with WidgetsBindingObserver {
  Map<Object, Widget> _views = <Object, Widget>{};

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _updateViews();
  }

  @override
  void didChangeMetrics() {
    _updateViews();
  }

  void _updateViews() {
    final Map<Object, Widget> newViews = <Object, Widget>{};
    for (final FlutterView view in WidgetsBinding.instance.platformDispatcher.views) {
      final Widget viewWidget = _views[view.viewId] ?? _createViewWidget(view);
      newViews[view.viewId] = viewWidget;
    }
    setState(() {
      _views = newViews;
    });
  }

  Widget _createViewWidget(FlutterView view) {
    return View(
      view: view,
      child: Builder(builder: widget.viewBuilder),
    );
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ViewCollection(views: _views.values.toList(growable: false));
  }
}

class MyEmbeddedWidget extends StatelessWidget {
  const MyEmbeddedWidget({super.key});

  @override
  Widget build(BuildContext context) {
    // Retrieve the viewId to handle specific logic if needed
    final int viewId = View.of(context).viewId;
    return Directionality(
      textDirection: TextDirection.ltr,
      child: Center(child: Text('Rendered in View ID: $viewId')),
    );
  }
}
```

## Constraints
*   **Do not** use `runApp` when configuring Flutter Web for multi-view embedding. You must use `runWidget` and manage the `FlutterView` lifecycle via `WidgetsBindingObserver`.
*   **Do not** use `ShaderMask` or `ColorFiltered` widgets over iOS Platform Views, as they are unsupported. `BackdropFilter` has strict limitations.
*   **Do not** assume Android `SurfaceView` or `SurfaceTexture` will automatically invalidate when their content changes. You must manually call `invalidate()` on the view or its parent.
*   **Do not** wrap the entire output in a markdown code block. Return raw markdown text.
*   **Always** verify the Android API level is 23+ before implementing Platform Views.
