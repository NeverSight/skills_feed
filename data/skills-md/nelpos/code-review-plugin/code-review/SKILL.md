---
name: code-review
description: Analyze source code quality and propose prioritized fixes using Tidy First and Modern Software Engineering principles. Use for requests like code review, PR review, refactoring suggestions, architecture quality checks, maintainability analysis, or improvement proposals across TypeScript, JavaScript, Python, React, and Next.js codebases.
---

# Code Review Skill

## 목적

코드 품질을 일관된 기준으로 평가하고, 재현 가능한 근거와 함께 우선순위 기반 개선안을 제시한다.

## 목차

- 실행 워크플로우
- Sub-agent 위임 정책
- Sub-agent 호출 패킷
- 원칙 로딩 규칙
- 산출물 규격
- 검증 루프
- 제외 범위
- 확장 규칙
- 참조 문서

## 실행 워크플로우

1. 리뷰 범위를 확정한다.
- 사용자가 지정한 파일, 폴더, diff, PR 번호를 우선 사용한다.
- 범위가 모호하면 대화 문맥에서 가장 최근 코드 블록을 기본 범위로 사용한다.

2. Sub-agent 위임 필요성을 먼저 판단한다.
- 위임 기준과 역할 분리는 `references/sub-agent-playbook.md`를 따른다.
- 대규모 변경, 다중 스택, 출력이 매우 긴 작업은 sub-agent 위임을 기본값으로 한다.

3. 언어/프레임워크를 식별한다.
- `package.json`: TypeScript/JavaScript 후보
- `requirements.txt`, `pyproject.toml`: Python 후보
- React/Next.js 파일 패턴(`*.tsx`, `app/`, `next.config.*`) 확인

4. 1차 리뷰를 수행한다 (Tidy First).
- Guard Clauses
- Extract Function
- High Cohesion
- Low Coupling
- 상세 기준: `references/tidy-first.md`

5. 2차 리뷰를 수행한다 (Modern SE).
- Modularity
- Cohesion
- Separation of Concerns
- Information Hiding
- Coupling
- 상세 기준: `references/modern-engineering.md`

6. 필요 시 언어/프레임워크 가이드를 추가 로드한다.
- TypeScript: `references/language-guides/typescript.md`
- JavaScript: `references/language-guides/javascript.md`
- Python: `references/language-guides/python.md`
- React: `references/framework-guides/react.md`
- Next.js: `references/framework-guides/nextjs.md`

7. 이슈를 우선순위로 분류한다.
- `High`: 버그 가능성, 보안/성능 리스크, 테스트 불가능 구조, 순환 의존성
- `Medium`: 가독성/유지보수성 저하, 중복, 과도한 복잡도
- `Low`: 스타일, 네이밍, 경미한 개선

8. 리뷰 결과를 템플릿 형식으로 출력한다.
- 기본 템플릿: `assets/review-template.md`

## Sub-agent 위임 정책

- `MUST`: 아래 조건 중 하나라도 만족하면 sub-agent를 사용한다.
  - 변경 파일이 8개 이상
  - diff가 대략 400줄 이상
  - 언어/프레임워크가 2개 이상 섞인 변경
  - 테스트/로그/문서 탐색 결과가 길어 메인 컨텍스트를 크게 소비하는 경우
- `SHOULD`: 보안, 성능, 아키텍처 이슈가 동시에 의심되면 역할별 sub-agent를 병렬로 호출한다.
- `SHOULD`: 단일 파일의 짧은 변경(예: 150줄 이하)과 빠른 피드백 요청은 메인 대화에서 직접 처리한다.

권장 역할:
- `code-reviewer`: 일반 품질/가독성/유지보수성
- `security-reviewer`: 입력 검증, 민감정보, 권한/인증 경계
- `performance-reviewer`: 복잡도, 렌더링/쿼리/비동기 병목
- `framework-reviewer`: React/Next.js 등 프레임워크 특화 규칙

sub-agent 템플릿:
- `assets/sub-agents/code-reviewer.md`
- `assets/sub-agents/security-reviewer.md`
- `assets/sub-agents/performance-reviewer.md`

Claude Code 설치 스크립트:
- `scripts/install-claude-subagents.sh`

## Sub-agent 호출 패킷

sub-agent 호출 시 아래 정보를 반드시 포함한다.

- 작업 목표: 무엇을 검토할지 한 문장
- 리뷰 범위: 파일/디렉터리/PR 번호
- 제약: read-only 여부, 금지 도구, 시간/토큰 제한
- 출력 계약:
  - 이슈 목록 (`priority`, `file`, `line`, `principle`, `problem`, `fix`, `evidence`)
  - 확인한 명령/근거
  - 미확인 가정

통합 시 규칙:
- 중복 이슈는 병합하고 근거가 더 강한 항목을 남긴다.
- 충돌하는 제안은 리스크가 낮고 롤백이 쉬운 쪽을 우선한다.
- 최종 결과는 `assets/review-template.md` 형식으로 재정렬한다.

## 원칙 로딩 규칙

- `MUST`: 기본 리뷰 시 `references/tidy-first.md`와 `references/modern-engineering.md`를 기준으로 판단한다.
- `MUST`: 기술 스택이 확인된 경우 해당 언어/프레임워크 가이드를 추가 반영한다.
- `MUST`: sub-agent를 사용한 경우 각 sub-agent 결과를 교차 검증 후 통합한다.
- `SHOULD`: 사용자가 특정 원칙만 요청하면 해당 원칙 중심으로 압축 리뷰한다.

## 산출물 규격

- 각 이슈에 파일/라인 근거를 포함한다.
- 모든 High/Medium 이슈에는 가능한 경우 Before/After 예시를 포함한다.
- 제안마다 기대 효과를 1~3줄로 명시한다.
- 마지막에 실행 가능한 다음 단계(즉시/차기/장기)를 분리한다.

## 검증 루프

1. 1차 결과를 작성한다.
2. 다음 누락 여부를 자체 점검한다.
- 우선순위 분류 누락
- 파일/라인 근거 누락
- 수정 제안은 있으나 기대 효과 부재
3. 누락이 있으면 결과를 수정한다.
4. 최종 출력 전에 중복/상충 제안을 제거한다.

## 제외 범위

기본적으로 아래 경로는 리뷰에서 제외한다.

- 자동 생성 코드: `*.generated.*`, `migrations/`, `__generated__/`
- 의존성/빌드 산출물: `node_modules/`, `vendor/`, `dist/`, `build/`, `out/`, `target/`
- 커버리지/캐시: `coverage/`, `.nyc_output/`, `.cache/`

필요하면 사용자 요청에 따라 제외 규칙을 해제한다.

## 확장 규칙

새 언어 또는 프레임워크를 추가할 때 다음 규칙을 지킨다.

1. `references/` 하위에 전용 가이드를 추가한다.
2. 체크리스트 + Before/After 예시를 반드시 포함한다.
3. SKILL 본문에는 경로만 추가하고 상세 설명은 참조 문서에 둔다.

## 참조 문서

- Tidy First: `references/tidy-first.md`
- Modern Software Engineering: `references/modern-engineering.md`
- Sub-agent Playbook: `references/sub-agent-playbook.md`
- TypeScript: `references/language-guides/typescript.md`
- JavaScript: `references/language-guides/javascript.md`
- Python: `references/language-guides/python.md`
- React: `references/framework-guides/react.md`
- Next.js: `references/framework-guides/nextjs.md`
- 리뷰 템플릿: `assets/review-template.md`
