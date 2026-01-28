---
name: sentry-python-setup
description: Setup Sentry in Python apps. Use when asked to add Sentry to Python, install sentry-sdk, or configure error monitoring for Python applications, Django, Flask, FastAPI.
---

# Sentry Python Setup

Install and configure Sentry in Python projects.

## Invoke This Skill When

- User asks to "add Sentry to Python" or "install Sentry" in a Python app
- User wants error monitoring, logging, or tracing in Python
- User mentions "sentry-sdk" or Python frameworks (Django, Flask, FastAPI)

## Install

```bash
pip install sentry-sdk
```

## Configure

Initialize as early as possible in your application:

```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    send_default_pii=True,
    
    # Tracing
    traces_sample_rate=1.0,
    
    # Profiling
    profile_session_sample_rate=1.0,
    profile_lifecycle="trace",
    
    # Logs
    enable_logs=True,
)
```

### Async Applications

For async apps, initialize inside an async function:

```python
import asyncio
import sentry_sdk

async def main():
    sentry_sdk.init(
        dsn="YOUR_SENTRY_DSN",
        send_default_pii=True,
        traces_sample_rate=1.0,
        enable_logs=True,
    )
    # ... rest of app

asyncio.run(main())
```

## Framework Integrations

### Django

```python
# settings.py
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    send_default_pii=True,
    traces_sample_rate=1.0,
    enable_logs=True,
)
```

### Flask

```python
from flask import Flask
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    send_default_pii=True,
    traces_sample_rate=1.0,
    enable_logs=True,
)

app = Flask(__name__)
```

### FastAPI

```python
from fastapi import FastAPI
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    send_default_pii=True,
    traces_sample_rate=1.0,
    enable_logs=True,
)

app = FastAPI()
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `dsn` | Sentry DSN | Required |
| `send_default_pii` | Include user data | `False` |
| `traces_sample_rate` | % of transactions traced | `0` |
| `profile_session_sample_rate` | % of sessions profiled | `0` |
| `enable_logs` | Send logs to Sentry | `False` |
| `environment` | Environment name | Auto-detected |
| `release` | Release version | Auto-detected |

## Environment Variables

```bash
SENTRY_DSN=https://xxx@o123.ingest.sentry.io/456
SENTRY_AUTH_TOKEN=sntrys_xxx
SENTRY_ORG=my-org
SENTRY_PROJECT=my-project
```

Or use in code:

```python
import os
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    # ...
)
```

## Verification

```python
# Intentional error to test
division_by_zero = 1 / 0
```

Or capture manually:

```python
sentry_sdk.capture_message("Test message from Python")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Errors not appearing | Ensure `init()` is called early, check DSN |
| No traces | Set `traces_sample_rate` > 0 |
| IPython errors not captured | Run from file, not interactive shell |
| Async errors missing | Initialize inside async function |
