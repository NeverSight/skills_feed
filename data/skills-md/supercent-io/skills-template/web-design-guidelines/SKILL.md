---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices". Fetches latest Vercel guidelines and checks files against all rules.
tags: [UI, review, web-interface, guidelines, vercel, design-audit, UX]
platforms: [Claude, ChatGPT, Gemini]
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines Review

Review files for compliance with Vercel's Web Interface Guidelines.

## When to use this skill

- **UI 코드 리뷰**: 웹 인터페이스 가이드라인 준수 여부 확인
- **접근성 체크**: "check accessibility" 요청 시
- **디자인 감사**: "audit design" 요청 시
- **UX 리뷰**: "review UX" 요청 시
- **베스트 프랙티스 검토**: "check my site against best practices" 요청 시

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Instructions

### Step 1: 가이드라인 가져오기

**WebFetch 사용**:
```
WebFetch URL: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
Prompt: "Extract all UI rules and guidelines"
```

### Step 2: 파일 분석

사용자가 제공한 파일 또는 패턴을 읽고 분석합니다.

**분석 대상**:
- React/Vue/Svelte 컴포넌트
- HTML 파일
- CSS/SCSS 파일
- TypeScript/JavaScript 파일

### Step 3: 규칙 적용

가져온 가이드라인의 모든 규칙을 파일에 적용하고 위반 사항을 출력합니다.

## Input Format

### 필수 정보
- **파일 또는 패턴**: 검토할 파일 경로 또는 glob 패턴

### 입력 예시

```
내 UI 코드 리뷰해줘:
- 파일: src/components/Button.tsx
```

```
접근성 체크해줘:
- 패턴: src/**/*.tsx
```

## Output Format

가이드라인에서 지정한 형식을 따릅니다 (일반적으로 `file:line` 형식):

```
src/components/Button.tsx:15 - Button should have aria-label for icon-only buttons
src/components/Modal.tsx:42 - Modal should trap focus within itself
src/pages/Home.tsx:8 - Main content should be wrapped in <main> element
```

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.

## Constraints

### 필수 규칙 (MUST)

1. **최신 가이드라인 사용**: 매 리뷰 시 source URL에서 fresh 가이드라인 fetch
2. **전체 규칙 적용**: 가져온 가이드라인의 모든 규칙 검사
3. **정확한 위치 표시**: file:line 형식으로 위반 위치 명시

### 금지 사항 (MUST NOT)

1. **오래된 캐시 사용**: 항상 최신 가이드라인 fetch
2. **부분 검사**: 일부 규칙만 적용하지 않음

## Best practices

1. **파일 범위 제한**: 한 번에 너무 많은 파일 검사 시 컨텍스트 초과 주의
2. **우선순위 지정**: critical 이슈부터 보고
3. **수정 제안**: 위반 사항과 함께 수정 방법 제안

## References

- [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2026-01-22
- **호환 플랫폼**: Claude, ChatGPT, Gemini
- **원본 출처**: vercel/agent-skills

### 관련 스킬
- [web-accessibility](../web-accessibility/SKILL.md): WCAG 접근성 구현
- [ui-component-patterns](../ui-component-patterns/SKILL.md): UI 컴포넌트 패턴

### 태그
`#UI` `#review` `#web-interface` `#guidelines` `#vercel` `#design-audit` `#UX` `#frontend`
