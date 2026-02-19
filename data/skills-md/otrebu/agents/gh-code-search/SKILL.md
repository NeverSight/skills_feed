---
name: gh-code-search
description: Search GitHub for real-world code examples and implementation patterns. Use when user wants to find code examples on GitHub, search GitHub repositories, discover how others implement features, learn library usage patterns, or research architectural approaches. Fetches top results with smart ranking (stars, recency, language), extracts factual data (imports, syntax patterns, metrics), and returns clean markdown for analysis and pattern identification.
allowed-tools: Bash(gh auth:*), Bash(pnpm:*)
---

# GitHub Code Search

Fetch real-world code examples from GitHub through intelligent multi-search orchestration.

## Prerequisites

**Required:**
- gh CLI installed and authenticated (`gh auth login --web`)
- Node.js + pnpm

**Validation:**
```bash
gh auth status  # Should show authenticated
```

## Usage

```bash
cd plugins/knowledge-work/skills/gh-code-search
pnpm install  # First time only
pnpm search "your query here"
```

## When to Use

**Invoke this skill when user requests:**
- Real-world examples ("how do people implement X?")
- Library usage patterns ("show me examples of workflow.dev usage")
- Implementation approaches ("claude code skills doing github search")
- Architectural patterns ("repository pattern in TypeScript")
- Best practices for specific frameworks/libraries

**Examples requiring nuanced multi-search:**
- "Find React hooks" → Need queries for `useState/useEffect` (imports), `function use` (definitions), `const use =` (arrow functions)
- "Express error handling middleware" → Queries for `(req, res, next) =>` (signatures), `app.use` (registration), `function(err,` (error handlers)
- "How do people use XState?" → Queries for `useMachine`, `createMachine`, `interpret` (actual function names, not "state machine")
- "GitHub Actions for TypeScript projects" → Queries for `.yml` workflow files + `actions/setup-node` + `tsc` or `pnpm build` (actual commands)

## How It Works

**Division of responsibilities:**

### Script Responsibilities (Tool Implementation)
1. Authenticates with GitHub (gh CLI token)
2. Executes single search query (Octokit API, pagination, text-match)
3. Ranks by quality (stars, recency, code structure)
4. Fetches top 10 files in parallel
5. Extracts factual data (imports, syntax patterns, metrics)
6. Returns clean markdown with code + metadata + **GitHub URLs for all files**

**The script is a single-query tool.** Claude orchestrates multiple invocations.

### Claude's Orchestration Responsibilities

**Claude executes a multi-phase workflow:**

1. **Query Strategy Generation:** Craft 3-5 targeted search queries considering:
   - Language context (TypeScript vs JavaScript)
   - File type nuances (tsx vs ts for React, config files vs implementations)
   - Specificity variants (broad → narrow)
   - Related terminology expansion

2. **Sequential Search Execution:** Run tool multiple times, adapting queries based on intermediate results

3. **Result Aggregation:** Combine all code files, deduplicate by repo+path, preserve GitHub URLs

4. **Pattern Analysis:** Extract common imports, architectural styles, implementation patterns

5. **Comprehensive Summary:** Synthesize findings with trade-offs, recommendations, key code highlights, and **GitHub URLs for ALL meaningful files**

---

## Claude's Orchestration Workflow

### Step 1: Analyze Request & Generate Queries (BLOCKING)

**Analyze user request to determine:**
- Primary language/framework (TypeScript, Python, Go, etc.)
- Specific patterns sought (hooks, middleware, configs, actions)
- File type variations needed (tsx vs ts, yaml vs json)

**Generate 3-5 targeted queries considering nuances:**

**Example 1: "Find React hooks"**
- Query 1: `useState useEffect language:typescript extension:tsx` (matches import statements, hook usage in components)
- Query 2: `function use language:typescript extension:ts` (matches hook definitions like `function useFetch()`)
- Query 3: `const use = language:typescript` (matches arrow function hooks like `const useAuth = () =>`)

**Example 2: "Express error handling"**
- Query 1: `(req, res, next) => language:javascript` (matches middleware function signatures)
- Query 2: `app.use express` (matches Express middleware registration)
- Query 3: `function(err, req, res, next) language:javascript` (matches error handler signatures with 4 params)

**Example 3: "XState state machines in React"**
- Query 1: `useMachine language:typescript extension:tsx` (matches React hook usage like `const [state, send] = useMachine(machine)`)
- Query 2: `createMachine language:typescript` (matches machine definitions and imports)
- Query 3: `interpret xstate language:typescript` (matches service creation like `const service = interpret(machine)`)

**Rationale for each query:**
- Match actual code patterns (function names, import statements, signatures)
- NOT human-friendly search terms or documentation phrases
- Different file extensions capture different use cases (tsx for components, ts for utilities)
- Specific function/variable names find concrete implementations
- Signature patterns match common code structures (arrow functions, function declarations)
- Language/extension filters prevent noise from unrelated languages

**CHECKPOINT:** Verify 3-5 queries generated before proceeding

---

### Step 2: Execute Searches Sequentially

**For each query (in order):**

```bash
cd plugins/knowledge-work/skills/gh-code-search
pnpm search "query text here"
```

**After each search:**
1. **Note result count** - Too many? Too few?
2. **Check quality indicators** - Stars, recency, code structure scores
3. **Identify patterns** - Are results converging on specific approaches?
4. **Adapt next query if needed:**
   - Too many results → Narrow scope (add more filters)
   - Too few results → Broaden (remove restrictive filters)
   - Found strong pattern → Search for similar variations

**Track which queries succeed** - Note for summary which strategies were effective

**Early stopping:** If first 2-3 queries yield 30+ high-quality results, remaining queries optional

---

### Step 3: Aggregate Results

**Combine all code files from all searches:**

1. **Collect files** from each search output with their GitHub URLs
2. **Deduplicate** by `repository.full_name + file_path`
   - Keep highest-scored version if duplicates exist
   - Note which queries found the same file (indicates strong relevance)
3. **Maintain diversity** - Ensure multiple repositories represented (avoid 10 files from one repo)
4. **Track provenance** - Remember which query found each file (useful for analysis)
5. **Preserve GitHub URLs** - Maintain full GitHub URLs for every file to include in summary

**Result:** Unified list of 15-30 unique, high-quality code files with GitHub URLs

---

### Step 4: Analyze Patterns

**Extract factual patterns across all code files:**

**Import Analysis:**
- List most common imports (group by library)
- Identify standard library vs third-party dependencies
- Note version-specific patterns (e.g., React 18 hooks)

**Architectural Patterns:**
- Functional vs class-based implementations
- Custom hooks vs inline logic
- Middleware chains vs single-handler
- Configuration patterns (env vars, config files, inline)

**Code Structure:**
- Function signatures (parameters, return types)
- Error handling approaches (try/catch, error middleware, Result types)
- Testing patterns (unit vs integration, mocking strategies)
- Documentation styles (JSDoc, inline comments, README)

**Language Distribution:**
- TypeScript vs JavaScript split
- Strict mode usage
- Type definition patterns

**DO NOT editorialize** - Extract facts, not opinions. Analysis comes in Step 5.

---

### Step 5: Generate Comprehensive Summary

**Output format (exact structure):**

```markdown
# GitHub Code Search: [User Query Topic]

## Search Strategy Executed

Ran [N] targeted queries:
1. `query text` - [brief rationale] → [X results]
2. `query text` - [brief rationale] → [Y results]
3. ...

**Total unique files analyzed:** [N]

---

## Pattern Analysis

### Common Imports
- `library-name` - Used in [N/total] files
- `another-lib` - Used in [M/total] files

### Architectural Styles
- **Functional Programming** - [N] files use pure functions, immutable patterns
- **Object-Oriented** - [M] files use classes, inheritance
- **Hybrid** - [K] files mix both approaches

### Implementation Patterns
- **Pattern 1 Name**: [Description with prevalence]
- **Pattern 2 Name**: [Description with prevalence]

---

## Approaches Found

### Approach 1: [Name]
**Repos:** [repo1], [repo2]
**Characteristics:**
- [Key trait 1]
- [Key trait 2]

**Example:** [repo/file_path:line_number](github_url)
```language
[relevant code snippet - NOT just first 40 lines]
```

### Approach 2: [Name]
[Similar structure]

---

## Trade-offs

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| Approach 1 | [pros] | [cons] | [use case] |
| Approach 2 | [pros] | [cons] | [use case] |

---

## Recommendations

**For your use case ([infer from user's context]):**

1. **Primary recommendation:** [Approach name]
   - **Why:** [Rationale based on analysis]
   - **Implementation:** [High-level steps]
   - **References:** [repo/file_path:line_number](github_url)

2. **Alternative:** [Another approach]
   - **When to use:** [Scenarios where this is better]
   - **References:** [repo/file_path:line_number](github_url)

---

## Key Code Sections

### [Concept 1]
**Source:** [repo/file_path:line_range](github_url)
```language
[Specific relevant code - imports, key function, not arbitrary truncation]
```
**Why this matters:** [Brief explanation]

### [Concept 2]
**Source:** [repo/file_path:line_range](github_url)
```language
[Specific relevant code]
```
**Why this matters:** [Brief explanation]

---

## All GitHub Files Analyzed

**IMPORTANT: Include GitHub URLs for ALL meaningful files found across all searches.**

List every unique file analyzed (15-30 files), grouped by repository:

### [repo-owner/repo-name] ([stars]⭐)
- [file_path](github_url) - [language] - [brief description of what this file demonstrates]
- [file_path](github_url) - [language] - [brief description]

### [repo-owner/repo-name2] ([stars]⭐)
- [file_path](github_url) - [language] - [brief description]

**Format:** Direct GitHub blob URLs with line numbers where relevant (e.g., `https://github.com/owner/repo/blob/main/path/file.ts#L10-L50`)
```

**Summary characteristics:**
- **Factual** - Based on extracted data, not assumptions
- **Actionable** - Clear recommendations with reasoning
- **Contextualized** - References specific code locations with line numbers
- **Balanced** - Shows trade-offs, not just "best practice"
- **Comprehensive** - Covers patterns, approaches, trade-offs, recommendations
- **Accessible** - GitHub URLs for ALL meaningful files so users can explore full source code

---

### Step 6: Save Results to File

**After generating comprehensive summary, persist for future reference:**

1. **Generate timestamp:**
   - Invoke `timestamp` skill to get deterministic YYYYMMDDHHMMSS format
   - Example: `20250110143052`

2. **Sanitize query for filename:**
   - Convert user's original query to kebab-case slug
   - Rules: lowercase, spaces → hyphens, remove special chars, max 50 chars
   - Example: "React hooks useState" → "react-hooks-usestate"

3. **Construct file path:**
   - Directory: `docs/research/github/`
   - Format: `<timestamp>-<sanitized-query>.md`
   - Full path: `docs/research/github/20250110143052-react-hooks-usestate.md`

4. **Save using Write tool:**
   - Content: Full comprehensive summary from Step 5
   - Ensures persistence across sessions
   - User can reference past research

5. **Log saved location:**
   - Inform user where file was saved
   - Example: "Research saved to docs/research/github/20250110143052-react-hooks-usestate.md"

**Why save:**
- Comprehensive summaries represent significant analysis work (30-150s of API calls)
- Users may want to reference patterns/trade-offs later
- Builds searchable knowledge base of GitHub research
- Avoids re-running expensive queries for same topics

---

## Error Handling

**Common issues:**

- **Auth errors:** Prompt user to run `gh auth login --web`
- **Rate limits:** Show remaining quota, reset time. If hit during multi-search, stop gracefully with partial results
- **Network failures:** Continue with partial results, note which queries failed
- **No results for query:** Note in summary, adjust subsequent queries to be broader
- **All queries return same files:** Note low diversity, recommend broader initial queries

**Graceful degradation:** Partial results are acceptable. Complete summary based on available data.

---

## Limitations

- GitHub API rate limit: 5,000 req/hr authenticated (multi-search uses more quota)
- Each tool invocation fetches top 10 results only
- Skips files >100KB
- Sequential execution takes longer than single query (10-30s per query)
- Provides factual data, not conclusions (Claude interprets patterns)
- Deduplication assumes exact path matches (renamed files treated as unique)

---

## Typical Execution Time

**Per query:** 10-30 seconds depending on:
- Number of results (100 max)
- File sizes
- Network latency
- API rate limits

**Full workflow (3-5 queries):** 30-150 seconds

**Optimization:** If first queries yield sufficient results, skip remaining queries

---

## Integration Notes

**Example: User asks "find Claude Code skills doing github search"**

```javascript
// 1. Claude analyzes: Skills use SKILL.md with frontmatter, likely in .claude/skills/
// 2. Claude generates queries:
//    - "filename:SKILL.md github search" (matches SKILL.md files with "github search" text)
//    - "octokit.rest.search language:typescript" (matches actual Octokit API usage)
//    - "gh api language:typescript path:skills" (matches gh CLI usage in skills)
// 3. Claude executes sequentially:
cd plugins/knowledge-work/skills/gh-code-search
pnpm search "filename:SKILL.md github search"
// [analyze results]
pnpm search "octokit.rest.search language:typescript"
// [analyze results]
pnpm search "gh api language:typescript path:skills"
// 4. Claude aggregates, deduplicates, analyzes patterns
// 5. Claude generates comprehensive summary with trade-offs and recommendations
```

---

## Testing

**Validate workflow with diverse queries:**
- Simple: "React hooks" (should generate 3+ queries, combine results)
- Complex: "GitHub Actions TypeScript project setup" (requires config + implementation queries)
- Ambiguous: "state management" (should generate queries for Redux, Zustand, XState, Context)

**Check quality:**
- Deduplication works (no repeated files in summary)
- Diverse repositories (not all from one repo)
- Summary includes trade-offs and recommendations
- Code snippets are relevant (not arbitrary truncations)
