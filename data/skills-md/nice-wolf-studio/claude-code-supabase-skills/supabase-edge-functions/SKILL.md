---
name: supabase-edge-functions
description: Deploy and manage Supabase Edge Functions. Use for invoking serverless functions, deploying new functions, and managing function deployments.
---

# Supabase Edge Functions

## Overview

This skill provides operations for working with Supabase Edge Functions - serverless TypeScript/JavaScript functions that run on Deno Deploy. Use for invoking functions, deploying code, and managing function lifecycles.

## Prerequisites

**Required environment variables:**
```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-anon-or-service-role-key"
```

**Required tools:**
- Supabase CLI (`supabase` command)
- Deno (for local development)

**Install Supabase CLI:**
```bash
# macOS
brew install supabase/tap/supabase

# Linux
curl -fsSL https://github.com/supabase/cli/releases/latest/download/supabase_linux_amd64.tar.gz | tar -xz
sudo mv supabase /usr/local/bin/

# Windows (PowerShell)
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase
```

**Helper script:**
This skill uses the shared Supabase API helper for invoking functions:
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"
```

## Invoke Edge Functions

### Basic Invocation

**Invoke a function with POST:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

FUNCTION_NAME="hello-world"

supabase_post "/functions/v1/${FUNCTION_NAME}" '{
  "name": "Alice"
}'
```

**Invoke with GET:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

FUNCTION_NAME="get-data"

supabase_get "/functions/v1/${FUNCTION_NAME}?id=123"
```

### Invoke with Headers

**Pass custom headers:**
```bash
FUNCTION_NAME="authenticated-function"
USER_TOKEN="user-access-token"

curl -s -X POST \
    "${SUPABASE_URL}/functions/v1/${FUNCTION_NAME}" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${USER_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"action": "process"}'
```

### Invoke with Authentication

**Invoke function as authenticated user:**
```bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

FUNCTION_NAME="user-profile"
ACCESS_TOKEN="user-jwt-token"

curl -s -X POST \
    "${SUPABASE_URL}/functions/v1/${FUNCTION_NAME}" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{}'
```

## Function Management (CLI)

### Initialize Function

**Create a new edge function:**
```bash
# Navigate to your Supabase project directory
cd /path/to/project

# Create new function
supabase functions new my-function

# This creates: supabase/functions/my-function/index.ts
```

### Function Template

**Basic function structure:**
```typescript
// supabase/functions/my-function/index.ts

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  const { name } = await req.json()

  const data = {
    message: `Hello ${name}!`,
  }

  return new Response(
    JSON.stringify(data),
    { headers: { "Content-Type": "application/json" } },
  )
})
```

**Function with authentication:**
```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // Get JWT from Authorization header
  const authHeader = req.headers.get('Authorization')!
  const token = authHeader.replace('Bearer ', '')

  // Create Supabase client with user's token
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    { global: { headers: { Authorization: authHeader } } }
  )

  // Get authenticated user
  const { data: { user }, error } = await supabase.auth.getUser(token)

  if (error || !user) {
    return new Response('Unauthorized', { status: 401 })
  }

  return new Response(
    JSON.stringify({ message: `Hello ${user.email}!` }),
    { headers: { "Content-Type": "application/json" } },
  )
})
```

### Deploy Function

**Deploy a function to Supabase:**
```bash
# Login to Supabase (first time only)
supabase login

# Link to your project (first time only)
supabase link --project-ref your-project-ref

# Deploy specific function
supabase functions deploy my-function

# Deploy with custom environment variables
supabase functions deploy my-function \
  --env-file ./supabase/.env.local

# Deploy all functions
supabase functions deploy
```

### Set Environment Variables

**Set secrets for edge functions:**
```bash
# Set individual secret
supabase secrets set MY_SECRET_KEY=value123

# Set multiple secrets from file
# Create .env file:
# API_KEY=abc123
# DATABASE_URL=postgres://...

supabase secrets set --env-file .env

# List secrets (names only, not values)
supabase secrets list

# Unset secret
supabase secrets unset MY_SECRET_KEY
```

### Local Development

**Run functions locally:**
```bash
# Start local Supabase (includes edge functions)
supabase start

# Serve functions locally
supabase functions serve

# Serve specific function
supabase functions serve my-function --env-file ./supabase/.env.local

# Invoke local function
curl http://localhost:54321/functions/v1/my-function \
  -H "Authorization: Bearer ${SUPABASE_KEY}" \
  -d '{"name": "test"}'
```

### Delete Function

**Remove a deployed function:**
```bash
# Delete function from Supabase dashboard or using SQL
# Note: No direct CLI command to delete, must use dashboard

# Remove local function file
rm -rf supabase/functions/my-function
```

## Common Patterns

### Invoke and Process Response

```bash
#!/bin/bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

FUNCTION_NAME="process-data"

response=$(supabase_post "/functions/v1/${FUNCTION_NAME}" '{
  "action": "calculate",
  "values": [1, 2, 3, 4, 5]
}')

if [[ $? -eq 0 ]]; then
    result=$(echo "$response" | jq -r '.result')
    echo "Function result: $result"
else
    echo "Function invocation failed"
    exit 1
fi
```

### Batch Function Invocations

```bash
#!/bin/bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

FUNCTION_NAME="send-email"
RECIPIENTS=("alice@example.com" "bob@example.com" "charlie@example.com")

for email in "${RECIPIENTS[@]}"; do
    echo "Processing $email..."

    supabase_post "/functions/v1/${FUNCTION_NAME}" '{
      "to": "'"$email"'",
      "subject": "Hello",
      "body": "Test message"
    }'

    echo "✓ Sent to $email"
done
```

### Function with Retry Logic

```bash
#!/bin/bash
source "$(dirname "${BASH_SOURCE[0]}")/../../scripts/supabase-api.sh"

invoke_with_retry() {
    local function_name="$1"
    local payload="$2"
    local max_retries=3
    local retry_count=0

    while [[ $retry_count -lt $max_retries ]]; do
        if response=$(supabase_post "/functions/v1/${function_name}" "$payload" 2>&1); then
            echo "$response"
            return 0
        else
            retry_count=$((retry_count + 1))
            echo "Retry $retry_count/$max_retries..." >&2
            sleep 2
        fi
    done

    echo "Function failed after $max_retries retries" >&2
    return 1
}

# Use it
invoke_with_retry "my-function" '{"action": "process"}'
```

### Deploy Function Script

```bash
#!/bin/bash
# deploy-function.sh

FUNCTION_NAME="${1:-my-function}"

echo "Deploying function: $FUNCTION_NAME"

# Validate function exists
if [[ ! -d "supabase/functions/$FUNCTION_NAME" ]]; then
    echo "Error: Function $FUNCTION_NAME not found"
    exit 1
fi

# Deploy
if supabase functions deploy "$FUNCTION_NAME"; then
    echo "✓ Deployed successfully"

    # Test invocation
    echo "Testing function..."
    response=$(curl -s -X POST \
        "${SUPABASE_URL}/functions/v1/${FUNCTION_NAME}" \
        -H "apikey: ${SUPABASE_KEY}" \
        -H "Content-Type: application/json" \
        -d '{}')

    echo "Test response: $response"
else
    echo "✗ Deployment failed"
    exit 1
fi
```

### Monitor Function Logs

```bash
# View function logs (requires Supabase CLI)
supabase functions logs my-function

# Follow logs in real-time
supabase functions logs my-function --follow

# Filter logs by level
supabase functions logs my-function --level error

# View logs from specific time
supabase functions logs my-function --since 1h
```

## Advanced Patterns

### Function with Database Access

```typescript
// supabase/functions/get-user-data/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )

  const { userId } = await req.json()

  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('id', userId)
    .single()

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    })
  }

  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

### Function with External API Call

```typescript
// supabase/functions/fetch-weather/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  const { city } = await req.json()
  const apiKey = Deno.env.get('WEATHER_API_KEY')

  const response = await fetch(
    `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}`
  )

  const data = await response.json()

  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

### Scheduled Function (Cron)

```typescript
// supabase/functions/daily-cleanup/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // Verify request is from Supabase Cron
  const authHeader = req.headers.get('Authorization')
  if (authHeader !== `Bearer ${Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')}`) {
    return new Response('Unauthorized', { status: 401 })
  }

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )

  // Delete old records
  const { data, error } = await supabase
    .from('logs')
    .delete()
    .lt('created_at', new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString())

  return new Response(JSON.stringify({ deleted: data?.length ?? 0 }), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

**Set up cron job in Supabase Dashboard:**
```sql
-- In SQL Editor, create pg_cron job:
select cron.schedule(
  'daily-cleanup',
  '0 2 * * *', -- Run at 2 AM daily
  $$
  select
    net.http_post(
      url := 'https://your-project.supabase.co/functions/v1/daily-cleanup',
      headers := '{"Content-Type": "application/json", "Authorization": "Bearer YOUR_SERVICE_ROLE_KEY"}'::jsonb,
      body := '{}'::jsonb
    ) as request_id;
  $$
);
```

## Testing Functions

### Test Locally

```bash
# Start local environment
supabase start

# Serve function
supabase functions serve my-function

# Test with curl
curl http://localhost:54321/functions/v1/my-function \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"test": "data"}'
```

### Integration Test Script

```bash
#!/bin/bash
# test-function.sh

FUNCTION_NAME="$1"
TEST_CASES_FILE="$2"

if [[ ! -f "$TEST_CASES_FILE" ]]; then
    echo "Test cases file not found"
    exit 1
fi

echo "Testing function: $FUNCTION_NAME"

while IFS= read -r test_case; do
    echo "Test case: $test_case"

    response=$(curl -s -X POST \
        "${SUPABASE_URL}/functions/v1/${FUNCTION_NAME}" \
        -H "apikey: ${SUPABASE_KEY}" \
        -H "Content-Type: application/json" \
        -d "$test_case")

    echo "Response: $response"
    echo "---"
done < "$TEST_CASES_FILE"
```

## Error Handling

**Function errors return HTTP status codes:**

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Bad request (invalid input) |
| 401 | Unauthorized (invalid/missing auth) |
| 403 | Forbidden (insufficient permissions) |
| 500 | Internal server error (function crashed) |
| 504 | Gateway timeout (function took too long) |

**Timeout limit:** Edge functions have a 2-second CPU time limit and 150-second wall clock timeout.

## Security Best Practices

1. **Validate input**: Always validate and sanitize request data
2. **Use service role key carefully**: Only in admin functions, never expose to clients
3. **Implement authentication**: Check user tokens for protected functions
4. **Rate limiting**: Implement rate limiting for public functions
5. **Environment variables**: Store secrets in Supabase secrets, not in code
6. **CORS**: Configure CORS headers appropriately
7. **Error messages**: Don't leak sensitive information in error responses

## Performance Tips

1. **Cold starts**: Functions may have cold starts (100-200ms delay)
2. **Keep functions small**: Faster cold starts and easier debugging
3. **Cache external data**: Use in-memory caching for repeated API calls
4. **Parallel execution**: Use `Promise.all()` for concurrent operations
5. **Stream large responses**: Use streaming for large data transfers

## API Documentation

- Supabase Edge Functions: https://supabase.com/docs/guides/functions
- Deno Deploy: https://deno.com/deploy/docs
