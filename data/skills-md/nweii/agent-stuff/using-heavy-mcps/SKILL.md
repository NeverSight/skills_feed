---
name: using-heavy-mcps
description: "Use mcporter and jq to reduce token bloat from heavy MCPs like Sanity or Brain vault. Filter and compact tool outputs outside chat to feed only essential data back to the model."
---

# Token-Efficient MCP Usage via MCPorter

When working with MCPs that return large payloads—like Sanity queries with full document content or Brain vault searches with entire file contents—you can route these calls through `mcporter` outside of chat, trim the output with `jq`, and feed only the compact result back to the model. This avoids the 20–40k token bloat that comes from loading full responses into context.

## When to Use This Pattern

Use mcporter + jq when:

- **Large responses**: Sanity queries returning full documents, Brain vault searches with file contents
- **Repeated queries**: You need the same data multiple times and only care about specific fields
- **Field filtering**: The MCP returns 50 fields but you only need 3
- **Chained operations**: Multiple MCP calls where each bloats context
- **List operations**: Getting 100 items but only needing titles and IDs

**Don't use this pattern when:**

- Exploring unfamiliar data (let Cursor call MCP directly to see full structure)
- Response is already small (< 1000 tokens)
- You need the full response for analysis

## The Core Pattern

The basic workflow:

1. **Run MCP outside chat** via `bunx mcporter call`
2. **Pipe to jq** to extract only needed fields
3. **Feed compact result** back into chat
4. **Save as one-liner** for reuse

```bash
bunx mcporter call 'MCP-Name.tool_name(param: "value")' | jq 'filter'
```

**Alternative syntaxes:**

```bash
# Shorthand (infers 'call' command)
bunx mcporter 'MCP-Name.tool_name(param: "value")' | jq 'filter'

# Structured JSON output (useful for error handling)
bunx mcporter call 'MCP-Name.tool_name(param: "value")' --output json | jq 'filter'
```

## Two Approaches: jq vs CallResult Helpers

mcporter responses include built-in helpers that can replace jq for simple extractions. Choose based on your needs:

### Option A: Built-in CallResult Helpers (Simpler)

mcporter returns results wrapped in a `CallResult` object with helper methods:

```bash
# Extract plain text only (strips all metadata/formatting)
bunx mcporter call 'Brain.vault(action: "search", query: "portfolio")' | node -e "console.log(JSON.parse(require('fs').readFileSync(0)).result.text())"

# Get markdown format
# Similar node one-liner but calling .markdown()

# Get parsed JSON
# Similar but calling .json()
```

**When to use:** Simple text extraction, when you want markdown, or when you need the full JSON object.

**Limitation:** Less flexible than jq for complex filtering/transforming.

### Option B: jq Filtering (More Powerful)

jq is a command-line JSON filter. Think of it as "grep for JSON."

**Basic patterns:**

```bash
# Get specific fields from each item in array
jq '[.[] | {id: ._id, title: .title}]'

# Limit to first 5 results
jq '.results[:5]'

# Extract nested field
jq '.results[] | .frontmatter.description'

# Combine: first 3 items, specific fields
jq '.results[:3] | [.[] | {path: .path, desc: .frontmatter.description}]'

# Filter by condition
jq '[.[] | select(.status == "published")]'
```

**When to use:** Precise field selection, transforming data structure, filtering by conditions, combining multiple operations.

**Recommendation:** Start with jq since it's more flexible and works across any JSON output, not just mcporter.

## Usage Examples

For concrete examples of using this pattern with Sanity and Brain Vault MCPs, see [EXAMPLES.md](EXAMPLES.md).

## Integration Patterns

### Pattern 1: One-liners in chat

When you need compact data mid-conversation, run the command and paste the filtered output:

```
User: "Can you review my portfolio projects? Here's the data:"
<paste result of mcporter + jq command>
```

### Pattern 2: Embedding in other Cursor rules

Add mcporter commands to rules that need specific data:

```markdown
## Portfolio Context

When discussing portfolio work, use this to fetch current project list:

<command>
bunx mcporter call 'Sanity Developer.query_documents(
  resource: {projectId: "xyz", dataset: "production"},
  query: "*[_type == \"project\"]"
)' | jq '[.[] | {title: .title, role: .role}]'
</command>
```

### Pattern 3: Save as shell alias

Add to your `.zshrc` for frequently-used queries:

```bash
alias portfolio-list='bunx mcporter call '"'"'Sanity Developer.query_documents(
  resource: {projectId: "xyz", dataset: "production"},
  query: "*[_type == \"project\"]"
)'"'"' | jq "[.[] | {title: .title, slug: .slug.current}]"'
```

Then just run: `portfolio-list`

## When to Just Use Cursor's MCP Calls

Let Cursor call MCPs directly when:

- **Exploring**: You don't know the response structure yet
- **Small responses**: The data is already compact
- **Interactive filtering**: You want to iteratively refine what you're looking for
- **One-off questions**: Not worth the setup overhead

The mcporter pattern is for repeatability and token efficiency, not every MCP interaction.

## Avoiding Token Waste on Failed Calls

**Set timeouts to fail fast:**

```bash
# Don't wait forever for a hung MCP call
bunx mcporter call 'Brain.vault(action: "search", query: "test")' --timeout 10000
```

Default timeout is 30 seconds. For slow operations, increase it. For quick checks, decrease it.

**Check auth before expensive queries:**

```bash
# Verify authentication status
bunx mcporter config get "Sanity Developer"

# If auth is required, do it once
bunx mcporter auth "Sanity Developer"
```

This prevents loading huge error messages into context when auth fails.

**Use --output json for programmatic error handling:**

```bash
bunx mcporter call 'Brain.vault(action: "search", query: "test")' --output json
```

The structured envelope makes it easier to detect failures without loading full error traces into context.

## Debugging Tips

**Check available MCPs:**

```bash
bunx mcporter list
```

**See tool signatures and schemas:**

```bash
bunx mcporter list Brain --schema
bunx mcporter list "Sanity Developer" --schema
```

**Test without jq first:**

```bash
bunx mcporter call 'Brain.vault(action: "search", query: "test")'
```

Then add jq filtering once you see the structure.

**Format jq output for readability:**

```bash
... | jq '.'
# vs compact:
... | jq -c '.'
```

## Real-World Token Savings

**Before (direct MCP call in chat):**

- Sanity query for 10 projects with full content: ~25,000 tokens
- Brain vault search returning 5 notes: ~15,000 tokens

**After (mcporter + jq):**

- Same Sanity query, titles/IDs only: ~500 tokens
- Same vault search, metadata only: ~300 tokens

**Savings:** 95%+ reduction for typical filtered queries.

## Additional Resources

**Official mcporter documentation:** Available via Context7 at `/steipete/mcporter`

**Key docs to reference:**

- Call syntax and examples: [mcporter/docs/call-syntax.md](https://github.com/steipete/mcporter/blob/main/docs/call-syntax.md)
- Tool calling guide: [mcporter/docs/tool-calling.md](https://github.com/steipete/mcporter/blob/main/docs/tool-calling.md)
- Configuration: [mcporter/docs/config.md](https://github.com/steipete/mcporter/blob/main/docs/config.md)
