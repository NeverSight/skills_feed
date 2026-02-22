---
name: cocos-mcp-setup
description: Cocos 프로젝트에 MCP 서버 설치
allowed-tools: Bash(ls:*), Bash(git:*), Bash(npm install:*)
---

Cocos Creator 프로젝트에 cocos-mcp-server 플러그인을 설치합니다.

## 상수

- **Git 저장소**: `https://github.com/TinycellCorp/cocos-mcp-server.git`
- **설치 경로**: `extensions/cocos-mcp-server`

## 절차

### 1. Cocos Creator 프로젝트 확인

현재 디렉토리에 `assets/` 폴더가 있는지 확인합니다.

```bash
ls assets/
```

- 없으면: "현재 디렉토리가 Cocos Creator 프로젝트가 아닙니다. Cocos Creator 프로젝트 루트에서 실행해주세요." 안내 후 **중단**

### 2. 플러그인 설치

`extensions/cocos-mcp-server/package.json` 존재 여부에 따라 분기합니다.

```bash
ls extensions/cocos-mcp-server/package.json
```

#### 이미 있는 경우 (업데이트)

"기존 설치가 감지되었습니다. 업데이트합니다." 안내 후 pull합니다.

```bash
git -C extensions/cocos-mcp-server pull
```

#### 없는 경우 (신규 설치)

```bash
git clone https://github.com/TinycellCorp/cocos-mcp-server.git extensions/cocos-mcp-server
```

- 오류 시: "플러그인 설치에 실패했습니다." 안내 후 **중단**

### 3. 의존성 설치

`--prefix` 옵션으로 대상 디렉토리를 지정합니다. (`cd` 사용 금지 - allowed-tools 매칭 보장)

```bash
npm install --production --prefix extensions/cocos-mcp-server
```

- 오류 시: "npm install에 실패했습니다." 안내 후 **중단**

### 4. 결과 안내

모든 단계가 완료되면 다음을 출력합니다:

```
## 설치 완료

플러그인: extensions/cocos-mcp-server/

### 다음 단계

1. Cocos Creator 에디터에서 프로젝트를 열고 Extension 패널에서 MCP 서버를 시작하세요.
2. 에디터에서 설정한 포트 번호를 확인한 뒤 아래 명령어로 MCP 서버를 등록하세요.

MCP 헬스체크:
  curl http://127.0.0.1:{포트}/mcp

MCP 등록:
  claude mcp add --transport http --scope local cocos-creator http://127.0.0.1:{포트}/mcp
```

## 오류 처리

- 각 단계에서 오류 발생 시 다른 방법으로 재시도하지 **않습니다**
- 오류 내용을 그대로 사용자에게 보여주고 **즉시 중단**합니다
