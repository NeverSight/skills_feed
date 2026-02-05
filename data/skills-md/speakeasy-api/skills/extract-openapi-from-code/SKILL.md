---
name: extract-openapi-from-code
description: Use when extracting or generating an OpenAPI spec from existing API code. Triggers on "extract OpenAPI", "code first", "generate spec from code", "FastAPI OpenAPI", "Spring Boot OpenAPI", "NestJS swagger", "Django OpenAPI", "Flask OpenAPI", "Rails swagger", "Laravel OpenAPI", "existing API code"
license: Apache-2.0
---

# extract-openapi-from-code

Extract an OpenAPI specification from an existing API codebase. Covers eight major frameworks across Python, Java, JavaScript/TypeScript, Ruby, and PHP.

## Content Guides

| Framework | Language | Guide |
|-----------|----------|-------|
| FastAPI | Python | [content/frameworks/fastapi.md](content/frameworks/fastapi.md) |
| Flask | Python | [content/frameworks/flask.md](content/frameworks/flask.md) |
| Django REST Framework | Python | [content/frameworks/django.md](content/frameworks/django.md) |
| Spring Boot | Java | [content/frameworks/spring-boot.md](content/frameworks/spring-boot.md) |
| NestJS | TypeScript | [content/frameworks/nestjs.md](content/frameworks/nestjs.md) |
| Hono | TypeScript | [content/frameworks/hono.md](content/frameworks/hono.md) |
| Rails | Ruby | [content/frameworks/rails.md](content/frameworks/rails.md) |
| Laravel | PHP | [content/frameworks/laravel.md](content/frameworks/laravel.md) |

Each guide provides detailed setup, schema definition, Speakeasy extensions, authentication, and troubleshooting for that framework.

## When to Use

- User has an existing API and wants to generate an OpenAPI spec from it
- User wants to create an SDK from code that has no OpenAPI spec yet
- User mentions a specific framework (FastAPI, Flask, Django, Spring Boot, NestJS, Hono, Rails, Laravel)
- User says: "extract OpenAPI", "code first", "generate spec from code", "existing API code"

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Framework | Yes | The API framework in use (see Decision Framework) |
| Project path | Yes | Root directory of the API project |
| Output path | No | Where to write the spec (default: `openapi.json` or `openapi.yaml`) |
| Target language | No | SDK target language, if generating an SDK after extraction |

## Outputs

| Output | Description |
|--------|-------------|
| OpenAPI spec | A JSON or YAML file describing the API |
| Validation report | Lint results from `speakeasy lint` |

## Prerequisites

- The API project must be buildable and its dependencies installed
- For runtime extraction (FastAPI, Spring Boot, NestJS, Hono), the app must be importable or startable
- `speakeasy` CLI installed for post-extraction validation and SDK generation

## Decision Framework

Use this tree to determine the extraction method:

| Framework | Language | Method | Requires Running Server? |
|-----------|----------|--------|--------------------------|
| FastAPI | Python | Built-in export | No |
| Flask (flask-smorest) | Python | CLI command | No |
| Django REST Framework | Python | drf-spectacular CLI | No |
| Spring Boot (springdoc) | Java | HTTP endpoint | Yes |
| NestJS | TypeScript | HTTP endpoint or script | Yes |
| Hono (zod-openapi) | TypeScript | Programmatic export | No |
| Rails (rswag) | Ruby | Rake task | No |
| Laravel (l5-swagger) | PHP | Artisan command | No |

## Command

Choose the command matching your framework below. After extraction, always validate with `speakeasy lint`.

### Python: FastAPI

FastAPI generates an OpenAPI schema at runtime. Export it without starting the server:

```bash
python -c "import json; from myapp import app; print(json.dumps(app.openapi()))" > openapi.json
```

Replace `myapp` with the module containing your FastAPI `app` instance. If the app uses a factory pattern:

```bash
python -c "import json; from myapp import create_app; app = create_app(); print(json.dumps(app.openapi()))" > openapi.json
```

You can also start the server and fetch from `http://localhost:8000/openapi.json`.

### Python: Flask (flask-smorest)

Requires [flask-smorest](https://flask-smorest.readthedocs.io/) or [apispec](https://apispec.readthedocs.io/):

```bash
flask openapi write openapi.json
```

If using apispec directly, export programmatically:

```python
import json
from myapp import create_app, spec
app = create_app()
with app.app_context():
    print(json.dumps(spec.to_dict()))
```

### Python: Django REST Framework

Requires [drf-spectacular](https://drf-spectacular.readthedocs.io/):

```bash
python manage.py spectacular --file openapi.yaml
```

For JSON output:

```bash
python manage.py spectacular --format openapi-json --file openapi.json
```

### Java: Spring Boot

Requires [springdoc-openapi](https://springdoc.org/). Start the application, then fetch the spec:

```bash
# Start the app (background)
./mvnw spring-boot:run &
# Wait for startup
sleep 15

# Fetch the spec
curl http://localhost:8080/v3/api-docs -o openapi.json

# For YAML format
curl http://localhost:8080/v3/api-docs.yaml -o openapi.yaml

# Stop the app
kill %1
```

If the server runs on a different port or context path, adjust the URL accordingly.

### TypeScript: NestJS

Requires [@nestjs/swagger](https://docs.nestjs.com/openapi/introduction). Start the application, then fetch:

```bash
# Start the app (background)
npm run start &
sleep 10

# Fetch the spec (default path with SwaggerModule)
curl http://localhost:3000/api-json -o openapi.json

# Stop the app
kill %1
```

Alternatively, create a script to export without running the server:

```typescript
// scripts/export-openapi.ts
import { NestFactory } from '@nestjs/core';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from '../src/app.module';
import * as fs from 'fs';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, { logger: false });
  const config = new DocumentBuilder().setTitle('API').build();
  const doc = SwaggerModule.createDocument(app, config);
  fs.writeFileSync('openapi.json', JSON.stringify(doc, null, 2));
  await app.close();
}
bootstrap();
```

### TypeScript: Hono (zod-openapi)

Requires [@hono/zod-openapi](https://github.com/honojs/middleware/tree/main/packages/zod-openapi). Export the schema programmatically:

```typescript
// scripts/export-openapi.ts
import { app } from '../src/app';
import * as fs from 'fs';

const doc = app.doc('/doc', {
  openapi: '3.1.0',
  info: { title: 'API', version: '1.0.0' },
});
fs.writeFileSync('openapi.json', JSON.stringify(doc, null, 2));
```

Run with:

```bash
npx tsx scripts/export-openapi.ts
```

### Ruby: Rails (rswag)

Requires [rswag](https://github.com/rswag/rswag):

```bash
rails rswag:specs:swaggerize
```

The spec is written to `swagger/v1/swagger.yaml` by default (configurable in `config/initializers/rswag_api.rb`).

### PHP: Laravel (l5-swagger)

Requires [l5-swagger](https://github.com/DarkaOnLine/L5-Swagger):

```bash
php artisan l5-swagger:generate
```

The spec is written to `storage/api-docs/api-docs.json` by default.

## Post-Extraction Steps

After extracting the spec, always run these steps:

### 1. Validate the spec

```bash
speakeasy lint openapi --non-interactive -s openapi.json
```

### 2. Fix issues with overlays (if needed)

If validation reveals issues, use an overlay rather than modifying the extracted spec directly:

```bash
speakeasy overlay apply -s openapi.json -o fixes.yaml
```

To fix validation errors, create an OpenAPI overlay file and apply it with `speakeasy overlay apply -s <spec> -o <overlay>`.

### 3. Generate an SDK

```bash
speakeasy quickstart --skip-interactive --output console \
  -s openapi.json \
  -t <target> \
  -n <name> \
  -p <package>
```

Run `speakeasy quickstart -s <spec> -t <language>` to initialize a new SDK project.

## Example

Full workflow for a FastAPI project:

```bash
# 1. Extract the OpenAPI spec
cd /path/to/my-fastapi-project
python -c "import json; from main import app; print(json.dumps(app.openapi()))" > openapi.json

# 2. Validate
speakeasy lint openapi --non-interactive -s openapi.json

# 3. Generate a TypeScript SDK
speakeasy quickstart --skip-interactive --output console \
  -s openapi.json \
  -t typescript \
  -n "MyApiSDK" \
  -p "my-api-sdk"
```

## Adding Speakeasy Extensions

After extracting a spec, add Speakeasy-specific extensions for better SDK output. These can be added in framework config or via overlay.

### FastAPI: Add Extensions via `openapi_extra`

```python
@app.get(
    "/items",
    openapi_extra={
        "x-speakeasy-retries": {
            "strategy": "backoff",
            "backoff": {"initialInterval": 500, "maxInterval": 60000, "exponent": 1.5},
            "statusCodes": ["5XX", "429"]
        },
        "x-speakeasy-group": "items",
        "x-speakeasy-name-override": "list"
    }
)
def list_items(): ...
```

### Django: Add Extensions via `SPECTACULAR_SETTINGS`

```python
# settings.py
SPECTACULAR_SETTINGS = {
    # ... other settings
    'EXTENSIONS_TO_SCHEMA_FUNCTION': lambda generator, request, public: {
        'x-speakeasy-retries': {
            'strategy': 'backoff',
            'backoff': {'initialInterval': 500, 'maxInterval': 60000, 'exponent': 1.5},
            'statusCodes': ['5XX']
        }
    }
}
```

### Spring Boot: Add Extensions via Custom `OperationCustomizer`

```java
@Bean
public OperationCustomizer operationCustomizer() {
    return (operation, handlerMethod) -> {
        operation.addExtension("x-speakeasy-group",
            handlerMethod.getBeanType().getSimpleName().replace("Controller", "").toLowerCase());
        return operation;
    };
}
```

### NestJS: Add Extensions via Decorator Options

```typescript
@Get()
@ApiOperation({
  summary: 'List items',
  operationId: 'listItems'
})
@ApiExtension('x-speakeasy-group', 'items')
@ApiExtension('x-speakeasy-name-override', 'list')
listItems() { ... }
```

### Via Overlay (Any Framework)

If you cannot modify framework code, use an overlay:

```yaml
overlay: 1.0.0
info:
  title: Speakeasy Extensions
  version: 1.0.0
actions:
  - target: $.paths['/items'].get
    update:
      x-speakeasy-group: items
      x-speakeasy-name-override: list
```

## Common Issues After Extraction

| Issue | Symptom | Fix |
|-------|---------|-----|
| Missing operationIds | Lint warning; SDK methods get generic names | Add operationIds via overlay or use `speakeasy suggest operation-ids -s openapi.json` |
| Missing descriptions | Lint hints; SDK has no documentation | Add descriptions to endpoints and schemas in source code or via overlay |
| Overly permissive schemas | Schemas use `additionalProperties: true` or lack type constraints | Tighten schemas in source code; use stricter validation decorators |
| No response schemas | Lint errors; SDK return types are `any`/`object` | Add explicit response models to your framework endpoints |
| Duplicate operationIds | Lint errors; generation fails | Ensure each endpoint has a unique operationId |
| Missing authentication | No security schemes in spec | Add security metadata to your framework config or via overlay |

## What NOT to Do

- **Do NOT** hand-write an OpenAPI spec when the framework can generate one -- always extract first
- **Do NOT** edit the extracted spec directly -- use overlays for fixes so re-extraction does not lose changes
- **Do NOT** skip validation -- extracted specs often have issues that block SDK generation
- **Do NOT** assume the extracted spec is complete -- frameworks may omit auth, error responses, or headers
- **Do NOT** start the server in production mode for extraction -- use development or test configuration

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` (Python) | App dependencies not installed | Run `pip install -r requirements.txt` or `pip install -e .` |
| Connection refused (Spring Boot, NestJS) | Server not fully started | Increase sleep time or poll for readiness |
| Empty or minimal spec | Routes not registered at import time | Ensure all route modules are imported; check lazy loading |
| YAML parse error | Extracted file has invalid syntax | Re-extract; check for print statements polluting stdout |
| `Cannot find module` (Node.js) | Dependencies not installed | Run `npm install` or `yarn install` |
| No `/v3/api-docs` endpoint (Spring Boot) | springdoc not configured | Add `springdoc-openapi-starter-webmvc-ui` to dependencies |
| No `/api-json` endpoint (NestJS) | Swagger module not set up | Configure `SwaggerModule.setup(app, ...)` in `main.ts` |

## Related Skills

- `manage-openapi-overlays` - Add x-speakeasy-* extensions via overlay
- `start-new-sdk-project` - Generate SDK after extraction
