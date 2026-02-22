---
name: kmp-di
description: Dependency Injection for KMP. Koin multiplatform setup, platform modules, and manual DI patterns.
---

# KMP Dependency Injection

Cross-platform dependency injection with Koin.

## Koin Multiplatform Setup

### Dependencies

```kotlin
// build.gradle.kts (shared module)
sourceSets {
    val commonMain by getting {
        dependencies {
            implementation("io.insert-koin:koin-core:${koinVersion}")
            implementation("io.insert-koin:koin-test:${koinVersion}")
        }
    }
    val androidMain by getting {
        dependencies {
            implementation("io.insert-koin:koin-android:${koinVersion}")
        }
    }
}
```

### Module Definition

```kotlin
// commonMain/kotlin/di/AppModule.kt
val sharedModule = module {
    // ViewModels (Android) / ScreenModels (multiplatform)
    factory { HomeViewModel(get(), get()) }
    factory { DetailViewModel(get()) }

    // Use Cases
    factory { GetUsersUseCase(get()) }
    factory { GetUserDetailUseCase(get()) }

    // Repositories
    single<UserRepository> { UserRepositoryImpl(get(), get()) }

    // Data Sources
    single { UserApi(get()) }
    single { createDatabase(get()) }
}
```

### Platform Modules

```kotlin
// androidMain/kotlin/di/PlatformModule.kt
val androidPlatformModule = module {
    includes(sharedModule)

    // Android-specific dependencies
    single { android.content.Context() }
    single { PlatformConnectivityMonitor(get()) }
    single { PlatformFileService(get()) }
}

// iosMain/kotlin/di/PlatformModule.kt
val iosPlatformModule = module {
    includes(sharedModule)

    // iOS-specific dependencies
    single { PlatformConnectivityMonitor() }
    single { PlatformFileService() }
}
```

## Koin Start

### Android

```kotlin
// androidMain/kotlin/MyApp.kt
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@MyApp)
            modules(androidPlatformModule)
        }
    }
}
```

### iOS

```kotlin
// iosMain/kotlin/di/KoinInit.kt
fun initKoin() {
    startKoin {
        modules(iosPlatformModule)
    }
}

// Called from Swift
// KotlinKMMSharedKt.doInitKoin()
```

### Compose Multiplatform

```kotlin
// commonMain/kotlin/Main.kt
fun main() {
    startKoin {
        modules(sharedModule)
    }

    App()
}
```

## ViewModel Injection

### Android (ViewModel)

```kotlin
// androidMain/kotlin/ui/HomeScreen.kt
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = koinViewModel()
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    HomeContent(state)
}
```

### iOS (ScreenModel)

```kotlin
// commonMain/kotlin/ui/HomeScreen.kt
@Composable
fun HomeScreen() {
    val model = getScreenModel<HomeScreenModel>()
    val state by model.state.collectAsState()

    HomeContent(state)
}
```

## Repository Pattern

### Factory vs Single

```kotlin
// ✅ factory - creates new instance each time
factory { HomeViewModel(get(), get()) }

// ✅ single - shared instance
single<UserRepository> { UserRepositoryImpl(get(), get()) }

// ✅ scoped - tied to component lifetime
scoped(HomeScope.homeScope) { HomeData(get()) }
```

## Named Dependencies

```kotlin
// ✅ Named dependencies
module {
    single(named("default")) { DefaultLogger() }
    single(named("analytics")) { AnalyticsLogger() }

    factory { MyRepository(logger = get(named("default"))) }
}
```

## Manual DI (Alternative)

### Simple Service Locator

```kotlin
// commonMain/kotlin/di/ServiceLocator.kt
object ServiceLocator {
    private val services = mutableMapOf<String, Any>()

    fun <T> get(key: String): T {
        return services[key] as T
    }

    fun register(key: String, service: Any) {
        services[key] = service
    }

    fun init() {
        register("repository", UserRepositoryImpl())
        register("api", UserApi())
    }
}
```

### Pure Kotlin DI

```kotlin
// commonMain/kotlin/di/AppContainer.kt
class AppContainer(
    private val platformService: PlatformService
) {
    val api: UserApi = UserApi()
    val database: AppDatabase = createDatabase()

    val userRepository: UserRepository by lazy {
        UserRepositoryImpl(api, database)
    }

    val homeViewModel: HomeViewModel by lazy {
        HomeViewModel(userRepository, platformService)
    }
}
```

## Testing with DI

```kotlin
// commonTest/kotlin/di/TestModule.kt
val testModule = module {
    single<MockUserService> { MockUserService() }
    single<UserService>(override = true) { get<MockUserService>() }
}

// In tests
@BeforeTest
fun setup() {
    startKoin { modules(testModule) }
}

@AfterTest
fun tearDown() {
    stopKoin()
}
```

---

**Remember**: DI simplifies testing. Use it to inject mocks and fakes easily.
