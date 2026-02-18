---
name: agentic-workflow
description: AI 에이전트 실전 워크플로우와 생산성 기법. 명령어, 단축키, Git 통합, MCP 활용, 세션 관리 등 일상 개발 작업의 최적화 패턴 제공.
allowed-tools: [Read, Write, Bash, Grep, Glob]
tags: [agentic-workflow, productivity, git, mcp, commands, multi-agent]
platforms: [Claude, Gemini, ChatGPT, Codex]
version: 2.0.0
source: Claude Code 완전 가이드 70가지 팁 (ykdojo + Ado Kukic)
---

# AI 에이전트 워크플로우 (Workflow & Productivity)

## When to use this skill

- 일상적인 AI 에이전트 작업 최적화
- Git/GitHub 워크플로우 통합
- MCP 서버 활용
- 세션 관리 및 복구
- 생산성 향상 기법 적용

---

## 1. 에이전트별 주요 명령어

### Claude Code 명령어

| 명령어 | 기능 | 사용 시점 |
|--------|------|----------|
| `/init` | CLAUDE.md 초안 자동 생성 | 새 프로젝트 시작 |
| `/usage` | 토큰 사용량/리셋 시간 표시 | 매 세션 시작 |
| `/clear` | 대화 내용 초기화 | 컨텍스트 오염 시, 새 작업 시작 |
| `/context` | 컨텍스트 윈도우 X-Ray | 성능 저하 시 |
| `/clone` | 대화 전체 복제 | A/B 비교 실험, 백업 |
| `/mcp` | MCP 서버 관리 | MCP 활성화/비활성화 |
| `!cmd` | Claude 처리 없이 즉시 실행 | 빠른 상태 확인 |

### Gemini CLI 명령어

| 명령어 | 기능 |
|--------|------|
| `gemini` | 대화 시작 |
| `@file` | 파일 컨텍스트 추가 |
| `-m model` | 모델 선택 |

### Codex CLI 명령어

| 명령어 | 기능 |
|--------|------|
| `codex` | 대화 시작 |
| `codex run` | 명령 실행 |

---

## 2. 키보드 단축키 (Claude Code)

### 필수 단축키

| 단축키 | 기능 | 중요도 |
|--------|------|--------|
| `Esc Esc` | 마지막 작업 즉시 취소 | 최고 |
| `Ctrl+R` | 이전 프롬프트 히스토리 검색 | 높음 |
| `Shift+Tab` x2 | 계획 모드 토글 | 높음 |
| `Tab` / `Enter` | 프롬프트 제안 수락 | 중간 |
| `Ctrl+B` | 백그라운드로 보내기 | 중간 |
| `Ctrl+G` | 외부 에디터로 편집 | 낮음 |

### 에디터 편집 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+A` | 줄 시작으로 이동 |
| `Ctrl+E` | 줄 끝으로 이동 |
| `Ctrl+W` | 이전 단어 삭제 |
| `Ctrl+U` | 줄 시작까지 삭제 |
| `Ctrl+K` | 줄 끝까지 삭제 |

---

## 3. 세션 관리

### Claude Code 세션
```bash
# 마지막 대화 이어서 시작
claude --continue

# 특정 세션 재개
claude --resume <session-name>

# 대화 중 이름 지정
/rename stripe-integration
```

### 권장 별칭 설정
```bash
# ~/.zshrc 또는 ~/.bashrc
alias c='claude'
alias cc='claude --continue'
alias cr='claude --resume'
alias g='gemini'
alias cx='codex'
```

---

## 4. Git 워크플로우

### 자동 커밋 메시지 생성
```
"변경 사항을 분석하고 적절한 커밋 메시지를 작성한 후 커밋해줘"
```

### Draft PR 자동 생성
```
"현재 브랜치의 변경 사항으로 draft PR을 만들어줘.
제목은 변경 내용을 요약하고, 본문에는 주요 변경 사항을 리스트로 작성해줘."
```

### Git Worktrees 활용
```bash
# 여러 브랜치 동시 작업
git worktree add ../myapp-feature-auth feature/auth
git worktree add ../myapp-hotfix hotfix/critical-bug

# 각 worktree에서 독립적 AI 세션
탭 1: ~/myapp-feature-auth → 새 기능 개발
탭 2: ~/myapp-hotfix → 긴급 버그 수정
탭 3: ~/myapp (main) → 메인 브랜치 유지
```

### PR 리뷰 워크플로우
```
1. "gh pr checkout 123을 실행하고 이 PR의 변경 사항을 요약해줘"
2. "src/auth/middleware.ts 파일의 변경점을 분석해줘. 보안 이슈나 성능 문제가 있는지 확인해줘"
3. "이 로직을 더 효율적으로 바꿀 방법이 있을까?"
4. "네가 제안한 개선 사항을 적용하고 테스트를 실행해줘"
```

---

## 5. MCP 서버 활용 (Multi-Agent)

### 주요 MCP 서버

| MCP 서버 | 기능 | 용도 |
|----------|------|------|
| Playwright | 웹 브라우저 제어 | E2E 테스트 |
| Supabase | 데이터베이스 쿼리 | DB 직접 접근 |
| Firecrawl | 웹 크롤링 | 데이터 수집 |
| Gemini-CLI | 대용량 분석 | 1M+ 토큰 분석 |
| Codex-CLI | 명령 실행 | 빌드, 배포 |

### MCP 활용 예시
```bash
# Gemini: 대용량 분석
> ask-gemini "@src/ 전체 코드베이스 구조 분석해줘"

# Codex: 명령 실행
> shell "docker-compose up -d"
> shell "npm test && npm run build"
```

### MCP 최적화
```bash
# 사용하지 않는 MCP 비활성화
/mcp

# 권장 수치
# - MCP 서버: 10개 미만
# - 활성 도구: 80개 미만
```

---

## 6. Multi-Agent 워크플로우 패턴

### 오케스트레이션 패턴
```
[Claude] 계획 수립 → [Gemini] 분석/리서치 → [Claude] 코드 작성 → [Codex] 실행/테스트 → [Claude] 결과 종합
```

### 실전 예시: API 설계 + 구현 + 테스트
```
1. [Claude] 스킬 기반 API 스펙 설계
2. [Gemini] ask-gemini "@src/ 기존 API 패턴 분석" - 대용량 코드베이스 분석
3. [Claude] 분석 결과 기반 코드 구현
4. [Codex] shell "npm test && npm run build" - 테스트 및 빌드
5. [Claude] 최종 리포트 생성
```

### TDD 워크플로우
```
"TDD 방식으로 작업해줘. 먼저 실패하는 테스트를 작성하고,
그 테스트를 통과시키는 코드를 작성해줘."

# AI가:
# 1. 실패하는 테스트 작성
# 2. git commit -m "Add failing test for user auth"
# 3. 테스트를 통과시키는 최소한의 코드 작성
# 4. 테스트 실행 → 통과 확인
# 5. git commit -m "Implement user auth to pass test"
```

---

## 7. 컨테이너 워크플로우

### Docker 컨테이너 설정
```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    curl git tmux vim nodejs npm python3 python3-pip
RUN curl -fsSL https://claude.ai/install.sh | sh
WORKDIR /workspace
CMD ["/bin/bash"]
```

### 안전한 실험 환경
```bash
# 컨테이너 빌드 및 실행
docker build -t ai-sandbox .
docker run -it --rm \
  -v $(pwd):/workspace \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  ai-sandbox

# 컨테이너 안에서 실험적 작업 수행
```

---

## 8. 문제 해결

### 컨텍스트 과다 시
```bash
/context  # 사용량 확인
/clear    # 컨텍스트 초기화

# 또는 HANDOFF.md 생성 후 새 세션
```

### 작업 취소
```
Esc Esc  # 마지막 작업 즉시 취소
```

### 성능 저하 시
```bash
# MCP/도구 수 확인
/mcp

# 불필요한 MCP 비활성화
# 컨텍스트 초기화
```

---

## Quick Reference Card

```
=== 필수 명령어 ===
/clear      컨텍스트 초기화
/context    사용량 확인
/usage      토큰 확인
/init       프로젝트 설명 파일 생성
!command    즉시 실행

=== 단축키 ===
Esc Esc     작업 취소
Ctrl+R      히스토리 검색
Shift+Tab×2 계획 모드
Ctrl+B      백그라운드

=== CLI 플래그 ===
--continue  대화 이어가기
--resume    세션 복구
-p "prompt" Headless 모드

=== Multi-Agent ===
Claude      계획/코드 생성
Gemini      대용량 분석
Codex       명령 실행

=== 문제 해결 ===
컨텍스트 과다 → /clear
작업 취소 → Esc Esc
성능 저하 → /context 확인
```
