---
name: networking
description: Retrofit, OkHttp, REST APIs, JSON serialization, network security.
version: "2.0.0"
sasmp_version: "1.3.0"

# Agent Binding
bonded_agent: 05-networking
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: HTTP networking & API integration

# Parameter Validation
parameters:
  api_type:
    type: string
    enum: [rest, graphql]
    default: rest
  concern:
    type: string
    enum: [setup, error_handling, security, caching]
    required: false

# Retry Configuration
retry:
  max_attempts: 3
  backoff: exponential
  on_failure: provide_fallback_pattern

# Observability
logging:
  level: info
  include: [api_endpoint, response_code, latency]
---

# API Integration Skill

## Quick Start

### Retrofit Setup
```kotlin
interface UserApi {
    @GET("/users/{id}")
    suspend fun getUser(@Path("id") id: Int): UserDto
    
    @POST("/users")
    suspend fun createUser(@Body user: UserDto): UserDto
}

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val api = retrofit.create(UserApi::class.java)
```

### OkHttp Configuration
```kotlin
val client = OkHttpClient.Builder()
    .addInterceptor(HttpLoggingInterceptor())
    .connectTimeout(30, TimeUnit.SECONDS)
    .certificatePinner(CertificatePinner.Builder()
        .add("api.example.com", "sha256/...").build())
    .build()
```

### Error Handling
```kotlin
sealed class Result<T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error<T>(val exception: Exception) : Result<T>()
}
```

## Key Concepts

### HTTP Methods
- GET: Fetch data
- POST: Create resource
- PUT/PATCH: Update
- DELETE: Remove

### Retrofit Features
- Type-safe interfaces
- Automatic serialization
- Suspend function support
- Error callbacks

### Network Security
- HTTPS/TLS enforcement
- SSL pinning
- Certificate validation
- Secure token storage

## Best Practices

✅ Use HTTPS always
✅ Implement SSL pinning
✅ Handle errors gracefully
✅ Optimize request/response size
✅ Cache when possible

## Resources

- [Retrofit Guide](https://square.github.io/retrofit/)
- [OkHttp Documentation](https://square.github.io/okhttp/)
