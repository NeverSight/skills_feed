---
name: android-development
description: Create production-quality Android applications following Google's official architecture guidance and NowInAndroid best practices. Use when building Android apps with Kotlin, Jetpack Compose, MVVM architecture, Hilt dependency injection, Room database, or multi-module projects. Triggers on requests to create Android projects, screens, ViewModels, repositories, feature modules, or when asked about Android architecture patterns.
---

# Android Development

Build Android applications following Google's official architecture guidance, as demonstrated in the NowInAndroid reference app.

## Quick Reference

| Task | Reference File |
|------|----------------|
| Project structure & modules | [modularization.md](references/modularization.md) |
| Architecture layers (UI, Domain, Data) | [architecture.md](references/architecture.md) |
| Jetpack Compose patterns | [compose-patterns.md](references/compose-patterns.md) |
| Gradle & build configuration | [gradle-setup.md](references/gradle-setup.md) |
| Testing approach | [testing.md](references/testing.md) |

## Workflow Decision Tree

**Creating a new project?**
→ Read [modularization.md](references/modularization.md) for project structure
→ Use templates in `assets/templates/`

**Adding a new feature?**
→ Create feature module with `api` and `impl` submodules
→ Follow patterns in [architecture.md](references/architecture.md)

**Building UI screens?**
→ Read [compose-patterns.md](references/compose-patterns.md)
→ Create Screen + ViewModel + UiState

**Setting up data layer?**
→ Read data layer section in [architecture.md](references/architecture.md)
→ Create Repository + DataSource + DAO

## Core Principles

1. **Offline-first**: Local database is source of truth, sync with remote
2. **Unidirectional data flow**: Events flow down, data flows up
3. **Reactive streams**: Use Kotlin Flow for all data exposure
4. **Modular by feature**: Each feature is self-contained with clear boundaries
5. **Testable by design**: Use interfaces and test doubles, no mocking libraries

## Architecture Layers

```
┌─────────────────────────────────────────┐
│              UI Layer                    │
│  (Compose Screens + ViewModels)          │
├─────────────────────────────────────────┤
│           Domain Layer                   │
│  (Use Cases - optional, for reuse)       │
├─────────────────────────────────────────┤
│            Data Layer                    │
│  (Repositories + DataSources)            │
└─────────────────────────────────────────┘
```

## Module Types

```
app/                    # App module - navigation, scaffolding
feature/
  ├── featurename/
  │   ├── api/          # Navigation keys (public)
  │   └── impl/         # Screen, ViewModel, DI (internal)
core/
  ├── data/             # Repositories
  ├── database/         # Room DAOs, entities
  ├── network/          # Retrofit, API models
  ├── model/            # Domain models (pure Kotlin)
  ├── common/           # Shared utilities
  ├── ui/               # Reusable Compose components
  ├── designsystem/     # Theme, icons, base components
  ├── datastore/        # Preferences storage
  └── testing/          # Test utilities
```

## Creating a New Feature

1. Create `feature:myfeature:api` module with navigation key
2. Create `feature:myfeature:impl` module with:
   - `MyFeatureScreen.kt` - Composable UI
   - `MyFeatureViewModel.kt` - State holder
   - `MyFeatureUiState.kt` - Sealed interface for states
   - `MyFeatureNavigation.kt` - Navigation setup
   - `MyFeatureModule.kt` - Hilt DI module

## Standard File Patterns

### ViewModel Pattern
```kotlin
@HiltViewModel
class MyFeatureViewModel @Inject constructor(
    private val myRepository: MyRepository,
) : ViewModel() {

    val uiState: StateFlow<MyFeatureUiState> = myRepository
        .getData()
        .map { data -> MyFeatureUiState.Success(data) }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = MyFeatureUiState.Loading,
        )
    
    fun onAction(action: MyFeatureAction) {
        when (action) {
            is MyFeatureAction.ItemClicked -> handleItemClick(action.id)
        }
    }
}
```

### UiState Pattern
```kotlin
sealed interface MyFeatureUiState {
    data object Loading : MyFeatureUiState
    data class Success(val items: List<Item>) : MyFeatureUiState
    data class Error(val message: String) : MyFeatureUiState
}
```

### Screen Pattern
```kotlin
@Composable
internal fun MyFeatureRoute(
    onNavigateToDetail: (String) -> Unit,
    viewModel: MyFeatureViewModel = hiltViewModel(),
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    MyFeatureScreen(
        uiState = uiState,
        onAction = viewModel::onAction,
        onNavigateToDetail = onNavigateToDetail,
    )
}

@Composable
internal fun MyFeatureScreen(
    uiState: MyFeatureUiState,
    onAction: (MyFeatureAction) -> Unit,
    onNavigateToDetail: (String) -> Unit,
) {
    when (uiState) {
        is MyFeatureUiState.Loading -> LoadingIndicator()
        is MyFeatureUiState.Success -> ContentList(uiState.items, onAction)
        is MyFeatureUiState.Error -> ErrorMessage(uiState.message)
    }
}
```

### Repository Pattern
```kotlin
interface MyRepository {
    fun getData(): Flow<List<MyModel>>
    suspend fun updateItem(id: String, data: MyModel)
}

internal class OfflineFirstMyRepository @Inject constructor(
    private val localDataSource: MyDao,
    private val networkDataSource: MyNetworkApi,
) : MyRepository {

    override fun getData(): Flow<List<MyModel>> =
        localDataSource.getAll().map { entities ->
            entities.map { it.toModel() }
        }
    
    override suspend fun updateItem(id: String, data: MyModel) {
        localDataSource.upsert(data.toEntity())
    }
}
```

## Key Dependencies

```kotlin
// Gradle version catalog (libs.versions.toml)
[versions]
kotlin = "1.9.x"
compose-bom = "2024.x.x"
hilt = "2.48"
room = "2.6.x"
coroutines = "1.7.x"

[libraries]
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
```

## Build Configuration

Use convention plugins in `build-logic/` for consistent configuration:
- `AndroidApplicationConventionPlugin` - App modules
- `AndroidLibraryConventionPlugin` - Library modules  
- `AndroidFeatureConventionPlugin` - Feature modules
- `AndroidComposeConventionPlugin` - Compose setup
- `AndroidHiltConventionPlugin` - Hilt setup

See [gradle-setup.md](references/gradle-setup.md) for complete build configuration.
