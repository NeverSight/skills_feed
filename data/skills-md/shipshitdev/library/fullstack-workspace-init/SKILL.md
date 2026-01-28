---
name: fullstack-workspace-init
description: Scaffold a production-ready full-stack monorepo with working MVP features, tests, and CI/CD. Generates complete CRUD functionality, Clerk authentication, and quality gates that run immediately with `bun dev`.
---

# Full Stack Workspace Init

Create a **production-ready** monorepo with working MVP features:

- **Frontend:** NextJS 16 + React 19 + TypeScript + Tailwind + @agenticindiedev/ui
- **Backend:** NestJS 11 + MongoDB + Clerk Auth + Swagger
- **Mobile:** React Native + Expo (optional)
- **Quality:** Vitest (80% coverage) + Biome + Husky + GitHub Actions CI/CD
- **Package Manager:** bun

## What Makes This Different

This skill generates **working applications**, not empty scaffolds:

- Complete CRUD operations for your main entities
- Clerk authentication configured and working
- Tests with 80% coverage threshold
- GitHub Actions CI/CD pipeline
- Runs immediately with `bun dev`

---

## Workflow

### Phase 1: PRD Brief Intake

**Ask the user for a 1-2 paragraph product description**, then extract and confirm:

```
I'll help you build [Project Name]. Based on your description, I understand:

**Entities:**
- [Entity1]: [fields]
- [Entity2]: [fields]

**Features:**
- [Feature 1]
- [Feature 2]

**Routes:**
- / - Home/Dashboard
- /[entity] - List view
- /[entity]/[id] - Detail view

**API Endpoints:**
- GET/POST /api/[entity]
- GET/PATCH/DELETE /api/[entity]/:id

Is this correct? Any adjustments?
```

### Phase 2: Auth Setup (Always Included)

Generate Clerk authentication:

**Backend:**

- `auth/guards/clerk-auth.guard.ts` - Token verification guard
- `auth/decorators/current-user.decorator.ts` - User extraction decorator

**Frontend:**

- `providers/clerk-provider.tsx` - ClerkProvider wrapper
- `app/sign-in/[[...sign-in]]/page.tsx` - Sign in page
- `app/sign-up/[[...sign-up]]/page.tsx` - Sign up page
- `middleware.ts` - Protected route middleware

**Environment:**

- `.env.example` with all required variables

### Phase 3: Entity Generation

For each extracted entity, generate complete CRUD **with tests**:

**Backend (NestJS):**

```
api/apps/api/src/collections/{entity}/
├── {entity}.module.ts
├── {entity}.controller.ts         # Full CRUD + Swagger + ClerkAuthGuard
├── {entity}.controller.spec.ts    # Controller unit tests
├── {entity}.service.ts            # Business logic
├── {entity}.service.spec.ts       # Service unit tests
├── schemas/
│   └── {entity}.schema.ts         # Mongoose schema with userId
└── dto/
    ├── create-{entity}.dto.ts     # class-validator decorators
    └── update-{entity}.dto.ts     # PartialType of create

api/apps/api/test/
├── {entity}.e2e-spec.ts           # E2E tests with supertest
└── setup.ts                       # Test setup with MongoDB Memory Server
```

**Frontend (NextJS):**

```
frontend/apps/dashboard/
├── app/{entity}/
│   ├── page.tsx                   # List view (protected)
│   └── [id]/page.tsx              # Detail view (protected)
├── src/test/
│   └── setup.ts                   # Test setup with Clerk mocks
└── vitest.config.ts               # Frontend test config (jsdom)

frontend/packages/components/
├── {entity}-list.tsx
├── {entity}-list.spec.tsx         # Component tests
├── {entity}-form.tsx
├── {entity}-form.spec.tsx         # Component tests
└── {entity}-item.tsx

frontend/packages/hooks/
├── use-{entities}.ts              # React hook for state management
└── use-{entities}.spec.ts         # Hook tests

frontend/packages/services/
└── {entity}.service.ts            # API client with auth headers
```

### Phase 4: Quality Setup

**Vitest Configuration:**

- `vitest.config.ts` in each project
- 80% coverage threshold for lines, functions, branches
- `@vitest/coverage-v8` provider

**GitHub Actions:**

- `.github/workflows/ci.yml`
- Runs on push to main and PRs
- Steps: install → lint → test → build

**Husky Hooks:**

- Pre-commit: `lint-staged` (Biome check)
- Pre-push: `bun run typecheck`

**Biome:**

- `biome.json` in each project
- 100 character line width
- Double quotes, semicolons

### Phase 5: Verification

Run quality gate and report results:

```
✅ Generation complete!

Quality Report:
- bun install: ✓ succeeded
- bun run lint: ✓ 0 errors
- bun run test: ✓ 24 tests passed
- Coverage: 82% (threshold: 80%)

Ready to run:
  cd [project]
  bun dev
```

---

## Usage

```bash
# Create workspace with PRD-style prompt
python3 ~/.claude/skills/fullstack-workspace-init/scripts/init-workspace.py \
  --root ~/www/myproject \
  --name "My Project" \
  --brief "A task management app where users can create tasks with titles and due dates, organize them into projects, and mark them complete."

# Or interactive mode (prompts for brief)
python3 ~/.claude/skills/fullstack-workspace-init/scripts/init-workspace.py \
  --root ~/www/myproject \
  --name "My Project" \
  --interactive
```

---

## Generated Structure

```
myproject/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD
├── .husky/
│   ├── pre-commit              # Lint staged files
│   └── pre-push                # Type check
├── .agent/                     # AI documentation
├── package.json                # Workspace root
├── biome.json                  # Root linting config
│
├── api/                        # NestJS backend
│   ├── apps/api/src/
│   │   ├── main.ts
│   │   ├── app.module.ts
│   │   ├── auth/
│   │   │   ├── guards/clerk-auth.guard.ts
│   │   │   ├── guards/clerk-auth.guard.spec.ts  # Auth guard tests
│   │   │   └── decorators/current-user.decorator.ts
│   │   └── collections/
│   │       └── {entity}/
│   │           ├── {entity}.controller.ts
│   │           ├── {entity}.controller.spec.ts  # Controller tests
│   │           ├── {entity}.service.ts
│   │           └── {entity}.service.spec.ts     # Service tests
│   ├── apps/api/test/
│   │   ├── {entity}.e2e-spec.ts                 # E2E tests
│   │   └── setup.ts                             # E2E test setup
│   ├── vitest.config.ts
│   ├── package.json
│   └── .env.example
│
├── frontend/                   # NextJS apps
│   ├── apps/dashboard/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── sign-in/[[...sign-in]]/page.tsx
│   │   │   ├── sign-up/[[...sign-up]]/page.tsx
│   │   │   └── {entity}/       # Generated per entity
│   │   ├── src/test/
│   │   │   └── setup.ts        # Test setup with Clerk mocks
│   │   ├── middleware.ts       # Clerk route protection
│   │   └── providers/
│   │       └── clerk-provider.tsx
│   ├── packages/
│   │   ├── components/
│   │   │   ├── {entity}-list.tsx
│   │   │   ├── {entity}-list.spec.tsx   # Component tests
│   │   │   ├── {entity}-form.tsx
│   │   │   └── {entity}-form.spec.tsx   # Component tests
│   │   ├── hooks/
│   │   │   ├── use-{entities}.ts
│   │   │   └── use-{entities}.spec.ts   # Hook tests
│   │   ├── services/           # API clients
│   │   └── interfaces/
│   ├── vitest.config.ts        # Frontend test config (jsdom)
│   └── package.json
│
├── mobile/                     # React Native + Expo (optional)
│   └── ...
│
└── packages/                   # Shared packages
    └── packages/
        ├── common/
        │   ├── interfaces/
        │   └── enums/
        └── helpers/
```

---

## Key Patterns

### Backend Controller Pattern

```typescript
@ApiTags('tasks')
@ApiBearerAuth()
@UseGuards(ClerkAuthGuard)
@Controller('tasks')
export class TasksController {
  constructor(private readonly tasksService: TasksService) {}

  @Post()
  @ApiOperation({ summary: 'Create a new task' })
  create(
    @Body() createTaskDto: CreateTaskDto,
    @CurrentUser() user: { userId: string },
  ) {
    return this.tasksService.create(createTaskDto, user.userId);
  }
  // ... full CRUD
}
```

### Backend Service Pattern

```typescript
@Injectable()
export class TasksService {
  constructor(
    @InjectModel(Task.name) private taskModel: Model<TaskDocument>,
  ) {}

  async create(createTaskDto: CreateTaskDto, userId: string): Promise<Task> {
    const task = new this.taskModel({ ...createTaskDto, userId });
    return task.save();
  }
  // ... full CRUD with userId filtering
}
```

### Frontend Component Pattern

```typescript
'use client';

import { useEffect, useState } from 'react';
import { TaskService } from '@services/task.service';
import { Task } from '@interfaces/task.interface';

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();
    TaskService.getAll({ signal: controller.signal })
      .then(setTasks)
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, []);

  // ... render
}
```

---

## Additional Scripts

```bash
# Add a new entity to existing project
python3 ~/.claude/skills/fullstack-workspace-init/scripts/add-entity.py \
  --root ~/www/myproject \
  --name "comment" \
  --fields "content:string,taskId:string"

# Add a new frontend app
python3 ~/.claude/skills/fullstack-workspace-init/scripts/add-frontend-app.py \
  --root ~/www/myproject/frontend \
  --name admin
```

---

## Development Commands

After scaffolding:

```bash
cd myproject

# Install all dependencies
bun install

# Start all services (backend + frontend)
bun dev

# Or start individually
bun run dev:api      # Backend on :3001
bun run dev:frontend # Frontend on :3000
bun run dev:mobile   # Mobile via Expo

# Quality commands
bun run lint         # Check code style
bun run test         # Run tests
bun run test:coverage # Run with coverage
bun run typecheck    # Type checking
```

---

## Environment Variables

Create `.env` files based on `.env.example`:

**API (.env):**

```
PORT=3001
MONGODB_URI=mongodb://localhost:27017/myproject
CLERK_SECRET_KEY=sk_test_...
```

**Frontend (.env.local):**

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_API_URL=http://localhost:3001
```

---

## References

- `references/templates/` - Code generation templates
  - `service.spec.template.ts` - NestJS service unit test template
  - `controller.spec.template.ts` - NestJS controller unit test template
  - `e2e.spec.template.ts` - E2E test template with supertest + MongoDB Memory Server
  - `component.spec.template.tsx` - React component test template
  - `hook.spec.template.ts` - React hook test template
  - `test-setup.template.ts` - Frontend test setup with Clerk mocks
- `references/vitest.config.ts` - Backend Vitest configuration (80% coverage)
- `references/vitest.config.frontend.ts` - Frontend Vitest configuration (jsdom)
- `references/github-actions/ci.yml` - CI/CD workflow
- `references/architecture-guide.md` - Architectural decisions
- `references/coding-standards.md` - Coding rules
