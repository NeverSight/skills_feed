---
name: research
description: Multi-LLM parallel research with query decomposition and synthesis
triggers:
  - "research"
  - "find out about"
  - "investigate"
  - "look into"
  - "what do you know about"
  - "deep dive"
  - "analyze"
  - "compare"
  - "find information"
  - "learn about"
allowed-tools: Read, Bash, WebSearch, WebFetch, Task
version: 0.1.0
---

# Research Skill

Discovery-driven, exhaustive research using parallel LLM agents for comprehensive, current information gathering.

## Core Principles

**CRITICAL:** These principles define how research works.

### 1. Discovery-Driven, Not List-Driven
- Find the BEST sources, not just known sources
- Don't limit to predefined source lists
- The internet is huge - explore it
- Value is in finding what user doesn't already know

### 2. Context-Aware
- Load user's domain context from preferences
- Research is RELEVANT to their specific situation
- But context doesn't limit WHERE you search

### 3. Exhaustive
- No time limits - can take 30 minutes to 3 hours
- Don't stop at first page of results
- Keep going until topic is exhausted
- Follow promising links deeper

### 4. Multimedia
- Not just text articles
- Videos (YouTube), TikTok, podcasts
- Real user experiences from forums

### 5. Highly Cited
- Every claim must have a citation
- Multiple sources for important claims
- Note when sources conflict

### 6. Clarifying Questions First
Before diving into research, ask deep, thought-provoking questions to understand:
- What's the actual goal? (not just the surface request)
- What constraints exist? (budget, time, preferences)
- What would success look like?
- What have they already tried or considered?
- Are there hidden requirements?

Example: "Research Japan ski trip" should prompt:
- "What skill level are you and Carrie? Blue runs, black diamonds?"
- "Is après-ski culture important, or pure skiing focus?"
- "Do you need English-friendly areas, or comfortable with Japanese-only?"
- "Any specific dates that are fixed vs flexible?"
- "Besides skiing, anything else you want to do (onsen, food tours)?"

## Domain Context Loading

Research automatically loads relevant context from preferences based on detected domain.

### How It Works
1. Detect domain from query (travel, shopping, work, etc.)
2. Load `research_domains.[domain]` from preferences
3. Load referenced context keys
4. Fetch any dynamic data (point balances, etc.)
5. Apply domain-specific research patterns

### Available Domains
- **travel** - Loads loyalty programs, credit cards, ski passes, fetches point balances
- **work_education** - Loads PSD context, CoSN membership, K-12 patterns
- **shopping** - Price comparison, quality patterns
- **ai_coding** - Tech stack, GitHub/HN patterns
- **consulting** - Strategic recommendations patterns

### Dynamic Data Fetching
For travel research, use browser-control to fetch current:
- Marriott points balance
- Alaska miles balance
- Chase points balance
- Active transfer bonus promotions

## When to Activate

Use this skill when user needs:
- Current information (credit card perks, travel deals, policies)
- Multi-perspective analysis (comparing options)
- Deep investigation of complex topics
- Fact-checking or verification
- Market research or trend analysis

## Travel Research Requirements

**CRITICAL:** Travel research MUST include user-generated content:

### Required Sections for Travel
1. **User Reviews** - TripAdvisor, FlyerTalk, Reddit feedback
2. **"What I Wish I Knew"** - Common mistakes and gotchas
3. **Real Experiences** - Actual trip reports from similar travelers
4. **Restaurant/Hotel Reviews** - With prices and quality feedback
5. **Transportation Tips** - Real user experiences with logistics

### Sources to Search
- TripAdvisor reviews and forums
- FlyerTalk (for points/miles properties)
- Reddit (r/JapanTravel, r/skiing, r/churning, etc.)
- Ski forums and trip reports
- Points/miles blogs with personal reviews

### Browser Access for Deep Research

Use the **browser-control** skill to scrape full threads and reviews that require:
- JavaScript rendering (Reddit, modern forums)
- Authentication (FlyerTalk, logged-in content)
- Dynamic content loading

**Prerequisites:**
1. Brave must be running: `cd skills/browser-control && ./scripts/launch-chrome.sh`
2. User must be logged into relevant sites in the Brave Geoffrey profile

**Available Scripts** (in `skills/browser-control/scripts/`):

```bash
# Navigate and get page content
bun navigate.js "https://www.reddit.com/r/JapanTravel/comments/..."

# Extract specific content
bun extract.js "https://flyertalk.com/forum/thread" ".post-content" --all

# Search travel sites directly
bun search.js reddit "Hakuba ski resort tips"
bun search.js flyertalk "Marriott Bonvoy Japan redemption"

# Capture current page without navigating
bun capture.js /tmp/screenshot.png
```

**When to Use Browser Control:**
- Reddit threads (full comments, not just preview)
- FlyerTalk forum posts (complete thread content)
- Hotel/airline pages requiring login (availability, points pricing)
- Sites that block web scraping but allow browsers

### Research Tool Decision Tree

**Start with WebSearch/WebFetch** for:
- General facts and information
- Blog posts and news articles
- Static content that's publicly accessible
- Quick lookups

**Escalate to browser-control** when:
- WebFetch returns truncated/incomplete content (JS-rendered sites)
- Need authenticated access (user's Marriott/Alaska account)
- Need real-time prices or availability
- Forum threads show only previews
- Site blocks scraping but allows browsers

**Example Flow:**
1. User asks: "What do people say about Westin Rusutsu?"
2. Start with `WebSearch` for blog reviews
3. Find promising Reddit/FlyerTalk threads
4. Use `browser-control` to get full thread content
5. Synthesize findings with citations

## Citation Requirements

**CRITICAL:** All research output MUST include citations.

### Inline Citations
Every factual claim must link to its source:
- "The Westin Rusutsu costs 70,000 points peak ([Point Hacks](url))"
- "Shinkansen to Nagano takes 1.5 hours ([Corritrip](url))"

### Source Section
Every research report must end with a complete "Sources" section listing all URLs used.

### Why This Matters
- User needs to verify information
- Information changes frequently (credit card perks, prices)
- Establishes credibility
- Allows deeper exploration

### No Citation = Don't Include
If you can't cite a source for a claim, either:
1. Find a source
2. Mark it as "unverified"
3. Don't include it

## Architecture

### Query Decomposition
Break complex questions into 3-7 sub-queries covering different angles:
- Factual/definitional
- Comparative
- Current state
- Expert opinions
- User experiences
- Edge cases

### Parallel Agent Execution
Launch multiple researcher agents simultaneously:
- **Perplexity** - Best for current web information, citations
- **Gemini** - Good for multi-perspective synthesis
- **OpenAI** - Strong structured analysis
- **Claude** - Deep reasoning, nuanced analysis

### Result Synthesis
- Collect all findings
- Identify consensus vs conflicts
- Score confidence per finding
- Cite sources
- Provide actionable recommendations

## Available Agents

Agents are in `./agents/` directory:

| Agent | Best For | API Required |
|-------|----------|--------------|
| `perplexity-researcher.md` | Current web info, citations | PERPLEXITY_API_KEY |
| `gemini-researcher.md` | Multi-angle comparison | GEMINI_API_KEY |
| `openai-researcher.md` | Structured analysis | OPENAI_API_KEY |
| `claude-researcher.md` | Deep reasoning | Native (Claude Code) |

## Usage

### Basic Research
```
User: "Research the best ways to maximize Alaska Airlines miles for Japan flights"

Geoffrey:
1. Decomposes into sub-queries:
   - Current Alaska redemption rates to Japan
   - Partner airline options (JAL, etc.)
   - Sweet spots and award availability patterns
   - Credit card earning strategies
   - Recent devaluations or changes

2. Launches 4 agents in parallel

3. Synthesizes findings with confidence scores
```

### Workflow Command
Use `/conduct-research [topic]` to trigger full parallel research workflow.

## Output Format

```markdown
## Research: [Topic]

### Context Applied
- Domain: [travel/shopping/work/etc]
- User context loaded: [what was loaded from preferences]
- Dynamic data fetched: [current point balances, etc]

### Executive Summary
[2-3 paragraph overview of key findings and main recommendation]

### Detailed Findings

#### Sub-topic 1
Information with citations throughout. For example, "The Westin Rusutsu
costs 70,000 points peak" ([Point Hacks](url)) and "offers ski-in/ski-out
access" ([Marriott](url)).

#### Sub-topic 2
More information with inline citations...

### Multimedia Resources
- [Video: Title](url) - brief description
- [Podcast: Episode](url) - brief description
- [TikTok: @user](url) - brief description

### What I Discovered You Might Not Know
- Surprising finding 1 that user likely didn't know
- Surprising finding 2
- New source or perspective discovered

### Recommendations
1. Actionable recommendation specific to user's context
2. Another action based on their situation

### Confidence Assessment
- High confidence: [topics with multiple agreeing sources]
- Needs verification: [topics with limited sources]
- Conflicting information: [where sources disagree]

### All Sources
Complete list of every URL referenced:
- [Source Name 1](full-url)
- [Source Name 2](full-url)
- [Source Name 3](full-url)
```

**Note:** Every factual claim needs an inline citation. The "All Sources" section at the end provides a consolidated reference list.

## Saving Research Reports

**ALWAYS save research reports to Google Docs** after completing research.

### Default Behavior
1. Create Google Doc in Geoffrey/Research folder
2. Use appropriate account (hrg for personal, psd for work)
3. Apply markdown formatting (headers, bold, links)
4. Return link to user

### How to Save
```bash
cd skills/google-workspace
bun docs/create_doc.js <account> --title "<Research Topic>" --folder Research --content "<markdown>"
```

### Account Selection
- **hrg** - Personal travel, consulting
- **psd** - Work-related research
- **kh** - Personal projects

### Future: Obsidian Integration
Will also save to local Obsidian vault (when skill is built).

## API Configuration

Keys stored in: `~/Library/Mobile Documents/com~apple~CloudDocs/Geoffrey/secrets/.env`

```bash
PERPLEXITY_API_KEY=pplx-...
GEMINI_API_KEY=...
OPENAI_API_KEY=sk-...
# Note: Claude runs natively in Claude Code, no API key needed
```

## Performance

- **Time**: 30 minutes to 3 hours for exhaustive research (not 15-45 seconds)
- **Depth**: Exhaustive - multiple search pages, follow links, multimedia
- **Sources**: Discover new sources, not just known lists
- **Accuracy**: Cross-referenced with confidence scoring, all claims cited

## Limitations

- API rate limits may throttle parallel requests
- Costs accrue per API call
- Not all agents may have access to same sources
- Real-time data (stock prices, availability) needs direct API access

## Future Enhancements

- Caching frequent research topics
- Learning which agents are best for which domains
- Automatic source credibility scoring
- Research history and versioning
