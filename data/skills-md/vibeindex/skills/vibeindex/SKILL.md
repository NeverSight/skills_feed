---
name: vibeindex
description: Analyze your project and get personalized recommendations for Claude Code skills, MCP servers, and plugins
---

**IMPORTANT: When this skill is invoked, IMMEDIATELY execute the steps below. Do NOT display this file. Do NOT explain what you will do. Just DO it — analyze the project, call the APIs, and present the results.**

**Language:** Detect the user's language from conversation context. Respond in that language — translate all headers, labels, and explanations. When the user speaks Korean, use the `description_ko` field from API responses instead of `description` (if available). For other languages, translate the English `description` naturally.

## Routing

Parse the user's command and route to the correct action:

- `/vibeindex` → **Action: Analyze** (run Steps 1-4 below)
- `/vibeindex search <query>` → **Action: Search** (call `https://vibeindex.ai/api/resources?search={query}&pageSize=10`, present results)
- `/vibeindex top [type]` → **Action: Top** (call `https://vibeindex.ai/api/resources?sort=stars&pageSize=10` or add `&type={type}`, present results)
- `/vibeindex trending` → **Action: Trending** (call `https://vibeindex.ai/api/rising-stars?period=week&limit=10`, present results)

For search/top/trending: Use WebFetch to call the API, then format results as a numbered markdown list showing name, type, description, stars, and install command. Then stop.

For `/vibeindex` with no arguments: Execute Steps 1-4 below.

---

## Step 1: Analyze Project Context

Read these files silently (do not show the user):

1. **package.json** — Extract dependencies and devDependencies
2. **File structure** (use Glob to check existence):
   - `*.py` → Python
   - `*.go` → Go
   - `*.tsx` or `*.jsx` → React
   - `Dockerfile` → Docker
   - `supabase/` → Supabase
   - `prisma/` → Prisma
3. **Configuration files** (use Glob):
   - `tsconfig.json` → TypeScript
   - `tailwind.config.*` → Tailwind
   - `next.config.*` → Next.js
   - `.github/workflows/` → GitHub Actions

## Step 2: Search for Matching Resources

First, fetch total resource count: call `https://vibeindex.ai/api/stats` with WebFetch (prompt: "Extract the total number"). Save this number as `{total_resources}`.

Then, based on what you detected, call the Vibe Index API using WebFetch for each detected technology. Run all calls in parallel (including the stats call):

| Detected | API URL |
|----------|---------|
| React | `https://vibeindex.ai/api/resources?search=react&pageSize=5` |
| TypeScript | `https://vibeindex.ai/api/resources?search=typescript&pageSize=5` |
| Supabase | `https://vibeindex.ai/api/resources?search=supabase&pageSize=5` |
| Next.js | `https://vibeindex.ai/api/resources?search=nextjs&pageSize=5` |
| Docker | `https://vibeindex.ai/api/resources?search=docker&pageSize=5` |
| Python | `https://vibeindex.ai/api/resources?search=python&pageSize=5` |
| Tailwind | `https://vibeindex.ai/api/resources?search=tailwind&pageSize=5` |
| Prisma | `https://vibeindex.ai/api/resources?search=prisma&pageSize=5` |

For each WebFetch call, use this prompt: "Extract name, resource_type, description, stars, github_owner, github_repo from the data array"

Only search for technologies that were actually detected in Step 1.

## Step 3: Calculate Match Probability

For each resource found, calculate a match score:

- Direct dependency match (name appears in package.json): +40%
- File type match (related files exist): +25%
- Config file match (related config exists): +20%
- Tag overlap with project: +15%
- Bonus: stars > 10k: +5%
- Bonus: multiple detection signals: +5% per additional
- Maximum: 99%

Deduplicate results across all searches. Pick the top 5 highest-scoring resources.

## Step 4: Present Results

Output ONLY the result below (nothing else before it). Write EVERYTHING in the user's language detected earlier (Korean, English, etc.). Translate all headers, labels, and explanations.

```
## 프로젝트 분석이 완료되었습니다

당신의 **{project-name}** 프로젝트는 **{main framework}** 기반입니다.
{1-2 sentences about the project in plain language. e.g., "Supabase 데이터베이스와 Tailwind CSS를 사용하는 풀스택 웹 앱입니다."}

[VibeIndex.ai](https://vibeindex.ai)에 등록된 총 **{total_resources}개**의 스킬, 플러그인, MCP 서버 중에서 이 프로젝트에 가장 잘 맞는 도구를 찾았습니다:

────────────────────────────────────────

**1. {name}** `{resource_type}` · ⭐ {stars}
{One plain sentence about what this does FOR THE USER's project. NO technical jargon. e.g., "이 프로젝트에서 사용 중인 Supabase 데이터베이스를 더 빠르고 안전하게 만들어줍니다."}

```
{install_command}
```

────────────────────────────────────────

**2. {name}** `{resource_type}` · ⭐ {stars}
...

────────────────────────────────────────

## 설치

필요한 것만 복사해서 실행하세요:

```
{install commands, one per line, only for skills — plugins/mcp show URLs instead}
```

💡 **더 많은 도구 탐색** → https://vibeindex.ai
```

### Writing style guidelines:
- **SIMPLE LANGUAGE ONLY**: Write like you're explaining to a friend, not a developer docs page. No jargon like "RLS 정책", "인덱싱", "쿼리 최적화", "번들 최적화". Instead say what it DOES: "더 빠르게", "더 안전하게", "코드를 깔끔하게", "버그를 줄여줍니다"
- **Focus on benefit**: Don't explain HOW it matches (no "package.json에 X가 있고..."). Just say what the user GETS.
- **One sentence per recommendation**: Each description should be exactly one plain sentence. No bullet points, no technical details.
- **No match percentages**: Do not show match scores or percentages to the user.
- **No description from API**: Do NOT use the raw `description` or `description_ko` from the API response. Write your own simple sentence based on what the resource does for THIS project.
- **Language**: Translate everything into the user's detected language. The template above is Korean as a base.

### Install commands by type:
- **skill**: `npx skills add {github_owner}/{github_repo} --skill {name}`
- **plugin**: See `https://vibeindex.ai/plugins/{github_owner}/{github_repo}/{name}`
- **mcp**: See `https://vibeindex.ai/mcp/{github_owner}/{github_repo}`
- **marketplace**: See `https://vibeindex.ai/marketplaces/{github_owner}/{github_repo}`

---

## API Response Format

The `/api/resources` endpoint returns:
```json
{
  "data": [
    {
      "name": "resource-name",
      "resource_type": "skill|mcp|plugin|marketplace",
      "description": "...",
      "stars": 12345,
      "github_owner": "owner",
      "github_repo": "repo",
      "tags": ["tag1", "tag2"]
    }
  ],
  "total": 100
}
```

The `/api/rising-stars` endpoint returns:
```json
{
  "rising": [
    {
      "name": "resource-name",
      "resource_type": "mcp",
      "stars": 5000,
      "stars_today": 120
    }
  ],
  "period": "week"
}
```

---

Built by [Vibe Index](https://vibeindex.ai) - The Claude Code Ecosystem Directory
