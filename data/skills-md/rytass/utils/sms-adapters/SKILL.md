---
name: sms-adapters
description: Taiwan SMS integration (台灣簡訊整合). Use when working with Every8D (每日簡訊 / 互動資通) or other Taiwan SMS service providers. Covers single SMS (單則簡訊), batch messaging (批次發送), multi-target messaging (多目標發送), Taiwan mobile number validation (台灣手機號碼驗證), delivery tracking (發送追蹤), and NestJS integration. Keywords - SMS, 簡訊, Every8D, 每日簡訊, 互動資通, Interactive Communications, mobile number, 手機號碼, batch send, 批次發送, message delivery, 訊息發送
---

# Taiwan SMS Adapters

This skill provides comprehensive guidance for using `@rytass/sms-adapter-*` packages to integrate Taiwan SMS service providers.

## Overview

All adapters implement the `SMSService` interface from `@rytass/sms`, providing a unified API across different providers:

| Package | Provider | Description |
|---------|----------|-------------|
| `@rytass/sms-adapter-every8d` | Every8D (每日簡訊 / 互動資通) | Taiwan SMS gateway by Interactive Communications |

### Base Interface (@rytass/sms)

All adapters share these core concepts:

**SMSService** - Main interface for SMS operations:
```typescript
interface SMSService<
  Request extends SMSRequest,
  SendResponse extends SMSSendResponse,
  MultiTarget extends MultiTargetRequest,
> {
  send(request: Request[]): Promise<SendResponse[]>;
  send(request: Request): Promise<SendResponse>;
  send(request: MultiTarget): Promise<SendResponse[]>;
}
```

**Request Types**:
- `SMSRequest` - Single SMS message to one recipient
- `MultiTargetRequest` - Same message to multiple recipients

**Response Status**:
- `SUCCESS` - Message sent successfully
- `FAILED` - Message delivery failed

**Taiwan Phone Number Helpers** (from `@rytass/sms`):
```typescript
// 台灣手機號碼正規表達式
const TAIWAN_PHONE_NUMBER_RE = /^(0|\+?886-?)9\d{2}-?\d{3}-?\d{3}$/;

// 正規化台灣手機號碼（移除非數字字元，將 886 前綴轉為 0）
function normalizedTaiwanMobilePhoneNumber(mobile: string): string;
// '0987-654-321' → '0987654321'
// '+886987654321' → '0987654321'
// '886987654321' → '0987654321'
```

## Installation

```bash
# Install base package
npm install @rytass/sms

# Choose the adapter for your provider
npm install @rytass/sms-adapter-every8d
```

## Quick Start

### Every8D (每日簡訊 / 互動資通)

```typescript
import { SMSServiceEvery8D } from '@rytass/sms-adapter-every8d';

// Initialize SMS service
const smsService = new SMSServiceEvery8D({
  username: process.env.EVERY8D_USERNAME!,
  password: process.env.EVERY8D_PASSWORD!,
  baseUrl: 'https://api.e8d.tw', // Default API endpoint
  onlyTaiwanMobileNumber: true, // Restrict to Taiwan numbers only
});

// Send single SMS
const result = await smsService.send({
  mobile: '0987654321',
  text: 'Hello! This is a test message.',
});

console.log('Message ID:', result.messageId);
console.log('Status:', result.status);
console.log('Mobile:', result.mobile);
```

## Common Usage Patterns

### Single SMS Delivery

Send a message to a single recipient:

```typescript
// Basic single SMS
const result = await smsService.send({
  mobile: '0987654321',
  text: 'Your verification code is 123456',
});

// Check delivery status
if (result.status === SMSRequestResult.SUCCESS) {
  console.log('SMS sent successfully!');
  console.log('Message ID:', result.messageId);
  console.log('Recipient:', result.mobile);
} else {
  console.error('SMS delivery failed');
  console.error('Error Code:', result.errorCode);
  console.error('Error Message:', result.errorMessage);
}
```

### Batch Messaging (Same Message to Multiple Recipients)

Send the same message to multiple recipients efficiently:

```typescript
// Batch send with same message
const results = await smsService.send({
  mobileList: [
    '0987654321',
    '0912345678',
    '0923456789',
    '0934567890'
  ],
  text: 'Important notification: Your order has been shipped!',
});

// Process results
console.log(`Total sent: ${results.length}`);

const successful = results.filter(r => r.status === SMSRequestResult.SUCCESS);
const failed = results.filter(r => r.status === SMSRequestResult.FAILED);

console.log(`Successful: ${successful.length}`);
console.log(`Failed: ${failed.length}`);

// Log failed deliveries
failed.forEach(result => {
  console.error(`Failed to send to ${result.mobile}:`, result.errorMessage);
});
```

### Multi-Target Messaging (Different Messages)

Send different messages to different recipients:

```typescript
// Send different messages to each recipient
const results = await smsService.send([
  {
    mobile: '0987654321',
    text: 'Dear John, your appointment is confirmed for tomorrow at 10 AM.',
  },
  {
    mobile: '0912345678',
    text: 'Hi Mary, your package will arrive today between 2-4 PM.',
  },
  {
    mobile: '0923456789',
    text: 'Hello Mike, thank you for your purchase! Your receipt is attached.',
  },
]);

// Check each result
results.forEach((result, index) => {
  console.log(`Message ${index + 1} to ${result.mobile}: ${result.status}`);

  if (result.status === SMSRequestResult.SUCCESS) {
    console.log(`  Message ID: ${result.messageId}`);
  } else {
    console.error(`  Error: ${result.errorMessage}`);
  }
});
```

## Taiwan Mobile Number Handling

### Automatic Number Normalization

The adapter automatically normalizes Taiwan mobile numbers:

```typescript
// All these formats are normalized to 0987654321
const validFormats = [
  '0987654321',       // Standard format
  '0987-654-321',     // With dashes
  '+886987654321',    // International format
  '886987654321',     // International without +
  '+886-987654321',   // International with dash after country code
];

// All will be normalized and send successfully
for (const number of validFormats) {
  const result = await smsService.send({
    mobile: number,
    text: 'Test message',
  });

  // Result.mobile will always be '0987654321'
  console.log('Normalized number:', result.mobile);
}
```

### Number Validation

Validate Taiwan mobile numbers with strict mode:

```typescript
// Enable Taiwan-only validation
const strictService = new SMSServiceEvery8D({
  username: process.env.EVERY8D_USERNAME!,
  password: process.env.EVERY8D_PASSWORD!,
  onlyTaiwanMobileNumber: true, // Enable strict validation
});

try {
  // This will work - valid Taiwan mobile number
  await strictService.send({
    mobile: '0987654321', // Taiwan number (09xxxxxxxx)
    text: 'Valid Taiwan number',
  });

  // This will throw error - international number
  await strictService.send({
    mobile: '+1234567890', // Non-Taiwan number
    text: 'Invalid for Taiwan-only mode',
  });
} catch (error) {
  console.error('Number validation error:', error.message);
  // Error: +1234567890 is not taiwan mobile phone (`onlyTaiwanMobileNumber` option is true)
}

// Taiwan number format requirements:
// - Must start with 09 (or +8869, 8869)
// - Total 10 digits after country code
// - Examples: 0912345678, 0923456789, 0987654321
```

### International Numbers

Send to international numbers when validation is disabled:

```typescript
// Allow international numbers
const globalService = new SMSServiceEvery8D({
  username: process.env.EVERY8D_USERNAME!,
  password: process.env.EVERY8D_PASSWORD!,
  onlyTaiwanMobileNumber: false, // Default: allow all numbers
});

// Send to various countries
const results = await globalService.send([
  { mobile: '0987654321', text: 'Taiwan message' },        // Taiwan
  { mobile: '+85298765432', text: 'Hong Kong message' },   // Hong Kong
  { mobile: '+60123456789', text: 'Malaysia message' },    // Malaysia
  { mobile: '+6591234567', text: 'Singapore message' },    // Singapore
]);

// Note: Check with Every8D for international coverage and rates
```

## Integration Examples

### E-commerce Order Notifications

```typescript
import { SMSServiceEvery8D } from '@rytass/sms-adapter-every8d';
import { SMSRequestResult } from '@rytass/sms';

class OrderNotificationService {
  private smsService: SMSServiceEvery8D;

  constructor() {
    this.smsService = new SMSServiceEvery8D({
      username: process.env.EVERY8D_USERNAME!,
      password: process.env.EVERY8D_PASSWORD!,
      onlyTaiwanMobileNumber: true,
    });
  }

  /**
   * Send order confirmation SMS
   * @param order - Order object with customer details
   * @returns SMS delivery result
   */
  async sendOrderConfirmation(order: {
    id: string;
    customerPhone: string;
    total: number;
    deliveryDate: string;
    trackingUrl: string;
  }): Promise<boolean> {
    const message = `
訂單已確認！
訂單編號：${order.id}
金額：NT$${order.total}
預計送達：${order.deliveryDate}
追蹤連結：${order.trackingUrl}
    `.trim();

    const result = await this.smsService.send({
      mobile: order.customerPhone,
      text: message,
    });

    return result.status === SMSRequestResult.SUCCESS;
  }

  /**
   * Send shipping notification
   * @param order - Order object with tracking number
   * @returns SMS delivery result
   */
  async sendShippingNotification(order: {
    id: string;
    customerPhone: string;
    trackingNumber: string;
  }): Promise<boolean> {
    const message = `您的訂單 #${order.id} 已出貨！追蹤號碼：${order.trackingNumber}`;

    const result = await this.smsService.send({
      mobile: order.customerPhone,
      text: message,
    });

    if (result.status === SMSRequestResult.FAILED) {
      console.error('Failed to send shipping notification:', {
        orderId: order.id,
        errorCode: result.errorCode,
        errorMessage: result.errorMessage,
      });
    }

    return result.status === SMSRequestResult.SUCCESS;
  }

  /**
   * Send delivery notification to multiple orders
   * @param orders - Array of orders ready for delivery
   * @returns Delivery statistics
   */
  async sendBulkDeliveryNotifications(orders: Array<{
    id: string;
    customerPhone: string;
  }>): Promise<{
    total: number;
    successful: number;
    failed: number;
  }> {
    const results = await this.smsService.send(
      orders.map(order => ({
        mobile: order.customerPhone,
        text: `您的訂單 #${order.id} 將於今日送達，請留意收件。`,
      }))
    );

    const successful = results.filter(r => r.status === SMSRequestResult.SUCCESS).length;
    const failed = results.filter(r => r.status === SMSRequestResult.FAILED).length;

    return {
      total: results.length,
      successful,
      failed,
    };
  }
}
```

### Authentication & Verification

```typescript
import { SMSServiceEvery8D } from '@rytass/sms-adapter-every8d';
import { SMSRequestResult } from '@rytass/sms';

class AuthSMSService {
  private smsService: SMSServiceEvery8D;

  constructor() {
    this.smsService = new SMSServiceEvery8D({
      username: process.env.EVERY8D_USERNAME!,
      password: process.env.EVERY8D_PASSWORD!,
      onlyTaiwanMobileNumber: true,
    });
  }

  /**
   * Generate and send verification code
   * @param phoneNumber - Recipient phone number
   * @returns Verification code (store in cache/database)
   */
  async sendVerificationCode(phoneNumber: string): Promise<string> {
    // Generate 6-digit code
    const code = Math.random().toString().slice(-6);

    const message = `您的驗證碼是 ${code}，10 分鐘內有效。請勿將此驗證碼告知他人。`;

    const result = await this.smsService.send({
      mobile: phoneNumber,
      text: message,
    });

    if (result.status === SMSRequestResult.SUCCESS) {
      // Store code in Redis/cache with 10-minute expiration
      await this.storeVerificationCode(phoneNumber, code, 600);
      console.log('Verification code sent:', result.messageId);
      return code;
    } else {
      throw new Error(`SMS delivery failed: ${result.errorMessage}`);
    }
  }

  /**
   * Send 2FA code for login
   * @param phoneNumber - User's phone number
   * @param serviceName - Name of the service for branding
   * @returns void
   */
  async send2FACode(
    phoneNumber: string,
    serviceName: string
  ): Promise<void> {
    const code = Math.random().toString().slice(-6);

    const message = `${serviceName} 登入驗證碼：${code}，5 分鐘內有效。`;

    const result = await this.smsService.send({
      mobile: phoneNumber,
      text: message,
    });

    if (result.status === SMSRequestResult.SUCCESS) {
      await this.store2FACode(phoneNumber, code, 300); // 5 minutes
    } else {
      throw new Error(`Failed to send 2FA code: ${result.errorMessage}`);
    }
  }

  /**
   * Send password reset link
   * @param phoneNumber - User's phone number
   * @param resetLink - Password reset URL
   * @returns SMS delivery result
   */
  async sendPasswordResetLink(
    phoneNumber: string,
    resetLink: string
  ): Promise<boolean> {
    const message = `密碼重設連結：${resetLink}。此連結將在 30 分鐘後失效。`;

    const result = await this.smsService.send({
      mobile: phoneNumber,
      text: message,
    });

    return result.status === SMSRequestResult.SUCCESS;
  }

  private async storeVerificationCode(
    phone: string,
    code: string,
    expirationSeconds: number
  ): Promise<void> {
    // Implementation depends on your storage solution
    // Redis, database, or in-memory cache
    // Example with Redis:
    // await redis.setex(`verification:${phone}`, expirationSeconds, code);
  }

  private async store2FACode(
    phone: string,
    code: string,
    expirationSeconds: number
  ): Promise<void> {
    // Store with shorter expiration for 2FA
    // await redis.setex(`2fa:${phone}`, expirationSeconds, code);
  }
}
```

### Marketing Campaign Service

```typescript
import { SMSServiceEvery8D } from '@rytass/sms-adapter-every8d';
import { SMSRequestResult } from '@rytass/sms';

class MarketingCampaignService {
  private smsService: SMSServiceEvery8D;

  constructor() {
    this.smsService = new SMSServiceEvery8D({
      username: process.env.EVERY8D_USERNAME!,
      password: process.env.EVERY8D_PASSWORD!,
      onlyTaiwanMobileNumber: true,
    });
  }

  /**
   * Send promotional campaign to customers
   * @param customers - Customer list with phone numbers
   * @param campaignMessage - Campaign message text
   * @returns Campaign statistics
   */
  async sendPromotionalCampaign(
    customers: Array<{ phoneNumber: string; name: string }>,
    campaignMessage: string
  ): Promise<{
    total: number;
    successful: number;
    failed: number;
    successRate: number;
  }> {
    // Split into batches to avoid rate limiting
    const batchSize = 100;
    const batches: Array<typeof customers> = [];

    for (let i = 0; i < customers.length; i += batchSize) {
      batches.push(customers.slice(i, i + batchSize));
    }

    const allResults = [];

    for (const batch of batches) {
      const phoneNumbers = batch.map(customer => customer.phoneNumber);

      try {
        const batchResult = await this.smsService.send({
          mobileList: phoneNumbers,
          text: campaignMessage,
        });

        allResults.push(...batchResult);

        // Add delay between batches to respect rate limits
        await this.delay(1000); // 1 second delay
      } catch (error) {
        console.error('Batch failed:', error);

        // Add failed entries for this batch
        phoneNumbers.forEach(phone => {
          allResults.push({
            mobile: phone,
            status: SMSRequestResult.FAILED,
            errorMessage: 'Batch processing error',
          });
        });
      }
    }

    return this.analyzeCampaignResults(allResults);
  }

  /**
   * Send personalized messages to customers
   * @param customers - Customer list with personalized data
   * @returns Campaign statistics
   */
  async sendPersonalizedCampaign(
    customers: Array<{
      phoneNumber: string;
      name: string;
      customMessage: string;
    }>
  ): Promise<{
    total: number;
    successful: number;
    failed: number;
    successRate: number;
  }> {
    const results = await this.smsService.send(
      customers.map(customer => ({
        mobile: customer.phoneNumber,
        text: customer.customMessage,
      }))
    );

    return this.analyzeCampaignResults(results);
  }

  /**
   * Delay helper for rate limiting
   * @param ms - Milliseconds to delay
   * @returns Promise that resolves after delay
   */
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Analyze campaign results
   * @param results - Array of SMS send results
   * @returns Campaign statistics
   */
  private analyzeCampaignResults(
    results: Array<{ status: SMSRequestResult; mobile: string }>
  ): {
    total: number;
    successful: number;
    failed: number;
    successRate: number;
  } {
    const successful = results.filter(
      r => r.status === SMSRequestResult.SUCCESS
    ).length;
    const failed = results.filter(
      r => r.status === SMSRequestResult.FAILED
    ).length;

    return {
      total: results.length,
      successful,
      failed,
      successRate: (successful / results.length) * 100,
    };
  }
}
```

### Appointment Reminders

```typescript
import { SMSServiceEvery8D } from '@rytass/sms-adapter-every8d';
import { SMSRequestResult } from '@rytass/sms';

class AppointmentReminderService {
  private smsService: SMSServiceEvery8D;

  constructor() {
    this.smsService = new SMSServiceEvery8D({
      username: process.env.EVERY8D_USERNAME!,
      password: process.env.EVERY8D_PASSWORD!,
      onlyTaiwanMobileNumber: true,
    });
  }

  /**
   * Send appointment reminder
   * @param appointment - Appointment details
   * @returns SMS delivery result
   */
  async sendAppointmentReminder(appointment: {
    customerPhone: string;
    customerName: string;
    date: string;
    time: string;
    location: string;
    doctorName?: string;
  }): Promise<boolean> {
    const message = appointment.doctorName
      ? `親愛的 ${appointment.customerName}，提醒您與 ${appointment.doctorName} 醫師的預約：${appointment.date} ${appointment.time}，地點：${appointment.location}。請提前 10 分鐘報到。`
      : `親愛的 ${appointment.customerName}，提醒您的預約：${appointment.date} ${appointment.time}，地點：${appointment.location}。請提前 10 分鐘報到。`;

    const result = await this.smsService.send({
      mobile: appointment.customerPhone,
      text: message,
    });

    return result.status === SMSRequestResult.SUCCESS;
  }

  /**
   * Send batch appointment reminders
   * @param appointments - Array of appointments
   * @returns Statistics of sent reminders
   */
  async sendBatchReminders(
    appointments: Array<{
      customerPhone: string;
      date: string;
      time: string;
    }>
  ): Promise<{
    total: number;
    sent: number;
    failed: number;
  }> {
    const results = await this.smsService.send(
      appointments.map(apt => ({
        mobile: apt.customerPhone,
        text: `預約提醒：${apt.date} ${apt.time}。請準時出席，如需取消請提前通知。`,
      }))
    );

    const sent = results.filter(
      r => r.status === SMSRequestResult.SUCCESS
    ).length;
    const failed = results.filter(
      r => r.status === SMSRequestResult.FAILED
    ).length;

    return {
      total: results.length,
      sent,
      failed,
    };
  }
}
```

## NestJS Integration

### Basic Setup

```typescript
// sms.module.ts
import { Module, Global } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { SMSServiceEvery8D } from '@rytass/sms-adapter-every8d';

export const SMS_SERVICE = Symbol('SMS_SERVICE');

@Global()
@Module({
  imports: [ConfigModule],
  providers: [
    {
      provide: SMS_SERVICE,
      useFactory: (config: ConfigService) => {
        return new SMSServiceEvery8D({
          username: config.get('EVERY8D_USERNAME')!,
          password: config.get('EVERY8D_PASSWORD')!,
          onlyTaiwanMobileNumber: config.get('EVERY8D_TAIWAN_ONLY') === 'true',
        });
      },
      inject: [ConfigService],
    },
  ],
  exports: [SMS_SERVICE],
})
export class SMSModule {}
```

### Using in Services

```typescript
// notification.service.ts
import { Injectable, Inject, Logger } from '@nestjs/common';
import { SMSServiceEvery8D } from '@rytass/sms-adapter-every8d';
import { SMSRequestResult } from '@rytass/sms';
import { SMS_SERVICE } from './sms.module';

@Injectable()
export class NotificationService {
  private readonly logger = new Logger(NotificationService.name);

  constructor(
    @Inject(SMS_SERVICE)
    private readonly smsService: SMSServiceEvery8D,
  ) {}

  /**
   * Send verification code via SMS
   * @param phoneNumber - Recipient phone number
   * @param code - Verification code
   * @returns Whether SMS was sent successfully
   */
  async sendVerificationCode(
    phoneNumber: string,
    code: string,
  ): Promise<boolean> {
    try {
      const result = await this.smsService.send({
        mobile: phoneNumber,
        text: `您的驗證碼是 ${code}，10 分鐘內有效。`,
      });

      if (result.status === SMSRequestResult.SUCCESS) {
        this.logger.log(`Verification code sent to ${phoneNumber}`);
        return true;
      } else {
        this.logger.error(
          `Failed to send verification code to ${phoneNumber}: ${result.errorMessage}`,
        );
        return false;
      }
    } catch (error) {
      this.logger.error('SMS sending error:', error);
      return false;
    }
  }

  /**
   * Send bulk notification
   * @param phoneNumbers - Array of recipient phone numbers
   * @param message - Message to send
   * @returns Statistics of sent messages
   */
  async sendBulkNotification(
    phoneNumbers: string[],
    message: string,
  ): Promise<{
    total: number;
    successful: number;
    failed: number;
  }> {
    try {
      const results = await this.smsService.send({
        mobileList: phoneNumbers,
        text: message,
      });

      const successful = results.filter(
        r => r.status === SMSRequestResult.SUCCESS,
      ).length;
      const failed = results.filter(
        r => r.status === SMSRequestResult.FAILED,
      ).length;

      this.logger.log(
        `Bulk notification sent: ${successful} successful, ${failed} failed`,
      );

      return {
        total: results.length,
        successful,
        failed,
      };
    } catch (error) {
      this.logger.error('Bulk SMS sending error:', error);
      throw error;
    }
  }
}
```

### Usage in Controllers

```typescript
// notification.controller.ts
import { Controller, Post, Body } from '@nestjs/common';
import { NotificationService } from './notification.service';

@Controller('notifications')
export class NotificationController {
  constructor(private readonly notificationService: NotificationService) {}

  @Post('send-verification')
  async sendVerification(
    @Body() body: { phoneNumber: string; code: string },
  ): Promise<{ success: boolean }> {
    const success = await this.notificationService.sendVerificationCode(
      body.phoneNumber,
      body.code,
    );

    return { success };
  }

  @Post('send-bulk')
  async sendBulk(
    @Body() body: { phoneNumbers: string[]; message: string },
  ): Promise<{
    total: number;
    successful: number;
    failed: number;
  }> {
    return await this.notificationService.sendBulkNotification(
      body.phoneNumbers,
      body.message,
    );
  }
}
```

## Configuration

### Environment Variables

```bash
# .env
EVERY8D_USERNAME=your_every8d_username
EVERY8D_PASSWORD=your_every8d_password
EVERY8D_BASE_URL=https://api.e8d.tw
EVERY8D_TAIWAN_ONLY=true
```

### TypeScript Configuration

```typescript
// config.ts
export interface SMSConfig {
  username: string;
  password: string;
  baseUrl?: string;
  onlyTaiwanMobileNumber?: boolean;
}

export const smsConfig: SMSConfig = {
  username: process.env.EVERY8D_USERNAME!,
  password: process.env.EVERY8D_PASSWORD!,
  baseUrl: process.env.EVERY8D_BASE_URL || 'https://api.e8d.tw',
  onlyTaiwanMobileNumber: process.env.EVERY8D_TAIWAN_ONLY === 'true',
};
```

## Error Handling

### Handling Delivery Failures

```typescript
import { SMSServiceEvery8D } from '@rytass/sms-adapter-every8d';
import { SMSRequestResult } from '@rytass/sms';
import { Every8DError } from '@rytass/sms-adapter-every8d';

async function sendWithRetry(
  smsService: SMSServiceEvery8D,
  mobile: string,
  text: string,
  maxRetries: number = 3
): Promise<boolean> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await smsService.send({ mobile, text });

      if (result.status === SMSRequestResult.SUCCESS) {
        console.log(`SMS sent successfully on attempt ${attempt}`);
        return true;
      }

      // Check error code
      if (result.errorCode === Every8DError.FORMAT_ERROR) {
        console.error('Invalid format - no retry needed');
        return false;
      }

      console.warn(`Attempt ${attempt} failed:`, result.errorMessage);

      if (attempt < maxRetries) {
        // Wait before retry (exponential backoff)
        await new Promise(resolve =>
          setTimeout(resolve, Math.pow(2, attempt) * 1000)
        );
      }
    } catch (error) {
      console.error(`Attempt ${attempt} error:`, error);

      if (attempt === maxRetries) {
        throw error;
      }
    }
  }

  return false;
}
```

### Batch Error Handling

```typescript
async function sendBatchWithErrorHandling(
  smsService: SMSServiceEvery8D,
  phoneNumbers: string[],
  message: string
): Promise<{
  successful: string[];
  failed: Array<{ phone: string; error: string }>;
}> {
  const results = await smsService.send({
    mobileList: phoneNumbers,
    text: message,
  });

  const successful: string[] = [];
  const failed: Array<{ phone: string; error: string }> = [];

  results.forEach(result => {
    if (result.status === SMSRequestResult.SUCCESS) {
      successful.push(result.mobile);
    } else {
      failed.push({
        phone: result.mobile,
        error: result.errorMessage || 'Unknown error',
      });
    }
  });

  // Log failures
  if (failed.length > 0) {
    console.error('Failed deliveries:', failed);
  }

  return { successful, failed };
}
```

## Best Practices

### Message Content

```typescript
class MessageTemplates {
  /**
   * Verification code template
   * - Keep message under 70 characters for single SMS
   * - Include expiration time
   * - Add security warning
   */
  static verification(code: string): string {
    return `您的驗證碼是 ${code}，10 分鐘內有效。請勿將此驗證碼告知他人。`;
  }

  /**
   * Order confirmation template
   * - Include order number for reference
   * - Keep essential info only
   */
  static orderConfirmation(orderNumber: string, amount: number): string {
    return `訂單 ${orderNumber} 已確認。金額：NT$${amount}。感謝您的購買！`;
  }

  /**
   * Appointment reminder template
   * - Include date, time, and location
   * - Add action instructions
   */
  static appointmentReminder(date: string, time: string): string {
    return `預約提醒：${date} ${time}。請提前 10 分鐘報到。如需取消請來電。`;
  }

  /**
   * Marketing campaign template
   * - Include opt-out instructions for compliance
   * - Keep under 70 characters if possible
   */
  static promotion(discount: string): string {
    return `限時優惠！${discount} 折扣活動進行中。查看詳情：[連結]。回 N 取消訂閱。`;
  }
}
```

### Security

```typescript
// 1. Store credentials securely
// ❌ Don't hardcode credentials
const badService = new SMSServiceEvery8D({
  username: 'myusername',
  password: 'mypassword',
});

// ✅ Use environment variables
const goodService = new SMSServiceEvery8D({
  username: process.env.EVERY8D_USERNAME!,
  password: process.env.EVERY8D_PASSWORD!,
});

// 2. Validate phone numbers before sending
function isValidTaiwanMobile(phone: string): boolean {
  const cleaned = phone.replace(/[^0-9]/g, '').replace(/^886/, '0');
  return /^09\d{8}$/.test(cleaned);
}

// 3. Implement rate limiting
class RateLimitedSMSService {
  private lastSendTime = 0;
  private minInterval = 1000; // 1 second between sends

  async send(smsService: SMSServiceEvery8D, data: any) {
    const now = Date.now();
    const timeSinceLastSend = now - this.lastSendTime;

    if (timeSinceLastSend < this.minInterval) {
      await new Promise(resolve =>
        setTimeout(resolve, this.minInterval - timeSinceLastSend)
      );
    }

    const result = await smsService.send(data);
    this.lastSendTime = Date.now();

    return result;
  }
}

// 4. Log all SMS activities for audit
async function sendWithAuditLog(
  smsService: SMSServiceEvery8D,
  mobile: string,
  text: string,
  userId?: string
): Promise<void> {
  const auditEntry = {
    timestamp: new Date(),
    userId,
    recipient: mobile,
    messageLength: text.length,
    action: 'SMS_SEND',
  };

  try {
    const result = await smsService.send({ mobile, text });

    await logAudit({
      ...auditEntry,
      status: result.status,
      messageId: result.messageId,
    });
  } catch (error) {
    await logAudit({
      ...auditEntry,
      status: 'ERROR',
      error: error.message,
    });
    throw error;
  }
}

async function logAudit(entry: any): Promise<void> {
  // Save to database or logging service
}
```

### Performance

```typescript
// 1. Batch messages efficiently
// ❌ Don't send one by one
async function inefficientSend(phones: string[], message: string) {
  for (const phone of phones) {
    await smsService.send({ mobile: phone, text: message });
  }
}

// ✅ Use batch send
async function efficientSend(phones: string[], message: string) {
  await smsService.send({ mobileList: phones, text: message });
}

// 2. Handle large batches with chunking
async function sendLargeBatch(
  smsService: SMSServiceEvery8D,
  phones: string[],
  message: string,
  chunkSize: number = 100
): Promise<void> {
  for (let i = 0; i < phones.length; i += chunkSize) {
    const chunk = phones.slice(i, i + chunkSize);

    await smsService.send({
      mobileList: chunk,
      text: message,
    });

    // Add delay between chunks
    if (i + chunkSize < phones.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
}
```

### Compliance

```typescript
// 1. Respect user preferences and opt-out requests
interface UserSMSPreference {
  phoneNumber: string;
  optedOut: boolean;
  marketingConsent: boolean;
  transactionalOnly: boolean;
}

async function sendRespectingPreferences(
  smsService: SMSServiceEvery8D,
  user: UserSMSPreference,
  message: string,
  messageType: 'marketing' | 'transactional'
): Promise<boolean> {
  // Check if user opted out completely
  if (user.optedOut) {
    console.log('User opted out - skipping SMS');
    return false;
  }

  // Check marketing consent
  if (messageType === 'marketing' && !user.marketingConsent) {
    console.log('No marketing consent - skipping SMS');
    return false;
  }

  // Send the message
  const result = await smsService.send({
    mobile: user.phoneNumber,
    text: message,
  });

  return result.status === SMSRequestResult.SUCCESS;
}

// 2. Include opt-out instructions in marketing messages
function createMarketingMessage(content: string): string {
  return `${content}\n\n回覆 N 取消訂閱簡訊通知。`;
}

// 3. Maintain do-not-contact list
class DoNotContactList {
  private blockedNumbers = new Set<string>();

  async add(phoneNumber: string): Promise<void> {
    this.blockedNumbers.add(phoneNumber);
    // Persist to database
  }

  async remove(phoneNumber: string): Promise<void> {
    this.blockedNumbers.delete(phoneNumber);
    // Update database
  }

  isBlocked(phoneNumber: string): boolean {
    return this.blockedNumbers.has(phoneNumber);
  }

  async filterAllowed(phoneNumbers: string[]): Promise<string[]> {
    return phoneNumbers.filter(phone => !this.isBlocked(phone));
  }
}
```

## Internal Implementation Details

### Empty Target Handling

傳入空陣列或空 mobileList 會拋出錯誤：

```typescript
// 以下情況會拋出 'No target provided.' 錯誤
await smsService.send([]);  // 空陣列
await smsService.send({ mobileList: [], text: 'Test' });  // 空 mobileList
```

### Batch Message Optimization

相同訊息內容的多個請求會自動合併為單一 API 呼叫，提高發送效率：

```typescript
// 這三個請求會合併成一個 API 呼叫
const results = await smsService.send([
  { mobile: '0912345678', text: 'Hello' },
  { mobile: '0923456789', text: 'Hello' },  // 相同訊息
  { mobile: '0934567890', text: 'Hello' },  // 相同訊息
]);
// 內部會將 DEST 參數合併為 '0912345678,0923456789,0934567890'
```

### Partial Delivery Failure Handling

當部分發送失敗時，API 回傳 `unsend` 數量，系統會從列表末端開始標記失敗：

```typescript
// 假設發送 5 個號碼，API 回傳 unsend=2
// 則前 3 個標記為 SUCCESS，後 2 個標記為 FAILED
const results = await smsService.send({
  mobileList: ['0911...', '0922...', '0933...', '0944...', '0955...'],
  text: 'Test',
});
// results[0..2].status === SMSRequestResult.SUCCESS
// results[3..4].status === SMSRequestResult.FAILED
```

## Troubleshooting

### Common Issues

#### 1. Authentication Failure

**Symptoms:**
- All messages fail to send
- Error message about credentials

**Solutions:**
```typescript
// Check credentials
console.log('Username:', process.env.EVERY8D_USERNAME);
console.log('Password length:', process.env.EVERY8D_PASSWORD?.length);

// Ensure no extra spaces in .env
EVERY8D_USERNAME=your_username  # ❌ Trailing space
EVERY8D_USERNAME=your_username   # ✅ No space

// Test with minimal code
const testService = new SMSServiceEvery8D({
  username: 'YOUR_USERNAME',
  password: 'YOUR_PASSWORD',
});

const result = await testService.send({
  mobile: '0987654321',
  text: 'Test',
});

console.log('Result:', result);
```

#### 2. Invalid Phone Number Format

**Symptoms:**
- FORMAT_ERROR (-306) error code
- Message fails for specific numbers

**Solutions:**
```typescript
// Enable Taiwan-only validation
const service = new SMSServiceEvery8D({
  username: process.env.EVERY8D_USERNAME!,
  password: process.env.EVERY8D_PASSWORD!,
  onlyTaiwanMobileNumber: true,
});

// Validate before sending
function validateTaiwanMobile(phone: string): boolean {
  const normalized = phone.replace(/[^0-9]/g, '').replace(/^886/, '0');
  return /^09\d{8}$/.test(normalized);
}

if (!validateTaiwanMobile(phoneNumber)) {
  console.error('Invalid Taiwan mobile number:', phoneNumber);
}
```

#### 3. Message Not Delivered

**Symptoms:**
- Status shows SUCCESS but message not received
- Delays in delivery

**Solutions:**
```typescript
// 1. Check message content
// - Avoid special characters that might cause issues
// - Keep message under 70 characters for single SMS

// 2. Verify phone number is active
// - Test with your own phone first

// 3. Check account balance
// - Contact Every8D to verify account status

// 4. Log message ID for tracking
const result = await smsService.send({ mobile, text });
console.log('Message ID for tracking:', result.messageId);
```

## API Reference

### SMSServiceEvery8D

**Constructor Options:**

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `username` | `string` | Yes | - | Every8D account username |
| `password` | `string` | Yes | - | Every8D account password |
| `baseUrl` | `string` | No | `'https://api.e8d.tw'` | API endpoint URL |
| `onlyTaiwanMobileNumber` | `boolean` | No | `false` | Restrict to Taiwan mobile numbers only |

**Methods:**

```typescript
// Send single SMS
send(request: Every8DSMSRequest): Promise<Every8DSMSSendResponse>

// Send multiple SMS with different messages
send(requests: Every8DSMSRequest[]): Promise<Every8DSMSSendResponse[]>

// Send same message to multiple recipients
send(request: Every8DSMSMultiTargetRequest): Promise<Every8DSMSSendResponse[]>
```

### Request Types

```typescript
interface Every8DSMSRequest {
  mobile: string;  // Phone number (will be normalized)
  text: string;    // Message content
}

interface Every8DSMSMultiTargetRequest {
  mobileList: string[];  // Array of phone numbers
  text: string;          // Message content (same for all)
}
```

### Response Types

```typescript
interface Every8DSMSSendResponse {
  messageId?: string;              // Message ID for tracking
  status: SMSRequestResult;        // SUCCESS or FAILED
  mobile: string;                  // Normalized phone number
  errorMessage?: string;           // Error message if failed
  errorCode?: Every8DError;        // Error code if failed
}

enum SMSRequestResult {
  SUCCESS = 'SUCCESS',
  FAILED = 'FAILED',
}

enum Every8DError {
  FORMAT_ERROR = -306,
  UNKNOWN = -99,
}
```

## Advanced Topics

For creating new SMS adapters or extending functionality, see the [SMS Development Guide](/sms-development).
