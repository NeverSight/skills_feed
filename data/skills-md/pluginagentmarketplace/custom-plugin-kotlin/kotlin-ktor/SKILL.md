---
name: kotlin-ktor
description: Ktor framework - routing, authentication, WebSockets
version: "1.0.0"
sasmp_version: "1.3.0"
bonded_agent: 05-kotlin-backend
bond_type: PRIMARY_BOND

execution:
  timeout_ms: 30000
  retry:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 1000

parameters:
  required:
    - name: topic
      type: string
      validation: "^(routing|plugins|auth|websocket|testing)$"
  optional:
    - name: ktor_version
      type: string
      default: "2.3.8"

logging:
  level: info
  events: [skill_invoked, topic_loaded, error_occurred]
---

# Kotlin Ktor Skill

Build production-ready backends with Ktor.

## Topics Covered

### Routing
```kotlin
fun Application.module() {
    install(ContentNegotiation) { json() }
    routing {
        route("/api/v1") {
            get("/users") { call.respond(userService.findAll()) }
            get("/users/{id}") {
                val id = call.parameters["id"]?.toLongOrNull()
                    ?: throw BadRequestException("Invalid ID")
                call.respond(userService.findById(id) ?: throw NotFoundException())
            }
        }
    }
}
```

### JWT Authentication
```kotlin
install(Authentication) {
    jwt("auth") {
        verifier(JWT.require(Algorithm.HMAC256(secret)).build())
        validate { credential ->
            if (credential.payload.getClaim("userId").asString().isNotEmpty())
                UserPrincipal(credential.payload)
            else null
        }
    }
}

authenticate("auth") { userRoutes() }
```

### Testing
```kotlin
@Test
fun `GET users returns list`() = testApplication {
    application { module() }
    client.get("/api/v1/users").apply {
        assertThat(status).isEqualTo(HttpStatusCode.OK)
    }
}
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| 404 for valid route | Order specific routes before wildcards |
| JSON not parsed | Install ContentNegotiation plugin |

## Usage
```
Skill("kotlin-ktor")
```
