---
name: iterative-code-review
description: Iteratively improve code quality by using task-planner-analyzer for planning, modular-code-architect agent to fix issues, code-reviewer agent to validate quality, and running tests to verify correctness. Use when implementing new features, after bug fixes, during refactoring, or when preparing code for production deployment. Loops until code-reviewer reports no critical issues AND tests pass.
---

# Iterative Code Review

태스크 플래너, 코드 아키텍트, 코드 리뷰어를 반복적으로 사용하고, 안정화 후 테스트를 실행하여 코드를 production-ready 수준까지 개선하는 스킬입니다.

## 사용 시점

다음과 같은 상황에서 이 스킬을 사용합니다:
- 새로운 기능 구현 후 품질 검증이 필요할 때
- 복잡한 버그 수정 후 side effect 확인이 필요할 때
- 리팩토링 후 코드 품질 검증이 필요할 때
- Production 배포 전 최종 검증이 필요할 때

## 워크플로우

### Phase 1: 초기 분석
1. 대상 파일/브랜치 식별
2. 현재 상태 파악 (git status, git diff)
3. 테스트 환경 탐지 (pytest, npm test, cargo test, go test, make test 등)
4. Todo 리스트 생성

### Phase 2: 반복 개선 루프

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────┐       │
│  │  Task Planner   │────▶│  Code Architect │────▶│   Code Reviewer     │       │
│  │  (분석 & 계획)   │     │    (수정)       │     │     (검토)          │       │
│  └─────────────────┘     └─────────────────┘     └──────────┬──────────┘       │
│           ▲                                                  │                  │
│           │                                                  ▼                  │
│           │                                       ┌─────────────────────┐       │
│           │                                       │  Critical Issues?   │       │
│           │                                       └──────────┬──────────┘       │
│           │                                                  │                  │
│           │                              Yes                 │    No            │
│           └──────────────────────────────────────────────────┤                  │
│                                                              ▼                  │
│                                               ┌─────────────────────┐           │
│                                               │  Stable? (3 loops   │           │
│                                               │  or Production Ready)│           │
│                                               └──────────┬──────────┘           │
│                                                          │                      │
│                                               No         │    Yes               │
│           ┌──────────────────────────────────────────────┤                      │
│           │                                              ▼                      │
│           │                                   ┌─────────────────────┐           │
│           │                                   │    Run Tests        │◀────────┐ │
│           │                                   │  (pytest, npm, etc) │         │ │
│           │                                   └──────────┬──────────┘         │ │
│           │                                              │                    │ │
│           │                                       Pass   │   Fail             │ │
│           │                                   ┌──────────┴──────────┐         │ │
│           │                                   ▼                     ▼         │ │
│           │                        ┌─────────────────┐   ┌─────────────────┐  │ │
│           │                        │   Complete!     │   │    Debugger     │──┘ │
│           │                        └─────────────────┘   │  (분석 & 수정)   │    │
│           │                                              └────────┬────────┘    │
│           │                                                       │             │
│           └───────────────────────────────────────────────────────┘             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Phase 3: 테스트 실행 (안정화 후)
1. 테스트 프레임워크 자동 탐지
2. 관련 테스트 실행
3. 실패 시 debugger 에이전트로 분석
4. 수정 후 다시 테스트

### Phase 4: 완료
1. 모든 변경사항 커밋
2. 브랜치 push
3. 최종 상태 보고

## 에이전트 호출 지침

### 1. task-planner-analyzer 에이전트 호출 (매 반복 시작)

각 반복 사이클의 시작 시 Task 도구로 호출:
```
Task tool 사용:
- subagent_type: "task-planner-analyzer"
- prompt:
  - 이전 code-reviewer의 피드백 (있는 경우)
  - 수정해야 할 이슈들의 목록
  - 코드베이스 구조 분석 및 제약 조건 파악 요청
  - 구체적인 수정 계획과 todo list 생성 요청
```

### 2. modular-code-architect 에이전트 호출

task-planner-analyzer의 계획에 따라 수정이 필요할 때 Task 도구로 호출:
```
Task tool 사용:
- subagent_type: "modular-code-architect"
- prompt:
  - task-planner-analyzer가 생성한 계획 포함
  - 수정해야 할 이슈들의 상세 설명
  - 파일 경로, 라인 번호, 구체적인 수정 방향 포함
```

### 3. code-reviewer 에이전트 호출

수정 후 검토할 때 Task 도구로 호출:
```
Task tool 사용:
- subagent_type: "code-reviewer"
- prompt:
  - main 브랜치와 비교 또는 특정 커밋과 비교
  - ultrathink 수준의 심층 분석 요청
  - Critical, Warning, Suggestion 구분하여 보고 요청
```

### 4. debugger 에이전트 호출 (테스트 실패 시)

테스트 실패 분석이 필요할 때 Task 도구로 호출:
```
Task tool 사용:
- subagent_type: "debugger"
- prompt:
  - 실패한 테스트 출력 전체 포함
  - 관련 파일 경로 명시
  - 에러 메시지와 스택 트레이스 포함
  - 수정 방향 제안 요청
```

## 테스트 프레임워크 탐지

다음 순서로 테스트 환경을 자동 탐지합니다:

### Python 프로젝트
```bash
# 탐지 방법
- pytest.ini, pyproject.toml, setup.cfg 확인
- tests/ 또는 test/ 디렉토리 존재 확인

# 실행 명령
pytest -v --tb=short
# 또는 특정 파일만
pytest -v path/to/test_file.py
```

### JavaScript/TypeScript 프로젝트
```bash
# 탐지 방법
- package.json의 scripts.test 확인
- jest.config.js, vitest.config.ts 확인

# 실행 명령
npm test
# 또는
yarn test
```

### Rust 프로젝트
```bash
# 탐지 방법
- Cargo.toml 확인

# 실행 명령
cargo test
```

### Go 프로젝트
```bash
# 탐지 방법
- go.mod 확인
- *_test.go 파일 존재 확인

# 실행 명령
go test ./...
```

### Makefile 기반
```bash
# 탐지 방법
- Makefile에 test 타겟 확인

# 실행 명령
make test
```

## 안정화 판단 기준

다음 조건 중 하나를 만족하면 "안정화"로 판단하고 테스트 실행:

1. **Production Ready 판정**: code-reviewer가 "production ready" 또는 "no critical issues"로 판정
2. **연속 3 라운드 무변경**: Critical 이슈 없이 3번의 리뷰 사이클 완료
3. **Warning만 남음**: Critical 이슈가 모두 해결되고 Warning/Suggestion만 남은 경우

## 반복 종료 조건

다음 조건이 **모두** 충족되면 반복을 종료합니다:

1. **Critical 이슈 없음**: code-reviewer가 Critical 이슈를 보고하지 않음
2. **테스트 통과**: 모든 관련 테스트가 통과
3. **Gradient Flow 정상**: (ML 코드의 경우) gradient가 올바르게 흐름
4. **Edge Case 처리 완료**: 모든 엣지 케이스가 처리됨

## 최대 반복 횟수

무한 루프 방지를 위해:
- **코드 리뷰 루프**: 최대 10회
- **테스트 수정 루프**: 최대 5회
- 초과 시 사용자에게 현재 상태 보고 후 수동 개입 요청

## 사용 예시

### 예시 1: 새 기능 검증
```
사용자: "이 브랜치의 코드를 iterative-code-review로 검증해줘"

Claude:
1. git diff main...HEAD로 변경사항 확인
2. 테스트 환경 탐지 (pytest 발견)
3. [반복 시작] task-planner-analyzer로 이슈 분석 및 수정 계획 수립
4. modular-code-architect로 계획에 따라 수정
5. code-reviewer로 검토
6. Critical 이슈 발견 시 → task-planner-analyzer로 돌아가서 반복 (3회)
7. Production-ready 판정 → 테스트 실행
8. pytest 실패 → debugger로 분석 → 수정
9. pytest 통과 → 완료!
```

### 예시 2: ML 모델 수정 검증
```
사용자: "/iterative-code-review models/trm_titans.py"

Claude:
1. 해당 파일 분석
2. [반복 1] task-planner-analyzer로 개선 계획 수립
3. modular-code-architect로 개선점 구현
4. code-reviewer로 검증 (gradient flow 특별 주의)
5. [반복 2-4] Critical 이슈에 대해 계획→수정→검토 반복
6. 4회 반복 후 안정화 → 테스트 실행
7. 완료 보고
```

### 예시 3: 테스트 실패 처리
```
코드 리뷰 완료 후:
1. pytest -v 실행
2. test_memory_update FAILED 발견
3. debugger 에이전트 호출:
   - 에러: "AssertionError: gradient is None"
   - 분석: create_graph=False로 인한 문제
4. task-planner-analyzer로 수정 계획 수립
5. modular-code-architect로 수정
6. pytest 재실행 → 통과
7. 완료!
```

## Best Practices

1. **Todo 리스트 활용**: TodoWrite 도구로 진행 상황 추적
2. **커밋 분리**: 각 수정 사이클마다 의미 있는 커밋 생성
3. **점진적 개선**: 한 번에 모든 것을 수정하지 않고 단계적으로 진행
4. **문서화**: 수정 이유와 결정 사항을 커밋 메시지에 기록
5. **테스트 우선**: 가능하면 수정 전 실패하는 테스트 먼저 확인

## 주의사항

- main 브랜치에 직접 머지하지 않음 (별도 지시가 없는 한)
- 파괴적 git 명령어 사용 금지 (force push, hard reset 등)
- 테스트 실행 시 전체 테스트 대신 관련 테스트만 실행 권장 (시간 절약)
- 테스트가 없는 프로젝트의 경우 code-reviewer 판정만으로 완료 가능
- ML 학습 테스트는 시간이 오래 걸릴 수 있으므로 짧은 smoke test 권장
