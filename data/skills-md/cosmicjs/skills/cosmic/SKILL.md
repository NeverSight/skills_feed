---
name: cosmic
description: Build applications with Cosmic headless CMS using the JavaScript SDK. Covers Objects, Media, AI generation (text, images, video), content modeling with Metafields, and queries. Use when working with Cosmic CMS, @cosmicjs/sdk, headless content, or building JAMstack applications.
---

# Cosmic CMS

Build content-powered applications with the [Cosmic](https://www.cosmicjs.com) headless CMS.

## SDK-First Principle

**Always use the `@cosmicjs/sdk` package.** The SDK provides type-safe methods, better error handling, and cleaner syntax than raw REST calls.

```bash
bun add @cosmicjs/sdk
# or: npm install @cosmicjs/sdk
```

## Setup

```typescript
import { createBucketClient } from '@cosmicjs/sdk'

const cosmic = createBucketClient({
  bucketSlug: 'BUCKET_SLUG',
  readKey: 'BUCKET_READ_KEY',
  writeKey: 'BUCKET_WRITE_KEY' // Required for create/update/delete
})
```

Find keys in Cosmic Dashboard → Bucket → Settings → API Access.

## Objects (Content)

Objects are the core content units. Each Object belongs to an Object type (like "posts", "products").

### Read Objects

```typescript
// Get multiple Objects
const posts = await cosmic.objects
  .find({ type: 'posts' })
  .props(['id', 'title', 'slug', 'metadata'])
  .limit(10)

// Get single Object by slug
const post = await cosmic.objects
  .findOne({ type: 'posts', slug: 'hello-world' })
  .props(['title', 'slug', 'metadata'])

// Get single Object by id
const obj = await cosmic.objects
  .findOne({ id: 'object-id' })
  .props(['title', 'metadata'])
```

### Props Syntax

Use GraphQL-style syntax for nested properties:

```typescript
const props = `{
  id
  slug
  title
  metadata {
    content
    author {
      title
      metadata {
        avatar { imgix_url }
      }
    }
  }
}`
await cosmic.objects.find({ type: 'posts' }).props(props)
```

### Create Object

```typescript
await cosmic.objects.insertOne({
  title: 'My Post',
  type: 'posts', // Object type SLUG, not title
  metadata: {
    content: 'Post content here...',
    author: 'author-object-id',        // Object relationship: use id
    featured_image: 'image-name.jpg'   // Media: use name property
  }
})
```

### Update Object

```typescript
await cosmic.objects.updateOne('object-id', {
  title: 'Updated Title',
  metadata: {
    featured: true,
    categories: ['cat1-id', 'cat2-id'] // Multiple objects: array of ids
  }
})
```

### Delete Object

```typescript
await cosmic.objects.deleteOne('object-id')
```

## Object Types

Define content structure with Object types.

```typescript
// List all Object types
const types = await cosmic.objectTypes.find()

// Get single Object type
const blogType = await cosmic.objectTypes.findOne('posts')

// Create Object type with Metafields
await cosmic.objectTypes.insertOne({
  title: 'Blog Posts',
  slug: 'posts',
  singular: 'Post',
  emoji: '📝',
  metafields: [
    { title: 'Content', key: 'content', type: 'markdown', required: true },
    { title: 'Image', key: 'image', type: 'file', media_validation_type: 'image' },
    { title: 'Author', key: 'author', type: 'object', object_type: 'authors' },
    { title: 'Tags', key: 'tags', type: 'objects', object_type: 'tags' }
  ]
})
```

## Metafield Types

| Type | Description | Value Format |
|------|-------------|--------------|
| `text` | Single line text | `string` |
| `textarea` | Multi-line text | `string` |
| `markdown` | Markdown editor | `string` |
| `html-textarea` | Rich HTML editor | `string` |
| `number` | Numeric value | `number` |
| `date` | Date picker | `"YYYY-MM-DD"` |
| `switch` | Boolean toggle | `true/false` |
| `select-dropdown` | Dropdown selection | `string` |
| `radio-buttons` | Radio selection | `string` |
| `check-boxes` | Multiple selection | `string[]` |
| `file` | Single media | Media `name` |
| `files` | Multiple media | Media `name[]` |
| `object` | Single relation | Object `id` |
| `objects` | Multiple relations | Object `id[]` |
| `json` | JSON data | `object` |
| `color` | Color picker | `"#hex"` |
| `repeater` | Repeatable group | `array` |
| `parent` | Nested group | `object` |

## Queries

Filter content using MongoDB-style queries:

```typescript
// Basic filter
await cosmic.objects.find({
  type: 'products',
  'metadata.category': 'electronics'
})

// Comparison operators
await cosmic.objects.find({
  type: 'products',
  'metadata.price': { $lt: 100 }    // Less than
  // $gt, $gte, $lte, $eq, $ne also available
})

// Array matching
await cosmic.objects.find({
  type: 'products',
  'metadata.tags': { $in: ['sale', 'featured'] }  // Any match
  // $all for all must match, $nin for none match
})

// Logical operators
await cosmic.objects.find({
  type: 'products',
  $and: [
    { 'metadata.price': { $lte: 50 } },
    { 'metadata.in_stock': true }
  ]
  // $or, $not, $nor also available
})

// Text search
await cosmic.objects.find({
  type: 'posts',
  title: { $regex: 'hello', $options: 'i' }  // Case insensitive
})
```

### Query Options

```typescript
await cosmic.objects.find({ type: 'posts' })
  .props(['title', 'slug', 'metadata'])
  .sort('-created_at')  // Descending by created date
  .limit(10)
  .skip(20)             // Pagination
  .depth(2)             // Resolve nested Object relationships
  .status('any')        // 'published' | 'draft' | 'any'
```

## Media

```typescript
// List media
const media = await cosmic.media
  .find({ folder: 'images' })
  .props(['url', 'imgix_url', 'alt_text'])
  .limit(20)

// Upload media
const uploaded = await cosmic.media.insertOne({
  media: { originalname: 'photo.jpg', buffer: fileBuffer },
  folder: 'uploads',
  alt_text: 'Description of image',
  metadata: { caption: 'Photo caption' }
})

// Update media
await cosmic.media.updateOne('media-id', {
  alt_text: 'Updated alt text',
  folder: 'new-folder'
})

// Delete media
await cosmic.media.deleteOne('media-id')
```

### imgix Image Processing

All images have `imgix_url` for transformations:

```typescript
const optimized = `${media.imgix_url}?w=800&auto=format,compress`
const thumbnail = `${media.imgix_url}?w=100&h=100&fit=crop`
```

## AI Generation

Cosmic provides built-in AI capabilities for text, images, and video.

### Generate Text

```typescript
// Simple prompt
const text = await cosmic.ai.generateText({
  prompt: 'Write a product description for a coffee mug',
  model: 'claude-sonnet-4-5-20250929', // Optional
  max_tokens: 500
})
console.log(text.text)

// Chat messages
const chat = await cosmic.ai.generateText({
  messages: [
    { role: 'user', content: 'Tell me about coffee' },
    { role: 'assistant', content: 'Coffee is a beverage...' },
    { role: 'user', content: 'What about espresso?' }
  ]
})

// Analyze image or document
const analysis = await cosmic.ai.generateText({
  prompt: 'Describe this image',
  media_url: 'https://cdn.cosmicjs.com/image.jpg'
})

// Streaming
const stream = await cosmic.ai.stream({
  prompt: 'Write a blog post',
  max_tokens: 1000
})
for await (const chunk of stream) {
  process.stdout.write(chunk.text || '')
}
```

### Generate Image

```typescript
const image = await cosmic.ai.generateImage({
  prompt: 'Mountain landscape at sunset',
  model: 'gemini-3-pro-image-preview', // Default, supports up to 4K
  size: '1024x1024',
  folder: 'ai-generated',
  alt_text: 'AI mountain landscape'
})
console.log(image.media.url)

// With reference images (Gemini only)
const styled = await cosmic.ai.generateImage({
  prompt: 'Same style but with ocean',
  reference_images: ['https://cdn.cosmicjs.com/style-ref.jpg']
})
```

### Generate Video

```typescript
const video = await cosmic.ai.generateVideo({
  prompt: 'A kitten playing with yarn in sunlight',
  model: 'veo-3.1-fast-generate-preview', // Fast: 30-90s generation
  duration: 8,        // 4, 6, or 8 seconds
  resolution: '720p', // or '1080p'
  folder: 'videos'
})
console.log(video.media.url)

// With reference image as first frame
const productVideo = await cosmic.ai.generateVideo({
  prompt: 'Product rotates smoothly',
  reference_images: ['https://cdn.cosmicjs.com/product.jpg'],
  duration: 6
})

// Extend existing video
const extended = await cosmic.ai.extendVideo({
  media_id: video.media.id,
  prompt: 'The kitten walks away into the garden'
})
```

## Available AI Models

**Text:** `claude-sonnet-4-5-20250929` (recommended), `claude-opus-4-5-20251101`, `gpt-5`, `gemini-3-pro-preview`

**Image:** `gemini-3-pro-image-preview` (default, up to 4K), `dall-e-3`

**Video:** `veo-3.1-fast-generate-preview` (recommended), `veo-3.1-generate-preview` (premium)

## Framework Patterns

### Next.js App Router

```typescript
// app/posts/page.tsx
import { createBucketClient } from '@cosmicjs/sdk'

const cosmic = createBucketClient({
  bucketSlug: process.env.COSMIC_BUCKET_SLUG!,
  readKey: process.env.COSMIC_READ_KEY!
})

export default async function Posts() {
  const { objects: posts } = await cosmic.objects
    .find({ type: 'posts' })
    .props(['title', 'slug', 'metadata.excerpt'])
    .limit(10)

  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

### Server Actions

```typescript
'use server'

export async function createPost(formData: FormData) {
  const cosmic = createBucketClient({
    bucketSlug: process.env.COSMIC_BUCKET_SLUG!,
    readKey: process.env.COSMIC_READ_KEY!,
    writeKey: process.env.COSMIC_WRITE_KEY!
  })

  await cosmic.objects.insertOne({
    title: formData.get('title') as string,
    type: 'posts',
    metadata: {
      content: formData.get('content')
    }
  })
}
```

## Common Patterns

### Pagination

```typescript
const page = 1
const limit = 10

const { objects, total } = await cosmic.objects
  .find({ type: 'posts' })
  .skip((page - 1) * limit)
  .limit(limit)

const totalPages = Math.ceil(total / limit)
```

### Draft Preview

```typescript
const post = await cosmic.objects
  .findOne({ type: 'posts', slug })
  .status('any')  // Include drafts
```

### Localized Content

```typescript
const post = await cosmic.objects
  .findOne({ type: 'posts', slug, locale: 'es' })
```

## Key Reminders

1. **Object type is the SLUG** - Use `type: 'blog-posts'`, not `type: 'Blog Posts'`
2. **Media uses `name`** - Reference media by `name` property, not URL
3. **Relations use `id`** - Reference related Objects by `id`, not slug
4. **Never expose `writeKey`** - Keep it server-side only
5. **Use `props()`** - Always specify needed properties for performance
6. **imgix for images** - Use `imgix_url` with query params for optimizations

## Resources

- [Documentation](https://www.cosmicjs.com/docs)
- [API Reference](https://www.cosmicjs.com/docs/api)
- [SDK on npm](https://www.npmjs.com/package/@cosmicjs/sdk)
- [Discord Community](https://discord.gg/cosmicjs)
