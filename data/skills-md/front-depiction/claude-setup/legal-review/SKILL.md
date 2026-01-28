---
name: legal-review
description: Orchestrate lawyer agents to review code for compliance with codebase laws. Spawns counsel in parallel to produce a unified legal brief.
---

# Legal Review

Orchestrates legal counsel to review code for compliance with codebase laws and standards. Determines applicable laws based on file patterns, spawns lawyers in PARALLEL, then aggregates findings into a unified legal brief.

## Execution Protocol

You are the Legal Review Coordinator. Follow this protocol exactly:

### Phase 1: Resolve Scope

Interpret natural language arguments to determine what files to review.

```
interpretScope :: $ARGUMENTS -> Scope
interpretScope args
  | null args                                    = Staged
  | isFilePath args                              = Files [args]
  | mentions "staged"                            = Staged
  | mentions "unstaged" || mentions "diff"       = Diff
  | mentions "all" || mentions "entire" ||
    mentions "everything" || mentions "codebase" = All
  | mentions "today" || mentions "changed"       = ChangedToday
  | otherwise                                    = Search (extractIntent args)
```

**Natural Language Patterns:**

| Pattern | Interpretation | Resolution Strategy |
|---------|----------------|---------------------|
| `the chat component` | Component search | Glob for `**/chat*.ts`, `**/Chat*.tsx` |
| `all VM files in the UI app` | Scoped pattern | Glob for `apps/ui/**/*.vm.ts` |
| `my staged changes` | Git staged | `git diff --cached --name-only` |
| `the sidebar and navigation` | Multiple components | Glob for each term |
| `everything I changed today` | Recent changes | `git diff --name-only $(git log --since="midnight" --format=%H | tail -1)^` |
| `the user authentication flow` | Domain search | Grep for auth patterns, Glob for auth files |

**Execute scope resolution based on interpretation:**

```bash
# For Staged (default, or "my staged changes"):
git diff --cached --name-only

# For Diff ("unstaged changes", "my diff"):
git diff --name-only

# For ChangedToday ("everything I changed today", "today's changes"):
git log --since="midnight" --name-only --format="" | sort -u

# For Files (explicit path like "src/components/Chat.vm.ts"):
# Use the provided file path directly

# For All ("the entire codebase", "all files"):
# Use Glob to find all *.ts and *.tsx files

# For Search (component/domain references):
# Use Glob and Grep to find relevant files
```

**Search Resolution Examples:**

When the user says "the chat component":

```bash
# Try multiple patterns to find relevant files
glob "**/chat*.ts" "**/Chat*.tsx" "**/chat/**"
grep -l "Chat" --include="*.ts" --include="*.tsx"
```

When the user says "all VM files in the UI app":

```bash
glob "apps/ui/**/*.vm.ts"
```

When the user says "the sidebar and navigation components":

```bash
glob "**/sidebar*.ts" "**/Sidebar*.tsx" "**/navigation*.ts" "**/Navigation*.tsx"
glob "**/nav*.ts" "**/Nav*.tsx"
```

When the user says "the user authentication flow":

```bash
grep -l "auth" "login" "session" --include="*.ts" --include="*.tsx"
glob "**/auth/**" "**/login/**" "**/session/**"
```

### Phase 2: Determine Applicable Laws

Match files to applicable bodies of law based on patterns:

| Body of Law | Pattern | Skill | Status |
|-------------|---------|-------|--------|
| VM Architecture Laws | `*.vm.ts` | `the-vm-standard` | ACTIVE |
| Effect Pattern Laws | `*.ts` (Effect code) | `effect-patterns-law` | FUTURE |
| Schema Laws | `**/Schema*.ts`, `**/domain/**` | `schema-law` | FUTURE |
| Layer Composition Laws | `**/Layer*.ts`, `**/*Layer.ts` | `layer-law` | FUTURE |
| Error Handling Laws | `**/errors/**`, `**/*Error.ts` | `error-handling-law` | FUTURE |
| Testing Laws | `*.test.ts`, `*.spec.ts` | `testing-law` | FUTURE |

```
determineApplicableLaws :: [FilePath] -> [(Law, [FilePath])]
determineApplicableLaws files = do
  let vmFiles = filter (matches "*.vm.ts") files
  -- Add more laws here as they become active
  catMaybes
    [ guard (not (null vmFiles)) >> pure (VMArchitectureLaw, vmFiles)
    ]
```

If no files match any active law jurisdiction, report: "No files within active law jurisdiction. Review complete."

### Phase 3: Dispatch Lawyer in PARALLEL

For each body of law with applicable files, spawn a lawyer agent IN PARALLEL.

**CRITICAL**: Spawn all applicable lawyers simultaneously using parallel agent dispatch.

#### Lawyer Agent

Spawn the `/lawyer` agent with appropriate context:

<lawyer-agent-prompt>
You are legal counsel for this codebase. Your task is to review the following files for compliance with applicable laws.

**Files under review:**
$FILES

**Applicable laws based on file patterns:**
$APPLICABLE_LAWS

**Your authority:** You are the `/lawyer` agent. Load relevant law skills for the full specifications.

**Procedure:**

1. Determine which laws apply to each file based on patterns
2. Load each applicable law skill (e.g., `/the-vm-standard` for *.vm.ts files)
3. Read each file completely
4. Audit against all applicable statutes systematically
5. Issue formal legal opinion with charges for any violations

**Required output format:**
For each file, produce a verdict with:

- File path
- Applicable laws
- Compliance status (COMPLIANT | VIOLATION | ADVISORY)
- For violations: charges citing specific law, statute, line number, evidence, and remedy
</lawyer-agent-prompt>

### Phase 4: Await and Aggregate

After all lawyers complete, aggregate findings:

```
data Finding = Finding
  { law       :: Law              -- e.g., VMArchitectureLaw
  , file      :: FilePath
  , severity  :: Severity         -- Critical | Major | Minor | Advisory
  , statute   :: String           -- e.g., "VM-COVENANT-VII" or "EFFECT-PATTERN-III"
  , violation :: Description
  , evidence  :: (LineNumber, CodeSnippet)
  , remedy    :: Recommendation
  }

data Verdict
  = Approved            -- no Critical or Major findings
  | ConditionalApproval -- Major findings exist
  | Blocked             -- Critical findings must be resolved

verdict :: [Finding] -> Verdict
verdict findings
  | any ((== Critical) . severity) findings = Blocked
  | any ((== Major) . severity) findings    = ConditionalApproval
  | otherwise                                = Approved
```

### Phase 5: Produce Legal Brief

Output the unified legal brief:

```
===============================================================================
                          LEGAL BRIEF
===============================================================================

SCOPE: [Staged | Diff | Files [...] | All]
FILES REVIEWED: [count] files
LAWS APPLIED: [list of bodies of law consulted]

-------------------------------------------------------------------------------
                        EXECUTIVE SUMMARY
-------------------------------------------------------------------------------

| Severity | Count |
|----------|-------|
| Critical | N     |
| Major    | N     |
| Minor    | N     |
| Advisory | N     |

VERDICT: [Approved | Conditional Approval | Blocked]

-------------------------------------------------------------------------------
                        COUNSEL OPINIONS
-------------------------------------------------------------------------------

## VM Architecture Laws

[Full opinion for VM files]

## [Other Laws - when active]

[Full opinion for other jurisdictions]

-------------------------------------------------------------------------------
                        RECOMMENDATIONS
-------------------------------------------------------------------------------

[Prioritized remediation steps, Critical first, then Major]

===============================================================================
                        BRIEF CONCLUDED
===============================================================================
```

## Usage Examples

```bash
# Review staged changes (default)
/legal-review
/legal-review my staged changes

# Review specific file (still supported)
/legal-review src/components/Chat.vm.ts

# Review by component name
/legal-review the chat component
/legal-review the sidebar and navigation components

# Review by domain/feature
/legal-review the user authentication flow
/legal-review everything related to sessions

# Review scoped to an app or package
/legal-review all VM files in the UI app
/legal-review the services in packages/ai

# Review by time
/legal-review everything I changed today
/legal-review my recent changes

# Review unstaged changes
/legal-review my unstaged changes
/legal-review the current diff

# Review entire codebase (expensive)
/legal-review the entire codebase
/legal-review all files
```

## Extending: Adding New Bodies of Law

To add a new body of law:

1. **Define the law** - Create `.claude/skills/{law-name}/SKILL.md` with the statutes
2. **Add to jurisdiction table** - Add pattern and skill name to Phase 2 table above
3. **Activate** - Change status from FUTURE to ACTIVE in jurisdiction table

The lawyer agent (`/lawyer`) automatically loads applicable law skills based on file patterns. The lawyer's jurisdiction table must also be updated to match.

## Severity Definitions

| Severity | Definition | Merge Impact |
|----------|------------|--------------|
| Critical | Fundamental violation that will cause runtime issues or architectural decay | BLOCKS merge |
| Major | Significant deviation from standards that should be fixed | Should fix before merge |
| Minor | Style or convention issues | Fix when convenient |
| Advisory | Suggestions for improvement | Optional |
