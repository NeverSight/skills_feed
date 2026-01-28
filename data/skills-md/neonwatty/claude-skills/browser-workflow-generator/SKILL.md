---
name: browser-workflow-generator
description: Generates, creates, or updates browser workflow files. Use this when the user says "generate browser workflows", "create browser workflows", "update browser workflows", or "iterate on browser workflows". Thoroughly explores the app's codebase to discover all user-facing features, routes, and interactions. Creates comprehensive numbered workflows with substeps that cover the full user experience.
---

# Browser Workflow Generator Skill

You are a senior QA engineer tasked with creating comprehensive user workflow documentation. Your job is to deeply explore the application and generate thorough, testable workflows that cover all key user journeys.

## Task List Integration

**CRITICAL:** This skill uses Claude Code's task list system for progress tracking and session recovery. You MUST use TaskCreate, TaskUpdate, and TaskList tools throughout execution.

### Why Task Lists Matter Here
- **Parallel agent tracking:** Monitor 3 exploration agents completing simultaneously
- **Progress visibility:** User sees "Exploring: 2/3 agents complete"
- **Session recovery:** If interrupted, know which agents finished and what they found
- **Iteration tracking:** Track multiple approval rounds with user
- **Audit trail:** Record what was explored, researched, and generated

### Task Hierarchy
```
[Main Task] "Generate: Browser Workflows"
  └── [Explore Task] "Explore: Routes & Navigation" (agent)
  └── [Explore Task] "Explore: Components & Features" (agent)
  └── [Explore Task] "Explore: State & Data" (agent)
  └── [Research Task] "Research: Web UX Conventions" (agent)
  └── [Generate Task] "Generate: Workflow Drafts"
  └── [Approval Task] "Approval: User Review #1"
  └── [Write Task] "Write: browser-workflows.md"
```

### Session Recovery Check
**At the start of this skill, always check for existing tasks:**
```
1. Call TaskList to check for existing workflow generator tasks
2. If a "Generate: Browser Workflows" task exists with status in_progress:
   - Check which exploration tasks completed (read their metadata for findings)
   - Check if UX research completed
   - Check if drafts were generated
   - Resume from appropriate phase
3. If no tasks exist, proceed with fresh execution
```

## Process

### Phase 1: Assess Current State

**Create the main workflow generator task:**
```
TaskCreate:
- subject: "Generate: Browser Workflows"
- description: |
    Generate comprehensive browser workflow documentation.
    Starting: assess current state
- activeForm: "Assessing current state"

TaskUpdate:
- taskId: [main task ID]
- status: "in_progress"
```

1. Check if `/workflows/browser-workflows.md` already exists
2. If it exists, read it and note:
   - What workflows are already documented
   - What might be outdated or incomplete
   - What's missing based on your knowledge of the app
3. Ask the user their goal:
   - **Create new:** Generate workflows from scratch
   - **Update:** Add new workflows for new features
   - **Refactor:** Reorganize or improve existing workflows
   - **Audit:** Check existing workflows against current app state

**Update task with assessment results:**
```
TaskUpdate:
- taskId: [main task ID]
- metadata: {
    "existingFile": true/false,
    "existingWorkflowCount": [N],
    "userGoal": "create" | "update" | "refactor" | "audit"
  }
```

### Phase 2: Explore the Application [DELEGATE TO AGENTS]

**Purpose:** Thoroughly understand the app by launching multiple Explore agents in parallel. This saves context and allows comprehensive codebase exploration.

**Create exploration tasks before spawning agents:**
```
TaskCreate (3 tasks in parallel):

Task 1:
- subject: "Explore: Routes & Navigation"
- description: "Find all routes, navigation patterns, and entry points"
- activeForm: "Exploring routes"

Task 2:
- subject: "Explore: Components & Features"
- description: "Find all interactive UI components and major features"
- activeForm: "Exploring components"

Task 3:
- subject: "Explore: State & Data"
- description: "Understand data model and user CRUD actions"
- activeForm: "Exploring data model"

Then for each:
TaskUpdate:
- taskId: [explore task ID]
- addBlockedBy: [main task ID]  # Links to main task
- status: "in_progress"
```

**Use the Task tool to spawn three agents in parallel (all in a single message):**

```
Agent 1 - Routes & Navigation:
Task tool parameters:
- subagent_type: "Explore"
- model: "sonnet"
- prompt: |
    You are exploring a web application to find all routes and navigation patterns.

    ## What to Find

    1. **All Routes/Pages**
       - Search for router configuration (React Router, Next.js pages, Vue Router, etc.)
       - Find all page/view components
       - Identify URL patterns and parameters

    2. **Navigation Patterns**
       - Find navigation menus, sidebars, headers
       - Identify breadcrumbs, tabs, or other nav UI
       - Map how users move between pages

    3. **Entry Points**
       - Find the main entry URL
       - Identify deep links or bookmarkable URLs
       - Note any authentication-gated routes

    ## Return Format

    ```
    ## Routes & Navigation Report

    ### All Routes
    | Route | Component | Purpose | Auth Required |
    |-------|-----------|---------|---------------|

    ### Navigation Structure
    - Primary nav: [description]
    - Secondary nav: [description]

    ### User Flow Map
    - Home → [possible destinations]
    - [Page] → [possible destinations]
    ```
```

```
Agent 2 - Components & Features:
Task tool parameters:
- subagent_type: "Explore"
- model: "sonnet"
- prompt: |
    You are exploring a web application to find all interactive UI components.

    ## What to Find

    1. **Interactive Components**
       - Buttons, links, clickable elements
       - Form inputs (text, select, checkbox, etc.)
       - Modals, dialogs, drawers
       - Drag-drop areas, toolbars, menus

    2. **Major Features**
       - Identify the app's core features
       - Find feature entry points in the UI
       - Note feature-specific components

    3. **Component Patterns**
       - Identify reusable component patterns
       - Note any component libraries used (MUI, Radix, etc.)
       - Find data-testid or accessibility attributes

    ## Return Format

    ```
    ## Components & Features Report

    ### Major Features
    | Feature | Entry Point | Key Components |
    |---------|-------------|----------------|

    ### Interactive Components by Page
    #### [Page Name]
    - Buttons: [list]
    - Forms: [list]
    - Other: [list]

    ### Component Patterns
    - UI library: [if any]
    - Common patterns: [list]
    ```
```

```
Agent 3 - State & Data:
Task tool parameters:
- subagent_type: "Explore"
- model: "sonnet"
- prompt: |
    You are exploring a web application to understand its data model and user actions.

    ## What to Find

    1. **Data Model**
       - Find state management (Redux, Zustand, Context, etc.)
       - Identify main data entities/types
       - Note data relationships

    2. **User Actions (CRUD)**
       - What can users create?
       - What can users read/view?
       - What can users update/edit?
       - What can users delete?

    3. **API & Persistence**
       - Find API call patterns
       - Identify endpoints used
       - Note localStorage/sessionStorage usage

    ## Return Format

    ```
    ## State & Data Report

    ### Data Entities
    | Entity | Properties | CRUD Operations |
    |--------|------------|-----------------|

    ### User Actions
    - Create: [list of things users can create]
    - Read: [list of things users can view]
    - Update: [list of things users can modify]
    - Delete: [list of things users can remove]

    ### API Patterns
    - Base URL: [if found]
    - Key endpoints: [list]
    ```
```

**After each agent returns, update its task:**
```
TaskUpdate:
- taskId: [explore task ID]
- status: "completed"
- metadata: {
    "routesFound": [count],        # For routes agent
    "componentsFound": [count],    # For components agent
    "entitiesFound": [count],      # For data agent
    "summary": "[brief summary of findings]"
  }
```

**After all agents return:** Synthesize findings into a feature inventory:
- List all user-facing features
- Group by area/section of the app
- Note entry points and exit points

**Update main task with exploration summary:**
```
TaskUpdate:
- taskId: [main task ID]
- metadata: {
    "explorationComplete": true,
    "routesFound": [total],
    "featuresFound": [total],
    "entitiesFound": [total]
  }
```

### Phase 3: Identify User Journeys

**Update main task for journey identification phase:**
```
TaskUpdate:
- taskId: [main task ID]
- activeForm: "Identifying user journeys"
```

Based on exploration, identify key user journeys:

**Core Journeys** (every user does these):
- Onboarding/first-time experience
- Primary task completion
- Navigation between main sections

**Feature Journeys** (specific feature usage):
- Each major feature should have its own workflow
- Include happy path and key variations

**Edge Case Journeys** (important but less common):
- Error handling flows
- Empty states
- Settings/preferences
- Account/profile management

**Update main task with journey counts:**
```
TaskUpdate:
- taskId: [main task ID]
- metadata: {
    "coreJourneys": [count],
    "featureJourneys": [count],
    "edgeCaseJourneys": [count],
    "totalWorkflows": [total]
  }
```

### Phase 4: Research UX Conventions [DELEGATE TO AGENT]

**Purpose:** For each major screen/page type identified, research what good web UX looks like. Delegate this to an agent to save context.

**Create UX research task:**
```
TaskCreate:
- subject: "Research: Web UX Conventions"
- description: |
    Research UX conventions for identified page types.
    Page types: [list from Phase 3]
- activeForm: "Researching UX conventions"

TaskUpdate:
- taskId: [research task ID]
- addBlockedBy: [main task ID]
- status: "in_progress"
```

**Use the Task tool to spawn a UX research agent:**

```
Task tool parameters:
- subagent_type: "general-purpose"
- model: "sonnet"
- prompt: |
    You are researching web UX conventions for a workflow generator.

    ## Page Types to Research
    [Include list of page types identified from Phase 2/3, e.g.:]
    - Login page
    - Dashboard
    - Settings page
    - List/table view
    - Detail page
    - Onboarding flow

    ## Your Task

    For each page type:

    1. **Search for reference examples** using WebSearch:
       - "web app [page type] design Dribbble"
       - "best SaaS [page type] UI examples"
       - "[well-known web app] [page type] screenshot"

    2. **Visit 2-3 reference examples** to understand conventions

    3. **Document UX conventions** for each page type

    ## Return Format

    For each page type, return:
    ```
    ### Page: [Page Type]
    **Reference Examples:** [Apps/sites compared]
    **Expected Web Conventions:**
    - [Convention 1]
    - [Convention 2]
    - [Convention 3]
    **Anti-patterns to flag:**
    - [Anti-pattern 1 - why it's wrong for web]
    - [Anti-pattern 2]
    ```

    ## Example Output

    ### Page: Dashboard
    **Reference Examples:** Linear, Notion, Figma
    **Expected Web Conventions:**
    - Top navigation bar with logo, search, and user menu
    - Sidebar for section navigation (collapsible on smaller screens)
    - Cards or widgets for key metrics
    - Hover states on all interactive elements
    - Keyboard shortcuts for power users (with visible hints)
    - Responsive layout that works from 320px to 2560px+
    **Anti-patterns to flag:**
    - Bottom tab bar (mobile pattern)
    - Pull-to-refresh gesture requirement
    - No hover states on buttons/links
    - URLs that don't reflect current view state
```

**After agent returns:**
```
TaskUpdate:
- taskId: [research task ID]
- status: "completed"
- metadata: {
    "pageTypesResearched": [count],
    "conventionsDocumented": [count],
    "antiPatternsIdentified": [count]
  }
```

Include UX expectations in workflows so the executor knows what to verify for each page type.

### Phase 5: Generate Workflows

**Create workflow generation task:**
```
TaskCreate:
- subject: "Generate: Workflow Drafts"
- description: |
    Generate [N] workflow drafts based on exploration and UX research.
    Core: [count], Feature: [count], Edge Case: [count]
- activeForm: "Generating workflow drafts"

TaskUpdate:
- taskId: [generate task ID]
- addBlockedBy: [main task ID]
- status: "in_progress"
```

For each journey, create a workflow with this structure:

```markdown
## Workflow: [Descriptive Name]

> [Brief description of what this workflow tests and why it matters]

1. [Top-level step]
   - [Substep with specific detail]
   - [Substep with expected outcome]
2. [Next top-level step]
   - [Substep]
3. Verify [expected final state]
```

**Guidelines for writing steps:**
- Be specific: "Click the blue 'Add Guest' button in the toolbar" not "Click add"
- Include expected outcomes: "Verify the modal appears" not just "Open modal"
- Use consistent language: Navigate, Click, Type, Verify, Drag, Select
- Group related actions under numbered steps with substeps
- Include wait conditions where timing matters

### Phase 6: Organize & Write

**Mark generation task as complete:**
```
TaskUpdate:
- taskId: [generate task ID]
- status: "completed"
- metadata: {
    "workflowsGenerated": [count],
    "totalSteps": [count],
    "coreWorkflows": [list of names],
    "featureWorkflows": [list of names],
    "edgeCaseWorkflows": [list of names]
  }
```

**Update main task for organization phase:**
```
TaskUpdate:
- taskId: [main task ID]
- activeForm: "Organizing workflows"
```

Structure the final document:

```markdown
# Browser Workflows

> Auto-generated workflow documentation for [App Name]
> Last updated: [Date]

## Quick Reference

| Workflow | Purpose | Steps |
|----------|---------|-------|
| [Name] | [Brief] | [Count] |

---

## Core Workflows

### Workflow: [Name]
...

## Feature Workflows

### Workflow: [Name]
...

## Edge Case Workflows

### Workflow: [Name]
...
```

**Do not write to file yet - proceed to Phase 7 for user approval first.**

### Phase 7: Review with User (REQUIRED)

**This step is mandatory. Do not write the final file without user approval.**

**Create approval task:**
```
TaskCreate:
- subject: "Approval: User Review #1"
- description: |
    Present workflows to user for approval.
    Workflows: [count]
    Awaiting user decision.
- activeForm: "Awaiting user approval"

TaskUpdate:
- taskId: [approval task ID]
- addBlockedBy: [main task ID]
- status: "in_progress"
```

After generating the workflows, use `AskUserQuestion` to get explicit approval:

1. **Present a summary** to the user:
   - Total workflows generated (list each by name)
   - Features/areas covered
   - Any gaps or areas you couldn't fully cover
   - Anything that needs manual verification

2. **Use AskUserQuestion** to ask:
   - "Do these workflows cover all the key user journeys?"
   - Provide options: Approve / Add more workflows / Modify existing / Start over

3. **If user wants additions or changes:**

   **Update approval task as needing changes:**
   ```
   TaskUpdate:
   - taskId: [approval task ID]
   - subject: "Approval: User Review #1 - changes requested"
   - status: "completed"
   - metadata: {"decision": "changes_requested", "feedback": "[user feedback]"}
   ```

   **Create new approval task for next round:**
   ```
   TaskCreate:
   - subject: "Approval: User Review #2"
   - description: |
       Second review round after changes.
       Changes made: [list of changes]
   - activeForm: "Awaiting user approval (round 2)"
   ```

   - Ask specifically what workflows to add or modify
   - Generate the additional/modified workflows
   - Return to step 1 and present updated summary
   - Repeat until user approves

4. **Only after explicit approval:**

   **Update approval task as approved:**
   ```
   TaskUpdate:
   - taskId: [approval task ID]
   - subject: "Approval: User Review #[N] - approved ✅"
   - status: "completed"
   - metadata: {"decision": "approved", "reviewRounds": [N]}
   ```

   Write to `/workflows/browser-workflows.md`

**Example AskUserQuestion usage:**

```
Question: "I've identified [N] workflows covering [areas]. Do these look complete?"
Options:
- "Yes, looks good - write the file"
- "Add more workflows"
- "Modify some workflows"
- "Let me describe what's missing"
```

If user selects "Add more" or "Modify", follow up with another question asking for specifics before proceeding.

### Phase 8: Write File and Complete

**Create write task:**
```
TaskCreate:
- subject: "Write: browser-workflows.md"
- description: "Write approved workflows to file"
- activeForm: "Writing workflow file"

TaskUpdate:
- taskId: [write task ID]
- status: "in_progress"
```

**Write the file to `/workflows/browser-workflows.md`**

**Mark write task as complete:**
```
TaskUpdate:
- taskId: [write task ID]
- status: "completed"
- metadata: {"outputPath": "/workflows/browser-workflows.md", "workflowCount": [N]}
```

**Mark main task as complete:**
```
TaskUpdate:
- taskId: [main task ID]
- status: "completed"
- metadata: {
    "outputPath": "/workflows/browser-workflows.md",
    "workflowCount": [N],
    "reviewRounds": [N],
    "explorationAgents": 3,
    "uxResearch": true
  }
```

**Final summary from task data:**
```
## Browser Workflows Generated

**File:** /workflows/browser-workflows.md
**Workflows:** [count from task metadata]
**Review rounds:** [count from approval task metadata]

### Exploration Summary
- Routes found: [from explore task metadata]
- Components found: [from explore task metadata]
- Data entities: [from explore task metadata]

### Workflows Created
[List from generate task metadata]

The workflows are ready to be executed with the browser-workflow-executor skill.
```

### Session Recovery

If resuming from an interrupted session:

**Recovery decision tree:**
```
TaskList shows:
├── Main task in_progress, no explore tasks
│   └── Start Phase 2 (exploration)
├── Main task in_progress, some explore tasks completed
│   └── Check which agents finished, spawn remaining
├── Main task in_progress, all explore tasks completed, no research task
│   └── Start Phase 4 (UX research)
├── Main task in_progress, research completed, no generate task
│   └── Start Phase 5 (generate workflows)
├── Main task in_progress, generate completed, no approval task
│   └── Start Phase 7 (user review)
├── Main task in_progress, approval task in_progress
│   └── Present summary to user again
├── Main task in_progress, approval completed (approved), no write task
│   └── Start Phase 8 (write file)
├── Main task completed
│   └── Show final summary
└── No tasks exist
    └── Fresh start (Phase 1)
```

**Resuming with partial exploration:**
If some exploration agents completed but others didn't:
1. Read completed agent findings from task metadata
2. Spawn only the missing agents
3. Combine all findings when all complete

**Always inform user when resuming:**
```
Resuming workflow generation session:
- Exploration: [N]/3 agents complete
- UX Research: [complete/pending]
- Workflows generated: [count or "pending"]
- Approval: [status]
- Resuming: [next action]
```

## Workflow Writing Standards

**Step Types:**

| Action | Format | Example |
|--------|--------|---------|
| Navigation | Navigate to [URL/page] | Navigate to the dashboard |
| Click | Click [specific element] | Click the "Save" button |
| Type | Type "[text]" in [field] | Type "john@email.com" in the email field |
| Select | Select "[option]" from [dropdown] | Select "Round" from table shape dropdown |
| Drag | Drag [element] to [target] | Drag guest card onto table |
| Verify | Verify [expected state] | Verify success toast appears |
| Wait | Wait for [condition] | Wait for loading spinner to disappear |

## Automation-Friendly Workflow Guidelines

When writing workflows, consider what can and cannot be automated by Claude-in-Chrome:

### Prefer UI Actions Over Keyboard Shortcuts

**Instead of:**
```markdown
- Press Cmd+Z to undo
- Press Cmd+S to save
- Press Delete to remove
```

**Write:**
```markdown
- Click the Undo button in toolbar, OR press Cmd+Z
- Click the Save button, OR press Cmd+S
- Click the Delete button, OR press Delete key
```

### Mark Non-Automatable Steps

Use `[MANUAL]` tag for steps that require manual verification:

```markdown
3. Grant camera permission
   - [MANUAL] Click "Allow" on browser permission prompt
   - Note: Browser permission dialogs cannot be automated

4. Download the report
   - [MANUAL] Click "Download PDF" and verify file saves
   - Note: File download dialogs cannot be automated
```

### Known Automation Limitations

These interactions **cannot** be automated and should include `[MANUAL]` tags or UI alternatives:

| Limitation | Example | Recommendation |
|------------|---------|----------------|
| Keyboard shortcuts | Cmd+Z, Cmd+C, Cmd+V | Provide button alternative |
| Native dialogs | alert(), confirm(), prompt() | Skip or mark [MANUAL] |
| File operations | Upload/download dialogs | Mark [MANUAL] |
| Browser permissions | Camera, location prompts | Mark [MANUAL], pre-configure |
| Pop-up windows | OAuth, new window opens | Document as [MANUAL] |
| Print dialogs | Print preview | Mark [MANUAL] |

### Include Prerequisites for Automation

When workflows require specific setup:

```markdown
## Workflow: Upload Profile Photo

**Prerequisites for automation:**
- Browser must have camera/file permissions pre-configured
- Test file should be accessible at known path

> Tests uploading a new profile photo.

1. Open profile settings
   ...
```

**Substep Format:**
- Use bullet points under numbered steps
- Include specific selectors or descriptions
- Note expected intermediate states

**Example Workflow:**

```markdown
## Workflow: Create New Event with Tables and Guests

> Tests the complete flow of setting up a new seating arrangement from scratch.

1. Enter the application
   - Navigate to https://app.example.com
   - Click "Get Started" or "Try Demo" button
   - Verify canvas view loads with empty state

2. Add a table to the canvas
   - Click "Add Table" button in toolbar
   - Select "Round" from shape options
   - Verify table appears on canvas
   - Verify table shows "0/8 seats" indicator

3. Add a guest
   - Click "Add Guest" button
   - Type "John Smith" in name field
   - Press Enter or click Save
   - Verify guest appears in guest list sidebar

4. Assign guest to table
   - Drag "John Smith" from guest list
   - Drop onto the round table
   - Verify guest name appears at table
   - Verify seat count updates to "1/8 seats"

5. Verify final state
   - Verify guest is no longer in unassigned list
   - Verify table shows assigned guest
   - Verify canvas can be zoomed and panned
```

## Handling Updates

When updating existing workflows:

1. **Preserve working workflows** - Don't rewrite what works
2. **Mark deprecated steps** - If UI changed, note what's outdated
3. **Add new workflows** - Append new features as new workflows
4. **Version notes** - Add changelog comments for significant changes

## Browser/Web Platform UX Anti-Patterns

When generating workflows, include UX verification steps that check for these common anti-patterns where web apps incorrectly use native mobile conventions or miss web-specific requirements:

### Navigation Anti-Patterns
| Anti-Pattern | Web Convention | What to Check |
|--------------|----------------|---------------|
| Gesture-only navigation | Click + gesture alternatives | All navigation should work with mouse clicks |
| Breaking back button | URL-based navigation | Browser back button should work intuitively |
| No URL for states | Deep linkable URLs | Important states should have shareable URLs |
| Tab bar at bottom | Top navigation or sidebar | Bottom tab bars are mobile patterns, not web |
| Swipe-only carousels | Arrow buttons + indicators | Carousels need visible click controls |

### Interaction Anti-Patterns
| Anti-Pattern | Web Convention | What to Check |
|--------------|----------------|---------------|
| Missing hover states | Clear hover feedback | All interactive elements need hover indication |
| No focus indicators | Visible focus rings | Keyboard navigation needs visible focus states |
| Touch-sized-only buttons | Standard web button sizes | Buttons can be smaller than 44pt on web |
| Pull-to-refresh | Refresh button or auto-refresh | Web doesn't support native pull-to-refresh |
| Long press menus | Right-click or visible menu buttons | Context menus should use right-click on web |

### Visual Anti-Patterns
| Anti-Pattern | Web Convention | What to Check |
|--------------|----------------|---------------|
| Full-screen modals everywhere | Inline expansion or sized modals | Web modals typically don't need full-screen |
| iOS/Android specific styling | Platform-agnostic web design | Avoid native mobile component styling |
| No responsive breakpoints | Responsive design | Layout should adapt to viewport width |
| Mobile-only viewport | Desktop-first or responsive | Should work well at 1200px+ widths |
| App-like splash screens | Immediate content loading | Web should show content quickly, not splash |

### Component Anti-Patterns
| Anti-Pattern | Web Convention | What to Check |
|--------------|----------------|---------------|
| Native mobile pickers | HTML select or custom dropdowns | Use web-native form components |
| Action sheets sliding up | Dropdown menus or modals | Use web-appropriate menu patterns |
| iOS-style toggle switches | Checkboxes or web-styled toggles | Consider web conventions for boolean inputs |
| Floating bottom bars | Fixed headers or inline CTAs | Sticky bottom bars can feel app-like |
| Edge swipe gestures | Visible navigation buttons | Don't rely on edge swipes for critical actions |

### Accessibility Anti-Patterns
| Anti-Pattern | Web Convention | What to Check |
|--------------|----------------|---------------|
| No keyboard navigation | Full keyboard support | All features accessible via keyboard |
| Missing ARIA labels | Proper accessibility markup | Screen readers should understand the UI |
| Color-only indicators | Color + icon/text indicators | Don't rely solely on color for meaning |
| Auto-playing media | User-initiated playback | Media should not auto-play with sound |
| Trapped focus in modals | Proper focus management | Focus should be trapped correctly in modals |

### Workflow UX Verification Steps

When writing workflows, include verification steps for platform appropriateness:

```markdown
## Workflow: [Name]

...

6. Verify web platform conventions
   - Verify all interactive elements have hover states
   - Verify browser back button works correctly
   - Verify keyboard navigation is possible
   - Verify layout is responsive (try different viewport widths)
   - Verify URLs are shareable/deep-linkable for important states
```
