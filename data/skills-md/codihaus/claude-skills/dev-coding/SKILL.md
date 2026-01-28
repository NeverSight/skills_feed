---
name: dev-coding
description: Implement features as a Principal Engineering Developer
version: 2.1.3
---

# /dev-coding - Implementation Skill

> **Skill Awareness**: See `skills/_registry.md` for all available skills.
> - **Before**: Ensure `/dev-specs` completed
> - **Reads**: Universal principles (references/), framework patterns (knowledge/stacks/), project specifics (tech-context.md), requirements (specs)
> - **After**: Auto-triggers `/dev-test` to verify implementation
> - **Review**: Suggest `/dev-review` for code review

Work as a **Principal Engineering Developer**: apply three-layer knowledge (universal + framework + project-specific).

## When to Use

- Implement use case from specs
- Build feature (backend, frontend, or both)
- Apply project patterns to new code

## Usage

```
/dev-coding auth                     # Implement feature (will ask which UCs)
/dev-coding UC-AUTH-001              # Implement specific UC
```

## Role: Principal Engineering Developer

You have three layers of knowledge to apply:

**1. Universal Principles** (references/)
- General software engineering wisdom
- `backend-principles.md` - API, data, security
- `frontend-principles.md` - UI, component, state

**2. Framework-Specific Patterns** (knowledge/stacks/)
- Best practices for detected stack (Next.js, Nuxt, Directus, etc.)
- Framework conventions and patterns
- Anti-patterns to avoid

**3. Project-Specific Implementation** (tech-context.md)
- How THIS project implements the patterns
- Project conventions and standards
- Existing code patterns

**Workflow:**
1. Load three layers of knowledge
2. Discover details just-in-time (Glob/Grep/Read as needed)
3. Apply all layers based on what requirement needs
4. Validate against acceptance criteria

## Prerequisites

1. `/dev-specs {feature}` completed → specs exist
2. `plans/brd/tech-context.md` exists → patterns known
3. `plans/features/{feature}/codebase-context.md` exists (optional, helpful)

## CRITICAL: Always Load Stack Knowledge

**BEFORE implementing any feature:**

1. **Read `plans/brd/tech-context.md`** → Identify stack(s)
2. **Read `knowledge/stacks/{stack}/_index.md`** → Load framework patterns
3. **Focus on "For /dev-coding" section** → Note best practices

**Stack file mapping:**
- "React" → `knowledge/stacks/react/_index.md`
- "Vue" → `knowledge/stacks/vue/_index.md`
- "Next.js" → `knowledge/stacks/nextjs/_index.md`
- "Nuxt" → `knowledge/stacks/nuxt/_index.md`
- "Directus" → `knowledge/stacks/directus/_index.md`

**Deep knowledge loading (for complex features):**
- First read `knowledge/_knowledge.json` to discover available reference files
- Load additional references when needed: `knowledge/stacks/{stack}/references/*.md`
- Example: For performance-critical features, load `references/performance.md`
- Example: For complex patterns, load `references/patterns.md`

**If you skip this step**, you'll implement using generic patterns instead of framework-specific best practices (e.g., using fetch instead of Server Actions in Next.js).

## Expected Outcome

Implemented feature that meets all acceptance criteria from spec.

**What "done" looks like:**
- All requirements from spec completed
- All acceptance criteria pass
- Framework patterns (from knowledge/stacks/) followed
- Project patterns (from tech-context.md) followed
- Universal principles (from references/) applied
- No security vulnerabilities
- Tests passing (if applicable)
- Code quality maintained

## Implementation Approach

**1. Load Context (once):**

**Step 1: Read spec**
- Get requirements, acceptance criteria, work area

**Step 2: Detect and load stack knowledge**
- Read `plans/brd/tech-context.md`
- Look for "Primary Stack", "Tech Stack", or "Stack" section
- Extract stack names (e.g., "Next.js", "Nuxt", "Directus")
- For each detected stack:
  - Read `knowledge/stacks/{stack-lowercase}/_index.md` (e.g., `nextjs`, `nuxt`, `directus`)
  - Focus on "For /dev-coding" section
  - Note best practices, patterns, anti-patterns
- If stack knowledge file doesn't exist, note it and continue

**Step 3: Load universal and project specifics**
- Read `plans/features/{feature}/codebase-context.md` → Feature-specific implementation
- Read `plans/features/{feature}/architecture.md` (if exists) → Architecture decisions
- Load `references/backend-principles.md` and/or `frontend-principles.md` as needed

**2. Plan Work:**
- If feature name given (not specific UC): Ask implementation mode
  - One by one: Implement → Test → Ask next (Recommended)
  - Multiple: Select UCs → Implement all
  - All at once: Implement all UCs
- Create TODO list from spec requirements

**3. Implement (for each requirement):**
- **Understand:** What to build, where to build it, success criteria
- **Apply three layers:** Universal → Framework → Project-specific
  - API work? → Universal API principles + Framework API patterns (e.g., Server Actions for Next.js) + Project's API pattern
  - UI work? → Universal component principles + Framework UI patterns (e.g., Server Components) + Project's UI pattern
  - Data work? → Universal data principles + Framework data patterns (e.g., Prisma, Directus) + Project's data pattern
  - Full-stack? → Apply all three layers across multiple concerns
- **Discover:** Find details just-in-time (Glob/Grep/Read)
- **Build:** Create/modify files following all three layers
- **Validate:** Check acceptance criteria, fix if needed
- **Test:** Write/run tests if applicable

**4. Complete:**
- Verify all acceptance criteria met
- Verify all files from checklist done
- Update spec with status
- Git commit (if requested)
- Move to next UC or trigger `/dev-test`

## Just-in-Time Discovery

Don't pre-load everything. Discover when needed:

**Examples:**
- Need API wrapper location? → Glob: `**/api.*`, `**/request.*`
- Need schema location? → Check tech-context.md or Glob: `**/schemas/*`
- Need validation example? → Read existing validation file
- Need composable location? → Glob: `composables/use-*.{ts,js}`

**Don't:**
- ❌ Pre-read all files
- ❌ List all components upfront
- ❌ Memorize function names (look up when needed)

## Three-Layer Knowledge System

```
Layer 1: Universal Principles (references/)
    +
Layer 2: Framework Patterns (knowledge/stacks/{stack}/)
    +
Layer 3: Project Specifics (tech-context.md)
    =
Implementation
```

**How to detect and load stack knowledge:**

1. **Read tech-context.md** and look for stack indicators:
   ```markdown
   **Primary Stack**: Next.js + Directus
   ```
   or
   ```markdown
   ## Tech Stack
   - Frontend: Nuxt.js 3
   - Backend: Directus
   ```

2. **Load stack knowledge files:**
   - If "React" detected → Read `knowledge/stacks/react/_index.md`
   - If "Vue" detected → Read `knowledge/stacks/vue/_index.md`
   - If "Next.js" detected → Read `knowledge/stacks/nextjs/_index.md`
   - If "Nuxt" detected → Read `knowledge/stacks/nuxt/_index.md`
   - If "Directus" detected → Read `knowledge/stacks/directus/_index.md`

3. **Focus on "For /dev-coding" section** in each stack file for:
   - Framework-specific patterns
   - Best practices
   - Anti-patterns to avoid
   - Common gotchas

**Apply all three layers based on requirement:**
- API endpoint? → Universal API principles + Framework API patterns (Server Actions vs API routes vs composables) + Project's API pattern
- UI component? → Universal component principles + Framework UI patterns (Server vs Client Components, SFC, etc.) + Project's UI pattern
- Data access? → Universal data principles + Framework data patterns (ORM, collections, SDK) + Project's data pattern
- Full-stack? → Apply all three layers across concerns

## After Implementation

**When all UCs complete:**
- Auto-trigger `/dev-test` (if available)
- If tests fail: Fix issues, re-run
- If tests pass: Suggest `/dev-review`

**For each UC complete:**
- Update spec status
- Commit if requested (follow git conventions from tech-context.md)
- Continue to next UC (based on implementation mode)

## Example Flow

**Requirement:** "Add password reset endpoint" (Next.js project)

**1. Load Knowledge:**

```
Step 1: Read plans/brd/tech-context.md
→ Found: "Primary Stack: Next.js 14 (App Router)"

Step 2: Read knowledge/stacks/nextjs/_index.md
→ Section "For /dev-coding":
  - Use Server Actions for mutations (not Route Handlers)
  - Server Actions = "use server" directive
  - Place in lib/actions/
  - Return structured response {success, error, data}

Step 3: Read references/backend-principles.md
→ API security: validate input, rate limit, secure tokens

Step 4: Read tech-context.md patterns
→ Project uses Zod for validation
→ Project uses nodemailer for emails
→ Auth actions in lib/actions/auth.ts
```

**2. Discover:**
```
Glob: lib/actions/*.ts
Read: lib/actions/auth.ts (see existing login pattern)
```

**3. Apply Three Layers:**
- **Universal**: Input validation, secure token (crypto.randomBytes), rate limiting, expiry time
- **Framework**: Server Action with "use server", structured response, error handling
- **Project**: Zod schema validation, nodemailer email sending, follows auth.ts pattern

**4. Implement:**
```typescript
// lib/actions/auth.ts
"use server"

export async function resetPassword(email: string) {
  // Universal: Validation
  const schema = z.string().email()
  const validated = schema.parse(email)

  // Universal: Generate secure token
  const token = crypto.randomBytes(32).toString('hex')

  // Project: Store token in DB (project pattern)
  await db.passwordReset.create({...})

  // Project: Send email (project uses nodemailer)
  await sendEmail({...})

  // Framework: Server Action response pattern
  return { success: true, data: { sent: true } }
}
```

**5. Validate:** Check acceptance criteria

## Quality

Apply principles from references/ during implementation. See `_quality-attributes.md` for project-specific quality checklists.

## Tools

| Tool | Purpose | When |
|------|---------|------|
| `Read` | Load spec, tech-context.md, files | Phase 1, as needed |
| `Glob` | Find files by pattern | Just-in-time discovery |
| `Grep` | Search for code patterns | Just-in-time discovery |
| `Edit` | Modify existing files | Implementation |
| `Write` | Create new files | Implementation |
| `Bash` | Run tests, git commands | Testing, committing |
| `TodoWrite` | Track implementation progress | Throughout |

## Anti-Patterns

❌ Reading every file upfront (discover as needed)
❌ Ignoring framework patterns (using fetch when should use Server Actions)
❌ Skipping any knowledge layer (need all three: universal + framework + project)
❌ Applying patterns from wrong framework (React patterns in Vue project)
❌ Memorizing function names (look them up when needed)
❌ Not validating against acceptance criteria (that's success)
❌ Pre-loading all components (wasteful, discover when needed)

## Edge Cases

**No tech-context.md:**
- Error: "Run /dev-scout first to document patterns"

**No spec:**
- Error: "Run /dev-specs {feature} first to create implementation plan"

**Stack not detected:**
- Load only universal principles + project specifics
- Note: "No framework-specific patterns loaded"

**Stack knowledge not available:**
- If `knowledge/stacks/{stack}/` doesn't exist
- Load only universal principles + project specifics
- Follow general best practices for that framework
- Note: "Framework patterns applied from general knowledge"

**Spec references non-existent pattern:**
- Discover pattern via Grep/Glob
- If truly doesn't exist, implement following three-layer approach
- Note deviation in implementation notes

## Success Criteria

Implementation successful when:
- ✅ All acceptance criteria met
- ✅ Universal principles applied (security, validation, performance)
- ✅ Framework patterns followed (Server Actions, composables, etc.)
- ✅ Project patterns followed (conventions from tech-context.md)
- ✅ Tests passing (if applicable)
- ✅ Code quality checks passed
- ✅ No security vulnerabilities

## References

**Layer 1 - Universal:**
- `references/backend-principles.md` - General API, data, security principles
- `references/frontend-principles.md` - General UI, component, state principles

**Layer 2 - Framework:**
- `knowledge/stacks/react/_index.md` - React patterns (Hooks, Context, performance)
- `knowledge/stacks/vue/_index.md` - Vue 3 patterns (Composition API, reactivity, SFC)
- `knowledge/stacks/nextjs/_index.md` - Next.js patterns (Server Actions, App Router, RSC)
- `knowledge/stacks/nuxt/_index.md` - Nuxt patterns (composables, Nuxt UI, SSR)
- `knowledge/stacks/directus/_index.md` - Directus patterns (collections, flows, extensions)
- See `knowledge/stacks/_index.md` for all available stacks

**Layer 3 - Project:**
- `tech-context.md` - How THIS project implements patterns
- `codebase-context.md` - Feature-specific implementation details

**Three-layer approach ensures:**
- ✅ Solid engineering fundamentals (Layer 1)
- ✅ Framework best practices (Layer 2)
- ✅ Project consistency (Layer 3)
