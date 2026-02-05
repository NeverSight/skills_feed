---
name: payment-development
description: Development guide for @rytass/payments base package (支付基底套件開發指南). Use when creating new payment adapters (新增支付 adapter), understanding base interfaces, or extending payment functionality. Covers PaymentGateway, Order, BindCardPaymentGateway interfaces and implementation patterns for Taiwan payment providers (台灣金流服務提供商). Keywords - payment adapter, 支付 adapter, gateway, order lifecycle, 訂單生命週期, card binding, 卡片綁定, credit card, 信用卡, virtual account, ATM 虛擬帳號, CVS payment, 超商代碼, event emitter, 事件監聽
---

# Payment Development Guide

This skill provides guidance for developers working with the `@rytass/payments` base package, including creating new payment adapters.

## Overview

The `@rytass/payments` package defines the core interfaces and types that all payment adapters must implement. It follows the adapter pattern to provide a unified API across different Taiwan payment providers.

## Architecture

```
@rytass/payments (Base Package)
    │
    ├── PaymentGateway<OCM, O>        # Gateway interface
    ├── Order<OCM>                    # Order entity interface
    ├── BindCardPaymentGateway<...>   # Card binding interface (optional)
    ├── Enums & Types                 # Shared types
    └── Event System                  # EventEmitter-based callbacks

@rytass/payments-adapter-*           # Provider implementations
    │
    ├── [Provider]Payment             # Implements PaymentGateway
    ├── [Provider]Order               # Implements Order
    └── [Provider]BindCard            # Implements card binding (optional)
```

## Installation

```bash
npm install @rytass/payments
```

## Core Interfaces

### PaymentItem

Item included in an order:

```typescript
interface PaymentItem {
  name: string;
  unitPrice: number;
  quantity: number;
}
```

### PaymentGateway

The main interface that all adapters must implement:

```typescript
interface PaymentGateway<
  OCM extends OrderCommitMessage = OrderCommitMessage,
  O extends Order<OCM> = Order<OCM>,
> {
  emitter: EventEmitter;
  prepare<N extends OCM>(input: InputFromOrderCommitMessage<N>): Promise<Order<N>>;
  query<OO extends O>(id: string, options?: unknown): Promise<OO>;
}
```

### PrepareOrderInput

Base input interface for orders:

```typescript
interface PrepareOrderInput<I extends PaymentItem = PaymentItem> {
  items: I[];
}
```

### Order

The order entity interface:

```typescript
interface Order<OCM extends OrderCommitMessage> extends PrepareOrderInput {
  state: OrderState;
  createdAt: Date | null;
  committedAt: Date | null;
  additionalInfo?: AdditionalInfo<OCM>;
  asyncInfo?: AsyncOrderInformation<OCM>;
  failedMessage: OrderFailMessage | null;
  id: string;
  items: PaymentItem[];
  committable: boolean;

  infoRetrieved<T extends OCM>(asyncInformation: AsyncOrderInformation<T>): void;
  fail(code: string, message: string): void;
  commit<T extends OCM>(message: T, additionalInfo?: AdditionalInfo<T>): void;
  refund(amount?: number, options?: unknown): Promise<void>;
}
```

### InputFromOrderCommitMessage

Input type for creating orders via `prepare()`:

```typescript
interface InputFromOrderCommitMessage<OCM extends OrderCommitMessage> extends PrepareOrderInput {
  id?: string;
  shopName?: string;
  clientBackUrl?: string;
  cardType?: CardType;
}
```

### BindCardRequest

Card binding request interface:

```typescript
interface BindCardRequest {
  cardId: string | undefined;
  memberId: string;
}
```

### CheckoutWithBoundCardOptions

Options for checkout with bound card:

```typescript
interface CheckoutWithBoundCardOptions {
  cardId: string;       // 綁定的卡片 ID
  memberId: string;     // 綁定會員 ID
  items: PaymentItem[];
  orderId?: string;     // 可選的訂單 ID，若未提供則自動生成
}
```

### BindCardPaymentGateway (Optional)

For adapters supporting card binding:

```typescript
interface BindCardPaymentGateway<
  CM extends OrderCommitMessage = OrderCommitMessage,
  R extends BindCardRequest = BindCardRequest,
  O extends Order<CM> = Order<CM>,
> {
  prepareBindCard(memberId: string): Promise<R>;
  checkoutWithBoundCard(options: CheckoutWithBoundCardOptions): Promise<O>;
}
```

## Quick Reference

### Order Lifecycle

```
INITED
  ↓ prepare()
PRE_COMMIT (Created - form/URL ready)
  ↓ User completes payment
ASYNC_INFO_RETRIEVED (for ATM/CVS - virtual account/code ready)
  ↓ User pays at bank/CVS
COMMITTED (Payment successful)
  ↓ OR
FAILED (Payment failed)
  ↓ (optional)
REFUNDED (Refund processed)
```

### Channel Enum (支付通道)

```typescript
import { Channel } from '@rytass/payments';

enum Channel {
  CREDIT_CARD = 'CREDIT_CARD',      // 信用卡
  WEB_ATM = 'WEB_ATM',              // 網路 ATM
  VIRTUAL_ACCOUNT = 'VIRTUAL_ACCOUNT', // 虛擬帳號
  CVS_KIOSK = 'CVS_KIOSK',          // 超商代碼繳費
  CVS_BARCODE = 'CVS_BARCODE',      // 超商條碼繳費
  APPLE_PAY = 'APPLE_PAY',          // Apple Pay
  LINE_PAY = 'LINE_PAY',            // LINE Pay
}
```

### Payment Channels

| Channel | Description | Commit Type |
|---------|-------------|-------------|
| `CREDIT_CARD` | Credit/Debit Card | Sync |
| `VIRTUAL_ACCOUNT` | ATM Virtual Account | Async |
| `WEB_ATM` | Online ATM | Async |
| `CVS_KIOSK` | Convenience Store Code | Async |
| `CVS_BARCODE` | Convenience Store Barcode | Async |
| `APPLE_PAY` | Apple Pay | Sync |
| `LINE_PAY` | LINE Pay | Sync |

### OrderState Enum

```typescript
enum OrderState {
  INITED = 'INITED',
  PRE_COMMIT = 'PRE_COMMIT',                 // Created
  ASYNC_INFO_RETRIEVED = 'ASYNC_INFO_RETRIEVED', // Async Payment Information Retrieved (ATM/CVS/Barcode...)
  COMMITTED = 'COMMITTED',                   // Fulfilled
  FAILED = 'FAILED',
  REFUNDED = 'REFUNDED',
}
```

| State | Description |
|-------|-------------|
| `INITED` | Order initialized |
| `PRE_COMMIT` | Order created, awaiting payment |
| `ASYNC_INFO_RETRIEVED` | Async payment info ready (ATM/CVS) |
| `COMMITTED` | Payment successful |
| `FAILED` | Payment failed |
| `REFUNDED` | Order refunded |

### OrderFailMessage

```typescript
interface OrderFailMessage {
  code: string;
  message: string;
}
```

### Card Types

```typescript
import { CardType } from '@rytass/payments';

enum CardType {
  VMJ = 'VMJ',  // Visa, MasterCard, JCB
  AE = 'AE',    // American Express
}
```

### CVS (便利商店)

```typescript
import { CVS } from '@rytass/payments';

enum CVS {
  FAMILY_MART = 'FAMILY_MART',    // 全家
  HILIFE = 'HILIFE',              // 萊爾富
  OK_MART = 'OK_MART',            // OK 超商
  SEVEN_ELEVEN = 'SEVEN_ELEVEN',  // 7-11
}
```

### CreditCardECI (3D 驗證結果)

```typescript
import { CreditCardECI } from '@rytass/payments';

enum CreditCardECI {
  MASTER_3D = '2',           // MasterCard 3D 驗證成功
  MASTER_3D_PART = '1',      // MasterCard 部分驗證
  MASTER_3D_FAILED = '0',    // MasterCard 驗證失敗
  VISA_AE_JCB_3D = '5',      // Visa/AE/JCB 3D 驗證成功
  VISA_AE_JCB_3D_PART = '6', // Visa/AE/JCB 部分驗證
  VISA_AE_JCB_3D_FAILED = '7', // Visa/AE/JCB 驗證失敗
}
```

### PaymentPeriod (定期定額)

```typescript
import { PaymentPeriod, PaymentPeriodType } from '@rytass/payments';

enum PaymentPeriodType {
  DAY = 'DAY',     // 每日
  MONTH = 'MONTH', // 每月
  YEAR = 'YEAR',   // 每年
}

interface PaymentPeriod {
  amountPerPeriod: number;  // 每期金額
  type: PaymentPeriodType;  // 週期類型
  frequency?: number;       // 頻率（可選）
  times: number;            // 扣款次數
}
```

### Payment Events

```typescript
enum PaymentEvents {
  SERVER_LISTENED = 'LISTENED',
  ORDER_INFO_RETRIEVED = 'INFO_RETRIEVED',
  ORDER_PRE_COMMIT = 'PRE_COMMIT',
  ORDER_COMMITTED = 'COMMITTED',
  ORDER_FAILED = 'FAILED',
  CARD_BOUND = 'CARD_BOUND',
  CARD_BINDING_FAILED = 'CARD_BINDING_FAILED',
}
```

| Event | When Triggered |
|-------|---------------|
| `SERVER_LISTENED` | Built-in server started |
| `ORDER_PRE_COMMIT` | Order created (form/URL ready) |
| `ORDER_INFO_RETRIEVED` | Async payment info ready |
| `ORDER_COMMITTED` | Payment successful |
| `ORDER_FAILED` | Payment failed |
| `CARD_BOUND` | Card bound successfully |
| `CARD_BINDING_FAILED` | Card binding failed |

### Event Usage

```typescript
import { PaymentEvents } from '@rytass/payments';

payment.emitter.on(PaymentEvents.ORDER_COMMITTED, (order) => {
  console.log('Payment successful:', order.id);
});

payment.emitter.on(PaymentEvents.ORDER_FAILED, (order) => {
  console.error('Payment failed:', order.failedMessage);
});
```

### OrderCommitMessage Types

Base commit message and channel-specific types:

```typescript
// Base commit message
interface OrderCommitMessage {
  id: string;
  totalPrice: number;
  committedAt: Date | null;
}

// Credit Card
interface OrderCreditCardCommitMessage extends OrderCommitMessage {
  type?: Channel.CREDIT_CARD;
  id: string;
  totalPrice: number;
  committedAt: Date;
  cardType?: CardType;
}

// Virtual Account (ATM)
interface OrderVirtualAccountCommitMessage extends OrderCommitMessage {
  type?: Channel.VIRTUAL_ACCOUNT;
  id: string;
  totalPrice: number;
  committedAt: Date | null;
}

// CVS Kiosk
interface OrderCVSCommitMessage extends OrderCommitMessage {
  type?: Channel.CVS_KIOSK;
  id: string;
  totalPrice: number;
  committedAt: Date | null;
}

// CVS Barcode
interface OrderBarcodeCommitMessage extends OrderCommitMessage {
  type?: Channel.CVS_BARCODE;
  id: string;
  totalPrice: number;
  committedAt: Date | null;
}

// Apple Pay
interface OrderApplePayCommitMessage extends OrderCommitMessage {
  type?: Channel.APPLE_PAY;
  id: string;
  totalPrice: number;
  committedAt: Date | null;
}

// LINE Pay
interface OrderLinePayCommitMessage extends OrderCommitMessage {
  type?: Channel.LINE_PAY;
  id: string;
  totalPrice: number;
  committedAt: Date | null;
}

// WebATM
interface OrderWebATMCommitMessage extends OrderCommitMessage {
  type?: Channel.WEB_ATM;
  id: string;
  totalPrice: number;
  committedAt: Date | null;
}
```

### AsyncOrderInformation Type

Conditional type for async payment info based on commit message type:

```typescript
type AsyncOrderInformation<OCM extends OrderCommitMessage> =
  OCM extends OrderVirtualAccountCommitMessage
    ? VirtualAccountInfo
    : OCM extends OrderCVSCommitMessage
      ? CVSInfo
      : OCM extends OrderBarcodeCommitMessage
        ? BarcodeInfo
        : never;
```

### AdditionalInfo Type

Conditional type for additional payment info based on commit message type:

```typescript
type AdditionalInfo<OCM extends OrderCommitMessage> =
  OCM extends OrderCreditCardCommitMessage
    ? CreditCardAuthInfo
    : OCM extends OrderVirtualAccountCommitMessage
      ? VirtualAccountPaymentInfo
      : OCM extends OrderWebATMCommitMessage
        ? WebATMPaymentInfo
        : OCM extends OrderCVSCommitMessage
          ? CVSPaymentInfo
          : OCM extends OrderBarcodeCommitMessage
            ? BarcodeInfo
            : OCM extends OrderApplePayCommitMessage
              ? undefined
              : never;
```

### Info Types

For async payment channels:

```typescript
// Virtual Account (ATM)
interface VirtualAccountInfo {
  channel: Channel.VIRTUAL_ACCOUNT;
  bankCode: string;
  account: string;
  expiredAt: Date;
}

// CVS Kiosk
interface CVSInfo {
  channel: Channel.CVS_KIOSK;
  paymentCode: string;
  expiredAt: Date;
}

// CVS Barcode
interface BarcodeInfo {
  channel: Channel.CVS_BARCODE;
  barcodes: [string, string, string];
  expiredAt: Date;
}
```

For credit card authorization:

```typescript
interface CreditCardAuthInfo {
  channel: Channel.CREDIT_CARD;
  processDate: Date;
  authCode: string;       // 信用卡授權碼 (6 碼)
  amount: number;
  eci: CreditCardECI;     // 3D 驗證結果
  card4Number: string;    // 卡號末 4 碼
  card6Number: string;    // 卡號前 6 碼
  gwsr?: string;          // 閘道序號（可選）
  xid?: string;           // 交易 ID（可選）
  aetId?: string;         // AE 交易 ID（可選）
}
```

For WebATM payment:

```typescript
interface WebATMPaymentInfo {
  channel: Channel.WEB_ATM;
  buyerAccountNumber: string;  // 付款人帳號
  buyerBankCode: string;       // 付款人銀行代碼
}
```

For Virtual Account payment (付款後):

```typescript
interface VirtualAccountPaymentInfo {
  channel: Channel.VIRTUAL_ACCOUNT;
  buyerAccountNumber: string;  // 付款人帳號
  buyerBankCode: string;       // 付款人銀行代碼
}
```

For CVS payment:

```typescript
interface CVSPaymentInfo {
  channel: Channel.CVS_KIOSK;
  cvsPayFrom: CVS;  // 付款超商
}
```

## Detailed Documentation

For complete interface specifications and implementation guide:

- [Base Interfaces Reference](BASE-INTERFACES.md) - Complete type definitions
- [Creating an Adapter](CREATE-ADAPTER.md) - Step-by-step guide
