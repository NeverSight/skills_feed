---
name: sms-development
description: Development guide for @rytass/sms base package (簡訊基底套件開發指南). Use when creating new SMS adapters (新增簡訊 adapter), understanding base interfaces, or extending SMS functionality. Covers SMSService interface and implementation patterns for Taiwan SMS providers (台灣簡訊服務提供商). Keywords - SMS adapter, 簡訊 adapter, service interface, 服務介面, message delivery, 訊息發送, batch processing, 批次處理, number normalization, 號碼正規化, Every8D, 互動資通, Interactive Communications
---

# SMS Development Guide

This skill provides guidance for developers working with the `@rytass/sms` base package, including creating new SMS adapters for Taiwan SMS service providers.

## Overview

The `@rytass/sms` package defines the core interfaces and types that all SMS adapters must implement. It follows the adapter pattern to provide a unified API across different SMS providers.

## Architecture

```
@rytass/sms (Base Package)
    │
    ├── SMSService<Request, SendResponse, MultiTarget>  # Service interface
    ├── SMSRequest                                       # Single message interface
    ├── SMSSendResponse                                  # Response interface
    ├── MultiTargetRequest                              # Batch message interface
    ├── SMSRequestResult                                # Status enum
    └── Taiwan Phone Number Helpers                     # Normalization utilities

@rytass/sms-adapter-*                                   # Provider implementations
    │
    ├── [Provider]SMSService                            # Implements SMSService
    ├── [Provider]SMSRequest                            # Extends SMSRequest
    ├── [Provider]SMSSendResponse                       # Extends SMSSendResponse
    └── [Provider] specific types and errors
```

## Installation

```bash
npm install @rytass/sms
```

## Core Interfaces

### SMSService

The main interface that all SMS adapters must implement:

```typescript
/**
 * SMS service interface
 * @template Request - SMS request type extending SMSRequest
 * @template SendResponse - SMS response type extending SMSSendResponse
 * @template MultiTarget - Multi-target request type extending MultiTargetRequest
 */
interface SMSService<
  Request extends SMSRequest,
  SendResponse extends SMSSendResponse,
  MultiTarget extends MultiTargetRequest,
> {
  /**
   * Send multiple SMS messages with different content
   * @param request - Array of SMS requests
   * @returns Promise resolving to array of send responses
   */
  send(request: Request[]): Promise<SendResponse[]>;

  /**
   * Send single SMS message
   * @param request - Single SMS request
   * @returns Promise resolving to send response
   */
  send(request: Request): Promise<SendResponse>;

  /**
   * Send same message to multiple recipients
   * @param request - Multi-target request with recipient list
   * @returns Promise resolving to array of send responses
   */
  send(request: MultiTarget): Promise<SendResponse[]>;
}
```

### Base Request Types

```typescript
/**
 * Base SMS request interface
 */
interface SMSRequest {
  /** Recipient mobile phone number */
  mobile: string;

  /** Message text content */
  text: string;
}

/**
 * Multi-target request for sending same message to multiple recipients
 */
interface MultiTargetRequest {
  /** Array of recipient mobile phone numbers */
  mobileList: string[];

  /** Message text content (same for all recipients) */
  text: string;
}
```

### Base Response Types

```typescript
/**
 * SMS request result status
 */
enum SMSRequestResult {
  /** Message sent successfully */
  SUCCESS = 'SUCCESS',

  /** Message delivery failed */
  FAILED = 'FAILED',
}

/**
 * Base SMS send response interface
 */
interface SMSSendResponse {
  /** Unique message identifier (if provided by gateway) */
  messageId?: string;

  /** Delivery status */
  status: SMSRequestResult;

  /** Recipient mobile phone number (normalized) */
  mobile: string;
}
```

## Taiwan Phone Number Utilities

The base package provides utilities for handling Taiwan mobile numbers:

```typescript
/**
 * Regular expression for validating Taiwan mobile phone numbers
 * Matches formats:
 * - 09XXXXXXXX (standard)
 * - 0912-345-678 (with dashes)
 * - 0912 345 678 (with spaces)
 * - +8869XXXXXXXX (international)
 * - 8869XXXXXXXX (international without +)
 */
const TAIWAN_PHONE_NUMBER_RE = /^(0|\+?886-?)9\d{2}-?\d{3}-?\d{3}$/;

/**
 * Normalize Taiwan mobile phone number to standard format (09XXXXXXXX)
 * @param mobile - Phone number in any supported format
 * @returns Normalized phone number (09XXXXXXXX)
 *
 * @example
 * normalizedTaiwanMobilePhoneNumber('0987-654-321') // '0987654321'
 * normalizedTaiwanMobilePhoneNumber('+886987654321') // '0987654321'
 * normalizedTaiwanMobilePhoneNumber('886987654321') // '0987654321'
 */
function normalizedTaiwanMobilePhoneNumber(mobile: string): string;
```

## Implementation Guide

### Step 1: Define Provider-Specific Types

Create interfaces extending the base types:

```typescript
import {
  SMSRequest,
  SMSSendResponse,
  MultiTargetRequest,
  SMSRequestResult,
} from '@rytass/sms';

/**
 * Provider-specific initialization options
 */
export interface MyProviderSMSRequestInit {
  /** API username/account ID */
  username: string;

  /** API password/secret key */
  password: string;

  /** API base URL (optional, defaults to production) */
  baseUrl?: string;

  /** Restrict to Taiwan mobile numbers only */
  onlyTaiwanMobileNumber?: boolean;

  // Add any other provider-specific config
}

/**
 * Provider-specific error codes
 */
export enum MyProviderError {
  /** Invalid credentials */
  INVALID_CREDENTIALS = -1,

  /** Invalid phone number format */
  FORMAT_ERROR = -2,

  /** Insufficient account balance */
  INSUFFICIENT_BALANCE = -3,

  /** Rate limit exceeded */
  RATE_LIMIT_EXCEEDED = -4,

  /** Unknown error */
  UNKNOWN = -99,
}

/**
 * Provider-specific SMS request
 * Extends base SMSRequest with additional fields if needed
 */
export interface MyProviderSMSRequest extends SMSRequest {
  mobile: string;
  text: string;

  // Add provider-specific fields if needed
  // priority?: 'low' | 'normal' | 'high';
  // scheduledTime?: Date;
}

/**
 * Provider-specific send response
 * Extends base SMSSendResponse with additional fields
 */
export interface MyProviderSMSSendResponse extends SMSSendResponse {
  messageId?: string;
  status: SMSRequestResult;
  mobile: string;

  /** Error message if delivery failed */
  errorMessage?: string;

  /** Provider-specific error code */
  errorCode?: MyProviderError;

  // Add provider-specific fields if needed
  // cost?: number;
  // remainingBalance?: number;
}

/**
 * Provider-specific multi-target request
 */
export interface MyProviderSMSMultiTargetRequest extends MultiTargetRequest {
  mobileList: string[];
  text: string;
}
```

### Step 2: Implement the SMS Service

```typescript
import {
  SMSService,
  SMSRequestResult,
  normalizedTaiwanMobilePhoneNumber,
  TAIWAN_PHONE_NUMBER_RE,
} from '@rytass/sms';
import axios from 'axios';

/**
 * SMS service implementation for MyProvider
 * Implements the SMSService interface with provider-specific logic
 */
export class SMSServiceMyProvider implements SMSService<
  MyProviderSMSRequest,
  MyProviderSMSSendResponse,
  MyProviderSMSMultiTargetRequest
> {
  private readonly username: string;
  private readonly password: string;
  private readonly baseUrl: string;
  private readonly onlyTaiwanMobileNumber: boolean;

  /**
   * Initialize SMS service
   * @param options - Provider configuration options
   */
  constructor(options: MyProviderSMSRequestInit) {
    this.username = options.username;
    this.password = options.password;
    this.baseUrl = options.baseUrl || 'https://api.myprovider.com';
    this.onlyTaiwanMobileNumber = options.onlyTaiwanMobileNumber || false;
  }

  /**
   * Send SMS message(s)
   * Handles three sending patterns:
   * 1. Single SMS to one recipient
   * 2. Multiple SMS with different messages
   * 3. Same message to multiple recipients
   */
  async send(requests: MyProviderSMSRequest[]): Promise<MyProviderSMSSendResponse[]>;
  async send(request: MyProviderSMSRequest): Promise<MyProviderSMSSendResponse>;
  async send(request: MyProviderSMSMultiTargetRequest): Promise<MyProviderSMSSendResponse[]>;

  async send(
    requests: MyProviderSMSMultiTargetRequest | MyProviderSMSRequest | MyProviderSMSRequest[],
  ): Promise<MyProviderSMSSendResponse | MyProviderSMSSendResponse[]> {
    // Validate input
    if (
      (Array.isArray(requests) && !requests.length) ||
      ((requests as MyProviderSMSMultiTargetRequest).mobileList &&
        !(requests as MyProviderSMSMultiTargetRequest).mobileList?.length)
    ) {
      throw new Error('No target provided.');
    }

    // Process and validate phone numbers
    const processedRequests = this.processRequests(requests);

    // Send to provider API
    const results = await this.sendToProvider(processedRequests);

    // Return results in appropriate format
    return this.formatResults(requests, results);
  }

  /**
   * Process and validate phone numbers
   * @param requests - Raw requests
   * @returns Processed requests with normalized phone numbers
   */
  private processRequests(
    requests: MyProviderSMSMultiTargetRequest | MyProviderSMSRequest | MyProviderSMSRequest[],
  ): Array<{ mobile: string; text: string }> {
    const requestArray = Array.isArray(requests) ? requests : [requests];
    const processed: Array<{ mobile: string; text: string }> = [];

    for (const request of requestArray) {
      if ((request as MyProviderSMSMultiTargetRequest).mobileList) {
        // Multi-target request
        const multiTarget = request as MyProviderSMSMultiTargetRequest;

        for (const mobile of multiTarget.mobileList) {
          const normalizedMobile = this.validateAndNormalizeMobile(mobile);
          processed.push({
            mobile: normalizedMobile,
            text: multiTarget.text,
          });
        }
      } else {
        // Single request
        const singleRequest = request as MyProviderSMSRequest;
        const normalizedMobile = this.validateAndNormalizeMobile(singleRequest.mobile);
        processed.push({
          mobile: normalizedMobile,
          text: singleRequest.text,
        });
      }
    }

    return processed;
  }

  /**
   * Validate and normalize phone number
   * @param mobile - Raw phone number
   * @returns Normalized phone number
   * @throws Error if number is invalid and onlyTaiwanMobileNumber is true
   */
  private validateAndNormalizeMobile(mobile: string): string {
    // Check if Taiwan number
    if (TAIWAN_PHONE_NUMBER_RE.test(mobile)) {
      return normalizedTaiwanMobilePhoneNumber(mobile);
    }

    // If strict Taiwan-only mode, reject non-Taiwan numbers
    if (this.onlyTaiwanMobileNumber) {
      throw new Error(
        `${mobile} is not taiwan mobile phone (\`onlyTaiwanMobileNumber\` option is true)`
      );
    }

    // Return as-is for international numbers
    return mobile;
  }

  /**
   * Send requests to provider API
   * @param requests - Processed requests
   * @returns API responses
   */
  private async sendToProvider(
    requests: Array<{ mobile: string; text: string }>,
  ): Promise<Map<string, MyProviderSMSSendResponse>> {
    // Group requests by message text for batch optimization
    const batches = this.groupByMessage(requests);
    const results = new Map<string, MyProviderSMSSendResponse>();

    // Send each batch
    for (const [message, mobileList] of batches.entries()) {
      try {
        // Call provider API
        const response = await this.callProviderAPI(mobileList, message);

        // Process API response
        const batchResults = this.parseAPIResponse(response, mobileList, message);

        // Store results
        for (const [key, result] of batchResults.entries()) {
          results.set(key, result);
        }
      } catch (error) {
        // Handle API errors
        for (const mobile of mobileList) {
          results.set(`${message}:${mobile}`, {
            status: SMSRequestResult.FAILED,
            mobile,
            errorMessage: error.message,
            errorCode: MyProviderError.UNKNOWN,
          });
        }
      }
    }

    return results;
  }

  /**
   * Group requests by message text for batch sending
   * @param requests - Array of requests
   * @returns Map of message text to mobile numbers
   */
  private groupByMessage(
    requests: Array<{ mobile: string; text: string }>,
  ): Map<string, string[]> {
    const batches = new Map<string, string[]>();

    for (const request of requests) {
      const existing = batches.get(request.text) || [];
      batches.set(request.text, [...existing, request.mobile]);
    }

    return batches;
  }

  /**
   * Call provider API
   * IMPORTANT: Implement this method according to your provider's API specification
   * @param mobileList - Array of phone numbers
   * @param message - Message text
   * @returns API response
   *
   * NOTE: Every8D uses the following API specification:
   * - Endpoint: `${baseUrl}/API21/HTTP/SendSMS.ashx`
   * - Method: POST with application/x-www-form-urlencoded
   * - Parameters: UID (username), PWD (password), MSG (message), DEST (comma-separated mobiles)
   * - Response: CSV format: "credit,sent,cost,unsent,batchId" or "errorCode,errorMessage"
   */
  private async callProviderAPI(
    mobileList: string[],
    message: string,
  ): Promise<any> {
    // Example implementation using Every8D API format
    // Other providers may use different endpoints and parameters
    const { data } = await axios.post(
      `${this.baseUrl}/API21/HTTP/SendSMS.ashx`,
      new URLSearchParams({
        UID: this.username,    // Every8D uses UID for username
        PWD: this.password,    // Every8D uses PWD for password
        MSG: message,          // Every8D uses MSG for message content
        DEST: mobileList.join(','), // Every8D uses DEST for comma-separated recipients
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );

    return data;
  }

  /**
   * Parse provider API response
   * IMPORTANT: Implement this method according to your provider's response format
   * @param response - API response data
   * @param mobileList - Array of phone numbers
   * @param message - Message text
   * @returns Map of results keyed by "message:mobile"
   */
  private parseAPIResponse(
    response: any,
    mobileList: string[],
    message: string,
  ): Map<string, MyProviderSMSSendResponse> {
    const results = new Map<string, MyProviderSMSSendResponse>();

    // Example parsing - REPLACE WITH ACTUAL PROVIDER RESPONSE PARSING
    if (response.success) {
      // All succeeded
      for (const mobile of mobileList) {
        results.set(`${message}:${mobile}`, {
          messageId: response.messageId,
          status: SMSRequestResult.SUCCESS,
          mobile,
        });
      }
    } else {
      // All failed
      for (const mobile of mobileList) {
        results.set(`${message}:${mobile}`, {
          status: SMSRequestResult.FAILED,
          mobile,
          errorMessage: response.errorMessage,
          errorCode: response.errorCode,
        });
      }
    }

    return results;
  }

  /**
   * Format results based on original request type
   * @param originalRequest - Original request
   * @param results - Processed results map
   * @returns Formatted response(s)
   */
  private formatResults(
    originalRequest: MyProviderSMSMultiTargetRequest | MyProviderSMSRequest | MyProviderSMSRequest[],
    results: Map<string, MyProviderSMSSendResponse>,
  ): MyProviderSMSSendResponse | MyProviderSMSSendResponse[] {
    // Multi-target request
    if ((originalRequest as MyProviderSMSMultiTargetRequest).mobileList) {
      const multiTarget = originalRequest as MyProviderSMSMultiTargetRequest;

      return multiTarget.mobileList.map(mobile => {
        const normalizedMobile = TAIWAN_PHONE_NUMBER_RE.test(mobile)
          ? normalizedTaiwanMobilePhoneNumber(mobile)
          : mobile;

        return results.get(`${multiTarget.text}:${normalizedMobile}`)!;
      });
    }

    // Array of requests
    if (Array.isArray(originalRequest)) {
      return originalRequest.map(request => {
        const normalizedMobile = TAIWAN_PHONE_NUMBER_RE.test(request.mobile)
          ? normalizedTaiwanMobilePhoneNumber(request.mobile)
          : request.mobile;

        return results.get(`${request.text}:${normalizedMobile}`)!;
      });
    }

    // Single request
    const singleRequest = originalRequest as MyProviderSMSRequest;
    const normalizedMobile = TAIWAN_PHONE_NUMBER_RE.test(singleRequest.mobile)
      ? normalizedTaiwanMobilePhoneNumber(singleRequest.mobile)
      : singleRequest.mobile;

    return results.get(`${singleRequest.text}:${normalizedMobile}`)!;
  }
}
```

### Step 3: Export Public API

```typescript
// index.ts
export { SMSServiceMyProvider } from './sms-service-my-provider';
export * from './typings';
```

### Step 4: Add Tests

```typescript
// __tests__/sms-service-my-provider.spec.ts
import { SMSServiceMyProvider } from '../src/sms-service-my-provider';
import { SMSRequestResult } from '@rytass/sms';

describe('SMSServiceMyProvider', () => {
  let smsService: SMSServiceMyProvider;

  beforeEach(() => {
    smsService = new SMSServiceMyProvider({
      username: 'test-username',
      password: 'test-password',
      onlyTaiwanMobileNumber: true,
    });
  });

  describe('send - single SMS', () => {
    it('should send single SMS successfully', async () => {
      const result = await smsService.send({
        mobile: '0987654321',
        text: 'Test message',
      });

      expect(result.status).toBe(SMSRequestResult.SUCCESS);
      expect(result.mobile).toBe('0987654321');
      expect(result.messageId).toBeDefined();
    });

    it('should normalize Taiwan phone number', async () => {
      const result = await smsService.send({
        mobile: '+886987654321',
        text: 'Test message',
      });

      expect(result.mobile).toBe('0987654321');
    });

    it('should reject non-Taiwan number when onlyTaiwanMobileNumber is true', async () => {
      await expect(
        smsService.send({
          mobile: '+1234567890',
          text: 'Test message',
        })
      ).rejects.toThrow('is not taiwan mobile phone');
    });
  });

  describe('send - batch SMS', () => {
    it('should send same message to multiple recipients', async () => {
      const results = await smsService.send({
        mobileList: ['0987654321', '0912345678', '0923456789'],
        text: 'Batch message',
      });

      expect(results).toHaveLength(3);
      expect(results.every(r => r.status === SMSRequestResult.SUCCESS)).toBe(true);
    });

    it('should send different messages to multiple recipients', async () => {
      const results = await smsService.send([
        { mobile: '0987654321', text: 'Message 1' },
        { mobile: '0912345678', text: 'Message 2' },
        { mobile: '0923456789', text: 'Message 3' },
      ]);

      expect(results).toHaveLength(3);
      expect(results.every(r => r.status === SMSRequestResult.SUCCESS)).toBe(true);
    });
  });

  describe('error handling', () => {
    it('should handle API errors gracefully', async () => {
      // Mock API error
      // ... test implementation
    });

    it('should return FAILED status on delivery failure', async () => {
      // Mock failed delivery
      // ... test implementation
    });
  });
});
```

## Implementation Checklist

When implementing a new SMS adapter, ensure:

### Required Features

- [ ] **Interface Implementation**: Implements `SMSService<Request, SendResponse, MultiTarget>`
- [ ] **Single SMS**: Supports sending single SMS to one recipient
- [ ] **Batch SMS**: Supports sending same message to multiple recipients
- [ ] **Multi-target**: Supports sending different messages to multiple recipients
- [ ] **Phone Validation**: Validates phone numbers before sending
- [ ] **Number Normalization**: Uses `normalizedTaiwanMobilePhoneNumber()` for Taiwan numbers
- [ ] **Error Handling**: Returns appropriate error codes and messages
- [ ] **Type Safety**: All methods have proper TypeScript types

### Recommended Features

- [ ] **Taiwan Number Support**: Uses `TAIWAN_PHONE_NUMBER_RE` for validation
- [ ] **Strict Mode**: Implements `onlyTaiwanMobileNumber` option
- [ ] **International Support**: Handles international numbers when strict mode is disabled
- [ ] **Message Batching**: Groups messages for efficient API calls
- [ ] **Rate Limiting**: Implements rate limiting if required by provider
- [ ] **Retry Logic**: Implements retry for transient failures
- [ ] **Logging**: Logs API calls and errors for debugging
- [ ] **Documentation**: Includes comprehensive JSDoc comments

### Quality Assurance

- [ ] **Unit Tests**: Comprehensive test coverage (>80%)
- [ ] **Integration Tests**: Tests against provider API (staging environment)
- [ ] **Error Cases**: Tests all error scenarios
- [ ] **Edge Cases**: Tests edge cases (empty lists, invalid numbers, etc.)
- [ ] **Performance**: Tests batch performance with large recipient lists
- [ ] **README**: Complete README with examples and API reference

## Best Practices

### 1. Phone Number Handling

```typescript
// ✅ GOOD: Use provided utilities
import { normalizedTaiwanMobilePhoneNumber, TAIWAN_PHONE_NUMBER_RE } from '@rytass/sms';

private validateMobile(mobile: string): string {
  if (TAIWAN_PHONE_NUMBER_RE.test(mobile)) {
    return normalizedTaiwanMobilePhoneNumber(mobile);
  }

  if (this.onlyTaiwanMobileNumber) {
    throw new Error(`Invalid Taiwan mobile number: ${mobile}`);
  }

  return mobile;
}

// ❌ BAD: Custom regex without normalization
private validateMobile(mobile: string): string {
  if (!/^09\d{8}$/.test(mobile)) {
    throw new Error('Invalid number');
  }
  return mobile;
}
```

### 2. Error Handling

```typescript
// ✅ GOOD: Detailed error information
catch (error) {
  return {
    status: SMSRequestResult.FAILED,
    mobile,
    errorMessage: error.response?.data?.message || error.message,
    errorCode: this.mapProviderErrorCode(error.response?.data?.code),
  };
}

// ❌ BAD: Generic error without details
catch (error) {
  return {
    status: SMSRequestResult.FAILED,
    mobile,
  };
}
```

### 3. Batch Optimization

```typescript
// ✅ GOOD: Group by message for efficiency
private groupByMessage(requests: Array<{ mobile: string; text: string }>) {
  const batches = new Map<string, string[]>();

  for (const request of requests) {
    const existing = batches.get(request.text) || [];
    batches.set(request.text, [...existing, request.mobile]);
  }

  return batches;
}

// ❌ BAD: Send each message individually
for (const request of requests) {
  await this.callAPI(request.mobile, request.text);
}
```

### 4. Type Safety

```typescript
// ✅ GOOD: Strict typing with generics
export class SMSServiceMyProvider implements SMSService<
  MyProviderSMSRequest,
  MyProviderSMSSendResponse,
  MyProviderSMSMultiTargetRequest
> {
  // ...
}

// ❌ BAD: Using any or loose typing
export class SMSServiceMyProvider {
  async send(request: any): Promise<any> {
    // ...
  }
}
```

### 5. Configuration

```typescript
// ✅ GOOD: Environment-based configuration
export class SMSServiceMyProvider {
  constructor(options: MyProviderSMSRequestInit) {
    this.baseUrl = options.baseUrl || this.getDefaultBaseUrl();
  }

  private getDefaultBaseUrl(): string {
    return process.env.NODE_ENV === 'production'
      ? 'https://api.myprovider.com'
      : 'https://api-staging.myprovider.com';
  }
}

// ❌ BAD: Hardcoded production URL
export class SMSServiceMyProvider {
  private baseUrl = 'https://api.myprovider.com';
}
```

## API Reference

### Base Package Exports

```typescript
// Types
export {
  SMSService,          // Service interface
  SMSRequest,          // Single message interface
  SMSSendResponse,     // Response interface
  MultiTargetRequest,  // Batch message interface
  SMSRequestResult,    // Status enum
};

// Utilities
export {
  TAIWAN_PHONE_NUMBER_RE,                   // Taiwan number regex
  normalizedTaiwanMobilePhoneNumber,        // Normalization function
};
```

### Taiwan Number Validation

**Supported Formats:**
- `09XXXXXXXX` - Standard Taiwan format
- `0912-345-678` - With dashes
- `0912 345 678` - With spaces
- `+8869XXXXXXXX` - International with +
- `8869XXXXXXXX` - International without +

**Normalization Output:**
- Always returns `09XXXXXXXX` format
- Removes dashes, spaces, and country code
- Converts `+886` or `886` prefix to `0`

## Examples

### Minimal Adapter Implementation

```typescript
import {
  SMSService,
  SMSRequest,
  SMSSendResponse,
  MultiTargetRequest,
  SMSRequestResult,
} from '@rytass/sms';

interface SimpleSMSRequest extends SMSRequest {
  mobile: string;
  text: string;
}

interface SimpleSMSResponse extends SMSSendResponse {
  messageId?: string;
  status: SMSRequestResult;
  mobile: string;
}

interface SimpleMultiTargetRequest extends MultiTargetRequest {
  mobileList: string[];
  text: string;
}

export class SimpleSMSService implements SMSService<
  SimpleSMSRequest,
  SimpleSMSResponse,
  SimpleMultiTargetRequest
> {
  async send(requests: SimpleSMSRequest[]): Promise<SimpleSMSResponse[]>;
  async send(request: SimpleSMSRequest): Promise<SimpleSMSResponse>;
  async send(request: SimpleMultiTargetRequest): Promise<SimpleSMSResponse[]>;

  async send(request: any): Promise<any> {
    // Minimal implementation
    if (Array.isArray(request)) {
      return Promise.all(request.map(r => this.sendSingle(r)));
    }

    if (request.mobileList) {
      return Promise.all(
        request.mobileList.map(mobile =>
          this.sendSingle({ mobile, text: request.text })
        )
      );
    }

    return this.sendSingle(request);
  }

  private async sendSingle(request: SimpleSMSRequest): Promise<SimpleSMSResponse> {
    // Call provider API
    // Return response
    return {
      messageId: 'MSG-' + Date.now(),
      status: SMSRequestResult.SUCCESS,
      mobile: request.mobile,
    };
  }
}
```

## Common Provider Patterns

### HTTP-based API

Most Taiwan SMS providers use HTTP POST:

```typescript
private async callProviderAPI(mobile: string, text: string): Promise<any> {
  const { data } = await axios.post(
    `${this.baseUrl}/api/sms/send`,
    new URLSearchParams({
      username: this.username,
      password: this.password,
      mobile: mobile,
      message: text,
    }),
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    }
  );

  return data;
}
```

### CSV Response Format

Some providers return CSV responses:

```typescript
private parseCSVResponse(data: string): {
  messageId: string;
  status: SMSRequestResult;
} {
  const [credit, sent, cost, unsent, messageId] = data.split(',');

  return {
    messageId,
    status: messageId ? SMSRequestResult.SUCCESS : SMSRequestResult.FAILED,
  };
}
```

### Signature-based Authentication

Some providers require request signatures:

```typescript
import crypto from 'crypto';

private generateSignature(params: Record<string, string>): string {
  const sorted = Object.keys(params)
    .sort()
    .map(key => `${key}=${params[key]}`)
    .join('&');

  return crypto
    .createHash('md5')
    .update(sorted + this.secretKey)
    .digest('hex');
}
```

## Troubleshooting

### Common Issues

**TypeScript Errors:**
```typescript
// Error: Type 'X' is not assignable to type 'SMSService<...>'
// Solution: Ensure all three send() overloads are implemented

async send(requests: MyProviderSMSRequest[]): Promise<MyProviderSMSSendResponse[]>;
async send(request: MyProviderSMSRequest): Promise<MyProviderSMSSendResponse>;
async send(request: MyProviderSMSMultiTargetRequest): Promise<MyProviderSMSSendResponse[]>;
```

**Phone Number Validation:**
```typescript
// Issue: Numbers not being normalized correctly
// Solution: Use TAIWAN_PHONE_NUMBER_RE before normalizing

if (TAIWAN_PHONE_NUMBER_RE.test(mobile)) {
  mobile = normalizedTaiwanMobilePhoneNumber(mobile);
}
```

**Batch Optimization:**
```typescript
// Issue: Too many API calls
// Solution: Group requests by message text

const batches = requests.reduce((map, req) => {
  const list = map.get(req.text) || [];
  map.set(req.text, [...list, req.mobile]);
  return map;
}, new Map<string, string[]>());
```

## Publishing Checklist

Before publishing your adapter:

- [ ] Package name follows convention: `@rytass/sms-adapter-{provider}`
- [ ] Peer dependency on `@rytass/sms` is declared
- [ ] All exports are properly typed
- [ ] README includes installation, usage, and examples
- [ ] Tests pass with >80% coverage
- [ ] TypeScript builds without errors
- [ ] Package builds with `npm run build`
- [ ] Version follows semantic versioning
- [ ] CHANGELOG.md is updated
- [ ] License is included (MIT recommended)

## Resources

For reference implementations:
- [Every8D Adapter](../../packages/sms-adapter-every8d) - Complete reference implementation (互動資通 / Interactive Communications)
- [Base Package](../../packages/sms) - Core interfaces and utilities

For usage guidance:
- [SMS Adapters Skill](/sms-adapters) - User guide for SMS adapters
