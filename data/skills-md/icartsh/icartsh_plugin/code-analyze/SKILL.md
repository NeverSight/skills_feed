---
name: code-analyze
version: 0.1.0
kind: cli
description: .NET 코드에서 정적 분석(Static analysis), 보안 스캔(Security scan) 및 종속성 체크(Dependency check)를 수행합니다. 코드 품질, 보안 감사 또는 취약점 탐지가 포함된 작업에서 사용합니다.
inputs:
  analysis_type: [static, security, dependencies, all]
  project_path: string
  severity_filter: [error, warning, suggestion, all]
contracts:
  success: '분석이 결과 보고서와 함께 완료됨; exit code 0'
  failure: 'Non-zero exit code 또는 도구 실행 에러'
---

# Code Analysis Skill (Entry Map)

> **Goal:** 에이전트가 필요한 분석 절차를 정확하게 찾을 수 있도록 가이드합니다.

## Quick Start (하나를 선택하세요)

- **Static code analysis 실행** → `references/static-analysis.md`
- **보안 이슈 스캔 (Scan for security issues)** → `references/security-scan.md`
- **종속성 취약점 체크 (Check dependency vulnerabilities)** → `references/dependency-check.md`

## When to Use

- 코드 품질 표준 및 모범 사례 시행
- 잠재적인 버그 및 code smell 탐지
- 코드 내 보안 취약점 식별
- 취약한 종속성(Dependency) 확인
- 자동화된 코드 리뷰 실행

**다음을 위한 것이 아님:** 빌드 (dotnet-build), 테스트 (dotnet-test), 또는 포맷팅 (code-format)

## Inputs & Outputs

**Inputs:** `analysis_type` (static/security/dependencies/all), `project_path` (default: ./dotnet/PigeonPea.sln), `severity_filter` (error/warning/suggestion)

**Outputs:** `analysis_report` (파일/라인이 포함된 결과), `exit_code` (0=clean, 1=issues), `metrics` (심각도별 위반 사항)

**Guardrails:** 분석만 수행하며 코드를 절대 수정하지 마십시오. 모든 결과를 컨텍스트와 함께 보고하고 심각한 이슈 발생 시 실패로 처리합니다.

## Navigation

**1. Static Code Analysis** → [`references/static-analysis.md`](references/static-analysis.md)

- Roslyn analyzers, StyleCop, 코드 품질 규칙, 모범 사례

**2. Security Scanning** → [`references/security-scan.md`](references/security-scan.md)

- Secret 탐지 (gitleaks, detect-secrets), 보안 analyzers, 취약점 패턴

**3. Dependency Vulnerability Check** → [`references/dependency-check.md`](references/dependency-check.md)

- NuGet 패키지 취약점, 오래된 종속성, CVE 탐지

## Common Patterns

### Quick Analysis (모든 체크 수행)

```bash
cd ./dotnet
dotnet build PigeonPea.sln /p:TreatWarningsAsErrors=true
dotnet list package --vulnerable
```

### Static Analysis 전용

```bash
cd ./dotnet
dotnet build PigeonPea.sln /p:RunAnalyzers=true /warnaserror
```

### Security Scan (커밋 전)

```bash
pre-commit run gitleaks --all-files
pre-commit run detect-secrets --all-files
```

### Dependency Check

```bash
cd ./dotnet
dotnet list package --vulnerable --include-transitive
dotnet list package --outdated
```

### Full Analysis Suite

```bash
# 저장소 루트에서 실행
.agent/skills/code-analyze/scripts/analyze.sh --all
```

### 특정 심각도(Severity)를 포함한 분석

```bash
cd ./dotnet
# 에러 전용
dotnet build PigeonPea.sln /p:TreatWarningsAsErrors=false

# 경고를 에러로 처리
dotnet build PigeonPea.sln /p:TreatWarningsAsErrors=true
```

## Troubleshooting

**Analyzer를 찾을 수 없음:** Roslyn analyzers가 활성화되어 있는지 확인하십시오. `references/static-analysis.md`를 참조하세요.

**경고가 너무 많음:** Severity별로 필터링하거나 suppression을 추가하십시오. `references/static-analysis.md`를 참조하세요.

**False positives:** `.editorconfig` 또는 suppression을 사용하십시오. `references/static-analysis.md`를 참조하세요.

**Secret이 탐지되지 않음:** `.gitleaksignore` 및 `.secrets.baseline`을 확인하십시오. `references/security-scan.md`를 참조하세요.

**Dependency scan 실패:** 네트워크 문제 또는 패키지 복원(Restore)이 필요할 수 있습니다. `references/dependency-check.md`를 참조하세요.

## Success Indicators

**Static Analysis:**

```
Build succeeded.
    0 Warning(s)
    0 Error(s)
```

**Security Scan:**

```
gitleaks................Passed
detect-secrets...........Passed
```

**Dependency Check:**

```
No vulnerable packages found.
```

## Integration

**커밋 전:** 보안 스캔(gitleaks, detect-secrets) 실행
**빌드 후:** 정적 분석(Roslyn, StyleCop) 실행
**정기 체크:** 종속성 취약점 체크 실행

**CI/CD Integration:** 빌드 파이프라인에 모든 분석을 포함하고 심각한 이슈 발생 시 실패 처리

## Related

- [`./dotnet/ARCHITECTURE.md`](../../../dotnet/ARCHITECTURE.md) - 프로젝트 구조
- [`.pre-commit-config.yaml`](../../../.pre-commit-config.yaml) - Pre-commit hooks
- [`.editorconfig`](../../../.editorconfig) - 코드 스타일 규칙
- [`dotnet-build`](../dotnet-build/SKILL.md) - 빌드 SKILL
