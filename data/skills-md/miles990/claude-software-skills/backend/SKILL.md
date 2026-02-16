---
name: backend
description: Backend development with Node.js, Express, NestJS, and server patterns
domain: development-stacks
version: 1.0.0
tags: [nodejs, express, nestjs, fastify, api, middleware, authentication]
triggers:
  keywords:
    primary: [backend, server, nodejs, express, nestjs, api, microservice]
    secondary: [fastify, middleware, authentication, rest, graphql, queue]
  context_boost: [service, endpoint, database, http]
  context_penalty: [frontend, css, ui, mobile]
  priority: high
collaboration:
  prerequisites:
    - skill: typescript
      reason: Type-safe backend development
  delegation_triggers:
    - trigger: API endpoint design decisions
      delegate_to: api-design
      context: RESTful conventions, versioning, error formats
    - trigger: Database schema design or query optimization
      delegate_to: database
      context: Data modeling, indexing strategy
    - trigger: Writing tests for services or controllers
      delegate_to: testing-strategies
      context: Integration test patterns, mocking strategies
  receives_context_from:
    - skill: api-design
      receives:
        - Endpoint naming conventions
        - Request/response formats
        - Error response structure
    - skill: database
      receives:
        - Connection pool settings
        - Query optimization hints
        - Transaction patterns
  provides_context_to:
    - skill: frontend
      provides:
        - API endpoints list
        - Authentication flow
        - WebSocket events
    - skill: testing-strategies
      provides:
        - Service dependencies to mock
        - Integration test scenarios
---

# Backend Development

## Overview

Server-side development patterns, frameworks, and best practices for building scalable APIs and services.

---

## Express.js

### Application Structure

```typescript
// app.ts
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import { errorHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/requestLogger';
import routes from './routes';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  credentials: true,
}));

// Request processing
app.use(compression());
app.use(express.json({ limit: '10kb' }));
app.use(express.urlencoded({ extended: true }));

// Logging
app.use(requestLogger);

// Routes
app.use('/api/v1', routes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Error handling (must be last)
app.use(errorHandler);

export default app;
```

### Middleware Patterns

```typescript
// Authentication middleware
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

interface AuthRequest extends Request {
  user?: { id: string; role: string };
}

export function authenticate(req: AuthRequest, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as { id: string; role: string };
    req.user = decoded;
    next();
  } catch {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// Authorization middleware
export function authorize(...roles: string[]) {
  return (req: AuthRequest, res: Response, next: NextFunction) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

// Rate limiting
import rateLimit from 'express-rate-limit';

export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  message: { error: 'Too many requests' },
  standardHeaders: true,
});

// Validation middleware
import { z } from 'zod';

export function validate(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse({
      body: req.body,
      query: req.query,
      params: req.params,
    });

    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.error.flatten(),
      });
    }

    req.body = result.data.body;
    req.query = result.data.query;
    req.params = result.data.params;
    next();
  };
}
```

### Error Handling

```typescript
// Custom error classes
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true
  ) {
    super(message);
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, `${resource} not found`);
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(400, message);
  }
}

// Global error handler
export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  console.error('Error:', err);

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
    });
  }

  // Mongoose/Prisma errors
  if (err.name === 'CastError') {
    return res.status(400).json({ error: 'Invalid ID format' });
  }

  if (err.name === 'ValidationError') {
    return res.status(400).json({ error: err.message });
  }

  // Default error
  res.status(500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : err.message,
  });
}
```

---

## NestJS

### Module Structure

```typescript
// users/users.module.ts
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
  imports: [PrismaModule],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}

// users/users.controller.ts
import {
  Controller, Get, Post, Put, Delete,
  Body, Param, Query, UseGuards,
  HttpCode, HttpStatus,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { UsersService } from './users.service';
import { CreateUserDto, UpdateUserDto, QueryUsersDto } from './dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';

@ApiTags('users')
@Controller('users')
@UseGuards(JwtAuthGuard, RolesGuard)
@ApiBearerAuth()
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  @ApiOperation({ summary: 'List users' })
  async findAll(@Query() query: QueryUsersDto) {
    return this.usersService.findAll(query);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get user by ID' })
  async findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);
  }

  @Post()
  @Roles('admin')
  @ApiOperation({ summary: 'Create user' })
  async create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }

  @Put(':id')
  @ApiOperation({ summary: 'Update user' })
  async update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
    return this.usersService.update(id, updateUserDto);
  }

  @Delete(':id')
  @Roles('admin')
  @HttpCode(HttpStatus.NO_CONTENT)
  @ApiOperation({ summary: 'Delete user' })
  async remove(@Param('id') id: string) {
    await this.usersService.remove(id);
  }
}
```

### DTOs with Validation

```typescript
// users/dto/create-user.dto.ts
import { IsEmail, IsString, MinLength, IsOptional, IsEnum } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export enum UserRole {
  USER = 'user',
  ADMIN = 'admin',
}

export class CreateUserDto {
  @ApiProperty({ example: 'user@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ minLength: 8 })
  @IsString()
  @MinLength(8)
  password: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  name?: string;

  @ApiPropertyOptional({ enum: UserRole, default: UserRole.USER })
  @IsOptional()
  @IsEnum(UserRole)
  role?: UserRole = UserRole.USER;
}

// Partial DTO for updates
import { PartialType, OmitType } from '@nestjs/swagger';

export class UpdateUserDto extends PartialType(
  OmitType(CreateUserDto, ['password'] as const)
) {}
```

### Services with Dependency Injection

```typescript
// users/users.service.ts
import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateUserDto, UpdateUserDto, QueryUsersDto } from './dto';
import * as argon2 from 'argon2';

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  async findAll(query: QueryUsersDto) {
    const { page = 1, limit = 10, search } = query;

    const where = search
      ? {
          OR: [
            { name: { contains: search, mode: 'insensitive' } },
            { email: { contains: search, mode: 'insensitive' } },
          ],
        }
      : {};

    const [users, total] = await Promise.all([
      this.prisma.user.findMany({
        where,
        skip: (page - 1) * limit,
        take: limit,
        select: {
          id: true,
          email: true,
          name: true,
          role: true,
          createdAt: true,
        },
      }),
      this.prisma.user.count({ where }),
    ]);

    return {
      data: users,
      meta: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    };
  }

  async findOne(id: string) {
    const user = await this.prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        name: true,
        role: true,
        createdAt: true,
      },
    });

    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }

    return user;
  }

  async create(dto: CreateUserDto) {
    const hashedPassword = await argon2.hash(dto.password);

    return this.prisma.user.create({
      data: {
        ...dto,
        password: hashedPassword,
      },
      select: {
        id: true,
        email: true,
        name: true,
        role: true,
      },
    });
  }

  async update(id: string, dto: UpdateUserDto) {
    await this.findOne(id); // Throws if not found

    return this.prisma.user.update({
      where: { id },
      data: dto,
      select: {
        id: true,
        email: true,
        name: true,
        role: true,
      },
    });
  }

  async remove(id: string) {
    await this.findOne(id); // Throws if not found
    await this.prisma.user.delete({ where: { id } });
  }
}
```

---

## Database Integration

### Prisma ORM

```typescript
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  password  String
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

enum Role {
  USER
  ADMIN
}

// Prisma service
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}
```

### Transactions

```typescript
// Complex transaction
async transferFunds(fromId: string, toId: string, amount: number) {
  return this.prisma.$transaction(async (tx) => {
    const from = await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } },
    });

    if (from.balance < 0) {
      throw new Error('Insufficient funds');
    }

    const to = await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } },
    });

    await tx.transfer.create({
      data: {
        fromId,
        toId,
        amount,
      },
    });

    return { from, to };
  });
}
```

---

## Background Jobs

### Bull Queue

```typescript
// jobs/email.processor.ts
import { Process, Processor } from '@nestjs/bull';
import { Job } from 'bull';
import { MailService } from '../mail/mail.service';

@Processor('email')
export class EmailProcessor {
  constructor(private mailService: MailService) {}

  @Process('welcome')
  async handleWelcomeEmail(job: Job<{ email: string; name: string }>) {
    const { email, name } = job.data;
    await this.mailService.sendWelcome(email, name);
  }

  @Process('password-reset')
  async handlePasswordReset(job: Job<{ email: string; token: string }>) {
    const { email, token } = job.data;
    await this.mailService.sendPasswordReset(email, token);
  }
}

// Using the queue
import { InjectQueue } from '@nestjs/bull';
import { Queue } from 'bull';

@Injectable()
export class UsersService {
  constructor(@InjectQueue('email') private emailQueue: Queue) {}

  async createUser(dto: CreateUserDto) {
    const user = await this.prisma.user.create({ data: dto });

    await this.emailQueue.add('welcome', {
      email: user.email,
      name: user.name,
    });

    return user;
  }
}
```

---

## WebSockets

```typescript
// events/events.gateway.ts
import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  OnGatewayConnection,
  OnGatewayDisconnect,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({
  cors: { origin: '*' },
  namespace: '/events',
})
export class EventsGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer()
  server: Server;

  handleConnection(client: Socket) {
    console.log(`Client connected: ${client.id}`);
  }

  handleDisconnect(client: Socket) {
    console.log(`Client disconnected: ${client.id}`);
  }

  @SubscribeMessage('join-room')
  handleJoinRoom(client: Socket, room: string) {
    client.join(room);
    this.server.to(room).emit('user-joined', { userId: client.id });
  }

  @SubscribeMessage('message')
  handleMessage(client: Socket, payload: { room: string; message: string }) {
    this.server.to(payload.room).emit('message', {
      userId: client.id,
      message: payload.message,
      timestamp: new Date(),
    });
  }

  // Broadcast from service
  broadcastToRoom(room: string, event: string, data: any) {
    this.server.to(room).emit(event, data);
  }
}
```

---

## Related Skills

- [[api-design]] - API design patterns
- [[database]] - Database patterns
- [[security-practices]] - Backend security

---

## Sharp Edges（常見陷阱）

> 這些是後端開發中最常見且代價最高的錯誤

### SE-1: 未處理的 Promise Rejection
- **嚴重度**: critical
- **情境**: Async 函數中的錯誤沒有被 catch，導致應用程式崩潰或無聲失敗
- **原因**: 忘記 await、沒有錯誤處理、或在 callback 中使用 async
- **症狀**:
  - UnhandledPromiseRejectionWarning
  - API 請求 hang 住不回應
  - 資料庫操作部分完成
- **檢測**: `\.then\([^)]*\)(?!\s*\.catch)|async.*(?<!await\s)db\.|async.*(?<!await\s)fetch`
- **解法**: 使用 try-catch 包裝、加上 global error handler、使用 ESLint no-floating-promises 規則

### SE-2: N+1 查詢問題
- **嚴重度**: high
- **情境**: 在迴圈中執行資料庫查詢，導致效能急劇下降
- **原因**: ORM 的 lazy loading、沒有使用 batch fetch
- **症狀**:
  - 查詢數量與資料量成正比
  - API 響應時間隨資料量線性增長
  - 資料庫連接池耗盡
- **檢測**: `for.*await.*findOne|forEach.*await.*find|\.map\(.*await.*query`
- **解法**: 使用 eager loading (include/populate)、DataLoader、批次查詢

### SE-3: 敏感資訊洩露
- **嚴重度**: critical
- **情境**: 錯誤訊息、日誌、或 API 回應中包含敏感資訊
- **原因**: 開發環境的 debug 設定被帶到生產、錯誤處理過於詳細
- **症狀**:
  - 錯誤回應包含 stack trace
  - 日誌中有密碼或 token
  - API 回應包含內部資料庫結構
- **檢測**: `console\.log.*password|console\.log.*token|res\.json\(err\)|stack.*trace`
- **解法**: 生產環境只回傳通用錯誤訊息、使用專門的錯誤序列化、過濾敏感欄位

### SE-4: 競態條件 (Race Condition)
- **嚴重度**: high
- **情境**: 多個請求同時修改同一資源，導致資料不一致
- **原因**: 缺乏適當的鎖定機制、read-modify-write 沒有原子性
- **症狀**:
  - 庫存數量變成負數
  - 重複扣款
  - 資料覆蓋（後來的寫入覆蓋先前的）
- **檢測**: `findOne.*update|get.*set|read.*write`
- **解法**: 使用資料庫事務、樂觀鎖 (version field)、分散式鎖

### SE-5: 未驗證的用戶輸入
- **嚴重度**: critical
- **情境**: 直接使用用戶輸入進行資料庫查詢或系統命令
- **原因**: 信任前端驗證、沒有後端驗證、拼接 SQL/命令字串
- **症狀**:
  - SQL Injection 攻擊
  - NoSQL Injection
  - Command Injection
- **檢測**: `\$\{.*req\.body|query\(.*\+.*req\.|exec\(.*req\.|eval\(`
- **解法**: 使用參數化查詢、輸入驗證（Zod/Joi）、白名單驗證

---

## Validations

### V-1: 禁止空的 catch block
- **類型**: regex
- **嚴重度**: critical
- **模式**: `catch\s*\([^)]*\)\s*\{\s*\}`
- **訊息**: Empty catch block silently swallows errors
- **修復建議**: Add error logging: `console.error(err)` or `logger.error(err)`
- **適用**: `*.ts`, `*.js`

### V-2: 禁止 forEach + async
- **類型**: regex
- **嚴重度**: high
- **模式**: `\.forEach\s*\(\s*async`
- **訊息**: forEach does not await async callbacks - use for...of or Promise.all
- **修復建議**: Replace with `for (const item of items)` or `await Promise.all(items.map(...))`
- **適用**: `*.ts`, `*.js`

### V-3: 檢測未處理的 Promise
- **類型**: regex
- **嚴重度**: high
- **模式**: `(?<!await\s)(?<!return\s)(?<!\.\s*catch\()fetch\(|db\.(find|query|insert|update|delete)`
- **訊息**: Async operation may not be awaited or caught
- **修復建議**: Add `await` keyword or `.catch()` handler
- **適用**: `*.ts`, `*.js`

### V-4: 禁止硬編碼密鑰
- **類型**: regex
- **嚴重度**: critical
- **模式**: `(password|secret|api_key|apikey|token)\s*[=:]\s*["'][^"']+["']`
- **訊息**: Hardcoded secret detected - use environment variables
- **修復建議**: Move to environment variables: `process.env.SECRET_KEY`
- **適用**: `*.ts`, `*.js`, `*.json`

### V-5: 禁止 SELECT *
- **類型**: regex
- **嚴重度**: medium
- **模式**: `SELECT\s+\*\s+FROM|\.findMany\s*\(\s*\)|\.find\s*\(\s*\{\s*\}\s*\)`
- **訊息**: SELECT * fetches unnecessary data - specify fields
- **修復建議**: Explicitly list needed fields: `SELECT id, name FROM...`
- **適用**: `*.ts`, `*.js`, `*.sql`

