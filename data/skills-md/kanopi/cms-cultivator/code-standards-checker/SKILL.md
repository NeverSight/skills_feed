---
name: code-standards-checker
description: Automatically check code against PHPCS, ESLint, WordPress Coding Standards, or Drupal Coding Standards when user asks about code style, standards compliance, or best practices. Invoke when user mentions "coding standards", "code style", "linting", "PHPCS", "ESLint", or asks if code follows conventions.
---

# Code Standards Checker

Automatically check code against coding standards and style guides.

## Philosophy

Consistent code style makes collaboration seamless and reduces cognitive load.

### Core Beliefs

1. **Standards Reduce Friction**: Consistent style means less time debating formatting
2. **Automated Enforcement Saves Time**: Tools catch style issues faster than humans
3. **Community Standards Build Better Software**: Following established patterns improves code quality
4. **Readability is Paramount**: Code is read far more often than it's written

### Why Coding Standards Matter

- **Team Collaboration**: Everyone writes code the same way
- **Easier Maintenance**: Consistent patterns are easier to understand and modify
- **Fewer Bugs**: Many standards prevent common mistakes
- **Professional Quality**: Shows attention to detail and best practices

## When to Use This Skill

Activate this skill when the user:
- Asks "does my code follow standards?"
- Mentions "coding standards", "code style", or "best practices"
- Asks "is this code compliant?"
- References "PHPCS", "ESLint", "WordPress Coding Standards", or "Drupal Coding Standards"
- Shows code and asks if it's properly formatted
- Asks "should I lint this?"

## Decision Framework

Before running standards checks, consider:

### What Platform Is This?

1. **Drupal** → Use Drupal Coding Standards (via PHPCS)
2. **WordPress** → Use WordPress Coding Standards (via PHPCS)
3. **Generic PHP** → Use PSR-12 (via PHPCS)
4. **JavaScript** → Use ESLint with project config
5. **Mixed** → Run both PHP and JavaScript checks

### What's the Scope?

- **Specific file(s)** - User shows code or mentions file → Check that file
- **Recent changes** - User mentions "my changes" → Check git diff
- **Entire project** - User says "whole project" → Run project-wide check
- **Directory** - User mentions component/module → Check that directory

### What Standard Should Apply?

**Automatic detection**:
- Drupal project → Drupal Coding Standards
- WordPress project → WordPress Coding Standards
- .eslintrc present → Use project's ESLint config
- composer.json with PHPCS → Use configured standard

**User-specified**:
- User mentions specific standard → Use that standard
- No config found → Suggest installing standards tools

### Should This Auto-Fix?

- ✅ **Yes** - User asks "can you fix these?" → Provide `--fix` commands
- ❌ **No** - Just checking compliance → Report violations only
- ⚠️ **Ask** - Many violations found → Suggest auto-fix option

### Decision Tree

```
User asks about standards
    ↓
Detect platform (Drupal/WordPress/Generic)
    ↓
Determine scope (file/changes/project)
    ↓
Check for existing config (.phpcs.xml, .eslintrc)
    ↓
Run appropriate tool
    ↓
Report violations
    ↓
Auto-fix? → Provide --fix commands if requested
```

## Workflow

### 1. Detect Project Type

Check for indicators:

**Drupal**:
```bash
# Check for Drupal
test -f web/core/lib/Drupal.php && echo "Drupal project"
test -f docroot/core/lib/Drupal.php && echo "Drupal project"
```

**WordPress**:
```bash
# Check for WordPress
test -f wp-config.php && echo "WordPress project"
test -f web/wp-config.php && echo "WordPress project"
```

**JavaScript/Frontend**:
```bash
# Check for Node project
test -f package.json && echo "Node project"
```

### 2. Quick Start for Kanopi Projects

For projects with Kanopi DDEV add-ons:

**Drupal/WordPress**:
```bash
# Run all code quality checks
ddev composer code-check

# Individual checks
ddev composer phpstan      # Static analysis
ddev composer phpcs        # Coding standards
ddev composer rector-check # Modernization check
```

**Themes with Node**:
```bash
# ESLint for JavaScript
ddev theme-npm run lint
# or
ddev exec npm run lint
```

### 3. Manual Analysis (Non-Kanopi Projects)

#### PHP Standards (Drupal/WordPress)

**Check if PHPCS is available**:
```bash
test -f vendor/bin/phpcs && echo "PHPCS found"
```

**Run PHPCS**:
```bash
# Drupal
vendor/bin/phpcs --standard=Drupal,DrupalPractice web/modules/custom

# WordPress
vendor/bin/phpcs --standard=WordPress wp-content/themes/custom-theme
vendor/bin/phpcs --standard=WordPress wp-content/plugins/custom-plugin
```

**Common Issues to Report**:
- Missing docblocks
- Incorrect indentation (2 spaces for Drupal, tabs for WordPress)
- Line length violations
- Naming conventions (camelCase vs snake_case)
- Missing/incorrect type hints

#### JavaScript Standards

**Check if ESLint is available**:
```bash
test -f node_modules/.bin/eslint && echo "ESLint found"
```

**Run ESLint**:
```bash
npx eslint src/**/*.js
npx eslint themes/custom/js/**/*.js
```

**Common Issues to Report**:
- Missing semicolons (or extra semicolons)
- Incorrect quotes (single vs double)
- Unused variables
- Console.log statements
- Missing JSDoc comments

### 4. Analyze Specific Code Snippet

If user shows code without running tools:

**PHP Analysis Checklist**:
- ✅ Proper indentation (2 spaces Drupal, 4 spaces or tabs WordPress)
- ✅ Opening braces on same line (PHP) or next line (JS)
- ✅ Docblocks present for functions/classes
- ✅ Type hints for parameters and return types
- ✅ No deprecated functions
- ✅ SQL queries use placeholders (no concatenation)
- ✅ Strings use proper quotes (single for non-interpolated)

**JavaScript Analysis Checklist**:
- ✅ Consistent semicolon usage
- ✅ Proper quote style (single or double, consistent)
- ✅ No `var` (use `const` or `let`)
- ✅ Arrow functions where appropriate
- ✅ Proper JSDoc comments
- ✅ No console.log in production code

### 5. Report Results

**Format**:
```markdown
## Code Standards Check Results

**Project Type**: Drupal 10
**Standard**: Drupal Coding Standards + DrupalPractice

### Summary
- ✅ 45 files checked
- ⚠️ 12 warnings
- ❌ 3 errors

### Errors (Must Fix)

1. **Missing type hint** - `src/Controller/MyController.php:23`
   ```php
   public function process($data) {  // Missing type hint
   ```
   **Fix**: Add type hint `public function process(array $data): void {`

2. **SQL Injection Risk** - `src/Service/UserService.php:45`
   ```php
   db_query("SELECT * FROM users WHERE id = " . $id);
   ```
   **Fix**: Use placeholders `db_query("SELECT * FROM users WHERE id = :id", [':id' => $id]);`

### Warnings (Should Fix)

1. **Line too long** - `src/Form/MyForm.php:67`
   - Line length: 95 characters (exceeds 80)
   - Consider breaking into multiple lines

### Quick Fixes Available

Run this to auto-fix formatting issues:
```bash
ddev composer code-fix
# or manually
vendor/bin/phpcbf --standard=Drupal web/modules/custom
```
```

## Integration with CMS Cultivator

This skill complements the `/quality-standards` slash command:

- **This Skill**: Automatically triggered during conversation
  - "Is this code up to standards?"
  - "Does this follow Drupal conventions?"
  - Quick checks on code snippets

- **`/quality-standards` Command**: Explicit full project scan
  - Comprehensive standards check
  - CI/CD integration
  - Full project analysis

## Platform-Specific Standards

### Drupal Coding Standards

**Key Conventions**:
- 2-space indentation
- Opening brace on same line
- Type hints required (PHP 7.4+)
- Drupal-specific naming (snake_case for functions, PascalCase for classes)
- Services over procedural code
- Dependency injection preferred

**Example Good Code**:
```php
<?php

namespace Drupal\mymodule\Controller;

use Drupal\Core\Controller\ControllerBase;

/**
 * Provides route responses for the My Module module.
 */
class MyModuleController extends ControllerBase {

  /**
   * Returns a render array for the page.
   *
   * @return array
   *   A render array.
   */
  public function content(): array {
    return [
      '#markup' => $this->t('Hello World'),
    ];
  }

}
```

### WordPress Coding Standards

**Key Conventions**:
- Tab indentation (not spaces)
- Yoda conditions (`if ( true === $condition )`)
- Braces on next line for control structures
- WordPress naming (underscores, not camelCase)
- Escaping and sanitization required
- Nonces for forms

**Example Good Code**:
```php
<?php
/**
 * Display user dashboard widget.
 *
 * @param int $user_id User ID.
 * @return void
 */
function my_theme_display_dashboard( $user_id ) {
	if ( ! is_user_logged_in() ) {
		return;
	}

	$user_data = get_userdata( $user_id );

	if ( ! $user_data ) {
		return;
	}

	echo '<div class="dashboard">';
	echo '<h2>' . esc_html( $user_data->display_name ) . '</h2>';
	echo '</div>';
}
```

### JavaScript Standards

**Modern JavaScript Best Practices**:
```javascript
// Good: const/let, arrow functions, template literals
const getUserName = (user) => {
  return `${user.firstName} ${user.lastName}`;
};

// Bad: var, function keyword, concatenation
var getUserName = function(user) {
  return user.firstName + ' ' + user.lastName;
};
```

## Common Standards Violations

### High Priority (Security/Functionality)

1. **SQL Injection**
   - Direct query string concatenation
   - Missing prepared statements

2. **XSS Vulnerabilities**
   - Unescaped output
   - Missing sanitization

3. **Missing Access Checks**
   - No permission verification
   - Unauthenticated endpoints

### Medium Priority (Maintainability)

1. **Missing Type Hints**
2. **Poor Function/Variable Names**
3. **Missing Documentation**
4. **Overly Long Functions**
5. **Deep Nesting**

### Low Priority (Style)

1. **Whitespace Issues**
2. **Line Length**
3. **Brace Placement**
4. **Comment Formatting**

## Example Interactions

**Example 1: Quick snippet check**
```
User: "Is this WordPress code following standards?"
[Shows code with tabs and proper escaping]

Skill: "Let me check that against WordPress Coding Standards...
✅ Proper tab indentation
✅ Output properly escaped with esc_html()
✅ Correct brace placement
⚠️ Missing docblock - should document the function

Overall: Good! Just add a docblock."
```

**Example 2: Project-wide check**
```
User: "Does my custom module follow Drupal standards?"

Skill: "I'll run PHPCS on your custom module...
[Runs ddev composer phpcs or vendor/bin/phpcs]

Found 3 errors and 12 warnings across 8 files.
Most common issues:
- Missing type hints (5 occurrences)
- Lines too long (7 occurrences)

Would you like me to show the specific issues or run the auto-fixer?"
```

## Resources

- [Drupal Coding Standards](https://www.drupal.org/docs/develop/standards)
- [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/)
- [PHP_CodeSniffer](https://github.com/squizlabs/PHP_CodeSniffer)
- [ESLint](https://eslint.org/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
