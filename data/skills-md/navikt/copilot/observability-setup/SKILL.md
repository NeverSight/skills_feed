---
name: observability-setup
description: Setting up Prometheus metrics, OpenTelemetry tracing, and health endpoints for Nais applications
---

# Observability Setup Skill

This skill provides patterns for setting up observability in Nais applications.

## Required Health Endpoints

```kotlin
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.http.*

fun Application.configureHealthEndpoints(
    dataSource: HikariDataSource,
    kafkaProducer: KafkaProducer<String, String>
) {
    routing {
        get("/isalive") {
            call.respondText("Alive", ContentType.Text.Plain)
        }

        get("/isready") {
            val databaseHealthy = checkDatabase(dataSource)
            val kafkaHealthy = checkKafka(kafkaProducer)

            if (databaseHealthy && kafkaHealthy) {
                call.respondText("Ready", ContentType.Text.Plain)
            } else {
                call.respondText(
                    "Not ready",
                    ContentType.Text.Plain,
                    HttpStatusCode.ServiceUnavailable
                )
            }
        }
    }
}

fun checkDatabase(dataSource: HikariDataSource): Boolean {
    return try {
        dataSource.connection.use { it.isValid(1) }
    } catch (e: Exception) {
        false
    }
}

fun checkKafka(producer: KafkaProducer<String, String>): Boolean {
    return try {
        producer.partitionsFor("health-check-topic").isNotEmpty()
    } catch (e: Exception) {
        false
    }
}
```

## Prometheus Metrics Setup

```kotlin
import io.micrometer.core.instrument.Clock
import io.micrometer.core.instrument.binder.jvm.*
import io.micrometer.prometheus.PrometheusConfig
import io.micrometer.prometheus.PrometheusMeterRegistry
import io.prometheus.client.CollectorRegistry
import io.ktor.server.metrics.micrometer.*
import io.ktor.server.response.*
import io.ktor.http.*

val meterRegistry = PrometheusMeterRegistry(
    PrometheusConfig.DEFAULT,
    CollectorRegistry.defaultRegistry,
    Clock.SYSTEM
)

fun Application.configureMetrics() {
    install(MicrometerMetrics) {
        registry = meterRegistry
        // Production pattern from navikt/ao-oppfolgingskontor
        meterBinders = listOf(
            JvmMemoryMetrics(),        // Heap, non-heap memory
            JvmGcMetrics(),            // Garbage collection
            ProcessorMetrics(),        // CPU usage
            UptimeMetrics()            // Application uptime
        )
    }

    routing {
        get("/metrics") {
            call.respondText(
                meterRegistry.scrape(),
                ContentType.parse("text/plain; version=0.0.4")
            )
        }
    }
}
```

## Business Metrics

```kotlin
import io.micrometer.core.instrument.Counter
import io.micrometer.core.instrument.Timer

class UserService(private val meterRegistry: PrometheusMeterRegistry) {
    private val userCreatedCounter = Counter.builder("users_created_total")
        .description("Total users created")
        .register(meterRegistry)

    private val userCreationTimer = Timer.builder("user_creation_duration_seconds")
        .description("User creation duration")
        .register(meterRegistry)

    fun createUser(user: User) {
        userCreationTimer.record {
            repository.save(user)
        }
        userCreatedCounter.increment()
    }
}
```

## OpenTelemetry Tracing

Nais enables OpenTelemetry auto-instrumentation by default. For manual spans:

```kotlin
import io.opentelemetry.api.GlobalOpenTelemetry
import io.opentelemetry.api.trace.Span
import io.opentelemetry.api.trace.StatusCode

val tracer = GlobalOpenTelemetry.getTracer("my-app")

fun processPayment(paymentId: String) {
    val span = tracer.spanBuilder("processPayment")
        .setAttribute("payment.id", paymentId)
        .startSpan()

    try {
        // Business logic
        val payment = repository.findPayment(paymentId)
        span.setAttribute("payment.amount", payment.amount)

        processPaymentInternal(payment)
        span.setStatus(StatusCode.OK)
    } catch (e: Exception) {
        span.setStatus(StatusCode.ERROR, "Payment processing failed")
        span.recordException(e)
        throw e
    } finally {
        span.end()
    }
}
```

## Structured Logging

```kotlin
import mu.KotlinLogging
import net.logstash.logback.argument.StructuredArguments.kv

private val logger = KotlinLogging.logger {}

fun processOrder(orderId: String) {
    logger.info(
        "Processing order",
        kv("order_id", orderId),
        kv("timestamp", LocalDateTime.now())
    )

    try {
        orderService.process(orderId)

        logger.info(
            "Order processed successfully",
            kv("order_id", orderId)
        )
    } catch (e: Exception) {
        logger.error(
            "Order processing failed",
            kv("order_id", orderId),
            kv("error", e.message),
            e
        )
        throw e
    }
}
```

## Nais Manifest

```yaml
apiVersion: nais.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: myteam
  labels:
    team: myteam
spec:
  image: ghcr.io/navikt/my-app:latest
  port: 8080

  # Health checks
  liveness:
    path: /isalive
    initialDelay: 10
    timeout: 1
    periodSeconds: 10
    failureThreshold: 3

  readiness:
    path: /isready
    initialDelay: 10
    timeout: 1
    periodSeconds: 10
    failureThreshold: 3

  # Prometheus scraping
  prometheus:
    enabled: true
    path: /metrics

  # OpenTelemetry auto-instrumentation
  observability:
    autoInstrumentation:
      enabled: true
      runtime: java # Instruments Ktor, JDBC, Kafka automatically
    logging:
      destinations:
        - id: loki # Automatic Loki shipping
        - id: team-logs # Optional: private team logs

  # Resources (for metrics alerting)
  resources:
    limits:
      memory: 512Mi
    requests:
      cpu: 50m
      memory: 256Mi
```

## Alert Configuration

Create `.nais/alert.yml`:

```yaml
apiVersion: nais.io/v1
kind: Alert
metadata:
  name: my-app-alerts
  namespace: myteam
  labels:
    team: myteam
spec:
  receivers:
    slack:
      channel: "#team-alerts"
      prependText: "@here "
  alerts:
    - alert: HighErrorRate
      expr: |
        (sum(rate(http_requests_total{app="my-app",status=~"5.."}[5m]))
        / sum(rate(http_requests_total{app="my-app"}[5m]))) > 0.05
      for: 5m
      description: "Error rate is {{ $value | humanizePercentage }}"
      action: "Check logs in Grafana Loki"
      documentation: https://teamdocs/runbooks/high-error-rate
      sla: "Respond within 15 minutes"
      severity: critical

    - alert: HighResponseTime
      expr: |
        histogram_quantile(0.95,
          rate(http_request_duration_seconds_bucket{app="my-app"}[5m])
        ) > 1
      for: 10m
      description: "95th percentile response time is {{ $value }}s"
      action: "Check Tempo traces for slow requests"
      severity: warning

    - alert: PodCrashLooping
      expr: |
        rate(kube_pod_container_status_restarts_total{
          pod=~"my-app-.*"
        }[15m]) > 0
      for: 5m
      description: "Pod {{ $labels.pod }} is crash looping"
      action: "Check logs: kubectl logs {{ $labels.pod }}"
      severity: critical

    - alert: HighMemoryUsage
      expr: |
        (container_memory_working_set_bytes{app="my-app"}
        / container_spec_memory_limit_bytes{app="my-app"}) > 0.9
      for: 10m
      description: "Memory usage is {{ $value | humanizePercentage }}"
      action: "Check for memory leaks, increase limits if needed"
      severity: warning
```

## Complete Example

```kotlin
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.micrometer.core.instrument.Timer
import io.opentelemetry.api.GlobalOpenTelemetry
import io.opentelemetry.api.trace.StatusCode

fun main() {
    val env = Environment.from(System.getenv())
    val dataSource = createDataSource(env.databaseUrl)

    // Run database migrations
    runMigrations(dataSource)

    // Setup metrics
    val meterRegistry = setupMetrics()

    embeddedServer(Netty, port = 8080) {
        configureHealthEndpoints(dataSource)
        configureMetrics(meterRegistry)
        configureRouting(dataSource, meterRegistry)
    }.start(wait = true)
}

fun Application.configureRouting(
    dataSource: HikariDataSource,
    meterRegistry: PrometheusMeterRegistry
) {
    val tracer = GlobalOpenTelemetry.getTracer("my-app")

    routing {
        get("/api/users") {
            val requestTimer = Timer.sample()
            val requestCounter = meterRegistry.counter(
                "http_requests_total",
                "method", "GET",
                "endpoint", "/api/users"
            )

            val span = tracer.spanBuilder("getUsersRequest")
                .setAttribute("http.method", "GET")
                .setAttribute("http.route", "/api/users")
                .startSpan()

            try {
                val users = userRepository.findAll()
                span.setAttribute("user.count", users.size.toLong())
                span.setStatus(StatusCode.OK)

                requestCounter.increment()
                requestTimer.stop(meterRegistry.timer(
                    "http_request_duration_seconds",
                    "method", "GET",
                    "endpoint", "/api/users",
                    "status", "200"
                ))

                call.respond(users)
            } catch (e: Exception) {
                span.setStatus(StatusCode.ERROR, "Failed to get users")
                span.recordException(e)

                meterRegistry.counter(
                    "http_requests_total",
                    "method", "GET",
                    "endpoint", "/api/users",
                    "status", "500"
                ).increment()

                logger.error(
                    "Failed to get users",
                    kv("trace_id", span.spanContext.traceId),
                    kv("span_id", span.spanContext.spanId),
                    e
                )

                throw e
            } finally {
                span.end()
            }
        }
    }
}
```

## Grafana Dashboard Example

Create a dashboard in Grafana with these panels:

**Panel 1: Request Rate**

```promql
sum(rate(http_requests_total{app="my-app"}[5m])) by (endpoint)
```

**Panel 2: Error Rate**

```promql
sum(rate(http_requests_total{app="my-app",status=~"5.."}[5m]))
/ sum(rate(http_requests_total{app="my-app"}[5m])) * 100
```

**Panel 3: Response Time (p50, p95, p99)**

```promql
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{app="my-app"}[5m]))
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{app="my-app"}[5m]))
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{app="my-app"}[5m]))
```

**Panel 4: Memory Usage**

```promql
container_memory_working_set_bytes{app="my-app"}
/ container_spec_memory_limit_bytes{app="my-app"} * 100
```

**Panel 5: Database Connections**

```promql
hikaricp_connections_active{app="my-app"}
hikaricp_connections_max{app="my-app"}
```

**Panel 6: Kafka Consumer Lag**

```promql
kafka_consumer_lag{app="my-app"}
```

## Loki Query Examples

View logs in Grafana Loki Explorer:

```logql
# All logs from your app
{app="my-app", namespace="myteam"}

# Only errors
{app="my-app"} |= "ERROR"

# JSON logs with specific field
{app="my-app"} | json | event_type="payment_processed"

# Logs correlated with trace
{app="my-app"} | json | trace_id="abc123def456"

# Count errors per minute
sum(rate({app="my-app"} |= "ERROR" [1m])) by (pod)
```

## Tempo Trace Search

View traces in Grafana Tempo:

1. Open Grafana → Explore
2. Select Tempo data source
3. Query by:
   - Service name: `my-app`
   - Operation: `getUsersRequest`
   - Duration: `> 1s`
   - Status: `error`

Or link from logs by clicking trace_id in Loki.

## Monitoring Checklist

- [ ] `/isalive` endpoint implemented
- [ ] `/isready` endpoint with dependency checks (database, Kafka)
- [ ] `/metrics` endpoint exposing Prometheus metrics
- [ ] Health checks configured in Nais manifest
- [ ] Business metrics instrumented (counters, timers, gauges)
- [ ] Structured logging with correlation IDs (trace_id, span_id)
- [ ] OpenTelemetry auto-instrumentation enabled in Nais manifest
- [ ] Alert rules created in `.nais/alert.yml`
- [ ] Slack channel configured for alerts
- [ ] Grafana dashboard created
- [ ] No sensitive data in logs or metrics (verify in Grafana)
- [ ] High-cardinality labels avoided (no user_ids, transaction_ids)

## Production Patterns from navikt

Based on 177+ repositories using observability setup:

### JVM Metrics Binders (navikt/ao-oppfolgingskontor)

```kotlin
import io.micrometer.core.instrument.binder.jvm.*

install(MicrometerMetrics) {
    registry = meterRegistry
    meterBinders = listOf(
        JvmMemoryMetrics(),        // Heap, non-heap, buffer pool metrics
        JvmGcMetrics(),            // GC pause time, count
        ProcessorMetrics(),        // CPU usage
        UptimeMetrics()            // Application uptime
    )
}
```

### Common Counter Patterns

```kotlin
// From dp-rapportering: Track business events
val eventsProcessed = Counter.builder("events_processed_total")
    .description("Total events processed")
    .tag("event_type", "rapportering_innsendt")
    .tag("status", "ok")
    .register(meterRegistry)

// From dp-rapportering: Track API errors
val apiErrors = Counter.builder("api_errors_total")
    .description("Total API errors")
    .tag("endpoint", "/api/rapporteringsperioder")
    .tag("error_type", "validation_error")
    .register(meterRegistry)
```

### Timer Patterns

```kotlin
// From dp-rapportering: Measure HTTP call duration
suspend fun <T> timedAction(navn: String, block: suspend () -> T): T {
    val (result, duration) = measureTimedValue {
        block()
    }
    Timer.builder("http_timer")
        .tag("navn", navn)
        .description("HTTP call duration")
        .register(meterRegistry)
        .record(duration.inWholeMilliseconds, MILLISECONDS)
    return result
}
```

## DORA Metrics Examples

Track DORA metrics for your team:

```kotlin
// Deployment frequency
val deployments = Counter.builder("deployments_total")
    .description("Total deployments")
    .tag("team", "myteam")
    .tag("environment", "production")
    .register(meterRegistry)

// Lead time for changes (commit to deploy)
val leadTime = Timer.builder("deployment_lead_time_seconds")
    .description("Time from commit to deployment")
    .tag("team", "myteam")
    .register(meterRegistry)

// Change failure rate
val failedDeployments = Counter.builder("deployments_failed_total")
    .description("Total failed deployments")
    .tag("team", "myteam")
    .register(meterRegistry)

// Time to restore service
val incidentResolutionTime = Timer.builder("incident_resolution_duration_seconds")
    .description("Time to resolve incidents")
    .tag("team", "myteam")
    .tag("severity", "critical")
    .register(meterRegistry)
```

Alert on DORA metrics:

```yaml
- alert: LowDeploymentFrequency
  expr: |
    sum(increase(deployments_total{team="myteam",environment="production"}[7d]))
    < 5
  description: "Only {{ $value }} deployments in last 7 days (target: >1/day)"
  severity: info

- alert: HighChangeFailureRate
  expr: |
    sum(rate(deployments_failed_total{team="myteam"}[7d]))
    / sum(rate(deployments_total{team="myteam"}[7d]))
    > 0.15
  description: "Change failure rate is {{ $value | humanizePercentage }} (target: <15%)"
  severity: warning
```

See https://dora.dev for benchmarks and best practices.
