---
name: invoice-adapters
description: Taiwan e-invoice integration (台灣電子發票整合). Use when working with ECPay (綠界), EZPay (藍新), BankPro (金財通), or Amego (光貿) invoice services. Covers issuing invoices (開立發票), voiding (作廢), allowances (折讓), and querying invoice data.
---

# Taiwan E-Invoice Adapters

This skill provides guidance for using `@rytass/invoice-adapter-*` packages to integrate Taiwan e-invoice services.

## Overview

All adapters implement the `InvoiceGateway` interface from `@rytass/invoice`, providing a unified API across different providers:

| Package | Provider | Description |
|---------|----------|-------------|
| `@rytass/invoice-adapter-ecpay` | ECPay (綠界科技) | Most popular Taiwan payment gateway |
| `@rytass/invoice-adapter-ezpay` | EZPay (藍新科技) | Also known as NewebPay |
| `@rytass/invoice-adapter-bank-pro` | BankPro (金財通) | Bank-integrated invoice service |
| `@rytass/invoice-adapter-amego` | Amego (光貿) | Enterprise invoice platform |

## Installation

```bash
# Choose the adapter for your provider
npm install @rytass/invoice-adapter-ecpay
npm install @rytass/invoice-adapter-ezpay
npm install @rytass/invoice-adapter-bank-pro
npm install @rytass/invoice-adapter-amego
```

## Quick Start

### ECPay

```typescript
import { ECPayInvoiceGateway } from '@rytass/invoice-adapter-ecpay';
import { TaxType, InvoiceCarriers } from '@rytass/invoice';

const gateway = new ECPayInvoiceGateway({
  merchantId: 'YOUR_MERCHANT_ID',
  aesKey: 'YOUR_AES_KEY',
  aesIv: 'YOUR_AES_IV',
  // 可選: 跳過手機條碼/愛心碼驗證
  // skipMobileBarcodeValidation: true,
  // skipLoveCodeValidation: true,
});

// Issue an invoice
const invoice = await gateway.issue({
  orderId: 'ORDER001',  // alphanumeric only, max 30 chars
  customer: {
    email: 'customer@example.com',  // must provide email or mobile
  },
  carrier: InvoiceCarriers.MOBILE('/ABC+123'),
  items: [
    { name: 'Product A', quantity: 2, unitPrice: 100, unit: 'pcs' },
  ],
});

console.log(invoice.invoiceNumber); // e.g., "AB12345678"
```

### EZPay

```typescript
import { EZPayInvoiceGateway } from '@rytass/invoice-adapter-ezpay';
import { TaxType, InvoiceCarrierType } from '@rytass/invoice';

const gateway = new EZPayInvoiceGateway({
  merchantId: 'YOUR_MERCHANT_ID',
  hashKey: 'YOUR_HASH_KEY',
  hashIv: 'YOUR_HASH_IV',
});

// Issue a B2C invoice
const invoice = await gateway.issue({
  orderId: 'ORDER_001',  // alphanumeric + underscore, max 20 chars
  buyerName: '測試買家',  // required, max 30 chars for B2C
  carrier: { type: InvoiceCarrierType.MOBILE, code: '/ABC+123' },
  items: [
    { name: 'Product A', quantity: 2, unitPrice: 100, unit: 'pcs' },
  ],
});
```

### BankPro

```typescript
import { BankProInvoiceGateway } from '@rytass/invoice-adapter-bank-pro';

const gateway = new BankProInvoiceGateway({
  user: 'YOUR_USER',
  password: 'YOUR_PASSWORD',
  systemOID: 12345,
  sellerBAN: '12345678',
});

// Issue an invoice
const invoice = await gateway.issue({
  orderId: 'ORDER-001',
  buyerEmail: 'customer@example.com',
  items: [
    { name: 'Product A', quantity: 2, unitPrice: 100, unit: 'pcs' },
  ],
});
```

### Amego

```typescript
import { AmegoInvoiceGateway, AMEGO_CONSTANTS } from '@rytass/invoice-adapter-amego';

const gateway = new AmegoInvoiceGateway({
  appKey: 'YOUR_APP_KEY',
  vatNumber: '12345678', // 賣方統一編號（必填）
});

// Issue a B2C invoice (消費者發票)
// 注意: Amego 的 taxType 和 detailVat 為必填，item 的 taxType 也是必填
import { TaxType } from '@rytass/invoice';

const b2cInvoice = await gateway.issue({
  orderId: 'ORDER-001',
  taxType: TaxType.TAXED,  // 必填: 課稅別
  detailVat: true,          // 必填: 單價含稅
  items: [
    {
      name: 'Product A',
      quantity: 2,
      unitPrice: 100,
      unit: 'pcs',
      taxType: TaxType.TAXED,  // 必填: 商品課稅別
    },
  ],
  // vatNumber 不填則為 B2C 發票（預設 '0000000000'）
});

// Issue a B2B invoice (公司發票)
const b2bInvoice = await gateway.issue({
  orderId: 'ORDER-002',
  taxType: TaxType.TAXED,  // 必填
  detailVat: true,         // 必填: 明細單價類型: true=含稅, false=未稅
  items: [
    {
      name: 'Product A',
      quantity: 2,
      unitPrice: 100,
      unit: 'pcs',
      taxType: TaxType.TAXED,  // 必填
    },
  ],
  vatNumber: '55880710',   // 買方統一編號
  buyerName: '買方公司名稱',
  taxRate: 0.05,           // 稅率，預設 5%
});

// Invoice 物件包含 taxRate 和 vatNumber
console.log(b2bInvoice.vatNumber); // '55880710'
console.log(b2bInvoice.taxRate);   // 0.05
```

**AMEGO_CONSTANTS 常數：**

```typescript
import { AMEGO_CONSTANTS } from '@rytass/invoice-adapter-amego';

// 欄位長度限制
AMEGO_CONSTANTS.MAX_ORDER_ID_LENGTH;    // 40 字元
AMEGO_CONSTANTS.MAX_ITEM_NAME_LENGTH;   // 256 字元
AMEGO_CONSTANTS.MAX_ITEM_UNIT_LENGTH;   // 6 字元
AMEGO_CONSTANTS.MAX_ITEM_REMARK_LENGTH; // 40 字元

// 預設值
AMEGO_CONSTANTS.DEFAULT_TAX_RATE;       // 0.05 (5%)
AMEGO_CONSTANTS.LOVE_CODE_MIN_LENGTH;   // 3
AMEGO_CONSTANTS.LOVE_CODE_MAX_LENGTH;   // 7
```

## Common Operations

### Void an Invoice

> **注意:** 各 adapter 的 void 參數不同：
> - ECPay/EZPay: 需要 `reason` 參數
> - BankPro: options 為可選，只有 `sellerCode` 參數
> - Amego: 完全不需要 options 參數

```typescript
// ECPay / EZPay
const voidedInvoice = await gateway.void(invoice, {
  reason: 'Customer requested cancellation',
});

// BankPro
const voidedInvoice = await gateway.void(invoice);
// 或
const voidedInvoice = await gateway.void(invoice, { sellerCode: 'SELLER01' });

// Amego
const voidedInvoice = await gateway.void(invoice);
```

### Create an Allowance (Partial Refund)

```typescript
const updatedInvoice = await gateway.allowance(invoice, [
  { name: 'Product A', quantity: 1, unitPrice: 100, unit: 'pcs' },
]);
```

### Query an Invoice

```typescript
// By order ID (ECPay, BankPro, Amego)
const invoice = await gateway.query({ orderId: 'ORDER-001' });

// By invoice number (ECPay requires issuedOn date)
const invoice = await gateway.query({
  invoiceNumber: 'AB12345678',
  issuedOn: new Date('2024-01-15'),
});

// EZPay: By order ID (需要 amount 參數)
const ezpayInvoice = await ezpayGateway.query({
  orderId: 'ORDER-001',
  amount: 1000,  // 發票金額（必填）
});

// EZPay: By invoice number
const ezpayInvoice = await ezpayGateway.query({
  invoiceNumber: 'AB12345678',
  randomCode: '1234',  // 隨機碼（必填）
});

// Amego: By invoice number
const amegoInvoice = await amegoGateway.query({
  invoiceNumber: 'AB12345678',
});
```

### Validate Carrier Codes

```typescript
// Check mobile barcode validity
const isValid = await gateway.isMobileBarcodeValid('/ABC1234');

// Check love code validity
const isValid = await gateway.isLoveCodeValid('168001');
```

### ECPay: List Invoices (分頁查詢)

```typescript
import { ECPayInvoiceGateway, ECPayInvoiceListQueryOptions } from '@rytass/invoice-adapter-ecpay';

// 列出指定日期範圍內的發票
const invoices = await gateway.list({
  startDate: '2024-01-01', // YYYY-MM-DD
  endDate: '2024-01-31',   // YYYY-MM-DD
  onlyAward: false,        // 只查詢中獎發票
  onlyInvalid: false,      // 只查詢作廢發票
});

// 自動分頁取得所有發票（每頁 200 筆）
console.log(`Found ${invoices.length} invoices`);
```

### ECPay: Validate GUI (驗證統一編號)

```typescript
import { ECPayInvoiceGateway } from '@rytass/invoice-adapter-ecpay';

// 驗證統一編號並取得公司名稱
const result = await gateway.isValidGUI('12345678');

if (result[0]) {
  // [true, 'Company Name']
  console.log(`Valid GUI, Company: ${result[1]}`);
} else {
  // [false]
  console.log('Invalid GUI');
}

// 注意：此功能為輔助驗證，無法涵蓋所有公司/組織
```

## Feature Comparison

| Feature                      | ECPay | EZPay | BankPro | Amego |
|------------------------------|:-----:|:-----:|:-------:|:-----:|
| Issue Invoice                | Yes   | Yes   | Yes     | Yes   |
| Void Invoice                 | Yes   | Yes   | Yes     | Yes   |
| Allowance                    | Yes   | Yes   | Yes     | Yes   |
| Invalid Allowance            | Yes   | Yes   | Yes     | Yes   |
| Query Invoice                | Yes   | Yes   | Yes     | Yes   |
| List Invoices                | Yes   | No    | No      | No    |
| Mobile Barcode Validation    | Yes   | Yes   | No      | Yes   |
| Love Code Validation         | Yes   | Yes   | No      | No    |
| GUI (VAT Number) Validation  | Yes   | No    | No      | No    |
| B2B Invoice                  | Yes   | Yes   | Yes     | Yes   |
| B2C Invoice                  | Yes   | Yes   | Yes     | Yes   |
| Print Carrier                | Yes   | Yes   | Yes     | No    |
| Mobile Carrier               | Yes   | Yes   | No      | Yes   |
| MOICA Carrier                | Yes   | Yes   | No      | Yes   |
| Love Code Donation           | Yes   | Yes   | No      | Yes   |
| Platform Carrier             | No    | Yes   | No      | Yes   |

## Error Handling

### EZPay Error Codes

EZPay 提供詳細的錯誤碼枚舉，可用於錯誤處理：

```typescript
import { ErrorCode } from '@rytass/invoice-adapter-ezpay';

// 常見錯誤碼
ErrorCode.KEY10002  // '資料解密錯誤'
ErrorCode.KEY10004  // '資料不齊全'
ErrorCode.KEY10006  // '商店未申請啟用電子發票'
ErrorCode.INV10003  // '商品資訊格式錯誤或缺少資料'
ErrorCode.INV10013  // '發票欄位資料不齊全或格式錯誤'
ErrorCode.INV20006  // '查無發票資料'
ErrorCode.LIB10003  // '商店自訂編號重覆'
ErrorCode.LIB10005  // '發票已作廢過'
ErrorCode.INV90006  // '可開立張數已用罄'
```

<details>
<summary>完整 EZPay ErrorCode 列表</summary>

| Code       | 說明                                      |
|------------|-------------------------------------------|
| KEY10002   | 資料解密錯誤                              |
| KEY10004   | 資料不齊全                                |
| KEY10006   | 商店未申請啟用電子發票                    |
| KEY10007   | 頁面停留超過 30 分鐘                      |
| KEY10010   | 商店代號空白                              |
| KEY10011   | PostData_欄位空白                         |
| KEY10012   | 資料傳遞錯誤                              |
| KEY10013   | 資料空白                                  |
| KEY10014   | TimeOut                                   |
| KEY10015   | 發票金額格式錯誤                          |
| INV10003   | 商品資訊格式錯誤或缺少資料                |
| INV10004   | 商品資訊的商品小計計算錯誤                |
| INV10006   | 稅率格式錯誤                              |
| INV10012   | 發票金額、課稅別驗證錯誤                  |
| INV10013   | 發票欄位資料不齊全或格式錯誤              |
| INV10014   | 自訂編號格式錯誤                          |
| INV10015   | 無未稅金額                                |
| INV10016   | 無稅金                                    |
| INV10017   | 輸入的版本不支援混合稅率功能              |
| INV10019   | 資料含有控制碼                            |
| INV10020   | 暫停使用                                  |
| INV10021   | 異常終止                                  |
| INV70001   | 欄位資料格式錯誤                          |
| INV70002   | 上傳失敗之發票不得作廢                    |
| INV90005   | 未簽定合約或合約已到期                    |
| INV90006   | 可開立張數已用罄                          |
| NOR10001   | 網路連線異常                              |
| LIB10003   | 商店自訂編號重覆                          |
| LIB10005   | 發票已作廢過                              |
| LIB10007   | 無法作廢                                  |
| LIB10008   | 超過可作廢期限                            |
| LIB10009   | 發票已開立，但未上傳至財政部，無法作廢    |
| IAI10001   | 缺少參數 作廢折讓錯誤代碼                 |
| IAI10002   | 查詢失敗 作廢折讓錯誤代碼                 |
| IAI10003   | 更新失敗 作廢折讓錯誤代碼                 |
| IAI10004   | 參數錯誤 作廢折讓錯誤代碼                 |
| IAI10005   | 新增失敗 作廢折讓錯誤代碼                 |
| IAI10006   | 異常終止                                  |
| API10001   | 缺少參數                                  |
| API10002   | 查詢失敗                                  |
| API10004   | 參數錯誤                                  |
| CBC10001   | 欄位資料空白                              |
| CBC10002   | 欄位資料格式錯誤                          |
| CBC10003   | 異常終止                                  |
| CBC10004   | 財政部大平台網路連線異常                  |

</details>

### BankPro Invoice Status

BankPro 提供發票狀態枚舉：

```typescript
import { BankProInvoiceStatus } from '@rytass/invoice-adapter-bank-pro';

// 發票狀態
BankProInvoiceStatus.CREATE            // '0' - 新增
BankProInvoiceStatus.UPDATE            // '1' - 更新
BankProInvoiceStatus.DELETE            // '2' - 作廢
BankProInvoiceStatus.ALLOWANCE         // '3' - 折讓
BankProInvoiceStatus.INVALID_ALLOWANCE // '4' - 作廢折讓
```

## Additional Types

### Amego Types

```typescript
import {
  AmegoTaxType,
  ReverseAmegoTaxType,
  AmegoAllowanceType,
} from '@rytass/invoice-adapter-amego';
import { TaxType } from '@rytass/invoice';

// TaxType 轉 Amego API 值
AmegoTaxType[TaxType.TAXED];     // '1'
AmegoTaxType[TaxType.ZERO_TAX];  // '2'
AmegoTaxType[TaxType.TAX_FREE];  // '3'
AmegoTaxType[TaxType.SPECIAL];   // '4'
AmegoTaxType[TaxType.MIXED];     // '9'

// Amego API 值轉回 TaxType
ReverseAmegoTaxType[1];  // TaxType.TAXED
ReverseAmegoTaxType[2];  // TaxType.ZERO_TAX
ReverseAmegoTaxType[3];  // TaxType.TAX_FREE

// 折讓類型
AmegoAllowanceType.BUYER_ISSUED   // 1 - 買方開立
AmegoAllowanceType.SELLER_ISSUED  // 2 - 賣方開立
```

### EZPay Types

```typescript
import {
  EZPayInvoiceIssueStatus,
  EZPayTaxTypeCode,
} from '@rytass/invoice-adapter-ezpay';
import { TaxType } from '@rytass/invoice';

// 發票開立狀態
EZPayInvoiceIssueStatus.INSTANT  // '1' - 即時開立
EZPayInvoiceIssueStatus.WAITING  // '0' - 等待開立
EZPayInvoiceIssueStatus.DELAY    // '3' - 延遲開立

// TaxType 轉 EZPay API 值
EZPayTaxTypeCode[TaxType.TAXED];     // '1'
EZPayTaxTypeCode[TaxType.ZERO_TAX];  // '2'
EZPayTaxTypeCode[TaxType.TAX_FREE];  // '3'
EZPayTaxTypeCode[TaxType.MIXED];     // '9'
```

### BankPro Types

```typescript
import { BankProRateType } from '@rytass/invoice-adapter-bank-pro';
import { TaxType } from '@rytass/invoice';

// TaxType 轉 BankPro API 值
BankProRateType[TaxType.TAXED];     // '1'
BankProRateType[TaxType.ZERO_TAX];  // '2'
BankProRateType[TaxType.TAX_FREE];  // '3'
```

## Environment Configuration

All adapters support development and production environments:

```typescript
// ECPay
import { ECPayInvoiceGateway } from '@rytass/invoice-adapter-ecpay';
const gateway = new ECPayInvoiceGateway(); // Development by default
const prodGateway = new ECPayInvoiceGateway({
  baseUrl: 'https://einvoice.ecpay.com.tw',
  // ... credentials
});

// EZPay
import { EZPayInvoiceGateway, EZPayBaseUrls } from '@rytass/invoice-adapter-ezpay';
const gateway = new EZPayInvoiceGateway({
  baseUrl: EZPayBaseUrls.PRODUCTION,
  // ... credentials
});

// BankPro
import { BankProInvoiceGateway, BankProBaseUrls } from '@rytass/invoice-adapter-bank-pro';
const gateway = new BankProInvoiceGateway({
  baseUrl: BankProBaseUrls.PRODUCTION,
  // ... credentials
});

// Amego
import { AmegoInvoiceGateway, AmegoBaseUrls } from '@rytass/invoice-adapter-amego';
const gateway = new AmegoInvoiceGateway({
  baseUrl: AmegoBaseUrls.PRODUCTION,
  // ... credentials
});
```

## Detailed Documentation

For complete API reference including all methods, types, and advanced usage:

- [ECPay Adapter Reference](ECPAY.md)
- [EZPay Adapter Reference](EZPAY.md)
- [BankPro Adapter Reference](BANK-PRO.md)
- [Amego Adapter Reference](AMEGO.md)
