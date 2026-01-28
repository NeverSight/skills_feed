---
name: gmail
description: Gmail API via curl. Use this skill to read, send, and manage emails, labels, drafts, and threads.
vm0_secrets:
  - GMAIL_CLIENT_SECRET
  - GMAIL_REFRESH_TOKEN
vm0_vars:
  - GMAIL_CLIENT_ID
---

# Gmail API

Read, send, and manage emails via Google's Gmail REST API.

> Official docs: https://developers.google.com/workspace/gmail/api/reference/rest

---

## When to Use

Use this skill when you need to:

- Read and search emails
- Send emails or reply to threads
- Manage drafts
- Create and manage labels
- List and modify threads
- Get user profile information

---

## Prerequisites

### 1. Create Google Cloud Project

1. Go to https://console.cloud.google.com
2. Create a new project or select existing
3. Enable Gmail API: https://console.cloud.google.com/apis/library/gmail.googleapis.com

### 2. Configure OAuth Consent Screen

1. Go to https://console.cloud.google.com/apis/credentials/consent
2. Select **External** → Create
3. Fill required fields (app name, support email, developer email)
4. Click **Save and Continue** through Scopes (skip adding scopes)
5. In **Audience** section, click **Add Users** and add your Gmail address as test user
6. Save and continue to finish

### 3. Create OAuth Client ID

1. Go to https://console.cloud.google.com/apis/credentials
2. Click **Create Credentials** → **OAuth client ID**
3. Choose **Web application** (not Desktop)
4. Add Authorized redirect URI: `https://developers.google.com/oauthplayground`
5. Click Create and note the **Client ID** and **Client Secret**

### 4. Get Refresh Token (OAuth Playground)

1. Go to https://developers.google.com/oauthplayground/
2. Click **Settings** (gear icon ⚙️) → Check **Use your own OAuth credentials**
3. Enter your Client ID and Client Secret
4. In the left panel, enter scope: `https://www.googleapis.com/auth/gmail.modify`
5. Click **Authorize APIs** → Sign in with your test user account
6. Click **Exchange authorization code for tokens**
7. Copy the **Refresh token**

### 5. Set Environment Variables

```bash
export GMAIL_CLIENT_ID="your-client-id"
export GMAIL_CLIENT_SECRET="your-client-secret"
export GMAIL_REFRESH_TOKEN="your-refresh-token"
```

---

## Get Access Token

Access tokens expire after 1 hour. Use refresh token to get a new one and save to `/tmp`:

```bash
bash -c 'curl -s -X POST "https://oauth2.googleapis.com/token" -d "client_id=$GMAIL_CLIENT_ID" -d "client_secret=$GMAIL_CLIENT_SECRET" -d "refresh_token=$GMAIL_REFRESH_TOKEN" -d "grant_type=refresh_token"' | jq -r '.access_token' > /tmp/gmail_token.txt

# Verify token was obtained
head -c 20 /tmp/gmail_token.txt && echo "..."
```

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.

> **Placeholders:** Values in `{curly-braces}` like `{message-id}` are placeholders. Replace them with actual values when executing.

---

## User Profile

### Get Profile

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/profile" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

---

## Messages

### List Messages

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=10" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

### List Messages with Query

Search using Gmail query syntax:

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=is:unread&maxResults=10" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

Common queries:
- `is:unread` - Unread messages
- `from:example@gmail.com` - From specific sender
- `subject:hello` - Subject contains "hello"
- `after:2024/01/01` - After date
- `has:attachment` - Has attachments
- `label:INBOX` - In inbox

### Get Message

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/{message-id}" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

### Get Message (Metadata Only)

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/{message-id}?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

### Send Email

```bash
# Create RFC 2822 message and base64url encode
RAW_MESSAGE=$(echo -e "To: {recipient-email}\r\nSubject: {subject}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{body-text}" | base64 | tr '+/' '-_' | tr -d '=')
```

Write to `/tmp/gmail_request.json`:

```json
{
  "raw": "$RAW_MESSAGE"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/messages/send" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)" --header "Content-Type: application/json" -d @/tmp/gmail_request.json'
```

### Reply to Thread

```bash
# Include In-Reply-To and References headers for proper threading
RAW_MESSAGE=$(echo -e "To: {recipient-email}\r\nSubject: Re: {original-subject}\r\nIn-Reply-To: <{original-message-id}>\r\nReferences: <{original-message-id}>\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{reply-text}" | base64 | tr '+/' '-_' | tr -d '=')
```

Write to `/tmp/gmail_request.json`:

```json
{
  "raw": "$RAW_MESSAGE",
  "threadId": "{thread-id}"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/messages/send" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)" --header "Content-Type: application/json" -d @/tmp/gmail_request.json'
```

### Modify Message Labels

Write to `/tmp/gmail_request.json`:

```json
{
  "addLabelIds": ["STARRED"],
  "removeLabelIds": ["UNREAD"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/messages/{message-id}/modify" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)" --header "Content-Type: application/json" -d @/tmp/gmail_request.json'
```

### Trash Message

```bash
bash -c 'curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/messages/{message-id}/trash" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

### Delete Message Permanently

```bash
bash -c 'curl -s -X DELETE "https://gmail.googleapis.com/gmail/v1/users/me/messages/{message-id}" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

---

## Threads

### List Threads

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/threads?maxResults=10" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

### Get Thread

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/threads/{thread-id}" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

### Trash Thread

```bash
bash -c 'curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/threads/{thread-id}/trash" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

---

## Labels

### List Labels

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/labels" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"' | jq '.labels[] | {id, name, type}'
```

### Create Label

Write to `/tmp/gmail_request.json`:

```json
{
  "name": "{label-name}",
  "labelListVisibility": "labelShow",
  "messageListVisibility": "show"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/labels" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)" --header "Content-Type: application/json" -d @/tmp/gmail_request.json'
```

### Delete Label

```bash
bash -c 'curl -s -X DELETE "https://gmail.googleapis.com/gmail/v1/users/me/labels/{label-id}" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

---

## Drafts

### List Drafts

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/drafts" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

### Create Draft

```bash
RAW_MESSAGE=$(echo -e "To: {recipient-email}\r\nSubject: {subject}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{body-text}" | base64 | tr '+/' '-_' | tr -d '=')
```

Write to `/tmp/gmail_request.json`:

```json
{
  "message": {
    "raw": "$RAW_MESSAGE"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/drafts" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)" --header "Content-Type: application/json" -d @/tmp/gmail_request.json'
```

### Send Draft

Write to `/tmp/gmail_request.json`:

```json
{
  "id": "{draft-id}"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/drafts/send" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)" --header "Content-Type: application/json" -d @/tmp/gmail_request.json'
```

### Delete Draft

```bash
bash -c 'curl -s -X DELETE "https://gmail.googleapis.com/gmail/v1/users/me/drafts/{draft-id}" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

---

## Attachments

### Get Attachment

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/{message-id}/attachments/{attachment-id}" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"' | jq -r '.data' | base64 -d > attachment.bin
```

---

## Settings

### Get Vacation Settings

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/settings/vacation" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

### Update Vacation Settings

Write to `/tmp/gmail_request.json`:

```json
{
  "enableAutoReply": true,
  "responseSubject": "Out of Office",
  "responseBodyPlainText": "I am currently out of office.",
  "restrictToContacts": false,
  "restrictToDomain": false
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://gmail.googleapis.com/gmail/v1/users/me/settings/vacation" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)" --header "Content-Type: application/json" -d @/tmp/gmail_request.json'
```

### List Filters

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/settings/filters" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"'
```

### Create Filter

Write to `/tmp/gmail_request.json`:

```json
{
  "criteria": {
    "from": "{filter-email}"
  },
  "action": {
    "addLabelIds": ["TRASH"],
    "removeLabelIds": ["INBOX"]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/settings/filters" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)" --header "Content-Type: application/json" -d @/tmp/gmail_request.json'
```

---

## Common Scopes

| Scope | Permission |
|-------|------------|
| `gmail.readonly` | Read-only access |
| `gmail.send` | Send emails only |
| `gmail.compose` | Create drafts and send |
| `gmail.modify` | Read, send, delete, manage |
| `gmail.labels` | Manage labels only |
| `gmail.settings.basic` | Manage basic settings |
| `gmail.settings.sharing` | Manage sensitive settings |

Use full URL: `https://www.googleapis.com/auth/gmail.modify`

---

## Decode Message Body

Gmail returns message body as base64url encoded. To decode:

```bash
bash -c 'curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages/{message-id}" --header "Authorization: Bearer $(cat /tmp/gmail_token.txt)"' | jq -r '.payload.body.data // .payload.parts[0].body.data' | tr '_-' '/+' | base64 -d
```

---

## Guidelines

1. **Token Refresh**: Access tokens expire in 1 hour; always refresh before API calls
2. **Rate Limits**: Gmail API has quota limits; implement exponential backoff
3. **Batch Requests**: Use batch endpoints for multiple operations
4. **Message Format**: Messages must be RFC 2822 compliant and base64url encoded
5. **Scopes**: Request minimum required scopes for your use case

---

## API Reference

- REST Reference: https://developers.google.com/workspace/gmail/api/reference/rest
- Guides: https://developers.google.com/workspace/gmail/api/guides
- OAuth Playground: https://developers.google.com/oauthplayground/
- Scopes: https://developers.google.com/identity/protocols/oauth2/scopes#gmail
