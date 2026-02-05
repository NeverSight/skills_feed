---
name: ai-collaborate-teaching
category: "pedagogical"
applies_to: ["all-chapters"]
required_for: ["content-implementer", "chapter-planner"]
description: |
  Design learning experiences for AI-native software development, integrating the Three Roles Framework 
  (AI as Teacher/Student/Co-Worker), co-learning partnership pedagogy, and "Specs Are the New Syntax" 
  paradigm into programming curriculum. Use this skill when educators need to prepare students for 
  professional AI-driven development workflows, teach effective specification-first collaboration, or 
  balance AI assistance with foundational learning goals. This skill helps create lessons that leverage
  AI tools appropriately while ensuring students build independent capability, bidirectional learning
  patterns, and ethical AI use practices. Aligned with Constitution v4.0.1.
version: "2.1.0"
dependencies: ["constitution:v4.0.1"]
---

# AI Collaborate Teaching

## Purpose

Enable educators to design **co-learning experiences** where AI is a bidirectional learning partner following the Three Roles Framework, not just autocomplete. This skill helps:
- Teach **"Specs Are the New Syntax"** as the PRIMARY skill (not code-writing)
- Design lessons that emphasize **specification-first**, **co-learning** with AI, and **validation-before-trust**
- Establish patterns for AI pair programming in education
- Build AI tool literacy (capabilities, limitations, verification), with explicit **spec → generate → validate** loops
- Demonstrate the **Three Roles Framework** (AI as Teacher/Student/Co-Worker)
- Show **bidirectional learning** (human teaches AI, AI teaches human)
- Create ethical guidelines for responsible AI use
- Assess appropriate balance of AI integration in curriculum

## The Three Roles Framework (Section IIa Stage 2, Constitution v5.0.0)

**CRITICAL**: All co-learning content MUST demonstrate this framework (per Section IIa Stage 2 forcing functions):

### AI's Three Roles:
1. **Teacher**: Suggests patterns, architectures, best practices students may not know
2. **Student**: Learns from student's domain expertise, feedback, corrections
3. **Co-Worker**: Collaborates as peer, not subordinate

### Human's Three Roles:
1. **Teacher**: Guides AI through clear specifications, provides domain knowledge
2. **Student**: Learns from AI's suggestions, explores new patterns
3. **Orchestrator**: Designs collaboration strategy, makes final decisions

### The Convergence Loop

**Required Pattern for All AI-Integrated Lessons:**

```
┌─────────────────────────────────────────────────────────┐
│  1. Human specifies intent (with context/constraints)   │
│  2. AI suggests approach (may include new patterns)     │
│  3. Human evaluates AND LEARNS ("I hadn't thought of X")│
│  4. AI learns from feedback (adapts to preferences)     │
│  5. CONVERGE on optimal solution (better than either    │
│     could produce alone)                                 │
└─────────────────────────────────────────────────────────┘
```

**Content Requirements:**
- ✅ At least ONE instance per lesson where student learns FROM AI's suggestion
- ✅ At least ONE instance where AI adapts TO student's feedback
- ✅ Convergence through iteration (not "perfect on first try")
- ✅ Both parties contributing unique value
- ❌ NEVER present AI as passive tool awaiting commands
- ❌ NEVER show only human teaching AI (one-way instruction)
- ❌ NEVER hide what student learns from AI's approaches

## Relationship to Graduated Teaching Pattern (Constitution Principle 13)

**This skill complements the graduated teaching pattern:**

**Graduated Teaching Pattern** (Constitution Principle 13) defines **WHAT book teaches vs WHAT AI handles:**
- **Tier 1:** Book teaches foundational concepts (stable, won't change)
- **Tier 2:** AI companion handles complex execution (student specifies, AI executes)
- **Tier 3:** AI orchestration at scale (10+ items, multi-step workflows)

**This skill (AI Collaborate Learning)** defines **HOW students use AI during learning:**
- When AI is involved (from Pattern Tier 2+), students use AI collaboration patterns (explainer, debugger, pair programmer)
- Balance AI-assisted work with independent verification (40/40/20 model)
- Apply ethical guidelines and verification strategies

**In Practice:**
```
1. Book teaches Markdown # headings (Tier 1 - foundational)
   → Students practice manually
   → No AI collaboration patterns needed yet

2. Students learn Markdown tables (Tier 2 - complex syntax)
   → AI companion handles table generation
   → Now apply AI collaboration patterns from this skill:
     - Student specifies table requirements
     - AI generates table
     - Student validates output
     - Student can ask AI to explain syntax (AI as Explainer)

3. Students convert 10 documents (Tier 3 - orchestration)
   → AI orchestrates batch conversion
   → Apply AI pair programming pattern (AI as Pair Programmer)
   → Maintain 40/40/20 balance with verification checkpoints
```

**Key Integration Points:**

**With 4-Layer Method (Section IIa):**
- Layer 1 (Manual practice): Minimal AI collaboration — build independent capability first
- Layer 2-4 (AI-assisted onward): Apply this skill's collaboration patterns

**With Graduated Teaching (Principle 2):**
- Tier 1 (Foundational): Book teaches directly — minimal AI patterns needed
- Tier 2 (Complex): AI companion handles — apply this skill's collaboration patterns
- Tier 3 (Scale): AI orchestration — full pair programming with strategic oversight

Refer to Section IIa (4-Layer Method) and Principle 2 (Graduated Teaching) for decisions about WHEN and WHAT. Use this skill for HOW students collaborate with AI effectively.

## When to Activate

Use this skill when:
- Designing programming courses that integrate AI coding assistants
- Teaching students to use AI tools (ChatGPT, GitHub Copilot, Claude) effectively
- Creating prompt engineering curriculum or exercises
- Establishing policies for AI use in programming education
- Balancing AI assistance with independent skill development
- Assessing whether AI integration enhances or hinders learning
- Educators ask about "AI in teaching", "prompt engineering pedagogy", "AI pair programming", "AI tool literacy"
- Reviewing existing AI-integrated curricula for improvements

## Process

### Step 1: Understand the Educational Context

When a request comes in to integrate AI into programming education, first clarify:
- **What programming topic or course?** (Intro to Python, web development, data structures, etc.)
- **What is the student level?** (Complete beginners, intermediate, advanced)
- **What AI tools are available?** (ChatGPT, GitHub Copilot, Claude, other)
- **What are the learning objectives?** (What should students be able to do?)
- **What foundational skills must be built independently?** (Core concepts that shouldn't use AI)
- **What ethical concerns exist?** (Academic integrity, over-reliance, attribution)

### Step 2: Review Prompt Engineering Pedagogy

Learn how to teach students to craft effective prompts:
📖 [reference/prompt-engineering-pedagogy.md](reference/prompt-engineering-pedagogy.md)

This document covers:
- **Four Prompt Competencies**: Context setting, constraint specification, output format, iterative refinement
- **Teaching Prompt Quality**: Clarity, specificity, context completeness, testability
- **Scaffolding Strategies**: Templates (beginner), critique (intermediate), independent crafting (advanced)
- **Common Anti-Patterns**: Vague requests, assuming AI knows context, overloading prompts, passive acceptance
- **Assessment Strategies**: Prompt journals, prompt challenges, peer review

**Key Insight**: Prompt engineering is about effective communication, problem specification, and critical evaluation - all valuable software engineering skills.

### Step 3: Design AI Pair Programming Patterns

Review how students can work with AI as a collaborative partner:
📖 [reference/ai-pair-programming-patterns.md](reference/ai-pair-programming-patterns.md)

This document covers five patterns:
- **Pattern 1: AI as Explainer** - Student inquires, AI clarifies concepts
- **Pattern 2: AI as Debugger** - Student reports bugs, AI helps diagnose
- **Pattern 3: AI as Code Reviewer** - Student writes code, AI provides feedback
- **Pattern 4: AI as Pair Programmer** - Student and AI co-create code incrementally
- **Pattern 5: AI as Hypothesis Validator** - Student forms hypotheses, AI confirms/refutes

**Critical Balance**: Student should understand and own all code, not just copy-paste AI output.

**Teaching Strategies**:
- Scaffold from guided templates to independent use
- Require students to explain all code (even AI-generated)
- Include AI-free checkpoints to verify learning
- Balance assistance with independent struggle

### Step 4: Build AI Tool Literacy

Teach students to understand AI capabilities and limitations:
📖 [reference/ai-tool-literacy.md](reference/ai-tool-literacy.md)

This document covers:
- **What AI Does Well**: Pattern recognition, code generation, explanation, refactoring, debugging common issues
- **What AI Does Poorly**: Complex domain logic, system design, originality, understanding unstated context, comprehensive security
- **Conceptual Understanding**: AI is pattern recognition from training data, not logical reasoning
- **Verification Strategies**: Read/understand, test thoroughly, code review, cross-check documentation, run and observe
- **When to Trust**: High confidence for well-known patterns, low confidence for security/performance/complex logic
- **Recognizing Biases**: Recency, popularity, correctness, cultural, representation biases

**Key Principle**: Trust, but verify - always.

### Step 5: Establish Ethical Guidelines

Create clear ethical frameworks for AI use:
📖 [reference/ethical-ai-use.md](reference/ethical-ai-use.md)

This document covers seven ethical principles:
1. **Honesty and Transparency**: Disclose AI assistance
2. **Academic Integrity**: AI enhances learning, doesn't substitute for it
3. **Attribution and Credit**: Give credit where due
4. **Understanding Over Outputs**: Never submit code you don't understand
5. **Bias Awareness**: Recognize AI limitations and biases
6. **Over-Reliance Prevention**: Maintain independent coding ability
7. **Professional Responsibility**: You're accountable for all code

**Teaching Strategies**:
- Set explicit policies early (Week 1)
- Discuss ethical dilemmas regularly
- Model ethical AI use
- Require process documentation (when/why AI was used)
- Include AI-free assessments periodically

### Step 6: Design AI-Integrated Lesson

Use the lesson template to structure AI integration:
📄 [templates/ai-lesson-template.yml](templates/ai-lesson-template.yml)

The template includes:
- **Lesson Metadata**: Topic, duration, audience, AI integration level
- **Learning Objectives**: With AI role specified for each
- **Foundational vs. AI-Assisted Skills**: What must be learned independently vs. with AI help
- **Lesson Phases**:
  - **Introduction** (no AI): Motivation and prerequisites
  - **Foundation** (no AI): Build core concepts independently first
  - **AI-Assisted Exploration** (with AI): Practice and explore with scaffolding
  - **Independent Consolidation** (no AI): Verify learning without AI
  - **Wrap-Up**: Reflection and discussion
- **AI Integration Strategy**: Tools, guidelines, prompt templates, disclosure requirements
- **Balance Assessment**: 40% foundational / 40% AI-assisted / 20% verification (target ratio)
- **Ethical Considerations**: Policies, prohibited actions, verification requirements

**Key Structure**: Always start with independent foundation, allow AI assistance with scaffolding, verify learning independently.

### Step 7: Create Effective Prompt Templates

Provide students with templates for different tasks:
📄 [templates/prompt-design-template.md](templates/prompt-design-template.md)

This template provides structures for:
- **Basic Prompt Structure**: Context + Task + Constraints
- **Detailed Prompt Template**: With focus areas and output format specs
- **Task-Specific Templates**: Code generation, explanation, debugging, code review, alternatives
- **Anti-Patterns**: What to avoid
- **Prompt Quality Checklist**: Verify before submission

**Teaching Approach**: Start with templates, gradually remove scaffolding as students gain expertise.

### Step 8: Assess AI Integration Balance

Once a lesson is designed, validate the AI integration:

```bash
python .claude/skills/ai-augmented-teaching/scripts/assess-ai-integration.py lesson-plan.yml
```

**The script assesses**:
- ✅ **Balance**: Is the ratio appropriate (foundation/AI-assisted/verification)?
- ✅ **Foundational Skills**: Are core skills protected from AI assistance?
- ✅ **Verification**: Are there checkpoints to test learning without AI?
- ✅ **Ethical Guidelines**: Are disclosure, understanding, and verification required?

**Interpret Results**:
- **Overall Score**: 90+ (Excellent), 75-89 (Good), 60-74 (Needs Improvement), <60 (Poor)
- **Balance Issues**: Adjust percentages if too much/little AI assistance
- **Missing Verification**: Add independent checkpoints
- **Ethical Gaps**: Include disclosure requirements, understanding checks

**If score is low**:
1. Review recommendations
2. Adjust lesson phases (add independent work or verification)
3. Clarify foundational vs. AI-assisted skills
4. Add ethical guidelines
5. Re-assess until score improves

### Step 9: Validate Prompt Quality

For prompt engineering exercises, validate prompt quality:

```bash
python .claude/skills/ai-augmented-teaching/scripts/validate-prompts.py prompts.yml
```

**The script checks**:
- **Clarity**: Is the prompt specific and clear?
- **Context**: Does it provide adequate background?
- **Task Specification**: Is the requested task explicit?
- **Testability**: Can the output be verified?
- **Constraints**: Are requirements and limitations specified?

**Interpret Results**:
- **Quality Score**: 85+ (Excellent), 70-84 (Good), 50-69 (Needs Improvement), <50 (Poor)
- **Suggestions**: Specific improvements for each prompt
- **Common Issues**: Vague language, missing context, unclear tasks

**Use for**:
- Evaluating student-written prompts
- Improving prompt templates
- Teaching prompt quality criteria

### Step 10: Iterate and Refine

After teaching with AI integration:
1. **Gather Feedback**: What worked? What didn't?
2. **Assess Learning**: Did students achieve objectives independently?
3. **Check for Over-Reliance**: Can students code without AI?
4. **Review Ethical Use**: Were guidelines followed?
5. **Adjust Balance**: Increase/decrease AI assistance based on outcomes

## Output Format

Present AI-integrated lesson plans following the ai-lesson-template.yml structure:

```yaml
lesson_metadata:
  title: "Lesson Title"
  topic: "Programming Topic"
  duration: "90 minutes"
  ai_integration_level: "Medium"

learning_objectives:
  - statement: "Students will be able to [action]"
    ai_role: "Explainer | Pair Programmer | Code Reviewer | None"

foundational_skills_focus:
  - "Core skill 1 (no AI)"
  - "Core skill 2 (no AI)"

ai_assisted_skills_focus:
  - "Advanced skill 1 (with AI)"
  - "Advanced skill 2 (with AI)"

phases:
  - phase_name: "Foundation (Independent)"
    ai_usage: "None"
    activities: [...]

  - phase_name: "AI-Assisted Exploration"
    ai_usage: "Encouraged"
    activities: [...]

  - phase_name: "Independent Consolidation"
    ai_usage: "None"
    activities: [...]

ai_assistance_balance:
  foundational_work_percentage: 40
  ai_assisted_work_percentage: 40
  independent_verification_percentage: 20
```

## Acceptance Checks

- [ ] Spectrum tag specified for the lesson: Assisted | Driven | Native
- [ ] Spec → Generate → Validate loop outlined for AI usage
- [ ] At least one “verification prompt” included to force the model to explain/test its own output

### Verification prompt examples
```
- “Explain why this output satisfies the acceptance criteria from the spec.”
- “Generate unit tests that would fail if requirement X is not met.”
- “List assumptions you made; propose a test to verify each.”
```

## Examples

### Example 1: Intro to Python Functions (Beginner)

**Context**: Teaching functions to absolute beginners

**AI Integration Strategy**:

```yaml
lesson_metadata:
  title: "Introduction to Python Functions"
  duration: "90 minutes"
  target_audience: "Beginners"
  ai_integration_level: "Low"

foundational_skills_focus:
  - "Understanding function syntax (def, parameters, return)"
  - "Tracing function execution mentally"
  - "Writing simple functions independently"

ai_assisted_skills_focus:
  - "Exploring function variations"
  - "Generating test cases"
  - "Getting alternative implementations"

phases:
  - phase_name: "Foundation (30 min, No AI)"
    activities:
      - Introduce function concepts (lecture)
      - Work through examples on board
      - Students write 3 simple functions independently
      - Quick comprehension check

  - phase_name: "AI-Assisted Practice (40 min)"
    activities:
      - Students use AI to explain functions they don't understand
      - Request AI help generating test cases
      - Ask AI for alternative approaches
      - All AI usage must be documented

  - phase_name: "Independent Verification (15 min, No AI)"
    activities:
      - Write 2 functions without AI assistance
      - Explain what each function does
      - Prove they can code functions independently

ai_assistance_balance:
  foundational: 40%
  ai_assisted: 45%
  verification: 15%
```

**Rationale**: Beginners need strong foundation before AI assistance. Mostly independent work.

---

### Example 2: Web API Integration (Intermediate)

**Context**: Teaching how to integrate external APIs

**AI Integration Strategy**:

```yaml
lesson_metadata:
  title: "Integrating REST APIs in Python"
  duration: "2 hours"
  target_audience: "Intermediate"
  ai_integration_level: "High"

foundational_skills_focus:
  - "Understanding HTTP methods (GET, POST, PUT, DELETE)"
  - "Reading API documentation"
  - "Handling JSON responses"

ai_assisted_skills_focus:
  - "Crafting API requests with authentication"
  - "Error handling for network issues"
  - "Building robust API clients"

phases:
  - phase_name: "Foundation (25 min, No AI)"
    activities:
      - Review HTTP basics
      - Demonstrate simple API call with requests library
      - Students make first API call independently

  - phase_name: "AI-Assisted Building (60 min)"
    activities:
      - Use AI as pair programmer to build API client
      - Request AI help with authentication patterns
      - Ask AI to suggest error handling strategies
      - Students build incrementally with AI assistance

  - phase_name: "Independent Consolidation (25 min, No AI)"
    activities:
      - Extend API client with new endpoint (no AI)
      - Debug intentionally broken API call
      - Explain all code including AI-generated parts

ai_assistance_balance:
  foundational: 25%
  ai_assisted: 55%
  verification: 20%
```

**Rationale**: Intermediate students can handle more AI integration. Foundation is brief since they know Python basics.

---

### Example 3: Prompt Engineering Bootcamp (Advanced)

**Context**: Teaching prompt engineering as a skill

**AI Integration Strategy**:

```yaml
lesson_metadata:
  title: "Mastering Prompt Engineering for Code"
  duration: "3 hours"
  target_audience: "Advanced"
  ai_integration_level: "High"

foundational_skills_focus:
  - "Understanding prompt structure (context/task/constraints)"
  - "Identifying vague vs. specific prompts"
  - "Recognizing AI capabilities and limitations"

ai_assisted_skills_focus:
  - "Iterative prompt refinement"
  - "Crafting complex multi-step prompts"
  - "Effective code review requests"

phases:
  - phase_name: "Prompt Quality Foundation (30 min, No AI)"
    activities:
      - Analyze good vs. bad prompts
      - Practice prompt critique
      - Learn quality criteria (clarity, context, testability)

  - phase_name: "Iterative Prompt Design (90 min, With AI)"
    activities:
      - Students write prompts for complex tasks
      - Test prompts with AI, evaluate outputs
      - Refine prompts based on results
      - Compare approaches with peers

  - phase_name: "Prompt Challenge (30 min, No AI first)"
    activities:
      - Design prompts for given scenarios (no AI)
      - Then test prompts with AI
      - Evaluate: Did prompts produce useful outputs?
      - Reflect on prompt quality and effectiveness

ai_assistance_balance:
  foundational: 20%
  ai_assisted: 60%
  verification: 20%
```

**Rationale**: Advanced students learning prompt engineering should spend most time experimenting with AI. But they must demonstrate prompt design skills independently first.

---

## Common Patterns

### Pattern 1: 40/40/20 Balance (Standard)

```
40% Foundation (no AI): Build core skills independently
40% AI-Assisted: Practice and explore with AI support
20% Verification (no AI): Prove independent capability
```

**Use for**: Most programming lessons for intermediate students

---

### Pattern 2: 60/20/20 Balance (Beginner-Heavy)

```
60% Foundation (no AI): Extensive independent skill-building
20% AI-Assisted: Limited, scaffolded AI use
20% Verification (no AI): Ensure basics are solid
```

**Use for**: Absolute beginners, core foundational concepts

---

### Pattern 3: 25/55/20 Balance (Advanced Integration)

```
25% Foundation (no AI): Brief independent practice
55% AI-Assisted: Heavy AI collaboration
20% Verification (no AI): Confirm understanding
```

**Use for**: Advanced students, exploring new libraries/frameworks

---

## Troubleshooting

### Assessment Shows Poor Balance (<60 score)

**Problem**: assess-ai-integration.py reports low score

**Common Issues**:
1. Too much AI assistance (>60%) - Students won't build independent skills
2. Too little verification (<15%) - No way to confirm learning
3. No foundational phase - Students use AI from the start
4. Missing ethical guidelines

**Solutions**:
1. Add foundational phase (no AI) at the beginning
2. Reduce AI-assisted percentage to 30-50%
3. Add independent verification phase at end
4. Include disclosure requirements and ethical guidelines
5. Re-assess until score improves to 75+

---

### Students Over-Rely on AI

**Problem**: Students can't code without AI assistance

**Indicators**:
- Panic when AI unavailable
- Can't explain AI-generated code
- Performance drops significantly on AI-free assessments

**Solutions**:
1. **Increase AI-Free Time**: More foundational and verification phases
2. **20-Minute Rule**: Students must try independently for 20 min before AI
3. **Progressive Independence**: Gradually reduce AI assistance over semester
4. **Regular AI-Free Assessments**: Verify retention of skills

---

### Prompts Are Low Quality (<50 score)

**Problem**: validate-prompts.py reports poor quality prompts

**Common Issues**:
- Too vague: "Write code for sorting"
- No context: "Fix this" [paste code]
- No testability: Can't verify if output is correct
- Missing constraints: No requirements specified

**Solutions**:
1. **Teach Prompt Structure**: Context + Task + Constraints + Output Format
2. **Provide Templates**: Scaffold with fill-in-the-blank templates
3. **Prompt Critique Practice**: Analyze good vs. bad prompts
4. **Iterative Refinement**: Show how to improve prompts based on results

---

### Ethical Violations Occur

**Problem**: Students use AI without disclosure, submit code they don't understand

**Prevention**:
1. **Set Policy Early**: Week 1, explicit guidelines
2. **Require Documentation**: Students log all AI use
3. **Explanation Requirement**: Must explain all code (including AI-generated)
4. **AI-Free Assessments**: Periodically verify independent capability
5. **Consequences**: Clear penalties for violations

---

## Teaching Agentic AI and Advanced Topics

As curriculum evolves to include agentic AI systems and Model Context Protocol (MCP), teaching strategies shift:

### Special Considerations for Agentic AI

**Agentic AI differs from traditional AI assistance:**
- Students are designing AGENTS (goal-seeking systems), not just using AI as a code generator
- Agency and autonomy introduce new concepts: agent goals, decision-making, state management, tool selection
- Students must understand agent behavior at a deeper level (not just "give it a prompt")

**Teaching Agentic AI Effectively:**

1. **Start with Agent Concepts** (Not Just Prompting)
   - Begin with what agents ARE and why they differ from traditional AI use
   - Use diagrams showing agent loops: perceive → decide → act → repeat
   - Compare agents with traditional chatbots (students often conflate them)

2. **Build Agent Design Gradually**
   - First agents: simple goal-seeking with 2-3 available tools
   - Mid-level: agents with state management and complex goals
   - Advanced: agent orchestration and multi-agent systems

3. **Include Failure Analysis**
   - Agents often fail or loop - teach students to recognize and debug these
   - Log analysis exercises: "Why did the agent pick the wrong tool?"
   - Improvement exercises: "How would you change the goal/tools to fix this?"

4. **Emphasize Agent Testing and Safety**
   - Simple prompts can work fine; complex agents need careful testing
   - Teach students to set boundaries and constraints for agents
   - Include cost monitoring (API calls can add up with agents!)

5. **Real-World Agent Projects**
   - Research assistant agent
   - Data processing agent
   - System administration agent
   - Customer support agent
   - Each demonstrates different agent patterns and challenges

### Special Considerations for MCP (Model Context Protocol)

**MCP extends traditional AI assistance:**
- MCP servers provide tools/resources that models can access
- Students learn to integrate external capabilities into AI systems
- Bridge between application development and AI enhancement

**Teaching MCP Effectively:**

1. **Start with Architecture Understanding**
   - Draw diagrams: Client ← Protocol → Server
   - Explain what servers can provide (tools, resources, data access)
   - Compare with traditional APIs (similar but bidirectional communication)

2. **Learn Existing MCP Servers First**
   - Install and integrate established MCP servers
   - Understand how applications use MCP
   - Build confidence with known tools before creating custom ones

3. **Build Custom MCP Servers**
   - Start simple: single-purpose server with 2-3 tools
   - Progress to complex: multi-tool servers with state management
   - Industry example: build an MCP server for your domain (database access, API wrapper, etc.)

4. **Integrate MCP + Agents**
   - Advanced students can build agents that use MCP servers
   - Students appreciate how MCP provides reliable tool access for agents
   - Real problem-solving: agent + MCP creates powerful combinations

5. **Emphasize Reusability**
   - Well-designed MCP servers are reusable across projects
   - Teach documentation: others should be able to use your server
   - Portfolio value: publishing MCP servers shows engineering maturity

---

## Integration with Other Skills

This skill works well with:

**→ learning-objectives skill**: Define what students should achieve, then decide what AI role supports those objectives

**→ exercise-designer skill**: Create exercises that balance AI assistance with independent practice

**→ assessment-builder skill**: Design assessments measuring understanding (not just code completion)

**→ code-example-generator skill**: Generate examples, then teach students to use AI similarly

---

## Tips for Success

1. **Start with Foundation**: Always build core skills independently before AI
2. **Balance is Critical**: 40/40/20 is a good starting ratio
3. **Verify Learning**: AI-free checkpoints are non-negotiable
4. **Teach Verification**: Students must test and understand AI outputs
5. **Model Ethical Use**: Demonstrate how YOU use AI responsibly
6. **Iterate Prompts**: First prompts are rarely perfect
7. **Document Everything**: Require students to log AI usage
8. **Maintain Independence**: Periodic AI-free work ensures skills remain
9. **Discuss Ethics Often**: Not just Week 1 - ongoing conversations
10. **Adapt to Context**: Beginners need more foundation, advanced students can handle more AI

---

**Ready to design AI-integrated curriculum?** Provide:
- Programming topic and level
- Student audience (beginner/intermediate/advanced)
- Available AI tools
- Learning objectives
- Current concerns (over-reliance, academic integrity, etc.)

Or share an existing lesson plan and I'll assess AI integration balance and suggest improvements!
