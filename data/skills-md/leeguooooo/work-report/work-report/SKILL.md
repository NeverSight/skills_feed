---
name: work-report
description: Write a daily or weekly work report using git commits. Use when the user asks to write or send a daily report/standup or weekly report, especially "日报", "发日报", "周报", "发周报", "daily report", "weekly report", or "work report".
---

# Work Report

## Workflow

- Determine local date and format as `MM.DD` (no year).
- Decide daily vs weekly based on the user's request.
- Confirm the workspace root path for scanning multiple repos; if the user hasn't provided one, first check WORK_REPORT_ROOT or CODEX_WORK_ROOT, then ask.
- For daily reports, collect git commit subjects by author across all repos under the target root, grouped by project (repo).
  - Prefer using `scripts/git_today_commits.sh --root <path> --period daily --group-by-repo`.
  - If needed, run manually per repo: `git log --since=midnight --author "<name>" --pretty=format:%s`.
  - Rewrite commit subjects into concise Chinese items and then turn them into a numbered list under each project (avoid English output); replace low-value or sensitive phrases (e.g., "解决冲突") with business-friendly wording (e.g., "代码集成与稳定性维护").
  - If there are no commits, ask the user for manual items.
- For weekly reports, summarize git commits into concise Chinese items grouped by project (do not require user input unless there are no commits).
  - Prefer using `scripts/git_today_commits.sh --root <path> --period weekly --group-by-repo`.
  - Convert commit subjects into 1-5 Chinese summary items per project (merge similar changes).
- Only treat directories with a `.git` folder or file as projects. Ignore non-git directories. Include nested repos under the root.

## Script

Use `scripts/git_today_commits.sh` to list commit subjects.

- If you're not in this skill directory, call it via `~/.codex/skills/work-report/scripts/git_today_commits.sh` (or `$CODEX_HOME/skills/work-report/scripts/git_today_commits.sh`).
- `--root <path>` is required unless `--repo` is provided or WORK_REPORT_ROOT/CODEX_WORK_ROOT is set.
- Default author comes from `git config --global user.name`, then `git config --global user.email`.
- Use `--root <path>` to target a different root folder.
- Use `--repo <path>` to target a single repo.
- Use `--author "Name"` to override author.
- Use `--period daily|weekly` to pick the time range.
- Use `--since "<expr>"` to override the time range (e.g., "yesterday").
- Use `--with-repo` to prefix each item with the repo name.
- Use `--group-by-repo` to output sections grouped by repo for easier report formatting.
- Commits are collected across all branches by default (`git log --all`). Use `--no-all` to limit to the current branch.
- Normalization is enabled by default to make items more business-friendly; use `--no-normalize` to keep raw commit subjects.

## Output format

Use "今日工作总结" as the header text for daily reports. When the script outputs bullets, convert them into a numbered list.

```
MM.DD 今日工作总结
<项目A>
1.<item>
2.<item>
<项目B>
1.<item>
```

Use "本周工作总结" as the header text for weekly reports. Weekly items are a Chinese summary derived from git commits. The time range should follow the natural week starting Monday.

```
MM.DD-MM.DD 本周工作总结
<项目A>
1.<item>
2.<item>
<项目B>
1.<item>
```
