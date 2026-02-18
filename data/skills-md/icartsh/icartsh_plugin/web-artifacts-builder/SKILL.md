---
name: web-artifacts-builder
description: 현대적인 프런트엔드 웹 기술(React, Tailwind CSS, shadcn/ui)을 사용하여 정교한 다중 컴포넌트 claude.ai용 HTML artifact를 제작하기 위한 툴킷입니다. 상태 관리, 라우팅 또는 shadcn/ui 컴포넌트가 필요한 복잡한 artifact에 사용하세요. 단순한 단일 파일 HTML/JSX artifact용이 아닙니다.
license: LICENSE.txt의 전체 약관 참조
---

# Web Artifacts Builder

강력한 프런트엔드 claude.ai artifact를 제작하려면 다음 단계를 따르세요:
1. `scripts/init-artifact.sh`를 사용하여 프런트엔드 레포지토리를 초기화합니다.
2. 생성된 코드를 편집하여 artifact를 개발합니다.
3. `scripts/bundle-artifact.sh`를 사용하여 모든 코드를 단일 HTML 파일로 번들링합니다.
4. 사용자에게 artifact를 표시합니다.
5. (선택 사항) artifact를 테스트합니다.

**기술 스택(Stack)**: React 18 + TypeScript + Vite + Parcel (번들링) + Tailwind CSS + shadcn/ui

## 디자인 및 스타일 가이드라인

매우 중요: "AI가 만든 뻔한 느낌(AI slop)"을 피하기 위해, 과도한 중앙 정렬 레이아웃, 보라색 그라데이션, 일률적인 둥근 모서리, Inter 폰트 사용을 지양하세요.

## 빠른 시작 (Quick Start)

### Step 1: 프로젝트 초기화

초기화 스크립트를 실행하여 새로운 React 프로젝트를 생성합니다:
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

이 명령은 다음이 구성된 프로젝트를 생성합니다:
- ✅ React + TypeScript (Vite 기반)
- ✅ Tailwind CSS 3.4.1 (shadcn/ui 테마 시스템 포함)
- ✅ 경로 별칭(`@/`) 설정 완료
- ✅ 40개 이상의 shadcn/ui 컴포넌트 사전 설치
- ✅ 모든 Radix UI 종속성 포함
- ✅ Parcel 번들링 설정 완료 (.parcelrc 사용)
- ✅ Node 18+ 호환성 (Vite 버전 자동 정밀 감지)

### Step 2: artifact 개발

생성된 파일들을 편집하여 artifact를 빌드합니다. 안내가 필요한 경우 아래의 **일반적인 개발 작업**을 참조하세요.

### Step 3: 단일 HTML 파일로 번들링

React 앱을 단일 HTML artifact로 번들링합니다:
```bash
bash scripts/bundle-artifact.sh
```

이 명령은 `bundle.html`을 생성합니다. 이는 모든 JavaScript, CSS 및 종속성이 인라인화된 독립적인 artifact 파일입니다. 이 파일은 Claude 대화에서 artifact로 직접 공유할 수 있습니다.

**요구 사항**: 프로젝트 루트 디렉토리에 `index.html`이 있어야 합니다.

**스크립트 동작 원리**:
- 번들링 종속성 설치 (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- 경로 별칭을 지원하는 `.parcelrc` 설정 생성
- Parcel로 빌드 (소스 맵 제외)
- html-inline을 사용하여 모든 에셋을 단일 HTML로 인라인화

### Step 4: 사용자에게 artifact 공유

번들링된 HTML 파일을 사용자에게 공유하여 artifact로 볼 수 있게 합니다.

### Step 5: artifact 테스트/시각화 (선택 사항)

참고: 이 단계는 완전히 선택 사항입니다. 필요한 경우 또는 요청이 있을 때만 수행하세요.

artifact를 테스트하거나 시각화하려면 가용한 도구들(다른 SKILL이나 Playwright, Puppeteer와 같은 내장 도구 포함)을 사용하세요. 일반적으로 artifact 테스트를 미리 수행하는 것은 요청과 결과 확인 사이의 지연 시간(latency)을 유발하므로 피하는 것이 좋습니다. 요청이 있거나 문제가 발생했을 때, artifact를 먼저 제시한 후에 테스트를 진행하세요.

## 참조 (Reference)

- **shadcn/ui components**: https://ui.shadcn.com/docs/components