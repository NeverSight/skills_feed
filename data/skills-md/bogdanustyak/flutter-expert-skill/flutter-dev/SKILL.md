---
name: flutter-dev
description: Expert Flutter and Dart development skill for building beautiful, performant, and maintainable applications. Use when users request Flutter/Dart development tasks including creating apps, widgets, screens, implementing features, debugging, testing, state management, navigation, theming, layouts, or working with Flutter projects. Covers mobile, web, and desktop platforms with modern best practices, Material Design, responsive UI, and code quality standards.
---

# Flutter Development Expert

Expert guidance for Flutter and Dart development following official Flutter team best practices.

## Core Development Principles

### Code Philosophy
- Apply SOLID principles throughout the codebase
- Write concise, modern, technical Dart code with functional and declarative patterns
- Favor composition over inheritance for building complex widgets and logic
- Prefer immutable data structures, especially for widgets (use `StatelessWidget` when possible)
- Separate ephemeral state from app state using appropriate state management
- Keep functions short with single purpose (strive for less than 20 lines)
- Use meaningful, descriptive names - avoid abbreviations

### Project Structure Assumptions
- Standard Flutter project structure with `lib/main.dart` as entry point
- Organize by logical layers: Presentation (widgets/screens), Domain (business logic), Data (models/API clients), Core (utilities/extensions)
- For larger projects: organize by feature with presentation/domain/data subfolders per feature

## Interaction Guidelines

When generating code:
- Provide explanations for Dart-specific features (null safety, futures, streams)
- If request is ambiguous, ask for clarification on functionality and target platform
- When suggesting new dependencies from pub.dev, explain their benefits
- Use `dart format` tool for consistent formatting
- Use `dart fix` tool to automatically fix common errors
- Use the Dart linter with recommended rules to catch issues

## Code Quality Standards

### Styling Rules
- Line length: 80 characters or fewer
- Naming conventions:
  - `PascalCase` for classes
  - `camelCase` for members/variables/functions/enums
  - `snake_case` for files
- No trailing comments
- Use arrow syntax for simple one-line functions

### Error Handling
- Anticipate and handle potential errors - never fail silently
- Use `try-catch` blocks with appropriate exception types
- Use custom exceptions for code-specific situations
- Proper `async`/`await` usage with robust error handling

### Documentation
- Add `dartdoc` comments to all public APIs (classes, constructors, methods, top-level functions)
- Write clear comments for complex/non-obvious code
- Use `///` for doc comments
- Start with single-sentence summary ending with period
- Comment why code is written a certain way, not what it does

## Dart Best Practices

### Type System & Null Safety
- Write soundly null-safe code
- Leverage Dart's null safety features
- Avoid `!` operator unless value is guaranteed non-null
- Use pattern matching features where they simplify code
- Use records to return multiple types when defining a class is cumbersome
- Prefer exhaustive `switch` statements/expressions (no `break` needed)

### Async Programming
- Use `Future`s, `async`, `await` for single asynchronous operations
- Use `Stream`s for sequences of asynchronous events
- Ensure proper error handling in async operations

### Class & Library Organization
- Define related classes within the same library file
- For large libraries: export smaller private libraries from single top-level library
- Group related libraries in same folder

## Flutter Best Practices

### Widget Design
- Widgets (especially `StatelessWidget`) are immutable
- When UI needs to change, Flutter rebuilds widget tree
- Prefer composing smaller widgets over extending existing ones
- Use small, private `Widget` classes instead of private helper methods returning widgets
- Break down large `build()` methods into smaller, reusable private Widget classes
- Use `const` constructors whenever possible to reduce rebuilds

### Performance Optimization
- Use `ListView.builder` or `SliverList` for long lists (lazy-loaded)
- Use `compute()` to run expensive calculations in separate isolate (e.g., JSON parsing)
- Avoid expensive operations (network calls, complex computations) in `build()` methods
- Use `const` constructors in `build()` methods to minimize rebuilds

### Responsive Design
- Use `LayoutBuilder` or `MediaQuery` for responsive UIs
- Ensure mobile responsive design across different screen sizes
- Test on mobile and web platforms

## State Management

Prefer Flutter's built-in solutions unless third-party explicitly requested:

### Built-in Solutions (in order of simplicity)
1. **ValueNotifier + ValueListenableBuilder** - Simple, local state with single value
```dart
final ValueNotifier<int> _counter = ValueNotifier<int>(0);

ValueListenableBuilder<int>(
  valueListenable: _counter,
  builder: (context, value, child) => Text('Count: $value'),
);
```

2. **ChangeNotifier + ListenableBuilder** - Complex/shared state across widgets
```dart
class CounterModel extends ChangeNotifier {
  int _count = 0;
  int get count => _count;
  void increment() {
    _count++;
    notifyListeners();
  }
}

ListenableBuilder(
  listenable: counterModel,
  builder: (context, child) => Text('${counterModel.count}'),
);
```

3. **Streams + StreamBuilder** - Sequences of asynchronous events
4. **Futures + FutureBuilder** - Single async operations

### Advanced Patterns
- **MVVM**: Model-View-ViewModel pattern for robust applications
- **Dependency Injection**: Use manual constructor injection for explicit dependencies
- **Provider**: Only if explicitly requested for DI beyond manual injection

## Navigation

### GoRouter (Recommended)
Use `go_router` for declarative navigation, deep linking, and web support:

```dart
// Add dependency
flutter pub add go_router

// Configure router
final GoRouter _router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) {
            final String id = state.pathParameters['id']!;
            return DetailScreen(id: id);
          },
        ),
      ],
    ),
  ],
);

// Use in MaterialApp
MaterialApp.router(routerConfig: _router);
```

- Configure `redirect` property for authentication flows
- Use for deep-linkable routes

### Navigator (Built-in)
Use for short-lived screens not needing deep links (dialogs, temporary views):

```dart
Navigator.push(context, MaterialPageRoute(builder: (context) => DetailsScreen()));
Navigator.pop(context);
```

## Package Management

### Using pub Tool
- Add dependency: `flutter pub add <package_name>`
- Add dev dependency: `flutter pub add dev:<package_name>`
- Add override: `flutter pub add override:<package_name>:1.0.0`
- Remove dependency: `dart pub remove <package_name>`

### External Packages
- Search pub.dev for suitable, stable packages
- Explain benefits when suggesting new dependencies

## Data Handling

### JSON Serialization
Use `json_serializable` and `json_annotation`:

```dart
import 'package:json_annotation/json_annotation.dart';
part 'user.g.dart';

@JsonSerializable(fieldRename: FieldRename.snake)
class User {
  final String firstName;
  final String lastName;
  
  User({required this.firstName, required this.lastName});
  
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

### Code Generation
- Ensure `build_runner` is dev dependency
- Run after modifications: `dart run build_runner build --delete-conflicting-outputs`

## Logging

Use `dart:developer` for structured logging:

```dart
import 'dart:developer' as developer;

// Simple messages
developer.log('User logged in successfully.');

// Structured error logging
try {
  // code
} catch (e, s) {
  developer.log(
    'Failed to fetch data',
    name: 'myapp.network',
    level: 1000, // SEVERE
    error: e,
    stackTrace: s,
  );
}
```

## UI & Theming

### Material Design 3 & ThemeData
Use `ColorScheme.fromSeed()` for harmonious palettes:

```dart
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.deepPurple,
      brightness: Brightness.light,
    ),
    textTheme: TextTheme(
      displayLarge: TextStyle(fontSize: 57, fontWeight: FontWeight.bold),
      bodyMedium: TextStyle(fontSize: 14, height: 1.4),
    ),
  ),
  darkTheme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.deepPurple,
      brightness: Brightness.dark,
    ),
  ),
  themeMode: ThemeMode.system,
);
```

### Custom Theme Extensions
For custom design tokens beyond standard ThemeData:

```dart
@immutable
class MyColors extends ThemeExtension<MyColors> {
  const MyColors({required this.success, required this.danger});
  final Color? success;
  final Color? danger;
  
  @override
  ThemeExtension<MyColors> copyWith({Color? success, Color? danger}) {
    return MyColors(success: success ?? this.success, danger: danger ?? this.danger);
  }
  
  @override
  ThemeExtension<MyColors> lerp(ThemeExtension<MyColors>? other, double t) {
    if (other is! MyColors) return this;
    return MyColors(
      success: Color.lerp(success, other.success, t),
      danger: Color.lerp(danger, other.danger, t),
    );
  }
}

// Register in ThemeData
theme: ThemeData(
  extensions: [MyColors(success: Colors.green, danger: Colors.red)],
),

// Use in widgets
Container(color: Theme.of(context).extension<MyColors>()!.success)
```

### Fonts
Use `google_fonts` package for custom fonts:

```dart
flutter pub add google_fonts

final TextTheme appTextTheme = TextTheme(
  displayLarge: GoogleFonts.oswald(fontSize: 57, fontWeight: FontWeight.bold),
  titleLarge: GoogleFonts.roboto(fontSize: 22, fontWeight: FontWeight.w500),
  bodyMedium: GoogleFonts.openSans(fontSize: 14),
);
```

### Images & Assets
Declare in `pubspec.yaml`:
```yaml
flutter:
  uses-material-design: true
  assets:
    - assets/images/
```

```dart
// Local images
Image.asset('assets/images/placeholder.png')

// Network images (always include error handling)
Image.network(
  'https://example.com/image.png',
  loadingBuilder: (context, child, progress) {
    if (progress == null) return child;
    return Center(child: CircularProgressIndicator());
  },
  errorBuilder: (context, error, stackTrace) => Icon(Icons.error),
)
```

## Layout Best Practices

### Flexible Layouts
- **Expanded**: Fill remaining space in Row/Column
- **Flexible**: Shrink to fit (don't combine with Expanded)
- **Wrap**: Auto-wrap to next line on overflow
- **SingleChildScrollView**: For fixed-size content larger than viewport
- **ListView.builder/GridView.builder**: For long lists (lazy loading)
- **FittedBox**: Scale/fit single child within parent
- **LayoutBuilder**: Responsive layouts based on available space

### Stack Layouts
- **Positioned**: Precisely place child by anchoring to edges
- **Align**: Position using alignments (e.g., Alignment.center)

### Overlays
Use `OverlayPortal` for UI elements on top of everything:

```dart
final _controller = OverlayPortalController();

OverlayPortal(
  controller: _controller,
  overlayChildBuilder: (context) => Positioned(
    top: 50,
    left: 10,
    child: Card(child: Text('Overlay content')),
  ),
  child: ElevatedButton(
    onPressed: _controller.toggle,
    child: Text('Toggle'),
  ),
)
```

## Visual Design Principles

### Design Guidelines
- Build beautiful, intuitive UIs following modern design
- Ensure responsive across screen sizes (mobile & web)
- Provide intuitive navigation
- Use typography hierarchy (hero text, headlines, keywords)
- Apply subtle background textures for premium feel
- Use multi-layered shadows for depth
- Incorporate icons for enhanced understanding
- Interactive elements have shadows with color glow effects

### Color Guidelines
- **60-30-10 Rule**: 60% primary/neutral, 30% secondary, 10% accent
- **Contrast Ratios** (WCAG 2.1):
  - Normal text: 4.5:1 minimum
  - Large text (18pt or 14pt bold): 3:1 minimum
- Avoid complementary colors for text/background (causes eye strain)
- Use complementary colors sparingly for accents

### Typography
- Limit to 1-2 font families
- Prioritize legibility (sans-serif for UI body text)
- Line height: 1.4x-1.6x font size
- Line length: 45-75 characters for body text
- Avoid all caps for long-form text

## Testing

### Test Types
- **Unit Tests**: `package:test` for domain logic, data layer, state management
- **Widget Tests**: `package:flutter_test` for UI components
- **Integration Tests**: `package:integration_test` for end-to-end flows

### Testing Best Practices
- Follow Arrange-Act-Assert (Given-When-Then) pattern
- Prefer `package:checks` for more expressive assertions
- Prefer fakes/stubs over mocks
- If mocks necessary: use `mockito` or `mocktail`
- Aim for high test coverage
- Write testable code: use `file`, `process`, `platform` packages for dependency injection

### Running Tests
```bash
flutter test
```

## Accessibility (A11y)

- **Color Contrast**: Text minimum 4.5:1 ratio against background
- **Dynamic Text Scaling**: Test UI with increased system font size
- **Semantic Labels**: Use `Semantics` widget for clear, descriptive labels
- **Screen Reader Testing**: Test with TalkBack (Android) and VoiceOver (iOS)

## Analysis & Linting

Include in `analysis_options.yaml`:
```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    # Add additional lint rules here
```

## Additional Resources

For detailed patterns and examples, see:
- `references/navigation_patterns.md` - Advanced navigation patterns with GoRouter
- `references/state_patterns.md` - Comprehensive state management examples
- `references/theme_patterns.md` - Advanced theming and styling patterns
