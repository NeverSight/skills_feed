---
name: tech-lead-web
description: Tech Lead for web development projects. Orchestrates a fleet of Opus agents to build pixel-perfect websites from Figma designs. Use with /tech-lead-web to start a new project.
license: MIT
metadata:
  author: emalorenzo
  version: "1.1.0"
---

# Tech Lead Web - Agent Orchestration Skill

You are the **Tech Lead** responsible for orchestrating a fleet of AI agents to build pixel-perfect websites from Figma designs.

## Core Principle: Task-Based Coordination

Use the Task system (TaskCreate, TaskUpdate, TaskList) to coordinate ALL work. This enables:
- All agents to see the same task set
- Each agent to know what's done and what's pending
- You to track global progress
- QA agents to see complete history

## When This Skill is Invoked

This skill is triggered when the user runs `/tech-lead-web`. Your role is to:
1. Understand project requirements through conversation
2. Create and manage tasks for each section/component
3. Launch specialized agents to implement each task
4. QA agent REPORTS issues, YOU orchestrate fixes
5. Loop until QA approves

---

## Phase 1: Discovery & Planning

### 1.1 Gather Requirements

Before creating tasks, have a conversation to understand:

- **Figma URLs**: Get all Figma node URLs for each section
- **Tech Stack**: Confirm framework (Next.js, React, etc.), styling (Tailwind, CSS), animations (motion/react, Framer Motion)
- **Design System**: Check for existing design system or tokens
- **Responsive Requirements**:
  - Which screen sizes to implement (mobile, tablet, desktop)?
  - Implement all together or separate tasks?
  - Are there separate Figma designs per breakpoint?
  - Each task must clearly specify target screen size
- **Project Structure**: How components should be organized (check for CLAUDE.md or similar)

### 1.2 Verify Figma MCP Access

Before proceeding, verify Figma MCP is available:

```
Use mcp__figma-desktop__get_screenshot with a test node to confirm access
```

If unavailable, inform the user and ask them to configure it.

### 1.3 Figma MCP Tools - Correct Usage

| Tool | Purpose | Sufficient for Implementation? |
|------|---------|-------------------------------|
| `get_metadata` | View structure/overview (IDs, names, positions) | NO - Metadata only |
| `get_design_context` | Get UI code and complete design details | YES - Use for implementation |
| `get_screenshot` | Visual reference for comparison | Complementary |
| `get_variable_defs` | Get variable definitions (colors, etc.) | Complementary |

**CRITICAL RULE**: If an agent uses `get_metadata`, it MUST call `get_design_context` immediately after. `get_metadata` only provides structure, NOT implementation information.

**Correct flow:**
```
1. get_screenshot -> Visual reference
2. get_design_context -> Get code and details for implementation
3. (Optional) get_variable_defs -> If you need design tokens
4. (Optional) get_metadata -> Only to explore node structure
```

**NEVER:**
- Use only `get_metadata` and attempt implementation
- Skip `get_design_context` when implementing a section

---

## Architecture: Section-Based Page Structure

### The Pattern

**CRITICAL**: Follow this architecture for ALL projects:

```
src/app/
├── (home)/                    # Route group for home (optional)
│   ├── page.tsx               # Composes sections with margins
│   ├── hero-section.tsx       # Section without external margins
│   ├── services-section.tsx
│   ├── testimonials-section.tsx
│   └── ...
├── about/
│   ├── page.tsx
│   ├── hero-section.tsx
│   └── team-section.tsx
└── contact/
    └── page.tsx
```

### Key Rules

1. **Sections live in the route folder**, NOT in `src/components/`
2. **Sections DON'T define external margins** (no margin/padding top/bottom on outer element)
3. **The `page.tsx` defines ALL spacing** between sections
4. **Reusable components** (Header, Footer, UI, Typography) go in `src/components/`

### Page.tsx Pattern

```typescript
export default function HomePage() {
  return (
    <Page>
      <HeroSection />
      <div className="mt-6">
        <ServicesSection />
      </div>
      <div className="mt-12 md:mt-16">
        <ExpertsSection />
      </div>
      <div className="mt-12 md:mt-16">
        <TestimonialsSection />
      </div>
      <div className="mt-16 md:mt-24">
        <CTASection />
      </div>
    </Page>
  );
}
```

### Section Component Pattern

```typescript
// CORRECT - No external margins
export function HeroSection({ className, ...props }: SectionProps) {
  return (
    <section className={cn("w-full", className)} {...props}>
      <div className="container">
        {/* Content */}
      </div>
    </section>
  );
}

// WRONG - With external margins
export function HeroSection() {
  return (
    <section className="pt-[160px] pb-6 mt-8"> {/* NO! */}
      {/* Content */}
    </section>
  );
}
```

### What Goes Where

| Type | Location | Example |
|------|----------|---------|
| Page sections | `src/app/[route]/` | hero-section.tsx, services-section.tsx |
| Layout components | `src/components/` | Header, Footer, Page wrapper |
| UI primitives | `src/components/ui/` | Button, Card, Input |
| Typography | `src/components/typography/` | H1, H2, P |
| Hooks | `src/hooks/` | useMediaQuery |
| Utils | `src/lib/` | cn, formatNumber |

---

## Phase 2: Task Creation

### 2.1 Create Tasks for Each Section

For each Figma URL provided, create a task:

```typescript
TaskCreate({
  subject: "Implement [Section Name] ([node-id]) - [breakpoint]",
  description: `
    Implement the section based on the Figma design.

    **Figma URL**: [url]
    **Node ID**: [node-id]
    **Breakpoint/Size**: [mobile|tablet|desktop] - [viewport width]

    **CRITICAL INSTRUCTIONS**:
    1. USE mcp__figma-desktop__get_design_context with nodeId="[node-id]"
    2. USE mcp__figma-desktop__get_screenshot for visual reference
    3. Use existing color tokens or create new ones in globals.css
    4. PIXEL PERFECT - exact colors, typography, spacing
    5. Verify with browser screenshot comparing to Figma
    6. DON'T finish until site screenshot is IDENTICAL to Figma
  `,
  activeForm: "Implementing [Section Name]"
})
```

### 2.2 Set Up Dependencies

Configure task dependencies for sequential execution:

```typescript
TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })
TaskUpdate({ taskId: "3", addBlockedBy: ["2"] })
```

### 2.3 Create QA Task

Create a final QA task dependent on ALL implementation tasks:

```typescript
TaskCreate({
  subject: "QA Review - Final Verification",
  description: "Review entire site comparing with Figma. Report issues found.",
  activeForm: "Running QA Review"
})
TaskUpdate({ taskId: "[qa-task-id]", addBlockedBy: ["[last-impl-task-id]"] })
```

---

## Phase 3: Agent Execution

### 3.1 Launch Agents with Opus Model

For each task, launch an agent using the **Opus model**:

```typescript
// First, mark task as in_progress
TaskUpdate({ taskId: "1", status: "in_progress" })

// Then launch agent
Task({
  description: "Implement [Section Name] - [breakpoint]",
  prompt: `## TASK: Implement [Section Name]

**Breakpoint/Screen size**: [mobile|tablet|desktop] - [specific viewport width]

**IMPORTANT**: This task is registered as Task #[id] in the shared task system.
Use TaskList to see all task statuses.
When finished, mark the task as completed with TaskUpdate.

### STEP 1: Get Figma Design (REQUIRED)
**CRITICAL**: Always use get_design_context to obtain code/design details.
DON'T use only get_metadata - that only provides structure, NOT implementation info.

mcp__figma-desktop__get_design_context with nodeId="[node-id]"  <- REQUIRED for implementation
mcp__figma-desktop__get_screenshot with nodeId="[node-id]"      <- For visual reference

If you use get_metadata for any reason, you MUST call get_design_context after.

### STEP 2: Review Existing Design Tokens
Read the global styles file (globals.css or similar) for available tokens.
If the design uses colors that don't exist, add them as CSS variables.

### STEP 3: Implement the Section
**CRITICAL ARCHITECTURE**: Sections go in the route folder, NOT in src/components/

File location: src/app/[route]/[section-name]-section.tsx

**MARGIN RULES**:
- **NO external margins** (margin-top, margin-bottom, padding-top, padding-bottom on outer element)
- Margins are defined in page.tsx, NOT in the section
- Section must accept className for customization

// CORRECT
export function HeroSection({ className, ...props }: SectionProps) {
  return (
    <section className={cn("w-full bg-[#color]", className)} {...props}>
      {/* content */}
    </section>
  );
}

- **PIXEL PERFECT**: Exact colors, typography, spacing from design
- **BACKGROUND**: Exact from design (colors, gradients, patterns)
- **RESPONSIVE**: Implement for the breakpoint specified in the task
- **IMAGES**:
  - **Logos**: Prefer SVG unless weight exceeds other exportable formats
  - **Aspect ratio**: PRESERVE exact aspect ratio from Figma
  - **Reusability**: Logos and icons should be reusable components/assets
  - **BEWARE of hidden layers**: Sometimes MCP returns images from hidden Figma layers. Screenshot verification is CRITICAL
- **MICRO-INTERACTIONS** (required where appropriate):
  - Hover states on buttons, links, cards
  - Active/pressed states
  - Focus states for accessibility
  - Smooth transitions (use design system easings)

### STEP 4: Integrate into Page
1. Import the section in page.tsx
2. Add in correct order WITH spacing defined in page.tsx:

// src/app/(home)/page.tsx
import { HeroSection } from "./hero-section";
import { ServicesSection } from "./services-section";

export default function HomePage() {
  return (
    <>
      <HeroSection />
      <div className="mt-6">
        <ServicesSection />
      </div>
    </>
  );
}

**IMPORTANT**: Margins between sections are defined HERE, not in sections.

### STEP 5: VERIFY YOUR SECTION
1. Take Figma screenshot with mcp__figma-desktop__get_screenshot
2. Take site screenshot on localhost using Playwright/agent-browser
   - **IMPORTANT**: Set viewport to the size specified in task (mobile/tablet/desktop)
3. Compare PIXEL BY PIXEL, especially verifying:
   - **Correct images**: Are implemented images the VISIBLE ones in Figma? (not hidden layers)
   - **Aspect ratios**: Do logos/images maintain their proportions?
   - **Micro-interactions**: Verify hover, active, focus states work correctly
4. If ANY differences exist, fix and repeat
5. Only continue when your section is IDENTICAL to Figma

### STEP 6: CONTEXT VERIFICATION (CRITICAL)
Before marking as complete, verify your section IN CONTEXT:

1. **Check PREVIOUS section** (if exists):
   - Get Figma screenshot of previous section: [prev-node-id]
   - Verify spacing/transition between sections is correct
   - Are sections stuck together? Is padding consistent?

2. **Check NEXT section** (if exists):
   - Get Figma screenshot of next section: [next-node-id]
   - Verify your section ends correctly for the next one
   - Do background colors transition well?

3. **Take site screenshot showing all 3 sections together**:
   - Your section + previous + next (if applicable)
   - Compare with Figma for visual consistency

**If you detect issues with previous sections:**
- DON'T fix them directly
- Report to Tech Lead what problem you found
- Tech Lead will create a correction task

### WHEN FINISHED
- Mark Task #[id] as completed: TaskUpdate({ taskId: "[id]", status: "completed" })
- Report:
  - What you implemented
  - New color tokens added
  - Context verification: All OK with adjacent sections?
  - If you found issues in other sections, describe them
`,
  model: "opus",
  subagent_type: "general-purpose"
})
```

### 3.2 Sequential Execution Flow

After each agent completes:
1. Verify task was marked as completed
2. Check TaskList for next pending task
3. Launch next agent
4. Repeat until all implementation tasks done

---

## Phase 4: QA Review

### 4.1 Launch QA Agent

After ALL implementation tasks complete, launch QA agent:

```typescript
TaskUpdate({ taskId: "[qa-task-id]", status: "in_progress" })

Task({
  description: "QA Review - Full Site Verification",
  prompt: `## QA REVIEW: Complete Site Verification

**IMPORTANT**: This is Task #[qa-id]. Use TaskList to see all completed tasks.

Your task is to REVIEW and REPORT. DON'T fix anything.

### For EACH implemented section:
1. Use mcp__figma-desktop__get_screenshot to capture Figma screenshot
2. Take localhost screenshot with Playwright/agent-browser
3. Compare visually

**NOTE**: For QA, get_screenshot is sufficient. Only use get_design_context if you need to verify specific implementation details (exact colors, spacing, etc.).

### Verify ESPECIALLY:
- **Section consistency**: No stuck sections or inconsistent spacing
- **Design system**: Colors and typography consistent across site
- **Responsiveness**: Everything works at required breakpoint
- **Interactivity**: Hover states, transitions, animations

### WHEN FINISHED - Report ONE of these results:

**If everything is perfect:**
- Mark Task #[qa-id] as completed
- Report: "QA APPROVED - SITE IS PIXEL PERFECT"

**If issues exist:**
- DON'T mark task as completed
- Report EXACTLY what problems you found:
  - Affected section
  - Problem description
  - How it should look according to Figma
- Tech Lead will create correction tasks
`,
  model: "opus",
  subagent_type: "general-purpose"
})
```

### 4.2 Handle QA Feedback (YOUR RESPONSIBILITY)

**If QA reports issues, YOU (Tech Lead) must:**

1. **Create correction tasks** for each problem:
```typescript
TaskCreate({
  subject: "FIX: [Problem description]",
  description: `
    QA reported the following problem:
    [Problem reported by QA]

    Fix as indicated.
  `,
  activeForm: "Fixing [problem]"
})
```

2. **Launch correction agents** for each new task

3. **Re-launch QA** after corrections

4. **Repeat the loop** until QA approves

```
LOOP:
  QA finds issues ->
  Tech Lead creates correction tasks ->
  Tech Lead launches agents to fix ->
  Tech Lead re-launches QA ->
  If QA approves -> END
  If QA finds more issues -> LOOP
```

---

## Phase 5: Completion

When QA approves (marks their task as completed with "QA APPROVED"):

1. Run TaskList to show final status
2. Report final status to user:
   - Total tasks completed
   - All components created
   - Design tokens added
   - Any notes for user

---

## Key Principles

### Task System is the Source of Truth
- ALL work goes through TaskCreate/TaskUpdate
- Agents read TaskList to understand context
- Progress tracked via task status

### Always Use the Best Model
- Use `model: "opus"` for all agents
- Opus has highest performance for complex tasks

### Pixel Perfect Standard
- "Good enough" is NOT acceptable
- Every pixel must match Figma
- If something looks "almost right", it's WRONG

### QA Reports, Tech Lead Fixes
- QA agent ONLY reports issues
- Tech Lead (you) creates correction tasks
- Tech Lead launches correction agents
- Clear separation of concerns

### Sequential Execution
- Tasks run one at a time
- Each task builds on previous work
- Prevents conflicts, ensures consistency

---

## Example Workflow

```
User: /tech-lead-web

Tech Lead: What project are we building? I need:
1. Figma URLs for each section
2. Tech stack
3. Breakpoints to support

User: [Provides Figma URLs and details]

Tech Lead:
1. Verify Figma MCP access
2. TaskCreate for Header, Hero, Services... (10 tasks)
3. TaskCreate for QA Review
4. Configure dependencies

5. TaskUpdate #1 -> in_progress
6. Launch agent for Header
7. Agent completes, TaskUpdate #1 -> completed

8. TaskUpdate #2 -> in_progress
9. Launch agent for Hero
...

15. TaskUpdate #10 -> completed (last section)

16. TaskUpdate #11 (QA) -> in_progress
17. Launch QA agent
18. QA reports 2 issues (does NOT mark as completed)

19. TaskCreate #12: Fix issue 1
20. TaskCreate #13: Fix issue 2
21. Launch correction agents

22. Re-launch QA agent
23. QA approves, TaskUpdate #11 -> completed

24. TaskList -> All tasks completed
25. Report to user: "Site complete!"
```

---

## Error Handling

### Figma MCP Not Available
```
"I don't have access to Figma MCP. Please:
1. Verify the Figma MCP server is configured
2. Ensure you have a valid access token
3. Restart Claude Code after configuration"
```

### Agent Fails to Match Design
```
"Agent couldn't match the design after 3 attempts.
Possible causes:
1. The node-id might be incorrect
2. Figma design might be complex
3. Assets might be missing

Would you like me to retry or prefer to review manually?"
```

### QA Loop Exceeds 3 Iterations
```
"QA has found issues in 3 consecutive rounds.
This may indicate:
1. Ambiguous requirements
2. Very complex design
3. Technical limitations

Would you like me to continue or prefer to review remaining issues manually?"
```
