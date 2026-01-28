---
name: performance
description: Production-grade performance testing skill with k6, JMeter, load testing, stress testing, and performance optimization guidance
sasmp_version: "1.3.0"
bonded_agent: qa-expert
bond_type: PRIMARY_BOND
version: "2.1.0"
---

# Performance Testing Skill

## Overview

Enterprise-grade performance testing capabilities for load, stress, spike, and soak testing with actionable optimization recommendations.

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["create_test", "analyze_results", "optimize", "benchmark", "generate_report"],
      "description": "Performance action to perform"
    },
    "test_type": {
      "type": "string",
      "enum": ["load", "stress", "spike", "soak", "capacity", "baseline"],
      "description": "Type of performance test"
    },
    "tool": {
      "type": "string",
      "enum": ["k6", "jmeter", "gatling", "locust", "artillery"],
      "default": "k6"
    },
    "target": {
      "type": "object",
      "properties": {
        "url": {"type": "string", "format": "uri"},
        "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]},
        "headers": {"type": "object"},
        "body": {"type": "object"}
      },
      "required": ["url"]
    },
    "load_profile": {
      "type": "object",
      "properties": {
        "vus": {"type": "integer", "minimum": 1, "maximum": 10000},
        "duration": {"type": "string", "pattern": "^[0-9]+[smh]$"},
        "ramp_up": {"type": "string"},
        "ramp_down": {"type": "string"}
      }
    },
    "thresholds": {
      "type": "object",
      "properties": {
        "p95_response_time_ms": {"type": "integer"},
        "p99_response_time_ms": {"type": "integer"},
        "error_rate_percent": {"type": "number"},
        "throughput_rps": {"type": "integer"}
      }
    }
  },
  "required": ["action"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "status": {"type": "string", "enum": ["success", "partial", "failed"]},
    "script": {"type": "string", "description": "Generated test script"},
    "results": {
      "type": "object",
      "properties": {
        "p50_ms": {"type": "number"},
        "p95_ms": {"type": "number"},
        "p99_ms": {"type": "number"},
        "avg_ms": {"type": "number"},
        "min_ms": {"type": "number"},
        "max_ms": {"type": "number"},
        "throughput_rps": {"type": "number"},
        "error_rate": {"type": "number"},
        "total_requests": {"type": "integer"}
      }
    },
    "recommendations": {"type": "array", "items": {"type": "string"}},
    "bottlenecks": {"type": "array", "items": {"type": "string"}}
  }
}
```

## Parameter Validation

```yaml
load_profile.vus:
  required: false
  default: 10
  validate:
    - type: range
      min: 1
      max: 10000
    - type: resource_check
      warn_above: 1000

load_profile.duration:
  required: false
  default: "1m"
  validate:
    - type: pattern
      regex: "^[0-9]+[smh]$"
    - type: range
      min: "10s"
      max: "24h"

thresholds.p95_response_time_ms:
  required: false
  default: 500
  validate:
    - type: range
      min: 10
      max: 60000

thresholds.error_rate_percent:
  required: false
  default: 1.0
  validate:
    - type: range
      min: 0
      max: 100
```

## Error Handling

```yaml
retry_config:
  strategy: exponential_backoff
  max_retries: 3
  base_delay_ms: 2000
  max_delay_ms: 30000
  retryable_errors:
    - NETWORK_TIMEOUT
    - TARGET_UNAVAILABLE
    - RATE_LIMITED

error_categories:
  target_errors:
    - TARGET_UNAVAILABLE
    - DNS_RESOLUTION_FAILED
    - SSL_HANDSHAKE_FAILED
    recovery: verify_target_health

  resource_errors:
    - MEMORY_EXHAUSTED
    - CPU_THROTTLED
    - SOCKET_LIMIT_REACHED
    recovery: reduce_load_profile

  threshold_errors:
    - P95_EXCEEDED
    - ERROR_RATE_EXCEEDED
    - THROUGHPUT_BELOW_TARGET
    recovery: analyze_bottlenecks

  tool_errors:
    - TOOL_NOT_INSTALLED
    - CONFIG_INVALID
    - SCRIPT_SYNTAX_ERROR
    recovery: validate_configuration
```

## Test Type Definitions

### Load Test
```yaml
purpose: Validate system under expected load
load_profile:
  pattern: ramp_up_sustain_ramp_down
  typical_vus: 100-500
  typical_duration: 15-30min
success_criteria:
  - Response time within SLA
  - Error rate < 1%
  - No resource exhaustion
```

### Stress Test
```yaml
purpose: Find breaking point
load_profile:
  pattern: stepped_increase
  typical_vus: 100-5000 (stepped)
  typical_duration: 30-60min
success_criteria:
  - Identify breaking point
  - Graceful degradation
  - Recovery after load reduction
```

### Spike Test
```yaml
purpose: Validate sudden traffic surge
load_profile:
  pattern: sudden_spike
  typical_vus: 10 -> 1000 -> 10
  typical_duration: 5-15min
success_criteria:
  - System survives spike
  - Quick recovery
  - No data loss
```

### Soak Test
```yaml
purpose: Identify memory leaks, resource issues
load_profile:
  pattern: sustained_load
  typical_vus: 50-200
  typical_duration: 4-24 hours
success_criteria:
  - Stable memory usage
  - No performance degradation
  - Consistent response times
```

## Code Templates

### k6 Load Test
```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const responseTime = new Trend('response_time');

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up
    { duration: '5m', target: 100 },  // Sustain
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    errors: ['rate<0.01'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/endpoint', {
    headers: {
      'Authorization': `Bearer ${__ENV.API_TOKEN}`,
      'Content-Type': 'application/json',
    },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'body contains expected': (r) => r.body.includes('success'),
  });

  errorRate.add(res.status !== 200);
  responseTime.add(res.timings.duration);

  sleep(1);
}

export function handleSummary(data) {
  return {
    'summary.json': JSON.stringify(data),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}
```

### k6 Stress Test with Steps
```javascript
// stress-test.js
export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '2m', target: 300 },
    { duration: '5m', target: 300 },
    { duration: '2m', target: 400 },
    { duration: '5m', target: 400 },
    { duration: '5m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(99)<2000'],
    http_req_failed: ['rate<0.05'],
  },
};
```

## Troubleshooting

### Issue: High Response Times
```yaml
symptoms:
  - P95 > threshold
  - Increasing latency under load
  - Timeouts

diagnosis:
  1. Check database query performance
  2. Review connection pooling
  3. Analyze network latency
  4. Profile application code
  5. Check external service calls

solutions:
  - Add database indexes
  - Increase connection pool size
  - Implement caching
  - Optimize slow queries
  - Add CDN for static content
```

### Issue: High Error Rate
```yaml
symptoms:
  - 5xx errors under load
  - Connection refused
  - Timeout errors

diagnosis:
  1. Check server resource utilization
  2. Review application logs
  3. Analyze error distribution
  4. Check rate limiting
  5. Verify infrastructure capacity

solutions:
  - Scale horizontally
  - Increase resource limits
  - Implement circuit breaker
  - Add retry logic with backoff
  - Review rate limit settings
```

### Issue: Resource Exhaustion
```yaml
symptoms:
  - Memory growing continuously
  - CPU at 100%
  - Open file descriptor limit

diagnosis:
  1. Monitor resource metrics during test
  2. Profile memory allocation
  3. Check for connection leaks
  4. Review garbage collection

solutions:
  - Fix memory leaks
  - Optimize resource usage
  - Increase limits
  - Implement connection pooling
  - Add resource cleanup
```

## Performance Benchmarks

```yaml
web_api:
  p50: < 100ms
  p95: < 500ms
  p99: < 1000ms
  error_rate: < 0.1%
  throughput: > 100 RPS

database_query:
  simple_select: < 10ms
  complex_join: < 100ms
  aggregation: < 500ms

page_load:
  first_contentful_paint: < 1.5s
  time_to_interactive: < 3s
  largest_contentful_paint: < 2.5s
```

## Best Practices

```yaml
test_design:
  - Start with baseline test
  - Use realistic load profiles
  - Include think time
  - Test with production-like data

execution:
  - Run from multiple locations
  - Monitor target resources
  - Capture detailed metrics
  - Record for replay/debug

analysis:
  - Compare against baseline
  - Focus on percentiles not averages
  - Identify bottlenecks
  - Document findings

optimization:
  - Fix one issue at a time
  - Re-test after each change
  - Track improvement trends
  - Set realistic targets
```

## Logging & Observability

```yaml
log_events:
  - test_started
  - test_completed
  - threshold_exceeded
  - error_spike_detected

metrics:
  - requests_per_second
  - response_time_percentiles
  - error_rate
  - concurrent_users

alerts:
  - p95 > threshold
  - error_rate > 5%
  - throughput < baseline
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2025-01 | Production-grade with full error handling |
| 2.0.0 | 2024-12 | SASMP v1.3.0 compliance |
| 1.0.0 | 2024-11 | Initial release |
