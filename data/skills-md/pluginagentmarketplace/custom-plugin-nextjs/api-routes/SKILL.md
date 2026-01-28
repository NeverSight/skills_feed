---
name: api-routes
description: "Next.js API Routes - Route handlers, middleware, edge runtime"
sasmp_version: "1.3.0"
bonded_agent: nextjs-expert
bond_type: PRIMARY_BOND
---

# Api Routes Skill

## Overview

Build API endpoints with Next.js Route Handlers and middleware.

## Capabilities

- **Route Handlers**: app/api/route.ts files
- **HTTP Methods**: GET, POST, PUT, DELETE, PATCH
- **Request/Response**: Web API standard
- **Middleware**: Edge runtime processing
- **Dynamic Routes**: [param] patterns

## Examples

```ts
// app/api/users/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  const users = await db.users.findMany()
  return NextResponse.json(users)
}

export async function POST(request: Request) {
  const body = await request.json()
  const user = await db.users.create(body)
  return NextResponse.json(user, { status: 201 })
}

// app/api/users/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const user = await db.users.findById(params.id)
  return NextResponse.json(user)
}
```

## Middleware Example

```ts
// middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}
```

