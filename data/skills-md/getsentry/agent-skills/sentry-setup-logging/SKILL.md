---
name: sentry-setup-logging
description: Setup Sentry Logging in any project. Use when asked to add Sentry logs, enable structured logging, capture console logs, or integrate logging libraries (Pino, Winston, Loguru) with Sentry. Supports JavaScript, Python, and Ruby.
---

# Setup Sentry Logging

Configure Sentry's structured logging feature.

## Invoke This Skill When

- User asks to "setup Sentry logging" or "capture logs in Sentry"
- User wants to integrate logging libraries (Pino, Winston, Loguru) with Sentry
- User asks about `Sentry.logger` or `sentry_sdk.logger`

## Quick Reference

| Platform | Min SDK | Enable Flag | Logger API |
|----------|---------|-------------|------------|
| JavaScript | 9.41.0+ | `enableLogs: true` | `Sentry.logger.*` |
| Python | 2.35.0+ | `enable_logs=True` | `sentry_sdk.logger.*` |
| Ruby | 5.24.0+ | `config.enable_logs = true` | `Sentry.logger.*` |

## JavaScript Setup

### 1. Verify SDK version
```bash
grep -E '"@sentry/(nextjs|react|node|browser)"' package.json
```

### 2. Enable in Sentry.init()
```javascript
Sentry.init({
  dsn: "YOUR_DSN",
  enableLogs: true,
});
```

### 3. Console capture (optional)
```javascript
integrations: [
  Sentry.consoleLoggingIntegration({ levels: ["warn", "error"] }),
],
```

### 4. Use structured logging
```javascript
Sentry.logger.info("User logged in", { userId: "123" });
Sentry.logger.error("Payment failed", { orderId: "456", amount: 99.99 });

// Template literals (creates searchable attributes)
Sentry.logger.info(Sentry.logger.fmt`User ${userId} purchased ${productName}`);
```

### Third-party integrations

| Library | Integration | Min SDK |
|---------|-------------|---------|
| Pino | `Sentry.pinoIntegration()` | 10.18.0+ |
| Winston | `Sentry.createSentryWinstonTransport()` | 9.13.0+ |
| Consola | `Sentry.createConsolaReporter()` | 10.12.0+ |

## Python Setup

### 1. Verify SDK version
```bash
pip show sentry-sdk | grep Version
```

### 2. Enable in init()
```python
sentry_sdk.init(
    dsn="YOUR_DSN",
    enable_logs=True,
)
```

### 3. Stdlib logging capture (optional)
```python
from sentry_sdk.integrations.logging import LoggingIntegration
integrations=[LoggingIntegration(sentry_logs_level=logging.WARNING)]
```

### 4. Use structured logging
```python
from sentry_sdk import logger as sentry_logger

sentry_logger.info("User logged in: {user_id}", user_id="123")
sentry_logger.error("Payment failed", order_id="456", amount=99.99)
```

### Loguru integration
```python
from sentry_sdk.integrations.loguru import LoguruIntegration
integrations=[LoguruIntegration(sentry_logs_level=LoggingLevels.WARNING.value)]
```

## Ruby Setup

### 1. Verify SDK version
```bash
bundle show sentry-ruby
```

### 2. Enable in init
```ruby
Sentry.init do |config|
  config.dsn = "YOUR_DSN"
  config.enable_logs = true
  config.enabled_patches = [:logger]  # Optional: capture stdlib Logger
end
```

### 3. Use structured logging
```ruby
Sentry.logger.info("User logged in")
Sentry.logger.error("Payment failed. Order: %{order_id}", order_id: "456")
```

## Log Filtering

### JavaScript
```javascript
beforeSendLog: (log) => log.level === "info" ? null : log,
```

### Python
```python
def before_send_log(log, hint):
    return None if log["severity_text"] == "info" else log
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Logs not appearing | Verify SDK version, check `enableLogs`/`enable_logs` is set |
| Too many logs | Use `beforeSendLog` to filter, reduce captured levels |
| Console not captured | Add `consoleLoggingIntegration` to integrations array |
