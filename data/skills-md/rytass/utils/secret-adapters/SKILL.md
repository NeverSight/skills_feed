---
name: secret-adapters
description: |
  Secret management integration (密鑰管理整合). Use when working with HashiCorp Vault, credential management, or secure configuration. Covers secret storage (密鑰儲存), key management (金鑰管理), NestJS integration, online/offline modes, and automatic token renewal. Keywords: 密鑰, 機密, 金鑰, 秘密管理, secret, vault, credential, key management, HashiCorp, token, 環境變數, configuration
---

# Secret Management Adapters (密鑰管理適配器)

## Overview

`@rytass/secret` 系列套件提供統一的密鑰管理介面，目前支援 HashiCorp Vault 作為後端儲存。

### 套件清單

| 套件 | 說明 | 用途 |
|------|------|------|
| `@rytass/secret` | 基礎介面 | 定義 `SecretManager` 抽象類別 |
| `@rytass/secret-adapter-vault` | Vault 適配器 | HashiCorp Vault 完整實現 |
| `@rytass/secret-adapter-vault-nestjs` | NestJS 模組 | Vault 的 NestJS 依賴注入整合 |

### SecretManager 抽象類別

```typescript
import { SecretManager } from '@rytass/secret';

// 所有 Secret Adapter 都繼承此抽象類別
abstract class SecretManager {
  constructor(project: string);
  get project(): string;  // 取得初始化時的 path
  abstract get<T>(key: string): Promise<T> | T;
  abstract set<T>(key: string, value: T): Promise<void> | void;
  abstract delete(key: string): Promise<void> | void;
}
```

## Quick Start

### 安裝

```bash
# 直接使用 Vault
npm install @rytass/secret-adapter-vault

# NestJS 專案
npm install @rytass/secret-adapter-vault-nestjs
```

### 基本使用（離線模式）

```typescript
import { VaultSecret } from '@rytass/secret-adapter-vault';

const vault = new VaultSecret('apps/myapp/config', {
  host: 'https://vault.company.com',
  online: false,  // 離線模式（預設）
  auth: {
    account: 'myapp-service',
    password: 'secure-password',
  },
  onReady: () => {
    // 同步操作，無需 await
    const dbPassword = vault.get<string>('DATABASE_PASSWORD');

    // 修改本地快取（不立即同步到 Vault）
    vault.set('API_KEY', 'new-value');
    vault.delete('OLD_CONFIG');

    // 或者立即同步到 Vault（syncToOnline = true）
    vault.set('ANOTHER_KEY', 'value', true);  // 立即同步
    vault.delete('TEMP_KEY', true);           // 立即同步

    // 批次同步變更到 Vault
    vault.sync();  // 如果版本不符會拋錯
    vault.sync(true);  // force = true，強制覆蓋
  },
});
```

### NestJS 整合

```typescript
// app.module.ts
import { VaultModule } from '@rytass/secret-adapter-vault-nestjs';

@Module({
  imports: [
    VaultModule.forRoot({
      path: '/secret/data/myapp',
      fallbackFile: '.env.local',  // Vault 不可用時的備用
    }),
  ],
})
export class AppModule {}

// config.service.ts
@Injectable()
export class ConfigService {
  constructor(private readonly vault: VaultService) {}

  // get() 預設泛型為 string，可省略
  async getDatabaseUrl(): Promise<string> {
    return this.vault.get('DATABASE_URL');  // 等同 get<string>()
  }

  // set() 和 delete() 也支援 syncToOnline 參數
  async updateConfig(key: string, value: string): Promise<void> {
    await this.vault.set(key, value);       // syncToOnline = false（預設）
    await this.vault.set(key, value, true); // syncToOnline = true，立即同步
  }

  async removeConfig(key: string): Promise<void> {
    await this.vault.delete(key);       // syncToOnline = false（預設）
    await this.vault.delete(key, true); // syncToOnline = true，立即同步
  }
}
```

## Core Concepts

### 線上模式 vs 離線模式

| 特性 | 線上模式 | 離線模式（預設） |
|------|---------|-----------------|
| 操作方式 | 即時連接 Vault | 使用本地快取 |
| `get()` 返回 | `Promise<T>` | `T`（同步） |
| `set()`/`delete()` 返回 | `Promise<void>` | `Promise<void>`（syncToOnline 時）或同步操作本地快取 |
| 效能 | 有網路延遲 | 極快 |
| 適用場景 | 需即時更新 | 頻繁讀取 |
| Token 管理 | 自動續期（預設 TTL 約 32 天）| 初始化時取得 |

### 狀態管理

```typescript
enum VaultSecretState {
  INIT = 'INIT',              // 初始化中
  READY = 'READY',            // 可用
  TERMINATED = 'TERMINATED',  // 已終止
}

// 檢查狀態
if (vault.state === VaultSecretState.READY) {
  // 可以安全操作
}
```

### 事件驅動

```typescript
enum VaultEvents {
  INITED = 'INITED',              // 初始化開始
  READY = 'READY',                // Vault 準備就緒
  TOKEN_RENEWED = 'TOKEN_RENEWED', // Token 已續期
  TERMINATED = 'TERMINATED',       // 連線已終止
  ERROR = 'ERROR',                 // 發生錯誤
}
```

### 完整型別定義

以下所有型別皆從 `@rytass/secret-adapter-vault` 導出：

```typescript
import {
  VaultSecret,
  VaultSecretState,
  VaultEvents,
  VaultAuthMethods,
  VaultAuthMethodAccountPassword,
  VaultSecretOptions,
  VaultSecretOnlineOptions,
  VaultSecretOfflineOptions,
  VaultGetType,
  VaultSetType,
  VaultDeleteType,
  VaultTokenRetrieveSuccessResponse,
  VaultAPIFailedResponse,
  VaultTokenRetrieveResponse,
  VaultGetSecretSuccessResponse,
  VaultGetSecretResponse,
} from '@rytass/secret-adapter-vault';
```

**認證型別：**
```typescript
// 帳號密碼認證
interface VaultAuthMethodAccountPassword {
  account: string;
  password: string;
}

// 支援的認證方式（目前僅支援帳號密碼）
type VaultAuthMethods = VaultAuthMethodAccountPassword;
```

**選項型別：**
```typescript
// 通用選項
interface VaultSecretOptions {
  host: string;               // Vault 伺服器位址
  auth: VaultAuthMethods;     // 認證方式
  online?: boolean;           // 是否使用線上模式（預設 false）
  tokenTTL?: number;          // Token TTL（毫秒），預設 2764724（約 32 天）
  onError?: (error: string) => void;  // 錯誤回調
  onReady?: () => void;       // 準備就緒回調
}

// 線上模式選項（online: true）
// 注意：獨立定義，非繼承自 VaultSecretOptions
interface VaultSecretOnlineOptions {
  host: string;
  auth: VaultAuthMethods;
  online: true;
  tokenTTL?: number;
  onError?: (error: string) => void;
  onReady?: () => void;
}

// 離線模式選項（online: false 或省略）
// 注意：獨立定義，非繼承自 VaultSecretOptions
interface VaultSecretOfflineOptions {
  host: string;
  auth: VaultAuthMethods;
  online?: false;
  tokenTTL?: number;
  onError?: (error: string) => void;
  onReady?: () => void;
}
```

**條件型別（根據模式決定返回值）：**
```typescript
// get() 返回型別：線上模式為 Promise<T>，離線模式為 T
type VaultGetType<O extends VaultSecretOptions, T> = O extends VaultSecretOnlineOptions ? Promise<T> : T;

// set() 返回型別
type VaultSetType<O extends VaultSecretOptions> = O extends VaultSecretOnlineOptions ? Promise<void> : void;

// delete() 返回型別
type VaultDeleteType<O extends VaultSecretOptions> = O extends VaultSecretOnlineOptions ? Promise<void> : void;
```

**API 回應型別：**
```typescript
// API 失敗回應
interface VaultAPIFailedResponse {
  errors: string[];
}

// Token 取得成功回應
// 注意：token_type 使用內部 enum VaultTokenType（未導出）
type VaultTokenRetrieveSuccessResponse = {
  auth: {
    client_token: string;
    accessor: string;
    policies: string[];
    token_policies: string[];
    metadata: Record<string, string> | null;
    lease_duration: number;
    renewable: boolean;
    entity_id: string;
    token_type: 'service' | 'batch';  // VaultTokenType enum（未導出）
    orphan: boolean;
    mfa_requirement: null;
    num_uses: number;
  };
} & VaultAPIBaseInfo<null>;

// Token 取得回應（成功或失敗）
type VaultTokenRetrieveResponse = VaultTokenRetrieveSuccessResponse | VaultAPIFailedResponse;

// Secret 取得成功回應
type VaultGetSecretSuccessResponse = VaultAPIBaseInfo<{
  data: Record<string, unknown>;
  metadata: {
    created_time: string;
    custom_metadata: null;
    deletion_time: string;
    destroyed: boolean;
    version: number;
  };
}>;

// Secret 取得回應（成功或失敗）
type VaultGetSecretResponse = VaultGetSecretSuccessResponse | VaultAPIFailedResponse;
```

## Common Patterns

### 線上模式使用

```typescript
const vault = new VaultSecret('apps/myapp/config', {
  host: 'https://vault.company.com',
  online: true,
  auth: {
    account: 'service-account',
    password: 'password',
  },
});

// 需要 await
const secret = await vault.get<string>('SECRET_KEY');
await vault.set('NEW_KEY', 'value');
await vault.delete('OLD_KEY');
```

### TypeORM 整合

```typescript
@Module({
  imports: [
    VaultModule.forRoot({ path: '/secret/data/database' }),
    TypeOrmModule.forRootAsync({
      imports: [VaultModule],
      inject: [VaultService],
      useFactory: async (vault: VaultService) => ({
        type: 'postgres',
        host: await vault.get<string>('DB_HOST'),
        port: await vault.get<number>('DB_PORT'),
        username: await vault.get<string>('DB_USERNAME'),
        password: await vault.get<string>('DB_PASSWORD'),
        database: await vault.get<string>('DB_NAME'),
      }),
    }),
  ],
})
export class DatabaseModule {}
```

### JWT 模組整合

```typescript
@Module({
  imports: [
    VaultModule.forRoot({ path: '/secret/data/auth' }),
    JwtModule.registerAsync({
      imports: [VaultModule],
      inject: [VaultService],
      useFactory: async (vault: VaultService) => ({
        secret: await vault.get<string>('JWT_SECRET'),
        signOptions: {
          expiresIn: await vault.get<string>('JWT_EXPIRY') || '1h',
        },
      }),
    }),
  ],
})
export class AuthModule {}
```

### 錯誤處理與備用機制

```typescript
const vault = new VaultSecret('apps/myapp/config', {
  host: 'https://vault.company.com',
  online: false,
  auth: { account: 'user', password: 'pass' },
  onError: (error) => {
    console.error('Vault error:', error);
    // 可在此切換到備用配置
  },
  onReady: () => {
    console.log('Vault ready');
  },
});
```

### 定期同步（離線模式）

```typescript
// 離線模式下定期同步變更
setInterval(async () => {
  try {
    // sync() 會檢查版本，如果 Vault 上的版本與快取不符會拋出錯誤
    await vault.sync();
    console.log('Synced to Vault');
  } catch (error) {
    if (error.message.includes('version is not match')) {
      // 版本不符時，可選擇強制覆蓋
      await vault.sync(true); // force = true
      console.log('Force synced to Vault');
    } else {
      console.warn('Sync failed:', error);
    }
  }
}, 300000); // 每 5 分鐘
```

### set() / delete() 的 syncToOnline 參數

```typescript
// 離線模式下，set() 和 delete() 預設只修改本地快取
vault.set('KEY', 'value');        // syncToOnline = false（預設）
vault.delete('KEY');               // syncToOnline = false（預設）

// 如果需要立即同步到 Vault，傳入 syncToOnline = true
vault.set('KEY', 'value', true);   // 立即同步到 Vault
vault.delete('KEY', true);          // 立即同步到 Vault
```

### 優雅關閉

```typescript
process.on('SIGTERM', () => {
  vault.terminate();
  process.exit(0);
});
```

## NestJS Module Reference

### VaultModuleOptions

```typescript
// NestJS 模組配置選項
interface VaultModuleOptions {
  path: string;         // Vault secret path（預設 '/'）
  fallbackFile?: string; // Vault 不可用時的備用 .env 檔案
}
```

### VaultService 方法簽名

```typescript
class VaultService {
  // get() 預設泛型為 string，可省略
  async get<T = string>(key: string): Promise<T>;

  // set() 支援 syncToOnline 參數
  async set<T = string>(key: string, value: T, syncToOnline = false): Promise<void>;

  // delete() 支援 syncToOnline 參數
  async delete(key: string, syncToOnline = false): Promise<void>;
}
```

## Environment Variables (NestJS)

```bash
# 必需（若未設置 VAULT_HOST，會自動切換至備用模式）
VAULT_HOST=https://vault.example.com:8200
VAULT_ACCOUNT=your-username
VAULT_PASSWORD=your-password
```

> **注意：** `path` 不是透過環境變數設定，而是在 `VaultModule.forRoot({ path: '...' })` 中指定。

## API Reference

詳細 API 文件請參閱 [reference.md](reference.md)。

## Troubleshooting

### 連線失敗

1. 確認 `VAULT_HOST` 使用 HTTPS
2. 檢查網路連線和防火牆
3. 驗證帳號密碼正確

### Token 過期

線上模式會自動續期。如果仍然過期：
1. 檢查 `tokenTTL` 設定
2. 確認 Vault 伺服器時間同步
3. 查看 Vault Token 政策設定

### NestJS 備用模式

當 `VAULT_HOST` 未設置時或連線失敗時，VaultService 會切換至備用模式：
- `get()` 從 ConfigService（環境變數）讀取
- `set()` 和 `delete()` **會拋出錯誤**：`"Cannot set/delete value when fallback to env file is enabled."`

```typescript
// 備用模式下的行為
try {
  await vaultService.set('KEY', 'value');
} catch (error) {
  // Error: Cannot set value when fallback to env file is enabled.
  console.log('Vault 備用模式不支援寫入操作');
}
```
