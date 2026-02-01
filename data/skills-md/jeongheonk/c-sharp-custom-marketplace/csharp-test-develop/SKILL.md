---
name: csharp-test-develop
description: C#/.NET 테스트 코드 작성. 기존 코드에 대한 단위/통합 테스트를 xUnit, Moq, FluentAssertions 기반으로 생성. csharp-expert agent에 위임.
user-invocable: true
context: current
model: opus
argument-hint: "<class-or-file-path>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# C# Test Develop

기존 C# 코드에 대한 테스트 코드를 작성하는 스킬. TDD 워크플로우 없이 구현된 코드를 분석하고 테스트를 생성합니다.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│  csharp-test-develop (Orchestrator)                         │
│  ├── Phase 0: 환경 감지 ──── test-detector.js 재사용        │
│  ├── Phase 1: 분석 ───────── 대상 코드 → 테스트 시나리오   │
│  └── Phase 2: 검증 ───────── dotnet test 통과 확인          │
├─────────────────────────────────────────────────────────────┤
│  csharp-expert agent (Executor)                             │
│  └── 테스트 코드 작성 ────── references/csharp-test-patterns│
│                                                             │
│  ※ csharp-best-practices 규칙 자동 적용                    │
└─────────────────────────────────────────────────────────────┘
```

## csharp-tdd-develop과의 차이

| 구분 | csharp-tdd-develop | csharp-test-develop |
|------|-------------------|---------------------|
| 목적 | 새 기능 TDD 개발 | 기존 코드에 테스트 추가 |
| 워크플로우 | Red-Green-Refactor | 분석 → 테스트 작성 → 검증 |
| 구현 코드 | 테스트 후 작성 | 이미 존재 |
| 시점 | 개발 시작 | 개발 후 / 레거시 코드 |

---

## Workflow

### Phase 0: 환경 확인

.csproj 파일에서 테스트 환경 자동 감지.

```bash
node skills/csharp-tdd-develop/scripts/test-detector.js --detect
```

미설치 시 필요한 패키지 안내 후 중단.

---

### Phase 1: 분석

대상 코드를 읽고 테스트 시나리오를 도출합니다.

**동작:**
1. 대상 파일/클래스 읽기
2. public 메서드 목록 추출
3. 의존성 분석 (DI 인터페이스)
4. 테스트 시나리오 도출 (정상/예외/엣지 케이스)
5. 테스트 파일 경로 결정

**Output:**
```markdown
## 분석 결과

### 대상 클래스
- 이름: OrderService
- 경로: src/Services/OrderService.cs
- 의존성: IOrderRepository, IPaymentGateway, ILogger<OrderService>

### 테스트 시나리오
1. CreateOrderAsync — 유효한 주문 생성 성공
2. CreateOrderAsync — 재고 부족 시 예외 발생
3. CreateOrderAsync — 결제 실패 시 롤백
4. GetOrderByIdAsync — 존재하는 주문 반환
5. GetOrderByIdAsync — 존재하지 않는 주문 null 반환
6. CancelOrderAsync — 이미 취소된 주문 예외

### 테스트 파일
- 경로: tests/UnitTests/Services/OrderServiceTests.cs
```

---

### Phase 2: 테스트 작성 (csharp-expert 위임)

**Task tool로 위임:**
```
Task({
  subagent_type: "csharp-expert",
  prompt: `
기존 코드에 대한 단위 테스트를 작성하세요.

## 대상
- 클래스: OrderService
- 경로: src/Services/OrderService.cs
- 테스트 파일: tests/UnitTests/Services/OrderServiceTests.cs

## 테스트 시나리오
1. CreateOrderAsync — 유효한 주문 생성 성공
2. CreateOrderAsync — 재고 부족 시 예외 발생
...

## 테스트 패턴 (필수 적용)
- AAA Pattern (Arrange-Act-Assert)
- 네이밍: Method_Scenario_ExpectedBehavior
- Moq로 의존성 Mock
- FluentAssertions 사용 (설치된 경우)
- xUnit Theory/InlineData (매개변수화 테스트)

## 지침
1. references/csharp-test-patterns.md 패턴 적용
2. 테스트 실행하여 **통과 확인** (dotnet test)
3. 테스트 결과 리포트
`
})
```

---

### Phase 3: 검증

- agent 응답에서 테스트 통과 확인
- 실패 시 수정 요청 (최대 3회)
- 커버리지 리포트 출력 (coverlet 설치 시)

---

## 현재 전달받은 인자

**ARGUMENTS**: $ARGUMENTS

## 실행 지시

위 ARGUMENTS가 테스트를 작성할 대상 클래스/파일 설명입니다.

**ARGUMENTS가 비어있으면** 사용자에게 테스트 대상을 질문하세요.

**호출 예시:**
- `/csharp-test-develop src/Services/UserService.cs` → 해당 파일 테스트 작성
- `/csharp-test-develop OrderService` → OrderService 클래스 찾아서 테스트 작성

---

## 실행 예시

### 요청
"OrderService에 대한 단위 테스트 작성해줘"

### 실행 흐름

```markdown
## Phase 0: 환경 확인
Runner: xUnit ✓ | FluentAssertions: YES ✓ | Moq: YES ✓

---

## Phase 1: 분석
- 클래스: OrderService
- public 메서드 3개
- 의존성 3개 (모두 인터페이스)
- 시나리오 6개 도출

---

## Phase 2: 테스트 작성
→ csharp-expert agent 호출
← 테스트 파일 생성, 모든 테스트 통과 ✅

---

## 완료!
- tests/UnitTests/Services/OrderServiceTests.cs (6 tests)
```

---

## 테스트 파일 경로 규칙

| 소스 위치 | 테스트 위치 |
|-----------|------------|
| `src/Services/UserService.cs` | `tests/UnitTests/Services/UserServiceTests.cs` |
| `src/ViewModels/MainViewModel.cs` | `tests/UnitTests/ViewModels/MainViewModelTests.cs` |
| `src/Repositories/UserRepository.cs` | `tests/IntegrationTests/Repositories/UserRepositoryTests.cs` |

---

## Error Handling

| 상황 | 처리 |
|------|------|
| 테스트 러너 미설치 | 설치 명령어 출력 후 중단 |
| 대상 파일 미발견 | 사용자에게 경로 확인 요청 |
| 테스트 실패 | 최대 3회 수정 시도 후 사용자에게 도움 요청 |

---

## 위임 구조

```
csharp-test-develop (Orchestrator)
    │
    └── csharp-expert agent
            │
            └── skills:
                  ├── csharp-best-practices ← C# 12 규칙 적용
                  └── references/
                        └── csharp-test-patterns.md ← 테스트 패턴 참조
```

---

## Resources

### references/
- `csharp-test-patterns.md`: C# 테스트 패턴 가이드 (AAA, Moq, FluentAssertions 등)
