---
name: flutter
description: >
  Flutter and Dart best practices for mobile development.
  Trigger: When building Flutter/Dart mobile applications.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with flutter"

## When to Use

Use this skill when:
- Building Flutter mobile applications
- Writing Dart code
- Managing widget state
- Implementing cross-platform UI

---

## Critical Patterns

### Widget Structure (REQUIRED)

```dart
// ✅ ALWAYS: Prefer StatelessWidget when possible
class UserCard extends StatelessWidget {
  final User user;
  
  const UserCard({super.key, required this.user});
  
  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(user.name),
        subtitle: Text(user.email),
      ),
    );
  }
}
```

### State Management (REQUIRED)

```dart
// ✅ Use Riverpod for state management
final userProvider = FutureProvider<User>((ref) async {
  return await api.getUser();
});

// In widget
Consumer(
  builder: (context, ref, child) {
    final userAsync = ref.watch(userProvider);
    return userAsync.when(
      data: (user) => Text(user.name),
      loading: () => CircularProgressIndicator(),
      error: (e, s) => Text('Error: $e'),
    );
  },
)
```

### Null Safety (REQUIRED)

```dart
// ✅ ALWAYS: Use null safety properly
String? nullableName;
String nonNullName = nullableName ?? 'Default';

// Use late for lazy initialization
late final UserService userService;
```

---

## Decision Tree

```
Need simple UI?            → StatelessWidget
Need local state?          → StatefulWidget
Need shared state?         → Provider/Riverpod
Need navigation?           → GoRouter
Need forms?                → Form + TextFormField
```

---

## Commands

```bash
flutter create myapp
flutter run
flutter build apk
flutter build ios
flutter test
flutter analyze
```
