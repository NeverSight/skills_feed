---
name: docs-to-skill
description: Convert online documentation into Claude Code skills with working scripts. Crawls docs, analyzes patterns, generates SKILL.md, reference files, and executable code examples.
---

# docs-to-skill

Convert any online documentation into a Claude Code skill with working scripts.

## Usage

```
/docs-to-skill <documentation-url>
```

Example:
```
/docs-to-skill https://docs.browserbase.com
```

## Workflow

When invoked, execute these phases in order:

### Phase 1: Discover ALL Documentation Pages

**IMPORTANT**: Get the COMPLETE list of pages before crawling. Many doc sites provide indexes.

#### Step 1: Check for Documentation Index Files

Try these URLs in order (use WebFetch). Stop when one works:

1. **llms.txt** (AI-friendly index, increasingly common):
   ```
   https://docs.example.com/llms.txt
   https://example.com/llms.txt
   ```
   Prompt: "Extract ALL documentation URLs listed in this file"

2. **sitemap.xml**:
   ```
   https://docs.example.com/sitemap.xml
   https://example.com/sitemap.xml
   ```
   Prompt: "Extract ALL URLs from this sitemap"

3. **docs.json or manifest**:
   ```
   https://docs.example.com/docs.json
   https://docs.example.com/_sidebar.md
   ```

If an index file exists, you now have the COMPLETE list of pages. Skip to Step 3.

#### Step 2: Fallback - Link Discovery (if no index found)

If no index file exists, crawl by following links:

1. **Fetch the starting URL** using WebFetch:
   ```
   Extract all information from this documentation page. Return:
   1. The main content/text of this page
   2. ALL internal documentation links (same domain)
   3. The page title
   4. Navigation structure (sidebar links, breadcrumbs)
   ```

2. **Build a URL queue** from discovered links:
   - Include paths: `/docs/`, `/guide/`, `/api/`, `/reference/`, `/tutorial/`, `/quickstart/`, `/introduction/`, `/getting-started/`, `/examples/`, `/features/`, `/integrations/`
   - Exclude paths: `/blog/`, `/changelog/`, `/legal/`, `/privacy/`, `/terms/`, `/pricing/`, `/about/`, `/careers/`, `/contact/`
   - Exclude: external domains, asset files (`.css`, `.js`, `.png`, `.jpg`, `.svg`, `.ico`)

3. **Recursively discover more links** from each fetched page until no new URLs are found.

#### Step 3: Prioritize and Crawl Pages

With your complete URL list (from index or discovery):

1. **Categorize by priority**:
   - **HIGH**: quickstart, getting-started, introduction, overview (fetch first)
   - **MEDIUM**: guides, tutorials, features, api-reference
   - **LOW**: integrations, advanced, edge cases

2. **Fetch pages in priority order** using WebFetch:
   ```
   Extract ALL content from this documentation page:
   1. Full text content
   2. ALL code examples with language tags
   3. Environment variables mentioned
   4. Package/dependency names
   5. API methods and signatures
   ```

3. **Batch for efficiency**: Fetch up to 3-5 pages in parallel using multiple WebFetch calls.

4. **Coverage targets**:
   - Small docs (<30 pages): Fetch ALL pages
   - Medium docs (30-100 pages): Fetch all HIGH + MEDIUM priority (~50-70%)
   - Large docs (100+ pages): Fetch all HIGH + selective MEDIUM (~30-50%)

5. **Store results**: `{ url, title, content, codeExamples[], category }`

### Phase 2: Analyze Content

Analyze the collected documentation to understand:

1. **Core Purpose**: What does this tool/library/service do? What problem does it solve?

2. **Content Categories** - Group pages into:
   - **Quickstart/Getting Started**: Installation, setup, first steps
   - **Core Concepts**: Key ideas, architecture, how it works
   - **API Reference**: Functions, methods, parameters, types
   - **Guides/Tutorials**: Step-by-step walkthroughs
   - **Integrations**: Framework support, third-party tools
   - **Advanced**: Edge cases, optimization, troubleshooting

3. **Code Patterns**: Extract ALL code snippets from the documentation:
   - Installation commands
   - Import statements
   - Initialization/setup code
   - Common API calls
   - Full working examples
   - Error handling patterns

4. **Detect Language & Framework**:
   - Primary language: TypeScript, Python, JavaScript, Go, etc.
   - Package manager: npm, pnpm, pip, etc.
   - Framework dependencies: Playwright, Puppeteer, Express, FastAPI, etc.
   - Environment variables required

5. **Key Triggers**: What keywords/phrases should activate this skill?
   - The tool/library name
   - Common tasks it performs
   - Error messages users might encounter
   - Related technologies

### Phase 3: Generate Scripts

Before generating the skill files, create working executable scripts based on the documentation.

#### 3.1 Determine Script Types Needed

Based on the documentation, identify which scripts to create:

| Doc Content | Script to Generate |
|-------------|-------------------|
| Quickstart guide | `scripts/quickstart.ts` - minimal working example |
| Authentication/setup | `scripts/setup.ts` - initialization and config |
| Core API operations | `scripts/examples/*.ts` - one per major feature |
| Data extraction | `scripts/extract.ts` - scraping/data gathering |
| Automation workflows | `scripts/automate.ts` - multi-step workflows |

#### 3.2 Script Structure

Each script should be **complete and runnable**:

```typescript
// scripts/quickstart.ts
import { Client } from "library-name";
import "dotenv/config";

// Environment variables needed
const apiKey = process.env.LIBRARY_API_KEY;
if (!apiKey) {
  console.error("Missing LIBRARY_API_KEY environment variable");
  process.exit(1);
}

async function main() {
  // Initialize client
  const client = new Client({ apiKey });

  // Core functionality from docs
  const result = await client.doSomething();

  console.log("Result:", result);
}

main().catch(console.error);
```

#### 3.3 Generate package.json / requirements.txt

**For TypeScript/JavaScript:**
```json
{
  "name": "skill-name-scripts",
  "type": "module",
  "scripts": {
    "quickstart": "npx tsx scripts/quickstart.ts",
    "example:feature": "npx tsx scripts/examples/feature.ts"
  },
  "dependencies": {
    // Extract from docs - the actual packages needed
  },
  "devDependencies": {
    "tsx": "^4.0.0",
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "dotenv": "^16.0.0"
  }
}
```

**For Python:**
```
# requirements.txt
library-name>=1.0.0
python-dotenv>=1.0.0
# Additional deps from docs
```

#### 3.4 Generate .env.example

Create a template for required environment variables:
```
# .env.example
LIBRARY_API_KEY=your_api_key_here
# Add other env vars mentioned in docs
```

### Phase 4: Generate Skill Files

Create the skill in `skills/<skill-name>/` where `<skill-name>` is derived from the documentation (e.g., "browserbase", "stagehand", "stripe").

#### 4.1 Generate SKILL.md

Create `SKILL.md` with:

```yaml
---
name: <skill-name>
description: <one-line description of what the skill helps with>
---
```

**SKILL.md Body Guidelines** (read `references/skill-creator-guide.md` for full details):

- **Keep under 500 lines** - move detailed content to `references/`
- **Context efficiency**: Only include what Claude can't deduce
- **Focus on the "how"**: Step-by-step workflows, not encyclopedic coverage
- **Include code examples**: Show, don't tell
- **Define triggers clearly**: When should this skill activate?
- **Reference scripts**: Point users to `scripts/` for runnable examples

**Structure the body as:**
1. Brief overview (2-3 sentences max)
2. When to use this skill (trigger conditions)
3. Quick reference for common tasks
4. Code templates for frequent patterns
5. Available scripts and how to run them
6. Pointers to reference files for deep dives

#### 4.2 Generate Reference Files

Create `references/` directory with topic-specific files:

- `quickstart.md` - Installation and first steps
- `api-reference.md` - Detailed API documentation
- `examples.md` - Code examples and patterns
- Additional files as needed based on content categories

**Reference file guidelines:**
- One topic per file
- Include table of contents if >100 lines
- Preserve code examples from original docs
- Keep formatting clean and scannable

#### 4.3 Include Generated Scripts

Move the scripts created in Phase 3 into the skill:
- `scripts/` - All executable scripts
- `package.json` or `requirements.txt` - Dependencies
- `.env.example` - Environment variable template

### Phase 5: Output Summary

After generation, provide:

1. **Skill location**: `skills/<skill-name>/`
2. **Files created**: List all generated files
3. **Skill statistics**: Line counts, reference file count
4. **Installation command**: `claude skill install ./skills/<skill-name>`
5. **Test suggestion**: A simple command to verify the skill works

## URL Discovery Strategy

### Priority: Use Index Files First

Many documentation platforms provide complete page indexes:

| Platform | Index Location | Format |
|----------|---------------|--------|
| Mintlify | `/llms.txt` | Plain text URLs |
| Docusaurus | `/sitemap.xml` | XML |
| GitBook | `/sitemap.xml` | XML |
| ReadTheDocs | `/sitemap.xml` | XML |
| MkDocs | `/sitemap.xml` | XML |
| Custom | `/docs.json`, `/_sidebar.md` | Varies |

**Always check for llms.txt first** - it's specifically designed for AI consumption and lists all documentation pages.

### Handling Large Documentation Sites

For sites with 100+ pages (like Browserbase with 127 pages):

1. **Don't try to fetch everything** - context limits make this impractical
2. **Prioritize by category**:
   - Introduction/Overview: Always fetch
   - Quickstart: Always fetch
   - Core API: Always fetch
   - Guides: Fetch top 5-10
   - Integrations: Fetch most popular 3-5
   - Reference: Summarize, link to full docs

3. **Generate comprehensive reference files** that point to full docs for deep dives

### Handling Subdomains

- `docs.example.com` - crawl
- `api.example.com` - only if it's API docs
- `blog.example.com` - skip
- `example.com` (main site) - skip unless it contains docs

### Rate Limiting

WebFetch handles rate limiting automatically. For large crawls:
- Batch 3-5 parallel fetches
- Wait briefly between batches if errors occur

## Example Output Structure

For `https://docs.browserbase.com`:

```
skills/browserbase/
├── SKILL.md                 # ~200-400 lines
│   - Overview
│   - When to use
│   - Quick reference
│   - Common patterns
│   - Available scripts
│
├── scripts/                 # Runnable code examples
│   ├── quickstart.ts        # Minimal working example
│   ├── create-session.ts    # Session management
│   ├── extract-data.ts      # Data extraction example
│   └── examples/
│       ├── playwright.ts    # Playwright integration
│       ├── puppeteer.ts     # Puppeteer integration
│       └── stealth.ts       # Anti-detection setup
│
├── references/
│   ├── quickstart.md        # Installation, first session
│   ├── api-reference.md     # Sessions, contexts, CDP
│   ├── integrations.md      # Playwright, Puppeteer, Selenium
│   └── advanced.md          # Proxies, captchas, debugging
│
├── package.json             # Dependencies & run scripts
└── .env.example             # Required environment variables
```

### Running Generated Scripts

After skill generation, users can run scripts with:

```bash
cd skills/browserbase
npm install
cp .env.example .env  # Then fill in API keys
npm run quickstart    # Run the quickstart example
```

## Quality Checklist

Before completing, verify:

**SKILL.md:**
- [ ] Has valid YAML frontmatter
- [ ] Under 500 lines
- [ ] Description clearly states what the skill does
- [ ] Triggers are specific and relevant

**Scripts:**
- [ ] All scripts are syntactically correct
- [ ] Scripts have proper error handling
- [ ] Environment variables are validated
- [ ] package.json/requirements.txt includes all dependencies
- [ ] .env.example lists all required variables
- [ ] npm run scripts are defined for each script

**References:**
- [ ] Code examples are syntactically correct
- [ ] Reference files are well-organized
- [ ] No broken internal links between files

**Test the skill:**
- [ ] Run `npm install` in the skill directory
- [ ] Run `npm run quickstart` (should fail gracefully without API key)
- [ ] Verify skill loads correctly in Claude Code
