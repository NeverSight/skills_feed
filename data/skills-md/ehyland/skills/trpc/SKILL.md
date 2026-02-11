---
name: trpc
description: End-to-end typesafe APIs with tRPC
metadata:
  author: Eamon Hyland
  version: "2026.2.3"
  source: Generated from https://trpc.io/docs, scripts located at https://github.com/ehyland/skills
---

> The skill is based on tRPC v11.9.0, generated at 2026-02-03.

tRPC allows you to build & consume fully typesafe APIs without schemas or code generation. It uses TypeScript to share types between your server and client.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Routers | Initializing tRPC and defining routers | [core-router](references/core-router.md) |
| Procedures | Defining queries, mutations, and subscriptions | [core-procedure](references/core-procedure.md) |
| Validators | Input and output validation using Zod/Standard Schema | [core-validator](references/core-validator.md) |
| Context | Defining and creating context (inner/outer) | [core-context](references/core-context.md) |
| Middlewares | Procedure middlewares and context extension | [core-middleware](references/core-middleware.md) |
| Vanilla Client | Setting up and using the vanilla tRPC client | [core-client-vanilla](references/core-client-vanilla.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Error Handling | Throwing and handling TRPCError | [features-error-handling](references/features-error-handling.md) |
| Links | Understanding and using tRPC links | [features-links](references/features-links.md) |
| TanStack Query | Integration with TanStack React Query | [features-tanstack-react-query](references/features-tanstack-react-query.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Base Procedures | Creating and using reusable base procedures | [best-practices-base-procedures](references/best-practices-base-procedures.md) |
