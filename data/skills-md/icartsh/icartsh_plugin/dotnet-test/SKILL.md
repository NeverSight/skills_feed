---
name: dotnet-test
version: 0.1.0
kind: cli
description: dotnet CLI를 사용하여 .NET 테스트를 실행합니다. 유닛 테스트 실행, 코드 커버리지 리포트 생성 또는 벤치마크 수행 시 사용합니다.
inputs:
  target: [all, project, specific]
  configuration: [Debug, Release]
  coverage: ['true', 'false']
  project_path: string
contracts:
  success: '테스트 통과 (실패 없음); 요청 시 커버리지 데이터 생성 완료'
  failure: '0이 아닌 종료 코드, 테스트 실패 또는 커버리지 생성 에러 발생'
---

# .NET Test Skill (Entry Map)

> **목표:** 정확한 테스트 절차를 안내합니다.

## 빠른 시작 (택일)

- **유닛 테스트 실행** → `references/run-unit-tests.md`
- **커버리지 리포트 생성** → `references/generate-coverage.md`
- **벤치마크 실행** → `references/run-benchmarks.md`

## 사용 시기

- 유닛 테스트 실행 (xUnit, NUnit)
- coverlet을 이용한 코드 커버리지 리포트 생성
- BenchmarkDotNet을 이용한 성능 벤치마크 수행
- 테스트 스위트를 통한 코드 변경 사항 검증
- 테스트 실행 시간 측정

**다음의 경우에는 사용하지 마세요:** 코드 빌드 (dotnet-build), 포맷팅 (code-format), 또는 정적 분석 (code-analyze)

## 입력 및 출력 (Inputs & Outputs)

**입력:** `target` (all/project/specific), `configuration` (Debug/Release), `coverage` (true/false), `project_path` (기본값: 모든 테스트 프로젝트)

**출력:** 테스트 결과 (성공/실패 카운트), 커버리지 리포트 (요청 시), 벤치마크 결과, 종료 코드 (0=성공)

**가드레일:** ./dotnet 디렉토리 내에서만 작업하며, 실패 사항을 명확히 보고하고, 허가 없이 테스트를 건너뛰지 않습니다.

## 탐색 (Navigation)

**1. 유닛 테스트 실행** → [`references/run-unit-tests.md`](references/run-unit-tests.md)

- 모든 테스트 실행, 특정 프로젝트 테스트 실행, 테스트 실패 트러블슈팅

**2. 커버리지 리포트 생성** → [`references/generate-coverage.md`](references/generate-coverage.md)

- 커버리지 데이터 수집, 리포트 생성 (HTML/Cobertura), 커버리지 지표 분석

**3. 벤치마크 실행** → [`references/run-benchmarks.md`](references/run-benchmarks.md)

- 성능 벤치마크 수행, 결과 비교, 데이터 기반 최적화

## 일반적인 패턴 (Common Patterns)

### 모든 테스트 실행 (빠른 속도)

```bash
cd ./dotnet
dotnet test
```

### 상세 출력을 포함한 테스트 실행

```bash
cd ./dotnet
dotnet test --verbosity normal
```

### 특정 테스트 프로젝트 실행

```bash
cd ./dotnet
dotnet test console-app.Tests/PigeonPea.Console.Tests.csproj
```

### 커버리지와 함께 테스트 실행

```bash
cd ./dotnet
dotnet test --collect:"XPlat Code Coverage"
```

### 테스트 실행 및 커버리지 리포트 생성

```bash
cd ./dotnet
dotnet test --collect:"XPlat Code Coverage" --results-directory ./TestResults
# 커버리지 파일: ./TestResults/{guid}/coverage.cobertura.xml
```

### 이름으로 테스트 필터링

```bash
cd ./dotnet
dotnet test --filter "FullyQualifiedName~FrameTests"
```

### 카테고리로 테스트 필터링

```bash
cd ./dotnet
dotnet test --filter "Category=Unit"
```

### Release 구정으로 테스트 실행

```bash
cd ./dotnet
dotnet test --configuration Release
```

### 벤치마크 실행

```bash
cd ./dotnet/benchmarks
dotnet run -c Release
```

## 트러블슈팅 (Troubleshooting)

**테스트 실패:** Assertion 실패에 대한 테스트 출력을 확인하세요. 디버깅은 `references/run-unit-tests.md`를 참조하세요.

**커버리지 미생성:** coverlet.collector가 설치되어 있는지 확인하세요. `references/generate-coverage.md`를 참조하세요.

**벤치마크 실행 실패:** Release 구성을 사용해야 합니다. `references/run-benchmarks.md`를 참조하세요.

**테스트 실행 속도 저하:** 테스트 필터 사용, 병렬 실행 또는 빌드 후 `--no-build` 옵션을 사용하세요.

**테스트 발견 실패:** 프로젝트 참조를 확인하고 테스트 프레임워크 패키지가 설치되어 있는지 확인하세요.

## 성공 지표 (Success Indicators)

```
Passed!  - Failed:     0, Passed:    42, Skipped:     0, Total:    42
```

테스트 아티팩트 위치: `./dotnet/TestResults/`

커버리지 리포트 위치: `./dotnet/TestResults/coverage.cobertura.xml`

## 통합 (Integration)

**테스트 전:** dotnet-build (코드가 빌드되었는지 확인)
**테스트 후:** code-analyze (정적 분석), code-review (품질 검사)

## 테스트 프레임워크

이 저장소는 다음을 사용합니다:

- 유닛 테스트를 위한 **xUnit** (console-app.Tests, shared-app.Tests, windows-app.Tests)
- 코드 커버리지를 위한 **coverlet.collector**
- 성능 벤치마크를 위한 **BenchmarkDotNet**

## 관련 링크 (Related)

- [`./dotnet/README.md`](../../../dotnet/README.md) - 프로젝트 구조
- [`./dotnet/ARCHITECTURE.md`](../../../dotnet/ARCHITECTURE.md) - 아키텍처
- [`.pre-commit-config.yaml`](../../../.pre-commit-config.yaml) - Pre-commit hooks
- [`dotnet-build` skill](../dotnet-build/SKILL.md) - 빌드 스킬
