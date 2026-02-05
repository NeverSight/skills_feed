---
name: secret-development
description: |
  Development guide for @rytass/secret base package (密鑰基底套件開發指南). Use when creating new secret adapters (新增密鑰 adapter), understanding base interfaces, or extending secret management functionality. Covers SecretManager abstract class and implementation patterns. Keywords: secret adapter, 密鑰 adapter, 開發指南, vault, credential, key management
---

# Secret Adapter Development Guide (密鑰 Adapter 開發指南)

## Overview

本指南說明如何基於 `@rytass/secret` 基礎套件開發新的密鑰管理適配器。

## Base Package Architecture

```
@rytass/secret (Base)
└── SecretManager (Abstract Class)
    ├── project: string
    ├── get<T>(key): Promise<T> | T
    ├── set<T>(key, value): Promise<void> | void
    └── delete(key): Promise<void> | void
```

## Core Abstract Class

### SecretManager

```typescript
abstract class SecretManager {
  constructor(project: string);

  get project(): string;

  abstract get<T>(key: string): Promise<T> | T;
  abstract set<T>(key: string, value: T): Promise<void> | void;
  abstract delete(key: string): Promise<void> | void;
}
```

## Implementing a New Adapter

### Step 1: Define Configuration Interface

```typescript
// my-secret-adapter/src/typings.ts
export interface MySecretOptions {
  endpoint: string;
  apiKey: string;
  namespace?: string;
  cacheEnabled?: boolean;
  cacheTTL?: number;  // milliseconds
}
```

### Step 2: Implement Secret Manager

```typescript
// my-secret-adapter/src/my-secret.ts
import { SecretManager } from '@rytass/secret';
import axios from 'axios';

export class MySecret extends SecretManager {
  private cache: Map<string, { value: unknown; expiry: number }> = new Map();

  constructor(
    project: string,
    private readonly options: MySecretOptions,
  ) {
    super(project);
  }

  async get<T>(key: string): Promise<T> {
    // Check cache first
    if (this.options.cacheEnabled) {
      const cached = this.cache.get(key);
      if (cached && cached.expiry > Date.now()) {
        return cached.value as T;
      }
    }

    const response = await axios.get(
      `${this.options.endpoint}/secrets/${this.project}/${key}`,
      {
        headers: { 'Authorization': `Bearer ${this.options.apiKey}` },
      },
    );

    const value = response.data.value as T;

    // Update cache
    if (this.options.cacheEnabled && this.options.cacheTTL) {
      this.cache.set(key, {
        value,
        expiry: Date.now() + this.options.cacheTTL,
      });
    }

    return value;
  }

  async set<T>(key: string, value: T): Promise<void> {
    await axios.put(
      `${this.options.endpoint}/secrets/${this.project}/${key}`,
      { value },
      {
        headers: { 'Authorization': `Bearer ${this.options.apiKey}` },
      },
    );

    // Invalidate cache
    this.cache.delete(key);
  }

  async delete(key: string): Promise<void> {
    await axios.delete(
      `${this.options.endpoint}/secrets/${this.project}/${key}`,
      {
        headers: { 'Authorization': `Bearer ${this.options.apiKey}` },
      },
    );

    // Invalidate cache
    this.cache.delete(key);
  }

  // Optional: Clear all cache
  clearCache(): void {
    this.cache.clear();
  }
}
```

### Step 3: Add NestJS Module (Optional)

```typescript
// my-secret-adapter-nestjs/src/my-secret.module.ts
import { Module, DynamicModule, Global } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { MySecret, MySecretOptions } from '@rytass/my-secret-adapter';

export const MY_SECRET_SERVICE = Symbol('MY_SECRET_SERVICE');

@Global()
@Module({})
export class MySecretModule {
  static forRoot(options: MySecretOptions & { project: string }): DynamicModule {
    return {
      module: MySecretModule,
      providers: [
        {
          provide: MY_SECRET_SERVICE,
          useFactory: () => new MySecret(options.project, options),
        },
      ],
      exports: [MY_SECRET_SERVICE],
    };
  }

  static forRootAsync(options: {
    useFactory: (...args: any[]) => MySecretOptions & { project: string };
    inject?: any[];
  }): DynamicModule {
    return {
      module: MySecretModule,
      providers: [
        {
          provide: MY_SECRET_SERVICE,
          useFactory: (...args) => {
            const config = options.useFactory(...args);
            return new MySecret(config.project, config);
          },
          inject: options.inject || [],
        },
      ],
      exports: [MY_SECRET_SERVICE],
    };
  }
}
```

### Step 4: Create NestJS Service Wrapper

```typescript
// my-secret-adapter-nestjs/src/my-secret.service.ts
import { Injectable, Inject } from '@nestjs/common';
import { MySecret } from '@rytass/my-secret-adapter';
import { MY_SECRET_SERVICE } from './my-secret.module';

@Injectable()
export class MySecretService {
  constructor(
    @Inject(MY_SECRET_SERVICE)
    private readonly manager: MySecret,
  ) {}

  async get<T = string>(key: string): Promise<T> {
    return this.manager.get<T>(key);
  }

  async set<T = string>(key: string, value: T): Promise<void> {
    return this.manager.set(key, value);
  }

  async delete(key: string): Promise<void> {
    return this.manager.delete(key);
  }
}
```

## Design Patterns

### Sync vs Async Operations

根據後端特性選擇同步或非同步：

```typescript
// 非同步（網路請求）
async get<T>(key: string): Promise<T> {
  return await fetchFromRemote(key);
}

// 同步（本地快取）
get<T>(key: string): T {
  return this.localCache.get(key);
}

// 混合模式（像 Vault adapter）
get<T>(key: string): VaultGetType<Options, T> {
  if (this.options.online) {
    return this.fetchOnline(key);  // Promise<T>
  }
  return this.localCache.get(key);  // T
}
```

### Event-Driven Architecture

```typescript
import { EventEmitter } from 'events';

export enum MySecretEvents {
  CONNECTED = 'CONNECTED',
  DISCONNECTED = 'DISCONNECTED',
  ERROR = 'ERROR',
}

export class MySecret extends SecretManager {
  private emitter = new EventEmitter();

  on(event: MySecretEvents, listener: (...args: any[]) => void): void {
    this.emitter.on(event, listener);
  }

  private emit(event: MySecretEvents, ...args: any[]): void {
    this.emitter.emit(event, ...args);
  }
}
```

### Fallback Mechanism

```typescript
export class MySecretWithFallback extends SecretManager {
  constructor(
    project: string,
    private readonly primary: SecretManager,
    private readonly fallback: SecretManager,
  ) {
    super(project);
  }

  async get<T>(key: string): Promise<T> {
    try {
      return await this.primary.get<T>(key);
    } catch {
      return await this.fallback.get<T>(key);
    }
  }
}
```

## Testing Guidelines

```typescript
// __tests__/my-secret.spec.ts
import { MySecret } from '../src';

describe('MySecret', () => {
  const secret = new MySecret('test-project', {
    endpoint: 'https://api.example.com',
    apiKey: 'test-key',
    cacheEnabled: true,
    cacheTTL: 5000,
  });

  it('should get secret value', async () => {
    const value = await secret.get<string>('DATABASE_URL');
    expect(value).toBeDefined();
  });

  it('should set and get secret', async () => {
    await secret.set('TEST_KEY', 'test-value');
    const value = await secret.get<string>('TEST_KEY');
    expect(value).toBe('test-value');
  });

  it('should delete secret', async () => {
    await secret.set('TO_DELETE', 'value');
    await secret.delete('TO_DELETE');
    await expect(secret.get('TO_DELETE')).rejects.toThrow();
  });

  it('should use cache', async () => {
    const spy = jest.spyOn(axios, 'get');
    await secret.get('CACHED_KEY');
    await secret.get('CACHED_KEY');
    expect(spy).toHaveBeenCalledTimes(1);
  });
});
```

## Package Structure

```
my-secret-adapter/
├── src/
│   ├── index.ts
│   ├── typings.ts
│   └── my-secret.ts
├── __tests__/
│   └── my-secret.spec.ts
├── package.json
└── tsconfig.build.json

my-secret-adapter-nestjs/          # Optional NestJS wrapper
├── src/
│   ├── index.ts
│   ├── my-secret.module.ts
│   └── my-secret.service.ts
└── package.json
```

## Publishing Checklist

- [ ] 繼承 `SecretManager` 抽象類別
- [ ] 實現 `get`, `set`, `delete` 方法
- [ ] 定義清楚的配置介面
- [ ] 實現快取機制（如適用）
- [ ] 實現錯誤處理
- [ ] 撰寫單元測試
- [ ] 提供 NestJS 模組包裝（可選）
- [ ] 遵循 `@rytass/secret-adapter-*` 命名規範
