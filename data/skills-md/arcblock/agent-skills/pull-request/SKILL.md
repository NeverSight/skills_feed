---
name: pull-request
description: PR Generator - Generate standardized Pull Request based on branch diff and submit via gh or save as PR.md
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Pull Request Skill

Generate standardized Pull Requests by analyzing the diff between current branch and main branch.

## Step 0: Check for Project PR Template (IMPORTANT)

**CRITICAL**: Before generating PR content, ALWAYS check if the project has a custom PR template:

```bash
# Check for PR template in common locations
ls -la .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null || \
ls -la .github/PULL_REQUEST_TEMPLATE/ 2>/dev/null || \
ls -la docs/PULL_REQUEST_TEMPLATE.md 2>/dev/null
```

**If a PR template exists**:
1. Read the template file using the Read tool
2. Use that template's structure for the PR body
3. Fill in each section according to the template's format and comments
4. Keep any checkboxes or structured lists from the template

**If no PR template exists**:
Use the default template defined below.

## PR Template (Default - Use only if no project template exists)

Based on analysis of high-quality PRs, use this template:

### Title Format

```
<type>(<scope>): <description>
```

**Types** (same as Conventional Commits):
| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Code style changes |
| `refactor` | Code refactoring |
| `perf` | Performance improvement |
| `test` | Add or modify tests |
| `chore` | Build process or tools |
| `ci` | CI/CD configuration |
| `build` | Build system changes |

**Scope**: Optional, indicates affected module (e.g., `devflow`, `blocklet`, `auth`)

**Description**:
- Imperative mood ("add" not "added")
- Lowercase first letter
- No period at end
- Under 72 characters

### Body Format

```markdown
## Summary

<1-5 bullet points describing key changes>

## Motivation / Context

<Why this change is needed - the problem being solved>

## Changes

<Detailed list of what was changed, organized by area>

## Test Plan

<How to verify the changes work correctly>
- [ ] Step 1
- [ ] Step 2

---

Generated with [Claude Code](https://claude.com/claude-code)
```

## Workflow

### Step 1: Gather Branch Information

```bash
# Get current branch name
git branch --show-current

# Get main branch (usually 'main' or 'master')
git remote show origin | grep 'HEAD branch' | cut -d' ' -f5

# Check if branch is pushed to remote
git status -sb
```

### Step 2: Analyze All Commits and Changes

**IMPORTANT**: Analyze ALL commits from branch divergence point, not just the latest commit.

```bash
# Get the merge base (where current branch diverged from main)
git merge-base main HEAD

# View all commits since diverging from main
git log main..HEAD --oneline

# Get comprehensive diff statistics
git diff main...HEAD --stat

# Get full diff for content analysis
git diff main...HEAD
```

### Step 3: Generate PR Content

Based on the diff analysis:

1. **Determine type**: Look at the nature of changes
   - New files/features → `feat`
   - Bug fixes → `fix`
   - Only .md files → `docs`
   - Only test files → `test`
   - Configuration/tooling → `chore`

2. **Identify scope**: Look at which module/area is most affected

3. **Use project template if exists**: If Step 0 found a PR template:
   - Read the template file
   - Fill in each section according to the template's structure
   - Keep all checkboxes from the template (check appropriate ones based on changes)
   - Respect the template's language (Chinese/English)
   - Follow any instructions in HTML comments

4. **Otherwise use default template**:
   - Write summary: Capture the essence of ALL commits, not just one
   - Document motivation: Explain why these changes are needed
   - List changes: Organize by logical groupings
   - Create test plan: Practical verification steps

### Step 4: Present PR Draft and Ask User

Display the generated PR title and body to the user, then use **AskUserQuestion** to determine next action:

```json
{
  "questions": [{
    "question": "How would you like to proceed with this PR?",
    "header": "PR Action",
    "options": [
      {"label": "Save as PR.md (Recommended)", "description": "Save PR content to PR.md file in project root (will overwrite if exists)"},
      {"label": "Submit via gh", "description": "Create PR directly using GitHub CLI"}
    ],
    "multiSelect": false
  }]
}
```

### Step 5A: If "Save as PR.md"

Write the PR content to `./PR.md` in the project root:

```markdown
# PR Title

<type>(<scope>): <description>

---

## Summary

...

## Motivation / Context

...

## Changes

...

## Test Plan

...

---

Generated with [Claude Code](https://claude.com/claude-code)
```

Inform user that PR.md has been created (or overwritten if it existed).

### Step 5B: If "Submit via gh"

#### 5B.1: Check gh CLI availability

```bash
which gh
```

If `gh` is not found:
```
GitHub CLI (gh) is not installed. Please install it:

- macOS: brew install gh
- Linux: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md
- Windows: winget install --id GitHub.cli

After installation, run: gh auth login
```

#### 5B.2: Check gh authentication

```bash
gh auth status
```

If not authenticated or token lacks permissions:
```
GitHub CLI is not authenticated or lacks permissions. Please run:

gh auth login

Select:
- GitHub.com
- HTTPS
- Authenticate with browser (recommended)

Ensure you grant 'repo' scope for creating PRs.
```

#### 5B.3: Check if branch is pushed

```bash
git status -sb
```

If branch is not pushed to remote:
```bash
# Push current branch to origin
git push -u origin $(git branch --show-current)
```

#### 5B.4: Create the PR

```bash
gh pr create --base main --title "<title>" --body "$(cat <<'EOF'
<body content>
EOF
)"
```

#### 5B.5: Report Success

Display the PR URL and summary to the user.

## Example Output

### Title
```
feat(devflow): add PR generation skill
```

### Body
```markdown
## Summary

- Add new `pull-request` skill for generating standardized Pull Requests
- Analyze diff between current branch and main branch
- Support both gh CLI submission and PR.md file generation
- Include comprehensive PR template based on best practices

## Motivation / Context

Creating consistent, well-documented PRs is important for code review efficiency.
This skill automates PR generation by analyzing git diff and following established patterns.

## Changes

### New Files
- `.claude/skills/pull-request/SKILL.md` - Pull Request generation skill definition

### Workflow
- Step 1: Gather branch and diff information
- Step 2: Analyze all commits since branch divergence
- Step 3: Generate PR content following template
- Step 4: Ask user for submission method
- Step 5: Execute chosen action (gh submit or save to file)

## Test Plan

- [ ] Run `/pull-request` on a feature branch with changes
- [ ] Verify PR title follows conventional commit format
- [ ] Verify summary captures all changes
- [ ] Test gh submission flow
- [ ] Test PR.md generation flow

```

## Example Output (With Project Template)

When project has `.github/PULL_REQUEST_TEMPLATE.md`, fill in that template instead:

### Title
```
feat(test): add coverage merge and reporting support
```

### Body (following project template structure)
```markdown
### 关联 Issue

related: https://github.com/example/repo/issues/123

### 主要改动

1. 新增 `--coverage` 参数支持测试覆盖率收集
2. 创建 `merge-coverage.js` 脚本合并所有子包的覆盖率报告
3. 重新启用 CI 覆盖率报告功能
4. 排除编译后和自动生成的文件以获得准确的覆盖率统计

### 界面截图

N/A (无 UI 变更)

### 测试清单

- [x] 本次变更的地方已经有测试覆盖
- [ ] 本次变更的地方调整了测试覆盖
- [x] 本次变更的地方新增了测试覆盖
- [ ] 本次变更的兼容性测试覆盖了桌面端 Chrome
- [ ] 本次变更的兼容性测试覆盖了桌面端 Safari
- [ ] 本次变更的兼容性测试覆盖了移动端：ArcSphere + DID Wallet
- [ ] 本次变更有新增界面，且我检查了 light 模式下的展示效果
- [ ] 本次变更有新增界面，且我检查了 dark 模式下的展示效果
- [ ] 如果修改 domain 相关 issue, 请检查 server / service / 购买启动中 是否正常

### 检查清单

- [x] 这次变更包含 breaking change，我为 breaking change 编写了 migration script【如果不是 breaking change 可以勾选】
- [ ] 本次变更需要更新文档，并且我更新了相关文档，如果还没更新文档，请新建文档更新的 Issue 并关联上来
- [x] 本次变更中有用户输入的逻辑，用户输入的后端、前端都增加了校验、错误提示
- [ ] 本次变更中新增了修改后端数据的 API，我给这个 API 增加了 AuditLog
- [x] 本次变更中新增了修改后端数据的 API，且该接口返回的数据中不包含敏感信息
- [x] 本次变更新增了文件，对应 package.json 的 files 字段包括了这些新增的文件
- [ ] 本次变更增加了依赖，并且 core/blocklet-services 和 core/webapp 的前端依赖我放在了 devDependencies 里面
- [ ] 本次变更增加了 blocklet/sdk 的依赖，不会导致 bundle 失败
- [ ] 本次变更中有添加或更新 npm 依赖，并且没有导致同 1 个依赖出现多个版本
- [x] 本次变更我已经把 ArcBlock 的依赖升级到了最新
- [ ] (merge master 前检测) 成功 `make build`, `blocklet server init`, `blocklet server start`
- [ ] (merge master 前检测) 成功 `bn dev`, `bn dev --app-id xxx`
- [ ] (merge master 前检测) 我已阅读并理解了发布 beta 版 Server 的手册

---

Generated with [Claude Code](https://claude.com/claude-code)
```

## Rules

1. **Always check for project PR template first** - Look for `.github/PULL_REQUEST_TEMPLATE.md` before generating content
2. **Use project template if exists** - Follow the project's PR template structure, language, and checkboxes
3. **Always analyze ALL commits** from branch divergence point, not just HEAD
4. **Follow Conventional Commits** format for title
5. **Keep title under 72 characters**
6. **Include test plan** with actionable verification steps
7. **Base PR on main branch** (or project's default branch)
8. **Check gh auth** before attempting to create PR
9. **Push branch first** if not already pushed to remote
10. **Preserve user's intent** - ask before overwriting existing PR.md
11. **Respect template language** - If project template is in Chinese, write PR body in Chinese
