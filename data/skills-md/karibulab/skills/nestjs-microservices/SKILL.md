---
name: nestjs-microservices
description: Build microservices using design and architecture best practices. Use when you need to create or modify code for a project developed with NestJS and deployed with Helm.
---

# NestJS Microservices

Production-ready NestJS microservices deployable on Kubernetes.

## Purpose

Create or modify microservice code for a NestJS project following design and architecture best practices, with Kubernetes deployment in mind.
- Follow monitoring and logging best practices using Pino Logger.
- Follow RESTful API design principles.
- Follow SOLID principles using TypeScript and NestJS.
- Input validation using Valibot.
- Use TypedORM for ORM.
- Use Valibot for input validation.
- Use Docker for containerization.
- Use GCP service accounts for GCP integration.

## When to Use

- Build API using NestJS.
- Follow SOLID principles using TypeScript and NestJS.
- Use Pino Logger for logging with nestjs-pino.
- Use Valibot for input validation with nestjs-valibot.
- Development environment with NestJS CLI and NestJS Dev Server.
- Use Helm 3 for Kubernetes deployment.

## Instructions

1. Create the microservice.
2. Add default values.
3. Add required values.
4. Add optional values.
5. Add sensitive values.
6. Add environment values.
7. Add configuration values.
8. Secret values must NEVER be in the source code, but they can be loaded into the template at deployment time.
9. Always validate that NestJS module configuration is correct and that they are added in `app.module.ts`.
10. Follow NestJS naming conventions.

## DTOs

DTOs are objects used to validate API input and output data. Valibot must be used for input validation.

```typescript
// src/dto/get-access-token.dto.ts
import * as v from 'valibot';
import { createDto } from 'nestjs-valibot';

export const GetAccessTokenInputSchema = v.object({
    user_id: v.number(),
    expires_in_minutes: v.optional(v.number()),
});

export class GetAccessTokenInputDto extends createDto(GetAccessTokenInputSchema) {}

export class GetAccessTokenOutputDto {
    access_token: string;
}
```

## Reference Files

- `references/typed-orm.md` - TypedORM
- `references/pino-logger.md` - Pino Logger

## Related Skills

- `screaming-architecture` - For project structure
