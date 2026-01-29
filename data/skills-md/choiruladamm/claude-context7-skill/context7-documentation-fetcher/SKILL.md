---
name: context7-documentation-fetcher
description: Automatically fetches up-to-date library documentation from Context7 when code generation, setup instructions, or API documentation is needed
---

# Context7 Documentation Fetcher

## Overview

This skill automatically fetches up-to-date, version-specific documentation from Context7 whenever you need:
- Code generation for specific libraries
- Setup or configuration steps
- Library/API documentation
- Framework-specific implementations

Claude will automatically invoke this skill when it detects you're asking about libraries, frameworks, or need accurate API documentation.

## When This Skill Is Used

Claude automatically uses this skill when:
- You ask for code examples using specific libraries (e.g., "Create a form with React Hook Form")
- You request setup instructions (e.g., "How to setup Next.js 15 app router?")
- You need API documentation (e.g., "Show me Supabase auth methods")
- You mention library names in your questions
- You ask "how to" questions about frameworks or libraries

## How It Works

1. **Detect Library**: Claude identifies which library/framework you need docs for
2. **Search Context7**: Queries Context7 API to find the exact library ID
3. **Fetch Docs**: Retrieves up-to-date documentation with relevant code examples
4. **Generate Code**: Uses fresh docs to provide accurate, non-hallucinated code

## Supported Libraries

This skill can fetch documentation for any library available in Context7, including:
- **Frontend**: React, Next.js, Vue, Nuxt, Svelte, Astro
- **State Management**: Zustand, Redux, TanStack Query, Jotai
- **Forms**: React Hook Form, Formik, Zod
- **Backend**: Express, Fastify, Hono, tRPC
- **Database**: Supabase, Prisma, Drizzle, MongoDB
- **UI Libraries**: Tailwind CSS, shadcn/ui, Radix UI, Mantine
- **And many more...**

## Examples

### Example 1: Form Validation
**User**: "Create a login form with React Hook Form and Zod validation"

**What happens**:
1. Skill searches Context7 for "react hook form" and "zod"
2. Fetches docs with topic="validation" and topic="integration"
3. Claude generates accurate code using current API methods

### Example 2: Next.js Setup
**User**: "Setup Next.js 15 with app router and server actions"

**What happens**:
1. Skill searches for "next.js"
2. Fetches docs with topic="app router" and topic="server actions"
3. Claude provides step-by-step setup with correct configuration

### Example 3: Database Integration
**User**: "How do I setup Supabase authentication?"

**What happens**:
1. Skill searches for "supabase"
2. Fetches docs with topic="authentication"
3. Claude shows current auth methods and code examples

## Technical Details

### API Integration
The skill uses Context7's REST API:
- **Search Endpoint**: `GET /api/v1/search?query={library_name}`
- **Docs Endpoint**: `GET /api/v1/{library_id}?topic={topic}&tokens={limit}`

### Configuration
- **API Key**: Pre-configured (secure)
- **Default Token Limit**: 5000 tokens per request
- **Response Format**: Plain text suitable for direct display
- **Rate Limits**: Follows Context7 free tier limits

### Error Handling
If a library is not found or docs are unavailable:
1. Claude will inform you the library isn't available in Context7
2. Claude will fall back to its training knowledge with appropriate caveats
3. Claude may suggest alternative libraries that are available

## Best Practices

1. **Be Specific**: Mention the exact library name for best results
   - Good: "Create form with React Hook Form"
   - Less good: "Create a form" (skill won't know which library to fetch)

2. **Include Version**: If you need a specific version, mention it
   - "Using Next.js 15..." (skill will attempt to fetch that version)

3. **Mention Topics**: Include relevant topics for focused docs
   - "Next.js server actions" → fetches server actions docs specifically
   - "Supabase realtime" → fetches realtime-specific documentation

## Limitations

- Only fetches from libraries available in Context7's database
- Limited to Context7's free tier rate limits (generous for daily use)
- Cannot access private/proprietary documentation
- Requires internet connection to fetch docs

## Resources

For more information about Context7:
- Website: https://context7.com
- GitHub: https://github.com/upstash/context7
- Add Libraries: https://context7.com/add-library
