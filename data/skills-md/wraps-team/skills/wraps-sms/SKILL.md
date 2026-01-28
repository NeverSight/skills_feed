---
name: wraps-sms
description: TypeScript SDK for AWS End User Messaging (Pinpoint SMS) with opt-out management, batch sending, and E.164 validation.
---

# @wraps.dev/sms SDK

TypeScript SDK for AWS End User Messaging (Pinpoint SMS) with opt-out management, batch sending, and E.164 validation. Calls your AWS account directly — no proxy, no markup.

## Installation

```bash
npm install @wraps.dev/sms
# or
pnpm add @wraps.dev/sms
```

## Quick Start

```typescript
import { WrapsSMS } from '@wraps.dev/sms';

const sms = new WrapsSMS();

const result = await sms.send({
  to: '+14155551234',
  message: 'Your verification code is 123456',
});

console.log('Sent:', result.messageId);
```

## Client Configuration

### Default (Auto-detect credentials)

```typescript
// Uses AWS credential chain (env vars, IAM role, ~/.aws/credentials)
const sms = new WrapsSMS();
```

### With Region

```typescript
const sms = new WrapsSMS({
  region: 'us-west-2', // defaults to us-east-1
});
```

### With Explicit Credentials

```typescript
const sms = new WrapsSMS({
  region: 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});
```

### With IAM Role (OIDC / Cross-account)

```typescript
// For Vercel, EKS, GitHub Actions with OIDC federation
const sms = new WrapsSMS({
  region: 'us-east-1',
  roleArn: 'arn:aws:iam::123456789012:role/WrapsSMSRole',
  roleSessionName: 'my-app-session', // optional
});
```

### With Credential Provider (Advanced)

```typescript
import { fromWebToken } from '@aws-sdk/credential-providers';

const credentials = fromWebToken({
  roleArn: process.env.AWS_ROLE_ARN!,
  webIdentityToken: async () => process.env.VERCEL_OIDC_TOKEN!,
});

const sms = new WrapsSMS({
  region: 'us-east-1',
  credentials,
});
```

## Sending SMS

### Basic Send

```typescript
const result = await sms.send({
  to: '+14155551234', // E.164 format required
  message: 'Hello from Wraps!',
});

console.log('Message ID:', result.messageId);
console.log('Segments:', result.segments);
console.log('Status:', result.status);
```

### Transactional vs Promotional

```typescript
// OTP, alerts, notifications (higher priority, opt-out not required)
await sms.send({
  to: '+14155551234',
  message: 'Your code is 123456',
  messageType: 'TRANSACTIONAL', // default
});

// Marketing messages (requires opt-in, subject to quiet hours)
await sms.send({
  to: '+14155551234',
  message: 'Sale! 20% off today only!',
  messageType: 'PROMOTIONAL',
});
```

### With Custom Sender

```typescript
// Use a specific origination number from your account
await sms.send({
  to: '+14155551234',
  message: 'Hello!',
  from: '+18005551234', // Your registered number
});
```

### With Tracking Context

```typescript
await sms.send({
  to: '+14155551234',
  message: 'Your order has shipped!',
  context: {
    orderId: 'order_123',
    userId: 'user_456',
    type: 'shipping_notification',
  },
});
```

### With Price Limit

```typescript
// Fail if message would cost more than specified amount
await sms.send({
  to: '+14155551234',
  message: 'Hello!',
  maxPrice: '0.05', // USD per segment
});
```

### With TTL (Time to Live)

```typescript
// Message expires if not delivered within TTL
await sms.send({
  to: '+14155551234',
  message: 'Your OTP is 123456',
  ttl: 300, // 5 minutes in seconds
});
```

### Dry Run (Validate without sending)

```typescript
const result = await sms.send({
  to: '+14155551234',
  message: 'Test message',
  dryRun: true,
});

console.log('Would use', result.segments, 'segment(s)');
// No message is actually sent
```

## Batch Sending

```typescript
const result = await sms.sendBatch({
  messages: [
    { to: '+14155551234', message: 'Hello Alice!' },
    { to: '+14155555678', message: 'Hello Bob!' },
    { to: '+14155559012', message: 'Hello Carol!' },
  ],
  messageType: 'TRANSACTIONAL',
});

console.log(`Total: ${result.total}`);
console.log(`Queued: ${result.queued}`);
console.log(`Failed: ${result.failed}`);

// Check individual results
result.results.forEach((r) => {
  if (r.status === 'QUEUED') {
    console.log(`${r.to}: ${r.messageId}`);
  } else {
    console.log(`${r.to}: FAILED - ${r.error}`);
  }
});
```

## Phone Number Management

### List Your Numbers

```typescript
const numbers = await sms.numbers.list();

numbers.forEach((n) => {
  console.log(`${n.phoneNumber} (${n.numberType})`);
  console.log(`  Message type: ${n.messageType}`);
  console.log(`  Two-way enabled: ${n.twoWayEnabled}`);
  console.log(`  Country: ${n.isoCountryCode}`);
});
```

### Get Number Details

```typescript
const number = await sms.numbers.get('phone-number-id-123');

if (number) {
  console.log(`Phone: ${number.phoneNumber}`);
  console.log(`Type: ${number.numberType}`);
}
```

## Opt-Out Management

TCPA compliance requires honoring opt-out requests.

### Check Opt-Out Status

```typescript
const isOptedOut = await sms.optOuts.check('+14155551234');

if (isOptedOut) {
  console.log('User has opted out, do not send');
} else {
  await sms.send({
    to: '+14155551234',
    message: 'Hello!',
  });
}
```

### List Opted-Out Numbers

```typescript
const optOuts = await sms.optOuts.list();

optOuts.forEach((entry) => {
  console.log(`${entry.phoneNumber} opted out at ${entry.optedOutAt}`);
});
```

### Manually Add to Opt-Out List

```typescript
// User requested to stop receiving messages
await sms.optOuts.add('+14155551234');
```

### Remove from Opt-Out List

```typescript
// User re-subscribed (must have explicit consent)
await sms.optOuts.remove('+14155551234');
```

## Error Handling

```typescript
import { WrapsSMS, SMSError, ValidationError, OptedOutError } from '@wraps.dev/sms';

try {
  await sms.send({
    to: '+14155551234',
    message: 'Hello!',
  });
} catch (error) {
  if (error instanceof ValidationError) {
    // Invalid parameters (e.g., invalid phone number format)
    console.error('Validation error:', error.message);
  } else if (error instanceof OptedOutError) {
    // Recipient has opted out
    console.error('User opted out:', error.phoneNumber);
  } else if (error instanceof SMSError) {
    // AWS SMS service error
    console.error('SMS error:', error.message);
    console.error('Error code:', error.code);
    console.error('Request ID:', error.requestId);
    console.error('Is throttled:', error.isThrottled);
  } else {
    throw error;
  }
}
```

## Utility Functions

### Validate Phone Number

```typescript
import { validatePhoneNumber } from '@wraps.dev/sms';

const isValid = validatePhoneNumber('+14155551234'); // true
const isInvalid = validatePhoneNumber('415-555-1234'); // false (not E.164)
```

### Sanitize Phone Number

```typescript
import { sanitizePhoneNumber } from '@wraps.dev/sms';

const clean = sanitizePhoneNumber('(415) 555-1234', 'US');
// Returns: '+14155551234'
```

### Calculate Segments

```typescript
import { calculateSegments } from '@wraps.dev/sms';

// GSM-7 encoding: 160 chars = 1 segment
const segments1 = calculateSegments('Hello world!'); // 1

// Unicode: 70 chars = 1 segment
const segments2 = calculateSegments('Hello! emoji here'); // may be more due to encoding

// Long message
const longMsg = 'A'.repeat(200);
const segments3 = calculateSegments(longMsg); // 2 (for GSM-7)
```

## Cleanup

```typescript
// When done (e.g., in serverless cleanup or app shutdown)
sms.destroy();
```

## Type Exports

```typescript
import type {
  WrapsSMSConfig,
  SendOptions,
  SendResult,
  BatchOptions,
  BatchResult,
  BatchMessage,
  BatchMessageResult,
  PhoneNumber,
  OptOutEntry,
  MessageType,
  MessageStatus,
} from '@wraps.dev/sms';
```

## Common Patterns

### OTP Service

```typescript
import { WrapsSMS } from '@wraps.dev/sms';

class OTPService {
  private sms: WrapsSMS;

  constructor() {
    this.sms = new WrapsSMS({
      region: process.env.AWS_REGION,
    });
  }

  async sendOTP(phoneNumber: string, code: string) {
    return this.sms.send({
      to: phoneNumber,
      message: `Your verification code is ${code}. Valid for 10 minutes.`,
      messageType: 'TRANSACTIONAL',
      ttl: 600, // 10 minutes
      context: {
        type: 'otp',
      },
    });
  }
}
```

### Notification Service with Opt-Out Check

```typescript
import { WrapsSMS, OptedOutError } from '@wraps.dev/sms';

class NotificationService {
  private sms: WrapsSMS;

  constructor() {
    this.sms = new WrapsSMS();
  }

  async sendNotification(phoneNumber: string, message: string) {
    // Check opt-out status first
    const isOptedOut = await this.sms.optOuts.check(phoneNumber);

    if (isOptedOut) {
      console.log(`Skipping ${phoneNumber} - opted out`);
      return null;
    }

    try {
      return await this.sms.send({
        to: phoneNumber,
        message,
        messageType: 'TRANSACTIONAL',
      });
    } catch (error) {
      if (error instanceof OptedOutError) {
        // Race condition: user opted out between check and send
        console.log(`User ${phoneNumber} opted out`);
        return null;
      }
      throw error;
    }
  }
}
```

### Vercel Edge/Serverless

```typescript
import { WrapsSMS } from '@wraps.dev/sms';

// Initialize outside handler for connection reuse
const sms = new WrapsSMS({
  roleArn: process.env.AWS_ROLE_ARN,
});

export async function POST(request: Request) {
  const { to, message } = await request.json();

  const result = await sms.send({
    to,
    message,
    messageType: 'TRANSACTIONAL',
  });

  return Response.json({ messageId: result.messageId });
}
```

## Phone Number Formats

**Always use E.164 format:**
- US: `+14155551234` (not `415-555-1234`)
- UK: `+447911123456` (not `07911 123456`)
- Germany: `+4915112345678`

## SMS Segments

Messages are billed per segment:
- **GSM-7 encoding** (basic characters): 160 chars = 1 segment
- **Unicode** (emojis, non-Latin chars): 70 chars = 1 segment
- Long messages are split: 153 chars/segment (GSM-7) or 67 chars/segment (Unicode)

## Requirements

- Node.js 18+
- AWS account with End User Messaging configured
- Phone number (toll-free, 10DLC, or short code) provisioned in AWS
