---
name: flutter-development
description: Build cross-platform mobile apps with Flutter and Dart. Use when creating mobile applications, working with Flutter projects, designing UIs with widgets, implementing state management (Provider/BLoC), handling navigation, or when user mentions Flutter, Dart, mobile app development, iOS/Android apps, or Material Design.
---

# Flutter Development

Build beautiful, natively compiled applications for mobile, web, and desktop from a single codebase using Flutter and Dart.

## When to use this Skill

Use this Skill when:
- Creating new Flutter applications
- Working with Flutter widgets and UI components
- Implementing state management (Provider, BLoC, Riverpod)
- Setting up navigation and routing
- Integrating APIs and HTTP requests
- Debugging Flutter applications
- Following Flutter best practices
- User mentions Flutter, Dart, mobile apps, iOS, Android, or cross-platform development

## Project structure

Standard Flutter project:
```
my_flutter_app/
├── lib/
│   ├── main.dart           # App entry point
│   ├── screens/            # Screen widgets
│   ├── widgets/            # Reusable widgets
│   ├── models/             # Data models
│   ├── services/           # API, database services
│   └── providers/          # State management
├── pubspec.yaml            # Dependencies and assets
├── test/                   # Unit and widget tests
└── assets/                 # Images, fonts, etc.
```

## Common Flutter commands

### Create new project
```bash
flutter create my_app
cd my_app
```

### Run application
```bash
flutter run              # Default device
flutter run -d chrome    # Web
flutter run -d linux     # Linux desktop
flutter run -d android   # Android device/emulator
```

### Manage dependencies
```bash
flutter pub add package_name    # Add dependency
flutter pub get                 # Install dependencies
flutter pub upgrade            # Update dependencies
```

### Testing and building
```bash
flutter test                   # Run tests
flutter analyze               # Static analysis
flutter build apk             # Android APK
flutter build ios             # iOS build
flutter build web             # Web build
```

## Basic Flutter app template

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: const Center(
        child: Text('Hello, Flutter!'),
      ),
    );
  }
}
```

## State management with Provider

Install Provider:
```bash
flutter pub add provider
```

Example usage:

```dart
// 1. Create a ChangeNotifier model
class Counter extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }
}

// 2. Wrap app with ChangeNotifierProvider
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => Counter(),
      child: const MyApp(),
    ),
  );
}

// 3. Access in widgets
class CounterDisplay extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final counter = context.watch<Counter>();
    return Text('Count: ${counter.count}');
  }
}

// 4. Trigger updates
ElevatedButton(
  onPressed: () => context.read<Counter>().increment(),
  child: const Text('Increment'),
)
```

## Navigation

### Basic navigation
```dart
// Navigate to new screen
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => const SecondScreen()),
);

// Navigate back
Navigator.pop(context);

// Navigate with data
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => DetailScreen(data: myData),
  ),
);
```

### GoRouter (recommended for complex apps)
```bash
flutter pub add go_router
```

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/details/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return DetailScreen(id: id);
      },
    ),
  ],
);

// Use in app
MaterialApp.router(
  routerConfig: router,
)

// Navigate
context.go('/details/123');
```

## HTTP requests

Install http package:
```bash
flutter pub add http
```

Example:
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<List<User>> fetchUsers() async {
  final response = await http.get(
    Uri.parse('https://api.example.com/users'),
  );

  if (response.statusCode == 200) {
    final List<dynamic> data = json.decode(response.body);
    return data.map((json) => User.fromJson(json)).toList();
  } else {
    throw Exception('Failed to load users');
  }
}

// Use with FutureBuilder
FutureBuilder<List<User>>(
  future: fetchUsers(),
  builder: (context, snapshot) {
    if (snapshot.hasData) {
      return ListView.builder(
        itemCount: snapshot.data!.length,
        itemBuilder: (context, index) {
          return ListTile(title: Text(snapshot.data![index].name));
        },
      );
    } else if (snapshot.hasError) {
      return Text('Error: ${snapshot.error}');
    }
    return const CircularProgressIndicator();
  },
)
```

## Essential widgets

### Layout widgets
- **Container** - Box model with padding, margin, decoration
- **Column** - Vertical layout
- **Row** - Horizontal layout
- **Stack** - Layered widgets
- **Expanded** - Fills available space
- **Padding** - Adds padding around widget
- **Center** - Centers child widget
- **SizedBox** - Fixed size box or spacer

### Input widgets
- **TextField** - Text input
- **Form** - Group input fields with validation
- **Checkbox** - Boolean selection
- **Radio** - Single choice from options
- **Switch** - Toggle on/off
- **Slider** - Select value from range
- **DropdownButton** - Select from dropdown

### Display widgets
- **Text** - Display text with styling
- **Image** - Display images (network, asset, file)
- **Icon** - Material or custom icons
- **Card** - Material Design card
- **ListTile** - Standard list item

### Interactive widgets
- **ElevatedButton** - Raised button with elevation
- **TextButton** - Flat text button
- **IconButton** - Button with icon
- **FloatingActionButton** - Floating action button
- **GestureDetector** - Detect gestures (tap, swipe, etc.)
- **InkWell** - Touch feedback with ripple

### Async widgets
- **FutureBuilder** - Build based on Future
- **StreamBuilder** - Build based on Stream

## Best practices

### DO:
✅ Use `const` constructors wherever possible for better performance
✅ Implement proper dispose() methods to prevent memory leaks
✅ Extract widgets into separate classes for reusability
✅ Use meaningful, descriptive widget names
✅ Separate business logic from UI (use services/providers)
✅ Handle errors comprehensively with try-catch
✅ Test on both iOS and Android platforms
✅ Use responsive design (MediaQuery, LayoutBuilder)
✅ Follow Dart naming conventions (lowerCamelCase for variables, UpperCamelCase for classes)
✅ Add comments for complex logic

### DON'T:
❌ Hardcode values (use constants or configuration)
❌ Use complex setState logic (prefer state management solutions)
❌ Make network calls in build() methods
❌ Skip testing phases
❌ Ignore platform-specific differences
❌ Create deeply nested widget trees (extract to methods/classes)
❌ Store heavy objects in state unnecessarily
❌ Forget to add loading and error states

## Common patterns

### Stateless vs Stateful widgets
- **StatelessWidget**: UI doesn't change, no mutable state
- **StatefulWidget**: UI changes based on state updates

### Lifting state up
Move state to common ancestor when multiple widgets need access:
```dart
class Parent extends StatefulWidget {
  @override
  State<Parent> createState() => _ParentState();
}

class _ParentState extends State<Parent> {
  int _count = 0;

  void _increment() => setState(() => _count++);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ChildA(count: _count),
        ChildB(onPressed: _increment),
      ],
    );
  }
}
```

### Responsive design
```dart
Widget build(BuildContext context) {
  final size = MediaQuery.of(context).size;
  final isLargeScreen = size.width > 600;

  return isLargeScreen
      ? Row(children: [...])  // Tablet/Desktop layout
      : Column(children: [...]);  // Mobile layout
}
```

## Debugging tips

1. **Hot reload**: Press `r` in terminal or save file (for quick UI updates)
2. **Hot restart**: Press `R` in terminal (for state reset)
3. **Flutter DevTools**: Run `flutter pub global activate devtools` then `flutter pub global run devtools`
4. **Debug print**: Use `debugPrint()` instead of `print()`
5. **Widget inspector**: Enable in DevTools to inspect widget tree
6. **Performance overlay**: `flutter run --profile` for performance metrics

## Instructions for Claude

When helping with Flutter development:

1. **Always check Flutter installation** before creating projects
2. **Create proper project structure** following Flutter conventions
3. **Use Material Design 3** (`useMaterial3: true`) for modern UI
4. **Implement responsive design** considering different screen sizes
5. **Add proper error handling** and loading states
6. **Use const constructors** wherever possible
7. **Follow Dart naming conventions** throughout the code
8. **Add helpful comments** for complex logic
9. **Suggest appropriate state management** based on app complexity
10. **Test code structure** before suggesting advanced features
11. **Provide both code and explanations** for learning
12. **Include pubspec.yaml changes** when adding dependencies

## Common issues and solutions

### Issue: "Waiting for another flutter command to release the startup lock"
Solution: Delete `flutter.lock` file or restart terminal

### Issue: "Gradle build failed"
Solution: Run `flutter clean` then `flutter pub get`

### Issue: "setState called during build"
Solution: Move setState calls to lifecycle methods or use Future.microtask

### Issue: "RenderBox overflow"
Solution: Wrap content in SingleChildScrollView or use Flexible/Expanded widgets

### Issue: Hot reload not working
Solution: Use hot restart (R) or restart app completely
