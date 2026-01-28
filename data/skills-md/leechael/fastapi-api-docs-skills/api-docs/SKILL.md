---
name: api-docs
version: 1.0.0
description: |
  Analyze FastAPI route files and complete API documentation metadata.
  Follows the complete call stack including Depends, traces all possible errors,
  and generates comprehensive OpenAPI documentation elements.
  Use when: user provides a file path with @filename syntax and wants API docs completed.
---

# API Documentation Completion Skill

Analyze FastAPI endpoints and complete their documentation for OpenAPI generation.

**IMPORTANT:** Before writing any documentation text, read and internalize the anti-slop guidelines in `references/anti-slop.md`. All copywriting must follow those rules.

## Invocation

### Single File
```
/api-docs @path/to/routes/file.py
```

### Batch Mode
```
/api-docs @teehouse/api/routes/       # All files in directory
/api-docs all api routes              # Natural language (finds all route files)
/api-docs @file1.py @file2.py @file3.py  # Multiple specific files
```

When batch mode is detected:
1. Use Glob to find all matching `*.py` files
2. Filter to files containing `APIRouter` or `@router.`
3. Process each file sequentially, showing progress
4. Summarize changes at the end

## Analysis Workflow

### Phase 1: Endpoint Discovery

1. Read the target file completely
2. Identify all route handlers decorated with `@router.{method}(...)`:
   - Extract HTTP method (GET, POST, PUT, PATCH, DELETE)
   - Extract path pattern
   - Extract existing response_model if present
   - Extract existing status_code if present
   - Extract existing summary/description if present

### Phase 2: Deep Call Stack Analysis

For EACH endpoint, trace the complete execution flow:

#### 2.1 Dependency Analysis (`Depends(...)`)

For each `Depends(...)` in the handler signature:

1. **Locate the dependency function** - may be:
   - Local function in same file
   - Imported from `...auth`, `...core.database`, etc.
   - A repository/service class method

2. **Trace what it provides**:
   - Database sessions
   - Authentication
   - Request data validation (Pydantic models)
   - Domain objects

3. **Document authentication requirements**:
   - Does it require `get_current_user`? → User auth required

4. **Track possible HTTP errors from dependencies**:
   - Auth failures: 401, 403
   - Resource not found: 404
   - Validation errors: 422

#### 2.2 Handler Body Analysis

Trace the handler's main logic:

1. **Follow function calls** - for each called function:
   - Read its implementation
   - Track what errors it raises (`raise HTTPException`, `raise ValueError`, etc.)
   - Track what Result types it returns (`is_err(...)`)
   - Recurse into its dependencies

2. **Database operations**:
   - What queries are executed?
   - What constraints might fail? (unique violations, foreign keys)
   - What models are created/updated/deleted?

3. **External service calls**:
   - Redis operations
   - Celery task dispatching
   - Third-party API calls

4. **Error propagation**:
   - Explicit `HTTPException` raises with status codes
   - ValueError/Exception catches that convert to HTTP errors
   - Result unwrapping that may surface errors

### Phase 3: Documentation Generation

**Read `references/anti-slop.md` before writing any text.**

For each endpoint, generate/complete:

#### 3.1 Function Docstring

```python
async def handler(...):
    """One-line summary. No "This endpoint..." prefix.

    What it does and when to use it. State facts directly.
    No hedging ("may", "might", "potentially").

    Args:
        param_name: What it is. Include format/constraints.

    Returns:
        What the response contains.

    Raises:
        HTTPException(400): When X happens.
        HTTPException(401): Invalid or missing credentials.
        HTTPException(404): Resource not found.
    """
```

#### 3.2 OpenAPI Metadata

```python
@router.post(
    "/path",
    response_model=ResponseModel,
    status_code=status.HTTP_201_CREATED,
    summary="Verb object",  # ≤6 words, imperative
    description="What it does. When to use it.",  # Direct, no filler
    responses={
        400: {"description": "Invalid input"},
        401: {"description": "Not authenticated"},
        404: {"description": "Resource not found"},
    },
    tags=["Category"],
)
```

#### 3.3 Parameter Documentation

```python
# Path/Query parameters
app_id: str = Path(
    ...,
    description="40-character hex string",  # What it is, not what it "represents"
)

# Body parameters
payload: SomeModel = Body(..., description="Configuration to apply")

# Pydantic fields
class RequestModel(BaseModel):
    field_name: str = Field(..., description="The X value", min_length=1)
```

## Writing Rules (from references/anti-slop.md)

### Summary: ≤6 words, imperative verb

| Bad | Good |
|-----|------|
| "This endpoint retrieves..." | "List KMS instances" |
| "Allows users to get..." | "Get encryption key" |
| "Provides functionality for..." | "Update compose file" |

### Description: Direct statements

| Bad | Good |
|-----|------|
| "This powerful endpoint enables seamless..." | "Encrypt environment variables for deployment." |
| "It's important to note that..." | (delete, state the fact) |
| "The identifier serves as..." | "Identifies the KMS by ID or slug." |

### Banned patterns

- "serves as", "acts as", "stands as" → use "is"
- "in order to" → "to"
- "It's worth noting" → (delete)
- "comprehensive", "robust", "seamless" → (delete or use plain words)
- Rule of three → pick two or one
- Em-dash reveals → rewrite as normal sentence

## Output Format

### Single File
1. Summary table of endpoints found
2. Per-endpoint analysis with call trace
3. Apply edits directly

### Batch Mode
```
Processing 5 files...

[1/5] project/api/routes/kms.py
  - 4 endpoints analyzed
  - 12 fields documented

[2/5] project/api/routes/cvms/tools.py
  - 1 endpoint analyzed
  - 8 fields documented

...

Summary:
  Files processed: 5
  Endpoints documented: 23
  Fields added: 67
```

## Tracing Depth Limits

- Maximum call depth: 5 levels
- Stop tracing at:
  - SQLAlchemy core methods
  - Redis primitive operations
  - Celery task submission (note as async side effect)
  - Standard library functions

## Key Patterns to Recognize

### Error Patterns

```python
# Direct raise
raise HTTPException(status_code=400, detail="message")

# Result type
if is_err(result):
    raise HTTPException(...)

# Exception conversion
except ValueError as err:
    raise HTTPException(status_code=422, detail=str(err))
```

### Auth Patterns

```python
current_user: User = Depends(get_current_user)           # → 401
```

## Quality Checklist

Before completing each file:

- [ ] All endpoints have summary (≤6 words)
- [ ] All endpoints have responses dict
- [ ] All Depends traced for auth/errors
- [ ] No "serves as" / "acts as" (use "is")
- [ ] No "in order to" (use "to")
- [ ] No "It's important/worth noting"
- [ ] No rule-of-three lists
- [ ] Each description adds information beyond the name
- [ ] Error descriptions state what happened, not what "may occur"
