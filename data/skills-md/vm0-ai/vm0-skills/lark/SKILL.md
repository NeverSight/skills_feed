---
name: lark
description: Lark/Feishu API integration for messaging, group management, contacts, and calendar. Use this skill to send messages, manage chats, query contacts, and sync calendar events with Lark/Feishu.
vm0_secrets:
  - LARK_APP_SECRET
vm0_vars:
  - LARK_APP_ID
---

# Lark (Feishu) API

Complete Lark/Feishu integration for enterprise collaboration, including messaging, group management, contacts, and calendar.

## When to Use

- Send automated notifications to users or groups
- Build interactive bot workflows
- Manage group chats and members
- Query contacts and organization structure
- Sync calendar events and schedules
- Integrate Lark with other systems

## Prerequisites

Set the following environment variables:

```bash
export LARK_APP_ID=cli_xxxxx
export LARK_APP_SECRET=xxxxx
```

Get your credentials from: https://open.larkoffice.com/

### Required Permissions

Enable these API scopes in your Lark app:
- `im:message` - Send and read messages
- `im:chat` - Manage group chats
- `contact:user.base:readonly` - Read contacts
- `calendar:calendar` - Manage calendars

## Token Management

Lark uses tenant access tokens that expire after 2 hours. Use this helper to get or refresh the token:

```bash
# Get or refresh token (cached to /tmp/lark_token.json)
get_lark_token() {
  local token_file="/tmp/lark_token.json"
  local current_time=$(date +%s)

  # Check if cached token is still valid
  if [ -f "$token_file" ]; then
    local expire_time=$(jq -r '.expire_time // 0' "$token_file" 2>/dev/null || echo "0")
    if [ "$current_time" -lt "$expire_time" ]; then
      jq -r '.tenant_access_token' "$token_file"
      return 0
    fi
  fi

  # Get new token
  local response=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\": \"${LARK_APP_ID}\", \"app_secret\": \"${LARK_APP_SECRET}\"}")

  local code=$(echo "$response" | jq -r '.code // -1')
  if [ "$code" != "0" ]; then
    echo "Error: $(echo "$response" | jq -r '.msg')" >&2
    return 1
  fi

  local expire=$(echo "$response" | jq -r '.expire')
  local expire_time=$((current_time + expire - 300))
  echo "$response" | jq ". + {expire_time: $expire_time}" > "$token_file"
  jq -r '.tenant_access_token' "$token_file"
}

# Usage in commands
TOKEN=$(get_lark_token)
```

Or get token directly without caching:

```bash
TOKEN=$(bash -c 'curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"${LARK_APP_ID}\", \"app_secret\": \"${LARK_APP_SECRET}\"}"' | jq -r '.tenant_access_token')
```

## Examples

### 1. Authentication - Get Access Token

Get and display tenant access token:

Write to `/tmp/lark_request.json`:
```json
{
  "app_id": "${LARK_APP_ID}",
  "app_secret": "${LARK_APP_SECRET}"
}
```

```bash
bash -c 'curl -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json'
```

### 2. Messaging - Send Messages

#### Send Text Message to User

Write to `/tmp/lark_request.json`:
```json
{
  "receive_id": "ou_xxx",
  "msg_type": "text",
  "content": "{\"text\": \"Hello World\"}"
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

#### Send Text Message to Group Chat

Write to `/tmp/lark_request.json`:
```json
{
  "receive_id": "oc_xxx",
  "msg_type": "text",
  "content": "{\"text\": \"Group message\"}"
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

#### Send Rich Text (Post) Message

Write to `/tmp/lark_request.json`:
```json
{
  "receive_id": "ou_xxx",
  "msg_type": "post",
  "content": "{\"zh_cn\": {\"title\": \"Title\", \"content\": [[{\"tag\": \"text\", \"text\": \"Content\"}]]}}"
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

#### Send Interactive Card Message

Write to `/tmp/lark_request.json`:
```json
{
  "receive_id": "oc_xxx",
  "msg_type": "interactive",
  "content": "{\"header\": {\"title\": {\"tag\": \"plain_text\", \"content\": \"Alert\"}}, \"elements\": [{\"tag\": \"div\", \"text\": {\"tag\": \"plain_text\", \"content\": \"Message\"}}]}"
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

#### Reply to Message

Write to `/tmp/lark_request.json`:
```json
{
  "msg_type": "text",
  "content": "{\"text\": \"Reply content\"}"
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages/om_xxx/reply" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

#### Get Chat History

```bash
TOKEN=$(get_lark_token)
curl -X GET "https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id=oc_xxx&page_size=20" \
  -H "Authorization: Bearer ${TOKEN}"
```

### 3. Chat Management - Group Operations

#### Create Group Chat

Write to `/tmp/lark_request.json`:
```json
{
  "name": "Project Team",
  "description": "Project discussion group",
  "user_id_list": ["ou_xxx", "ou_yyy"]
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/chats?user_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

#### List All Chats

```bash
TOKEN=$(get_lark_token)
curl -X GET "https://open.feishu.cn/open-apis/im/v1/chats" \
  -H "Authorization: Bearer ${TOKEN}"
```

#### Get Chat Info

```bash
TOKEN=$(get_lark_token)
curl -X GET "https://open.feishu.cn/open-apis/im/v1/chats/oc_xxx" \
  -H "Authorization: Bearer ${TOKEN}"
```

#### Add Members to Chat

Write to `/tmp/lark_request.json`:
```json
{
  "id_list": ["ou_xxx", "ou_yyy"]
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/chats/oc_xxx/members?member_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

#### Remove Members from Chat

Write to `/tmp/lark_request.json`:
```json
{
  "id_list": ["ou_xxx"]
}
```

```bash
TOKEN=$(get_lark_token)
curl -X DELETE "https://open.feishu.cn/open-apis/im/v1/chats/oc_xxx/members?member_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

### 4. Contacts - Directory Queries

#### Get User Info

```bash
TOKEN=$(get_lark_token)
curl -X GET "https://open.feishu.cn/open-apis/contact/v3/users/ou_xxx?user_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}"
```

#### Search Users

Write to `/tmp/lark_request.json`:
```json
{
  "query": "John"
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/contact/v3/users/search?user_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

#### List Departments

```bash
TOKEN=$(get_lark_token)
curl -X GET "https://open.feishu.cn/open-apis/contact/v3/departments?parent_department_id=0" \
  -H "Authorization: Bearer ${TOKEN}"
```

#### Get Department Members

```bash
TOKEN=$(get_lark_token)
curl -X GET "https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=od_xxx&user_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}"
```

### 5. Calendar - Schedule Management

#### List Calendars

```bash
TOKEN=$(get_lark_token)
curl -X GET "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
  -H "Authorization: Bearer ${TOKEN}"
```

#### Create Calendar

Write to `/tmp/lark_request.json`:
```json
{
  "summary": "Project Calendar",
  "description": "Calendar for project events"
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

#### Create Calendar Event

Note: Replace `<calendar_id>` with an actual calendar ID from List Calendars API.

```bash
TOKEN=$(get_lark_token)

# Convert ISO 8601 to Unix timestamp
START_TS=$(date -d "2025-01-15T10:00:00+08:00" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S%z" "2025-01-15T10:00:00+08:00" +%s)
END_TS=$(date -d "2025-01-15T11:00:00+08:00" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S%z" "2025-01-15T11:00:00+08:00" +%s)

# Write request with timestamps
cat > /tmp/lark_request.json <<EOF
{
  "summary": "Team Meeting",
  "description": "Weekly sync",
  "start_time": {"timestamp": "${START_TS}"},
  "end_time": {"timestamp": "${END_TS}"}
}
EOF

curl -X POST "https://open.feishu.cn/open-apis/calendar/v4/calendars/<calendar_id>/events" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

#### List Calendar Events

```bash
TOKEN=$(get_lark_token)

# Convert date range
START_TS=$(date -d "2025-01-01T00:00:00+08:00" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S%z" "2025-01-01T00:00:00+08:00" +%s)
END_TS=$(date -d "2025-01-31T23:59:59+08:00" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S%z" "2025-01-31T23:59:59+08:00" +%s)

curl -X GET "https://open.feishu.cn/open-apis/calendar/v4/calendars/<calendar_id>/events?start_time=${START_TS}&end_time=${END_TS}" \
  -H "Authorization: Bearer ${TOKEN}"
```

### 6. Bot Information

#### Get Bot Info

```bash
TOKEN=$(get_lark_token)
curl -X GET "https://open.feishu.cn/open-apis/bot/v3/info" \
  -H "Authorization: Bearer ${TOKEN}"
```

## Workflows

### Send System Alert to Group

Write to `/tmp/lark_request.json`:
```json
{
  "receive_id": "oc_xxx",
  "msg_type": "interactive",
  "content": "{\"header\": {\"title\": {\"tag\": \"plain_text\", \"content\": \"System Alert\"}, \"template\": \"red\"}, \"elements\": [{\"tag\": \"div\", \"text\": {\"tag\": \"lark_md\", \"content\": \"**Error:** Service down\"}}]}"
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

### Create Team Group with Members

Write to `/tmp/lark_request.json`:
```json
{
  "name": "Q1 Project",
  "description": "Q1 project discussion",
  "user_id_list": ["ou_abc", "ou_def", "ou_ghi"]
}
```

```bash
TOKEN=$(get_lark_token)
curl -X POST "https://open.feishu.cn/open-apis/im/v1/chats?user_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

### Query Organization Structure

```bash
TOKEN=$(get_lark_token)

# Get root departments
curl -X GET "https://open.feishu.cn/open-apis/contact/v3/departments?parent_department_id=0" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.data.items[] | {id: .department_id, name: .name}'

# Get members in a department
curl -X GET "https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=od_xxx&user_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.data.items[] | {id: .user_id, name: .name}'
```

### Schedule a Meeting

```bash
TOKEN=$(get_lark_token)

START_TS=$(date -d "2025-01-20T09:00:00+08:00" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S%z" "2025-01-20T09:00:00+08:00" +%s)
END_TS=$(date -d "2025-01-20T10:30:00+08:00" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S%z" "2025-01-20T10:30:00+08:00" +%s)

# Write request with timestamps
cat > /tmp/lark_request.json <<EOF
{
  "summary": "Sprint Planning",
  "description": "Sprint 5 planning session",
  "start_time": {"timestamp": "${START_TS}"},
  "end_time": {"timestamp": "${END_TS}"}
}
EOF

curl -X POST "https://open.feishu.cn/open-apis/calendar/v4/calendars/<calendar_id>/events" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/lark_request.json
```

## Message Types Reference

| Type | msg_type | content Format |
|------|----------|----------------|
| Text | `text` | `{"text": "message"}` |
| Rich Text | `post` | `{"zh_cn": {"title": "...", "content": [...]}}` |
| Image | `image` | `{"image_key": "img_xxx"}` |
| Card | `interactive` | `{"header": {...}, "elements": [...]}` |

## ID Types Reference

| ID Type | Description | Example |
|---------|-------------|---------|
| `open_id` | User open ID (default) | `ou_xxx` |
| `user_id` | User ID | `abc123` |
| `union_id` | Union ID across apps | `on_xxx` |
| `email` | User email address | `user@example.com` |
| `chat_id` | Group chat ID | `oc_xxx` |

## Guidelines

1. **Token Management**: Tokens expire after 2 hours. Use the `get_lark_token` helper function for automatic caching and refresh.

2. **Rate Limits**: Lark has rate limits per app. Add delays for bulk operations to avoid hitting limits.

3. **ID Types**: Use `open_id` for most user operations. Use `chat_id` when targeting group chats.

4. **Card Builder**: Design complex interactive cards using Lark Card Builder: https://open.larkoffice.com/tool/cardbuilder

5. **Error Handling**: Check the `code` field in responses. `0` means success, non-zero indicates an error.

6. **Content Escaping**: Message content must be JSON-escaped when passed as string. Use `jq` to build complex payloads:
   ```bash
   CONTENT=$(jq -n --arg text "Hello" '{text: $text}')
   curl ... -d "{\"content\": \"$(echo $CONTENT | jq -c .)\"}"
   ```

7. **Date Conversion**: Calendar events require Unix timestamps. Use `date` command with appropriate flags for your OS:
   - Linux: `date -d "2025-01-15T10:00:00+08:00" +%s`
   - macOS: `date -j -f "%Y-%m-%dT%H:%M:%S%z" "2025-01-15T10:00:00+08:00" +%s`

## API Reference

- API Documentation: https://open.larkoffice.com/document/home/index
- API Explorer: https://open.larkoffice.com/api-explorer
- Card Builder: https://open.larkoffice.com/tool/cardbuilder
- Permissions: https://open.larkoffice.com/document/home/introduction-to-scope-and-authorization/overview
