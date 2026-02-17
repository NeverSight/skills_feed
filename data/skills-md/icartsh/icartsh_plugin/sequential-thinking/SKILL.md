---
name: sequential-thinking
description: 다단계 분석, 수정 능력 및 가설 검증이 필요한 복잡한 작업을 위해 구조화되고 성찰적인 문제 해결 방식을 적용합니다. 복잡한 문제 분해, 적응형 계획 수립, 경로 수정이 필요한 분석, 범위가 불분명한 문제, 다단계 해결책 및 가설 기반 작업 시 사용합니다.
version: 1.0.0
license: MIT
---

# Sequential Thinking

역동적인 조정을 동반한 관리 가능하고 성찰적인 사고 시퀀스를 통해 구조화된 문제 해결을 수행합니다.

## 적용 시기

- 복잡한 문제의 분해
- 수정을 포함한 적응형 계획 수립
- 경로 수정(course correction)이 필요한 분석
- 범위가 불분명하거나 새로 형성되는 문제
- 컨텍스트 유지가 필요한 다단계 해결책
- 가설 기반의 조사/디버깅

## 핵심 프로세스 (Core Process)

### 1. 개략적인 추정으로 시작
```
Thought 1/5: [초기 분석]
```
이해도가 높아짐에 따라 역동적으로 조정하세요.

### 2. 각 사고의 구조화
- 이전 컨텍스트를 명시적으로 기반으로 삼음
- 사고당 하나의 측면만 다룸
- 가정, 불확실성, 깨달은 점을 명시
- 다음 사고에서 다루어야 할 내용 예고

### 3. 역동적인 조정 (Dynamic Adjustment) 적용
- **확장 (Expand)**: 더 많은 복잡성 발견 → 총 사고 횟수 증가
- **축소 (Contract)**: 예상보다 단순함 → 총 사고 횟수 감소
- **수정 (Revise)**: 새로운 통찰이 이전을 무효화함 → 수정 마킹
- **분기 (Branch)**: 여러 접근 방식 존재 → 대안 탐색

### 4. 필요시 수정(Revision) 사용
```
Thought 5/8 [Thought 2의 REVISION]: [수정된 이해]
- 이전 내용: [언급되었던 내용]
- 수정 이유: [새로운 통찰]
- 영향: [변경되는 사항]
```

### 5. 대안을 위한 분기 (Branching)
```
Thought 4/7 [Thought 2에서 시작된 BRANCH A]: [접근 방식 A]
Thought 4/7 [Thought 2에서 시작된 BRANCH B]: [접근 방식 B]
```
명시적으로 비교하고, 결정 근거와 함께 수렴(converge)시키세요.

### 6. 가설 생성 및 검증
```
Thought 6/9 [HYPOTHESIS]: [제안된 해결책]
Thought 7/9 [VERIFICATION]: [테스트 결과]
```
가설이 검증될 때까지 반복하세요.

### 7. 준비가 되었을 때만 완료
최종 마킹: `Thought N/N [FINAL]`

완료 조건:
- 해결책 검증 완료
- 모든 핵심 측면 처리 완료
- 확신(Confidence) 확보
- 해결되지 않은 불확실성 없음

## 적용 모드 (Application Modes)

**Explicit (명시적)**: 복잡성이 가시적인 추론을 정당화하거나 사용자가 분석을 요청할 때 가시적인 사고 마커를 사용합니다.

**Implicit (암묵적)**: 응답을 복잡하게 만들지 않으면서 정확도를 높이기 위해 일상적인 문제 해결 시 내부적으로 방법론을 적용합니다.

## 스크립트 (선택 사항)

결정론적 검증/추적을 위한 선택적 스크립트:
- `scripts/process-thought.js` - 히스토리와 함께 사고를 검증하고 추적
- `scripts/format-thought.js` - 표시용 포맷팅 (박스/마크다운/단순형)

사용 예시는 README.md를 참조하세요. 검증이나 로그 보존이 필요할 때 사용하며, 그렇지 않으면 방법론을 직접 적용합니다.

## 참조 문서 (References)

더 깊은 이해가 필요할 때 로드하세요:
- `references/core-patterns.md` - 수정 및 분기 패턴
- `references/examples-api.md` - API 설계 예시
- `references/examples-debug.md` - 디버깅 예시
- `references/examples-architecture.md` - 아키텍처 결정 예시
- `references/advanced-techniques.md` - 나선형 정밀화(spiral refinement), 가설 테스트, 수렴
- `references/advanced-strategies.md` - 불확실성, 수정 케스케이드(revision cascades), 메타 사고(meta-thinking)
