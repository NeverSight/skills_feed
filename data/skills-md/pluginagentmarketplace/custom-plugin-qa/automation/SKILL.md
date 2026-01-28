---
name: automation
description: Production-grade test automation skill covering Selenium, Cypress, Playwright, Appium with POM architecture, retry logic, and CI/CD integration
sasmp_version: "1.3.0"
bonded_agent: qa-expert
bond_type: PRIMARY_BOND
version: "2.1.0"
---

# Test Automation Skill

## Overview

Enterprise-grade test automation capabilities for web, mobile, and API testing with production-ready patterns.

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["create_test", "debug_test", "optimize", "migrate", "generate_report"],
      "description": "Automation action to perform"
    },
    "framework": {
      "type": "string",
      "enum": ["selenium", "cypress", "playwright", "appium", "webdriverio"],
      "description": "Target automation framework"
    },
    "language": {
      "type": "string",
      "enum": ["javascript", "typescript", "python", "java", "csharp"],
      "default": "typescript"
    },
    "test_type": {
      "type": "string",
      "enum": ["e2e", "integration", "component", "visual", "accessibility"]
    },
    "target": {
      "type": "object",
      "properties": {
        "url": {"type": "string", "format": "uri"},
        "selector": {"type": "string"},
        "page_name": {"type": "string"}
      }
    }
  },
  "required": ["action", "framework"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "status": {"type": "string", "enum": ["success", "partial", "failed"]},
    "code": {"type": "string", "description": "Generated test code"},
    "file_path": {"type": "string"},
    "dependencies": {"type": "array", "items": {"type": "string"}},
    "setup_commands": {"type": "array", "items": {"type": "string"}},
    "warnings": {"type": "array", "items": {"type": "string"}},
    "best_practices": {"type": "array", "items": {"type": "string"}}
  }
}
```

## Parameter Validation

```yaml
framework:
  required: true
  validate:
    - type: enum
      values: [selenium, cypress, playwright, appium, webdriverio]
    - type: compatibility_check
      with: language

language:
  required: false
  default: typescript
  validate:
    - type: enum
      values: [javascript, typescript, python, java, csharp]

target.url:
  required: false
  validate:
    - type: format
      pattern: "^https?://"
    - type: reachability_check
      timeout_ms: 5000

target.selector:
  required: false
  validate:
    - type: selector_syntax
      formats: [css, xpath, data-testid]
```

## Error Handling

```yaml
retry_config:
  strategy: exponential_backoff
  max_retries: 5
  base_delay_ms: 1000
  max_delay_ms: 30000
  jitter: true
  retryable_errors:
    - ELEMENT_NOT_FOUND
    - TIMEOUT
    - STALE_ELEMENT
    - NETWORK_ERROR

error_categories:
  locator_errors:
    - ELEMENT_NOT_FOUND
    - ELEMENT_NOT_VISIBLE
    - ELEMENT_NOT_INTERACTABLE
    recovery: suggest_alternative_locators

  timing_errors:
    - TIMEOUT
    - STALE_ELEMENT
    - ANIMATION_NOT_COMPLETE
    recovery: increase_wait_add_retry

  framework_errors:
    - DRIVER_NOT_FOUND
    - BROWSER_CRASH
    - SESSION_EXPIRED
    recovery: restart_session

  environment_errors:
    - NETWORK_ERROR
    - SSL_ERROR
    - PROXY_ERROR
    recovery: check_environment_config
```

## Capabilities

### Selenium WebDriver
```yaml
languages: [java, python, javascript, csharp]
browsers: [chrome, firefox, safari, edge]
features:
  - Cross-browser testing
  - Grid support
  - Mobile emulation
  - Screenshot capture
  - Video recording (with plugins)
```

### Cypress
```yaml
languages: [javascript, typescript]
browsers: [chrome, firefox, edge, electron]
features:
  - Time-travel debugging
  - Automatic waiting
  - Network stubbing
  - Component testing
  - Visual testing (plugins)
```

### Playwright
```yaml
languages: [javascript, typescript, python, java, csharp]
browsers: [chromium, firefox, webkit]
features:
  - Multi-browser parallel
  - Auto-wait
  - Tracing
  - Mobile emulation
  - API testing
```

### Appium
```yaml
languages: [java, python, javascript]
platforms: [ios, android]
features:
  - Native app testing
  - Hybrid app testing
  - Mobile web testing
  - Gestures support
```

## Code Templates

### Page Object Model (TypeScript/Playwright)
```typescript
// pages/BasePage.ts
export abstract class BasePage {
  constructor(protected page: Page) {}

  async waitForPageLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }

  protected async click(selector: string): Promise<void> {
    await this.page.click(selector, { timeout: 10000 });
  }

  protected async fill(selector: string, value: string): Promise<void> {
    await this.page.fill(selector, value);
  }

  protected async getText(selector: string): Promise<string> {
    return await this.page.textContent(selector) || '';
  }
}

// pages/LoginPage.ts
export class LoginPage extends BasePage {
  private selectors = {
    email: '[data-testid="email-input"]',
    password: '[data-testid="password-input"]',
    submit: '[data-testid="login-button"]',
    error: '[data-testid="error-message"]'
  };

  async login(email: string, password: string): Promise<void> {
    await this.fill(this.selectors.email, email);
    await this.fill(this.selectors.password, password);
    await this.click(this.selectors.submit);
  }

  async getErrorMessage(): Promise<string> {
    return await this.getText(this.selectors.error);
  }
}
```

### Test with Retry Pattern
```typescript
// utils/retry.ts
export async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    baseDelayMs?: number;
    maxDelayMs?: number;
  } = {}
): Promise<T> {
  const { maxRetries = 3, baseDelayMs = 1000, maxDelayMs = 10000 } = options;

  let lastError: Error;
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      const delay = Math.min(baseDelayMs * Math.pow(2, attempt), maxDelayMs);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw lastError!;
}
```

## Troubleshooting

### Issue: Element Not Found
```yaml
symptoms:
  - TimeoutError waiting for selector
  - Element not visible
  - Stale element reference

diagnosis:
  1. Check selector validity in browser DevTools
  2. Verify element exists in DOM
  3. Check if element is in iframe
  4. Verify page has fully loaded
  5. Check for dynamic content loading

solutions:
  - Use data-testid attributes
  - Add explicit waits
  - Handle iframes properly
  - Wait for network idle
  - Use more specific selectors
```

### Issue: Flaky Tests
```yaml
symptoms:
  - Intermittent failures
  - Works locally, fails in CI
  - Random timeout errors

diagnosis:
  1. Identify timing dependencies
  2. Check for race conditions
  3. Review parallel execution conflicts
  4. Analyze failure patterns

solutions:
  - Replace implicit with explicit waits
  - Add retry logic
  - Isolate test data
  - Use deterministic selectors
  - Add proper cleanup
```

### Issue: Slow Test Execution
```yaml
symptoms:
  - Tests taking > 30 seconds each
  - CI pipeline timeout
  - Resource exhaustion

diagnosis:
  1. Profile test execution
  2. Identify slow operations
  3. Check network latency
  4. Review wait times

solutions:
  - Parallelize test execution
  - Mock slow APIs
  - Optimize selectors
  - Reduce unnecessary waits
  - Use headless mode
```

## Best Practices

```yaml
locators:
  - Prefer data-testid over CSS classes
  - Avoid XPath when possible
  - Use semantic HTML attributes
  - Keep selectors short and specific

waits:
  - Always use explicit waits
  - Wait for specific conditions
  - Avoid Thread.sleep/setTimeout
  - Set reasonable timeouts

architecture:
  - Implement Page Object Model
  - Separate test data from tests
  - Use fixtures for setup/teardown
  - Create reusable utilities

ci_integration:
  - Run tests in parallel
  - Use retry on failure
  - Generate detailed reports
  - Archive screenshots on failure
```

## Unit Test Template

```typescript
// tests/automation.skill.test.ts
describe('Automation Skill', () => {
  describe('Input Validation', () => {
    it('should reject invalid framework', async () => {
      const result = await automationSkill.invoke({
        action: 'create_test',
        framework: 'invalid'
      });
      expect(result.status).toBe('failed');
      expect(result.error).toContain('Invalid framework');
    });

    it('should accept valid input', async () => {
      const result = await automationSkill.invoke({
        action: 'create_test',
        framework: 'playwright',
        language: 'typescript'
      });
      expect(result.status).toBe('success');
    });
  });

  describe('Code Generation', () => {
    it('should generate POM structure', async () => {
      const result = await automationSkill.invoke({
        action: 'create_test',
        framework: 'playwright',
        test_type: 'e2e',
        target: { page_name: 'LoginPage' }
      });
      expect(result.code).toContain('class LoginPage');
      expect(result.code).toContain('extends BasePage');
    });
  });
});
```

## Logging & Observability

```yaml
log_events:
  - skill_invoked
  - validation_complete
  - code_generated
  - error_occurred
  - retry_attempted

metrics:
  - invocation_count
  - success_rate
  - generation_time_ms
  - error_distribution

trace_context:
  - request_id
  - user_session
  - framework_version
  - timestamp
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2025-01 | Production-grade with full error handling |
| 2.0.0 | 2024-12 | SASMP v1.3.0 compliance |
| 1.0.0 | 2024-11 | Initial release |
