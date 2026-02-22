---
name: react
description: "React 성능 최적화 및 베스트 프랙티스 스킬. Vercel Engineering 가이드 기반, 프레임워크 비종속. 다음 상황에서 사용: (1) React 컴포넌트(.tsx, .jsx) 작성 또는 수정 시, (2) 상태 관리, hooks, 리렌더링 최적화 작업 시, (3) 비동기 데이터 페칭 또는 Suspense 패턴 작업 시, (4) 번들 사이즈 최적화 또는 코드 스플리팅 시, (5) 'react', 'useState', 'useEffect', 'useMemo', 'useCallback', 'memo', 'Suspense', 'lazy' 키워드가 포함된 작업 시"
license: MIT
metadata:
  author: DaleStudy
  version: "1.0.0"
---

# React

Vercel 가이드 기반 React 성능 최적화 베스트 프랙티스. 프레임워크 비종속(Next.js, Remix, Vite 등 무관).

각 규칙의 상세 설명과 코드 예제는 [references/](references/) 참고. 원본 Vercel 가이드의 전체 규칙(Next.js/SSR 포함)은 [vercel-react-best-practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices) 참고.

## 규칙 카테고리

| 우선순위 | 카테고리 | 영향도 | 접두사 |
|----------|----------|--------|--------|
| 1 | 비동기 워터폴 제거 | CRITICAL | `async-` |
| 2 | 번들 사이즈 최적화 | CRITICAL | `bundle-` |
| 3 | 리렌더링 최적화 | MEDIUM | `rerender-` |
| 4 | 렌더링 성능 | MEDIUM | `rendering-` |
| 5 | 클라이언트 데이터/이벤트 | MEDIUM | `client-` |
| 6 | JavaScript 성능 | LOW-MEDIUM | `js-` |
| 7 | 고급 패턴 | LOW | `advanced-` |

## 빠른 참조

### 1. 비동기 워터폴 제거 (CRITICAL)

- [`async-parallel`](references/async-parallel.md) - `Promise.all()`로 독립 작업 병렬화
- [`async-defer-await`](references/async-defer-await.md) - 불필요한 경로에서 await 지연
- [`async-suspense-boundaries`](references/async-suspense-boundaries.md) - Suspense로 부분 렌더링
- [`async-dependencies`](references/async-dependencies.md) - 부분 의존성 있는 작업의 최대 병렬화

### 2. 번들 사이즈 최적화 (CRITICAL)

- [`bundle-barrel-imports`](references/bundle-barrel-imports.md) - barrel file 직접 import 지양
- [`bundle-lazy`](references/bundle-lazy.md) - `React.lazy`로 코드 스플리팅
- [`bundle-preload`](references/bundle-preload.md) - hover/focus 시 프리로드
- [`bundle-conditional`](references/bundle-conditional.md) - 기능 활성화 시에만 모듈 로드
- [`bundle-defer-third-party`](references/bundle-defer-third-party.md) - 비필수 서드파티 하이드레이션 후 로드

### 3. 리렌더링 최적화 (MEDIUM)

- [`rerender-functional-setstate`](references/rerender-functional-setstate.md) - 함수형 setState로 안정적 콜백
- [`rerender-lazy-state-init`](references/rerender-lazy-state-init.md) - 비용 큰 초기값 지연 초기화
- [`rerender-derived-state`](references/rerender-derived-state.md) - 파생 boolean 구독
- [`rerender-dependencies`](references/rerender-dependencies.md) - Effect 의존성 좁히기
- [`rerender-memo`](references/rerender-memo.md) - memo로 비용 큰 작업 분리
- [`rerender-transitions`](references/rerender-transitions.md) - startTransition으로 UI 반응성 유지
- [`rerender-ref-callbacks`](references/rerender-ref-callbacks.md) - ref callback으로 DOM 접근 (useRef+useEffect 대체)
- [`rerender-avoid-usestate`](references/rerender-avoid-usestate.md) - useState 대체 패턴 판단 가이드
- [`rerender-url-state`](references/rerender-url-state.md) - URL 검색 매개변수로 상태 관리
- [`rerender-form-libraries`](references/rerender-form-libraries.md) - 폼 라이브러리로 useState 제거
- [`rerender-discriminated-union`](references/rerender-discriminated-union.md) - discriminated union으로 불가능한 상태 방지
- [`rerender-use-reducer`](references/rerender-use-reducer.md) - useReducer로 복잡한 상태 전이
- [`rerender-derived-state-no-effect`](references/rerender-derived-state-no-effect.md) - 파생 상태를 렌더링 중 계산
- [`rerender-defer-reads`](references/rerender-defer-reads.md) - 상태 읽기를 사용 시점으로 지연
- [`rerender-memo-with-default-value`](references/rerender-memo-with-default-value.md) - memo 컴포넌트 기본값 상수 추출
- [`rerender-move-effect-to-event`](references/rerender-move-effect-to-event.md) - 인터랙션 로직을 이벤트 핸들러로 이동
- [`rerender-simple-expression-in-memo`](references/rerender-simple-expression-in-memo.md) - 단순 표현식에 useMemo 사용 금지
- [`rerender-use-ref-transient-values`](references/rerender-use-ref-transient-values.md) - 일시적 값에 useRef 사용
- [`rerender-simplify-useeffect`](references/rerender-simplify-useeffect.md) - useEffect를 커스텀 훅으로 단순화

### 4. 렌더링 성능 (MEDIUM)

- [`rendering-animate-svg-wrapper`](references/rendering-animate-svg-wrapper.md) - SVG 래퍼로 GPU 가속
- [`rendering-content-visibility`](references/rendering-content-visibility.md) - 긴 목록 오프스크린 최적화
- [`rendering-hoist-jsx`](references/rendering-hoist-jsx.md) - 정적 JSX 호이스팅
- [`rendering-conditional-render`](references/rendering-conditional-render.md) - 삼항 연산자로 falsy 버그 방지
- [`rendering-hydration-no-flicker`](references/rendering-hydration-no-flicker.md) - 하이드레이션 불일치 없이 깜빡임 방지
- [`rendering-activity`](references/rendering-activity.md) - Activity/CSS로 상태/DOM 보존
- [`rendering-svg-precision`](references/rendering-svg-precision.md) - SVG 좌표 정밀도 축소 (SVGO)
- [`rendering-usetransition-loading`](references/rendering-usetransition-loading.md) - useTransition으로 수동 로딩 상태 대체
- [`rendering-inp-css-feedback`](references/rendering-inp-css-feedback.md) - CSS :active + yield로 INP 개선
- [`rendering-composition-vs-early-return`](references/rendering-composition-vs-early-return.md) - Composition vs Early Return 선택 기준

### 5. 클라이언트 데이터/이벤트 (MEDIUM)

- [`client-passive-event-listeners`](references/client-passive-event-listeners.md) - passive로 스크롤 지연 제거
- [`client-localstorage-schema`](references/client-localstorage-schema.md) - localStorage 버전 관리
- [`client-sync-external-store`](references/client-sync-external-store.md) - useSyncExternalStore로 브라우저 API/외부 스토어 구독
- [`client-event-listeners`](references/client-event-listeners.md) - 글로벌 이벤트 리스너 중복 제거
- [`client-data-dedup`](references/client-data-dedup.md) - TanStack Query/SWR로 데이터 페칭 중복 제거
- [`client-abort-redundant-work`](references/client-abort-redundant-work.md) - AbortController로 불필요한 비동기 작업 취소

### 6. JavaScript 성능 (LOW-MEDIUM)

- [`js-index-maps`](references/js-index-maps.md) - Map으로 O(1) 조회
- [`js-tosorted-immutable`](references/js-tosorted-immutable.md) - toSorted()로 불변성 유지
- [`js-set-map-lookups`](references/js-set-map-lookups.md) - Set으로 O(1) 멤버십 검사
- [`js-early-exit`](references/js-early-exit.md) - 조기 반환으로 불필요한 처리 방지
- [`js-batch-dom-css`](references/js-batch-dom-css.md) - DOM 읽기/쓰기 분리로 레이아웃 스래싱 방지
- [`js-cache-function-results`](references/js-cache-function-results.md) - 반복 함수 호출 모듈 레벨 캐싱
- [`js-cache-property-access`](references/js-cache-property-access.md) - 루프 내 프로퍼티 접근 캐싱
- [`js-cache-storage`](references/js-cache-storage.md) - localStorage/cookie 읽기 메모리 캐싱
- [`js-combine-iterations`](references/js-combine-iterations.md) - 복수 배열 순회를 단일 루프로
- [`js-hoist-regexp`](references/js-hoist-regexp.md) - RegExp를 모듈 스코프로 호이스팅
- [`js-length-check-first`](references/js-length-check-first.md) - 배열 비교 시 길이 먼저 확인
- [`js-min-max-loop`](references/js-min-max-loop.md) - 정렬 대신 단일 루프로 min/max
- [`js-iterator-helpers`](references/js-iterator-helpers.md) - Iterator Helper로 지연 처리

### 7. 고급 패턴 (LOW)

- [`advanced-event-handler-refs`](references/advanced-event-handler-refs.md) - 이벤트 핸들러를 ref에 저장 (재구독 방지)
- [`advanced-use-latest`](references/advanced-use-latest.md) - useEffectEvent/useLatest로 안정적 콜백 ref
- [`advanced-init-once`](references/advanced-init-once.md) - 앱 초기화를 컴포넌트가 아닌 모듈 레벨에서
- [`advanced-closure-scope`](references/advanced-closure-scope.md) - 클로저 스코프 격리로 메모리 누수 방지

## Vercel 원본 가이드 추가 규칙

이 스킬은 프레임워크 비종속 규칙만 포함. Next.js/SSR 전용 규칙은 원본 참고:

| 규칙 | 영향도 | 설명 |
|------|--------|------|
| `server-cache-react` | MEDIUM | `React.cache()`로 요청 내 중복 제거 |
| `server-cache-lru` | HIGH | LRU 캐시로 요청 간 캐싱 |
| `server-serialization` | HIGH | RSC 경계에서 직렬화 최소화 |
| `server-parallel-fetching` | CRITICAL | 컴포넌트 구성으로 서버 데이터 병렬 페칭 |
| `server-after-nonblocking` | MEDIUM | `after()`로 논블로킹 후처리 |
| `server-auth-actions` | MEDIUM | 서버 액션 인증 검증 |
| `server-dedup-props` | LOW | 중복 props 제거 |
| `bundle-dynamic-imports` | CRITICAL | `next/dynamic`으로 동적 임포트 |
| `rendering-hydration-suppress-warning` | LOW | suppressHydrationWarning 사용 |
| `async-api-routes` | MEDIUM | API 라우트 비동기 패턴 |

원본 전체 문서: [vercel-labs/agent-skills: react-best-practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices)

## 참고

- [React 공식 문서](https://react.dev)
- [React Compiler](https://react.dev/learn/react-compiler) - 사용 시 `memo()`, `useMemo()` 수동 적용 불필요
- [Vercel: How we made the dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)
- [Vercel: How we optimized package imports](https://vercel.com/blog/how-we-optimized-package-imports-in-next-js)
