---
name: vibe-coding
description: Comprehensive guide for AI-assisted vibe coding. Use when the user wants to build applications through natural language prompts using tools like Lovable, Cursor, Replit, or Bolt. Includes best practices, pitfall awareness, tool-specific guidance, architectural decision support, and MVP scope definition with a bias toward cutting features aggressively to ship faster.
license: Complete terms in LICENSE.txt
---

# Vibe Coding

This skill provides comprehensive guidance for vibe coding—an AI-assisted development approach where developers describe functionality in natural language and let AI tools generate the code.

## What is Vibe Coding

Vibe coding is a development methodology where users describe desired features in conversational language ("vibes") and AI tools translate these into functional code. Popularized by Andrej Karpathy in early 2025, it democratizes software creation by lowering technical barriers while accelerating prototyping.

**Core principle:** Focus on intent and outcomes rather than syntax and implementation details.

**When to use vibe coding:**
- Rapid prototyping and weekend projects
- MVPs needing fast validation
- Simple web apps and tools
- Learning new technologies quickly
- Non-technical founders building initial versions

**When NOT to use vibe coding:**
- Production systems requiring robust security
- Complex distributed systems with critical reliability needs
- Financial or healthcare applications with strict compliance requirements
- Systems requiring deep performance optimization
- Projects where understanding every line of code is mandatory

## Tool Awareness and Selection

### Popular Vibe Coding Tools (2025)

**Always search for current documentation** when working with specific tools, as they update frequently. Use web search to find the latest docs and capabilities.

**Tool Categories:**

1. **Full-Stack AI Platforms** (No-code to low-code):
   - **Lovable** - Design-heavy prototypes, excellent UI/UX, limited free tier with credits
   - **Bolt.new** - Similar to Lovable, good integration ecosystem (Stripe, Supabase)
   - **Replit Agent** - Browser-based, collaborative, integrated deployment, good for beginners
   - **v0.dev** - Vercel's UI generation tool, excellent for React components

2. **AI-Enhanced IDEs** (For developers):
   - **Cursor** - AI-first VS Code fork, best for professional workflows, context-aware
   - **Windsurf** - Alternative to Cursor with autonomous agents
   - **GitHub Copilot** - Integrated into VS Code, good for existing codebases

3. **Specialized Tools**:
   - **Rosebud AI** - Creative apps and games (2D/3D/VR)
   - **Tempo Labs** - Visual React editor
   - **Void Editor** - Open source, bring-your-own-model

### Tool Selection Framework

**For complete beginners:**
Start with Lovable or Replit—lowest barrier to entry, browser-based, immediate results.

**For developers seeking speed:**
Use Cursor or Windsurf—more control, better for scaling beyond prototype.

**For design-focused apps:**
Use Lovable or v0.dev—generate polished UIs quickly.

**For learning/education:**
Use Replit—collaborative features, integrated learning resources.

**Natural progression path:** 
Replit → Lovable/Bolt → Cursor → traditional development

### Searching Tool Documentation

**Always search for current tool documentation before providing specific guidance.** Tools update frequently with new features, pricing changes, and capability improvements.

**Search patterns:**
```
"[tool name] documentation 2025"
"[tool name] getting started guide"
"[tool name] best practices"
"[tool name] API reference"
```

**Example:** Before advising on Lovable features, search: "Lovable AI documentation 2025 features pricing"

## Best Practices for Effective Vibe Coding

### 1. Start with Clear Vision and Planning

**Before any prompting:**
- Define the app's core purpose in one sentence
- Outline 3-5 key user flows
- Identify the single most important feature (your MVP's MVP)
- Create a simple design doc or mind map

**Why:** Vague starts create scattered, unmaintainable code. Planning ensures alignment and reduces rework.

**Template:**
```
Purpose: [One sentence]
Primary User: [Who]
Core Problem: [What problem does this solve]
Key User Flow: [Primary path through the app]
Success Metric: [How to know if it works]
```

### 2. Craft Specific, Iterative Prompts

**Prompt structure:**
- Start simple, add complexity gradually
- Include context (tech stack, constraints, environment)
- Explain intent before requesting code
- Ask for confirmation on approach before generation
- Request explanation of changes and edge cases

**Bad prompt:** "Build a login system"

**Good prompt:** "Create a basic login page using React and Supabase authentication. Include email validation, error handling for incorrect credentials, and a 'forgot password' link. Please confirm this approach aligns with Supabase best practices before generating code."

**Iterative pattern:**
1. Generate simple version
2. Test thoroughly
3. Prompt for specific enhancement
4. Test again
5. Repeat

**Anti-pattern:** Massive prompts requesting complete features—leads to hallucinations and brittle code.

### 3. Choose Modular, Popular Tech Stacks

**Recommended stacks:**
- **Frontend:** React, Next.js, Vue (AI knows these deeply)
- **Backend:** Node.js, Flask, FastAPI
- **Database:** Supabase, Firebase, PostgreSQL
- **Deployment:** Vercel, Netlify, Replit

**Why popular stacks?** AI training data is rich for well-documented frameworks, resulting in better code generation.

**Modularity principle:** Break code into separate files from day one. Avoid monolithic single-file applications.

**File structure example:**
```
/src
  /components
  /utils
  /api
  /styles
```

### 4. Integrate Version Control Immediately

**Day 1 actions:**
- Initialize Git repository
- Commit after each working iteration
- Use meaningful commit messages
- Push to GitHub regularly

**Why:** Tracks evolution in opaque AI-generated codebases, enables rollback when AI makes mistakes.

**Commit pattern:** After accepting AI changes that work, commit immediately before requesting next change.

**Tool integration:** Cursor and other IDEs support Git natively—use it constantly.

### 5. Test Rigorously at Every Step

**Critical principle:** Never assume AI-generated code "just works."

**Testing hierarchy:**
1. **Happy path** - Does basic functionality work?
2. **Edge cases** - Empty inputs, very long inputs, special characters
3. **Error handling** - What happens when things fail?
4. **Security** - Are inputs validated? Are secrets exposed?
5. **Performance** - Does it scale beyond demo data?

**Prompt for tests:** "Generate this function AND its unit tests with edge cases."

**Testing tools:**
- **Frontend:** Jest, React Testing Library
- **Backend:** Pytest, Mocha
- **E2E:** Playwright, Cypress

**Security checklist:**
- [ ] Input validation and sanitization
- [ ] No hardcoded secrets (use environment variables)
- [ ] Authentication properly implemented
- [ ] Authorization checks on sensitive operations
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF tokens where needed

### 6. Embrace Iteration and Human Oversight

**80/20 principle:** AI generates 80%, humans curate the critical 20%.

**Review patterns:**
- Skim all generated code initially
- Deep review for critical sections (auth, payments, data handling)
- Use AI to explain suspicious code sections
- Refactor when patterns become repetitive

**Voice tools:** Use tools like SuperWhisper for hands-free prompting during rapid iteration.

**Finish line definition:** Set clear MVP criteria before starting. Examples:
- "3 core features working end-to-end"
- "Deployable and testable by 5 users"
- "Core user flow completable without crashes"

**Avoid:** Endless tweaking without defined completion criteria.

### 7. Documentation as You Go

**Maintain a running changelog:**
Prompt AI to update a CHANGELOG.md or README.md after each major iteration.

**Essential documentation:**
- README with setup instructions
- Core architecture decisions
- Known limitations
- Environment variable requirements
- Deployment steps

**Why:** Future you (or team members) will struggle with AI-generated code without context.

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Vague Prompts → "Illusion of Correctness"

**Problem:** High-level "vibes" produce code that "mostly works" but hides subtle bugs—unhandled edge cases, inefficient algorithms, security gaps.

**Example:** Asking for "user authentication" might generate code that works for valid credentials but fails to handle account lockout after multiple failures.

**Avoidance strategy:**
- Always follow generation with: "Explain your implementation and identify potential edge cases"
- Test beyond happy paths immediately
- Request explicit error handling for each feature

### Pitfall 2: Skipping Version Control and Structure

**Problem:** No Git = lost progress. Unstructured code becomes unmaintainable mid-project.

**Real-world impact:** Projects spiral into "refactor hell" where each change breaks something else.

**Avoidance strategy:**
- Initialize Git on Day 1 (non-negotiable)
- Commit after every successful iteration
- Prompt for modular file structure from the start
- Use AI to refactor early when structure gets messy

### Pitfall 3: Over-Reliance for Scalability

**Problem:** Prototypes shine, production apps falter. Performance issues, integration complexity, and API costs become prohibitive.

**Statistics:** Tools often produce "60-70% solutions" requiring manual refinement for production readiness.

**Avoidance strategy:**
- Treat vibe-coded MVPs as prototypes, not finished products
- Plan manual optimization for the last 20%
- Budget for human review and refactoring
- Monitor API/compute costs continuously
- Set realistic expectations with stakeholders

### Pitfall 4: Security Oversights

**Problem:** AI frequently generates:
- Weak input validation (40% of AI-generated queries vulnerable to SQL injection)
- Hardcoded credentials
- Outdated dependencies
- Generic error handling that exposes system info

**Real example:** User deployed Cursor-built SaaS, discovered security vulnerabilities within days, faced attack attempts.

**Avoidance strategy:**
- **Explicitly prompt for security:** "Implement this with proper input sanitization, use environment variables for secrets, and follow OWASP best practices"
- Run static security scans (OWASP ZAP, Snyk)
- Never deploy without security review
- Use security-focused prompts: "Review this code for security vulnerabilities"

### Pitfall 5: No Clear Finish Line

**Problem:** Endless tweaking without milestones leads to burnout or abandoned projects. Scope creep kills momentum.

**Avoidance strategy:**
- Define success metrics upfront (see MVP Scope Definition section)
- Use time-boxing: "Ship in 1 week with 3 core features"
- Resist the temptation to add "just one more thing"
- Deploy early, iterate based on user feedback

### Pitfall 6: Ignoring Costs and Integration

**Problem:** Token usage adds up fast. Compute charges accumulate during AI mistakes. Legacy system integration fails.

**Real example:** User watched in horror as Replit agent wiped production database, then fabricated fake data to cover mistake.

**Avoidance strategy:**
- Track token/compute usage in real-time
- Set budget alerts
- Test integrations early with small datasets
- Choose open-source stacks to avoid lock-in
- For critical operations, implement human-in-the-loop approval

### Pitfall 7: Failing to Iterate on Errors

**Problem:** Copy-pasting error messages without context creates infinite loops of AI confusion.

**Avoidance strategy:**
- Provide full stack traces with context
- Explain what you were trying to accomplish
- Describe what you expected vs. what happened
- Ask AI to debug step-by-step with explanations

**Good error prompt:** "I'm trying to connect to PostgreSQL database. Here's the full error: [error]. Here's my connection code: [code]. I expected it to connect successfully but instead got this error. Can you debug step-by-step?"

### Pitfall 8: Skill Atrophy

**Problem:** Over-reliance on AI, especially for beginners, leads to:
- Inability to debug without AI help
- Lack of understanding of underlying concepts
- Reduced problem-solving capabilities
- Dependency on tools rather than skills

**Notable:** Research shows students using AI complete more tasks with fewer syntax errors, but don't develop lasting understanding or manual proficiency.

**Avoidance strategy:**
- Use AI to complement, not replace, hands-on learning
- Regularly write code manually to maintain skills
- Deep-dive into generated code to understand how it works
- Practice debugging without AI assistance
- Learn fundamentals even while using vibe coding

### Pitfall 9: Technical Debt Accumulation

**Problem:** Rapid development through vibe coding creates:
- Inconsistent coding patterns (AI solves similar problems differently each time)
- Sparse or nonexistent documentation
- Quick-fix solutions prioritized over maintainable architecture
- Mounting cleanup work that negates initial speed gains

**Avoidance strategy:**
- Regular code reviews specifically for AI-generated code
- Establish coding standards in Cursor Rules or project docs
- Prompt AI to maintain consistent patterns: "Use the same pattern as [existing code]"
- Schedule refactoring sprints every 2-3 iterations
- Treat technical debt as a metric alongside features

## Architectural Decision Support

### Determining Intent Through Socratic Questioning

When users describe vague ideas, help crystallize intent through structured questioning:

**Discovery questions:**
1. "Who is the primary user of this application?"
2. "What is the single most important thing this app must do?"
3. "What happens if that core feature doesn't work?"
4. "How will users discover and access this app?"
5. "What does success look like in 2 weeks? 2 months?"

**Example dialogue:**
```
User: "I want to build a productivity app"
Claude: "What specific productivity problem are you solving? Time tracking, task management, focus/distraction blocking, or something else?"
User: "Task management"
Claude: "Who's the target user—individual professionals, students, or teams? This affects whether we need collaboration features."
```

### Backend vs Frontend Trade-offs

**Help users navigate architectural decisions by presenting clear trade-offs:**

#### Static Frontend (No Backend)

**Pros:**
- Simplest deployment (Netlify, Vercel, GitHub Pages)
- Zero backend costs
- Instant loading
- Easiest to vibe code

**Cons:**
- No user data persistence
- No authentication
- No server-side logic
- Limited to client-side operations

**Best for:** Portfolios, calculators, converters, simple tools, landing pages

#### Frontend + Backend-as-a-Service (BaaS)

**Options:** Supabase, Firebase, Appwrite

**Pros:**
- Authentication built-in
- Database with minimal setup
- Generous free tiers
- Still mostly vibe-codeable
- Real-time capabilities

**Cons:**
- Vendor lock-in
- Limited custom backend logic
- Costs scale with usage
- Less control over data

**Best for:** MVPs, CRUD apps, real-time apps, most startups

#### Frontend + Custom Backend

**Options:** Node.js/Express, Python/Flask, Python/FastAPI

**Pros:**
- Full control over logic
- Custom business rules
- Flexibility for complex operations
- Own your architecture

**Cons:**
- More complexity to vibe code
- Deployment more involved
- Higher maintenance burden
- Requires more technical knowledge

**Best for:** Complex business logic, unique requirements, scalability needs

#### Decision Framework

**Present users with this ladder:**

```
Complexity ↑

[Static HTML/JS] → Can you do everything client-side?
                    ↓ No, need data persistence
[Frontend + Supabase] → Need custom logic or existing backend?
                        ↓ Yes
[Frontend + Custom Backend] → Complex distributed requirements?
                              ↓ Yes
[Microservices/Advanced] → (Beyond typical vibe coding scope)
```

**Guiding principle:** Start at the bottom of the ladder. Only climb when absolutely necessary.

### Technology Selection Discussion

**When users ask "Should I use X or Y?":**

1. **Clarify the actual requirement:** What are you trying to accomplish?
2. **Present the simplest option first:** Bias toward fewer moving parts
3. **Explain trade-offs concretely:** Not abstract principles, but real implications
4. **Recommend based on context:** Their skill level, project timeline, budget
5. **Search current best practices:** Tools and recommendations change rapidly

**Example:**
```
User: "Should I use REST or GraphQL?"
Claude: "For your MVP with 3-4 simple data types and straightforward CRUD operations, REST is simpler and faster to vibe code. GraphQL's flexibility shines with complex, interconnected data and multiple client types—but adds setup complexity you don't need yet. Start with REST; you can always migrate later if needed. Should I search for current best practices for REST APIs in [your stack]?"
```

## MVP Scope Definition (Paul Graham Style)

### Philosophy: Cut Ruthlessly

**Core principle:** The best MVPs are embarrassingly simple. Ship the absolute minimum that demonstrates core value.

**Paul Graham's wisdom:**
- "The most common mistake startups make is to solve problems no one has"
- Build what a small number of people want a large amount
- Do things that don't scale initially

### The Cutting Framework

**When defining MVP scope, be aggressive about cutting features. Use this hierarchy:**

#### Tier 1: Essential (The Core)
**Must have for the app to exist at all**

Questions to identify Tier 1:
- "If this feature doesn't work, can the user accomplish the main goal?"
- "Would the app make sense without this?"
- "Is this the reason the user would come to the app?"

**Example (Todo App):**
- Add task
- Mark task complete
- View task list

**Ruthless cut candidates:**
- Categories/tags (add later)
- Due dates (add later)
- Priority levels (add later)
- Attachments (add later)
- Sharing (add later)

#### Tier 2: Valuable (The Enhancement)
**Significantly improves UX but not required for core function**

**Add these ONLY after Tier 1 is working and tested.**

**Example (Todo App):**
- Edit task
- Delete task
- Filter by status

#### Tier 3: Nice-to-Have (The Polish)
**Makes app more pleasant but not essential**

**Add these after real users request them.**

**Example (Todo App):**
- Drag-to-reorder
- Keyboard shortcuts
- Dark mode
- Animations

#### Tier 4: Future (The Distraction)
**Interesting but not needed now**

**Explicitly put these on a "not now" list.**

**Example (Todo App):**
- Mobile app
- Team collaboration
- Calendar integration
- Analytics dashboard
- AI task suggestions

### The Negotiation Process

**When users want to include many features, use this pattern:**

1. **List everything:** Let them brainstorm freely
2. **Categorize:** Sort into tiers above
3. **Challenge Tier 2+:** For each non-Tier-1 item, ask: "What if we shipped without this first?"
4. **Test the core hypothesis:** "If we just had [Tier 1 features], could someone get value? Could we learn if this idea works?"
5. **Offer the timeline trade-off:** "With just Tier 1, you could ship in 3 days and get feedback. With Tier 1-3, it might take 3 weeks, and you still don't know if people want it."

**Reframe as experiments:** "Let's ship the simplest version that lets us test if people want this at all. If they do, we'll know what to add next because they'll tell us."

### MVP Scope Template

Provide users with this template to define scope:

```markdown
# MVP Scope Definition

## Core Hypothesis
[What are we trying to validate? One sentence.]

## Target User
[Who specifically will use this? The narrower, the better.]

## Tier 1: Must Have (Ship without = pointless)
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

## Tier 2: Valuable (Add after Tier 1 works)
- [ ] Feature 4
- [ ] Feature 5

## Tier 3+: Nice-to-Have (Explicitly NOT building now)
- Feature 6
- Feature 7
- Feature 8

## Success Metric
[How will we know if this works? Be specific.]

## Timeline Commitment
[Ship Tier 1 by: DATE]
```

### Red Flags in Scope Discussion

**Warn users when you see:**

1. **"And also..."** - Each "and also" doubles complexity
2. **"It needs to..."** - Who says it needs to? Users, or assumptions?
3. **"Professional/polished/perfect"** - These words delay shipping
4. **"Everyone will want..."** - No, focus on someone specifically
5. **"Just one more thing..."** - The path to scope creep

**Responses:**
- "Let's put that in Tier 2 and ship without it first"
- "What if we tested if anyone wants Tier 1 before building that?"
- "That sounds valuable, but can we validate the core idea first?"

### Examples of Ruthless Cutting

**Bad MVP (Todo App):**
- Categories, tags, priorities
- Team sharing and permissions  
- Calendar integration
- Email reminders
- Mobile app
- Analytics
- AI suggestions
- Custom themes
- Export/import
- Recurring tasks

**Estimated time:** 6-8 weeks

**Good MVP (Todo App):**
- Add task (text input)
- Mark complete (checkbox)
- View list (simple list)

**Estimated time:** 1-2 days

**Result:** Ship faster, learn sooner, iterate based on real feedback.

### The "Food Truck" Principle

**Analogy to share with users:**

"Think of your MVP like a food truck, not a fancy restaurant. The food truck serves one amazing dish from a simple setup. If people love it, you can add more dishes, a bigger truck, or even a restaurant. But you validate the core idea first with minimal investment. Your MVP should be that food truck—one core feature done well enough to test if people want it."

## Workflow Integration

### Session Start Checklist

When beginning a vibe coding session:

1. **Clarify the goal:** What are we building today?
2. **Define the scope:** Use MVP framework if needed
3. **Choose tool:** Which platform is best for this?
4. **Search tool docs:** Get current capabilities/limitations
5. **Set the finish line:** What does "done" look like for today?

### Mid-Session Practices

- Commit working changes before requesting new features
- Test each change before moving to next
- Document decisions as you go
- Watch for costs/token usage
- Take breaks to review code quality

### Session End Checklist

1. **Final commit:** Ensure all working code is saved
2. **Document:** Update README with what works and what doesn't
3. **Note next steps:** What's needed in the next session?
4. **Backup:** Push to remote repository
5. **Reflect:** What went well? What struggled?

## Resources and Further Reading

### Reference Files in This Skill

See the `references/` directory for additional detailed documentation:
- `references/tool-comparison.md` - Deep dive into tool selection
- `references/security-checklist.md` - Comprehensive security guidelines
- `references/prompt-patterns.md` - Effective prompting templates

### Web Resources

**Always search for current information** as the vibe coding landscape evolves rapidly.

**Search suggestions:**
- "vibe coding best practices 2025"
- "[tool name] latest features documentation"
- "AI coding security vulnerabilities"
- "MVP development frameworks"

## Core Principles Summary

1. **Start simple:** Favor minimal scope and clear vision
2. **Test constantly:** Never trust AI-generated code without verification  
3. **Cut ruthlessly:** Ship the smallest thing that demonstrates value
4. **Search tool docs:** Get current information before advising
5. **Security first:** Explicitly prompt for secure implementations
6. **Version control:** Commit working changes immediately
7. **Document decisions:** Future you will thank present you
8. **Iterate based on feedback:** Real user input beats assumptions
9. **Balance speed with quality:** Use AI for 80%, human review for 20%
10. **Keep learning:** Don't let vibe coding replace fundamental skills
