---
name: my
description: |
  Personal toolkit - session handoff, git worktree.
  Triggers: "handoff", "resume", "worktree"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: claude-sonnet-4-5-20250929
---

# My Skill

개인 개발 도구 모음. 공식 플러그인에 없는 기능 제공.

## Commands

### Session (`session-*`)
세션 컨텍스트 연속성: `/my:session-handoff`, `/my:session-resume`
See: `context/session.md`

### Worktree (`wt-*`)
병렬 개발: `/my:wt-plan`, `/my:wt-distribute`, `/my:wt-launch`, `/my:wt-status`, `/my:wt-sync`
See: `context/worktree.md`

## Context Files

| File | Purpose |
|------|---------|
| `context/session.md` | Session management guide |
| `context/worktree.md` | Worktree operation guide |
| `context/handoff-template.md` | Handoff document template |
| `context/worktree-guide.md` | Worktree quick reference |
