---
name: ai-assessment-scale
description: Evaluate AI contribution in projects using the AI Assessment Scale (AIAS) 5-level framework. Measure AI involvement from no AI to full AI exploration across development stages.
---

# AI Assessment Scale (AIAS)

This skill enables AI agents to evaluate the **level of AI contribution** in software projects using the **AI Assessment Scale (AIAS)** framework developed by Mike Perkins, Leon Furze, Jasper Roe, and Jason MacVaugh.

The AIAS provides a **5-level framework** for understanding and documenting AI's role in project development, from zero AI assistance to creative AI exploration. Originally designed for educational assessments, this framework has been adapted for software development to help teams transparently communicate AI involvement in their work.

Use this skill to assess AI contribution levels, document AI usage for transparency, and understand where human critical thinking vs AI assistance is applied throughout your project lifecycle.

## When to Use This Skill

Invoke this skill when:
- Documenting AI contribution levels in open-source projects
- Evaluating team workflows and AI tool usage
- Preparing transparency reports for stakeholders or clients
- Assessing compliance with AI disclosure requirements
- Planning AI adoption strategies in development processes
- Auditing projects for responsible AI usage
- Creating badges or documentation about AI involvement
- Understanding the balance between human expertise and AI assistance

## Inputs Required

When executing this assessment, gather:

- **project_description**: Brief description of the project (type, purpose, tech stack, team size) [REQUIRED]
- **project_url_or_codebase**: Repository URL, codebase access, or screenshots of key components [OPTIONAL but recommended]
- **development_areas**: Specific areas to assess (e.g., "backend API", "frontend UI", "documentation", "tests") [OPTIONAL]
- **ai_tools_used**: List of AI tools employed (Claude, Copilot, ChatGPT, cursor.ai, etc.) [OPTIONAL]
- **team_workflow**: Description of how AI is integrated into the development process [OPTIONAL]
- **specific_concerns**: Particular questions about AI usage or transparency requirements [OPTIONAL]

## The 5-Level AIAS Framework

The AI Assessment Scale categorizes AI usage across five distinct levels, each representing increasing AI involvement:

### **Level 1 - No AI**
**Definition**: Work completed entirely without AI assistance in a controlled environment, relying solely on existing knowledge, skills, and traditional tools.

**Characteristics:**
- Zero generative AI tool usage
- Traditional IDEs without AI features
- Manual code writing, debugging, and documentation
- Human-only research and problem-solving
- Stack Overflow, official docs, and human expertise only

**Indicators:**
- No AI-generated code or text
- No AI-assisted debugging or refactoring
- Traditional version control practices
- Manual testing and code review

**Project Example**: Legacy system maintenance using vanilla text editors and human-written documentation.

---

### **Level 2 - AI Planning**
**Definition**: AI supports preliminary activities like brainstorming, research, and planning, but final implementation is entirely human-driven.

**Characteristics:**
- AI used for ideation and exploration
- Research assistance (summarizing docs, comparing approaches)
- Architecture brainstorming
- API discovery and option evaluation
- **Critical**: All AI suggestions are evaluated, refined, and validated by humans before implementation

**Indicators:**
- AI-generated project outlines or roadmaps
- AI-assisted technology selection research
- Brainstorming session transcripts with AI
- Architecture diagrams refined from AI suggestions
- Human-written code implementing AI-researched approaches

**Project Example**: Using ChatGPT to research database options, then manually implementing PostgreSQL based on team's critical evaluation.

---

### **Level 3 - AI Collaboration**
**Definition**: AI assists with drafting code, documentation, and provides feedback during development. Humans critically evaluate, modify, and refine all AI-generated content.

**Characteristics:**
- AI generates initial code drafts
- Human developers review, test, and refine
- AI-assisted debugging and error analysis
- Co-creation of documentation
- **Critical**: Significant human modification and validation of AI outputs

**Indicators:**
- Code with AI-generated boilerplate, human-refined logic
- AI-suggested bug fixes that humans verify
- Documentation co-authored with AI assistance
- Test cases drafted by AI, validated by humans
- Commit messages showing iterative refinement

**Project Example**: Using GitHub Copilot to draft React components, then extensively refactoring for performance, accessibility, and team standards.

---

### **Level 4 - Full AI**
**Definition**: Extensive AI usage throughout development while maintaining human oversight, critical thinking, and strategic direction.

**Characteristics:**
- AI handles majority of implementation
- Humans direct AI with clear requirements
- Strategic decisions remain human-controlled
- Humans validate outputs and maintain quality standards
- AI used for routine coding, testing, refactoring
- **Critical**: Human expertise guides AI, not vice versa

**Indicators:**
- High percentage of AI-generated code (60-90%)
- Human-written specifications guiding AI implementation
- AI-powered test generation with human validation
- Automated refactoring with human approval
- Human code reviews of AI outputs
- Strategic architecture decisions by humans

**Project Example**: Using cursor.ai to implement entire API endpoints from human-written specifications, with human code review and integration testing.

---

### **Level 5 - AI Exploration**
**Definition**: Creative and experimental AI usage for novel problem-solving, pushing boundaries of what AI can accomplish in software development.

**Characteristics:**
- Cutting-edge AI techniques and workflows
- Novel AI tool combinations
- Experimental AI-driven development processes
- Co-design of solutions with AI
- AI exploring solution spaces humans might not consider
- **Critical**: Humans curate, evaluate, and select from AI's creative explorations

**Indicators:**
- Custom AI workflows or toolchains
- AI-generated architectural alternatives
- Novel use of AI for code generation or optimization
- Experimental AI pair programming techniques
- AI-discovered patterns or optimizations
- Documentation of AI exploration process

**Project Example**: Using fine-tuned LLMs to generate domain-specific DSLs, or employing AI to discover novel algorithms for complex optimization problems.

---

## Assessment Procedure

Follow these steps to evaluate AI contribution:

### Step 1: Project Discovery (10-15 minutes)

1. **Understand the project:**
   - Review `project_description`, `project_url_or_codebase`
   - Identify key development areas (frontend, backend, docs, tests, etc.)
   - Note `ai_tools_used` and `team_workflow`

2. **Identify assessment scope:**
   - Determine which components or phases to evaluate
   - Consider: planning, implementation, testing, documentation
   - Note any `specific_concerns` or transparency requirements

3. **Gather evidence:**
   - Review commit history for AI tool patterns
   - Check README, CONTRIBUTING, or AI disclosure docs
   - Look for AI-generated code markers (comments, patterns)
   - Examine code review comments mentioning AI

### Step 2: Evidence Analysis (20-30 minutes)

For each development area, assess:

#### **Planning & Architecture (10 min)**
- [ ] Was AI used for research or technology selection?
- [ ] Are there AI-generated architectural diagrams or proposals?
- [ ] Did humans critically evaluate AI suggestions?
- [ ] What level of human modification occurred?

#### **Implementation (10 min)**
- [ ] What percentage of code appears AI-generated?
- [ ] How much human refinement is evident?
- [ ] Are there signs of human validation (tests, reviews)?
- [ ] Does code follow team conventions (indicates human curation)?

#### **Testing & Quality Assurance (5 min)**
- [ ] Were tests AI-generated, human-written, or collaborative?
- [ ] Is there evidence of human test validation?
- [ ] How sophisticated are the test scenarios?

#### **Documentation (5 min)**
- [ ] Is documentation AI-generated, collaborative, or human-only?
- [ ] Does it show human refinement and contextualization?
- [ ] Is there disclosure of AI usage?

### Step 3: Level Assignment (15-20 minutes)

For each development area, assign AIAS level based on evidence:

**Decision Tree:**

1. **Was AI used at all?**
   - No → **Level 1: No AI**
   - Yes → Continue

2. **Was AI only used for planning/research?**
   - Yes (no AI in implementation) → **Level 2: AI Planning**
   - No → Continue

3. **Did AI draft code that humans significantly modified?**
   - Yes (>50% human modification) → **Level 3: AI Collaboration**
   - No → Continue

4. **Did AI generate majority of code with human oversight?**
   - Yes (60-90% AI-generated) → **Level 4: Full AI**
   - No → Continue

5. **Is AI usage novel, experimental, or exploring new approaches?**
   - Yes → **Level 5: AI Exploration**

**Cross-cutting considerations:**
- **Human critical evaluation** is present at Levels 2-5
- **Strategic control** remains human at all levels except potentially Level 5
- **Quality validation** must be human-led at Levels 3-5

### Step 4: Documentation Review (10 minutes)

Check for existing AI disclosure:
- [ ] README mentions AI usage
- [ ] CONTRIBUTING guidelines address AI tools
- [ ] LICENSE or NOTICE files include AI disclosures
- [ ] Commit messages reference AI assistance
- [ ] Code comments indicate AI generation
- [ ] Project badges or labels indicate AIAS level

### Step 5: Report Generation (20 minutes)

Compile comprehensive assessment with evidence, level assignments, and recommendations.

---

## Output Format

Generate a comprehensive AIAS evaluation report with the following structure:

```markdown
# AI Assessment Scale (AIAS) Evaluation Report

**Project**: [Name]
**Repository**: [URL]
**Date**: [Date]
**Evaluator**: [AI Agent or Human]
**AIAS Version**: 2.0 (2024)

---

## Executive Summary

### Overall AIAS Level: [Level X - Name]

**Primary AI Tools Used:**
- [Tool 1] - [Usage context]
- [Tool 2] - [Usage context]

**Key Finding**: [1-2 sentence summary of AI contribution level]

**Transparency Status**: ✅ Disclosed / ⚠️ Partially Disclosed / ❌ Not Disclosed

---

## Detailed Assessment by Development Area

### 1. Planning & Architecture
**AIAS Level**: Level [X] - [Name]

**Evidence:**
- [Evidence point 1]
- [Evidence point 2]

**Human Critical Evaluation:**
- [How humans evaluated and refined AI suggestions]

**Rationale**: [Why this level was assigned]

---

### 2. Implementation
**AIAS Level**: Level [X] - [Name]

**Evidence:**
- Code analysis: [Percentage AI-generated vs human-written]
- Commit history: [Patterns observed]

**Human Critical Evaluation:**
- [Validation and refinement processes]

**Rationale**: [Why this level was assigned]

---

### 3. Testing & Quality Assurance
**AIAS Level**: Level [X] - [Name]

**Evidence:**
- [Test coverage and generation method]

**Human Critical Evaluation:**
- [How humans validated tests]

**Rationale**: [Why this level was assigned]

---

### 4. Documentation
**AIAS Level**: Level [X] - [Name]

**Evidence:**
- [Documentation quality and generation]

**Human Critical Evaluation:**
- [Contextualization efforts]

**Rationale**: [Why this level was assigned]

---

## Transparency Assessment

### Current Disclosure Status
**Level**: [✅ Transparent / ⚠️ Partially Transparent / ❌ Not Transparent]

**What's Disclosed:**
- [Existing disclosures]

**What's Missing:**
- [ ] List missing transparency elements

### Recommended Disclosures

**1. README Badge**
```markdown
![AI Contribution](https://img.shields.io/badge/AI%20Contribution-Level%20[X]%20[Name]-[color])
```

**2. README Section**
```markdown
## 🤖 AI Transparency

This project was developed with AI assistance:

- **AIAS Level**: Level [X] - [Name]
- **Tools Used**: [List tools]
- **Human Oversight**: [Description of human review process]
- **Critical Decisions**: [Areas where humans made key decisions]
```

---

## Recommendations

### For Transparency
1. [Recommendation 1]
2. [Recommendation 2]

### For Process Improvement
1. [Recommendation 1]
2. [Recommendation 2]

---

## AIAS Badge Examples

### Level 1 - No AI
```markdown
![AI Contribution](https://img.shields.io/badge/AI%20Contribution-Level%201%20No%20AI-gray)
```

### Level 2 - AI Planning
```markdown
![AI Contribution](https://img.shields.io/badge/AI%20Contribution-Level%202%20Planning-lightblue)
```

### Level 3 - AI Collaboration
```markdown
![AI Contribution](https://img.shields.io/badge/AI%20Contribution-Level%203%20Collaboration-blue)
```

### Level 4 - Full AI
```markdown
![AI Contribution](https://img.shields.io/badge/AI%20Contribution-Level%204%20Full%20AI-darkblue)
```

### Level 5 - AI Exploration
```markdown
![AI Contribution](https://img.shields.io/badge/AI%20Contribution-Level%205%20Exploration-purple)
```

---

## Best Practices

### For Open Source Projects
1. **Be Transparent**: Clearly disclose AI usage in README
2. **Document Tools**: List AI tools used and their role
3. **Human Accountability**: Emphasize human review processes
4. **Contributor Guidelines**: Set expectations for AI-assisted contributions
5. **Badge Display**: Use AIAS badge for quick disclosure

### For Commercial Projects
1. **Client Communication**: Inform clients of AI usage level
2. **Quality Assurance**: Maintain rigorous validation processes
3. **IP Considerations**: Understand AI tool licensing implications
4. **Risk Management**: Document AI-related risks and mitigations
5. **Team Training**: Ensure team understands AI tool limitations

---

## Key Takeaways

1. **AIAS is descriptive, not prescriptive**: It measures AI usage, doesn't judge it
2. **Context matters**: Appropriate level depends on project goals and domain
3. **Transparency builds trust**: Clear disclosure enhances credibility
4. **Human oversight is critical**: At all levels, human judgment remains essential
5. **No "right" level**: Different projects benefit from different AI contribution levels

---

## Resources

### AIAS Framework
- [AI Assessment Scale Website](https://aiassessmentscale.com)
- [AIAS Version 2.0 Documentation](https://aiassessmentscale.com) (2024)
- Framework Authors: Mike Perkins, Leon Furze, Jasper Roe, Jason MacVaugh

### AI Transparency Best Practices
- [OpenAI AI Disclosure Guidelines](https://openai.com/policies/)
- [GitHub Copilot Attribution Guide](https://docs.github.com/en/copilot)

---

**Report Version**: 1.0
**Date**: [Date]
```

---

## Version

1.0 - Initial release (AIAS v2.0 adapted for software development)

---

**Remember**: The AI Assessment Scale is a framework for transparency and communication, not a quality metric. Projects at any AIAS level can be excellent or poor quality—what matters is appropriate use of AI for the context and honest disclosure of that use.
