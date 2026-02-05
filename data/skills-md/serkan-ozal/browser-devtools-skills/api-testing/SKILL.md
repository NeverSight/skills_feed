---
name: api-testing
description: Test API integrations by mocking responses, intercepting requests, and monitoring network traffic. Use when the user wants to mock backend APIs, simulate errors, test offline behavior, intercept requests, or add authentication headers.
allowed-tools: Bash(browser-devtools-cli:*)
---

# API Testing Skill

Test API integrations by mocking responses, intercepting requests, and monitoring network traffic.

## When to Use

This skill activates when:
- User wants to test API integrations
- User needs to mock backend responses
- User wants to simulate error scenarios
- User asks about request interception
- User needs to test offline behavior

## Capabilities

### Response Mocking
```bash
browser-devtools-cli stub mock-http-response \
  --pattern "**/api/users" \
  --response '{"action":"fulfill","status":200,"body":[{"id":1,"name":"Test"}]}'
```

### Request Interception
```bash
browser-devtools-cli stub intercept-http-request \
  --pattern "**/api/**" \
  --modifications '{"headers":{"Authorization":"Bearer token"}}'
```

### Network Monitoring
```bash
browser-devtools-cli --json o11y get-http-requests
browser-devtools-cli --json o11y get-http-requests --resource-type fetch,xhr
browser-devtools-cli --json o11y get-http-requests --status-min 400
```

### Stub Management
```bash
browser-devtools-cli stub list
browser-devtools-cli stub clear --stub-id <id>
browser-devtools-cli stub clear --all
```

## Common Scenarios

### Mock Successful Response
```bash
browser-devtools-cli stub mock-http-response \
  --pattern "**/api/users" \
  --response '{"action":"fulfill","status":200,"body":[{"id":1,"name":"Test"}]}'
```

### Simulate Server Error
```bash
browser-devtools-cli stub mock-http-response \
  --pattern "**/api/checkout" \
  --response '{"action":"fulfill","status":500,"body":{"error":"Internal Server Error"}}'
```

### Simulate 404 Not Found
```bash
browser-devtools-cli stub mock-http-response \
  --pattern "**/api/missing" \
  --response '{"action":"fulfill","status":404,"body":{"error":"Not Found"}}'
```

### Simulate Network Timeout
```bash
browser-devtools-cli stub mock-http-response \
  --pattern "**/api/slow-endpoint" \
  --response '{"action":"abort","abortErrorCode":"timedout"}'
```

### Simulate Connection Failed
```bash
browser-devtools-cli stub mock-http-response \
  --pattern "**/api/offline" \
  --response '{"action":"abort","abortErrorCode":"connectionfailed"}'
```

### Add Auth Header
```bash
browser-devtools-cli stub intercept-http-request \
  --pattern "**/api/**" \
  --modifications '{"headers":{"Authorization":"Bearer test-token"}}'
```

### Modify Request Body
```bash
browser-devtools-cli stub intercept-http-request \
  --pattern "**/api/submit" \
  --modifications '{"body":{"injected":"value"}}'
```

### Add Delay
```bash
browser-devtools-cli stub mock-http-response \
  --pattern "**/api/slow" \
  --response '{"action":"fulfill","status":200,"body":{}}' \
  --delay-ms 3000
```

### Simulate Flaky API
```bash
browser-devtools-cli stub mock-http-response \
  --pattern "**/api/unreliable" \
  --response '{"action":"fulfill","status":503}' \
  --chance 0.3
```

### One-Shot Mock
```bash
browser-devtools-cli stub mock-http-response \
  --pattern "**/api/once" \
  --response '{"action":"fulfill","status":200,"body":{"first":true}}' \
  --times 1
```

## Testing Workflow

```bash
SESSION="--session-id api-test"

# 1. Setup mocks before navigation
browser-devtools-cli $SESSION stub mock-http-response \
  --pattern "**/api/users" \
  --response '{"action":"fulfill","status":200,"body":[{"id":1,"name":"Mock User"}]}'

# 2. Navigate to application
browser-devtools-cli $SESSION navigation go-to --url "https://app.example.com"
browser-devtools-cli $SESSION sync wait-for-network-idle

# 3. Interact with the app
browser-devtools-cli $SESSION interaction click --selector "#load-users"
browser-devtools-cli $SESSION sync wait-for-network-idle

# 4. Check network requests
browser-devtools-cli $SESSION --json o11y get-http-requests

# 5. Verify UI shows mocked data
browser-devtools-cli $SESSION content get-as-text --selector ".user-list"

# 6. List active stubs
browser-devtools-cli $SESSION stub list

# 7. Clear all stubs
browser-devtools-cli $SESSION stub clear --all

# 8. Cleanup
browser-devtools-cli session delete api-test
```

## Error Testing Workflow

```bash
SESSION="--session-id error-test"

# Mock error response
browser-devtools-cli $SESSION stub mock-http-response \
  --pattern "**/api/checkout" \
  --response '{"action":"fulfill","status":500,"body":{"error":"Payment failed"}}'

# Navigate and trigger error
browser-devtools-cli $SESSION navigation go-to --url "https://app.example.com/checkout"
browser-devtools-cli $SESSION interaction click --selector "#pay-button"
browser-devtools-cli $SESSION sync wait-for-network-idle

# Check error handling in UI
browser-devtools-cli $SESSION content take-screenshot --name "error-state"
browser-devtools-cli $SESSION content get-as-text --selector ".error-message"

# Cleanup
browser-devtools-cli $SESSION stub clear --all
browser-devtools-cli session delete error-test
```

## Best Practices

1. **Use specific patterns** to avoid mocking unintended requests
2. **Clear stubs after tests** to prevent interference
3. **List stubs** to debug unexpected behavior
4. **Use times limit** for one-shot mocks
5. **Add delays** to test loading states
6. **Test error scenarios** not just happy paths
7. **Set up mocks before navigation** for first-load testing
8. **Monitor actual requests** to verify mocks are working
