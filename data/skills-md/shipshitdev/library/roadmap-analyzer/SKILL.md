---
name: roadmap-analyzer
description: Analyze project features against ICP (Ideal Customer Profile) needs to identify gaps and recommend roadmap priorities. Use this skill when asked to evaluate current product state, identify what should be built next, assess competitive positioning, or plan product roadmap based on target customer needs. Outputs gap analysis, prioritized backlog, and strategic themes. Discovers ICP and features from project documentation.
---

# Roadmap Analyzer

## Overview

This skill analyzes a project's current feature set against the needs of the Ideal Customer Profile (ICP). Before analyzing, discover the project's ICP from documentation (`.agent/SYSTEM/` or project docs) and current features from the codebase and documentation.

The skill produces three outputs:

1. **Gap Analysis Table**: Side-by-side comparison of ICP needs vs current features with gaps highlighted
2. **Prioritized Backlog**: Ranked list of features to build next based on ICP alignment and impact
3. **Strategic Themes**: High-level focus areas with specific initiatives

## When to Use This Skill

Invoke this skill when asked to:

- "What should we build next?"
- "Compare our features against what our customers need"
- "Analyze product gaps for our ICP"
- "Help me plan the product roadmap"
- "What features are missing for our target customers?"
- "Evaluate our competitive positioning"
- "What do we need to focus on to serve SMBs creating UGC?"

## Analysis Workflow

### Step 1: Discover Current Features

Use a hybrid approach to identify existing project capabilities (discover from project):

#### 1.1 Automated Codebase Scan

Search the codebase for feature implementations. Focus on:

**Key directories to explore:**

```
apps/frontend-apps/*/      - Frontend applications
apps/apis/*/               - Backend APIs
packages/*/                - Shared packages
```

**Search patterns for features:**

- Component names (React components often indicate UI features)
- API endpoints (routes indicate backend capabilities)
- Service methods (business logic indicates functionality)
- Database schemas (data models reveal supported features)
- Configuration files (feature flags, settings)

**Use grep/glob to find:**

- Video editing features: `pattern: "edit|timeline|trim|cut|transition"`
- Avatar features: `pattern: "avatar|character|persona|voice"`
- Export features: `pattern: "export|format|platform|render"`
- Template features: `pattern: "template|preset|brand"`
- AI features: `pattern: "ai|generate|auto|openai|anthropic"`

#### 1.2 User Context Integration

Ask the user:

- "Are there features I should know about that might not be obvious in the code?"
- "Any recent features added that might not be fully integrated?"
- "Features in beta or soft-launched?"
- "Integrations or capabilities documented elsewhere?"

#### 1.3 Feature Inventory Creation

Organize discovered features into categories from `references/feature-categories.md`:

1. Content Input & Ideation
2. AI Avatar Creation & Management
3. Video Editing & Assembly
4. Visual Enhancement & Effects
5. Text, Captions & Typography
6. Audio & Music
7. Platform Optimization & Export
8. Templates & Brand Management
9. Collaboration & Workflow
10. Asset Management & Media Library
11. AI & Automation Features
12. Analytics & Performance
13. Learning & Support
14. Integration & Ecosystem
15. E-commerce & Monetization

For each feature, note:

- **Status**: Exists (production), Partial (incomplete), Planned, Missing
- **Quality**: Production-ready, Beta, Prototype, Needs improvement
- **Location**: Where found in codebase (file paths)

### Step 2: Load ICP and Editor Needs Context

Read the reference documents to understand requirements:

**Required reading:**

- `references/icp-profile.md` - Deep understanding of target customer needs
- `references/editor-needs.md` - What editors need for great social content
- `references/feature-categories.md` - Comprehensive feature taxonomy

**Key focus areas from ICP:**

1. **AI Avatar Army**: Creating multiple avatars, consistency, customization
2. **User Empowerment**: Self-service creation, templates, intuitive UX
3. **UGC at Scale**: Volume, speed, platform-native content
4. **Team Collaboration**: Multi-user, approvals, brand consistency

**Critical editor needs:**

- Platform-specific optimization (TikTok, Instagram, YouTube)
- Fast pacing and trending effects
- Text overlays and captions
- Audio/music integration
- Quick variations for A/B testing

### Step 3: Gap Analysis

Compare current features against ICP needs and editor requirements.

#### 3.1 Create Gap Analysis Table

Format:

```markdown
| Feature Category | ICP Need Priority | Current State | Gap Severity | Key Missing Elements |
|-----------------|-------------------|---------------|--------------|----------------------|
| AI Avatar Creation | CRITICAL | Partial | HIGH | Multiple avatars, avatar library, voice cloning |
| Platform Optimization | CRITICAL | Missing | CRITICAL | Auto-reframe, batch export multiple formats |
| ... | ... | ... | ... | ... |
```

**Gap Severity Levels:**

- **CRITICAL**: Blocking ICP adoption, core value prop missing
- **HIGH**: Significantly impacts ICP success, competitive disadvantage
- **MEDIUM**: Limits scale/efficiency, nice-to-have
- **LOW**: Future enhancement, not blocking

**Priority Levels:**

- **CRITICAL**: Must-have for ICP, core to value proposition
- **HIGH**: Important for ICP success, competitive requirement
- **MEDIUM**: Valuable but not essential
- **LOW**: Nice-to-have, future consideration

#### 3.2 Identify Critical Gaps

Highlight gaps where:

1. ICP Need Priority = CRITICAL AND Gap Severity = CRITICAL/HIGH
2. Feature is table stakes for competitors
3. Feature directly enables "AI avatar army" or "user empowerment"
4. Feature required for platform-native content (TikTok, Instagram, etc.)

### Step 4: Generate Prioritized Backlog

Create a ranked list of features to build next.

#### 4.1 Prioritization Framework

Score each feature on:

**ICP Impact (1-5)**

- 5: Core to ICP value prop, directly addresses primary pain point
- 4: Strongly supports ICP needs, key differentiator
- 3: Valuable for ICP, improves experience
- 2: Nice-to-have for ICP
- 1: Minimal ICP impact

**Urgency (1-5)**

- 5: Blocking sales/adoption, critical competitive gap
- 4: Significant competitive pressure, customer requests
- 3: On roadmap, good timing to build
- 2: Can wait, not time-sensitive
- 1: Future consideration

**Implementation Effort (1-5)**

- 5: Very high effort, 3+ months, complex
- 4: High effort, 1-3 months, significant work
- 3: Medium effort, 2-4 weeks, moderate complexity
- 2: Low effort, < 2 weeks, straightforward
- 1: Very low effort, < 1 week, simple

**Priority Score = (ICP Impact × 2 + Urgency × 1.5) / Implementation Effort**

Higher score = higher priority.

#### 4.2 Backlog Format

```markdown
## Prioritized Feature Backlog

### P0 (Build Immediately - Priority Score > 3.0)
1. **[Feature Name]** (Score: 4.2)
   - **Why**: [ICP impact explanation]
   - **Customer need**: [Specific ICP pain point addressed]
   - **Effort**: [Time estimate]
   - **Dependencies**: [What's needed first]

### P1 (Build Next Quarter - Priority Score 2.0-3.0)
[Same format]

### P2 (Future Consideration - Priority Score < 2.0)
[Same format]
```

#### 4.3 Quick Wins Section

Identify features with:

- High ICP Impact (4-5)
- Low Implementation Effort (1-2)
- Decent Urgency (3+)

These are "quick wins" that deliver high value with low investment.

### Step 5: Define Strategic Themes

Group features into high-level strategic focus areas.

#### 5.1 Theme Identification

Analyze feature clusters to identify 3-5 strategic themes, such as:

**Example themes:**

- **"AI Avatar Arsenal"**: Building the avatar creation and management system
- **"Platform-Native Mastery"**: Optimizing for TikTok, Instagram, YouTube
- **"Team Empowerment Engine"**: Collaboration, templates, workflows
- **"Speed to Market"**: Automation, batch processing, quick variations
- **"Editor's Toolkit"**: Core editing capabilities for creators

#### 5.2 Theme Structure

For each theme, provide:

```markdown
## [Theme Name]

**Vision**: [1-2 sentence vision for this theme]

**ICP Alignment**: [How this theme serves ICP needs]

**Current State**: [Where we are today]

**Target State**: [Where we need to be]

**Key Initiatives**:
1. **[Initiative Name]**
   - Features: [Specific features]
   - Impact: [Expected outcome]
   - Timeline: [When to build]

2. **[Next initiative]**
   [Same format]

**Success Metrics**:
- [Metric 1]: [Target]
- [Metric 2]: [Target]
```

#### 5.3 Theme Prioritization

Recommend theme focus order based on:

1. **Foundation themes first**: Core platform capabilities required for everything else
2. **Differentiator themes next**: Unique value props (e.g., AI avatar army)
3. **Enhancement themes last**: Improvements to existing capabilities

### Step 6: Output Assembly

Combine all analysis into a comprehensive report:

```markdown
# [Project] Roadmap Analysis
## [Date]

## Executive Summary
[3-5 bullets summarizing key findings and recommendations]

## Gap Analysis
[Gap analysis table from Step 3]

## Critical Gaps
[Detailed explanation of critical gaps from Step 3.2]

## Prioritized Backlog
[Prioritized backlog from Step 4]

## Quick Wins
[Quick wins list from Step 4.3]

## Strategic Themes
[Strategic themes from Step 5]

## Recommended Focus
**Next 30 days**: [Immediate priorities]
**Next quarter**: [Q1 focus areas]
**Next 6 months**: [Half-year vision]

## Appendix
### Feature Inventory
[Complete list of discovered features]

### ICP Summary
[Brief ICP recap]
```

## Best Practices

### Analysis Quality

1. **Be specific**: Don't just say "add editing features"—specify "Add timeline trimming with frame-level precision"
2. **Show evidence**: Reference where features exist (or don't) in codebase
3. **Connect to customer**: Explain how each feature serves ICP needs
4. **Consider competition**: Note when gaps create competitive disadvantage
5. **Balance ambition with reality**: Acknowledge technical constraints

### Prioritization Rigor

1. **Defend scores**: Explain why a feature gets specific impact/urgency/effort scores
2. **Consider dependencies**: Note when features require others to be built first
3. **Think sequentially**: Some features enable others (e.g., avatar library before multi-avatar videos)
4. **Question assumptions**: If effort seems high, suggest simpler MVP versions

### Strategic Thinking

1. **Theme coherence**: Themes should feel cohesive, not arbitrary groupings
2. **ICP-centric**: Every recommendation should trace back to ICP needs
3. **Differentiation**: Emphasize features that set the project apart
4. **Reality check**: Acknowledge market timing, competitive landscape, technical feasibility

## Common Pitfalls to Avoid

1. **Don't just list features**: Explain WHY each feature matters for ICP
2. **Don't ignore existing features**: Give credit for what already exists
3. **Don't treat all gaps equally**: Not all missing features are critical
4. **Don't forget the "AI avatar army" vision**: This is a key differentiator
5. **Don't overlook platform-specific needs**: TikTok ≠ YouTube
6. **Don't assume features work well**: Existing features might have quality gaps

## Resources

### references/

Three comprehensive reference documents inform the analysis:

- **icp-profile.md**: Detailed profile of target customers (SMBs creating UGC with AI, empowering users, building AI avatar armies). Includes pain points, core needs, success metrics, and buying journey.

- **editor-needs.md**: Comprehensive breakdown of what video editors need to create great content for social platforms (TikTok, Instagram, YouTube). Covers editing capabilities, platform-specific requirements, audio/visual needs, and competitive benchmarks.

- **feature-categories.md**: Taxonomy of 15 feature categories typical in AI UGC platforms. Provides framework for organizing discovered features and identifying gaps systematically.

Load these references at the start of analysis to inform all evaluation and recommendations.
