---
name: kotlin-serialization
description: kotlinx.serialization - JSON, Protobuf, custom serializers
version: "1.0.0"
sasmp_version: "1.3.0"
bonded_agent: 01-kotlin-fundamentals
bond_type: SECONDARY_BOND

execution:
  timeout_ms: 30000
  retry:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 1000

parameters:
  required:
    - name: format
      type: string
      validation: "^(json|protobuf|cbor|custom)$"
  optional:
    - name: version
      type: string
      default: "1.6.3"

logging:
  level: info
  events: [skill_invoked, format_loaded, error_occurred]
---

# Kotlin Serialization Skill

Type-safe serialization with kotlinx.serialization.

## Topics Covered

### JSON Serialization
```kotlin
@Serializable
data class User(
    val id: Long,
    val name: String,
    @SerialName("email_address") val email: String,
    val createdAt: Instant = Instant.now()
)

val json = Json {
    ignoreUnknownKeys = true
    encodeDefaults = true
    prettyPrint = true
}

val user = json.decodeFromString<User>(jsonString)
val output = json.encodeToString(user)
```

### Custom Serializers
```kotlin
object InstantSerializer : KSerializer<Instant> {
    override val descriptor = PrimitiveSerialDescriptor("Instant", PrimitiveKind.LONG)
    override fun serialize(encoder: Encoder, value: Instant) = encoder.encodeLong(value.toEpochMilli())
    override fun deserialize(decoder: Decoder) = Instant.ofEpochMilli(decoder.decodeLong())
}

@Serializable
data class Event(
    @Serializable(with = InstantSerializer::class) val timestamp: Instant
)
```

### Polymorphic Serialization
```kotlin
@Serializable
sealed class Response {
    @Serializable @SerialName("success")
    data class Success(val data: String) : Response()

    @Serializable @SerialName("error")
    data class Error(val message: String) : Response()
}

val json = Json { classDiscriminator = "type" }
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| "Serializer not found" | Add @Serializable or plugin |
| Unknown property fails | Set ignoreUnknownKeys = true |

## Usage
```
Skill("kotlin-serialization")
```
