---
name: laravel:exception-handling-and-logging
description: Use reportable/renderable exceptions, structured logs, and channel strategy for observability and graceful failures
---

# Exception Handling and Logging

Treat errors as first-class signals; provide context and paths to remediation.

## Commands

```
// app/Exceptions/Handler.php
public function register(): void
{
    $this->reportable(function (DomainException $e) {
        Log::warning('domain exception', ['code' => $e->getCode()]);
    });

    $this->renderable(function (ModelNotFoundException $e, $request) {
        if ($request->expectsJson()) {
            return response()->json(['message' => 'Not Found'], 404);
        }
    });
}
```

## Patterns

- Use domain-specific exceptions for expected error paths
- Add structured context to logs; avoid logging secrets
- Route noisy logs to separate channels; keep defaults actionable
- Convert to API-appropriate responses in `renderable()`

