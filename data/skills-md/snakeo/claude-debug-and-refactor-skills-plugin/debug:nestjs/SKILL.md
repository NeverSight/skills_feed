---
name: debug:nestjs
description: Debug NestJS issues systematically. Use when encountering dependency injection errors like "Nest can't resolve dependencies", module import issues, circular dependencies between services or modules, guard and interceptor problems, decorator configuration issues, microservice communication errors, WebSocket gateway failures, pipe validation errors, or any NestJS-specific runtime issues requiring diagnosis.
---

# NestJS Debugging Guide

This guide provides a systematic approach to debugging NestJS applications. Use the four-phase methodology below to efficiently identify and resolve issues.

## Common Error Patterns

### 1. Dependency Resolution Errors

**Error Message:**
```
Nest can't resolve dependencies of the <ProviderName> (?). Please make sure that the argument <DependencyName> at index [0] is available in the <ModuleName> context.
```

**Common Causes:**
- Provider not added to module's `providers` array
- Missing `@Injectable()` decorator on service class
- Incorrect import/export between modules
- Typo in injection token name
- Missing `forRoot()`/`forRootAsync()` configuration

**Solutions:**
```typescript
// Ensure provider is in the module
@Module({
  providers: [MyService], // Add missing provider here
  exports: [MyService],   // Export if used by other modules
})
export class MyModule {}

// Ensure @Injectable() decorator exists
@Injectable()
export class MyService {
  constructor(private readonly dependency: OtherService) {}
}

// For external modules, import the module not just the service
@Module({
  imports: [OtherModule], // Import the module
})
export class MyModule {}
```

### 2. Circular Dependency Errors

**Error Message:**
```
Nest cannot create the module instance. The module at index [X] of the imports array is undefined.
```

**Common Causes:**
- Two modules importing each other
- Two services depending on each other
- File-level circular imports (constants, types)

**Solutions:**
```typescript
// Use forwardRef() for circular module dependencies
@Module({
  imports: [forwardRef(() => OtherModule)],
})
export class MyModule {}

// Use forwardRef() for circular service dependencies
@Injectable()
export class ServiceA {
  constructor(
    @Inject(forwardRef(() => ServiceB))
    private serviceB: ServiceB,
  ) {}
}

// Alternative: Extract shared logic to a third module
@Module({
  providers: [SharedService],
  exports: [SharedService],
})
export class SharedModule {}
```

### 3. Guard/Interceptor Issues

**Error Message:**
```
Cannot read property 'canActivate' of undefined
Cannot read property 'intercept' of undefined
```

**Common Causes:**
- Guard/Interceptor not properly registered
- Missing `@UseGuards()` or `@UseInterceptors()` decorator
- Incorrect scope (request-scoped vs singleton)
- Dependencies not available in guard/interceptor context

**Solutions:**
```typescript
// Register globally in main.ts
app.useGlobalGuards(new AuthGuard());
app.useGlobalInterceptors(new LoggingInterceptor());

// Or register via module for DI support
@Module({
  providers: [
    {
      provide: APP_GUARD,
      useClass: AuthGuard,
    },
    {
      provide: APP_INTERCEPTOR,
      useClass: LoggingInterceptor,
    },
  ],
})
export class AppModule {}

// Controller-level registration
@UseGuards(AuthGuard)
@UseInterceptors(LoggingInterceptor)
@Controller('users')
export class UsersController {}
```

### 4. Pipe Validation Errors

**Error Message:**
```
An instance of an invalid class-validator value was provided
Validation failed (expected type)
```

**Common Causes:**
- Missing `class-transformer` or `class-validator` packages
- DTO not properly decorated with validation decorators
- ValidationPipe not configured correctly
- Transform option not enabled

**Solutions:**
```typescript
// Enable ValidationPipe globally with proper options
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,           // Strip non-whitelisted properties
    forbidNonWhitelisted: true, // Throw on extra properties
    transform: true,           // Auto-transform payloads to DTO instances
    transformOptions: {
      enableImplicitConversion: true,
    },
  }),
);

// Properly decorate DTOs
import { IsString, IsInt, Min, IsOptional } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateUserDto {
  @IsString()
  name: string;

  @IsInt()
  @Min(0)
  @Type(() => Number)
  age: number;

  @IsOptional()
  @IsString()
  email?: string;
}
```

### 5. Microservice Communication Errors

**Error Message:**
```
There is no matching message handler defined in the remote service
Connection refused / ECONNREFUSED
```

**Common Causes:**
- Message pattern mismatch between client and server
- Transport configuration mismatch
- Service not connected or not running
- Serialization/deserialization issues

**Solutions:**
```typescript
// Ensure matching patterns
// Server side
@MessagePattern({ cmd: 'get_user' })
async getUser(data: { id: number }) {
  return this.usersService.findOne(data.id);
}

// Client side - pattern must match exactly
const user = await this.client.send({ cmd: 'get_user' }, { id: 1 }).toPromise();

// Check transport configuration matches
// Server
const app = await NestFactory.createMicroservice<MicroserviceOptions>(
  AppModule,
  {
    transport: Transport.TCP,
    options: { host: '0.0.0.0', port: 3001 },
  },
);

// Client module
ClientsModule.register([
  {
    name: 'USER_SERVICE',
    transport: Transport.TCP,
    options: { host: 'localhost', port: 3001 },
  },
]);
```

### 6. WebSocket/Gateway Errors

**Error Message:**
```
Gateway is not defined
WebSocket connection failed
```

**Common Causes:**
- Missing `@WebSocketGateway()` decorator
- Gateway not added to module providers
- CORS issues with WebSocket connections
- Adapter not properly configured

**Solutions:**
```typescript
// Properly configure gateway
@WebSocketGateway({
  cors: {
    origin: '*',
  },
  namespace: '/events',
})
export class EventsGateway implements OnGatewayConnection {
  @WebSocketServer()
  server: Server;

  handleConnection(client: Socket) {
    console.log('Client connected:', client.id);
  }

  @SubscribeMessage('message')
  handleMessage(client: Socket, payload: any): string {
    return 'Hello world!';
  }
}

// Add to module
@Module({
  providers: [EventsGateway],
})
export class EventsModule {}

// Configure adapter in main.ts if needed
import { IoAdapter } from '@nestjs/platform-socket.io';
app.useWebSocketAdapter(new IoAdapter(app));
```

## Debugging Tools

### 1. NestJS Debug Mode

```bash
# Start with debug flag
nest start --debug --watch

# Or add to package.json
"start:debug": "nest start --debug --watch"
```

### 2. VS Code Debugger Configuration

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug NestJS",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "start:debug"],
      "console": "integratedTerminal",
      "restart": true,
      "autoAttachChildProcesses": true,
      "sourceMaps": true,
      "envFile": "${workspaceFolder}/.env"
    },
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to NestJS",
      "port": 9229,
      "restart": true,
      "sourceMaps": true
    }
  ]
}
```

### 3. Docker Debug Configuration

```yaml
# docker-compose.debug.yml
version: '3.8'
services:
  api:
    command: npm run start:debug
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port
    environment:
      - NODE_OPTIONS=--inspect=0.0.0.0:9229
```

### 4. Built-in Logger Service

```typescript
import { Logger, Injectable } from '@nestjs/common';

@Injectable()
export class MyService {
  private readonly logger = new Logger(MyService.name);

  async doSomething() {
    this.logger.log('Processing started');
    this.logger.debug('Debug info', { data: someData });
    this.logger.warn('Warning message');
    this.logger.error('Error occurred', error.stack);
    this.logger.verbose('Verbose details');
  }
}

// Configure logger level in main.ts
const app = await NestFactory.create(AppModule, {
  logger: ['error', 'warn', 'log', 'debug', 'verbose'],
});
```

### 5. @nestjs/testing Utilities

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';

describe('UsersController (e2e)', () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    })
    .overrideProvider(UsersService)
    .useValue(mockUsersService)
    .compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/users (GET)', () => {
    return request(app.getHttpServer())
      .get('/users')
      .expect(200)
      .expect({ data: [] });
  });
});
```

## The Four Phases (NestJS-specific)

### Phase 1: Gather Context

Before debugging, collect all relevant information:

```bash
# Check NestJS and dependency versions
npm list @nestjs/core @nestjs/common @nestjs/platform-express

# Check for peer dependency issues
npm ls 2>&1 | grep -i "peer dep"

# Review recent changes
git diff HEAD~5 --name-only | grep -E '\.(ts|json)$'

# Check environment configuration
cat .env | grep -v -E '^#|^$'
```

**Key Questions:**
- When did the error start occurring?
- What changes were made recently?
- Is this reproducible in all environments?
- Are there any relevant logs or stack traces?

### Phase 2: Isolate the Problem

Narrow down the issue systematically:

```typescript
// 1. Check module structure
import { Logger } from '@nestjs/common';

@Module({
  imports: [
    // Comment out imports one by one to isolate
    ConfigModule.forRoot(),
    // DatabaseModule,  // Try disabling
    // UsersModule,     // Try disabling
  ],
})
export class AppModule {
  constructor() {
    Logger.log('AppModule initialized');
  }
}

// 2. Add lifecycle logging
@Injectable()
export class MyService implements OnModuleInit, OnModuleDestroy {
  private readonly logger = new Logger(MyService.name);

  onModuleInit() {
    this.logger.log('MyService initialized');
  }

  onModuleDestroy() {
    this.logger.log('MyService destroyed');
  }
}

// 3. Test dependency injection manually
@Controller()
export class TestController {
  constructor(
    @Optional() private myService?: MyService,
  ) {
    console.log('MyService injected:', !!this.myService);
  }
}
```

### Phase 3: Debug and Fix

Apply targeted debugging techniques:

```typescript
// 1. For DI issues - check the module graph
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    logger: ['verbose'],  // Enable all logging
  });

  // Log all registered routes
  const server = app.getHttpServer();
  const router = server._events.request._router;
  console.log('Registered routes:', router.stack
    .filter(r => r.route)
    .map(r => `${Object.keys(r.route.methods)} ${r.route.path}`));

  await app.listen(3000);
}

// 2. For async configuration issues
@Module({
  imports: [
    ConfigModule.forRootAsync({
      useFactory: async () => {
        console.log('ConfigModule factory called');
        const config = await loadConfig();
        console.log('Config loaded:', config);
        return config;
      },
    }),
  ],
})
export class AppModule {}

// 3. For guard/interceptor debugging
@Injectable()
export class DebugGuard implements CanActivate {
  private readonly logger = new Logger(DebugGuard.name);

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    this.logger.debug(`Guard checking: ${request.method} ${request.url}`);
    this.logger.debug(`Headers: ${JSON.stringify(request.headers)}`);
    this.logger.debug(`User: ${JSON.stringify(request.user)}`);
    return true;  // Allow through for debugging
  }
}
```

### Phase 4: Verify and Document

Ensure the fix is complete and documented:

```typescript
// 1. Write a test for the fixed issue
describe('UserService', () => {
  it('should resolve dependencies correctly', async () => {
    const module = await Test.createTestingModule({
      imports: [UsersModule],
    }).compile();

    const service = module.get<UsersService>(UsersService);
    expect(service).toBeDefined();
    expect(service.userRepository).toBeDefined();
  });
});

// 2. Add error handling to prevent recurrence
@Injectable()
export class RobustService {
  private readonly logger = new Logger(RobustService.name);

  async riskyOperation() {
    try {
      return await this.externalCall();
    } catch (error) {
      this.logger.error(`Operation failed: ${error.message}`, error.stack);
      throw new InternalServerErrorException('Operation failed');
    }
  }
}

// 3. Document in comments
/**
 * UserService handles user-related operations.
 *
 * IMPORTANT: This service depends on DatabaseModule being imported
 * before UsersModule in AppModule to avoid circular dependency issues.
 *
 * @see https://docs.nestjs.com/fundamentals/circular-dependency
 */
@Injectable()
export class UsersService {}
```

## Quick Reference Commands

### Debugging Commands

```bash
# Start in debug mode
npm run start:debug

# Start with increased heap memory
NODE_OPTIONS="--max-old-space-size=4096" npm run start:debug

# Run with verbose logging
LOG_LEVEL=verbose npm run start

# Debug specific module loading
DEBUG=nest:* npm run start

# Check TypeScript compilation
npx tsc --noEmit

# Validate module structure
npx nest info
```

### Common Fixes

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Rebuild NestJS
npm run build
rm -rf dist && npm run build

# Clear cache
npm cache clean --force

# Check for duplicate packages
npm dedupe

# Update NestJS packages
npx npm-check-updates -u "@nestjs/*"
npm install
```

### Inspection Commands

```bash
# List all modules and providers
npx nest info

# Check circular dependencies
npx madge --circular --extensions ts src/

# Analyze bundle size
npx source-map-explorer dist/main.js

# Check TypeScript config
npx tsc --showConfig

# Verify imports
npx ts-unused-exports tsconfig.json
```

### Docker Debugging

```bash
# Access container shell
docker exec -it <container_id> sh

# View container logs
docker logs -f <container_id>

# Check container environment
docker exec <container_id> env

# Debug with docker compose
docker compose -f docker-compose.debug.yml up

# Attach to running container
docker attach <container_id>
```

## Exception Filters for Better Error Handling

```typescript
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
  Logger,
} from '@nestjs/common';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    const message =
      exception instanceof HttpException
        ? exception.getResponse()
        : 'Internal server error';

    const errorResponse = {
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      method: request.method,
      message: typeof message === 'string' ? message : (message as any).message,
    };

    this.logger.error(
      `${request.method} ${request.url} ${status}`,
      exception instanceof Error ? exception.stack : String(exception),
    );

    response.status(status).json(errorResponse);
  }
}

// Register globally
app.useGlobalFilters(new AllExceptionsFilter());
```

## Performance Debugging

```typescript
// 1. Add timing interceptor
@Injectable()
export class TimingInterceptor implements NestInterceptor {
  private readonly logger = new Logger(TimingInterceptor.name);

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const now = Date.now();
    const request = context.switchToHttp().getRequest();

    return next.handle().pipe(
      tap(() => {
        const elapsed = Date.now() - now;
        this.logger.log(`${request.method} ${request.url} - ${elapsed}ms`);

        if (elapsed > 1000) {
          this.logger.warn(`Slow request: ${request.url} took ${elapsed}ms`);
        }
      }),
    );
  }
}

// 2. Profile database queries
import { Logger } from '@nestjs/common';

// In TypeORM configuration
{
  logging: ['query', 'error', 'warn'],
  logger: 'advanced-console',
  maxQueryExecutionTime: 1000,  // Log slow queries
}
```

## Sources

- [NestJS Official Documentation - Common Errors](https://docs.nestjs.com/faq/common-errors)
- [NestJS Official Documentation - Exception Filters](https://docs.nestjs.com/exception-filters)
- [NestJS Official Documentation - Logger](https://docs.nestjs.com/techniques/logger)
- [Debugging NestJS in VSCode - Plain English](https://plainenglish.io/blog/debugging-nestjs-in-vscode)
- [Debugging NestJS Applications in VS Code - Medium](https://medium.com/@xjaroo.iphone/debugging-nestjs-applications-in-vs-code-or-cursor-ai-ide-a-comprehensive-guide-5a6848d97cf7)
- [Step-debugging Docker Compose NestJS services - Rob Allen](https://akrabat.com/step-debugging-docker-compose-nestjs-services/)
- [NestJS Error Handling Patterns - Better Stack](https://betterstack.com/community/guides/scaling-nodejs/error-handling-nestjs/)
- [Error Handling in NestJS Best Practices - DEV Community](https://dev.to/geampiere/error-handling-in-nestjs-best-practices-and-examples-5e76)
- [10 Common Mistakes to Avoid in NestJS - Medium](https://medium.com/@enguerrandpp/10-common-mistakes-to-avoid-when-using-nest-js-ea96f5f460b0)
- [Debugging Nest.js Applications - Rookout](https://www.rookout.com/blog/debugging-nest-js-applications-examples-packages-config/)
