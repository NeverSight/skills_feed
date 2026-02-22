---
name: smilegate-connector
description: 스마일게이트 업무 도구(Slack, Jira, Confluence)를 Claude Code에 연결하는 설정 가이드. 비개발자도 따라할 수 있도록 단계별로 안내한다. "커넥터", "connector", "MCP 설정", "jira 연결", "confluence 연결", "slack 연결" 요청에 사용.
triggers:
  - "커넥터"
  - "connector"
  - "커넥터 설정"
  - "MCP 설정"
  - "jira 연결"
  - "confluence 연결"
  - "slack 연결"
  - "스마일게이트 커넥터"
---

# Smilegate Connector

스마일게이트 업무 도구를 Claude Code에 연결하는 설정 스킬.
비개발자도 따라할 수 있도록 단계별로 안내한다.

## 연결 대상

| 서비스 | 연결 방식 | 난이도 |
|--------|----------|--------|
| Slack | Connectors (클릭만) | 쉬움 |
| Jira | MCP (토큰 발급 필요) | 보통 |
| Confluence | MCP (토큰 발급 필요) | 보통 |

## 실행 흐름

이 스킬이 트리거되면 아래 순서로 진행한다.

**링크 출력 규칙**: 모든 URL은 코드 블록 밖에서 마크다운 링크 형식 `[텍스트](URL)` 으로 표시한다. 코드 블록 안에 URL을 절대 넣지 않는다. 코드 블록 안의 URL은 클릭이 불가능하고 줄바꿈이 발생할 수 있다.

### Phase 0: 현재 연결 상태 진단

스킬 시작 시 먼저 현재 연결 상태를 진단한다.

확인 방법:
1. ToolSearch로 `+slack read` 검색 → Slack 연결 여부 확인
2. ToolSearch로 `+jira test` 검색 → Jira MCP 존재 여부 확인
3. ToolSearch로 `+confluence test` 검색 → Confluence MCP 존재 여부 확인

진단 결과를 테이블로 보여준다:

```
현재 연결 상태:
  Slack:      ✅ 연결됨 / ❌ 미연결
  Jira:       ✅ 연결됨 / ❌ 미연결
  Confluence: ✅ 연결됨 / ❌ 미연결
```

이미 연결된 서비스는 건너뛴다. 미연결 서비스만 설정을 진행한다.
모두 연결되어 있으면 "모든 서비스가 연결되어 있습니다!"를 출력하고 기본 사용법을 안내한다.

AskUserQuestion으로 어떤 서비스를 설정할지 선택받는다 (multiSelect: true).

### Phase 1: Slack 연결 (Connectors)

Slack은 가장 쉽다. 브라우저에서 클릭 몇 번이면 끝.

안내 사항:
```
Slack 연결 방법:

① 아래 링크를 브라우저에서 열어주세요:
   👉 https://claude.ai/settings

② 왼쪽 메뉴에서 "커넥터 둘러보기"를 클릭하세요

③ 목록에서 "Slack"을 찾아 클릭하세요

④ Slack 로그인 화면이 나오면 로그인하세요
   (이미 로그인되어 있으면 자동으로 넘어갑니다)

⑤ "허용" 버튼을 클릭하세요

⑥ 끝! 이제 Claude Code에서 Slack을 사용할 수 있습니다.
```

주의 사항:
- Claude Code에서 로그인한 계정과 claude.ai 계정이 동일해야 한다
- 회사 Slack 워크스페이스 관리자가 앱 설치를 승인해야 할 수 있다

연결 확인:
- ToolSearch로 slack 도구를 검색하여 사용 가능한지 확인
- `mcp__claude_ai_Slack__slack_search_channels(query="general")` 호출로 실제 테스트

AskUserQuestion으로 완료 여부를 확인한 뒤 다음 Phase로 이동한다.

### Phase 2: Jira & Confluence 연결 (MCP)

Jira와 Confluence는 동일한 패턴으로 PAT(개인 액세스 토큰)를 발급받아 연결한다.
**두 서비스 모두 선택한 경우, 토큰을 모두 먼저 발급받고 한번에 설정한다.**

#### Step 1: 토큰 발급 안내

선택한 서비스에 해당하는 토큰 발급 안내를 모두 출력한다.

##### Jira 토큰 발급 (Jira 선택 시)

아래 내용을 코드 블록 없이 마크다운으로 출력한다. URL은 반드시 마크다운 링크 형식으로 한 줄에 표시한다:

Jira 토큰 발급 방법:

① 아래 링크를 브라우저에서 열어주세요:
   👉 [Jira 토큰 발급 페이지](https://jira.smilegate.net/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens)

② "Create token" 버튼을 클릭하세요

③ 토큰 이름을 입력하세요 (예: "Claude Code 연동용")

④ ⚠️ "만료 날짜" 옵션에서 **자동 만료를 해제**하는 것을 권장합니다 (체크 해제)
   자동 만료가 켜져 있으면 일정 기간 후 토큰이 무효화되어 재발급이 필요합니다.

⑤ "Create" 버튼을 클릭하세요

⑥ ⚠️ 생성된 토큰을 반드시 복사하세요!
   토큰은 이 화면에서만 볼 수 있고, 나중에 다시 확인할 수 없습니다.

##### Confluence 토큰 발급 (Confluence 선택 시)

아래 내용을 코드 블록 없이 마크다운으로 출력한다. URL은 반드시 마크다운 링크 형식으로 한 줄에 표시한다:

Confluence 토큰 발급 방법:

① 아래 링크를 브라우저에서 열어주세요:
   👉 [Confluence 토큰 발급 페이지](https://wiki.smilegate.net/plugins/personalaccesstokens/usertokens.action)

② "토큰 만들기(Create token)" 버튼을 클릭하세요

③ 토큰 이름을 입력하세요 (예: "Claude Code 연동용")

④ ⚠️ "만료 날짜" 옵션에서 **자동 만료를 해제**하는 것을 권장합니다 (체크 해제)
   자동 만료가 켜져 있으면 일정 기간 후 토큰이 무효화되어 재발급이 필요합니다.

⑤ "만들기(Create)" 버튼을 클릭하세요

⑥ ⚠️ 생성된 토큰을 반드시 복사하세요!
   토큰은 이 화면에서만 볼 수 있고, 나중에 다시 확인할 수 없습니다.

#### Step 2: 사용자 정보 입력

토큰 발급 안내 직후, AskUserQuestion으로 필요한 정보를 순서대로 입력받는다.
"준비됐나요?" 같은 중간 확인 단계 없이 바로 붙여넣기를 유도한다.

- 사용자 ID 질문 (Jira/Confluence 공통):
  - question: "사용자 ID를 입력해주세요 (Jira/Confluence 공통, 예: hyuntkim)"
  - options: [
      {label: "3번(Other)을 선택해서 입력", description: "아래 Other를 선택한 뒤 사용자 ID를 입력하세요"},
      {label: "잘 모르겠어요", description: "Jira 또는 Confluence에 로그인할 때 사용하는 ID입니다"}
    ]

- Jira PAT 토큰 질문 (Jira 선택 시):
  - question: "발급받은 Jira PAT 토큰을 붙여넣어 주세요"
  - options: [
      {label: "3번(Other)을 선택해서 토큰 붙여넣기", description: "아래 Other를 선택한 뒤 복사한 Jira 토큰을 붙여넣으세요"},
      {label: "아직 발급 안 했어요", description: "위의 토큰 발급 안내를 따라 먼저 토큰을 발급받으세요"}
    ]

- Confluence PAT 토큰 질문 (Confluence 선택 시):
  - question: "발급받은 Confluence PAT 토큰을 붙여넣어 주세요"
  - options: [
      {label: "3번(Other)을 선택해서 토큰 붙여넣기", description: "아래 Other를 선택한 뒤 복사한 Confluence 토큰을 붙여넣으세요"},
      {label: "아직 발급 안 했어요", description: "위의 토큰 발급 안내를 따라 먼저 토큰을 발급받으세요"}
    ]

**중요**: 토큰은 민감정보이므로 대화 내용에 그대로 노출하지 않는다.
입력받은 즉시 `~/.claude.json`에 저장하고, 대화에서는 마스킹하여 표시한다.

#### Step 3: ~/.claude.json 업데이트

`~/.claude.json` 파일의 `mcpServers` 키에 선택한 서비스를 **한번에** 추가한다.

먼저 Read 도구로 `~/.claude.json`을 읽고, `mcpServers` 객체 안에 아래 형식으로 추가한다:

Jira 선택 시:
```json
"jira": {
  "type": "http",
  "url": "http://mcp.sginfra.net/confluence-jira-mcp",
  "headers": {
    "x-confluence-jira-username": "{사용자ID}",
    "x-confluence-jira-token": "{PAT토큰}"
  }
}
```

Confluence 선택 시:
```json
"confluence": {
  "type": "http",
  "url": "http://mcp.sginfra.net/confluence-wiki-mcp",
  "headers": {
    "x-confluence-wiki-username": "{사용자ID}",
    "x-confluence-wiki-token": "{PAT토큰}"
  }
}
```

추가 후 사용자에게 아래 내용을 코드 블록 없이 출력한다:

~/.claude.json의 mcpServers에 {설정한 서비스 목록} 설정이 추가되었습니다!

MCP 설정을 적용하려면 **Claude Code를 재시작**해야 합니다:

| OS | 재시작 방법 |
|-----|------------|
| Mac | `Cmd + R` |
| Windows / Linux | `Ctrl + R` |

재시작하면 현재 대화가 종료됩니다. 이어서 연결 테스트를 하려면:
→ Claude Code가 다시 열린 후 `/resume` 을 입력하면 **직전 대화를 이어서** 진행할 수 있습니다.

재시작 후 돌아오시면 연결 테스트를 진행합니다!

#### Step 4: 재시작 및 연결 테스트

사용자가 재시작을 완료했다고 (또는 `/resume`으로 돌아왔다고) 알려주면 선택한 서비스의 연결을 모두 테스트한다.

Jira 테스트:
- `mcp__jira__test_jira_connection()` 호출
- 성공하면: 사용자 이름, Jira URL 등 연결 정보 표시
- 실패하면: 에러 메시지와 함께 트러블슈팅 안내

Confluence 테스트:
- `mcp__confluence__test_confluence_connection()` 호출
- 성공하면: 연결 정보 표시
- 실패하면: 트러블슈팅 안내

트러블슈팅:
```
연결 실패 시 확인할 것:
1. Claude Code를 재시작했는지 (설정 변경 후 재시작 필수)
2. 토큰이 올바르게 복사되었는지 (~/.claude.json 열어서 mcpServers 확인)
3. 사용자 ID가 맞는지 (Jira/Confluence 프로필에서 확인)
4. 네트워크에서 mcp.sginfra.net 접근이 가능한지 (사내망 또는 VPN 필요)
```

### Phase 3: 완료 리포트

모든 설정이 끝나면 최종 상태를 요약한다:

```
🎉 스마일게이트 커넥터 설정 완료!

연결 상태:
  Slack:      ✅ 연결됨 (Connectors)
  Jira:       ✅ 연결됨 (jira.smilegate.net)
  Confluence: ✅ 연결됨 (wiki.smilegate.net)

기본 사용법:

  Slack:
    "Slack에서 #general 채널 최근 메시지 보여줘"
    "Slack에서 '배포' 관련 메시지 검색해줘"

  Jira:
    "나한테 할당된 Jira 이슈 보여줘"
    "PROJ-123 이슈 상태 알려줘"
    "이번 주 마감인 이슈 목록 정리해줘"

  Confluence:
    "최근 업데이트된 Wiki 페이지 보여줘"
    "'프로젝트 계획' 관련 문서 검색해줘"
    "이 Wiki 페이지 내용 요약해줘: (페이지 URL)"

💡 팁: 토큰이 만료되면 이 스킬을 다시 실행하세요!
   "커넥터 설정해줘" 한 마디면 됩니다.
```

## 참고 정보

| 항목 | 값 |
|------|-----|
| Jira MCP 서버 | `http://mcp.sginfra.net/confluence-jira-mcp` |
| Confluence MCP 서버 | `http://mcp.sginfra.net/confluence-wiki-mcp` |
| Jira 토큰 발급 | https://jira.smilegate.net/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens |
| Confluence 토큰 발급 | https://wiki.smilegate.net/plugins/personalaccesstokens/usertokens.action |
| Slack Connectors | https://claude.ai/settings |
| 공식 설치 가이드 | https://wiki.smilegate.net/pages/viewpage.action?pageId=589459355 |

## MCP 설정 위치

Jira/Confluence MCP는 항상 **전역 설정 파일**에 추가한다:

| 파일 | 역할 |
|------|------|
| `~/.claude.json` | Claude Code 전역 설정 파일. `mcpServers` 키에 MCP 서버를 등록 |

> `~/.claude.json`에 저장하면 모든 프로젝트에서 Jira/Confluence를 사용할 수 있다.
> Git 저장소 밖에 있으므로 토큰이 실수로 커밋될 위험이 없다.
