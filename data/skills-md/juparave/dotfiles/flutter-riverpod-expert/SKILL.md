---
name: flutter-riverpod-expert
description: Expert knowledge in Flutter Riverpod state management (2025 best practices). Use when working with Riverpod, Flutter state management, AsyncNotifier, provider types, code generation with riverpod_generator, state synchronization, or when the user mentions data fetching, mutations, reactive state, performance optimization, or testing in Flutter apps. Covers AsyncNotifierProvider patterns, repository architecture, autoDispose, family providers, and common anti-patterns to avoid.
---

# Flutter Riverpod Expert - 2025 Best Practices

You have expert knowledge in Flutter Riverpod state management following 2025 best practices. When the user is working with Riverpod or Flutter state management, apply these patterns and guidelines.

## When to Use This Skill

Activate this expertise when the user mentions:
- Riverpod, providers, state management, or StateNotifier
- AsyncNotifier, FutureProvider, StreamProvider, NotifierProvider
- Code generation with riverpod_generator or build_runner
- Data fetching, API integration, mutations, or reactive state
- State synchronization, caching, autoDispose, or memory management
- Provider testing, dependency injection, or repository patterns
- Performance issues with rebuilds, provider selection, or optimization
- Migration from old Riverpod patterns to modern approaches

## Core Principles (2025)

1. **Code Generation is STRONGLY RECOMMENDED** - Use `@riverpod` annotations and `riverpod_generator`
2. **AsyncNotifierProvider is PREFERRED** for async state (replaces FutureProvider/StreamProvider for consistency)
3. **AutoDispose by Default** - Codegen makes providers auto-dispose automatically
4. **Repository Pattern** - Separate data layer from state management
5. **Performance First** - Use `select()` to optimize rebuilds

## Provider Selection Guide

### Quick Decision Tree

**Immutable/Computed Values** - Use `Provider`:
```dart
@riverpod
String apiKey(Ref ref) => 'YOUR_API_KEY';

@riverpod
int totalPrice(Ref ref) {
  final cart = ref.watch(cartProvider);
  return cart.items.fold(0, (sum, item) => sum + item.price);
}
```

**Simple Synchronous State** - Use `NotifierProvider`:
```dart
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;

  void increment() => state++;
  void decrement() => state = max(0, state - 1);
}
```

**Async Data with Mutations (PREFERRED 2025)** - Use `AsyncNotifierProvider`:
```dart
@riverpod
class TodoList extends _$TodoList {
  @override
  Future<List<Todo>> build() async {
    final repo = ref.watch(todoRepositoryProvider);
    return repo.fetchTodos();
  }

  Future<void> addTodo(String title) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final repo = ref.read(todoRepositoryProvider);
      await repo.createTodo(title);
      return repo.fetchTodos();
    });
  }

  Future<void> deleteTodo(String id) async {
    // Optimistic update
    state = AsyncData(state.value!.where((t) => t.id != id).toList());

    try {
      await ref.read(todoRepositoryProvider).deleteTodo(id);
    } catch (e) {
      ref.invalidateSelf(); // Rollback on error
    }
  }
}
```

**Real-time Streams Only** - Use `StreamProvider`:
```dart
@riverpod
Stream<User?> authState(Ref ref) {
  return FirebaseAuth.instance.authStateChanges();
}
```

**Key Rule**: Prefer AsyncNotifierProvider over FutureProvider/StreamProvider for better consistency and mutation support.

## Code Generation Setup

### Dependencies (pubspec.yaml)
```yaml
dependencies:
  flutter_riverpod: ^2.5.0
  riverpod_annotation: ^2.3.0

dev_dependencies:
  build_runner: ^2.4.0
  riverpod_generator: ^2.4.0
  custom_lint: ^0.6.0
  riverpod_lint: ^2.3.0
```

### File Template
Every provider file needs:
```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'filename.g.dart';  // REQUIRED

@riverpod
class MyProvider extends _$MyProvider {
  @override
  Future<Data> build() async => fetchData();
}
```

### Run Generator
```bash
# Watch mode (RECOMMENDED during development)
dart run build_runner watch -d

# One-time generation
dart run build_runner build --delete-conflicting-outputs
```

## Performance Optimization Patterns

### Use ref.select() for Specific Fields
```dart
// ❌ BAD: Rebuilds on ANY product change
final product = ref.watch(productProvider);
return Text('\$${product.price}');

// ✅ GOOD: Only rebuilds when price changes
final price = ref.watch(productProvider.select((p) => p.price));
return Text('\$$price');
```

### ref.watch() vs ref.select() vs ref.read() vs ref.listen()

**ref.watch()** - Subscribe to changes (use in build):
```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  final todos = ref.watch(todoListProvider);
  return ListView(...);
}
```

**ref.select()** - Subscribe to specific property (optimize rebuilds):
```dart
final count = ref.watch(todoListProvider.select((todos) => todos.length));
final isAdult = ref.watch(personProvider.select((p) => p.age >= 18));
```

**ref.read()** - One-time read with NO subscription (event handlers only):
```dart
onPressed: () {
  ref.read(todoListProvider.notifier).addTodo('New task');
}

// ❌ NEVER use read() in build to "optimize" - it won't rebuild!
```

**ref.listen()** - Side effects (navigation, snackbars, logging):
```dart
ref.listen<AsyncValue<List<Todo>>>(
  todoListProvider,
  (previous, next) {
    next.whenOrNull(
      error: (error, stack) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $error')),
        );
      },
    );
  },
);
```

### Avoid Watching in Loops
```dart
// ❌ BAD: Causes performance issues
ListView.builder(
  itemBuilder: (context, index) {
    final todo = ref.watch(todoProvider(ids[index])); // DON'T!
    return ListTile(...);
  },
);

// ✅ GOOD: Separate widget for each item
class TodoItem extends ConsumerWidget {
  const TodoItem({required this.todoId});
  final String todoId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final todo = ref.watch(todoProvider(todoId));
    return ListTile(title: Text(todo.title));
  }
}

class TodoList extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final ids = ref.watch(todoIdsProvider);
    return ListView.builder(
      itemCount: ids.length,
      itemBuilder: (context, index) => TodoItem(todoId: ids[index]),
    );
  }
}
```

### Create Derived Providers
```dart
// ✅ GOOD: Separate provider for computed state
@riverpod
List<Todo> filteredSortedTodos(Ref ref) {
  final todos = ref.watch(todoListProvider);
  final filter = ref.watch(filterProvider);
  final sortOrder = ref.watch(sortOrderProvider);

  final filtered = todos.where((t) => t.matches(filter)).toList();
  return filtered..sort(sortOrder.comparator);
}
```

## Repository Pattern Architecture

### 3-Layer Architecture

**1. Data Layer - Repository**:
```dart
@riverpod
TodoRepository todoRepository(Ref ref) {
  return TodoRepository(dio: ref.watch(dioProvider));
}

class TodoRepository {
  TodoRepository({required this.dio});
  final Dio dio;

  Future<List<Todo>> fetchTodos() async {
    final response = await dio.get('/todos');
    return (response.data as List)
      .map((json) => Todo.fromJson(json))
      .toList();
  }

  Future<Todo> createTodo(String title) async {
    final response = await dio.post('/todos', data: {'title': title});
    return Todo.fromJson(response.data);
  }

  Future<void> deleteTodo(String id) async {
    await dio.delete('/todos/$id');
  }
}
```

**2. Application Layer - State Management**:
```dart
@riverpod
class TodoList extends _$TodoList {
  @override
  Future<List<Todo>> build() async {
    final repository = ref.watch(todoRepositoryProvider);
    return repository.fetchTodos();
  }

  Future<void> addTodo(String title) async {
    final repository = ref.read(todoRepositoryProvider);

    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      await repository.createTodo(title);
      return repository.fetchTodos();
    });
  }
}
```

**3. Presentation Layer - UI**:
```dart
class TodoListScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final todosAsync = ref.watch(todoListProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Todos')),
      body: todosAsync.when(
        data: (todos) => ListView.builder(
          itemCount: todos.length,
          itemBuilder: (context, index) => TodoTile(todos[index]),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => ErrorView(error: error),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddDialog(context, ref),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

### Dependency Injection
```dart
// Services
@riverpod
Dio dio(Ref ref) {
  final dio = Dio(BaseOptions(baseUrl: 'https://api.example.com'));
  dio.interceptors.add(LogInterceptor());
  return dio;
}

@riverpod
Future<SharedPreferences> sharedPreferences(Ref ref) async {
  return await SharedPreferences.getInstance();
}

@riverpod
AuthService authService(Ref ref) {
  return AuthService(
    dio: ref.watch(dioProvider),
    storage: ref.watch(sharedPreferencesProvider).value!,
  );
}

// Repositories depend on services
@riverpod
UserRepository userRepository(Ref ref) {
  return UserRepository(
    dio: ref.watch(dioProvider),
    authService: ref.watch(authServiceProvider),
  );
}

// State providers depend on repositories
@riverpod
class CurrentUser extends _$CurrentUser {
  @override
  Future<User?> build() async {
    final authService = ref.watch(authServiceProvider);
    final userId = await authService.getCurrentUserId();

    if (userId == null) return null;

    final repository = ref.watch(userRepositoryProvider);
    return repository.fetchUser(userId);
  }

  Future<void> logout() async {
    final authService = ref.read(authServiceProvider);
    await authService.logout();
    ref.invalidateSelf();
  }
}
```

## Family Providers (Parameterized)

Family providers are automatic with code generation when you add parameters:

```dart
// Simple family provider
@riverpod
Future<User> user(Ref ref, String id) async {
  final dio = ref.watch(dioProvider);
  final response = await dio.get('/users/$id');
  return User.fromJson(response.data);
}

// Usage
final user = ref.watch(userProvider('123'));

// Family with AsyncNotifier
@riverpod
class UserNotifier extends _$UserNotifier {
  @override
  Future<User> build(String id) async {
    final repo = ref.watch(userRepositoryProvider);
    return repo.fetchUser(id);
  }

  Future<void> updateName(String newName) async {
    final userId = arg; // Access the parameter via 'arg'
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      await ref.read(userRepositoryProvider).updateUser(userId, name: newName);
      return ref.read(userRepositoryProvider).fetchUser(userId);
    });
  }
}

// Complex parameters need proper equality
class UserFilter {
  const UserFilter({required this.role, required this.active});
  final String role;
  final bool active;

  @override
  bool operator ==(Object other) =>
    identical(this, other) ||
    other is UserFilter &&
    role == other.role &&
    active == other.active;

  @override
  int get hashCode => Object.hash(role, active);
}

@riverpod
Future<List<User>> filteredUsers(Ref ref, UserFilter filter) async {
  return fetchUsers(filter);
}
```

## AutoDispose and Caching

Code generation makes providers **auto-dispose by default**.

```dart
// Default: auto-dispose when no listeners
@riverpod
Future<String> data(Ref ref) async => fetchData();

// Keep alive permanently
@Riverpod(keepAlive: true)
Future<Config> config(Ref ref) async => loadConfig();

// Conditional keep alive - cache on success
@riverpod
Future<String> cachedData(Ref ref) async {
  final data = await fetchData();
  ref.keepAlive(); // Cache this result forever
  return data;
}

// Timed cache (5 minutes)
@riverpod
Future<String> timedCache(Ref ref) async {
  final data = await fetchData();
  final link = ref.keepAlive();
  Timer(const Duration(minutes: 5), link.close);
  return data;
}

// Manual disposal - cleanup resources
@riverpod
Stream<int> websocket(Ref ref) {
  final client = WebSocketClient();

  ref.onDispose(() {
    client.close(); // Cleanup when provider is disposed
  });

  return client.stream;
}
```

## Error Handling

### Comprehensive Error Handling
```dart
@riverpod
class TodoList extends _$TodoList {
  @override
  Future<List<Todo>> build() async {
    try {
      final repository = ref.watch(todoRepositoryProvider);
      return await repository.fetchTodos();
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        ref.read(authServiceProvider).logout();
        throw UnauthorizedException();
      }
      throw NetworkException(e.message);
    } catch (e) {
      throw UnexpectedException(e.toString());
    }
  }

  Future<void> addTodo(String title) async {
    state = const AsyncLoading();

    state = await AsyncValue.guard(() async {
      final repository = ref.read(todoRepositoryProvider);
      await repository.createTodo(title);
      return repository.fetchTodos();
    });
  }
}
```

### UI Error Handling
```dart
// Using .when()
todosAsync.when(
  data: (todos) => ListView.builder(...),
  loading: () => const Center(child: CircularProgressIndicator()),
  error: (error, stack) {
    if (error is NetworkException) {
      return ErrorView(
        message: 'Network error. Check your connection.',
        onRetry: () => ref.invalidate(todoListProvider),
      );
    }
    if (error is UnauthorizedException) {
      return const ErrorView(message: 'Please log in again.');
    }
    return ErrorView(message: 'Error: $error');
  },
);

// Listen for errors (side effects)
ref.listen<AsyncValue<List<Todo>>>(
  todoListProvider,
  (previous, next) {
    next.whenOrNull(
      error: (error, stack) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(error.toString()),
            backgroundColor: Colors.red,
          ),
        );
      },
    );
  },
);
```

## Testing

### Provider Testing
```dart
test('TodoList fetches todos correctly', () async {
  final container = ProviderContainer.test(
    overrides: [
      todoRepositoryProvider.overrideWithValue(MockTodoRepository()),
    ],
  );

  final todos = await container.read(todoListProvider.future);

  expect(todos.length, 2);
  expect(todos[0].title, 'Test Todo 1');
});

test('TodoList adds todo correctly', () async {
  final mockRepo = MockTodoRepository();
  final container = ProviderContainer.test(
    overrides: [
      todoRepositoryProvider.overrideWithValue(mockRepo),
    ],
  );

  await container.read(todoListProvider.notifier).addTodo('New Todo');

  verify(() => mockRepo.createTodo('New Todo')).called(1);
});
```

### Widget Testing
```dart
testWidgets('TodoListScreen displays todos', (tester) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: [
        todoRepositoryProvider.overrideWithValue(MockTodoRepository()),
      ],
      child: const MaterialApp(home: TodoListScreen()),
    ),
  );

  await tester.pumpAndSettle();

  expect(find.text('Test Todo 1'), findsOneWidget);
  expect(find.text('Test Todo 2'), findsOneWidget);
});
```

## Common Anti-Patterns to AVOID

### Performance Pitfalls
```dart
// ❌ Using ref.read() to avoid rebuilds
final todos = ref.read(todoListProvider); // Won't rebuild!

// ✅ Use ref.watch() or ref.select()
final count = ref.watch(todoListProvider.select((todos) => todos.length));
```

### Memory Leaks
```dart
// ❌ Not disposing resources
@riverpod
Stream<int> badWebsocket(Ref ref) {
  final client = WebSocketClient();
  return client.stream; // Never closed!
}

// ✅ Dispose resources
@riverpod
Stream<int> goodWebsocket(Ref ref) {
  final client = WebSocketClient();
  ref.onDispose(() => client.close());
  return client.stream;
}
```

### Multiple Sources of Truth
```dart
// ❌ BAD: Which is the source of truth?
class BadWidget extends StatefulWidget {
  int localCount = 0; // Local state

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final providerCount = ref.watch(counterProvider); // Provider state
    return Text('$localCount vs $providerCount'); // Confusing!
  }
}

// ✅ GOOD: Single source of truth
class GoodWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('$count');
  }
}
```

### Not Invalidating Dependent Providers
```dart
// ❌ BAD
Future<void> logout() async {
  state = null;
  // Other providers still have old user data!
}

// ✅ GOOD: Invalidate dependent providers
Future<void> logout() async {
  state = null;
  ref.invalidate(userProfileProvider);
  ref.invalidate(userSettingsProvider);
  ref.invalidate(userNotificationsProvider);
}

// ✅ EVEN BETTER: Make providers watch auth
@riverpod
Future<UserProfile> userProfile(Ref ref) async {
  final user = ref.watch(authProvider);
  if (user == null) throw UnauthenticatedException();
  return fetchUserProfile(user.id); // Auto-refetches when user changes
}
```

## Instructions for Use

When the user is working with Riverpod:

1. **Always recommend code generation** with `@riverpod` annotations
2. **Prefer AsyncNotifierProvider** over FutureProvider/StreamProvider for async state
3. **Optimize performance** by suggesting `select()` when watching specific fields
4. **Follow repository pattern** for clean architecture
5. **Use proper error handling** with AsyncValue.guard() and .when()
6. **Remind about autoDispose** and caching strategies
7. **Point out anti-patterns** if you see them in user code
8. **Provide complete, working examples** with proper imports

## Reference

For complete details and advanced patterns, refer to:
`/Users/pablito/EVOworkspace/flutter/CesarferPromotoresFlutter/promotores/RIVERPOD_2025_BEST_PRACTICES.md`
