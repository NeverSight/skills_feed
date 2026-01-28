---
name: context7-auto-research
version: 1.0.1
author: BenedictKing
description: Automatically fetches up-to-date documentation from Context7 when users ask about libraries, frameworks, APIs, or need code examples. Triggers proactively without explicit user request.
allowed-tools:
  - Task
  - Bash
  - Read
  - Write
user-invocable: true
---

# Context7 Auto Research Skill

This skill automatically fetches current documentation from Context7 API when detecting library/framework-related queries, ensuring responses use up-to-date information instead of potentially outdated training data.

## Automatic Activation Triggers

This skill should activate **proactively** when the user's message contains:

### Implementation Queries (实现相关)

- "如何实现" / "怎么写" / "怎么做"
- "How do I..." / "How to..." / "How can I..."
- "Show me how to..." / "Write code for..."

### Configuration & Setup (配置相关)

- "配置" / "设置" / "安装"
- "configure" / "setup" / "install"
- "初始化" / "initialize"

### Documentation Requests (文档相关)

- "文档" / "参考" / "API"
- "documentation" / "docs" / "reference"
- "查看" / "look up"

### Library/Framework Mentions (库/框架提及)

- React, Vue, Angular, Svelte, Solid
- Next.js, Nuxt, Remix, Astro
- Express, Fastify, Koa, Hono
- Prisma, Drizzle, TypeORM
- Supabase, Firebase, Clerk
- Tailwind, shadcn/ui, Radix
- Any npm package or GitHub repository

### Code Generation Requests (代码生成)

- "生成代码" / "写一个" / "创建"
- "generate" / "create" / "build"
- "implement" / "add feature"

## Research Process

When triggered, follow this workflow:

### Step 1: Extract Library Information

Identify the library/framework from the user's query:

- Library name (e.g., "react", "next.js", "prisma")
- Version if specified (e.g., "React 19", "Next.js 15")
- Specific feature/API mentioned (e.g., "useEffect", "middleware", "relations")

### Step 2: Search for Library

**Use Task tool to call context7-fetcher sub-skill:**

```
Task parameters:
- subagent_type: Bash
- description: "Search Context7 for library"
- prompt: node .claude/skills/context7-auto-research/context7-api.js search "<library-name>" "<user-query>"
```

**Example:**

```
Task: Search for Next.js
Prompt: node .claude/skills/context7-auto-research/context7-api.js search "next.js" "How to configure middleware in Next.js 15"
```

**Response format:**

```json
{
  "libraries": [
    {
      "id": "/vercel/next.js",
      "name": "Next.js",
      "description": "The React Framework",
      "trustScore": 95,
      "versions": ["v15.1.8", "v14.2.0", "v13.5.0"]
    }
  ]
}
```

**Why use Task tool?**

- Uses `context: fork` from context7-fetcher sub-skill
- Avoids carrying conversation history to API calls
- Reduces Token consumption

### Step 3: Select Best Match

From search results, choose the library based on:

1. **Exact name match** to user's query
2. **Highest trust score** (indicates quality/popularity)
3. **Version match** if user specified (e.g., "Next.js 15" → prefer v15.x)
4. **Official packages** over community forks

### Step 4: Fetch Documentation

**Use Task tool to call context7-fetcher sub-skill:**

```
Task parameters:
- subagent_type: Bash
- description: "Fetch documentation from Context7"
- prompt: node .claude/skills/context7-auto-research/context7-api.js context "<library-id>" "<specific-query>"
```

**Example:**

```
Task: Fetch Next.js middleware docs
Prompt: node .claude/skills/context7-auto-research/context7-api.js context "/vercel/next.js" "middleware configuration"
```

**Response format:**

```json
{
  "results": [
    {
      "title": "Middleware",
      "content": "Middleware allows you to run code before a request is completed...",
      "source": "docs/app/building-your-application/routing/middleware.md",
      "relevance": 0.95
    }
  ]
}
```

**Why use Task tool?**

- Independent context for API calls
- No conversation history overhead
- Faster execution

### Step 5: Integrate into Response

Use the fetched documentation to:

1. **Answer accurately** with current information
2. **Include code examples** from the docs
3. **Cite version** when relevant
4. **Provide context** about the feature/API

## Helper Script Usage

The `context7-api.js` script provides two commands:

### Search Library

```bash
node context7-api.js search <libraryName> <query>
```

- Returns matching libraries with metadata
- Use for initial library resolution

### Get Context

```bash
node context7-api.js context <libraryId> <query>
```

- Returns relevant documentation snippets
- Use after selecting a library

### Environment Setup

The script supports two ways to configure the API key:

#### Option 1: .env File (Recommended)

Create a `.env` file in the skill directory:

```bash
# In .claude/skills/context7-auto-research/.env
CONTEXT7_API_KEY=your_api_key_here
```

You can copy from the example:

```bash
cp .env.example .env
# Then edit .env with your actual API key
```

#### Option 2: Environment Variable

```bash
export CONTEXT7_API_KEY="your-api-key"
```

**Priority:** Environment variable > .env file

**Get API Key:** Visit [context7.com/dashboard](https://context7.com/dashboard) to register and obtain your API key.

If not set, the API will use public rate limits (lower quota).

## Best Practices

### Query Specificity

- Pass the **full user question** as the query parameter for better relevance
- Include specific feature names (e.g., "useEffect cleanup" vs just "useEffect")

### Version Awareness

- When users mention versions, use version-specific library IDs
- Example: `/vercel/next.js/v15.1.8` instead of `/vercel/next.js`

### Error Handling

- If library search returns no results, inform user and suggest alternatives
- If API fails, fall back to training data but mention it may be outdated
- Handle rate limits gracefully (429 errors)

### Response Quality

- Don't dump entire documentation - extract relevant parts
- Combine multiple doc snippets if needed for complete answer
- Always include practical code examples

## Example Workflows

### Example 1: React Hook Question

**User:** "How do I use useEffect to fetch data in React 19?"

**Skill Actions:**

1. Detect trigger: "How do I use" + "useEffect" + "React 19"
2. Search: `node context7-api.js search "react" "useEffect fetch data"`
3. Select: `/facebook/react/v19.0.0` (version match)
4. Fetch: `node context7-api.js context "/facebook/react/v19.0.0" "useEffect data fetching"`
5. Respond with current React 19 patterns (e.g., using `use()` hook if applicable)

### Example 2: Next.js Configuration

**User:** "配置 Next.js 15 的中间件"

**Skill Actions:**

1. Detect trigger: "配置" + "Next.js 15" + "中间件"
2. Search: `node context7-api.js search "next.js" "middleware configuration"`
3. Select: `/vercel/next.js/v15.1.8`
4. Fetch: `node context7-api.js context "/vercel/next.js/v15.1.8" "middleware"`
5. Respond with Next.js 15 middleware setup

### Example 3: Prisma Relations

**User:** "Show me how to define one-to-many relations in Prisma"

**Skill Actions:**

1. Detect trigger: "Show me how" + "Prisma"
2. Search: `node context7-api.js search "prisma" "one-to-many relations"`
3. Select: `/prisma/prisma` (highest trust score)
4. Fetch: `node context7-api.js context "/prisma/prisma" "one-to-many relations"`
5. Respond with Prisma schema examples

## Architecture: Context Separation

### Why Split into Two Skills?

This skill adopts a **two-phase architecture**:

1. **Main Skill (context7-auto-research)** - Needs conversation context:

   - Detect trigger keywords in user message
   - Extract user query intent
   - Select best matching library (version, name, trust score)
   - Integrate documentation into response

2. **Sub-Skill (context7-fetcher)** - Independent context (`context: fork`):
   - Execute API calls to Context7
   - Pure HTTP requests, no conversation history needed
   - Reduce Token consumption

### Benefits

| Aspect      | Main Skill        | Sub-Skill          |
| ----------- | ----------------- | ------------------ |
| Context     | Full conversation | Fork (independent) |
| Purpose     | Intent analysis   | API execution      |
| Token usage | Higher            | Lower              |
| Execution   | Sequential        | Can be parallel    |

### Call Flow

```
User Query → Main Skill (detect + analyze)
                ↓
           Task Tool → Sub-Skill (API search)
                ↓
           Main Skill (select best match)
                ↓
           Task Tool → Sub-Skill (API fetch docs)
                ↓
           Main Skill (integrate + respond)
```

## Integration with Existing Skills

This skill **complements** the existing `documentation-lookup` skill:

- **auto-research**: Proactive, automatic activation
- **documentation-lookup**: Manual, user-invoked via `/context7:docs`

Both can coexist - use auto-research for seamless UX, documentation-lookup for explicit queries.

## Performance Considerations

- **Cache responses**: Documentation changes infrequently
- **Parallel requests**: If user asks about multiple libraries, fetch in parallel using multiple Task calls
- **Timeout handling**: Set reasonable timeouts (5-10s) for API calls
- **Fallback strategy**: If API unavailable, use training data with disclaimer
- **Context efficiency**: Sub-skill uses fork context to minimize Token consumption

## Limitations

- Requires internet connection for API access
- Subject to Context7 API rate limits
- May not have documentation for very new or obscure libraries
- Documentation quality depends on source repository structure
