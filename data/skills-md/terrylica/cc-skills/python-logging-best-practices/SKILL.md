---
name: python-logging-best-practices
description: Python logging with loguru and platformdirs. TRIGGERS - loguru, structured logging, JSONL logs, log rotation, XDG directories.
allowed-tools: Read, Bash, Grep, Edit, Write
---

# Python Logging Best Practices

## When to Use This Skill

Use this skill when:

- Setting up Python logging with loguru
- Configuring structured JSONL logging for analysis
- Implementing log rotation
- Using platformdirs for cross-platform log directories

## Overview

Unified reference for Python logging patterns optimized for machine readability (Claude Code analysis) and operational reliability.

## MANDATORY Best Practices

### 1. Log Rotation (ALWAYS CONFIGURE)

Prevent unbounded log growth - configure rotation for ALL log files:

```python
# Loguru pattern (recommended for modern scripts)
from loguru import logger

logger.add(
    log_path,
    rotation="10 MB",      # Rotate at 10MB
    retention="7 days",    # Keep 7 days
    compression="gz"       # Compress old logs
)

# RotatingFileHandler pattern (stdlib-only)
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    log_path,
    maxBytes=100 * 1024 * 1024,  # 100MB
    backupCount=5                 # Keep 5 backups (~500MB max)
)
```

### 2. JSONL Format (Machine-Readable)

Use JSONL (`.jsonl`) for logs that Claude Code or other tools will analyze:

```python
# One JSON object per line - jq-parseable
{"timestamp": "2026-01-14T12:45:23.456Z", "level": "info", "message": "..."}
{"timestamp": "2026-01-14T12:45:24.789Z", "level": "error", "message": "..."}
```

**File extension**: Always use `.jsonl` (not `.json` or `.log`)

**Validation**: `cat file.jsonl | jq -c .`

**Terminology**: JSONL is canonical. Equivalent terms: NDJSON, JSON Lines.

## When to Use Which Approach

| Approach              | Use Case                         | Pros                                       | Cons                |
| --------------------- | -------------------------------- | ------------------------------------------ | ------------------- |
| `loguru`              | Modern scripts, CLI tools        | Zero-config, async-safe, built-in rotation | External dependency |
| `RotatingFileHandler` | LaunchAgent daemons, stdlib-only | No dependencies                            | More setup          |
| `logger_setup.py`     | Rich terminal apps               | Beautiful output                           | Complex setup       |

## Complete Loguru + platformdirs Pattern

Cross-platform log directory handling with structured JSONL output:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["loguru", "platformdirs"]
# ///

import json
import sys
from pathlib import Path
from uuid import uuid4

import platformdirs
from loguru import logger


def json_formatter(record) -> str:
    """JSONL formatter for Claude Code analysis."""
    log_entry = {
        "timestamp": record["time"].strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "level": record["level"].name.lower(),
        "component": record["function"],
        "operation": record["extra"].get("operation", "unknown"),
        "operation_status": record["extra"].get("status", None),
        "trace_id": record["extra"].get("trace_id"),
        "message": record["message"],
        "context": {k: v for k, v in record["extra"].items()
                   if k not in ("operation", "status", "trace_id", "metrics")},
        "metrics": record["extra"].get("metrics", {}),
        "error": None
    }

    if record["exception"]:
        exc_type, exc_value, _ = record["exception"]
        log_entry["error"] = {
            "type": exc_type.__name__ if exc_type else "Unknown",
            "message": str(exc_value) if exc_value else "Unknown error",
        }

    return json.dumps(log_entry)


def setup_logger(app_name: str = "my-app"):
    """Configure Loguru for machine-readable JSONL output."""
    logger.remove()

    # Console output (JSONL to stderr)
    logger.add(sys.stderr, format=json_formatter, level="INFO")

    # Cross-platform log directory
    # macOS: ~/Library/Logs/{app_name}/
    # Linux: ~/.local/state/{app_name}/log/
    log_dir = Path(platformdirs.user_log_dir(
        appname=app_name,
        ensure_exists=True
    ))

    # File output with rotation
    logger.add(
        str(log_dir / f"{app_name}.jsonl"),
        format=json_formatter,
        rotation="10 MB",
        retention="7 days",
        compression="gz",
        level="DEBUG"
    )

    return logger


# Usage
setup_logger("my-app")
trace_id = str(uuid4())

logger.info(
    "Operation started",
    operation="my_operation",
    status="started",
    trace_id=trace_id
)

logger.info(
    "Operation complete",
    operation="my_operation",
    status="success",
    trace_id=trace_id,
    metrics={"duration_ms": 150, "items_processed": 42}
)
```

## Semantic Fields Reference

| Field              | Type            | Purpose                               |
| ------------------ | --------------- | ------------------------------------- |
| `timestamp`        | ISO 8601 with Z | Event ordering                        |
| `level`            | string          | debug/info/warning/error/critical     |
| `component`        | string          | Module/function name                  |
| `operation`        | string          | What action is being performed        |
| `operation_status` | string          | started/success/failed/skipped        |
| `trace_id`         | UUID4           | Correlation for async operations      |
| `message`          | string          | Human-readable description            |
| `context`          | object          | Operation-specific metadata           |
| `metrics`          | object          | Quantitative data (counts, durations) |
| `error`            | object/null     | Exception details if failed           |

## Related Resources

- [Python logging.handlers](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler) - RotatingFileHandler for log rotation
- [platformdirs reference](./references/platformdirs-xdg.md) - Cross-platform directories
- [loguru patterns](./references/loguru-patterns.md) - Advanced loguru configuration
- [migration guide](./references/migration-guide.md) - From print() to structured logging

## Anti-Patterns to Avoid

1. **Unbounded logs** - Always configure rotation
2. **print() for logging** - Use structured logger
3. **Bare except** - Catch specific exceptions, log them
4. **Silent failures** - Log errors before suppressing
5. **Hardcoded paths** - Use platformdirs for cross-platform

---

## Troubleshooting

| Issue                     | Cause                   | Solution                               |
| ------------------------- | ----------------------- | -------------------------------------- |
| loguru not found          | Not installed           | Run `uv add loguru`                    |
| Logs not appearing        | Wrong log level         | Set level to DEBUG for troubleshooting |
| Log rotation not working  | Missing rotation config | Add rotation param to logger.add()     |
| platformdirs import error | Not installed           | Run `uv add platformdirs`              |
| JSONL parse errors        | Malformed log line      | Check for unescaped special characters |
| Logs in wrong directory   | Using hardcoded path    | Use platformdirs.user_log_dir()        |
