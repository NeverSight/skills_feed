---
name: review-ruby-code
description: Comprehensive Ruby and Rails code review using Sandi Metz rules and SOLID principles. Automatically runs rubycritic and simplecov, analyzes changed files in current branch vs base branch, identifies OOP violations, Rails anti-patterns, security issues, and test coverage gaps. Outputs REVIEW.md with VSCode-compatible file links. Use when reviewing Ruby/Rails code, conducting code reviews, checking for design issues, or when user mentions code review, pull request review, or code quality analysis.
---

<objective>
Perform comprehensive code reviews of Ruby and Rails applications by analyzing changes in the current branch against the base branch. Apply Sandi Metz rules and SOLID principles to identify design issues, detect Rails anti-patterns and performance problems, flag security vulnerabilities, and assess test coverage. Generate a structured REVIEW.md file with VSCode-compatible links to every referenced line of code, incorporating findings from rubycritic and simplecov.
</objective>

<quick_start>
<basic_usage>
1. Ensure you're on a feature branch (not main/master/dev)
2. Run `git fetch` to update remote refs
3. Auto-detect base branch from git configuration
4. Get diff of changed files: `git diff --name-only base-branch...HEAD`
5. Run rubycritic and simplecov on changed files
6. Analyze each changed file for OOP, Rails, security, and test issues
7. Generate REVIEW.md with findings and VSCode links
</basic_usage>

<vscode_link_format>
Every code reference must use this format:
```markdown
[description](file:///absolute/path/to/file.rb#L42)
```

Example:
```markdown
[UserService#create_user violates SRP](file:///Users/dev/app/services/user_service.rb#L15)
```

Clicking opens the file at the specified line in VSCode.
</vscode_link_format>
</quick_start>

<workflow>
<step_1_detect_base_branch>
Auto-detect the base branch using git configuration:

```bash
# Get default branch from remote
git remote show origin | grep 'HEAD branch' | cut -d' ' -f5

# Or detect from common naming
git branch -r | grep -E 'origin/(main|master|develop)' | head -n1
```

If detection fails, default to `main`.
</step_1_detect_base_branch>

<step_2_identify_changes>
Get list of changed Ruby files:

```bash
git diff --name-only --diff-filter=ACMR base-branch...HEAD | grep '\.rb$'
```

Focus only on added, changed, modified, or renamed files (exclude deleted).
</step_2_identify_changes>

<step_3_run_analysis_tools>
Execute rubycritic and simplecov:

```bash
# Run rubycritic on changed files
rubycritic $(git diff --name-only base-branch...HEAD | grep '\.rb$' | tr '\n' ' ')

# Run test suite with simplecov
COVERAGE=true bundle exec rspec
```

Parse output to extract:
- **RubyCritic**: Complexity scores, code smells, churn, duplication
- **SimpleCov**: Coverage percentages, uncovered lines, missing test files
</step_3_run_analysis_tools>

<step_4_analyze_each_file>
For each changed file, review in this order:

**1. OOP Design Review** (see [references/sandi-metz-rules.md](references/sandi-metz-rules.md) and [references/solid-principles.md](references/solid-principles.md))
- Check Sandi Metz rules violations
- Identify SOLID principle violations
- Look for design patterns misuse
- Assess class cohesion and coupling

**2. Rails Patterns Review** (see [references/rails-patterns.md](references/rails-patterns.md))
- Detect N+1 queries
- Review callback usage
- Check scope and query object patterns
- Validate service object implementations
- Review concerns for proper abstraction

**3. Security Review** (see [references/security-checklist.md](references/security-checklist.md))
- SQL injection vulnerabilities
- XSS vulnerabilities
- Mass assignment issues
- Authentication/authorization gaps
- Input validation missing

**4. Test Coverage Review**
- Compare changed files with simplecov output
- Identify untested methods
- Check test quality and patterns
- Recommend missing test scenarios
</step_4_analyze_each_file>

<step_5_analyze_codebase_patterns>
Before making suggestions, understand larger patterns:

```bash
# Find similar patterns in codebase
grep -r "class.*Service" app/services/
grep -r "include Concerns" app/models/

# Check existing architectural patterns
ls app/services/ app/queries/ app/decorators/ app/presenters/
```

**Ensure suggestions align with established patterns:**
- If codebase uses service objects, recommend service objects
- If codebase uses decorators, recommend decorators
- Match naming conventions and file structure
- Respect existing abstraction layers
</step_5_analyze_codebase_patterns>

<step_6_generate_review_md>
Create REVIEW.md with this structure:

```markdown
# Code Review - [Branch Name]

**Base Branch**: [detected-branch]
**Changed Files**: [count]
**Review Date**: [date]

---

## Summary

[High-level overview of changes and main findings]

## Critical Issues

[Issues requiring immediate attention - security, major bugs]

## Design & Architecture

### OOP Violations

[Sandi Metz and SOLID violations with VSCode links]

### Rails Patterns

[N+1 queries, callback issues, anti-patterns with VSCode links]

## Security Concerns

[Security vulnerabilities with VSCode links]

## Test Coverage

[Coverage gaps and missing tests with VSCode links]

## Tool Reports

### RubyCritic Summary
- **Complexity**: [score]
- **Duplication**: [score]
- **Code Smells**: [count]

### SimpleCov Summary
- **Total Coverage**: [percentage]
- **Files with < 90% coverage**: [list]

---

## Recommendations

[Prioritized list of improvements considering codebase patterns]

## Positive Observations

[Well-designed code, good patterns, improvements from previous reviews]
```

Every code reference MUST include VSCode-compatible link.
</step_6_generate_review_md>
</workflow>

<tool_integration>
<rubycritic_integration>
RubyCritic analyzes code quality and complexity.

**Run on changed files only:**
```bash
rubycritic --format json --no-browser $(git diff --name-only base...HEAD | grep '\.rb$')
```

**Extract from JSON output:**
- Complexity score per file
- Code smells (complexity, duplication, method length)
- Churn rate (files changed frequently)

Incorporate findings into "Tool Reports" section of REVIEW.md.
</rubycritic_integration>

<simplecov_integration>
SimpleCov tracks test coverage.

**Trigger coverage run:**
```bash
COVERAGE=true bundle exec rspec
```

**Read from coverage/.resultset.json:**
- Overall coverage percentage
- Per-file coverage
- Uncovered lines

Cross-reference with changed files to identify coverage gaps.

If simplecov not configured, check for existing skill:
```bash
# Check if simplecov skill exists
ls ~/.claude/skills/simplecov/
```

Use Skill tool to invoke simplecov skill for setup guidance if needed.
</simplecov_integration>

<skill_invocation>
If rubycritic or simplecov skills exist, invoke them:

```
Skill(rubycritic)  # For RubyCritic setup and advanced usage
Skill(simplecov)   # For SimpleCov setup and configuration
```

These skills provide deeper integration patterns and troubleshooting.
</skill_invocation>
</tool_integration>

<review_areas>
<oop_design_review>
Apply both Sandi Metz rules and SOLID principles:

**Sandi Metz Rules:**
1. Classes ≤ 100 lines
2. Methods ≤ 5 lines
3. Methods ≤ 4 parameters
4. Controllers instantiate ≤ 1 object
5. Views reference ≤ 1 instance variable

**SOLID Principles:**
- **S**ingle Responsibility: One reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes must be substitutable
- **I**nterface Segregation: Many specific interfaces > one general
- **D**ependency Inversion: Depend on abstractions, not concretions

See detailed guides:
- [references/sandi-metz-rules.md](references/sandi-metz-rules.md)
- [references/solid-principles.md](references/solid-principles.md)
</oop_design_review>

<rails_patterns_review>
Check for Rails-specific issues:

**Performance:**
- N+1 queries (missing `includes`, `preload`, `eager_load`)
- Inefficient database queries
- Missing database indexes
- Memory-intensive operations

**Patterns:**
- Callback overuse (prefer service objects)
- Fat models (extract to concerns, services, or queries)
- Business logic in controllers
- Missing query objects for complex queries

**Best Practices:**
- Strong parameters properly configured
- Scopes returning ActiveRecord::Relation
- Proper use of concerns vs. mixins
- Background job usage for slow operations

See: [references/rails-patterns.md](references/rails-patterns.md)
</rails_patterns_review>

<security_review>
Check for common vulnerabilities:

**SQL Injection:**
- Raw SQL without parameterization
- String interpolation in `where` clauses
- Unsafe use of `sanitize_sql_array`

**XSS:**
- `html_safe` or `raw` on user input
- Missing escaping in views
- Unsafe rendering of user content

**Mass Assignment:**
- Missing strong parameters
- `permit!` usage
- Unprotected attributes

**Authorization:**
- Missing authorization checks
- Inconsistent permission patterns
- Direct object references without verification

See: [references/security-checklist.md](references/security-checklist.md)
</security_review>

<test_coverage_review>
Assess test quality and completeness:

**Coverage Analysis:**
- Methods without any tests
- Edge cases not covered
- Error handling paths untested
- Integration points missing tests

**Test Quality:**
- Tests testing implementation vs. behavior
- Brittle tests with excessive mocking
- Missing integration/system tests
- Slow tests that could be unit tests

**Recommendations:**
- Specific test scenarios to add
- Refactoring to improve testability
- Mock/stub suggestions
- Coverage improvement strategy
</test_coverage_review>
</review_areas>

<codebase_pattern_recognition>
<understanding_context>
Before making recommendations, understand existing patterns:

**Architectural Layers:**
```bash
# Discover what layers exist
find app -type d -maxdepth 1 | sort
```

Common patterns:
- `/services` - Business logic extraction
- `/queries` - Complex database queries
- `/decorators` or `/presenters` - View logic
- `/policies` - Authorization logic
- `/forms` - Form objects for complex validations
- `/serializers` - API response formatting

**Naming Conventions:**
```bash
# Understand naming patterns
ls app/services/ | head -10
ls app/models/concerns/ | head -10
```

Check for patterns like:
- `UserCreationService` vs. `Users::Creator`
- `Authenticatable` vs. `Authentication`
- File organization (flat vs. namespaced)
</understanding_context>

<matching_suggestions_to_patterns>
**Rule**: Recommendations must match existing codebase patterns.

Examples:
- If codebase has `/services` with `VerbNounService` naming → recommend similar
- If codebase uses concerns heavily → suggest concern extraction
- If codebase uses namespaced modules → follow namespace structure
- If tests use FactoryBot → recommend FactoryBot in test suggestions

**Anti-pattern**: Suggesting decorator pattern when codebase has no decorators.
**Better**: Suggest service object if that's the established pattern.
</matching_suggestions_to_patterns>
</codebase_pattern_recognition>

<validation>
Before finalizing REVIEW.md, validate:

**Link Format:**
- [ ] Every code reference has VSCode link
- [ ] Links use absolute paths
- [ ] Line numbers are accurate
- [ ] Links follow format: `file:///absolute/path#L42`

**Content Completeness:**
- [ ] All changed files reviewed
- [ ] RubyCritic findings incorporated
- [ ] SimpleCov findings incorporated
- [ ] Each section has specific examples with links

**Quality:**
- [ ] Suggestions match codebase patterns
- [ ] Critical issues clearly marked
- [ ] Positive observations included
- [ ] Recommendations are actionable and prioritized
</validation>

<success_criteria>
A successful review has:

1. **Accurate scope**: Only reviews changed files in branch vs. base
2. **Comprehensive coverage**: Addresses OOP, Rails, security, and tests
3. **Tool integration**: Includes rubycritic and simplecov findings
4. **Clickable links**: Every code reference has working VSCode link
5. **Contextual suggestions**: Recommendations align with codebase patterns
6. **Actionable findings**: Clear, specific, prioritized improvements
7. **Balanced perspective**: Includes positive observations alongside issues
8. **Structured output**: REVIEW.md follows consistent format
</success_criteria>

<reference_guides>
**Core Principles:**
- [references/sandi-metz-rules.md](references/sandi-metz-rules.md) - POODR rules and Law of Demeter
- [references/solid-principles.md](references/solid-principles.md) - Detailed SOLID principle explanations with Ruby examples

**Domain-Specific:**
- [references/rails-patterns.md](references/rails-patterns.md) - Rails anti-patterns, N+1 queries, callback issues, best practices
- [references/security-checklist.md](references/security-checklist.md) - Security vulnerability patterns and detection strategies

**Technical Reference:**
- [references/vscode-links.md](references/vscode-links.md) - VSCode link format specifications and examples
</reference_guides>
