---
name: bunjs-docker-mastery
description: |
  Senior/Lead Developer Bun.js + Docker dengan pengalaman 20 tahun. Skill ini digunakan ketika: (1) Membuat project Bun.js baru dengan Docker, (2) Code review dan refactoring untuk clean code, (3) Debugging complex issues, (4) Optimisasi performa dan scalability, (5) Arsitektur aplikasi production-ready, (6) Memilih library yang tepat dan terpercaya, (7) Setup CI/CD dan deployment. Trigger keywords: "bun", "bunjs", "bun.js", "docker", "typescript backend", "clean code", "scalable", "maintainable", "debugging", "performance".
---

# Bun.js + Docker Mastery

> "Simplicity is the ultimate sophistication." — Leonardo da Vinci

## Filosofi Inti (20 Tahun Wisdom)

### KISS - Keep It Stupid Simple
```typescript
// ❌ Over-engineering
class UserServiceFactoryAbstractSingletonProxyDecorator { ... }

// ✅ Simple & Clear
const userService = { create, update, delete, findById }
```

### Less is More
- 1 file = 1 tanggung jawab (max 200 lines)
- 1 function = 1 task (max 20 lines)
- Jika butuh komentar panjang, refactor kodenya
- Nama yang jelas > komentar yang panjang

### Red Flags (Warning Signs)
- File > 300 lines → split
- Function > 30 lines → extract
- Nested callback > 2 level → refactor
- Cyclomatic complexity > 10 → simplify
- `any` type → define proper types

## Quick Start

### Inisialisasi Project Baru
```bash
# Gunakan script init
./scripts/init-project.sh my-app

# Atau manual
bun init
bun add hono zod drizzle-orm pino
bun add -d @types/bun vitest
```

### Struktur Folder Production-Ready
```
src/
├── index.ts              # Entry point ONLY (max 20 lines)
├── app.ts                # App setup & middleware registration
├── config/
│   ├── index.ts          # Export semua config
│   ├── env.ts            # Environment validation dengan Zod
│   └── database.ts       # Database config
├── routes/
│   ├── index.ts          # Route aggregator
│   ├── user.route.ts     # User routes
│   └── auth.route.ts     # Auth routes
├── controllers/          # HTTP layer ONLY
├── services/             # Business logic
├── repositories/         # Data access layer
├── middlewares/
│   ├── auth.ts           # Authentication
│   ├── validate.ts       # Request validation
│   └── error.ts          # Error handler
├── utils/
│   ├── response.ts       # Standard response helper
│   ├── logger.ts         # Pino logger setup
│   └── errors.ts         # Custom error classes
└── types/
    ├── index.d.ts        # Global types
    └── api.types.ts      # API request/response types
```

## Core Patterns

### 1. Entry Point yang Bersih
```typescript
// src/index.ts - HANYA INI
import { app } from "./app"
import { env } from "./config/env"
import { logger } from "./utils/logger"

const server = Bun.serve({
  port: env.PORT,
  fetch: app.fetch,
})

logger.info(`🚀 Server running on ${server.url}`)
```

### 2. Environment Validation (WAJIB)
```typescript
// src/config/env.ts
import { z } from "zod"

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  REDIS_URL: z.string().url().optional(),
})

export const env = envSchema.parse(process.env)
export type Env = z.infer<typeof envSchema>
```

### 3. Layered Architecture
```
HTTP Request → Controller → Service → Repository → Database
                  ↓            ↓           ↓
              Validation   Business    Data Access
                          Logic        (Drizzle)
```

### 4. Error Handling yang Proper
```typescript
// src/utils/errors.ts
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code: string = "INTERNAL_ERROR"
  ) {
    super(message)
    Error.captureStackTrace(this, this.constructor)
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, "NOT_FOUND")
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400, "VALIDATION_ERROR")
  }
}
```

### 5. Response Standard
```typescript
// src/utils/response.ts
export const ok = <T>(data: T) => ({ success: true, data })
export const created = <T>(data: T) => ({ success: true, data })
export const error = (message: string, code: string) => ({
  success: false,
  error: { message, code }
})
```

## Docker Best Practices

### Multi-stage Build (Production)
```dockerfile
# Build stage
FROM oven/bun:1-alpine AS builder
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile --production=false
COPY . .
RUN bun run build

# Production stage
FROM oven/bun:1-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Security: Non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S bunjs -u 1001
USER bunjs

COPY --from=builder --chown=bunjs:nodejs /app/dist ./dist
COPY --from=builder --chown=bunjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=bunjs:nodejs /app/package.json ./

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["bun", "run", "dist/index.js"]
```

### Docker Compose (Development)
Lihat `assets/project-template/docker/docker-compose.yml`

## Debugging Mastery

### Common Crash Points & Solutions
| Issue | Penyebab | Solusi |
|-------|----------|--------|
| Memory leak | Uncleared intervals/listeners | Cleanup di graceful shutdown |
| Connection pool exhausted | Tidak release connection | Gunakan `using` atau finally |
| Race condition | Async tanpa proper await | Promise.all dengan error handling |
| Uncaught Promise rejection | Missing try-catch | Global error handler |

### Debugging Tools
```typescript
// Bun native debugger
bun --inspect src/index.ts

// Memory profiling
bun --smol src/index.ts  // Low memory mode

// Trace async operations
process.on("unhandledRejection", (reason, promise) => {
  logger.error({ reason, promise }, "Unhandled Rejection")
})
```

## References (Detailed Guides)

- **Clean Code Patterns**: See [references/clean-code-patterns.md](references/clean-code-patterns.md)
- **Debugging Deep Dive**: See [references/debugging-guide.md](references/debugging-guide.md)  
- **Library Arsenal (20+ recommended)**: See [references/library-arsenal.md](references/library-arsenal.md)
- **Docker Advanced Patterns**: See [references/docker-patterns.md](references/docker-patterns.md)
- **Testing Strategy**: See [references/testing-strategy.md](references/testing-strategy.md)

## Scripts

- `scripts/init-project.sh` - Initialize new project dengan template
- `scripts/healthcheck.ts` - Healthcheck endpoint template

## Assets

- `assets/project-template/` - Full project boilerplate siap pakai

## Checklist Sebelum Production

- [ ] Environment variables validated dengan Zod
- [ ] Graceful shutdown implemented
- [ ] Health check endpoint `/health`
- [ ] Structured logging dengan Pino
- [ ] Error handling global
- [ ] Rate limiting
- [ ] CORS configured
- [ ] Security headers (helmet)
- [ ] Database connection pooling
- [ ] Docker multi-stage build
- [ ] CI/CD pipeline
- [ ] Monitoring & alerting ready
