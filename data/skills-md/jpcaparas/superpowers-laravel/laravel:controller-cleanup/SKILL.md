---
name: laravel:controller-cleanup
description: Reduce controller bloat using Form Requests for auth/validation, small Actions/Services with DTOs, and resource/single-action controllers
---

# Controller Cleanup

Keep controllers small and focused on orchestration.

## Move auth/validation to Form Requests

- Create a Request class (e.g., `StoreUserRequest`) and use `authorize()` + `rules()`
- Type-hint the Request in your controller method; Laravel runs it before the action

```
php artisan make:request StoreUserRequest
```

## Extract business logic to Actions/Services

- Create a small Action (one thing well) or a Service for larger workflows
- Pass a DTO from the Request to the Action to avoid leaking framework concerns

```php
final class CreateUserAction {
    public function __invoke(CreateUserDTO $dto): User { /* ... */ }
}
```

## Prefer Resource or Single-Action Controllers

- Use resource controllers for standard CRUD
- For one-off endpoints, use invokable (single-action) controllers

## Testing

- Write feature tests for the controller route
- Unit test Actions/Services independently with DTOs

