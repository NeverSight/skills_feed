---
name: flutter
description: Flutter framework for building beautiful, fast user experiences for mobile, web, and desktop from a single codebase. Use when building Flutter apps, working with widgets, state management, navigation, animations, or Material Design components.
metadata:
  author: hairy
  version: "2026.1.31"
  source: Generated from https://github.com/flutter/flutter, scripts located at https://github.com/hairyf/skills
---

# Flutter

> The skill is based on Flutter framework, generated at 2026-01-31.

Flutter is Google's SDK for crafting beautiful, fast user experiences for mobile, web, and desktop from a single codebase. Flutter works with existing code, is used by developers and organizations around the world, and is free and open source.

Flutter uses Dart as its programming language and follows a widget-based architecture where everything is a widget. The framework provides hot reload for fast development cycles, a rich set of Material Design and Cupertino widgets, and excellent performance through compiled code.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Widget System | StatelessWidget, StatefulWidget, Widget lifecycle, keys | [core-widgets](references/core-widgets.md) |
| State Management | setState, StatefulWidget, ValueNotifier, ChangeNotifier | [core-state-management](references/core-state-management.md) |
| Layout System | Row, Column, Stack, Flex, constraints, sizing | [core-layout](references/core-layout.md) |
| BuildContext | Context usage, InheritedWidget, theme access | [core-build-context](references/core-build-context.md) |
| InheritedWidget | Sharing data down widget tree, InheritedWidget patterns | [features-inherited-widget](references/features-inherited-widget.md) |

## Widgets

### Basic Widgets

| Topic | Description | Reference |
|-------|-------------|-----------|
| Text & Styling | Text widget, TextStyle, RichText, TextSpan | [widgets-text](references/widgets-text.md) |
| Images | Image widget, AssetImage, NetworkImage, ImageProvider | [widgets-images](references/widgets-images.md) |
| Icons | Icon widget, IconData, IconTheme | [widgets-icons](references/widgets-icons.md) |
| Buttons | ElevatedButton, TextButton, OutlinedButton, IconButton | [widgets-buttons](references/widgets-buttons.md) |
| Input Fields | TextField, TextFormField, Form, FormField | [widgets-input](references/widgets-input.md) |
| Async Widgets | FutureBuilder, StreamBuilder, async operations | [widgets-async](references/widgets-async.md) |
| ValueListenableBuilder | Building widgets based on ValueListenable changes | [widgets-value-listenable](references/widgets-value-listenable.md) |
| PageView | Swipeable pages, PageController, page navigation | [widgets-pageview](references/widgets-pageview.md) |
| RefreshIndicator | Pull-to-refresh functionality | [widgets-refresh-indicator](references/widgets-refresh-indicator.md) |
| Dismissible | Swipe-to-dismiss widgets | [widgets-dismissible](references/widgets-dismissible.md) |
| TabBar & Tabs | Tab navigation, TabController, TabBarView | [widgets-tabs](references/widgets-tabs.md) |
| Forms & Validation | Form validation, validators, form handling | [features-forms-validation](references/features-forms-validation.md) |

### Layout Widgets

| Topic | Description | Reference |
|-------|-------------|-----------|
| Flex Layouts | Row, Column, Flex, Flexible, Expanded | [layout-flex](references/layout-flex.md) |
| Stack Layout | Stack, Positioned, alignment | [layout-stack](references/layout-stack.md) |
| Container | Container, BoxDecoration, padding, margin | [layout-container](references/layout-container.md) |
| List Views | ListView, ListTile, GridView, Sliver widgets | [layout-lists](references/layout-lists.md) |
| Slivers | CustomScrollView, SliverList, SliverGrid, advanced scrolling | [features-slivers](references/features-slivers.md) |
| Scroll Controller | Programmatic scroll control, scroll listeners | [features-scroll-controller](references/features-scroll-controller.md) |

## Features

### Navigation

| Topic | Description | Reference |
|-------|-------------|-----------|
| Navigator | Navigator.push, Navigator.pop, routes | [features-navigation](references/features-navigation.md) |
| Named Routes | Route configuration, onGenerateRoute | [features-named-routes](references/features-named-routes.md) |
| Router | GoRouter, declarative routing | [features-router](references/features-router.md) |

### Animations

| Topic | Description | Reference |
|-------|-------------|-----------|
| Implicit Animations | AnimatedContainer, AnimatedOpacity, AnimatedSize | [features-implicit-animations](references/features-implicit-animations.md) |
| Explicit Animations | AnimationController, Tween, AnimationBuilder | [features-explicit-animations](references/features-explicit-animations.md) |
| Hero Animations | Hero widget, shared element transitions | [features-hero-animations](references/features-hero-animations.md) |

### Material Design

| Topic | Description | Reference |
|-------|-------------|-----------|
| Material App | MaterialApp, Theme, ThemeData | [features-material-app](references/features-material-app.md) |
| Material Components | AppBar, Scaffold, Drawer, BottomNavigationBar | [features-material-components](references/features-material-components.md) |
| Material 3 | Material 3 design system, color schemes | [features-material-3](references/features-material-3.md) |

### Cupertino (iOS)

| Topic | Description | Reference |
|-------|-------------|-----------|
| Cupertino Widgets | iOS-style widgets, CupertinoApp, CupertinoNavigationBar | [features-cupertino](references/features-cupertino.md) |

### UI Components

| Topic | Description | Reference |
|-------|-------------|-----------|
| Dialogs & Modals | AlertDialog, showDialog, showModalBottomSheet | [features-dialogs](references/features-dialogs.md) |
| Focus Management | FocusNode, FocusScope, keyboard navigation | [features-focus](references/features-focus.md) |

### Platform Integration

| Topic | Description | Reference |
|-------|-------------|-----------|
| Platform Channels | MethodChannel, EventChannel, native communication | [features-platform-channels](references/features-platform-channels.md) |
| Platform Views | AndroidView, UiKitView, embedding native views | [features-platform-views](references/features-platform-views.md) |
| Assets & Resources | Asset management, pubspec.yaml, asset loading | [features-assets](references/features-assets.md) |
| HTTP & Networking | HTTP requests, API calls, JSON parsing | [features-http](references/features-http.md) |
| Responsive Design | MediaQuery, LayoutBuilder, screen adaptation | [features-responsive](references/features-responsive.md) |
| Keys | ValueKey, ObjectKey, GlobalKey, when to use keys | [features-keys](references/features-keys.md) |
| Widget Lifecycle | initState, dispose, lifecycle management | [features-lifecycle](references/features-lifecycle.md) |
| Error Handling | Try-catch, error widgets, error boundaries | [features-error-handling](references/features-error-handling.md) |
| PopScope | Handle back button and navigation pop events | [features-pop-scope](references/features-pop-scope.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Custom Paint | CustomPainter, Canvas, custom graphics | [advanced-custom-paint](references/advanced-custom-paint.md) |
| Gestures | GestureDetector, GestureRecognizer, drag and drop | [advanced-gestures](references/advanced-gestures.md) |
| Performance | Performance optimization, const constructors, keys | [advanced-performance](references/advanced-performance.md) |
| Testing | Widget testing, integration testing, test utilities | [advanced-testing](references/advanced-testing.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| State Management | When to use setState, state lifting, patterns | [best-practices-state](references/best-practices-state.md) |
| Performance | Optimization techniques, const usage, patterns | [best-practices-performance](references/best-practices-performance.md) |
