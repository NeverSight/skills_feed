---
name: react-refactoring
description: |
  React/TypeScript 코드 리팩토링을 위한 비판적 분석 및 실행 스킬.
  사용자가 컴포넌트 경로와 문제점을 제시하면, 각 문제점을 "수정하기 좋은 코드" 관점에서
  비판적으로 검토하고, sequential-thinking으로 단계별 분석 후 리팩토링 계획을 수립하여 실행한다.

  트리거: "리팩토링", "개선하고 싶어", "코드 구조 변경", "훅 분리", "응집도", "결합도" 등의
  키워드와 함께 React 컴포넌트 경로가 제시될 때 사용.
---

# React Refactoring Skill

사용자가 제시하는 문제점을 **무조건 수용하지 않는다**. 각 문제점에 대해 비판적으로 검토하고, 정말 문제인지, 제시된 방향이 최선인지 분석한 후 리팩토링을 수행한다.

## 핵심 원칙: 수정하기 좋은 코드

모든 판단의 기준은 **"수정하기 좋은 코드인가?"**이다. 평가 기준 상세는 [references/evaluation-criteria.md](references/evaluation-criteria.md) 참조.

## 워크플로우

### Phase 1: 현황 파악

1. 대상 컴포넌트/파일 읽기
2. 관련 의존성 파일들 파악 (imports, hooks, types)
3. 현재 코드의 구조를 간략히 정리

### Phase 2: 문제점별 비판적 분석

사용자가 제시한 문제점의 수와 복잡도에 따라 **모드를 선택**한다.

#### 모드 선택 기준

| 조건                        | 모드                   | 설명                              |
| --------------------------- | ---------------------- | --------------------------------- |
| 1-2개 단순 문제점           | Standard Mode          | 기존 sequential-thinking 3회 방식 |
| 3개 이상 또는 복잡한 문제점 | Multi-Perspective Mode | 병렬 sub-agent 3관점 분석         |

---

#### Standard Mode (1-2개 단순 문제점)

각 문제점마다 `mcp__sequential-thinking__sequentialthinking` 도구를 사용하여 사고 과정을 기록한다.

**각 문제점당 최소 3번의 thinking 루프를 수행한다.**

##### Step 2.1: 문제 정의 검증

sequential-thinking으로 다음을 분석:

```
이 문제가 정말 문제인가?
- 현재 코드가 실제로 어떤 불편/위험을 초래하는가?
- "수정하기 좋은 코드" 9가지 기준 중 어떤 것을 위반하는가?
- 위반이 없다면, 이건 취향의 문제인가 실질적 문제인가?
```

##### Step 2.2: 제안된 방향 평가

사용자가 방향을 제시했다면:

```
이 방향이 정말 개선인가?
- 제안된 변경이 "수정하기 좋은 코드" 기준을 충족하는가?
- 오히려 복잡성을 증가시키지는 않는가?
- 기존 코드베이스의 일관성을 해치지 않는가?
- 과한 추상화(Over-engineering)는 아닌가?
```

##### Step 2.3: 대안 탐색

제안된 방향이 최선이 아니라면:

```
더 나은 대안은?
- 더 단순한 해결책이 있는가?
- 점진적으로 개선할 수 있는 방법은?
- 이 문제를 해결하지 않는 것도 선택지인가?
```

---

#### Multi-Perspective Mode (3개 이상 또는 복잡한 문제점)

각 문제점에 대해 3개 관점의 Task sub-agent를 **병렬 실행**한다.

##### 에이전트 구성

| Agent                | subagent_type      | model  | 관점                                    |
| -------------------- | ------------------ | ------ | --------------------------------------- |
| Readability Advocate | general-purpose    | sonnet | 가독성, 의도의 명확성                   |
| Architecture Purist  | typescript-pro     | sonnet | 타입 안전성, 패턴 일관성, 구조적 정합성 |
| Pragmatic Developer  | frontend-developer | sonnet | 유지보수성, 실용성, 개발 경험           |

##### 실행 방법

3개의 Task sub-agent를 **단일 메시지에서 동시 실행** (`run_in_background: true`):

**Agent: Readability Advocate**

```
You are a Readability Advocate analyzing a React refactoring proposal.
Your lens: code readability, intent clarity, self-documenting code.

Read the target component at: [파일 경로]
The user's proposed issues and changes:
[문제점 목록]

For EACH issue, provide your verdict:
- Verdict: [수용/수정/기각]
- Reasoning: [Why, focused on readability impact]
- Alternative: [Better approach from readability perspective, if any]

Write your analysis. Focus on whether each change makes the code easier to READ and UNDERSTAND.
```

**Agent: Architecture Purist**

```
You are an Architecture Purist analyzing a React refactoring proposal.
Your lens: type safety, pattern consistency, structural integrity, SOLID principles.

Read the target component at: [파일 경로]
The user's proposed issues and changes:
[문제점 목록]

For EACH issue, provide your verdict:
- Verdict: [수용/수정/기각]
- Reasoning: [Why, focused on type safety and architectural patterns]
- Alternative: [Better approach from architecture perspective, if any]

Write your analysis. Focus on whether each change improves TYPE SAFETY and STRUCTURAL CONSISTENCY.
```

**Agent: Pragmatic Developer**

```
You are a Pragmatic Developer analyzing a React refactoring proposal.
Your lens: maintainability, practicality, developer experience, cost-benefit.

Read the target component at: [파일 경로]
The user's proposed issues and changes:
[문제점 목록]

For EACH issue, provide your verdict:
- Verdict: [수용/수정/기각]
- Reasoning: [Why, focused on practical maintenance impact]
- Alternative: [Better approach from practical perspective, if any]

Write your analysis. Focus on whether each change is WORTH THE EFFORT and improves MAINTAINABILITY.
```

##### 종합 규칙

3개 에이전트의 결과를 수집한 후 오케스트레이터가 종합:

| 합의 상황                 | 행동                                                                |
| ------------------------- | ------------------------------------------------------------------- |
| 3개 일치 (수용/수정/기각) | 높은 확신으로 해당 판단 채택                                        |
| 2:1 (다수:소수)           | 소수 의견의 근거를 검토 후 오케스트레이터가 최종 결정               |
| 3개 상이                  | `AskUserQuestion`으로 사용자에게 선택지와 근거를 제시하여 판단 요청 |

---

#### Step 2.4: 불명확한 점 질문 (공통)

분석 중 다음 상황이면 **반드시** `AskUserQuestion` 도구로 질문:

- 비즈니스 컨텍스트가 필요한 경우 (예: "이 컴포넌트가 여러 곳에서 재사용되나요?")
- 기존 코드의 의도가 불명확한 경우 (예: "이 훅이 이렇게 설계된 이유가 있나요?")
- 사용자의 제안과 분석 결과가 충돌하는 경우 (예: "이 방향은 오히려 복잡해질 수 있는데, 그래도 진행할까요?")
- 팀 컨벤션 확인이 필요한 경우 (예: "팀에서 네임스페이스 패턴을 사용하는 곳이 있나요?")

### Phase 3: 리팩토링 계획 수립

모든 문제점 분석 완료 후:

1. **분석 결과 요약**: 각 문제점에 대한 판단 (수용/수정/기각)
   - Multi-Perspective Mode인 경우: 각 관점의 Verdict와 최종 결정 근거 포함
2. **리팩토링 계획서 작성**:

- 변경 대상 파일 목록
- 각 변경의 목적과 기대 효과
- 변경 순서 (의존성 고려)
- 예상 위험 요소

3. **점진적 실행 계획**: 한 번에 큰 변경 대신 작은 단위로 분리

### Phase 4: 사용자 승인

계획서를 제시하고 `AskUserQuestion`으로 승인 요청:

```
리팩토링 계획을 검토해주세요.
- [수용] 문제 1: ... → 이렇게 변경
- [수정] 문제 2: ... → 제안과 다르게 이 방향으로
- [기각] 문제 3: ... → 현재 구조가 더 적절함
진행해도 될까요?
```

### Phase 5: 리팩토링 실행

승인 후 계획에 따라 코드 수정. 각 단계마다:

1. 변경 전 상태 확인
2. 변경 수행
3. 변경이 의도대로 되었는지 검증
4. 필요시 관련 테스트 확인/수정

## 주의사항

### 하지 말아야 할 것

- 사용자 제안을 무비판적으로 수용
- 분석 없이 바로 코드 수정 시작
- "일반적으로 좋은 패턴"이라는 이유만으로 변경 제안
- 한 번에 너무 많은 것을 변경

### 항상 해야 할 것

- 모든 판단에 구체적 근거 제시
- 불확실하면 질문
- 변경의 트레이드오프 명시
- 기존 코드베이스 스타일 존중

## React/TypeScript 특화 체크리스트

훅 분리 시:

- 분리 후에도 co-location이 유지되는가?
- 커스텀 훅의 반환 타입이 명확한가?
- 훅 간 의존성이 단방향인가?

컴포넌트 분리 시:

- Props drilling이 과도해지지 않는가?
- 상태 끌어올리기가 필요해지지 않는가?
- 컴포넌트 경계가 자연스러운가?

폴더 구조 변경 시:

- import 경로가 과도하게 길어지지 않는가?
- 순환 의존성이 생기지 않는가?
- 기존 구조와의 일관성은?
