---
name: zeptomail
description: Zoho ZeptoMail transactional email API. Use this skill for sending password resets, OTPs, order confirmations, and other transactional emails.
vm0_secrets:
  - ZEPTOMAIL_API_KEY
---

# Zoho ZeptoMail

Use the ZeptoMail API via `curl` to send **transactional emails** like password resets, OTPs, welcome emails, and order confirmations.

> Official docs: `https://www.zoho.com/zeptomail/help/api-home.html`

---

## When to Use

Use this skill when you need to:

- **Send transactional emails** (password resets, OTPs, confirmations)
- **Send templated emails** with dynamic merge fields
- **Batch send** to multiple recipients (up to 500)
- **Track email opens and clicks**
- **Send emails with attachments** or inline images

**Note:** ZeptoMail is for transactional emails only. For marketing/bulk emails, use Zoho Campaigns instead.

---

## Prerequisites

1. Sign up at [Zoho ZeptoMail](https://www.zoho.com/zeptomail/)
2. Add and verify your domain
3. Create a Mail Agent and get your Send Mail Token

### Get API Token

1. Go to **Mail Agents** in ZeptoMail dashboard
2. Click on your Mail Agent
3. Go to **SMTP & API** tab
4. Copy the **Send Mail Token**

```bash
export ZEPTOMAIL_API_KEY="your-send-mail-token"
```

### Pricing

- **Free tier**: 10,000 emails
- **Paid**: $2.50 per 10,000 emails

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

Base URL: `https://api.zeptomail.com/v1.1`

---

### 1. Send Basic Email

Write to `/tmp/zeptomail_request.json`:

```json
{
  "from": {
    "address": "noreply@yourdomain.com",
    "name": "Your App"
  },
  "to": [
    {
      "email_address": {
        "address": "user@example.com",
        "name": "User"
      }
    }
  ],
  "subject": "Welcome to Our Service",
  "htmlbody": "<h1>Welcome!</h1><p>Thank you for signing up.</p>"
}
```

Then run:

```bash
bash -c 'curl -s "https://api.zeptomail.com/v1.1/email" -X POST --header "Authorization: Zoho-enczapikey ${ZEPTOMAIL_API_KEY}" --header "Content-Type: application/json" -d @/tmp/zeptomail_request.json'
```

---

### 2. Send Plain Text Email

Write to `/tmp/zeptomail_request.json`:

```json
{
  "from": {
    "address": "noreply@yourdomain.com",
    "name": "Your App"
  },
  "to": [
    {
      "email_address": {
        "address": "user@example.com",
        "name": "User"
      }
    }
  ],
  "subject": "Your OTP Code",
  "textbody": "Your one-time password is: 123456\n\nThis code expires in 10 minutes."
}
```

Then run:

```bash
bash -c 'curl -s "https://api.zeptomail.com/v1.1/email" -X POST --header "Authorization: Zoho-enczapikey ${ZEPTOMAIL_API_KEY}" --header "Content-Type: application/json" -d @/tmp/zeptomail_request.json'
```

---

### 3. Send Email with Tracking

Enable open and click tracking:

Write to `/tmp/zeptomail_request.json`:

```json
{
  "from": {
    "address": "noreply@yourdomain.com",
    "name": "Your App"
  },
  "to": [
    {
      "email_address": {
        "address": "user@example.com",
        "name": "User"
      }
    }
  ],
  "subject": "Order Confirmation #12345",
  "htmlbody": "<p>Your order has been confirmed. <a href=\"https://example.com/track\">Track your order</a></p>",
  "track_clicks": true,
  "track_opens": true,
  "client_reference": "order-12345"
}
```

Then run:

```bash
bash -c 'curl -s "https://api.zeptomail.com/v1.1/email" -X POST --header "Authorization: Zoho-enczapikey ${ZEPTOMAIL_API_KEY}" --header "Content-Type: application/json" -d @/tmp/zeptomail_request.json'
```

---

### 4. Send to Multiple Recipients (CC/BCC)

Write to `/tmp/zeptomail_request.json`:

```json
{
  "from": {
    "address": "noreply@yourdomain.com",
    "name": "Your App"
  },
  "to": [
    {
      "email_address": {
        "address": "user1@example.com",
        "name": "User 1"
      }
    }
  ],
  "cc": [
    {
      "email_address": {
        "address": "user2@example.com",
        "name": "User 2"
      }
    }
  ],
  "bcc": [
    {
      "email_address": {
        "address": "admin@example.com",
        "name": "Admin"
      }
    }
  ],
  "subject": "Team Update",
  "htmlbody": "<p>Here is the latest update for the team.</p>",
  "reply_to": [
    {
      "address": "support@yourdomain.com",
      "name": "Support"
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s "https://api.zeptomail.com/v1.1/email" -X POST --header "Authorization: Zoho-enczapikey ${ZEPTOMAIL_API_KEY}" --header "Content-Type: application/json" -d @/tmp/zeptomail_request.json'
```

---

### 5. Send Email with Attachment (Base64)

```bash
# Encode file to base64
FILE_CONTENT=$(base64 -i /path/to/file.pdf)
```

Write to `/tmp/zeptomail_request.json`:

```json
{
  "from": {
    "address": "noreply@yourdomain.com",
    "name": "Your App"
  },
  "to": [
    {
      "email_address": {
        "address": "user@example.com",
        "name": "User"
      }
    }
  ],
  "subject": "Your Invoice",
  "htmlbody": "<p>Please find your invoice attached.</p>",
  "attachments": [
    {
      "name": "invoice.pdf",
      "mime_type": "application/pdf",
      "content": "${FILE_CONTENT}"
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s "https://api.zeptomail.com/v1.1/email" -X POST --header "Authorization: Zoho-enczapikey ${ZEPTOMAIL_API_KEY}" --header "Content-Type: application/json" -d @/tmp/zeptomail_request.json'
```

---

### 6. Send Email with Inline Image

```bash
# Encode image to base64
IMAGE_CONTENT=$(base64 -i /path/to/logo.png)
```

Write to `/tmp/zeptomail_request.json`:

```json
{
  "from": {
    "address": "noreply@yourdomain.com",
    "name": "Your App"
  },
  "to": [
    {
      "email_address": {
        "address": "user@example.com",
        "name": "User"
      }
    }
  ],
  "subject": "Newsletter",
  "htmlbody": "<p><img src='cid:logo'/></p><p>Welcome to our newsletter!</p>",
  "inline_images": [
    {
      "cid": "logo",
      "name": "logo.png",
      "mime_type": "image/png",
      "content": "${IMAGE_CONTENT}"
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s "https://api.zeptomail.com/v1.1/email" -X POST --header "Authorization: Zoho-enczapikey ${ZEPTOMAIL_API_KEY}" --header "Content-Type: application/json" -d @/tmp/zeptomail_request.json'
```

---

### 7. Send Templated Email

Use pre-defined templates with merge fields:

Write to `/tmp/zeptomail_request.json`:

```json
{
  "template_key": "your-template-key",
  "from": {
    "address": "noreply@yourdomain.com",
    "name": "Your App"
  },
  "to": [
    {
      "email_address": {
        "address": "user@example.com",
        "name": "User"
      }
    }
  ],
  "merge_info": {
    "user_name": "John",
    "order_id": "12345",
    "total": "$99.00"
  }
}
```

Then run:

```bash
bash -c 'curl -s "https://api.zeptomail.com/v1.1/email/template" -X POST --header "Authorization: Zoho-enczapikey ${ZEPTOMAIL_API_KEY}" --header "Content-Type: application/json" -d @/tmp/zeptomail_request.json'
```

Template example (in ZeptoMail dashboard):
```html
<p>Hi {{user_name}},</p>
<p>Your order #{{order_id}} totaling {{total}} has been shipped!</p>
```

---

### 8. Batch Send (Multiple Recipients)

Send to up to 500 recipients with personalized merge fields:

Write to `/tmp/zeptomail_request.json`:

```json
{
  "from": {
    "address": "noreply@yourdomain.com",
    "name": "Your App"
  },
  "subject": "Your Monthly Report - {{month}}",
  "htmlbody": "<p>Hi {{name}},</p><p>Here is your report for {{month}}.</p>",
  "to": [
    {
      "email_address": {
        "address": "user1@example.com",
        "name": "User 1"
      },
      "merge_info": {
        "name": "Alice",
        "month": "December"
      }
    },
    {
      "email_address": {
        "address": "user2@example.com",
        "name": "User 2"
      },
      "merge_info": {
        "name": "Bob",
        "month": "December"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s "https://api.zeptomail.com/v1.1/email/batch" -X POST --header "Authorization: Zoho-enczapikey ${ZEPTOMAIL_API_KEY}" --header "Content-Type: application/json" -d @/tmp/zeptomail_request.json'
```

---

### 9. Batch Send with Template

Write to `/tmp/zeptomail_request.json`:

```json
{
  "template_key": "your-template-key",
  "from": {
    "address": "noreply@yourdomain.com",
    "name": "Your App"
  },
  "to": [
    {
      "email_address": {
        "address": "user1@example.com",
        "name": "User 1"
      },
      "merge_info": {
        "user_name": "Alice",
        "code": "ABC123"
      }
    },
    {
      "email_address": {
        "address": "user2@example.com",
        "name": "User 2"
      },
      "merge_info": {
        "user_name": "Bob",
        "code": "XYZ789"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s "https://api.zeptomail.com/v1.1/email/template/batch" -X POST --header "Authorization: Zoho-enczapikey ${ZEPTOMAIL_API_KEY}" --header "Content-Type: application/json" -d @/tmp/zeptomail_request.json'
```

---

## Response Format

### Success Response

```json
{
  "data": [
  {
  "code": "EM_104",
  "additional_info": [],
  "message": "OK"
  }
  ],
  "message": "OK",
  "request_id": "abc123..."
}
```

### Error Response

```json
{
  "error": {
  "code": "TM_102",
  "details": [
  {
  "code": "TM_102",
  "message": "Invalid email address",
  "target": "to"
  }
  ],
  "message": "Invalid request"
  },
  "request_id": "abc123..."
}
```

---

## Common Error Codes

| Code | Description |
|------|-------------|
| TM_101 | Authentication failed (invalid token) |
| TM_102 | Invalid request parameters |
| TM_103 | Domain not verified |
| TM_104 | Rate limit exceeded |
| EM_104 | Success |

---

## Guidelines

1. **Transactional only** - Do not use for marketing or bulk promotional emails
2. **Verify domain first** - Sender address must be from a verified domain
3. **Size limit** - Total email size (headers + body + attachments) must not exceed 15 MB
4. **Batch limit** - Maximum 500 recipients per batch request
5. **Use templates** - For consistent emails, create templates in the dashboard
6. **Track reference** - Use `client_reference` to correlate emails with your transactions
7. **TLS required** - API only supports TLS v1.2+
