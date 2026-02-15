---
name: nestjs-best-practices
description: "NestJS 11+ best practices for enterprise Node.js applications with TypeScript. Use when writing, reviewing, or refactoring NestJS controllers, services, modules, or APIs. Triggers on: NestJS modules, controllers, providers, dependency injection, @Injectable, @Controller, @Module, middleware, guards, interceptors, pipes, exception filters, ValidationPipe, class-validator, class-transformer, DTOs, JWT authentication, Passport strategies, @nestjs/passport, TypeORM entities, Prisma client, Drizzle ORM, repository pattern, circular dependencies, forwardRef, @nestjs/swagger, OpenAPI decorators, GraphQL resolvers, @nestjs/graphql, microservices, TCP transport, Redis transport, NATS, Kafka, NestJS 11 breaking changes, Express v5 migration, custom decorators, ConfigService, @nestjs/config, health checks, or NestJS testing patterns."
license: MIT
metadata:
  author: ejirocodes
  version: '1.0.0'
---

# NestJS 11 Best Practices

## Quick Reference

| Topic | When to Use | Reference |
|-------|-------------|-----------|
| **Core Architecture** | Modules, Providers, DI, forwardRef, custom decorators | [core-architecture.md](references/core-architecture.md) |
| **Request Lifecycle** | Middleware, Guards, Interceptors, Pipes, Filters | [request-lifecycle.md](references/request-lifecycle.md) |
| **Validation & Pipes** | DTOs, class-validator, ValidationPipe, transforms | [validation-pipes.md](references/validation-pipes.md) |
| **Authentication** | JWT, Passport, Guards, Local/OAuth strategies, RBAC | [authentication.md](references/authentication.md) |
| **Database** | TypeORM, Prisma, Drizzle ORM, repository patterns | [database-integration.md](references/database-integration.md) |
| **Testing** | Unit tests, E2E tests, mocking providers | [testing.md](references/testing.md) |
| **OpenAPI & GraphQL** | Swagger decorators, resolvers, subscriptions | [openapi-graphql.md](references/openapi-graphql.md) |
| **Microservices** | TCP, Redis, NATS, Kafka patterns | [microservices.md](references/microservices.md) |

## Essential Patterns

### Module with Providers

```typescript
@Module({
  imports: [DatabaseModule],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService], // Export for other modules
})
export class UsersModule {}
```

### Controller with Validation

```typescript
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }

  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.usersService.findOne(id);
  }
}
```

### DTO with Validation

```typescript
import { IsEmail, IsString, MinLength, IsOptional } from 'class-validator';

export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;

  @IsOptional()
  @IsString()
  name?: string;
}
```

### Exception Filter

```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();

    response.status(status).json({
      statusCode: status,
      message: exception.message,
      timestamp: new Date().toISOString(),
    });
  }
}
```

### Guard with JWT

```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  canActivate(context: ExecutionContext) {
    return super.canActivate(context);
  }
}
```

## NestJS 11 Breaking Changes

- **Express v5**: Wildcards must be named (e.g., `*splat`), optional params use braces `/:file{.:ext}`
- **Node.js 20+**: Minimum required version
- **Fastify v5**: Updated adapter for Fastify users
- **Dynamic Modules**: Same module with identical config imported multiple times = separate instances

## Common Mistakes

1. **Not using `forwardRef()` for circular deps** - Causes "cannot resolve dependency" errors; wrap in `forwardRef(() => ModuleName)`
2. **Throwing plain errors instead of HttpException** - Loses status codes, breaks exception filters; use `throw new BadRequestException('message')`
3. **Missing `@Injectable()` decorator** - Provider won't be injectable; always decorate services
4. **Global ValidationPipe without `whitelist: true`** - Allows unexpected properties; set `whitelist: true, forbidNonWhitelisted: true`
5. **Importing modules instead of exporting providers** - Use `exports` array to share providers across modules
6. **Async config without `ConfigModule.forRoot()`** - ConfigService undefined; import ConfigModule in AppModule
7. **Testing without `overrideProvider()`** - Uses real services in unit tests; mock dependencies with `overrideProvider(Service).useValue(mock)`
8. **E2E tests sharing database state** - No isolation between tests; use transactions or truncate tables in beforeEach
