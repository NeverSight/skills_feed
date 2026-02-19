---
name: laravel:specifying-constraints
description: Define clear constraints—performance, security, testing, architecture, dependencies—so AI generates code that meets your project standards
---

# Specifying Constraints

Constraints guide the AI toward solutions that fit your project. Without them, you get generic code that may not meet your requirements.

## Performance Constraints

### Vague
"Make it fast"

### Specific
"Optimize product search:
- Response time < 200ms for 95th percentile
- Support 1000 concurrent users
- Cache results for 5 minutes using Redis
- Use database indexes on `name`, `category_id`, `published_at`
- Paginate results, max 50 per page
- Avoid N+1 queries with eager loading"

### Database Performance
"Query orders with performance constraints:
- Use `select()` to load only needed columns
- Eager load `items`, `customer`, `shipping_address` in one query
- Add composite index on `(user_id, created_at, status)`
- Use `chunk()` for batch processing > 1000 records
- Set query timeout to 5 seconds"

## Security Constraints

### Vague
"Make it secure"

### Specific
"Implement user profile update with security requirements:
- Authorize using `ProfilePolicy@update`
- Validate all inputs in `ProfileUpdateRequest`
- Sanitize HTML in bio field (strip scripts, allow basic formatting)
- Rate limit to 10 requests per minute per user
- Hash passwords with bcrypt (cost factor 12)
- Log all profile changes for audit trail
- Prevent mass assignment vulnerabilities with `$fillable`"

### API Security
"Secure the payment API:
- Require `auth:sanctum` middleware
- Validate API tokens have `process-payments` ability
- Use HTTPS only (enforce in middleware)
- Validate webhook signatures from payment provider
- Store sensitive data encrypted in database
- Never log credit card numbers or tokens
- Return generic error messages (don't leak system details)"

## Testing Constraints

### Vague
"Add tests"

### Specific
"Test the order processing feature:
- Feature test for complete order flow (create → process → confirm)
- Unit tests for OrderService methods
- Test validation failures (invalid payment, insufficient inventory)
- Test edge cases (zero quantity, negative prices)
- Mock external payment gateway
- Use factories for test data
- Aim for 80% code coverage on business logic
- Tests must run in < 30 seconds"

### Test Requirements
"Testing requirements for authentication:
- Test successful login with valid credentials
- Test failed login with invalid credentials
- Test rate limiting (max 5 attempts per minute)
- Test token expiration after 24 hours
- Test logout invalidates token
- Use `RefreshDatabase` trait
- No external API calls in tests (use mocks)"

## Architectural Constraints

### Patterns to Follow
"Implement payment processing following our architecture:
- Use repository pattern: `PaymentRepository` for data access
- Use service layer: `PaymentService` for business logic
- Use jobs for async work: `ProcessPaymentJob`
- Use events: `PaymentProcessed`, `PaymentFailed`
- Controllers orchestrate only, no business logic
- Keep cyclomatic complexity < 7 per method
- Follow SOLID principles"

### Patterns to Avoid
"Implement user management with these constraints:
- Don't use static methods or facades in business logic
- Don't put business logic in controllers or models
- Don't use global state or singletons
- Don't mix concerns (separate validation, business logic, persistence)
- Don't use raw SQL queries (use Eloquent or Query Builder)
- Don't bypass authorization checks"

## Dependency Constraints

### Version Requirements
"Add image processing feature:
- Use `intervention/image` ^3.0 (Laravel 11.x compatible)
- Requires PHP 8.2+
- Requires GD or Imagick extension
- Compatible with our existing `spatie/laravel-medialibrary` ^11.0
- No conflicts with current dependencies"

### Package Selection
"Choose a package for PDF generation:
- Must support Laravel 11.x
- Must handle UTF-8 and special characters
- Should support headers/footers
- Prefer actively maintained (updated in last 6 months)
- Check compatibility with our PHP 8.2 requirement
- Consider: `barryvdh/laravel-dompdf` or `spatie/laravel-pdf`"

## Constraint Templates

### Performance Template
```
- Response time: < X ms
- Throughput: Y requests/second
- Cache strategy: Redis, TTL Z minutes
- Database: indexes on [columns], eager load [relationships]
- Pagination: max X per page
```

### Security Template
```
- Authentication: [Sanctum/Passport/Session]
- Authorization: [Policy/Gate]
- Validation: [Form Request class]
- Rate limiting: X requests per Y minutes
- Data protection: [encryption/hashing requirements]
- Audit logging: [what to log]
```

### Testing Template
```
- Coverage: X% on business logic
- Test types: [feature/unit/integration]
- Mocking: [external services to mock]
- Factories: [models to factory]
- Performance: tests complete in < X seconds
- Edge cases: [specific scenarios to test]
```

## Quick Reference

Specify constraints clearly:
- **Performance** - Response times, throughput, caching, indexes
- **Security** - Auth, validation, rate limiting, data protection
- **Testing** - Coverage, test types, mocking, edge cases
- **Architecture** - Patterns to follow/avoid, complexity limits
- **Dependencies** - Versions, compatibility, package requirements

Clear constraints = code that fits your project.
