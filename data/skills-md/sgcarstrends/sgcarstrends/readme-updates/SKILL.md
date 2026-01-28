---
name: readme-updates
description: Maintain README files with setup instructions, features, tech stack, and usage examples. Use when updating project documentation, adding new features, or improving onboarding.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# README Updates Skill

This skill helps you create and maintain high-quality README files across the monorepo.

## When to Use This Skill

- Creating README for new packages
- Updating project features
- Documenting setup instructions
- Adding usage examples
- Updating tech stack information
- Adding badges and shields
- Improving documentation clarity
- Onboarding new contributors

## README Structure

### Root README.md

```markdown
# SG Cars Trends

[![License](https://img.shields.io/github/license/sgcarstrends/sgcarstrends)](LICENSE)
[![CI](https://github.com/sgcarstrends/sgcarstrends/workflows/CI/badge.svg)](https://github.com/sgcarstrends/sgcarstrends/actions)
[![Coverage](https://codecov.io/gh/sgcarstrends/sgcarstrends/branch/main/graph/badge.svg)](https://codecov.io/gh/sgcarstrends/sgcarstrends)

> Platform for accessing Singapore vehicle registration and COE bidding data

## Features

- 📊 **Comprehensive Data**: Access car registration and COE bidding data
- 🔄 **Real-time Updates**: Automated daily data updates from LTA DataMall
- 📝 **AI-Generated Blog**: Automated insights using Google Gemini
- 🔗 **Social Media**: Auto-post updates to Discord, LinkedIn, Telegram, Twitter
- 📈 **Interactive Charts**: Visualize trends with Recharts
- 🚀 **Modern Stack**: Next.js 16, Hono, SST v3, PostgreSQL, Redis

## Quick Start

```bash
# Clone repository
git clone https://github.com/sgcarstrends/sgcarstrends.git
cd sgcarstrends

# Install dependencies
pnpm install

# Set up environment variables
cp .env.example .env

# Run database migrations
pnpm db:migrate

# Start development servers
pnpm dev
\```

## Documentation

- **[Contributing](CONTRIBUTING.md)** - Contribution guidelines

## Tech Stack

### Frontend
- **Next.js 16** - React framework with App Router
- **HeroUI** - React UI component library
- **Recharts** - Data visualization
- **Tailwind CSS** - Utility-first CSS

### Backend
- **Hono** - Fast web framework for Edge
- **Drizzle ORM** - TypeScript ORM
- **PostgreSQL** - Relational database
- **Upstash Redis** - Caching layer

### Infrastructure
- **SST v3** - Serverless framework
- **AWS Lambda** - Serverless compute
- **Cloudflare** - DNS and SSL
- **Vercel Blob** - File storage

### AI & Automation
- **Google Gemini** - AI blog generation
- **QStash** - Workflow engine
- **Better Auth** - Authentication

## Project Structure

```
sgcarstrends/
├── apps/
│   ├── api/          # Hono API service
│   ├── web/          # Next.js web app
│   └── admin/        # Admin panel
├── packages/
│   ├── database/     # Drizzle ORM schemas
│   ├── types/        # Shared TypeScript types
│   ├── ui/           # UI component library
│   ├── utils/        # Shared utilities
│   └── logos/        # Car logo management
└── infra/           # SST infrastructure
\```

## Development

```bash
# Start all development servers
pnpm dev

# Start specific service
pnpm -F @sgcarstrends/api dev
pnpm -F @sgcarstrends/web dev

# Run tests
pnpm test

# Build for production
pnpm build

# Lint and format
pnpm biome check --write .
\```

## Deployment

```bash
# Deploy to staging
pnpm deploy:staging

# Deploy to production
pnpm deploy:prod
\```

See deployment documentation for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE) © SG Cars Trends

## Support

- **Issues**: [GitHub Issues](https://github.com/sgcarstrends/sgcarstrends/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sgcarstrends/sgcarstrends/discussions)
```

### Package README Template

```markdown
# @sgcarstrends/database

Database schema and migrations for SG Cars Trends using Drizzle ORM.

## Installation

```bash
pnpm add @sgcarstrends/database
\```

## Usage

```typescript
import { db } from "@sgcarstrends/database";
import { cars } from "@sgcarstrends/database/schema";

// Query cars
const allCars = await db.query.cars.findMany();

// Insert car
await db.insert(cars).values({
  make: "Toyota",
  model: "Corolla",
  month: "2024-01",
  number: 150,
});
\```

## Schema

### Cars Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | `uuid` | Primary key |
| `make` | `text` | Car manufacturer |
| `model` | `text` | Car model |
| `month` | `text` | Registration month (YYYY-MM) |
| `number` | `integer` | Number of registrations |

## Migrations

```bash
# Generate migration
pnpm db:generate

# Run migrations
pnpm db:migrate

# Push schema (dev only)
pnpm db:push
\```

## Development

```bash
# Run tests
pnpm test

# Type check
pnpm tsc --noEmit
\```

## License

MIT
```

## README Components

### Badges

```markdown
<!-- License -->
[![License](https://img.shields.io/github/license/user/repo)](LICENSE)

<!-- CI Status -->
[![CI](https://github.com/user/repo/workflows/CI/badge.svg)](https://github.com/user/repo/actions)

<!-- Coverage -->
[![Coverage](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/user/repo)

<!-- npm version -->
[![npm](https://img.shields.io/npm/v/@sgcarstrends/database)](https://www.npmjs.com/package/@sgcarstrends/database)

<!-- Downloads -->
[![Downloads](https://img.shields.io/npm/dm/@sgcarstrends/database)](https://www.npmjs.com/package/@sgcarstrends/database)

<!-- TypeScript -->
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://www.typescriptlang.org/)
```

### Table of Contents

```markdown
## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
```

### Code Examples

```markdown
## Usage

### Basic Example

```typescript
import { db } from "@sgcarstrends/database";

const cars = await db.query.cars.findMany();
console.log(cars);
\```

### Advanced Example

```typescript
import { db } from "@sgcarstrends/database";
import { cars } from "@sgcarstrends/database/schema";
import { eq, desc } from "drizzle-orm";

// Get Toyota cars from January 2024
const toyotaCars = await db.query.cars.findMany({
  where: eq(cars.make, "Toyota"),
  orderBy: [desc(cars.number)],
  limit: 10,
});
\```
```

### Screenshots

```markdown
## Screenshots

### Homepage

![Homepage](docs/images/homepage.png)

### Dashboard

![Dashboard](docs/images/dashboard.png)
```

### Features List

```markdown
## Features

- ✅ **Feature 1**: Description of feature 1
- ✅ **Feature 2**: Description of feature 2
- 🚧 **Upcoming**: Description of planned feature
- ❌ **Not Supported**: Description of unsupported feature
```

## Best Practices

### 1. Clear Project Description

```markdown
# ❌ Unclear
This is a project for cars.

# ✅ Clear
> Platform for accessing Singapore vehicle registration and COE bidding data with AI-generated insights
```

### 2. Installation Instructions

```markdown
# ❌ Incomplete
Install dependencies

# ✅ Complete
## Installation

\```bash
# Clone repository
git clone https://github.com/sgcarstrends/sgcarstrends.git
cd sgcarstrends

# Install dependencies
pnpm install

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run migrations
pnpm db:migrate

# Start development server
pnpm dev
\```
```

### 3. Working Examples

```markdown
# ❌ Non-working example
\```typescript
import { db } from "database";
const data = await db.query();
\```

# ✅ Working example
\```typescript
import { db } from "@sgcarstrends/database";
import { cars } from "@sgcarstrends/database/schema";

const allCars = await db.query.cars.findMany();
console.log(`Found ${allCars.length} cars`);
\```
```

### 4. Links to Documentation

```markdown
# ❌ No documentation links
See docs for more info

# ✅ Linked documentation
For detailed documentation, see:
- [README](README.md) - Project overview
- [CLAUDE.md](CLAUDE.md) - Development guidelines
- [Contributing](CONTRIBUTING.md) - Contribution guidelines
```

## Maintaining README Files

### Update Checklist

- [ ] Update features list when new features added
- [ ] Update tech stack when dependencies change
- [ ] Update setup instructions when process changes
- [ ] Update badges (CI, coverage, version)
- [ ] Update screenshots for UI changes
- [ ] Update links (check for broken links)
- [ ] Update examples for API changes
- [ ] Add new sections as needed

### Check for Broken Links

```bash
# Install markdown-link-check
pnpm add -g markdown-link-check

# Check README for broken links
markdown-link-check README.md

# Check all README files
find . -name "README.md" -exec markdown-link-check {} \;
```

### Validate Markdown

```bash
# Install markdownlint
pnpm add -D markdownlint-cli

# Lint README
pnpm markdownlint README.md

# Fix issues automatically
pnpm markdownlint --fix README.md
```

## Template for New Packages

```markdown
# @sgcarstrends/[package-name]

> Brief description of what this package does

## Installation

\```bash
pnpm add @sgcarstrends/[package-name]
\```

## Usage

\```typescript
import { functionName } from "@sgcarstrends/[package-name]";

// Example usage
const result = functionName();
\```

## API

### `functionName(param: string): ReturnType`

Description of function.

**Parameters:**
- `param` (string): Description of parameter

**Returns:**
- `ReturnType`: Description of return value

**Example:**
\```typescript
const result = functionName("example");
\```

## Development

\```bash
# Run tests
pnpm test

# Build
pnpm build

# Type check
pnpm tsc --noEmit
\```

## License

MIT
```

## Common Sections

### Prerequisites

```markdown
## Prerequisites

Before you begin, ensure you have:

- **Node.js** 20 or later
- **pnpm** 8 or later
- **PostgreSQL** 14 or later
- **Redis** (via Upstash account)
```

### Environment Variables

```markdown
## Environment Variables

Create a `.env` file in the root directory:

\```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sgcarstrends

# Redis
UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token

# API Keys
LTA_API_KEY=your-lta-api-key
GEMINI_API_KEY=your-gemini-api-key
\```
```

### Troubleshooting

```markdown
## Troubleshooting

### Database Connection Error

**Issue:** Cannot connect to database

**Solution:**
1. Verify DATABASE_URL is correct
2. Ensure PostgreSQL is running
3. Check firewall settings

### Build Fails

**Issue:** Build fails with TypeScript errors

**Solution:**
\```bash
# Clear caches
rm -rf node_modules .turbo dist
pnpm install
pnpm build
\```
```

## Automation

### Update Version Badge

```bash
# Get current version
VERSION=$(node -p "require('./package.json').version")

# Update badge in README
sed -i "s/version-[0-9.]*-blue/version-$VERSION-blue/" README.md
```

### Generate Table of Contents

```bash
# Install markdown-toc
pnpm add -g markdown-toc

# Generate TOC
markdown-toc -i README.md
```

## References

- Awesome README: https://github.com/matiassingers/awesome-readme
- Shields.io: https://shields.io (for badges)
- markdown-link-check: https://github.com/tcort/markdown-link-check
- markdownlint: https://github.com/DavidAnson/markdownlint
- Related files:
  - `README.md` - Root README
  - `packages/*/README.md` - Package READMEs
  - Root CLAUDE.md - Documentation guidelines

## Best Practices Summary

1. **Clear Description**: Concise, clear project description at the top
2. **Quick Start**: Immediate value with quick start section
3. **Working Examples**: Provide copy-paste ready code examples
4. **Visual Aids**: Use screenshots, diagrams, and badges
5. **Complete Instructions**: Step-by-step setup and usage
6. **Link Documentation**: Link to comprehensive docs
7. **Keep Updated**: Regularly update when features change
8. **Check Links**: Regularly check for broken links
