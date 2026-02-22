---
name: kmp-networking
description: Ktor client for Kotlin Multiplatform. Shared networking layer with platform-specific engines (OkHttp for Android, Darwin for iOS).
---

# KMP Networking with Ktor

Configure Ktor client for cross-platform networking with platform-optimized engines.

## Dependencies

```kotlin
// build.gradle.kts (shared module)
plugins {
    kotlin("multiplatform")
    kotlin("plugin.serialization")
}

kotlin {
    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-core:2.3.7")
                implementation("io.ktor:ktor-client-content-negotiation:2.3.7")
                implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.7")
                implementation("io.ktor:ktor-client-logging:2.3.7")
                implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
            }
        }
        val androidMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-okhttp:2.3.7")
            }
        }
        val iosMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-darwin:2.3.7")
            }
        }
    }
}
```

## HttpClient Factory

```kotlin
// commonMain/kotlin/network/HttpClientFactory.kt
object HttpClientFactory {
    fun create(
        platform: Platform,
        isDebug: Boolean = false
    ): HttpClient {
        return HttpClient(createEngine(platform)) {
            install(ContentNegotiation) {
                json(Json {
                    ignoreUnknownKeys = true
                    isLenient = true
                    encodeDefaults = false
                })
            }

            if (isDebug) {
                install(Logging) {
                    level = LogLevel.INFO
                    logger = object : Logger {
                        override fun log(message: String) {
                            println("Ktor: $message")
                        }
                    }
                }
            }

            install(Auth) {
                bearer {
                    loadTokens {
                        // Access Token from secure storage
                        BearerTokens(
                            accessTokenStorage.get() ?: "",
                            refreshTokenStorage.get() ?: ""
                        )
                    }
                    refreshTokens {
                        // Refresh token logic
                        val newTokens = authApi.refreshToken()
                        accessTokenStorage.save(newTokens.accessToken)
                        refreshTokenStorage.save(newTokens.refreshToken)
                        BearerTokens(newTokens.accessToken, newTokens.refreshToken)
                    }
                }
            }

            defaultRequest {
                url {
                    protocol = URLProtocol.HTTPS
                    host = "api.example.com"
                }
                header("X-API-Version", "1.0")
                header("X-Platform", platform.name)
            }

            expectSuccess = true
            HttpResponseValidator {
                handleResponseExceptionWithRequest { exception, request ->
                    when (exception) {
                        is ClientRequestException -> {
                            val statusCode = exception.response.status.value
                            when (statusCode) {
                                401 -> throw UnauthorizedException()
                                403 -> throw ForbiddenException()
                                404 -> throw NotFoundException()
                                in 500..599 -> throw ServerException()
                            }
                        }
                        is ServerResponseException -> throw ServerException()
                    }
                }
            }

            install(ResponseObserver) {
                onResponse { response ->
                    // Track response times, errors
                }
            }
        }
    }

    private fun createEngine(platform: Platform): HttpClientEngine {
        return when (platform) {
            Platform.ANDROID -> createOkhttpEngine()
            Platform.IOS -> createDarwinEngine()
        }
    }
}
```

## Platform-Specific Engines

### Android (OkHttp)

```kotlin
// androidMain/kotlin/network/OkHttpEngineFactory.kt
fun createOkhttpEngine(): OkHttpEngine {
    val config = OkHttpConfig {
        preconfigured = OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .addInterceptor { chain ->
                val request = chain.request().newBuilder()
                    .header("User-Agent", "Android App/1.0")
                    .build()
                chain.proceed(request)
            }
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = if (BuildConfig.DEBUG) {
                    HttpLoggingInterceptor.Level.BODY
                } else {
                    HttpLoggingInterceptor.Level.NONE
                }
            })
            .cache(
                Cache(
                    File(context.cacheDir, "http_cache"),
                    10 * 1024 * 1024 // 10MB
                )
            )
            .build()
    }
    return OkHttpEngine(config)
}
```

### iOS (Darwin)

```kotlin
// iosMain/kotlin/network/DarwinEngineFactory.kt
fun createDarwinEngine(): DarwinEngine {
    val config = DarwinClientConfig {
        configureSession {
            setAllowsCellularAccess(true)
            setAllowsExpensiveNetworkAccess(true)
            setAllowsConstrainedNetworkAccess(true)

            // Configure timeout
            setTimeoutIntervalForRequest(30.0)
            setTimeoutIntervalForResource(60.0)

            // Configure cache
            URLCache(
                sharedCacheDirectory,
                10 * 1024 * 1024 // 10MB
            ).let {
                URLCache.setSharedURLCache(it)
            }
        }
    }
    return DarwinEngine(config)
}
```

## API Service Pattern

```kotlin
// commonMain/kotlin/network/api/UserApi.kt
class UserApi(
    private val client: HttpClient
) {
    suspend fun getUsers(page: Int = 1): PaginatedResponse<User> {
        return client.get("/users") {
            parameter("page", page)
            parameter("limit", 20)
        }.body()
    }

    suspend fun getUser(id: String): User {
        return client.get("/users/$id").body()
    }

    suspend fun createUser(request: CreateUserRequest): User {
        return client.post("/users") {
            setBody(request)
            contentType(ContentType.Application.Json)
        }.body()
    }

    suspend fun updateUser(id: String, request: UpdateUserRequest): User {
        return client.put("/users/$id") {
            setBody(request)
            contentType(ContentType.Application.Json)
        }.body()
    }

    suspend fun deleteUser(id: String) {
        return client.delete("/users/$id")
    }

    suspend fun uploadAvatar(userId: String, file: ByteArray): String {
        return client.submitFormWithBinaryData(
            url = "https://api.example.com/users/$userId/avatar",
            formData = formData {
                append("avatar", file, Headers.build {
                    append(HttpHeaders.ContentDisposition, "filename=avatar.jpg")
                })
            }
        ).body()
    }
}
```

## Network Exceptions

```kotlin
// commonMain/kotlin/network/NetworkExceptions.kt
sealed class NetworkException(message: String? = null) : Exception(message)

class UnauthorizedException : NetworkException("User not authenticated")
class ForbiddenException : NetworkException("Access forbidden")
class NotFoundException : NetworkException("Resource not found")
class ServerException : NetworkException("Server error occurred")
class NetworkUnavailableException : NetworkException("Network unavailable")
class TimeoutException : NetworkException("Request timeout")

// Wrap Ktor exceptions
fun Throwable.toNetworkException(): NetworkException {
    return when (this) {
        is NetworkException -> this
        is ClientRequestException -> when (response.status.value) {
            401 -> UnauthorizedException()
            403 -> ForbiddenException()
            404 -> NotFoundException()
            else -> NetworkException(message)
        }
        is ServerResponseException -> ServerException()
        is HttpRequestTimeoutException -> TimeoutException()
        is UnreachableAddressException,
        is ConnectTimeoutException -> NetworkUnavailableException()
        else -> NetworkException(message ?: "Unknown network error")
    }
}
```

## Result Wrapper

```kotlin
// commonMain/kotlin/network/ApiResult.kt
sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val error: NetworkException) : ApiResult<Nothing>()

    suspend fun <R> map(transform: (T) -> R): ApiResult<R> = when (this) {
        is Success -> Success(transform(data))
        is Error -> this
    }

    suspend fun <R> flatMap(transform: (T) -> ApiResult<R>): ApiResult<R> = when (this) {
        is Success -> transform(data)
        is Error -> this
    }

    fun getOrNull(): T? = when (this) {
        is Success -> data
        is Error -> null
    }

    fun getOrElse(defaultValue: T): T = when (this) {
        is Success -> data
        is Error -> defaultValue
    }
}

suspend fun <T> apiCall(block: suspend () -> T): ApiResult<T> = try {
    ApiResult.Success(block())
} catch (e: Exception) {
    ApiResult.Error(e.toNetworkException())
}

// Usage
val result: ApiResult<User> = apiCall { userApi.getUser("123") }
when (result) {
    is ApiResult.Success -> showUser(result.data)
    is ApiResult.Error -> showError(result.error)
}
```

## Retry Logic

```kotlin
// commonMain/kotlin/network/Retry.kt
suspend fun <T> retryApiCall(
    maxRetries: Int = 3,
    delayMs: Long = 1000,
    block: suspend () -> T
): T {
    var lastException: Exception? = null
    repeat(maxRetries) { attempt ->
        try {
            return block()
        } catch (e: Exception) {
            lastException = e
            if (e is NetworkUnavailableException || e is TimeoutException) {
                if (attempt < maxRetries - 1) {
                    delay(delayMs * (attempt + 1))
                }
            } else {
                throw e
            }
        }
    }
    throw lastException ?: RuntimeException("Max retries exceeded")
}
```

## Offline Support

```kotlin
// commonMain/kotlin/network/OfflineCapableApi.kt
class OfflineCapableApi<T : Any>(
    private val api: T,
    private val cache: DatabaseCache
) : OfflineCapableApi<T> by api {

    suspend fun <R> withCache(
        key: String,
        ttl: Duration,
        block: suspend () -> R
    ): R = withContext(Dispatchers.IO) {
        // Try cache first
        cache.get<R>(key)?.let { cached ->
            if (cached.timestamp + ttl.toMillisMilliseconds() > Clock.System.now()) {
                return@withContext cached.data
            }
        }

        // Fetch from network
        try {
            val result = block()
            cache.put(key, CachedData(result, Clock.System.now()))
            result
        } catch (e: NetworkException) {
            // Return stale cache if network fails
            cache.get<R>(key)?.data ?: throw e
        }
    }
}
```

## Dependency Injection Setup

```kotlin
// commonMain/kotlin/di/NetworkModule.kt
val networkModule = module {
    single { HttpClientFactory.create(get(), get()) }
    single { UserApi(get()) }
    single { AuthApi(get()) }
    factory { ConnectivityMonitor(get()) }
}
```

## Best Practices

### ✅ DO

```kotlin
// ✅ Use typed API services
class UserApi(private val client: HttpClient)

// ✅ Wrap calls in result types
suspend fun getUser(): ApiResult<User>

// ✅ Configure timeouts
config { setTimeoutIntervalForRequest(30.0) }

// ✅ Add logging for debug builds
if (isDebug) { install(Logging) }

// ✅ Handle exceptions at boundaries
try { api.call() } catch (e: NetworkException) { /* handle */ }
```

### ❌ DON'T

```kotlin
// ❌ Don't create multiple HttpClient instances
// Use singleton via DI

// ❌ Don't block on suspend calls
runBlocking { api.call() }  // ❌

// ❌ Don't ignore exceptions
try { api.call() } catch (e: Exception) { }  // ❌

// ❌ Don't hardcode URLs
client.get("https://api.example.com/users")  // ❌
// Configure base URL in defaultRequest
```

---

**Remember**: Networking is the bridge between your app and the world. Make it robust, testable, and platform-optimized.
