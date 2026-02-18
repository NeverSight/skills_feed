---
name: project-profiler
version: 2.0.0
description: |
  Generate an LLM-optimized project profile for any git repository.
  Outputs docs/{project-name}.md covering architecture, core abstractions,
  usage guide, design decisions, and recommendations.
  Trigger: "/project-profiler", "profile this project", "為專案建側寫"
user_invocable: true
argument_hint: "[target directory, default .]"
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash, Task, WebSearch, WebFetch]
---

# project-profiler

Generate an **LLM-optimized project profile** — a judgment-rich document that lets any future LLM answer within 60 seconds:

1. **What are the core abstractions?**
2. **Which modules to modify for feature X?**
3. **What is the biggest risk/debt?**
4. **When should / shouldn't you use this?**

This is NOT a codebase map (directory + module navigation) or a diff schematic. This is **architectural judgment**: design tradeoffs, usage patterns, and when NOT to use.

---

## Model Strategy

- **Opus**: Orchestrator — runs all phases, writes the final profile. Does NOT read source code directly (except in direct mode).
- **Sonnet**: Subagents — read source code files, analyze patterns, report structured findings.
- All subagents launch in a **single message** (parallel, never sequential).

---

## Phase 0: Preflight

### 0.1 Target & Project Name

Determine the target directory (use argument if provided, else `.`).

Extract project name from the first available source:
1. `package.json` → `name`
2. `pyproject.toml` → `[project] name`
3. `Cargo.toml` → `[package] name`
4. `go.mod` → module path (last segment)
5. Directory name as fallback

### 0.2 Run Scanner

```bash
uv run {SKILL_DIR}/scripts/scan-project.py {TARGET_DIR} --format summary
```

Capture the summary output. This provides:
- Project metadata (name, version, license, deps count)
- Tech stack (languages, frameworks, package manager)
- Language distribution (top 5 by tokens)
- Entry points (CLI, API, library)
- Project features (dockerfile, CI, tests, codebase_map)
- **Detected conditional sections** (Storage, Embedding, Infrastructure, etc.)
- **Workspaces** (monorepo packages, if any)
- Top 20 largest files
- Directory structure (depth 3)

For debugging or when full file details are needed, use `--format json` instead.

### 0.3 Git Metadata

Run these commands (use Bash tool):

```bash
# Recent commits
git -C {TARGET_DIR} log --oneline -20

# Contributors
git -C {TARGET_DIR} log --format="%aN" | sort -u | head -20

# Version tags
git -C {TARGET_DIR} tag --sort=-v:refname | head -5

# First commit date
git -C {TARGET_DIR} log --format="%aI" --reverse | head -1
```

### 0.4 Check Existing CODEBASE_MAP

If `docs/CODEBASE_MAP.md` exists, note its presence. The profile will reference it rather than duplicating directory structure.

### 0.5 Token Budget → Execution Mode

Based on `total_tokens` from scanner, choose execution mode:

| Total Tokens | Mode | Strategy |
|-------------|------|----------|
| **≤ 80k** | **Direct** | **Skip subagents. Opus reads all files directly and performs all analysis in a single context.** |
| 80k – 200k | 2 agents | Agent AB (Core + Architecture + Design), Agent C (Usage + Patterns + Deployment) |
| 200k – 400k | 3 agents | Agent A (Core + Design), Agent B (Architecture + Patterns), Agent C (Usage + Deployment) |
| > 400k | 3 agents | Agent A, Agent B, Agent C — each ≤150k tokens, with overflow files assigned to lightest agent |

**Why 80k threshold**: Opus has 200k context. At ≤80k source tokens, loading all files + scanner output + git metadata + writing the profile all fit comfortably. Subagent overhead (spawn + communication + wait) adds 2-3 minutes for zero benefit.

**Direct mode workflow**: Skip Phase 2 entirely. After Phase 0+1, proceed to Phase 3 (read scanner `detected_sections` directly), then Phase 4, then Phase 5. Read files on-demand during synthesis — do NOT pre-read all files; read only what's needed for each section.

---

## Phase 1: Community & External Data

> Run in parallel with Phase 2 subagent launches (or with Phase 3 in direct mode).

### 1.1 GitHub Stats

Parse owner/repo from `.git/config` remote origin URL:

```bash
git -C {TARGET_DIR} remote get-url origin
```

Extract `owner/repo` from the URL. Then:

```bash
gh api repos/{owner}/{repo} --jq '{stars: .stargazers_count, forks: .forks_count, open_issues: .open_issues_count}'
```

If `gh` is unavailable or not a GitHub repo → fill with `N/A`. Do not fail.

### 1.2 Package Downloads

**npm** (if `package.json` exists):
```
WebFetch https://api.npmjs.org/downloads/point/last-month/{package_name}
```

**PyPI** (if `pyproject.toml` exists):
```
WebFetch https://pypistats.org/api/packages/{package_name}/recent
```

If fetch fails → fill with `N/A`.

### 1.3 License

Read from (in order): LICENSE file → package metadata field → `N/A`.

### 1.4 Maturity Assessment

Calculate from:
- **Git history length**: first commit date → now
- **Release count**: number of version tags
- **Contributor count**: unique authors

| Criteria | Score |
|----------|-------|
| < 3 months, < 3 releases, 1-2 contributors | experimental |
| 3-12 months, 3-10 releases, 2-5 contributors | growing |
| 1-3 years, 10-50 releases, 5-20 contributors | stable |
| > 3 years, > 50 releases, > 20 contributors | mature |

Use the **lowest** matching tier (conservative estimate).

---

## Phase 2: Parallel Deep Exploration

> **Direct mode (≤80k tokens): SKIP this entire phase.** Proceed to Phase 3. Opus reads files directly during synthesis.

Launch Sonnet subagents using the `Task` tool. **All subagents must be launched in a single message.**

Assign files to each agent based on the token budget from Phase 0.5. Use the scanner output to determine which files go to which agent.

### File Assignment Strategy

**If workspaces detected** (monorepo):
1. Group files by workspace package
2. Assign complete packages to agents (never split a package across agents)
3. Agent A gets packages with core business logic
4. Agent B gets packages with infrastructure/shared libraries
5. Agent C gets packages with CLI/API/SDK surface + docs

**If no workspaces** (single project):
1. Sort all files by path
2. Group by top-level directory
3. Assign groups to agents based on their responsibility:
   - Agent A gets: core source files (src/lib, core/, models/, types/) + README, CHANGELOG
   - Agent B gets: architecture files (routes/, middleware/, config/, entry points) + tests/
   - Agent C gets: integration files (API, CLI, SDK, examples/, docs/) + .github/
4. If files don't fit neatly, distribute remaining to agents under budget

### Agent A: Core Abstractions + Design Decisions

```
Task prompt for Agent A — subagent_type: "general-purpose", model: "sonnet"

## Mission
Identify the most architecturally significant abstractions AND key design decisions in this codebase.

## Files to Read
{LIST_OF_ASSIGNED_FILES}
Also read: README.md, CHANGELOG.md (if they exist and not already assigned)

## Output Format

### Part 1: Core Abstractions
Report the TOP 10-15 most architecturally significant abstractions, ranked by fan-in (how many other files reference them). If the project has fewer than 15 meaningful abstractions, report all.

For EACH abstraction:

#### {Name}
- **Purpose**: {≤15 words}
- **Defined in**: `{file_path}:ClassName` or `{file_path}:function_name`
- **Type**: {class / interface / type / trait / struct / protocol}
- **Public methods/fields**: {exact_count}
- **Adapters/implementations**: {count} — {names with file paths}
- **Imported by**: {count} files
- **Key pattern**: {factory / singleton / strategy / observer / none}

### Part 2: Design Decisions
For EACH decision (identify 3-5):

#### {Decision Title}
- **Problem**: {what needed solving}
- **Choice made**: {what was chosen}
- **Evidence**: `{file_path}:ClassName` or `{file_path}:function_name` — {relevant code pattern}
- **Alternatives NOT chosen**: {what else could have been done}
- **Why not**: {concrete reason — performance / complexity / ecosystem / team preference}
- **Tradeoff**: {what is gained} vs. {what is lost}

### Part 3: Architecture Risks
For EACH risk (identify 2-4):
- **Risk**: {specific description}
- **Location**: `{file_path}:SymbolName`
- **Impact**: {what breaks if this goes wrong}
- **Mitigation**: {how to fix or reduce risk}

### Part 4: Recommendations
For EACH recommendation (identify 2-4):
- **Current state**: `{file_path}` — {what exists now}
- **Problem**: {specific issue — not "could be better"}
- **Fix**: {concrete action — not "consider refactoring"}
- **Effect**: {measurable outcome}

## Rules
- Every number must come from actual code (count imports, count methods)
- No subjective language (no "well-designed", "elegant", "robust", "clean", "優雅", "完美", "強大")
- Every claim needs a `file:SymbolName` reference (NOT line numbers — they break on next commit)
- Each decision must have a "why NOT the alternative" answer
- Report the TOTAL count of abstractions found
```

### Agent B: Architecture + Code Quality Patterns

```
Task prompt for Agent B — subagent_type: "general-purpose", model: "sonnet"

## Mission
Map the system topology, layer boundaries, data flow paths, AND code quality patterns.

## Files to Read
{LIST_OF_ASSIGNED_FILES}

## Output Format

### Part 1: Topology
- **Architecture style**: {monolith / microservices / serverless / library / CLI tool / plugin system}
- **Entry points**: {list with file paths}
- **Layer count**: {N}

### Part 2: Layers (table)
| Layer | Modules | Files | Responsibility |
|-------|---------|-------|---------------|

### Part 3: Data Flow Paths
For each major user-facing operation:
1. **{Operation name}**: {step1_module} → {step2_module} → ... → {result}
   - Evidence: `{file:SymbolName}` for each step

### Part 4: Mermaid Diagram Elements
Provide raw data for Mermaid diagrams:
- Nodes: {module_name} — {file_path}
- Edges: {from} → {to} — {relationship_type: imports/calls/extends}

### Part 5: Module Dependencies (structured)
For each module:
- **{module_name}** (`{path}`): imports [{dep1}, {dep2}, ...]

### Part 6: Boundary Violations
List any cases where a lower layer imports from a higher layer.

### Part 7: Code Quality Patterns
- **Error handling**: {strategy and consistency — e.g., "try/catch at controller layer, custom AppError class"}
- **Logging**: {framework and coverage — e.g., "winston, structured JSON, covers all API routes"}
- **Testing**: {framework, coverage level, patterns — e.g., "vitest, 47 test files, unit + integration"}
- **Type safety**: {strict / partial / none — e.g., "strict TypeScript with no `any` casts"}

## Rules
- Every number must come from actual code
- No subjective language (no "well-designed", "elegant", "robust", "clean", "優雅", "完美", "強大")
- Every claim needs a `file:SymbolName` reference (NOT line numbers)
- Focus on HOW data moves, not WHAT the code does
```

### Agent C: Usage + Deployment + Security

```
Task prompt for Agent C — subagent_type: "general-purpose", model: "sonnet"

## Mission
Document all consumption interfaces, deployment modes, security surface, and AI agent integration points.

## Files to Read
{LIST_OF_ASSIGNED_FILES}

## Output Format

### Part 1: Consumption Interfaces
For each interface found:
- **Type**: {Python SDK / TS SDK / REST API / MCP / CLI / Vercel AI SDK / Library import}
- **Entry point**: `{file_path}:ClassName` or `{file_path}:function_name`
- **Public surface**: {N} exported functions/classes/endpoints
- **Example usage**: {minimal code snippet from docs/examples or inferred from exports}

### Part 2: Configuration
| Source | Path | Key Settings |
|--------|------|-------------|

### Part 3: Deployment Modes
| Mode | Evidence | Prerequisites |
|------|----------|--------------|

### Part 4: AI Agent Integration
- **MCP tools**: {count and names, if any}
- **Function calling schemas**: {count, if any}
- **Tool definitions**: {count, if any}
- **SDK integration**: {Vercel AI SDK / LangChain / LlamaIndex / custom}

### Part 5: Security Surface
- **API key handling**: {how and where}
- **Auth mechanism**: {type and file}
- **CORS config**: {if applicable}
- **Data at rest**: {encrypted / plaintext / N/A}
- **PII handling**: {anonymized / logged / none detected}

### Part 6: Performance & Cost Indicators
| Metric | Value | Source |
|--------|-------|--------|
| {LLM calls per request} | {N} | `{file:SymbolName}` |
| {Cache strategy} | {type} | `{file:SymbolName}` |
| {Rate limiting} | {config} | `{file:SymbolName}` |

## Rules
- Every number must come from actual code
- No subjective language (no "well-designed", "elegant", "robust", "clean", "優雅", "完美", "強大")
- Every claim needs a `file:SymbolName` reference (NOT line numbers)
- Include BOTH documented and undocumented interfaces
```

---

## Phase 3: Conditional Section Detection

Read the scanner's `detected_sections` output from Phase 0.2. This is the **primary** detection source — the scanner checks dependency manifests and file presence automatically.

**Cross-reference** with subagent reports (skip in direct mode) for additional evidence richness. If a subagent reports a pattern not caught by the scanner (e.g., concurrency via raw `Promise.all` without a library dependency), add it.

Refer to `references/section-detection-rules.md` for the full pattern reference.

Record results as a checklist:
```
- [x] Storage Layer — scanner detected: prisma in dependencies
- [ ] Embedding Pipeline — not detected
- [x] Infrastructure Layer — scanner detected: Dockerfile present
- [ ] Knowledge Graph — not detected
- [ ] Scalability — not detected
- [x] Concurrency — Agent B reported: Promise.all pattern in src/worker.ts
```

---

## Phase 4: Synthesis & Draft

### 4.1 Merge Reports

**Subagent mode**: Combine all subagent outputs into a working document.
**Direct mode**: Read key files on-demand as you write each section. Do NOT pre-read all files. For each section, read only the files relevant to that section's analysis.

Cross-validate:
- Core abstractions ↔ Architecture layers: each abstraction belongs to a layer
- Architecture data flow ↔ Usage interfaces: flows end at documented interfaces
- Design decisions ↔ Code evidence: decisions are backed by found patterns

### 4.2 Generate Mermaid Diagrams + Structured Dependencies

Using Agent B's raw data (or direct file analysis in direct mode), create:

**Architecture Topology** (`graph TB`):
- Each node = actual module/directory
- Each edge = import/dependency relationship
- Label edges with relationship type
- Group nodes by layer using subgraph

**Data Flow** (`sequenceDiagram`):
- Each participant = actual module
- Each arrow = actual function call or event
- Cover the primary user-facing operation

**Structured Module Dependencies** (text, below each Mermaid diagram):
- Provide a machine-parseable dependency list as fallback for LLM readers
- Format: `- **{module_name}** (\`{path}\`): imports [{dep1}, {dep2}, ...]`

### 4.3 Fill Output Template

Follow `references/output-template.md` exactly. Fill each section:

| Section | Primary Source | Secondary Source |
|---------|---------------|-----------------|
| 1. Project Identity | Scanner metadata + Phase 1 | Git metadata |
| 2. Architecture | Agent B (Parts 1-6) | Agent A (abstractions per layer) |
| 3. Core Abstractions | Agent A (Part 1) | Agent B (layer context) |
| 4. Conditional | Phase 3 detection + relevant agents | — |
| 5. Usage Guide | Agent C (Parts 1-4) | Scanner entry_points |
| 6. Performance & Cost | Agent C (Part 6) + Agent B | — |
| 7. Security & Privacy | Agent C (Part 5) | — |
| 8. Design Decisions | Agent A (Part 2) | Agent B (architecture context) |
| 8.5 Code Quality & Patterns | Agent B (Part 7) | Agent A (supporting observations) |
| 9. Recommendations | Agent A (Part 4) | Agents B/C (supporting evidence) |

### 4.4 Write Output

Write the profile to `docs/{project-name}.md` using the Write tool.

---

## Phase 5: Quality Gate

Read `references/quality-checklist.md` and verify the output.

### 5.1 Banned Language Scan

Search the written file for any word from the banned list:

**English:**
```
well-designed, elegant, elegantly, robust, clean, impressive,
state-of-the-art, cutting-edge, best-in-class, beautifully,
carefully crafted, thoughtfully, well-thought-out, well-architected,
nicely, cleverly, sophisticated, powerful, seamless, seamlessly,
intuitive, intuitively
```

**Chinese:**
```
優雅、完美、強大、直觀、無縫、精心、巧妙、出色、卓越、先進、高效、靈活、穩健、簡潔
```

If found → replace with verifiable descriptions and re-write.

### 5.2 Number Audit

Scan for all numeric claims. Each must have a traceable source.
Remove or fix any "approximately", "around", "roughly", "several", "many", "numerous".

### 5.3 Structure Verification

- [ ] Every `##` section starts with `>` blockquote summary
- [ ] No directory tree duplicated from CODEBASE_MAP.md
- [ ] No file extension enumeration (use percentages)
- [ ] No generic concluding paragraph
- [ ] At least one Mermaid diagram in Architecture section
- [ ] Structured module dependency list below each Mermaid diagram
- [ ] All Mermaid nodes reference actual modules

### 5.4 Core Question Test

For each of the 4 core questions, locate the specific answer in the output:
1. Core abstractions → Section 3
2. Module to modify → Section 2 Layer Boundaries table
3. Biggest risk → Section 9 first recommendation
4. When to use/not use → Section 1 positioning line

### 5.5 Evidence Audit

- Section 3: every abstraction has `file:SymbolName` reference
- Section 8: every decision has `file:SymbolName` + alternative + tradeoff
- Section 8.5: code quality patterns have framework names + coverage facts
- Section 9: every recommendation has `file_path` + specific problem + concrete fix

If any check fails → fix the issue in the file and re-verify.

---

## Output

After all phases complete, report to the user:

```
Profile generated: docs/{project-name}.md
- {total_files} files scanned ({total_tokens} tokens)
- {N} core abstractions identified
- {N} design decisions documented
- {N} recommendations
- Conditional sections: {list of included sections or "none"}
```
