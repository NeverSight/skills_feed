---
name: nestjs
description: >
  NestJS best practices with decorators, modules, and TypeORM.
  Trigger: When building NestJS applications with decorators.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with nestjs"

## When to Use

Use this skill when:
- Building NestJS backend applications
- Using decorators and dependency injection
- Implementing REST or GraphQL APIs
- Working with TypeORM or Prisma

---

## Critical Patterns

### Module Organization (REQUIRED)

```typescript
// ✅ ALWAYS: Feature modules with clear boundaries
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

### DTOs with Validation (REQUIRED)

```typescript
// ✅ ALWAYS: Use class-validator decorators
export class CreateUserDto {
  @IsString()
  @MinLength(2)
  name: string;

  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;
}
```

### Exception Filters (REQUIRED)

```typescript
// ✅ ALWAYS: Custom exceptions for domain errors
export class UserNotFoundException extends NotFoundException {
  constructor(userId: string) {
    super(`User with ID ${userId} not found`);
  }
}

// Global exception filter
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    // Handle all exceptions
  }
}
```

---

## Decision Tree

```
Need CRUD?                 → Use @nestjs/crud
Need auth?                 → Use @nestjs/passport + JWT
Need caching?              → Use @nestjs/cache-manager
Need queue processing?     → Use @nestjs/bull
Need GraphQL?              → Use @nestjs/graphql
Need WebSockets?           → Use @nestjs/websockets
```

---

## Code Examples

### Controller with Guards

```typescript
@Controller('users')
@UseGuards(JwtAuthGuard)
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<User> {
    return this.usersService.findById(id);
  }

  @Post()
  @UsePipes(new ValidationPipe({ transform: true }))
  async create(@Body() dto: CreateUserDto): Promise<User> {
    return this.usersService.create(dto);
  }
}
```

### Service with Repository

```typescript
@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
  ) {}

  async findById(id: string): Promise<User> {
    const user = await this.usersRepository.findOne({ where: { id } });
    if (!user) throw new UserNotFoundException(id);
    return user;
  }
}
```

---

## Commands

```bash
nest new myapp
nest generate module users
nest generate controller users
nest generate service users
npm run start:dev
npm run test
```

---

## Resources

- **Backend patterns**: [backend.md](backend.md)
