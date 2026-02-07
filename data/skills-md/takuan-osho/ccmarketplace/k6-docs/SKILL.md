---
name: k6-docs
description: Use this skill when writing or debugging Grafana k6 load testing code. Provides access to the latest official k6 documentation including API references, examples, and best practices for creating performance tests.
---

# Grafana k6 Documentation Access

## Overview

This skill enables access to the latest official Grafana k6 documentation for writing and debugging load testing scripts. k6 is a modern load testing tool built for performance testing APIs, microservices, and websites.

## When to Use This Skill

Use this skill when:
- Writing new k6 load testing scripts
- Debugging existing k6 test code
- Looking up k6 API methods and their parameters
- Understanding k6 test lifecycle hooks
- Learning about k6 metrics and thresholds
- Implementing k6 checks and custom metrics
- Using k6 extensions or modules
- Troubleshooting k6 test execution issues

## Core Capabilities

### 1. Documentation Access

Access the latest k6 documentation using the WebFetch tool:

**Primary documentation URLs:**
- Main documentation: https://grafana.com/docs/k6/latest/
- JavaScript API: https://grafana.com/docs/k6/latest/javascript-api/
- Examples: https://grafana.com/docs/k6/latest/examples/
- Using k6: https://grafana.com/docs/k6/latest/using-k6/

**Common API reference URLs:**
- HTTP requests: https://grafana.com/docs/k6/latest/javascript-api/k6-http/
- Checks: https://grafana.com/docs/k6/latest/javascript-api/k6/check/
- Metrics: https://grafana.com/docs/k6/latest/javascript-api/k6-metrics/
- Thresholds: https://grafana.com/docs/k6/latest/using-k6/thresholds/
- Options: https://grafana.com/docs/k6/latest/using-k6/k6-options/
- Execution contexts: https://grafana.com/docs/k6/latest/using-k6/test-lifecycle/

**Usage pattern:**
```
Use WebFetch with the appropriate documentation URL and a focused prompt like:
- "Show me the API reference for http.post method"
- "Explain how to use checks in k6"
- "Show examples of custom metrics"
```

### 2. Common k6 Patterns

**Basic HTTP GET test:**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  const res = http.get('https://test.k6.io');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);
}
```

**HTTP POST with JSON:**
```javascript
import http from 'k6/http';
import { check } from 'k6';

export default function () {
  const url = 'https://httpbin.test.k6.io/post';
  const payload = JSON.stringify({
    name: 'test',
  });
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(url, payload, params);
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}
```

### 3. Documentation Search Strategy

When searching for specific k6 functionality:

1. **Start broad**: Use WebSearch to find relevant documentation pages
   - Example: "k6 load testing custom metrics documentation"

2. **Then go specific**: Use WebFetch on the most relevant documentation URL
   - Example: WebFetch https://grafana.com/docs/k6/latest/javascript-api/k6-metrics/

3. **For API methods**: Navigate to the JavaScript API section
   - Base URL: https://grafana.com/docs/k6/latest/javascript-api/
   - Module-specific: https://grafana.com/docs/k6/latest/javascript-api/k6-http/

4. **For how-to guides**: Check the "Using k6" section
   - Base URL: https://grafana.com/docs/k6/latest/using-k6/

### 4. Key k6 Concepts

**Test lifecycle:**
- `init` context: Load-time code (imports, options)
- `setup()`: Runs once before tests
- `default function()`: VU code, runs repeatedly
- `teardown()`: Runs once after tests

**Load options:**
- `vus`: Number of virtual users
- `duration`: Test duration
- `iterations`: Total iterations across all VUs
- `stages`: Ramping pattern
- `thresholds`: Pass/fail criteria

**HTTP methods:**
- `http.get()`, `http.post()`, `http.put()`, `http.delete()`
- `http.batch()` for parallel requests

**Checks vs Thresholds:**
- `check()`: Validates conditions, doesn't stop test
- `thresholds`: Define pass/fail criteria, can abort test

## Workflow

1. **Identify the need**: Determine what k6 functionality is required
2. **Search documentation**: Use WebSearch or directly access known doc URLs
3. **Fetch specific pages**: Use WebFetch to get detailed information
4. **Implement code**: Write k6 test code based on documentation
5. **Validate**: Check against examples and best practices in docs

## Best Practices

- Always check the latest documentation URL structure (grafana.com/docs/k6/latest/)
- For complex scenarios, look for examples in the Examples section
- When troubleshooting, check both the API reference and the Using k6 guides
- Use WebSearch first if unsure which documentation page to fetch
- Reference multiple documentation pages if implementing complex features

## Common Documentation Sections

| Topic | URL Pattern |
|-------|-------------|
| Main docs | https://grafana.com/docs/k6/latest/ |
| JavaScript API | https://grafana.com/docs/k6/latest/javascript-api/{module}/ |
| HTTP module | https://grafana.com/docs/k6/latest/javascript-api/k6-http/ |
| Examples | https://grafana.com/docs/k6/latest/examples/ |
| Test lifecycle | https://grafana.com/docs/k6/latest/using-k6/test-lifecycle/ |
| Thresholds | https://grafana.com/docs/k6/latest/using-k6/thresholds/ |
| Options | https://grafana.com/docs/k6/latest/using-k6/k6-options/ |
| Metrics | https://grafana.com/docs/k6/latest/using-k6/metrics/ |
| Checks | https://grafana.com/docs/k6/latest/javascript-api/k6/check/ |

## Notes

- This skill does not bundle k6 documentation locally; it fetches the latest version online
- Always verify that fetched documentation is current by checking the URL includes `/latest/`
- For version-specific documentation, replace `/latest/` with the specific version number
- k6 documentation is comprehensive and well-organized; use the table of contents for navigation
