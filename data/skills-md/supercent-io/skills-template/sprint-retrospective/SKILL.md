---
name: sprint-retrospective
description: Facilitate effective sprint retrospectives for continuous team improvement. Use when conducting team retrospectives, identifying improvements, or fostering team collaboration. Handles retrospective formats, action items, and facilitation techniques.
tags: [retrospective, agile, scrum, team-improvement, facilitation]
platforms: [Claude, ChatGPT, Gemini]
---

# Sprint Retrospective


## When to use this skill

- **스프린트 종료**: 매 스프린트 마지막
- **프로젝트 마일스톤**: 주요 릴리스 후
- **팀 문제 발생**: 즉시 회고 필요 시

## Instructions

### Step 1: Start-Stop-Continue

```markdown
## Retrospective Template: Start-Stop-Continue

### START (시작할 것)
- Daily standup을 더 짧게 (5분 이내)
- Code review 체크리스트 사용
- 페어 프로그래밍 도입

### STOP (중단할 것)
- 금요일 오후 배포 (롤백 위험)
- 긴급 회의 남발
- 문서화 없는 기능 추가

### CONTINUE (계속할 것)
- 주간 기술 공유 세션
- 자동화된 테스트
- 투명한 커뮤니케이션

### Action Items
1. [ ] Standup 시간을 9:00 → 9:30으로 변경 (팀장)
2. [ ] Code review checklist 문서 작성 (개발자 A)
3. [ ] 금요일 배포 금지 규칙 공지 (팀장)
```

### Step 2: Mad-Sad-Glad

```markdown
## Retrospective: Mad-Sad-Glad

### MAD (화가 났던 것)
- 배포 후 긴급 버그 발생 (2번)
- 요구사항이 자주 변경됨
- 테스트 환경 불안정

### SAD (아쉬웠던 것)
- 코드 리뷰 시간 부족
- 문서화가 뒤처짐
- 기술 부채 누적

### GLAD (좋았던 것)
- 새 팀원 빠른 적응
- CI/CD 파이프라인 안정화
- 고객 피드백 긍정적

### Action Items
- 배포 체크리스트 강화
- 요구사항 변경 프로세스 개선
- 매주 금요일 문서화 시간 확보
```

### Step 3: 4Ls (Liked-Learned-Lacked-Longed For)

```markdown
## Retrospective: 4Ls

### LIKED (좋았던 것)
- 팀워크가 좋았음
- 새로운 기술 스택 도입 성공

### LEARNED (배운 것)
- Docker Compose로 로컬 환경 통일
- React Query로 서버 상태 관리 개선

### LACKED (부족했던 것)
- 성능 테스트
- 모바일 대응

### LONGED FOR (바라는 것)
- 더 나은 개발 도구
- 외부 교육 기회

### Action Items
- Lighthouse CI 도입으로 성능 자동 측정
- 반응형 디자인 가이드라인 작성
```

## Output format

### Retrospective 문서

```markdown
# Sprint [N] Retrospective
**Date**: 2025-01-15
**Participants**: 팀원 A, B, C, D
**Format**: Start-Stop-Continue

## What Went Well
- 모든 스토리 완료 (Velocity: 25 points)
- 버그 발생 0건
- 팀 분위기 좋음

## What Didn't Go Well
- 기술 스파이크에 예상보다 시간 소요
- 디자인 변경으로 재작업

## Action Items
1. [ ] 기술 스파이크는 별도 스프린트 할당 (팀장, ~01/20)
2. [ ] 디자인 사전 리뷰 프로세스 도입 (디자이너, ~01/18)
3. [ ] Velocity 차트 공유 (스크럼 마스터, 매주)

## Key Metrics
- Velocity: 25 points
- Bugs Found: 0
- Sprint Goal Achievement: 100%
```

## Constraints

### 필수 규칙 (MUST)

1. **Safe Space**: 비난 없는 환경
2. **Action Items**: 구체적이고 실행 가능해야 함
3. **Follow-up**: 다음 회고에서 진행 상황 확인

### 금지 사항 (MUST NOT)

1. **개인 공격**: 사람이 아닌 프로세스 개선
2. **너무 많은 Action**: 2-3개로 제한

## Best practices

1. **Time-box**: 1시간 이내
2. **Rotate Facilitator**: 팀원이 돌아가며 진행
3. **Celebrate Wins**: 성공도 함께 축하

## References

- [Retrospective Formats](https://retromat.org/)
- [Agile Retrospectives](https://www.amazon.com/Agile-Retrospectives-Making-Teams-Great/dp/0977616649)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 태그
`#retrospective` `#agile` `#scrum` `#team-improvement` `#project-management`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
