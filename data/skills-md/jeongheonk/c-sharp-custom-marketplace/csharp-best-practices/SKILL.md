---
name: csharp-best-practices
description: C# 12 / .NET 8 기준 코드 작성 가이드라인. 코드 작성 전/중에 참조하는 knowledge-base skill. Modern C# 기능과 베스트 프랙티스를 자동 주입.
user-invocable: true
context: current
argument-hint: "[topic]"
---

# C# Best Practices

C# 12 / .NET 8 기준 코드 작성 가이드라인 knowledge-base skill.

## Overview

이 스킬은 코드 **작성 시** 참조하는 가이드라인을 제공합니다. 코드 리뷰(csharp-code-review)와 달리, 작성 전/중에 올바른 패턴을 안내합니다.

| 구분 | csharp-code-review | csharp-best-practices |
|------|-------------------|----------------------|
| 목적 | 기존 코드 리뷰/검토 | 코드 작성 시 가이드라인 참조 |
| 시점 | 코드 작성 후 | 코드 작성 전/중 |
| 출력 | 리뷰 리포트 | 가이드라인 주입 |

## Arguments

- `$ARGUMENTS[0]`: 조회할 토픽 (optional)
  - 미지정 시 전체 규칙 목록 표시
  - 예: `primary-constructor`, `record`, `pattern-matching`

## Rules

### C# 12 Features (.NET 8) — CRITICAL

코드 작성 시 반드시 고려해야 할 C# 12 기능:

| 규칙 | 파일 | 설명 |
|------|------|------|
| Primary Constructors | `rules/cs12-primary-constructor.md` | class/struct 직접 생성자 매개변수 |
| Collection Expressions | `rules/cs12-collection-expression.md` | `[1, 2, 3]` 통합 구문 |
| Alias Any Type | `rules/cs12-alias-any-type.md` | `using` alias 모든 타입 |
| Lambda Default Params | `rules/cs12-lambda-defaults.md` | 람다 기본 매개변수 |
| Inline Arrays | `rules/cs12-inline-array.md` | struct 고정 크기 배열 |
| ref readonly Parameters | `rules/cs12-ref-readonly-param.md` | ref/in 명확한 API |

### Modern C# (C# 9-11, .NET 8 호환) — MEDIUM

| 규칙 | 파일 | 버전 |
|------|------|------|
| Record Types | `rules/modern-record-type.md` | C# 9 |
| required / init | `rules/modern-required-init.md` | C# 11 |
| Pattern Matching | `rules/modern-pattern-matching.md` | C# 8-11 |
| List Patterns | `rules/modern-list-pattern.md` | C# 11 |
| Raw String Literals | `rules/modern-raw-string-literal.md` | C# 11 |
| File-scoped Namespaces | `rules/modern-file-scoped-namespace.md` | C# 10 |

## Execution

### 토픽 지정 시

해당 규칙 파일을 읽고 가이드라인을 출력합니다.

```
/csharp-best-practices primary-constructor
→ rules/cs12-primary-constructor.md 내용 출력
```

### 토픽 미지정 시

전체 규칙 목록을 요약하여 출력합니다.

```
/csharp-best-practices
→ 12개 규칙 목록 + 간단 설명 출력
```

## 현재 전달받은 인자

**ARGUMENTS**: $ARGUMENTS

## 실행 지시

1. ARGUMENTS가 있으면 해당 토픽과 매칭되는 규칙 파일을 찾아 내용을 출력하세요.
2. ARGUMENTS가 비어있으면 전체 규칙 목록을 요약하여 출력하세요.
3. 규칙 출력 시 **Before/After 코드 예시**를 반드시 포함하세요.
