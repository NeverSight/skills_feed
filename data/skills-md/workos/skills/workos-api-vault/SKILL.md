---
name: workos-api-vault
description: WorkOS Vault API endpoints — create, read, update, delete encrypted objects.
---

<!-- refined:sha256:59789ab29ba2 -->

# WorkOS Vault API Reference

## Step 1: Fetch Documentation

**STOP. WebFetch the relevant docs for latest implementation details before proceeding.**

- https://workos.com/docs/reference/vault
- https://workos.com/docs/reference/vault/key
- https://workos.com/docs/reference/vault/key/create-data-key
- https://workos.com/docs/reference/vault/key/decrypt-data
- https://workos.com/docs/reference/vault/key/decrypt-data-key
- https://workos.com/docs/reference/vault/key/encrypt-data
- https://workos.com/docs/reference/vault/object
- https://workos.com/docs/reference/vault/object/create

_2 additional doc pages available at https://workos.com/docs_

## Authentication Setup

Set your API key as a bearer token in the Authorization header:

```bash
Authorization: Bearer sk_your_api_key_here
```

All Vault API requests require authentication. The API key must have Vault permissions enabled in the WorkOS Dashboard.

## Endpoint Catalog

### Key Management Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/vault/key/create-data-key` | Generate a new data encryption key |
| POST | `/vault/key/encrypt-data` | Encrypt data with a data key |
| POST | `/vault/key/decrypt-data` | Decrypt data with a data key |
| POST | `/vault/key/decrypt-data-key` | Decrypt an encrypted data key |

### Object Storage Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/vault/object/create` | Create a new vault object |
| GET | `/vault/object/get` | Retrieve object by ID |
| GET | `/vault/object/get-by-name` | Retrieve object by name |
| GET | `/vault/object/list` | List all vault objects |
| PUT | `/vault/object/update` | Update an existing object |
| DELETE | `/vault/object/delete` | Delete a vault object |
| GET | `/vault/object/metadata` | Get object metadata only |
| GET | `/vault/object/version` | Get specific object version |
| GET | `/vault/object/versions` | List all object versions |

## Operation Decision Tree

### Should I use Key Management or Object Storage?

**Use Key Management** (`/vault/key/*`) when:
- You need client-side encryption
- You want to encrypt data before sending to WorkOS
- You need to manage encryption keys outside WorkOS
- You're implementing envelope encryption

**Use Object Storage** (`/vault/object/*`) when:
- You want WorkOS to handle encryption automatically
- You need versioned storage for sensitive data
- You need to store and retrieve data by name or ID
- You want built-in encryption at rest

### CRUD Operations for Objects

| Action | Endpoint | When to Use |
|--------|----------|-------------|
| **Create** | `POST /vault/object/create` | First time storing data; fails if name already exists |
| **Read** | `GET /vault/object/get` | You have the object ID |
| **Read** | `GET /vault/object/get-by-name` | You know the object name |
| **Update** | `PUT /vault/object/update` | Modify existing object; creates new version |
| **Delete** | `DELETE /vault/object/delete` | Permanently remove object and all versions |
| **List** | `GET /vault/object/list` | Browse all objects; supports pagination |

## Request/Response Patterns

### Create Data Key

**Request:**
```bash
curl -X POST https://api.workos.com/vault/key/create-data-key \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "plaintext_key": "base64_encoded_plaintext_key",
  "encrypted_key": "base64_encoded_encrypted_key"
}
```

### Encrypt Data

**Request:**
```bash
curl -X POST https://api.workos.com/vault/key/encrypt-data \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "plaintext": "sensitive data to encrypt",
    "data_key": "base64_plaintext_key_from_create"
  }'
```

**Response:**
```json
{
  "ciphertext": "base64_encoded_encrypted_data"
}
```

### Create Vault Object

**Request:**
```bash
curl -X POST https://api.workos.com/vault/object/create \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "user_ssn_12345",
    "data": {
      "ssn": "123-45-6789",
      "verified_at": "2024-01-15T10:30:00Z"
    }
  }'
```

**Response:**
```json
{
  "id": "vault_obj_01H1EXAMPLE",
  "name": "user_ssn_12345",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z",
  "version": 1
}
```

### Get Vault Object

**Request:**
```bash
curl -X GET https://api.workos.com/vault/object/get?id=vault_obj_01H1EXAMPLE \
  -H "Authorization: Bearer ${WORKOS_API_KEY}"
```

**Response:**
```json
{
  "id": "vault_obj_01H1EXAMPLE",
  "name": "user_ssn_12345",
  "data": {
    "ssn": "123-45-6789",
    "verified_at": "2024-01-15T10:30:00Z"
  },
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z",
  "version": 1
}
```

### Update Vault Object

**Request:**
```bash
curl -X PUT https://api.workos.com/vault/object/update \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "vault_obj_01H1EXAMPLE",
    "data": {
      "ssn": "123-45-6789",
      "verified_at": "2024-01-20T14:00:00Z",
      "updated_by": "admin_user"
    }
  }'
```

**Response:**
```json
{
  "id": "vault_obj_01H1EXAMPLE",
  "name": "user_ssn_12345",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-20T14:00:00.000Z",
  "version": 2
}
```

### List Vault Objects

**Request:**
```bash
curl -X GET "https://api.workos.com/vault/object/list?limit=10&before=vault_obj_01H2EXAMPLE" \
  -H "Authorization: Bearer ${WORKOS_API_KEY}"
```

**Response:**
```json
{
  "data": [
    {
      "id": "vault_obj_01H1EXAMPLE",
      "name": "user_ssn_12345",
      "created_at": "2024-01-15T10:30:00.000Z",
      "updated_at": "2024-01-20T14:00:00.000Z",
      "version": 2
    }
  ],
  "list_metadata": {
    "before": "vault_obj_01H0EXAMPLE",
    "after": "vault_obj_01H2EXAMPLE"
  }
}
```

## Pagination Handling

The List Objects endpoint uses cursor-based pagination:

1. **Initial request:** `GET /vault/object/list?limit=10`
2. **Next page:** Use the `after` cursor from `list_metadata`: `GET /vault/object/list?limit=10&after=vault_obj_01H2EXAMPLE`
3. **Previous page:** Use the `before` cursor from `list_metadata`: `GET /vault/object/list?limit=10&before=vault_obj_01H0EXAMPLE`
4. **Stop condition:** When `list_metadata` is empty or `data` array is empty

Maximum `limit` value: 100 (default: 10)

## Error Code Mapping

| Status Code | Error Type | Cause | Fix |
|-------------|-----------|-------|-----|
| 400 | `invalid_request` | Missing required field (e.g., `name`, `data`, `id`) | Check request body matches expected schema from docs |
| 401 | `unauthorized` | Missing or invalid API key | Verify `WORKOS_API_KEY` is set and starts with `sk_` |
| 403 | `forbidden` | API key lacks Vault permissions | Enable Vault in WorkOS Dashboard for this API key |
| 404 | `not_found` | Object ID or name doesn't exist | Verify object exists with `list` endpoint; check for typos |
| 409 | `conflict` | Object with this name already exists | Use `update` instead, or choose a different name |
| 422 | `unprocessable_entity` | Invalid data format (e.g., `data` must be JSON object) | Ensure `data` field is a valid JSON object, not a string |
| 429 | `rate_limit_exceeded` | Too many requests | Implement exponential backoff; wait 60 seconds before retry |
| 500 | `internal_server_error` | WorkOS service error | Retry with exponential backoff; contact support if persistent |

### Specific Error Scenarios

**"Object not found" on update:**
- Cause: Object was deleted or ID is incorrect
- Fix: Use `GET /vault/object/list` to find correct ID, or create new object

**"Name already exists" on create:**
- Cause: An object with this name already exists
- Fix: Use `GET /vault/object/get-by-name` to retrieve existing object, then update it

**"Invalid data key" on encrypt/decrypt:**
- Cause: Data key is corrupted, expired, or not base64-encoded
- Fix: Generate a new data key with `POST /vault/key/create-data-key`

## Runnable Verification Commands

### Test Authentication

```bash
curl -X GET https://api.workos.com/vault/object/list \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -w "\nHTTP Status: %{http_code}\n"
```

**Expected:** Status 200 with JSON response

### Test Full Object Lifecycle

```bash
# 1. Create object
OBJECT_ID=$(curl -s -X POST https://api.workos.com/vault/object/create \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test_object_'$(date +%s)'",
    "data": {"test": "value"}
  }' | jq -r '.id')

echo "Created object: $OBJECT_ID"

# 2. Retrieve object
curl -X GET "https://api.workos.com/vault/object/get?id=$OBJECT_ID" \
  -H "Authorization: Bearer ${WORKOS_API_KEY}"

# 3. Update object
curl -X PUT https://api.workos.com/vault/object/update \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "'$OBJECT_ID'",
    "data": {"test": "updated_value"}
  }'

# 4. Delete object
curl -X DELETE https://api.workos.com/vault/object/delete \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"id": "'$OBJECT_ID'"}'
```

### Test Key Management Flow

```bash
# 1. Create data key
KEY_RESPONSE=$(curl -s -X POST https://api.workos.com/vault/key/create-data-key \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -H "Content-Type: application/json")

PLAINTEXT_KEY=$(echo $KEY_RESPONSE | jq -r '.plaintext_key')
ENCRYPTED_KEY=$(echo $KEY_RESPONSE | jq -r '.encrypted_key')

echo "Plaintext Key: $PLAINTEXT_KEY"
echo "Encrypted Key: $ENCRYPTED_KEY"

# 2. Encrypt data
CIPHERTEXT=$(curl -s -X POST https://api.workos.com/vault/key/encrypt-data \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "plaintext": "secret data",
    "data_key": "'$PLAINTEXT_KEY'"
  }' | jq -r '.ciphertext')

echo "Ciphertext: $CIPHERTEXT"

# 3. Decrypt data
curl -X POST https://api.workos.com/vault/key/decrypt-data \
  -H "Authorization: Bearer ${WORKOS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "ciphertext": "'$CIPHERTEXT'",
    "data_key": "'$PLAINTEXT_KEY'"
  }'
```

## Rate Limit Guidance

- **Limit:** 1000 requests per minute per API key
- **Headers:** Check `X-RateLimit-Remaining` and `X-RateLimit-Reset` in responses
- **Retry strategy:** When you receive 429:
  1. Wait 60 seconds
  2. Retry with exponential backoff (60s, 120s, 240s)
  3. Maximum 3 retries before failing

## SDK Usage Patterns

### Node.js SDK

```javascript
import { WorkOS } from '@workos-inc/node';

const workos = new WorkOS(process.env.WORKOS_API_KEY);

// Create vault object
const object = await workos.vault.createObject({
  name: 'user_ssn_12345',
  data: { ssn: '123-45-6789' }
});

// Retrieve vault object
const retrieved = await workos.vault.getObject({
  id: object.id
});

// Update vault object
const updated = await workos.vault.updateObject({
  id: object.id,
  data: { ssn: '123-45-6789', verified: true }
});

// List vault objects
const { data, listMetadata } = await workos.vault.listObjects({
  limit: 10
});

// Delete vault object
await workos.vault.deleteObject({ id: object.id });
```

### Python SDK

```python
from workos import WorkOS

workos = WorkOS(api_key=os.environ['WORKOS_API_KEY'])

# Create vault object
vault_object = workos.vault.create_object(
    name='user_ssn_12345',
    data={'ssn': '123-45-6789'}
)

# Retrieve vault object
retrieved = workos.vault.get_object(id=vault_object.id)

# Update vault object
updated = workos.vault.update_object(
    id=vault_object.id,
    data={'ssn': '123-45-6789', 'verified': True}
)

# List vault objects
result = workos.vault.list_objects(limit=10)
objects = result.data

# Delete vault object
workos.vault.delete_object(id=vault_object.id)
```

## Common Integration Patterns

### Envelope Encryption Pattern

Use this when you need client-side encryption before data reaches WorkOS:

1. Create a data key: `POST /vault/key/create-data-key`
2. Store `encrypted_key` in your database
3. Use `plaintext_key` to encrypt data locally: `POST /vault/key/encrypt-data`
4. Store `ciphertext` in your database
5. To decrypt: Use stored `encrypted_key` to get `plaintext_key`: `POST /vault/key/decrypt-data-key`
6. Decrypt data: `POST /vault/key/decrypt-data`

### Managed Storage Pattern

Use this when you want WorkOS to handle encryption:

1. Create object: `POST /vault/object/create` with plaintext data
2. Retrieve when needed: `GET /vault/object/get`
3. WorkOS encrypts/decrypts automatically

### Versioning Pattern

Track changes to sensitive data over time:

1. Create initial object: `POST /vault/object/create`
2. Update when data changes: `PUT /vault/object/update` (creates version 2, 3, etc.)
3. List all versions: `GET /vault/object/versions?id=vault_obj_01H1EXAMPLE`
4. Retrieve specific version: `GET /vault/object/version?id=vault_obj_01H1EXAMPLE&version=1`

## Related Skills

- workos-vault — Feature overview and use cases for WorkOS Vault
