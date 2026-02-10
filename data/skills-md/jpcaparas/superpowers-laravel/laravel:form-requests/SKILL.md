---
name: laravel:form-requests
description: Move validation and authorization into Form Requests; use rule objects, custom messages, and nested data handling to keep controllers slim
---

# Form Requests and Validation

Promote validation and authorization to dedicated Form Request classes. Keep controllers focused on orchestration and domain intents.

## Commands

```
# Create a request
sail artisan make:request UpdateProfileRequest      # or: php artisan make:request UpdateProfileRequest

# Use in controller method signature
public function update(UpdateProfileRequest $request) {
    $data = $request->validated();
    // ...
}
```

## Patterns

- Define `authorize()` to gate access; prefer Policies for complex checks
- Use rule objects: `Rule::unique('users', 'email')->ignore($user->id)`
- Validate nested arrays: `items.*.sku`, `addresses.home.city`
- Prefer `nullable` + specific rules instead of `sometimes` for optional fields
- Standardize attribute names / messages via `attributes()` and `messages()`
- Centralize common rules in custom `Rule` classes or traits
- Return `$request->safe()->only([...])` when partial updates are intended

## Testing

- Feature test the endpoint: assert validation errors and success flows
- Unit test custom validators and rule objects in isolation

