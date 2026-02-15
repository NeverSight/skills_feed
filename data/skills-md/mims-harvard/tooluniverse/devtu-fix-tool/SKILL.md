---
name: devtu-fix-tool
description: Fix failing ToolUniverse tools by diagnosing test failures, identifying root causes, implementing fixes, and validating solutions. Use when ToolUniverse tools fail tests, return errors, have schema validation issues, or when asked to debug or fix tools in the ToolUniverse framework.
---

# Fix ToolUniverse Tools

Diagnose and fix failing ToolUniverse tools through systematic error identification, targeted fixes, and validation.

## Instructions

When fixing a failing tool:

1. **Run targeted test to identify error**:

```bash
python scripts/test_new_tools.py <tool-pattern> -v
```

2. **Verify API is correct** - search online for official API documentation to confirm endpoints, parameters, and patterns are correct

3. **Identify error type** (see Error Types section)

4. **Apply appropriate fix** based on error pattern

4. **Regenerate tools** if you modified JSON configs or tool classes:

```bash
python -m tooluniverse.generate_tools
```

5. **Check and update unit tests** if they exist in `tests/unit/`:

```bash
ls tests/unit/test_<tool-name>_tool.py
```

6. **Verify fix** by re-running both integration and unit tests

7. **Provide fix summary** with problem, root cause, solution, and test results

## Where to Fix

| Issue Type | File to Modify |
|------------|----------------|
| Binary response | `src/tooluniverse/*_tool.py` + `src/tooluniverse/data/*_tools.json` |
| Schema mismatch | `src/tooluniverse/data/*_tools.json` (return_schema) |
| Missing data wrapper | `src/tooluniverse/*_tool.py` (operation methods) |
| Endpoint URL | `src/tooluniverse/data/*_tools.json` (endpoint field) |
| Invalid test example | `src/tooluniverse/data/*_tools.json` (test_examples) |
| Unit test updates | `tests/unit/test_*_tool.py` (if exists) |
| API key as parameter | `src/tooluniverse/data/*_tools.json` (remove param) + `*_tool.py` (use env var) |
| Tool not loading (optional key) | `src/tooluniverse/data/*_tools.json` (use `optional_api_keys` not `required_api_keys`) |

## Error Types

### 1. JSON Parsing Errors

**Symptom**: `Expecting value: line 1 column 1 (char 0)`

**Cause**: Tool expects JSON but receives binary data (images, PDFs, files)

**Fix**: Check Content-Type header. For binary responses, return a description string instead of parsing JSON. Update `return_schema` to `{"type": "string"}`.

### 2. Schema Validation Errors

**Symptom**: `Schema Mismatch: At root: ... is not of type 'object'` or `Data: None`

**Cause**: Missing `data` field wrapper OR wrong schema type

**Fix depends on the error**:
- If `Data: None` → Add `data` wrapper to ALL operation methods (see Multi-Operation Pattern below)
- If type mismatch → Update `return_schema` in JSON config:
  - Data is string: `{"type": "string"}`
  - Data is array: `{"type": "array", "items": {...}}`
  - Data is object: `{"type": "object", "properties": {...}}`

**Key concept**: Schema validates the `data` field content, NOT the full response.

### 3. Nullable Field Errors

**Symptom**: `Schema Mismatch: At N->fieldName: None is not of type 'integer'`

**Cause**: API returns `None`/`null` for optional fields

**Fix**: Allow nullable types in JSON config using `{"type": ["<base_type>", "null"]}`. Use for optional fields, not required identifiers.

### 4. Mixed Type Field Errors

**Symptom**: `Schema Mismatch: At N->field: {object} is not of type 'string', 'null'`

**Cause**: Field returns different structures depending on context

**Fix**: Use `oneOf` in JSON config for fields with multiple distinct schemas. Different from nullable (`{"type": ["string", "null"]}`) which is same base type + null.

### 5. Invalid Test Examples

**Symptom**: `404 ERROR - Not found` or `400 Bad Request`

**Cause**: Test example uses invalid/outdated IDs

**Fix**: Discover valid examples using the List → Get or Search → Details patterns below.

### 6. API Parameter Errors

**Symptom**: `400 Bad Request` or parameter validation errors

**Fix**: Update parameter schema in JSON config with correct types, required fields, and enums.

### 7. API Key Configuration Errors

**Symptom**: Tool not loading when API key is optional, or `api_key` parameter causing confusion

**Cause**: Using `required_api_keys` for keys that should be optional, or exposing API key as tool parameter

**Key differences**:
- `required_api_keys`: Tool is **skipped** if keys are missing
- `optional_api_keys`: Tool **loads and works** without keys (with reduced performance)

**Fix**: Use `optional_api_keys` in JSON config for APIs that work anonymously but have better rate limits with keys. Read API key from environment only (`os.environ.get()`), never as a tool parameter.

### 8. API Endpoint Pattern Errors

**Symptom**: `404` for valid resources, or unexpected results

**Fix**: Verify official API docs - check if values belong in URL path vs query parameters.

### 9. Transient API Failures

**Symptom**: Tests fail intermittently with timeout/connection/5xx errors

**Fix**: Use `pytest.skip()` for transient errors in unit tests - don't fail on external API outages.

## Common Fix Patterns

### Schema Validation Pattern

Schema validates the `data` field content, not the full response. Match `return_schema` type to what's inside `data` (array, object, or string).

### Multi-Operation Tool Pattern

Every internal method must return `{"status": "...", "data": {...}}`. Don't use alternative field names at top level.

## Finding Valid Test Examples

When test examples fail with 400/404, discover valid IDs by:
- **List → Get**: Call a list endpoint first, extract ID from results
- **Search → Details**: Search for a known entity, use returned ID
- **Iterate Versions**: Try different dataset versions if supported

## Unit Test Management

### Check for Unit Tests

After fixing a tool, check if unit tests exist:

```bash
ls tests/unit/test_<tool-name>_tool.py
```

### When to Update Unit Tests

Update unit tests when you:

1. **Change return structure**: Update assertions checking `result["data"]` structure
2. **Add/modify operations**: Add test cases for new operations
3. **Change error handling**: Update error assertions
4. **Modify required parameters**: Update parameter validation tests
5. **Fix schema issues**: Ensure tests validate correct data structure
6. **Add binary handling**: Add tests for binary responses

### Running Unit Tests

```bash
# Run specific tool tests
pytest tests/unit/test_<tool-name>_tool.py -v

# Run all unit tests
pytest tests/unit/ -v
```

### Unit Test Checklist

- [ ] Check if `tests/unit/test_<tool-name>_tool.py` exists
- [ ] Run unit tests before and after fix
- [ ] Update assertions if data structure changed
- [ ] Ensure both direct and interface tests pass

For detailed unit test patterns and examples, see [unit-tests-reference.md](unit-tests-reference.md).

## Verification

### Run Integration Tests

```bash
python scripts/test_new_tools.py <pattern> -v
```

### Run Unit Tests (if exist)

```bash
pytest tests/unit/test_<tool-name>_tool.py -v
```

### Regenerate Tools

After modifying JSON configs or tool classes:

```bash
python -m tooluniverse.generate_tools
```

Regenerate after:
- Changing `src/tooluniverse/data/*_tools.json` files
- Modifying tool class implementations

Not needed for test script changes.

## Output Format

After fixing, provide this summary:

**Problem**: [Brief description]

**Root Cause**: [Why it failed]

**Solution**: [What was changed]

**Changes Made**:
- File 1: [Description]
- File 2: [Description]
- File 3 (if applicable): [Unit test updates]

**Integration Test Results**:
- Before: X tests, Y passed (Z%), N failed, M schema invalid
- After: X tests, X passed (100.0%), 0 failed, 0 schema invalid

**Unit Test Results** (if applicable):
- Before: X tests, Y passed, Z failed
- After: X tests, X passed, 0 failed

## Common Pitfalls

1. **Schema validates `data` field**, not full response
2. **All methods need `{"status": "...", "data": {...}}`** wrapper
3. **JSON config changes require regeneration**
4. **Use `optional_api_keys`** for APIs that work without keys
5. **Check official API docs** for correct endpoint patterns
6. **Unit tests should skip** on transient API failures, not fail

## Debugging

- **Inspect API response**: Check status code, Content-Type header, and body preview
- **Check tool config**: Load ToolUniverse and inspect the tool's configuration
- **Add debug prints**: Log URL, params, status, and Content-Type in the run method

## Quick Reference

| Task | Command |
|------|---------|
| Run integration tests | `python scripts/test_new_tools.py <pattern> -v` |
| Run unit tests | `pytest tests/unit/test_<tool-name>_tool.py -v` |
| Check if unit tests exist | `ls tests/unit/test_<tool-name>_tool.py` |
| Regenerate tools | `python -m tooluniverse.generate_tools` |
| Check status | `git status --short \| grep -E "(data\|tools\|.*_tool.py\|tests/unit)"` |

| Error Type | Fix Location |
|------------|--------------|
| JSON parse error | `src/tooluniverse/*_tool.py` run() method |
| Schema mismatch | `src/tooluniverse/data/*_tools.json` return_schema |
| 404 errors | `src/tooluniverse/data/*_tools.json` test_examples or endpoint |
| Parameter errors | `src/tooluniverse/data/*_tools.json` parameter schema |
| Unit test failures | `tests/unit/test_*_tool.py` assertions |
| Tool skipped (optional key) | `src/tooluniverse/data/*_tools.json` use `optional_api_keys` |
| API key as parameter | Remove from JSON params, use `os.environ.get()` in Python |
