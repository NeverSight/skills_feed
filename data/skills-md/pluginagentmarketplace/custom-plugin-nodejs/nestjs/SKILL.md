---
name: nestjs
description: Build enterprise-grade Node.js applications with NestJS framework, TypeScript, dependency injection, and modular architecture
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 08-nodejs-microservices
bond_type: PRIMARY_BOND
---

# NestJS Framework Skill

Master NestJS for building scalable, maintainable Node.js applications with TypeScript, dependency injection, and enterprise patterns.

## Quick Start

NestJS app in 4 steps:
1. **Create Project** - `nest new project-name`
2. **Define Modules** - Organize features
3. **Add Controllers** - Handle requests
4. **Create Services** - Business logic

## Core Concepts

### Module Structure
```typescript
// users/users.module.ts
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './entities/user.entity';

@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService] // Make available to other modules
})
export class UsersModule {}
```

### Controller
```typescript
// users/users.controller.ts
import { Controller, Get, Post, Body, Param, Query, UseGuards } from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';

@ApiTags('users')
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  @ApiOperation({ summary: 'Get all users' })
  findAll(@Query('page') page = 1, @Query('limit') limit = 10) {
    return this.usersService.findAll(page, limit);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);
  }

  @Post()
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }
}
```

### Service with Dependency Injection
```typescript
// users/users.service.ts
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './entities/user.entity';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>
  ) {}

  async findAll(page: number, limit: number) {
    const [users, total] = await this.usersRepository.findAndCount({
      skip: (page - 1) * limit,
      take: limit
    });
    return { data: users, total, page, limit };
  }

  async findOne(id: string): Promise<User> {
    const user = await this.usersRepository.findOne({ where: { id } });
    if (!user) {
      throw new NotFoundException(`User #${id} not found`);
    }
    return user;
  }

  async create(createUserDto: CreateUserDto): Promise<User> {
    const user = this.usersRepository.create(createUserDto);
    return this.usersRepository.save(user);
  }
}
```

## Learning Path

### Beginner (2-3 weeks)
- ✅ NestJS CLI and project structure
- ✅ Modules, Controllers, Services
- ✅ Dependency injection basics
- ✅ Basic CRUD operations

### Intermediate (4-6 weeks)
- ✅ Guards, Pipes, Interceptors
- ✅ TypeORM/Prisma integration
- ✅ JWT authentication
- ✅ Validation with class-validator

### Advanced (8-12 weeks)
- ✅ Microservices with transports
- ✅ GraphQL with NestJS
- ✅ WebSockets (Gateways)
- ✅ Testing strategies

## Validation with DTOs
```typescript
// dto/create-user.dto.ts
import { IsEmail, IsString, MinLength, IsOptional } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateUserDto {
  @ApiProperty({ example: 'john@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'John Doe' })
  @IsString()
  @MinLength(2)
  name: string;

  @ApiProperty({ example: 'password123' })
  @IsString()
  @MinLength(8)
  password: string;

  @ApiProperty({ required: false })
  @IsOptional()
  @IsString()
  avatar?: string;
}
```

## Guards for Authentication
```typescript
// auth/guards/jwt-auth.guard.ts
import { Injectable, ExecutionContext } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  canActivate(context: ExecutionContext) {
    return super.canActivate(context);
  }
}

// auth/guards/roles.guard.ts
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>('roles', context.getHandler());
    if (!requiredRoles) return true;

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}
```

## Exception Filters
```typescript
// filters/http-exception.filter.ts
import { ExceptionFilter, Catch, ArgumentsHost, HttpException } from '@nestjs/common';
import { Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();

    response.status(status).json({
      success: false,
      statusCode: status,
      message: exception.message,
      timestamp: new Date().toISOString()
    });
  }
}
```

## Microservices Transport
```typescript
// main.ts for microservice
import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';

const app = await NestFactory.createMicroservice<MicroserviceOptions>(
  AppModule,
  {
    transport: Transport.RMQ,
    options: {
      urls: ['amqp://localhost:5672'],
      queue: 'orders_queue',
      queueOptions: { durable: true }
    }
  }
);
await app.listen();
```

## Unit Test Template
```typescript
describe('UsersService', () => {
  let service: UsersService;
  let repository: Repository<User>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: getRepositoryToken(User),
          useValue: {
            findOne: jest.fn(),
            create: jest.fn(),
            save: jest.fn()
          }
        }
      ]
    }).compile();

    service = module.get<UsersService>(UsersService);
    repository = module.get<Repository<User>>(getRepositoryToken(User));
  });

  it('should find user by id', async () => {
    const user = { id: '1', name: 'John' };
    jest.spyOn(repository, 'findOne').mockResolvedValue(user as User);

    expect(await service.findOne('1')).toEqual(user);
  });
});
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Circular dependency | Module imports | Use forwardRef() |
| Injection token not found | Missing provider | Add to module providers |
| Validation not working | Missing pipe | Add ValidationPipe globally |
| Guards not firing | Wrong order | Use @UseGuards correctly |

## When to Use

Use NestJS when:
- Building enterprise Node.js applications
- Need TypeScript with strong typing
- Want dependency injection
- Building microservices
- Need OpenAPI documentation

## Related Skills

- Express REST API (underlying framework)
- TypeScript (language)
- GraphQL (alternative to REST)
- Microservices (distributed systems)

## Resources

- [NestJS Documentation](https://docs.nestjs.com)
- [TypeORM Integration](https://docs.nestjs.com/techniques/database)
- [NestJS Microservices](https://docs.nestjs.com/microservices/basics)
