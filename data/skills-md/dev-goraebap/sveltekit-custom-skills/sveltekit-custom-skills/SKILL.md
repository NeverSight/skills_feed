---
name: sveltekit-custom-skills
description: SvelteKit 프로젝트의 서버 아키텍처와 코드 작성 규칙. 서버 레이어(Active Record, Query Service, REST API), 컴포넌트 재사용 정책, 코드 가독성 가이드를 정의한다. SvelteKit 코드를 작성하거나 리뷰할 때 참고한다.
---

# SvelteKit Custom Skills

SvelteKit 프로젝트에 적용하는 아키텍처와 코드 작성 규칙을 정의한다.

## 서버 아키텍처 (Server Architecture)

Active Record 도메인 모델, Query Service 조회 패턴, REST API 엔드포인트 규칙, 서브도메인 기반 스키마 조직.

핵심 규칙:
- **레이어 분리**: `server/domain/` (Active Record CUD) + `server/infra/` (Query Service 조회)
- **직접 ORM 조작 금지**: `+server.ts` → Domain Model, `+page.server.ts` → Query Service
- **R/CUD 분리**: load는 `+page.server.ts`, 쓰기는 `routes/api/` REST 엔드포인트
- **form actions 미사용**: REST API로 분리하여 백엔드 이식성 확보
- **서버 타입이 원천**: CUD 타입은 Drizzle 스키마에서 추출, 조회 뷰모델은 `infra/view-models/`에 정의. `$lib/entities/` 같은 별도 공유 타입 레이어 금지

상세: [references/server-architecture.md](references/server-architecture.md)

## 기본 규칙 (Base Rules)

컴포넌트·함수 재사용 정책과 코드 작성 가이드.

핵심 규칙:
- **라우트 우선 배치**: 반복 패턴이 보여도 `$lib`로 바로 빼지 않는다. 해당 라우트 내부에서 먼저 해결한다
- **`$lib/components`는 신중하게**: 3개 이상 페이지에서 쓰이는 범용 UI만 배치한다
- **인라인 타입 금지**: 구조 분해 할당에 인라인 타입 금지. 반드시 `interface`나 `type`으로 분리 정의한다
- **스크립트 섹션 주석**: Svelte 파일의 `<script>` 영역은 역할별로 섹션 주석을 단다
- **함수 주석**: 함수에는 목적을 설명하는 간단한 주석을 단다

상세: [references/base-rules.md](references/base-rules.md)
