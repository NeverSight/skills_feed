---
name: resend-box
description: Resend Box is a local email sandbox that mocks the Resend API and captures emails for inspection. Use this skill when working with the Resend SDK or SMTP to send emails during development. It captures all emails sent via the Resend SDK (when RESEND_BASE_URL points to the sandbox) or via SMTP (port 1025). Use to verify emails are sent correctly, inspect email content, or test email templates without sending real emails.
compatibility: Requires Resend Box server running locally (default HTTP port 4657, SMTP port 1025)
---

# Resend Box Skill

Resend Box is a local email sandbox that:

1. **Mocks the Resend API** - Drop-in replacement for `https://api.resend.com`
2. **Runs an SMTP server** - Captures emails sent via SMTP on port 1025
3. **Provides a Web UI** - View captured emails at http://127.0.0.1:4657
4. **Stores emails in-memory** - All emails are lost when the server restarts

## When to Use

- You're using the Resend SDK and want to test emails locally
- You're sending emails via SMTP and need to verify they're sent correctly
- You want to inspect email content (HTML, text, headers) during development
- You need to verify emails are sent to the correct recipients
- You're testing email templates before sending to real users

## Prerequisites

Start Resend Box:

```bash
npx resend-box start
```

Configure your project to use the sandbox - see [Setup Guide](references/setup.md).

## Quick Reference

### Send an Email (via Resend API)

```bash
curl -X POST http://127.0.0.1:4657/emails \
  -H "Content-Type: application/json" \
  -d '{
    "from": "sender@example.com",
    "to": "recipient@example.com",
    "subject": "Test Email",
    "html": "<p>Hello!</p>"
  }'
```

Required fields: `from`, `to`, `subject`
Optional fields: `html`, `text`, `cc`, `bcc`, `replyTo`

### Get All Emails

```bash
curl http://127.0.0.1:4657/sandbox/emails
```

### Filter Emails by Recipient

```bash
curl "http://127.0.0.1:4657/sandbox/emails?to=user@example.com"
```

The `to` filter is case-insensitive and supports partial matching.

### Get a Specific Email

```bash
curl http://127.0.0.1:4657/sandbox/emails/{id}
```

### Delete All Emails

```bash
curl -X DELETE http://127.0.0.1:4657/sandbox/emails
```

### View in Browser

Open http://127.0.0.1:4657 to view captured emails in the web UI.

## Detailed Documentation

- [Setup Guide](references/setup.md) - Configure your project to use Resend Box
- [Send Email Reference](references/send-email.md) - Complete API for sending emails
- [Get Emails Reference](references/get-emails.md) - Complete API for retrieving and filtering emails
