---
name: tokenx-auth
description: Service-to-service authentication using TokenX token exchange in Nais
---

# TokenX Authentication Skill

This skill provides patterns for secure service-to-service authentication using TokenX.

## Nais Manifest Setup

```yaml
apiVersion: nais.io/v1alpha1
kind: Application
metadata:
  name: my-app
spec:
  tokenx:
    enabled: true

  accessPolicy:
    outbound:
      rules:
        - application: user-service
          namespace: team-user
```

This creates environment variables:

- `TOKEN_X_WELL_KNOWN_URL`
- `TOKEN_X_CLIENT_ID`
- `TOKEN_X_PRIVATE_JWK`

## Token Exchange with Caching

Production pattern from [navikt/tms-ktor-token-support](https://github.com/navikt/tms-ktor-token-support) - used across 198+ Nav repositories:

```kotlin
import com.github.benmanes.caffeine.cache.Cache
import com.github.benmanes.caffeine.cache.Caffeine
import com.nimbusds.jose.jwk.RSAKey

class CachingTokendingsService(
    private val tokendingsConsumer: TokendingsConsumer,
    private val jwtAudience: String,
    private val clientId: String,
    privateJwk: String,
    maxCacheEntries: Long = 10000,
    cacheExpiryMarginSeconds: Int = 10
) : TokendingsService {

    private val cache: Cache<String, AccessTokenEntry> = Caffeine.newBuilder()
        .maximumSize(maxCacheEntries)
        .expireAfter(ExpiryPolicy(cacheExpiryMarginSeconds))
        .build()

    private val privateRsaKey = RSAKey.parse(privateJwk)

    override suspend fun exchangeToken(token: String, targetApp: String): String {
        val cacheKey = "$token:$targetApp".hashCode().toString()
        return cache.get(cacheKey) {
            performTokenExchange(token, targetApp)
        }.accessToken
    }

    private suspend fun performTokenExchange(
        token: String,
        targetApp: String
    ): AccessTokenEntry {
        val clientAssertion = createSignedAssertion(clientId, jwtAudience, privateRsaKey)
        return tokendingsConsumer.exchangeToken(
            subjectToken = token,
            clientAssertion = clientAssertion,
            targetApp = "cluster:namespace:$targetApp"
        )
    }
}
```

## Token Exchange (Basic)

```kotlin
import com.nimbusds.jose.JWSAlgorithm
import com.nimbusds.jose.JWSHeader
import com.nimbusds.jose.crypto.RSASSASigner
import com.nimbusds.jose.jwk.RSAKey
import com.nimbusds.jwt.JWTClaimsSet
import com.nimbusds.jwt.SignedJWT
import java.time.Instant
import java.util.*

class TokenXClient(
    private val tokenXUrl: String,
    private val clientId: String,
    private val privateJwk: String
) {
    private val rsaKey = RSAKey.parse(privateJwk)

    fun exchangeToken(
        userToken: String,
        targetApp: String,
        targetNamespace: String = "default"
    ): String {
        val audience = "cluster:$targetNamespace:$targetApp"
        val clientAssertion = createClientAssertion()

        val response = httpClient.post("$tokenXUrl/token") {
            contentType(ContentType.Application.FormUrlEncoded)
            setBody(
                listOf(
                    "grant_type" to "urn:ietf:params:oauth:grant-type:token-exchange",
                    "client_assertion_type" to "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                    "client_assertion" to clientAssertion,
                    "subject_token_type" to "urn:ietf:params:oauth:token-type:jwt",
                    "subject_token" to userToken,
                    "audience" to audience
                ).formUrlEncode()
            )
        }

        val tokenResponse = response.body<TokenResponse>()
        return tokenResponse.access_token
    }

    private fun createClientAssertion(): String {
        val now = Instant.now()

        val claimsSet = JWTClaimsSet.Builder()
            .subject(clientId)
            .issuer(clientId)
            .audience(tokenXUrl)
            .issueTime(Date.from(now))
            .expirationTime(Date.from(now.plusSeconds(60)))
            .jwtID(UUID.randomUUID().toString())
            .build()

        val signedJWT = SignedJWT(
            JWSHeader.Builder(JWSAlgorithm.RS256)
                .keyID(rsaKey.keyID)
                .build(),
            claimsSet
        )

        signedJWT.sign(RSASSASigner(rsaKey))
        return signedJWT.serialize()
    }
}

data class TokenResponse(
    val access_token: String,
    val token_type: String,
    val expires_in: Int
)
```

## Calling Another Service

```kotlin
import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.http.*

class UserServiceClient(
    private val tokenXClient: TokenXClient,
    private val httpClient: HttpClient,
    private val userServiceUrl: String
) {
    suspend fun getUser(userId: String, userToken: String): User {
        val exchangedToken = tokenXClient.exchangeToken(
            userToken = userToken,
            targetApp = "user-service",
            targetNamespace = "team-user"
        )

        val response = httpClient.get("$userServiceUrl/api/users/$userId") {
            headers {
                append(HttpHeaders.Authorization, "Bearer $exchangedToken")
            }
        }

        return response.body<User>()
    }
}
```

## Validating Inbound Tokens

```kotlin
import com.auth0.jwk.JwkProviderBuilder
import com.auth0.jwt.JWT
import com.auth0.jwt.algorithms.Algorithm
import java.net.URL
import java.security.interfaces.RSAPublicKey

class TokenValidator(
    private val tokenXWellKnownUrl: String,
    private val clientId: String
) {
    private val metadata = fetchMetadata()
    private val jwkProvider = JwkProviderBuilder(URL(metadata.jwks_uri)).build()

    fun validate(token: String): Boolean {
        return try {
            val jwt = JWT.decode(token)
            val jwk = jwkProvider.get(jwt.keyId)
            val algorithm = Algorithm.RSA256(jwk.publicKey as RSAPublicKey, null)

            val verifier = JWT.require(algorithm)
                .withIssuer(metadata.issuer)
                .withAudience(clientId)
                .build()

            verifier.verify(token)
            true
        } catch (e: Exception) {
            logger.warn("Token validation failed", e)
            false
        }
    }

    private fun fetchMetadata(): OAuthMetadata {
        return httpClient.get(tokenXWellKnownUrl).body()
    }
}

data class OAuthMetadata(
    val issuer: String,
    val jwks_uri: String,
    val token_endpoint: String
)
```

## Ktor Integration

```kotlin
import io.ktor.server.application.*
import io.ktor.server.auth.*
import io.ktor.server.auth.jwt.*

fun Application.configureTokenX() {
    val tokenValidator = TokenValidator(
        tokenXWellKnownUrl = environment.config.property("tokenx.well.known.url").getString(),
        clientId = environment.config.property("tokenx.client.id").getString()
    )

    install(Authentication) {
        jwt("tokenx") {
            verifier(
                JwkProviderBuilder(URL(tokenValidator.metadata.jwks_uri)).build(),
                tokenValidator.metadata.issuer
            ) {
                withAudience(tokenValidator.clientId)
            }

            validate { credential ->
                if (credential.payload.audience.contains(tokenValidator.clientId)) {
                    JWTPrincipal(credential.payload)
                } else {
                    null
                }
            }
        }
    }

    routing {
        authenticate("tokenx") {
            get("/api/protected") {
                val principal = call.principal<JWTPrincipal>()
                val userId = principal?.payload?.subject

                call.respond("Authenticated user: $userId")
            }
        }
    }
}
```

## Complete Example

```kotlin
fun main() {
    val env = Environment.from(System.getenv())

    val tokenXClient = TokenXClient(
        tokenXUrl = env.tokenXUrl,
        clientId = env.tokenXClientId,
        privateJwk = env.tokenXPrivateJwk
    )

    val userServiceClient = UserServiceClient(
        tokenXClient = tokenXClient,
        httpClient = HttpClient(),
        userServiceUrl = env.userServiceUrl
    )

    embeddedServer(Netty, port = 8080) {
        configureTokenX()

        routing {
            authenticate("tokenx") {
                get("/api/users/{id}") {
                    val userId = call.parameters["id"]!!
                    val userToken = call.request.headers["Authorization"]!!
                        .removePrefix("Bearer ")

                    val user = userServiceClient.getUser(userId, userToken)
                    call.respond(user)
                }
            }
        }
    }.start(wait = true)
}
```

## Testing with MockOAuth2Server

```kotlin
import no.nav.security.mock.oauth2.MockOAuth2Server
import org.junit.jupiter.api.*

class TokenXTest {
    private lateinit var mockOAuth2Server: MockOAuth2Server

    @BeforeEach
    fun setup() {
        mockOAuth2Server = MockOAuth2Server()
        mockOAuth2Server.start()
    }

    @AfterEach
    fun teardown() {
        mockOAuth2Server.shutdown()
    }

    @Test
    fun `should exchange token successfully`() {
        val userToken = mockOAuth2Server.issueToken(
            issuerId = "tokenx",
            subject = "user123",
            audience = "my-app"
        )

        val tokenXClient = TokenXClient(
            tokenXUrl = mockOAuth2Server.tokenEndpointUrl("tokenx").toString(),
            clientId = "my-app",
            privateJwk = generatePrivateJwk()
        )

        val exchangedToken = tokenXClient.exchangeToken(
            userToken = userToken.serialize(),
            targetApp = "user-service",
            targetNamespace = "team-user"
        )

        assertNotNull(exchangedToken)
    }
}
```

## Security Checklist

- [ ] TokenX enabled in Nais manifest
- [ ] Access policy defined for outbound calls
- [ ] Token validation on all protected endpoints
- [ ] Client assertion signed with private JWK
- [ ] Tokens not logged or exposed
- [ ] Token expiry handled gracefully
- [ ] HTTPS enforced for all calls
