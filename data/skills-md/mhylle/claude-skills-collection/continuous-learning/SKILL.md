---
name: continuous-learning
description: Pattern extraction framework for learning from sessions. This skill captures valuable patterns discovered during work sessions including error resolutions, user corrections, workarounds, debugging techniques, and project-specific patterns. Triggers on Stop hook, end of session, "save learnings", "extract patterns", or when explicitly asked to capture knowledge from the current session. Outputs learned skills to ~/.claude/skills/learned/.
---

# Continuous Learning

## Overview

This skill provides a systematic framework for extracting and preserving valuable patterns discovered during work sessions. Rather than letting hard-won insights disappear when a session ends, it captures solutions, techniques, and project-specific knowledge as reusable learned skills.

## Design Philosophy

### Learning from Experience

The most valuable knowledge often emerges through struggle - debugging sessions that reveal non-obvious solutions, user corrections that expose better approaches, and workarounds that navigate framework limitations. This tacit knowledge typically evaporates between sessions, forcing repeated rediscovery.

This skill operationalizes experience by:

1. **Pattern Recognition** - Identifying moments of insight during sessions
2. **Knowledge Extraction** - Distilling insights into reusable formats
3. **Persistent Storage** - Saving patterns for future session retrieval
4. **Progressive Refinement** - Improving patterns as they're reused and validated

### The Learning Loop

```
Session Work
     |
     v
Pattern Detection -----> Threshold Check (skip if too generic)
     |
     v
Extraction & Structuring
     |
     v
Deduplication Check -----> Merge if similar pattern exists
     |
     v
Storage in ~/.claude/skills/learned/
     |
     v
Future Session Retrieval
     |
     v
Pattern Validation & Refinement
```

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Specificity over Generality** | A pattern that solves a specific problem well beats a vague principle |
| **Context Preservation** | Include enough context to understand when the pattern applies |
| **Actionable Format** | Patterns should be immediately usable, not just informative |
| **Progressive Confidence** | Patterns gain confidence through repeated successful use |
| **Graceful Degradation** | Patterns include fallback approaches when primary fails |

## When to Use

### Automatic Triggers

- **Stop Hook**: Configured to run automatically when a session ends
- **Session Timeout**: When a session is about to expire
- **Explicit Invocation**: User says "save learnings", "extract patterns"

### Manual Triggers

- After solving a particularly difficult bug
- When user corrects an approach (indicating a learning opportunity)
- After discovering an undocumented workaround
- When a debugging technique proves especially effective
- After understanding project-specific conventions

### Signal Phrases

- "Save what we learned"
- "Remember this for next time"
- "This should be a pattern"
- "Extract learnings from this session"
- "What patterns did we discover?"

## Pattern Types

### 1. Error Resolution Patterns

**Definition**: Solutions to errors, exceptions, or unexpected behaviors that required non-obvious fixes.

**Extraction Criteria**:
- Error was not immediately obvious from the error message
- Solution required investigation or research
- Fix involved understanding underlying cause, not just symptom
- Solution would be useful if the same error recurs

**Structure**:
```yaml
type: error_resolution
trigger: "[Exact error message or pattern]"
symptoms:
  - "[Observable symptom 1]"
  - "[Observable symptom 2]"
root_cause: "[Underlying cause]"
solution:
  steps:
    - "[Step 1]"
    - "[Step 2]"
  code_example: |
    // Before (problematic)
    problematic_code_here

    // After (fixed)
    fixed_code_here
context:
  framework: "[Framework/library name]"
  version: "[Version if relevant]"
  environment: "[Environment factors]"
confidence: [0.0-1.0]
times_applied: 0
```

**Quality Threshold**:
- Must have specific error trigger (not generic "it didn't work")
- Must explain root cause, not just provide fix
- Must include context for when pattern applies

### 2. User Correction Patterns

**Definition**: Insights gained when the user corrects Claude's approach, revealing better methods or project-specific preferences.

**Extraction Criteria**:
- User explicitly corrected an approach or suggestion
- Correction revealed a preference not evident from code/docs
- Learning is transferable to similar situations
- Correction wasn't due to simple misunderstanding

**Structure**:
```yaml
type: user_correction
original_approach: "[What Claude initially did/suggested]"
corrected_approach: "[What the user preferred]"
reasoning: "[Why the corrected approach is better]"
applies_when:
  - "[Situation 1]"
  - "[Situation 2]"
project_specific: [true/false]
project_identifier: "[Project name/path if specific]"
confidence: [0.0-1.0]
times_validated: 0
```

**Quality Threshold**:
- Must capture the "why" behind the correction
- Must be generalizable (not one-off preference)
- Must include clear applicability criteria

### 3. Workaround Patterns

**Definition**: Clever solutions to limitations in tools, frameworks, or environments.

**Extraction Criteria**:
- Standard approach was blocked by a limitation
- Workaround achieved the goal despite the limitation
- Workaround is reliable and maintainable
- Limitation is likely to be encountered again

**Structure**:
```yaml
type: workaround
limitation: "[What was blocked/unavailable]"
goal: "[What we were trying to achieve]"
workaround:
  approach: "[Description of the workaround]"
  steps:
    - "[Step 1]"
    - "[Step 2]"
  code_example: |
    // Workaround implementation
    code_here
caveats:
  - "[Caveat 1]"
  - "[Caveat 2]"
better_alternative: "[What to use when limitation is removed]"
context:
  tool: "[Tool/framework name]"
  version: "[Version with limitation]"
confidence: [0.0-1.0]
```

**Quality Threshold**:
- Must clearly describe the limitation being worked around
- Must include caveats and risks
- Should note when the workaround becomes unnecessary

### 4. Debugging Technique Patterns

**Definition**: Effective debugging approaches that proved particularly useful for specific types of problems.

**Extraction Criteria**:
- Technique successfully identified a non-obvious issue
- Approach is systematic and repeatable
- Would accelerate debugging similar issues
- Goes beyond basic debugging (not just "add console.log")

**Structure**:
```yaml
type: debugging_technique
problem_class: "[Type of problem this technique addresses]"
indicators:
  - "[Sign that this technique might help]"
  - "[Another indicator]"
technique:
  name: "[Descriptive name]"
  description: "[How it works]"
  steps:
    - "[Step 1]"
    - "[Step 2]"
    - "[Step 3]"
  tools_used:
    - "[Tool 1]"
    - "[Tool 2]"
example_application: |
  [Concrete example of using this technique]
effectiveness:
  typical_time_saved: "[Estimate]"
  success_rate: "[Estimate]"
confidence: [0.0-1.0]
```

**Quality Threshold**:
- Must be specific to a problem class (not generic "debugging")
- Must include clear indicators for when to apply
- Must be actionable with concrete steps

### 5. Project-Specific Patterns

**Definition**: Patterns unique to a particular project's conventions, architecture, or domain.

**Extraction Criteria**:
- Pattern is specific to current project's codebase
- Reflects architectural decisions or conventions
- Would help future work in same project
- Not obvious from reading documentation

**Structure**:
```yaml
type: project_specific
project:
  identifier: "[Unique project identifier]"
  path: "[Project root path]"
  description: "[Brief project description]"
pattern:
  name: "[Pattern name]"
  category: "[e.g., naming, architecture, testing, deployment]"
  description: "[What the pattern is]"
  rationale: "[Why this project uses this pattern]"
examples:
  - file: "[file path]"
    line_range: "[start-end]"
    description: "[What this example shows]"
applies_to:
  - "[Situation 1]"
  - "[Situation 2]"
anti_patterns:
  - "[What not to do]"
confidence: [0.0-1.0]
discovered_date: "[ISO date]"
```

**Quality Threshold**:
- Must be truly project-specific (not general best practice)
- Must include concrete examples from codebase
- Must explain rationale, not just prescription

## Pattern Extraction Process

### Step 1: Session Analysis

Scan the session for learning signals:

```
1. Error/Exception Events
   - Search for error messages, stack traces, failed commands
   - Note which required multiple attempts to resolve
   - Flag solutions that weren't immediately obvious

2. User Corrections
   - Identify messages where user redirected approach
   - Note phrases like "actually", "instead", "don't do that"
   - Capture the before/after of corrections

3. Workarounds Discovered
   - Look for "can't do X, so we'll do Y"
   - Note framework/tool limitations encountered
   - Capture creative solutions to obstacles

4. Debugging Journeys
   - Identify investigation sequences
   - Note hypotheses tested and results
   - Capture successful diagnostic approaches

5. Project Conventions Learned
   - Note corrections about "how we do things here"
   - Capture architectural patterns discovered
   - Record naming conventions and preferences
```

### Step 2: Threshold Evaluation

Apply the extraction threshold to filter noise:

**Include if**:
- [ ] Pattern would save significant time if encountered again
- [ ] Solution wasn't immediately obvious from error/docs
- [ ] Pattern is specific enough to be actionable
- [ ] Context is clear enough for future matching

**Exclude if**:
- [ ] Solution was first result in documentation
- [ ] Pattern is too generic to be useful
- [ ] Context is too narrow (one-time unique situation)
- [ ] Better patterns already exist for this case

**Configurable Threshold**: The extraction sensitivity can be adjusted:

```yaml
# ~/.claude/config/learning.yaml
extraction:
  threshold: 0.7  # 0.0-1.0, higher = more selective
  min_investigation_steps: 3  # Minimum complexity for extraction
  require_root_cause: true    # Must understand why, not just what
  max_patterns_per_session: 10  # Prevent noise
```

### Step 3: Pattern Structuring

For each pattern that passes threshold:

1. **Identify Type** - Classify into one of the five pattern types
2. **Extract Context** - Capture framework, version, environment details
3. **Formulate Trigger** - Define when this pattern should be recalled
4. **Structure Solution** - Format according to type-specific template
5. **Assign Confidence** - Initial confidence based on validation level

### Step 4: Deduplication Check

Before saving, check for existing similar patterns:

```
1. Load existing patterns from ~/.claude/skills/learned/
2. For each candidate pattern:
   a. Search for patterns with similar triggers
   b. Search for patterns in same category/context
   c. Calculate similarity score
3. If similarity > 0.8:
   a. Merge: Combine insights, increment times_applied
   b. Update: If new pattern is more complete, replace
4. If similarity < 0.8:
   a. Save as new pattern
```

**Similarity Calculation**:
- Error patterns: Compare error message patterns
- User corrections: Compare original/corrected approaches
- Workarounds: Compare limitations and solutions
- Debugging: Compare problem classes
- Project-specific: Compare project + pattern category

### Step 5: Storage

Write patterns to the learned skills directory:

```
~/.claude/skills/learned/
  ├── index.yaml                    # Pattern index for quick lookup
  ├── error_resolution/
  │   ├── typescript-null-check.yaml
  │   └── react-hook-deps.yaml
  ├── user_corrections/
  │   └── test-naming-convention.yaml
  ├── workarounds/
  │   └── jest-esm-modules.yaml
  ├── debugging_techniques/
  │   └── async-race-condition.yaml
  └── project_specific/
      └── myproject-123/
          ├── api-naming.yaml
          └── state-management.yaml
```

## Learned Skills Output Format

### Storage Location

All learned patterns are stored in: `~/.claude/skills/learned/`

This location is:
- Persistent across sessions
- Backed up with user's home directory
- Searchable during future sessions

### File Naming Convention

```
{type}/{slug}.yaml

Where:
- type: One of [error_resolution, user_corrections, workarounds,
        debugging_techniques, project_specific]
- slug: Kebab-case descriptive name derived from pattern content

Examples:
- error_resolution/typescript-circular-dependency.yaml
- workarounds/prisma-connection-pooling.yaml
- project_specific/acme-corp/api-versioning.yaml
```

### Skill File Structure

Each learned skill file contains:

```yaml
# Metadata
id: "[UUID]"
type: "[pattern_type]"
created: "[ISO timestamp]"
updated: "[ISO timestamp]"
version: 1

# Pattern Content (type-specific structure from above)
pattern:
  # ... type-specific fields ...

# Usage Tracking
usage:
  times_applied: 0
  times_successful: 0
  times_failed: 0
  last_applied: null

# Confidence Tracking
confidence:
  initial: 0.7
  current: 0.7
  adjustments:
    - date: "[ISO timestamp]"
      reason: "[Why confidence changed]"
      delta: 0.0

# Relationships
related_patterns:
  - id: "[Related pattern UUID]"
    relationship: "[supersedes|supplements|conflicts]"

# Tags for Retrieval
tags:
  - "[tag1]"
  - "[tag2]"
```

### Index File Structure

The `index.yaml` file enables fast pattern lookup:

```yaml
# ~/.claude/skills/learned/index.yaml
version: 1
last_updated: "[ISO timestamp]"
pattern_count: 42

patterns:
  - id: "[UUID]"
    type: "[type]"
    file: "[relative path]"
    triggers:
      - "[trigger phrase 1]"
      - "[trigger phrase 2]"
    tags:
      - "[tag1]"
    confidence: 0.85
    project: null  # or project identifier

  # ... more patterns ...

# Inverted index for fast lookup
trigger_index:
  "TypeError: Cannot read":
    - "[pattern-id-1]"
    - "[pattern-id-2]"
  "ECONNREFUSED":
    - "[pattern-id-3]"

tag_index:
  typescript:
    - "[pattern-id-1]"
    - "[pattern-id-4]"
  react:
    - "[pattern-id-2]"
```

## Stop Hook Configuration

### Overview

The continuous-learning skill can be automatically triggered when a Claude Code session ends, ensuring no valuable patterns are lost.

### Hook Configuration

Create or update the hooks configuration file:

```json
// ~/.claude/hooks.json
{
  "hooks": {
    "stop": [
      {
        "name": "continuous-learning",
        "enabled": true,
        "command": "skill:continuous-learning",
        "config": {
          "threshold": 0.7,
          "interactive": false,
          "summary": true
        }
      }
    ],
    "pre-commit": [],
    "post-error": []
  }
}
```

### Hook Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | true | Whether the hook is active |
| `threshold` | float | 0.7 | Extraction threshold (0.0-1.0) |
| `interactive` | boolean | false | Ask for confirmation before saving |
| `summary` | boolean | true | Display summary of extracted patterns |
| `max_patterns` | int | 10 | Maximum patterns to extract per session |
| `auto_merge` | boolean | true | Automatically merge similar patterns |

### Integration with Claude Code

The hook integrates with Claude Code's lifecycle events:

```
Session Start
     |
     v
Load learned patterns from ~/.claude/skills/learned/
     |
     v
Pattern retrieval during session (automatic matching)
     |
     v
Session End (Stop command or timeout)
     |
     v
Stop hook triggers continuous-learning skill
     |
     v
Extract and save new patterns
     |
     v
Display summary (if configured)
```

### Manual Hook Testing

Test the hook configuration:

```bash
# Validate hooks.json syntax
claude hook validate

# Run the stop hook manually
claude hook run stop

# Check hook execution logs
claude hook logs --hook stop
```

## Pattern Quality Criteria

### What Makes a Pattern Worth Saving

**High-Value Indicators**:

| Indicator | Description | Weight |
|-----------|-------------|--------|
| **Non-Obvious Solution** | Answer wasn't in first search result | High |
| **Time Investment** | Took significant debugging time | High |
| **Root Cause Depth** | Understanding goes beyond symptoms | High |
| **Recurrence Likelihood** | Likely to encounter again | High |
| **Transferability** | Applies beyond immediate context | Medium |
| **Specificity** | Clear trigger conditions | Medium |
| **Actionability** | Concrete steps, not abstract advice | Medium |

**Scoring Model**:
```
quality_score = (
  non_obvious * 0.20 +
  time_investment * 0.15 +
  root_cause_depth * 0.20 +
  recurrence * 0.20 +
  transferability * 0.10 +
  specificity * 0.10 +
  actionability * 0.05
)

# Save if quality_score >= threshold (default 0.7)
```

### Exclusion Criteria

**Do NOT extract patterns that**:

- [ ] Are documented in official docs (first page of results)
- [ ] Are common knowledge for the technology stack
- [ ] Have insufficient context for future matching
- [ ] Are too narrow (unique one-time situation)
- [ ] Are too broad (generic advice without specifics)
- [ ] Lack root cause understanding
- [ ] Would be outdated quickly (version-specific hacks)
- [ ] Duplicate existing patterns without adding value

### Pattern Maintenance

Patterns should be reviewed periodically:

```yaml
# Pattern lifecycle states
lifecycle:
  active: true          # Currently in use
  deprecated: false     # Superseded but kept for reference
  archived: false       # No longer relevant

  # Automatic deprecation triggers
  deprecate_if:
    - confidence_below: 0.3
    - months_unused: 12
    - failed_applications: 5
```

## Example Patterns

### Example 1: Error Resolution

```yaml
# ~/.claude/skills/learned/error_resolution/prisma-client-not-generated.yaml
id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
type: error_resolution
created: "2025-01-15T10:30:00Z"
updated: "2025-01-15T10:30:00Z"
version: 1

pattern:
  trigger: "PrismaClientInitializationError: Unable to require"
  symptoms:
    - "Error occurs on first Prisma query"
    - "Usually after schema changes"
    - "Works locally but fails in CI/Docker"
  root_cause: |
    The Prisma Client was not regenerated after schema changes.
    In Docker/CI environments, the generated client in node_modules
    may be stale or missing because it's not committed to git.
  solution:
    steps:
      - "Run 'npx prisma generate' to regenerate the client"
      - "In Docker, add 'prisma generate' to build steps"
      - "In CI, run generate before tests"
    code_example: |
      # Dockerfile
      RUN npx prisma generate

      # package.json
      "scripts": {
        "postinstall": "prisma generate"
      }
  context:
    framework: "Prisma"
    version: ">=4.0.0"
    environment: "Docker, CI/CD"

usage:
  times_applied: 3
  times_successful: 3
  times_failed: 0
  last_applied: "2025-01-20T14:00:00Z"

confidence:
  initial: 0.8
  current: 0.95
  adjustments:
    - date: "2025-01-20T14:00:00Z"
      reason: "Successfully resolved issue for third user"
      delta: 0.05

tags:
  - prisma
  - docker
  - ci-cd
  - database
```

### Example 2: User Correction

```yaml
# ~/.claude/skills/learned/user_corrections/test-file-colocation.yaml
id: "b2c3d4e5-f6g7-8901-bcde-f12345678901"
type: user_correction
created: "2025-01-18T09:15:00Z"
updated: "2025-01-18T09:15:00Z"
version: 1

pattern:
  original_approach: |
    Created test files in a separate __tests__ directory at project root,
    mirroring the source directory structure.
  corrected_approach: |
    Place test files adjacent to the source files they test,
    using .test.ts or .spec.ts suffix.
  reasoning: |
    The project follows test colocation pattern for several reasons:
    1. Easier to find tests for a given file
    2. Tests move with source files during refactoring
    3. Encourages writing tests (visible reminder)
    4. Reduces directory navigation
  applies_when:
    - "Creating new test files in this project"
    - "Moving or renaming source files"
    - "Setting up test configuration"
  project_specific: true
  project_identifier: "acme-frontend"

usage:
  times_applied: 2
  times_successful: 2
  times_failed: 0
  last_applied: "2025-01-20T11:00:00Z"

confidence:
  initial: 0.9
  current: 0.95
  adjustments: []

tags:
  - testing
  - project-conventions
  - file-organization
```

### Example 3: Workaround

```yaml
# ~/.claude/skills/learned/workarounds/jest-esm-import-assertions.yaml
id: "c3d4e5f6-g7h8-9012-cdef-123456789012"
type: workaround
created: "2025-01-19T16:45:00Z"
updated: "2025-01-19T16:45:00Z"
version: 1

pattern:
  limitation: |
    Jest doesn't support import assertions syntax (import ... with { type: 'json' })
    even with experimental ESM support enabled.
  goal: "Import JSON files in ESM modules being tested with Jest"
  workaround:
    approach: |
      Use createRequire to import JSON files instead of import assertions.
      This works because require() still supports JSON natively.
    steps:
      - "Import createRequire from 'node:module'"
      - "Create a require function scoped to the current module"
      - "Use require() for JSON imports"
    code_example: |
      // Instead of:
      // import config from './config.json' with { type: 'json' };

      // Use:
      import { createRequire } from 'node:module';
      const require = createRequire(import.meta.url);
      const config = require('./config.json');
  caveats:
    - "Slightly more verbose than import assertions"
    - "May need to update when Jest adds proper support"
    - "The require is synchronous, which is fine for JSON"
  better_alternative: |
    When Jest supports import assertions natively, revert to:
    import config from './config.json' with { type: 'json' };
  context:
    tool: "Jest"
    version: "<30.0.0"

usage:
  times_applied: 1
  times_successful: 1
  times_failed: 0
  last_applied: "2025-01-19T16:45:00Z"

confidence:
  initial: 0.85
  current: 0.85
  adjustments: []

tags:
  - jest
  - esm
  - json
  - import-assertions
  - nodejs
```

### Example 4: Debugging Technique

```yaml
# ~/.claude/skills/learned/debugging_techniques/react-stale-closure.yaml
id: "d4e5f6g7-h8i9-0123-defg-234567890123"
type: debugging_technique
created: "2025-01-20T08:00:00Z"
updated: "2025-01-20T08:00:00Z"
version: 1

pattern:
  problem_class: "React hook state appears to have stale values"
  indicators:
    - "State value is always the initial value in callbacks"
    - "Console.log shows correct state, but callback uses old value"
    - "Adding state to useEffect deps causes infinite loop"
    - "Problem appears in setTimeout, setInterval, or event listeners"
  technique:
    name: "Stale Closure Debugger"
    description: |
      Systematically identify which closure is capturing stale values
      and determine the appropriate fix (ref, functional update, or effect cleanup).
    steps:
      - "Add console.log inside the problematic callback showing the state value"
      - "Add console.log in the component body showing current state"
      - "Compare values - if callback shows old value, it's a stale closure"
      - "Check how the callback is created - is it recreated when state changes?"
      - "If callback is memoized (useCallback), check its dependency array"
      - "Determine fix: useRef for value, functional update for setState, or proper deps"
    tools_used:
      - "React DevTools"
      - "Console logging"
      - "ESLint react-hooks plugin"
  example_application: |
    Problem: onClick handler always logs initial count (0)

    // Problematic code
    const [count, setCount] = useState(0);
    const handleClick = useCallback(() => {
      console.log(count); // Always 0!
    }, []); // Missing count in deps

    // Fix options:
    // 1. Add count to deps: useCallback(() => {...}, [count])
    // 2. Use ref: countRef.current
    // 3. Use functional update: setCount(prev => prev + 1)
  effectiveness:
    typical_time_saved: "30-60 minutes"
    success_rate: "~90%"

usage:
  times_applied: 2
  times_successful: 2
  times_failed: 0
  last_applied: "2025-01-20T08:00:00Z"

confidence:
  initial: 0.9
  current: 0.9
  adjustments: []

tags:
  - react
  - hooks
  - closures
  - debugging
  - state-management
```

### Example 5: Project-Specific Pattern

```yaml
# ~/.claude/skills/learned/project_specific/acme-api/error-response-format.yaml
id: "e5f6g7h8-i9j0-1234-efgh-345678901234"
type: project_specific
created: "2025-01-17T14:20:00Z"
updated: "2025-01-17T14:20:00Z"
version: 1

pattern:
  project:
    identifier: "acme-api"
    path: "/home/user/projects/acme-api"
    description: "Backend API service for Acme Corp"
  pattern:
    name: "Standardized Error Response Format"
    category: "api-design"
    description: |
      All API endpoints must return errors in a standardized format
      with specific fields for client consumption and logging.
    rationale: |
      Enables consistent error handling in frontend clients and
      structured logging in the observability platform.
  examples:
    - file: "src/controllers/users.controller.ts"
      line_range: "45-62"
      description: "Validation error response"
    - file: "src/middleware/error-handler.ts"
      line_range: "12-38"
      description: "Global error handler implementation"
  applies_to:
    - "Creating new API endpoints"
    - "Adding error handling to existing endpoints"
    - "Implementing new error types"
  anti_patterns:
    - "Throwing raw Error objects without transformation"
    - "Returning error strings instead of structured objects"
    - "Using HTTP status codes inconsistently"
  response_format: |
    {
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "Human readable message",
        "details": [...],
        "requestId": "uuid",
        "timestamp": "ISO8601"
      }
    }

usage:
  times_applied: 4
  times_successful: 4
  times_failed: 0
  last_applied: "2025-01-21T10:00:00Z"

confidence:
  initial: 0.95
  current: 0.95
  adjustments: []

tags:
  - api
  - error-handling
  - project-conventions
  - acme-api
```

## Workflow Summary

### On Session End (Stop Hook)

```
1. Analyze session for learning signals
   |
   v
2. Apply extraction threshold
   |
   v
3. Structure identified patterns by type
   |
   v
4. Check for duplicates in existing patterns
   |
   v
5. Merge or create new pattern files
   |
   v
6. Update index.yaml
   |
   v
7. Display summary to user (if configured)
```

### Summary Output Format

When the stop hook completes, display:

```
=== Continuous Learning Summary ===

Session analyzed: 2.5 hours, 47 tool calls

Patterns Extracted: 3
  - [error_resolution] TypeScript strict null check fix
  - [user_correction] Prefer named exports in this project
  - [debugging_technique] Async stack trace reconstruction

Patterns Updated: 1
  - [workaround] Jest ESM handling (confidence: 0.85 -> 0.90)

Patterns Skipped: 2
  - Below threshold: Generic TypeScript error (0.45)
  - Duplicate: React hook dependency warning (exists)

Total learned patterns: 47 (across all sessions)

Patterns saved to: ~/.claude/skills/learned/
```

## Best Practices

### Effective Pattern Capture

- **Be specific**: "React useState stale closure in event handler" > "React bug"
- **Include context**: Framework, version, environment conditions
- **Explain why**: Root cause matters more than surface fix
- **Show examples**: Concrete code beats abstract description

### Avoiding Anti-Patterns

- **Don't save obvious solutions**: First Google result doesn't need saving
- **Don't over-generalize**: Keep patterns focused and actionable
- **Don't skip validation**: Patterns should be tested before high confidence
- **Don't ignore updates**: Revisit patterns as frameworks evolve

### Pattern Hygiene

- Review patterns periodically (monthly suggested)
- Deprecate patterns for outdated framework versions
- Merge similar patterns to reduce duplication
- Increase confidence only after successful reuse

## Integration Points

### With Context-Saver Skill

When context-saver runs, it can include a section on "Patterns Discovered":

```markdown
## Patterns Discovered This Session

These patterns have been saved to ~/.claude/skills/learned/:

1. **[error_resolution]** TypeScript strict mode null handling
   - Trigger: "Object is possibly 'undefined'"
   - File: ~/.claude/skills/learned/error_resolution/ts-strict-null.yaml
```

### With Brainstorm Skill

Learned patterns can inform brainstorming sessions:

- Surface relevant patterns when discussing technical approaches
- Reference past workarounds when evaluating options
- Include project-specific patterns in codebase context

### Future Session Retrieval

At session start, patterns are loaded and available for:

- Automatic matching when similar errors occur
- Explicit recall: "What did we learn about X?"
- Pattern suggestions during debugging
