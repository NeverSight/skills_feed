---
name: qiita
description: Qiita API integration for searching, reading, and publishing technical articles. Use this skill to search articles, get user posts, publish content, and manage comments on Qiita.
vm0_secrets:
  - QIITA_ACCESS_TOKEN
---

# Qiita API

Qiita is a technical knowledge sharing platform popular in Japan. This skill provides integration for searching articles, publishing content, and interacting with the community.

## When to Use

- Search technical articles on Qiita
- Get articles by tag or user
- Publish technical articles
- Read and post comments
- Get trending tags and topics

## Prerequisites

Set the following environment variable:

```bash
export QIITA_ACCESS_TOKEN=your_access_token
```

Get your access token from: https://qiita.com/settings/tokens/new

### Important: Environment Variables and Pipes

When using environment variables in commands with pipes, always wrap the command in `bash -c '...'` and keep the pipe outside. This ensures proper variable substitution:

```bash
# Good - wraps curl in bash -c, pipe is outside
bash -c 'curl -H "Authorization: Bearer ${QIITA_ACCESS_TOKEN}" https://api.qiita.com/api/v2/users'

# Bad - environment variable with pipe causes issues
curl -H "Authorization: Bearer ${QIITA_ACCESS_TOKEN}" https://api.qiita.com/api/v2/users
```

### Required Scopes

- `read_qiita` - Read articles, comments, users
- `write_qiita` - Post articles, comments

## How to Use

### Commands

The script supports 5 modules: `item`, `user`, `tag`, `comment`, `auth`

---

### 1. Item - Articles

#### Search Articles

```bash
scripts/qiita.sh item search --query "React hooks"
scripts/qiita.sh item search --query "tag:Python" --per-page 20
scripts/qiita.sh item search --query "user:username title:tutorial"
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --query | Yes | - | Search query (supports tag:, user:, title:, body:, stocks:) |
| --page | No | 1 | Page number |
| --per-page | No | 20 | Items per page (max 100) |

#### Get Article

```bash
scripts/qiita.sh item get --id "article_id"
```

#### Get My Articles

```bash
scripts/qiita.sh item mine --per-page 10
```

#### Post Article

```bash
scripts/qiita.sh item post --title "Article Title" --body "# Content" --tags "Python,Tutorial"
scripts/qiita.sh item post --title "Draft Post" --body-file ./article.md --tags "React" --private
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --title | Yes | - | Article title |
| --body | Yes* | - | Article body in Markdown |
| --body-file | Yes* | - | Read body from file (alternative to --body) |
| --tags | Yes | - | Comma-separated tags (max 5) |
| --private | No | false | Create as private article |

#### Update Article

```bash
scripts/qiita.sh item update --id "article_id" --title "New Title" --body "Updated content"
```

#### Delete Article

```bash
scripts/qiita.sh item delete --id "article_id"
```

---

### 2. User - User Information

#### Get Current User

```bash
scripts/qiita.sh user me
```

#### Get User Profile

```bash
scripts/qiita.sh user get --id "username"
```

#### Get User's Articles

```bash
scripts/qiita.sh user items --id "username" --per-page 10
```

#### Get User's Stocks

```bash
scripts/qiita.sh user stocks --id "username"
```

#### Get User's Followers/Following

```bash
scripts/qiita.sh user followers --id "username"
scripts/qiita.sh user following --id "username"
```

---

### 3. Tag - Tags

#### List Popular Tags

```bash
scripts/qiita.sh tag list --per-page 20
scripts/qiita.sh tag list --sort count
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --page | No | 1 | Page number |
| --per-page | No | 20 | Tags per page |
| --sort | No | count | Sort by: count or name |

#### Get Tag Info

```bash
scripts/qiita.sh tag get --id "Python"
```

#### Get Articles by Tag

```bash
scripts/qiita.sh tag items --id "JavaScript" --per-page 10
```

---

### 4. Comment - Comments

#### Get Article Comments

```bash
scripts/qiita.sh comment list --item-id "article_id"
```

#### Post Comment

```bash
scripts/qiita.sh comment post --item-id "article_id" --body "Great article!"
```

#### Delete Comment

```bash
scripts/qiita.sh comment delete --id "comment_id"
```

---

### 5. Auth - Authentication

#### Verify Token

```bash
scripts/qiita.sh auth verify
```

Returns current user info if token is valid.

---

## Search Query Syntax

Qiita search supports special operators:

| Operator | Example | Description |
|----------|---------|-------------|
| tag: | `tag:Python` | Filter by tag |
| user: | `user:qiita` | Filter by author |
| title: | `title:tutorial` | Search in title |
| body: | `body:example` | Search in body |
| stocks: | `stocks:>100` | Filter by stock count |
| created: | `created:>2024-01-01` | Filter by date |

Combine operators: `tag:React title:hooks stocks:>50`

## Examples

### Search and Read Articles

```bash
# Search for Python tutorials
scripts/qiita.sh item search --query "tag:Python title:tutorial" --per-page 5

# Get specific article
scripts/qiita.sh item get --id "abc123def456"
```

### Publish an Article

```bash
# Post from command line
scripts/qiita.sh item post --title "Getting Started with Docker" --body "# Introduction

Docker is a containerization platform..." --tags "Docker,DevOps,Tutorial"

# Post from file
scripts/qiita.sh item post --title "My Technical Article" --body-file ./my-article.md --tags "Programming"
```

### Explore Tags and Users

```bash
# Get trending tags
scripts/qiita.sh tag list --per-page 10 --sort count

# Get user's articles
scripts/qiita.sh user items --id "famous_author" --per-page 5
```

## Guidelines

1. **Rate Limits**: 1000 requests/hour (authenticated), 60/hour (unauthenticated)
2. **Tags**: Maximum 5 tags per article
3. **Markdown**: Article body supports GitHub-flavored Markdown
4. **Private Articles**: Use `--private` flag for drafts or private content
5. **Search**: Use operators for precise search results

## API Reference

- Documentation: https://qiita.com/api/v2/docs
- Access Tokens: https://qiita.com/settings/tokens/new
