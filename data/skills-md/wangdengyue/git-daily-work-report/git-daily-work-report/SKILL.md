---
name: git-daily-work-report
description: "Automatically generate daily work reports by scanning Git repositories. Use this skill when the user asks to: (1) Generate a daily report from git commits, (2) Summarize work done on a specific date based on code changes, (3) Check commits and create work summary for a date. The skill scans all git repositories under a root directory, filters by author, retrieves commit records with file changes, and generates a summarized work content description using LLM analysis."
---

# Git Daily Work Report

Automatic daily work report generation by scanning Git repositories.

## When to Use

Use this skill when:
- User asks to generate a daily report from git commits
- User wants to summarize work done on a specific date
- User requests work summary based on code changes in a monorepo or multi-repo project
- User needs to check commits by a specific author

## Workflow

### Step 1: Scan Git Repositories

Use the bundled script to scan all git repositories under a root directory:

```bash
python scripts/get_git_log.py <root_path> <date> [--author <name>] [--json]
```

Parameters:
- `root_path`: Root directory containing multiple git repositories
- `date`: Date in `YYYY-MM-DD` format
- `--author` (optional): Filter commits by author name
- `--json`: Output in JSON format for LLM processing (default: formatted report)

Example:
```bash
# Scan all repos for commits on a specific date
python scripts/get_git_log.py /path/to/project 2026-01-23

# Filter by author
python scripts/get_git_log.py /path/to/project 2026-01-23 --author "dengyue"

# Output JSON for LLM processing
python scripts/get_git_log.py /path/to/project 2026-01-23 --json
```

**Note:** The script automatically scans all subdirectories and finds git repositories. It's designed for monorepo layouts where multiple projects exist under a single root directory (e.g., `D:\work\` containing projects like `Libraries`, `core`, `Admin`, etc.).

### Step 2: Analyze Commits with LLM

Process the git log output to generate work summary:

1. Group commits by repository/project
2. Summarize what was changed based on commit messages and file changes
3. Identify major features, bug fixes, or improvements
4. Generate clear, professional work content description

### Step 3: Submit Report (via MCP)

Use browser automation MCP to submit the generated work content to the internal reporting system.

## Output Format

The script generates a formatted report by default:

```
   dengyue 提交日报（2026-01-23）
==========================================

[Libraries]
- 连接redis的slave
  文件变更：
    M       src/redis/connection.py

[Admin]
- 修复用户登录bug
  文件变更：
    M       controllers/auth.go
    M       models/user.go
```

For LLM processing, use `--json` to get structured data. The final work summary should be:

- **Clear and concise**: Describe what work was done
- **Categorized**: Group related changes by repository
- **Professional**: Use appropriate language for daily reporting

Example final output format:

```
## 2026-01-23 工作总结

### EMLibraries
- 修改 Redis 连接配置，切换到 slave 节点以实现读写分离

### Admin
- 修复用户登录时的 session 验证 bug
- 优化用户信息查询性能

### Bug 修复
- 解决登录超时问题
- 修复权限验证逻辑错误

### 代码优化
- 重构 Redis 连接池管理
```

## Notes

- Ensure git is installed and accessible in the system PATH
- The script sets UTF-8 encoding for output on Windows platforms automatically
- The script handles UTF-8 encoding for commit messages (with error tolerance)
- File changes are included for each commit to provide context
- The script skips nested git repositories (only scans top-level repos)
- For projects with many repositories, the scan may take some time
