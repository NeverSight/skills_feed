---
name: environment-setup
description: Configure and manage development, staging, and production environments. Use when setting up environment variables, managing configurations, or separating environments. Handles .env files, config management, and environment-specific settings.
allowed-tools: [Read, Write, Edit, Bash]
tags: [environment, configuration, env-variables, dotenv, config-management]
platforms: [Claude, ChatGPT, Gemini]
---

# Environment Configuration


## When to use this skill

- **신규 프로젝트**: 초기 환경 설정
- **다중 환경**: dev, staging, production 분리
- **팀 협업**: 일관된 환경 공유

## Instructions

### Step 1: .env 파일 구조

**.env.example** (템플릿):
```bash
# Application
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10

# Redis
REDIS_URL=redis://localhost:6379
REDIS_TTL=3600

# Authentication
JWT_ACCESS_SECRET=change-me-in-production-min-32-characters
JWT_REFRESH_SECRET=change-me-in-production-min-32-characters
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# External APIs
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
AWS_ACCESS_KEY_ID=AKIAXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxx
AWS_REGION=us-east-1
AWS_S3_BUCKET=myapp-uploads

# Monitoring
SENTRY_DSN=https://xxx@sentry.io/xxx
LOG_LEVEL=info

# Feature Flags
ENABLE_2FA=false
ENABLE_ANALYTICS=true
```

**.env.local** (개발자별):
```bash
# 개발자 개인 설정 (.gitignore에 추가)
DATABASE_URL=postgresql://localhost:5432/myapp_dev
LOG_LEVEL=debug
```

**.env.production**:
```bash
NODE_ENV=production
PORT=8080
APP_URL=https://myapp.com

DATABASE_URL=${DATABASE_URL}  # 환경변수에서 주입
REDIS_URL=${REDIS_URL}

JWT_ACCESS_SECRET=${JWT_ACCESS_SECRET}
JWT_REFRESH_SECRET=${JWT_REFRESH_SECRET}

LOG_LEVEL=warn
ENABLE_2FA=true
```

### Step 2: Type-Safe 환경변수 (TypeScript)

**config/env.ts**:
```typescript
import { z } from 'zod';
import dotenv from 'dotenv';

// Load .env file
dotenv.config();

// Define schema
const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.coerce.number().default(3000),

  DATABASE_URL: z.string().url(),

  JWT_ACCESS_SECRET: z.string().min(32),
  JWT_REFRESH_SECRET: z.string().min(32),

  SMTP_HOST: z.string(),
  SMTP_PORT: z.coerce.number(),
  SMTP_USER: z.string().email(),
  SMTP_PASSWORD: z.string(),

  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),

  LOG_LEVEL: z.enum(['error', 'warn', 'info', 'debug']).default('info'),
});

// Validate and export
export const env = envSchema.parse(process.env);

// Usage:
// import { env } from './config/env';
// console.log(env.DATABASE_URL); // Type-safe!
```

**에러 처리**:
```typescript
try {
  const env = envSchema.parse(process.env);
} catch (error) {
  if (error instanceof z.ZodError) {
    console.error('❌ Invalid environment variables:');
    error.errors.forEach((err) => {
      console.error(`  - ${err.path.join('.')}: ${err.message}`);
    });
    process.exit(1);
  }
}
```

### Step 3: 환경별 Config 파일

**config/index.ts**:
```typescript
interface Config {
  env: string;
  port: number;
  database: {
    url: string;
    pool: { min: number; max: number };
  };
  jwt: {
    accessSecret: string;
    refreshSecret: string;
    accessExpiry: string;
    refreshExpiry: string;
  };
  features: {
    enable2FA: boolean;
    enableAnalytics: boolean;
  };
}

const config: Config = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000'),

  database: {
    url: process.env.DATABASE_URL!,
    pool: {
      min: parseInt(process.env.DATABASE_POOL_MIN || '2'),
      max: parseInt(process.env.DATABASE_POOL_MAX || '10'),
    },
  },

  jwt: {
    accessSecret: process.env.JWT_ACCESS_SECRET!,
    refreshSecret: process.env.JWT_REFRESH_SECRET!,
    accessExpiry: process.env.JWT_ACCESS_EXPIRY || '15m',
    refreshExpiry: process.env.JWT_REFRESH_EXPIRY || '7d',
  },

  features: {
    enable2FA: process.env.ENABLE_2FA === 'true',
    enableAnalytics: process.env.ENABLE_ANALYTICS !== 'false',
  },
};

// Validate required fields
const requiredEnvVars = [
  'DATABASE_URL',
  'JWT_ACCESS_SECRET',
  'JWT_REFRESH_SECRET',
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}

export default config;
```

### Step 4: 환경별 설정 파일

**config/environments/development.ts**:
```typescript
export default {
  logging: {
    level: 'debug',
    prettyPrint: true,
  },
  cors: {
    origin: '*',
    credentials: true,
  },
  rateLimit: {
    enabled: false,
  },
};
```

**config/environments/production.ts**:
```typescript
export default {
  logging: {
    level: 'warn',
    prettyPrint: false,
  },
  cors: {
    origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
    credentials: true,
  },
  rateLimit: {
    enabled: true,
    windowMs: 15 * 60 * 1000,
    max: 100,
  },
};
```

**config/index.ts** (통합):
```typescript
import development from './environments/development';
import production from './environments/production';

const env = process.env.NODE_ENV || 'development';

const configs = {
  development,
  production,
  test: development,
};

export const environmentConfig = configs[env];
```

### Step 5: Docker 환경변수

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env.local
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp

  redis:
    image: redis:7-alpine
```

## Output format

```
project/
├── .env.example           # 템플릿 (커밋)
├── .env                   # 로컬 (gitignore)
├── .env.local             # 개발자별 (gitignore)
├── .env.production        # 프로덕션 (gitignore or vault)
├── config/
│   ├── index.ts           # 메인 설정
│   ├── env.ts             # 환경변수 검증
│   └── environments/
│       ├── development.ts
│       ├── production.ts
│       └── test.ts
└── .gitignore
```

**.gitignore**:
```
.env
.env.local
.env.*.local
.env.production
```

## Constraints

### 필수 규칙 (MUST)

1. **.env.example 제공**: 필요한 환경변수 목록
2. **검증**: 필수 환경변수 누락 시 에러
3. **.gitignore**: .env 파일 절대 커밋하지 않음

### 금지 사항 (MUST NOT)

1. **Secrets 커밋**: .env 파일 절대 커밋하지 않음
2. **하드코딩**: 코드에 환경별 설정 하드코딩 금지

## Best practices

1. **12 Factor App**: 환경변수로 설정 관리
2. **Type Safety**: Zod로 런타임 검증
3. **Secrets Management**: AWS Secrets Manager, Vault 사용

## References

- [dotenv](https://github.com/motdotla/dotenv)
- [Zod](https://zod.dev/)
- [12 Factor App - Config](https://12factor.net/config)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 태그
`#environment` `#configuration` `#env-variables` `#dotenv` `#config-management` `#utilities`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
