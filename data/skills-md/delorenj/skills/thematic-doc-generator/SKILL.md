---
name: thematic-doc-generator
description: Generate comprehensive, publication-quality technical manuals with thematic storytelling using multi-agent orchestration. Use when user asks for themed documentation, narrative technical guides, memorable training materials, or mentions themes like Victorian, steampunk, art deco, medieval, or nautical combined with technical topics. Triggers on phrases like "create themed manual", "documentation with storytelling", or requests to make docs "more engaging" or "memorable".
---

# Thematic Technical Documentation Generator

Generate comprehensive, publication-quality technical manuals with thematic storytelling using multi-agent orchestration.

## What This Skill Does

Transforms dry technical topics into engaging, memorable documentation through:
- **Multi-agent parallel content generation** - 8 chapters written simultaneously
- **Thematic metaphor system** - Make complex topics memorable (e.g., git → Victorian railways)
- **AI-generated illustrations** - Custom artwork matching your theme
- **Publication-ready output** - Professional structure with front/back matter
- **Automated quality assurance** - 98%+ quality scores with comprehensive validation

## When to Use

- Creating internal technical documentation with personality
- Generating training materials that need to be memorable
- Building comprehensive guides that stand out from typical docs
- Transforming complex topics into accessible narratives
- Team onboarding materials that people actually want to read

## Example Usage

### Basic Usage

```bash
# Generate a Victorian railway-themed git worktree manual
Use this skill with:
  topic: "git worktree safety and best practices"
  theme: "Victorian railway operations (1880s-1920s)"
  chapters: 8
  include_illustrations: true
```

### Advanced Usage

```bash
# Art Deco automation theme for API documentation
Use this skill with:
  topic: "microservices architecture patterns"
  theme: "Art Deco automation and streamlined design"
  audience: "intermediate DevOps engineers"
  chapters: 10
  word_count: {min: 3000, max: 4000}
  illustration_count: 8
  character_guide: true
  output_dir: "./docs/architecture-manual"
```

### Quick Reference Guide

```bash
# Minimal setup for quick guide (no illustrations)
Use this skill with:
  topic: "Docker security best practices"
  theme: "Maritime navigation safety protocols"
  chapters: 5
  comprehensive_vs_quick: "quick-reference"
  include_illustrations: false
```

## What You Get

**Primary Deliverable**:
- Complete manual (30,000+ words) in single markdown file
- Professional front matter (foreword, TOC, usage guide)
- Complete back matter (appendices, index, glossary, statistics)

**Visual Assets** (if illustrations enabled):
- 6-8 AI-generated illustrations matching theme
- High-resolution PNGs (1024px+ minimum dimension)
- Complete integration documentation
- Alt text for accessibility

**Quality Documentation**:
- Comprehensive QA report with metrics
- Theme consistency validation
- Technical accuracy verification
- Publication readiness assessment

**Supporting Files**:
- Individual chapter source files
- Theme proposal document
- Image integration guides
- Sample integration examples

## Parameters

### Required

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `topic` | string | Technical subject to document | "git worktree safety" |
| `theme` | string | Thematic metaphor/aesthetic | "Victorian railway operations" |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `audience` | string | "intermediate practitioners" | Target skill level |
| `chapters` | number | 8 | Number of chapters (5-12) |
| `word_count` | object | {min: 2500, max: 3500} | Target words per chapter |
| `include_illustrations` | boolean | true | Generate AI images |
| `illustration_count` | number | 6 | Target image count (3-10) |
| `character_guide` | boolean | true | Include mascot narrator |
| `output_dir` | string | "./docs/manual" | Output location |
| `comprehensive_vs_quick` | enum | "comprehensive" | Manual style |
| `code_examples` | boolean | true | Include working code |
| `case_studies` | boolean | true | Include real-world examples |

## How It Works

### Phase 1: Adversarial Theme Research (15-30 min)
Two agents collaboratively design theme and structure, challenging each other's proposals.

**Agents**:
- **Theme Designer**: Proposes aesthetic, visual identity, tone, metaphor mappings
- **Structure Architect**: Challenges theme viability, proposes chapter outline

**Output**: `THEME_PROPOSAL.md` (synthesized vision both agents approve)

### Phase 2: Parallel Content Generation (30-60 min)
Each chapter generated independently by specialized agent, all running concurrently.

**Agents**: N chapter agents (one per chapter, typically 8)

**Outputs**: `CHAPTER_1_*.md` through `CHAPTER_N_*.md`

**Key Design**: Chapters are self-contained with no cross-dependencies, enabling true parallelism.

### Phase 3: Publisher Assembly (15-30 min)
Publisher agent synthesizes chapters into cohesive manual with transitions.

**Tasks**:
- Create front matter (title, copyright, foreword, TOC, usage guide)
- Integrate all chapters with smooth transitions
- Create back matter (appendices, index, glossary, statistics, colophon)
- Handle missing chapters gracefully

**Output**: `THE_COMPLETE_MANUAL.md` (unified publication)

### Phase 4: Visual Enhancement (15-30 min, optional)
Illustrator generates thematic imagery using AI.

**Tasks**:
- Generate 6-8 illustrations matching theme
- Ensure visual consistency (color palette, era, style)
- Create comprehensive documentation
- Provide alt text for accessibility

**Outputs**: Images + integration guides

### Phase 5: Quality Assurance (15-30 min)
QA agent validates all deliverables against quality standards.

**Validates**:
- Structural integrity (front/back matter complete)
- Theme consistency (no anachronisms, metaphor accuracy)
- Technical accuracy (code examples, commands)
- Documentation quality (completeness, accessibility)
- Publication readiness (no placeholders, proper licensing)

**Output**: `QA_FINAL_REPORT.md` with APPROVED/REJECTED recommendation

## Success Stories

### Victorian Railway Git Safety Manual
- **Topic**: Git worktree safety and best practices
- **Theme**: Victorian railway operations (1880s-1920s)
- **Results**:
  - 30,606 words across 6 chapters
  - 6 Victorian illustrations (signal towers, brass instruments)
  - 98.4% quality score from QA
  - Publication-ready on first execution
  - Character: Cornelius Worktree (elderly railway dispatcher)

**Excerpt**:
> "Dear Reader and Fellow Dispatcher, you hold in your hands a manual born of necessity. In the modern age of distributed version control, we find ourselves managing not merely a single line of development, but entire networks of parallel tracks..."

## Tips for Best Results

### Theme Selection
- **Choose themes with rich visual vocabulary**: Victorian, Art Deco, Space Age, Medieval
- **Match theme to content domain when possible**: Railways→branching, Architecture→structure
- **Consider character potential**: Who naturally exists in this world?
- **Avoid overly abstract themes**: Concrete metaphors work better

### Scope Planning
- **8 chapters is optimal**: Comprehensive coverage without overwhelming length
- **Allow variance in chapter length**: Quality > rigid word counts
- **Plan for 75% completion**: Missing 1-2 chapters is acceptable if acknowledged
- **Front/back matter adds ~20%**: Factor this into total length

### Visual Enhancement
- **Enable illustrations**: Images significantly boost engagement
- **6 images is ideal**: Cover, character, 4 concepts/diagrams
- **Budget time for iteration**: AI image generation may require refinement
- **Document everything**: Image prompts, models used, regeneration instructions

### Quality Assurance
- **Trust the QA gate**: 95%+ scores indicate publication readiness
- **Address critical issues only**: Minor issues rarely block publication
- **Expect some variance**: Parallel agents produce slightly different styles
- **Publisher smooths inconsistencies**: Trust the synthesis process

## Requirements

### Essential
- Claude Code CLI with skill support
- Task orchestration capability
- File system write access
- Minimum context: ~100K tokens (for 8 chapters)

### Optional
- `fal-text-to-image` skill (for illustrations)
- `pandoc` (for PDF export)
- Markdown linter (for validation)

## Limitations

- **Context window**: Very large manuals (12+ chapters) may exceed limits
- **AI image generation**: Requires API access and credits (fal.ai)
- **Execution time**: 2-3 hours total (not instant)
- **Theme quality**: Success depends on metaphor strength
- **Manual review**: QA catches most issues but human review recommended

## Troubleshooting

**Problem**: "Chapter agents incomplete"
- **Solution**: Retry failed chapters or accept partial completion with transitional notes

**Problem**: "Illustration generation fails"
- **Solution**: Check fal-text-to-image skill installation, API key, credits

**Problem**: "Context window exceeded"
- **Solution**: Reduce chapter count or word count targets

**Problem**: "Theme feels forced"
- **Solution**: Choose more natural metaphor, consult examples/

**Problem**: "QA rejects output"
- **Solution**: Review critical issues, re-run appropriate phase (usually chapter agents)

## License

This skill is released under the Unlicense (public domain). Generated manuals inherit this license unless you specify otherwise.

## Support

- Documentation: See `docs/` directory in skill package
- Examples: See `examples/` directory
- Issues: https://github.com/delorenj/thematic-doc-generator/issues

---

**Generated manuals are publication-ready. No additional editing required (though always welcome).**
