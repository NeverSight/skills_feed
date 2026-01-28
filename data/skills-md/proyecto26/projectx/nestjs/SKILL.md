---
name: nestjs
description: NestJS microservices development. Use when creating controllers, services, modules, guards, interceptors, or working with NestJS patterns in auth, order, or product services.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# NestJS Microservices Development

## Project Structure

This project uses NestJS for three microservices:
- `apps/auth` - Authentication (JWT, Passport)
- `apps/order` - Order management (integrates with Temporal)
- `apps/product` - Product catalog

Shared modules are in `packages/core`.

## Creating a New Module

### 1. Create Module File

```typescript
// feature/feature.module.ts
import { Module } from '@nestjs/common';
import { FeatureController } from './feature.controller';
import { FeatureService } from './feature.service';

@Module({
  controllers: [FeatureController],
  providers: [FeatureService],
  exports: [FeatureService],
})
export class FeatureModule {}
```

### 2. Create Service with Repository Pattern

```typescript
// feature/feature.service.ts
import { Injectable } from '@nestjs/common';
import { PrismaService } from '@projectx/db';

@Injectable()
export class FeatureService {
  constructor(private readonly prisma: PrismaService) {}

  async findAll() {
    return this.prisma.feature.findMany();
  }

  async findOne(id: string) {
    return this.prisma.feature.findUnique({ where: { id } });
  }

  async create(data: CreateFeatureDto) {
    return this.prisma.feature.create({ data });
  }
}
```

### 3. Create Controller with Swagger

```typescript
// feature/feature.controller.ts
import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { FeatureService } from './feature.service';

@ApiTags('features')
@Controller('features')
export class FeatureController {
  constructor(private readonly featureService: FeatureService) {}

  @Get()
  @ApiOperation({ summary: 'Get all features' })
  @ApiResponse({ status: 200, description: 'Returns all features' })
  findAll() {
    return this.featureService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get feature by ID' })
  findOne(@Param('id') id: string) {
    return this.featureService.findOne(id);
  }

  @Post()
  @ApiOperation({ summary: 'Create a feature' })
  create(@Body() createFeatureDto: CreateFeatureDto) {
    return this.featureService.create(createFeatureDto);
  }
}
```

## DTOs with Validation

```typescript
// feature/dto/create-feature.dto.ts
import { IsString, IsNotEmpty, IsOptional } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateFeatureDto {
  @ApiProperty({ description: 'Feature name' })
  @IsString()
  @IsNotEmpty()
  name: string;

  @ApiPropertyOptional({ description: 'Feature description' })
  @IsString()
  @IsOptional()
  description?: string;
}
```

## Authentication Guards

Use guards from `@projectx/core`:

```typescript
import { UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '@projectx/core';

@Controller('protected')
@UseGuards(JwtAuthGuard)
export class ProtectedController {
  // All routes require authentication
}
```

## Exception Handling

```typescript
import { NotFoundException, BadRequestException } from '@nestjs/common';

// In service
async findOne(id: string) {
  const item = await this.prisma.feature.findUnique({ where: { id } });
  if (!item) {
    throw new NotFoundException(`Feature with ID ${id} not found`);
  }
  return item;
}
```

## Testing Services

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { FeatureService } from './feature.service';
import { PrismaService } from '@projectx/db';

describe('FeatureService', () => {
  let service: FeatureService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        FeatureService,
        {
          provide: PrismaService,
          useValue: {
            feature: {
              findMany: jest.fn(),
              findUnique: jest.fn(),
              create: jest.fn(),
            },
          },
        },
      ],
    }).compile();

    service = module.get<FeatureService>(FeatureService);
    prisma = module.get<PrismaService>(PrismaService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
```

## Running Services

```bash
# Run specific service
pnpm dev:auth
pnpm dev:order
pnpm dev:product

# Run all services
pnpm dev
```

## Best Practices

1. **Always use DTOs** for request/response validation
2. **Document with Swagger** decorators for API documentation
3. **Use repository pattern** via Prisma services from `@projectx/db`
4. **Handle errors** with NestJS built-in exceptions
5. **Write tests** for services and controllers
6. **Use guards** from `@projectx/core` for authentication
