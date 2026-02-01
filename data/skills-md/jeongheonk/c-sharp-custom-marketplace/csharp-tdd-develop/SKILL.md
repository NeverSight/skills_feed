---
name: csharp-tdd-develop
description: TDD 기반 C#/.NET 개발. 테스트 먼저 작성 후 구현. Red-Green-Refactor 순서 강제. csharp-expert agent에 위임.
user-invocable: true
context: current
model: opus
argument-hint: "<class-description>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# C# TDD Develop

TDD(Test-Driven Development) 워크플로우 조율 스킬. 순서를 강제하고, 실제 작업은 `csharp-expert` agent에 위임.

## Overview

이 스킬은 워크플로우 **조율**에 집중합니다:

```
┌─────────────────────────────────────────────────────────────┐
│  csharp-tdd-develop (Orchestrator)                          │
│  ├── Phase 0: 환경 감지 ──── scripts/test-detector.js       │
│  └── Phase 1: 분석 ───────── 요구사항 → 테스트 시나리오     │
├─────────────────────────────────────────────────────────────┤
│  csharp-expert agent (Executor)                             │
│  ├── Phase 2 RED ─────────── 테스트 작성 + dotnet test 실패 │
│  ├── Phase 3 GREEN ───────── 최소 구현 + dotnet test 통과   │
│  └── Phase 4 REFACTOR ────── 코드 정리 + 회귀 방지         │
│                                                             │
│  ※ csharp-best-practices 규칙 자동 적용                    │
│  ※ csharp-test-develop 테스트 패턴 참조                    │
└─────────────────────────────────────────────────────────────┘
```

## 강제 규칙

| 규칙 | 설명 | 위반 시 |
|------|------|---------|
| 환경 확인 | .csproj에서 테스트 환경 감지 | 미설치 시 안내 |
| 테스트 먼저 | 구현 코드 작성 전 테스트 코드 필수 | 중단 |
| Red 확인 | 테스트가 실패해야 다음 단계 진행 | 중단 |
| Green 확인 | 테스트 통과해야 리팩토링 진행 | 반복 |
| Refactor 검증 | 리팩토링 후 테스트 재실행 | 롤백 |

---

## Workflow

### Phase 0: 환경 확인

.csproj 파일에서 테스트 환경 자동 감지.

```bash
node skills/csharp-tdd-develop/scripts/test-detector.js --detect
```

**정상:**
```
## Test Environment
Runner: xUnit ✓
FluentAssertions: YES ✓
Moq: YES ✓
Test Command: dotnet test
```

**미설치 시:**
```
## Missing Dependencies
  dotnet add package xunit
  dotnet add package xunit.runner.visualstudio
  dotnet add package Microsoft.NET.Test.Sdk
```
→ 설치 안내 후 중단

---

### Phase 1: 분석

요구사항을 테스트 시나리오로 변환.

**동작:**
1. 사용자 요구사항 파악
2. 클래스/서비스 구조 설계
3. 테스트 시나리오 3-5개 도출
4. 테스트 파일 경로 결정

**Output:**
```markdown
## 분석 결과

### 대상 클래스
- 이름: UserService
- 경로: src/Services/UserService.cs
- 타입: Business Service

### 테스트 시나리오
1. GetByIdAsync — 유효한 ID로 사용자 반환
2. GetByIdAsync — 존재하지 않는 ID로 null 반환
3. CreateAsync — 유효한 데이터로 사용자 생성
4. CreateAsync — 중복 이메일로 예외 발생

### 테스트 파일
- 경로: tests/UnitTests/Services/UserServiceTests.cs
```

---

### Phase 2: RED (csharp-expert 위임)

**Task tool로 위임:**
```
Task({
  subagent_type: "csharp-expert",
  prompt: `
TDD RED 단계를 수행하세요.

## 대상 클래스
- 이름: UserService
- 경로: src/Services/UserService.cs

## 테스트 시나리오
1. GetByIdAsync — 유효한 ID로 사용자 반환
2. GetByIdAsync — 존재하지 않는 ID로 null 반환
3. CreateAsync — 유효한 데이터로 사용자 생성
4. CreateAsync — 중복 이메일로 예외 발생

## 지침
1. 테스트 파일 생성: tests/UnitTests/Services/UserServiceTests.cs
2. 위 시나리오에 대한 테스트 케이스 작성
3. csharp-test-develop 테스트 패턴 적용 (AAA 패턴, Method_Scenario_ExpectedBehavior 네이밍)
4. 테스트 실행하여 **실패 확인** (dotnet test)
5. 테스트 결과 리포트

## 중요
- 구현 코드 작성 금지 (GREEN 단계에서 수행)
- 테스트가 반드시 실패해야 함
`
})
```

**검증 (csharp-tdd-develop):**
- agent 응답에서 테스트 실패 확인
- 통과하면 중단: "테스트가 이미 통과합니다. 시나리오를 검토하세요."

---

### Phase 3: GREEN (csharp-expert 위임)

**Task tool로 위임:**
```
Task({
  subagent_type: "csharp-expert",
  prompt: `
TDD GREEN 단계를 수행하세요.

## 대상 클래스
- 이름: UserService
- 경로: src/Services/UserService.cs
- 테스트 파일: tests/UnitTests/Services/UserServiceTests.cs

## 지침
1. 테스트를 통과하는 **최소한의** 구현
2. Over-engineering 금지 (추가 기능, 최적화는 REFACTOR에서)
3. 테스트 실행하여 **통과 확인** (dotnet test)
4. 테스트 결과 리포트

## 중요
- 테스트 파일 수정 금지
- 불필요한 추상화 금지
`
})
```

**검증 (csharp-tdd-develop):**
- agent 응답에서 테스트 통과 확인
- 실패하면 재시도 요청 (최대 3회)

---

### Phase 4: REFACTOR (csharp-expert 위임)

**Task tool로 위임:**
```
Task({
  subagent_type: "csharp-expert",
  prompt: `
TDD REFACTOR 단계를 수행하세요.

## 대상 파일
- 구현: src/Services/UserService.cs
- 테스트: tests/UnitTests/Services/UserServiceTests.cs

## 체크리스트
- [ ] SOLID 원칙 적용
- [ ] Modern C# 12 기능 활용
- [ ] 중복 코드 제거
- [ ] 네이밍 개선

## 지침
1. 코드 가독성 개선
2. csharp-best-practices 규칙 적용
3. 테스트 재실행하여 **회귀 없음 확인** (dotnet test)
4. 개선 사항 + 테스트 결과 리포트

## 중요
- 테스트가 실패하면 변경 사항 롤백
`
})
```

**검증 (csharp-tdd-develop):**
- agent 응답에서 테스트 통과 확인
- 실패하면 롤백 요청

---

## 현재 전달받은 인자

**ARGUMENTS**: $ARGUMENTS

## 실행 지시

위 ARGUMENTS가 구현할 클래스/기능 설명입니다. 이 설명을 기반으로 TDD 워크플로우를 시작하세요.

**ARGUMENTS가 비어있으면** 사용자에게 구현할 클래스/기능을 질문하세요.

**호출 예시:**
- `/csharp-tdd-develop UserService` → ARGUMENTS = "UserService"
- `/csharp-tdd-develop 주문 처리 서비스` → ARGUMENTS = "주문 처리 서비스"

---

## 실행 예시

### 요청
"TDD로 UserService 만들어줘"

### 실행 흐름

```markdown
## Phase 0: 환경 확인
Runner: xUnit ✓ | FluentAssertions: YES ✓ | Moq: YES ✓

---

## Phase 1: 분석
- 클래스: UserService (Business Service)
- 시나리오 4개 도출

---

## Phase 2: RED
→ csharp-expert agent 호출
← 테스트 파일 생성, 실패 확인됨 ❌

---

## Phase 3: GREEN
→ csharp-expert agent 호출
← 서비스 구현, 테스트 통과 ✅

---

## Phase 4: REFACTOR
→ csharp-expert agent 호출
← 코드 정리 완료, 테스트 유지 ✅

---

## TDD 사이클 완료!
- src/Services/UserService.cs
- tests/UnitTests/Services/UserServiceTests.cs
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
| RED에서 테스트 통과 | 중단 + 시나리오 검토 요청 |
| GREEN에서 계속 실패 | 최대 3회 재시도 후 사용자에게 도움 요청 |
| REFACTOR에서 실패 | 롤백 요청 |

---

## 위임 구조

```
csharp-tdd-develop (Orchestrator)
    │
    └── csharp-expert agent
            │
            └── skills:
                  ├── csharp-best-practices ← 12개 규칙 자동 적용
                  │     ├── rules/cs12-primary-constructor.md
                  │     ├── rules/cs12-collection-expression.md
                  │     └── ...
                  └── csharp-test-develop ← 테스트 패턴 참조
                        └── references/csharp-test-patterns.md
```

---

## Resources

### scripts/
- `test-detector.js`: .csproj 기반 테스트 환경 감지
  - `--detect`: 테스트 환경만 확인
