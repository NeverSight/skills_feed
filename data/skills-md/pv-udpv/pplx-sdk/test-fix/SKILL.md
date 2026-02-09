---
name: test-fix
description: Diagnose and fix failing pytest tests in the pplx-sdk project, following existing test patterns and conventions.
context: fork
agent: test-runner
---

# test-fix

Diagnose and fix failing tests following pplx-sdk testing conventions.

## When to use

Use this skill when pytest tests fail and you need to identify the root cause and apply the correct fix.

## Instructions

1. **Read the failure output** carefully — identify the root cause (assertion error, import error, missing mock, timeout, etc.).
2. **Locate the source code** the test exercises — the fix may be in the source, not the test itself.
3. **Follow existing patterns**: Look at passing tests in the same file for mock setup and assertion style.
4. **Preserve test intent**: Never weaken assertions to make tests pass. Fix the underlying issue.
5. **Run the fix**: Execute `pytest tests/<file> -v` to confirm the fix works.

## Project Testing Conventions

- **Framework**: pytest with `pytest-asyncio` and `pytest-httpx`
- **HTTP mocking**: Use `HTTPXMock` from `pytest-httpx` for transport tests
- **Fixtures**: Common fixtures in `tests/conftest.py` — `mock_auth_token`, `mock_context_uuid`, `mock_frontend_uuid`, `mock_backend_uuid`
- **Test naming**: `test_<what>_<behavior>` (e.g., `test_http_transport_auth_error`)
- **Structure**: Arrange-Act-Assert pattern
- **No docstrings needed** in test files (per ruff config)

## Exception Testing

Verify the exception hierarchy when testing error cases:

```python
# AuthenticationError is a TransportError which is a PerplexitySDKError
with pytest.raises(AuthenticationError) as exc_info:
    transport.request("GET", "/api/test")
assert exc_info.value.status_code == 401
```

## Common Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `ImportError` | Module restructured | Update import path |
| `AttributeError` | Model field renamed | Check `domain/models.py` |
| `HTTPXMock` not matching | URL or method mismatch | Verify mock URL matches request |
| `TransportError` vs `RuntimeError` | Exception type changed | Use `pplx_sdk.core.exceptions` types |
