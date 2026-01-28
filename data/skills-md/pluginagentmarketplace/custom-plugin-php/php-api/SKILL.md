---
name: php-api
version: "2.0.0"
description: PHP API development mastery - REST, GraphQL, JWT/OAuth, OpenAPI documentation
sasmp_version: "1.3.0"
bonded_agent: 07-php-api
bond_type: PRIMARY_BOND
atomic: true
category: integration
---

# PHP API Development Skill

> Atomic skill for mastering API design and implementation in PHP

## Overview

Comprehensive skill for PHP API development covering REST design, GraphQL, authentication strategies, and API documentation.

## Skill Parameters

### Input Validation
```typescript
interface SkillParams {
  topic:
    | "rest"             // RESTful API design
    | "graphql"          // GraphQL with PHP
    | "authentication"   // JWT, OAuth 2.0
    | "documentation"    // OpenAPI, Swagger
    | "versioning"       // API versioning strategies
    | "security";        // Rate limiting, CORS

  level: "beginner" | "intermediate" | "advanced";
  framework?: "laravel" | "symfony" | "slim";
  auth_method?: "jwt" | "oauth2" | "api_key";
}
```

### Validation Rules
```yaml
validation:
  topic:
    required: true
    allowed: [rest, graphql, authentication, documentation, versioning, security]
  level:
    required: true
  framework:
    default: "laravel"
```

## Learning Modules

### Module 1: REST API Design
```yaml
beginner:
  - Resource naming conventions
  - HTTP methods semantics
  - Status codes usage

intermediate:
  - Pagination patterns
  - Filtering and sorting
  - HATEOAS basics

advanced:
  - Hypermedia APIs
  - Conditional requests
  - Bulk operations
```

### Module 2: Authentication
```yaml
beginner:
  - API keys
  - Basic auth
  - Token basics

intermediate:
  - JWT implementation
  - Refresh tokens
  - Token revocation

advanced:
  - OAuth 2.0 flows
  - PKCE
  - Scopes and permissions
```

### Module 3: API Security
```yaml
beginner:
  - Input validation
  - Output encoding
  - CORS basics

intermediate:
  - Rate limiting
  - Request throttling
  - API versioning

advanced:
  - Security headers
  - Request signing
  - Audit logging
```

## Error Handling & Retry Logic

```yaml
errors:
  VALIDATION_ERROR:
    code: "API_001"
    http_status: 422
    recovery: "Return field-level errors"

  AUTH_ERROR:
    code: "API_002"
    http_status: 401
    recovery: "Check token, suggest refresh"

  RATE_LIMIT_ERROR:
    code: "API_003"
    http_status: 429
    recovery: "Return Retry-After header"

retry:
  max_attempts: 3
  backoff:
    type: exponential
    initial_delay_ms: 100
```

## Code Examples

### REST Controller (Laravel)
```php
<?php
declare(strict_types=1);

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreUserRequest;
use App\Http\Resources\UserResource;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Response;

final class UserController extends Controller
{
    public function index()
    {
        $users = User::query()
            ->with(['profile'])
            ->filter(request(['search', 'status']))
            ->paginate(request('per_page', 15));

        return UserResource::collection($users);
    }

    public function store(StoreUserRequest $request): JsonResponse
    {
        $user = User::create($request->validated());

        return (new UserResource($user))
            ->response()
            ->setStatusCode(Response::HTTP_CREATED)
            ->header('Location', route('api.v1.users.show', $user));
    }

    public function show(User $user): UserResource
    {
        return new UserResource($user->load('profile'));
    }

    public function destroy(User $user): Response
    {
        $this->authorize('delete', $user);
        $user->delete();

        return response()->noContent();
    }
}
```

### Error Response (RFC 7807)
```php
<?php
declare(strict_types=1);

namespace App\Http\Responses;

final class ProblemDetails
{
    public static function validation(array $errors): array
    {
        return [
            'type' => 'https://api.example.com/errors/validation',
            'title' => 'Validation Error',
            'status' => 422,
            'detail' => 'The request contains invalid data',
            'errors' => $errors,
        ];
    }

    public static function unauthorized(): array
    {
        return [
            'type' => 'https://api.example.com/errors/unauthorized',
            'title' => 'Unauthorized',
            'status' => 401,
            'detail' => 'Authentication required',
        ];
    }
}
```

### JWT Authentication
```php
<?php
declare(strict_types=1);

namespace App\Services;

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

final class JwtService
{
    public function __construct(
        private readonly string $secret,
        private readonly string $algorithm = 'HS256',
        private readonly int $ttl = 3600,
    ) {}

    public function generate(array $payload): string
    {
        $issuedAt = time();

        return JWT::encode([
            ...$payload,
            'iat' => $issuedAt,
            'exp' => $issuedAt + $this->ttl,
        ], $this->secret, $this->algorithm);
    }

    public function decode(string $token): object
    {
        return JWT::decode($token, new Key($this->secret, $this->algorithm));
    }
}
```

### OpenAPI Specification
```yaml
openapi: 3.1.0
info:
  title: User API
  version: 1.0.0

paths:
  /api/v1/users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserCollection'

    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
      responses:
        '201':
          description: Created

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        email:
          type: string
          format: email
        name:
          type: string

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

### Rate Limiting (Laravel)
```php
<?php
// RouteServiceProvider or bootstrap/app.php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

RateLimiter::for('api', function ($request) {
    return Limit::perMinute(60)
        ->by($request->user()?->id ?: $request->ip())
        ->response(function () {
            return response()->json([
                'type' => 'https://api.example.com/errors/rate-limit',
                'title' => 'Too Many Requests',
                'status' => 429,
            ], 429)->header('Retry-After', 60);
        });
});
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| CORS errors | Missing headers | Configure CORS middleware |
| JWT invalid | Expired or wrong secret | Check exp claim, verify secret |
| 429 errors | Rate limited | Implement backoff, cache responses |
| N+1 in resources | Missing eager loading | Use with() in controller |

## Quality Metrics

| Metric | Target |
|--------|--------|
| Response time | <200ms P95 |
| Error rate | <0.1% |
| Documentation | 100% endpoints |
| Test coverage | ≥90% |

## Usage

```
Skill("php-api", {topic: "authentication", level: "intermediate"})
```
