---
name: opentelemetry
description: OpenTelemetry observability - use for distributed tracing, metrics, instrumentation, Sentry integration, and monitoring
---

# OpenTelemetry Patterns

## Spring Boot Configuration

```kotlin
// build.gradle.kts
dependencies {
    implementation(platform("io.opentelemetry.instrumentation:opentelemetry-instrumentation-bom:2.15.0"))
    implementation("io.opentelemetry.instrumentation:opentelemetry-spring-boot-starter")
    implementation("io.micrometer:micrometer-tracing-bridge-otel")
    implementation("io.opentelemetry:opentelemetry-exporter-zipkin")

    // Sentry integration
    implementation("io.sentry:sentry-spring-boot-starter-jakarta:8.26.0")
    implementation("io.sentry:sentry-logback:8.26.0")
}
```

```yaml
# application.yaml
spring:
  application:
    name: orca-facade

management:
  tracing:
    sampling:
      probability: 1.0  # 100% in dev, lower in prod
  otlp:
    tracing:
      endpoint: http://localhost:4318/v1/traces

otel:
  exporter:
    otlp:
      endpoint: http://otel-collector:4317
  service:
    name: orca-facade
  resource:
    attributes:
      deployment.environment: ${ENVIRONMENT:dev}
      service.version: ${APP_VERSION:unknown}

sentry:
  dsn: ${SENTRY_DSN:}
  environment: ${ENVIRONMENT:dev}
  traces-sample-rate: 1.0
```

## Custom Span Creation

```kotlin
import io.opentelemetry.api.trace.Span
import io.opentelemetry.api.trace.Tracer
import io.opentelemetry.context.Context
import org.springframework.stereotype.Component

@Component
class TracingService(
    private val tracer: Tracer
) {

    fun <T> withSpan(
        spanName: String,
        attributes: Map<String, String> = emptyMap(),
        block: () -> T
    ): T {
        val span = tracer.spanBuilder(spanName)
            .setParent(Context.current())
            .startSpan()

        attributes.forEach { (key, value) ->
            span.setAttribute(key, value)
        }

        return try {
            span.makeCurrent().use {
                block()
            }
        } catch (e: Exception) {
            span.recordException(e)
            span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR, e.message ?: "Error")
            throw e
        } finally {
            span.end()
        }
    }
}

// Usage
@Service
class EnvironmentService(
    private val tracingService: TracingService,
    private val repository: EnvironmentRepository
) {

    fun createEnvironment(request: CreateRequest): Environment {
        return tracingService.withSpan(
            "EnvironmentService.createEnvironment",
            mapOf(
                "environment.name" to request.name,
                "user.id" to request.userId
            )
        ) {
            // Add events
            Span.current().addEvent("Validating request")
            validateRequest(request)

            Span.current().addEvent("Saving to database")
            repository.save(request.toEntity())
        }
    }
}
```

## Annotation-Based Tracing

```kotlin
import io.micrometer.tracing.annotation.NewSpan
import io.micrometer.tracing.annotation.SpanTag

@Service
class ComputeService {

    @NewSpan("compute.createInstance")
    fun createInstance(
        @SpanTag("instance.type") type: String,
        @SpanTag("instance.region") region: String
    ): Instance {
        // Automatically traced
        return computeClient.create(type, region)
    }
}
```

## Baggage Propagation

```kotlin
import io.opentelemetry.api.baggage.Baggage

// Set baggage (propagates across services)
fun setUserContext(userId: String, tenantId: String) {
    Baggage.current()
        .toBuilder()
        .put("user.id", userId)
        .put("tenant.id", tenantId)
        .build()
        .makeCurrent()
}

// Read baggage
fun getCurrentUserId(): String? {
    return Baggage.current().getEntryValue("user.id")
}
```

## Next.js / Node.js Setup

```typescript
// instrumentation.ts (Next.js)
import { NodeSDK } from '@opentelemetry/sdk-node'
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { Resource } from '@opentelemetry/resources'
import { SEMRESATTRS_SERVICE_NAME, SEMRESATTRS_SERVICE_VERSION } from '@opentelemetry/semantic-conventions'

export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    const sdk = new NodeSDK({
      resource: new Resource({
        [SEMRESATTRS_SERVICE_NAME]: 'orca-lab',
        [SEMRESATTRS_SERVICE_VERSION]: process.env.npm_package_version || 'unknown',
      }),
      traceExporter: new OTLPTraceExporter({
        url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318/v1/traces',
      }),
      instrumentations: [
        getNodeAutoInstrumentations({
          '@opentelemetry/instrumentation-fs': { enabled: false },
        }),
      ],
    })

    sdk.start()
  }
}
```

```typescript
// lib/tracing.ts
import { trace, SpanStatusCode, context } from '@opentelemetry/api'

const tracer = trace.getTracer('orca-lab')

export async function withSpan<T>(
  name: string,
  attributes: Record<string, string>,
  fn: () => Promise<T>
): Promise<T> {
  return tracer.startActiveSpan(name, async (span) => {
    try {
      Object.entries(attributes).forEach(([key, value]) => {
        span.setAttribute(key, value)
      })

      const result = await fn()
      span.setStatus({ code: SpanStatusCode.OK })
      return result
    } catch (error) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: error instanceof Error ? error.message : 'Unknown error',
      })
      span.recordException(error as Error)
      throw error
    } finally {
      span.end()
    }
  })
}

// Usage
export async function createEnvironment(data: CreateEnvInput) {
  return withSpan(
    'createEnvironment',
    { 'environment.name': data.name },
    async () => {
      const response = await fetch('/api/environments', {
        method: 'POST',
        body: JSON.stringify(data),
      })
      return response.json()
    }
  )
}
```

## Metrics

```kotlin
// Kotlin/Spring Boot
import io.micrometer.core.instrument.MeterRegistry
import io.micrometer.core.instrument.Timer

@Component
class MetricsService(
    private val registry: MeterRegistry
) {

    private val environmentCreatedCounter = registry.counter(
        "orca.environment.created",
        "type", "standard"
    )

    private val environmentCreationTimer = Timer.builder("orca.environment.creation.duration")
        .description("Time to create an environment")
        .register(registry)

    fun recordEnvironmentCreated(type: String) {
        registry.counter("orca.environment.created", "type", type).increment()
    }

    fun <T> timeEnvironmentCreation(block: () -> T): T {
        return environmentCreationTimer.recordCallable(block)!!
    }
}
```

## Sentry Integration

```kotlin
// Error reporting with Sentry
import io.sentry.Sentry
import io.sentry.SentryLevel

@ControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(Exception::class)
    fun handleException(e: Exception): ResponseEntity<ErrorResponse> {
        // Report to Sentry with context
        Sentry.withScope { scope ->
            scope.setTag("error.type", e.javaClass.simpleName)
            scope.setLevel(SentryLevel.ERROR)
            scope.setContexts("request", mapOf(
                "path" to getCurrentRequestPath(),
                "method" to getCurrentRequestMethod()
            ))
            Sentry.captureException(e)
        }

        return ResponseEntity.status(500)
            .body(ErrorResponse("Internal server error"))
    }
}
```

## OpenTelemetry Collector Config

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  zipkin:
    endpoint: http://zipkin:9411/api/v2/spans
  prometheus:
    endpoint: 0.0.0.0:8889
  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [zipkin, logging]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```
