---
name: golang-observability-opentelemetry
description: "Instrumenting Go applications with OpenTelemetry for distributed tracing, Prometheus for metrics, and structured logging with slog"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Master Go observability through OpenTelemetry distributed tracing, Prometheus metrics, and slog structured logging for production-ready microservices"
    when_to_use: "Instrumenting microservices for observability, setting up distributed tracing across services, creating operational dashboards, debugging production issues, performance monitoring and optimization"
    quick_start: "1. Initialize OpenTelemetry tracer and exporter 2. Add Prometheus metrics endpoint 3. Configure slog for structured logging 4. Instrument HTTP middleware 5. Implement health checks"
  token_estimate:
    entry: 150
    full: 5000
context_limit: 700
tags:
  - observability
  - golang
  - opentelemetry
  - prometheus
  - tracing
  - metrics
  - logging
  - slog
requires_tools: []
---

# Go Observability with OpenTelemetry

## Overview

Modern Go applications require comprehensive observability through the three pillars: traces, metrics, and logs. OpenTelemetry provides vendor-neutral instrumentation for distributed tracing, Prometheus offers powerful metrics collection, and Go's slog package (1.21+) delivers structured logging with minimal overhead.

**Key Features:**
- 🔍 **OpenTelemetry**: Distributed tracing with context propagation
- 📊 **Prometheus**: Metrics collection with /metrics endpoint
- 📝 **Structured Logging**: slog with JSON formatting and correlation IDs
- 🎯 **Auto-Instrumentation**: HTTP/gRPC middleware patterns
- 💚 **Health Checks**: Kubernetes-ready readiness/liveness probes
- 🔄 **Graceful Shutdown**: Clean exporter shutdown and signal handling

## When to Use This Skill

Activate this skill when:
- Instrumenting microservices for production observability
- Setting up distributed tracing across service boundaries
- Creating operational dashboards with Prometheus/Grafana
- Debugging production performance issues or bottlenecks
- Implementing SLOs and monitoring SLIs
- Adding observability to existing Go applications
- Correlating logs, traces, and metrics for debugging

## Core Observability Principles

### The Three Pillars

1. **Traces**: Understand request flow across distributed systems
2. **Metrics**: Measure system behavior and performance over time
3. **Logs**: Record discrete events for debugging and audit

### Correlation Strategy

All three pillars must share common identifiers:
- **Trace ID**: Links all operations in a request
- **Span ID**: Identifies specific operation within trace
- **Request ID**: Correlates logs with traces and metrics

## OpenTelemetry Integration

### Installation

```bash
go get go.opentelemetry.io/otel
go get go.opentelemetry.io/otel/sdk
go get go.opentelemetry.io/otel/exporters/jaeger
go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp
```

### Basic Setup

```go
package main

import (
    "context"
    "log"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/jaeger"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
)

func initTracer(serviceName string) (*sdktrace.TracerProvider, error) {
    // Create Jaeger exporter
    exporter, err := jaeger.New(jaeger.WithCollectorEndpoint(
        jaeger.WithEndpoint("http://localhost:14268/api/traces"),
    ))
    if err != nil {
        return nil, err
    }

    // Create resource with service name
    res, err := resource.Merge(
        resource.Default(),
        resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceName(serviceName),
            semconv.ServiceVersion("1.0.0"),
        ),
    )
    if err != nil {
        return nil, err
    }

    // Create tracer provider
    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(res),
        sdktrace.WithSampler(sdktrace.AlwaysSample()), // Use probability sampler in production
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}

func main() {
    tp, err := initTracer("order-service")
    if err != nil {
        log.Fatal(err)
    }
    defer func() {
        if err := tp.Shutdown(context.Background()); err != nil {
            log.Printf("Error shutting down tracer: %v", err)
        }
    }()

    // Application code...
}
```

### Creating Spans

```go
import (
    "context"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/codes"
    "go.opentelemetry.io/otel/trace"
)

func ProcessOrder(ctx context.Context, order Order) error {
    tracer := otel.Tracer("order-service")
    ctx, span := tracer.Start(ctx, "ProcessOrder")
    defer span.End()

    // Add attributes
    span.SetAttributes(
        attribute.String("order.id", order.ID),
        attribute.Int("order.items", len(order.Items)),
        attribute.Float64("order.total", order.Total),
    )

    // Validate order (creates child span)
    if err := validateOrder(ctx, order); err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, "validation failed")
        return err
    }

    // Fulfill order
    if err := fulfillOrder(ctx, order); err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, "fulfillment failed")
        return err
    }

    span.SetStatus(codes.Ok, "order processed successfully")
    return nil
}

func validateOrder(ctx context.Context, order Order) error {
    _, span := otel.Tracer("order-service").Start(ctx, "validateOrder")
    defer span.End()

    // Validation logic...
    return nil
}
```

### HTTP Middleware Instrumentation

```go
import (
    "net/http"

    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

func main() {
    // Wrap handler with automatic tracing
    handler := http.HandlerFunc(orderHandler)
    wrappedHandler := otelhttp.NewHandler(handler, "order-handler")

    http.Handle("/orders", wrappedHandler)
    http.ListenAndServe(":8080", nil)
}

// Manual instrumentation for more control
func orderHandler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    tracer := otel.Tracer("order-service")

    ctx, span := tracer.Start(ctx, "orderHandler")
    defer span.End()

    // Extract order ID from request
    orderID := r.URL.Query().Get("id")
    span.SetAttributes(attribute.String("order.id", orderID))

    // Process order with propagated context
    order, err := fetchOrder(ctx, orderID)
    if err != nil {
        span.RecordError(err)
        http.Error(w, "Order not found", http.StatusNotFound)
        return
    }

    // ... handle response
}
```

## Prometheus Metrics

### Installation

```bash
go get github.com/prometheus/client_golang/prometheus
go get github.com/prometheus/client_golang/prometheus/promhttp
```

### Metric Types and Patterns

```go
package metrics

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    // Counter: Monotonically increasing value
    httpRequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "path", "status"},
    )

    // Gauge: Value that can go up or down
    activeConnections = promauto.NewGauge(
        prometheus.GaugeOpts{
            Name: "active_connections",
            Help: "Number of active connections",
        },
    )

    // Histogram: Observations bucketed by value
    httpRequestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets, // [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
        },
        []string{"method", "path"},
    )

    // Summary: Similar to histogram but calculates quantiles
    dbQueryDuration = promauto.NewSummaryVec(
        prometheus.SummaryOpts{
            Name:       "db_query_duration_seconds",
            Help:       "Database query duration",
            Objectives: map[float64]float64{0.5: 0.05, 0.9: 0.01, 0.99: 0.001},
        },
        []string{"query_type"},
    )
)
```

### Metrics Middleware

```go
import (
    "net/http"
    "strconv"
    "time"

    "github.com/prometheus/client_golang/prometheus/promhttp"
)

// Metrics middleware that instruments all HTTP handlers
func MetricsMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        // Track active connections
        activeConnections.Inc()
        defer activeConnections.Dec()

        // Wrap response writer to capture status code
        rw := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

        // Call next handler
        next.ServeHTTP(rw, r)

        // Record metrics
        duration := time.Since(start).Seconds()
        httpRequestDuration.WithLabelValues(r.Method, r.URL.Path).Observe(duration)
        httpRequestsTotal.WithLabelValues(r.Method, r.URL.Path, strconv.Itoa(rw.statusCode)).Inc()
    })
}

type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}

// Expose metrics endpoint
func main() {
    http.Handle("/metrics", promhttp.Handler())

    handler := MetricsMiddleware(http.HandlerFunc(orderHandler))
    http.Handle("/orders", handler)

    http.ListenAndServe(":8080", nil)
}
```

### Custom Metrics Example

```go
func ProcessPayment(ctx context.Context, payment Payment) error {
    timer := prometheus.NewTimer(dbQueryDuration.WithLabelValues("payment_insert"))
    defer timer.ObserveDuration()

    // Process payment
    if err := db.InsertPayment(payment); err != nil {
        httpRequestsTotal.WithLabelValues("POST", "/payments", "500").Inc()
        return err
    }

    httpRequestsTotal.WithLabelValues("POST", "/payments", "200").Inc()
    return nil
}
```

## Structured Logging with slog

### Basic Setup (Go 1.21+)

```go
package main

import (
    "context"
    "log/slog"
    "os"
)

func initLogger() *slog.Logger {
    // JSON logger for production
    handler := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
        AddSource: true, // Include file:line information
    })

    logger := slog.New(handler)
    slog.SetDefault(logger) // Set as default logger
    return logger
}

func main() {
    logger := initLogger()

    logger.Info("service starting",
        "service", "order-service",
        "version", "1.0.0",
        "port", 8080,
    )
}
```

### Context-Aware Logging

```go
import (
    "context"
    "log/slog"

    "go.opentelemetry.io/otel/trace"
)

// Add trace context to logger
func LoggerWithTrace(ctx context.Context) *slog.Logger {
    span := trace.SpanFromContext(ctx)
    spanCtx := span.SpanContext()

    return slog.With(
        "trace_id", spanCtx.TraceID().String(),
        "span_id", spanCtx.SpanID().String(),
    )
}

func HandleRequest(ctx context.Context, req Request) error {
    logger := LoggerWithTrace(ctx)

    logger.Info("processing request",
        "request_id", req.ID,
        "method", req.Method,
        "path", req.Path,
    )

    if err := processRequest(ctx, req); err != nil {
        logger.Error("request failed",
            "error", err,
            "duration_ms", time.Since(req.StartTime).Milliseconds(),
        )
        return err
    }

    logger.Info("request completed successfully",
        "duration_ms", time.Since(req.StartTime).Milliseconds(),
    )
    return nil
}
```

### Log Levels and Structured Fields

```go
func ProcessOrder(ctx context.Context, order Order) error {
    logger := LoggerWithTrace(ctx).With(
        "order_id", order.ID,
        "user_id", order.UserID,
    )

    logger.Debug("validating order", "items", len(order.Items))

    if len(order.Items) == 0 {
        logger.Warn("empty order received")
        return ErrEmptyOrder
    }

    logger.Info("order validation passed")

    if err := fulfillOrder(ctx, order); err != nil {
        logger.Error("fulfillment failed",
            "error", err,
            slog.Group("order_details",
                "total", order.Total,
                "items", len(order.Items),
            ),
        )
        return err
    }

    logger.Info("order processed successfully",
        "total", order.Total,
    )
    return nil
}
```

## Health Checks and Graceful Shutdown

### Health Check Endpoints

```go
import (
    "context"
    "database/sql"
    "encoding/json"
    "net/http"
    "time"
)

type HealthChecker struct {
    db *sql.DB
    // Add other dependencies
}

type HealthStatus struct {
    Status      string            `json:"status"`
    Version     string            `json:"version"`
    Checks      map[string]string `json:"checks"`
    Timestamp   time.Time         `json:"timestamp"`
}

// Liveness probe - is the app running?
func (hc *HealthChecker) LivenessHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{
        "status": "alive",
    })
}

// Readiness probe - is the app ready to serve traffic?
func (hc *HealthChecker) ReadinessHandler(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
    defer cancel()

    status := HealthStatus{
        Status:    "ready",
        Version:   "1.0.0",
        Checks:    make(map[string]string),
        Timestamp: time.Now(),
    }

    // Check database
    if err := hc.db.PingContext(ctx); err != nil {
        status.Status = "not_ready"
        status.Checks["database"] = "unhealthy: " + err.Error()
        w.WriteHeader(http.StatusServiceUnavailable)
    } else {
        status.Checks["database"] = "healthy"
    }

    // Add more dependency checks (Redis, external APIs, etc.)

    w.Header().Set("Content-Type", "application/json")
    if status.Status == "ready" {
        w.WriteHeader(http.StatusOK)
    }
    json.NewEncoder(w).Encode(status)
}
```

### Graceful Shutdown

```go
import (
    "context"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    // Initialize tracer
    tp, err := initTracer("order-service")
    if err != nil {
        log.Fatal(err)
    }

    // Setup HTTP server
    server := &http.Server{
        Addr:    ":8080",
        Handler: setupRoutes(),
    }

    // Channel for shutdown signals
    shutdown := make(chan os.Signal, 1)
    signal.Notify(shutdown, os.Interrupt, syscall.SIGTERM)

    // Start server in goroutine
    go func() {
        slog.Info("server starting", "port", 8080)
        if err := server.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatal(err)
        }
    }()

    // Wait for shutdown signal
    <-shutdown
    slog.Info("shutdown signal received")

    // Create shutdown context with timeout
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    // Shutdown HTTP server
    slog.Info("shutting down HTTP server")
    if err := server.Shutdown(ctx); err != nil {
        slog.Error("HTTP server shutdown error", "error", err)
    }

    // Shutdown tracer provider (flush spans)
    slog.Info("shutting down tracer")
    if err := tp.Shutdown(ctx); err != nil {
        slog.Error("tracer shutdown error", "error", err)
    }

    slog.Info("shutdown complete")
}
```

## Complete Instrumentation Example

```go
package main

import (
    "context"
    "database/sql"
    "log/slog"
    "net/http"
    "os"
    "time"

    "github.com/prometheus/client_golang/prometheus/promhttp"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
)

type Server struct {
    db     *sql.DB
    logger *slog.Logger
}

func (s *Server) orderHandler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    // Get tracer and create span
    tracer := otel.Tracer("order-service")
    ctx, span := tracer.Start(ctx, "orderHandler")
    defer span.End()

    // Create context-aware logger with trace ID
    logger := s.logger.With(
        "trace_id", span.SpanContext().TraceID().String(),
        "request_id", r.Header.Get("X-Request-ID"),
    )

    orderID := r.URL.Query().Get("id")
    span.SetAttributes(attribute.String("order.id", orderID))

    logger.Info("fetching order", "order_id", orderID)

    // Fetch order from database
    order, err := s.fetchOrder(ctx, orderID)
    if err != nil {
        span.RecordError(err)
        logger.Error("failed to fetch order", "error", err)
        http.Error(w, "Order not found", http.StatusNotFound)
        return
    }

    logger.Info("order fetched successfully",
        "order_id", orderID,
        "items", len(order.Items),
    )

    // Return order as JSON
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(order)
}

func (s *Server) fetchOrder(ctx context.Context, orderID string) (*Order, error) {
    _, span := otel.Tracer("order-service").Start(ctx, "fetchOrder")
    defer span.End()

    // Time database query
    start := time.Now()

    var order Order
    err := s.db.QueryRowContext(ctx, "SELECT * FROM orders WHERE id = ?", orderID).Scan(&order)

    duration := time.Since(start).Seconds()
    dbQueryDuration.WithLabelValues("select_order").Observe(duration)

    return &order, err
}

func setupRoutes(s *Server, hc *HealthChecker) http.Handler {
    mux := http.NewServeMux()

    // Health endpoints (no tracing needed)
    mux.HandleFunc("/health", hc.LivenessHandler)
    mux.HandleFunc("/ready", hc.ReadinessHandler)
    mux.Handle("/metrics", promhttp.Handler())

    // Business endpoints (with tracing)
    orderHandler := http.HandlerFunc(s.orderHandler)
    mux.Handle("/orders", otelhttp.NewHandler(orderHandler, "orders"))

    // Wrap everything with metrics middleware
    return MetricsMiddleware(mux)
}
```

## Decision Trees

### When to Use OpenTelemetry

**Use OpenTelemetry When:**
- Building distributed systems with multiple services
- Need to trace requests across service boundaries
- Debugging performance issues in microservices
- Want vendor-neutral observability (switch backends easily)
- Require correlation between traces, metrics, and logs

**Don't Use OpenTelemetry When:**
- Building simple monolithic applications
- Performance overhead is critical (consider sampling)
- Team lacks observability infrastructure (Jaeger, Zipkin)

### When to Use Prometheus

**Use Prometheus When:**
- Need time-series metrics for monitoring and alerting
- Building operational dashboards (Grafana)
- Measuring SLIs for SLO compliance
- Tracking business metrics (requests/sec, conversion rates)
- Kubernetes/containerized environments

**Don't Use Prometheus When:**
- Need high-cardinality metrics (Prometheus has limits)
- Require long-term metric storage (use Thanos/Cortex)
- Need push-based metrics (Prometheus is pull-based)

### When to Use slog

**Use slog When:**
- Go 1.21+ projects (standard library, zero dependencies)
- Need structured logging with JSON output
- Want high-performance logging with minimal allocations
- Integrating with log aggregation systems (Loki, ELK)

**Don't Use slog When:**
- Go < 1.21 (use zap or zerolog instead)
- Need complex log routing or filtering (use zap)
- Require very specific features (audit trails, etc.)

### Sampling Strategy Decision

**Always Sample When:**
- Development/staging environments
- Total traffic < 100 requests/sec
- Debugging specific issues

**Probabilistic Sampling When:**
- Production with moderate traffic (100-10K req/sec)
- Sample rate: 1-10% typically

**Tail-Based Sampling When:**
- High traffic production (>10K req/sec)
- Only sample errors and slow requests
- Requires tail-sampling processor (OpenTelemetry Collector)

## Anti-Patterns to Avoid

### ❌ Not Propagating Context

**WRONG: Breaking trace context**
```go
func processOrder(order Order) error {
    // Creates new context, loses trace!
    ctx := context.Background()
    return validateOrder(ctx, order)
}
```

**CORRECT: Propagate context through call chain**
```go
func processOrder(ctx context.Context, order Order) error {
    // Propagates trace context
    return validateOrder(ctx, order)
}
```

### ❌ Cardinality Explosion

**WRONG: Unbounded label values**
```go
// user_id can have millions of values!
httpRequests.WithLabelValues(r.Method, r.URL.Path, userID).Inc()
```

**CORRECT: Use bounded labels**
```go
// Only method and path (bounded values)
httpRequests.WithLabelValues(r.Method, r.URL.Path).Inc()
// Track user-specific metrics separately if needed
```

### ❌ Logging Sensitive Data

**WRONG: Exposing PII and secrets**
```go
logger.Info("user login",
    "email", user.Email,        // PII!
    "password", user.Password,  // CRITICAL!
    "token", authToken,         // SECRET!
)
```

**CORRECT: Redact sensitive information**
```go
logger.Info("user login",
    "user_id", user.ID,  // Safe identifier
    "method", "password",
)
```

### ❌ Not Closing Spans

**WRONG: Span leaks memory**
```go
func processOrder(ctx context.Context) error {
    ctx, span := tracer.Start(ctx, "processOrder")
    // Missing defer span.End()!

    if err := validate(); err != nil {
        return err  // Span never closed!
    }

    return nil
}
```

**CORRECT: Always defer span.End()**
```go
func processOrder(ctx context.Context) error {
    ctx, span := tracer.Start(ctx, "processOrder")
    defer span.End()  // Always runs

    if err := validate(); err != nil {
        span.RecordError(err)
        return err
    }

    return nil
}
```

### ❌ Synchronous Metric Export

**WRONG: Blocking requests with metric export**
```go
// Synchronous export blocks HTTP handler
exporter := jaeger.New(jaeger.WithCollectorEndpoint(...))
tp := sdktrace.NewTracerProvider(
    sdktrace.WithSyncer(exporter),  // BAD: Synchronous!
)
```

**CORRECT: Use batching for async export**
```go
// Batching exports asynchronously
tp := sdktrace.NewTracerProvider(
    sdktrace.WithBatcher(exporter),  // GOOD: Async batching
)
```

### ❌ Missing Graceful Shutdown

**WRONG: Losing traces on shutdown**
```go
func main() {
    tp, _ := initTracer("service")
    // Missing shutdown - spans lost!
    http.ListenAndServe(":8080", nil)
}
```

**CORRECT: Shutdown exporters properly**
```go
func main() {
    tp, _ := initTracer("service")
    defer tp.Shutdown(context.Background())

    // Handle signals and graceful shutdown
    server.ListenAndServe()
}
```

## Best Practices

1. **Context Propagation**: Always pass `context.Context` through call chains
2. **Bounded Labels**: Keep metric label cardinality under 1000 combinations
3. **Sampling**: Use probabilistic sampling in high-traffic production
4. **Correlation IDs**: Include trace_id in logs for correlation
5. **Health Checks**: Implement both `/health` (liveness) and `/ready` (readiness)
6. **Graceful Shutdown**: Flush traces and metrics before exit
7. **Error Recording**: Use `span.RecordError()` for automatic error tracking
8. **Metric Naming**: Follow Prometheus naming conventions (`_total`, `_seconds`)
9. **Log Levels**: Use appropriate levels (Debug, Info, Warn, Error)
10. **Auto-Instrumentation**: Use middleware for HTTP/gRPC when possible

## Metric Naming Conventions

Follow Prometheus best practices:

**Counter Metrics** (always increasing):
- `http_requests_total` (not `http_requests`)
- `payment_transactions_total`
- `errors_total`

**Gauge Metrics** (can go up or down):
- `active_connections`
- `queue_size`
- `memory_usage_bytes`

**Histogram/Summary Metrics** (observations):
- `http_request_duration_seconds` (not `_milliseconds`)
- `db_query_duration_seconds`
- `response_size_bytes`

**Label Naming**:
- Use `method`, not `http_method`
- Use `status`, not `status_code` or `http_status`
- Use snake_case, not camelCase

## Resources

**Official Documentation:**
- OpenTelemetry Go: https://opentelemetry.io/docs/instrumentation/go/
- Prometheus Client Library: https://github.com/prometheus/client_golang
- Go slog Package: https://pkg.go.dev/log/slog

**Recent Guides (2025):**
- "Observability in Go: What Real Engineers Are Saying in 2025" (Quesma Blog)
- "Monitoring Go Apps with OpenTelemetry Metrics" (Better Stack, 2025)
- Prometheus Best Practices: https://prometheus.io/docs/practices/naming/

**Related Skills:**
- **golang-web-frameworks**: HTTP server patterns and middleware
- **golang-testing-strategies**: Testing instrumented code
- **verification-before-completion**: Validating observability setup

## Quick Reference

### Initialize OpenTelemetry
```go
tp, _ := initTracer("service-name")
defer tp.Shutdown(context.Background())
```

### Create Spans
```go
ctx, span := otel.Tracer("name").Start(ctx, "operation")
defer span.End()
span.SetAttributes(attribute.String("key", "value"))
```

### Define Metrics
```go
counter := promauto.NewCounterVec(opts, []string{"label"})
histogram := promauto.NewHistogramVec(opts, []string{"label"})
```

### Structured Logging
```go
logger := slog.With("trace_id", traceID)
logger.Info("message", "key", value)
```

### Health Checks
```go
http.HandleFunc("/health", livenessHandler)
http.HandleFunc("/ready", readinessHandler)
```

---

**Token Estimate**: ~5,000 tokens (entry point + full content)
**Version**: 1.0.0
**Last Updated**: 2025-12-03
