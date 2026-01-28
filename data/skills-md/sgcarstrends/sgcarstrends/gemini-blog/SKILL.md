---
name: gemini-blog
description: Configure or debug LLM blog post generation using Vercel AI SDK and Google Gemini. Use when updating blog generation prompts, fixing AI integration issues, or modifying content generation logic.
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Gemini Blog Generation Skill

This skill helps you work with LLM-powered blog post generation in the `@sgcarstrends/ai` package.

## When to Use This Skill

- Creating or updating blog post generation prompts
- Debugging AI generation failures or quality issues
- Modifying content generation workflows
- Adding new blog post types or formats
- Optimising AI model parameters
- Working with structured output schemas
- Configuring Langfuse telemetry

## Architecture

The blog generation system uses a **2-step flow** with Vercel AI SDK and Google Gemini:

```
packages/ai/
├── src/
│   ├── index.ts              # Package exports
│   ├── generate-post.ts      # 2-step generation functions
│   ├── config.ts             # System instructions (analysis + generation)
│   ├── schemas.ts            # Zod schemas (postSchema, highlightSchema)
│   ├── tags.ts               # Tag constants (CARS_TAGS, COE_TAGS)
│   ├── hero-images.ts        # Hero image URLs and helpers
│   ├── queries.ts            # Database queries for data aggregation
│   ├── save-post.ts          # Post persistence with idempotency
│   └── instrumentation.ts    # Langfuse telemetry setup
└── package.json
```

### 2-Step Generation Flow

```
Step 1: Analysis                     Step 2: Structured Output
┌─────────────────────────┐         ┌─────────────────────────┐
│ generateText()          │         │ generateObject()        │
│ + Code Execution Tool   │   ──▶   │ + postSchema            │
│ + Extended Thinking     │         │ + Field Descriptions    │
│ = Accurate calculations │         │ = Type-safe output      │
└─────────────────────────┘         └─────────────────────────┘
```

**Why 2 steps?**
1. **Step 1 (Analysis)**: Code Execution Tool prevents hallucinations in calculations
2. **Step 2 (Generation)**: Zod schema ensures consistent, type-safe output
3. Extended thinking only in Step 1 for complex analysis (faster Step 2)

## Key Functions

### `generateBlogContent(params)`

Standalone blog generation without workflow dependency:

```typescript
import { generateBlogContent } from "@sgcarstrends/ai";

const { object, usage, response } = await generateBlogContent({
  data: tokenisedData,     // Pipe-delimited data from tokeniser
  month: "October 2024",   // Month/year for the report
  dataType: "cars",        // "cars" or "coe"
});

// object is fully typed via postSchema
console.log(object.title);      // SEO-optimised title
console.log(object.excerpt);    // Meta description
console.log(object.content);    // Markdown content
console.log(object.tags);       // Category tags
console.log(object.highlights); // Key statistics
```

### `generatePost(context, params)`

Workflow-aware generation for QStash:

```typescript
import { serve } from "@upstash/workflow/nextjs";
import { generatePost } from "@sgcarstrends/ai";

export const POST = serve(async (context) => {
  const result = await generatePost(context, {
    data: tokenisedData,
    month: "October 2024",
    dataType: "cars",
  });

  // Post is automatically:
  // - Saved to database with hero image
  // - Cache invalidated on web app
  // - Telemetry flushed

  return result;
});
```

## Structured Output Schema

### postSchema

```typescript
const postSchema = z.object({
  title: z.string()
    .max(100)
    .describe("SEO title, max 60 chars preferred"),

  excerpt: z.string()
    .max(500)
    .describe("2-3 sentence summary for meta description, ideally under 300 chars"),

  content: z.string()
    .describe("Full markdown blog post (without H1 title)"),

  tags: z.array(z.string())
    .min(1)
    .max(10)
    .describe('3-5 tags in Title Case: first tag is dataType ("Cars" or "COE")'),

  highlights: z.array(highlightSchema)
    .min(3)
    .max(10)
    .describe("3-6 key statistics for visual display"),
});
```

### highlightSchema

```typescript
const highlightSchema = z.object({
  value: z.string()
    .describe('Metric value, e.g. "52.60%", "$125,000"'),

  label: z.string()
    .describe('Short label, e.g. "Electric Vehicles Lead"'),

  detail: z.string()
    .describe('Context, e.g. "2,081 units registered"'),
});
```

## Tag Constants

Predefined vocabulary for consistent categorisation:

```typescript
// Cars-related tags
export const CARS_TAGS = [
  "Cars",
  "Registrations",
  "Fuel Types",
  "Vehicle Types",
  "Monthly Update",
  "New Registration",
  "Market Trends",
] as const;

// COE-related tags
export const COE_TAGS = [
  "COE",
  "Quota Premium",
  "1st Bidding Round",
  "2nd Bidding Round",
  "Monthly Update",
  "PQP",
] as const;

// Type extraction
export type CarsTag = (typeof CARS_TAGS)[number];
export type CoeTag = (typeof COE_TAGS)[number];
```

## System Instructions

Instructions are split for analysis vs generation:

### Analysis Instructions (`ANALYSIS_INSTRUCTIONS`)

```typescript
const ANALYSIS_INSTRUCTIONS = {
  cars: `You are a Singapore car market analyst.
Use Python code execution for ALL calculations.
Never estimate or guess numbers.

Data format: Pipe-delimited with fields:
month|make|importerType|fuelType|vehicleType|number

Required analysis:
1. Parse all records and calculate totals
2. Calculate percentages for fuel types and vehicle types
3. Identify top 10 makes by registration count
4. Compare with previous month if available
5. Identify notable trends and changes

Output: Detailed analysis with verified numbers only.`,

  coe: `You are a Singapore COE market analyst.
Use Python code execution for ALL calculations.

Data format: Pipe-delimited bidding results

Required analysis:
1. Calculate over-subscription rates per category
2. Compare premiums between bidding exercises
3. Analyse quota utilisation
4. Identify premium trends
5. Calculate month-over-month changes

Output: Detailed bidding analysis with accurate figures.`,
};
```

### Generation Instructions (`GENERATION_INSTRUCTIONS`)

```typescript
const GENERATION_INSTRUCTIONS = {
  cars: `You are a professional content writer for SG Cars Trends.
Transform the analysis into a structured blog post.

Requirements:
- Title: SEO-optimised, max 60 characters, include "Singapore" and month
- Excerpt: 2-3 sentences summarising key findings, under 300 characters
- Content: Markdown format, 500-700 words
  - Use ## for section headers (no # H1)
  - Include data tables with proper formatting
  - Explain trends and implications
- Tags: Select 3-5 from: ${CARS_TAGS.join(", ")}
  - First tag MUST be "Cars"
- Highlights: 3-6 key statistics
  - value: The metric (e.g., "52.60%", "3,245 units")
  - label: Short description (e.g., "Electric Vehicle Share")
  - detail: Context (e.g., "Up from 48% last month")

Tone: Professional, data-driven, accessible to general audience.`,

  coe: `You are a professional content writer for SG Cars Trends.
Transform the COE analysis into a structured blog post.

Requirements:
- Title: Include "COE", bidding exercise, and month
- Excerpt: Summarise premium movements and key changes
- Content: 500-700 words with two bidding tables
  - 1st Bidding Exercise results table
  - 2nd Bidding Exercise results table
  - Premium trend analysis
  - Buyer implications
- Tags: Select 3-5 from: ${COE_TAGS.join(", ")}
  - First tag MUST be "COE"
- Highlights: 3-6 key premiums and changes

Tone: Professional, informative for potential car buyers.`,
};
```

## Hero Images

Singapore-focused Unsplash images:

```typescript
const HERO_IMAGES = {
  cars: "https://images.unsplash.com/photo-1519043916581-33ecfdba3b1c", // Singapore highway
  coe: "https://images.unsplash.com/photo-1519045550819-021aa92e9312",  // Marina Bay Sands
};

// Get hero image with size parameters
export function getHeroImage(dataType: "cars" | "coe"): string {
  return `${HERO_IMAGES[dataType]}?w=1200&h=514&fit=crop`;
}
```

## Model Configuration

```typescript
import { google } from "@ai-sdk/google";

// Model: gemini-2.5-flash (fast, cost-effective)
const model = google("gemini-2.5-flash");

// Step 1: Analysis with extended thinking
await generateText({
  model,
  tools: { code_execution: google.tools.codeExecution({}) },
  providerOptions: {
    google: {
      thinkingConfig: {
        thinkingBudget: -1,  // Unlimited thinking
      },
    },
  },
  // ...
});

// Step 2: Generation (no extended thinking for speed)
await generateObject({
  model,
  schema: postSchema,
  // No thinkingConfig = faster response
});
```

## Langfuse Telemetry

Built-in telemetry for both generation steps:

### Step 1 Telemetry (Analysis)

```typescript
experimental_telemetry: {
  isEnabled: true,
  functionId: `post-analysis/${dataType}`,
  metadata: {
    month,
    dataType,
    step: "analysis",
    tags: [dataType, month, "post-analysis"],
  },
}
```

### Step 2 Telemetry (Generation)

```typescript
experimental_telemetry: {
  isEnabled: true,
  functionId: `post-generation/${dataType}`,
  metadata: {
    month,
    dataType,
    step: "generation",
    tags: [dataType, month, "post-generation"],
  },
}
```

### Tracked Metrics

- Token usage (input, output, total) per step
- API costs per generation
- Latency per step
- Model responses and errors
- Step-specific function IDs for filtering

## Database Persistence

### Save Post with Idempotency

```typescript
import { db } from "@sgcarstrends/database";
import { posts } from "@sgcarstrends/database/schema";

await db.insert(posts).values({
  title: object.title,
  slug: slugify(object.title),
  content: object.content,
  excerpt: object.excerpt,
  heroImage: getHeroImage(dataType),
  tags: object.tags,
  highlights: object.highlights,
  status: "published",
  metadata: {
    responseId: response.id,
    modelId: response.modelId,
    timestamp: response.timestamp,
    usage,
  },
  month,
  dataType,
  publishedAt: new Date(),
}).onConflictDoUpdate({
  target: [posts.month, posts.dataType],
  set: {
    title: object.title,
    content: object.content,
    excerpt: object.excerpt,
    tags: object.tags,
    highlights: object.highlights,
    modifiedAt: new Date(),
  },
});
```

### Unique Constraint

The posts table has a unique constraint on `(month, dataType)` to prevent duplicate posts:

```typescript
unique().on(table.month, table.dataType)
```

## Cache Invalidation

Automatic cache revalidation after saving:

```typescript
// Invalidate blog list and specific post caches
await fetch(`${webUrl}/api/revalidate`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-revalidate-token": process.env.REVALIDATE_TOKEN,
  },
  body: JSON.stringify({
    tags: [
      "posts:list",
      "posts:recent",
      `posts:slug:${slug}`,
    ],
  }),
});
```

## Common Tasks

### Updating Prompts

1. Edit `packages/ai/src/config.ts`
2. Modify `ANALYSIS_INSTRUCTIONS` for calculation changes
3. Modify `GENERATION_INSTRUCTIONS` for output format changes
4. Test with sample data

### Adding New Data Types

1. Add to `ANALYSIS_INSTRUCTIONS` object
2. Add to `GENERATION_INSTRUCTIONS` object
3. Add tag constants to `tags.ts`
4. Add hero image to `hero-images.ts`
5. Update `BlogGenerationParams` type

### Debugging Generation Issues

**Low Quality Output:**
1. Check analysis step output (Step 1 logs)
2. Verify Code Execution Tool is running Python
3. Review system instructions clarity
4. Check if data format matches expected pipe-delimited format

**Schema Validation Errors:**
1. Check Zod schema constraints (max lengths, array bounds)
2. Review field descriptions for clarity
3. Ensure generation instructions match schema requirements

**API Errors:**
1. Verify `GOOGLE_GENERATIVE_AI_API_KEY` is set
2. Check API quota and rate limits
3. Enable Langfuse to see full traces

### Optimising Generation

**Speed:**
- Extended thinking only in Step 1
- Use `gemini-2.5-flash` (not pro)
- Keep prompts concise

**Quality:**
- Detailed `.describe()` on schema fields
- Specific examples in instructions
- Clear constraints (word counts, formats)

**Cost:**
- Cache generated posts in database
- Use unique constraint to prevent regeneration
- Monitor token usage in Langfuse

## Environment Variables

Required:
```bash
GOOGLE_GENERATIVE_AI_API_KEY=...   # Google AI API key
DATABASE_URL=...                    # PostgreSQL connection
```

Optional (for telemetry):
```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

For cache invalidation:
```bash
NEXT_PUBLIC_SITE_URL=...           # Web app URL
REVALIDATE_TOKEN=...               # Cache revalidation token
```

## Testing

Run generation tests:
```bash
pnpm -F @sgcarstrends/ai test
```

Test in workflow:
```bash
# Start dev server
pnpm dev

# Trigger via workflow endpoint (requires authentication)
curl -X POST http://localhost:3001/workflows/cars \
  -H "Authorization: Bearer $SG_CARS_TRENDS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"month": "2024-01"}'
```

## Best Practices

1. **Always use 2-step flow** - Separate analysis from generation
2. **Never skip Code Execution** - Required for accurate calculations
3. **Use tag constants** - Maintain vocabulary consistency
4. **Enable telemetry** - Track costs and quality from the start
5. **Test with real data** - Mock data may not reveal edge cases
6. **Review generated content** - AI output should be verified
7. **Monitor Langfuse** - Track token usage and costs

## Related Skills

- `ai-structured-output` - Foundational patterns for structured output
- `schema-design` - Posts table schema and migrations
- `cache-components` - Next.js cache integration
- `workflow-management` - QStash workflow patterns
- `redis-cache` - Caching strategies

## References

- `packages/ai/CLAUDE.md` - Full package documentation
- `apps/api/CLAUDE.md` - Workflow integration details
- `packages/database/CLAUDE.md` - Posts schema documentation
- Vercel AI SDK: Use Context7 for latest documentation
- Google Gemini: Use Context7 for API reference
