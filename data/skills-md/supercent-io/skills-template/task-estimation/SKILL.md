---
name: task-estimation
description: Estimate software development tasks accurately using various techniques. Use when planning sprints, roadmaps, or project timelines. Handles story points, t-shirt sizing, planning poker, and estimation best practices.
tags: [estimation, agile, sprint-planning, story-points, planning-poker]
platforms: [Claude, ChatGPT, Gemini]
---

# Task Estimation


## When to use this skill

- **Sprint Planning**: 스프린트에 포함할 작업 결정
- **Roadmap 작성**: 장기 계획 수립
- **리소스 계획**: 팀 규모 및 일정 산정

## Instructions

### Step 1: Story Points (상대적 추정)

**Fibonacci 시퀀스**: 1, 2, 3, 5, 8, 13, 21

```markdown
## Story Point 기준

### 1 Point (Very Small)
- 예: 텍스트 변경, 상수 값 수정
- 시간: 1-2시간
- 복잡도: 매우 낮음
- 리스크: 없음

### 2 Points (Small)
- 예: 간단한 버그 수정, 로그 추가
- 시간: 2-4시간
- 복잡도: 낮음
- 리스크: 낮음

### 3 Points (Medium)
- 예: 단순 CRUD API 엔드포인트
- 시간: 4-8시간
- 복잡도: 중간
- 리스크: 낮음

### 5 Points (Medium-Large)
- 예: 복잡한 폼 구현, 인증 미들웨어
- 시간: 1-2일
- 복잡도: 중간
- 리스크: 중간

### 8 Points (Large)
- 예: 새로운 피처 (프론트+백엔드)
- 시간: 2-3일
- 복잡도: 높음
- 리스크: 중간

### 13 Points (Very Large)
- 예: 결제 시스템 통합
- 시간: 1주일
- 복잡도: 매우 높음
- 리스크: 높음
- **권장**: 더 작은 태스크로 분할

### 21+ Points (Epic)
- **필수**: 반드시 더 작은 스토리로 분할
```

### Step 2: Planning Poker

**프로세스**:
1. Product Owner가 스토리 설명
2. 팀원들이 질문
3. 각자 카드 선택 (1, 2, 3, 5, 8, 13)
4. 동시에 공개
5. 최고/최저 점수 설명
6. 재투표
7. 합의 도달

**예시**:
```
Story: "사용자가 프로필 사진을 업로드할 수 있다"

팀원 A: 3 points (프론트엔드 간단)
팀원 B: 5 points (이미지 리사이징 필요)
팀원 C: 8 points (S3 업로드, 보안 고려)

토론:
- 이미지 처리 라이브러리 사용
- S3 이미 설정됨
- 파일 크기 검증 필요

재투표 → 5 points 합의
```

### Step 3: T-Shirt Sizing (빠른 추정)

```markdown
## T-Shirt 사이즈

- **XS**: 1-2 Story Points (1시간 이내)
- **S**: 2-3 Story Points (반나절)
- **M**: 5 Story Points (1-2일)
- **L**: 8 Story Points (1주일)
- **XL**: 13+ Story Points (분할 필요)

**사용 시점**:
- 초기 백로그 정리
- 대략적인 로드맵
- 빠른 우선순위 설정
```

### Step 4: 리스크 및 불확실성 고려

**추정 조정**:
```typescript
interface TaskEstimate {
  baseEstimate: number;      // 기본 추정
  risk: 'low' | 'medium' | 'high';
  uncertainty: number;        // 0-1
  finalEstimate: number;      // 조정된 추정
}

function adjustEstimate(estimate: TaskEstimate): number {
  let buffer = 1.0;

  // 리스크 버퍼
  if (estimate.risk === 'medium') buffer *= 1.3;
  if (estimate.risk === 'high') buffer *= 1.5;

  // 불확실성 버퍼
  buffer *= (1 + estimate.uncertainty);

  return Math.ceil(estimate.baseEstimate * buffer);
}

// 예시
const task = {
  baseEstimate: 5,
  risk: 'medium',
  uncertainty: 0.2  // 20% 불확실
};

const final = adjustEstimate(task);  // 5 * 1.3 * 1.2 = 7.8 → 8 points
```

## Output format

### 추정 문서 템플릿

```markdown
## Task: [Task Name]

### Description
[작업 내용 설명]

### Acceptance Criteria
- [ ] 기준 1
- [ ] 기준 2
- [ ] 기준 3

### Estimation
- **Story Points**: 5
- **T-Shirt Size**: M
- **Estimated Time**: 1-2 days

### Breakdown
- Frontend UI: 2 points
- API Endpoint: 2 points
- Testing: 1 point

### Risks
- API 응답 속도 불확실 (medium risk)
- 외부 라이브러리 의존성 (low risk)

### Dependencies
- User authentication must be completed first

### Notes
- Need to discuss design with UX team
```

## Constraints

### 필수 규칙 (MUST)

1. **상대적 추정**: 절대 시간 대신 상대적 복잡도
2. **팀 합의**: 개인이 아닌 팀 전체 합의
3. **과거 데이터 참고**: Velocity 기반 계획

### 금지 사항 (MUST NOT)

1. **개인에게 압박**: 추정은 약속이 아님
2. **너무 세밀한 추정**: 13+ points는 분할
3. **추정치를 데드라인으로**: 추정 ≠ 확약

## Best practices

1. **Break Down**: 큰 작업은 작게 분할
2. **Reference Stories**: 과거 유사 작업 참고
3. **Buffer 포함**: 예상치 못한 일 대비

## References

- [Scrum Guide](https://scrumguides.org/)
- [Planning Poker](https://www.planningpoker.com/)
- [Story Points](https://www.atlassian.com/agile/project-management/estimation)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 태그
`#estimation` `#agile` `#story-points` `#planning-poker` `#sprint-planning` `#project-management`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
