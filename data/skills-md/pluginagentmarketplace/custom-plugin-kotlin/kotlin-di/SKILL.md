---
name: kotlin-di
description: Dependency Injection - Hilt, Koin, scopes, testing
version: "1.0.0"
sasmp_version: "1.3.0"
bonded_agent: 02-kotlin-android
bond_type: SECONDARY_BOND

execution:
  timeout_ms: 30000
  retry:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 1000

parameters:
  required:
    - name: framework
      type: string
      validation: "^(hilt|koin)$"
  optional:
    - name: platform
      type: string
      default: "android"

logging:
  level: info
  events: [skill_invoked, framework_loaded, error_occurred]
---

# Kotlin DI Skill

Dependency Injection with Hilt and Koin.

## Topics Covered

### Hilt for Android
```kotlin
@HiltAndroidApp
class App : Application()

@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides @Singleton
    fun provideDatabase(@ApplicationContext context: Context) =
        Room.databaseBuilder(context, AppDatabase::class.java, "app.db").build()

    @Provides
    fun provideUserDao(db: AppDatabase) = db.userDao()
}

@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel()
```

### Koin for Multiplatform
```kotlin
val appModule = module {
    single { HttpClient(getEngine()) }
    single { UserRepository(get()) }
    viewModel { UserViewModel(get()) }
}

// Start Koin
startKoin {
    modules(appModule)
}

// Inject
val repository: UserRepository by inject()
```

### Testing with DI
```kotlin
@HiltAndroidTest
class UserViewModelTest {
    @get:Rule val hiltRule = HiltAndroidRule(this)

    @BindValue @JvmField
    val repository: UserRepository = mockk()

    @Inject lateinit var viewModel: UserViewModel

    @Before fun setup() { hiltRule.inject() }
}
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| "No binding for..." | Add @Provides or @Binds |
| ViewModel not injected | Use hiltViewModel() in Compose |

## Usage
```
Skill("kotlin-di")
```
