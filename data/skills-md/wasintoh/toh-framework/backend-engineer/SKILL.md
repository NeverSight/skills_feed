---
name: backend-engineer
description: >
  Supabase integration specialist. Handles database schema, authentication, 
  Row Level Security (RLS), real-time subscriptions, and storage. Connects 
  existing UI to real backend. Only called AFTER UI exists with mock data.
  Triggers: connect database, connect Supabase, add auth, make login,
  backend integration, real data, authentication, database schema.
---

# Backend Engineer

Connect beautiful UI to real data. Supabase-first approach.

<core_principle>
## The Integration Promise

Working UI with mock data → Connect Supabase → Real data flows automatically

We DON'T redesign. We DON'T add features. We connect what exists.
</core_principle>

<default_to_action>
NEVER ask:
- "Which database should I use?" → Supabase (our standard)
- "What's the schema?" → Derive from existing TypeScript types
- "What type of auth do you need?" → Supabase Auth with social providers

ALWAYS do:
- Create Supabase client configuration
- Generate schema from existing types
- Setup RLS policies
- Replace mock API calls with Supabase queries
</default_to_action>

<supabase_setup>
## Initial Setup

### 1. Install Dependencies
```bash
npm install @supabase/supabase-js
```

### 2. Environment Variables
```env
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...
```

### 3. Client Configuration
```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'
import { Database } from '@/types/supabase'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient<Database>(supabaseUrl, supabaseKey)
```

### 4. Type Generation (after creating tables)
```bash
npx supabase gen types typescript --project-id xxxxx > src/types/supabase.ts
```
</supabase_setup>

<schema_patterns>
## Database Schema Patterns

### Derive from TypeScript Types
```typescript
// Existing type from dev-engineer
interface Product {
  id: string
  name: string
  description: string
  price: number
  stock: number
  category: string
  isActive: boolean
  createdAt: Date
  updatedAt: Date
}

// Becomes SQL
```

```sql
-- SQL for Supabase
create table products (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  description text,
  price decimal(10,2) not null default 0,
  stock integer not null default 0,
  category text not null,
  is_active boolean not null default true,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Auto-update updated_at
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger products_updated_at
  before update on products
  for each row execute function update_updated_at();
```

### Common Tables
```sql
-- Users (extends Supabase auth.users)
create table profiles (
  id uuid references auth.users(id) primary key,
  full_name text,
  avatar_url text,
  role text default 'user',
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Auto-create profile on signup
create or replace function handle_new_user()
returns trigger as $$
begin
  insert into profiles (id, full_name, avatar_url)
  values (
    new.id,
    new.raw_user_meta_data->>'full_name',
    new.raw_user_meta_data->>'avatar_url'
  );
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function handle_new_user();
```
</schema_patterns>

<rls_patterns>
## Row Level Security (RLS)

### Always Enable RLS
```sql
-- Enable RLS on all tables
alter table products enable row level security;
alter table profiles enable row level security;
```

### Common Policies

**Public Read, Authenticated Write**
```sql
-- Anyone can view products
create policy "Products are viewable by everyone"
  on products for select
  using (true);

-- Only authenticated users can insert
create policy "Authenticated users can create products"
  on products for insert
  to authenticated
  with check (true);

-- Only owners can update (if user_id column exists)
create policy "Users can update own products"
  on products for update
  to authenticated
  using (user_id = auth.uid());
```

**User-Owned Data**
```sql
-- Users can only see their own data
create policy "Users can view own orders"
  on orders for select
  to authenticated
  using (user_id = auth.uid());

create policy "Users can create own orders"
  on orders for insert
  to authenticated
  with check (user_id = auth.uid());
```

**Role-Based Access**
```sql
-- Admins can do everything
create policy "Admins have full access"
  on products for all
  to authenticated
  using (
    exists (
      select 1 from profiles
      where profiles.id = auth.uid()
      and profiles.role = 'admin'
    )
  );
```
</rls_patterns>

<auth_patterns>
## Authentication

### Setup Auth Provider
```typescript
// src/lib/auth.ts
import { supabase } from './supabase'

export async function signInWithEmail(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  })
  if (error) throw error
  return data
}

export async function signUp(email: string, password: string, fullName: string) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: { full_name: fullName }
    }
  })
  if (error) throw error
  return data
}

export async function signInWithGoogle() {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${window.location.origin}/auth/callback`
    }
  })
  if (error) throw error
  return data
}

export async function signInWithLine() {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'line' as any, // LINE needs custom setup
    options: {
      redirectTo: `${window.location.origin}/auth/callback`
    }
  })
  if (error) throw error
  return data
}

export async function signOut() {
  const { error } = await supabase.auth.signOut()
  if (error) throw error
}

export async function getCurrentUser() {
  const { data: { user } } = await supabase.auth.getUser()
  return user
}
```

### Auth Context
```tsx
// src/providers/auth-provider.tsx
'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import { User, Session } from '@supabase/supabase-js'
import { supabase } from '@/lib/supabase'

interface AuthContextType {
  user: User | null
  session: Session | null
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  session: null,
  isLoading: true,
})

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setUser(session?.user ?? null)
      setIsLoading(false)
    })

    // Listen for changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session)
        setUser(session?.user ?? null)
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  return (
    <AuthContext.Provider value={{ user, session, isLoading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
```

### Protected Routes (Next.js Middleware)
```typescript
// src/middleware.ts
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  const supabase = createMiddlewareClient({ req, res })
  const { data: { session } } = await supabase.auth.getSession()

  // Protected routes
  if (!session && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url))
  }

  // Redirect logged-in users from auth pages
  if (session && (req.nextUrl.pathname === '/login' || req.nextUrl.pathname === '/register')) {
    return NextResponse.redirect(new URL('/dashboard', req.url))
  }

  return res
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/register']
}
```
</auth_patterns>

<query_patterns>
## Database Queries

### CRUD Operations
```typescript
// src/lib/api/products.ts
import { supabase } from '@/lib/supabase'
import { Product, CreateProductInput, PaginatedResponse } from '@/types'

export async function getProducts(
  page = 1, 
  pageSize = 10,
  search?: string
): Promise<PaginatedResponse<Product>> {
  let query = supabase
    .from('products')
    .select('*', { count: 'exact' })
  
  if (search) {
    query = query.ilike('name', `%${search}%`)
  }
  
  const from = (page - 1) * pageSize
  const to = from + pageSize - 1
  
  const { data, error, count } = await query
    .range(from, to)
    .order('created_at', { ascending: false })
  
  if (error) throw error
  
  return {
    data: data ?? [],
    total: count ?? 0,
    page,
    pageSize,
    totalPages: Math.ceil((count ?? 0) / pageSize),
  }
}

export async function getProduct(id: string): Promise<Product | null> {
  const { data, error } = await supabase
    .from('products')
    .select('*')
    .eq('id', id)
    .single()
  
  if (error) throw error
  return data
}

export async function createProduct(input: CreateProductInput): Promise<Product> {
  const { data, error } = await supabase
    .from('products')
    .insert(input)
    .select()
    .single()
  
  if (error) throw error
  return data
}

export async function updateProduct(
  id: string, 
  input: Partial<Product>
): Promise<Product> {
  const { data, error } = await supabase
    .from('products')
    .update(input)
    .eq('id', id)
    .select()
    .single()
  
  if (error) throw error
  return data
}

export async function deleteProduct(id: string): Promise<void> {
  const { error } = await supabase
    .from('products')
    .delete()
    .eq('id', id)
  
  if (error) throw error
}
```

### Real-time Subscriptions
```typescript
// Subscribe to changes
export function subscribeToProducts(
  callback: (payload: any) => void
) {
  return supabase
    .channel('products_changes')
    .on(
      'postgres_changes',
      { event: '*', schema: 'public', table: 'products' },
      callback
    )
    .subscribe()
}

// Usage in component
useEffect(() => {
  const channel = subscribeToProducts((payload) => {
    console.log('Change received!', payload)
    refetchProducts()
  })
  
  return () => {
    supabase.removeChannel(channel)
  }
}, [])
```
</query_patterns>

<storage_patterns>
## File Storage

### Upload Files
```typescript
// src/lib/storage.ts
import { supabase } from './supabase'

export async function uploadFile(
  bucket: string,
  path: string,
  file: File
): Promise<string> {
  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(path, file, {
      cacheControl: '3600',
      upsert: false
    })
  
  if (error) throw error
  
  // Get public URL
  const { data: { publicUrl } } = supabase.storage
    .from(bucket)
    .getPublicUrl(data.path)
  
  return publicUrl
}

export async function deleteFile(bucket: string, path: string): Promise<void> {
  const { error } = await supabase.storage
    .from(bucket)
    .remove([path])
  
  if (error) throw error
}
```

### Image Upload Component
```tsx
// src/components/image-upload.tsx
'use client'

import { useState } from 'react'
import { uploadFile } from '@/lib/storage'
import { Button } from '@/components/ui/button'
import { Upload, X } from 'lucide-react'

interface ImageUploadProps {
  onUpload: (url: string) => void
  bucket?: string
}

export function ImageUpload({ onUpload, bucket = 'images' }: ImageUploadProps) {
  const [isUploading, setIsUploading] = useState(false)
  const [preview, setPreview] = useState<string | null>(null)

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    
    setIsUploading(true)
    setPreview(URL.createObjectURL(file))
    
    try {
      const path = `${Date.now()}-${file.name}`
      const url = await uploadFile(bucket, path, file)
      onUpload(url)
    } catch (error) {
      console.error('Upload failed:', error)
      setPreview(null)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="space-y-2">
      {preview ? (
        <div className="relative inline-block">
          <img src={preview} alt="Preview" className="w-32 h-32 object-cover rounded" />
          <button
            onClick={() => setPreview(null)}
            className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      ) : (
        <label className="flex flex-col items-center justify-center w-32 h-32 border-2 border-dashed rounded cursor-pointer hover:border-primary">
          <Upload className="h-8 w-8 text-slate-400" />
          <span className="text-xs text-slate-500 mt-2">Upload image</span>
          <input
            type="file"
            accept="image/*"
            onChange={handleUpload}
            className="hidden"
            disabled={isUploading}
          />
        </label>
      )}
    </div>
  )
}
```
</storage_patterns>

<migration_checklist>
## Migration Checklist (Mock → Supabase)

### Setup Phase
- [ ] Create Supabase project
- [ ] Add environment variables
- [ ] Install @supabase/supabase-js
- [ ] Create supabase client

### Schema Phase
- [ ] Convert TypeScript types to SQL
- [ ] Create tables in Supabase
- [ ] Setup triggers (updated_at, etc.)
- [ ] Generate TypeScript types from schema

### Security Phase
- [ ] Enable RLS on all tables
- [ ] Create appropriate policies
- [ ] Setup auth providers (if needed)

### Migration Phase
- [ ] Replace mock API functions with Supabase queries
- [ ] Update Zustand stores to use new API
- [ ] Test all CRUD operations
- [ ] Add real-time subscriptions (optional)

### Verification Phase
- [ ] All pages load with real data
- [ ] Create/Update/Delete works
- [ ] Auth flows work (if applicable)
- [ ] RLS policies work correctly
</migration_checklist>
