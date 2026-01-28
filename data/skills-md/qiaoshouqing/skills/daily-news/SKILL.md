---
name: daily-news
description: "Generate daily design inspiration & novel things report. Use when user asks for 'design news', 'design daily', 'design inspiration', '设计日报', '设计灵感', 'デザインニュース', 'what's new in design', 'novel products', '新奇事物'. Aggregates from Dribbble, Awwwards, Product Hunt, Behance, design influencers on Twitter, and more."
version: "2.0.0"
metadata:
  author: qiaoshouqing
  inspired_by: erduo-skills
---

# Design Daily - Design Inspiration & Novel Things

Generate daily design inspiration reports by aggregating from top design platforms, award sites, and design influencers on Twitter/X.

## When to Use

- User asks for design news, design inspiration, or design trends
- User says "design daily", "design news", "设计日报", "设计灵感", "デザインニュース"
- User wants to see what's trending in design today
- User asks for novel/interesting new products or creative tools
- User says "新奇事物", "有什么好玩的", "what's new"

## Language Detection

**CRITICAL: Detect user's language and respond in the EXACT SAME language.**

The skill supports ALL languages. Simply detect what language the user is using and generate the entire report in that language.

**Rule: User's language = Output language. No exceptions.**

Examples:
- User speaks English → Report in English
- 用户说中文 → 报告用中文
- ユーザーが日本語 → レポートは日本語
- Usuario habla español → Informe en español
- ...and ANY other language

## Data Sources

See `sources.json` for full configuration.

### Tier 1 - Design Curations & Novel Products (WebFetch)
| Source | Content |
|--------|---------|
| Sidebar.io | Top 5 curated design links |
| Hacker News (Show HN) | Novel projects, creative tools, interesting side projects |
| Kickstarter (Design & Tech) | Top 5 trending creative/design crowdfunding projects |
| Dezeen | Latest 5 industrial/product design news |
| GitHub Trending | Top 5 trending design tools, creative coding, UI repos |

### Tier 2 - Design Platforms (Chrome MCP)
| Source | Content |
|--------|---------|
| Product Hunt | Top 5 new products (focus on design/creative tools) |
| Dribbble | Top 8 popular shots |
| Awwwards | Latest 5 awarded websites |
| Behance | Featured creative projects |
| Muzli | Top 5 design inspirations |

### Tier 3 - Design Influencers on Twitter (Chrome MCP, 31 accounts)

**Design Tools & Systems:**
| Account | Who |
|---------|-----|
| @figma | Figma official |
| @steveschoger | Refactoring UI, practical design tips |
| @adamwathan | Tailwind CSS creator |
| @brad_frost | Brad Frost, Atomic Design creator |
| @danmall | Dan Mall, design systems expert |

**Design Leadership:**
| Account | Who |
|---------|-----|
| @joulee | Julie Zhuo, former Facebook Design VP |
| @jnd1er | Don Norman, father of UX |
| @khoi | Khoi Vinh, Adobe Principal Designer |
| @ireneau | Irene Au, former Google Design Head |
| @peterme | Peter Merholz, Adaptive Path founder |
| @lukew | Luke Wroblewski, coined 'Mobile First', Google |
| @jmspool | Jared Spool, UIE founder |
| @andybudd | Andy Budd, Clearleft founder |
| @veen | Jeff Veen, Typekit & Adaptive Path founder |
| @scottbelsky | Scott Belsky, Behance founder, Adobe |
| @boagworld | Paul Boag, UX leader |

**Visual & Brand Design:**
| Account | Who |
|---------|-----|
| @jessicawalsh | Jessica Walsh, &Walsh founder |
| @DannPetty | Dann Petty, Design Director |
| @davidairey | David Airey, brand identity specialist |
| @timothygoodman | Timothy Goodman, illustrator & muralist |
| @frank_chimero | Frank Chimero, 'The Shape of Design' |
| @hemeon | Marc Hemeon, former YouTube design lead |
| @rogie | Rogie King, GitHub designer |

**Typography:**
| Account | Who |
|---------|-----|
| @ilovetypography | I Love Typography, fonts & book history |
| @Typographica | Typographica, typeface reviews |

**UX & Content:**
| Account | Who |
|---------|-----|
| @zeldman | Jeffrey Zeldman, A List Apart founder |
| @debikielman | Debbie Millman, Design Matters podcast |
| @karenmcgrane | Karen McGrane, content & UX expert |
| @jbrewer | Josh Brewer, 52 Weeks of UX |
| @destroytoday | Jonnie Hallman, designer-developer |
| @tobiasahlin | Tobias Ahlin, Minecraft design lead |

## Instructions for Agent

### Step 1: Detect Language

Analyze user's message to determine output language:
```
1. Identify what language the user wrote their message in
2. Use that EXACT language for ALL output
3. Translate/localize everything to match user's language
```

### Step 2: Collect Design News (Parallel where possible)

**Tier 1 - WebFetch (parallel):**

```
1. Sidebar.io:
   - URL: https://sidebar.io/
   - Extract: Today's 5 best design links with title, source, URL

2. Hacker News (Show HN focus):
   - URL: https://news.ycombinator.com/
   - Extract: Top 10 Show HN projects, creative tools, novel side projects
   - SKIP: Papers, research, enterprise software, pure backend stuff

3. Kickstarter (Design & Tech):
   - Method: WebSearch "Kickstarter design tech trending [month] [year]"
   - Note: Site has Cloudflare protection, WebFetch/Chrome MCP blocked
   - Extract: Top 5 trending design/tech projects with funding progress
   - Focus on: product design, creative tools, gadgets, art projects

4. Dezeen:
   - Method: WebSearch "Dezeen design news [month] [year]"
   - Note: Site has Cloudflare protection, WebFetch/Chrome MCP blocked
   - Extract: Latest 5 design news (industrial design, product design, furniture)

5. GitHub Trending:
   - URL: https://github.com/trending
   - Extract: Top 5 repos related to design tools, creative coding, generative art, or UI
   - SKIP: Backend frameworks, DevOps tools, ML models (unless design-related)
```

**Tier 2 - Chrome MCP (parallel):**

```
3. Product Hunt:
   - URL: https://www.producthunt.com/
   - Extract: Top 5 products, prioritize design tools and creative products

4. Dribbble:
   - URL: https://dribbble.com/shots/popular
   - Extract: Top 8 popular shots with title, designer, likes

5. Awwwards:
   - URL: https://www.awwwards.com/websites/
   - Extract: Latest 5 awarded sites with title, agency, score

6. Behance:
   - URL: https://www.behance.net/
   - Extract: Featured projects with title, creator, category

7. Muzli:
   - URL: https://muz.li/
   - Extract: Top 5 design inspiration items
```

**Tier 3 - Twitter (Chrome MCP, sample 5-8 accounts per run):**

```
8. Pick 5-8 design influencer accounts from sources.json tier3_twitter (31 total)
   - Rotate selection each day for variety
   - Navigate to each account
   - Extract latest 2-3 design-related tweets
   - Focus on design tips, tools, and visual content
   - Prioritize accounts with recent activity
```

### Step 3: Generate Report

Create a structured Markdown report in the detected language.

**Report Template (adapt language):**

```markdown
# Design Daily - [DATE]

> Design Inspiration & Novel Things

---

## Design Picks (Sidebar.io)
[Curated design links of the day]

## Show HN & Novel Projects
[Interesting new tools and creative projects]

## Kickstarter Highlights
[Trending creative crowdfunding projects]

## Dezeen Design News
[Industrial design, product design, architecture]

## GitHub Trending (Design & Creative)
[Open source design tools and creative coding projects]

## Product Hunt Highlights
[New products worth checking out]

## Dribbble Hot Shots
[Popular design work with designer credits]

## Awwwards Winners
[Award-winning web design]

## Behance Featured
[Creative projects and portfolios]

## Design Twitter
[Key insights and tips from design influencers]

---

## Collection Stats
| Source | Count | Status |
|--------|-------|--------|
| ... | ... | ... |

*Generated at: [TIMESTAMP]*
```

### Step 4: Save Report

Save the report to `NewsReport/[DATE]-design-daily.md` in the current workspace.

## Content Filtering Rules

**INCLUDE:**
- Visual design work (UI, UX, graphic design, illustration, typography)
- Design tools and plugins
- Creative coding and generative art
- Novel/fun products and side projects
- Web design trends and awards
- Design tips, tutorials, and workflows
- Brand design and identity

**EXCLUDE:**
- Academic papers and research
- AI/ML model releases (unless design-focused)
- Enterprise software
- Pure backend/infrastructure
- Finance, crypto, blockchain

## Error Handling

| Situation | Action |
|-----------|--------|
| WebFetch 403 | Try Chrome MCP for that source |
| Cloudflare CAPTCHA | Use WebSearch as fallback (Kickstarter, Dezeen) |
| Source timeout | Skip and note in stats |
| No content | Mark as failed in stats |
| Chrome MCP unavailable | Use WebFetch-only sources |
| Twitter login wall | Try scrolling, if blocked skip |

## Response Guidelines

1. Always confirm language detection at start
2. Show progress as sources are collected
3. Present final report in user's language
4. Include collection statistics
5. Save report to file and confirm path
6. Prioritize visual and inspiring content over text-heavy articles
7. **CRITICAL: Every item MUST include a clickable link to the original source.** No item should be listed without a URL. Use markdown link format: `[Title](URL)`
8. **Include images when available.** For Dribbble, use the CDN thumbnail URLs (`cdn.dribbble.com/userupload/...?resize=400x0`). For other visual platforms, extract image URLs from page data. Use markdown image format: `![alt](image_url)`
