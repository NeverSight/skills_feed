---
name: kotlin-app-config
description: Sealed class configuration pattern for Kotlin applications with environment-specific settings
---

# Kotlin Application Configuration Skill

This skill provides patterns for type-safe environment configuration using Kotlin sealed classes.

## Sealed Class Configuration Pattern

```kotlin
sealed class Environment(
    val name: String,
    val databaseUrl: String,
    val kafkaBrokers: String,
    val azureAdIssuer: String
) {
    data object Local : Environment(
        name = "local",
        databaseUrl = "jdbc:postgresql://localhost:5432/myapp",
        kafkaBrokers = "localhost:9092",
        azureAdIssuer = "http://localhost:8080/azuread"
    )

    data class Dev(
        private val env: Map<String, String>
    ) : Environment(
        name = "dev",
        databaseUrl = env.getValue("DATABASE_URL"),
        kafkaBrokers = env.getValue("KAFKA_BROKERS"),
        azureAdIssuer = env.getValue("AZURE_OPENID_CONFIG_ISSUER")
    )

    data class Prod(
        private val env: Map<String, String>
    ) : Environment(
        name = "prod",
        databaseUrl = env.getValue("DATABASE_URL"),
        kafkaBrokers = env.getValue("KAFKA_BROKERS"),
        azureAdIssuer = env.getValue("AZURE_OPENID_CONFIG_ISSUER")
    )

    companion object {
        fun from(env: Map<String, String>): Environment {
            return when (env["Nais_CLUSTER_NAME"]) {
                "dev-gcp" -> Dev(env)
                "prod-gcp" -> Prod(env)
                else -> Local
            }
        }
    }
}
```

## Using Configuration

```kotlin
fun main() {
    val env = Environment.from(System.getenv())

    val dataSource = createDataSource(env.databaseUrl)
    val kafkaProducer = createKafkaProducer(env.kafkaBrokers)

    logger.info("Starting application in ${env.name} environment")
}
```

## With Konfig Library

```kotlin
import com.natpryce.konfig.*

data class AppConfig(
    val database: DatabaseConfig,
    val kafka: KafkaConfig,
    val azure: AzureConfig
)

data class DatabaseConfig(
    val url: String,
```

## Alternative: Sealed Interface Pattern (navikt/hotlibs)

Production pattern from [navikt/hotlibs](https://github.com/navikt/hotlibs) supporting multiple cluster types:

```kotlin
sealed interface Environment {
    val cluster: String
    val tier: Tier

    enum class Tier { TEST, LOCAL, DEV, PROD }

    companion object {
        private val all: List<Environment> = listOf(
            TestEnvironment,
            LocalEnvironment,
            GcpEnvironment.DEV,
            GcpEnvironment.PROD
        )

        val current: Environment by lazy {
            val cluster = System.getenv("Nais_CLUSTER_NAME")
            all.find { it.cluster == cluster } ?: LocalEnvironment
        }
    }
}

sealed class DefaultEnvironment(
    override val cluster: String,
    override val tier: Environment.Tier
) : Environment

object TestEnvironment : DefaultEnvironment("test", Environment.Tier.TEST)
object LocalEnvironment : DefaultEnvironment("local", Environment.Tier.LOCAL)

enum class GcpEnvironment(
    override val cluster: String,
    override val tier: Environment.Tier
) : Environment {
    DEV("dev-gcp", Environment.Tier.DEV),
    PROD("prod-gcp", Environment.Tier.PROD)
}
```

```kotlin
data class DatabaseConfig(
    val url: String,
    val username: String,
    val password: String
)

data class KafkaConfig(
    val brokers: String,
    val topic: String
)

data class AzureConfig(
    val clientId: String,
    val issuer: String,
    val jwksUri: String
)

fun loadConfig(): AppConfig {
    val config = ConfigurationProperties.systemProperties() overriding
                 EnvironmentVariables()

    return AppConfig(
        database = DatabaseConfig(
            url = config[Key("database.url", stringType)],
            username = config[Key("database.username", stringType)],
            password = config[Key("database.password", stringType)]
        ),
        kafka = KafkaConfig(
            brokers = config[Key("kafka.brokers", stringType)],
            topic = config[Key("kafka.topic", stringType)]
        ),
        azure = AzureConfig(
            clientId = config[Key("azure.client.id", stringType)],
            issuer = config[Key("azure.issuer", stringType)],
            jwksUri = config[Key("azure.jwks.uri", stringType)]
        )
    )
}
```

## Benefits

- **Type Safety**: Compile-time validation of configuration
- **Environment Separation**: Clear boundaries between local/dev/prod
- **Testability**: Easy to create test configurations
- **Documentation**: Configuration structure is self-documenting
