---
name: bun
description: "Node.js 대신 Bun 런타임 사용을 위한 스킬. 다음 상황에서 사용: (1) 새 JavaScript/TypeScript 프로젝트 생성 시, (2) package.json 또는 의존성 관련 작업 시, (3) 스크립트 실행 또는 개발 서버 시작 시, (4) Node.js 프로젝트를 Bun으로 전환 시, (5) 'bun', 'bunx', 'bun.lockb' 키워드가 포함된 작업 시"
license: MIT
compatibility: Requires bun CLI
metadata:
  author: DaleStudy
  version: "1.0"
allowed-tools: Bash(bun:*) Bash(bunx:*)
---

# Bun

Node.js 대신 Bun을 기본 런타임으로 사용.

## 설치

```bash
curl -fsSL https://bun.sh/install | bash
```

## 명령어 매핑

| Node.js / npm           | Bun                                    |
| ----------------------- | -------------------------------------- |
| `npm install`           | `bun install`                          |
| `npm install <pkg>`     | `bun add <pkg>`                        |
| `npm install -D <pkg>`  | `bun add -d <pkg>`                     |
| `npm uninstall <pkg>`   | `bun remove <pkg>`                     |
| `npm run <script>`      | `bun run <script>` 또는 `bun <script>` |
| `npx <cmd>`             | `bunx <cmd>`                           |
| `node <file>`           | `bun <file>`                           |
| `npm init`              | `bun init`                             |
| `npm create <template>` | `bun create <template>`                |

## 프로젝트 초기화

```bash
# 새 프로젝트
bun init

# 템플릿 사용
bun create next-app my-app
bun create vite my-app
```

## 패키지 관리

```bash
# 설치 (bun.lockb 생성)
bun install

# 의존성 추가
bun add express zod
bun add -d typescript @types/node  # devDependencies

# 삭제
bun remove lodash
```

> lockfile: `bun.lockb` (바이너리). `.gitignore`에 추가하지 않음.

## 스크립트 실행

```bash
# package.json scripts
bun run dev
bun run build

# 파일 직접 실행 (TypeScript 지원)
bun index.ts
bun src/server.ts

# 단축 (run 생략 가능)
bun dev
```

## GitHub Actions

```yaml
- uses: oven-sh/setup-bun@v{N} # 최신 버전 확인: gh api repos/oven-sh/setup-bun/releases/latest --jq '.tag_name'
- run: bun install
- run: bun test
```
