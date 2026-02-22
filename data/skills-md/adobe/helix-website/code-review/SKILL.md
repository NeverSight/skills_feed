---
name: Code Review
description: Review code for AEM Edge Delivery Services projects. Use at the end of development (before PR) for self-review, or to review pull requests. Validates code quality, performance, accessibility, and adherence to EDS best practices.
---

# Code Review

Review code for AEM Edge Delivery Services (EDS) projects following established coding standards, performance requirements, and best practices.

## When to Use This Skill

This skill supports **two modes** of operation:

### Mode 1: Self-Review (End of Development)

Use this mode when you've finished writing code and want to review it before committing or opening a PR. This is the recommended workflow integration point.

**When to invoke:**
- After completing implementation in the **content-driven-development** workflow (between Step 5 and Step 6)
- Before running `git add` and `git commit`
- When you want to catch issues early, before they reach PR review

**How to invoke:**
- Automatically: CDD workflow invokes this skill after implementation
- Manually: `/code-review` (reviews uncommitted changes in working directory)

**What it does:**
- Reviews all modified/new files in working directory
- Checks code quality, patterns, and best practices
- Validates against EDS standards
- Identifies issues to fix before committing
- Captures visual screenshots for validation

### Mode 2: PR Review

Use this mode to review an existing pull request (your own or someone else's).

**When to invoke:**
- Reviewing a PR before merge
- Automated review via GitHub Actions workflow
- Manual review of a specific PR

**How to invoke:**
- Manually: `/code-review <PR-number>` or `/code-review <PR-URL>`
- Automated: Via GitHub workflow on `pull_request` event

**What it does:**
- Fetches PR diff and changed files
- Validates PR structure (preview URLs, description)
- Reviews code quality
- Posts review comment with findings and screenshots
- Provides actionable fixes via GitHub suggestions or commits
- Explains reasoning for each fix with references to review feedback

---

## Review Workflow

### Step 1: Identify Review Mode and Gather Context

**For Self-Review (no PR number provided):**

```bash
# See what files have been modified
git status

# See the actual changes
git diff

# For staged changes
git diff --staged
```

**Understand the scope:**
- What files were modified?
- What type of change is this? (new block, bug fix, feature, styling, refactor)
- What is the test content URL? (from CDD workflow)

**For PR Review (PR number provided):**

```bash
# Get PR details
gh pr view <PR-number> --json title,body,author,baseRefName,headRefName,files,additions,deletions

# Get changed files
gh pr diff <PR-number>

# Get PR comments and reviews
gh api repos/{owner}/{repo}/pulls/<PR-number>/comments
gh api repos/{owner}/{repo}/pulls/<PR-number>/reviews
```

**Understand the scope:**
- What type of change is this? (new block, bug fix, feature, styling, refactor)
- What files are modified?
- Is there a related GitHub issue?
- Are there test/preview URLs provided?

---

### Step 2: Validate Structure (PR Review Mode Only)

**Skip this step for Self-Review mode.**

**Required elements for PRs (MUST HAVE):**

| Element | Requirement | Check |
|---------|-------------|-------|
| Preview URLs | Before/After URLs showing the change | Required |
| Description | Clear explanation of what changed and why | Required |
| Scope alignment | Changes match PR title and description | Required |
| Issue reference | Link to GitHub issue (if applicable) | Recommended |

**Preview URL format:**
- Before: `https://main--{repo}--{owner}.aem.page/{path}`
- After: `https://{branch}--{repo}--{owner}.aem.page/{path}`

**Flag if missing:**
- Missing preview URLs (blocks automated PSI checks)
- Vague or missing description
- Scope creep (changes unrelated to stated purpose)
- Missing issue reference for bug fixes

---

### Step 3: Code Quality Review

#### 3.1 JavaScript Review

**Linting & Style:**
- [ ] Code passes ESLint (airbnb-base configuration)
- [ ] No `eslint-disable` comments without justification
- [ ] No global `eslint-disable` directives
- [ ] ES6+ features used appropriately
- [ ] `.js` extensions included in imports

**Architecture:**
- [ ] No frameworks in critical rendering path (LCP/TBT impact)
- [ ] Third-party libraries loaded via `loadScript()` in blocks, not `head.html`
- [ ] Consider `IntersectionObserver` for heavy libraries
- [ ] `aem.js` is NOT modified (submit upstream PRs for improvements)
- [ ] No build steps introduced without team consensus

**Code Patterns:**
- [ ] Existing DOM elements re-used, not recreated
- [ ] Block selectors scoped appropriately
- [ ] No hardcoded values that should be configurable
- [ ] Console statements cleaned up (no debug logs)
- [ ] Proper error handling where needed

**Common Issues to Flag:**
```javascript
// BAD: CSS in JavaScript
element.style.backgroundColor = 'blue';

// GOOD: Use CSS classes
element.classList.add('highlighted');

// BAD: Hardcoded configuration
const temperature = 0.7;

// GOOD: Use config or constants
const { temperature } = CONFIG;

// BAD: Global eslint-disable
/* eslint-disable */

// GOOD: Specific, justified disables
/* eslint-disable-next-line no-console -- intentional debug output */
```

#### 3.2 CSS Review

**Linting & Style:**
- [ ] Code passes Stylelint (standard configuration)
- [ ] No `!important` unless absolutely necessary (with justification)
- [ ] Property order maintained (don't reorder in functional PRs)

**Scoping & Selectors:**
- [ ] All selectors scoped to block: `.{block-name} .selector` or `main .{block-name}`
- [ ] Private classes/variables prefixed with block name
- [ ] Simple, readable selectors (add classes rather than complex selectors)
- [ ] ARIA attributes used for styling when appropriate (`[aria-expanded="true"]`)

**Responsive Design:**
- [ ] Mobile-first approach (base styles for mobile, media queries for larger)
- [ ] Standard breakpoints used: `600px`, `900px`, `1200px` (all `min-width`)
- [ ] No mixing of `min-width` and `max-width` queries
- [ ] Layout works across all viewports

**Frameworks & Preprocessors:**
- [ ] No CSS preprocessors (Sass, Less, PostCSS) without team consensus
- [ ] No CSS frameworks (Tailwind, etc.) without team consensus
- [ ] Native CSS features used (supported by evergreen browsers)

**Common Issues to Flag:**
```css
/* BAD: Unscoped selector */
.title { color: red; }

/* GOOD: Scoped to block */
main .my-block .title { color: red; }

/* BAD: !important abuse */
.button { color: white !important; }

/* GOOD: Increase specificity instead */
main .my-block .button { color: white; }

/* BAD: Mixed breakpoint directions */
@media (max-width: 600px) { }
@media (min-width: 900px) { }

/* GOOD: Consistent mobile-first */
@media (min-width: 600px) { }
@media (min-width: 900px) { }

/* BAD: CSS in JS patterns */
element.innerHTML = '<style>.foo { color: red; }</style>';

/* GOOD: Use external CSS files */
```

#### 3.3 HTML Review

- [ ] Semantic HTML5 elements used appropriately
- [ ] Proper heading hierarchy maintained
- [ ] Accessibility attributes present (ARIA labels, alt text)
- [ ] No inline styles or scripts in `head.html`
- [ ] Marketing tech NOT in `<head>` (performance impact)

---

### Step 4: Performance Review

**Critical Requirements:**
- [ ] Lighthouse scores green (ideally 100) for mobile AND desktop
- [ ] No third-party libraries in critical path (`head.html`)
- [ ] No layout shifts introduced (CLS impact)
- [ ] Images optimized and lazy-loaded appropriately

**Performance Checklist:**
- [ ] Heavy operations use `IntersectionObserver` or delayed loading
- [ ] No synchronous operations blocking render
- [ ] Bundle size reasonable (no minification unless measurable Lighthouse gain)
- [ ] Fonts loaded efficiently

**Preview URL Verification:**
If preview URLs provided, check:
- PageSpeed Insights scores
- Core Web Vitals (LCP, CLS, INP)
- Mobile and desktop performance

---

### Step 5: Visual Validation with Screenshots

**Purpose:** Capture screenshots of the preview URL to validate visual appearance. For self-review, this confirms your changes look correct before committing. For PR review, this provides visual evidence in the review comment.

**When to capture screenshots:**
- Always capture at least one screenshot of the primary changed page/component
- For responsive changes, capture mobile (375px), tablet (768px), and desktop (1200px)
- For visual changes (styling, layout), capture before AND after for comparison
- For block changes, capture the specific block area

**How to capture screenshots:**

**Option 1: Playwright (Recommended for automation)**

```javascript
// capture-screenshots.js
import { chromium } from 'playwright';

async function captureScreenshots(afterUrl, outputDir = './screenshots') {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Desktop screenshot
  await page.setViewportSize({ width: 1200, height: 800 });
  await page.goto(afterUrl, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000); // Wait for animations
  await page.screenshot({
    path: `${outputDir}/desktop.png`,
    fullPage: true
  });

  // Tablet screenshot
  await page.setViewportSize({ width: 768, height: 1024 });
  await page.screenshot({
    path: `${outputDir}/tablet.png`,
    fullPage: true
  });

  // Mobile screenshot
  await page.setViewportSize({ width: 375, height: 667 });
  await page.screenshot({
    path: `${outputDir}/mobile.png`,
    fullPage: true
  });

  // Optional: Capture specific block/element
  const block = page.locator('.my-block');
  if (await block.count() > 0) {
    await block.screenshot({ path: `${outputDir}/block.png` });
  }

  await browser.close();

  return {
    desktop: `${outputDir}/desktop.png`,
    tablet: `${outputDir}/tablet.png`,
    mobile: `${outputDir}/mobile.png`
  };
}

// Usage
captureScreenshots('https://branch--repo--owner.aem.page/path');
```

**Option 2: Using MCP Browser Tools**

If you have MCP browser or Playwright tools available:
1. Navigate to the After preview URL
2. Take screenshots at different viewport sizes
3. Optionally take element-specific screenshots of changed blocks

**Option 3: Manual capture with guidance**

Instruct the reviewer or PR author to:
1. Open the After preview URL
2. Use browser DevTools to set viewport sizes
3. Take screenshots and attach to PR

**Uploading screenshots to GitHub:**

```bash
# Upload screenshot as PR comment with image
# First, upload to a hosting service or use GitHub's image upload

# Option A: Embed in PR comment (drag & drop in GitHub UI)
gh pr comment <PR-number> --body "## Visual Preview

### Desktop (1200px)
![Desktop Screenshot](screenshot-url-or-drag-drop)

### Mobile (375px)
![Mobile Screenshot](screenshot-url-or-drag-drop)
"

# Option B: Use GitHub's attachment API (for automation)
# Screenshots can be uploaded as part of the comment body
```

**Screenshot checklist:**
- [ ] Primary page/component captured at desktop width
- [ ] Mobile viewport captured (if responsive changes)
- [ ] Specific block/component captured (if block changes)
- [ ] Before/After comparison (if significant visual changes)
- [ ] No sensitive data visible in screenshots
- [ ] Screenshots uploaded and embedded in PR comment

**Visual issues to look for:**
- Layout breaks or misalignment
- Text overflow or truncation
- Image sizing or aspect ratio issues
- Color/contrast problems (especially in dark mode)
- Missing or broken icons
- Responsive layout issues at breakpoints
- Unexpected visual differences from main branch

---

### Step 6: Content & Authoring Review

**Content Model (if applicable):**
- [ ] Content structure author-friendly
- [ ] Backward compatibility maintained with existing content
- [ ] No breaking changes requiring content migration
- [ ] New content features only available after preview/publish

**Static Resources:**
- [ ] No binaries/static assets committed (unless code-referenced)
- [ ] User-facing strings sourced from content (placeholders, spreadsheets)
- [ ] No hardcoded literals that should be translatable

---

### Step 7: Security Review

- [ ] No sensitive data committed (API keys, passwords, secrets)
- [ ] No XSS vulnerabilities (unsafe innerHTML, unsanitized user input)
- [ ] No SQL injection or command injection vectors
- [ ] CSP headers appropriate for tool pages
- [ ] External links have `rel="noopener noreferrer"`

---

### Step 8: Generate Review Summary

**Output depends on the review mode:**

#### For Self-Review Mode (End of Development)

Report findings directly to continue the development workflow:

```markdown
## Code Review Summary

### Files Reviewed
- `blocks/my-block/my-block.js` (new)
- `blocks/my-block/my-block.css` (new)

### Visual Validation
![Desktop Screenshot](path/to/screenshot.png)

✅ Layout renders correctly across viewports
✅ No console errors
✅ Responsive behavior verified

### Issues Found

#### Must Fix Before Committing
- [ ] `blocks/my-block/my-block.js:45` - Remove console.log debug statement
- [ ] `blocks/my-block/my-block.css:12` - Selector `.title` needs block scoping

#### Recommendations
- [ ] Consider using `loadScript()` for the external library

### Ready to Commit?
- [ ] All "Must Fix" issues resolved
- [ ] Linting passes: `npm run lint`
- [ ] Visual validation complete
```

**After self-review:** Fix any issues found, then proceed with committing and opening a PR.

#### For PR Review Mode

Structure the review comment for GitHub:

```markdown
## PR Review Summary

### Overview
[Brief summary of the PR and its purpose]

### Preview URLs Validated
- [ ] Before: [URL]
- [ ] After: [URL]

### Visual Preview

#### Desktop (1200px)
![Desktop Screenshot](url-or-embedded-image)

#### Mobile (375px)
![Mobile Screenshot](url-or-embedded-image)

<details>
<summary>Additional Screenshots</summary>

#### Tablet (768px)
![Tablet Screenshot](url-or-embedded-image)

#### Block Detail
![Block Screenshot](url-or-embedded-image)

</details>

### Visual Assessment
- [ ] Layout renders correctly across viewports
- [ ] No visual regressions from main branch
- [ ] Colors and typography consistent
- [ ] Images and icons display properly

### Checklist Results

#### Must Fix (Blocking)
- [ ] [Critical issue with file:line reference]

#### Should Fix (High Priority)
- [ ] [Important issue with file:line reference]

#### Consider (Suggestions)
- [ ] [Nice-to-have improvement]

### Detailed Findings

#### [Category: e.g., JavaScript, CSS, Performance]
**File:** `path/to/file.js:123`
**Issue:** [Description of the issue]
**Suggestion:** [How to fix it]
```

---

### Step 9: Provide Actionable Fixes (PR Review Mode Only)

**Skip this step for Self-Review mode** - in self-review, you fix issues directly in your working directory.

After identifying issues in a PR review, provide actionable fixes to make it easier for the PR author to address them. **The goal is to provide one-click fixes whenever possible.**

#### Quick Reference

**PRIMARY METHOD: GitHub Suggestions** (use for ~70-80% of fixable issues)
- One-click acceptance by PR author
- Proper git attribution
- Works for changes < 20 lines
- Native GitHub UI integration

**SECONDARY: Guidance Comments** (~20-30% of issues)
- For subjective or architectural issues
- When multiple approaches exist
- "Consider" level suggestions

**RARE: Fix Commits** (avoid unless necessary)
- Only when suggestions won't work
- Multi-file complex refactors
- Changes requiring extensive testing

---

#### Decision Tree: When to Use Which Approach

| Approach | When to Use | Examples |
|----------|-------------|----------|
| **GitHub Suggestions** (PRIMARY) | Any change that can be expressed as a code replacement | Remove console.log, fix typos, add comments, refactor selectors, update functions, add error handling |
| **Fix Commits** (SECONDARY) | Changes that need testing, span many files, or are too large for suggestions | Complex multi-file refactors, security fixes requiring validation, changes >20 lines |
| **Guidance Only** (FALLBACK) | Architectural changes, subjective improvements, or when multiple approaches exist | "Consider using IntersectionObserver", design pattern suggestions, performance optimizations |

**IMPORTANT:** Always prefer GitHub Suggestions when possible - they provide the best user experience with one-click acceptance and proper git attribution.

#### Approach 1: GitHub Inline Suggestions (PRIMARY APPROACH - Recommended)

Use GitHub's native suggestion feature for most fixes. This provides the best user experience with **one-click acceptance** and proper git attribution.

**When to use:**
- ✅ ANY change that can be expressed as a line replacement
- ✅ Single-line to multi-line changes (up to ~20 lines works well)
- ✅ Clear, actionable fixes with known solutions
- ✅ Independent changes that can be applied separately
- ✅ Changes that don't require extensive testing before commit

**When NOT to use:**
- ❌ Changes requiring testing/validation before commit
- ❌ Very large changes (>20 lines become unwieldy in GitHub UI)
- ❌ Changes spanning many files (better as fix commits)
- ❌ Subjective/architectural suggestions with multiple valid approaches

**Benefits:**
- 🚀 One-click acceptance by PR author
- ✅ Proper co-author attribution in git history
- 🎯 Batch multiple suggestions into single commit
- 📱 Works in GitHub mobile app
- ⚡ Zero copy/paste errors
- 🔍 Clear before/after diff in GitHub UI

**How to create suggestions:**

GitHub suggestions are created using the Pull Request Reviews API with a special markdown syntax in the comment body:

````markdown
```suggestion
// The corrected code here
```
````

**Complete workflow with examples:**

```bash
# Step 1: Get PR information
PR_NUMBER=196
OWNER="adobe"
REPO="helix-tools-website"

# Get the current HEAD commit SHA (required for review API)
COMMIT_SHA=$(gh api repos/$OWNER/$REPO/pulls/$PR_NUMBER --jq '.head.sha')

# Step 2: Analyze the diff to find line positions
# IMPORTANT: Use 'position' in the diff, NOT 'line' in the original file
# Position is the line number in the unified diff output starting from the first diff hunk

# Get the diff to understand positions
gh pr diff $PR_NUMBER --repo $OWNER/$REPO > /tmp/pr-$PR_NUMBER.diff

# Step 3: Create review JSON with suggestions
# Each comment needs:
# - path: file path relative to repo root
# - position: line number IN THE DIFF (not in the file!)
# - body: description + ```suggestion block

cat > /tmp/review-suggestions.json <<JSON
{
  "commit_id": "$COMMIT_SHA",
  "event": "COMMENT",
  "comments": [
    {
      "path": "tools/page-status/diff.js",
      "position": 58,
      "body": "**Fix: Add XSS Safety Documentation** (BLOCKING)\\n\\nAdd a comment to document that this HTML injection is safe:\\n\\n\`\`\`suggestion\\n      const previewBodyHtml = previewDom.querySelector('body').innerHTML;\\n\\n      // XSS Safe: previewBodyHtml is sanitized by mdToDocDom from trusted admin API\\n      const newPageHtml = \\\`\\n\`\`\`\\n\\nThis addresses the security concern by making it clear that XSS has been considered."
    },
    {
      "path": "tools/page-status/diff.js",
      "position": 6,
      "body": "**Fix: Improve Error Handling Pattern**\\n\\nAdd an \\\`ok\\\` flag for more consistent error handling:\\n\\n\`\`\`suggestion\\n  * @returns {Promise<{content: string|null, status: number, ok: boolean}>} Content, status, and success flag\\n\`\`\`"
    },
    {
      "path": "tools/page-status/diff.js",
      "position": 12,
      "body": "**Fix: Return consistent result object**\\n\\n\`\`\`suggestion\\n    return { content: null, status: res.status, ok: false };\\n\`\`\`"
    },
    {
      "path": "tools/page-status/diff.js",
      "position": 16,
      "body": "**Fix: Include ok flag in success case**\\n\\n\`\`\`suggestion\\n  return { content, status: res.status, ok: true };\\n\`\`\`"
    },
    {
      "path": "tools/page-status/diff.css",
      "position": 41,
      "body": "**Fix: Remove stylelint-disable by refactoring selector**\\n\\nUse \\\`.diff-new-page\\\` as intermediate selector to avoid specificity conflict:\\n\\n\`\`\`suggestion\\n.page-diff .diff-new-page .doc-diff-side-header {\\n  padding: var(--spacing-s) var(--spacing-m);\\n\`\`\`"
    }
  ]
}
JSON

# Step 4: Submit the review with all suggestions at once
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  repos/$OWNER/$REPO/pulls/$PR_NUMBER/reviews \
  --input /tmp/review-suggestions.json

# Step 5: Add a friendly summary comment
gh pr comment $PR_NUMBER --repo $OWNER/$REPO --body "$(cat <<'EOF'
## ✨ One-Click Fix Suggestions Added!

I've added **GitHub Suggestions** that you can apply with a single click! 

### How to Apply

1. Go to the **Files changed** tab
2. Find the inline comments with suggestions
3. Click **"Commit suggestion"** to apply individually
4. Or click **"Add suggestion to batch"** on multiple, then **"Commit suggestions"** to batch

### What's Included

- ✅ [BLOCKING] XSS safety documentation
- ✅ Error handling improvements  
- ✅ CSS selector refactoring (removes linter disables)

After applying, run \`npm run lint\` to verify all checks pass!
EOF
)"

echo "✅ Review with suggestions posted successfully!"
echo "View at: https://github.com/$OWNER/$REPO/pull/$PR_NUMBER"
```

**Key points:**
- **Use `position` (diff position) NOT `line` (file line number)** - This is critical!
- The `position` is the line number in the unified diff output, counting from the first `@@` hunk marker
- Multiple suggestions in one review enables batch application
- Each suggestion creates a properly attributed co-authored commit when accepted
- Escape special characters in JSON (quotes, backticks, newlines)
- Always include context in the body before the suggestion block

**How to determine the correct `position` value:**

The `position` is the line number in the unified diff, NOT the line number in the file. Here's how to find it:

1. **Get the diff:**
   ```bash
   gh pr diff <PR-number> > pr.diff
   ```

2. **Open the diff and count lines** from the top, including:
   - File headers (`--- a/file` and `+++ b/file`)
   - Hunk headers (`@@ -old,lines +new,lines @@`)
   - Context lines (no prefix or space prefix)
   - Removed lines (- prefix)
   - Added lines (+ prefix)

3. **The position is the line number of the ADDED line** you want to comment on

**Example from actual diff:**
```diff
--- a/tools/page-status/diff.js
+++ b/tools/page-status/diff.js
  async function fetchContent(url) {
    const res = await fetch(url);
-   if (!res.ok) throw new Error(`Failed to fetch ${url}: ${res.status}`);
-   return res.text();
+   if (!res.ok) {
+     return { content: null, status: res.status };  ← Position 12 (counting from top)
+   }
```

**Best practices for suggestions:**
- Keep suggestions focused and atomic (one fix per suggestion)
- **Always include context** - explain WHY the change is needed before the suggestion block
- Test the suggestion mentally or locally before posting
- Only suggest changes you're confident are correct
- Include surrounding lines for context (GitHub shows ~3 lines of context)
- Use `position` in the diff, not `line` in the file (critical!)
- Batch related suggestions in one review for easier application
- Add a friendly summary comment explaining how to apply
- Format suggestion body with markdown (bold headers, inline code)
- Escape special characters properly in JSON (quotes, backticks, backslashes)

#### Approach 2: Fix Commits (For Complex or Multi-File Fixes)

For more complex fixes, create commits directly on the PR branch. This is especially useful when:
- Fixes span multiple files
- Changes need to be tested together
- Refactoring is required
- You want to demonstrate the fix working

**Prerequisites:**
- Ensure you have write access to the repository or the PR is from a fork you can access
- Verify the PR author has enabled maintainer edits (usually default for same-org PRs)

**Workflow:**

```bash
# 1. Get PR branch information
PR_INFO=$(gh pr view <PR-number> --json headRefName,headRepository,headRepositoryOwner)
BRANCH=$(echo $PR_INFO | jq -r '.headRefName')
REPO_OWNER=$(echo $PR_INFO | jq -r '.headRepositoryOwner.login')

# 2. Fetch the PR branch
git fetch origin pull/<PR-number>/head:pr-<PR-number>

# 3. Check out the PR branch
git checkout pr-<PR-number>

# 4. Make fixes based on review findings
# Example: Fix CSS linter issues by refactoring selectors

# 5. Test your fixes
npm run lint
# Run any relevant tests

# 6. Commit with detailed reasoning
git commit -m "$(cat <<'EOF'
fix: refactor CSS selectors to eliminate linter disables

Refactored CSS selectors in diff.css to resolve specificity conflicts
without using stylelint-disable comments. Changes:

- Increased specificity using .diff-new-page parent selector
- Reordered rules to prevent descending specificity issues
- Maintains same visual appearance and functionality

Addresses code review feedback: https://github.com/{owner}/{repo}/pull/<PR-number>#issuecomment-XXXXX
EOF
)"

# 7. Push to the PR branch
git push origin pr-<PR-number>:$BRANCH

# 8. Add comment to PR explaining what you fixed
gh pr comment <PR-number> --body "$(cat <<'EOF'
## Fixes Applied

I've pushed commits to address some of the review findings:

### Commit 1: Refactor CSS selectors
- ✅ Eliminated all `stylelint-disable` comments
- ✅ Resolved specificity conflicts properly
- ✅ Maintained visual appearance

### Commit 2: Standardize error handling  
- ✅ Updated fetchContent to return consistent result objects
- ✅ Updated all callers to use new pattern
- ✅ Added JSDoc for clarity

### Still Need Action From You:
- [ ] **[BLOCKING]** Add XSS safety comment (see suggestion in review)
- [ ] Consider extracting renderDiffPanel helper (optional)

All linting passes now. Please review the commits and address the remaining item.
EOF
)"
```

**Commit message format for fixes:**

```
fix: <short description>

<Detailed explanation of what was fixed and why>

Changes:
- <specific change 1>
- <specific change 2>

Addresses review feedback: <link to review comment>
```

#### Approach 3: Hybrid Approach (RECOMMENDED FOR MOST PRs)

**For the majority of PRs, use this hybrid strategy:**

1. **GitHub suggestions** for all fixable issues (primary method)
2. **Guidance/comments** for subjective or architectural issues
3. **Fix commits** only for very complex multi-file refactors

**Typical workflow:**

```bash
# 1. Post comprehensive review comment with summary (from Step 8)
gh pr comment <PR-number> --repo {owner}/{repo} --body "<detailed review summary>"

# 2. Submit a review with GitHub suggestions for ALL fixable issues
# (Create JSON as shown in Approach 1 with all suggestions)
gh api POST repos/{owner}/{repo}/pulls/<PR-number>/reviews \
  --input /tmp/review-suggestions.json

# 3. Add a friendly summary about the suggestions
gh pr comment <PR-number> --repo {owner}/{repo} --body "$(cat <<'EOF'
## ✨ One-Click Suggestions Added!

I've added GitHub Suggestions for the fixable issues:
- ✅ [BLOCKING] Security documentation
- ✅ Error handling improvements
- ✅ CSS selector refactoring

Go to **Files changed** tab and click **"Commit suggestion"** to apply!
EOF
)"

# 4. For subjective/architectural issues, add guidance comments separately
# (Only if needed - most issues should have suggestions)
```

**Real-world example distribution:**

For a typical PR with 10 issues:
- **GitHub suggestions**: 7-8 issues (concrete fixes)
- **Guidance comments**: 2-3 issues (architectural, subjective, or "consider" level)
- **Fix commits**: 0-1 (only if critically needed)

**This approach provides:**
- ✅ Maximum ease of use (one-click fixes)
- ✅ Clear distinction between concrete fixes and suggestions
- ✅ Reduced review cycles
- ✅ Better PR author experience

#### Real-World Example

**PR #196: Support unpublished pages in diff tool**

Issues identified in review:
1. XSS safety documentation needed (BLOCKING)
2. Four CSS stylelint-disable comments (should fix)
3. Inconsistent error handling (should fix)
4. CSS variable fallback inconsistency (optional)

**Action taken:**
```bash
# Created two reviews with 9 total GitHub Suggestions
# - 4 suggestions for diff.js (XSS comment, error handling)
# - 5 suggestions for diff.css (selector refactoring)

# Posted friendly summary comment explaining one-click application

# Result: PR author can fix all issues in ~30 seconds vs 5-10 minutes of manual work
```

**View the actual implementation:**
- JavaScript suggestions: https://github.com/adobe/helix-tools-website/pull/196#pullrequestreview-3747855930
- CSS suggestions: https://github.com/adobe/helix-tools-website/pull/196#pullrequestreview-3747857266
- Summary comment: https://github.com/adobe/helix-tools-website/pull/196#issuecomment-3843945119

**Time saved:**
- Traditional review: Author spends 5-10 minutes copying code, editing files, testing
- With suggestions: Author spends 30 seconds clicking "Commit suggestions"
- **Time savings: 90%+ reduction in fix application time**

#### Guidelines for Choosing Approach

**Use GitHub Suggestions when:** (DEFAULT - use this ~70-80% of the time)
- ✅ You know the exact fix needed
- ✅ Change is < 20 lines (works well in GitHub UI)
- ✅ Fix is objective and unambiguous
- ✅ Can be applied without extensive testing
- ✅ Independent of other changes
- ✅ **Examples:** Add comments, remove debug code, fix typos, refactor selectors, update error handling, add JSDoc, fix linting issues

**Use Fix Commits when:** (RARE - use only when suggestions won't work)
- ✅ Changes span many files (>5 files)
- ✅ Complex refactoring requiring testing
- ✅ Changes are interdependent and must be tested together
- ✅ Security fixes that need immediate attention and validation
- ✅ You're already working on the PR branch for other reasons
- ✅ **Examples:** Large refactors, multi-file renames, complex security patches

**Use Guidance Only when:** (~20-30% of issues)
- ✅ Architectural decisions needed
- ✅ Multiple valid approaches exist
- ✅ Requires domain knowledge or context from PR author
- ✅ Subjective improvements ("Consider", "Think about")
- ✅ Performance optimizations with trade-offs
- ✅ **Examples:** "Consider using IntersectionObserver", "You might want to extract this to a util", "Have you thought about caching?"

**Decision flowchart:**
```
Issue identified
    ↓
Do I know the exact fix? ──NO──→ Use Guidance
    ↓ YES
Is it < 20 lines? ──NO──→ Use Fix Commit or Guidance
    ↓ YES
Use GitHub Suggestion ✅ (BEST OPTION)
```

#### Quality Standards for Fixes

**Before posting suggestions or commits:**

1. **Verify correctness:** Test locally or mentally verify the fix is correct
2. **Check scope:** Ensure your fix doesn't introduce new issues
3. **Maintain style:** Match existing code style and patterns
4. **Run linters:** Ensure fixes don't break linting
5. **Be respectful:** Frame fixes as helpful suggestions, not criticism
6. **Link context:** Reference the review comment explaining WHY

**Don't:**
- Don't fix issues outside the PR scope
- Don't change code style unrelated to the issue
- Don't add features or enhancements
- Don't push commits without explaining what you fixed
- Don't fix subjective issues without discussion

#### Troubleshooting GitHub Suggestions

**Common issues and solutions:**

| Problem | Cause | Solution |
|---------|-------|----------|
| "Validation Failed: line could not be resolved" | Used `line` instead of `position` | Use `position` (diff line number) not `line` (file line number) |
| Suggestion doesn't appear inline | Wrong position value | Count lines in the diff carefully, including headers |
| Can't apply suggestion | Merge conflict or branch updated | Author needs to update branch first |
| Suggestion formatting broken | Unescaped JSON characters | Escape quotes, backticks, newlines in JSON |
| "Invalid commit_id" | Used old commit SHA | Get current HEAD SHA before creating review |

**How to verify your review before posting:**

```bash
# 1. Validate JSON syntax
cat /tmp/review-suggestions.json | jq . > /dev/null && echo "✅ Valid JSON"

# 2. Check position values against diff
gh pr diff <PR-number> > pr.diff
# Manually verify each position value in your JSON matches an added line

# 3. Test with one suggestion first
# Before posting 10 suggestions, test with 1 to ensure positions are correct
```

#### Success Criteria

A good fix provision should:
- [ ] **Use GitHub Suggestions as the primary method** (for ~70-80% of fixable issues)
- [ ] Make it easy for the author to address issues (one-click accept)
- [ ] Provide working, tested code (not untested suggestions)
- [ ] Explain the reasoning behind each fix in the comment body
- [ ] Reference the original review feedback from Step 8
- [ ] Be respectful and collaborative in tone
- [ ] Focus only on issues identified in the review
- [ ] Not introduce new issues or regressions
- [ ] Include a friendly summary comment explaining how to apply suggestions
- [ ] Use proper `position` values (diff lines, not file lines)
- [ ] Batch related suggestions in one review for efficient application

---

### Quick Start Template

**Copy this template to quickly create a review with GitHub Suggestions:**

```bash
#!/bin/bash
# Quick script to create GitHub Suggestions for PR review

PR_NUMBER=YOUR_PR_NUMBER
OWNER="adobe"
REPO="helix-tools-website"

# Get commit SHA
COMMIT_SHA=$(gh api repos/$OWNER/$REPO/pulls/$PR_NUMBER --jq '.head.sha')
echo "✅ PR Head SHA: $COMMIT_SHA"

# Create review JSON
cat > /tmp/review-$PR_NUMBER.json <<JSON
{
  "commit_id": "$COMMIT_SHA",
  "event": "COMMENT",
  "comments": [
    {
      "path": "path/to/file.js",
      "position": DIFF_LINE_NUMBER,
      "body": "**Fix: Issue Title**\\n\\nExplanation of the issue.\\n\\n\`\`\`suggestion\\nYour fixed code here\\n\`\`\`\\n\\nReasoning for the fix."
    }
  ]
}
JSON

# Submit review
gh api POST repos/$OWNER/$REPO/pulls/$PR_NUMBER/reviews \
  --input /tmp/review-$PR_NUMBER.json

# Add summary comment
gh pr comment $PR_NUMBER --repo $OWNER/$REPO --body "✨ GitHub Suggestions added! Go to **Files changed** tab and click **Commit suggestion** to apply."

echo "✅ Review posted! View at: https://github.com/$OWNER/$REPO/pull/$PR_NUMBER"
```

**To use:**
1. Set `PR_NUMBER`, `OWNER`, `REPO`
2. Replace the comments array with your actual suggestions
3. Run the script

---

## Review Priority Levels

### Must Fix (Blocking)
Issues that MUST be resolved before merge:
- Missing preview URLs
- Linting failures
- Security vulnerabilities
- Breaking existing functionality
- Performance regressions (Lighthouse score drop)
- Accessibility violations
- Modifications to `aem.js`

### Should Fix (High Priority)
Issues that SHOULD be resolved:
- `!important` usage without justification
- Unscoped CSS selectors
- Hardcoded values that should be configurable
- Missing error handling
- Console statements left in code
- CSS in JavaScript

### Consider (Suggestions)
Improvements to consider:
- Code organization
- Naming conventions
- Documentation
- Additional test coverage
- Modern API usage opportunities

---

## Common Review Patterns

Based on actual PR reviews, watch for these patterns:

### CSS Issues
- **"No CSS in JS, please"** - Inline styles should use CSS classes
- **"Use proper CSS"** - Avoid style manipulation in JavaScript
- **"Do we need the `!important`?"** - Strong preference against `!important`
- **"Solvable with more CSS specificity"** - Increase specificity instead of `!important`

### JavaScript Issues
- **"Why is it hardcoded here?"** - Configuration should be externalized
- **"No global eslint-disable directives"** - Specific, justified disables only
- **"Clean up console messages"** - Remove debug logging
- **"Use proper feature (e.g., decorateIcons, loadScript)"** - Leverage existing utilities

### Architecture Issues
- **"Use existing patterns"** - Check if similar functionality exists
- **"Consider IntersectionObserver"** - For lazy loading
- **"Extract and align design tokens"** - Use CSS custom properties

### Content Issues
- **"Check the type in content config"** - Validate against expected schema
- **"Is this feature needed?"** - Question value vs complexity

---

## Review Response Templates

### Approval
```markdown
## Approved

Preview URLs verified and changes look good.

### Visual Preview
![Desktop Screenshot](url-or-embedded-image)

<details>
<summary>Mobile View</summary>

![Mobile Screenshot](url-or-embedded-image)

</details>

**Verified:**
- [x] Code quality and linting
- [x] Performance (Lighthouse scores)
- [x] Visual appearance (screenshots captured)
- [x] Responsive behavior
- [x] Accessibility basics

[Any additional notes]
```

### Request Changes
```markdown
## Changes Requested

### Blocking Issues
[List with file:line references]

### Suggestions
[List of recommendations]

Please address the blocking issues before merge.
```

### Comment
```markdown
## Review Notes

[Non-blocking observations and questions]
```

---

## Integration with GitHub Workflow

When triggered via GitHub Actions, the skill should:

1. **Receive:** PR number, repository info, event context
2. **Execute:** Full review workflow above
3. **Output:**
   - Review comment on the PR
   - Appropriate review status (approve/request-changes/comment)
   - Summary posted as PR comment

**GitHub Actions integration points:**
- `pull_request` event triggers
- `gh pr review` for posting reviews
- `gh pr comment` for detailed feedback

---

## Resources

### EDS-Specific Resources
- **EDS Development Guidelines:** https://www.aem.live/docs/dev-collab-and-good-practices
- **Performance Best Practices:** https://www.aem.live/developer/keeping-it-100
- **Block Development:** https://www.aem.live/developer/block-collection
- **David's Model:** https://www.aem.live/docs/davidsmodel

### GitHub Code Review Resources
- **GitHub Suggestions Documentation:** https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/incorporating-feedback-in-your-pull-request
- **Pull Request Reviews API:** https://docs.github.com/en/rest/pulls/reviews
- **Review Comments API:** https://docs.github.com/en/rest/pulls/comments
- **Creating Review Comments:** https://docs.github.com/en/rest/pulls/comments#create-a-review-comment-for-a-pull-request

---

## Success Criteria

### For Self-Review Mode

A complete self-review should:
- [ ] Review all modified/new files
- [ ] Check code against all quality criteria
- [ ] Run linting and fix issues
- [ ] Capture visual screenshots of test content
- [ ] Verify responsive behavior across viewports
- [ ] Identify issues to fix before committing
- [ ] Confirm code is ready for commit and PR

### For PR Review Mode

A complete PR review should:
- [ ] Validate all PR structure requirements (preview URLs, description)
- [ ] Check code against all quality criteria
- [ ] Verify performance requirements
- [ ] Capture and include visual screenshots
- [ ] Assess visual appearance for regressions
- [ ] Assess content/authoring impact
- [ ] Identify security concerns
- [ ] Provide actionable feedback with specific references
- [ ] Include screenshots in PR review comment
- [ ] **Provide GitHub Suggestions for all fixable issues (primary method - ~70-80% of issues)**
- [ ] **Submit suggestions as a single review for batch application**
- [ ] **Include a friendly summary comment explaining how to apply suggestions**
- [ ] **Explain reasoning for each fix in the suggestion comment body**
- [ ] Use guidance comments only for subjective/architectural issues
- [ ] Use fix commits only when suggestions won't work (rare)
- [ ] Use appropriate review status (approve/request-changes/comment)

---

## Integration with Content-Driven Development

This skill integrates with the **content-driven-development** workflow:

```
CDD Workflow:
Step 1: Start dev server
Step 2: Analyze & plan
Step 3: Design content model
Step 4: Identify/create test content
Step 5: Implement (building-blocks skill)
    └── testing-blocks skill (browser testing)
        └── **code-review skill (self-review)** ← Invoke here
Step 6: Lint & test
Step 7: Final validation
Step 8: Ship it (commit & PR)
```

**Recommended invocation point:** After implementation and testing-blocks skill complete, before final linting and committing.

**What this catches before PR:**
- Code quality issues
- EDS pattern violations
- Security concerns
- Performance problems
- Visual regressions

**Benefits of self-review:**
- Catch issues early (cheaper to fix)
- Cleaner PRs with fewer review cycles
- Learn from immediate feedback
- Consistent code quality
