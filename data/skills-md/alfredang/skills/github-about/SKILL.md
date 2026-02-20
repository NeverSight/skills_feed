---
name: GitHub About
description: Auto-update GitHub repo description, live site URL, and topics. Analyzes your codebase to generate a compelling description, detects deployment URLs, and adds relevant topics. Use when setting up a repo, after deploying, or to polish your GitHub presence. Use when the user says "update github about", "update repo about", "set repo description", "add topics", "update about section", "github about", or any reference to updating a GitHub repository's about/description/topics/homepage.
---

# GitHub About

## Command
`/github-about` or `github-about`

## Navigate
Git & Repository

## Keywords
github about, repo description, github topics, live site url, homepage url, repo setup, github metadata, repo settings, github description, add topics, set homepage, repo about, github profile, project metadata, update about, update repo, update github, update description, set topics, repo about section, about section, update repo about, update github about

## Description
Automatically update your GitHub repository's About section — description, live site URL, and topics — by analyzing your codebase. No manual repo settings needed.

## Execution
This skill runs using **Claude Code with subscription plan**. Do NOT use pay-as-you-go API keys. All AI operations should be executed through the Claude Code CLI environment with an active subscription.

**IMPORTANT: Auto-trigger behavior**
This skill should be automatically invoked (without the user needing to type `/github-about`) whenever the user asks to:
- Update the GitHub about section
- Set or change the repo description
- Add topics to the repo
- Set the homepage/live site URL
- Update repo metadata
- "Polish" or "set up" their GitHub repo

When auto-triggered, run the full workflow silently and report results at the end.

## Environment Setup
Before running ANY `gh` commands, always source the token:
```bash
source ~/.zshrc 2>/dev/null
```
This loads `GH_TOKEN` which the `gh` CLI uses automatically for authentication. This MUST be done at the start of every execution.

## Response
I'll update your GitHub repo's About section!

The workflow includes:

| Step | Description |
|------|-------------|
| **Env Setup** | Source `~/.zshrc` to load `GH_TOKEN` |
| **Auth Check** | Verify `gh` CLI authentication via token |
| **Repo Info** | Extract owner/repo from git remote |
| **Description** | Generate and set a compelling repo description |
| **Live Site** | Detect and set the live site URL |
| **Topics** | Analyze tech stack and add relevant topics |

## Instructions

When executing `/github-about`, follow this workflow:

### Phase 1: Pre-flight

#### 1.1 Verify GitHub CLI
```bash
gh --version
```

If not installed, inform the user:
```
ERROR: GitHub CLI (gh) not found.
Install: https://cli.github.com/
```

#### 1.2 Authenticate with GH_TOKEN
The `GH_TOKEN` environment variable is already configured in `~/.zshrc`. The `gh` CLI automatically uses `GH_TOKEN` when present — no browser login needed.

**Authentication check order:**
1. Source the token and verify:
```bash
source ~/.zshrc 2>/dev/null
echo "GH_TOKEN is set: ${GH_TOKEN:+yes}"
```

2. Verify it works:
```bash
gh auth status
```

3. If `GH_TOKEN` is not set and `gh auth status` fails, fall back to browser login:
```bash
gh auth login --hostname github.com --git-protocol https --web
```

**Important:** Always run `source ~/.zshrc` before any `gh` commands to ensure `GH_TOKEN` is loaded into the current shell session. The `gh` CLI respects `GH_TOKEN` and `GITHUB_TOKEN` environment variables automatically — no extra configuration needed.

#### 1.3 Extract Owner/Repo
```bash
REMOTE_URL=$(git remote get-url origin)
OWNER=$(echo "$REMOTE_URL" | sed -E 's#.*(github\.com)[:/]([^/]+)/([^/.]+)(\.git)?$#\2#')
REPO=$(echo "$REMOTE_URL" | sed -E 's#.*(github\.com)[:/]([^/]+)/([^/.]+)(\.git)?$#\3#')
```

#### 1.4 Get Current Repo Metadata
```bash
gh repo view --json description,homepageUrl,repositoryTopics
```

Store the current values so we know what needs updating.

### Phase 2: Repository Description

#### 2.1 Check Current Description

If the description is already set, skip unless user explicitly asks to update it.

#### 2.2 Generate Description

Analyze the project to generate a short, compelling description (max 350 characters):

**Sources to analyze (in priority order):**
1. `README.md` — project title, first paragraph, features
2. `package.json` → `description` field
3. `pyproject.toml` → `[project] description`
4. `Cargo.toml` → `description`
5. `setup.py` or `setup.cfg` → description
6. Main source files — understand what the project does

**Description guidelines:**
- Start with a verb or noun (e.g., "A fast...", "Build...", "CLI tool for...")
- Be specific about what the project does
- Mention key technology if relevant
- Keep it under 350 characters
- No emojis in the description
- Don't start with "This is..." or "A repo for..."

#### 2.3 Set Description
```bash
gh repo edit --description "Your generated description"
```

### Phase 3: Live Site URL

#### 3.1 Check Current Homepage

If the homepage URL is already set, skip unless user explicitly asks to update it.

#### 3.2 Detect Live Site URL

Search for deployment URLs in this priority order:

1. **Vercel**: Check for Vercel deployment
   ```bash
   # Check if Vercel project exists
   cat .vercel/project.json 2>/dev/null
   # Or check vercel.json for project name
   cat vercel.json 2>/dev/null
   ```
   URL pattern: `https://<project-name>.vercel.app`

2. **GitHub Pages**: Check if Pages is enabled
   ```bash
   gh api "/repos/$OWNER/$REPO/pages" 2>/dev/null
   ```
   URL pattern: `https://<owner>.github.io/<repo>/`

3. **package.json**: Check `homepage` field
   ```bash
   node -e "console.log(require('./package.json').homepage || '')" 2>/dev/null
   ```

4. **README.md**: Scan for deployment URLs
   - Look for URLs containing: `.vercel.app`, `.netlify.app`, `.github.io`, `.herokuapp.com`, `.fly.dev`, `.railway.app`

5. **Custom domain**: Check CNAME file (GitHub Pages custom domain)
   ```bash
   cat CNAME 2>/dev/null
   ```

#### 3.3 Set Homepage URL
```bash
gh repo edit --homepage "https://detected-url.com"
```

### Phase 4: Repository Topics

#### 4.1 Check Current Topics

If topics are already set, **add to them** rather than replacing. Never remove existing topics.

#### 4.2 Detect Topics from Codebase

Analyze the project to determine relevant topics:

**Language detection:**
| File/Pattern | Topic |
|-------------|-------|
| `*.ts`, `*.tsx` | `typescript` |
| `*.js`, `*.jsx` | `javascript` |
| `*.py` | `python` |
| `*.rs` | `rust` |
| `*.go` | `go` |
| `*.java` | `java` |
| `*.swift` | `swift` |
| `*.rb` | `ruby` |

**Framework detection:**
| File/Pattern | Topic |
|-------------|-------|
| `next.config.*` | `nextjs`, `react` |
| `vite.config.*` | `vite` |
| `package.json` with `react` | `react` |
| `package.json` with `vue` | `vue` |
| `package.json` with `svelte` | `svelte` |
| `angular.json` | `angular` |
| `requirements.txt` with `django` | `django` |
| `requirements.txt` with `fastapi` | `fastapi` |
| `requirements.txt` with `flask` | `flask` |
| `Cargo.toml` | `rust` |
| `go.mod` | `golang` |
| `tailwind.config.*` | `tailwindcss` |
| `expo` in package.json | `expo`, `react-native` |

**Platform detection:**
| File/Pattern | Topic |
|-------------|-------|
| `.vercel/` or `vercel.json` | `vercel` |
| `Dockerfile` | `docker` |
| `fly.toml` | `fly-io` |
| `railway.json` | `railway` |
| `.github/workflows/` | `github-actions` |
| `supabase/` | `supabase` |

**Domain detection** (analyze README and source):
- AI/ML projects → `ai`, `machine-learning`, `llm`
- CLI tools → `cli`, `command-line`
- APIs → `api`, `rest-api`, `graphql`
- Web apps → `web-app`, `webapp`
- Games → `game`, `gamedev`
- DevTools → `developer-tools`, `devtools`

**Topic guidelines:**
- All lowercase
- Use hyphens for multi-word topics (e.g., `react-native`)
- Add 3-10 relevant topics
- Don't add generic topics like `code` or `project`
- Prefer specific topics over vague ones

#### 4.3 Add Topics
```bash
gh repo edit --add-topic "topic1" --add-topic "topic2" --add-topic "topic3"
```

**Important:** Use `--add-topic` (not `--topic`) to preserve existing topics.

### Phase 5: Report

Print a summary of all changes made:

```
=== GitHub About Updated ===

Repository: OWNER/REPO

Description: <the description that was set>
Homepage:    <the URL that was set>
Topics:      topic1, topic2, topic3, topic4

View: https://github.com/OWNER/REPO
```

If any step was skipped (already set), note it:
```
Description: Already set (skipped)
Homepage:    https://example.vercel.app (updated)
Topics:      react, nextjs, typescript (added 3 new)
```

## Capabilities

- Auto-detect and set repository description from codebase analysis
- Detect live site URLs from Vercel, GitHub Pages, Netlify, and more
- Analyze tech stack to generate relevant repository topics
- Preserve existing topics when adding new ones
- Authenticate via `GH_TOKEN` from `~/.zshrc` (no browser login needed)
- Falls back to browser-based `gh auth login` if token is unavailable
- Works with any project type (Node.js, Python, Rust, Go, etc.)

## Next Steps

After running `/github-about`:
1. Check your repo's About section on GitHub
2. Verify the description accurately represents your project
3. Click the homepage URL to confirm it works
4. Review topics and add/remove any manually if needed
