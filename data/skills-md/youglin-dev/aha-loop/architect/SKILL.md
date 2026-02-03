---
name: architect
description: "Designs system architecture and selects technology stack based on vision analysis. Use after vision analysis for technical decisions. Triggers on: design architecture, select tech stack, choose framework."
---

# Architect Skill

Research, evaluate, and decide on technology stack and system architecture based on project requirements.

## Workspace Mode Note

When running in workspace mode, all paths are relative to `.aha-loop/` directory:
- Vision analysis: `.aha-loop/project.vision-analysis.md`
- Architecture output: `.aha-loop/project.architecture.md`

The orchestrator will provide the actual paths in the prompt context.

---

## The Job

1. Read `project.vision-analysis.md` for requirements
2. Research candidate technologies for each layer
3. Evaluate and compare options
4. Make decisions with documented rationale
5. Design system architecture
6. Output `project.architecture.md`

---

## Core Principles

### 1. Prefer Latest Stable Versions

**Always use the latest stable version of libraries unless there's a specific reason not to.**

```markdown
## Version Selection Process

1. Query official source for latest version:
   - Rust: crates.io API or `cargo search`
   - Node: npmjs.com or `npm view [pkg] version`
   - Python: pypi.org or `pip index versions`

2. Check release date and stability:
   - Released > 2 weeks ago (not bleeding edge)
   - No critical issues in GitHub issues
   - Changelog shows no breaking changes from common patterns

3. Document the version and why:
   - Record in project.architecture.md
   - Add to knowledge/project/decisions.md
```

### 2. Consider Long-term Maintenance

- Active community and regular updates
- Good documentation
- Large ecosystem of plugins/extensions
- Backed by reputable organization or strong community

### 3. Evaluate Total Cost

- Learning curve for the team/AI
- Bundle size / binary size
- Runtime performance
- Development velocity

---

## Research Process

### Step 1: Identify Technology Layers

Based on project type, identify which layers need decisions:

| Layer | Examples |
|-------|----------|
| **Language** | Rust, TypeScript, Python, Go |
| **Frontend Framework** | React, Vue, Svelte, SolidJS |
| **Backend Framework** | Axum, Actix, Express, FastAPI |
| **Database** | PostgreSQL, SQLite, MongoDB |
| **ORM/Query Builder** | Diesel, SQLx, Prisma, Drizzle |
| **Authentication** | JWT, Sessions, OAuth providers |
| **Deployment** | Docker, Serverless, VPS |
| **Testing** | Built-in, Jest, Pytest, Vitest |

### Step 2: Research Each Layer

For each layer requiring a decision:

1. **Identify 2-4 candidates** - Don't over-research
2. **Fetch source code** if needed for deep understanding
3. **Check latest versions** - Use web search or package registry
4. **Read documentation** - Understand core concepts
5. **Compare tradeoffs** - Performance, DX, ecosystem

### Step 3: Use Structured Comparison

```markdown
## [Layer Name] Decision

### Candidates

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Latest Version | v1.2.3 | v2.0.0 | v0.9.0 |
| Release Date | 2026-01-15 | 2026-01-20 | 2025-12-01 |
| GitHub Stars | 45k | 30k | 15k |
| Bundle Size | 50kb | 80kb | 30kb |
| Learning Curve | Medium | Low | High |
| Documentation | Excellent | Good | Fair |
| TypeScript Support | Native | Via types | Partial |
| Community Activity | Very Active | Active | Moderate |

### Decision: [Option B]

### Rationale
- [Reason 1]
- [Reason 2]
- [Reason 3]

### Tradeoffs Accepted
- [What we're giving up]
- [Mitigation strategy if any]
```

### Step 4: Check Compatibility

Before finalizing:

- Verify all chosen technologies work together
- Check for known integration issues
- Ensure versions are compatible
- Test with a minimal proof-of-concept if uncertain

---

## Version Research Commands

### Rust (crates.io)

```bash
# Get latest version
curl -s "https://crates.io/api/v1/crates/tokio" | jq '.crate.max_stable_version'

# Or use cargo
cargo search tokio --limit 1
```

### Node.js (npm)

```bash
# Get latest version
npm view react version

# Get all versions
npm view react versions --json
```

### Check GitHub for Activity

```bash
# Using gh CLI
gh api repos/tokio-rs/tokio --jq '.pushed_at, .stargazers_count'
```

---

## Architecture Design

After technology decisions, design the architecture:

### 1. Component Diagram

```markdown
## System Components

[Component A] --> [Component B] --> [Component C]
       |                               |
       v                               v
  [Database]                    [External API]
```

### 2. Data Flow

Document how data flows through the system:
- User inputs
- Processing steps
- Storage points
- Output paths

### 3. Directory Structure

Propose the project structure:

```
project/
├── src/
│   ├── main.rs
│   ├── api/
│   ├── db/
│   └── ...
├── tests/
├── Cargo.toml
└── ...
```

### 4. Key Patterns

Document architectural patterns to follow:
- Error handling approach
- Logging strategy
- Configuration management
- Testing approach

---

## Output: project.architecture.md

```markdown
# Project Architecture

**Generated:** [timestamp]
**Based on:** project.vision-analysis.md

## Technology Stack

### Core Technologies

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Language | Rust | 1.75 | Performance, safety |
| Web Framework | Axum | 0.7.4 | Ergonomic, async |
| Database | SQLite | 3.45 | Simple, embedded |
| ORM | SQLx | 0.7.3 | Compile-time checks |

### Development Tools

| Tool | Version | Purpose |
|------|---------|---------|
| cargo-watch | 8.5.2 | Auto-rebuild |
| sqlx-cli | 0.7.3 | Migrations |

## Architecture Decisions

### ADR-001: [Decision Title]

**Context:** [Why this decision was needed]
**Decision:** [What was decided]
**Rationale:** [Why this option]
**Consequences:** [Impact of decision]

### ADR-002: ...

## System Design

### Component Overview

[Diagram or description]

### Data Flow

[How data moves through system]

### Directory Structure

```
[Proposed structure]
```

## Key Patterns

### Error Handling
[Approach]

### Configuration
[Approach]

### Testing Strategy
[Approach]

## Dependencies

### Production Dependencies

```toml
[dependencies]
axum = "0.7.4"
tokio = { version = "1.35", features = ["full"] }
sqlx = { version = "0.7.3", features = ["sqlite", "runtime-tokio"] }
```

### Development Dependencies

```toml
[dev-dependencies]
```

## Security Considerations

- [Security item 1]
- [Security item 2]

## Performance Considerations

- [Performance item 1]
- [Performance item 2]

## Deployment Strategy

[How the project will be deployed]

## Next Steps

1. Initialize project structure
2. Set up CI/CD
3. Begin roadmap planning
```

---

## Integration with Orchestrator

After architecture design:

1. Save `project.architecture.md` to project root
2. Update `knowledge/project/decisions.md` with ADRs
3. Signal completion to orchestrator
4. Roadmap Skill uses architecture as input

---

## Checklist

Before completing architecture:

- [ ] All technology layers evaluated
- [ ] Latest stable versions verified for each choice
- [ ] Compatibility between choices confirmed
- [ ] Decisions documented with rationale
- [ ] Directory structure proposed
- [ ] Key patterns defined
- [ ] Dependencies listed with versions
- [ ] ADRs recorded in knowledge/project/decisions.md
- [ ] Architecture saved to `project.architecture.md`

---

## Example: Web App Architecture

**Input:** Vision analysis showing PWA finance tracker

**Output:**

```markdown
# Project Architecture

## Technology Stack

### Core Technologies

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Language | TypeScript | 5.3.3 | Type safety, ecosystem |
| Framework | SvelteKit | 2.5.0 | Fast, simple, SSR+SPA |
| Styling | Tailwind CSS | 3.4.1 | Utility-first, fast |
| Database | IndexedDB (Dexie) | 4.0.1 | Offline-first PWA |
| Build | Vite | 5.0.12 | Fast, modern |

### PWA Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Service Worker | Workbox | 7.0.0 |
| Manifest | Vite PWA Plugin | 0.17.4 |

## Architecture Decisions

### ADR-001: SvelteKit over React/Next.js

**Context:** Need a modern frontend framework for PWA
**Decision:** Use SvelteKit 2.x
**Rationale:**
- Smaller bundle size (critical for PWA)
- Built-in SSR and static generation
- Simpler mental model than React
- Excellent TypeScript support
**Consequences:** Smaller community than React, but sufficient for this project.

### ADR-002: Dexie for IndexedDB

**Context:** Need offline data storage
**Decision:** Use Dexie.js 4.x wrapper for IndexedDB
**Rationale:**
- Promise-based API
- Excellent TypeScript support
- Reactive queries
- Well-maintained
**Consequences:** Additional 30kb bundle, but worth the DX improvement.
```
