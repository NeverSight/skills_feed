---
name: mailsac
description: Mailsac disposable email API via curl. Use this skill to receive test emails, validate email addresses, manage inboxes, and automate email-based QA testing.
vm0_secrets:
  - MAILSAC_API_KEY
---

# Mailsac

Use the Mailsac API via direct `curl` calls to **manage disposable email addresses for testing and QA automation**.

> Official docs: `https://docs.mailsac.com/`

---

## When to Use

Use this skill when you need to:

- **Receive test emails** in disposable inboxes
- **Validate email addresses** (check format and disposable status)
- **Automate email verification flows** in E2E tests
- **Configure webhooks** for real-time email notifications
- **Manage private email addresses** for testing

---

## Prerequisites

1. Sign up at https://mailsac.com/
2. Get your API key from the dashboard (Account > API Key)

```bash
export MAILSAC_API_KEY="your-api-key"
```

---

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://mailsac.com/api/..." --header "Mailsac-Key: $MAILSAC_API_KEY"'
> ```

## How to Use

All examples below assume you have `MAILSAC_API_KEY` set.

Base URL: `https://mailsac.com`

---

## 1. Messages - Read Emails

Retrieve and read emails from any inbox.

### List Messages in Inbox

```bash
bash -c 'curl -s "https://mailsac.com/api/addresses/test@mailsac.com/messages" --header "Mailsac-Key: $MAILSAC_API_KEY"' | jq .
```

### Read Message Content (Plain Text)

Replace `<message-id>` with the actual messageId from the list:

```bash
bash -c 'curl -s "https://mailsac.com/api/text/test@mailsac.com/<message-id>" --header "Mailsac-Key: $MAILSAC_API_KEY"'
```

### Read Message Content (HTML)

```bash
bash -c 'curl -s "https://mailsac.com/api/body/test@mailsac.com/<message-id>" --header "Mailsac-Key: $MAILSAC_API_KEY"'
```

### Get Raw SMTP Message (with headers and attachments)

```bash
bash -c 'curl -s "https://mailsac.com/api/raw/test@mailsac.com/<message-id>" --header "Mailsac-Key: $MAILSAC_API_KEY"'
```

### Get Message Headers as JSON

```bash
bash -c 'curl -s "https://mailsac.com/api/headers/test@mailsac.com/<message-id>" --header "Mailsac-Key: $MAILSAC_API_KEY"' | jq .
```

**Message Format Endpoints:**

| Endpoint | Description |
|----------|-------------|
| `/api/text/{email}/{messageId}` | Plain text body |
| `/api/body/{email}/{messageId}` | Sanitized HTML body |
| `/api/dirty/{email}/{messageId}` | Unsanitized HTML with inlined images |
| `/api/raw/{email}/{messageId}` | Complete SMTP message |
| `/api/headers/{email}/{messageId}` | JSON headers |

---

## 2. Messages - Delete

Delete single messages or purge entire inboxes.

### Delete Single Message

```bash
bash -c 'curl -s -X DELETE "https://mailsac.com/api/addresses/test@mailsac.com/messages/<message-id>" --header "Mailsac-Key: $MAILSAC_API_KEY"'
```

### Purge Entire Inbox (Enhanced Address only)

```bash
bash -c 'curl -s -X DELETE "https://mailsac.com/api/addresses/test@mailsac.com/messages" --header "Mailsac-Key: $MAILSAC_API_KEY"'
```

Note: Starred messages will NOT be purged. Unstar them first if you want to delete everything.

### Delete All Messages in Custom Domain

```bash
bash -c 'curl -s -X PUT "https://mailsac.com/api/domains/yourdomain.com/delete-all-domain-mail" --header "Mailsac-Key: $MAILSAC_API_KEY"'
```

---

## 3. Private Addresses - Reserve and Release

Manage private email addresses for exclusive use.

### Reserve a Private Address

```bash
bash -c 'curl -s -X POST "https://mailsac.com/api/addresses/mytest@mailsac.com" --header "Mailsac-Key: $MAILSAC_API_KEY"' | jq .
```

**Response:**

```json
{
  "_id": "mytest@mailsac.com",
  "owner": "your-username",
  "forward": null,
  "webhook": null,
  "webhookSlack": null,
  "enablews": false,
  "created": "2024-01-01T00:00:00.000Z",
  "updated": "2024-01-01T00:00:00.000Z"
}
```

### List Your Private Addresses

```bash
bash -c 'curl -s "https://mailsac.com/api/addresses" --header "Mailsac-Key: $MAILSAC_API_KEY"' | jq .
```

### Release a Private Address

```bash
bash -c 'curl -s -X DELETE "https://mailsac.com/api/addresses/mytest@mailsac.com" --header "Mailsac-Key: $MAILSAC_API_KEY"'
```

### Release Address and Delete All Messages

```bash
bash -c 'curl -s -X DELETE "https://mailsac.com/api/addresses/mytest@mailsac.com?deleteAddressMessages=true" --header "Mailsac-Key: $MAILSAC_API_KEY"'
```

---

## 4. Webhook Forwarding

Configure webhooks to receive email notifications in real-time.

### Set Webhook for Private Address

Write to `/tmp/mailsac_webhook.json`:

```json
{
  "webhook": "https://your-server.com/email-webhook"
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://mailsac.com/api/private-address-forwarding/mytest@mailsac.com" --header "Mailsac-Key: $MAILSAC_API_KEY" --header "Content-Type: application/json" -d @/tmp/mailsac_webhook.json' | jq .
```

### Remove Webhook

Write to `/tmp/mailsac_webhook.json`:

```json
{
  "webhook": ""
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://mailsac.com/api/private-address-forwarding/mytest@mailsac.com" --header "Mailsac-Key: $MAILSAC_API_KEY" --header "Content-Type: application/json" -d @/tmp/mailsac_webhook.json' | jq .
```

**Webhook Payload Format:**

```json
{
  "text": "Email body content",
  "subject": "Email subject",
  "from": [{"address": "sender@example.com", "name": "Sender Name"}],
  "to": [{"address": "recipient@mailsac.com", "name": ""}],
  "headers": {},
  "messageId": "unique-message-id",
  "date": "2024-01-01T00:00:00.000Z",
  "receivedDate": "2024-01-01T00:00:00.000Z",
  "raw": "Full RFC-formatted email"
}
```

---

## 5. Email Validation

Validate email addresses and detect disposable email services.

### Validate Single Email

```bash
bash -c 'curl -s "https://mailsac.com/api/validations/addresses/test@example.com" --header "Mailsac-Key: $MAILSAC_API_KEY"' | jq .
```

**Response:**

```json
{
  "email": "test@example.com",
  "isValidFormat": true,
  "isDisposable": false,
  "disposableDomains": [],
  "aliases": [],
  "domain": "example.com",
  "local": "test"
}
```

### Check if Email is Disposable

```bash
bash -c 'curl -s "https://mailsac.com/api/validations/addresses/test@mailsac.com" --header "Mailsac-Key: $MAILSAC_API_KEY"' | jq '{email, isDisposable}'
```

**Validation Response Fields:**

| Field | Description |
|-------|-------------|
| `isValidFormat` | Email syntax is valid |
| `isDisposable` | Email is from a disposable service |
| `disposableDomains` | List of identified disposable domains |
| `aliases` | Domain aliases and IP addresses |
| `domain` | Domain part of email |
| `local` | Local part of email |

---

## 6. Send Email (Outgoing)

Send emails via API (requires outgoing message credits).

Write to `/tmp/mailsac_outgoing.json`:

```json
{
  "to": "recipient@example.com",
  "from": "sender@mailsac.com",
  "subject": "Test Email",
  "text": "This is the email body content."
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://mailsac.com/api/outgoing-messages" --header "Mailsac-Key: $MAILSAC_API_KEY" --header "Content-Type: application/json" -d @/tmp/mailsac_outgoing.json' | jq .
```

Note: Sending requires purchased credits unless sending within your custom domain.

---

## 7. Attachments

Download attachments from received emails.

### Get Attachment by MD5 Hash

```bash
bash -c 'curl -s "https://mailsac.com/api/addresses/test@mailsac.com/messages/<message-id>/attachments/<attachment-md5>" --header "Mailsac-Key: $MAILSAC_API_KEY"' > attachment.bin
```

### Get Raw Message and Parse Attachments

```bash
bash -c 'curl -s "https://mailsac.com/api/raw/test@mailsac.com/<message-id>" --header "Mailsac-Key: $MAILSAC_API_KEY"' > message.eml
```

Note: For public addresses, attachments must be downloaded via API; they are not viewable on the website.

---

## 8. Star/Save Messages

Prevent messages from being auto-deleted by starring them.

### Star a Message

```bash
bash -c 'curl -s -X PUT "https://mailsac.com/api/addresses/test@mailsac.com/messages/<message-id>/star" --header "Mailsac-Key: $MAILSAC_API_KEY"' | jq .
```

---

## Practical Examples

### Wait for Email and Extract Verification Code

```bash
EMAIL="test-$(date +%s)@mailsac.com"
echo "Use this email for registration: $EMAIL"

# Poll for new message (check every 5 seconds, max 60 seconds)
for i in $(seq 1 12); do
  MESSAGES=$(bash -c 'curl -s "https://mailsac.com/api/addresses/'"$EMAIL"'/messages" --header "Mailsac-Key: $MAILSAC_API_KEY"')
  COUNT=$(echo "$MESSAGES" | jq 'length')
  if [ "$COUNT" -gt "0" ]; then
    MESSAGE_ID=$(echo "$MESSAGES" | jq -r '.[0]._id')
    echo "Message received: $MESSAGE_ID"
    bash -c 'curl -s "https://mailsac.com/api/text/'"$EMAIL"'/'"$MESSAGE_ID"'" --header "Mailsac-Key: $MAILSAC_API_KEY"'
    break
  fi
  echo "Waiting for email... ($i/12)"
  sleep 5
done
```

### List Recent Messages with Subject and Sender

```bash
bash -c 'curl -s "https://mailsac.com/api/addresses/test@mailsac.com/messages" --header "Mailsac-Key: $MAILSAC_API_KEY"' | jq '.[] | {subject, from: .from[0].address, received: .received}'
```

### Clean Up Test Inbox Before Tests

```bash
bash -c 'curl -s -X DELETE "https://mailsac.com/api/addresses/test@mailsac.com/messages" --header "Mailsac-Key: $MAILSAC_API_KEY"'
echo "Inbox purged"
```

### Check if Email Service is Disposable

```bash
bash -c 'curl -s "https://mailsac.com/api/validations/addresses/user@tempmail.com" --header "Mailsac-Key: $MAILSAC_API_KEY"' | jq 'if .isDisposable then "DISPOSABLE" else "LEGITIMATE" end'
```

---

## Response Format

### Message List Response

```json
[
  {
    "_id": "message-id-here",
    "from": [{"address": "sender@example.com", "name": "Sender"}],
    "to": [{"address": "test@mailsac.com", "name": ""}],
    "subject": "Email Subject",
    "received": "2024-01-01T00:00:00.000Z",
    "size": 1234,
    "attachments": []
  }
]
```

### Validation Response

```json
{
  "email": "test@mailsac.com",
  "isValidFormat": true,
  "isDisposable": true,
  "disposableDomains": ["mailsac.com"],
  "aliases": ["104.197.186.12"],
  "domain": "mailsac.com",
  "local": "test"
}
```

---

## Limits and Quotas

| Type | Limit |
|------|-------|
| Public address message retention | 4 days |
| Public inbox max messages | 6 |
| Max message size | 2.5 MB |
| Operations quota reset | 1st of each month (UTC) |

---

## Guidelines

1. **Public vs Private**: Public addresses are accessible by anyone; use private addresses for sensitive test data
2. **Starred messages**: Star important messages to prevent auto-deletion
3. **Rate limits**: Free accounts may experience throttling; paid plans have higher limits
4. **Webhook reliability**: Check Recent Activity page for webhook debugging
5. **Attachments security**: For security reasons, attachments on public addresses require API access
6. **Operations count**: Listing messages + reading content = 2 API operations
