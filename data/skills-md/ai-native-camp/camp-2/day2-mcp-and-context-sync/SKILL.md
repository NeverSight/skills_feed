---
name: day2-mcp-and-context-sync
description: AI Native Camp Day 2 MCP & Context Sync. MCP를 배우고 나만의 Context Sync 스킬을 만든다. "2일차", "Day 2", "MCP", "context sync" 요청에 사용.
---

# Day 2: MCP & Context Sync

이 스킬이 호출되면 아래 **STOP PROTOCOL**을 반드시 따른다.

---

## 용어 정리

이 스킬에서 사용하는 핵심 용어:

| 용어 | 설명 |
|------|------|
| **MCP** | Model Context Protocol. AI와 외부 도구를 연결하는 오픈 표준. USB-C처럼 다양한 서비스를 하나의 규격으로 연결 |
| **Host / Client / Server** | MCP의 3요소. Host=AI 앱(Claude Code), Client=연결 관리자, Server=외부 도구 제공자 |
| **Transport** | MCP 서버 연결 방식. HTTP(클라우드 서비스)와 stdio(로컬 실행) 2가지 |
| **Plugin** | Skill + MCP + Hook + Agent를 묶은 패키지. 설치 한 줄이면 MCP 서버까지 자동 연결 |
| **subagent** | Claude가 다른 Claude를 불러서 일을 시키는 것. 여러 일을 동시에 처리할 때 사용 |
| **Explore 에이전트** | 프로젝트 폴더 구조를 파악해주는 전문 subagent. 읽기 전용 |
| **API** | 서비스가 제공하는 데이터 창구. MCP가 없을 때 직접 코드로 데이터를 가져오는 방법 |
| **스킬(Skill)** | Claude Code에게 특정 작업 방법을 가르치는 문서. Day 1 Block 3-2에서 체험한 것 |
| **STUB** | 나중에 채울 빈칸. "여기에 나중에 내용이 들어갑니다"라는 표시. Part B에서 블록마다 하나씩 채워나간다 |
| **스켈레톤** | 빈칸(STUB)만 있는 뼈대. 건물로 치면 철골 구조만 세운 상태 |
| **frontmatter** | 파일 맨 위에 `---`로 감싼 정보 영역. 스킬의 이름, 설명, 트리거 등을 적는 곳 |
| **YAML / JSON** | 데이터를 정리하는 형식. 엑셀이 표로 데이터를 정리하듯, 텍스트로 정리하는 방식 |
| **CLI** | Command Line Interface. 터미널에 직접 명령어를 입력하는 방식 |

---

## STOP PROTOCOL — 절대 위반 금지

> 이 프로토콜은 이 스킬의 최우선 규칙이다.
> 아래 규칙을 위반하면 수업이 망가진다.

### 각 블록은 반드시 2턴에 걸쳐 진행한다

```
┌─ Phase A (첫 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 EXPLAIN 섹션을 읽는다    │
│ 2. 기능을 설명한다                                        │
│ 3. references/에서 해당 블록 파일의 EXECUTE 섹션을 읽는다    │
│ 4. "지금 직접 실행해보세요"라고 안내한다                     │
│ 5. ⛔ 여기서 반드시 STOP. 턴을 종료한다.                    │
│                                                          │
│ ❌ 절대 하지 않는 것: 퀴즈 출제, QUIZ 섹션 읽기             │
│ ❌ 절대 하지 않는 것: AskUserQuestion 호출 (Block 6,7,8,9,10 제외)│
│ ❌ 절대 하지 않는 것: "실행해봤나요?" 질문                   │
└──────────────────────────────────────────────────────────┘

  ⬇️ 사용자가 돌아와서 "했어", "완료", "다음" 등을 입력한다

┌─ Phase B (두 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 QUIZ 섹션을 읽는다       │
│ 2. AskUserQuestion으로 퀴즈를 출제한다                     │
│ 3. 정답/오답 피드백을 준다                                 │
│ 4. 다음 블록으로 이동할지 AskUserQuestion으로 묻는다         │
│ 5. ⛔ 다음 블록을 시작하면 다시 Phase A부터.                │
└──────────────────────────────────────────────────────────┘
```

### 핵심 금지 사항 (절대 위반 금지)

1. **Phase A에서 AskUserQuestion을 호출하지 않는다 (Block 6, 7, 8, 9, 10 제외)** — 이 5개 블록은 사용자 선택/확인이 필수이므로 예외
2. **Phase A에서 퀴즈를 내지 않는다** — QUIZ 섹션은 Phase B에서만 읽는다
3. **Phase A에서 "실행해봤나요?"를 묻지 않는다** — 사용자가 먼저 말할 때까지 기다린다
4. **한 턴에 EXPLAIN + QUIZ를 동시에 하지 않는다** — 반드시 2턴으로 나눈다

### 공식 문서 URL 출력 (절대 누락 금지)

모든 블록의 Phase A 시작 시, 해당 reference 파일 상단의 `> 공식 문서:` URL을 **반드시 그대로 출력**한다.

```
📖 공식 문서: [URL]
```

- reference 파일에 URL이 여러 개 있으면 전부 출력한다
- URL을 요약하거나 생략하지 않는다
- 참가자가 직접 클릭해서 공식 문서를 볼 수 있어야 한다

### Phase A 종료 시 필수 문구

Phase A의 마지막에는 반드시 아래 형태의 문구를 출력하고 Stop한다:

```
---
👆 위 내용을 직접 실행해보세요.
실행이 끝나면 "완료" 또는 "다음"이라고 입력해주세요.
```

이 문구 이후에 어떤 도구 호출(AskUserQuestion 포함)이나 추가 텍스트도 출력하지 않는다.

---

## 소요 시간

| Part | 블록 | 예상 시간 |
|------|------|----------|
| Part A: MCP 딥다이브 | Block 0~4 | ~60분 |
| Part B: Context Sync 스킬 만들기 | Block 5~10 | ~110분 |
| **합계** | **Block 0~10** | **~170분** |

---

## 핵심 전략

### Part A: MCP 개념부터 Plugin까지 체계적으로 배우기

MCP의 개념(Block 0)부터 시작해서, 서버 추가(Block 1), 도구 탐색(Block 2), 인기 서버 설치(Block 3), Plugin으로 확장(Block 4)까지 순서대로 진행한다.

### Part B: 4개 도구 × 4가지 연결 방법 — 점진적 빌드

아래 방식으로 진행한다:

1. Block 5에서 `templates/context-sync.md` 기반으로 **4개 소스 STUB이 포함된 스켈레톤** 스킬 파일을 생성한다
2. Block 6~9에서 **블록마다 하나의 도구를 다른 연결 방법으로** 연결하고, 해당 소스 STUB을 실제 내용으로 채운다
3. Block 10에서 실행 흐름 + 출력 포맷을 완성하고, 전체 스킬을 실행한다

> **핵심**: 4개 도구를 일괄 연결하는 것이 아니라, 블록마다 **다른 연결 방식**을 실습한다.

#### Part B 블록 구조

| Block | 연결 방법 | 도구 | 난이도 | 시간 |
|-------|----------|------|--------|------|
| 5 | — | 전체 | — | ~12min |
| 6 | claude.ai Connector | Slack | ★☆☆☆ | ~15min |
| 7 | `claude mcp add` | Notion | ★★☆☆ | ~18min |
| 8 | Official Plugin (`/plugin`) | Linear | ★★★☆ | ~15min |
| 9 | 커뮤니티 Plugin (구조 분석) | Google Calendar/Gmail | ★★★★ | ~20min |
| 10 | — (병렬 수집 + Output + 마무리) | 전체 | — | ~20min |

#### 점진적 빌드 — 템플릿 채움 순서

```
Block 5:  [STUB] [STUB] [STUB] [STUB] [STUB흐름] [STUB포맷]
Block 6:  [Slack] [STUB] [STUB] [STUB] [STUB흐름] [STUB포맷]
Block 7:  [Slack] [Notion] [STUB] [STUB] [STUB흐름] [STUB포맷]
Block 8:  [Slack] [Notion] [Linear] [STUB] [STUB흐름] [STUB포맷]
Block 9:  [Slack] [Notion] [Linear] [Google] [STUB흐름] [STUB포맷]
Block 10: [Slack] [Notion] [Linear] [Google] [완성흐름] [완성포맷] → 실행!
```

#### 블록-소스 매핑

| Block | 채우는 소스 | 연결 방법 | 스킬 파일 변경 영역 |
|-------|-----------|----------|------------------|
| 5 | — (골격 생성) | — | 전체 스켈레톤 생성 |
| 6 | 소스 1: Slack | Connector | 소스 1 STUB → 실제 내용 |
| 7 | 소스 2: Notion | `claude mcp add` | 소스 2 STUB → 실제 내용 |
| 8 | 소스 3: Linear | `/plugin install` | 소스 3 STUB → 실제 내용 |
| 9 | 소스 4: Google | 커뮤니티 Plugin | 소스 4 STUB → 실제 내용 |
| 10 | — (완성 + 실행) | — | 실행 흐름 + 출력 포맷 완성 |

---

## 블록 특수 규칙

### Part A (Block 0~4)

- **Block 4 [BONUS]**: 시간이 남을 때만 진행한다
- Block 3 완료 후 Part A 마무리 안내 → Part B 전환 안내
- Part A에서 배운 MCP 지식이 Part B의 도구 연결(Block 7)에서 직접 활용된다

### Part B (Block 5~10)

- **Block 5 (스켈레톤 생성)**: Phase A에서 Context Sync 개념 + 4가지 연결 방법 소개 + Explore로 프로젝트 탐색 + `templates/context-sync.md` 기반 스켈레톤 생성 → Stop. Phase B에서 퀴즈.
- **Block 6 (Connector → Slack)**: Phase A에서 Connector 개념 설명 + Slack Connector 연결 안내 + 테스트 + 스킬 소스 1 채우기 → Stop. Phase B에서 퀴즈.
- **Block 7 (mcp add → Notion)**: Phase A에서 `claude mcp add` 설명 + AskUserQuestion으로 Notion 확인 + MCP 서버 등록 + 테스트 + 스킬 소스 2 채우기 → Stop. Phase B에서 퀴즈.
- **Block 8 (Plugin → Linear)**: Phase A에서 Plugin 개념 설명 + `/plugin install linear` + MCP 자동 등록 확인 + 테스트 + 스킬 소스 3 채우기 → Stop. Phase B에서 퀴즈.
- **Block 9 (커뮤니티 Plugin → Google)**: Phase A에서 Plugin 구조 분석 + AskUserQuestion으로 Calendar/Gmail 선택 + Explore로 Plugin 구조 탐색 + 설치 + 스킬 소스 4 채우기 → Stop. Phase B에서 퀴즈.
- **Block 10 (병렬 수집 + Output + 마무리)**: Phase A에서 AskUserQuestion으로 출력 형식 선택 + 실행 흐름/출력 포맷 완성 + 4개 소스 병렬 수집 실행 + 결과 확인 → Stop. Phase B에서 종합 퀴즈 + 마무리.

#### AskUserQuestion 예외 블록

| Block | 이유 |
|-------|------|
| Block 6 | Slack 사용 여부 확인 (회사 계정 제한 시 대안 안내) |
| Block 7 | Notion workspace 사용 여부 확인 |
| Block 8 | Linear 사용 여부 확인 (미사용 시 대안 Plugin 안내) |
| Block 9 | Google Calendar vs Gmail vs 둘 다 선택 |
| Block 10 | Output format 선택 |

#### Block 6 예외 규칙

Block 6의 Phase A는 **AskUserQuestion을 사용**한다. Slack 사용 여부와 연결 가능 여부를 확인해야 한다.

Slack 사용 시:
1. claude.ai/settings/connectors에서 Slack Connector 연결
2. `/mcp`로 claude.ai 섹션에 등록 확인
3. 연결 테스트 후 스킬 소스 1 채우기

Slack 미사용 또는 회사 계정 제한 시 (Plan B):
1. 개인 Slack workspace나 AI Native Camp Slack으로 연결
2. Connector 연결 방식 자체를 체험하는 것이 핵심임을 안내

> ⚠️ 보안 안내: 회사 Slack은 관리자 정책상 외부 앱 연결이 차단될 수 있다. 이 경우 개인 workspace를 사용한다.

#### Block 7 예외 규칙

Block 7의 Phase A는 **AskUserQuestion을 사용**한다. Notion 사용 여부를 확인해야 한다.

**핵심 원칙: Claude가 설정을 대신 수행하고, 사용자는 결과를 확인한다.**

Notion 사용 시:
1. `claude mcp add --transport http notion https://mcp.notion.com/mcp` 실행
2. `/mcp`로 local 섹션에 등록 확인
3. 연결 테스트 후 스킬 소스 2 채우기

Notion 미사용 시 (Plan B):
1. `scripts/mcp_servers.py`를 사용하여 대체 MCP 서버 검색
2. 검색 결과에서 선택하여 `claude mcp add`로 등록

#### Block 8 예외 규칙

Block 8의 Phase A는 **AskUserQuestion을 사용**한다. Linear 사용 여부를 확인해야 한다.

Linear 사용 시:
1. `/plugin install linear` 실행
2. `/mcp`로 local 섹션에 Linear MCP 자동 등록 확인
3. 연결 테스트 후 스킬 소스 3 채우기

Linear 미사용 시 (Plan B):
1. `/plugin` 명령어로 설치 가능한 다른 공식 Plugin 목록 확인
2. 사용 중인 도구의 Plugin이 있으면 그것을 설치
3. Plugin이 없으면 Block 8은 skip하고 Block 9로 이동 가능
4. **핵심**: Plugin 설치 → MCP 자동 등록이라는 과정을 체험하는 것이 목표

> ⚠️ Plugin 설치 후 Claude Code 재시작이 필요할 수 있다. MCP 연결이 안 보이면 Claude Code를 재시작한다.

#### Block 9 예외 규칙

Block 9의 Phase A는 **AskUserQuestion을 사용**한다. Google Calendar vs Gmail vs 둘 다를 선택해야 한다.

Phase A 진행 순서:
1. `references/block9-skill-google.md`의 EXPLAIN 섹션을 읽고 Plugin 구조를 설명한다
2. `/plugin marketplace add team-attention/plugins-for-claude-natives` 실행
3. AskUserQuestion으로 Calendar/Gmail/둘 다/Skip 선택
4. Explore 에이전트로 Plugin 디렉토리 구조 탐색 + 설명
5. 선택한 도구 Plugin 설치 + 테스트 + 스킬 소스 4 채우기 → Stop

#### Block 10 예외 규칙

Block 10의 Phase A는 **AskUserQuestion을 사용**한다. Output format을 선택해야 한다.

---

## References 파일 맵

### Part A: MCP 딥다이브

| 블록 | 파일 | 주제 |
|------|------|------|
| Block 0 | `references/block0-concept.md` | MCP 개념 이해 |
| Block 1 | `references/block1-add-server.md` | MCP 서버 추가하기 |
| Block 2 | `references/block2-mcp-command.md` | /mcp 명령어로 도구 탐색 |
| Block 3 | `references/block3-popular-servers.md` | 인기 MCP 서버 탐색 및 설치 |
| Block 4 [BONUS] | `references/block4-plugin-mcp.md` | /plugin으로 MCP 확장 |

### Part B: Context Sync 스킬 만들기 (4개 도구 × 4가지 연결 방법)

| 블록 | 파일 | 주제 |
|------|------|------|
| Block 5 | `references/block5-template-creation.md` | Context Sync 개념 + Explore + 스켈레톤 생성 |
| Block 6 | `references/block6-connector-slack.md` | Connector로 Slack 연결 + 스킬 소스 1 채우기 |
| Block 7 | `references/block7-mcp-add-notion.md` | `claude mcp add`로 Notion 연결 + 스킬 소스 2 채우기 |
| Block 8 | `references/block8-plugin-linear.md` | `/plugin install`로 Linear 연결 + 스킬 소스 3 채우기 |
| Block 9 | `references/block9-skill-google.md` | Plugin 구조 분석 + Google 연결 + 스킬 소스 4 채우기 |
| Block 10 | `references/block10-finalize.md` | 병렬 수집 + Output 선택 + 최종 실행 + 마무리 |

> 파일 경로는 이 SKILL.md 기준 상대경로다.
> 각 reference 파일은 `## EXPLAIN`, `## EXECUTE`, `## QUIZ` 섹션으로 구성된다.

---

## Templates / Scripts 파일 맵

| 파일 | 용도 |
|------|------|
| `templates/context-sync.md` | Context Sync 스킬 기본 템플릿 (Slack, Notion, Gmail, GCal 4종 포함) |
| `scripts/mcp_servers.py` | GitHub에서 MCP 서버 검색 + README.md 파싱 + 설치 안내 |

> Gmail/Calendar 등의 수집 스크립트는 Block 7에서 Claude가 사용자의 선택에 맞춰 직접 작성한다.

---

## 진행 규칙

- 한 번에 한 블록씩 진행한다
- "다음", "skip", 블록 번호/이름으로 이동한다
- BONUS 블록(Block 4)은 시간이 남을 때만 진행한다
- Part A(Block 0~4) 완료 후 Part B(Block 5~10)로 자연스럽게 전환한다. Part A에서 배운 MCP 지식이 Part B의 도구 연결(Block 6~9)에서 직접 활용된다
- Block 5에서 생성한 스켈레톤 스킬 파일의 STUB을 Block 6~9에서 하나씩 채운다. 각 블록에서 도구를 연결한 뒤 해당 소스 섹션을 실제 내용으로 교체한다
- 사용자 프로젝트의 `.claude/skills/my-context-sync/` 디렉토리에 스킬을 생성한다
- Block 6~9에서 각각 Connector, mcp add, Plugin, 커뮤니티 Plugin을 통해 다른 연결 방식을 실습한다
- Explore 에이전트와 subagent 사용이 핵심이므로 적극 활용한다
- Claude Code 관련 질문이 오면 claude-code-guide 에이전트(내장 도구)로 답변한다. 답변 후 사용자가 직접 따라할 수 있게 단계별로 안내하고, 질문할 때는 AskUserQuestion을 사용한다. 내장 에이전트 답변이 부정확하다고 판단되면, 공식 문서를 `curl`로 파일에 저장한 뒤 Read 툴로 꼼꼼히 읽고 정확한 정보로 다시 답한다

---

## 시작

스킬 시작 시 **먼저 최신 커리큘럼을 설치**한 뒤 블록을 선택한다.

### Step 1: 최신 스킬 설치

아래 명령어를 출력하고 Bash로 실행한다:

```bash
npx skills add ai-native-camp/camp-2 --agent claude-code --yes
```

실행 결과를 간략히 안내한다 (예: "스킬이 최신 버전으로 설치되었습니다").

### Step 2: 블록 선택

아래 테이블을 보여주고 AskUserQuestion으로 어디서 시작할지 물어본다.

**Part A: MCP 딥다이브**

| Block | 주제 | 내용 |
|-------|------|------|
| 0 | MCP 개념 | MCP가 뭔지, USB-C 비유, 아키텍처 |
| 1 | 서버 추가 | `claude mcp add`로 실제 서버 연결 |
| 2 | /mcp 탐색 | 연결된 서버와 도구 목록 확인 |
| 3 | 인기 서버 | 공식 목록에서 유용한 서버 설치 |
| 4 [BONUS] | Plugin + MCP | /plugin으로 MCP 포함 플러그인 설치 |

**Part B: 나만의 Context Sync 스킬 만들기 (4개 도구 × 4가지 연결 방법)**

| Block | 연결 방법 | 도구 | 내용 |
|-------|----------|------|------|
| 5 | — | 전체 | Context Sync 개념 + 스켈레톤 생성 |
| 6 | Connector | Slack | 브라우저 클릭으로 Slack 연결 |
| 7 | `claude mcp add` | Notion | CLI 명령어로 Notion 연결 |
| 8 | Plugin (`/plugin`) | Linear | 공식 Plugin으로 Linear 연결 |
| 9 | 커뮤니티 Plugin | Google | Plugin 구조 분석 + Google 연결 |
| 10 | — | 전체 | 병렬 수집 + Output + 최종 실행 |

```json
AskUserQuestion({
  "questions": [{
    "question": "Day 2: MCP & Context Sync\n\n어디서부터 시작할까요?",
    "header": "시작 블록",
    "options": [
      {"label": "Part A: MCP 개념 (Block 0)", "description": "MCP가 뭔지, 왜 필요한지부터 시작"},
      {"label": "Part A: 서버 추가 (Block 1)", "description": "MCP 개념을 알고 있어서 실습부터"},
      {"label": "Part B: 스켈레톤 생성 (Block 5)", "description": "MCP를 이미 알고 있어서 스킬 만들기부터"},
      {"label": "Part B: Notion 연결 (Block 7)", "description": "Slack은 연결했고, mcp add로 Notion 연결부터"}
    ],
    "multiSelect": false
  }]
})
```

> 시작 블록 선택 후 → 해당 블록의 Phase A부터 진행한다.
