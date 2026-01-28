---
name: next-js-framework
description: Build production-grade React apps with Next.js 14 App Router, Server Components, and Edge Runtime
sasmp_version: "2.0.0"
bonded_agent: 01-react-fundamentals
bond_type: SECONDARY_BOND
input_validation:
  required_packages:
    - "next": ">=14.0.0"
    - "react": ">=18.0.0"
output_format:
  code_examples: tsx
  test_template: jest
error_handling:
  patterns:
    - error_boundary
    - not_found
    - loading_states
observability:
  logging: next_telemetry
  metrics: ["build_time", "fcp", "lcp"]
---

# Next.js Framework Skill

## Overview
Master Next.js for building production-ready React applications with server-side rendering, static site generation, and API routes.

## Learning Objectives
- Understand Next.js fundamentals
- Implement SSR and SSG
- Build API routes
- Optimize performance
- Deploy to production

## Quick Start

### Installation
```bash
npx create-next-app@latest my-app
cd my-app
npm run dev
```

## File-Based Routing

### Pages
```
pages/
├── index.js          → /
├── about.js          → /about
├── blog/
│   ├── index.js      → /blog
│   └── [slug].js     → /blog/:slug
└── api/
    └── hello.js      → /api/hello
```

### Dynamic Routes
```jsx
// pages/blog/[slug].js
import { useRouter } from 'next/router';

export default function BlogPost() {
  const router = useRouter();
  const { slug } = router.query;

  return <div>Post: {slug}</div>;
}
```

## Data Fetching

### Static Site Generation (SSG)
```jsx
// pages/blog/[slug].js
export async function getStaticProps({ params }) {
  const post = await fetchPost(params.slug);

  return {
    props: { post },
    revalidate: 60 // ISR: Revalidate every 60 seconds
  };
}

export async function getStaticPaths() {
  const posts = await fetchAllPosts();

  return {
    paths: posts.map(post => ({ params: { slug: post.slug } })),
    fallback: 'blocking' // or true, false
  };
}

export default function BlogPost({ post }) {
  return <div>{post.title}</div>;
}
```

### Server-Side Rendering (SSR)
```jsx
// pages/profile.js
export async function getServerSideProps(context) {
  const { req, res, params, query } = context;

  const user = await fetchUser(query.id);

  if (!user) {
    return {
      redirect: {
        destination: '/404',
        permanent: false
      }
    };
  }

  return {
    props: { user }
  };
}

export default function Profile({ user }) {
  return <div>{user.name}</div>;
}
```

### Client-Side Fetching
```jsx
import useSWR from 'swr';

function Profile() {
  const { data, error, isLoading } = useSWR('/api/user', fetcher);

  if (error) return <div>Failed to load</div>;
  if (isLoading) return <div>Loading...</div>;

  return <div>Hello {data.name}!</div>;
}
```

## API Routes

```jsx
// pages/api/users.js
export default async function handler(req, res) {
  if (req.method === 'GET') {
    const users = await fetchUsers();
    res.status(200).json(users);
  } else if (req.method === 'POST') {
    const newUser = await createUser(req.body);
    res.status(201).json(newUser);
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}

// pages/api/users/[id].js
export default async function handler(req, res) {
  const { id } = req.query;

  const user = await fetchUser(id);
  res.status(200).json(user);
}
```

## Image Optimization

```jsx
import Image from 'next/image';

function Avatar() {
  return (
    <Image
      src="/profile.jpg"
      alt="Profile"
      width={200}
      height={200}
      priority // Load immediately for LCP
    />
  );
}

// External images
<Image
  src="https://example.com/image.jpg"
  alt="External"
  width={500}
  height={300}
  loader={({ src, width }) => `${src}?w=${width}`}
/>
```

## Layouts

### App-Wide Layout
```jsx
// pages/_app.js
import Layout from '../components/Layout';

export default function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}
```

### Per-Page Layout
```jsx
// pages/dashboard.js
import DashboardLayout from '../components/DashboardLayout';

export default function Dashboard() {
  return <div>Dashboard content</div>;
}

Dashboard.getLayout = function getLayout(page) {
  return <DashboardLayout>{page}</DashboardLayout>;
};

// pages/_app.js
export default function MyApp({ Component, pageProps }) {
  const getLayout = Component.getLayout || ((page) => page);

  return getLayout(<Component {...pageProps} />);
}
```

## Metadata

```jsx
import Head from 'next/head';

export default function Page() {
  return (
    <>
      <Head>
        <title>Page Title</title>
        <meta name="description" content="Page description" />
        <meta property="og:title" content="OG Title" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div>Content</div>
    </>
  );
}
```

## Middleware

```javascript
// middleware.js
import { NextResponse } from 'next/server';

export function middleware(request) {
  const { pathname } = request.nextUrl;

  // Redirect if not authenticated
  if (pathname.startsWith('/dashboard') && !request.cookies.get('token')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: '/dashboard/:path*'
};
```

## Environment Variables

```bash
# .env.local
DATABASE_URL=postgresql://...
NEXT_PUBLIC_API_URL=https://api.example.com
```

```jsx
// Server-side only
const dbUrl = process.env.DATABASE_URL;

// Client-side accessible (NEXT_PUBLIC_ prefix)
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

## Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Self-Hosting
```bash
npm run build
npm start
```

### Docker
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

CMD ["npm", "start"]
```

## Practice Projects

1. Build blog with SSG
2. Create e-commerce site with ISR
3. Build dashboard with SSR
4. Implement authentication API
5. Create image gallery with optimization
6. Build multi-language site
7. Implement search with API routes

## Resources

- [Next.js Docs](https://nextjs.org/docs)
- [Next.js Learn](https://nextjs.org/learn)
- [Next.js Examples](https://github.com/vercel/next.js/tree/canary/examples)

---

**Difficulty**: Intermediate to Advanced
**Estimated Time**: 3-4 weeks
**Prerequisites**: React, Node.js Basics
