---
name: nestjs-pro
description: Senior Backend Architect for NestJS v11 (2026). Specialized in modular microservices, high-performance runtimes (Bun), and type-safe enterprise architectures. Expert in building scalable, resilient, and observable systems using native ESM, NATS/MQTT, and optimized Dependency Injection patterns.
---

# 🦅 Skill: nestjs-pro (v1.0.0)

## Executive Summary
Senior Backend Architect for NestJS v11 (2026). Specialized in modular microservices, high-performance runtimes (Bun), and type-safe enterprise architectures. Expert in building scalable, resilient, and observable systems using native ESM, NATS/MQTT, and optimized Dependency Injection patterns.

---

## 📋 The Conductor's Protocol

1.  **Requirement Decomposition**: Evaluate if the system should be a modular monolith (standard) or a distributed microservice (NATS/MQTT/gRPC).
2.  **Runtime Selection**: Prioritize **Bun** for new performance-critical services; use Node.js only for legacy compatibility.
3.  **Module Architecture**: Enforce "Feature Modules" over technical layers. Every module must be self-contained.
4.  **Verification**: Always run `bun x nest build` and check for circular dependencies using `madge` or internal CLI tools.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Bun & Native ESM
As of 2026, NestJS v11 fully embraces the Bun runtime and native ESM.
- **Rule**: Use `bun` for all package management, testing, and execution.
- **ESM**: Always include `.js` extensions in relative imports as per native ESM requirements.
- **Config**: Set `"type": "module"` in `package.json` and `"module": "NodeNext"` in `tsconfig.json`.

### 2. High-Performance Startup (v11+)
- **Rule**: Leverages the new "Object Reference" module resolution. Avoid heavy metadata hashing.
- **Lazy Loading**: Use `LazyModuleLoader` for modules that are not required on initial boot (e.g., specific PDF generators or export tools).

### 3. Hardened Security & Validation
- **Rule**: Every entry point (Controller/Gateway) MUST use `ValidationPipe` with `whitelist: true` and `forbidNonWhitelisted: true`.
- **Guards**: Implement centralized `AuthGuard` and `RolesGuard` using `Reflector` for metadata-driven authorization.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Quick Start: Modern Bun + NestJS v11 Bootstrap
```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module.js'; // Note the .js extension
import { Logger } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    logger: ['error', 'warn', 'log', 'debug', 'verbose'],
  });
  
  app.setGlobalPrefix('api/v1');
  app.enableShutdownHooks(); // Mandatory for 2026 cloud-native apps

  const port = process.env.PORT || 3000;
  await app.listen(port);
  Logger.log(`🚀 Application is running on: http://localhost:${port}/api/v1`);
}
bootstrap();
```

### Advanced Pattern: Type-Safe Microservice (NATS)
```typescript
// orders.service.ts
import { Injectable, Inject } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { timeout } from 'rxjs';

@Injectable()
export class OrdersService {
  constructor(
    @Inject('PAYMENTS_SERVICE') private paymentsClient: ClientProxy,
  ) {}

  async processOrder(orderData: any) {
    return this.paymentsClient
      .send({ cmd: 'process_payment' }, orderData)
      .pipe(timeout(5000)); // Resilience standard for 2026
  }
}
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** use `@Injectable({ scope: Scope.REQUEST })` unless absolutely necessary. It destroys performance in high-concurrency apps.
2.  **DO NOT** share a single database across different microservices. It leads to distributed monolith hell.
3.  **DO NOT** leave circular dependencies unresolved. v11 startup performance is degraded by complex circular resolutions.
4.  **DO NOT** use `CommonJS` (`require`). Native ESM is the 2026 standard for NestJS.
5.  **DO NOT** perform heavy computation in the main thread. Use `Worker Threads` or offload to specialized microservices.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Enterprise Architecture](./references/architecture.md)**: Feature Modules, CQRS, and Domain-Driven Design.
- **[Microservices & Transports](./references/microservices.md)**: NATS, MQTT, gRPC, and RabbitMQ in 2026.
- **[Security & IAM](./references/security.md)**: JWT, OIDC, and custom Permission Guards.
- **[Performance & Bun](./references/performance-bun.md)**: Cold starts, memory management, and AOT optimization.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/check-circular.ts`: Automated check for circular dependencies using native ESM resolution.
- `scripts/generate-feature.py`: Scaffolds a complete feature module (Controller, Service, DTO, Entity).

---

## 🎓 Learning Resources
- [NestJS Official Documentation](https://docs.nestjs.com/)
- [NestJS v11 Migration Guide](https://docs.nestjs.com/migration-guide)
- [Bun + NestJS Integration](https://bun.sh/guides/runtime/nestjs)

---
*Updated: January 23, 2026 - 17:10*
