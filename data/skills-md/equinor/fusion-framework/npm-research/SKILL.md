---
name: npm-research
description: Research npm packages for changelog, security advisories, and breaking changes. Provides structured analysis for dependency upgrades, vulnerability assessment, and impact evaluation.
---

# NPM Research Skill

Automated skill for researching npm packages to identify changelogs, security advisories, breaking changes, and compatibility impacts.

## Use Cases

- Evaluate a dependency upgrade before applying it
- Find security vulnerabilities affecting a package
- Understand breaking changes between versions
- Generate research summaries for dependency reviews
- Validate compatibility with current codebase
- Check release history and maintenance status

## Core Research Methods

### 1. Retrieve Package Metadata

Get comprehensive package information from npm registry:

```bash
npm view PACKAGE --json > package-meta.json
```

**Extracts:**
- Current version and tags (latest, next, alpha, beta)
- All published versions and release dates
- Maintainers and repository information
- Dependencies and peer dependencies
- Keywords and homepage
- Download statistics

Parse to find specific versions:

```bash
npm view PACKAGE@VERSION --json
```

Get only the latest version info (compact):

```bash
npm view PACKAGE version
npm view PACKAGE versions --json | jq '.[-1]'
```

### 2. Changelog Research

#### From npm registry (if published in README or description)

```bash
npm view PACKAGE readme | grep -A 50 -i "changelog\|release\|history" | head -100
```

#### From GitHub releases (if package has repo link)

```bash
# Extract repository URL from package metadata
REPO_URL=$(npm view PACKAGE repository.url | sed 's/git+//g' | sed 's/.git$//g' | sed 's|https://github.com/||g')

# Fetch releases using GitHub CLI
gh api repos/${REPO_URL}/releases --paginate \
  | jq -r '.[] | "\(.tag_name): \(.name)\n\(.body)\n---"' \
  | head -200
```

#### From npm package release notes

```bash
# Query npm registry for release timeline
npm view PACKAGE time --json \
  | jq 'to_entries[] | select(.key | test("VERSION_PATTERN")) | "\(.key): \(.value)"'
```

#### Manual inspection approach

1. Visit `https://www.npmjs.com/package/PACKAGE`
2. Navigate to **Versions** tab → select target version
3. Check **README** and **Changelog** links in sidebar
4. Read linked GitHub repository releases section

### 3. Security Vulnerability Research

#### NPM audit data (local or remote)

```bash
# Check local project vulnerabilities for a specific package
npm audit --package-lock-only | grep -A 5 "PACKAGE"

# Query npm registry for package vulnerabilities
curl -s https://api.github.com/repos/npm/npm-audit-db/contents/data | jq '.'
```

#### NPM security advisories database

```bash
# Use npm CLI (requires npm v6+)
npm audit --audit-level=moderate

# Check specific package audit
npm audit --package-lock-only | jq '.vulnerabilities.PACKAGE'
```

#### Third-party security resources

- **Snyk.io**: `https://snyk.io/vuln/npm:PACKAGE` (search by package name)
- **CVE Database**: `https://cve.mitre.org/` (search by CVE ID if known)
- **GitHub Security Advisories**: Search package name in `https://github.com/advisories`
- **OWASP Dependency Check**: Local scanning with known vulnerabilities database

#### Manual security check

1. Visit `https://www.npmjs.com/package/PACKAGE`
2. Check **Security** tab (if available)
3. Review recent issues on GitHub repository (`/issues` or `/security`)
4. Check for **SECURITY.md** file in repo root

### 4. Breaking Changes Research

#### From package.json semver bumps

```bash
# Compare two versions to estimate breaking changes
npm view PACKAGE versions --json | jq -r '.[] | select(test("VERSION_REGEX"))' | tail -20

# Identify major version bumps (likely breaking changes)
npm view PACKAGE versions --json | jq -r '.[] | select(startswith("2.") or startswith("3."))' 
```

#### From GitHub releases and tags

```bash
# Extract repository from package metadata
REPO=$(npm view PACKAGE repository.url | sed 's/git+//g' | sed 's/.git$//g' | sed 's|https://github.com/||g')

# Get tags using GitHub CLI
gh api repos/${REPO}/tags --paginate | jq -r '.[] | "\(.name): \(.commit.message)"'

# Compare commits between two tags
gh api repos/${REPO}/compare/VERSION1...VERSION2 \
  | jq -r '.commits[] | .commit.message' \
  | grep -i "breaking\|BREAKING CHANGE\|⚠️"
```

#### From CHANGELOG files

```bash
# Extract repository from package
REPO=$(npm view PACKAGE repository.url | sed 's/git+//g' | sed 's/.git$//g' | sed 's|https://github.com/||g')

# View file directly
gh api repos/${REPO}/contents/CHANGELOG.md --jq .content | base64 -d \
  | sed -n '/## \[VERSION_FROM\]/,/## \[VERSION_TO\]/p'

# Or clone repo and extract changelog
gh repo clone ${REPO} /tmp/repo-temp -- --depth=1
cat /tmp/repo-temp/CHANGELOG.md | sed -n '/## \[VERSION_FROM\]/,/## \[VERSION_TO\]/p'

```

Patterns to search for breaking changes:

- `BREAKING CHANGE:` or `breaking change`
- `⚠️` (warning emoji)
- Major version bumps (1.0.0 → 2.0.0)
- API changes in function signatures
- Removed exports or modules
- Changed configuration options
- Dependency removals or upgrades with semver constraints

#### Manual inspection

1. Visit package repository (link in `https://www.npmjs.com/package/PACKAGE`)
2. Check **CHANGELOG.md**, **HISTORY.md**, or **RELEASES.md** in repo root
3. Navigate to GitHub **Releases** section → filter by versions of interest
4. Search commit history for "BREAKING CHANGE" commits between versions
5. Check repository **Wiki** or **Discussions** for migration guides

### 5. Dependency Impact Analysis

Check what new or updated dependencies come with the package:

```bash
# Install in temporary directory and check dependencies
npm install PACKAGE@VERSION --no-save --prefix /tmp/research-PACKAGE

# List dependency tree
npm ls --prefix /tmp/research-PACKAGE

# Find new deps vs current version
diff <(npm ls PACKAGE@OLD_VERSION --json --prefix /tmp/old | jq '.dependencies | keys') \
     <(npm ls PACKAGE@NEW_VERSION --json --prefix /tmp/new | jq '.dependencies | keys')
```

### 6. Pull Request Research (when needed)

When a release mentions specific PRs or you need to understand code-level changes:

#### List recent PRs in package repository

```bash
# Extract repository from package
REPO=$(npm view PACKAGE repository.url | sed 's/git+//g' | sed 's/.git$//g' | sed 's|https://github.com/||g')

# List PRs merged between two tags/versions
gh pr list --repo ${REPO} --state merged --search "merged:>=VERSION_DATE" --json number,title,mergedAt,labels

# List PRs by milestone (if package uses milestones for releases)
gh pr list --repo ${REPO} --state merged --search "milestone:VERSION" --json number,title,url
```

#### View specific PR details and code changes

```bash
# Get PR details (title, body, labels, review status)
gh pr view PR_NUMBER --repo ${REPO} --json title,body,state,labels,reviews

# View PR diff (changed files summary)
gh pr diff PR_NUMBER --repo ${REPO}

# View specific file changes in PR
gh pr diff PR_NUMBER --repo ${REPO} -- path/to/file.ts

# Get list of changed files
gh pr view PR_NUMBER --repo ${REPO} --json files | jq -r '.files[].path'
```

#### Research breaking changes from PR content

```bash
# Search PR titles/bodies for breaking change keywords
gh pr list --repo ${REPO} --state merged --search "BREAKING in:title,body" --json number,title,url

# View PR conversation and review comments (identify concerns/warnings)
gh pr view PR_NUMBER --repo ${REPO} --comments

# Check if PR has breaking change label
gh pr view PR_NUMBER --repo ${REPO} --json labels | jq -r '.labels[] | select(.name | test("breaking"; "i")) | .name'
```

#### Find PRs between two releases

```bash
# Get commit range between versions
COMMITS=$(gh api repos/${REPO}/compare/v${OLD_VERSION}...v${NEW_VERSION} --jq '.commits[].sha')

# Find PRs associated with those commits
for commit in $COMMITS; do
  gh api "repos/${REPO}/commits/${commit}/pulls" --jq '.[].number'
done | sort -u | while read pr; do
  gh pr view $pr --repo ${REPO} --json number,title,url
done
```

#### When to research PRs

- **Release notes reference specific PR numbers** → View those PRs for detailed context
- **Breaking changes mentioned without details** → Search for related PRs
- **Major refactors or API changes** → Review code changes to understand impact
- **Security fixes** → Verify the fix and check if it affects your usage patterns
- **Undocumented changes** → Find PRs between versions to discover unlisted changes
- **Migration guidance needed** → Look for migration-related PRs or discussions

### 7. Peer Dependency Warnings

Identify peer dependency requirements:

```bash
npm view PACKAGE@VERSION peerDependencies --json

# Check if current project satisfies peer deps
npm ls --depth=0 REQUIRED_PEER_DEP
```

## Structured Research Template

Use this checklist for comprehensive research:

```markdown
## NPM Research: PACKAGE (OLD_VERSION → NEW_VERSION)

### Release Information
- [ ] Current stable version: `X.Y.Z`
- [ ] Target version: `X.Y.Z`
- [ ] Release date: YYYY-MM-DD
- [ ] Maintenance status: (active/inactive/deprecated)

### Changelog Summary
- **Key features added**: ...
- **Bug fixes**: ...
- **Performance improvements**: ...
- **Deprecated features**: ...

### Breaking Changes
- [ ] Major version bump: Yes / No
- **Critical breaking changes**:
  - ...
- **Migration guide**: Link to docs or GitHub discussion
- **Related PRs reviewed**: #123, #456 (if applicable)

### Security Advisories
- [ ] Known vulnerabilities in current version: None / CVE-LIST
- [ ] Known vulnerabilities in target version: None / CVE-LIST
- [ ] Security advisory links: ...
- **Security fix PRs**: (if applicable)

### Dependency Changes
- **New dependencies**: (list major ones)
- **Removed dependencies**: (list major ones)
- **Updated dependency versions**: (check for conflicts)
- **Peer dependency requirements**: (verify compatibility)

### Pull Requests Reviewed (if needed)
- **PR #XXX**: Brief summary of changes and impact
- **PR #YYY**: Brief summary of changes and impact
- **Code changes affecting us**: (specific files/functions if relevant)

### Codebase Impact
- [ ] Need code changes: Yes / No
  - Details: ...
- [ ] Need configuration changes: Yes / No
  - Details: ...
- **Estimated risk level**: Low / Medium / High
- **Recommendation**: Safe to upgrade / Review carefully / Wait

### References
- npm registry: https://www.npmjs.com/package/PACKAGE
- GitHub releases: LINK
- Changelog: LINK
- Security advisories: LINK
```

## Quick Commands Reference

| Task | Command |
|------|---------|
| Get latest version | `npm view PACKAGE version` |
| List all versions | `npm view PACKAGE versions --json \| jq '.[]'` |
| Get package info | `npm view PACKAGE --json` |
| Check vulnerabilities | `npm audit --audit-level=moderate` |
| Read changelog | `npm view PACKAGE readme \| grep -i changelog` |
| Get repo URL | `npm view PACKAGE repository.url` |
| Test install | `npm install PACKAGE@VERSION --dry-run` |
| Check peer deps | `npm view PACKAGE@VERSION peerDependencies` |
| List merged PRs | `gh pr list --repo OWNER/REPO --state merged` |
| View PR details | `gh pr view PR_NUMBER --repo OWNER/REPO` |
| View PR diff | `gh pr diff PR_NUMBER --repo OWNER/REPO` |
| Search PRs | `gh pr list --repo OWNER/REPO --search "QUERY"` |

## Integration with Fusion Framework

### When used in Dependabot PR handler

The npm-research skill feeds into [dependabot-pr-handler](../dependabot-pr-handler/SKILL.md) **Step 4** (Research Dependencies) to provide:

1. **Changelog summary** for research comment
2. **Security advisories** for risk assessment
3. **Breaking changes** for code impact analysis
4. **Dependency blast radius** combined with pnpm-dependency-analysis
5. **PR-level code changes** when release notes lack details or breaking changes need investigation

### Recommended workflow

1. Run npm-research to gather data (changelog, security, versions)
2. **If needed**: Use gh CLI to research specific PRs mentioned in release notes
3. **If needed**: View code-level changes from critical PRs (breaking changes, security fixes)
4. Feed findings to pnpm-dependency-analysis for workspace impact
5. Use results to populate research comment template
6. Inform decision on whether code changes are needed
7. Gate merge approval on security and breaking change assessment

## Guardrails

- **Always check date**: Release dates reveal maintenance activity and urgency
- **Cross-reference sources**: Compare npm.js info, GitHub, and CVE databases
- **Test locally first**: Use `--dry-run` or test in isolated environment before full upgrade
- **Document findings**: Always provide research summary for team review
- **Check peer dependencies**: Ensure compatibility with entire dependency tree
- **Verify deprecation status**: Don't upgrade to deprecated versions without reason
