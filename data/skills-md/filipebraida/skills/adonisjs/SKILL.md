---
name: adonisjs
description: Build AdonisJS 6 features from scratch through production. Full lifecycle - build, debug, test, optimize, refactor. Follows TypeScript-first, Lucid ORM, and AdonisJS conventions.
---

<essential_principles>
## AdonisJS 6 Principles

**TypeScript-first** - Every request, service, and model is typed. Prefer explicit types over any.

### 1. Thin Controllers, Focused Services

Controllers orchestrate. Business logic lives in services or domain modules.

```ts
// app/controllers/users_controller.ts
import type { HttpContext } from "@adonisjs/core/http";
import CreateUserService from "#services/users/create_user_service";

export default class UsersController {
  async store({ request, response }: HttpContext) {
    const payload = await request.validateUsing(CreateUserService.validator);
    const user = await new CreateUserService().handle(payload);
    return response.created({ data: user });
  }
}
```

### 2. Validate Every Input with VineJS

Never trust request data. Validate on entry.

```ts
// app/validators/create_user.ts
import vine from "@vinejs/vine";

export const createUserValidator = vine.compile(
  vine.object({
    email: vine.string().email(),
    fullName: vine.string().minLength(2).maxLength(120),
    password: vine.string().minLength(8),
  }),
);
```

### 3. Lucid Models Own Persistence

Use models for persistence and relationships. Keep queries in one place.

```ts
// app/models/user.ts
import { BaseModel, column } from "@adonisjs/lucid/orm";

export default class User extends BaseModel {
  @column({ isPrimary: true })
  declare id: number;

  @column()
  declare email: string;
}
```

### 4. Middleware for Cross-Cutting Concerns

Authentication, tenant scoping, and rate limiting belong in middleware.

```ts
// app/middleware/auth_middleware.ts
import type { HttpContext } from "@adonisjs/core/http";
import type { NextFn } from "@adonisjs/core/types/http";

export default class AuthMiddleware {
  async handle(ctx: HttpContext, next: NextFn) {
    await ctx.auth.check();
    return next();
  }
}
```
</essential_principles>

<intake>
**What would you like to do?**

1. Build a new feature/endpoint
2. Debug an existing issue
3. Write/run tests
4. Optimize performance
5. Refactor code
6. Something else

**Then read the matching workflow from `workflows/` and follow it.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "new", "create", "build", "feature", "endpoint", "api" | `workflows/build-feature.md` |
| 2, "broken", "fix", "debug", "crash", "bug", "error" | `workflows/debug.md` |
| 3, "test", "tests", "spec", "coverage" | `workflows/write-tests.md` |
| 4, "slow", "optimize", "performance", "fast", "n+1" | `workflows/optimize-performance.md` |
| 5, "refactor", "clean", "improve", "restructure" | `workflows/refactor.md` |
| 6, other | Clarify, then select workflow or references |
</routing>

<verification_loop>
## After Every Change

```bash
# 1. Type check
pnpm typecheck

# 2. Run tests
node ace test tests/functional/changed.spec.ts

# 3. Lint
pnpm lint
```

Report: "Types: OK | Tests: X pass | Lint: clean"
</verification_loop>

<reference_index>
## Domain Knowledge

All in `references/`:

**Architecture:** architecture.md
**Models:** models.md
**Controllers:** controllers.md
**Serialization (DTOs):** serialization.md
**Validations:** validations-callbacks.md
**Background Jobs:** background-jobs.md
**Performance:** performance.md
**Testing:** testing.md
**Multi-Tenant:** multi-tenant.md
**Anti-Patterns:** anti-patterns.md
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| build-feature.md | Create new feature/endpoint from scratch |
| debug.md | Find and fix bugs |
| write-tests.md | Write and run tests |
| optimize-performance.md | Profile and speed up |
| refactor.md | Restructure code following patterns |
</workflows_index>
