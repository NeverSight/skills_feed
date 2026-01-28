---
name: supabase-auth
description: Manage authentication and user operations in Supabase. Use for sign up, sign in, sign out, password resets, and user management.
---

# Supabase Authentication

## Overview

This skill provides authentication and user management operations through the Supabase Auth API. Supports email/password authentication, session management, user metadata, and password recovery.

## Prerequisites

**Required environment variables:**
```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-anon-or-service-role-key"
```

**Helper script:**
This skill uses the shared Supabase API helper. Make sure to source it:
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"
```

## Common Operations

### Sign Up - Create New User

**Basic email/password signup:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

supabase_post "/auth/v1/signup" '{
  "email": "user@example.com",
  "password": "securepassword123"
}'
```

**Signup with user metadata:**
```bash
supabase_post "/auth/v1/signup" '{
  "email": "user@example.com",
  "password": "securepassword123",
  "data": {
    "first_name": "John",
    "last_name": "Doe",
    "age": 30
  }
}'
```

**Auto-confirm user (requires service role key):**
```bash
# Note: Use SUPABASE_KEY with service_role key for this
supabase_post "/auth/v1/signup" '{
  "email": "user@example.com",
  "password": "securepassword123",
  "email_confirm": true
}'
```

### Sign In - Authenticate User

**Email/password login:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

response=$(supabase_post "/auth/v1/token?grant_type=password" '{
  "email": "user@example.com",
  "password": "securepassword123"
}')

# Extract access token
access_token=$(echo "$response" | jq -r '.access_token')
refresh_token=$(echo "$response" | jq -r '.refresh_token')

echo "Access Token: $access_token"
echo "Refresh Token: $refresh_token"
```

**Response includes:**
- `access_token` - JWT token for authenticated requests
- `refresh_token` - Token to get new access token when expired
- `user` - User object with id, email, metadata
- `expires_in` - Token expiration time in seconds

### Get Current User

**Retrieve user info with access token:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

# Set your access token from login
ACCESS_TOKEN="eyJhbGc..."

curl -s -X GET \
    "${SUPABASE_URL}/auth/v1/user" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Update User

**Update user metadata:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

ACCESS_TOKEN="eyJhbGc..."

curl -s -X PUT \
    "${SUPABASE_URL}/auth/v1/user" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{
      "data": {
        "first_name": "Jane",
        "avatar_url": "https://example.com/avatar.jpg"
      }
    }'
```

**Update email:**
```bash
curl -s -X PUT \
    "${SUPABASE_URL}/auth/v1/user" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "newemail@example.com"
    }'
```

**Update password:**
```bash
curl -s -X PUT \
    "${SUPABASE_URL}/auth/v1/user" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{
      "password": "newsecurepassword123"
    }'
```

### Sign Out

**Sign out user (invalidate refresh token):**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

ACCESS_TOKEN="eyJhbGc..."

curl -s -X POST \
    "${SUPABASE_URL}/auth/v1/logout" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Refresh Token

**Get new access token using refresh token:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

REFRESH_TOKEN="your-refresh-token"

supabase_post "/auth/v1/token?grant_type=refresh_token" '{
  "refresh_token": "'"${REFRESH_TOKEN}"'"
}'
```

### Password Recovery

**Send password reset email:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

supabase_post "/auth/v1/recover" '{
  "email": "user@example.com"
}'
```

**Reset password with recovery token:**
```bash
# This is typically done through email link
# The recovery token comes from the email link

RECOVERY_TOKEN="token-from-email"

curl -s -X PUT \
    "${SUPABASE_URL}/auth/v1/user" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${RECOVERY_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{
      "password": "newpassword123"
    }'
```

### Resend Confirmation Email

**Resend email verification:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

supabase_post "/auth/v1/resend" '{
  "type": "signup",
  "email": "user@example.com"
}'
```

## Admin Operations (Service Role Key Required)

### List All Users

**Get all users (requires service role key):**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

# Make sure SUPABASE_KEY is set to service_role key
supabase_get "/auth/v1/admin/users"
```

**Paginated user list:**
```bash
# Get users with pagination
supabase_get "/auth/v1/admin/users?page=1&per_page=50"
```

### Get User by ID

**Retrieve specific user (requires service role key):**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

USER_ID="user-uuid-here"

supabase_get "/auth/v1/admin/users/${USER_ID}"
```

### Create User (Admin)

**Create user without email confirmation:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

supabase_post "/auth/v1/admin/users" '{
  "email": "admin-created@example.com",
  "password": "securepassword123",
  "email_confirm": true,
  "user_metadata": {
    "first_name": "Admin",
    "last_name": "Created"
  }
}'
```

### Update User (Admin)

**Update user as admin:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

USER_ID="user-uuid-here"

curl -s -X PUT \
    "${SUPABASE_URL}/auth/v1/admin/users/${USER_ID}" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "updated@example.com",
      "user_metadata": {
        "role": "admin"
      }
    }'
```

### Delete User (Admin)

**Delete user account:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

USER_ID="user-uuid-here"

supabase_delete "/auth/v1/admin/users/${USER_ID}"
```

## Common Patterns

### Login and Store Tokens
```bash
#!/bin/bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

# Login
response=$(supabase_post "/auth/v1/token?grant_type=password" '{
  "email": "user@example.com",
  "password": "password123"
}')

# Extract tokens
access_token=$(echo "$response" | jq -r '.access_token')
refresh_token=$(echo "$response" | jq -r '.refresh_token')
user_id=$(echo "$response" | jq -r '.user.id')

# Store in environment or file for subsequent requests
export SUPABASE_ACCESS_TOKEN="$access_token"
export SUPABASE_REFRESH_TOKEN="$refresh_token"
export SUPABASE_USER_ID="$user_id"

echo "Logged in as user: $user_id"
```

### Check if User Exists
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

# Note: This requires service role key and admin endpoint
email="check@example.com"

users=$(supabase_get "/auth/v1/admin/users")
exists=$(echo "$users" | jq --arg email "$email" '.users[] | select(.email == $email)')

if [[ -n "$exists" ]]; then
    echo "User exists"
else
    echo "User does not exist"
fi
```

### Verify JWT Token
```bash
# Tokens are JWTs - you can decode them (requires jq)
ACCESS_TOKEN="eyJhbGc..."

# Decode payload (base64)
payload=$(echo "$ACCESS_TOKEN" | cut -d. -f2 | base64 -d 2>/dev/null)
echo "$payload" | jq '.'

# Check expiration
exp=$(echo "$payload" | jq -r '.exp')
now=$(date +%s)

if [[ $now -gt $exp ]]; then
    echo "Token expired"
else
    echo "Token valid"
fi
```

## Error Handling

Common error responses:

| Status | Error | Meaning |
|--------|-------|---------|
| 400 | Invalid login credentials | Wrong email or password |
| 400 | User already registered | Email already exists |
| 401 | Invalid token | Access token expired or invalid |
| 422 | Validation error | Invalid email format or weak password |
| 429 | Too many requests | Rate limit exceeded |

```bash
if response=$(supabase_post "/auth/v1/token?grant_type=password" '{...}' 2>&1); then
    echo "Login successful"
    access_token=$(echo "$response" | jq -r '.access_token')
else
    echo "Login failed: $response"
    exit 1
fi
```

## Security Best Practices

1. **Never commit credentials**: Store tokens in environment variables or secure files
2. **Use anon key for client operations**: Public-facing authentication
3. **Use service role key carefully**: Admin operations only, never expose to clients
4. **Implement token refresh**: Refresh access tokens before they expire
5. **Enable RLS**: Configure Row Level Security policies in Supabase dashboard
6. **Validate tokens server-side**: Don't trust client-provided tokens without verification

## Session Management

**Typical flow:**
1. User signs in → Get access_token and refresh_token
2. Store tokens securely
3. Use access_token in Authorization header for authenticated requests
4. When access_token expires → Use refresh_token to get new access_token
5. User signs out → Invalidate refresh_token

**Token lifespan:**
- Access token: 1 hour (default)
- Refresh token: 30 days (default)

## API Documentation

Full Supabase Auth API documentation: https://supabase.com/docs/guides/auth
