---
name: vercel
description: Vercel Platform and API Documentation
---

# Vercel Skill

Comprehensive assistance with Vercel deployment, API integration, and platform features. This skill provides practical guidance for building and deploying modern web applications on Vercel's AI Cloud platform.

## When to Use This Skill

This skill should be triggered when:

- **Deployment & CI/CD**: Deploying applications, configuring continuous deployment, or setting up preview environments
- **API Integration**: Working with Vercel REST API endpoints for programmatic deployments and management
- **CLI Operations**: Using Vercel CLI commands for local development and deployment workflows
- **Configuration**: Setting up `vercel.json` for build commands, routing, environment variables, or cron jobs
- **Framework Setup**: Configuring Next.js, SvelteKit, Nuxt, or other supported frameworks
- **Serverless Functions**: Creating and deploying serverless functions or Edge runtime code
- **Domain Management**: Managing custom domains, SSL certificates, or DNS configuration
- **Environment Variables**: Setting up secrets and environment variables for different environments
- **Team Management**: Working with team resources, access tokens, or collaboration features
- **AI Integration**: Deploying AI-powered applications, agents, or MCP servers

## Quick Reference

### Authentication with Access Token

```bash
# Using cURL with Vercel API
curl -X GET "https://api.vercel.com/v9/projects" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

### Basic CLI Deployment

```bash
# Deploy to production
vercel --prod

# Deploy with environment variables
vercel --env NEXT_PUBLIC_API_URL=https://api.example.com

# Force new deployment without cache
vercel --force

# Deploy with build logs
vercel --logs
```

### CI/CD Deployment Workflow

```bash
# Pull environment variables and project settings
vercel pull --yes --environment=preview --token=$VERCEL_TOKEN

# Build locally
vercel build --token=$VERCEL_TOKEN

# Deploy pre-built artifacts
vercel deploy --prebuilt --token=$VERCEL_TOKEN
```

### vercel.json - Cron Jobs Configuration

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "crons": [
    {
      "path": "/api/every-minute",
      "schedule": "* * * * *"
    },
    {
      "path": "/api/every-hour",
      "schedule": "0 * * * *"
    },
    {
      "path": "/api/daily-cleanup",
      "schedule": "0 0 * * *"
    }
  ]
}
```

### vercel.json - Build Configuration

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "nextjs",
  "installCommand": "npm install"
}
```

### Environment Variables Configuration

```json
{
  "env": {
    "API_URL": "https://api.example.com",
    "FEATURE_FLAG": "true"
  },
  "build": {
    "env": {
      "BUILD_TIME": "@now"
    }
  }
}
```

### Accessing Team Resources via API

```bash
# Get team deployments
curl -X GET "https://api.vercel.com/v6/deployments?teamId=TEAM_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create deployment for team project
curl -X POST "https://api.vercel.com/v13/deployments?teamId=TEAM_ID" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-project", "files": []}'
```

### Bun Runtime Configuration

```json
{
  "bunVersion": "1.0.0",
  "functions": {
    "api/**/*.ts": {
      "runtime": "bun"
    }
  }
}
```

### Serverless Function Example

```javascript
// api/hello.js
export default function handler(req, res) {
  const { name = 'World' } = req.query;
  res.status(200).json({
    message: `Hello ${name}!`,
    timestamp: new Date().toISOString()
  });
}
```

### Edge Function Example

```javascript
// middleware.js
export const config = {
  matcher: '/api/:path*',
};

export default function middleware(req) {
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'my-value');
  return response;
}
```

## Key Concepts

### REST API Architecture

The Vercel REST API operates at `https://api.vercel.com` following REST principles. All requests require:
- **Authentication**: Bearer token in Authorization header
- **Content-Type**: `application/json` for all requests
- **HTTP Versions**: Supports HTTP/1, 1.1, and 2 (HTTP/2 preferred)
- **TLS**: Supports TLS 1.2 and 1.3 with resumption

### Rate Limiting

API responses include rate limit headers:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests left in current window
- `X-RateLimit-Reset`: Reset time (UTC epoch seconds)

Exceeding limits returns HTTP 429 with "too_many_requests" error.

### Pagination

- Default: 20 items per page
- Maximum: 100 items per page
- Navigate with `until` query parameter and `next`/`prev` timestamps

### Token Security

- Set expiration dates (1 day to 1 year)
- Store tokens securely immediately after creation
- Tokens display only once and cannot be retrieved later
- Use team-scoped tokens for team resource access

### Deployment Workflow

1. **Preview Deployments**: Automatic deployments for every git push to non-production branches
2. **Production Deployments**: Deployments to production domain from main branch or via `--prod` flag
3. **Build Artifacts**: Local builds with `vercel build` upload only compiled output
4. **Environment Variables**: Different values for development, preview, and production

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Vercel REST API endpoints, authentication, and integration patterns
- **llms-full.md** - Complete Vercel documentation for comprehensive reference
- **llms-small.md** - Condensed documentation for quick lookups

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners

Start with basic deployment workflows:
1. Install Vercel CLI: `npm i -g vercel`
2. Authenticate: `vercel login`
3. Deploy your first project: `vercel`
4. Learn about `vercel.json` configuration basics

### For Intermediate Users

Focus on:
- Custom build configurations in `vercel.json`
- Environment variable management across environments
- Setting up cron jobs for scheduled tasks
- Working with serverless functions
- Git integration and preview deployments

### For Advanced Users

Explore:
- Vercel REST API for programmatic deployments
- Custom CI/CD pipelines with `vercel build` and `vercel deploy --prebuilt`
- Edge runtime and middleware configurations
- Multi-tenant application patterns
- Team management and access control
- AI SDK integration and agent deployment

### Navigation Tips

- Use CLI commands for rapid iteration during development
- Use REST API for automation and custom workflows
- Reference `vercel.json` schema for configuration validation
- Check rate limits when building high-volume integrations
- Use team IDs for accessing shared resources

## Platform Capabilities

### Computing Infrastructure

- **Serverless Functions**: Node.js, Python, Go, Ruby, Bun, Wasm runtimes
- **Edge Runtime**: Low-latency edge computing
- **Fluid Compute**: Active CPU allocation for optimal performance
- **Streaming Support**: Real-time data streaming capabilities
- **Cron Jobs**: Scheduled function execution

### Development Features

- **Framework Support**: Next.js, SvelteKit, Nuxt, Astro, and 30+ more
- **Git Integration**: GitHub, GitLab, Bitbucket, Azure DevOps
- **Automatic CI/CD**: Preview environments for every push
- **Environment Variables**: Secure secrets management
- **Deployment Protection**: Password protection and access control

### AI Capabilities

- **AI SDK**: Language model integration framework
- **AI Gateway**: Multi-provider LLM routing
- **Agent Building**: Frameworks for AI agents
- **MCP Servers**: Model Context Protocol server deployment

### Performance & Optimization

- **CDN**: Global edge network
- **Image Optimization**: Automatic image processing
- **OG Image Generation**: Dynamic social media images
- **Caching**: Intelligent caching strategies

## Common Use Cases

1. **Marketing Sites**: Rapid deployment with preview environments
2. **E-commerce Platforms**: Composable commerce with serverless architecture
3. **SaaS Applications**: Multi-tenant applications with edge computing
4. **AI Applications**: AI-powered apps with intelligent infrastructure
5. **API Backends**: Hosting RESTful APIs and GraphQL servers
6. **Static Sites**: Optimized static site delivery
7. **Jamstack Applications**: Modern web architectures

## Resources

### Official Documentation
- **Main Docs**: https://vercel.com/docs
- **REST API**: https://vercel.com/docs/rest-api
- **CLI Reference**: https://vercel.com/docs/cli
- **Framework Guides**: https://vercel.com/docs/frameworks

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed API endpoint specifications
- Complete configuration options
- Framework-specific deployment guides
- Code examples with best practices
- Links to original documentation

### scripts/
Add helper scripts here for common automation tasks such as:
- Deployment automation scripts
- Environment variable management
- Team resource provisioning
- Batch operations on projects

### assets/
Add templates, boilerplate, or example projects here such as:
- `vercel.json` templates for different use cases
- Serverless function boilerplates
- Edge middleware examples
- CI/CD workflow templates

## Best Practices

1. **Security**
   - Always set expiration dates on access tokens
   - Use team-scoped tokens for shared resources
   - Store tokens in secure environment variables
   - Rotate tokens regularly

2. **Performance**
   - Use `--prebuilt` for faster deployments in CI/CD
   - Enable caching for build dependencies
   - Optimize images using Vercel's image optimization
   - Use Edge runtime for low-latency operations

3. **Configuration**
   - Version control your `vercel.json` configuration
   - Use environment-specific settings appropriately
   - Document custom build commands
   - Test configurations in preview environments first

4. **API Integration**
   - Implement retry logic for rate-limited requests
   - Handle pagination for large result sets
   - Monitor rate limit headers proactively
   - Use team IDs consistently for team resources

## Notes

- This skill provides guidance based on Vercel's latest documentation (as of January 2025)
- Reference files preserve structure and examples from official documentation
- Code examples include proper language detection for syntax highlighting
- Quick reference patterns are extracted from common usage scenarios

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with Vercel URLs
2. Update reference files with latest API changes
3. Verify code examples against current API versions
4. Test configurations with latest CLI version
