---
name: extract-rules
description: Extract project-specific coding rules and domain knowledge from existing codebase, generating markdown documentation for AI agents.
model: opus
allowed-tools: Read, Glob, Grep, Write, Bash(ls *), Bash(mkdir *), Bash(git ls-files *), Bash(grep *), Bash(wc *), Bash(head *), Bash(tail *), Bash(sort *), Bash(uniq *), Bash(tree *)
---

# Extract Rules

Analyzes existing codebase to extract project-specific coding rules and domain knowledge, generating structured markdown documentation for AI agents.

## Usage

```text
/extract-rules                      # Extract rules from codebase (initial)
/extract-rules --update             # Re-scan and add new patterns (preserve existing)
/extract-rules --force              # Overwrite all rule files (discard existing)
/extract-rules --from-conversation  # Extract rules from conversation and append
```

## Configuration

Users can configure extraction settings in `extract-rules.local.md`:

- Project-level: `.claude/extract-rules.local.md` (takes precedence)
- User-level: `~/.claude/extract-rules.local.md`

**File format:** YAML frontmatter only (no markdown body). The file uses `.md` extension for consistency with other Claude Code config files, but contains only YAML between `---` delimiters.

```yaml
---
# Target directories for analysis
# Default: "." (all directories not excluded by .gitignore)
# Set specific directories to limit scope
target_dirs:
  - .

# Directories to exclude (in addition to .gitignore)
# These are applied even if not in .gitignore
exclude_dirs:
  - .git
  - .claude

# File patterns to exclude (in addition to .gitignore)
exclude_patterns:
  - "*.generated.ts"
  - "*.d.ts"
  - "*.min.js"

# Note: .gitignore patterns are automatically applied
# Common exclusions like node_modules/, dist/, build/ are typically in .gitignore

# Output directory
output_dir: .claude/rules

# Output language for reports
language: ja
---
```

## Output Structure

```text
.claude/rules/
├── languages/
│   ├── typescript.md
│   └── ...              # python.md, go.md, ruby.md, etc.
├── frameworks/
│   ├── react.md
│   └── ...              # nextjs.md, firebase.md, rails.md, etc.
└── project.md           # Domain, architecture (not portable)
```

## Processing Flow

### Mode Detection

Check arguments to determine mode:

- No arguments or `--force` → **Full Extraction Mode** (Step 1-7)
- `--update` → **Update Mode** (Step U1-U5)
- `--from-conversation` → **Conversation Extraction Mode** (Step C1-C4)

---

## Full Extraction Mode

### Step 1: Load Settings

Search for `extract-rules.local.md`:

1. **Project-level**: `.claude/extract-rules.local.md`
2. **User-level**: `~/.claude/extract-rules.local.md`

**Priority:**
- If both exist, use project-level only
- If only one exists, use that file
- If neither exists, use default settings

**Extract from settings:**
- `target_dirs` (default: `["."]` - all directories)
- `exclude_dirs` (default: `[".git", ".claude"]`)
- `exclude_patterns` (default: `["*.generated.ts", "*.d.ts", "*.min.js"]`)
- `output_dir` (default: `.claude/rules`)
- `language` (default: `ja`)

**Note:** `.gitignore` patterns are always applied. Common exclusions like `node_modules/`, `dist/`, `build/` are typically in `.gitignore` and automatically excluded.

### Step 2: Detect Project Type

Detect project language and framework:

**1. Check configuration files:**
- `package.json` → Node.js/TypeScript/JavaScript
- `tsconfig.json` → TypeScript
- `pyproject.toml`, `requirements.txt` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `Gemfile` → Ruby/Rails
- `pom.xml`, `build.gradle` → Java

**2. Count file extensions:**
- `.ts`, `.tsx` → TypeScript
- `.js`, `.jsx` → JavaScript
- `.py` → Python
- `.go` → Go
- `.rb` → Ruby

**3. Detect framework-specific files:**

Identify frameworks by their config files (e.g., `next.config.*`, `playwright.config.*`, `jest.config.*`) and dependencies in package.json, requirements.txt, Gemfile, etc.

**Output:** List of detected languages and frameworks

### Step 3: Collect Sample Files

Collect target files for analysis:

1. **Get git-tracked files** (if in a git repository)
   - Use `git ls-files` to get list of tracked files
   - This automatically respects ALL `.gitignore` files (root and subdirectories)
   - If not a git repo, fall back to Glob with manual exclusions:
     - Read `.gitignore` if present and apply patterns
     - Apply `exclude_dirs` and `exclude_patterns` from settings
     - Note: Nested `.gitignore` files may not be fully respected in non-git mode

2. Filter files by `target_dirs` setting

3. Exclude files matching:
   - `exclude_dirs` from settings
   - `exclude_patterns` from settings

4. Filter by detected language extensions

5. Sample files per category, distributed across directories for representative coverage

**Note:** Using `git ls-files` ensures that nested `.gitignore` files in subdirectories are automatically respected. Untracked files (e.g., `.env`, local configs) are excluded, which helps protect sensitive information.

### Step 4: Analyze by Category

For each detected language and framework:

1. Use Grep/Read to collect relevant code patterns

2. **Classify each pattern** (see Concrete Example Criteria):
   - **General style choice** (uses only language built-ins) → Abstract principle + hints
   - **Project-defined symbol** (types, functions, hooks defined in project) → Include concrete example

3. **For general style patterns:**
   - Group related patterns (e.g., "prefer const", "avoid mutations", "use spread" → Immutability)
   - Formulate as principle with parenthetical implementation hints (2-4 keywords)

4. **For project-specific patterns:**
   - Extract only the **minimal signature** (type definition, function signature, or API combination)
   - Format as one line: `signature` - brief context (2-5 words)
   - Avoid multi-line code blocks to minimize context overhead

5. Apply AI judgment to determine which patterns meet the extraction criteria (see Principle Extraction Criteria)

Determine appropriate detection methods based on language and project structure.

### Step 5: Analyze Documentation

Also analyze non-code documentation:

- README.md
- CONTRIBUTING.md
- PR templates
- Existing CLAUDE.md

Extract explicit coding rules and guidelines from these documents.

### Step 6: Generate Output

1. Check if output directory exists
   - If exists and `--force` not set: Error "Output directory already exists. Use --force to overwrite."
   - If exists and `--force` set:
     - **Warning:** "Existing rules will be overwritten. Manual edits will be lost."
     - List files that will be overwritten
     - Proceed with overwrite (backup is user's responsibility via git)
   - If not exists: Create directory

2. Generate rule files:
   - `languages/<lang>.md` for language-specific rules
   - `frameworks/<framework>.md` for framework-specific rules
   - `project.md` for project-specific rules

**Rule file format (hybrid: principles + project-specific patterns):**

```markdown
---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---
# TypeScript Rules

## Principles

- Immutability (spread演算子, map/filter/reduce, const優先)
- Declarative style (命令的ループより宣言的変換)
- Type safety (strict mode, 明示的型注釈, any禁止)

## Project-specific patterns

- `RefOrNull<T extends { id: string }> = T | { id: null }` - nullable relationships
- `pathFor(page) + url()` - Page Object navigation pair
- `useAuthClient()` returns `{ user, login, logout }` - auth hook interface
```

**Format guidelines:**

For **Principles** section:
- Each principle: `Principle name (hint1, hint2, hint3)`
- 2-4 implementation hints per principle
- Only for general style choices (language built-ins)

For **Project-specific patterns** section:
- **One line per pattern**: `signature/definition` - brief context
- Use inline code for signatures, not code blocks
- Keep context to 2-5 words maximum
- Only include the minimal signature needed for AI to infer usage

**paths patterns by category:**
- TypeScript: `**/*.ts`, `**/*.tsx`
- Python: `**/*.py`
- React: `**/*.tsx`, `**/*.jsx`
- (project.md: no paths frontmatter = applies to all files)

### Step 7: Report Summary

Display analysis summary:

```markdown
## Extraction Complete

**Project**: [project name]
**Languages**: [detected languages]
**Frameworks**: [detected frameworks]
**Analyzed files**: [count]

### Generated Files

| File | Principles |
|------|------------|
| languages/typescript.md | 3 principles |
| frameworks/react.md | 2 principles |
| project.md | 2 principles |

**Output**: `<output_dir>` (default: .claude/rules/)

### Recommended Actions

1. Review generated rules and edit if needed
2. Add reference to CLAUDE.md:
   \`\`\`markdown
   ## Coding Rules
   See .claude/rules/ for project-specific coding rules.
   \`\`\`
3. Re-run with `/extract-rules --update` when codebase evolves
```

---

## Update Mode

When `--update` is specified, re-scan the codebase and add new patterns while preserving existing rules.

### Step U1: Check Prerequisites

1. Check if output directory exists (default: `.claude/rules/`)
   - If not exists: Error "Run /extract-rules first to initialize rule files."

2. Load existing rule files to understand current rules

### Step U2: Re-scan Codebase

Execute Step 1-5 from Full Extraction Mode:
- Load settings
- Detect project type
- Collect sample files
- Analyze by category
- Analyze documentation

### Step U3: Compare and Merge

For each extracted principle/pattern:

1. **Check if already exists**: Compare with existing rules
   - Exact match → Skip
   - Similar but different → Keep both (let user review)
   - New → Add

2. **Preserve manual edits**: Do not modify existing rules

### Step U4: Append New Rules

1. Append new principles to appropriate section (`## Principles`)
2. Append new project-specific patterns to appropriate section (`## Project-specific patterns`)
3. Maintain file structure and formatting

### Step U5: Report Changes

```markdown
## Update Complete

### Added to languages/typescript.md:
#### Principles
- (none)

#### Project-specific patterns
- `useNewFeature()` returns `{ data, refresh }` - new feature hook

### Added to frameworks/react.md:
- (none)

### Unchanged files:
- project.md

**Tip**: Review added rules and remove any that are incorrect or redundant.
```

---

## Conversation Extraction Mode

When `--from-conversation` is specified, extract rules from the conversation history.

### Step C1: Check Prerequisites

1. Check if output directory exists (default: `.claude/rules/`)
   - If not exists: Error "Run /extract-rules first to initialize rule files."

2. Load existing rule files to understand current rules

### Step C2: Determine Conversation Source

**Option A: Read from transcript file (preferred, full history)**

If transcript file path is known:
- Location: `~/.claude/projects/<project-path>/<session-id>.jsonl`
- Read the JSONL file (each line is a JSON object)
- Focus on `type: "user"` and `type: "assistant"` entries
- This includes ALL messages from session start (even after compaction)

**Option B: Use current context (fallback)**

If transcript path is unknown (e.g., running in Codex or other AI tools):
- Analyze the current conversation context
- Note: May have limited history if context was compacted

### Step C3: Extract Principles and Patterns

Look for user preferences and classify them (same as Full Extraction Mode):

**1. General style preferences** → Abstract to principles:
   - "Use type instead of interface" → Type safety principle
   - "Avoid mutations" → Immutability principle

**2. Project-specific patterns** → Extract with concrete examples:
   - "Use `RefOrNull<T>` for nullable refs" → Include type definition
   - "Always use `pathFor()` with `url()`" → Include usage pattern

**3. Code review feedback**: Identify underlying philosophy or specific patterns

Apply the same criteria as Full Extraction Mode (see Principle Extraction Criteria and Concrete Example Criteria).

### Step C4: Append Principles and Patterns

1. Categorize each extracted item:
   - Language-specific → `languages/<lang>.md`
   - Framework-specific → `frameworks/<framework>.md`
   - Project-specific → `project.md`

2. Check for duplicates: Skip if already exists or covered

3. Append in appropriate format:
   - Principles: `Principle name (hint1, hint2, hint3)`
   - Project-specific patterns: `signature` - brief context (one line)

4. Report what was added:
   ```markdown
   ## Extracted from Conversation

   ### Added to languages/typescript.md:
   #### Principles
   - Immutability (spread operators, map/filter, avoid mutations)

   #### Project-specific patterns
   - `RefOrNull<T extends { id: string }> = T | { id: null }` - nullable refs

   ### No changes:
   - Functional style - Already documented
   ```

---

## Important Notes

- This skill uses AI to understand intent, not just pattern matching
- Both code AND documentation are analyzed
- Use `--from-conversation` after significant discussions about coding style
- Generated rules are meant to be reviewed and refined by humans

## Principle Extraction Criteria

**Goal:** Extract abstract principles that guide AI to write code consistent with project style.

### Extract these principles

Principles where **multiple common approaches exist** and AI might choose differently without guidance:

- **Immutability vs Mutability** - AI often writes mutable code by default
- **Declarative vs Imperative** - Both are common approaches
- **Functional vs Class-based** - Both are valid paradigms
- **OOP vs FP** - Different design philosophies

### Do NOT extract these

Principles where **only one practical approach exists**:

- React components use PascalCase (no alternative)
- Python uses snake_case (language standard)
- TypeScript files use `.ts` extension

### Decision criterion

> "Would a general AI write code differently without this principle?"
> - **Yes** → Extract it
> - **No** → Skip it

### Abstraction examples

| Concrete patterns observed | Abstract principle |
|---|---|
| `const` preferred, spread operators, no mutations | Immutability (const, spread, map/filter) |
| Arrow functions, no classes, pure functions | Functional style (arrow functions, pure, no this) |
| Strict TypeScript, explicit types, no any | Type safety (strict, explicit, no any) |

## Concrete Example Criteria

**Goal:** Determine when to include concrete code examples vs abstract principles.

### Include concrete examples when

Pattern involves **project-defined symbols** that AI cannot infer:

- **Custom types/interfaces** defined in the project (not from node_modules)
- **Project-specific hooks** (e.g., `useAuthClient`, `useDataFetch`)
- **Utility functions** with non-obvious signatures
- **Non-obvious combinations** (e.g., `pathFor()` + `url()` must be used together)

**Important: Keep examples minimal**
- One line per pattern: `signature` - context (2-5 words)
- Include only the type signature or function signature
- Omit implementation details, only show the "shape" AI needs to know

### Keep abstract (principles only) when

Pattern uses only **language built-ins** or **well-known patterns**:

- `const`, `let`, spread operators, map/filter/reduce
- Standard design patterns with well-known implementations
- Framework APIs documented in official docs

### Decision criterion

> "Can AI correctly implement this pattern by knowing only its name?"
> - **Yes** → Abstract principle with hints
> - **No** → Include concrete example

### Example classification

| Pattern | Classification | Reason |
|---------|---------------|--------|
| Prefer `const` over `let` | Principle only | Language built-in, AI knows this |
| `RefOrNull<T>` type usage | Concrete example | Project-defined type, AI cannot infer |
| Page Object Model | Principle + hints | Well-known pattern |
| `pathFor()` + `url()` combination | Concrete example | Project-specific API combination |

### Gray zone handling

For patterns that are **not clearly general or project-specific**:

- Extended types from node_modules (e.g., `type MyUser = User & { custom: string }`)
- Specific combinations of standard libraries (e.g., zod + react-hook-form patterns)

**Fallback rule: When uncertain, include a concrete example.**

Rationale: Over-specifying is less harmful than under-specifying. An unnecessary example adds minimal context overhead, but a missing example may cause AI to guess incorrectly.

## Security Considerations

**Sensitive Information Protection:**

- `git ls-files` only analyzes tracked files, automatically excluding untracked `.env`, credentials, and other gitignored files
- **Warning:** If `.env` or credential files are accidentally tracked in git, they WILL be included in analysis
- Hardcoded secrets in source code may appear in examples
- When generating rule files, avoid including:
  - API keys, tokens, or credentials found in code
  - Internal URLs or endpoints
  - Customer names or personal information
  - High-entropy strings that may be secrets
- If sensitive information is detected in samples, redact with placeholders (e.g., `API_KEY_REDACTED`)
- Review generated rule files before committing to repository
- **Conversation extraction:** Same rules apply - do not extract sensitive information from conversation history (API keys, credentials, internal URLs mentioned in chat)
