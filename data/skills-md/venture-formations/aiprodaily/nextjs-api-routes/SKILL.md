---
name: nextjs-api-routes
description: Next.js 15 API route patterns, NextRequest, NextResponse, error handling, maxDuration configuration, authentication, request validation, server-side operations, route handlers, and API endpoint best practices. Use when creating API routes, handling requests, configuring timeouts, or building server-side endpoints.
---

# Next.js API Routes - Pattern Library

## Purpose

Comprehensive guide for building API routes in Next.js 15 for the AIProDaily platform, including request handling, error management, authentication, and performance optimization.

## When to Use

Automatically activates when:
- Creating new API routes in `app/api/**/*.ts`
- Working with NextRequest/NextResponse
- Configuring route timeouts
- Handling authentication
- Processing API requests
- Building server-side endpoints

---

## Quick Start: API Route Template

### Standard POST Route

```typescript
// app/api/[feature]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { supabaseAdmin } from '@/lib/supabase'

export async function POST(request: NextRequest) {
  try {
    // 1. Parse request body
    const body = await request.json()

    // 2. Validate required fields
    if (!body.campaignId) {
      return NextResponse.json(
        { error: 'Missing required field: campaignId' },
        { status: 400 }
      )
    }

    // 3. Extract newsletter context (from body or auth)
    const newsletterId = body.newsletter_id

    // 4. Perform operation
    const result = await processData(body, newsletterId)

    // 5. Return success response
    return NextResponse.json({
      success: true,
      data: result
    })

  } catch (error: any) {
    // 6. Handle errors
    console.error('[API] Error in /api/feature:', error.message)
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    )
  }
}

// 7. Configure timeout for long-running operations
export const maxDuration = 600  // 10 minutes
```

---

## Route Configuration

### maxDuration Settings

**Default**: 10 seconds
**Maximum**:
- Pro plan: 300 seconds (5 minutes) for serverless
- Pro plan: 900 seconds (15 minutes) for Edge Runtime
- Workflow steps: 800 seconds (13 minutes)

```typescript
// Short operations (default)
export const maxDuration = 10  // 10 seconds

// Medium operations (API calls, database queries)
export const maxDuration = 60  // 1 minute

// Long operations (RSS processing, content generation)
export const maxDuration = 300  // 5 minutes

// Very long operations (campaign workflow, batch processing)
export const maxDuration = 600  // 10 minutes

// Workflow steps only
export const maxDuration = 800  // 13 minutes (workflow routes only)
```

### Runtime Configuration

```typescript
// Use Edge Runtime for faster cold starts (limited Node.js APIs)
export const runtime = 'edge'

// Use Node.js runtime for full compatibility (default)
export const runtime = 'nodejs'

// Dynamic route (disable static optimization)
export const dynamic = 'force-dynamic'
```

---

## HTTP Methods

### GET Route

```typescript
export async function GET(request: NextRequest) {
  try {
    // Extract query parameters
    const searchParams = request.nextUrl.searchParams
    const campaignId = searchParams.get('campaignId')
    const newsletterId = searchParams.get('newsletter_id')

    if (!newsletterId) {
      return NextResponse.json(
        { error: 'newsletter_id required' },
        { status: 400 }
      )
    }

    // Fetch data
    const { data, error } = await supabaseAdmin
      .from('newsletter_campaigns')
      .select('id, status, date')
      .eq('newsletter_id', newsletterId)
      .eq('id', campaignId)
      .single()

    if (error) {
      throw new Error(error.message)
    }

    return NextResponse.json({ data })

  } catch (error: any) {
    console.error('[API GET] Error:', error.message)
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }
}

export const maxDuration = 30
```

### POST Route (with validation)

```typescript
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // Validate input
    const validation = validateInput(body)
    if (!validation.valid) {
      return NextResponse.json(
        { error: validation.error },
        { status: 400 }
      )
    }

    // Process request
    const result = await processRequest(body)

    return NextResponse.json({
      success: true,
      data: result
    })

  } catch (error: any) {
    console.error('[API POST] Error:', error.message)
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }
}

function validateInput(body: any): { valid: boolean; error?: string } {
  if (!body.newsletter_id) {
    return { valid: false, error: 'newsletter_id is required' }
  }
  if (!body.campaignId) {
    return { valid: false, error: 'campaignId is required' }
  }
  return { valid: true }
}

export const maxDuration = 120
```

### PUT Route (update)

```typescript
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const { id, newsletter_id, ...updates } = body

    if (!id || !newsletter_id) {
      return NextResponse.json(
        { error: 'id and newsletter_id required' },
        { status: 400 }
      )
    }

    const { data, error } = await supabaseAdmin
      .from('articles')
      .update(updates)
      .eq('id', id)
      .eq('newsletter_id', newsletter_id)
      .select()
      .single()

    if (error) {
      throw new Error(error.message)
    }

    return NextResponse.json({ data })

  } catch (error: any) {
    console.error('[API PUT] Error:', error.message)
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }
}

export const maxDuration = 30
```

### DELETE Route

```typescript
export async function DELETE(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const id = searchParams.get('id')
    const newsletterId = searchParams.get('newsletter_id')

    if (!id || !newsletterId) {
      return NextResponse.json(
        { error: 'id and newsletter_id required' },
        { status: 400 }
      )
    }

    const { error } = await supabaseAdmin
      .from('articles')
      .delete()
      .eq('id', id)
      .eq('newsletter_id', newsletterId)

    if (error) {
      throw new Error(error.message)
    }

    return NextResponse.json({ success: true })

  } catch (error: any) {
    console.error('[API DELETE] Error:', error.message)
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }
}

export const maxDuration = 30
```

---

## Dynamic Routes

### Route with Parameters

```typescript
// app/api/campaigns/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const campaignId = params.id
    const searchParams = request.nextUrl.searchParams
    const newsletterId = searchParams.get('newsletter_id')

    if (!newsletterId) {
      return NextResponse.json(
        { error: 'newsletter_id required' },
        { status: 400 }
      )
    }

    const { data, error } = await supabaseAdmin
      .from('newsletter_campaigns')
      .select('*')
      .eq('id', campaignId)
      .eq('newsletter_id', newsletterId)
      .single()

    if (error) {
      throw new Error(error.message)
    }

    return NextResponse.json({ data })

  } catch (error: any) {
    console.error('[API] Error:', error.message)
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }
}
```

---

## Authentication Patterns

### Protected Route (Server-Side)

```typescript
import { cookies } from 'next/headers'
import { createServerClient } from '@supabase/ssr'

export async function GET(request: NextRequest) {
  try {
    // Create Supabase client with cookies
    const cookieStore = cookies()
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          get(name: string) {
            return cookieStore.get(name)?.value
          },
        },
      }
    )

    // Check authentication
    const { data: { user }, error: authError } = await supabase.auth.getUser()

    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    // Process authenticated request
    const result = await processAuthenticatedRequest(user)

    return NextResponse.json({ data: result })

  } catch (error: any) {
    console.error('[API] Error:', error.message)
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }
}
```

### CRON Secret Validation

```typescript
export async function GET(request: NextRequest) {
  try {
    // Validate CRON secret
    const authHeader = request.headers.get('authorization')
    const cronSecret = process.env.CRON_SECRET

    if (!cronSecret || authHeader !== `Bearer ${cronSecret}`) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    // Process cron job
    const result = await processCronJob()

    return NextResponse.json({
      success: true,
      data: result
    })

  } catch (error: any) {
    console.error('[CRON] Error:', error.message)
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }
}

export const maxDuration = 300
```

---

## Error Handling Patterns

### Standard Error Handler

```typescript
function handleApiError(error: any, context: string) {
  console.error(`[API Error - ${context}]`, {
    message: error.message,
    stack: error.stack,
    timestamp: new Date().toISOString()
  })

  // Return user-friendly error
  return NextResponse.json(
    {
      error: error.message || 'An unexpected error occurred',
      context: context
    },
    { status: error.status || 500 }
  )
}

// Usage
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const result = await processData(body)
    return NextResponse.json({ data: result })
  } catch (error: any) {
    return handleApiError(error, 'POST /api/feature')
  }
}
```

### Validation Error Pattern

```typescript
class ValidationError extends Error {
  status = 400

  constructor(message: string) {
    super(message)
    this.name = 'ValidationError'
  }
}

function validateRequest(body: any) {
  if (!body.newsletter_id) {
    throw new ValidationError('newsletter_id is required')
  }
  if (!body.campaignId) {
    throw new ValidationError('campaignId is required')
  }
  // More validations...
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    validateRequest(body)
    const result = await processData(body)
    return NextResponse.json({ data: result })
  } catch (error: any) {
    const status = error.status || 500
    return NextResponse.json(
      { error: error.message },
      { status }
    )
  }
}
```

---

## Response Patterns

### Success Response

```typescript
return NextResponse.json({
  success: true,
  data: result,
  timestamp: new Date().toISOString()
})
```

### Error Response

```typescript
return NextResponse.json(
  {
    error: 'Descriptive error message',
    code: 'ERROR_CODE',
    details: additionalInfo
  },
  { status: 400 }
)
```

### Paginated Response

```typescript
return NextResponse.json({
  data: items,
  pagination: {
    page: currentPage,
    limit: pageSize,
    total: totalItems,
    hasMore: hasNextPage
  }
})
```

---

## Headers and CORS

### Set Custom Headers

```typescript
export async function GET(request: NextRequest) {
  const data = await fetchData()

  return NextResponse.json({ data }, {
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=30',
      'X-Custom-Header': 'value'
    }
  })
}
```

### CORS Configuration

```typescript
export async function OPTIONS(request: NextRequest) {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}

export async function POST(request: NextRequest) {
  const response = NextResponse.json({ data: result })
  response.headers.set('Access-Control-Allow-Origin', '*')
  return response
}
```

---

## Best Practices

### ✅ DO:

- Always validate input parameters
- Use appropriate maxDuration for operation length
- Filter by newsletter_id for tenant-scoped data
- Return consistent response formats
- Log errors with context
- Use try-catch for error handling
- Set appropriate HTTP status codes
- Validate authentication when needed

### ❌ DON'T:

- Expose sensitive error details to clients
- Skip input validation
- Use default 10s timeout for long operations
- Return raw database errors
- Forget to check newsletter_id
- Skip error logging
- Use inconsistent response formats

---

## Common Patterns

### Batch Processing

```typescript
export async function POST(request: NextRequest) {
  try {
    const { items, newsletter_id } = await request.json()

    const results = await Promise.all(
      items.map(item => processItem(item, newsletter_id))
    )

    return NextResponse.json({
      success: true,
      processed: results.length,
      results
    })

  } catch (error: any) {
    console.error('[API Batch] Error:', error.message)
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }
}

export const maxDuration = 300
```

### Streaming Response (for long operations)

```typescript
export async function GET(request: NextRequest) {
  const stream = new ReadableStream({
    async start(controller) {
      try {
        const items = await fetchLargeDataset()

        for (const item of items) {
          const chunk = JSON.stringify(item) + '\n'
          controller.enqueue(new TextEncoder().encode(chunk))
        }

        controller.close()
      } catch (error) {
        controller.error(error)
      }
    }
  })

  return new NextResponse(stream, {
    headers: {
      'Content-Type': 'application/x-ndjson',
      'Transfer-Encoding': 'chunked'
    }
  })
}

export const maxDuration = 600
```

---

**Skill Status**: ACTIVE ✅
**Line Count**: < 500 ✅
**Framework**: Next.js 15 App Router ✅
