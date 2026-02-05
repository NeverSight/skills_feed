---
name: nestjs-openapi-docs
description: Comprehensive OpenAPI (Swagger) documentation setup and implementation for NestJS applications. Use when working with NestJS projects that need API documentation, Swagger UI setup, or OpenAPI specification generation. Covers initial setup, decorator usage, CLI plugin configuration, model definitions, authentication, and advanced features like multiple specifications and custom responses.
---

# NestJS OpenAPI Documentation

This skill provides step-by-step guidance for setting up and using OpenAPI (Swagger) documentation in NestJS applications.

## Quick Start Workflow

Follow these steps based on your needs:

1. **First-time setup** → Follow [Initial Setup](#initial-setup)
2. **Document endpoints** → See [Documenting Endpoints](#documenting-endpoints)
3. **Define DTOs/Models** → See [Defining Models](#defining-models)
4. **Enable CLI plugin** → See [CLI Plugin Setup](#cli-plugin-setup)
5. **Advanced features** → See [references/advanced-features.md](references/advanced-features.md)

## Initial Setup

### Installation

```bash
npm install --save @nestjs/swagger
```

### Bootstrap Configuration

In `main.ts`:

```typescript
import { NestFactory } from '@nestjs/core';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const config = new DocumentBuilder()
    .setTitle('Cats example')
    .setDescription('The cats API description')
    .setVersion('1.0')
    .addTag('cats')
    .build();
  const documentFactory = () => SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, documentFactory);

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

### Access Documentation

After starting the server (`npm run start`):

- **Swagger UI**: `http://localhost:3000/api`
- **JSON spec**: `http://localhost:3000/api-json`

To customize JSON endpoint:
```typescript
SwaggerModule.setup('api', app, documentFactory, {
  jsonDocumentUrl: 'swagger/json',
});
// Access at: http://localhost:3000/swagger/json
```

## Documenting Endpoints

### Basic Controller Documentation

```typescript
import { Controller, Get, Post, Body } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiCreatedResponse } from '@nestjs/swagger';

@ApiTags('cats')
@Controller('cats')
export class CatsController {
  @Post()
  @ApiOperation({ summary: 'Create a cat' })
  @ApiCreatedResponse({
    description: 'The cat has been successfully created.',
    type: Cat,
  })
  async create(@Body() createCatDto: CreateCatDto): Promise<Cat> {
    return this.catsService.create(createCatDto);
  }

  @Get()
  @ApiOperation({ summary: 'Get all cats' })
  @ApiOkResponse({
    description: 'List of cats',
    type: [Cat],
  })
  async findAll(): Promise<Cat[]> {
    return this.catsService.findAll();
  }
}
```

### Response Decorators

Use short-hand decorators for common status codes:

```typescript
@Post()
@ApiCreatedResponse({ description: 'Created successfully', type: Cat })
@ApiBadRequestResponse({ description: 'Invalid input' })
@ApiUnauthorizedResponse({ description: 'Unauthorized' })
async create(@Body() createCatDto: CreateCatDto) {}
```

For full list of response decorators, see [references/decorators.md](references/decorators.md).

### Query Parameters

```typescript
import { ApiQuery } from '@nestjs/swagger';

@Get()
@ApiQuery({ name: 'search', required: false, type: String })
@ApiQuery({ name: 'limit', required: false, type: Number })
async findAll(
  @Query('search') search?: string,
  @Query('limit') limit?: number,
) {}
```

### Path Parameters

```typescript
import { ApiParam } from '@nestjs/swagger';

@Get(':id')
@ApiParam({ name: 'id', type: 'string', description: 'Cat ID' })
async findOne(@Param('id') id: string) {}
```

### Custom Headers

```typescript
import { ApiHeader } from '@nestjs/swagger';

@Get()
@ApiHeader({
  name: 'X-Custom-Header',
  description: 'Custom header description',
})
async findAll() {}
```

## Defining Models

### Basic DTO

```typescript
import { ApiProperty } from '@nestjs/swagger';

export class CreateCatDto {
  @ApiProperty()
  name: string;

  @ApiProperty()
  age: number;

  @ApiProperty()
  breed: string;
}
```

### Optional Properties

```typescript
@ApiPropertyOptional()
nickname?: string;

// Or
@ApiProperty({ required: false, default: 'Unknown' })
nickname?: string;
```

### Property with Details

```typescript
@ApiProperty({
  description: 'The age of a cat',
  minimum: 1,
  maximum: 20,
  default: 1,
  example: 5,
})
age: number;
```

### Arrays

```typescript
@ApiProperty({ type: [String] })
tags: string[];
```

### Enums

```typescript
export enum CatBreed {
  Persian = 'Persian',
  Tabby = 'Tabby',
  Siamese = 'Siamese',
}

@ApiProperty({ enum: CatBreed, enumName: 'CatBreed' })
breed: CatBreed;
```

For complex types, nested objects, polymorphic types, and raw definitions, see [references/types-and-models.md](references/types-and-models.md).

## CLI Plugin Setup

The CLI plugin automatically generates `@ApiProperty()` decorators, reducing boilerplate significantly.

### Enable Plugin

Edit `nest-cli.json`:

```json
{
  "collection": "@nestjs/schematics",
  "sourceRoot": "src",
  "compilerOptions": {
    "plugins": ["@nestjs/swagger"]
  }
}
```

### With Options

```json
{
  "collection": "@nestjs/schematics",
  "sourceRoot": "src",
  "compilerOptions": {
    "plugins": [
      {
        "name": "@nestjs/swagger",
        "options": {
          "classValidatorShim": true,
          "introspectComments": true
        }
      }
    ]
  }
}
```

### Before/After Plugin

**Before** (manual decorators):
```typescript
export class CreateCatDto {
  @ApiProperty()
  name: string;

  @ApiProperty()
  age: number;

  @ApiProperty({ required: false })
  breed?: string;
}
```

**After** (with plugin):
```typescript
export class CreateCatDto {
  name: string;
  age: number;
  breed?: string;
}
```

### Comment Introspection

With `introspectComments: true`:

```typescript
/**
 * A list of user's roles
 * @example ['admin']
 */
roles: RoleEnum[] = [];
```

Equivalent to manually writing:
```typescript
@ApiProperty({
  description: `A list of user's roles`,
  example: ['admin'],
})
roles: RoleEnum[] = [];
```

For detailed plugin configuration, SWC setup, and Jest integration, see [references/cli-plugin.md](references/cli-plugin.md).

## File Upload Documentation

```typescript
import { UseInterceptors, UploadedFile } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { ApiConsumes, ApiBody } from '@nestjs/swagger';

class FileUploadDto {
  @ApiProperty({ type: 'string', format: 'binary' })
  file: any;
}

@Post('upload')
@UseInterceptors(FileInterceptor('file'))
@ApiConsumes('multipart/form-data')
@ApiBody({
  description: 'File upload',
  type: FileUploadDto,
})
uploadFile(@UploadedFile() file: Express.Multer.File) {}
```

## Authentication Documentation

### Bearer Token

```typescript
// In controller
@ApiBearerAuth()
@Controller('cats')
export class CatsController {}

// In bootstrap
const config = new DocumentBuilder()
  .addBearerAuth()
  .build();
```

### Basic Auth

```typescript
// In controller
@ApiBasicAuth()
@Controller('cats')
export class CatsController {}

// In bootstrap
const config = new DocumentBuilder()
  .addBasicAuth()
  .build();
```

For OAuth2, Cookie auth, and custom security schemes, see [references/advanced-features.md](references/advanced-features.md#security).

## Common Issues

### Fastify + Helmet CSP Conflict

When using Fastify with Helmet:

```typescript
app.register(helmet, {
  contentSecurityPolicy: {
    directives: {
      defaultSrc: [`'self'`],
      styleSrc: [`'self'`, `'unsafe-inline'`],
      imgSrc: [`'self'`, 'data:', 'validator.swagger.io'],
      scriptSrc: [`'self'`, `https: 'unsafe-inline'`],
    },
  },
});
```

### Plugin Not Working

1. Delete `/dist` folder
2. Restart the application
3. Ensure files have `.dto.ts` or `.entity.ts` suffix
4. Check `nest-cli.json` configuration

### Missing Models in Swagger

Add extra models explicitly:

```typescript
@ApiExtraModels(ExtraModel)
export class CreateCatDto {}

// Or in document options
const documentFactory = () =>
  SwaggerModule.createDocument(app, options, {
    extraModels: [ExtraModel],
  });
```

## Reference Files

Detailed documentation for specific features:

- **[decorators.md](references/decorators.md)** - Complete list of all OpenAPI decorators with examples
- **[types-and-models.md](references/types-and-models.md)** - Complex types, generics, polymorphic models, raw definitions
- **[cli-plugin.md](references/cli-plugin.md)** - Plugin configuration, SWC setup, Jest integration
- **[advanced-features.md](references/advanced-features.md)** - Mapped types, security, multiple specs, global config

## Example

A working example is available at: https://github.com/nestjs/nest/tree/master/sample/11-swagger
