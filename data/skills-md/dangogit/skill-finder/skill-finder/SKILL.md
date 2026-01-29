---
name: skill-finder
description: Find and install the best skill for your current task. Use when the user wants to discover skills, asks "is there a skill for...", "find a skill for...", or "/skill-finder". Searches skills.sh in real-time and uses LLM reasoning to match skills to the user's context.
license: Apache 2.0
---

# Skill Finder

The smartest way to discover and install skills from skills.sh.

## Trigger Phrases

- `/skill-finder`
- `/skill-finder [description]`
- "find a skill for..."
- "is there a skill for..."
- "what skill should I use for..."

## Process Overview

```
User Request
     │
     ▼
┌─────────────────────────┐
│ 0. Check Installed      │ ← Don't recommend what user already has
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ 1. Detect Agent         │ ← Auto-detect Claude Code, Cursor, etc.
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ 2. Parse Intent         │ ← Extract keywords, map to search terms
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ 3. Targeted Search      │ ← Search with specific keywords + categories
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ 4. Context Check        │ ← Only if needed for disambiguation
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ 5. Rank & Compare       │ ← Quality signals + comparison mode
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ 6. Recommend            │ ← Present with quality badges
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ 7. Install              │ ← Global or project, auto-detect agent
└─────────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ 8. Related Skills       │ ← Suggest complementary skills
└─────────────────────────┘
```

---

## Step 0: Check Already Installed Skills

**Before searching, check what's already installed:**

```bash
# Check common skill locations
ls -la .claude/skills/ 2>/dev/null
ls -la .cursor/rules/ 2>/dev/null
ls -la .agents/skills/ 2>/dev/null
ls -la ~/.claude/skills/ 2>/dev/null  # Global
```

**If the skill user needs is already installed:**
```markdown
You already have **{skill-name}** installed at `{path}`.

→ Want me to invoke it now, or find alternatives?
```

**If outdated version is installed:**
```markdown
You have **{skill-name}** installed, but there may be updates.

→ Want me to check for updates, or use the current version?
```

---

## Step 1: Detect Agent

**Auto-detect which AI agent the user is using:**

| Check For | Agent | Install Flag |
|-----------|-------|--------------|
| `.claude/` directory or `CLAUDE.md` | Claude Code | `-a claude-code` |
| `.cursor/` directory | Cursor | `-a cursor` |
| `.github/copilot/` directory | GitHub Copilot | `-a copilot` |
| `.cline/` directory | Cline | `-a cline` |
| `.codex/` directory | Codex | `-a codex` |
| `.continue/` directory | Continue | `-a continue` |

**Store detected agent for installation step.**

**If multiple detected or none detected:**
- Default to `claude-code` in Claude Code context
- Or ask user which agent they're using

---

## Step 2: Parse Intent & Extract Keywords

**From user request, extract:**
- Primary topic (e.g., "payments", "authentication", "testing")
- Specific technologies mentioned (e.g., "Stripe", "Supabase", "Playwright")
- Action type (e.g., "add", "build", "improve", "debug")

**Map to search keywords:**

| User Says | Search Keywords |
|-----------|-----------------|
| payments, billing, checkout | stripe, payment, billing, checkout, subscription |
| auth, login, sign in | auth, authentication, login, oauth, jwt, session, clerk, better-auth |
| tests, testing, TDD | test, testing, playwright, jest, vitest, e2e, tdd, qa |
| database, DB, data | postgres, supabase, prisma, mongodb, sql, database, migration |
| AI, LLM, RAG, embeddings | rag, llm, embedding, ai-sdk, mcp, vector, openai, anthropic |
| frontend, UI, React | react, nextjs, vue, svelte, frontend, tailwind, ui, component |
| backend, API, server | fastapi, express, nestjs, backend, api, server, node |
| DevOps, CI/CD, deploy | docker, k8s, kubernetes, github-actions, terraform, deploy, ci |
| email, notifications | email, resend, notification, messaging, smtp |
| docs, PDF, Excel | pdf, docx, xlsx, pptx, document, report |
| video, animation | remotion, video, animation, threejs, canvas, webgl |
| scraping, automation | browser, scrape, automation, crawl, puppeteer, playwright |
| marketing, SEO, growth | seo, marketing, cro, copywriting, analytics, conversion |
| mobile, React Native, iOS | react-native, ios, android, swiftui, mobile, flutter, expo |
| security | security, auth, encryption, vulnerability, audit, secrets |

---

## Step 3: Targeted Search

**IMPORTANT: Use the CLI search command first to get proper skill references:**

```bash
npx skills search {keyword} --limit 10
```

This returns skills in the correct format: `author/repo@skill-name`

**Understanding the format:**
- `author/repo@skill-name` - Full skill reference from search results
- `author/repo` - What you pass to `npx skills add` (installs all skills in that repo)

**For WebFetch fallback (if CLI unavailable):**

```
WebFetch: https://skills.sh/?search={primary_keyword}
Prompt: List matching skills with:
        - Full reference (author/repo@skill-name format)
        - Install count
        - Description
        Focus on skills matching: {specific_technologies_mentioned}
```

**If user request is vague (just "/skill-finder"):**
- Ask: "What are you trying to accomplish?"
- Wait for response before searching

---

## Step 4: Context Check (Only If Needed)

**Skip context gathering if:**
- User specified exact technology (e.g., "Stripe", "Playwright")
- Search returned one clear winner
- User request is unambiguous

**Gather context if:**
- Multiple similar skills found (need stack to disambiguate)
- User request is generic (e.g., "database best practices")
- Need to verify compatibility

**Quick context check:**

| File | What to Extract |
|------|-----------------|
| `package.json` | Framework (react, next, vue), key deps, has supabase/stripe/etc |
| `pyproject.toml` | Python framework (fastapi, django, flask) |
| `go.mod` | Go project confirmation |
| `Cargo.toml` | Rust project confirmation |
| `.env.example` | Integrated services (Stripe, Supabase, etc.) |

**Summarize as:** `Stack: {framework}, {language}, {key_dependencies}`

---

## Step 5: Rank with Quality Signals

**Quality indicators to factor into ranking:**

| Signal | How to Identify | Weight |
|--------|-----------------|--------|
| **Official/Verified** | Author is `stripe/`, `anthropics/`, `vercel/`, `supabase/`, `resend/` | High |
| **High Installs** | 1000+ installs | Medium |
| **Stack Match** | Skill matches user's detected tech stack | High |
| **Specific Match** | Skill name contains user's exact query | High |

**Official/Verified Authors (show ⭐ badge):**
- `stripe/` - Stripe official
- `anthropics/` - Anthropic official
- `vercel/` or `vercel-labs/` - Vercel official
- `supabase/` - Supabase official
- `resend/` - Resend official
- `remotion-dev/` - Remotion official
- `better-auth/` - Better Auth official
- `callstackincubator/` - Callstack (React Native experts)
- `cloudai-x/` - Three.js skills
- `trailofbits/` - Security experts

---

## Step 5b: Comparison Mode

**When multiple skills are similarly relevant, show comparison:**

```markdown
## Comparing {Category} Skills

| Feature | {skill-1} | {skill-2} | {skill-3} |
|---------|-----------|-----------|-----------|
| Installs | {count} | {count} | {count} |
| Official | ⭐ Yes | No | No |
| Your Stack | ✅ Match | ✅ Match | ❌ Different |
| Focus | {focus} | {focus} | {focus} |

**Recommendation:** {skill-name} ({reason})

→ Want details on any of these, or should I install the recommendation?
```

**Trigger comparison mode when:**
- Top 2-3 skills have similar relevance scores
- User asks "what's the difference between..."
- Skills serve same purpose but different approaches

---

## Safety Checks

**Before recommending any skill, verify:**

### 1. Author Verification
```markdown
✅ TRUSTED - Official/Verified authors (install without warning):
   stripe/, anthropics/, vercel/, vercel-labs/, supabase/, resend/,
   remotion-dev/, better-auth/, callstackincubator/, trailofbits/

⚠️ COMMUNITY - Other authors (show warning before install):
   "This skill is from a community author. Review before installing."
```

### 2. Typosquatting Check
Before recommending, verify skill name doesn't look like a typo of a popular skill:
- `stripe-best-pracitces` → suspicious (typo of `stripe-best-practices`)
- `react-best-prctices` → suspicious
- `supabase-postgers` → suspicious

**If suspicious:** Don't recommend, or warn user explicitly.

### 3. Install Confirmation
**Always show before installing:**
```markdown
**About to install:** {skill-name}
**Author:** {author}
**Source:** https://github.com/{author}/{repo}

⚠️ Installing skills runs code on your machine.
   Review the source if you don't trust the author.

→ Proceed with installation? (y/n)
```

### 4. Link to Source
Always provide GitHub link so user can review:
```markdown
📂 **View source:** https://github.com/{author}/{repo}/blob/main/skills/{skill}/SKILL.md
```

---

## Step 6: Present Recommendations

**Format with quality badges:**

```markdown
## Recommended Skills

Based on your {stack} project and goal to {userIntent}:

1. **{skill-name}** by {author} ({installs} installs) ⭐ Official
   {Why this matches - be specific about the fit}

2. **{skill-name}** ({installs} installs)
   {Why this is relevant, any trade-offs vs #1}

3. **{skill-name}** ({installs} installs)
   {When you'd choose this instead}

→ Want me to install any of these?
```

**Quality badges:**
- ⭐ = Official/Verified author
- 🔥 = Trending (high installs)
- ✅ = Perfect stack match

---

## Step 7: Installation

**CRITICAL: The CLI uses `author/repo` format, NOT `author/skill-name`!**

From search results like `jezweb/claude-skills@tanstack-query`:
- `jezweb/claude-skills` = the repo (use this for install)
- `tanstack-query` = specific skill name in that repo

**⚠️ IMPORTANT: Installing a repo installs ALL skills in it!**

Some repos contain many skills:
- `jezweb/claude-skills` has 90+ skills (probably too many)
- `vercel-labs/next-skills` has 3 skills (focused)

**Prefer focused repos** with fewer skills relevant to user's need.

**If a large repo is the only option:**
1. Warn the user: "This repo contains {N} skills. Install anyway?"
2. Suggest browsing: https://skills.sh/{author}/{repo} to see all skills
3. After install, suggest removing unneeded skills

**Ask about installation scope:**

```markdown
Install **{skill-name}** from `{author}/{repo}` to:
1. **This project** (./agents/skills/) - Recommended
2. **Globally** (all your projects)

→ Which do you prefer? (default: this project)

⚠️ Note: This will install {N} skills from this repo.
```

**Installation commands:**

```bash
# Project-level (default) - uses author/repo, NOT skill name
npx skills add {author}/{repo} -a {detected_agent} -y

# Global installation
npx skills add {author}/{repo} -a {detected_agent} -y -g
```

**After successful installation:**

```markdown
✓ Installed skills from **{author}/{repo}** to {install_path}

Agent: {detected_agent}
Scope: {project|global}
Skills installed: {list of skill names}
```

---

## Step 8: Suggest Related Skills

**After installing, suggest complementary skills:**

| Installed Skill | Related Skills to Suggest |
|-----------------|---------------------------|
| stripe-* | webhook-patterns, subscription-management, billing-automation |
| *-auth, authentication | session-management, secrets-management, security-* |
| supabase-* | row-level-security, database-migration, sql-optimization |
| playwright-*, testing | test-driven-development, e2e-testing-patterns, qa-test-planner |
| react-* | react-testing, react-performance, react-state-management |
| nextjs-* | vercel-deployment, nextjs-app-router-patterns |
| fastapi-* | async-python-patterns, python-testing-patterns |
| docker-* | k8s-*, deployment-pipeline-design |
| ai-sdk, rag-* | embedding-strategies, mcp-builder, llm-evaluation |
| remotion-* | video processing skills, animation skills |

**Format:**

```markdown
**You might also need:**
- **{related-skill-1}** - {why relevant to what they just installed}
- **{related-skill-2}** - {why relevant}

→ Want me to install any of these too?
```

---

## Step 9: Check for Updates (Optional)

**When user has skills installed, offer update check:**

```bash
npx skills check
```

**If updates available:**

```markdown
📦 **Updates Available**

| Skill | Current | Latest | Changes |
|-------|---------|--------|---------|
| stripe-integration | 1.0.0 | 1.2.0 | New webhook patterns |
| react-best-practices | 2.1.0 | 2.3.0 | React 19 support |

→ Want me to update these?
```

**Update command:**
```bash
npx skills update
```

---

## Error Handling

### No Matches Found

```markdown
I couldn't find skills that directly match "{user_request}".

**Suggestions:**
- Try different keywords (e.g., "auth" instead of "login system")
- Be more specific (e.g., "Supabase auth" instead of "auth")
- Browse skills.sh directly: https://skills.sh/

**Popular categories you might explore:**
- Authentication: `better-auth`, `clerk-auth`, `supabase-auth`
- Testing: `playwright-skill`, `webapp-testing`
- Payments: `stripe-best-practices`

What would you like to try?
```

### skills.sh Unreachable

```markdown
I'm having trouble reaching skills.sh right now.

**Options:**
1. Try again in a moment
2. Browse directly: https://skills.sh/
3. Tell me what you need and I'll help without a skill

What would you like to do?
```

### Installation Failed

```markdown
Installation failed: {error_message}

**Try manually:**
```bash
npx skills add {author}/{skill-name}
```

**Or browse the skill:** https://skills.sh/{author}/{skill-name}

**Common fixes:**
- Run `npm cache clean --force` and retry
- Check your internet connection
- Try installing globally with `-g` flag
```

### Skill Already Installed

```markdown
**{skill-name}** is already installed at `{path}`.

**Options:**
1. Invoke it now for your current task
2. Check for updates
3. Find alternative skills
4. Reinstall (overwrite)

What would you like to do?
```

---

## Examples

### Fast Path (Clear Intent)

```
User: /skill-finder Stripe payments

Agent: Let me search for Stripe skills...
       [Runs: npx skills search stripe --limit 10]

       ## Recommended Skills

       Based on your goal to add Stripe payments:

       1. **stripe-best-practices** from `stripe/ai-skills` (354 installs) ⭐ Official
          Official Stripe patterns - checkout, webhooks, subscriptions
          Repo contains 2 skills (focused)

       2. **stripe-integration** from `wshobson/agents` (349 installs)
          End-to-end integration patterns
          ⚠️ Repo contains 15 skills

       → Want me to install any of these?

User: Install #1

Agent: Install from `stripe/ai-skills` to:
       1. This project (./agents/skills/) - Recommended
       2. Globally (all your projects)

       This repo contains 2 skills - both Stripe-related.

User: 1

Agent: [Runs: npx skills add stripe/ai-skills -a claude-code -y]

       ✓ Installed 2 skills from **stripe/ai-skills** to .agents/skills/

       Skills installed:
       - stripe-best-practices
       - stripe-webhooks

       → Want me to apply these to your current task?
```

### With Comparison Mode

```
User: /skill-finder authentication

Agent: I found several auth skills. Here's a comparison:

       ## Comparing Authentication Skills

       | Feature | better-auth | clerk-auth | supabase-auth |
       |---------|-------------|------------|---------------|
       | Installs | 3,373 | 129 | 142 |
       | Official | ⭐ Yes | No | No |
       | Self-hosted | ✅ | ❌ Cloud | ✅ |
       | Social login | ✅ | ✅ | ✅ |
       | Your Stack | ✅ Next.js | ✅ Next.js | ⭐ You use Supabase |

       **Recommendation:** supabase-auth (best fit - you already use Supabase)

       → Want me to install supabase-auth, or details on another?
```

### Already Installed

```
User: /skill-finder React testing

Agent: You already have **webapp-testing** installed at `.claude/skills/webapp-testing/`.

       **Options:**
       1. Invoke it now for your React testing needs
       2. Find additional/alternative testing skills
       3. Check for updates

       What would you like to do?

User: 2

Agent: ## Additional Testing Skills

       Since you have webapp-testing, here are complementary skills:

       1. **react-testing** (412 installs)
          React-specific testing patterns (RTL, hooks testing)

       2. **test-driven-development** (1,289 installs) ⭐ Popular
          TDD methodology and workflow

       → Want me to install any of these?
```

### Update Check

```
User: /skill-finder --check-updates

Agent: 📦 **Checking your installed skills...**

       | Skill | Status |
       |-------|--------|
       | stripe-best-practices | ✅ Up to date |
       | webapp-testing | 🔄 Update available (1.2.0 → 1.3.0) |
       | react-best-practices | ✅ Up to date |

       → Want me to update webapp-testing?
```

---

## Performance Tips

1. **Be specific** — "Stripe checkout" finds better matches than "payments"
2. **Mention your stack** — "React Native auth" narrows results
3. **One topic at a time** — Split "auth and payments" into two searches
4. **Check installed first** — Avoid duplicates with `/skill-finder --installed`
5. **Use official skills** — Look for the ⭐ badge for verified quality
