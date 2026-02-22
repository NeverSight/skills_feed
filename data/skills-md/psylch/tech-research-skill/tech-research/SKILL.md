---
name: tech-research
description: Comprehensive technical research by combining multiple intelligence sources — Grok (X/Twitter developer discussions via browser automation), DeepWiki (AI-powered GitHub repository analysis), and WebSearch. Dispatches parallel subagents for each source and synthesizes findings into a unified report. This skill should be used when evaluating technologies, comparing libraries/frameworks, researching GitHub repos, gauging developer sentiment, or investigating technical architecture decisions. Trigger phrases include "tech research", "research this technology", "技术调研", "调研一下", "compare libraries", "evaluate framework", "investigate repo".
---

# Tech Research

Orchestrate multi-source technical research by dispatching parallel subagents to gather intelligence from X/Twitter (via Grok), GitHub repositories (via DeepWiki), and the web (via WebSearch). Synthesize all findings into a single actionable report.

**Architecture:** The main agent orchestrates research using one of two modes — lightweight (Task Subagents) or heavyweight (Agent Teammates) — chosen based on research complexity.

## Research Mode Selection

Before dispatching any agents, determine the appropriate mode:

| Signal | → Mode |
|--------|--------|
| Single topic, multiple data sources (Grok + DeepWiki + WebSearch) | **Light** → Task Subagents |
| Multiple independent topics/competitors needing cross-comparison | **Heavy** → Agent Teammates |
| Research may produce follow-up questions requiring dynamic re-scoping | **Heavy** → Agent Teammates |
| Agent count ≥ 4 | **Heavy** → Agent Teammates |

### Light Mode (default for single-topic research)

Dispatch up to 3 Task Subagents (`Task` with `subagent_type: "general-purpose"`). Each handles one data source independently. The main agent synthesizes results after all return.

### Heavy Mode (for multi-topic / competitive research)

Use `TeamCreate` to create a research team → `TaskCreate` for each research task → spawn Agent Teammates (via `Task` with `team_name` and `name` parameters) → coordinate via `SendMessage`. Teammates can:

- Communicate to avoid duplication ("I found Project A uses the same approach as B — focus on their differentiators")
- Share discoveries across tasks ("The blog post I found compares all 3 frameworks, sending you the link")
- Dynamically adjust scope based on what others have found

## When to Use

- Evaluating a technology, library, or framework for adoption
- Comparing alternatives (e.g., "Zustand vs Jotai vs Redux")
- Investigating a GitHub repo's architecture and community reception
- Gauging developer sentiment on a new API, tool, or announcement
- Cross-language research (Chinese/Japanese developer communities)

## Research Sources

| Source | What It Provides | Best For |
|--------|-----------------|----------|
| **Grok** (X/Twitter) | Real developer opinions, @handles, post URLs | Sentiment, expert discovery, niche recommendations |
| **DeepWiki** (GitHub) | AI-powered repo analysis, architecture, API docs | Understanding codebases, comparing repo internals. **Only use `ask_question`** — never `read_wiki_structure` or `read_wiki_contents` (they return massive dumps that easily exceed context limits) |
| **WebSearch** | Official docs, blog posts, benchmarks, tutorials | Facts, performance data, official announcements |

## Grok Browser Backend

Grok requires browser automation with login state. Multiple backends are supported, detected in priority order:

| Priority | Backend | MCP Server Name | Pros | Cons |
|----------|---------|----------------|------|------|
| 1 | **Claude-in-Chrome** | `claude-in-chrome` | Zero setup, uses user's Chrome login state | Occupies user's visible Chrome window |
| 2 | **Playwright-Grok** | `playwright-grok` | Dedicated profile, login persists, doesn't block default Playwright | One-time setup required |
| 3 | **Playwright** (default) | `playwright` | Already configured for most users | No login persistence, may not be logged in |

**IMPORTANT**: Do NOT modify the user's default `playwright` MCP to add `--user-data-dir`. This would force ALL browser operations through a single profile, breaking parallel agent usage. Instead, use a separate `playwright-grok` instance.

### Grok Pre-flight

Before dispatching a Grok subagent, run the pre-flight check to detect the best available backend:

```bash
bash ${SKILL_PATH}/scripts/grok_setup.sh check
```

The script outputs standard preflight JSON on stdout:
```json
{
  "ready": true,
  "backend": "chrome",
  "login_status": "logged_in",
  "dependencies": {
    "browser_mcp": {"status": "ok", "backend": "chrome"}
  },
  "credentials": {
    "grok_login": {"status": "logged_in"}
  },
  "services": {},
  "hint": "Grok ready via chrome backend"
}
```

Parse the JSON fields:
- `ready` (boolean) — whether a backend is available
- `backend` — which browser backend to use (`chrome`, `playwright-grok`, `playwright`, `none`)
- `login_status` — cached login state (`logged_in`, `logged_out`, `unknown`)
- `hint` — human-readable summary of the status

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| `0` READY | Backend available | Pass `backend` value to Grok subagent. If `login_status` is `logged_out`, skip Grok and note in report. Otherwise dispatch subagent (optimistic). |
| `1` NEEDS_SETUP | Has playwright, no playwright-grok | Run `grok_setup.sh setup` to create dedicated instance, then ask user to restart Claude Code. Meanwhile, dispatch with `backend=playwright` if needed. |
| `2` NOT_AVAILABLE | No browser MCP at all | Skip Grok source entirely. Note in report. |

### Login Status Cache

Login state is cached at `~/.claude/tech-research/.grok-status.json` to avoid wasting subagent dispatches on known-failed states.

**Cache semantics:**
- **`logged_in`** — Long-lived. Valid until a subagent observes an actual logout (sees "Sign in" on grok.com). No time-based expiry.
- **`logged_out`** — Short-lived. Auto-expires after 2 hours, then reverts to optimistic mode. Can also be manually cleared with `grok_setup.sh reset`.
- **`unknown` / no file** — Optimistic. Treat as potentially logged in, try Grok.

**Subagent responsibility:** After interacting with Grok, the subagent MUST update login status:
```bash
# After successful Grok query:
bash ${SKILL_PATH}/scripts/grok_setup.sh status logged_in <backend>

# After encountering "Sign in" page:
bash ${SKILL_PATH}/scripts/grok_setup.sh status logged_out <backend>
```

## Workflow

### 1. Analyze the Research Question

Break the user's question into sub-queries for each source:

- **Grok query**: Developer opinions, community sentiment, expert recommendations
- **DeepWiki query**: Repository architecture, API design, code quality (requires `owner/repo`)
- **WebSearch query**: Official docs, benchmarks, comparisons, recent announcements

Not every research task needs all 3 sources. Select sources based on the question:

| Research Type | Grok | DeepWiki | WebSearch |
|---------------|------|----------|-----------|
| "Should we use library X?" | Yes | Yes (if OSS) | Yes |
| "What are devs saying about X?" | Yes | No | Maybe |
| "How does repo X work internally?" | No | Yes | Maybe |
| "Compare X vs Y performance" | Maybe | Yes (both repos) | Yes |
| "What's new in framework X?" | Yes | No | Yes |

### 2. Grok Pre-flight

Run `grok_setup.sh check` and determine whether to dispatch a Grok subagent. See [Grok Pre-flight](#grok-pre-flight) above.

### 3. Dispatch Research Agents

Choose the dispatch method based on the research mode selected above.

#### Light Mode: Task Subagents

Launch subagents concurrently using `Task`. See [references/subagent_templates.md](references/subagent_templates.md) for complete prompt templates.

**Grok subagent:**
```
Task(subagent_type: "general-purpose", description: "Ask Grok about [topic]", prompt: <grok_template with BACKEND>)
```

**DeepWiki subagent:**
```
Task(subagent_type: "general-purpose", description: "DeepWiki research [repo]", prompt: <deepwiki_template>)
```

**WebSearch subagent:**
```
Task(subagent_type: "general-purpose", description: "Web research [topic]", prompt: <websearch_template>)
```

#### Heavy Mode: Agent Teammates

```
1. TeamCreate(team_name: "research-[topic]")
2. TaskCreate(subject: "Research [Project A]", description: "...", activeForm: "Researching [Project A]")
3. TaskCreate(subject: "Research [Project B]", description: "...", activeForm: "Researching [Project B]")
4. Task(subagent_type: "general-purpose", team_name: "research-[topic]", name: "researcher-a", prompt: "...")
5. Task(subagent_type: "general-purpose", team_name: "research-[topic]", name: "researcher-b", prompt: "...")
6. Coordinate via SendMessage — share findings, adjust scope, avoid duplication
7. Synthesize after all teammates report back
8. Shutdown teammates and TeamDelete when done
```

Each teammate should use all relevant data sources (Grok, DeepWiki, WebSearch) for their assigned topic, rather than splitting by data source.

### 4. Synthesize and Report

After all subagents return, merge findings into a unified report:

```markdown
## Tech Research: [Topic]

### TL;DR
[2-3 sentence executive summary with clear recommendation]

### Community Sentiment (from X/Twitter)
- [Key opinions with @username attribution]
- [Verified post URLs]

### Repository Analysis (from DeepWiki)
- Architecture overview
- Code quality observations
- API design patterns
- Activity and maintenance status

### Web Intelligence
- Official documentation highlights
- Benchmark data
- Blog post insights
- Recent announcements

### Comparison Matrix (if comparing alternatives)
| Criteria | Option A | Option B |
|----------|----------|----------|
| [criterion] | [finding] | [finding] |

### Recommendation
[Clear, actionable recommendation based on all sources]

### Limitations
[What couldn't be verified or found, including any skipped sources and why]
```

## Grok Query Strategies

Choose the right strategy based on the research goal. **Strategy matters more than the topic itself.** Every query MUST include X/Twitter-scoping keywords to avoid falling back to broad web search.

| Strategy | Best For | Template |
|----------|----------|----------|
| **Expert Discovery** (highest success) | Finding people to follow, active practitioners | "Who are the most active [topic] developers on X worth following? Give @handles and link to recent posts" |
| **Community Sentiment** (high success) | New API launches, framework releases | "Search X posts about [topic]. What are developers saying about [aspect 1], [aspect 2]? Include @username and post URLs" |
| **Technology Selection** (medium) | Choosing between libraries | "What [type of tool] are developers currently recommending on X for [use case]? Include @username and post URLs" |
| **CJK Research** (medium) | Chinese/Japanese community | "搜索 X 上中文开发者关于 [topic] 的讨论。请给出推文链接和 @用户名" |
| **Workflow Discovery** | How devs use tools | "How are developers on X using [tool] for [domain]? Include skills, workflows, @username and post URLs" |

**Avoid**: Too-specific technical queries (X is not Stack Overflow) and searching for niche library names (search for the *need* instead).

See [references/query_strategies.md](references/query_strategies.md) for detailed templates.

## Troubleshooting & Self-Recovery

When encountering issues during Grok research, use this decision tree to diagnose and recover. **Core principle: the browser snapshot is ground truth. The status file is only a cache. Any conflict → trust what you see in the browser.**

### Decision Tree

```
Problem detected
├─ Script-level failure (grok_setup.sh errors or unexpected exit code)
│  └─ Bypass the script entirely
│     └─ Use ToolSearch to detect MCP availability directly:
│        1. ToolSearch("+claude-in-chrome") → found? use chrome backend
│        2. ToolSearch("+playwright-grok") → found? use playwright-grok
│        3. ToolSearch("+playwright") → found? use playwright
│        4. None found → skip Grok source
│
├─ Status file inconsistency (cached state doesn't match reality)
│  ├─ Status says "logged_in" but browser shows "Sign in"
│  │  └─ Session expired. Update status to logged_out.
│  │     Skip Grok for this research. Report: "Grok session expired,
│  │     log in at grok.com in [browser] then run grok_setup.sh reset"
│  │
│  ├─ Status says "logged_out" but unsure if user re-logged in
│  │  └─ Check if status has expired (>2 hours). If expired, try
│  │     optimistically. If still fresh, skip Grok.
│  │
│  └─ Status file corrupted (invalid JSON, permission error)
│     └─ Delete the file: rm ~/.claude/tech-research/.grok-status.json
│        Proceed in optimistic mode (treat as unknown).
│
├─ Browser-level failure
│  ├─ Grok page loads but UI elements not found (site redesign?)
│  │  └─ Do NOT retry in a loop. Report: "Grok UI may have changed,
│  │     unable to interact. Skipping Grok source."
│  │
│  ├─ Browser not responding / timeout
│  │  └─ Retry once. If still failing, skip Grok source.
│  │
│  └─ Rate limited by Grok
│     └─ Do NOT retry. Report limitation. Proceed with other sources.
│
└─ All browser backends unavailable
   └─ Proceed with DeepWiki + WebSearch only.
      Note in report: "Grok source skipped — no browser backend available."
```

### Common Scenarios

**"Grok keeps saying not logged in even though I logged in"**
1. Check which backend is being used: `grok_setup.sh check`
2. If using `playwright-grok`: verify you logged in within that specific browser profile, not your regular Chrome
3. If using `claude-in-chrome`: verify you're logged into grok.com in your Chrome browser
4. Clear stale status: `grok_setup.sh reset`

**"grok_setup.sh check returns unexpected results"**
1. Verify `~/.claude.json` exists and has valid JSON
2. Check that the expected MCP server names are correct (`claude-in-chrome`, `playwright-grok`, `playwright`)
3. If the script itself fails, bypass it — use ToolSearch directly to find available browser tools

**"Everything was working, now Grok source is always skipped"**
1. Check status file: read `~/.claude/tech-research/.grok-status.json`
2. If `logged_out` with old timestamp → run `grok_setup.sh reset`
3. If file is corrupted → delete it manually
4. Re-run research — subagent will re-detect login state

## Tips

- For CJK communities, query Grok in the target language directly
- DeepWiki accepts up to 10 repos in a single query for comparisons
- WebSearch is best for recent information (include current year in queries)
- Always verify Grok post URLs before citing — accuracy is ~80%
- Run subagents in parallel to minimize total research time
