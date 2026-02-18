---
name: opencontext
description: OpenContext를 활용한 AI 에이전트 영구 메모리 및 컨텍스트 관리. 세션/레포/날짜 간 컨텍스트 유지, 결론 저장, 문서 검색 워크플로우 제공.
allowed-tools: [Read, Write, Bash, Grep, Glob]
tags: [opencontext, context-management, memory, knowledge-base, multi-agent]
platforms: [Claude, Gemini, ChatGPT, Codex, Cursor]
version: 1.0.0
source: OpenContext Multi-Agent Workflow Guide
---

# OpenContext 컨텍스트 관리 (Persistent Memory)

> AI 어시스턴트에게 영구 메모리를 부여하세요.
> 반복 설명을 멈추고, 더 스마트하게 빌드하세요.

## When to use this skill

- 세션 간 컨텍스트 유지가 필요할 때
- 프로젝트 배경/결정사항을 기록해야 할 때
- 이전 결론/교훈을 검색해야 할 때
- Multi-Agent 워크플로우에서 지식 공유가 필요할 때
- 반복적인 배경 설명을 줄이고 싶을 때

---

## 1. 핵심 개념

### 문제점
AI 어시스턴트로 작업할 때 컨텍스트가 손실됩니다 (세션, 레포, 날짜 간). 배경 설명을 반복하고, 결정을 다시 설명하며, 때때로 어시스턴트가 잘못된 가정으로 계속 진행합니다.

### 해결책
**OpenContext**는 AI 어시스턴트를 위한 경량 개인 컨텍스트/지식 저장소입니다.

```
[컨텍스트 로드] → [작업 수행] → [결론 저장]
```

### 기본 경로
| 항목 | 경로 |
|------|------|
| **Contexts** | `~/.opencontext/contexts` |
| **Database** | `~/.opencontext/opencontext.db` |

---

## 2. 설치 및 초기화

### CLI 설치
```bash
npm install -g @aicontextlab/cli
# 또는 npx 사용
npx @aicontextlab/cli <command>
```

### 초기화 (레포 내에서 실행)
```bash
cd your-project
oc init
```

**`oc init` 수행 작업:**
- 글로벌 컨텍스트 저장소 준비 (최초 실행 시)
- 선택한 도구에 대한 user-level commands/skills + mcp.json 생성
- 레포의 AGENTS.md 갱신

---

## 3. Slash Commands

### 초보자 친화 명령어

| Command | 용도 |
|---------|------|
| `/opencontext-help` | 어디서 시작할지 모를 때 |
| `/opencontext-context` | **(기본 권장)** 작업 전 배경 로드 |
| `/opencontext-search` | 기존 문서 검색 |
| `/opencontext-create` | 새 문서/아이디어 작성 |
| `/opencontext-iterate` | 결론 및 인용 저장 |

### 설치 위치
```
# Slash Commands
Cursor:      ~/.cursor/commands
Claude Code: ~/.claude/commands

# Skills
Cursor:      ~/.cursor/skills/opencontext-*/SKILL.md
Claude Code: ~/.claude/skills/opencontext-*/SKILL.md
Codex:       ~/.codex/skills/opencontext-*/SKILL.md

# MCP Config
Cursor:      ~/.cursor/mcp.json
Claude Code: ~/.claude/mcp.json
```

---

## 4. 핵심 CLI 명령어

### 폴더/문서 관리
```bash
# 폴더 목록 조회
oc folder ls --all

# 폴더 생성
oc folder create project-a -d "My project"

# 문서 생성
oc doc create project-a design.md -d "Design doc"

# 문서 목록 조회
oc doc ls project-a
```

### 검색 & 매니페스트
```bash
# 검색 (키워드/하이브리드/벡터)
oc search "your query" --mode keyword --format json

# 매니페스트 생성 (AI가 읽을 파일 목록)
oc context manifest project-a --limit 10
```

### 검색 모드
| 모드 | 설명 | 요구사항 |
|------|------|----------|
| `--mode keyword` | 키워드 기반 검색 | 임베딩 불필요 |
| `--mode vector` | 벡터 검색 | 임베딩 + 인덱스 필요 |
| `--mode hybrid` | 하이브리드 (기본값) | 임베딩 + 인덱스 필요 |

### 임베딩 설정 (시맨틱 검색용)
```bash
# API Key 설정
oc config set EMBEDDING_API_KEY "<<your_key>>"

# (선택) Base URL 설정
oc config set EMBEDDING_API_BASE "https://api.openai.com/v1"

# (선택) 모델 설정
oc config set EMBEDDING_MODEL "text-embedding-3-small"

# 인덱스 빌드
oc index build
```

---

## 5. MCP Tools

### OpenContext MCP Tools
```bash
oc_list_folders    # 폴더 목록 조회
oc_list_docs       # 문서 목록 조회
oc_manifest        # 매니페스트 생성
oc_search          # 문서 검색
oc_create_doc      # 문서 생성
oc_get_link        # 안정적 링크 생성
```

### Multi-Agent 통합
```bash
# Gemini: 대용량 분석
ask-gemini "전체 코드베이스 구조 분석해줘"

# Codex: 명령 실행
shell "docker-compose up -d"

# OpenContext: 결과 저장
oc doc create project-a conclusions.md -d "분석 결론"
```

---

## 6. Multi-Agent 워크플로우 통합

### Orchestration Pattern
```
[Claude] 계획 수립
    ↓
[Gemini] 분석/리서치 + OpenContext 검색
    ↓
[Claude] 코드 작성
    ↓
[Codex] 실행/테스트
    ↓
[Claude] 결과 종합 + OpenContext 저장
```

### 실전 예시: API 설계 + 구현 + 테스트
```bash
# 1. [Claude] 스킬 기반 API 스펙 설계
/opencontext-context   # 프로젝트 배경 로드

# 2. [Gemini] 대용량 코드베이스 분석
ask-gemini "@src/ 기존 API 패턴 분석"

# 3. [Claude] 분석 결과 기반 코드 구현
# (OpenContext에서 로드한 컨텍스트 활용)

# 4. [Codex] 테스트 및 빌드
shell "npm test && npm run build"

# 5. [Claude] 최종 리포트 생성 + 결론 저장
/opencontext-iterate   # 결정사항 및 교훈 저장
```

---

## 7. 권장 일일 워크플로우

### 작업 전 (1분)
```bash
/opencontext-context
```
- 프로젝트 배경 + 알려진 함정 로드

### 작업 중
```bash
/opencontext-search
```
- 불확실할 때 기존 결론 검색

### 작업 후 (2분)
```bash
/opencontext-iterate
```
- 결정사항, 함정, 다음 단계 기록

### 고ROI 문서 유형
- **Acceptance Criteria** - 수락 기준
- **Common Pitfalls** - 자주 발생하는 함정
- **API Contracts** - API 계약
- **Dependency Versions** - 의존성 버전

---

## 8. 안정적 링크 (Stable Links)

문서 ID 기반 참조로 이름/이동에도 링크 유지:

```markdown
[label](oc://doc/<stable_id>)
```

### CLI로 링크 생성
```bash
oc doc link <doc_path>
```

### MCP로 링크 생성
```bash
oc_get_link doc_path="Product/api-spec"
```

---

## 9. Desktop App & Web UI

### Desktop App (권장)
- 네이티브 UI로 컨텍스트 관리/검색/편집
- CLI 없이 사용 가능
- 자동 인덱스 빌드 (백그라운드)

**인용 기능:**
| 액션 | 방법 | 효과 |
|------|------|------|
| 텍스트 스니펫 인용 | 텍스트 선택 → 우클릭 → "Copy Citation" | Agent가 스니펫 + 출처 읽음 |
| 문서 인용 | 문서 제목 옆 인용 아이콘 클릭 | Agent가 전체 문서 + stable_id 획득 |
| 폴더 인용 | 폴더 우클릭 → "Copy Folder Citation" | Agent가 폴더 내 모든 문서 일괄 읽음 |

### Web UI
```bash
oc ui
# 기본 주소: http://127.0.0.1:4321
```

---

## Quick Reference

### 필수 워크플로우
```
작업 전: /opencontext-context (배경 로드)
작업 중: /opencontext-search (검색)
작업 후: /opencontext-iterate (저장)
```

### 핵심 CLI 명령어
```bash
oc init              # 프로젝트 초기화
oc folder ls --all   # 폴더 목록
oc doc ls <folder>   # 문서 목록
oc search "query"    # 검색
oc doc create ...    # 문서 생성
```

### MCP Tools
```
oc_list_folders  폴더 목록
oc_list_docs     문서 목록
oc_search        검색
oc_manifest      매니페스트
oc_create_doc    문서 생성
oc_get_link      링크 생성
```

### 경로
```
~/.opencontext/contexts      컨텍스트 저장소
~/.opencontext/opencontext.db  데이터베이스
```

---

## References

- [OpenContext Website](https://0xranx.github.io/OpenContext/en/)
- [Usage Guide](https://0xranx.github.io/OpenContext/en/usage/)
- [Download Desktop](https://github.com/0xranx/OpenContext/releases)
- [GitHub Repository](https://github.com/0xranx/OpenContext)
