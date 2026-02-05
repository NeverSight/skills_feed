---
name: logistics-adapters
description: |
  Taiwan logistics integration (台灣物流整合). Use when working with CTC (中華宅配/宅配通), T-CAT (黑貓宅急便), or Taiwan delivery services. Covers package tracking (貨件追蹤), shipment creation (建立託運單), delivery status (配送狀態), and batch operations (批次追蹤). Keywords: 物流, 宅配, 貨運, 出貨, 寄送, logistics, shipping, delivery, tracking, CTC, TCAT, 黑貓, 中華宅配
---

# Taiwan Logistics Adapters (台灣物流適配器)

## Overview

`@rytass/logistics` 系列套件提供統一的台灣物流服務整合介面，支援包裹追蹤、訂單建立和狀態管理。

### 套件清單

| 套件 | 說明 | 功能 |
|------|------|------|
| `@rytass/logistics` | 基礎介面 | 定義統一的物流服務介面 |
| `@rytass/logistics-adapter-tcat` | 黑貓宅急便 | 包裹追蹤（HTML 爬蟲） |
| `@rytass/logistics-adapter-ctc` | 中華宅配 | 包裹追蹤 + 訂單管理（REST API） |

## Quick Start

### 安裝

```bash
# 黑貓宅急便
npm install @rytass/logistics-adapter-tcat

# 中華宅配
npm install @rytass/logistics-adapter-ctc
```

### 黑貓宅急便追蹤

```typescript
import { TCatLogisticsService, TCatLogistics } from '@rytass/logistics-adapter-tcat';

const logistics = new TCatLogisticsService(TCatLogistics);

// 追蹤單一包裹
const [result] = await logistics.trace('800978442950');
console.log(result.statusHistory);
// [{ date: '2024-01-15 14:30', status: 'DELIVERED', businessPremise: '台北營業所' }]

// 批量追蹤
const results = await logistics.trace(['800978442950', '903404283301']);
```

### 中華宅配追蹤與建單

> **⚠️ 安全警告**：預設的 `CtcLogistics` 配置包含測試用的 API Token，**請勿用於生產環境**。務必使用您自己的 API Token。

```typescript
import { CtcLogisticsService, CtcLogistics } from '@rytass/logistics-adapter-ctc';

// 使用預設設定（必須替換 apiToken）
const logistics = new CtcLogisticsService({
  ...CtcLogistics,
  apiToken: process.env.CTC_API_TOKEN!, // ⚠️ 必須替換為您的 API Token
});

// 追蹤包裹
const [result] = await logistics.trace('TRACKING-001');

// 建立託運單
const order = await logistics.create({
  senderCompany: '寄件公司',
  senderAddress: '台北市中正區重慶南路一段122號',
  senderMobile: '0912345678',
  receiverCompany: '收件公司',
  receiverContactName: '收件人',
  receiverAddress: '台北市信義區信義路五段7號',
  receiverMobile: '0987654321',
  paidCode: '客戶宅配',
});

console.log(order.shippingNumber); // 託運單號
console.log(order.trackingNumber); // 查件單號

// 更新託運單（需指定 trackingNumber）
const updatedOrder = await logistics.update({
  trackingNumber: 'TRACKING-001', // 必填：查件單號
  senderCompany: '新寄件公司',
  senderAddress: '台北市中正區重慶南路一段122號',
  senderMobile: '0912345678',
  receiverCompany: '新收件公司',
  receiverContactName: '新收件人',
  receiverAddress: '台北市信義區信義路五段7號',
  receiverMobile: '0987654321',
  paidCode: '客戶宅配',
});
```

### CTC 建單/更新選項

```typescript
interface CreateOrUpdateCtcLogisticsOptions {
  // 基本資訊
  trackingNumber?: string;        // 查件單號（create 時可選，update 時必填）
  customerDepartmentId?: number;  // 客戶部門 ID
  customerDepartmentUnitId?: number; // 客戶部門單位 ID

  // 寄件人資訊
  senderCompany: string;          // 寄件人公司名稱（必填）
  senderContactName?: string;     // 寄件人聯絡人（預設同 senderCompany）
  senderAddress: string;          // 寄件人地址（必填）
  senderTel?: string;             // 寄件人市話（與 senderMobile 二擇一）
  senderMobile?: string;          // 寄件人手機（與 senderTel 二擇一）
  senderRemark?: string;          // 寄件人備註

  // 收件人資訊
  receiverCompany: string;        // 收件人公司名稱（必填）
  receiverContactName: string;    // 收件人聯絡人（必填）
  receiverAddress: string;        // 收件人地址（必填）
  receiverTel?: string;           // 收件人市話（與 receiverMobile 二擇一）
  receiverMobile?: string;        // 收件人手機（與 receiverTel 二擇一）
  receiverRemark?: string;        // 收件人備註

  // 運送資訊
  paidCode: string;                // 付款代碼（必填）
  shipmentContent?: string;       // 貨物內容（預設 '貨件'）
  transportation?: string;        // 運輸工具（預設 'truck'）
  shippingMethod?: string;        // 運送方式（預設 'land'）
  payer?: string;                 // 費用支付方（預設 'receiver'）
  shippingTime?: string;          // 送件時效（預設 'regular'）
  paymentMethod?: string;         // 結算方式（預設 'monthly'）
  quantity?: number;              // 件數（預設 1）
  weight?: number;                // 重量（預設 1）
  volume?: number;                // 材積（預設 1）
}

// 回傳結果
interface CtcLogisticsDto {
  trackingNumber?: string;  // 查件單號
  shippingNumber: string;   // 託運單號
}
```

## Core Concepts

### 統一介面 LogisticsService

所有適配器都實現 `LogisticsService` 介面：

```typescript
// 基礎物流介面
interface LogisticsInterface<T = LogisticsBaseStatus> {
  reference?: T;
  url: string;
}

// LogisticsService 介面（泛型約束較複雜）
interface LogisticsService<LogisticsType extends LogisticsInterface<LogisticsStatus<LogisticsType>>> {
  trace(request: string): Promise<LogisticsTraceResponse<LogisticsType>[]>;
  trace(request: string[]): Promise<LogisticsTraceResponse<LogisticsType>[]>;
}
```

### 追蹤結果結構

```typescript
// 泛型約束較複雜，簡化理解：K 代表物流介面類型
interface LogisticsTraceResponse<K extends LogisticsInterface<LogisticsStatus<K>>> {
  logisticsId: string;                          // 追蹤號碼
  statusHistory: LogisticsStatusHistory<K['reference']>[];  // 狀態歷史
}

interface LogisticsStatusHistory<T> {
  date: string;    // 時間
  status: T;       // 狀態代碼（字串）
}

// T-CAT 擴展（包含營業所資訊）
interface TCatLogisticsStatusHistory<T> extends LogisticsStatusHistory<T> {
  businessPremise: string;  // 營業所名稱
}

// CTC 擴展（包含狀態碼）
interface CtcLogisticsStatusHistory<T> extends LogisticsStatusHistory<T> {
  statusCode: CtcLogisticsStatusEnum;  // 狀態碼（數字）
}

// CTC 狀態碼枚舉
enum CtcLogisticsStatusEnum {
  CREATED = 10,              // 新單
  PICKUP_EXCEPTION = 29,     // 取件異常
  PICKED_UP = 30,            // 已取件
  PICKUP_ARRIVED_AT_HUB = 40, // 取件到站
  IN_TRANSIT = 50,           // 轉運中
  TRANSIT_ARRIVED_AT_HUB = 60, // 轉運到站
  SHELVED = 65,              // 回站保管
  DELIVERING = 70,           // 配送中
  DELIVERY_EXCEPTION = 75,   // 配送異常
  DELIVERED = 80,            // 配送完成
  EMPTY_TRIP = 87,           // 空趟
  COMPLETED = 88,            // 正常結案
  NOTIFICATION_SENT = 91,    // 通知完成
  CANCELLED = 99,            // 取消
}
```

### 基本狀態類型

```typescript
type LogisticsBaseStatus = 'DELIVERED' | 'DELIVERING' | 'SHELVED';

// 完整的 T-CAT 狀態類型（Union Type）
type TCatLogisticsStatus =
  | 'DELIVERED'
  | 'TRANSPORTING'
  | 'DELIVERING'
  | 'COLLECTING'
  | 'CONSOLIDATED'
  | 'PICKUP_CANCELED'
  | 'SHELVED'
  | 'INVESTIGATING'
  | 'DELIVERING_TODAY'
  | 'FAIL_PICKUP'
  | 'AWAY_HOME'
  | LogisticsBaseStatus;

// 完整的 CTC 狀態類型（Union Type）
type CtcLogisticsStatus =
  | 'CREATED'
  | 'PICKUP_EXCEPTION'
  | 'PICKED_UP'
  | 'PICKUP_ARRIVED_AT_HUB'
  | 'IN_TRANSIT'
  | 'TRANSIT_ARRIVED_AT_HUB'
  | 'SHELVED'
  | 'DELIVERING'
  | 'DELIVERY_EXCEPTION'
  | 'DELIVERED'
  | 'EMPTY_TRIP'
  | 'COMPLETED'
  | 'NOTIFICATION_SENT'
  | 'CANCELLED';
```

### 額外導出類型

```typescript
// 錯誤介面
interface LogisticsErrorInterface {
  readonly code: string;
  readonly message?: string;
}

// T-CAT 物流介面（可自訂 statusMap）
interface TCatLogisticsInterface<T> extends LogisticsInterface<T> {
  ignoreNotFound: boolean;
  statusMap: (html: string, id: string) => LogisticsStatusHistory<T>[];
}

// CTC 物流介面
interface CtcLogisticsInterface<T> extends LogisticsInterface<T> {
  apiToken: string;
  ignoreNotFound?: boolean;
}

// CTC 狀態對照表常數（可用於自訂映射）
const CtcLogisticsStatusMap: { [key: string]: CtcLogisticsStatus };

// CTC API 回應（內部使用，但有導出）
interface CreateOrUpdateCtcLogisticsResponse {
  success: boolean;
  error: string;
  shipping_number: string;
  tracking_number?: string;
}
```

## Common Patterns

### T-CAT 狀態對照表

| 狀態 | 中文原文 | 說明 |
|------|---------|------|
| `DELIVERED` | 順利送達 | 包裹已成功送達 |
| `TRANSPORTING` | 轉運中 | 包裹在轉運途中 |
| `DELIVERING` | 配送中 | 配送員正在派送 |
| `COLLECTING` | 取件中 | 正在取件 |
| `CONSOLIDATED` | 已集貨 | 已完成集貨 |
| `PICKUP_CANCELED` | 取消取件 | 取件已取消 |
| `SHELVED` | 暫置營業所 | 暫存於營業所 |
| `INVESTIGATING` | 調查處理中 | 正在調查處理 |
| `DELIVERING_TODAY` | 配送中(當配下車) (當配上車) | 當日配送中 |
| `FAIL_PICKUP` | 未順利取件，請洽客服中心 | 取件失敗 |
| `AWAY_HOME` | 不在家.公司行號休息 | 收件人不在 |

### CTC 狀態對照表

| 狀態 | 狀態碼 | 說明 |
|------|--------|------|
| `CREATED` | 10 | 新單 |
| `PICKUP_EXCEPTION` | 29 | 取件異常 |
| `PICKED_UP` | 30 | 已取件 |
| `PICKUP_ARRIVED_AT_HUB` | 40 | 取件到站 |
| `IN_TRANSIT` | 50 | 轉運中 |
| `TRANSIT_ARRIVED_AT_HUB` | 60 | 轉運到站 |
| `SHELVED` | 65 | 回站保管 |
| `DELIVERING` | 70 | 配送中 |
| `DELIVERY_EXCEPTION` | 75 | 配送異常 |
| `DELIVERED` | 80 | 配送完成 |
| `EMPTY_TRIP` | 87 | 空趟 |
| `COMPLETED` | 88 | 正常結案 |
| `NOTIFICATION_SENT` | 91 | 通知完成 |
| `CANCELLED` | 99 | 取消 |

### 錯誤處理

```typescript
import { LogisticsError, ErrorCode } from '@rytass/logistics';

// ErrorCode 枚舉
enum ErrorCode {
  NOT_IMPLEMENTED = '999',   // 未實作
  NOT_FOUND_ERROR = '101',   // 找不到包裹
  PERMISSION_DENIED = '102', // 無權查詢
  INVALID_PARAMETER = '103', // 無效參數
}

try {
  const result = await logistics.trace('INVALID');
} catch (error) {
  if (error instanceof LogisticsError) {
    switch (error.code) {
      case ErrorCode.NOT_FOUND_ERROR:
        console.error('找不到此包裹');
        break;
      case ErrorCode.PERMISSION_DENIED:
        console.error('無權查詢');
        break;
      case ErrorCode.INVALID_PARAMETER:
        console.error('無效的追蹤號碼');
        break;
      case ErrorCode.NOT_IMPLEMENTED:
        console.error('功能未實作');
        break;
    }
  }
}
```

### 忽略找不到錯誤

```typescript
// T-CAT 預設 ignoreNotFound: false
const tcatLogistics = new TCatLogisticsService({
  ...TCatLogistics,  // 預設 ignoreNotFound: false
  ignoreNotFound: true,  // 找不到時返回空歷史而非拋出錯誤
});

// CTC 預設 ignoreNotFound: true
const ctcLogistics = new CtcLogisticsService({
  ...CtcLogistics,  // 預設 ignoreNotFound: true
  apiToken: 'your-token',
  ignoreNotFound: false,  // 改為找不到時拋出錯誤
});
```

## API Reference

詳細 API 文件請參閱 [reference.md](reference.md)。

## Troubleshooting

### T-CAT 追蹤失敗

T-CAT 使用 HTML 爬蟲，可能因網站改版而失效。檢查：
1. 網站是否可正常訪問
2. HTML 結構是否變更
3. 考慮使用自訂 `statusMap` 函數

### CTC API 認證失敗

1. 確認 `apiToken` 正確
2. 檢查 API 端點 URL
3. 確認帳戶有對應權限

### 批量追蹤效能

批量追蹤使用 `Promise.all`，注意：
- 避免一次追蹤過多包裹
- 考慮分批處理大量請求
- 設置適當的超時時間
