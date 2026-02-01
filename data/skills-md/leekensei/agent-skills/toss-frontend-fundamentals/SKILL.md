---
name: toss-frontend-fundamentals
description: 토스 Frontend Fundamentals 기반 코드 품질 가이드. 코드 리뷰, 새 코드 작성, 리팩토링 시 4가지 기준(가독성, 예측 가능성, 응집도, 결합도)으로 피드백 제공. 프론트엔드 코드 품질, 클린 코드, 코드 개선 요청 시 활성화.
license: MIT
metadata:
  author: toss
  version: "1.0"
  source: https://frontend-fundamentals.com
---

# Toss Frontend Fundamentals

> "좋은 프론트엔드 코드는 **변경하기 쉬운** 코드다"

## 언제 이 스킬을 사용하는가

- 프론트엔드 코드 리뷰 요청 시
- 새로운 컴포넌트/함수 작성 시
- 기존 코드 리팩토링 시
- "코드 품질", "클린 코드", "개선" 관련 요청 시

## 4가지 핵심 기준

| 기준 | 설명 | 영향도 |
|------|------|--------|
| **가독성** | 코드를 얼마나 빠르게 이해할 수 있는가 | CRITICAL |
| **예측 가능성** | 함수/컴포넌트가 예상대로 동작하는가 | HIGH |
| **응집도** | 함께 수정될 코드가 함께 있는가 | HIGH |
| **결합도** | 코드 수정 시 영향 범위가 적절한가 | MEDIUM |

## 규칙 목록

### 가독성 (Readability) - 8개 규칙

**맥락 줄이기**
| 규칙 ID | 규칙 | 상세 |
|---------|------|------|
| `readability-context-separate-code-paths` | 같이 실행되지 않는 코드 분리하기 | [상세](rules/readability-context-separate-code-paths.md) |
| `readability-context-abstract-implementation` | 구현 상세 추상화하기 | [상세](rules/readability-context-abstract-implementation.md) |
| `readability-context-split-by-logic-type` | 로직 종류에 따라 함수 쪼개기 | [상세](rules/readability-context-split-by-logic-type.md) |

**이름 붙이기**
| 규칙 ID | 규칙 | 상세 |
|---------|------|------|
| `readability-naming-complex-conditions` | 복잡한 조건에 이름 붙이기 | [상세](rules/readability-naming-complex-conditions.md) |
| `readability-naming-magic-numbers` | 매직 넘버에 이름 붙이기 | [상세](rules/readability-naming-magic-numbers.md) |

**위에서 아래로 읽히게 하기**
| 규칙 ID | 규칙 | 상세 |
|---------|------|------|
| `readability-flow-reduce-time-travel` | 시점 이동 줄이기 | [상세](rules/readability-flow-reduce-time-travel.md) |
| `readability-flow-simplify-ternary` | 삼항 연산자 단순하게 하기 | [상세](rules/readability-flow-simplify-ternary.md) |
| `readability-flow-left-to-right` | 왼쪽에서 오른쪽으로 읽히게 하기 | [상세](rules/readability-flow-left-to-right.md) |

### 예측 가능성 (Predictability) - 3개 규칙

| 규칙 ID | 규칙 | 상세 |
|---------|------|------|
| `predictability-unique-names` | 이름 겹치지 않게 관리하기 | [상세](rules/predictability-unique-names.md) |
| `predictability-consistent-return-types` | 같은 종류의 함수는 반환 타입 통일하기 | [상세](rules/predictability-consistent-return-types.md) |
| `predictability-expose-hidden-logic` | 숨은 로직 드러내기 | [상세](rules/predictability-expose-hidden-logic.md) |

### 응집도 (Cohesion) - 3개 규칙

| 규칙 ID | 규칙 | 상세 |
|---------|------|------|
| `cohesion-colocate-modified-files` | 함께 수정되는 파일을 같은 디렉토리에 두기 | [상세](rules/cohesion-colocate-modified-files.md) |
| `cohesion-eliminate-magic-numbers` | 매직 넘버 없애기 | [상세](rules/cohesion-eliminate-magic-numbers.md) |
| `cohesion-form-structure` | 폼의 응집도 생각하기 | [상세](rules/cohesion-form-structure.md) |

### 결합도 (Coupling) - 3개 규칙

| 규칙 ID | 규칙 | 상세 |
|---------|------|------|
| `coupling-single-responsibility` | 책임을 하나씩 관리하기 | [상세](rules/coupling-single-responsibility.md) |
| `coupling-allow-duplication` | 중복 코드 허용하기 | [상세](rules/coupling-allow-duplication.md) |
| `coupling-eliminate-props-drilling` | Props Drilling 지우기 | [상세](rules/coupling-eliminate-props-drilling.md) |

## 사용 방법

### 코드 리뷰 시

1. 위 4가지 기준 순서대로 검토
2. 위반 사항 발견 시 해당 규칙 파일 참조하여 구체적 피드백 제공
3. 개선 코드 예시 함께 제시

### 새 코드 작성 시

1. 가독성 우선: 맥락 최소화, 명확한 이름
2. 예측 가능하게: 일관된 패턴 사용
3. 응집도 고려: 관련 코드 함께 배치
4. 결합도 낮추기: 책임 분리

### 트레이드오프

4가지 기준을 모두 만족하기 어려울 때는 [트레이드오프 가이드](references/TRADEOFFS.md) 참조.

일반적인 우선순위: **가독성 > 예측 가능성 > 응집도 > 결합도**

## 참고

- [Toss Frontend Fundamentals](https://frontend-fundamentals.com)
- [GitHub Repository](https://github.com/toss/frontend-fundamentals)
