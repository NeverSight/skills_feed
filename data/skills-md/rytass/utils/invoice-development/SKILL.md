---
name: invoice-development
description: Development guide for @rytass/invoice base package (發票基底套件開發指南). Use when creating new invoice adapters (新增發票 adapter), understanding base interfaces, or extending invoice functionality. Covers Invoice, InvoiceGateway, InvoiceAllowance interfaces and implementation patterns.
---

# Invoice Development Guide

This skill provides guidance for developers working with the `@rytass/invoice` base package, including creating new invoice adapters.

## Overview

The `@rytass/invoice` package defines the core interfaces and types that all invoice adapters must implement. It follows the adapter pattern to provide a unified API across different Taiwan e-invoice providers.

## Architecture

```
@rytass/invoice (Base Package)
    │
    ├── Invoice<Item>              # Invoice entity interface
    ├── InvoiceGateway<...>        # Gateway interface
    ├── InvoiceAllowance<Item>     # Allowance interface
    ├── Enums & Types              # Shared types
    └── Utility Functions          # Helpers

@rytass/invoice-adapter-*         # Provider implementations
    │
    ├── [Provider]InvoiceGateway   # Implements InvoiceGateway
    ├── [Provider]Invoice          # Implements Invoice
    └── [Provider]Allowance        # Implements InvoiceAllowance
```

## Installation

```bash
npm install @rytass/invoice
```

## Core Interfaces

### InvoiceGateway

The main interface that all adapters must implement:

```typescript
interface InvoiceGateway<
  Item extends PaymentItem = PaymentItem,
  I extends Invoice<Item> = Invoice<Item>,
  QueryOptions = unknown,
> {
  issue(options: InvoiceIssueOptions<Item>): Promise<I>;
  void(invoice: Invoice<PaymentItem>, options: InvoiceVoidOptions): Promise<Invoice<PaymentItem>>;
  allowance(invoice: Invoice<PaymentItem>, allowanceItems: InvoicePaymentItem[], options?: InvoiceAllowanceOptions): Promise<Invoice<PaymentItem>>;
  invalidAllowance(allowance: InvoiceAllowance<PaymentItem>): Promise<Invoice<PaymentItem>>;
  query(options: QueryOptions): Promise<I>;
  isMobileBarcodeValid(code: string): Promise<boolean>;
  isLoveCodeValid(code: string): Promise<boolean>;
}
```

### Invoice

The invoice entity interface:

```typescript
interface Invoice<Item extends PaymentItem> {
  readonly invoiceNumber: string;
  readonly issuedOn: Date;
  readonly allowances: InvoiceAllowance<PaymentItem>[];
  readonly issuedAmount: number;
  readonly randomCode: string;
  readonly items: Item[];
  state: InvoiceState;
  nowAmount: number;
  voidOn: Date | null;
  setVoid: () => void;
  awardType?: InvoiceAwardType;
}
```

### InvoiceAllowance

The allowance entity interface:

```typescript
interface InvoiceAllowance<Item extends PaymentItem> {
  readonly allowanceNumber: string;
  readonly allowancePrice: number;
  readonly allowancedOn: Date;
  readonly remainingAmount: number;
  readonly items: Item[];
  readonly parentInvoice: Invoice<Item>;
  status: InvoiceAllowanceState;
  invalidOn: Date | null;
  invalid: () => void;
}
```

## Quick Reference

### Supporting Types

```typescript
// Issue Options
interface InvoiceIssueOptions<Item extends PaymentItem = PaymentItem> {
  items: InvoicePaymentItem<Item>[];
  vatNumber?: string;
  carrier?: InvoiceCarrier;
  customsMark?: CustomsMark;
}

// Payment Item with Tax Type
type InvoicePaymentItem<Item extends PaymentItem = PaymentItem> = Item & {
  taxType?: Omit<TaxType, TaxType.MIXED>;
};

// Void Options
interface InvoiceVoidOptions {
  reason: string;
}

// Allowance Options
interface InvoiceAllowanceOptions {
  taxType?: Omit<TaxType, TaxType.MIXED | TaxType.SPECIAL>;
}

// Query Options
interface BaseInvoiceQueryOptions {
  orderId?: string;
  invoiceNumber?: string;
  [key: string]: unknown;
}
type InvoiceQueryOptions<T = BaseInvoiceQueryOptions> = T;

// Carrier Types (Union)
type InvoiceCarrier =
  | InvoicePrintCarrier
  | InvoiceMobileCarrier
  | InvoiceMoicaCarrier
  | InvoiceLoveCodeCarrier
  | InvoiceMemberCarrier
  | InvoicePlatformCarrier;

// Tax Types (Union)
type InvoiceTax = CommonTax | SpecialTax;

interface CommonTax {
  type: Exclude<TaxType, TaxType.SPECIAL>;
}

interface SpecialTax {
  type: TaxType.SPECIAL;
  taxCode: SpecialTaxCode;
}
```

### Enums

| Enum | Values |
|------|--------|
| `TaxType` | TAXED, TAX_FREE, ZERO_TAX, SPECIAL, MIXED |
| `InvoiceState` | INITED, ISSUED, VOID, ALLOWANCED |
| `InvoiceAllowanceState` | INITED, ISSUED, INVALID |
| `InvoiceCarrierType` | PRINT, MOBILE, MOICA, LOVE_CODE, MEMBER, PLATFORM |
| `CustomsMark` | YES, NO |
| `SpecialTaxCode` | TEA, CLUB, BANK_SELF, INSURANCE, BANK_COMMON, BANK_SELF_SALES_BEFORE_103, BANK_SELF_SALES_AFTER_103, FREE |
| `InvoiceAwardType` | TWO_HUNDRED, FIVE_HUNDRED, EIGHT_HUNDRED, ONE_THOUSAND, FOUR_THOUSAND, TEN_THOUSAND, FORTY_THOUSAND, TWO_HUNDRED_THOUSAND, ONE_MILLION, TWO_MILLION, TEN_MILLION, CLOUD_TWO_THOUSAND |

### InvoiceAwardType (發票中獎類型)

```typescript
import { InvoiceAwardType } from '@rytass/invoice';

enum InvoiceAwardType {
  TWO_HUNDRED = 6,          // 200 元
  FIVE_HUNDRED = 11,        // 500 元
  EIGHT_HUNDRED = 12,       // 800 元
  ONE_THOUSAND = 5,         // 1,000 元
  FOUR_THOUSAND = 4,        // 4,000 元
  TEN_THOUSAND = 3,         // 10,000 元
  FORTY_THOUSAND = 2,       // 40,000 元
  TWO_HUNDRED_THOUSAND = 1, // 200,000 元
  ONE_MILLION = 10,         // 1,000,000 元
  TWO_MILLION = 7,          // 2,000,000 元
  TEN_MILLION = 8,          // 10,000,000 元
  CLOUD_TWO_THOUSAND = 9,   // 雲端發票專屬 2,000 元
}
```

### SpecialTaxCode (特殊稅種代碼)

當 `TaxType.SPECIAL` 時需指定特殊稅種代碼：

```typescript
import { TaxType, SpecialTaxCode } from '@rytass/invoice';

enum SpecialTaxCode {
  TEA = 1,                      // 茶葉
  CLUB = 2,                     // 娛樂業
  BANK_SELF = 3,                // 銀行業（本業）
  INSURANCE = 4,                // 保險業
  BANK_COMMON = 5,              // 銀行業（一般）
  BANK_SELF_SALES_BEFORE_103 = 6, // 銀行業本業銷售額（103年前）
  BANK_SELF_SALES_AFTER_103 = 7,  // 銀行業本業銷售額（103年後）
  FREE = 8,                     // 免稅
}

// 使用 SpecialTaxCode
const invoice = await gateway.issue({
  orderId: 'ORDER-001',
  items: [...],
  tax: {
    type: TaxType.SPECIAL,
    taxCode: SpecialTaxCode.BANK_COMMON,
  },
});
```

### Utility Functions

| Function | Description |
|----------|-------------|
| `isValidVATNumber(input)` | Validate Taiwan VAT number |
| `getTaxTypeFromItems(items)` | Determine TaxType from items |

### Carrier Helpers

```typescript
import { InvoiceCarriers } from '@rytass/invoice';

InvoiceCarriers.PRINT;              // 列印發票
InvoiceCarriers.MEMBER;             // 會員載具
InvoiceCarriers.PLATFORM;           // 平台載具
InvoiceCarriers.MOBILE('/ABC+123'); // 手機條碼
InvoiceCarriers.MOICA('...');       // 自然人憑證
InvoiceCarriers.LOVE_CODE('168001'); // 愛心碼捐贈
```

### Deprecated Functions

```typescript
import { verifyVatNumber, isValidVATNumber } from '@rytass/invoice';

// ⚠️ Deprecated - 請改用 isValidVATNumber
verifyVatNumber('12345678'); // 會顯示 deprecation warning

// ✅ 建議使用
isValidVATNumber('12345678');
```

## Detailed Documentation

For complete interface specifications and implementation guide:

- [Base Interfaces Reference](BASE-INTERFACES.md) - Complete type definitions
- [Creating an Adapter](CREATE-ADAPTER.md) - Step-by-step guide
