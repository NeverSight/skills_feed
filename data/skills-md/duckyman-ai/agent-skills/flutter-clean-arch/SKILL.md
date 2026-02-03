---
name: flutter-clean-arch
description: Generate Flutter applications using Clean Architecture with feature-first structure, Riverpod state management, Dio + Retrofit for networking, and fpdart error handling. Use this skill when creating Flutter apps, implementing features with clean architecture patterns, setting up Riverpod providers, handling data with Either type for functional error handling, making HTTP requests with type-safe API clients, or structuring projects with domain/data/presentation layers. Triggers include "Flutter app", "clean architecture", "Riverpod", "feature-first", "state management", "API client", "Retrofit", "Dio", "REST API", or requests to build Flutter features with separation of concerns.
---

# Flutter Clean Architecture Skill

Generate Flutter applications following Clean Architecture principles with feature-first organization, Riverpod for state management, and functional error handling using fpdart.

Includes **Dio + Retrofit** for type-safe REST API calls.

## Core Principles

**Architecture**: Clean Architecture (Feature-First)
- Domain layer: Pure business logic, no dependencies
- Data layer: Data sources, repositories implementation, data models
- Presentation layer: UI, state management, view models

**Dependency Rule**: Presentation → Domain ← Data (Domain has no external dependencies)

**State Management**: Riverpod 3.0+ with code generation

> **Note: Riverpod 3.0+ & Freezed 3.0+ Required**
>
> **Riverpod 3.0+**: The `XxxRef` types (like `DioRef`, `UserRepositoryRef`, etc.) have been **removed** in favor of a unified `Ref` type.
>
> **Riverpod 2.x (Legacy)**:
> ```dart
> @riverpod
> SomeType someType(SomeTypeRef ref) { ... }
> ```
>
> **Riverpod 3.x+ (Current)**:
> ```dart
> @riverpod
> SomeType someType(Ref ref) { ... }
> ```
>
> **Freezed 3.0+**: Requires `sealed` keyword for union types with Dart 3.3.
>
> **Freezed 2.x (Legacy)**:
> ```dart
> @freezed
> class Failure with _$Failure { ... }
> ```
>
> **Freezed 3.x+ (Current)**:
> ```dart
> @freezed
> sealed class Failure with _$Failure { ... }
> ```
>
> **Required versions**: This skill requires Riverpod 3.0+ and Freezed 3.0+. Check your version with `flutter pub deps | grep riverpod`.

**Error Handling**: fpdart's Either<Failure, T> for functional error handling

**Networking**: Dio + Retrofit for type-safe REST API calls

## Project Structure

```
lib/
├── core/
│   ├── constants/
│   │   ├── api_constants.dart
│   ├── errors/
│   │   ├── failures.dart
│   │   └── network_exceptions.dart
│   ├── network/
│   │   ├── dio_provider.dart
│   │   └── interceptors/
│   │       ├── auth_interceptor.dart
│   │       ├── logging_interceptor.dart
│   │       └── error_interceptor.dart
│   ├── storage/
│   ├── services/
│   ├── router/
│   │   └── app_router.dart
│   └── utils/
├── shared/ 
├── features/
│   └── [feature_name]/
│       ├── data/
│       │   ├── models/
│       │   │   └── [entity]_model.dart
│       │   ├── datasources/
│       │   │   └── [feature]_api_service.dart
│       │   └── repositories/
│       │       └── [feature]_repository_impl.dart
│       ├── domain/
│       │   ├── entities/
│       │   ├── repositories/
│       │   │   └── [feature]_repository.dart
│       │   └── usecases/
│       │       └── [action]_usecase.dart
│       └── presentation/
│           ├── providers/
│           │   └── [feature]_provider.dart
│           ├── screens/
│           │   └── [feature]_screen.dart
│           └── widgets/
│               └── [feature]_widget.dart
└── main.dart
```

## Quick Start

### 1. Domain Layer (Entities, Repository Interfaces, UseCases)

```dart
// Entity
@freezed
sealed class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
  }) = _User;
}

// Repository Interface
abstract class UserRepository {
  Future<Either<Failure, User>> getUser(String id);
}

// UseCase
class GetUser {
  final UserRepository repository;
  GetUser(this.repository);
  Future<Either<Failure, User>> call(String id) => repository.getUser(id);
}
```

### 2. Data Layer (Models, API Service, Repository Implementation)

```dart
// Model with JSON serialization
@freezed
sealed class UserModel with _$UserModel {
  const UserModel._();
  const factory UserModel({
    required String id,
    required String name,
    required String email,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) => _$UserModelFromJson(json);

  User toEntity() => User(id: id, name: name, email: email);
}

// Retrofit API Service
@RestApi()
abstract class UserApiService {
  factory UserApiService(Dio dio) = _UserApiService;

  @GET('/users/{id}')
  Future<UserModel> getUser(@Path('id') String id);
}

// Repository Implementation
class UserRepositoryImpl implements UserRepository {
  final UserApiService apiService;

  @override
  Future<Either<Failure, User>> getUser(String id) async {
    try {
      final userModel = await apiService.getUser(id);
      return Right(userModel.toEntity());
    } on DioException catch (e) {
      return Left(Failure.network(NetworkExceptions.fromDioError(e).message));
    }
  }
}
```

### 3. Presentation Layer (Providers, Screens)

```dart
// Provider
@riverpod
UserApiService userApiService(Ref ref) {
  return UserApiService(ref.watch(dioProvider));
}

@riverpod
UserRepositoryImpl userRepository(Ref ref) {
  return UserRepositoryImpl(ref.watch(userApiServiceProvider));
}

@riverpod
class UserNotifier extends _$UserNotifier {
  @override
  FutureOr<User?> build() => null;

  Future<void> fetchUser(String id) async {
    state = const AsyncLoading();
    final result = await ref.read(userRepositoryProvider).getUser(id);
    state = result.fold(
      (failure) => AsyncError(failure, StackTrace.current),
      (user) => AsyncData(user),
    );
  }
}

// Screen
class UserScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userState = ref.watch(userNotifierProvider);

    return Scaffold(
      body: userState.when(
        data: (user) => Text('Hello ${user?.name}'),
        loading: () => const CircularProgressIndicator(),
        error: (e, _) => Text('Error: $e'),
      ),
    );
  }
}
```

## Code Generation

```bash
# Generate all files
dart run build_runner build --delete-conflicting-outputs

# Watch mode
dart run build_runner watch --delete-conflicting-outputs
```

## Best Practices

**DO**:
- Keep domain entities pure (no external dependencies)
- Use freezed with `sealed` keyword for immutable data classes
- Handle all error cases with Either<Failure, T>
- Use riverpod_generator with unified `Ref` type
- Separate models (data) from entities (domain)
- Place business logic in use cases, not in widgets
- Use Retrofit for type-safe API calls
- Handle DioException in repositories with NetworkExceptions
- Use interceptors for cross-cutting concerns (auth, logging)

**DON'T**:
- Import Flutter/HTTP libraries in domain layer
- Mix presentation logic with business logic
- Use try-catch directly in widgets when using Either
- Create god objects or god providers
- Skip the repository pattern
- Use legacy `XxxRef` types in new code

## Common Issues

| Issue | Solution |
|-------|----------|
| Build runner conflicts | `dart run build_runner clean && dart run build_runner build --delete-conflicting-outputs` |
| Provider not found | Ensure generated files are imported and run build_runner |
| Either not unwrapping | Use `fold()`, `match()`, or `getOrElse()` to extract values |
| `XxxRef` not found | Use unified `Ref` type instead (Riverpod 3.x+) |
| `sealed` keyword error | Upgrade to Dart 3.3+ and Freezed 3.0+ |

## Knowledge References

**Primary Libraries** (used in this skill):
- **Flutter 3.19+**: Latest framework features
- **Dart 3.3+**: Language features (patterns, records, `sealed` modifier)
- **Riverpod 3.0+**: State management with unified `Ref` type
- **Dio 5.9+**: HTTP client with interceptors
- **Retrofit 4.9+**: Type-safe REST API code generation
- **freezed 3.0+**: Immutable data classes with code generation
- **json_serializable 6.x**: JSON serialization
- **go_router 14.x+**: Declarative routing
- **fpdart**: Functional error handling with Either type

## References

- **[quick_start.md](references/quick_start.md)** - Step-by-step feature creation workflow
- **[data_layer.md](references/data_layer.md)** - Models, Retrofit API services, Repositories
- **[presentation_layer.md](references/presentation_layer.md)** - Providers, Screens, Widgets patterns
- **[network_setup.md](references/network_setup.md)** - Dio provider, Interceptors, Network exceptions
- **[error_handling.md](references/error_handling.md)** - Either patterns, Failure types, Error strategies
- **[retrofit_patterns.md](references/retrofit_patterns.md)** - Complete Retrofit API request patterns