---
name: resend-integration
description: Set up Resend email integration with newsletters, contact forms, and booking systems. Use when implementing email functionality with Resend Audiences, segments, topics, webhooks, and multi-domain accounts.
---

# Resend Integration

Complete guide for integrating Resend email services into Next.js applications with proper Audiences setup.

## When to Use

- Setting up newsletter signups
- Adding contact form email notifications
- Implementing booking/calendar email confirmations
- Configuring email forwarding via webhooks
- Managing multi-domain Resend accounts

## Resend Audiences Architecture

Resend has ONE audience per account. Use these features to organize:

| Feature | Purpose | Visibility |
|---------|---------|------------|
| **Contacts** | Individual subscribers | - |
| **Properties** | Custom data fields (domain, source, company) | Internal |
| **Segments** | Internal groupings for targeting | Internal |
| **Topics** | User-facing email preferences | User can manage |
| **Broadcasts** | Campaign sending with auto-unsubscribe | - |

## Multi-Domain Strategy

For accounts with multiple domains, tag contacts with properties:

```typescript
await resend.contacts.create({
  email,
  properties: {
    domain: "example.com",     // Which project
    source: "newsletter",       // How they signed up
  },
  segments: [{ id: SEGMENT_ID }],
  topics: [{ id: TOPIC_ID, subscription: "opt_in" }],
});
```

## Implementation

### 1. Shared Utility (`lib/resend.ts`)

```typescript
import { Resend } from "resend";

export const resend = new Resend(process.env.RESEND_API_KEY);

const SEGMENT_NEWSLETTER = process.env.RESEND_SEGMENT_NEWSLETTER;
const SEGMENT_LEADS = process.env.RESEND_SEGMENT_LEADS;
const TOPIC_NEWSLETTER = process.env.RESEND_TOPIC_NEWSLETTER;

type ContactSource = "newsletter" | "booking" | "contact";

interface CreateContactOptions {
  email: string;
  firstName?: string;
  lastName?: string;
  company?: string;
  source: ContactSource;
  subscribeToNewsletter?: boolean;
}

export async function createContact({
  email,
  firstName,
  lastName,
  company,
  source,
  subscribeToNewsletter = false,
}: CreateContactOptions) {
  const segments: { id: string }[] = [];
  if (source === "newsletter" && SEGMENT_NEWSLETTER) {
    segments.push({ id: SEGMENT_NEWSLETTER });
  } else if ((source === "booking" || source === "contact") && SEGMENT_LEADS) {
    segments.push({ id: SEGMENT_LEADS });
  }

  const topics: { id: string; subscription: "opt_in" | "opt_out" }[] = [];
  if (subscribeToNewsletter && TOPIC_NEWSLETTER) {
    topics.push({ id: TOPIC_NEWSLETTER, subscription: "opt_in" });
  }

  const properties: Record<string, string> = {
    domain: "YOUR_DOMAIN.com",  // Replace with actual domain
    source,
  };
  if (company) properties.company = company;

  const { data, error } = await resend.contacts.create({
    email,
    firstName: firstName || undefined,
    lastName: lastName || undefined,
    unsubscribed: false,
    ...(Object.keys(properties).length > 0 && { properties }),
    ...(segments.length > 0 && { segments }),
    ...(topics.length > 0 && { topics }),
  });

  if (error?.message?.includes("already exists")) {
    return { exists: true, error: null };
  }
  return { data, exists: false, error };
}

export async function contactExists(email: string): Promise<boolean> {
  try {
    const { data } = await resend.contacts.get({ email });
    return !!data;
  } catch {
    return false;
  }
}
```

### 2. Newsletter Route (`/api/newsletter`)

```typescript
import { NextResponse } from "next/server";
import { resend, createContact, contactExists } from "@/lib/resend";

export async function POST(request: Request) {
  const { email } = await request.json();

  if (!email) {
    return NextResponse.json({ error: "Email is required" }, { status: 400 });
  }

  // Duplicate check
  if (await contactExists(email)) {
    return NextResponse.json(
      { error: "already_subscribed", message: "You're already subscribed!" },
      { status: 409 },
    );
  }

  const { error } = await createContact({
    email,
    source: "newsletter",
    subscribeToNewsletter: true,
  });

  if (error) {
    // Return actual error, not generic 500
    const message = typeof error === "object" && "message" in error
      ? (error as { message: string }).message
      : "Failed to subscribe";
    const statusCode = typeof error === "object" && "statusCode" in error
      ? (error as { statusCode: number }).statusCode
      : 500;
    return NextResponse.json({ error: message }, { status: statusCode });
  }

  // Send welcome email
  await resend.emails.send({
    from: "Company <noreply@example.com>",
    to: [email],
    subject: "Welcome to our Newsletter",
    html: `<h2>Thanks for subscribing!</h2>...`,
  });

  return NextResponse.json({ success: true });
}
```

### 3. Frontend Duplicate Handling

```typescript
const response = await fetch("/api/newsletter", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email }),
});

const data = await response.json();

if (response.status === 409) {
  toast.info("You're already subscribed!");
  return;
}

if (!response.ok) {
  throw new Error(data.error);
}

toast.success("Thanks for subscribing!");
```

### 4. Booking/Contact Form (Create Lead)

Add contact creation without blocking the main flow:

```typescript
// In booking or contact form API route
createContact({
  email,
  firstName,
  lastName,
  company,
  source: "booking", // or "contact"
}).catch((err) => console.error("Failed to create contact:", err));
```

### 5. Inbound Email Forwarding

For receiving emails via subdomain (e.g., `mail.example.com`):

**Webhook handler (`/api/webhooks/resend`):**

```typescript
case "email.received":
  const forwardTo = process.env.EMAIL_FORWARD_TO?.split(",").map(e => e.trim());

  if (!forwardTo?.length) return;

  await resend.emails.send({
    from: "Forwarded <forwarded@example.com>",
    to: forwardTo,
    replyTo: event.data.from,
    subject: `[Fwd] ${event.data.subject}`,
    html: `
      <div style="padding: 16px; background: #f5f5f5;">
        <p><strong>From:</strong> ${event.data.from}</p>
        <p><strong>To:</strong> ${event.data.to?.join(", ")}</p>
      </div>
      <hr/>
      ${event.data.html || event.data.text}
    `,
    attachments: event.data.attachments,
  });
  break;
```

## Environment Variables

```bash
# Required
RESEND_API_KEY=re_xxxxx

# Optional - for Audiences integration
RESEND_SEGMENT_NEWSLETTER=seg_xxxxx
RESEND_SEGMENT_LEADS=seg_xxxxx
RESEND_TOPIC_NEWSLETTER=top_xxxxx

# Optional - for email forwarding
EMAIL_FORWARD_TO=email1@example.com,email2@example.com
```

## Resend Dashboard Setup

**IMPORTANT: Create these in the dashboard BEFORE deploying code that uses them.**

### Create Properties

Properties must exist before the API can use them.

1. Go to Audiences → Properties tab
2. Create these properties:
   - `domain` (text) - For multi-domain account filtering
   - `source` (text) - How contact signed up (newsletter, booking, contact)
   - `company` (text) - Optional company name

### Create Segments

1. Go to Audiences → Segments
2. Create "project-newsletter" segment
3. Create "project-leads" segment
4. Copy IDs to env vars

### Create Topics

1. Go to Audiences → Topics
2. Create topic (e.g., "Project Newsletter")
3. **Defaults to**: Opt-in (subscribers must explicitly opt in)
4. **Visibility**: Public (visible on preference page) or Private
5. Copy ID to env var

### Email Receiving (Subdomain)

To receive emails without conflicting with existing email (e.g., Google Workspace):

1. **DNS**: Add MX record for subdomain
   - Name: `mail`
   - Content: `inbound-smtp.us-east-1.amazonaws.com`
   - Priority: 10

2. **Resend**: Enable receiving for `mail.yourdomain.com`

3. **Webhook**: Point to your `/api/webhooks/resend` endpoint

## Broadcasts

Use Resend dashboard for sending newsletters:

1. Go to Broadcasts → Create
2. Select segment to target
3. Use personalization: `{{{FIRST_NAME|there}}}`
4. Include unsubscribe: `{{{RESEND_UNSUBSCRIBE_URL}}}`
5. Send or schedule

## Common Patterns

### Sender Addresses

Use consistent from addresses:
- `noreply@domain.com` - Automated notifications
- `contact@domain.com` - Contact form
- `booking@domain.com` - Calendar invites
- `forwarded@domain.com` - Forwarded inbound emails

### Team Notifications

Send internal notifications to a subdomain address that forwards:
```typescript
to: ["info@mail.domain.com"]  // Forwards via webhook
```
