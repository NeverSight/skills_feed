---
name: error-recoverer
description: Intelligent error detection and recovery for autonomous coding. Use when handling errors, implementing retry logic, recovering from failures, or managing exception handling.
version: 1.0.0
category: autonomous-coding
layer: verification-recovery
---

# Error Recoverer

Detects, classifies, and recovers from errors during autonomous coding sessions.

## Quick Start

### Handle Error
```python
from scripts.error_recoverer import ErrorRecoverer

recoverer = ErrorRecoverer(project_dir)
result = await recoverer.handle_error(error, context)

if result.recovered:
    print(f"Recovered via: {result.strategy}")
else:
    print(f"Failed: {result.reason}")
```

### Automatic Recovery
```python
@recoverer.with_recovery
async def risky_operation():
    # Operation that might fail
    pass
```

## Error Recovery Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    ERROR RECOVERY FLOW                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DETECT                                                  │
│     ├─ Catch exception                                     │
│     ├─ Parse error message                                 │
│     └─ Extract error context                               │
│                                                             │
│  2. CLASSIFY                                                │
│     ├─ Determine error category                            │
│     ├─ Assess severity level                               │
│     └─ Check if recoverable                                │
│                                                             │
│  3. STRATEGIZE                                              │
│     ├─ Query causal memory for similar errors              │
│     ├─ Select recovery strategy                            │
│     └─ Prepare recovery action                             │
│                                                             │
│  4. RECOVER                                                 │
│     ├─ Execute recovery strategy                           │
│     ├─ Verify recovery success                             │
│     └─ Store error→solution chain                          │
│                                                             │
│  5. ESCALATE (if recovery fails)                           │
│     ├─ Rollback to checkpoint                              │
│     ├─ Create detailed error report                        │
│     └─ Signal for human intervention                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Error Categories

| Category | Examples | Recovery Strategy |
|----------|----------|-------------------|
| **Transient** | Network timeout, rate limit | Retry with backoff |
| **Resource** | File not found, permission denied | Fix path/permissions |
| **Syntax** | Parse error, invalid JSON | Fix syntax errors |
| **Logic** | Test failure, assertion error | Debug and fix code |
| **Environment** | Missing dependency, version mismatch | Install/update deps |
| **Unrecoverable** | Disk full, OOM | Escalate immediately |

## Recovery Strategies

```python
class RecoveryStrategy(Enum):
    RETRY = "retry"              # Simple retry
    RETRY_BACKOFF = "backoff"    # Exponential backoff
    ROLLBACK = "rollback"        # Restore checkpoint
    FIX_AND_RETRY = "fix_retry"  # Apply fix, then retry
    SKIP = "skip"                # Skip and continue
    ESCALATE = "escalate"        # Human intervention
```

## Integration Points

- **memory-manager**: Query/store causal chains
- **checkpoint-manager**: Rollback on failure
- **coding-agent**: Provide fixes for code errors
- **progress-tracker**: Log error metrics

## References

- `references/ERROR-CATEGORIES.md` - Error classification
- `references/RECOVERY-STRATEGIES.md` - Strategy details

## Scripts

- `scripts/error_recoverer.py` - Core recovery logic
- `scripts/error_classifier.py` - Error classification
- `scripts/retry_handler.py` - Retry with backoff
- `scripts/recovery_strategies.py` - Strategy implementations
