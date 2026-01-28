---
name: rubycritic
description: Integrate RubyCritic to analyze Ruby code quality and maintain high standards throughout development. Use when working on Ruby projects to check code smells, complexity, and duplication. Triggers include creating/editing Ruby files, refactoring code, reviewing code quality, or when user requests code analysis or quality checks.
---

<objective>
Maintain high code quality standards in Ruby projects by integrating RubyCritic analysis into the development workflow. Automatically detect code smells, complexity issues, and duplication, providing actionable guidance for improvements.
</objective>

<quick_start>
Run quality check on Ruby files:

```bash
scripts/check_quality.sh [path/to/ruby/files]
```

If no path is provided, analyzes the current directory. The script automatically installs RubyCritic if missing.

**Immediate feedback**:
- Overall score (0-100)
- File ratings (A-F)
- Specific code smells detected
</quick_start>

<workflow>
<automated_quality_checks>
**Proactive analysis**: Run RubyCritic automatically after significant code changes:

- After creating new Ruby files or classes
- After implementing complex methods (>10 lines)
- After refactoring existing code
- Before marking tasks as complete
- Before committing code

**Integration pattern**:
1. Make code changes
2. Run `scripts/check_quality.sh [changed_files]`
3. Review output for issues
4. Address critical smells (if any)
5. Re-run to verify improvements
6. Proceed with next task

**When to skip**: Simple variable renames, comment changes, or minor formatting adjustments don't require quality checks.
</automated_quality_checks>

<interpreting_results>
**Overall Score**:
- 95+ (excellent) - Maintain this standard
- 90-94 (good) - Minor improvements possible
- 80-89 (acceptable) - Consider refactoring
- Below 80 - Prioritize improvements

**File Ratings**:
- A/B - Acceptable quality
- C - Needs attention
- D/F - Requires refactoring

**Issue Types**:
- **Code Smells** (Reek) - Design and readability issues
- **Complexity** (Flog) - Overly complex methods
- **Duplication** (Flay) - Repeated code patterns
</interpreting_results>

<responding_to_issues>
**Priority order**:
1. **Critical smells** - Long parameter lists, high complexity, feature envy
2. **Duplication** - Extract shared methods or modules
3. **Minor smells** - Unused parameters, duplicate method calls
4. **Style issues** - Naming, organization

**Incremental fixing**:
- Fix one issue at a time
- Run analysis after each fix
- Verify score improves
- Explain significant improvements to user

**When scores drop**:
- Identify which file/method caused the drop
- Review recent changes in that area
- Fix immediately before continuing
- Don't accumulate technical debt
</responding_to_issues>

<error_handling>
**Common errors and solutions**:

**"RubyCritic not found"**: Script auto-installs, but if it fails:
- Check Ruby is installed: `ruby --version`
- Manually install: `gem install rubycritic`
- Or add to Gemfile: `gem 'rubycritic', require: false`

**"No files to analyze"**: Verify path contains `.rb` files
- Check path is correct
- Use explicit path: `scripts/check_quality.sh app/models`

**"Bundler error"**: Gemfile.lock conflict
- Run `bundle install` first
- Or use system gem: `gem install rubycritic && rubycritic [path]`

**Analysis hangs**: Large codebase
- Analyze specific directories instead of entire project
- Use `--no-browser` flag to skip HTML generation
- Consider `.rubycritic.yml` to exclude paths

For additional error scenarios, see [references/error-handling.md](references/error-handling.md)
</error_handling>
</workflow>

<git_hooks_integration>
**Pre-commit quality checks**: Automatically run RubyCritic before commits:

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Get staged Ruby files
RUBY_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.rb$')

if [ -n "$RUBY_FILES" ]; then
  echo "Running RubyCritic on staged files..."
  scripts/check_quality.sh $RUBY_FILES

  if [ $? -ne 0 ]; then
    echo "Quality check failed. Fix issues or use --no-verify to skip."
    exit 1
  fi
fi
```

**CI integration**: Add to GitHub Actions, GitLab CI, or other CI systems:

```yaml
# .github/workflows/quality.yml
- name: Run RubyCritic
  run: |
    gem install rubycritic
    rubycritic --format json --minimum-score 90
```

For complete git hooks setup and CI examples, see [references/git-hooks.md](references/git-hooks.md)
</git_hooks_integration>

<configuration>
**Basic configuration** (`.rubycritic.yml`):

```yaml
minimum_score: 95
formats:
  - console
paths:
  - 'app/'
  - 'lib/'
no_browser: true
```

**Common options**:
- `minimum_score`: Fail if score below this threshold
- `formats`: Output formats (console, html, json)
- `paths`: Directories to analyze
- `no_browser`: Don't auto-open HTML report

For advanced configuration and custom thresholds, see [references/configuration.md](references/configuration.md)
</configuration>

<common_patterns>
**Quick quality check during development**:
```bash
# Check recently modified files
scripts/check_quality.sh $(git diff --name-only | grep '\.rb$')
```

**Generate detailed HTML report**:
```bash
bundle exec rubycritic --format html app/
# Opens browser with detailed analysis
```

**Compare with main branch** (CI mode):
```bash
rubycritic --mode-ci --branch main app/
# Shows only changes from main branch
```

**Check specific file types**:
```bash
scripts/check_quality.sh app/models/*.rb
scripts/check_quality.sh app/services/**/*.rb
```
</common_patterns>

<code_smell_reference>
For detailed examples of common code smells and how to fix them, see [references/code_smells.md](references/code_smells.md)

**Quick reference**:
- **Control Parameter** - Replace boolean params with separate methods
- **Feature Envy** - Move method to the class it uses most
- **Long Parameter List** - Use parameter objects or hashes
- **High Complexity** - Extract methods, use early returns
- **Duplication** - Extract to shared methods or modules
</code_smell_reference>

<installation>
**Automatic installation**: The `check_quality.sh` script handles installation automatically:

- Detects if RubyCritic is installed
- Uses bundler if Gemfile present
- Falls back to system gem installation
- Adds to Gemfile development group if needed

**Manual installation**:

With Bundler:
```ruby
# Gemfile
group :development do
  gem 'rubycritic', require: false
end
```

System-wide:
```bash
gem install rubycritic
```
</installation>

<success_criteria>
RubyCritic is successfully integrated when:

- Quality checks run automatically after significant code changes
- Overall score maintained at 90+ (or project-defined threshold)
- Critical code smells addressed immediately
- Quality improvements explained to user when significant
- No quality regressions introduced by changes
- Files maintain A or B ratings
</success_criteria>

<reference_guides>
**Detailed references**:
- [references/code_smells.md](references/code_smells.md) - Common smells and fixes with examples
- [references/configuration.md](references/configuration.md) - Advanced RubyCritic configuration
- [references/git-hooks.md](references/git-hooks.md) - Pre-commit hooks and CI integration
- [references/error-handling.md](references/error-handling.md) - Troubleshooting common errors
</reference_guides>
