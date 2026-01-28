---
name: wraps-email
description: TypeScript SDK for AWS SES with automatic credential resolution, React.email support, and template management.
---

# @wraps.dev/email SDK

TypeScript SDK for AWS SES with automatic credential resolution, React.email support, and template management. Calls your SES directly — no proxy, no markup.

## Installation

```bash
npm install @wraps.dev/email
# or
pnpm add @wraps.dev/email
```

## Quick Start

```typescript
import { WrapsEmail } from '@wraps.dev/email';

const email = new WrapsEmail();

const result = await email.send({
  from: 'hello@yourapp.com',
  to: 'user@example.com',
  subject: 'Welcome!',
  html: '<h1>Hello from Wraps!</h1>',
});

console.log('Sent:', result.messageId);
```

## Client Configuration

### Default (Auto-detect credentials)

```typescript
// Uses AWS credential chain (env vars, IAM role, ~/.aws/credentials)
const email = new WrapsEmail();
```

### With Region

```typescript
const email = new WrapsEmail({
  region: 'us-west-2', // defaults to us-east-1
});
```

### With Explicit Credentials

```typescript
const email = new WrapsEmail({
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
const email = new WrapsEmail({
  region: 'us-east-1',
  roleArn: 'arn:aws:iam::123456789012:role/WrapsEmailRole',
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

const email = new WrapsEmail({
  region: 'us-east-1',
  credentials,
});
```

### With Pre-configured SES Client

```typescript
import { SESClient } from '@aws-sdk/client-ses';

const sesClient = new SESClient({ region: 'us-east-1' });
const email = new WrapsEmail({ client: sesClient });
```

## Sending Emails

### Simple Email

```typescript
const result = await email.send({
  from: 'sender@example.com',
  to: 'recipient@example.com',
  subject: 'Hello!',
  html: '<h1>Welcome</h1><p>This is a test email.</p>',
  text: 'Welcome! This is a test email.', // optional fallback
});
```

### With Named Sender

```typescript
await email.send({
  from: { email: 'hello@example.com', name: 'My App' },
  to: 'user@example.com',
  subject: 'Welcome!',
  html: '<h1>Hello!</h1>',
});
```

### Multiple Recipients

```typescript
await email.send({
  from: 'sender@example.com',
  to: ['user1@example.com', 'user2@example.com'],
  cc: 'manager@example.com',
  bcc: ['audit@example.com'],
  subject: 'Team Update',
  html: '<p>Hello team!</p>',
});
```

### With Reply-To

```typescript
await email.send({
  from: 'noreply@example.com',
  to: 'user@example.com',
  replyTo: 'support@example.com',
  subject: 'Your Request',
  html: '<p>We received your request.</p>',
});
```

### With Tags (for SES tracking)

```typescript
await email.send({
  from: 'sender@example.com',
  to: 'user@example.com',
  subject: 'Welcome!',
  html: '<h1>Hello!</h1>',
  tags: {
    campaign: 'onboarding',
    userId: 'user_123',
  },
});
```

### With Configuration Set

```typescript
await email.send({
  from: 'sender@example.com',
  to: 'user@example.com',
  subject: 'Welcome!',
  html: '<h1>Hello!</h1>',
  configurationSetName: 'wraps-email-tracking', // for opens/clicks/bounces
});
```

## React.email Integration

Use React components for beautiful, maintainable email templates.

```typescript
import { WrapsEmail } from '@wraps.dev/email';
import WelcomeEmail from './emails/welcome';

const email = new WrapsEmail();

await email.send({
  from: 'hello@example.com',
  to: 'user@example.com',
  subject: 'Welcome to Our App!',
  react: <WelcomeEmail username="John" />,
});
```

**Note:** Cannot use both `html` and `react` — choose one.

## Attachments

```typescript
import { readFileSync } from 'fs';

await email.send({
  from: 'sender@example.com',
  to: 'user@example.com',
  subject: 'Your Invoice',
  html: '<p>Please find your invoice attached.</p>',
  attachments: [
    {
      filename: 'invoice.pdf',
      content: readFileSync('./invoice.pdf'),
      contentType: 'application/pdf',
    },
    {
      filename: 'logo.png',
      content: Buffer.from(base64Logo, 'base64'),
      contentType: 'image/png',
    },
  ],
});
```

**Limits:**
- Maximum 100 attachments per email
- Total message size: 10MB (AWS SES limit)

## Templates

SES templates allow personalized bulk emails with variable substitution.

### Create Template

```typescript
await email.templates.create({
  name: 'welcome-email',
  subject: 'Welcome, {{name}}!',
  html: '<h1>Hello {{name}}</h1><p>Thanks for joining {{company}}!</p>',
  text: 'Hello {{name}}, Thanks for joining {{company}}!',
});
```

### Create Template from React

```typescript
import WelcomeTemplate from './emails/welcome-template';

await email.templates.createFromReact({
  name: 'welcome-email',
  subject: 'Welcome, {{name}}!',
  react: <WelcomeTemplate />, // Use {{variable}} placeholders in the component
});
```

### Send with Template

```typescript
await email.sendTemplate({
  from: 'hello@example.com',
  to: 'user@example.com',
  template: 'welcome-email',
  templateData: {
    name: 'John',
    company: 'Acme Inc',
  },
});
```

### Bulk Send with Template

```typescript
const result = await email.sendBulkTemplate({
  from: 'hello@example.com',
  template: 'welcome-email',
  destinations: [
    { to: 'user1@example.com', templateData: { name: 'Alice', company: 'Acme' } },
    { to: 'user2@example.com', templateData: { name: 'Bob', company: 'Acme' } },
    { to: 'user3@example.com', templateData: { name: 'Carol', company: 'Acme' } },
  ],
  defaultTemplateData: {
    company: 'Acme Inc', // fallback if not in destination
  },
});

// Check results
result.status.forEach((s, i) => {
  if (s.status === 'success') {
    console.log(`Email ${i} sent: ${s.messageId}`);
  } else {
    console.log(`Email ${i} failed: ${s.error}`);
  }
});
```

**Limit:** Maximum 50 destinations per bulk send.

### Manage Templates

```typescript
// List all templates
const templates = await email.templates.list();

// Get template details
const template = await email.templates.get('welcome-email');

// Update template
await email.templates.update({
  name: 'welcome-email',
  subject: 'Welcome aboard, {{name}}!',
  html: '<h1>Welcome {{name}}!</h1>',
});

// Delete template
await email.templates.delete('welcome-email');
```

## Error Handling

```typescript
import { WrapsEmail, SESError, ValidationError } from '@wraps.dev/email';

try {
  await email.send({
    from: 'sender@example.com',
    to: 'user@example.com',
    subject: 'Hello',
    html: '<p>Hi!</p>',
  });
} catch (error) {
  if (error instanceof ValidationError) {
    // Invalid parameters (e.g., invalid email format)
    console.error('Validation error:', error.message);
  } else if (error instanceof SESError) {
    // AWS SES error
    console.error('SES error:', error.message);
    console.error('Error code:', error.code);
    console.error('Request ID:', error.requestId);
    console.error('Is throttled:', error.isThrottled);
  } else {
    throw error;
  }
}
```

## Cleanup

```typescript
// When done (e.g., in serverless cleanup or app shutdown)
email.destroy();
```

## Type Exports

```typescript
import type {
  WrapsEmailConfig,
  SendEmailParams,
  SendEmailResult,
  SendTemplateParams,
  SendBulkTemplateParams,
  SendBulkTemplateResult,
  CreateTemplateParams,
  UpdateTemplateParams,
  Template,
  TemplateMetadata,
  EmailAddress,
  Attachment,
} from '@wraps.dev/email';
```

## Common Patterns

### Transactional Email Service

```typescript
import { WrapsEmail } from '@wraps.dev/email';

class EmailService {
  private email: WrapsEmail;

  constructor() {
    this.email = new WrapsEmail({
      region: process.env.AWS_REGION,
      configurationSetName: 'wraps-email-tracking',
    });
  }

  async sendWelcome(to: string, name: string) {
    return this.email.send({
      from: { email: 'hello@myapp.com', name: 'My App' },
      to,
      subject: `Welcome, ${name}!`,
      html: `<h1>Welcome ${name}!</h1><p>Thanks for signing up.</p>`,
      tags: { type: 'welcome', userId: to },
    });
  }

  async sendPasswordReset(to: string, resetLink: string) {
    return this.email.send({
      from: 'security@myapp.com',
      to,
      subject: 'Reset Your Password',
      html: `<p>Click <a href="${resetLink}">here</a> to reset your password.</p>`,
      tags: { type: 'password-reset' },
    });
  }
}
```

### Vercel Edge/Serverless

```typescript
import { WrapsEmail } from '@wraps.dev/email';

// Initialize outside handler for connection reuse
const email = new WrapsEmail({
  roleArn: process.env.AWS_ROLE_ARN,
});

export async function POST(request: Request) {
  const { to, subject, html } = await request.json();

  const result = await email.send({
    from: 'noreply@myapp.com',
    to,
    subject,
    html,
  });

  return Response.json({ messageId: result.messageId });
}
```

## Requirements

- Node.js 18+
- AWS SES configured (use `npx @wraps.dev/cli email init` for easy setup)
- Verified domain or email address in SES
