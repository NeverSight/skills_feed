---
name: logistics-development
description: |
  Development guide for @rytass/logistics base package (物流基底套件開發指南). Use when creating new logistics adapters (新增物流 adapter), understanding base interfaces, or extending logistics functionality. Covers LogisticsService, LogisticsInterface, error handling patterns for Taiwan logistics providers. Keywords: logistics adapter, 物流 adapter, 開發指南, CTC, TCAT, 宅配, shipping, delivery
---

# Logistics Adapter Development Guide (物流 Adapter 開發指南)

## Overview

本指南說明如何基於 `@rytass/logistics` 基礎套件開發新的物流服務適配器。

## Base Package Architecture

```
@rytass/logistics (Base)
├── LogisticsService<T>      # 核心服務介面
├── LogisticsInterface<T>    # 配置介面
├── LogisticsBaseStatus      # 基礎狀態類型 ('DELIVERED' | 'DELIVERING' | 'SHELVED')
├── LogisticsStatus<T>       # 泛型狀態類型
├── LogisticsTraceResponse   # 追蹤結果
├── LogisticsStatusHistory   # 狀態歷史
├── LogisticsErrorInterface  # 錯誤介面
├── LogisticsError          # 統一錯誤類別
└── ErrorCode               # 錯誤代碼列舉
```

## Core Interfaces

### LogisticsService

```typescript
interface LogisticsService<T extends LogisticsInterface<LogisticsStatus<T>>> {
  trace(request: string): Promise<LogisticsTraceResponse<T>[]>;
  trace(request: string[]): Promise<LogisticsTraceResponse<T>[]>;
}
```

### LogisticsInterface

```typescript
interface LogisticsInterface<T = LogisticsBaseStatus> {
  reference?: T;
  url: string;
}

type LogisticsBaseStatus = 'DELIVERED' | 'DELIVERING' | 'SHELVED';
```

### Response Types

```typescript
interface LogisticsTraceResponse<K extends LogisticsInterface<LogisticsStatus<K>>> {
  logisticsId: string;
  statusHistory: LogisticsStatusHistory<K['reference']>[];
}

interface LogisticsStatusHistory<T> {
  date: string;
  status: T;
}

interface LogisticsErrorInterface {
  readonly code: string;
  readonly message?: string;
}
```

## Implementing a New Adapter

### Step 1: Define Status Types

```typescript
// my-logistics-adapter/src/typings.ts
export type MyLogisticsStatus =
  | 'DELIVERED'
  | 'DELIVERING'
  | 'SHELVED'
  | 'PENDING'
  | 'CANCELLED';

export interface MyLogisticsInterface<T> extends LogisticsInterface<T> {
  apiKey: string;
  apiSecret: string;
  ignoreNotFound?: boolean;
}
```

### Step 2: Create Status Map

```typescript
// my-logistics-adapter/src/constants.ts
export const MyLogisticsStatusMap: Record<string, MyLogisticsStatus> = {
  '已送達': 'DELIVERED',
  '配送中': 'DELIVERING',
  '待取': 'SHELVED',
  '待處理': 'PENDING',
  '已取消': 'CANCELLED',
};
```

### Step 3: Implement Service Class

```typescript
// my-logistics-adapter/src/my-logistics.service.ts
import { LogisticsService, LogisticsTraceResponse, LogisticsError, ErrorCode } from '@rytass/logistics';
import axios from 'axios';

export class MyLogisticsService<T extends MyLogisticsInterface<LogisticsStatus<T>>>
  implements LogisticsService<T> {

  constructor(private readonly configuration: T) {}

  async trace(logisticsIds: string | string[]): Promise<LogisticsTraceResponse<T>[]> {
    const ids = Array.isArray(logisticsIds) ? logisticsIds : [logisticsIds];

    return Promise.all(ids.map(id => this.getLogisticsStatus(id)));
  }

  private async getLogisticsStatus(trackingId: string): Promise<LogisticsTraceResponse<T>> {
    try {
      const response = await axios.get(`${this.configuration.url}/track/${trackingId}`, {
        headers: {
          'X-API-Key': this.configuration.apiKey,
          'X-API-Secret': this.configuration.apiSecret,
        },
      });

      if (!response.data.success) {
        if (this.configuration.ignoreNotFound) {
          return { logisticsId: trackingId, statusHistory: [] };
        }
        throw new LogisticsError(ErrorCode.NOT_FOUND_ERROR, `Tracking ${trackingId} not found`);
      }

      return {
        logisticsId: trackingId,
        statusHistory: this.mapStatusHistory(response.data.history),
      };
    } catch (error) {
      if (error instanceof LogisticsError) throw error;

      if (axios.isAxiosError(error)) {
        if (error.response?.status === 403) {
          throw new LogisticsError(ErrorCode.PERMISSION_DENIED, 'Invalid API credentials');
        }
        if (error.response?.status === 400) {
          throw new LogisticsError(ErrorCode.INVALID_PARAMETER, 'Invalid tracking number');
        }
      }

      throw new LogisticsError(ErrorCode.NOT_IMPLEMENTED, 'Unknown error');
    }
  }

  private mapStatusHistory(history: any[]): LogisticsStatusHistory<T['reference']>[] {
    return history.map(item => ({
      date: item.timestamp,
      status: MyLogisticsStatusMap[item.status] || 'DELIVERING',
    }));
  }
}
```

### Step 4: Export Default Configuration

```typescript
// my-logistics-adapter/src/index.ts
export * from './typings';
export * from './constants';
export * from './my-logistics.service';

export const MyLogistics: MyLogisticsInterface<MyLogisticsStatus> = {
  url: 'https://api.mylogistics.com/v1',
  apiKey: '',
  apiSecret: '',
  ignoreNotFound: false,
};
```

## Error Handling

### ErrorCode Reference

| Code | Constant | Usage |
|------|----------|-------|
| 999 | NOT_IMPLEMENTED | 未實現的功能 |
| 101 | NOT_FOUND_ERROR | 找不到追蹤號碼 |
| 102 | PERMISSION_DENIED | API 認證失敗 |
| 103 | INVALID_PARAMETER | 無效的參數 |

### Best Practices

```typescript
// 1. 使用統一的 LogisticsError
throw new LogisticsError(ErrorCode.NOT_FOUND_ERROR, 'Custom message');

// 2. 支援 ignoreNotFound 選項
if (this.configuration.ignoreNotFound) {
  return { logisticsId: id, statusHistory: [] };
}

// 3. 適當的 HTTP 錯誤映射
if (response.status === 403) {
  throw new LogisticsError(ErrorCode.PERMISSION_DENIED);
}
```

## Testing Guidelines

```typescript
// __tests__/my-logistics.spec.ts
import { MyLogisticsService, MyLogistics } from '../src';
import { LogisticsError, ErrorCode } from '@rytass/logistics';

describe('MyLogisticsService', () => {
  const service = new MyLogisticsService({
    ...MyLogistics,
    apiKey: 'test-key',
    apiSecret: 'test-secret',
  });

  it('should trace single package', async () => {
    const result = await service.trace('TRACK-001');
    expect(result).toHaveLength(1);
    expect(result[0].logisticsId).toBe('TRACK-001');
  });

  it('should trace multiple packages', async () => {
    const result = await service.trace(['TRACK-001', 'TRACK-002']);
    expect(result).toHaveLength(2);
  });

  it('should handle not found with ignoreNotFound', async () => {
    const serviceWithIgnore = new MyLogisticsService({
      ...MyLogistics,
      ignoreNotFound: true,
    });
    const result = await serviceWithIgnore.trace('INVALID');
    expect(result[0].statusHistory).toHaveLength(0);
  });
});
```

## Package Structure

```
my-logistics-adapter/
├── src/
│   ├── index.ts
│   ├── typings.ts
│   ├── constants.ts
│   └── my-logistics.service.ts
├── __tests__/
│   └── my-logistics.spec.ts
├── package.json
├── tsconfig.build.json
└── README.md
```

## Publishing Checklist

- [ ] 實現 `LogisticsService` 介面
- [ ] 定義完整的狀態類型
- [ ] 實現錯誤處理
- [ ] 支援批量追蹤
- [ ] 撰寫單元測試
- [ ] 更新 README
- [ ] 遵循 `@rytass/logistics-adapter-*` 命名規範
