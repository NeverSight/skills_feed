---
name: planning-architect
description: Comprehensive skill development planning. Analyzes requirements, chooses organizational patterns (workflow/task/reference/capabilities), defines structure, estimates complexity, identifies dependencies, and creates detailed implementation plan. Use when planning new skills, converting documentation to skills, or architecting complex skill systems.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Planning Architect

## Overview

planning-architect systematically plans Claude Code skill development from initial concept to detailed implementation blueprint. It guides you through six sequential steps to create comprehensive skill plans that ensure successful development.

**Purpose**: Transform skill ideas into actionable implementation plans with clear structure, accurate estimates, and identified dependencies.

**Value**: Prevents rework, reduces development time, ensures consistency, and produces better-designed skills through systematic planning.

**When to Use**:
- Planning new skills from scratch
- Converting existing documentation into skills
- Architecting complex multi-file skills
- Planning skill improvements or refactoring
- Coordinating dependent skill development

## Prerequisites

Before planning a skill, gather:

1. **Problem Definition**: Clear understanding of what problem the skill solves
2. **Domain Knowledge**: Familiarity with the domain being captured
3. **User Context**: Understanding of who will use the skill and how
4. **Existing Resources**: Any documentation, examples, or patterns to reference
5. **Skill-Builder Context**: Familiarity with skill-builder-generic patterns

## Planning Workflow

### Step 1: Analyze Requirements

**Objective**: Clearly define what the skill must accomplish and its scope

**Process**:

1. **Define the Problem**
   - What specific problem does this skill solve?
   - What pain point does it address?
   - What would happen without this skill?

2. **Identify Target Users**
   - Who will use this skill? (You, team, community)
   - What is their expertise level?
   - What context will they invoke it in?

3. **Capture Domain Knowledge**
   - What domain expertise must be captured?
   - What workflows need documentation?
   - What best practices should be included?
   - What anti-patterns should be avoided?

4. **Determine Scope**
   - What is explicitly in scope?
   - What is explicitly out of scope?
   - What are the boundaries?
   - What is the minimum viable skill?

5. **Identify Existing Resources**
   - Are there similar skills to reference?
   - Is there existing documentation to convert?
   - Are there community patterns to follow?
   - Are there anti-patterns to avoid?

**Questions to Answer**:

```
Problem Definition:
- What problem does this skill solve?
- Who experiences this problem?
- How do they currently solve it (if at all)?
- What would success look like?

Scope:
- What is the primary objective?
- What are secondary objectives?
- What is explicitly out of scope?
- What is the minimum viable version?

Users:
- Who will use this skill?
- What is their expertise level?
- What context will they invoke it in?
- What other skills do they likely have?

Domain:
- What domain knowledge is required?
- What workflows exist in this domain?
- What terminology is standard?
- What are common pitfalls?

Resources:
- Are there similar skills to study?
- Is there documentation to convert?
- Are there examples to follow?
- What research is needed?
```

**Output**: Requirements document answering all questions above

**Example**:
```
Problem: Developers waste time debugging Railway deployments
Users: Development team with Node.js experience
Domain: Railway deployment, Docker, environment config
Scope: Railway-specific deployment workflow for Node.js + React
Out of Scope: Other platforms (Vercel, AWS), other languages
Resources: Railway docs, existing deployment notes
MVP: Basic deployment workflow with common troubleshooting
```

**See Also**: [references/pattern-selection-guide.md](references/pattern-selection-guide.md) includes requirements analysis templates

---

### Step 2: Select Organizational Pattern

**Objective**: Choose the optimal organizational pattern for this skill

**The 4 Organizational Patterns**:

#### Pattern 1: Workflow-Based
**Use When**: Sequential processes with clear steps where order matters

**Characteristics**:
- Linear progression (Step 1 → Step 2 → Step 3)
- Each step builds on previous steps
- Clear start and end points
- Dependencies between steps

**Examples**:
- Deployment workflows
- API integration processes
- Testing workflows
- Setup/configuration sequences

**Structure**:
```markdown
## Workflow
### Step 1: [Action]
### Step 2: [Action]
### Step 3: [Action]
```

**Choose This When**:
- Process has clear sequential steps
- Order of operations matters
- Steps have dependencies
- There's a defined goal at the end

---

#### Pattern 2: Task-Based
**Use When**: Independent operations without order dependency

**Characteristics**:
- Tasks can be performed in any order
- No dependencies between tasks
- Quick reference format
- Each task is self-contained

**Examples**:
- Troubleshooting guides
- Utility collections
- Command references
- Independent operations

**Structure**:
```markdown
## Tasks
### Task A: [Action]
### Task B: [Action]
### Task C: [Action]
```

**Choose This When**:
- Operations are independent
- Order doesn't matter
- Users will perform subset of tasks
- Quick lookup is primary use case

---

#### Pattern 3: Reference/Guidelines
**Use When**: Standards, patterns, design systems, best practices

**Characteristics**:
- Reference material (look-up)
- Guidelines and standards
- Comprehensive coverage
- Examples and specifications

**Examples**:
- Design systems
- Coding standards
- API documentation
- Style guides

**Structure**:
```markdown
## Guidelines
### Guideline 1: [Concept]
### Guideline 2: [Concept]

## Reference
### Component A
### Component B
```

**Choose This When**:
- Documenting standards or patterns
- Creating reference material
- Establishing guidelines
- Comprehensive coverage needed

---

#### Pattern 4: Capabilities-Based
**Use When**: Integrated feature suites with multiple entry points

**Characteristics**:
- Multiple interconnected features
- Various entry points
- Features work together
- Complex integrations

**Examples**:
- Complex systems
- Platforms with multiple features
- Toolkits with related capabilities

**Structure**:
```markdown
## Capabilities
### Capability A: [Feature]
### Capability B: [Feature]

## Integration
How capabilities work together
```

**Choose This When**:
- Multiple related features
- Features can be used independently or together
- Multiple valid starting points
- Complex system with many capabilities

---

**Decision Process**:

```
START
↓
Does the skill describe a sequential process?
├─ YES → Is order important?
│         ├─ YES → WORKFLOW-BASED
│         └─ NO → TASK-BASED
│
└─ NO → Is it primarily reference material?
         ├─ YES → REFERENCE/GUIDELINES
         └─ NO → Does it have multiple integrated features?
                  ├─ YES → CAPABILITIES-BASED
                  └─ NO → Re-examine requirements (likely TASK-BASED)
```

**Pattern Selection Factors**:

| Factor | Workflow | Task | Reference | Capabilities |
|--------|----------|------|-----------|--------------|
| Order matters | ✓ | ✗ | ✗ | ~ |
| Dependencies | ✓ | ✗ | ✗ | ✓ |
| Quick lookup | ✗ | ✓ | ✓ | ~ |
| Sequential process | ✓ | ✗ | ✗ | ~ |
| Standards/guidelines | ✗ | ✗ | ✓ | ✗ |
| Multiple features | ~ | ✗ | ✗ | ✓ |
| Integration complexity | ~ | ✗ | ✗ | ✓ |

**Output**: Selected organizational pattern with justification

**Example**:
```
Pattern: Workflow-Based
Justification: Railway deployment is sequential (prepare → configure → deploy → verify)
Alternative Considered: Task-based rejected because order matters
```

**See Also**: [references/pattern-selection-guide.md](references/pattern-selection-guide.md) for comprehensive decision tree and examples

---

### Step 3: Plan File Structure

**Objective**: Define complete file structure using progressive disclosure

**Progressive Disclosure Architecture**:

The key principle: **Keep SKILL.md lean, bundle details in references/**

**Three-Level System**:

1. **SKILL.md** (Always Loaded)
   - Target: <5,000 words (~1,000-1,500 lines)
   - Content: Overview, quick start, key workflows, core concepts
   - Purpose: Provides essential context without overwhelming Claude's context window

2. **references/** (Loaded On-Demand)
   - Target: 10,000+ words okay per file
   - Content: Comprehensive guides, detailed explanations, extensive examples
   - Purpose: Deep details available when needed without bloating main skill

3. **scripts/** (Loaded When Executed)
   - Target: Any size
   - Content: Automation helpers, validation tools, generators
   - Purpose: Executable tools that extend skill capabilities

4. **templates/** (Loaded When Needed)
   - Target: Any size
   - Content: Reusable patterns, boilerplate code, scaffolds
   - Purpose: Starting points for common patterns

**File Structure Planning**:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter
│   ├── Overview
│   ├── Prerequisites (if needed)
│   ├── Main content (workflow/tasks/guidelines/capabilities)
│   ├── Quick Start
│   ├── Examples (brief)
│   └── References (links to references/)
│
├── references/ (optional but recommended)
│   ├── detailed-guide-1.md (comprehensive guide)
│   ├── detailed-guide-2.md (another detailed guide)
│   └── advanced-topics.md (deep dive content)
│
├── scripts/ (optional)
│   ├── helper-script.py (automation)
│   └── validation-script.py (validation)
│
└── templates/ (optional)
    ├── template-1.md (reusable pattern)
    └── template-2.md (another pattern)
```

**SKILL.md Content Allocation**:

**Include in SKILL.md**:
- Problem overview (why skill exists)
- Prerequisites
- Core workflow/tasks/guidelines/capabilities
- Quick start instructions
- Brief examples (1-3)
- Links to references for details

**Move to references/**:
- Comprehensive step-by-step guides
- Extensive examples (4+)
- Detailed explanations
- Advanced topics
- Troubleshooting guides
- Deep dives into concepts
- Long reference tables

**Move to scripts/**:
- Automation helpers
- Validation tools
- Code generators
- Analysis tools
- Interactive wizards

**Move to templates/**:
- Boilerplate files
- Configuration templates
- Code scaffolds
- Reusable patterns

**Reference File Naming**:

Use descriptive hyphen-case names:
- `pattern-selection-guide.md` (not `guide1.md`)
- `complexity-estimation-techniques.md` (not `complexity.md`)
- `advanced-workflows.md` (not `advanced.md`)

**Reference Organization Strategies**:

1. **By Topic** (Most Common)
   ```
   references/
   ├── authentication-guide.md
   ├── data-fetching-guide.md
   └── error-handling-guide.md
   ```

2. **By Depth** (Progressive Learning)
   ```
   references/
   ├── basics-guide.md
   ├── intermediate-guide.md
   └── advanced-guide.md
   ```

3. **By Workflow Step** (For Workflow-Based)
   ```
   references/
   ├── step1-preparation-guide.md
   ├── step2-execution-guide.md
   └── step3-validation-guide.md
   ```

4. **By Use Case** (For Task-Based)
   ```
   references/
   ├── use-case-api-integration.md
   ├── use-case-database-setup.md
   └── use-case-testing.md
   ```

**Linking to References**:

Always use relative paths with descriptive link text:

```markdown
Good:
See [Pattern Selection Guide](references/pattern-selection-guide.md) for detailed decision tree.

Bad:
See references/pattern-selection-guide.md for details.
```

**Output**: Complete file structure plan with file names and content allocation

**Example**:
```
railway-deployment/
├── SKILL.md (~1,200 lines)
│   - Overview of Railway deployment
│   - Prerequisites
│   - 4-step deployment workflow
│   - Quick start example
│   - Links to references
│
├── references/
│   ├── environment-configuration-guide.md (~800 lines)
│   ├── docker-setup-guide.md (~600 lines)
│   ├── troubleshooting-common-issues.md (~1,000 lines)
│   └── railway-pricing-optimization.md (~400 lines)
│
├── scripts/
│   └── validate-config.py (~150 lines)
│
└── templates/
    └── railway-config-template.json (~50 lines)
```

**See Also**: [references/structure-planning-guide.md](references/structure-planning-guide.md) for comprehensive progressive disclosure planning

---

### Step 4: Estimate Complexity

**Objective**: Estimate development time and effort required

**Complexity Factors**:

1. **Skill Size**
   - Minimal (SKILL.md only): 2-4 hours
   - Small (SKILL.md + 1-2 references): 6-10 hours
   - Medium (SKILL.md + 3-5 references): 12-18 hours
   - Large (SKILL.md + 6+ references + scripts): 20-30 hours
   - Very Large (Multiple scripts, templates, extensive docs): 30+ hours

2. **Pattern Complexity**
   - Workflow-based: Medium (need to document each step clearly)
   - Task-based: Low-Medium (independent tasks easier to document)
   - Reference/Guidelines: Medium-High (requires comprehensive coverage)
   - Capabilities-based: High (complex interactions to document)

3. **Domain Complexity**
   - Familiar domain: 1x multiplier
   - Some learning needed: 1.5x multiplier
   - Significant research needed: 2x multiplier
   - Novel/complex domain: 2.5x+ multiplier

4. **Automation Requirements**
   - No scripts: 0 additional hours
   - Simple scripts (1-2): +4-6 hours
   - Complex scripts (3+): +10-15 hours
   - Interactive tools: +15-20 hours

5. **Research Requirements**
   - Existing documentation: 1x
   - Some research needed: +2-4 hours
   - Extensive research: +8-12 hours
   - No existing resources: +15+ hours

**Estimation Formula**:

```
Base Time = Skill Size (from factor 1)
Pattern Multiplier = Factor 2
Domain Multiplier = Factor 3
Automation Add = Factor 4
Research Add = Factor 5

Total Estimate = (Base Time × Pattern Multiplier × Domain Multiplier) + Automation Add + Research Add
```

**Estimation Examples**:

**Example 1: Simple Troubleshooting Skill**
```
Base: Small (6-10h) = 8h
Pattern: Task-based (1x)
Domain: Familiar (1x)
Automation: None (0h)
Research: Existing docs (0h)

Total: 8h × 1 × 1 + 0 + 0 = 8 hours
```

**Example 2: Complex Deployment Workflow**
```
Base: Large (20-30h) = 25h
Pattern: Workflow-based (1.2x)
Domain: Some learning (1.5x)
Automation: Simple scripts (5h)
Research: Some needed (3h)

Total: 25h × 1.2 × 1.5 + 5 + 3 = 53 hours
```

**Example 3: Design System Reference**
```
Base: Medium (12-18h) = 15h
Pattern: Reference/Guidelines (1.3x)
Domain: Familiar (1x)
Automation: None (0h)
Research: Existing docs (0h)

Total: 15h × 1.3 × 1 + 0 + 0 = 19.5 hours
```

**Estimation Checklist**:

- [ ] Counted number of reference files needed
- [ ] Assessed domain knowledge gap
- [ ] Identified automation needs
- [ ] Determined research requirements
- [ ] Applied pattern complexity multiplier
- [ ] Added buffer for iteration (10-20%)
- [ ] Validated estimate seems reasonable

**Output**: Time estimate with breakdown by component

**Example**:
```
Estimated Development Time: 42-48 hours

Breakdown:
- SKILL.md: 8 hours
- references/ (4 files): 20 hours
  - pattern-selection-guide.md: 6h
  - structure-planning-guide.md: 6h
  - complexity-estimation-guide.md: 4h
  - dependency-analysis-guide.md: 4h
- scripts/plan-skill.py: 10 hours
- templates/: 2 hours
- Validation & testing: 4 hours

Total: 44 hours (42-48 hour range)
```

**See Also**: [references/complexity-estimation-guide.md](references/complexity-estimation-guide.md) for detailed estimation techniques and calibration data

---

### Step 5: Identify Dependencies

**Objective**: Identify what this skill depends on and what depends on it

**Dependency Types**:

#### 1. Skill Dependencies
Skills this skill relies on or references

**Identification Questions**:
- Does this skill assume other skills exist?
- Does this skill reference other skills in examples?
- Would this skill be more effective with other skills available?

**Example**:
```
planning-architect depends on:
- skill-builder-generic (for skill patterns)
- No hard dependencies, but enhanced by:
  - task-development (for breaking down implementation)
  - complexity-estimation (for time estimates)
```

#### 2. Tool Dependencies
External tools or MCPs this skill requires

**Identification Questions**:
- Does this skill use specific Claude Code tools? (WebSearch, WebFetch, Bash, etc.)
- Does this skill require MCPs? (Context7, GitHub, etc.)
- Are there external services needed? (APIs, databases, etc.)

**Example**:
```
skill-researcher depends on:
- WebSearch tool (for latest patterns)
- WebFetch tool (for documentation)
- Context7 MCP (optional, for deep context)
- GitHub API (for community skill analysis)
```

#### 3. Knowledge Dependencies
Domain knowledge or prerequisites users must have

**Identification Questions**:
- What knowledge must users have before using this skill?
- What terminology must users understand?
- What concepts are assumed as known?

**Example**:
```
railway-deployment requires users know:
- Basic Node.js and npm
- Git basics
- Command line usage
- HTTP concepts (for API deployments)
```

#### 4. File Dependencies
Files in the project this skill references

**Identification Questions**:
- Does this skill reference specific file paths?
- Does it assume certain project structure?
- Does it expect configuration files to exist?

**Example**:
```
deployment-guide assumes:
- package.json exists
- .env.example exists (for environment variables)
- Dockerfile exists (or provides template)
```

#### 5. Reverse Dependencies (What Depends On This)
Other skills that will depend on this skill

**Identification Questions**:
- What skills will be built after this one?
- What skills might reference this skill?
- Who is the downstream consumer?

**Example**:
```
planning-architect will be depended on by:
- task-development (uses planning output)
- skill-researcher (feeds into planning)
- All future skill development (planning is first step)
```

**Dependency Documentation Format**:

```markdown
## Dependencies

### Required
- skill-builder-generic: Core patterns and templates
- WebSearch tool: For researching similar skills

### Optional
- Context7 MCP: Enhanced context for complex planning
- skill-researcher: For comprehensive research phase

### User Prerequisites
- Familiarity with skill-builder-generic
- Understanding of progressive disclosure
- Basic markdown knowledge

### Reverse Dependencies
- task-development (will use planning output)
- skill-composer (for multi-skill workflows)
```

**Output**: Complete dependency list with all five types

**Example**:
```
Dependencies for planning-architect:

Skill Dependencies:
- Required: skill-builder-generic
- Optional: skill-researcher, analysis

Tool Dependencies:
- None (uses only standard Claude Code capabilities)

Knowledge Dependencies:
- Familiarity with Claude Code skills
- Understanding of progressive disclosure
- Markdown knowledge

File Dependencies:
- skill-builder-package/examples/* (for reference examples)

Reverse Dependencies:
- task-development (next in bootstrap sequence)
- todo-management (uses planning structure)
- All future skills (planning is foundation)
```

**See Also**: [references/dependency-analysis-guide.md](references/dependency-analysis-guide.md) for dependency mapping techniques

---

### Step 6: Define Validation Criteria

**Objective**: Establish how to validate the skill works correctly

**Validation Categories**:

#### 1. Structure Validation
Does the skill have correct file structure?

**Criteria**:
- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] Directory structure matches plan
- [ ] All reference files exist
- [ ] All scripts are executable
- [ ] All templates are present

**Validation Method**: Run `validate-skill.py` script

---

#### 2. Content Validation
Is the content complete and correct?

**Criteria**:
- [ ] Overview clearly states purpose
- [ ] Prerequisites are documented
- [ ] Main content follows chosen pattern
- [ ] Examples are provided
- [ ] References are linked correctly
- [ ] Writing uses imperative voice
- [ ] No TODO placeholders (except in templates)
- [ ] Trigger keywords present in description

**Validation Method**: Manual review + automated checks

---

#### 3. Functional Validation
Does the skill actually work?

**Criteria**:
- [ ] Can invoke skill by name
- [ ] Skill loads without errors
- [ ] References load when requested
- [ ] Scripts execute successfully
- [ ] Templates can be used
- [ ] Examples produce expected results

**Validation Method**: Test invocation + script execution

---

#### 4. Usability Validation
Is the skill easy to use?

**Criteria**:
- [ ] Quick start is actually quick (<5 min)
- [ ] Examples are clear and relevant
- [ ] Instructions are unambiguous
- [ ] Terminology is consistent
- [ ] Navigation is intuitive
- [ ] Context window impact is minimal

**Validation Method**: User testing + feedback

---

#### 5. Completeness Validation
Does the skill cover everything it should?

**Criteria**:
- [ ] All requirements from Step 1 are addressed
- [ ] All workflows are documented
- [ ] Edge cases are covered
- [ ] Troubleshooting is included
- [ ] Best practices are captured
- [ ] Anti-patterns are noted

**Validation Method**: Requirements traceability matrix

---

**Validation Plan Template**:

```markdown
## Validation Plan

### Structure Validation
Method: Automated script
Tool: validate-skill.py
Pass Criteria: Zero errors, max 1 warning

### Content Validation
Method: Manual review
Checklist: 50-point validation checklist
Pass Criteria: All checklist items pass

### Functional Validation
Method: Test invocation
Test Cases:
1. Invoke skill in clean session
2. Request reference file
3. Execute scripts with test input
4. Use templates in sample project
Pass Criteria: All test cases succeed

### Usability Validation
Method: User testing
Testers: 2-3 developers
Pass Criteria: Users can complete quick start in <5 min

### Completeness Validation
Method: Requirements review
Process: Check each requirement has corresponding content
Pass Criteria: 100% requirements coverage
```

**Output**: Comprehensive validation plan with test cases

**Example**:
```
Validation Plan for planning-architect:

Structure:
- Run validate-skill.py
- Verify 4 reference files present
- Verify plan-skill.py is executable

Content:
- Review all 6 workflow steps
- Verify examples in each step
- Check imperative voice usage
- Validate trigger keywords

Functional:
- Invoke planning-architect
- Follow workflow for test skill
- Run plan-skill.py with test input
- Verify generates complete plan

Usability:
- Ask developer to plan simple skill
- Time quick start completion
- Gather feedback on clarity

Completeness:
- Verify all planning aspects covered
- Check all 4 patterns documented
- Ensure estimation methods present
- Validate dependency analysis included
```

---

## Quick Start: Plan a Skill in 30 Minutes

### 1. Analyze Requirements (10 minutes)

Answer these questions:
- **Problem**: What problem does this skill solve?
- **Users**: Who will use it?
- **Domain**: What knowledge to capture?
- **Scope**: What's in/out of scope?

### 2. Select Pattern (5 minutes)

Use decision tree:
- Sequential process with dependencies? → **Workflow-based**
- Independent operations? → **Task-based**
- Standards/reference? → **Reference/Guidelines**
- Multiple integrated features? → **Capabilities-based**

### 3. Plan Structure (5 minutes)

```
skill-name/
├── SKILL.md (always)
├── references/ (if detailed guides needed)
├── scripts/ (if automation needed)
└── templates/ (if reusable patterns needed)
```

### 4. Estimate Time (5 minutes)

- Count reference files: ____
- Automation needed?: ____
- Research required?: ____
- Rough estimate: ____ hours

### 5. List Dependencies (3 minutes)

- Skill dependencies: ____
- Tool dependencies: ____
- Knowledge prerequisites: ____

### 6. Define Validation (2 minutes)

- Structure: validate-skill.py
- Functional: Test invoke + scripts
- Complete: Requirements coverage

**Result**: Complete plan ready for implementation!

---

## Examples

### Example 1: Simple Troubleshooting Skill

**Requirements**:
- Problem: Railway deployment errors are cryptic
- Users: Dev team with Railway experience
- Domain: Railway troubleshooting
- Scope: Common errors + solutions

**Pattern**: Task-based (independent error cases)

**Structure**:
```
railway-troubleshooting/
├── SKILL.md (task-based format)
└── references/
    └── advanced-troubleshooting.md
```

**Estimate**: 8-10 hours (small, familiar domain)

**Dependencies**:
- Knowledge: Basic Railway concepts
- No skill dependencies

**Validation**: Test each troubleshooting case

---

### Example 2: Complex API Integration

**Requirements**:
- Problem: FHIR API integration is complex
- Users: Medical dev team
- Domain: FHIR, OAuth, REST
- Scope: Complete integration workflow

**Pattern**: Workflow-based (sequential integration steps)

**Structure**:
```
fhir-integration/
├── SKILL.md (workflow format)
├── references/
│   ├── fhir-resources-guide.md
│   ├── oauth-setup-guide.md
│   └── error-handling-guide.md
├── scripts/
│   └── validate-fhir-response.py
└── templates/
    └── fhir-request-template.json
```

**Estimate**: 35-40 hours (large, some research needed)

**Dependencies**:
- Skill: oauth-integration
- Tool: WebFetch (for API testing)
- Knowledge: REST APIs, JSON

**Validation**: Full integration test with FHIR server

---

### Example 3: Design System Reference

**Requirements**:
- Problem: Inconsistent UI components
- Users: Frontend team
- Domain: Design system
- Scope: Colors, typography, components

**Pattern**: Reference/Guidelines (design standards)

**Structure**:
```
design-system/
├── SKILL.md (reference format)
├── references/
│   ├── color-palette-guide.md
│   ├── typography-guide.md
│   └── component-library.md
└── assets/
    ├── colors.png
    └── typography-examples.png
```

**Estimate**: 18-22 hours (medium, design domain)

**Dependencies**:
- Knowledge: Design principles, CSS
- No skill dependencies

**Validation**: Apply design system to sample component

---

## Planning Output

After completing the 6-step workflow, you should have:

1. **Requirements Document**
   - Problem statement
   - User profile
   - Domain knowledge scope
   - Explicit scope boundaries
   - Resource inventory

2. **Pattern Selection**
   - Chosen pattern with justification
   - Rejected patterns with reasons

3. **File Structure Plan**
   - Complete directory tree
   - File names for all files
   - Content allocation (what goes where)
   - Progressive disclosure strategy

4. **Time Estimate**
   - Overall estimate with range
   - Breakdown by component
   - Complexity factors applied
   - Buffer included

5. **Dependency Map**
   - Skill dependencies (required + optional)
   - Tool dependencies
   - Knowledge prerequisites
   - Reverse dependencies

6. **Validation Plan**
   - Structure validation method
   - Content validation checklist
   - Functional test cases
   - Usability testing approach
   - Completeness criteria

**Format**: See [templates/skill-plan-template.md](templates/skill-plan-template.md) for structured output format

---

## Best Practices

### Planning Best Practices

1. **Start with Why**
   - Clearly articulate the problem
   - Validate the need before planning
   - Consider if skill is the right solution

2. **Choose Pattern Carefully**
   - Pattern drives entire structure
   - Consider user mental model
   - Validate pattern with examples

3. **Plan for Evolution**
   - Skills will grow over time
   - Structure should accommodate additions
   - Leave room for future enhancements

4. **Optimize Context Usage**
   - Keep SKILL.md lean
   - Move details to references
   - Every word costs context tokens

5. **Validate Early**
   - Review plan before implementation
   - Get feedback from potential users
   - Adjust based on feedback

### Common Planning Mistakes

1. **Scope Creep**
   - Problem: Planning too much at once
   - Solution: Define MVP, plan iterations

2. **Wrong Pattern**
   - Problem: Choosing workflow for independent tasks
   - Solution: Use decision tree carefully

3. **Poor Progressive Disclosure**
   - Problem: Putting everything in SKILL.md
   - Solution: Follow <5,000 word guideline

4. **Underestimating Complexity**
   - Problem: Unrealistic time estimates
   - Solution: Use formula, add buffer

5. **Ignoring Dependencies**
   - Problem: Missing prerequisite skills
   - Solution: Complete dependency analysis

---

## References

Comprehensive guides for each planning step:

- **[Pattern Selection Guide](references/pattern-selection-guide.md)** - Complete decision tree with detailed examples for choosing between workflow, task, reference, and capabilities patterns. Includes edge cases and combination patterns.

- **[Structure Planning Guide](references/structure-planning-guide.md)** - Deep dive into progressive disclosure, file organization strategies, content allocation techniques, and context optimization methods.

- **[Complexity Estimation Guide](references/complexity-estimation-guide.md)** - Detailed estimation techniques, calibration data from real skills, estimation worksheets, and accuracy improvement methods.

- **[Dependency Analysis Guide](references/dependency-analysis-guide.md)** - Comprehensive dependency identification techniques, dependency mapping strategies, circular dependency resolution, and version management.

---

## Automation

Use the planning automation script for guided planning:

```bash
# Interactive planning wizard
python scripts/plan-skill.py --interactive

# Plan from description file
python scripts/plan-skill.py --description skill-description.txt

# Generate plan with specific pattern
python scripts/plan-skill.py --pattern workflow --name my-skill

# Output plan to file
python scripts/plan-skill.py --interactive --output skill-plan.md
```

See script help for all options:
```bash
python scripts/plan-skill.py --help
```

---

## Success Criteria

A successful skill plan includes:

✅ **Clear Requirements**
- Problem clearly stated
- Users identified
- Scope explicitly defined
- Resources inventoried

✅ **Justified Pattern Selection**
- Pattern chosen with clear reasoning
- Alternatives considered and rejected
- Pattern fits user mental model

✅ **Complete Structure Plan**
- All files identified
- Content allocated appropriately
- Progressive disclosure optimized
- Naming follows conventions

✅ **Realistic Estimate**
- Breakdown by component
- Complexity factors applied
- Range provided (not single number)
- Buffer included

✅ **Comprehensive Dependencies**
- All dependency types covered
- Prerequisites documented
- Reverse dependencies identified

✅ **Validation Strategy**
- Multiple validation types
- Clear pass/fail criteria
- Test cases defined
- Validation plan is actionable

---

## Next Steps

After completing skill planning:

1. **Review Plan**
   - Validate completeness
   - Get feedback if team skill
   - Adjust based on feedback

2. **Proceed to Implementation**
   - Use skill-builder-generic for implementation
   - Follow file structure from plan
   - Reference estimates for time management

3. **Track Progress**
   - Use task-development to break down implementation
   - Use todo-management to track progress
   - Adjust plan if significant deviations

4. **Validate Continuously**
   - Run validations frequently
   - Test as you build
   - Iterate based on findings

---

## Quick Reference

### The 6-Step Planning Process

| Step | Focus | Key Output | Time |
|------|-------|------------|------|
| 1. Analyze Requirements | Problem, users, scope, domain | Requirements document | 30-60m |
| 2. Choose Pattern | Workflow/task/reference/capabilities | Pattern selection with rationale | 15-30m |
| 3. Design Structure | Files, sections, progressive disclosure | File structure plan | 30-45m |
| 4. Plan Content | Section-by-section content outline | Content plan | 45-90m |
| 5. Estimate Complexity | Time, dependencies, risks | Effort estimate | 20-30m |
| 6. Create Plan Document | Consolidated implementation plan | Complete skill plan | 30-45m |

**Total Planning Time**: 3-5 hours for comprehensive plan

### The 4 Organizational Patterns

| Pattern | When to Use | Structure | Example |
|---------|-------------|-----------|---------|
| **Workflow** | Sequential dependencies, process with steps | Numbered steps (Step 1→2→3) | deployment-guide, development-workflow |
| **Task** | Independent operations, no required order | Unnumbered operations | railway-troubleshooting, review-multi |
| **Reference** | Standards, guidelines, design systems | Topic-based sections | botanical-design, common-patterns |
| **Capabilities** | Multiple related features used together | Integrated capabilities | Complex multi-feature skills |

### Pattern Selection Decision Tree

```
Do steps have sequential dependencies?
├─ Yes → WORKFLOW (use numbered steps)
└─ No → Are operations independent?
    ├─ Yes → TASK (use unnumbered operations)
    └─ No → Is it standards/guidelines?
        ├─ Yes → REFERENCE (topic-based organization)
        └─ No → CAPABILITIES (integrated features)
```

### Complexity Estimation Guidelines

| Complexity | Files | Lines | Time | Characteristics |
|------------|-------|-------|------|-----------------|
| **Simple** | 1-3 | 400-800 | 2-4h | Single file or minimal references |
| **Medium** | 4-8 | 1,500-3,000 | 8-15h | Multiple references, maybe scripts |
| **Complex** | 9-15+ | 3,000-5,000+ | 20-40h | Extensive references, automation scripts |

### Progressive Disclosure Rules

- **SKILL.md**: <1,200 lines ideal (overview + essentials)
- **references/**: 300-600 lines per file (detailed guides)
- **scripts/**: Automation tools (loaded when needed)

**Decision**: If content >1,000 lines → move detailed content to references/

### Common Planning Outputs

**Requirements Document**:
- Problem definition
- User analysis
- Scope boundaries
- Domain knowledge capture

**Structure Plan**:
- File organization
- Section outline
- Progressive disclosure strategy
- Naming conventions

**Implementation Plan**:
- Complete file-by-file breakdown
- Content specifications
- Time estimates
- Dependencies identified
- Validation criteria

### Quick Planning Checklist

- [ ] Problem clearly defined (what, who, why)
- [ ] Users identified (expertise level, context)
- [ ] Scope boundaries established (in/out of scope)
- [ ] Pattern selected with rationale
- [ ] File structure designed
- [ ] Content planned section-by-section
- [ ] Complexity estimated (simple/medium/complex)
- [ ] Dependencies identified
- [ ] Time budget allocated
- [ ] Plan document created

### For More Information

- **Requirements analysis**: See Step 1
- **Pattern selection**: See Step 2 + references/pattern-selection-guide.md
- **Structure design**: See Step 3 + references/structure-planning-guide.md
- **Content planning**: See Step 4 + references/content-specification-guide.md
- **Complexity estimation**: See Step 5 + references/complexity-assessment-guide.md

---

**planning-architect** is the foundation of systematic skill development. Use it to transform ideas into actionable implementation plans that lead to high-quality, well-structured Claude Code skills.