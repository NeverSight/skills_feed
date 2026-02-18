---
name: standup-meeting
description: Conduct effective daily standup meetings for agile teams. Use when facilitating standups, tracking blockers, or improving team synchronization. Handles standup format, time management, and blocker resolution.
tags: [standup, daily-scrum, agile, team-sync, blockers]
platforms: [Claude, ChatGPT, Gemini]
---

# Standup Meeting


## When to use this skill

- **매일**: 같은 시간, 같은 장소
- **스프린트 중**: 팀 동기화 필요 시
- **원격 팀**: 비동기 스탠드업

## Instructions

### Step 1: 3 Questions 포맷

```markdown
## Daily Standup Template

**Date**: 2025-01-15
**Time**: 9:30 AM
**Duration**: 15분

### 팀원 A
- **어제 한 일**:
  - 사용자 인증 API 완료 (#123)
  - Code review 2건
- **오늘 할 일**:
  - JWT refresh token 구현 (#124)
  - 단위 테스트 작성
- **블로커**:
  - Redis 설정 문서 필요 (팀원 B에게 도움 요청)

### 팀원 B
- **어제 한 일**:
  - 프론트엔드 폼 validation (#125)
- **오늘 할 일**:
  - 프로필 페이지 UI 구현 (#126)
- **블로커**: 없음

### 팀원 C
- **어제 한 일**:
  - 데이터베이스 마이그레이션 (#127)
  - 성능 테스트
- **오늘 할 일**:
  - 인덱스 최적화 (#128)
- **블로커**:
  - 프로덕션 DB 접근 권한 필요 (긴급)

### Action Items
1. [ ] 팀원 B가 팀원 A에게 Redis 문서 공유 (오늘 10:00)
2. [ ] 팀장이 팀원 C의 DB 권한 요청 (오늘 중)
```

### Step 2: Walking the Board (보드 기반)

```markdown
## Standup: Walking the Board

**Sprint Goal**: 사용자 인증 시스템 완성

### In Progress
- #123: User Login API (팀원 A, 80% 완료)
- #124: Refresh Token (팀원 A, 시작 예정)
- #125: Form Validation (팀원 B, 90% 완료)

### Blocked
- #127: DB Migration (팀원 C)
  - **블로커**: 권한 필요
  - **Owner**: 팀장
  - **ETA**: 오늘 오후

### Ready for Review
- #122: Password Reset (팀원 D)
  - 리뷰어 필요

### Done
- #120: Email Service Integration
- #121: User Registration

### Sprint Progress
- **Completed**: 12 points
- **Remaining**: 13 points
- **On Track**: Yes ✅
```

### Step 3: 비동기 Standup (원격 팀)

**Slack 템플릿**:
```markdown
[Daily Update - 2025-01-15]

**Yesterday**
- Completed user authentication flow
- Fixed bug in password validation

**Today**
- Implementing JWT refresh tokens
- Writing unit tests

**Blockers**
- None

**Sprint Progress**
- 8/13 story points completed
```

## Output format

### Standup 회의록

```markdown
# Daily Standup - 2025-01-15

**Attendees**: 5/5
**Duration**: 12 minutes
**Sprint**: Sprint 10 (Day 3/10)

## Summary
- Stories Completed: 2 (5 points)
- Stories In Progress: 3 (8 points)
- Blockers: 1 (DB access권한)

## Individual Updates
[위의 3 Questions 포맷 참조]

## Action Items
1. 팀장: DB 권한 요청 (High priority)
2. 팀원 B: Redis 문서 공유
3. 팀원 D: PR #122 리뷰어 할당

## Notes
- Sprint goal on track
- Team morale: High
```

## Constraints

### 필수 규칙 (MUST)

1. **Time-boxed**: 15분 이내
2. **같은 시간**: 매일 일정한 시간
3. **전원 참여**: 모든 팀원 업데이트

### 금지 사항 (MUST NOT)

1. **Problem Solving**: 스탠드업에서 문제 해결하지 않음
2. **Status Report**: 관리자에게 보고하는 자리 아님
3. **Late Start**: 시간 엄수

## Best practices

1. **Stand Up**: 실제로 서서 진행 (짧게 유지)
2. **Parking Lot**: 깊은 논의는 별도 시간
3. **Visualize**: 보드를 보며 진행

## References

- [Scrum Guide - Daily Scrum](https://scrumguides.org/)
- [15 Minute Stand-up](https://www.mountaingoatsoftware.com/agile/scrum/meetings/daily-scrum)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 태그
`#standup` `#daily-scrum` `#agile` `#team-sync` `#project-management`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
