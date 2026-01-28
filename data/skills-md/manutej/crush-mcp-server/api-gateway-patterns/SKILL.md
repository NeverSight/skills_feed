---
name: api-gateway-patterns
description: Comprehensive API gateway patterns skill covering Kong, routing, rate limiting, authentication, load balancing, traffic management, and production gateway architecture
---

# API Gateway Patterns

A comprehensive skill for implementing production-grade API gateways using Kong and industry best practices. This skill covers advanced routing, authentication, rate limiting, load balancing, traffic management, and observability patterns for microservices architectures.

## When to Use This Skill

Use this skill when:

- Implementing an API gateway for microservices architectures
- Managing traffic routing, load balancing, and service discovery
- Implementing authentication and authorization at the gateway level
- Enforcing rate limiting, quotas, and traffic policies
- Adding observability, logging, and monitoring to API traffic
- Implementing request/response transformation and caching
- Managing API versioning and deprecation strategies
- Setting up circuit breakers and resilience patterns
- Configuring multi-environment API deployments
- Implementing API security policies (CORS, CSRF, WAF)
- Building developer portals and API documentation
- Managing API lifecycle from development to production

## Core Concepts

### API Gateway Architecture

An API gateway acts as a single entry point for client applications, routing requests to appropriate backend services while providing cross-cutting concerns:

- **Reverse Proxy**: Routes client requests to backend services
- **API Composition**: Aggregates multiple service calls into single responses
- **Protocol Translation**: Converts between protocols (HTTP, gRPC, WebSocket)
- **Cross-Cutting Concerns**: Authentication, logging, rate limiting, caching
- **Traffic Management**: Load balancing, circuit breaking, retries
- **Security**: SSL termination, API key validation, OAuth2 flows

### Key Gateway Components

1. **Services**: Upstream APIs that the gateway proxies to
2. **Routes**: Request matching rules that determine service routing
3. **Upstreams**: Load balancer configurations for service instances
4. **Plugins**: Extensible middleware for features (auth, logging, etc.)
5. **Consumers**: API clients with authentication credentials
6. **Certificates**: SSL/TLS certificates for secure communication
7. **SNIs**: Server Name Indication for multi-domain SSL

### Kong Gateway Fundamentals

Kong is a cloud-native, platform-agnostic, scalable API gateway:

**Architecture:**
- **Control Plane**: Admin API for configuration management
- **Data Plane**: Proxy layer handling runtime traffic
- **Database**: PostgreSQL or Cassandra for config storage (or DB-less mode)
- **Plugin System**: Lua-based extensibility for custom logic

**Core Entities:**
```
Service (upstream API)
  └── Routes (request matching)
       └── Plugins (features/policies)

Upstream (load balancer)
  └── Targets (service instances)

Consumer (API client)
  └── Credentials (auth keys/tokens)
       └── Plugins (consumer-specific policies)
```

## Routing Patterns

### Pattern 1: Path-Based Routing

Route requests based on URL paths to different backend services.

**Use Case:** Microservices with distinct URL prefixes (e.g., /users, /orders, /products)

**Configuration:**
```yaml
# Users Service
service:
  name: users-service
  url: http://users-api:8001

routes:
  - name: users-route
    paths:
      - /users
      - /api/users
    strip_path: true
    methods:
      - GET
      - POST
      - PUT
      - DELETE

# Orders Service
service:
  name: orders-service
  url: http://orders-api:8002

routes:
  - name: orders-route
    paths:
      - /orders
      - /api/orders
    strip_path: true
```

**Key Options:**
- `strip_path: true` - Removes matched path before proxying (e.g., /users/123 → /123)
- `strip_path: false` - Preserves full path (e.g., /users/123 → /users/123)
- `preserve_host: true` - Forwards original Host header to upstream

### Pattern 2: Header-Based Routing

Route based on HTTP headers for A/B testing, canary deployments, or API versioning.

**Use Case:** Gradual rollout of new API versions or feature flags

**Configuration:**
```yaml
# V1 Service (stable)
service:
  name: api-v1
  url: http://api-v1:8001

routes:
  - name: api-v1-route
    paths:
      - /api
    headers:
      X-API-Version:
        - "1"
        - "1.0"

# V2 Service (beta)
service:
  name: api-v2
  url: http://api-v2:8002

routes:
  - name: api-v2-route
    paths:
      - /api
    headers:
      X-API-Version:
        - "2"
        - "2.0"

# Default route (no version header)
routes:
  - name: api-default
    paths:
      - /api
    # Routes to V1 by default
```

**Advanced Header Routing:**
```yaml
# Mobile vs Web routing
routes:
  - name: mobile-api
    headers:
      User-Agent:
        - ".*Mobile.*"
        - ".*Android.*"
        - ".*iOS.*"
    service: mobile-optimized-api

  - name: web-api
    headers:
      User-Agent:
        - ".*Chrome.*"
        - ".*Firefox.*"
        - ".*Safari.*"
    service: web-api
```

### Pattern 3: Method-Based Routing

Route different HTTP methods to specialized services.

**Use Case:** CQRS pattern - separate read and write services

**Configuration:**
```yaml
# Read Service (queries)
service:
  name: query-service
  url: http://read-api:8001

routes:
  - name: read-operations
    paths:
      - /api/resources
    methods:
      - GET
      - HEAD
      - OPTIONS

# Write Service (commands)
service:
  name: command-service
  url: http://write-api:8002

routes:
  - name: write-operations
    paths:
      - /api/resources
    methods:
      - POST
      - PUT
      - PATCH
      - DELETE
```

### Pattern 4: Host-Based Routing

Route based on the requested hostname for multi-tenant applications.

**Use Case:** Different subdomains for different customers or environments

**Configuration:**
```yaml
# Tenant A
service:
  name: tenant-a-api
  url: http://tenant-a:8001

routes:
  - name: tenant-a-route
    hosts:
      - tenant-a.api.example.com
      - a.api.example.com

# Tenant B
service:
  name: tenant-b-api
  url: http://tenant-b:8002

routes:
  - name: tenant-b-route
    hosts:
      - tenant-b.api.example.com
      - b.api.example.com

# Wildcard for dynamic tenants
routes:
  - name: dynamic-tenant
    hosts:
      - "*.api.example.com"
    service: multi-tenant-api
```

### Pattern 5: Weighted Routing (Canary Deployments)

Gradually shift traffic between service versions.

**Implementation:**
```yaml
# Create two upstreams with weight distribution
upstream:
  name: api-upstream
  algorithm: round-robin

targets:
  - target: api-v1:8001
    weight: 90  # 90% traffic to stable version

  - target: api-v2:8002
    weight: 10  # 10% traffic to canary version

service:
  name: api-service
  host: api-upstream  # Points to upstream

routes:
  - name: api-route
    paths:
      - /api
```

**Gradual Rollout Strategy:**
1. Start: 100% v1, 0% v2
2. Phase 1: 90% v1, 10% v2 (monitor metrics)
3. Phase 2: 75% v1, 25% v2
4. Phase 3: 50% v1, 50% v2
5. Phase 4: 25% v1, 75% v2
6. Complete: 0% v1, 100% v2

## Rate Limiting Patterns

### Pattern 1: Global Rate Limiting

Protect your entire API from abuse with global limits.

**Use Case:** Prevent DDoS attacks and ensure fair usage

**Configuration:**
```yaml
plugins:
  - name: rate-limiting
    config:
      minute: 1000
      hour: 10000
      day: 100000
      policy: local  # or 'cluster', 'redis'
      fault_tolerant: true
      hide_client_headers: false
      limit_by: ip  # or 'consumer', 'credential', 'service'
```

**Policy Options:**
- `local`: In-memory, single node (not cluster-safe)
- `cluster`: Shared across Kong nodes via database
- `redis`: High-performance distributed limiting via Redis

### Pattern 2: Consumer-Specific Rate Limiting

Different limits for different API consumers (tiers).

**Use Case:** Freemium model with tiered pricing

**Configuration:**
```yaml
# Free tier consumer
consumer:
  username: free-user-123

plugins:
  - name: rate-limiting
    consumer: free-user-123
    config:
      minute: 10
      hour: 100
      day: 1000

# Premium tier consumer
consumer:
  username: premium-user-456

plugins:
  - name: rate-limiting
    consumer: premium-user-456
    config:
      minute: 1000
      hour: 10000
      day: 100000

# Enterprise tier (unlimited)
consumer:
  username: enterprise-user-789
# No rate limiting plugin for enterprise
```

### Pattern 3: Endpoint-Specific Rate Limiting

Different limits for different API endpoints.

**Use Case:** Protect expensive operations while allowing higher rates for cheap ones

**Configuration:**
```yaml
# Expensive search endpoint - strict limits
routes:
  - name: search-route
    paths:
      - /api/search

plugins:
  - name: rate-limiting
    route: search-route
    config:
      minute: 10
      hour: 100

# Regular CRUD endpoints - moderate limits
routes:
  - name: users-route
    paths:
      - /api/users

plugins:
  - name: rate-limiting
    route: users-route
    config:
      minute: 100
      hour: 1000

# Health check - no limits
routes:
  - name: health-route
    paths:
      - /health
# No rate limiting plugin
```

### Pattern 4: Sliding Window Rate Limiting

More accurate rate limiting using sliding windows.

**Use Case:** Prevent burst attacks that exploit fixed window boundaries

**Configuration:**
```yaml
plugins:
  - name: rate-limiting-advanced  # Kong Enterprise
    config:
      limit:
        - 100  # Limit value
      window_size:
        - 60  # Window in seconds
      window_type: sliding
      retry_after_jitter_max: 1
      sync_rate: 0.5
      namespace: my-api
      strategy: redis
      redis:
        host: redis
        port: 6379
        database: 0
```

**Sliding vs Fixed Windows:**
- Fixed: 100 requests per minute resets at :00 seconds
- Sliding: 100 requests in any 60-second window
- Sliding prevents burst exploitation at window boundaries

### Pattern 5: Quota Management

Long-term usage quotas (monthly, yearly).

**Use Case:** Enforce subscription limits based on plan

**Configuration:**
```yaml
plugins:
  - name: request-termination
    enabled: false  # Will be enabled when quota exceeded

plugins:
  - name: acme  # Custom quota tracking plugin
    config:
      quota:
        month: 1000000
      reset_on: first_day
      consumer_groups:
        - name: starter
          quota: 10000
        - name: professional
          quota: 100000
        - name: enterprise
          quota: 1000000
```

## Authentication Patterns

### Pattern 1: API Key Authentication

Simple API key validation for basic security.

**Use Case:** Internal APIs, development environments, simple integrations

**Configuration:**
```yaml
# Enable key-auth plugin
plugins:
  - name: key-auth
    config:
      key_names:
        - apikey
        - api-key
        - X-API-Key
      hide_credentials: true
      anonymous: null  # Require authentication
      run_on_preflight: false

# Create consumer with API key
consumers:
  - username: mobile-app
    custom_id: app-001

# Add key credential
keyauth_credentials:
  - consumer: mobile-app
    key: sk_live_abc123def456ghi789
```

**Usage:**
```bash
curl -H "apikey: sk_live_abc123def456ghi789" \
  https://api.example.com/users
```

**Best Practices:**
- Use cryptographically random keys (min 32 chars)
- Rotate keys periodically
- Different keys for different environments
- Never commit keys to version control
- Use HTTPS to protect keys in transit

### Pattern 2: JWT Authentication

Token-based authentication with payload verification.

**Use Case:** Modern SPAs, mobile apps, microservices

**Configuration:**
```yaml
plugins:
  - name: jwt
    config:
      uri_param_names:
        - jwt
      cookie_names:
        - jwt_token
      header_names:
        - Authorization
      claims_to_verify:
        - exp
        - nbf
      key_claim_name: iss
      secret_is_base64: false
      anonymous: null
      run_on_preflight: false
      maximum_expiration: 3600  # 1 hour max

# Create consumer with JWT credential
consumers:
  - username: web-app

jwt_secrets:
  - consumer: web-app
    key: myapp-issuer
    algorithm: HS256
    secret: my-secret-key-change-in-production
```

**RS256 (Asymmetric) Configuration:**
```yaml
jwt_secrets:
  - consumer: mobile-app
    key: mobile-issuer
    algorithm: RS256
    rsa_public_key: |
      -----BEGIN PUBLIC KEY-----
      MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
      -----END PUBLIC KEY-----
```

**Token Format:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJteWFwcC1pc3N1ZXIiLCJzdWIiOiJ1c2VyMTIzIiwiZXhwIjoxNjQwOTk1MjAwfQ.signature
```

### Pattern 3: OAuth 2.0 Authorization

Full OAuth 2.0 flows for third-party integrations.

**Use Case:** Public APIs, third-party developer access

**Supported Flows:**
- Authorization Code Flow
- Client Credentials Flow
- Implicit Flow (deprecated)
- Resource Owner Password Flow

**Configuration:**
```yaml
plugins:
  - name: oauth2
    config:
      scopes:
        - read
        - write
        - admin
      mandatory_scope: true
      token_expiration: 3600
      enable_authorization_code: true
      enable_client_credentials: true
      enable_implicit_grant: false
      enable_password_grant: false
      hide_credentials: true
      accept_http_if_already_terminated: false
      refresh_token_ttl: 1209600  # 14 days

# Create OAuth application
oauth2_credentials:
  - consumer: third-party-app
    name: "Partner Integration"
    client_id: client_abc123
    client_secret: secret_xyz789
    redirect_uris:
      - https://partner.com/callback
```

**Authorization Code Flow:**
```bash
# 1. Get authorization code
GET /oauth2/authorize?
  response_type=code&
  client_id=client_abc123&
  redirect_uri=https://partner.com/callback&
  scope=read write

# 2. Exchange code for token
POST /oauth2/token
  grant_type=authorization_code&
  client_id=client_abc123&
  client_secret=secret_xyz789&
  code=AUTH_CODE&
  redirect_uri=https://partner.com/callback
```

### Pattern 4: OpenID Connect (OIDC)

Enterprise SSO integration with identity providers.

**Use Case:** Enterprise authentication with Google, Okta, Auth0, Azure AD

**Configuration:**
```yaml
plugins:
  - name: openid-connect
    config:
      issuer: https://accounts.google.com
      client_id: your-client-id.apps.googleusercontent.com
      client_secret: your-client-secret
      redirect_uri:
        - https://api.example.com/callback
      scopes:
        - openid
        - email
        - profile
      auth_methods:
        - authorization_code
      login_redirect_uri: https://app.example.com/login
      logout_redirect_uri: https://app.example.com/logout
      ssl_verify: true
      session_secret: change-this-secret-in-production
      discovery: https://accounts.google.com/.well-known/openid-configuration
```

**Multi-Provider Configuration:**
```yaml
# Google OIDC
plugins:
  - name: openid-connect
    route: google-login
    config:
      issuer: https://accounts.google.com
      client_id: google-client-id
      client_secret: google-secret

# Azure AD OIDC
plugins:
  - name: openid-connect
    route: azure-login
    config:
      issuer: https://login.microsoftonline.com/tenant-id/v2.0
      client_id: azure-client-id
      client_secret: azure-secret

# Okta OIDC
plugins:
  - name: openid-connect
    route: okta-login
    config:
      issuer: https://dev-123456.okta.com
      client_id: okta-client-id
      client_secret: okta-secret
```

### Pattern 5: mTLS (Mutual TLS) Authentication

Certificate-based authentication for service-to-service security.

**Use Case:** Microservices mutual authentication, B2B integrations

**Configuration:**
```yaml
# Enable mTLS plugin
plugins:
  - name: mtls-auth
    config:
      ca_certificates:
        - ca-cert-id-1
        - ca-cert-id-2
      skip_consumer_lookup: false
      anonymous: null
      revocation_check_mode: SKIP  # or IGNORE_CA_ERROR, STRICT

# Upload CA certificate
ca_certificates:
  - cert: |
      -----BEGIN CERTIFICATE-----
      MIIDXTCCAkWgAwIBAgIJAKL...
      -----END CERTIFICATE-----

# Create consumer mapped to client certificate
consumers:
  - username: service-a
    custom_id: service-a-001

# Map certificate to consumer
mtls_auth_credentials:
  - consumer: service-a
    subject_name: CN=service-a,O=MyOrg
```

## Load Balancing Patterns

### Pattern 1: Round-Robin Load Balancing

Distribute requests evenly across service instances.

**Use Case:** Stateless services with uniform capacity

**Configuration:**
```yaml
upstreams:
  - name: api-upstream
    algorithm: round-robin
    slots: 10000
    healthchecks:
      active:
        type: http
        http_path: /health
        healthy:
          interval: 5
          successes: 2
        unhealthy:
          interval: 5
          http_failures: 3
          timeouts: 3
      passive:
        healthy:
          successes: 5
        unhealthy:
          http_failures: 5
          timeouts: 2

targets:
  - upstream: api-upstream
    target: api-1.internal:8001
    weight: 100

  - upstream: api-upstream
    target: api-2.internal:8001
    weight: 100

  - upstream: api-upstream
    target: api-3.internal:8001
    weight: 100
```

### Pattern 2: Weighted Load Balancing

Distribute traffic proportionally based on server capacity.

**Use Case:** Heterogeneous servers with different capacities

**Configuration:**
```yaml
upstreams:
  - name: api-upstream
    algorithm: round-robin

targets:
  # Powerful server - 50% traffic
  - target: api-1.internal:8001
    weight: 500

  # Medium server - 30% traffic
  - target: api-2.internal:8001
    weight: 300

  # Small server - 20% traffic
  - target: api-3.internal:8001
    weight: 200
```

**Weight Distribution:**
- Total weight: 500 + 300 + 200 = 1000
- api-1: 500/1000 = 50% of requests
- api-2: 300/1000 = 30% of requests
- api-3: 200/1000 = 20% of requests

### Pattern 3: Consistent Hashing

Route requests from same client to same backend (session affinity).

**Use Case:** Stateful services requiring session persistence

**Configuration:**
```yaml
upstreams:
  - name: api-upstream
    algorithm: consistent-hashing
    hash_on: header
    hash_on_header: X-User-ID
    hash_fallback: ip
    hash_fallback_header: X-Forwarded-For

targets:
  - target: api-1.internal:8001
  - target: api-2.internal:8001
  - target: api-3.internal:8001
```

**Hashing Options:**
- `hash_on: none` - Random distribution
- `hash_on: consumer` - Hash by authenticated consumer
- `hash_on: ip` - Hash by client IP
- `hash_on: header` - Hash by specified header value
- `hash_on: cookie` - Hash by cookie value
- `hash_on: path` - Hash by request path

**Use Cases by Hash Type:**
- User sessions: `hash_on: header` (X-User-ID)
- Geographic routing: `hash_on: ip`
- Tenant isolation: `hash_on: header` (X-Tenant-ID)
- Shopping carts: `hash_on: cookie` (session_id)

### Pattern 4: Least Connections

Route to server with fewest active connections.

**Use Case:** Long-lived connections (WebSockets, streaming)

**Configuration:**
```yaml
upstreams:
  - name: websocket-upstream
    algorithm: least-connections

targets:
  - target: ws-1.internal:8001
  - target: ws-2.internal:8001
  - target: ws-3.internal:8001
```

**When to Use:**
- WebSocket servers
- Long-polling endpoints
- Streaming APIs (SSE, gRPC streaming)
- Services with variable request duration

### Pattern 5: Active Health Checks

Automatically remove unhealthy targets from rotation.

**Use Case:** High availability with automatic failover

**Configuration:**
```yaml
upstreams:
  - name: api-upstream
    healthchecks:
      active:
        type: http
        http_path: /health
        https_verify_certificate: true
        concurrency: 10
        timeout: 1
        headers:
          X-Health-Check:
            - gateway
        healthy:
          interval: 5  # Check every 5 seconds
          http_statuses:
            - 200
            - 302
          successes: 2  # 2 successes → healthy
        unhealthy:
          interval: 5
          http_statuses:
            - 429
            - 500
            - 503
          http_failures: 3  # 3 failures → unhealthy
          tcp_failures: 3
          timeouts: 3

      passive:
        type: http
        healthy:
          http_statuses:
            - 200
            - 201
            - 202
            - 203
            - 204
            - 205
            - 206
            - 207
            - 208
            - 226
            - 300
            - 301
            - 302
          successes: 5
        unhealthy:
          http_statuses:
            - 429
            - 500
            - 503
          http_failures: 5
          tcp_failures: 2
          timeouts: 2
```

## Traffic Control Patterns

### Pattern 1: Circuit Breaker

Prevent cascading failures by failing fast when downstream is unhealthy.

**Use Case:** Protect your system when dependencies fail

**Configuration:**
```yaml
plugins:
  - name: proxy-cache-advanced  # Kong Enterprise
    config:
      # Serve stale cache during outages
      cache_control: false

plugins:
  - name: request-termination
    enabled: false  # Enabled programmatically on circuit open

# Custom circuit breaker (via passive health checks)
upstreams:
  - name: api-upstream
    healthchecks:
      passive:
        unhealthy:
          http_failures: 5  # Open circuit after 5 failures
          timeouts: 3
        healthy:
          successes: 3  # Close circuit after 3 successes
```

**Circuit States:**
1. **Closed**: Normal operation, requests flow through
2. **Open**: Failures detected, requests fail immediately
3. **Half-Open**: Test if service recovered, allow limited requests

### Pattern 2: Request Timeout

Prevent slow requests from tying up resources.

**Use Case:** Prevent resource exhaustion from slow backends

**Configuration:**
```yaml
services:
  - name: api-service
    url: http://api.internal:8001
    read_timeout: 5000    # 5 seconds
    write_timeout: 5000   # 5 seconds
    connect_timeout: 2000 # 2 seconds

plugins:
  - name: request-timeout  # Additional timeout enforcement
    config:
      http_timeout: 5000
      stream_timeout: 30000
```

**Timeout Strategy:**
```
connect_timeout: 2s   → Connection establishment
write_timeout: 5s     → Writing request to upstream
read_timeout: 5s      → Reading response from upstream
http_timeout: 5s      → Overall HTTP transaction
```

### Pattern 3: Retry Logic

Automatically retry failed requests with exponential backoff.

**Use Case:** Handle transient failures in distributed systems

**Configuration:**
```yaml
services:
  - name: api-service
    retries: 5  # Maximum retry attempts

plugins:
  - name: proxy-retry  # Custom retry plugin
    config:
      retries: 3
      retry_on:
        - 500
        - 502
        - 503
        - 504
      backoff:
        type: exponential
        base: 2
        max: 30
      jitter: 0.5
```

**Retry Schedule:**
```
Attempt 1: Immediate
Attempt 2: 2s + jitter
Attempt 3: 4s + jitter
Attempt 4: 8s + jitter
Attempt 5: 16s + jitter
```

**Idempotency Considerations:**
- Retry GET, HEAD, PUT, DELETE (idempotent)
- DO NOT retry POST unless idempotency keys used
- Check for Idempotency-Key header

### Pattern 4: Request Size Limiting

Prevent large payload attacks and memory exhaustion.

**Use Case:** Protect against oversized request bodies

**Configuration:**
```yaml
plugins:
  - name: request-size-limiting
    config:
      allowed_payload_size: 10  # Megabytes
      size_unit: megabytes
      require_content_length: true

# Different limits per route
plugins:
  - name: request-size-limiting
    route: file-upload
    config:
      allowed_payload_size: 100  # Allow larger files

  - name: request-size-limiting
    route: api-endpoints
    config:
      allowed_payload_size: 1  # Strict limit for APIs
```

### Pattern 5: Traffic Shaping (Throttling)

Control request rate beyond simple rate limiting.

**Use Case:** Smooth traffic spikes, prevent backend overload

**Configuration:**
```yaml
plugins:
  - name: request-transformer-advanced
    config:
      # Add delay headers for client-side throttling
      add:
        headers:
          - "Retry-After:60"

plugins:
  - name: proxy-cache-advanced
    config:
      # Cache responses to reduce backend load
      cache_ttl: 300
      strategy: memory

# Upstream connection limits
upstreams:
  - name: api-upstream
    slots: 1000  # Limit concurrent connections
```

## Request/Response Transformation

### Pattern 1: Request Header Manipulation

Add, modify, or remove request headers before proxying.

**Use Case:** Add authentication, tracing, or context headers

**Configuration:**
```yaml
plugins:
  - name: request-transformer
    config:
      add:
        headers:
          - "X-Gateway:kong"
          - "X-Request-ID:$(uuid)"
          - "X-Forwarded-Proto:https"
      append:
        headers:
          - "X-Trace-Id:$(uuid)"
      replace:
        headers:
          - "User-Agent:Kong-Gateway/3.0"
      remove:
        headers:
          - "X-Internal-Secret"
```

**Advanced Transformations:**
```yaml
plugins:
  - name: request-transformer-advanced
    config:
      add:
        headers:
          - "X-Consumer-Username:$(consumer_username)"
          - "X-Consumer-ID:$(consumer_id)"
          - "X-Authenticated-Scope:$(authenticated_credential.scope)"
          - "X-Client-IP:$(remote_addr)"
      rename:
        headers:
          - "Authorization:X-Original-Auth"
```

### Pattern 2: Response Header Manipulation

Modify response headers before returning to client.

**Use Case:** Add security headers, CORS, caching directives

**Configuration:**
```yaml
plugins:
  - name: response-transformer
    config:
      add:
        headers:
          - "X-Gateway-Response-Time:$(latencies.request)"
          - "X-Server-ID:$(upstream_addr)"
      remove:
        headers:
          - "X-Powered-By"
          - "Server"

# Security headers
plugins:
  - name: response-transformer
    config:
      add:
        headers:
          - "Strict-Transport-Security:max-age=31536000; includeSubDomains"
          - "X-Content-Type-Options:nosniff"
          - "X-Frame-Options:DENY"
          - "X-XSS-Protection:1; mode=block"
          - "Content-Security-Policy:default-src 'self'"
```

### Pattern 3: Request Body Transformation

Modify request payloads before forwarding.

**Use Case:** Add fields, transform formats, sanitize input

**Configuration:**
```yaml
plugins:
  - name: request-transformer-advanced
    config:
      add:
        body:
          - "gateway_timestamp:$(timestamp)"
          - "request_id:$(uuid)"
      remove:
        body:
          - "internal_field"
      replace:
        body:
          - "api_version:v2"
```

### Pattern 4: GraphQL to REST Translation

Expose REST APIs as GraphQL endpoints.

**Use Case:** Modernize legacy REST APIs with GraphQL

**Configuration:**
```yaml
plugins:
  - name: graphql-proxy-cache-advanced
    config:
      strategy: memory

# Define GraphQL schema mapping
graphql_schemas:
  - name: users-graphql
    schema: |
      type Query {
        user(id: ID!): User
        users: [User]
      }

      type User {
        id: ID!
        name: String!
        email: String!
      }
    resolvers:
      Query:
        user: http://users-api/users/{id}
        users: http://users-api/users
```

### Pattern 5: Protocol Translation

Convert between HTTP, gRPC, and WebSocket protocols.

**Use Case:** Expose gRPC services via HTTP/JSON

**Configuration:**
```yaml
# gRPC to HTTP/JSON
plugins:
  - name: grpc-gateway
    config:
      proto: /path/to/service.proto

services:
  - name: grpc-service
    url: grpc://grpc.internal:9000
    protocol: grpc

routes:
  - name: grpc-http-route
    paths:
      - /v1/users
    protocols:
      - http
      - https
```

## Caching Patterns

### Pattern 1: Response Caching

Cache upstream responses to reduce backend load.

**Use Case:** Cache expensive queries, reduce database load

**Configuration:**
```yaml
plugins:
  - name: proxy-cache
    config:
      strategy: memory  # or 'redis'
      content_type:
        - "application/json"
        - "text/html"
      cache_ttl: 300  # 5 minutes
      cache_control: false  # Ignore client cache headers
      storage_ttl: 600  # Backend storage TTL
      memory:
        dictionary_name: kong_cache
      vary_headers:
        - "Accept-Language"
        - "X-User-Tier"
```

**Redis-Based Caching:**
```yaml
plugins:
  - name: proxy-cache-advanced
    config:
      strategy: redis
      cache_ttl: 3600
      redis:
        host: redis.internal
        port: 6379
        database: 0
        password: redis-password
        timeout: 2000
        sentinel_master: mymaster
        sentinel_addresses:
          - redis-sentinel-1:26379
          - redis-sentinel-2:26379
```

### Pattern 2: Conditional Caching

Cache based on status codes, headers, or request criteria.

**Use Case:** Cache only successful responses, skip errors

**Configuration:**
```yaml
plugins:
  - name: proxy-cache-advanced
    config:
      response_code:
        - 200
        - 301
        - 302
      request_method:
        - GET
        - HEAD
      vary_headers:
        - "Accept"
        - "Accept-Encoding"
      vary_query_params:
        - "page"
        - "limit"
      ignore_uri_case: true
```

### Pattern 3: Cache Invalidation

Purge cache on-demand or based on events.

**Use Case:** Update cache when data changes

**Configuration:**
```yaml
# Admin API cache purge
POST /cache/purge

# Purge specific endpoint
POST /cache/purge/users

# TTL-based expiration
plugins:
  - name: proxy-cache
    config:
      cache_ttl: 60  # Short TTL for frequently updated data

# Event-based invalidation (custom plugin)
plugins:
  - name: custom-cache-invalidator
    config:
      invalidate_on:
        - POST
        - PUT
        - PATCH
        - DELETE
      propagate: true  # Clear related caches
```

### Pattern 4: Multi-Tier Caching

Layer caching at gateway and backend.

**Use Case:** Maximize cache hit rate across layers

**Architecture:**
```
Client
  ↓
Kong Gateway Cache (L1)
  ↓
Backend API Cache (L2)
  ↓
Database
```

**Configuration:**
```yaml
# Gateway cache (L1)
plugins:
  - name: proxy-cache
    config:
      strategy: memory
      cache_ttl: 60  # 1 minute

# Backend passes Cache-Control headers
# Gateway respects them if cache_control: true
plugins:
  - name: proxy-cache
    config:
      cache_control: true  # Respect upstream Cache-Control
      vary_headers:
        - "Cache-Control"
```

### Pattern 5: Surrogate-Key Based Invalidation

Tag caches for granular invalidation.

**Use Case:** Invalidate related resources efficiently

**Configuration:**
```yaml
# Tag responses with surrogate keys
plugins:
  - name: response-transformer
    config:
      add:
        headers:
          - "Surrogate-Key:user-$(user_id) tenant-$(tenant_id)"

# Invalidate by surrogate key
# Custom plugin or Varnish integration
POST /cache/purge
Headers:
  Surrogate-Key: user-123
```

## Security Patterns

### Pattern 1: CORS (Cross-Origin Resource Sharing)

Enable controlled cross-origin requests.

**Use Case:** Web apps calling APIs from different domains

**Configuration:**
```yaml
plugins:
  - name: cors
    config:
      origins:
        - "https://app.example.com"
        - "https://admin.example.com"
      methods:
        - GET
        - POST
        - PUT
        - PATCH
        - DELETE
        - OPTIONS
      headers:
        - Accept
        - Authorization
        - Content-Type
        - X-Request-ID
      exposed_headers:
        - X-Total-Count
        - X-Page-Number
      credentials: true
      max_age: 3600
      preflight_continue: false
```

**Wildcard CORS (Development Only):**
```yaml
plugins:
  - name: cors
    config:
      origins:
        - "*"
      methods:
        - "*"
      headers:
        - "*"
      credentials: false  # Must be false with wildcard origins
```

### Pattern 2: IP Restriction

Allow or deny based on IP addresses.

**Use Case:** Restrict admin APIs to office IPs

**Configuration:**
```yaml
# Whitelist approach
plugins:
  - name: ip-restriction
    config:
      allow:
        - 10.0.0.0/8
        - 192.168.1.100
        - 203.0.113.0/24

# Blacklist approach
plugins:
  - name: ip-restriction
    config:
      deny:
        - 1.2.3.4
        - 5.6.7.0/24
```

**Combined with Authentication:**
```yaml
# Admin route: IP + Auth
plugins:
  - name: ip-restriction
    route: admin-api
    config:
      allow:
        - 10.0.0.0/8

  - name: key-auth
    route: admin-api
```

### Pattern 3: Bot Detection

Detect and block malicious bots.

**Use Case:** Prevent scraping, brute force, spam

**Configuration:**
```yaml
plugins:
  - name: bot-detection
    config:
      allow:
        - "googlebot"
        - "bingbot"
        - "slackbot"
      deny:
        - "curl"
        - "wget"
        - "scrapy"
      blacklist_cache_size: 10000
      whitelist_cache_size: 10000
```

### Pattern 4: Request Validation

Validate requests against schemas.

**Use Case:** Ensure API contract compliance, prevent injection

**Configuration:**
```yaml
plugins:
  - name: request-validator
    config:
      body_schema: |
        {
          "type": "object",
          "properties": {
            "username": {
              "type": "string",
              "minLength": 3,
              "maxLength": 50
            },
            "email": {
              "type": "string",
              "format": "email"
            },
            "age": {
              "type": "integer",
              "minimum": 18,
              "maximum": 120
            }
          },
          "required": ["username", "email"]
        }
      parameter_schema:
        - name: page
          in: query
          required: false
          schema:
            type: integer
            minimum: 1
```

### Pattern 5: WAF (Web Application Firewall)

Protect against OWASP Top 10 vulnerabilities.

**Use Case:** Block SQL injection, XSS, path traversal

**Configuration:**
```yaml
plugins:
  - name: waf  # Kong Enterprise or ModSecurity plugin
    config:
      rule_sets:
        - owasp_crs
      anomaly_threshold: 5
      paranoia_level: 1
      blocked_status_code: 403
```

## Observability Patterns

### Pattern 1: Request Logging

Log all API requests for audit and debugging.

**Use Case:** Compliance, debugging, analytics

**Configuration:**
```yaml
plugins:
  - name: file-log
    config:
      path: /var/log/kong/requests.log
      reopen: true

# JSON structured logging
plugins:
  - name: http-log
    config:
      http_endpoint: http://logstash:5000
      method: POST
      content_type: application/json
      timeout: 5000
      keepalive: 60000
      custom_fields_by_lua:
        request_id: "return kong.request.get_header('X-Request-ID')"
```

**Log to Multiple Destinations:**
```yaml
# Elasticsearch
plugins:
  - name: http-log
    config:
      http_endpoint: http://elasticsearch:9200/_bulk

# Splunk
plugins:
  - name: http-log
    config:
      http_endpoint: https://splunk:8088/services/collector
      headers:
        Authorization: "Splunk token"

# Datadog
plugins:
  - name: datadog
    config:
      host: datadog-agent
      port: 8125
```

### Pattern 2: Distributed Tracing

Track requests across microservices.

**Use Case:** Diagnose latency, understand request flow

**Configuration:**
```yaml
# Zipkin
plugins:
  - name: zipkin
    config:
      http_endpoint: http://zipkin:9411/api/v2/spans
      sample_ratio: 0.1  # Trace 10% of requests
      include_credential: true
      traceid_byte_count: 16
      header_type: preserve  # or 'jaeger', 'b3', 'w3c'

# Jaeger
plugins:
  - name: opentelemetry
    config:
      endpoint: http://jaeger:14268/api/traces
      resource_attributes:
        service.name: api-gateway
        service.version: 1.0.0
      batch_span_processor:
        max_queue_size: 2048
        batch_timeout: 5000
```

**W3C Trace Context:**
```yaml
plugins:
  - name: opentelemetry
    config:
      propagation:
        default: w3c
      headers:
        - traceparent
        - tracestate
```

### Pattern 3: Metrics Collection

Expose Prometheus metrics for monitoring.

**Use Case:** Monitor gateway performance, errors, latency

**Configuration:**
```yaml
plugins:
  - name: prometheus
    config:
      per_consumer: true
      status_code_metrics: true
      latency_metrics: true
      bandwidth_metrics: true
      upstream_health_metrics: true

# Expose /metrics endpoint
routes:
  - name: metrics
    paths:
      - /metrics
    service: prometheus-service
```

**Available Metrics:**
```
# Requests
kong_http_requests_total{service,route,code}

# Latency
kong_latency_ms{type,service,route}
kong_request_latency_ms{service,route}
kong_upstream_latency_ms{service,route}

# Bandwidth
kong_bandwidth_bytes{type,service,route}

# Connections
kong_datastore_reachable
kong_nginx_connections_total{state}
```

### Pattern 4: Health Checks

Expose health check endpoints.

**Use Case:** Kubernetes liveness/readiness probes

**Configuration:**
```yaml
# Gateway health
routes:
  - name: health
    paths:
      - /health
    plugins:
      - name: request-termination
        config:
          status_code: 200
          message: "OK"

# Detailed status
routes:
  - name: status
    paths:
      - /status
    service: kong-status-service

# Upstream health aggregation
plugins:
  - name: upstream-health-check
    config:
      healthy_threshold: 2
      unhealthy_threshold: 3
```

### Pattern 5: Error Tracking

Track and report errors to monitoring systems.

**Use Case:** Proactive error detection and alerting

**Configuration:**
```yaml
# Sentry integration
plugins:
  - name: sentry
    config:
      dsn: https://key@sentry.io/project
      environment: production
      release: v1.2.3

# Custom error logging
plugins:
  - name: http-log
    config:
      http_endpoint: http://error-tracker:5000
      custom_fields_by_lua:
        error_type: |
          if kong.response.get_status() >= 500 then
            return "server_error"
          elseif kong.response.get_status() >= 400 then
            return "client_error"
          end
```

## Multi-Environment Patterns

### Pattern 1: Environment Separation

Separate configurations for dev, staging, production.

**Use Case:** Consistent deployment across environments

**Structure:**
```
config/
  ├── base.yaml          # Shared configuration
  ├── dev.yaml           # Development overrides
  ├── staging.yaml       # Staging overrides
  └── production.yaml    # Production overrides
```

**Configuration:**
```yaml
# base.yaml
_format_version: "3.0"

services:
  - name: users-api
    url: http://users-service:8001

routes:
  - name: users-route
    service: users-api
    paths:
      - /users

# production.yaml
_format_version: "3.0"

services:
  - name: users-api
    url: https://users-api-prod.internal:8001
    retries: 5
    read_timeout: 5000

plugins:
  - name: rate-limiting
    service: users-api
    config:
      minute: 1000
```

### Pattern 2: Blue-Green Deployments

Zero-downtime deployments with instant rollback.

**Use Case:** Safe production deployments

**Configuration:**
```yaml
# Blue environment (current production)
upstreams:
  - name: api-blue
    targets:
      - target: api-blue-1:8001
      - target: api-blue-2:8001

# Green environment (new version)
upstreams:
  - name: api-green
    targets:
      - target: api-green-1:8001
      - target: api-green-2:8001

# Route points to active environment
services:
  - name: api-service
    host: api-blue  # Switch to api-green for deployment

# Rollback: Switch service.host back to api-blue
```

### Pattern 3: Canary Releases

Gradual rollout with monitoring.

**Use Case:** Risk mitigation for new releases

**Configuration:**
```yaml
# Canary routing with header
routes:
  - name: api-canary
    paths:
      - /api
    headers:
      X-Canary:
        - "true"
    service: api-v2

routes:
  - name: api-stable
    paths:
      - /api
    service: api-v1

# Weighted canary (10% traffic)
upstreams:
  - name: api-upstream
    targets:
      - target: api-v1:8001
        weight: 90
      - target: api-v2:8001
        weight: 10
```

**Canary Progression:**
```
Phase 1: 5% canary, monitor errors
Phase 2: 25% canary, check metrics
Phase 3: 50% canary, verify performance
Phase 4: 100% canary, deprecate old version
```

### Pattern 4: Feature Flags

Enable/disable features dynamically.

**Use Case:** A/B testing, gradual feature rollout

**Configuration:**
```yaml
# Feature flag via header
routes:
  - name: new-feature
    paths:
      - /api/new-feature
    headers:
      X-Feature-Flag:
        - "new-dashboard"
    service: new-feature-service

# Default route (feature disabled)
routes:
  - name: old-feature
    paths:
      - /api/new-feature
    service: old-feature-service

# Consumer-based feature flags
plugins:
  - name: request-transformer
    consumer: beta-users
    config:
      add:
        headers:
          - "X-Feature-Flags:new-dashboard,advanced-search"
```

### Pattern 5: Multi-Region Deployment

Route to nearest region for low latency.

**Use Case:** Global API with regional failover

**Configuration:**
```yaml
# US region
upstreams:
  - name: api-us
    targets:
      - target: api-us-east:8001
      - target: api-us-west:8001

# EU region
upstreams:
  - name: api-eu
    targets:
      - target: api-eu-west:8001
      - target: api-eu-central:8001

# Geographic routing (via DNS or header)
routes:
  - name: us-traffic
    hosts:
      - us.api.example.com
    service: api-us-service

routes:
  - name: eu-traffic
    hosts:
      - eu.api.example.com
    service: api-eu-service
```

## Best Practices

### Architecture Design

1. **Single Responsibility**: Gateway handles cross-cutting concerns only
2. **Stateless Design**: Keep gateway stateless for horizontal scaling
3. **Declarative Configuration**: Use YAML/JSON for version-controlled config
4. **Database-Less Mode**: Use DB-less for simpler deployments
5. **Plugin Minimalism**: Only enable necessary plugins

### Security Best Practices

1. **Defense in Depth**: Layer multiple security mechanisms
2. **Least Privilege**: Minimal permissions for consumers
3. **Secrets Management**: Never hardcode credentials
4. **TLS Everywhere**: Encrypt all traffic (client and upstream)
5. **Rate Limiting**: Always protect public endpoints
6. **Input Validation**: Validate all request data
7. **Regular Updates**: Keep Kong and plugins updated

### Performance Optimization

1. **Enable Caching**: Cache responses aggressively
2. **Connection Pooling**: Reuse upstream connections
3. **Load Balancing**: Distribute load evenly
4. **Health Checks**: Remove unhealthy targets quickly
5. **Timeouts**: Set appropriate timeouts to prevent hangs
6. **Monitoring**: Track latency, errors, throughput
7. **Resource Limits**: Set memory and connection limits

### Operational Excellence

1. **Logging**: Structured logging for all requests
2. **Monitoring**: Comprehensive metrics collection
3. **Alerting**: Alert on anomalies and errors
4. **Documentation**: Document all routes and plugins
5. **Testing**: Test gateway config in staging
6. **Versioning**: Version control all configurations
7. **Disaster Recovery**: Plan for failover scenarios

### Plugin Strategy

1. **Order Matters**: Plugins execute in specific order
2. **Scope Appropriately**: Global, service, route, or consumer
3. **Test Thoroughly**: Test plugin combinations
4. **Monitor Impact**: Track plugin performance overhead
5. **Custom Plugins**: Write custom plugins for unique needs

**Plugin Execution Order:**
```
1. Authentication (key-auth, jwt, oauth2)
2. Security (ip-restriction, bot-detection)
3. Traffic Control (rate-limiting, request-size-limiting)
4. Transformation (request-transformer)
5. Logging (file-log, http-log)
6. Analytics (prometheus, datadog)
```

### Configuration Management

1. **Version Control**: Git for all configurations
2. **Environment Parity**: Consistent configs across environments
3. **Automated Deployment**: CI/CD for configuration changes
4. **Validation**: Validate configs before applying
5. **Rollback Plan**: Quick rollback on issues
6. **Change Log**: Document all configuration changes

### Scaling Guidelines

1. **Horizontal Scaling**: Add more Kong nodes
2. **Database Scaling**: Scale PostgreSQL separately
3. **Cache Offloading**: Use Redis for distributed caching
4. **Regional Deployment**: Deploy close to users
5. **CDN Integration**: Offload static content
6. **Connection Limits**: Set per-worker limits

## Common Use Cases

### Use Case 1: SaaS API Platform

**Requirements:**
- Multi-tenant isolation
- Tiered pricing (free, pro, enterprise)
- Rate limiting per tier
- Analytics per customer
- Self-service developer portal

**Implementation:**
```yaml
# Tenant identification
plugins:
  - name: key-auth
    config:
      key_names:
        - X-API-Key

# Tier-based rate limiting
consumers:
  - username: free-tier-customer
    custom_id: customer-123

plugins:
  - name: rate-limiting
    consumer: free-tier-customer
    config:
      minute: 60
      hour: 1000

# Usage analytics
plugins:
  - name: prometheus
    config:
      per_consumer: true

# Request transformation (add tenant context)
plugins:
  - name: request-transformer
    config:
      add:
        headers:
          - "X-Tenant-ID:$(consumer_custom_id)"
```

### Use Case 2: Microservices Gateway

**Requirements:**
- Service discovery
- Load balancing
- Circuit breaking
- Distributed tracing
- Centralized authentication

**Implementation:**
```yaml
# Service registry
services:
  - name: users-service
    url: http://users.internal:8001

  - name: orders-service
    url: http://orders.internal:8002

  - name: inventory-service
    url: http://inventory.internal:8003

# Load balancing with health checks
upstreams:
  - name: users-upstream
    healthchecks:
      active:
        http_path: /health
        healthy:
          interval: 5

# Distributed tracing
plugins:
  - name: zipkin
    config:
      http_endpoint: http://zipkin:9411/api/v2/spans

# JWT authentication (single sign-on)
plugins:
  - name: jwt
    config:
      claims_to_verify:
        - exp
```

### Use Case 3: Mobile Backend

**Requirements:**
- Versioned APIs
- GraphQL support
- Offline caching
- Push notifications
- Device-based rate limiting

**Implementation:**
```yaml
# API versioning
routes:
  - name: api-v1
    paths:
      - /api/v1
    service: mobile-api-v1

  - name: api-v2
    paths:
      - /api/v2
    service: mobile-api-v2

# GraphQL endpoint
plugins:
  - name: graphql-proxy-cache-advanced
    route: graphql-route

# Aggressive caching for mobile
plugins:
  - name: proxy-cache
    config:
      cache_ttl: 3600
      strategy: redis

# Device-based rate limiting
plugins:
  - name: rate-limiting
    config:
      limit_by: header
      header_name: X-Device-ID
      minute: 100
```

### Use Case 4: Public API

**Requirements:**
- OAuth 2.0
- Developer portal
- API documentation
- Usage analytics
- Monetization

**Implementation:**
```yaml
# OAuth 2.0
plugins:
  - name: oauth2
    config:
      scopes:
        - read
        - write
        - admin
      enable_authorization_code: true

# Developer portal
routes:
  - name: developer-docs
    paths:
      - /docs
    service: developer-portal

# Usage tracking
plugins:
  - name: prometheus
    config:
      per_consumer: true

# Billing integration
plugins:
  - name: http-log
    config:
      http_endpoint: http://billing-system:5000
```

### Use Case 5: Legacy Modernization

**Requirements:**
- REST to GraphQL
- Protocol translation
- Request/response transformation
- Gradual migration
- Backward compatibility

**Implementation:**
```yaml
# GraphQL facade over REST
plugins:
  - name: graphql-proxy-cache-advanced

# SOAP to REST transformation
plugins:
  - name: request-transformer-advanced
    config:
      # Transform REST to SOAP
      replace:
        headers:
          - "Content-Type:text/xml"

# Version migration (route legacy to new)
upstreams:
  - name: api-upstream
    targets:
      - target: legacy-api:8001
        weight: 20  # 20% legacy
      - target: new-api:8002
        weight: 80  # 80% new
```

## Quick Reference

### Essential Commands

```bash
# Declarative configuration
deck sync -s kong.yaml

# Database migrations
kong migrations bootstrap
kong migrations up

# Start Kong
kong start

# Reload configuration
kong reload

# Health check
curl http://localhost:8001/status

# List services
curl http://localhost:8001/services

# List routes
curl http://localhost:8001/routes

# List plugins
curl http://localhost:8001/plugins
```

### Configuration Templates

**Minimal Service:**
```yaml
services:
  - name: my-service
    url: http://api.internal:8001

routes:
  - name: my-route
    service: my-service
    paths:
      - /api
```

**Production Service:**
```yaml
services:
  - name: production-service
    url: http://api.internal:8001
    protocol: http
    retries: 5
    connect_timeout: 5000
    read_timeout: 60000
    write_timeout: 60000

upstreams:
  - name: production-upstream
    algorithm: consistent-hashing
    hash_on: header
    hash_on_header: X-User-ID
    healthchecks:
      active:
        http_path: /health
        healthy:
          interval: 5
          successes: 2
        unhealthy:
          http_failures: 3
          timeouts: 3

targets:
  - upstream: production-upstream
    target: api-1:8001
  - upstream: production-upstream
    target: api-2:8001

routes:
  - name: production-route
    service: production-service
    paths:
      - /api
    protocols:
      - https
    strip_path: true
    preserve_host: false

plugins:
  - name: rate-limiting
    route: production-route
    config:
      minute: 1000
      policy: redis

  - name: jwt
    route: production-route

  - name: cors
    route: production-route

  - name: prometheus
    route: production-route
```

## Resources

- Kong Documentation: https://docs.konghq.com/
- Kong Gateway: https://konghq.com/kong/
- Kong Plugin Hub: https://docs.konghq.com/hub/
- Kong Admin API: https://docs.konghq.com/gateway/latest/admin-api/
- decK (Declarative Config): https://docs.konghq.com/deck/
- Kong Ingress Controller: https://docs.konghq.com/kubernetes-ingress-controller/
- Kong Community: https://discuss.konghq.com/

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: API Gateway, Microservices, Traffic Management
**Compatible With**: Kong Gateway 3.x, Kubernetes, Docker, Cloud Platforms
