---
name: task-planning
description: Plan and organize software development tasks effectively. Use when breaking down features, creating user stories, or planning sprints. Handles task breakdown, user stories, acceptance criteria, and backlog management.
tags: [task-planning, user-stories, backlog, sprint-planning, agile]
platforms: [Claude, ChatGPT, Gemini]
---

# Task Planning


## When to use this skill

- **피처 개발**: 새 기능을 작은 태스크로 분할
- **Sprint Planning**: 스프린트에 포함할 작업 선정
- **Backlog Grooming**: 백로그 정리 및 우선순위 설정

## Instructions

### Step 1: User Story 작성 (INVEST)

**INVEST 원칙**:
- **I**ndependent: 독립적
- **N**egotiable: 협상 가능
- **V**aluable: 가치 있음
- **E**stimable: 추정 가능
- **S**mall: 작음
- **T**estable: 테스트 가능

**템플릿**:
```markdown
## User Story: [제목]

**As a** [사용자 유형]
**I want** [기능]
**So that** [가치/이유]

### Acceptance Criteria
- [ ] Given [상황] When [행동] Then [결과]
- [ ] Given [상황] When [행동] Then [결과]
- [ ] Given [상황] When [행동] Then [결과]

### Technical Notes
- API endpoint: POST /api/users
- Database: users 테이블
- Frontend: React component

### Estimation
- Story Points: 5
- T-Shirt: M

### Dependencies
- User authentication must be completed first

### Priority
- MoSCoW: Must Have
- Business Value: High
```

**예시**:
```markdown
## User Story: User Registration

**As a** new visitor
**I want** to create an account
**So that** I can access personalized features

### Acceptance Criteria
- [ ] Given valid email and password When user submits form Then account is created
- [ ] Given duplicate email When user submits Then error message is shown
- [ ] Given weak password When user submits Then validation error is shown
- [ ] Given successful registration When account created Then welcome email is sent

### Technical Notes
- Hash password with bcrypt
- Validate email format
- Send welcome email via SendGrid
- Store user in PostgreSQL

### Estimation
- Story Points: 5

### Dependencies
- Email service integration (#123)

### Priority
- MoSCoW: Must Have
```

### Step 2: Epic → Story → Task 분해

```markdown
## Epic: User Management System

### Story 1: User Registration
- **Points**: 5
- Tasks:
  - [ ] Design registration form UI (2h)
  - [ ] Create POST /api/users endpoint (3h)
  - [ ] Implement email validation (1h)
  - [ ] Add password strength checker (2h)
  - [ ] Write unit tests (2h)
  - [ ] Integration testing (2h)

### Story 2: User Login
- **Points**: 3
- Tasks:
  - [ ] Design login form (2h)
  - [ ] Create POST /api/auth/login endpoint (2h)
  - [ ] Implement JWT token generation (2h)
  - [ ] Add "Remember Me" functionality (1h)
  - [ ] Write tests (2h)

### Story 3: Password Reset
- **Points**: 5
- Tasks:
  - [ ] "Forgot Password" UI (2h)
  - [ ] Generate reset token (2h)
  - [ ] Send reset email (1h)
  - [ ] Reset password form (2h)
  - [ ] Update password API (2h)
  - [ ] Tests (2h)
```

### Step 3: MoSCoW 우선순위

```markdown
## Feature Prioritization (MoSCoW)

### Must Have (Sprint 1)
- User Registration
- User Login
- Basic Profile Page

### Should Have (Sprint 2)
- Password Reset
- Email Verification
- Profile Picture Upload

### Could Have (Sprint 3)
- Two-Factor Authentication
- Social Login (Google, GitHub)
- Account Deletion

### Won't Have (This Release)
- Biometric Authentication
- Multiple Sessions Management
```

### Step 4: Sprint Planning

```markdown
## Sprint 10 Planning

**Sprint Goal**: Complete user authentication system

**Duration**: 2 weeks
**Team Capacity**: 40 hours × 4 people = 160 hours
**Estimated Velocity**: 30 story points

### Selected Stories
1. User Registration (5 points) - Must Have
2. User Login (3 points) - Must Have
3. Password Reset (5 points) - Must Have
4. Email Verification (3 points) - Should Have
5. Profile Edit (5 points) - Should Have
6. JWT Refresh Token (3 points) - Should Have
7. Rate Limiting (2 points) - Should Have
8. Security Audit (4 points) - Must Have

**Total**: 30 points

### Sprint Backlog
- [ ] User Registration (#101)
- [ ] User Login (#102)
- [ ] Password Reset (#103)
- [ ] Email Verification (#104)
- [ ] Profile Edit (#105)
- [ ] JWT Refresh Token (#106)
- [ ] Rate Limiting (#107)
- [ ] Security Audit (#108)

### Definition of Done
- [ ] Code written and reviewed
- [ ] Unit tests passing (80%+ coverage)
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] QA approved
```

## Output format

### 태스크 보드 구조

```
Backlog → To Do → In Progress → Review → Done

Backlog:
- 우선순위별 정렬
- Grooming 완료된 스토리

To Do:
- Sprint에 선택된 작업
- 담당자 할당됨

In Progress:
- WIP Limit: 2 per person
- 진행 중인 작업

Review:
- Code review 대기
- QA 테스트 중

Done:
- DoD 충족
- 배포 완료
```

## Constraints

### 필수 규칙 (MUST)

1. **명확한 AC**: Acceptance Criteria 필수
2. **추정 완료**: 모든 스토리에 포인트 할당
3. **의존성 파악**: 선행 작업 명시

### 금지 사항 (MUST NOT)

1. **너무 큰 스토리**: 13+ points는 분할
2. **모호한 요구사항**: "개선한다", "최적화한다" 금지

## Best practices

1. **INVEST 원칙**: 좋은 사용자 스토리 작성
2. **Definition of Ready**: 스프린트 시작 전 준비 완료
3. **Definition of Done**: 명확한 완료 기준

## References

- [User Story Guide](https://www.atlassian.com/agile/project-management/user-stories)
- [MoSCoW Prioritization](https://www.productplan.com/glossary/moscow-prioritization/)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 태그
`#task-planning` `#user-stories` `#backlog` `#sprint-planning` `#agile` `#project-management`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
