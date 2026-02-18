---
name: encore-frontend
description: Connect React/Next.js apps to Encore.ts backends.
---

# Frontend Integration with Encore

## Instructions

Encore provides tools to connect your frontend applications to your backend APIs.

### Generate a TypeScript Client

```bash
# Generate client for local development
encore gen client --output=./frontend/src/client.ts --env=local

# Generate client for a deployed environment
encore gen client --output=./frontend/src/client.ts --env=staging
```

This generates a fully typed client based on your API definitions.

### Using the Generated Client

```typescript
// frontend/src/client.ts is auto-generated
import Client from "./client";

const client = new Client("http://localhost:4000");

// Fully typed API calls
const user = await client.user.getUser({ id: "123" });
console.log(user.email);

const newUser = await client.user.createUser({
  email: "new@example.com",
  name: "New User",
});
```

### React Example

```tsx
// frontend/src/components/UserProfile.tsx
import { useState, useEffect } from "react";
import Client from "../client";

const client = new Client(import.meta.env.VITE_API_URL);

export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    client.user.getUser({ id: userId })
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### React with TanStack Query

```tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import Client from "../client";

const client = new Client(import.meta.env.VITE_API_URL);

export function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => client.user.getUser({ id: userId }),
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>{user.name}</div>;
}

export function CreateUserForm() {
  const queryClient = useQueryClient();
  
  const mutation = useMutation({
    mutationFn: (data: { email: string; name: string }) => 
      client.user.createUser(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    mutation.mutate({
      email: formData.get("email") as string,
      name: formData.get("name") as string,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <input name="name" required />
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Creating..." : "Create User"}
      </button>
    </form>
  );
}
```

### Next.js Server Components

```tsx
// app/users/[id]/page.tsx
import Client from "@/lib/client";

const client = new Client(process.env.API_URL);

export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await client.user.getUser({ id: params.id });
  
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### CORS Configuration

Configure CORS in your `encore.app` file:

```cue
{
    "id": "my-app",
    "global_cors": {
        "allow_origins_with_credentials": [
            "http://localhost:3000",
            "https://myapp.com",
            "https://*.myapp.com"
        ]
    }
}
```

### CORS Options

| Option | Description |
|--------|-------------|
| `allow_origins_without_credentials` | Origins allowed for non-credentialed requests (default: `["*"]`) |
| `allow_origins_with_credentials` | Origins allowed for credentialed requests (cookies, auth headers) |
| `allow_headers` | Additional request headers to allow |
| `expose_headers` | Additional response headers to expose |
| `debug` | Enable CORS debug logging |

### Authentication from Frontend

```typescript
// With the generated client
const client = new Client("http://localhost:4000");

// Set auth token
client.setAuthToken(userToken);

// Now all requests include the Authorization header
const profile = await client.user.getProfile();
```

Or manually with fetch:

```typescript
const response = await fetch("http://localhost:4000/profile", {
  headers: {
    "Authorization": `Bearer ${token}`,
  },
});
```

### Using Plain Fetch

If you prefer not to use the generated client:

```typescript
async function getUser(id: string) {
  const response = await fetch(`http://localhost:4000/users/${id}`);
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }
  return response.json();
}

async function createUser(email: string, name: string) {
  const response = await fetch("http://localhost:4000/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, name }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }
  return response.json();
}
```

### Environment Variables

```bash
# .env.local (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:4000

# .env (Vite)
VITE_API_URL=http://localhost:4000
```

### Guidelines

- Use `encore gen client` to generate typed API clients
- Regenerate the client when your API changes
- Configure CORS in `encore.app` for production domains
- Use `allow_origins_with_credentials` for authenticated requests
- Set auth tokens on the client for protected endpoints
- Use environment variables for API URLs (different per environment)
- The generated client handles errors and types automatically
