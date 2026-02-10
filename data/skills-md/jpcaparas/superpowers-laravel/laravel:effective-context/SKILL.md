---
name: laravel:effective-context
description: Provide comprehensive context in prompts—files, errors, Laravel version, dependencies, and monorepo details—for accurate AI responses
---

# Effective Context

Give the AI assistant the right context to generate accurate, relevant code. Missing context leads to generic solutions that don't fit your project.

## What to Include

### Files and Structure
- Reference specific files: `app/Models/User.php`, `routes/api.php`
- Mention relevant directories: "working in `app/Services/Payment`"
- Share project structure when it matters: "using repository pattern with interfaces in `app/Contracts`"

### Current State
- Show existing code you're modifying or extending
- Describe what works and what doesn't
- Include relevant configuration: `.env` settings, `config/` values

### Laravel Context
- **Version**: "Laravel 11.x" or "Laravel 12.x"
- **Dependencies**: Mention packages like Sanctum, Horizon, Telescope
- **Patterns in use**: "using Form Requests", "jobs with Horizon", "API resources"
- **Runner**: Specify if using Sail or host commands

### Monorepo Projects
- Specify which app: "working in `apps/api`" vs "working in `apps/admin`"
- Mention shared packages if relevant: "using shared `packages/common`"

## Describing Problems

### Errors
```
BAD: "Getting an error with users"

GOOD: "Getting error when creating user:
  Illuminate\Database\QueryException: SQLSTATE[23000]: 
  Integrity constraint violation: 1062 Duplicate entry
  
  In UserController@store, line 45:
  $user = User::create($request->validated());
  
  Using Laravel 11.x with MySQL 8.0"
```

### Stack Traces
Include the full stack trace, especially:
- The exception class and message
- File paths and line numbers
- The method chain that led to the error

### Reproduction Steps
```
1. POST to /api/users with email that exists
2. Validation passes (should catch this)
3. Database throws constraint violation
```

## Vague vs Specific

### Vague
"Add validation to the user form"

### Specific
"Add validation to UserStoreRequest:
- Email must be unique in users table
- Password min 12 chars, requires uppercase + number
- Name required, max 255 chars
- Optional phone field, must match E.164 format"

### Vague
"Need to handle payments"

### Specific
"Implement Stripe payment processing:
- Create PaymentService with charge() method
- Store payment records in payments table (user_id, amount, stripe_id, status)
- Dispatch ProcessPaymentJob to queue
- Handle webhook for payment.succeeded
- Using Laravel 11.x with Cashier"

## Quick Checklist

Before sending a prompt, verify:
- [ ] Mentioned Laravel version and relevant packages
- [ ] Included file paths or directory context
- [ ] Shared error messages and stack traces (if debugging)
- [ ] Specified validation rules, relationships, or business logic
- [ ] Noted if using Sail or host commands
- [ ] Identified which app (if monorepo)

More context = better results. When in doubt, include it.
