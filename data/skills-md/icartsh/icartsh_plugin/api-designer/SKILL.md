---
name: api-designer
description: "OpenAPI/Swagger 사양, 인증 패턴, 버전 관리 전략 및 모범 사례를 사용하여 RESTful 및 GraphQL API를 설계하고 문서화합니다. 사용 사례: (1) API 사양 생성, (2) REST 엔드포인트 설계, (3) GraphQL 스키마 설계, (4) API 인증 및 권한 부여, (5) API 버전 관리 전략, (6) 문서 생성"
---

# API Designer

## Overview

이 SKILL은 현대적인 API를 설계, 문서화 및 구현하기 위한 포괄적인 가이드를 제공합니다. REST 및 GraphQL 패러다임을 모두 다루며, 업계의 모범 사례, 명확한 문서화 및 유지보수 가능한 아키텍처를 강조합니다. 확장 가능하고 안전하며 개발자 친화적인 Production-ready API 설계를 위해 이 SKILL을 사용하세요.

## Core Capabilities

### REST API Design
- 적절한 URL 구조를 갖춘 리소스 지향 엔드포인트 설계
- HTTP method 의미론 및 status code 사용
- 일관된 명명 규칙을 적용한 Request/response payload 설계
- Pagination, filtering 및 sorting 전략
- Error handling 및 validation 패턴

### GraphQL API Design
- Type system 및 관계를 포함한 Schema 정의
- 적절한 input type을 사용한 Query 및 mutation 설계
- Resolver 패턴 및 성능 최적화
- Fragment 사용 및 directive 구현
- N+1 문제 방지 전략

### API Documentation
- OpenAPI 3.0 specification 생성
- Swagger UI를 통한 대화형 문서화
- Authentication 및 authorization 문서화
- 다양한 시나리오를 포함한 Example requests/responses
- 사양(Specification)으로부터 코드 생성

### Authentication & Authorization
- OAuth 2.0 flow (authorization code, client credentials, PKCE)
- JWT token 설계, validation 및 rotation
- API key 관리 및 rotation 전략
- Role-based access control (RBAC) 구현
- Rate limiting 및 throttling 패턴

### API Versioning
- URL versioning 및 header-based versioning 전략
- API 릴리스를 위한 Semantic versioning
- Deprecation 계획 및 커뮤니케이션
- Backward compatibility 유지
- Migration 경로 설계

## When to Use This Skill

이 SKILL은 다음과 같은 경우에 사용하세요:
- 새로운 API를 처음부터 설계하거나 기존 엔드포인트를 리팩토링할 때
- 문서화를 위해 OpenAPI/Swagger 사양을 생성할 때
- Authentication 및 authorization flow를 구현할 때
- API versioning 및 deprecation 전략을 계획할 때
- GraphQL schema 및 resolver를 설계할 때
- API governance 및 모범 사례를 확립할 때

## REST API Design Workflow

### Step 1: Identify Resources

API가 노출할 핵심 리소스(Noun)를 식별합니다:

```
Resources: Users, Posts, Comments

Collections:
- GET    /users              (모든 사용자 목록 조회)
- POST   /users              (새 사용자 생성)

Individual Resources:
- GET    /users/{id}         (특정 사용자 조회)
- PUT    /users/{id}         (사용자 교체 - 전체 업데이트)
- PATCH  /users/{id}         (사용자 업데이트 - 일부 업데이트)
- DELETE /users/{id}         (사용자 삭제)

Nested Resources:
- GET    /users/{id}/posts   (사용자의 포스트 조회)
- POST   /users/{id}/posts   (사용자를 위한 포스트 생성)
```

### Step 2: Design URL Structure

RESTful 명명 규칙을 따릅니다:

**Best Practices**:
- 복수형 명사 사용: `/users`, `/posts` (`/user`, `/post` 아님)
- 여러 단어는 하이픈 사용: `/blog-posts` (`/blogPosts` 또는 `/blog_posts` 아님)
- URL은 소문자로 유지
- Nesting은 최대 2단계로 제한
- Filtering을 위해 query parameter 사용: `/posts?status=published&author=123`

**Quick Examples**:
```
✅ Good:
GET /users
GET /users/123/posts
GET /posts?published=true&limit=10

❌ Bad:
GET /getUsers
GET /users/123/posts/comments/likes  (너무 깊은 nesting)
GET /posts/published  (대신 query param 사용)
```

### Step 3: Choose HTTP Methods

작업을 표준 HTTP method에 매핑합니다:

- **GET**: 리소스 조회 - Safe, idempotent, cacheable
- **POST**: 새 리소스 생성 - Location header와 함께 201 Created 반환
- **PUT**: 전체 리소스 교체 - Idempotent, 전체 교체
- **PATCH**: 부분 업데이트 - 특정 필드만 업데이트
- **DELETE**: 리소스 제거 - Idempotent, 204 또는 200 반환

### Step 4: Design Request/Response Payloads

JSON payload를 일관되게 구성합니다:

**Naming Conventions**:
- JSON 필드 이름에 camelCase 사용
- 타임스탬프에 ISO 8601 사용 (UTC)
- 접두사가 있는 일관된 ID 형식 사용: `usr_`, `post_`
- 메타데이터 포함: `createdAt`, `updatedAt`

**Example Response**:
```json
{
  "id": "usr_1234567890",
  "username": "johndoe",
  "email": "john@example.com",
  "profile": {
    "firstName": "John",
    "lastName": "Doe"
  },
  "createdAt": "2025-10-25T10:30:00Z",
  "updatedAt": "2025-10-25T10:30:00Z"
}
```

### Step 5: Implement Error Handling

포괄적인 에러 응답을 설계합니다:

**Error Response Format**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ],
    "requestId": "req_abc123xyz",
    "timestamp": "2025-10-25T10:30:00Z"
  }
}
```

**Key Status Codes**:
- `200 OK`: 성공적인 GET, PUT, PATCH
- `201 Created`: 성공적인 POST
- `204 No Content`: 성공적인 DELETE
- `400 Bad Request`: 유효하지 않은 요청 데이터
- `401 Unauthorized`: 인증 정보 누락/유효하지 않음
- `403 Forbidden`: 인증되었으나 권한 없음
- `404 Not Found`: 리소스가 존재하지 않음
- `422 Unprocessable Entity`: Validation 에러
- `429 Too Many Requests`: Rate limit 초과
- `500 Internal Server Error`: 서버 에러

### Step 6: Add Pagination and Filtering

**Cursor-Based Pagination** (대규모 데이터셋에 권장):
```
GET /posts?limit=20&cursor=eyJpZCI6MTIzfQ

Response:
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ",
    "hasMore": true
  }
}
```

**Offset-Based Pagination** (소규모 데이터셋에 적합):
```
GET /posts?limit=20&offset=40&sort=-createdAt

Response:
{
  "data": [...],
  "pagination": {
    "total": 500,
    "limit": 20,
    "offset": 40
  }
}
```

상세한 Pagination 전략 및 filtering 패턴은 `references/rest_best_practices.md`를 참조하세요.

## GraphQL API Design Workflow

### Step 1: Define Schema Types

도메인을 위한 type definition을 생성합니다:

```graphql
type User {
  id: ID!
  username: String!
  email: String!
  profile: Profile
  posts(limit: Int = 10): [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  published: Boolean!
  author: User!
  tags: [String!]!
  createdAt: DateTime!
}
```

### Step 2: Design Queries

Filtering을 포함한 조회 작업을 정의합니다:

```graphql
type Query {
  user(id: ID!): User
  post(id: ID!): Post

  users(
    limit: Int = 10
    offset: Int = 0
    search: String
  ): UserConnection!

  posts(
    limit: Int = 10
    published: Boolean
    authorId: ID
    tags: [String!]
  ): PostConnection!
}
```

### Step 3: Design Mutations

Input type 및 error handling을 포함한 쓰기 작업을 정의합니다:

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  createPost(input: CreatePostInput!): CreatePostPayload!
}

input CreateUserInput {
  username: String!
  email: String!
  password: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}
```

전체 GraphQL schema 예시는 `examples/graphql_schema.graphql`을 참조하세요.

## Authentication Patterns

### OAuth 2.0 Quick Reference

**Authorization Code Flow** (백엔드가 있는 웹 앱):
```
1. client_id, redirect_uri, scope와 함께 /oauth/authorize로 리다이렉트
2. 사용자가 인증하고 권한 부여
3. 리다이렉트를 통해 authorization code 수신
4. /oauth/token에서 코드를 access token으로 교환
5. Authorization header에 access token 사용
```

**Client Credentials Flow** (서비스 간 통신):
```
POST /oauth/token
{
  "grant_type": "client_credentials",
  "client_id": "CLIENT_ID",
  "client_secret": "SECRET"
}
```

**PKCE Flow** (모바일/SPA - 퍼블릭 클라이언트에 가장 안전):
```
1. code_verifier 및 code_challenge 생성
2. code_challenge와 함께 권한 요청
3. code_verifier로 코드를 토큰으로 교환 (client_secret 불필요)
```

### JWT Token Design

**Token Structure**:
```json
{
  "header": { "alg": "RS256", "typ": "JWT" },
  "payload": {
    "sub": "usr_1234567890",
    "iat": 1698336000,
    "exp": 1698339600,
    "scope": ["read:posts", "write:posts"],
    "roles": ["user", "editor"]
  }
}
```

**Usage**:
```http
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### API Key Authentication

```http
X-API-Key: sk_live_abcdef1234567890
```

**Best Practices**:
- 환경별(dev, staging, prod)로 다른 키 사용
- 로테이션을 위해 계정당 여러 키 지원
- Key expiration 및 사용 로그 구현
- 클라이언트 측 코드에 키를 노출하지 않음

Refresh token, MFA 및 보안 모범 사례를 포함한 종합적인 인증 패턴은 `references/authentication.md`를 참조하세요.

## API Versioning Strategies

### URL Versioning (권장)

```
/v1/users
/v2/users
```

**장점**: 명확하고 명시적이며, 캐싱 및 라우팅이 쉬움
**단점**: URL 확산, 여러 코드베이스 관리

### Header Versioning

```http
Accept: application/vnd.myapi.v2+json
API-Version: 2
```

**장점**: 깔끔한 URL, 동일한 엔드포인트 유지
**단점**: 덜 가시적이며, 브라우저에서 테스트하기 어려움

### When to Version

**새로운 버전이 필요한 경우**:
- 엔드포인트 또는 필드 삭제
- 필드 유형 또는 이름 변경
- 인증 방법 수정
- 기존 클라이언트 계약(Contract) 위반

**버전 관리가 필요 없는 경우**:
- 새로운 선택적(Optional) 필드 추가
- 새로운 엔드포인트 추가
- 버그 수정 또는 성능 향상

상세한 Versioning 전략, deprecation 프로세스 및 migration 패턴은 `references/versioning-strategies.md`를 참조하세요.

## OpenAPI Specification

### Basic Structure

```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
  description: API description

servers:
  - url: https://api.example.com/v1

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

components:
  schemas:
    User:
      type: object
      required:
        - username
        - email
      properties:
        id:
          type: string
        username:
          type: string
        email:
          type: string
          format: email
```

전체 OpenAPI 사양 예시는 `examples/openapi_spec.yaml`을 참조하세요.

### Generating Documentation

Helper script를 사용하여 사양을 생성하고 검증합니다:

```bash
# 코드에서 OpenAPI 사양 생성
python scripts/api_helper.py generate --input api.py --output openapi.yaml

# 기존 사양 검증
python scripts/api_helper.py validate --spec openapi.yaml

# 문서 사이트 생성
python scripts/api_helper.py docs --spec openapi.yaml --output docs/
```

## Best Practices Summary

### Consistency
- 모든 엔드포인트에서 일관된 명명 규칙 사용
- 에러 응답 형식 표준화
- 모든 곳에 동일한 인증 패턴 적용
- 통일된 타임스탬프 형식 사용 (ISO 8601 with UTC)

### Security
- Production에서는 항상 HTTPS 사용
- 모든 입력 데이터를 철저히 검증
- 사용자/키/IP별로 Rate limiting 구현
- 모든 엔드포인트에 적절한 인증 사용
- URL이나 로그에 민감한 데이터를 노출하지 않음
- 적절한 CORS 구성 구현

### Performance
- 대규모 데이터셋에 Pagination 사용
- 캐싱 헤더(ETag, Cache-Control) 구현
- 압축(gzip) 지원
- 실시간 데이터에 Cursor-based pagination 사용
- Sparse fieldsets을 위한 필드 선택(Field selection) 구현

### Documentation
- 모든 엔드포인트를 OpenAPI로 문서화
- Example requests 및 responses 제공
- 에러 코드 및 의미 문서화
- 인증 안내 포함
- 문서를 코드와 동기화된 상태로 유지

### Maintainability
- 명확한 deprecation 일정을 가지고 적절하게 API 버전 관리
- 기능을 제거하기 전에 deprecation 경고 제공
- 모든 엔드포인트에 대해 통합 테스트 작성
- API 사용량, 에러 및 성능 모니터링
- 가능한 경우 Backward compatibility 유지

## Common Patterns

### Health Check
```http
GET /health
Response: { "status": "ok", "timestamp": "2025-10-25T10:30:00Z" }
```

### Batch Operations
```http
POST /users/batch
{
  "operations": [
    { "method": "POST", "path": "/users", "body": {...} },
    { "method": "PATCH", "path": "/users/123", "body": {...} }
  ]
}
```

### Webhooks
```http
POST /webhooks/configure
{
  "url": "https://your-app.com/webhook",
  "events": ["user.created", "post.published"],
  "secret": "webhook_secret_key"
}
```

Idempotency, long-running operations, file uploads 및 soft deletes를 포함한 추가 패턴은 `references/common-patterns.md`를 참조하세요.

## Quick Reference Checklists

### REST Endpoint Design
- [ ] 컬렉션에 복수형 명사 사용
- [ ] URL nesting을 2단계로 제한
- [ ] 적절한 HTTP method 사용
- [ ] 정확한 status code 반환
- [ ] 일관된 에러 형식 구현
- [ ] 컬렉션에 Pagination 추가
- [ ] Filtering 및 sorting 포함
- [ ] OpenAPI로 문서화
- [ ] Authentication 구현
- [ ] Rate limiting 추가

### GraphQL Schema Design
- [ ] 명확한 type hierarchy 정의
- [ ] Nullable type을 적절하게 사용
- [ ] Pagination(connections) 구현
- [ ] Input type을 사용한 mutation 설계
- [ ] Payload에 에러 반환
- [ ] 설명(Description)으로 스키마 문서화
- [ ] Authentication/authorization 구현
- [ ] N+1 쿼리 최적화 (DataLoader)

## Additional Resources

### Comprehensive References
- `references/rest_best_practices.md` - 전체 REST API 패턴, status code 및 구현 세부 정보
- `references/authentication.md` - OAuth 2.0, JWT, API keys, MFA 및 보안 모범 사례
- `references/versioning-strategies.md` - Versioning 접근 방식, deprecation 및 migration 전략
- `references/common-patterns.md` - Health check, webhooks, batch operations 등

### Examples
- `examples/openapi_spec.yaml` - 블로그 API를 위한 전체 OpenAPI 3.0 사양
- `examples/graphql_schema.graphql` - Query, mutation 및 subscription을 포함한 전체 GraphQL schema

### Tools
- `scripts/api_helper.py` - API 사양 생성, 검증 및 문서화 유틸리티
