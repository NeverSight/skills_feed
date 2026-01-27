---
name: multi-ai-research
description: Comprehensive research and analysis using Claude (subagents), Gemini CLI, and Codex CLI. Multi-perspective research with cross-verification, iterative refinement, and 100% citation coverage. Use for security analysis, architecture research, code quality assessment, performance analysis, or any research requiring rigorous verification and multiple AI perspectives.
allowed-tools: Task, Bash, Read, Grep, Glob, Write
---

# Multi-AI Research & Analysis

## Overview

Harnesses three AI systems (Claude via Task tool, Gemini CLI, Codex CLI) for comprehensive research and analysis with multi-perspective verification and iterative refinement.

**Purpose**: Produce analysis more thorough than any single AI could achieve through specialized roles, cross-validation, and systematic verification.

**Key Innovation**: Not just parallel execution - specialized research roles with cross-verification and iterative refinement until production-ready (quality ≥95/100, 100% citations, zero gaps).

**The 3 AI Systems**:
1. **Claude Subagents** (via Task tool) - Documentation, codebase analysis, synthesis
2. **Gemini CLI** - Web research, latest trends, community practices
3. **Codex CLI** - GitHub patterns, code examples, deep reasoning

**Quality Guarantees**:
- ✓ **100% coverage** - All objectives addressed, zero gaps
- ✓ **100% citations** - Every claim sourced (file:line or URL)
- ✓ **Multi-perspective** - 3 AI systems cross-validated
- ✓ **≥95/100 quality** - Verified through 3-pass system
- ✓ **Actionable** - Specific recommendations with examples
- ✓ **Resumable** - External memory enables multi-session work

---

## When to Use

Use this skill for:

### Security Analysis
- Authentication/authorization assessment
- Vulnerability identification
- Best practice validation
- OWASP Top 10 coverage
- Penetration testing preparation

### Architecture Analysis
- System design review
- Component mapping
- Integration pattern analysis
- Scalability assessment
- Technical debt evaluation

### Code Quality Analysis
- Pattern detection
- Code smell identification
- Complexity metrics
- Refactoring opportunities
- Best practice adherence

### Performance Analysis
- Bottleneck identification
- Algorithm complexity
- Resource usage patterns
- Optimization opportunities
- Benchmark analysis

### Research Synthesis
- Multi-source research compilation
- Best practice identification
- Technology evaluation
- Pattern discovery
- Trend analysis

### Comprehensive Reviews
- Pre-production audit
- System health check
- Compliance verification
- Documentation audit
- Knowledge transfer

---

## Quick Start

### Option 1: Automated Script

```bash
# Run complete analysis automatically
bash .claude/skills/multi-ai-research/scripts/analyze.sh "Security analysis of authentication system"
```

This will:
1. Create analysis plan
2. Launch parallel research (Claude + Gemini + Codex)
3. Perform deep analysis
4. Synthesize and verify
5. Iterate if needed
6. Generate final report

### Option 2: Interactive Mode

Ask Claude Code to use this skill:

```
"Use multi-ai-research to analyze [objective]"
```

Claude will:
1. Create comprehensive analysis plan
2. Coordinate all three AI systems
3. Synthesize findings
4. Verify quality
5. Iterate until ≥95 quality
6. Deliver final report

---

## The 5-Phase Pipeline

### Phase 1: Planning & Strategy
**Duration**: 5-10 minutes
**Output**: `.analysis/ANALYSIS_PLAN.md`

Claude creates comprehensive plan:
- Defines objectives and scope
- Plans file reading strategy (glob → grep → read)
- Assigns tasks to AI systems
- Sets verification criteria
- Defines success thresholds

### Phase 2: Parallel Research
**Duration**: 10-20 minutes
**Output**: `.analysis/research/*.md`

All three systems research simultaneously:

**Claude Subagent**:
- Official documentation analysis
- Codebase examination (progressive disclosure)
- Architecture mapping
- Pattern identification

**Gemini CLI**:
- Web research (latest 2024-2025)
- Community best practices
- Industry trends
- Common pitfalls

**Codex CLI**:
- GitHub pattern analysis
- Code examples from top repos
- Implementation references
- Testing strategies

### Phase 3: Deep Analysis
**Duration**: 15-30 minutes
**Output**: `.analysis/analysis/code-patterns.md`

Claude Analysis Agent with extended thinking:
- Progressive codebase analysis
- Pattern recognition across sources
- Architecture mapping
- Metrics calculation
- Risk assessment

### Phase 4: Synthesis & Verification
**Duration**: 10-20 minutes
**Outputs**:
- `.analysis/SYNTHESIS_REPORT.md`
- `.analysis/verification/cross-check.md`

**Synthesis** (Claude with extended thinking):
- Read all research findings
- Identify themes across sources
- Resolve contradictions
- Create unified narrative
- Full citations

**Verification** (Verification Subagent):
- 3-pass verification (completeness, accuracy, quality)
- Cross-source validation
- Citation checking
- Gap analysis
- Quality scoring

### Phase 5: Iteration (if needed)
**Duration**: 10-30 minutes
**Output**: `.analysis/iterations/ITERATION_2.md`

If quality <95 or gaps exist:
- Targeted research for gaps
- Quality improvements
- Re-verification
- Repeat until ≥95

### Phase 6: Final Report
**Duration**: 5-10 minutes
**Output**: `.analysis/ANALYSIS_FINAL.md`

Comprehensive final report:
- Executive summary
- Complete findings
- All sources synthesized
- Prioritized recommendations
- Implementation guidance
- Full citations

**Total Time**: 45-90 minutes for comprehensive analysis

---

## Analysis Types

### Security Analysis

**What it checks**:
- Authentication/authorization patterns
- Input validation
- Secret management
- Injection vulnerabilities (SQL, XSS, etc.)
- Dependency vulnerabilities
- Rate limiting
- Session security

**Example**:
```
Use multi-ai-research for "Security audit of authentication system"
```

**Output**:
- Critical/High/Medium/Low priority issues
- OWASP Top 10 coverage
- Code examples with file:line
- Specific remediation steps
- Industry best practices comparison

### Architecture Analysis

**What it examines**:
- System components and boundaries
- Integration patterns
- Data flow
- Dependency relationships
- Scalability considerations
- Design patterns used

**Example**:
```
Use multi-ai-research for "Architecture analysis of microservices system"
```

**Output**:
- Component map with relationships
- Integration pattern analysis
- Scalability assessment
- Technical debt identification
- Refactoring recommendations

### Code Quality Analysis

**What it analyzes**:
- Code patterns and organization
- Complexity metrics
- Code smells
- Best practice adherence
- Test coverage
- Documentation quality

**Example**:
```
Use multi-ai-research for "Code quality assessment for ./src"
```

**Output**:
- Quality score with breakdown
- Pattern analysis
- Refactoring priorities
- Specific code improvements
- Complexity hotspots

### Performance Analysis

**What it identifies**:
- Algorithm complexity
- Bottlenecks
- Resource usage patterns
- Database query efficiency
- Network call patterns

**Example**:
```
Use multi-ai-research for "Performance bottleneck identification"
```

**Output**:
- Bottleneck analysis with file:line
- Optimization opportunities
- Before/after estimations
- Implementation guidance

### Research Synthesis

**What it compiles**:
- Official documentation
- Web best practices
- GitHub patterns
- Industry standards
- Community insights

**Example**:
```
Use multi-ai-research for "Research GraphQL federation patterns 2024-2025"
```

**Output**:
- Multi-source synthesis
- Consensus findings (all sources agree)
- Multiple perspectives (sources differ)
- Code examples
- Implementation recommendations

---

## How It Works

### Progressive Disclosure

**Never reads files blindly**. Always uses 3-level approach:

**Level 1: Metadata (glob)** - ~50 tokens
```bash
glob "**/*.{ts,js,py}"     # Understand structure
glob "**/*.md"             # Find documentation
glob "**/package.json"     # Check dependencies
```

**Level 2: Patterns (grep)** - ~5k tokens
```bash
grep "export class|interface" --glob "**/*.ts"
grep "TODO|FIXME|BUG" --glob "**/*"
grep "password|secret|token" --glob "**/*.ts"
```

**Level 3: Reading (read)** - ~50k tokens
```bash
read "src/auth/login.ts"   # Only critical files
read "docs/architecture.md"
```

**Result**: 90%+ reduction in unnecessary file reads

### External Memory Architecture

All state saved to files, not context:

```
.analysis/
├── ANALYSIS_PLAN.md           # Strategy and assignments
├── research/
│   ├── claude-docs.md         # Claude research
│   ├── gemini-web.md          # Gemini research
│   └── codex-github.md        # Codex research
├── analysis/
│   ├── code-patterns.md       # Pattern analysis
│   └── architecture-map.md    # System map
├── verification/
│   └── cross-check.md         # Verification results
├── iterations/
│   ├── ITERATION_1.md         # First pass
│   └── ITERATION_2.md         # Gap fills
└── ANALYSIS_FINAL.md          # Complete report
```

**Benefits**:
- Survives context window limits
- Enables multi-session analysis
- Resumable from any checkpoint
- No information loss

### Cross-Validation Pattern

**High Confidence** (★★★★★): All 3 sources agree + code verification
**Medium Confidence** (★★★☆☆): 2/3 sources agree
**Requires Investigation** (★★☆☆☆): Sources conflict

**Example**:
```markdown
## JWT Implementation (High Confidence ★★★★★)

**Claude**: "Uses JWT with HS256" (src/auth/jwt.ts:15)
**Gemini**: "HS256 is industry standard 2024" (URL)
**Codex**: "150+ repos use HS256 pattern" (GitHub)
**Code**: Verified at src/auth/jwt.ts:18-22

**Recommendation**: Implementation correct per standards
```

### Quality Scoring

**Comprehensive rubric** (0-100):
- **Comprehensiveness** (/20): All aspects covered
- **Accuracy** (/20): All claims sourced and verified
- **Specificity** (/20): File:line precision, not vague
- **Actionability** (/20): Specific recommendations
- **Consistency** (/20): No contradictions

**Quality Gates**:
- ≥95: Production-ready
- 85-94: Needs minor refinement
- 75-84: Needs iteration
- <75: Requires rework

### Iterative Refinement

**Iteration 1** (Breadth): Broad coverage, identifies gaps
**Iteration 2** (Depth): Fill gaps, improve quality
**Iteration 3** (Polish): Final verification, perfection

**Automatic iteration** until:
- Quality ≥95
- Citation coverage = 100%
- Critical gaps = 0

---

## AI System Roles

### Claude Subagents (via Task tool)

**Research Agent** (Haiku):
- Progressive disclosure expert
- Documentation analysis
- Codebase examination
- Pattern detection

**Analysis Agent** (Sonnet):
- Extended thinking for synthesis
- Multi-source integration
- Pattern recognition
- Architectural insights

**Verification Agent** (Haiku):
- 3-pass verification
- Citation checking
- Gap analysis
- Quality scoring

### Gemini CLI

**Strengths**:
- Native web search
- Latest trends (2024-2025)
- Community practices
- Multimodal analysis (if needed)

**Use for**:
- Best practice research
- Industry standards
- Latest vulnerabilities
- Framework comparisons

### Codex CLI

**Strengths**:
- GitHub integration
- Code pattern search
- Deep reasoning (o3 model)
- Implementation examples

**Use for**:
- Code examples
- Design patterns
- Architecture reasoning
- Testing strategies

---

## Configuration

### Prerequisites

**Required**:
- Claude Code (with Task tool access)

**Optional but Recommended**:
- Gemini CLI: `npm install -g @google/gemini-cli`
- Codex CLI: `npm install -g @openai/codex`

**Note**: Skill works with Claude-only fallback if Gemini/Codex unavailable.

### Gemini CLI Setup

```bash
# Install
npm install -g @google/gemini-cli

# Authenticate (OAuth - free)
gemini
# Follow browser authentication

# Test
gemini -p "test prompt"
```

### Codex CLI Setup

```bash
# Install
npm install -g @openai/codex

# Authenticate (ChatGPT Plus/Pro account)
codex login
# Follow browser authentication

# Test
codex exec "test prompt"
```

### Model Selection

**Claude**:
- Haiku: Research & verification (fast, efficient)
- Sonnet: Analysis & synthesis (balanced)
- Opus: Complex reasoning (if needed)

**Gemini**:
- gemini-2.5-flash: Quick research
- gemini-2.5-pro: Complex analysis

**Codex**:
- gpt-5.1-codex: Standard tasks
- o3: Deep architectural reasoning
- o4-mini: Quick operations

---

## Examples

### Example 1: Security Analysis

```
Objective: "Security audit of authentication system"

Phase 2 - Parallel Research:
├─ Claude: Analyzes src/auth/* for patterns
├─ Gemini: Researches "OAuth 2.0 security best practices 2024"
└─ Codex: Finds GitHub examples of secure auth

Phase 3 - Analysis:
└─ Claude: Identifies 3 critical, 5 high priority issues

Phase 4 - Synthesis:
└─ All agree: Missing rate limiting (CRITICAL)
   - Claude: No rate limit found in src/auth/login.ts
   - Gemini: OWASP recommends max 5 attempts/hour
   - Codex: 150+ repos use express-rate-limit
   - Recommendation: Implement with Redis backend

Final Report:
├─ Executive summary
├─ 8 issues (3 critical, 5 high) with fixes
├─ OWASP Top 10 coverage
├─ Specific code examples
└─ Priority implementation plan

Quality: 97/100 ✓
```

### Example 2: Architecture Analysis

```
Objective: "Analyze microservices architecture"

Phase 2:
├─ Claude: Maps services via glob + grep
├─ Gemini: Researches microservices patterns 2024
└─ Codex: Finds service mesh examples

Phase 3:
└─ Claude: Identifies 7 services, 12 integration points

Phase 4:
└─ Synthesis: Service communication patterns
   - Consensus: REST for external, gRPC for internal
   - Trade-offs documented
   - Scaling strategies from Codex examples

Final Report:
├─ Component map (7 services, dependencies)
├─ Integration analysis (12 patterns)
├─ Scalability assessment
└─ Modernization recommendations

Quality: 96/100 ✓
```

### Example 3: Research Synthesis

```
Objective: "Research state management patterns for React 2024"

Phase 2:
├─ Claude: Reviews React docs + examples
├─ Gemini: Web research "React state management 2024"
└─ Codex: Analyzes top 50 React repos

Phase 3:
└─ Pattern analysis: 5 major approaches identified

Phase 4:
└─ Synthesis by use case:
   - Small apps: Context (all sources agree)
   - Medium apps: Zustand (Gemini + Codex recommend)
   - Large apps: Redux Toolkit (battle-tested, Codex data)
   - Server state: TanStack Query (trending, Gemini research)

Final Report:
├─ Decision tree by project size
├─ Pros/cons with sources
├─ Migration strategies
└─ Code examples from Codex

Quality: 98/100 ✓
```

---

## Best Practices

### 1. Be Specific with Objectives
```
❌ "Analyze the code"
✅ "Security analysis of authentication module for OWASP Top 10 compliance"
```

### 2. Trust the Verification
Multi-pass verification catches issues. If quality <95, iteration happens automatically.

### 3. Review External Memory
Check `.analysis/` folder during execution to see progress.

### 4. Leverage Citations
Every claim has file:line or URL. Use for validation and deep dives.

### 5. Multi-Session Projects
Large projects can span sessions:
```
Session 1: Initial analysis → ITERATION_1.md
Session 2: Gap filling → ITERATION_2.md
Session 3: Final polish → ANALYSIS_FINAL.md
```

### 6. Check All Three Perspectives
High-value insights often come from comparing AI perspectives.

---

## Troubleshooting

### Low Quality Score (<95)

**Cause**: Gaps in coverage or missing citations
**Solution**: Automatic iteration 2 fills gaps
**Check**: `.analysis/verification/cross-check.md` for details

### Missing Citations

**Cause**: Verification flags uncited claims
**Solution**: Iteration adds missing attributions
**Prevention**: All agents trained to cite sources

### Gemini/Codex Unavailable

**Fallback**: Claude-only analysis with warning
**Impact**: Reduced perspectives but still comprehensive
**Install**: `npm install -g @google/gemini-cli @openai/codex`

### Conflicting Information

**Resolution**: Synthesis phase investigates conflicts
**Method**: Check ground truth (actual code/docs)
**Output**: Documented reasoning for resolution

---

## Related Skills

- `anthropic-expert`: Anthropic product expertise
- `codex-cli`: Codex integration patterns
- `gemini-cli`: Gemini integration patterns
- `tri-ai-collaboration`: General tri-AI workflows
- `analysis`: Code/skill/process analysis

---

## Quick Reference

### Command Line

```bash
# Full automated analysis
bash .claude/skills/multi-ai-research/scripts/analyze.sh "objective"

# Interactive with Claude Code
# Just ask: "Use multi-ai-research for [objective]"
```

### File Locations

| File | Purpose |
|------|---------|
| `.analysis/ANALYSIS_PLAN.md` | Strategy and assignments |
| `.analysis/research/` | All AI research outputs |
| `.analysis/SYNTHESIS_REPORT.md` | Multi-source synthesis |
| `.analysis/ANALYSIS_FINAL.md` | Complete final report |

### Quality Metrics

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| Quality Score | ≥95/100 | Production-ready |
| Citation Coverage | 100% | All claims sourced |
| Completeness | ≥95% | All objectives met |
| Critical Gaps | 0 | No missing essentials |

### Analysis Time Estimates

| Type | Time | Iterations |
|------|------|------------|
| Security | 45-60 min | 1-2 |
| Architecture | 60-90 min | 1-2 |
| Code Quality | 30-45 min | 1 |
| Performance | 45-60 min | 1-2 |
| Research | 30-60 min | 1 |

---

**multi-ai-research delivers production-ready analysis through systematic multi-AI collaboration, rigorous verification, and iterative refinement - ensuring nothing is missed and every claim is verified.**
