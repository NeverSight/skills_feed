---
name: osgrep
description: Semantic NLP-based code search using neural embeddings and hybrid ranking
version: 0.4.15
triggers:
  - semantic code search
  - find similar implementations
  - conceptual code exploration
  - NLP grep
  - meaning-based search
  - cross-language patterns
context_codebase: ../osgrep-codebase
author: osgrep team
integration: claude-code
---

# osgrep - Semantic Code Search Skill

## Overview

**osgrep** transforms code search from exact string matching to semantic understanding. It uses neural embeddings (Granite + ColBERT) with hybrid ranking (Vector + BM25 + RRF) to find code by *meaning*, not just tokens.

**Core principle**: `grep` finds strings, `osgrep` finds concepts.

## When to Use This Skill

### Activate osgrep when:
- User asks to "find" or "search for" concepts (not exact strings)
- Exploring unfamiliar codebases
- Finding similar implementations across files/languages
- Questions like "how does the code handle X?"
- Architectural understanding ("show me all API endpoints")
- Pattern discovery ("find retry logic examples")

### DO NOT use osgrep when:
- User provides exact string/regex pattern → use `rg` or `grep`
- Searching for specific variable/function names → use `rg`
- Simple token search → use `rg`
- User explicitly requests grep/ripgrep → respect their choice

## Core Concepts

### Semantic vs Lexical Search

```bash
# Lexical (grep/rg) - exact tokens
rg "authenticate"  # Finds: authenticate, authenticated, authentication

# Semantic (osgrep) - conceptual meaning
osgrep "user login verification"
# Finds: authenticate(), verifyCredentials(), checkUserSession(),
#        validateToken(), isAuthorized() - all semantically similar
```

### Hybrid Architecture

```
Query → [Vector Search] + [BM25 Full-Text] → [RRF Fusion] → [ColBERT Rerank] → Results
         (semantic)        (lexical)          (rank merge)    (precision)
```

**Why hybrid**:
- Vector search: Captures semantic similarity ("auth" ≈ "login" ≈ "credential")
- BM25: Ensures exact tokens aren't missed ("JWT", "bcrypt")
- RRF: Merges rankings without score normalization
- ColBERT: Refines top results with token-level cross-attention

### Relevance Scoring

```yaml
0.9-1.0: Nearly identical (duplicates)
0.7-0.9: Highly relevant ✓ (trust these)
0.5-0.7: Moderately relevant (check manually)
0.3-0.5: Weakly relevant (likely noise)
0.0-0.3: False positive (ignore)
```

**Best practice**: Filter for scores > 0.6 in automated workflows.

## Command Reference

### Basic Search
```bash
osgrep "<conceptual query>" [path] [options]

# Examples
osgrep "JWT token validation"
osgrep "error handling for database connections" src/
osgrep "rate limiting middleware" --max-count 20
```

### Server Mode (Recommended)
```bash
# Start server with live indexing
osgrep serve --port 4444 &

# All queries now use auto-updated index
osgrep "query"
```

### Indexing
```bash
osgrep index                    # Index current directory
osgrep list                     # Show all indexed projects
osgrep doctor                   # Check installation health
```

### Output Formats
```bash
osgrep "query"                  # Default: snippets with context
osgrep "query" --content        # Full chunk content
osgrep "query" --compact        # File paths only (for piping)
osgrep "query" --scores         # Show relevance scores
osgrep "query" --json           # JSON output (for scripting)
osgrep "query" --plain          # No ANSI colors
```

### Result Control
```bash
osgrep "query" --max-count 5    # Total results (default: 10)
osgrep "query" --per-file 3     # Matches per file (default: 1)
osgrep "query" --sync           # Sync index before search
```

## Integration with Claude Code

### Prefer --compact for File Lists
```bash
# When Claude needs file paths for further processing
files=$(osgrep "authentication logic" --compact)
echo "$files" | xargs cat  # Read files
echo "$files" | xargs rg "specific_token"  # Further filtering
```

### Use --json for Structured Output
```bash
# When Claude needs to parse results programmatically
osgrep "error handling" --json |
  jq -r '.results[] | select(.score > 0.7) | .path' |
  sort -u
```

### Use --scores for Confidence
```bash
# When Claude needs to assess result relevance
osgrep "database migration" --scores |
  awk '$2 > 0.65 {print $1}'  # Only high-confidence matches
```

### Combine with Other Tools
```bash
# osgrep → rg pipeline
osgrep "API endpoint" --compact | xargs rg "POST|PUT"

# osgrep → ast-grep pipeline
osgrep "validation function" --compact | xargs ast-grep --pattern 'validate($$$)'

# osgrep → fzf pipeline (interactive)
osgrep "component definition" --compact | fzf --preview 'bat {}'
```

## Common Workflows

### 1. Exploratory Search (Learning Codebase)
```bash
# Start broad
osgrep "authentication system" --max-count 20 --scores

# Identify key files
osgrep "authentication system" --compact | sort -u

# Deep dive specific aspects
osgrep "JWT token generation" --content
osgrep "password hashing" --content
osgrep "session management" --content
```

### 2. Finding Similar Implementations
```bash
# Find pattern variations
osgrep "rate limiting with token bucket" --max-count 15

# Cross-language search
cd ../python-service && osgrep "rate limiting middleware"
cd ../go-service && osgrep "rate limiting middleware"
```

### 3. Debugging (Find Error Sources)
```bash
# Semantic error search
osgrep "connection timeout error handling" --scores

# Filter high-confidence results
osgrep "connection timeout error handling" --scores |
  awk '$2 > 0.7' |
  cut -d: -f1 |
  sort -u |
  xargs bat
```

### 4. API Discovery
```bash
# Find endpoints
osgrep "REST API endpoint handlers" --max-count 30

# Filter by HTTP method
osgrep "POST API endpoint" --compact | xargs rg "POST"

# Find middleware
osgrep "authentication middleware" --content
```

### 5. Security Audit
```bash
# Find anti-patterns
osgrep "SQL injection vulnerability" --scores
osgrep "hardcoded secrets" --scores
osgrep "plaintext password" --scores

# Verify good patterns exist
osgrep "parameterized SQL queries" --max-count 10
osgrep "bcrypt password hashing" --max-count 10
```

### 6. Refactoring Prep (Impact Analysis)
```bash
# Find old pattern
osgrep "legacy cookie authentication" --compact > legacy.txt

# Find new pattern
osgrep "JWT token authentication" --compact > modern.txt

# Identify migration candidates
comm -23 <(sort legacy.txt) <(sort modern.txt)
```

### 7. Testing Gap Analysis
```bash
# Find tests
osgrep "unit test for authentication" --compact | sort > tested.txt

# Find implementations
osgrep "authentication logic" --compact | sort > all.txt

# Find untested code
comm -13 tested.txt all.txt
```

## Query Optimization

### Effective Queries (Conceptual + Specific)
```bash
# Good: Concept + context
osgrep "JWT authentication with refresh token rotation"
osgrep "error handling for database connection timeouts"
osgrep "input validation using zod schemas"
osgrep "pagination with cursor-based approach"
```

### Ineffective Queries (Too Vague or Too Specific)
```bash
# Too vague
osgrep "function"  # Use rg instead
osgrep "error"     # Too broad

# Too specific (exact token)
osgrep "getUserById"  # Use rg for exact names
osgrep "import { something }"  # Use rg for imports
```

### Query Expansion Strategy
```bash
# Instead of single term
osgrep "cache"  # ✗ Vague

# Expand to concept
osgrep "caching strategy with TTL expiration"  # ✓ Clear intent

# Add domain context
osgrep "Redis caching with automatic invalidation"  # ✓ Very specific
```

## Performance Considerations

### Query Speed
```yaml
Fast (<200ms):
  - osgrep "query" --max-count 3 --compact
  - osgrep "query" specific/path/ --max-count 5

Medium (~400ms):
  - osgrep "query"  # Default: 10 results
  - osgrep "query" --scores

Slow (>600ms):
  - osgrep "query" --max-count 50
  - osgrep "query" --content --max-count 20
```

### Index Size
```yaml
Small (<1k files):     ~50-100MB,    index time ~10-30s
Medium (1k-5k files):  ~100-500MB,   index time ~1-3min
Large (5k-10k files):  ~500MB-2GB,   index time ~5-15min
Monorepo (>10k files): ~2-10GB,      index time ~15-60min
```

### Optimization Tips
```bash
# Use server mode for active development (auto-indexing)
osgrep serve &

# Limit results for speed
osgrep "query" --max-count 5

# Target specific paths
osgrep "query" src/api/

# Use --compact to skip rendering
osgrep "query" --compact
```

## Best Practices for Claude Code

### 1. Always Check Index Status
```bash
# Before first search in a project
osgrep doctor  # Verify installation
osgrep list    # Check if project is indexed

# If not indexed
osgrep index
```

### 2. Start with Server Mode
```bash
# At project start
osgrep serve --port 4444 &

# Subsequent searches use live index
osgrep "query"
```

### 3. Use Appropriate Output Format
```bash
# For file lists → --compact
osgrep "concept" --compact

# For confidence assessment → --scores
osgrep "concept" --scores

# For scripting → --json
osgrep "concept" --json | jq ...

# For reading → default or --content
osgrep "concept"
osgrep "concept" --content
```

### 4. Filter by Relevance
```bash
# Only high-confidence results
osgrep "query" --scores | awk '$2 > 0.7'

# JSON filtering
osgrep "query" --json |
  jq -r '.results[] | select(.score > 0.7) | .path'
```

### 5. Combine with Traditional Tools
```bash
# Semantic → lexical pipeline
osgrep "API endpoint" --compact | xargs rg "router\.(get|post)"

# Semantic → syntax pipeline
osgrep "validation" --compact | xargs ast-grep --pattern 'validate($$$)'
```

### 6. Handle No Results Gracefully
```bash
# If no results, try broader query
results=$(osgrep "very specific query" --compact)
if [[ -z "$results" ]]; then
  results=$(osgrep "broader concept" --compact)
fi

# Or sync and retry
osgrep "query" --sync
```

### 7. Use Per-File Limits Strategically
```bash
# Finding entry points (one per file)
osgrep "main application initialization" --per-file 1

# Deep exploration (many per file)
osgrep "error handling patterns" --per-file 5
```

## Limitations and Workarounds

### Limitation: No Boolean Operators
```bash
# No AND/OR/NOT in queries
osgrep "auth AND JWT"  # ✗ Doesn't work

# Workaround: Multiple queries + set operations
comm -12 \
  <(osgrep "authentication" --compact | sort) \
  <(osgrep "JWT" --compact | sort)
```

### Limitation: No Regex
```bash
# Cannot use regex patterns
osgrep "user_\d+"  # ✗ Doesn't work

# Workaround: osgrep then grep
osgrep "user identifier" --compact | xargs rg "user_\d+"
```

### Limitation: English-Optimized
```bash
# Less effective on non-English code
osgrep "用户认证"  # May not work well

# Workaround: Use English equivalent
osgrep "user authentication"
```

### Limitation: Cold Start Delay
```bash
# First query after boot ~1-2s (model loading)

# Workaround: Use server mode (models stay loaded)
osgrep serve &
```

## Troubleshooting

### No Results or Low Scores
```bash
# Check if index exists
osgrep list

# Reindex if stale
osgrep index

# Try broader query
osgrep "broader concept" --max-count 20

# Check scores to diagnose
osgrep "query" --scores
```

### Server Issues
```bash
# Check if server is running
lsof -i :4444

# Start server if not running
osgrep serve &

# Check installation health
osgrep doctor
```

### Index Corruption
```bash
# Clear and rebuild
cd /path/to/project
rm -rf ~/.osgrep/data/$(basename $(pwd))
osgrep index
```

## Examples for Claude Code

### Example 1: Architecture Exploration
```bash
# User: "Explain how the authentication system works"

# Step 1: Find auth components
osgrep "authentication system" --compact > auth_files.txt

# Step 2: Get detailed content
cat auth_files.txt | head -5 | xargs osgrep "authentication flow" --content

# Step 3: Find related components
osgrep "JWT token management" --content
osgrep "session storage" --content
osgrep "password validation" --content
```

### Example 2: Bug Investigation
```bash
# User: "Why are database connections timing out?"

# Step 1: Find timeout handling
osgrep "database connection timeout" --scores --max-count 20

# Step 2: Filter high-confidence matches
osgrep "database connection timeout" --scores |
  awk '$2 > 0.7' |
  cut -d: -f1 |
  sort -u > relevant_files.txt

# Step 3: Check retry logic
cat relevant_files.txt | xargs osgrep "retry connection" --content
```

### Example 3: API Endpoint Discovery
```bash
# User: "List all POST endpoints"

# Step 1: Find API handlers
osgrep "API endpoint handler" --compact | sort -u > endpoints.txt

# Step 2: Filter by HTTP method
cat endpoints.txt | xargs rg "POST" | cut -d: -f1 | sort -u

# Step 3: Get endpoint details
osgrep "POST endpoint implementation" --content --max-count 10
```

### Example 4: Security Review
```bash
# User: "Audit the code for security issues"

# Step 1: Find potential vulnerabilities
osgrep "SQL injection" --scores > sql_issues.txt
osgrep "hardcoded credentials" --scores > cred_issues.txt
osgrep "plaintext password" --scores > pwd_issues.txt

# Step 2: Check for proper patterns
osgrep "parameterized SQL query" --max-count 10
osgrep "environment variable configuration" --max-count 10
osgrep "bcrypt password hashing" --max-count 10

# Step 3: Generate report
cat sql_issues.txt cred_issues.txt pwd_issues.txt |
  awk '$2 > 0.6 {print $0}'
```

### Example 5: Refactoring Analysis
```bash
# User: "Help me refactor legacy authentication to JWT"

# Step 1: Find legacy pattern
osgrep "session cookie authentication" --compact | sort > legacy.txt

# Step 2: Find modern pattern examples
osgrep "JWT token authentication" --compact | sort > modern.txt

# Step 3: Identify migration files
comm -23 legacy.txt modern.txt > needs_migration.txt

# Step 4: Analyze migration complexity
wc -l needs_migration.txt
cat needs_migration.txt | xargs wc -l | sort -n
```

## References

See the codebase documentation:
- **Core principles**: `../osgrep-codebase/principles/semantic-search.md`
- **Ranking details**: `../osgrep-codebase/principles/hybrid-ranking.md`
- **Workflow templates**: `../osgrep-codebase/templates/search-workflow.md`
- **Type definitions**: `../osgrep-codebase/types/core.ts`
- **Cheatsheet**: `./assets/cheatsheet.md`
- **Configuration**: `./references/configuration.md`
- **Search patterns**: `./references/search-patterns.md`

## Scripts

- **search-validator.sh**: Validate search result relevance
- See `./scripts/` directory

## Version

- **osgrep**: 0.4.15
- **Models**: Granite Embedding (30M) + osgrep-colbert (Q8)
- **Storage**: LanceDB with Tree-sitter parsing

## Quick Start for Claude Code

```bash
# 1. Check installation
osgrep doctor

# 2. Index project (if not already)
cd /path/to/project
osgrep list | grep -q "$(pwd)" || osgrep index

# 3. Start server (recommended)
osgrep serve --port 4444 &

# 4. Search semantically
osgrep "user authentication logic" --scores

# 5. Use with other tools
osgrep "API endpoint" --compact | xargs rg "router"
```

---

**Key Principle**: Use osgrep for *semantic* exploration, grep/rg for *lexical* precision. Combine both for powerful code understanding workflows.
