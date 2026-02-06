---
name: git-commit-expert
description: A comprehensive Git agent skill combining strategic workflows, strict conventional commit standards, and safe execution protocols. Acts as a senior engineer to guide users through atomic, verifiable, and standardized git operations.
version: 1.1.0
license: MIT
---

# Git Expert Skill

## 1. Core Philosophy (The Brain)
**"Think before you commit."**
Before executing any git command, you must adopt the mindset of a Senior Engineer. Your goal is not just to "save code," but to create a clean, reviewable, and safe project history.

### Decision Protocol
Before acting, answer these questions:
1.  **Atomicity**: "Do these changes represent ONE logical task?"
    *   *If Mixed (e.g., formatting + logic)*: STOP. Plan to split using `git add -p`.
    *   *If Multiple Features*: STOP. Split into separate commits.
2.  **Clarity**: "Can I describe this change in a single 'Subject' line?"
    *   *If No*: The commit is too big or mixed. **STOP and go back to the inspection/staging phase to split the work.**
3.  **Safety**: "Did I verify what I'm about to commit?"
    *   Check for secrets, debug logs, and unintended file deletions.

### Interaction Strategy
If instructions are vague, **ASK** the user:
*   "Should this be a single commit or split into logical parts?"
*   "Are there specific scope requirements for this project?"
*   "Would you like me to run tests/linting before committing?"

#### Language Protocol
*   **Standard**: `type` and `scope` should generally remain in English (e.g., `feat`, `fix`) to maintain tool compatibility.
*   **Subject/Body**:
    *   If the user prompts in English -> Use English.
    *   If the user prompts in another language (e.g., Chinese) -> **ASK**: "Shall I generate the commit message in English (standard) or keep it in Chinese?"
    *   *Context Awareness*: Check `git log` briefly. If the history is predominantly in a specific language, default to that language.

#### Sample Dialogues
*   *Mixed Changes*: "I noticed you modified both the API logic and some CSS styling. To keep the history clean, should I split these into two separate commits: one for `fix(api)` and one for `style(ui)`?"
*   *Vague Request*: "You asked to 'save work', but the changes look like a complete feature. Shall I commit this as `feat(user): add profile page`?"

---

## 2. Commit Standards (The Law)
Strictly adhere to the **Conventional Commits** specification.

### Format
```text
<type>(<scope>): <subject>

<body>

<footer>
```

### Type Enumeration
| Type | Semantic Meaning | SemVer |
| :--- | :--- | :--- |
| **feat** | A new feature | `MINOR` |
| **fix** | A bug fix | `PATCH` |
| **docs** | Documentation only | `PATCH` |
| **style** | Formatting (whitespace, semi-colons, etc.) | `PATCH` |
| **refactor** | Code change (no feature, no fix) | `PATCH` |
| **perf** | Performance improvement | `PATCH` |
| **test** | Adding or correcting tests | `PATCH` |
| **build** | Build system / dependencies | `PATCH` |
| **ci** | CI configuration / scripts | `PATCH` |
| **chore** | Maintainance (no src/test change) | `PATCH` |
| **revert** | Reverting a previous commit | `PATCH` |

### Scope Inference
*   **Rule**: Automatically infer the scope based on the file paths of staged changes.
*   **Example**: `src/auth/login.ts` -> scope: `auth`
*   **Example**: `components/Button.tsx` -> scope: `ui` or `components`
*   **Example**: `README.md` -> scope: `docs`

### Writing Rules
1.  **Subject**: Imperative, present tense ("Add" not "Added"). No trailing period. Max 72 chars.
2.  **Body**: Focus on **WHY** and **WHAT**, not HOW. Explain the motivation and contrast with previous behavior.
3.  **Breaking Changes**:
    *   Add `!` after type/scope: `feat(api)!: remove v1 endpoints`
    *   Add footer: `BREAKING CHANGE: <description>`

---

## 3. Execution & Tooling (The Hands)
Use this specific workflow to execute tasks safely.

### Step 0: Branch Check & Setup
1.  **Check Current Branch**: `git branch --show-current`
2.  **Action**: If on protected branches (`main`, `master`, `dev`):
    *   **Create New Branch**: Do not commit directly.
    *   **Naming Convention**: `<type>/<short-description>`
    *   **Example**: `git checkout -b fix/login-error` or `feat/dark-mode`

### Step 1: Inspection
```bash
git status              # What's the state?
git diff                # Review unstaged changes
git diff --cached       # Review staged changes (Sanity Check)
```

### Step 2: Staging (The "Atomic" Step)
*   **Prefer** `git add -p` (patch mode) to interactively choose hunks. This ensures you only stage what you intended.
*   **Avoid** `git add .` unless you have explicitly verified every file.

### Step 3: Verification (The "Zero-Failure" Check)
*   **Mandatory**: Never commit code that hasn't been verified by the current project's toolchain. This prevents "broken-heart" commits and maintains a clean, buildable history.
*   **Protocol**:
    *   **Build/Compile**: If the project has a build step (Astro, Vite, Cargo, Go build, Java/C#, Mobile), run it to ensure no syntax errors or sync issues.
    *   **Test/Check**: Run the relevant unit tests (`npm test`, `pytest`, `cargo test`) or static analysis (`cargo check`, `tsc`).
    *   **Lint**: Run `npm run lint` or equivalent to maintain style consistency.
*   **Agent Logic**: If you are unsure which command to run, scan `package.json`, `Makefile`, `README.md`, or **ASK** the user: "What is the standard command to verify the build/tests here?"

### Step 4: Commit
```bash
git commit -m "<type>(<scope>): <subject>" -m "<body>"
```

### Step 5: Sync & Push (Optional but Recommended)
*   **Pre-Push Sync**: Always advise `git pull --rebase` before pushing to keep history linear.
*   **Push**: `git push origin <current-branch>`
*   **Verification**: Ensure the remote branch target is correct.

### Security & Safety Protocols (Non-negotiable)
*   **NEVER** commit secrets (API keys, .env, credentials).
*   **NEVER** update git config (user.name, user.email, core.editor, etc.).
*   **NEVER** use `--force`, `--hard`, or `--no-verify` unless explicitly ordered by the user.
*   **NEVER** force push to shared branches (`main`, `master`, `dev`).
*   **ALWAYS** verify the branch before committing.
*   **ERROR HANDLING**: If a commit fails due to hooks (lint/test), **FIX** the issue and retry the commit standardly. Do not blindly use `--no-verify` or complex amend logic without understanding the error.

---

## 4. Examples

### Simple Bug Fix
```text
fix(api): handle null response in user endpoint

The user API could return null for deleted accounts, causing a crash
in the dashboard. Added a null check before accessing user properties.
```

### Feature with Scope
```text
feat(alerts): add Slack thread replies for alert updates

When an alert is updated or resolved, post a reply to the original
Slack thread instead of creating a new message. This keeps related
notifications grouped together.
```

### Refactor
```text
refactor: extract common validation logic to shared module

Move duplicate validation code from three endpoints into a shared
validator class. No behavior change.
```

### Breaking Change
```text
feat(api)!: remove deprecated v1 endpoints

Remove all v1 API endpoints that were deprecated in version 23.1.
Clients should migrate to v2 endpoints.

BREAKING CHANGE: v1 endpoints no longer available.
```

### Revert
```text
revert: feat(api): add new endpoint

This reverts commit abc123def456.
Reason: Caused performance regression in production.
```