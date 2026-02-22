---
name: kotlin-multiplatform
description: >-
  KMP/CMP shared business logic, Compose Multiplatform, expect/actual, Ktor, SQLDelight, and platform-specific implementations. Use when building cross-platform Kotlin applications for Android, iOS, desktop, or web.
---

# Kotlin Multiplatform Skill

Shared business logic and optional shared UI across Android, iOS, desktop, and web.

---

## Project Structure

```
project/
├── composeApp/                    # Shared Compose UI (if using CMP)
│   └── src/
│       ├── commonMain/            # Shared UI code
│       ├── androidMain/           # Android-specific UI
│       ├── iosMain/               # iOS-specific UI
│       └── desktopMain/          # Desktop-specific UI
├── shared/                        # Shared business logic (KMP)
│   └── src/
│       ├── commonMain/            # Shared code
│       │   └── kotlin/
│       │       ├── data/          # Repositories, data sources
│       │       ├── domain/        # Use cases, models
│       │       └── platform/      # expect declarations
│       ├── androidMain/           # actual implementations
│       ├── iosMain/               # actual implementations
│       └── commonTest/            # Shared tests
├── androidApp/                    # Android entry point
├── iosApp/                        # iOS entry point (Xcode project)
├── build.gradle.kts
└── settings.gradle.kts
```

---

## expect/actual Pattern

```kotlin
// commonMain - expect declaration
expect class PlatformContext

expect fun getPlatformName(): String

expect fun createHttpClient(): HttpClient

// androidMain - actual implementation
actual class PlatformContext(val context: android.content.Context)

actual fun getPlatformName(): String = "Android ${Build.VERSION.SDK_INT}"

actual fun createHttpClient(): HttpClient = HttpClient(OkHttp) {
    install(ContentNegotiation) { json() }
}

// iosMain - actual implementation
actual class PlatformContext

actual fun getPlatformName(): String = UIDevice.currentDevice.systemName()

actual fun createHttpClient(): HttpClient = HttpClient(Darwin) {
    install(ContentNegotiation) { json() }
}
```

---

## Key Libraries

| Library | Purpose | Multiplatform? |
|---------|---------|----------------|
| Ktor | HTTP client | Yes |
| kotlinx.serialization | JSON parsing | Yes |
| kotlinx.coroutines | Async/concurrency | Yes |
| SQLDelight | Local database | Yes |
| Koin | Dependency injection | Yes |
| Compose Multiplatform | Shared UI | Yes |
| kotlinx.datetime | Date/time | Yes |
| Napier | Logging | Yes |

---

## Networking with Ktor

```kotlin
// commonMain
class ApiClient(private val httpClient: HttpClient) {
    suspend fun getUsers(): List<User> {
        return httpClient.get("https://api.example.com/users").body()
    }

    suspend fun createUser(input: CreateUserInput): User {
        return httpClient.post("https://api.example.com/users") {
            contentType(ContentType.Application.Json)
            setBody(input)
        }.body()
    }
}

@Serializable
data class User(
    val id: String,
    val name: String,
    val email: String,
)
```

---

## Local Storage with SQLDelight

```sql
-- src/commonMain/sqldelight/com/example/UserQueries.sq
CREATE TABLE user (
    id TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    cached_at INTEGER NOT NULL
);

selectAll:
SELECT * FROM user ORDER BY name;

insertOrReplace:
INSERT OR REPLACE INTO user (id, name, email, cached_at)
VALUES (?, ?, ?, ?);

deleteById:
DELETE FROM user WHERE id = ?;
```

---

## Compose Multiplatform UI

```kotlin
// commonMain - Shared composable
@Composable
fun UserListScreen(viewModel: UserListViewModel) {
    val users by viewModel.users.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    Scaffold(
        topBar = { TopAppBar(title = { Text("Users") }) }
    ) { padding ->
        if (isLoading) {
            CircularProgressIndicator(modifier = Modifier.padding(padding))
        } else {
            LazyColumn(modifier = Modifier.padding(padding)) {
                items(users) { user ->
                    UserRow(user = user, onClick = { viewModel.onUserClick(user.id) })
                }
            }
        }
    }
}
```

---

## iOS Integration

### Swift Interop

```swift
// iosApp - Using shared Kotlin code from Swift
import shared

class UserViewController: UIViewController {
    private let viewModel = UserListViewModel()

    override func viewDidLoad() {
        super.viewDidLoad()
        viewModel.users.collect(collector: FlowCollector { users in
            // Update UI with users
        })
    }
}
```

### CocoaPods or SPM Integration

```kotlin
// build.gradle.kts
kotlin {
    iosX64()
    iosArm64()
    iosSimulatorArm64()

    cocoapods {
        summary = "Shared module"
        homepage = "https://example.com"
        ios.deploymentTarget = "16.0"
        framework { baseName = "shared" }
    }
}
```

---

## Testing

```kotlin
// commonTest
class UserRepositoryTest {
    private val fakeApi = FakeApiClient()
    private val repository = UserRepository(fakeApi)

    @Test
    fun fetchUsersReturnsListFromApi() = runTest {
        fakeApi.setUsers(listOf(User("1", "Alice", "alice@test.com")))

        val users = repository.getUsers()

        assertEquals(1, users.size)
        assertEquals("Alice", users.first().name)
    }
}
```

---

## Best Practices

- Share business logic (networking, storage, models) — keep platform UI native if needed
- Use `expect`/`actual` sparingly — prefer interfaces with platform implementations via DI
- Keep the shared module thin — avoid pulling in platform-heavy dependencies
- Test shared code in `commonTest` — it runs on all targets
- Use Compose Multiplatform for new projects where native look isn't critical

---

## Related Resources

- `~/.claude/skills/android-development/SKILL.md` - Android patterns
- `~/.claude/skills/ios-development/SKILL.md` - iOS patterns
- `~/.claude/agents/flutter-developer.md` - Alternative cross-platform

---

_Share logic, respect platforms. KMP gives you the best of both worlds._
