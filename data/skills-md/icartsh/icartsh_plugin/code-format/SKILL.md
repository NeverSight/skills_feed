---
name: code-format
version: 0.1.0
kind: cli
description: dotnet format, prettier 및 기타 포맷팅 도구를 사용하여 코드를 정리합니다. 코드 스타일 수정, 포맷 일관성 유지 또는 커밋 전 코드 준비가 필요한 작업에서 사용합니다.
inputs:
  target: [dotnet, prettier, all]
  files: string[]
  verify: boolean
contracts:
  success: '코드가 성공적으로 포맷팅됨; 남은 스타일 위반 사항 없음'
  failure: 'Non-zero exit code 또는 포맷팅 에러'
---

# Code Format Skill (Entry Map)

> **Goal:** 에이전트가 필요한 정확한 포맷팅 절차를 찾을 수 있도록 가이드합니다.

## Quick Start (하나를 선택하세요)

- **.NET 코드 포맷팅 (C#)** → `references/dotnet-format.md`
- **JSON/YAML/Markdown 포맷팅** → `references/prettier-format.md`
- **모든 항목 포맷팅** → `references/fix-all.md`

## When to Use

- 코드 스타일 위반 수정 (들여쓰기, 공백, 줄 바꿈 등)
- .editorconfig 규칙을 일관되게 적용
- 커밋을 위한 코드 준비 (pre-commit hook 포맷팅)
- 팀 코딩 표준 준수
- 특정 파일 또는 전체 코드베이스 포맷팅

**다음을 위한 것이 아님:** 빌드 (dotnet-build), 테스트 (dotnet-test), 또는 린팅 (code-analyze)

## Inputs & Outputs

**Inputs:** `target` (dotnet/prettier/all), `files` (특정 파일 또는 디렉토리), `verify` (체크 전용 모드)

**Outputs:** 포맷팅된 파일 (파일 내에서 직접 수정), exit code (0=success, non-zero=violations)

**Guardrails:** 비파괴적 방식 (변경 없이 확인하는 --verify-no-changes 가능), .editorconfig 존중, pre-commit과 통합

## Navigation

**1. Format .NET Code** → [`references/dotnet-format.md`](references/dotnet-format.md)

- C# 파일(.cs) 포맷팅, dotnet format 규칙 적용, 코드 스타일 이슈 수정

**2. Format with Prettier** → [`references/prettier-format.md`](references/prettier-format.md)

- JSON, YAML, Markdown, JavaScript, TypeScript 파일 포맷팅

**3. Format All Code** → [`references/fix-all.md`](references/fix-all.md)

- 모든 포맷터(dotnet + prettier)를 순차적으로 실행, 포괄적인 포맷팅 수행

## Common Patterns

### Quick Format (.NET)

```bash
cd ./dotnet
dotnet format PigeonPea.sln
```

### Quick Format (Prettier)

```bash
npx prettier --write "**/*.{json,yml,yaml,md}"
```

### Format Everything

```bash
./.agent/skills/code-format/scripts/format-all.sh
```

### Verify Only (체크 모드)

```bash
cd ./dotnet
dotnet format PigeonPea.sln --verify-no-changes
```

### 특정 파일 포맷팅

```bash
# .NET
dotnet format --include ./console-app/Program.cs

# Prettier
npx prettier --write ./README.md
```

## Troubleshooting

**포맷팅 실패:** 에러 메시지를 확인하십시오. 상세한 에러 처리는 관련 참조 파일을 확인하세요.

**파일이 포맷팅되지 않음:** .editorconfig 규칙, 파일 확장자, ignore 패턴을 확인하십시오.

**Pre-commit hook 실패:** 먼저 포맷터를 수동으로 실행한 후 커밋하십시오. `references/fix-all.md`를 참조하세요.

**스타일 충돌:** .editorconfig가 우선순위를 가집니다. 구성 파일을 확인하십시오.

**성능 이슈:** 전체 솔루션 대신 특정 프로젝트나 파일에 대해 포맷팅을 수행하십시오.

## Success Indicators

### dotnet format

```
Format complete in X ms.
```

이미 포맷팅된 경우 변경된 파일이 없거나, 포맷팅된 파일 목록이 표시됩니다.

### prettier

```
✔ Formatted X files
```

또는 모든 파일이 이미 포맷팅된 경우 출력이 없습니다.

## Integration

**커밋 전:** pre-commit hook을 사용하여 자동 포맷팅(`.pre-commit-config.yaml`에 구성됨)
**수동 포맷팅:** 코드 푸시 전, PR 생성 전 실행
**CI/CD:** CI에서 포맷팅 검증 (--verify-no-changes / --check 모드 사용)

**다른 SKILL과 함께 사용:**
- 이전 단계: code-analyze (스타일 먼저 수정)
- 다음 단계: dotnet-build (깔끔한 코드 빌드)

## Configuration Files

- **`.editorconfig`**: 포맷팅 규칙 정의 (indent size, line endings 등)
- **`.prettierrc.json`**: Prettier 구성 (print width, quotes 등)
- **`.pre-commit-config.yaml`**: Pre-commit hook 구성
- **`.prettierignore`**: Prettier 포맷팅에서 제외할 파일

## Related

- [`.editorconfig`](../../../.editorconfig) - 포맷팅 규칙
- [`.prettierrc.json`](../../../.prettierrc.json) - Prettier 설정
- [`.pre-commit-config.yaml`](../../../.pre-commit-config.yaml) - Pre-commit hooks
- [`setup-pre-commit.sh`](../../../setup-pre-commit.sh) - Pre-commit 설정 스크립트
