---
name: TanStack Query
description: Expert guidance for TanStack Query (React Query) including queries, mutations, caching, invalidation, optimistic updates, pagination, and infinite queries. Use this when managing server state in React applications.
---

# TanStack Query (React Query)

Expert assistance with TanStack Query - Powerful data fetching for React.

## Overview

TanStack Query manages server state in React:
- **Caching**: Automatic caching and background updates
- **Refetching**: Smart refetch strategies
- **Mutations**: Optimistic updates and cache invalidation
- **DevTools**: Built-in development tools
- **TypeScript**: Full TypeScript support

## Installation

```bash
npm install @tanstack/react-query
npm install --save-dev @tanstack/react-query-devtools
```

## Setup

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      cacheTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## useQuery

```typescript
import { useQuery } from '@tanstack/react-query';

function CertificateList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['certificates'],
    queryFn: () => fetch('/api/certificates').then(res => res.json()),
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {data.map(cert => (
        <li key={cert.id}>{cert.subject}</li>
      ))}
    </ul>
  );
}
```

### Query with Parameters

```typescript
function CertificateDetail({ id }: { id: string }) {
  const { data: certificate } = useQuery({
    queryKey: ['certificate', id],
    queryFn: () => fetch(`/api/certificates/${id}`).then(res => res.json()),
  });

  return <div>{certificate?.subject}</div>;
}
```

### Dependent Queries

```typescript
function Certificate({ id }: { id: string }) {
  const { data: certificate } = useQuery({
    queryKey: ['certificate', id],
    queryFn: () => fetchCertificate(id),
  });

  // Only run if certificate exists
  const { data: ca } = useQuery({
    queryKey: ['ca', certificate?.caId],
    queryFn: () => fetchCA(certificate.caId),
    enabled: !!certificate?.caId,
  });

  return <div>{ca?.subject}</div>;
}
```

## useMutation

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

function CreateCertificate() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newCert) => {
      return fetch('/api/certificates', {
        method: 'POST',
        body: JSON.stringify(newCert),
      });
    },
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['certificates'] });
    },
  });

  return (
    <button
      onClick={() => mutation.mutate({ subject: 'CN=example.com' })}
      disabled={mutation.isPending}
    >
      {mutation.isPending ? 'Creating...' : 'Create Certificate'}
    </button>
  );
}
```

## Optimistic Updates

```typescript
const mutation = useMutation({
  mutationFn: updateCertificate,
  onMutate: async (newCert) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['certificates'] });

    // Snapshot previous value
    const previousCerts = queryClient.getQueryData(['certificates']);

    // Optimistically update
    queryClient.setQueryData(['certificates'], (old) =>
      old.map((cert) =>
        cert.id === newCert.id ? newCert : cert
      )
    );

    return { previousCerts };
  },
  onError: (err, newCert, context) => {
    // Rollback on error
    queryClient.setQueryData(['certificates'], context.previousCerts);
  },
  onSettled: () => {
    // Refetch after success or error
    queryClient.invalidateQueries({ queryKey: ['certificates'] });
  },
});
```

## Pagination

```typescript
function CertificateList() {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ['certificates', page],
    queryFn: () => fetchCertificates(page),
    keepPreviousData: true, // Keep old data while fetching new
  });

  return (
    <>
      <ul>
        {data?.certificates.map(cert => (
          <li key={cert.id}>{cert.subject}</li>
        ))}
      </ul>

      <button onClick={() => setPage(p => p - 1)} disabled={page === 1}>
        Previous
      </button>
      <button onClick={() => setPage(p => p + 1)} disabled={!data?.hasMore}>
        Next
      </button>
    </>
  );
}
```

## Infinite Queries

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';

function InfiniteCertificates() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['certificates'],
    queryFn: ({ pageParam = 1 }) => fetchCertificates(pageParam),
    getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
    initialPageParam: 1,
  });

  return (
    <>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.certificates.map(cert => (
            <div key={cert.id}>{cert.subject}</div>
          ))}
        </div>
      ))}

      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? 'Loading...' : 'Load More'}
      </button>
    </>
  );
}
```

## Cache Invalidation

```typescript
const queryClient = useQueryClient();

// Invalidate all queries
queryClient.invalidateQueries();

// Invalidate specific query
queryClient.invalidateQueries({ queryKey: ['certificates'] });

// Invalidate query with params
queryClient.invalidateQueries({ queryKey: ['certificate', '123'] });

// Invalidate all queries starting with key
queryClient.invalidateQueries({ queryKey: ['certificates'], exact: false });

// Remove query from cache
queryClient.removeQueries({ queryKey: ['certificates'] });

// Reset query to initial state
queryClient.resetQueries({ queryKey: ['certificates'] });
```

## Manual Cache Updates

```typescript
// Set query data
queryClient.setQueryData(['certificate', '123'], newCertificate);

// Update query data
queryClient.setQueryData(['certificates'], (old) =>
  old.map((cert) => cert.id === '123' ? updated : cert)
);

// Get query data
const certificates = queryClient.getQueryData(['certificates']);

// Prefetch query
await queryClient.prefetchQuery({
  queryKey: ['certificate', '123'],
  queryFn: () => fetchCertificate('123'),
});
```

## Best Practices

1. **Query Keys**: Use arrays for structured keys `['certificates', { status: 'active' }]`
2. **Stale Time**: Set appropriate stale time for your data
3. **Cache Time**: Keep data in cache longer than stale time
4. **Optimistic Updates**: Improve UX with optimistic updates
5. **Error Handling**: Handle errors gracefully
6. **Invalidation**: Invalidate related queries on mutations
7. **Pagination**: Use `keepPreviousData` for better UX
8. **DevTools**: Use DevTools for debugging
9. **TypeScript**: Define types for query data
10. **Prefetching**: Prefetch data for better performance

## Resources

- Documentation: https://tanstack.com/query
- GitHub: https://github.com/TanStack/query
