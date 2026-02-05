---
name: payment-adapters
description: Taiwan payment integration (台灣支付整合). Use when working with ECPay (綠界), NewebPay (藍新), HwaNan Bank (華南銀行), CTBC (中信), iCash Pay, or Happy Card payment services. Covers credit card (信用卡), virtual account (虛擬帳號), ATM, CVS payment (超商代碼/條碼), card binding (卡片綁定), installments (分期付款), recurring payments (訂閱付款), and NestJS integration.
---

# Taiwan Payment Adapters

This skill provides comprehensive guidance for using `@rytass/payments-adapter-*` packages to integrate Taiwan payment service providers.

## Overview

All adapters implement the `PaymentGateway` interface from `@rytass/payments`, providing a unified API across different providers:

| Package | Provider | Description |
|---------|----------|-------------|
| `@rytass/payments-adapter-ecpay` | ECPay (綠界科技) | Most popular Taiwan payment gateway |
| `@rytass/payments-adapter-newebpay` | NewebPay (藍新金流) | Also known as EZPay, supports multiple payment methods |
| `@rytass/payments-adapter-hwanan` | HwaNan Bank (華南銀行) | Bank-integrated payment service |
| `@rytass/payments-adapter-ctbc-micro-fast-pay` | CTBC (中國信託) | CTBC Micro Fast Pay integration |
| `@rytass/payments-adapter-icash-pay` | iCash Pay (愛金卡) | Unified group payment service |
| `@rytass/payments-adapter-happy-card` | Happy Card (統一禮物卡) | Unified group gift card payment |

### Base Interface (@rytass/payments)

All adapters share these core concepts:

**PaymentGateway** - Main interface for payment operations
```typescript
interface PaymentGateway<OCM extends OrderCommitMessage> {
  emitter: EventEmitter;
  prepare<N extends OCM>(input: InputFromOrderCommitMessage<N>): Promise<Order<N>>;
  query<OO extends Order>(id: string, options?: unknown): Promise<OO>;
}
```

**Order Lifecycle** - All orders follow this state machine:
```
INITED → PRE_COMMIT → [ASYNC_INFO_RETRIEVED] → COMMITTED/FAILED → REFUNDED
```

**Payment Channels** - Supported payment methods:
- `CREDIT_CARD` - Credit card payments (信用卡)
- `VIRTUAL_ACCOUNT` - Virtual account transfer (虛擬帳號)
- `WEB_ATM` - Web ATM transfer (網路 ATM)
- `CVS_KIOSK` - Convenience store code payment (超商代碼)
- `CVS_BARCODE` - Convenience store barcode payment (超商條碼)
- `APPLE_PAY` - Apple Pay integration
- `LINE_PAY` - LINE Pay integration

## Installation

```bash
# Install base package
npm install @rytass/payments

# Choose the adapter for your provider
npm install @rytass/payments-adapter-ecpay
npm install @rytass/payments-adapter-newebpay
npm install @rytass/payments-adapter-hwanan
npm install @rytass/payments-adapter-ctbc-micro-fast-pay
npm install @rytass/payments-adapter-icash-pay
npm install @rytass/payments-adapter-happy-card

# For NestJS integration
npm install @rytass/payments-nestjs-module
```

## Quick Start

### ECPay (綠界)

```typescript
import { ECPayPayment, Channel, PaymentEvents } from '@rytass/payments-adapter-ecpay';

// Initialize gateway
const gateway = new ECPayPayment({
  merchantId: process.env.ECPAY_MERCHANT_ID!,
  hashKey: process.env.ECPAY_HASH_KEY!,
  hashIv: process.env.ECPAY_HASH_IV!,
  serverHost: 'https://your-domain.com', // Your server URL for callbacks
  withServer: true, // Enable built-in callback server
});

// Listen to payment events
gateway.emitter.on(PaymentEvents.ORDER_COMMITTED, (order) => {
  console.log('Payment successful:', order.id, order.totalPrice);
});

gateway.emitter.on(PaymentEvents.ORDER_FAILED, (failure) => {
  console.error('Payment failed:', failure.code, failure.message);
});

// Prepare payment order
const order = await gateway.prepare({
  channel: Channel.CREDIT_CARD,
  items: [
    { name: 'Product A', unitPrice: 1000, quantity: 2 },
    { name: 'Product B', unitPrice: 500, quantity: 1 },
  ],
  clientBackUrl: 'https://your-site.com/payment/return', // User return URL
});

// Get checkout URL (3 ways)
const checkoutUrl = order.checkoutURL; // Built-in server URL (recommended)
const autoSubmitHtml = order.formHTML; // HTML with auto-submit form
const formData = order.form; // Raw form data for custom implementation
```

### NewebPay (藍新)

```typescript
import { NewebPayPayment, NewebPaymentChannel } from '@rytass/payments-adapter-newebpay';

const gateway = new NewebPayPayment({
  merchantId: process.env.NEWEBPAY_MERCHANT_ID!,
  aesKey: process.env.NEWEBPAY_AES_KEY!,
  aesIv: process.env.NEWEBPAY_AES_IV!,
  serverHost: 'https://your-domain.com',
  withServer: true,
});

const order = await gateway.prepare({
  channel: NewebPaymentChannel.CREDIT,  // 注意：使用 NewebPaymentChannel 而非 Channel
  items: [{ name: 'Service Fee', unitPrice: 3000, quantity: 1 }],
});

console.log('Checkout URL:', order.checkoutURL);
```

### HwaNan Bank (華南銀行)

```typescript
import { HwaNanPayment, HwaNanPaymentChannel } from '@rytass/payments-adapter-hwanan';

const gateway = new HwaNanPayment({
  merchantId: process.env.HWANAN_MERCHANT_ID!,
  terminalId: process.env.HWANAN_TERMINAL_ID!,
  merID: process.env.HWANAN_MER_ID!,
  identifier: process.env.HWANAN_IDENTIFIER!,
  merchantName: 'My Store Name',
  withServer: true,
});

const order = await gateway.prepare({
  channel: HwaNanPaymentChannel.CREDIT_CARD,  // 注意：使用 HwaNanPaymentChannel
  items: [{ name: 'Purchase', unitPrice: 5000, quantity: 1 }],
});
```

### CTBC (中信)

```typescript
import { CTBCPayment, Channel } from '@rytass/payments-adapter-ctbc-micro-fast-pay';

const gateway = new CTBCPayment({
  merchantId: process.env.CTBC_MERCHANT_ID!,
  merId: process.env.CTBC_MER_ID!,
  txnKey: process.env.CTBC_TXN_KEY!,
  terminalId: process.env.CTBC_TERMINAL_ID!,
  withServer: true,
});

const order = await gateway.prepare({
  channel: Channel.CREDIT_CARD,
  items: [{ name: 'Item', unitPrice: 2000, quantity: 1 }],
});
```

### iCash Pay (愛金卡)

```typescript
import { ICashPayPayment, ICashPayBaseUrls } from '@rytass/payments-adapter-icash-pay';

const gateway = new ICashPayPayment({
  baseUrl: ICashPayBaseUrls.DEVELOPMENT, // 必填：環境設定
  merchantId: process.env.ICASH_PAY_MERCHANT_ID!,
  clientPrivateKey: process.env.ICASH_PAY_CLIENT_PRIVATE_KEY!,
  serverPublicKey: process.env.ICASH_PAY_SERVER_PUBLIC_KEY!,
  aesKey: {
    id: process.env.ICASH_PAY_AES_KEY_ID!,
    key: process.env.ICASH_PAY_AES_KEY!,
    iv: process.env.ICASH_PAY_AES_IV!,
  },
});

// iCash Pay uses barcode scanning
const order = await gateway.prepare({
  id: 'ORDER-001',
  storeName: 'My Coffee Shop',
  barcode: '280012345678901234', // 18-digit barcode from customer
  amount: 150,
  items: [{ name: 'Americano', unitPrice: 120, quantity: 1 }],
  collectedAmount: 150,
});

const result = await order.commit();
```

### Happy Card (統一禮物卡)

```typescript
import { HappyCardPayment, HappyCardRecordType } from '@rytass/payments-adapter-happy-card';

const gateway = new HappyCardPayment({
  cSource: process.env.HAPPY_CARD_C_SOURCE!,
  key: process.env.HAPPY_CARD_KEY!,
});

// Query card balance first (get detailed records)
const [records, productType] = await gateway.getCardBalance('HC1234567890123456', true);
console.log('Product type:', productType);
records.forEach(record => {
  console.log(`Record ${record.id}: Type=${record.type}, Amount=${record.amount}`);
});

// Make payment using card
const order = await gateway.prepare({
  id: 'HAPPY-ORDER-001',
  cardSerial: 'HC1234567890123456',
  items: [{ name: 'Coffee', unitPrice: 150, quantity: 2 }],
  useRecords: [
    { id: 12345, type: HappyCardRecordType.BONUS, amount: 300 },
  ],
});

const result = await order.commit(); // Immediate deduction
```

## Common Patterns

### Event-Driven Architecture

All payment adapters use `EventEmitter` for asynchronous notifications:

```typescript
import { PaymentEvents } from '@rytass/payments';

// Payment success
gateway.emitter.on(PaymentEvents.ORDER_COMMITTED, (order) => {
  console.log('Order ID:', order.id);
  console.log('Total Price:', order.totalPrice);
  console.log('Committed At:', order.committedAt);
  console.log('Additional Info:', order.additionalInfo); // Card info, bank code, etc.

  // Update database, send notifications, etc.
  updateOrderStatus(order.id, 'PAID');
  sendReceiptEmail(order);
});

// Payment failure
gateway.emitter.on(PaymentEvents.ORDER_FAILED, (failure) => {
  console.error('Failed Order ID:', failure.id);
  console.error('Error Code:', failure.code);
  console.error('Error Message:', failure.message);

  // Handle failure
  updateOrderStatus(failure.id, 'FAILED');
  notifyCustomer(failure);
});

// Async payment info retrieved (Virtual Account, CVS codes)
gateway.emitter.on(PaymentEvents.ORDER_INFO_RETRIEVED, (order) => {
  if (order.asyncInfo?.channel === Channel.VIRTUAL_ACCOUNT) {
    console.log('Bank Code:', order.asyncInfo.bankCode);
    console.log('Account Number:', order.asyncInfo.account);
    console.log('Expires At:', order.asyncInfo.expiredAt);

    // Send virtual account info to customer
    sendVirtualAccountEmail({
      bankCode: order.asyncInfo.bankCode,
      account: order.asyncInfo.account,
      amount: order.totalPrice,
      expiredAt: order.asyncInfo.expiredAt,
    });
  }

  if (order.asyncInfo?.channel === Channel.CVS_KIOSK) {
    console.log('Payment Code:', order.asyncInfo.paymentCode);
    console.log('Expires At:', order.asyncInfo.expiredAt);

    // Send CVS code to customer
    sendCVSCodeSMS(order.asyncInfo.paymentCode);
  }
});

// Card binding success
gateway.emitter.on(PaymentEvents.CARD_BOUND, (bindRequest) => {
  console.log('Member ID:', bindRequest.memberId);
  console.log('Card ID:', bindRequest.cardId);
  console.log('Card Suffix:', bindRequest.cardNumberSuffix);

  // Save card info to database
  saveCardToDatabase({
    memberId: bindRequest.memberId,
    cardId: bindRequest.cardId,
    lastFourDigits: bindRequest.cardNumberSuffix,
  });
});

// Card binding failure
gateway.emitter.on(PaymentEvents.CARD_BINDING_FAILED, (bindRequest) => {
  console.error('Binding failed for member:', bindRequest.memberId);
  console.error('Error:', bindRequest.failedMessage);
});
```

### Order Lifecycle

Understanding the order state machine:

```typescript
import { OrderState } from '@rytass/payments';

// 1. INITED - Order object created but not sent to gateway
const order = await gateway.prepare({ ... });
console.log(order.state); // OrderState.INITED

// Order becomes PRE_COMMIT after prepare() returns
console.log(order.state); // OrderState.PRE_COMMIT

// 2. For sync payments (Credit Card):
// User completes payment → Gateway sends callback → commit() called → COMMITTED

// 3. For async payments (Virtual Account, CVS):
// prepare() → ASYNC_INFO_RETRIEVED → User pays → COMMITTED

// 4. Payment can fail at any time → FAILED
// Check for failure:
if (order.state === OrderState.FAILED) {
  console.error('Reason:', order.failedMessage?.message);
}

// 5. After committed, can refund → REFUNDED (if supported)
if (order.state === OrderState.COMMITTED) {
  await order.refund(); // Full refund
  await order.refund(500); // Partial refund (if supported)
}
```

### Credit Card Payment Flow

Complete flow from preparation to completion:

```typescript
// 1. Prepare order
const order = await gateway.prepare({
  channel: Channel.CREDIT_CARD,
  items: [{ name: 'Product', unitPrice: 1000, quantity: 1 }],
  clientBackUrl: 'https://your-site.com/payment/return',
});

// 2. Three ways to get checkout:
// Option A: Built-in server URL (recommended if withServer: true)
res.redirect(order.checkoutURL);

// Option B: Auto-submit HTML
res.send(order.formHTML);

// Option C: Custom form implementation
res.render('checkout', { formData: order.form });

// 3. User completes payment on payment gateway page

// 4. Gateway sends callback to your server
// If withServer: true, this is handled automatically
// The ORDER_COMMITTED event will fire:

gateway.emitter.on(PaymentEvents.ORDER_COMMITTED, (order) => {
  // Order is now paid!
  console.log('Payment completed:', order.id);
  console.log('Card info:', {
    lastFour: order.additionalInfo.card4Number,
    authCode: order.additionalInfo.authCode,
    eci: order.additionalInfo.eci,
  });
});

// 5. User is redirected to clientBackUrl
// You can query the order status:
const updatedOrder = await gateway.query(order.id);
console.log('Final state:', updatedOrder.state);
console.log('Is paid:', updatedOrder.state === OrderState.COMMITTED);
```

### Virtual Account Payment Flow

Async payment with bank transfer:

```typescript
// 1. Prepare virtual account order
const order = await gateway.prepare({
  channel: Channel.VIRTUAL_ACCOUNT,
  items: [{ name: 'Bulk Purchase', unitPrice: 50000, quantity: 1 }],
  virtualAccountExpireDays: 7, // Account expires in 7 days
});

// 2. Listen for virtual account info
gateway.emitter.on(PaymentEvents.ORDER_INFO_RETRIEVED, (order) => {
  if (order.asyncInfo?.channel === Channel.VIRTUAL_ACCOUNT) {
    const { bankCode, account, expiredAt } = order.asyncInfo;

    console.log('=== Virtual Account Info ===');
    console.log('Bank Code:', bankCode); // e.g., '004' (Taiwan Bank)
    console.log('Account:', account); // e.g., '88801234567890'
    console.log('Amount:', order.totalPrice);
    console.log('Expires:', expiredAt);

    // Send to customer via email/SMS
    sendVirtualAccountNotification({
      orderId: order.id,
      bankCode,
      account,
      amount: order.totalPrice,
      expiredAt,
    });
  }
});

// 3. User makes bank transfer

// 4. When payment is received, ORDER_COMMITTED event fires
gateway.emitter.on(PaymentEvents.ORDER_COMMITTED, (order) => {
  console.log('Virtual account payment received!');
  console.log('Paid from bank:', order.additionalInfo.buyerBankCode);
  console.log('Account:', order.additionalInfo.buyerAccountNumber);

  // Fulfill order
  processOrder(order.id);
});
```

### CVS Payment Flow

Convenience store code/barcode payment:

```typescript
// CVS Kiosk Code Payment (超商代碼)
const cvsOrder = await gateway.prepare({
  channel: Channel.CVS_KIOSK,
  items: [{ name: 'Online Course', unitPrice: 1200, quantity: 1 }],
});

gateway.emitter.on(PaymentEvents.ORDER_INFO_RETRIEVED, (order) => {
  if (order.asyncInfo?.channel === Channel.CVS_KIOSK) {
    console.log('Payment Code:', order.asyncInfo.paymentCode); // e.g., '1234567890'
    console.log('Expires:', order.asyncInfo.expiredAt);

    // Customer can pay at 7-Eleven, FamilyMart, OK Mart, Hi-Life
    sendCVSCodeSMS(order.asyncInfo.paymentCode);
  }
});

// CVS Barcode Payment (超商條碼)
const barcodeOrder = await gateway.prepare({
  channel: Channel.CVS_BARCODE,
  items: [{ name: 'Magazine', unitPrice: 280, quantity: 1 }],
});

gateway.emitter.on(PaymentEvents.ORDER_INFO_RETRIEVED, (order) => {
  if (order.asyncInfo?.channel === Channel.CVS_BARCODE) {
    const [barcode1, barcode2, barcode3] = order.asyncInfo.barcodes;
    console.log('Barcode 1:', barcode1);
    console.log('Barcode 2:', barcode2);
    console.log('Barcode 3:', barcode3);

    // Send barcodes to customer (display on page or send via email)
    sendBarcodesEmail([barcode1, barcode2, barcode3]);
  }
});
```

### Query Order Status

Check payment status at any time:

```typescript
// Query by order ID
const order = await gateway.query('ORDER-2024-001');

console.log('Order State:', order.state);
console.log('Created At:', order.createdAt);
console.log('Committed At:', order.committedAt);
console.log('Total Price:', order.totalPrice);

// Check state
if (order.state === OrderState.COMMITTED) {
  console.log('Payment completed!');
  console.log('Additional Info:', order.additionalInfo);
}

if (order.state === OrderState.FAILED) {
  console.error('Payment failed!');
  console.error('Error Code:', order.failedMessage?.code);
  console.error('Error Message:', order.failedMessage?.message);
}

if (order.state === OrderState.PRE_COMMIT) {
  console.log('Waiting for payment...');
}

if (order.state === OrderState.ASYNC_INFO_RETRIEVED) {
  console.log('Virtual account/CVS code generated, waiting for customer payment');
  console.log('Payment Info:', order.asyncInfo);
}
```

## Advanced Features

### Card Binding (卡片綁定)

Bind credit cards for future one-click payments:

```typescript
import { PaymentEvents } from '@rytass/payments';

// Step 1: Prepare card binding request
const bindRequest = await gateway.prepareBindCard('MEMBER_123');

console.log('Binding URL:', bindRequest.checkoutURL);

// Redirect user to binding URL
res.redirect(bindRequest.checkoutURL);

// Step 2: Listen for binding result
gateway.emitter.on(PaymentEvents.CARD_BOUND, (bindRequest) => {
  console.log('Card bound successfully!');
  console.log('Member ID:', bindRequest.memberId);
  console.log('Card ID:', bindRequest.cardId); // Save this for future use
  console.log('Last 4 digits:', bindRequest.cardNumberSuffix);

  // Save to database
  await db.cards.create({
    memberId: bindRequest.memberId,
    cardId: bindRequest.cardId,
    lastFourDigits: bindRequest.cardNumberSuffix,
    createdAt: new Date(),
  });
});

// Step 3: Use bound card for payment
const boundOrder = await gateway.checkoutWithBoundCard({
  memberId: 'MEMBER_123',
  cardId: 'CARD_ID_FROM_BINDING',
  items: [{ name: 'Subscription', unitPrice: 999, quantity: 1 }],
  orderId: 'SUBSCRIPTION-001', // Optional
});

console.log('Payment result:', boundOrder);

// Alternative: Bind card with transaction (ECPay only)
gateway.emitter.on(PaymentEvents.ORDER_COMMITTED, async (order) => {
  // After successful payment, bind the card used
  const bindRequest = await gateway.bindCardWithTransaction(
    'MEMBER_123',
    order.platformTradeNumber,
    order.id
  );

  console.log('Card bound with transaction:', bindRequest.cardId);
});
```

### Memory Card vs Card Binding

Understanding the difference:

```typescript
// Memory Card (記憶卡) - Gateway remembers card for single user session
const memoryPayment = new ECPayPayment({
  merchantId: 'YOUR_MERCHANT_ID',
  hashKey: 'YOUR_KEY',
  hashIv: 'YOUR_IV',
  memory: true, // Enable memory card
});

// User only needs to enter card once per session
// Subsequent payments in same session can reuse card
// Card is NOT saved permanently
// Cannot use bindCardWithTransaction when memory: true

// Card Binding (卡片綁定) - Permanently save card for future use
const bindingPayment = new ECPayPayment({
  merchantId: 'YOUR_MERCHANT_ID',
  hashKey: 'YOUR_KEY',
  hashIv: 'YOUR_IV',
  memory: false, // Must be false for binding
});

// Card is saved permanently
// Can use across sessions and devices
// Requires prepareBindCard() or bindCardWithTransaction()
// User must consent to saving card
```

### Installment Payments (分期付款)

Credit card installment options:

```typescript
// ECPay installments
const installmentPayment = new ECPayPayment({
  merchantId: 'YOUR_MERCHANT_ID',
  hashKey: 'YOUR_KEY',
  hashIv: 'YOUR_IV',
  installments: '3,6,12,18,24', // Available installment periods
});

const order = await installmentPayment.prepare({
  channel: Channel.CREDIT_CARD,
  items: [{ name: 'Laptop', unitPrice: 30000, quantity: 1 }],
  // User can choose 3, 6, 12, 18, or 24 installments on payment page
});

// CTBC installments
const ctbcPayment = new CTBCPayment({
  merchantId: 'YOUR_MERCHANT_ID',
  merId: 'YOUR_MER_ID',
  txnKey: 'YOUR_KEY',
  terminalId: 'YOUR_TERMINAL',
  installmentCount: 12, // Fixed 12 installments
});

// HwaNan installments
const hwananPayment = new HwaNanPayment({
  merchantId: 'YOUR_MERCHANT_ID',
  terminalId: 'YOUR_TERMINAL',
  merID: 'YOUR_MER_ID',
  identifier: 'YOUR_IDENTIFIER',
  installmentAmount: 5000, // Minimum amount for installments
});
```

### Recurring Payments (訂閱付款)

Set up periodic payments:

```typescript
import { PaymentPeriodType } from '@rytass/payments';

// ECPay recurring payment
const recurringPayment = new ECPayPayment({
  merchantId: 'YOUR_MERCHANT_ID',
  hashKey: 'YOUR_KEY',
  hashIv: 'YOUR_IV',
  period: {
    amountPerPeriod: 999, // Amount per charge
    type: PaymentPeriodType.MONTH, // DAY, MONTH, or YEAR
    frequency: 1, // Charge every 1 month
    times: 12, // Total 12 charges
  },
});

const order = await recurringPayment.prepare({
  channel: Channel.CREDIT_CARD,
  items: [{ name: 'Monthly Subscription', unitPrice: 999, quantity: 1 }],
});

// Gateway will automatically charge 999 every month for 12 months

// Examples:
// Daily payment for 30 days
period: {
  amountPerPeriod: 50,
  type: PaymentPeriodType.DAY,
  frequency: 1,
  times: 30,
}

// Weekly payment (every 7 days) for 8 weeks
period: {
  amountPerPeriod: 200,
  type: PaymentPeriodType.DAY,
  frequency: 7,
  times: 8,
}

// Quarterly payment for 1 year (4 times)
period: {
  amountPerPeriod: 3000,
  type: PaymentPeriodType.MONTH,
  frequency: 3,
  times: 4,
}
```

### Built-in Server & Ngrok

Handle callbacks with built-in server:

```typescript
// Option 1: Built-in server with public domain
const gateway = new ECPayPayment({
  merchantId: 'YOUR_MERCHANT_ID',
  hashKey: 'YOUR_KEY',
  hashIv: 'YOUR_IV',
  serverHost: 'https://your-domain.com',
  withServer: true, // Enable built-in server
});

// Server automatically handles callbacks at:
// https://your-domain.com/payments/callbacks

// Option 2: Built-in server with Ngrok (for development)
const gateway = new ECPayPayment({
  merchantId: 'YOUR_MERCHANT_ID',
  hashKey: 'YOUR_KEY',
  hashIv: 'YOUR_IV',
  withServer: 'ngrok', // Auto-start ngrok tunnel
});

// Listen for server ready
gateway.emitter.on(PaymentEvents.SERVER_LISTENED, (info) => {
  console.log('Server listening on:', info.url);
  // e.g., "https://abc123.ngrok.io"
});

// Option 3: Custom server (no built-in server)
const gateway = new ECPayPayment({
  merchantId: 'YOUR_MERCHANT_ID',
  hashKey: 'YOUR_KEY',
  hashIv: 'YOUR_IV',
  withServer: false,
});

// Implement your own callback endpoint
app.post('/payment/callback', (req, res) => {
  gateway.defaultServerListener(req, res);
});
```

## NestJS Integration

Complete integration with NestJS dependency injection:

### Basic Setup

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { PaymentsModule } from '@rytass/payments-nestjs-module';
import { ECPayPayment } from '@rytass/payments-adapter-ecpay';

@Module({
  imports: [
    PaymentsModule.forRoot({
      paymentGateway: new ECPayPayment({
        merchantId: process.env.ECPAY_MERCHANT_ID!,
        hashKey: process.env.ECPAY_HASH_KEY!,
        hashIv: process.env.ECPAY_HASH_IV!,
        serverHost: process.env.SERVER_HOST!,
        withServer: true,
      }),
    }),
  ],
})
export class AppModule {}
```

### Async Configuration

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { PaymentsModule } from '@rytass/payments-nestjs-module';
import { ECPayPayment } from '@rytass/payments-adapter-ecpay';

@Module({
  imports: [
    ConfigModule.forRoot(),
    PaymentsModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        paymentGateway: new ECPayPayment({
          merchantId: config.get('ECPAY_MERCHANT_ID')!,
          hashKey: config.get('ECPAY_HASH_KEY')!,
          hashIv: config.get('ECPAY_HASH_IV')!,
          serverHost: config.get('SERVER_HOST')!,
          withServer: true,
        }),
      }),
    }),
  ],
})
export class AppModule {}
```

### Using in Services

```typescript
// payment.service.ts
import { Injectable, Inject, Logger } from '@nestjs/common';
import { PaymentGateway, Channel, PaymentEvents, OrderState } from '@rytass/payments';
import { PAYMENTS_GATEWAY } from '@rytass/payments-nestjs-module';

@Injectable()
export class PaymentService {
  private readonly logger = new Logger(PaymentService.name);

  constructor(
    @Inject(PAYMENTS_GATEWAY)
    private readonly paymentGateway: PaymentGateway,
  ) {
    this.setupEventListeners();
  }

  private setupEventListeners() {
    this.paymentGateway.emitter?.on(PaymentEvents.ORDER_COMMITTED, (message) => {
      this.logger.log(`Payment committed: ${message.id}`);
      this.handlePaymentSuccess(message);
    });

    this.paymentGateway.emitter?.on(PaymentEvents.ORDER_FAILED, (failure) => {
      this.logger.error(`Payment failed: ${failure.code} - ${failure.message}`);
      this.handlePaymentFailure(failure);
    });
  }

  async createPayment(data: {
    itemName: string;
    amount: number;
    quantity?: number;
  }) {
    const order = await this.paymentGateway.prepare({
      channel: Channel.CREDIT_CARD,
      items: [{
        name: data.itemName,
        unitPrice: data.amount,
        quantity: data.quantity || 1,
      }],
    });

    return {
      orderId: order.id,
      checkoutUrl: order.checkoutURL,
      totalAmount: order.totalPrice,
    };
  }

  async queryPayment(orderId: string) {
    const order = await this.paymentGateway.query(orderId);

    return {
      orderId: order.id,
      state: order.state,
      isPaid: order.state === OrderState.COMMITTED,
      totalAmount: order.totalPrice,
      committedAt: order.committedAt,
    };
  }

  private async handlePaymentSuccess(message: any) {
    // Update database, send notifications, etc.
  }

  private async handlePaymentFailure(failure: any) {
    // Handle failure logic
  }
}
```

### Built-in Endpoints

PaymentsModule automatically provides these endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/payments/checkout/:orderNo` | Payment checkout page |
| `POST` | `/payments/callbacks` | Payment gateway callbacks |

These endpoints are automatically marked as public (no authentication required).

### Multiple Gateways

Use multiple payment gateways in one application:

```typescript
// payments.config.ts
import { Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { ECPayPayment } from '@rytass/payments-adapter-ecpay';
import { NewebPayPayment } from '@rytass/payments-adapter-newebpay';

@Module({
  providers: [
    {
      provide: 'ECPAY_GATEWAY',
      useFactory: (config: ConfigService) => new ECPayPayment({
        merchantId: config.get('ECPAY_MERCHANT_ID'),
        hashKey: config.get('ECPAY_HASH_KEY'),
        hashIv: config.get('ECPAY_HASH_IV'),
        withServer: true,
      }),
      inject: [ConfigService],
    },
    {
      provide: 'NEWEBPAY_GATEWAY',
      useFactory: (config: ConfigService) => new NewebPayPayment({
        merchantId: config.get('NEWEBPAY_MERCHANT_ID'),
        aesKey: config.get('NEWEBPAY_AES_KEY'),
        aesIv: config.get('NEWEBPAY_AES_IV'),
        withServer: true,
      }),
      inject: [ConfigService],
    },
  ],
  exports: ['ECPAY_GATEWAY', 'NEWEBPAY_GATEWAY'],
})
export class PaymentsConfigModule {}

// Use in service
@Injectable()
export class MultiGatewayService {
  constructor(
    @Inject('ECPAY_GATEWAY') private ecpay: any,
    @Inject('NEWEBPAY_GATEWAY') private newebpay: any,
  ) {}

  async createPayment(provider: 'ecpay' | 'newebpay', data: any) {
    const gateway = provider === 'ecpay' ? this.ecpay : this.newebpay;
    return await gateway.prepare(data);
  }
}
```

## Feature Comparison

| Feature | ECPay | NewebPay | HwaNan | CTBC | iCash Pay | Happy Card |
|---------|:-----:|:--------:|:------:|:----:|:---------:|:----------:|
| **Credit Card** | Yes | Yes | Yes | Yes | Yes | No |
| **Installments** | Yes | Yes | Yes | Yes | No | No |
| **Virtual Account** | Yes | Yes | No | Yes | No | No |
| **Web ATM** | Yes | Yes | No | No | No | No |
| **CVS Code** | Yes | Yes | No | Yes | No | No |
| **CVS Barcode** | Yes | No | No | Yes | No | No |
| **Apple Pay** | Yes | No | No | Yes | No | No |
| **Card Binding** | Yes | Yes | No | Yes | No | No |
| **Memory Card** | Yes | Yes | No | No | No | No |
| **Recurring Payment** | Yes | No | No | No | No | No |
| **Built-in Server** | Yes | Yes | Yes | Yes | No | No |
| **Ngrok Support** | Yes | Yes | Yes | Yes | No | No |
| **Barcode Scan** | No | No | No | No | Yes | No |
| **Gift Card Balance** | No | No | No | No | No | Yes |
| **Bonus Points** | No | No | No | No | No | Yes |
| **Multi-language** | No | Yes | Yes | No | No | No |
| **Refund** | Partial | Partial | No | No | Yes | Yes |

### Signature Methods

| Provider | Method | Algorithm |
|----------|--------|-----------|
| ECPay | SHA256 Hash | SHA256 with URL encoding |
| NewebPay | AES Encryption | AES-256-CBC |
| HwaNan | MAC Signature | MD5/SHA256 |
| CTBC | MAC/TXN | Proprietary algorithm |
| iCash Pay | RSA + AES | RSA-SHA256 + AES-256-CBC |
| Happy Card | MD5 Hash | MD5 signature |

## Environment Configuration

### Development vs Production

All adapters support environment switching:

```typescript
// ECPay
import { ECPayPayment } from '@rytass/payments-adapter-ecpay';

// Development (default)
const devGateway = new ECPayPayment(); // Uses test credentials

// Production
const prodGateway = new ECPayPayment({
  baseUrl: 'https://payment.ecpay.com.tw',
  merchantId: 'YOUR_PROD_MERCHANT_ID',
  hashKey: 'YOUR_PROD_HASH_KEY',
  hashIv: 'YOUR_PROD_HASH_IV',
});

// NewebPay
import { NewebPayPayment } from '@rytass/payments-adapter-newebpay';

// 預設為測試環境: https://ccore.newebpay.com
const prodGateway = new NewebPayPayment({
  baseUrl: 'https://core.newebpay.com',  // 正式環境
  merchantId: 'YOUR_PROD_MERCHANT_ID',
  aesKey: 'YOUR_PROD_AES_KEY',
  aesIv: 'YOUR_PROD_AES_IV',
});

// Happy Card
import { HappyCardPayment, HappyCardBaseUrls } from '@rytass/payments-adapter-happy-card';

const prodGateway = new HappyCardPayment({
  baseUrl: HappyCardBaseUrls.PRODUCTION,
  cSource: 'YOUR_PROD_C_SOURCE',
  key: 'YOUR_PROD_KEY',
});
```

### Environment Variables

```bash
# .env
NODE_ENV=production

# ECPay
ECPAY_MERCHANT_ID=your_merchant_id
ECPAY_HASH_KEY=your_hash_key
ECPAY_HASH_IV=your_hash_iv

# NewebPay
NEWEBPAY_MERCHANT_ID=your_merchant_id
NEWEBPAY_AES_KEY=your_aes_key
NEWEBPAY_AES_IV=your_aes_iv

# HwaNan
HWANAN_MERCHANT_ID=your_merchant_id
HWANAN_TERMINAL_ID=your_terminal_id
HWANAN_MER_ID=your_mer_id
HWANAN_IDENTIFIER=your_identifier

# CTBC
CTBC_MERCHANT_ID=your_merchant_id
CTBC_MER_ID=your_mer_id
CTBC_TXN_KEY=your_txn_key
CTBC_TERMINAL_ID=your_terminal_id

# iCash Pay
ICASH_PAY_MERCHANT_ID=your_merchant_id
ICASH_PAY_CLIENT_PRIVATE_KEY=your_private_key
ICASH_PAY_SERVER_PUBLIC_KEY=server_public_key
ICASH_PAY_AES_KEY_ID=your_aes_key_id
ICASH_PAY_AES_KEY=your_32_char_aes_key
ICASH_PAY_AES_IV=your_16_char_aes_iv

# Happy Card
HAPPY_CARD_C_SOURCE=your_c_source
HAPPY_CARD_KEY=your_key

# Server
SERVER_HOST=https://your-domain.com
```

## Troubleshooting

### Common Issues

#### 1. Signature Verification Failed

**Symptoms:**
- Payment fails immediately
- Error message contains "signature", "checksum", or "verification"
- Callback returns error

**Solutions:**
```typescript
// Check credentials
console.log('Merchant ID:', process.env.ECPAY_MERCHANT_ID);
console.log('Hash Key length:', process.env.ECPAY_HASH_KEY?.length);
console.log('Hash IV length:', process.env.ECPAY_HASH_IV?.length);

// Ensure no extra spaces in .env file
ECPAY_HASH_KEY=your_key_here  # ❌ Trailing space
ECPAY_HASH_KEY=your_key_here   # ✅ No trailing space

// Check baseUrl matches environment
const gateway = new ECPayPayment({
  baseUrl: 'https://payment-stage.ecpay.com.tw', // Test environment
  // Use production URL for production
});
```

#### 2. Callback Not Received

**Symptoms:**
- Payment completes but ORDER_COMMITTED never fires
- Order stuck in PRE_COMMIT state

**Solutions:**
```typescript
// 1. Check withServer setting
const gateway = new ECPayPayment({
  withServer: true, // Must be true for built-in server
  serverHost: 'https://your-domain.com', // Must be accessible from internet
});

// 2. Verify server is listening
gateway.emitter.on(PaymentEvents.SERVER_LISTENED, (info) => {
  console.log('Server listening:', info.url);
  // Ensure this URL is accessible from payment gateway
});

// 3. Test callback endpoint manually
curl -X POST https://your-domain.com/payments/callbacks \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

// 4. Check firewall/nginx/load balancer
// Ensure POST requests to /payments/callbacks are allowed
```

#### 3. Ngrok Tunnel Issues

**Symptoms:**
- Ngrok tunnel fails to start
- Ngrok URL changes frequently

**Solutions:**
```typescript
// 1. Use environment variable for ngrok auth
process.env.NGROK_AUTHTOKEN = 'your_ngrok_auth_token';

const gateway = new ECPayPayment({
  withServer: 'ngrok',
});

// 2. Use static ngrok domain (paid feature)
const gateway = new ECPayPayment({
  withServer: 'ngrok',
  serverHost: 'your-static-subdomain.ngrok.io',
});

// 3. Check ngrok installation
// npm install @ngrok/ngrok
```

#### 4. Order ID Conflicts

**Symptoms:**
- Error: "Order ID already exists"
- Cannot create new orders

**Solutions:**
```typescript
// 1. Use unique order IDs
const order = await gateway.prepare({
  id: `ORDER-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
  items: [...],
});

// 2. Or let gateway auto-generate
const order = await gateway.prepare({
  // No id field - gateway generates unique ID
  items: [...],
});

// 3. Check for duplicate submissions
// Implement idempotency in your application
```

#### 5. Amount Mismatch

**Symptoms:**
- Payment amount different from expected
- Calculation errors

**Solutions:**
```typescript
// Check item calculation
const items = [
  { name: 'A', unitPrice: 100, quantity: 2 }, // 200
  { name: 'B', unitPrice: 50, quantity: 3 },  // 150
];
// Total: 350

const order = await gateway.prepare({ items });
console.log('Total Price:', order.totalPrice); // Should be 350

// Verify additionalInfo after payment
gateway.emitter.on(PaymentEvents.ORDER_COMMITTED, (order) => {
  console.log('Charged amount:', order.additionalInfo.amount);
  console.log('Expected amount:', order.totalPrice);

  if (order.additionalInfo.amount !== order.totalPrice) {
    console.error('Amount mismatch!');
  }
});
```

#### 6. Event Listeners Not Firing

**Symptoms:**
- PaymentEvents.ORDER_COMMITTED not triggered
- No event handlers executing

**Solutions:**
```typescript
// 1. Register listeners BEFORE calling prepare()
gateway.emitter.on(PaymentEvents.ORDER_COMMITTED, handler);
gateway.emitter.on(PaymentEvents.ORDER_FAILED, handler);

// Then create order
const order = await gateway.prepare({...});

// 2. Check emitter exists
if (!gateway.emitter) {
  console.error('Gateway has no emitter!');
}

// 3. Use once() for one-time events
gateway.emitter.once(PaymentEvents.ORDER_COMMITTED, handler);

// 4. Check for errors in handler
gateway.emitter.on(PaymentEvents.ORDER_COMMITTED, (order) => {
  try {
    // Your logic here
  } catch (error) {
    console.error('Handler error:', error);
  }
});
```

#### 7. Card Binding Failures

**Symptoms:**
- CARD_BINDING_FAILED event fires
- Cannot bind card

**Solutions:**
```typescript
// 1. Check memory setting
const gateway = new ECPayPayment({
  memory: false, // Must be false for binding
  // ...
});

// 2. Handle already-bound cards
gateway.emitter.on(PaymentEvents.CARD_BINDING_FAILED, (req) => {
  if (req.failedMessage?.code === '10100112') {
    console.log('Card already bound - this is OK');
    // Retrieve existing binding
  }
});

// 3. Use bindCardWithTransaction instead
gateway.emitter.on(PaymentEvents.ORDER_COMMITTED, async (order) => {
  const bindRequest = await gateway.bindCardWithTransaction(
    memberId,
    order.platformTradeNumber,
    order.id
  );
});
```

## CTBC Advanced Features (CTBC 進階功能)

### POS API Utility Functions

CTBC adapter exports utility functions for direct POS API operations:

```typescript
import {
  posApiQuery,
  posApiRefund,
  posApiCancelRefund,
  posApiReversal,
  posApiCapRev,
  posApiSmartCancelOrRefund,
  getPosNextActionFromInquiry,
  CTBCPosApiConfig,
} from '@rytass/payments-adapter-ctbc-micro-fast-pay';

// Configure POS API
const posConfig: CTBCPosApiConfig = {
  URL: 'https://ccapi.ctbcbank.com',
  MacKey: 'YOUR_MAC_KEY', // 8 or 24 characters
};

// Query transaction status
const queryResult = await posApiQuery(posConfig, {
  MERID: 'YOUR_MERID',
  'LID-M': 'ORDER-001',
  Tx_ATTRIBUTE: 'TX_AUTH', // TX_AUTH | TX_SETTLE | TX_VOID | TX_REFUND
});

// Smart cancel or refund (auto-determine action based on transaction state)
const { action, response, inquiry } = await posApiSmartCancelOrRefund(posConfig, {
  MERID: 'YOUR_MERID',
  'LID-M': 'ORDER-001',
  XID: 'TRANSACTION_XID',
  AuthCode: 'AUTH_CODE',
  OrgAmt: '1000',
  PurchAmt: '1000',
  currency: 'TWD',
  exponent: '0',
});

console.log('Action taken:', action); // 'Reversal' | 'CapRev' | 'Refund' | 'None' | 'Pending' | 'Failed'
```

### AMEX SOAP API Utility Functions

For American Express card processing:

```typescript
import {
  amexInquiry,
  amexRefund,
  amexCancelRefund,
  amexAuthRev,
  amexCapRev,
  amexSmartCancelOrRefund,
  getAmexNextActionFromInquiry,
  CTBCAmexConfig,
} from '@rytass/payments-adapter-ctbc-micro-fast-pay';

// Configure AMEX API
const amexConfig: CTBCAmexConfig = {
  wsdlUrl: 'https://amex.ctbcbank.com/wsdl',
  timeout: 30000,
  sslOptions: {
    rejectUnauthorized: true,
  },
};

// Query AMEX transaction
const amexResult = await amexInquiry(amexConfig, {
  merId: 'YOUR_MERID',
  lidm: 'ORDER-001',
  xid: 'TRANSACTION_XID',
  IN_MAC_KEY: 'YOUR_MAC_KEY',
});

// Smart cancel or refund for AMEX
const { action, response } = await amexSmartCancelOrRefund(amexConfig, {
  merId: 'YOUR_MERID',
  xid: 'TRANSACTION_XID',
  lidm: 'ORDER-001',
  purchAmt: 1000,
  orgAmt: 1000,
  IN_MAC_KEY: 'YOUR_MAC_KEY',
});
```

### CTBC Configuration Options

Complete configuration for CTBC gateway:

```typescript
interface CTBCPaymentOptions {
  merchantId: string;           // CTBC merchant ID
  merchantName?: string;        // Merchant display name
  merId: string;                // MER ID from CTBC
  txnKey: string;               // MAC/TXN key for encryption
  terminalId: string;           // Terminal ID
  baseUrl?: string;             // API base URL (default: https://ccapi.ctbcbank.com)
  isAmex?: boolean;             // Enable AMEX card support (uses SOAP API)

  // Server options
  withServer?: boolean | 'ngrok';
  serverHost?: string;
  callbackPath?: string;
  checkoutPath?: string;
  bindCardPath?: string;
  boundCardPath?: string;
  boundCardCheckoutResultPath?: string;

  // Cache options
  orderCache?: OrderCache;
  orderCacheTTL?: number;
  bindCardRequestsCache?: BindCardRequestCache;
  bindCardRequestsCacheTTL?: number;

  // Callbacks
  serverListener?: (req, res) => void;
  onServerListen?: () => void;
  onCommit?: (order) => void;
}
```

## Happy Card Advanced Features (統一禮物卡進階功能)

### Get Card Balance

Query card balance before making payment:

```typescript
import { HappyCardPayment, HappyCardRecordType } from '@rytass/payments-adapter-happy-card';

const gateway = new HappyCardPayment({
  cSource: process.env.HAPPY_CARD_C_SOURCE!,
  key: process.env.HAPPY_CARD_KEY!,
});

// Get total balance (sum of all records)
const [balance, productType] = await gateway.getCardBalance('HC1234567890123456', false);
console.log('Total balance:', balance);
console.log('Product type:', productType);

// Get detailed records
const [records, productType2] = await gateway.getCardBalance('HC1234567890123456', true);
records.forEach(record => {
  console.log(`Record ${record.id}: ${record.type === HappyCardRecordType.AMOUNT ? 'Amount' : 'Bonus'} = ${record.amount}`);
});
```

### Happy Card Enums

```typescript
// Record types
enum HappyCardRecordType {
  AMOUNT = 1,  // Cash value (現金價值)
  BONUS = 2,   // Bonus points (紅利點數)
}

// Product types
enum HappyCardProductType {
  INVOICE_FIRST_HAPPY_CARD_GF = '1',     // 發票先開禮物卡 GF
  INVOICE_LATER_HAPPY_CARD_GS = '2',     // 發票後開禮物卡 GS
  INVOICE_FIRST_DIGITAL_GIFT_GF = '3',   // 發票先開數位禮物 GF
  INVOICE_LATER_DIGITAL_GIFT_GS = '4',   // 發票後開數位禮物 GS
  INVOICE_FIRST_PHYSICAL_GIFT_GF = '5',  // 發票先開實體禮物 GF
  INVOICE_LATER_PHYSICAL_GIFT_GS = '6',  // 發票後開實體禮物 GS
}

// Result codes
enum HappyCardResultCode {
  FAILED = '0',
  SUCCESS = '1',
}

// Base URLs
enum HappyCardBaseUrls {
  PRODUCTION = 'https://prd-jp-posapi.azurewebsites.net/api/Pos',
  DEVELOPMENT = 'https://uat-pos-api.azurewebsites.net/api/Pos',
}
```

### Complete Happy Card Payment Flow

```typescript
import {
  HappyCardPayment,
  HappyCardRecordType,
  HappyCardBaseUrls,
} from '@rytass/payments-adapter-happy-card';

const gateway = new HappyCardPayment({
  baseUrl: HappyCardBaseUrls.PRODUCTION,
  cSource: process.env.HAPPY_CARD_C_SOURCE!,
  key: process.env.HAPPY_CARD_KEY!,
});

// Step 1: Check card balance and get records
const [records, productType] = await gateway.getCardBalance('HC1234567890123456', true);
console.log('Available records:', records);

// Step 2: Prepare payment with specific records
const order = await gateway.prepare({
  id: 'ORDER-001',
  cardSerial: 'HC1234567890123456',
  items: [
    { name: 'Coffee', unitPrice: 120, quantity: 1 },
    { name: 'Cake', unitPrice: 180, quantity: 1 },
  ],
  useRecords: [
    { id: records[0].id, type: HappyCardRecordType.AMOUNT, amount: 200 },
    { id: records[1].id, type: HappyCardRecordType.BONUS, amount: 100 },
  ],
  posTradeNo: 'POS001', // Optional, max 6 chars
  uniMemberGID: 'MEMBER_GID', // Optional unified member ID
  isIsland: false, // true for offshore islands (離島)
});

// Step 3: Commit the payment
await order.commit();
console.log('Payment successful');
```

## HwaNan Bank Advanced Features (華南銀行進階功能)

### Installment Payments

HwaNan supports installment payments (分期付款):

```typescript
import {
  HwaNanPayment,
  HwaNanTransactionType,
  HwaNanAutoCapMode,
  HwaNanCustomizePageType,
} from '@rytass/payments-adapter-hwanan';

const gateway = new HwaNanPayment({
  merchantId: process.env.HWANAN_MERCHANT_ID!,
  terminalId: process.env.HWANAN_TERMINAL_ID!,
  merID: process.env.HWANAN_MER_ID!,
  identifier: process.env.HWANAN_IDENTIFIER!,
  merchantName: 'My Store',
  withServer: true,
});

// The order payload includes installment configuration
// txType: HwaNanTransactionType.INSTALLMENTS (1)
// NumberOfPay: Number of installments (minimum 3)
```

### HwaNan Enums

```typescript
// Transaction types
enum HwaNanTransactionType {
  ONE_TIME = 0,      // 一次付清
  INSTALLMENTS = 1,  // 分期付款
}

// Auto capture mode
enum HwaNanAutoCapMode {
  MANUALLY = 0,  // 手動請款
  AUTO = 1,      // 自動請款
}

// Customize page language
enum HwaNanCustomizePageType {
  ZH_TW = 1,  // 繁體中文
  ZH_CN = 2,  // 簡體中文
  EN_US = 3,  // English
  JA_JP = 4,  // 日本語
  OTHER = 5,  // 其他
}

// Payment channel (currently only credit card)
enum HwaNanPaymentChannel {
  CREDIT = 1,
}
```

### HwaNan Configuration Options

```typescript
interface HwaNanPaymentInitOptions {
  merchantId: string;           // 商店代碼
  terminalId: string;           // 端末機代碼
  merchantName: string;         // 商店名稱
  merID: string;                // MER ID
  identifier: string;           // 識別碼 (用於產生 checkValue)
  baseUrl?: string;             // API base URL
  customizePageType?: HwaNanCustomizePageType;  // 頁面語言
  customizePageVersion?: string;                // 頁面版本

  // Server options
  serverHost?: string;
  callbackPath?: string;
  checkoutPath?: string;
  withServer?: boolean | 'ngrok';
  ttl?: number;                 // Order TTL in ms

  // Callbacks
  serverListener?: (req, res) => void;
  onCommit?: (order) => void;
  onServerListen?: () => void;

  // Cache
  ordersCache?: OrdersCache;
}
```

## Detailed Documentation

For complete API reference and advanced usage:

- [ECPay Adapter Reference](ECPAY.md)
- [NewebPay Adapter Reference](NEWEBPAY.md)
- [HwaNan Bank Adapter Reference](HWANAN.md)
- [CTBC Adapter Reference](CTBC.md)
- [iCash Pay Adapter Reference](ICASH-PAY.md)
- [Happy Card Adapter Reference](HAPPY-CARD.md)
