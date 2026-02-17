---
name: dotnet-build
version: 0.2.0
kind: cli
description: dotnet CLI를 사용하여 .NET 솔루션/프로젝트를 빌드합니다. 컴파일, 종속성 복원 또는 아티팩트 빌드 작업 시 사용합니다.
inputs:
  target: [solution, project, all]
  configuration: [Debug, Release]
  project_path: string
contracts:
  success: '에러 없이 빌드 완료; bin/ 디렉토리에 아티팩트 생성'
  failure: '0이 아닌 종료 코드 또는 컴파일 에러 발생'
---

# .NET Build Skill (Entry Map)

> **목표:** 정확한 빌드 절차를 안내합니다.

## 빠른 시작 (택일)

- **전체 솔루션 빌드** → `references/build-solution.md`
- **종속성만 복원** → `references/restore-deps.md`

## 사용 시기

- .NET 코드 컴파일 (`.csproj`, `.sln` 파일)
- NuGet 패키지 및 종속성 복원
- Debug/Release 구성 빌드
- 빌드 아티팩트(바이너리, 어셈블리) 생성

**다음의 경우에는 사용하지 마세요:** 테스트 (dotnet-test), 포맷팅 (code-format), 또는 분석 (code-analyze)

## 입력 및 출력 (Inputs & Outputs)

**입력:** `target` (solution/project/all), `configuration` (Debug/Release), `project_path` (기본값: ./dotnet/PigeonPea.sln)

**출력:** `artifact_path` (bin/ 디렉토리), `build_log`, 종료 코드 (0=성공)

**가드레일:** ./dotnet 디렉토리 내에서만 작업하며, bin/obj/ 디렉토리는 커밋하지 않습니다. 멱등성(idempotent) 있는 빌드를 지향합니다.

## 탐색 (Navigation)

**1. 전체 솔루션 빌드** → [`references/build-solution.md`](references/build-solution.md)

- 복제(Cloning) 후 첫 빌드, 테스트 전 빌드, 릴리스 아티팩트 생성 시

**2. 종속성만 복원** → [`references/restore-deps.md`](references/restore-deps.md)

- 개발 환경 설정, 누락된 패키지 수정, NuGet 트러블슈팅 시

## 일반적인 패턴 (Common Patterns)

### 빠른 빌드 (Debug)

```bash
cd ./dotnet
dotnet build PigeonPea.sln
```

### 빠른 빌드 (Release)

```bash
cd ./dotnet
dotnet build PigeonPea.sln --configuration Release
```

### 복원 후 빌드 (Restore then Build)

```bash
cd ./dotnet
dotnet restore PigeonPea.sln
dotnet build PigeonPea.sln --no-restore
```

### Clean 후 Rebuild

```bash
cd ./dotnet
dotnet clean PigeonPea.sln
dotnet build PigeonPea.sln
```

### 특정 프로젝트 빌드

```bash
cd ./dotnet
dotnet build console-app/PigeonPea.Console.csproj
```

### 디버깅을 위한 상세 빌드 (Verbose Build)

```bash
cd ./dotnet
dotnet build PigeonPea.sln --verbosity detailed
```

## 트러블슈팅 (Troubleshooting)

**빌드 실패:** 에러 메시지를 확인하세요. 상세한 에러 처리는 `references/build-solution.md`를 참조하세요.

**종속성 누락:** `dotnet restore`를 실행하세요. `references/restore-deps.md`를 참조하세요.

**NU1301 (service index):** NuGet에 접속할 수 없습니다. `references/restore-deps.md`를 확인하세요.

**빌드 속도 저하:** `--no-restore`, `-m` (병렬 처리), 또는 `/p:RunAnalyzers=false`를 사용하세요. `references/build-solution.md`를 참조하세요.

**오래된 아티팩트:** `dotnet clean`을 실행한 후 다시 빌드하세요.

## 성공 지표 (Success Indicators)

```
Build succeeded.
    0 Warning(s)
    0 Error(s)
```

아티팩트 위치: `./dotnet/{ProjectName}/bin/{Configuration}/net9.0/`

## 통합 (Integration)

**빌드 후:** dotnet-test (테스트), code-analyze (정적 분석)
**빌드 전:** code-format (스타일 수정)

## 관련 링크 (Related)

- [`./dotnet/README.md`](../../../dotnet/README.md) - 프로젝트 구조
- [`./dotnet/ARCHITECTURE.md`](../../../dotnet/ARCHITECTURE.md) - 아키텍처
- [`.pre-commit-config.yaml`](../../../.pre-commit-config.yaml) - Pre-commit hooks
