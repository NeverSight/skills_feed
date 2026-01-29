---
name: code-comprehension
description: |
  Quiz users about AI-generated code to build understanding and improve prompting skills.
  Triggers on: /code-comprehension with --setup, --quiz, --status, --mode, --skip, --config, --reset.
  Also activates automatically after generating code to track changes for quizzing.
  Helps users understand their codebase and catch issues before committing.
---

# Code Comprehension Skill

Ensure users understand AI-generated code before committing by quizzing them on what was written.

## State Management

### State File Location
`.claude/quiz-state.json` - Create parent directory if needed.

### State Schema
```json
{
  "version": 1,
  "mode": "commit",
  "pendingChanges": [],
  "completedQuizzes": [],
  "stats": {
    "totalQuizzes": 0,
    "totalPassed": 0,
    "totalFailed": 0,
    "totalSkipped": 0,
    "averageScore": 0,
    "streakCurrent": 0,
    "streakBest": 0
  },
  "config": {
    "questionsPerQuiz": 3,
    "passThreshold": 0.6,
    "showHints": true,
    "trackStreak": true
  }
}
```

### Pending Change Schema
```json
{
  "id": "chg_a1b2c3d4",
  "files": ["src/auth/login.ts", "src/auth/types.ts"],
  "summary": "Added JWT authentication with refresh tokens",
  "codeSnippets": {
    "src/auth/login.ts": "async function login(credentials)..."
  },
  "category": "auth",
  "timestamp": "2026-01-27T10:30:00Z"
}
```

### Completed Quiz Schema
```json
{
  "changeId": "chg_a1b2c3d4",
  "passed": true,
  "score": 3,
  "total": 4,
  "percentage": 0.75,
  "timestamp": "2026-01-27T10:45:00Z",
  "questions": [
    {"question": "...", "userAnswer": "B", "correct": true}
  ]
}
```

### Reading State
1. Check if `.claude/quiz-state.json` exists
2. If not, return null (skill not set up)
3. Read and parse JSON
4. Validate version field matches expected
5. Return state object

### Writing State
1. Ensure `.claude/` directory exists
2. Serialize state to formatted JSON (2-space indent)
3. Write atomically to `.claude/quiz-state.json`

### State Recovery
If state file is corrupted or invalid JSON:
1. Notify user of corruption
2. Offer to reset state (preserving stats if possible)
3. Create fresh state file

---

## Commands

### `--setup`

Initialize the skill for current project.

**Steps:**
1. Check if already set up (state file exists)
   - If yes, ask user if they want to reinitialize
2. Create `.claude/` directory if needed
3. Write initial state to `.claude/quiz-state.json`
4. Check `.gitignore` for `.claude/quiz-state.json`
   - If not present, append it
5. Check if `.git/hooks/pre-commit` exists
   - If exists, check if it's ours or user's custom hook
   - If custom, warn user and offer to create `.git/hooks/pre-commit.d/` setup
6. Write pre-commit hook (see Hook Script section)
7. Make hook executable
8. Display success message with next steps

**Hook Script:**
```bash
#!/bin/bash
# Code Comprehension Skill - Pre-commit Hook
# Blocks commits when there are pending quizzes

set -e

STATE_FILE=".claude/quiz-state.json"

# Skip if state file doesn't exist (skill not active)
if [ ! -f "$STATE_FILE" ]; then
  exit 0
fi

# Check for pending changes using jq if available, fallback to grep
if command -v jq &> /dev/null; then
  PENDING_COUNT=$(jq '.pendingChanges | length' "$STATE_FILE" 2>/dev/null || echo "0")
else
  # Fallback: count array elements with grep
  PENDING_COUNT=$(grep -c '"id":' "$STATE_FILE" 2>/dev/null || echo "0")
fi

if [ "$PENDING_COUNT" -gt 0 ]; then
  echo ""
  echo "╔════════════════════════════════════════════════════════════╗"
  echo "║  📚 Code Comprehension Quiz Required                       ║"
  echo "╠════════════════════════════════════════════════════════════╣"
  echo "║  You have $PENDING_COUNT pending code change(s) to review.          ║"
  echo "║                                                            ║"
  echo "║  Take the quiz:    /code-comprehension --quiz              ║"
  echo "║  Check status:     /code-comprehension --status            ║"
  echo "║  Skip (logged):    /code-comprehension --skip              ║"
  echo "║                                                            ║"
  echo "║  Or bypass with:   git commit --no-verify                  ║"
  echo "╚════════════════════════════════════════════════════════════╝"
  echo ""
  exit 1
fi

exit 0
```

**Success Message:**
```
✅ Code Comprehension Skill Setup Complete!

📁 State file: .claude/quiz-state.json
🔒 Git hook: .git/hooks/pre-commit
📝 Added to .gitignore

Current mode: commit (quiz at commit time)
Change to strict mode: /code-comprehension --mode strict

You're all set! I'll track code changes and quiz you before commits.
```

---

### `--mode strict|commit`

Change when quizzes occur.

**Strict Mode:**
- Quiz immediately after each code generation
- Cannot continue until quiz is passed
- Best for learning new technologies

**Commit Mode (default):**
- Track changes silently during session
- Quiz only when attempting to commit
- Better for experienced developers

**Steps:**
1. Read current state
2. Validate mode argument is "strict" or "commit"
3. Update `mode` field
4. Write state
5. Confirm change to user

---

### `--quiz`

Start quiz session for pending changes.

**IMPORTANT: Use batch mode for speed!**

Instead of asking questions one at a time (slow), generate ALL questions upfront
and ask them in a SINGLE AskUserQuestion call (supports up to 4 questions).

**Fast Quiz Flow:**
1. Read state, verify setup
2. Check for pending changes
   - If none: "No pending quizzes. You're all caught up!"
3. For each pending change:
   a. Display change header (files, summary)
   b. Read the actual file contents for context
   c. **Generate ALL questions at once** (2-4 based on complexity)
   d. **Ask ALL questions in ONE AskUserQuestion call**
   e. **Process all answers together**
   f. **Show batch results with all feedback**
4. Calculate final score
5. If passed (≥ threshold):
   - Move to completedQuizzes
   - Update stats (increment passed, update streak)
   - Congratulate user

**Example batch question call:**
```typescript
AskUserQuestion({
  questions: [
    {
      question: "Q1: In StatCard, what happens if trend prop is missing?",
      header: "Design",
      options: [
        { label: "A) Throws error", description: "..." },
        { label: "B) Uses neutral gray", description: "..." },
        // ...
      ]
    },
    {
      question: "Q2: What does auto-fit do on narrow screens?",
      header: "CSS Grid",
      options: [...]
    },
    {
      question: "Q3: What determines the trend color threshold?",
      header: "Logic",
      options: [...]
    }
  ]
})
```

This reduces 3 round-trips to 1, making quizzes ~3x faster!
6. If failed:
   - Show which questions were wrong with explanations
   - Offer options: Retry / Explain Code / Skip
   - If retry: restart quiz for this change
   - If explain: provide detailed code walkthrough
   - If skip: move to completed with failed status, update stats

---

### `--status`

Display current quiz status and statistics.

**Output Format:**
```
📊 Code Comprehension Status
═══════════════════════════════════════

Mode: commit
Pending quizzes: 2

📋 Pending Changes:
  1. chg_a1b2c3d4 - Added JWT authentication
     Files: src/auth/login.ts, src/auth/types.ts
     Tracked: 10 minutes ago

  2. chg_e5f6g7h8 - Created user dashboard component
     Files: src/components/Dashboard.tsx
     Tracked: 5 minutes ago

📈 Statistics:
  Total quizzes: 15
  Passed: 12 (80%)
  Failed: 2
  Skipped: 1
  Average score: 78%
  Current streak: 5 🔥
  Best streak: 8

💡 Run /code-comprehension --quiz to start
```

---

### `--skip`

Skip all pending quizzes (logged in stats).

**Steps:**
1. Read state
2. Confirm with user: "Skip all N pending quizzes? This will be logged."
3. If confirmed:
   - Move all pending to completed with `passed: false, skipped: true`
   - Increment `stats.totalSkipped`
   - Reset streak to 0
   - Write state
4. Warn user about learning impact

---

### `--config [key] [value]`

View or update configuration.

**Available Settings:**
- `questionsPerQuiz`: 2-5 (default: 3)
- `passThreshold`: 0.5-1.0 (default: 0.6)
- `showHints`: true/false (default: true)
- `trackStreak`: true/false (default: true)

**No arguments:** Display current config
**With arguments:** Update specified setting

---

### `--reset`

Reset all quiz state (keeps config).

1. Confirm with user
2. Clear pendingChanges and completedQuizzes
3. Reset stats to zeros
4. Preserve config
5. Write state

---

## Automatic Change Tracking

**CRITICAL: After EVERY Write or Edit tool use**, track the change with full context.

### What to Capture

For effective contextual quizzing, track:

1. **User's Original Request**
   - What did the user ask for?
   - What problem were they trying to solve?
   - Any specific requirements mentioned?

2. **Implementation Details**
   - Files created/modified
   - Key functions, components, classes
   - Libraries/packages used
   - Design patterns applied

3. **Decisions Made**
   - Why this approach over alternatives?
   - What trade-offs were considered?
   - What edge cases are handled?

4. **Code Context**
   - Function/component names
   - Important variable names
   - Key logic flows
   - Error handling approach

### Categories
Detect based on file path and content:
- `frontend`: React, Vue, Svelte, CSS, HTML components
- `backend`: API routes, controllers, services
- `database`: Models, migrations, queries
- `auth`: Authentication, authorization, tokens
- `infra`: Config, Docker, CI/CD, deployment
- `test`: Test files
- `general`: Everything else

### Tracking Steps
1. Read current state
2. Generate unique ID: `chg_` + 8 random alphanumeric chars
3. Create pending change object:
```json
{
  "id": "chg_a1b2c3d4",
  "userPrompt": "Add user authentication with JWT",
  "files": ["src/auth/login.ts", "src/auth/middleware.ts"],
  "summary": "Implemented JWT auth with refresh tokens",
  "category": "auth",
  "timestamp": "2026-01-27T10:30:00Z",
  "context": {
    "functions": ["login", "verifyToken", "refreshToken"],
    "components": [],
    "imports": ["jsonwebtoken", "bcrypt"],
    "keyDecisions": [
      "Used JWT over sessions for stateless auth",
      "Implemented refresh token rotation for security",
      "Added 15min access token expiry"
    ],
    "edgeCases": [
      "Handles expired tokens with 401",
      "Validates email format before DB lookup"
    ]
  }
}
```
4. Append to `pendingChanges`
5. Write state

### Strict Mode Behavior
If `mode === "strict"`:
1. After tracking, immediately announce quiz
2. Generate and present questions
3. User must pass before you continue with other tasks
4. If user tries to continue without passing, remind them

### Commit Mode Behavior
If `mode === "commit"`:
1. Track silently (no user notification)
2. Continue with requested tasks
3. Quiz happens at commit time via hook

---

## Question Generation

### CRITICAL: Contextual Questions Only

**Questions MUST be specific to:**
1. **The user's original request** - What they asked to be built
2. **The actual implementation** - The specific code that was written
3. **Decisions made** - Why this approach vs alternatives

**NEVER ask generic questions.** Every question must reference:
- Actual function/component/variable names from the code
- Specific line numbers or code snippets
- Real values, parameters, or return types used
- Actual libraries/packages imported

### Context to Capture When Tracking Changes

When tracking a code change, store:
```json
{
  "id": "chg_xxx",
  "userPrompt": "The original request from the user",
  "files": ["path/to/file.ts"],
  "summary": "What was implemented",
  "keyDecisions": [
    "Used JWT instead of sessions because...",
    "Chose useState over useReducer because..."
  ],
  "codeContext": {
    "functions": ["validateUser", "generateToken"],
    "components": ["LoginForm", "AuthProvider"],
    "imports": ["jsonwebtoken", "bcrypt"],
    "patterns": ["factory pattern for token generation"]
  }
}
```

### Question Generation Process

1. **Read the user's original prompt** - What did they ask for?
2. **Read the actual code** - What was implemented?
3. **Identify key aspects:**
   - What libraries/frameworks were used?
   - What functions/components were created?
   - What edge cases are handled?
   - What would happen if X fails?
   - Why was approach A chosen over B?
4. **Generate questions that test if user understands THIS specific code**

### Principles
1. **Test understanding, not memorization** - Ask "why" not just "what"
2. **Make wrong answers plausible** - Based on real alternatives
3. **Be 100% specific to the code** - Reference actual names, values, patterns
4. **Connect to user's intent** - "You asked for X, this code does Y because..."
5. **Educational value** - Every question teaches something about THIS implementation

### Example: Contextual vs Generic

**User prompt:** "Add a login form with validation"

**Code written:**
```tsx
function LoginForm() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!email.includes('@')) {
      setError('Invalid email format');
      return;
    }
    // ... api call
  };
}
```

**BAD (Generic):**
> "What React hook is used for state management?"

**GOOD (Contextual):**
> "In the LoginForm component, why is there a separate `error` state instead of
> validating inline in the JSX? What happens when `setError('Invalid email format')`
> is called?"

**BAD (Generic):**
> "What does useState return?"

**GOOD (Contextual):**
> "In handleSubmit, why does the validation check `!email.includes('@')` happen
> BEFORE the API call? What would happen if we removed this check?"

### Question Count
Based on change complexity:
- Small change (1 file, < 50 lines): 2 questions
- Medium change (1-3 files, 50-200 lines): 3 questions
- Large change (3+ files or 200+ lines): 4-5 questions

Override: Use `config.questionsPerQuiz` if set

### Reference Files (For Question Patterns Only)

Use reference files for **inspiration on question types**, but always make questions specific to the actual code:

**Example transformation:**

Reference pattern: *"What happens if [parameter] is null?"*

Contextual question: *"In `validateUser(email)`, what happens if `email` is undefined? Look at line 15."*

**See reference files for question type inspiration:**

| Category | Reference File |
|----------|---------------|
| General (any code) | [references/general-questions.md](references/general-questions.md) |
| Frontend (React, Vue, CSS) | [references/frontend-questions.md](references/frontend-questions.md) |
| React-specific | [references/react-questions.md](references/react-questions.md) |
| Backend (APIs, services) | [references/backend-questions.md](references/backend-questions.md) |
| API Design | [references/api-design-questions.md](references/api-design-questions.md) |
| Auth & Security | [references/auth-questions.md](references/auth-questions.md) |
| Security Deep Dive | [references/security-deep-dive.md](references/security-deep-dive.md) |
| Database | [references/database-questions.md](references/database-questions.md) |
| TypeScript | [references/typescript-questions.md](references/typescript-questions.md) |
| Testing | [references/testing-questions.md](references/testing-questions.md) |
| Async/Promises | [references/async-questions.md](references/async-questions.md) |
| DevOps/Infra | [references/devops-questions.md](references/devops-questions.md) |
| Design Patterns | [references/patterns-questions.md](references/patterns-questions.md) |
| Edge Cases | [references/edge-cases.md](references/edge-cases.md) |

### Question Structure

**Multiple Choice (Primary):**
```
Question 2 of 3: Edge Cases

In the `validateUser` function, what happens if the email parameter is undefined?

A) Returns null silently
B) Throws a ValidationError with message "Email required"
C) Returns an empty user object
D) Logs a warning and continues with empty string

[If hints enabled and user requests]:
💡 Hint: Look at line 15 where the validation starts
```

**Open-ended (Use sparingly):**
```
Question 3 of 3: Architecture

Why is the authentication logic separated into its own module instead of
being inline in the route handler? Explain the benefits.

[Evaluate response for key concepts: separation of concerns, reusability,
testability, single responsibility]
```

### Answer Evaluation

**MCQ:**
- Correct: Full point, brief positive reinforcement
- Wrong: Zero points, explain correct answer thoroughly

**Open-ended:**
- Check for key concepts (define 3-5 per question)
- 1.0 points: Mentions most/all concepts clearly
- 0.5 points: Mentions some concepts or shows partial understanding
- 0.0 points: Misses key concepts or shows misunderstanding

### Feedback Format

**Correct Answer:**
```
✅ Correct!

The function throws a ValidationError because input validation should fail
fast and explicitly. This follows the "fail early" principle - catching
invalid data at the boundary prevents harder-to-debug issues downstream.
```

**Wrong Answer:**
```
❌ Not quite. The correct answer is B.

The function throws a ValidationError with "Email required" because:
1. Explicit validation happens on line 15-18
2. The guard clause checks for falsy values first
3. This follows fail-fast principles for input validation

The code:
\`\`\`typescript
if (!email) {
  throw new ValidationError("Email required");
}
\`\`\`
```

---

## Quiz Flow Example (Batch Mode - FAST)

**IMPORTANT:** Ask ALL questions at once using AskUserQuestion with multiple questions.
This is 3x faster than asking one at a time!

**User's original request:** "Add user authentication with JWT tokens"

### Step 1: Show Header
```
╔════════════════════════════════════════════════════════════╗
║  📚 Code Comprehension Quiz                                ║
╚════════════════════════════════════════════════════════════╝

You asked: "Add user authentication with JWT tokens"
I implemented: JWT auth with refresh token rotation

Change: chg_a1b2c3d4
Files: src/auth/login.ts, src/auth/types.ts

Answer all 3 questions below:
```

### Step 2: Ask ALL Questions at Once

Use a SINGLE AskUserQuestion call with multiple questions:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "In the `login` function, what happens BEFORE bcrypt.compare()?",
      header: "Q1: Flow",
      options: [
        { label: "A) Validates email format", description: "Regex check first" },
        { label: "B) Looks up user by email", description: "Database query" },
        { label: "C) Checks account lock", description: "Security check" },
        { label: "D) Hashes the password", description: "Prepares for compare" }
      ],
      multiSelect: false
    },
    {
      question: "What is refresh token rotation in `refreshToken` function?",
      header: "Q2: Security",
      options: [
        { label: "A) Tokens never expire", description: "Permanent tokens" },
        { label: "B) Old token stays valid", description: "Reusable tokens" },
        { label: "C) New token + invalidate old", description: "One-time use" },
        { label: "D) Stored in localStorage", description: "Client storage" }
      ],
      multiSelect: false
    },
    {
      question: "If findUserByEmail throws a DB error, what happens?",
      header: "Q3: Errors",
      options: [
        { label: "A) Returns null", description: "Silent failure" },
        { label: "B) Throws AuthError", description: "Hides real error" },
        { label: "C) Throws DB error", description: "Propagates up" },
        { label: "D) Retries 3 times", description: "Retry logic" }
      ],
      multiSelect: false
    }
  ]
})
```

### Step 3: Process All Answers & Show Batch Results

After user answers all questions at once, show consolidated feedback:

```
═══════════════════════════════════════════════════════════════
📊 Quiz Results
═══════════════════════════════════════════════════════════════

Q1: Flow ✅ Correct!
   You answered: B) Looks up user by email

   The code calls findUserByEmail() first because we need the stored
   password hash before we can compare with bcrypt.

Q2: Security ❌ Incorrect
   You answered: A) Tokens never expire
   Correct answer: C) New token + invalidate old

   Refresh token rotation means each use creates a NEW token and
   invalidates the old one. This limits damage if a token is stolen.

Q3: Errors ✅ Correct!
   You answered: C) Throws DB error

   The catch block only handles AuthError. Database errors propagate
   up unchanged, triggering 500 responses and alerts.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Score: 2/3 (67%) - PASSED ✅
Streak: 1 🔥

You can now commit your changes!
```

### Why Batch Mode is Better

| Approach | Round Trips | User Experience |
|----------|-------------|-----------------|
| One at a time | 3 | Slow, interrupting |
| **Batch (recommended)** | **1** | **Fast, smooth** |

Always use batch mode unless you have a specific reason not to.

---

## Error Handling

### State File Missing
```
⚠️ Code Comprehension skill not set up for this project.

Run: /code-comprehension --setup
```

### State File Corrupted
```
⚠️ Quiz state file appears corrupted.

Would you like to:
1. Reset state (loses history)
2. Try to recover (may lose recent data)
3. Show raw file for manual fix
```

### No Git Repository
```
⚠️ Not a git repository. Pre-commit hook won't work.

The skill can still track changes and quiz you manually.
Continue with setup? (quiz tracking only)
```

### Hook Already Exists
```
⚠️ A pre-commit hook already exists at .git/hooks/pre-commit

Options:
1. View existing hook
2. Append our check to existing hook
3. Replace with our hook (backs up original)
4. Skip hook installation (manual quiz only)
```
