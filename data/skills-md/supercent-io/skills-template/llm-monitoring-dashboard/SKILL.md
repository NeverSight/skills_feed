---
name: llm-monitoring-dashboard
description: PM용 관리자 대시보드에 LLM 사용 모니터링 페이지를 자동 생성. Tokuin CLI 기반 토큰/비용/레이턴시 추적 + 사용자 랭킹 시스템 + 비사용자 추적 + 데이터 기반 PM 인사이트 자동 생성 + Cmd+K 글로벌 검색 + 사용자별 드릴다운 링크 탐색 포함. OpenAI/Anthropic/Gemini/OpenRouter 지원.
tags: [LLM, monitoring, dashboard, tokuin, pm-insights, ranking, user-tracking, cost-tracking, Next.js, React, admin]
platforms: [Claude, ChatGPT, Gemini, Codex]
---

# LLM 사용 모니터링 대시보드

> **Tokuin CLI** 기반으로 LLM API 비용·토큰·레이턴시를 추적하고,  
> PM에게 데이터 기반 인사이트를 제공하는 관리자 대시보드를 자동 생성합니다.

---

## When to use this skill

- **LLM 비용 가시성 확보**: 팀/개인별 API 사용 비용을 실시간 모니터링하고 싶을 때
- **PM 보고용 대시보드 필요**: 누가 얼마나 어떻게 AI를 쓰는지 주간 리포트가 필요할 때
- **사용자 채택률 관리**: 비사용자를 추적하고 AI 도입률을 높이고 싶을 때
- **모델 최적화 근거 마련**: 데이터 기반으로 모델 전환/비용 절감 의사결정이 필요할 때
- **관리자 대시보드에 모니터링 탭 추가**: 기존 Admin 페이지에 LLM 모니터링 섹션을 붙일 때

---

## Prerequisites

### 1. Tokuin CLI 설치 확인

```bash
# 설치 여부 확인
which tokuin && tokuin --version || echo "미설치 — Step 1 먼저 실행"
```

### 2. 환경 변수 (실제 API 호출 시만 필요)

```bash
# .env 파일에 저장 (절대 코드에 직접 입력 금지)
OPENAI_API_KEY=sk-...          # OpenAI
ANTHROPIC_API_KEY=sk-ant-...   # Anthropic
OPENROUTER_API_KEY=sk-or-...   # OpenRouter (400+ 모델)

# LLM 모니터링 설정
LLM_USER_ID=dev-alice           # 사용자 식별자
LLM_USER_ALIAS=Alice            # 표시명
COST_THRESHOLD_USD=10.00        # 비용 임계값 (초과 시 알림)
DASHBOARD_PORT=3000             # 대시보드 포트
MAX_COST_USD=5.00               # 단일 실행 최대 비용
SLACK_WEBHOOK_URL=https://...   # 알림용 (선택)
```

### 3. 프로젝트 스택 요구사항

```
Option A (권장): Next.js 15+ + React 18 + TypeScript
Option B (경량): Python 3.8+ + HTML/JavaScript (의존성 최소)
```

---

## Instructions

### Step 0: 안전 체크 (항상 가장 먼저 실행)

**⚠️ 스킬 실행 전 반드시 이 스크립트를 실행하세요. FAIL 항목이 있으면 중단됩니다.**

```bash
cat > safety-guard.sh << 'SAFETY_EOF'
#!/usr/bin/env bash
# safety-guard.sh — LLM 모니터링 대시보드 실행 전 안전 게이트
set -euo pipefail

RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'; NC='\033[0m'
ALLOW_LIVE="${1:-}"; PASS=0; WARN=0; FAIL=0

log_pass() { echo -e "${GREEN}✅ PASS${NC} $1"; ((PASS++)); }
log_warn() { echo -e "${YELLOW}⚠️  WARN${NC} $1"; ((WARN++)); }
log_fail() { echo -e "${RED}❌ FAIL${NC} $1"; ((FAIL++)); }

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛡  LLM Monitoring Dashboard — Safety Guard v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. Tokuin CLI 설치 확인 ────────────────────────────────
if command -v tokuin &>/dev/null; then
  log_pass "Tokuin CLI 설치됨: $(tokuin --version 2>&1 | head -1)"
else
  log_fail "Tokuin 미설치 → 아래 명령어로 설치 후 재실행:"
  echo "  curl -fsSL https://raw.githubusercontent.com/nooscraft/tokuin/main/install.sh | bash"
fi

# ── 2. API 키 하드코딩 감지 ────────────────────────────────
HARDCODED=$(grep -rE "(sk-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9]{20,}|sk-or-[a-zA-Z0-9]{20,})" \
  . --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  --include="*.html" --include="*.sh" --include="*.py" --include="*.json" \
  --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null \
  | grep -v "\.env" | grep -v "example" | wc -l || echo 0)
if [ "$HARDCODED" -eq 0 ]; then
  log_pass "API 키 하드코딩 없음"
else
  log_fail "⚠️  API 키 하드코딩 ${HARDCODED}건 감지! → 환경변수(.env)로 즉시 이동 필요"
  grep -rE "(sk-[a-zA-Z0-9]{20,})" . \
    --include="*.ts" --include="*.js" --include="*.html" \
    --exclude-dir=node_modules 2>/dev/null | head -5 || true
fi

# ── 3. .env → .gitignore 등록 확인 ────────────────────────
if [ -f .env ]; then
  if [ -f .gitignore ] && grep -q "\.env" .gitignore; then
    log_pass ".env가 .gitignore에 등록됨"
  else
    log_fail ".env 존재하지만 .gitignore 미등록! → echo '.env' >> .gitignore"
  fi
else
  log_warn ".env 파일 없음 — 실제 API 호출 시 생성 필요"
fi

# ── 4. 실제 API 호출 모드 확인 ────────────────────────────
if [ "$ALLOW_LIVE" = "--allow-live" ]; then
  log_warn "실제 API 호출 모드 활성화! 비용이 발생합니다."
  log_warn "최대 비용 임계값: \$${MAX_COST_USD:-5.00} (MAX_COST_USD 환경변수로 조정)"
  read -p "  실제 API 호출을 허용하시겠습니까? [y/N] " -r
  echo
  [[ $REPLY =~ ^[Yy]$ ]] || { echo "취소됨. dry-run 모드로 재실행하세요."; exit 1; }
else
  log_pass "dry-run 모드 (기본값) — API 비용 발생 없음"
fi

# ── 5. 포트 충돌 확인 ─────────────────────────────────────
PORT="${DASHBOARD_PORT:-3000}"
if lsof -i ":${PORT}" &>/dev/null 2>&1; then
  ALT_PORT=$((PORT + 1))
  log_warn "포트 ${PORT} 사용 중 → 대신 ${ALT_PORT} 사용: export DASHBOARD_PORT=${ALT_PORT}"
else
  log_pass "포트 ${PORT} 사용 가능"
fi

# ── 6. data/ 디렉토리 초기화 ──────────────────────────────
mkdir -p ./data
if [ -f ./data/metrics.jsonl ]; then
  BYTES=$(wc -c < ./data/metrics.jsonl || echo 0)
  if [ "$BYTES" -gt 10485760 ]; then
    log_warn "metrics.jsonl이 10MB 초과 (${BYTES}B) → 롤링 정책 적용 권장"
    echo "  cp data/metrics.jsonl data/metrics-$(date +%Y%m%d).jsonl.bak && > data/metrics.jsonl"
  else
    log_pass "data/ 준비됨 (metrics.jsonl: ${BYTES}B)"
  fi
else
  log_pass "data/ 준비됨 (신규)"
fi

# ── 결과 요약 ─────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "결과: ${GREEN}PASS $PASS${NC} / ${YELLOW}WARN $WARN${NC} / ${RED}FAIL $FAIL${NC}"
if [ "$FAIL" -gt 0 ]; then
  echo -e "${RED}❌ 안전 체크 실패. 위 FAIL 항목을 해결한 후 재실행하세요.${NC}"
  exit 1
else
  echo -e "${GREEN}✅ 안전 체크 통과. 스킬 실행을 계속합니다.${NC}"
  exit 0
fi
SAFETY_EOF
chmod +x safety-guard.sh

# 실행 (FAIL 있으면 즉시 중단됨)
bash safety-guard.sh
```

---

### Step 1: Tokuin CLI 설치 및 dry-run 검증

```bash
# 1-1. 설치 (macOS / Linux)
curl -fsSL https://raw.githubusercontent.com/nooscraft/tokuin/main/install.sh | bash

# Windows PowerShell:
# irm https://raw.githubusercontent.com/nooscraft/tokuin/main/install.ps1 | iex

# 1-2. 설치 확인
tokuin --version
which tokuin   # 기대: /usr/local/bin/tokuin 또는 ~/.local/bin/tokuin

# 1-3. 기본 토큰 카운트 테스트
echo "Hello, world!" | tokuin --model gpt-4

# 1-4. dry-run 비용 추정 (API 키 불필요 ✅)
echo "Analyze user behavior patterns from the following data" | \
  tokuin load-test \
  --model gpt-4 \
  --runs 50 \
  --concurrency 5 \
  --dry-run \
  --estimate-cost \
  --output-format json | python3 -m json.tool

# 기대 출력 구조:
# {
#   "total_requests": 50,
#   "successful": 50,
#   "failed": 0,
#   "latency_ms": { "average": ..., "p50": ..., "p95": ... },
#   "cost": { "input_tokens": ..., "output_tokens": ..., "total_cost": ... }
# }

# 1-5. 다중 모델 비교 (dry-run)
echo "Translate this to Korean" | tokuin --compare gpt-4 gpt-3.5-turbo claude-3-haiku --price

# 1-6. Prometheus 형식 출력 확인
echo "Benchmark" | tokuin load-test --model gpt-4 --runs 10 --dry-run --output-format prometheus
# 기대: "# HELP", "# TYPE", "tokuin_" 접두사 메트릭
```

---

### Step 2: 사용자 컨텍스트 포함 데이터 수집 파이프라인

```bash
# 2-1. 프롬프트 자동 카테고리 분류 모듈 생성
cat > categorize_prompt.py << 'PYEOF'
#!/usr/bin/env python3
"""프롬프트를 키워드 기반으로 자동 분류"""
import hashlib

CATEGORIES = {
    "코딩":   ["code", "function", "class", "implement", "debug", "fix", "refactor", "코드", "구현", "함수"],
    "분석":   ["analyze", "compare", "evaluate", "assess", "분석", "비교", "평가", "검토"],
    "번역":   ["translate", "translation", "번역", "영어로", "한국어로"],
    "요약":   ["summarize", "summary", "tldr", "brief", "요약", "정리"],
    "작성":   ["write", "draft", "create", "generate", "작성", "생성", "만들어"],
    "질문":   ["what is", "how to", "explain", "why", "무엇", "어떻게", "설명", "왜"],
    "데이터": ["data", "table", "csv", "json", "sql", "데이터", "테이블", "쿼리"],
}

def categorize(prompt: str) -> str:
    p = prompt.lower()
    for cat, keywords in CATEGORIES.items():
        if any(k in p for k in keywords):
            return cat
    return "기타"

def hash_prompt(prompt: str) -> str:
    """SHA-256 앞 16자 (원문 대신 저장 — 개인정보 보호)"""
    return hashlib.sha256(prompt.encode()).hexdigest()[:16]

def truncate_preview(prompt: str, limit: int = 100) -> str:
    return prompt[:limit] + ("…" if len(prompt) > limit else "")

if __name__ == "__main__":
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else ""
    print(categorize(prompt))
PYEOF

# 2-2. 사용자 컨텍스트 포함 메트릭 수집 스크립트 생성
cat > collect-metrics.sh << 'COLLECT_EOF'
#!/usr/bin/env bash
# collect-metrics.sh — Tokuin 실행 + 사용자 컨텍스트 저장 (dry-run 기본값)
set -euo pipefail

# 사용자 정보
USER_ID="${LLM_USER_ID:-$(whoami)}"
USER_ALIAS="${LLM_USER_ALIAS:-$USER_ID}"
SESSION_ID="${LLM_SESSION_ID:-$(date +%Y%m%d-%H%M%S)-$$}"
PROMPT="${1:-Benchmark prompt}"
MODEL="${MODEL:-gpt-4}"
PROVIDER="${PROVIDER:-openai}"
RUNS="${RUNS:-50}"
CONCURRENCY="${CONCURRENCY:-5}"
TAGS="${LLM_TAGS:-[]}"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CATEGORY=$(python3 categorize_prompt.py "$PROMPT" 2>/dev/null || echo "기타")
PROMPT_HASH=$(echo -n "$PROMPT" | sha256sum | cut -c1-16 2>/dev/null || echo "unknown")
PROMPT_LEN=${#PROMPT}

# Tokuin 실행 (dry-run 기본값)
RESULT=$(echo "$PROMPT" | tokuin load-test \
  --model "$MODEL" \
  --provider "$PROVIDER" \
  --runs "$RUNS" \
  --concurrency "$CONCURRENCY" \
  --output-format json \
  ${ALLOW_LIVE:+""} ${ALLOW_LIVE:-"--dry-run --estimate-cost"} 2>/dev/null)

# 사용자 컨텍스트 포함하여 JSONL 저장
python3 - << PYEOF
import json, sys

result = json.loads('''${RESULT}''')
latency = result.get("latency_ms", {})
cost = result.get("cost", {})

record = {
    "id": "${PROMPT_HASH}-${SESSION_ID}",
    "timestamp": "${TIMESTAMP}",
    "model": "${MODEL}",
    "provider": "${PROVIDER}",
    "user_id": "${USER_ID}",
    "user_alias": "${USER_ALIAS}",
    "session_id": "${SESSION_ID}",
    "prompt_hash": "${PROMPT_HASH}",
    "prompt_category": "${CATEGORY}",
    "prompt_length": ${PROMPT_LEN},
    "tags": json.loads('${TAGS}'),
    "is_dry_run": True,
    "total_requests": result.get("total_requests", 0),
    "successful": result.get("successful", 0),
    "failed": result.get("failed", 0),
    "input_tokens": cost.get("input_tokens", 0),
    "output_tokens": cost.get("output_tokens", 0),
    "cost_usd": cost.get("total_cost", 0),
    "latency_avg_ms": latency.get("average", 0),
    "latency_p50_ms": latency.get("p50", 0),
    "latency_p95_ms": latency.get("p95", 0),
    "status_code": 200 if result.get("successful", 0) > 0 else 500,
}

with open("./data/metrics.jsonl", "a") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"✅ 저장: [{record['user_alias']}] {record['prompt_category']} | ${record['cost_usd']:.4f} | {record['latency_avg_ms']:.0f}ms")
PYEOF
COLLECT_EOF
chmod +x collect-metrics.sh

# 2-3. 크론 설정 (5분마다 자동 수집)
(crontab -l 2>/dev/null; echo "*/5 * * * * cd $(pwd) && bash collect-metrics.sh 'Scheduled benchmark' >> ./data/collect.log 2>&1") | crontab -
echo "✅ 크론 등록 완료 (5분 간격)"

# 2-4. 첫 번째 수집 테스트 (dry-run)
bash collect-metrics.sh "Analyze user behavior patterns"
cat ./data/metrics.jsonl | python3 -m json.tool | head -30
```

---

### Step 3: 라우팅 구조 및 대시보드 프레임 생성

**Option A — Next.js (권장)**

```bash
# 3-1. Next.js 프로젝트 초기화 (기존 프로젝트에 추가 시 이 단계 생략)
npx create-next-app@latest llm-dashboard \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir
cd llm-dashboard

# 3-2. 의존성 설치
npm install recharts better-sqlite3 @types/better-sqlite3

# 3-3. 디자인 토큰 설정 (톤앤매너 일관성)
cat > app/globals.css << 'CSS_EOF'
:root {
  /* 배경 계층 */
  --bg-base:     #0f1117;
  --bg-surface:  #1a1d27;
  --bg-elevated: #21253a;
  --border:      rgba(255, 255, 255, 0.06);

  /* 텍스트 계층 */
  --text-primary:   #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted:     #475569;

  /* 3단계 신호등 시스템 (모든 컴포넌트에서 일관되게 사용) */
  --color-ok:      #22c55e;   /* 정상 — Green 500 */
  --color-warn:    #f59e0b;   /* 경고 — Amber 500 */
  --color-danger:  #ef4444;   /* 위험 — Red 500   */
  --color-neutral: #60a5fa;   /* 중립 — Blue 400  */

  /* 데이터 시리즈 컬러 (색맹 고려 팔레트) */
  --series-1: #818cf8;  /* Indigo  — System/GPT-4    */
  --series-2: #38bdf8;  /* Sky     — User/Claude     */
  --series-3: #34d399;  /* Emerald — Assistant/Gemini*/
  --series-4: #fb923c;  /* Orange  — 4번째 시리즈    */

  /* 비용 특화 */
  --cost-input:  #a78bfa;
  --cost-output: #f472b6;

  /* 랭킹 컬러 */
  --rank-gold:     #fbbf24;
  --rank-silver:   #94a3b8;
  --rank-bronze:   #b45309;
  --rank-inactive: #374151;

  /* 타이포그래피 */
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-ui:   'Geist', 'Plus Jakarta Sans', system-ui, sans-serif;
}

body {
  background: var(--bg-base);
  color: var(--text-primary);
  font-family: var(--font-ui);
}

/* 숫자 표시: 정렬 안정성 */
.metric-value {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  font-feature-settings: 'tnum';
}

/* KPI 카드 accent-bar */
.status-ok     { border-left-color: var(--color-ok); }
.status-warn   { border-left-color: var(--color-warn); }
.status-danger { border-left-color: var(--color-danger); }
CSS_EOF

# 3-4. 라우팅 구조 생성
mkdir -p app/admin/llm-monitoring
mkdir -p app/admin/llm-monitoring/users
mkdir -p "app/admin/llm-monitoring/users/[userId]"
mkdir -p "app/admin/llm-monitoring/runs/[runId]"
mkdir -p components/llm-monitoring
mkdir -p lib/llm-monitoring

# 3-5. SQLite DB 초기화
cat > lib/llm-monitoring/db.ts << 'TS_EOF'
import Database from 'better-sqlite3'
import path from 'path'

const DB_PATH = path.join(process.cwd(), 'data', 'monitoring.db')

const db = new Database(DB_PATH)

db.exec(`
  CREATE TABLE IF NOT EXISTS runs (
    id              TEXT PRIMARY KEY,
    timestamp       DATETIME NOT NULL DEFAULT (datetime('now')),
    model           TEXT NOT NULL,
    provider        TEXT NOT NULL,
    user_id         TEXT DEFAULT 'anonymous',
    user_alias      TEXT DEFAULT 'anonymous',
    session_id      TEXT,
    prompt_hash     TEXT,
    prompt_category TEXT DEFAULT '기타',
    prompt_length   INTEGER DEFAULT 0,
    tags            TEXT DEFAULT '[]',
    is_dry_run      INTEGER DEFAULT 1,
    total_requests  INTEGER DEFAULT 0,
    successful      INTEGER DEFAULT 0,
    failed          INTEGER DEFAULT 0,
    input_tokens    INTEGER DEFAULT 0,
    output_tokens   INTEGER DEFAULT 0,
    cost_usd        REAL DEFAULT 0,
    latency_avg_ms  REAL DEFAULT 0,
    latency_p50_ms  REAL DEFAULT 0,
    latency_p95_ms  REAL DEFAULT 0,
    status_code     INTEGER DEFAULT 200
  );

  CREATE TABLE IF NOT EXISTS user_profiles (
    user_id    TEXT PRIMARY KEY,
    user_alias TEXT NOT NULL,
    team       TEXT DEFAULT '',
    role       TEXT DEFAULT 'user',
    created_at DATETIME DEFAULT (datetime('now')),
    last_seen  DATETIME,
    notes      TEXT DEFAULT ''
  );

  CREATE INDEX IF NOT EXISTS idx_runs_timestamp  ON runs(timestamp DESC);
  CREATE INDEX IF NOT EXISTS idx_runs_user_id    ON runs(user_id);
  CREATE INDEX IF NOT EXISTS idx_runs_model      ON runs(model);

  CREATE VIEW IF NOT EXISTS user_stats AS
  SELECT
    user_id,
    user_alias,
    COUNT(*)                          AS total_runs,
    SUM(input_tokens + output_tokens) AS total_tokens,
    ROUND(SUM(cost_usd), 4)           AS total_cost,
    ROUND(AVG(latency_avg_ms), 1)     AS avg_latency,
    ROUND(AVG(CAST(successful AS REAL) / NULLIF(total_requests, 0) * 100), 1) AS success_rate,
    COUNT(DISTINCT model)             AS models_used,
    MAX(timestamp)                    AS last_seen
  FROM runs
  GROUP BY user_id;
`)

export default db
TS_EOF
```

**Option B — 경량 HTML (의존성 최소)**

```bash
# 기존 프로젝트가 없거나 빠른 프로토타입 필요 시
mkdir -p llm-monitoring/data

cat > llm-monitoring/index.html << 'HTML_EOF'
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🧮 LLM 사용 모니터링</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    /* 디자인 토큰 */
    :root {
      --bg-base: #0f1117; --bg-surface: #1a1d27; --bg-elevated: #21253a;
      --text-primary: #f1f5f9; --text-secondary: #94a3b8; --text-muted: #475569;
      --color-ok: #22c55e; --color-warn: #f59e0b; --color-danger: #ef4444;
      --series-1: #818cf8; --series-2: #38bdf8; --series-3: #34d399; --series-4: #fb923c;
      --rank-gold: #fbbf24; --rank-silver: #94a3b8; --rank-bronze: #b45309;
      --font-mono: 'JetBrains Mono', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: var(--bg-base); color: var(--text-primary); font-family: system-ui, sans-serif; padding: 24px; }
    header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
    header h1 { font-size: 1.5rem; font-weight: 700; color: #60a5fa; }
    .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
    @media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 480px) { .kpi-grid { grid-template-columns: 1fr; } }
    .kpi-card {
      background: var(--bg-surface);
      border: 1px solid rgba(255,255,255,0.06);
      border-left: 3px solid var(--color-neutral, #60a5fa);
      border-radius: 12px;
      padding: 20px;
    }
    .kpi-card.ok     { border-left-color: var(--color-ok); }
    .kpi-card.warn   { border-left-color: var(--color-warn); }
    .kpi-card.danger { border-left-color: var(--color-danger); }
    .kpi-label { font-size: 0.625rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); margin-bottom: 8px; }
    .kpi-value { font-family: var(--font-mono); font-size: 2rem; font-weight: 700; font-variant-numeric: tabular-nums; }
    .kpi-sub   { font-size: 0.75rem; color: var(--text-secondary); margin-top: 4px; }
    .chart-row { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; margin-bottom: 24px; }
    @media (max-width: 900px) { .chart-row { grid-template-columns: 1fr; } }
    .chart-card { background: var(--bg-surface); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 20px; }
    .chart-card h3 { font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.05em; }
    .ranking-table { width: 100%; border-collapse: collapse; }
    .ranking-table th { font-size: 0.625rem; text-transform: uppercase; color: var(--text-muted); padding: 8px 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.06); }
    .ranking-table td { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.04); font-family: var(--font-mono); font-size: 0.875rem; }
    .ranking-table tr:hover td { background: var(--bg-elevated); }
    .user-link { color: #60a5fa; text-decoration: none; cursor: pointer; }
    .user-link:hover { text-decoration: underline; }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; }
    .badge-ok     { background: rgba(34,197,94,0.1);  color: var(--color-ok); }
    .badge-warn   { background: rgba(245,158,11,0.1); color: var(--color-warn); }
    .badge-danger { background: rgba(239,68,68,0.1);  color: var(--color-danger); }
    .rank-1 { color: var(--rank-gold); }
    .rank-2 { color: var(--rank-silver); }
    .rank-3 { color: var(--rank-bronze); }
    .insight-box { background: rgba(96,165,250,0.05); border: 1px solid rgba(96,165,250,0.15); border-radius: 8px; padding: 16px; margin-top: 8px; }
    .insight-box h4 { font-size: 0.75rem; color: #60a5fa; margin-bottom: 8px; }
    .insight-box ul { font-size: 0.8rem; color: var(--text-secondary); padding-left: 16px; }
    .insight-box ul li { margin-bottom: 4px; }
    .section-title { font-size: 1rem; font-weight: 600; margin: 24px 0 12px; }
    #user-detail { display: none; background: var(--bg-surface); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 24px; margin-top: 16px; }
    .back-btn { background: none; border: 1px solid rgba(255,255,255,0.1); color: var(--text-secondary); padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 0.8rem; margin-bottom: 16px; }
    .back-btn:hover { background: var(--bg-elevated); }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>🧮 LLM 사용 모니터링</h1>
      <p style="font-size:0.75rem;color:#475569;margin-top:4px;">Powered by Tokuin CLI</p>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
      <span id="last-updated" style="font-size:0.75rem;color:#475569;"></span>
      <button onclick="loadData()" style="background:rgba(96,165,250,0.1);border:1px solid rgba(96,165,250,0.2);color:#60a5fa;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.8rem;">↻ 새로고침</button>
    </div>
  </header>

  <!-- 메인 대시보드 -->
  <div id="main-dashboard">
    <!-- KPI 카드 4종 -->
    <div class="kpi-grid">
      <div class="kpi-card" id="kpi-requests">
        <div class="kpi-label">총 요청 수</div>
        <div class="kpi-value metric-value" id="val-requests">-</div>
        <div class="kpi-sub" id="sub-requests">데이터 로딩 중...</div>
      </div>
      <div class="kpi-card" id="kpi-success">
        <div class="kpi-label">성공률</div>
        <div class="kpi-value metric-value" id="val-success">-</div>
        <div class="kpi-sub" id="sub-success">-</div>
      </div>
      <div class="kpi-card" id="kpi-latency">
        <div class="kpi-label">p95 레이턴시</div>
        <div class="kpi-value metric-value" id="val-latency">-</div>
        <div class="kpi-sub" id="sub-latency">-</div>
      </div>
      <div class="kpi-card" id="kpi-cost">
        <div class="kpi-label">총 비용</div>
        <div class="kpi-value metric-value" id="val-cost">-</div>
        <div class="kpi-sub" id="sub-cost">-</div>
      </div>
    </div>

    <!-- 차트 행 -->
    <div class="chart-row">
      <div class="chart-card">
        <h3>시간대별 비용 트렌드</h3>
        <canvas id="trend-chart" height="160"></canvas>
      </div>
      <div class="chart-card">
        <h3>카테고리 분포</h3>
        <canvas id="category-chart" height="160"></canvas>
      </div>
    </div>

    <!-- 사용자 랭킹 -->
    <h2 class="section-title">🏆 사용자 랭킹</h2>
    <div class="chart-card" style="margin-bottom:24px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
        <h3 style="margin-bottom:0;">비용 기준 순위</h3>
        <input id="user-search" type="text" placeholder="🔍 사용자 검색..." 
          style="background:var(--bg-elevated);border:1px solid rgba(255,255,255,0.08);color:var(--text-primary);padding:6px 12px;border-radius:6px;font-size:0.8rem;width:200px;"
          oninput="filterRanking(this.value)">
      </div>
      <table class="ranking-table" id="ranking-table">
        <thead>
          <tr>
            <th>순위</th>
            <th>사용자</th>
            <th>비용</th>
            <th>요청수</th>
            <th>선호 모델</th>
            <th>성공률</th>
            <th>마지막 활동</th>
          </tr>
        </thead>
        <tbody id="ranking-body">
          <tr><td colspan="7" style="text-align:center;color:#475569;padding:24px;">데이터 로딩 중...</td></tr>
        </tbody>
      </table>
    </div>

    <!-- 비사용자 추적 -->
    <h2 class="section-title">💤 비사용자 현황</h2>
    <div class="chart-card" style="margin-bottom:24px;">
      <table class="ranking-table" id="inactive-table">
        <thead>
          <tr><th>사용자</th><th>미사용 기간</th><th>마지막 활동</th><th>상태</th></tr>
        </thead>
        <tbody id="inactive-body">
          <tr><td colspan="4" style="text-align:center;color:#475569;padding:24px;">추적 데이터 없음</td></tr>
        </tbody>
      </table>
    </div>

    <!-- PM 인사이트 -->
    <h2 class="section-title">📊 PM 자동 인사이트</h2>
    <div id="pm-insights">
      <div class="insight-box">
        <h4>💡 자동 분석 중...</h4>
      </div>
    </div>
  </div>

  <!-- 사용자 개인 상세 페이지 (링크 클릭 시 표시) -->
  <div id="user-detail">
    <button class="back-btn" onclick="showMain()">← 대시보드로 돌아가기</button>
    <div id="user-detail-content"></div>
  </div>

  <script>
  let allData = [];
  let allUsers = {};

  async function loadData() {
    try {
      const res = await fetch('./data/metrics.jsonl');
      const text = await res.text();
      allData = text.trim().split('\n').filter(Boolean).map(l => JSON.parse(l));
      document.getElementById('last-updated').textContent = '마지막 갱신: ' + new Date().toLocaleTimeString('ko-KR');
      renderDashboard();
    } catch(e) {
      // JSONL 파일 없으면 샘플 데이터로 표시
      allData = generateSampleData();
      renderDashboard();
    }
  }

  function generateSampleData() {
    const users = ['dev-alice', 'team-backend', 'analyst-bob', 'pm-charlie'];
    const models = ['gpt-4', 'claude-3-sonnet', 'gemini-pro'];
    const categories = ['코딩', '분석', '번역', '요약', '작성'];
    const data = [];
    for (let i = 0; i < 50; i++) {
      const user = users[Math.floor(Math.random() * users.length)];
      const daysAgo = Math.floor(Math.random() * 30);
      const ts = new Date(Date.now() - daysAgo * 86400000 - Math.random() * 86400000);
      data.push({
        id: 'sample-' + i,
        timestamp: ts.toISOString(),
        model: models[Math.floor(Math.random() * models.length)],
        provider: 'openai',
        user_id: user,
        user_alias: user,
        prompt_category: categories[Math.floor(Math.random() * categories.length)],
        input_tokens: Math.floor(Math.random() * 2000) + 100,
        output_tokens: Math.floor(Math.random() * 1000) + 50,
        cost_usd: (Math.random() * 0.05).toFixed(4) * 1,
        latency_avg_ms: Math.floor(Math.random() * 1500) + 200,
        latency_p95_ms: Math.floor(Math.random() * 2500) + 500,
        successful: 1,
        total_requests: 1,
        is_dry_run: true,
        status_code: Math.random() > 0.05 ? 200 : 429,
      });
    }
    return data;
  }

  function renderDashboard() {
    if (!allData.length) return;

    // KPI 계산
    const totalReqs  = allData.reduce((s, r) => s + (r.total_requests || 1), 0);
    const totalSucc  = allData.filter(r => r.status_code === 200).length;
    const successRate = ((totalSucc / allData.length) * 100).toFixed(1);
    const avgLatency = (allData.reduce((s, r) => s + (r.latency_avg_ms || 0), 0) / allData.length).toFixed(0);
    const p95Latency = (allData.reduce((s, r) => s + (r.latency_p95_ms || 0), 0) / allData.length).toFixed(0);
    const totalCost  = allData.reduce((s, r) => s + (r.cost_usd || 0), 0).toFixed(4);

    // KPI 카드 업데이트
    document.getElementById('val-requests').textContent = totalReqs.toLocaleString();
    document.getElementById('sub-requests').textContent = allData.length + '개 실행 기록';

    document.getElementById('val-success').textContent = successRate + '%';
    document.getElementById('sub-success').textContent = '실패 ' + (allData.length - totalSucc) + '건';
    const kpiSuccess = document.getElementById('kpi-success');
    kpiSuccess.className = 'kpi-card ' + (successRate >= 95 ? 'ok' : successRate >= 90 ? 'warn' : 'danger');

    document.getElementById('val-latency').textContent = p95Latency + 'ms';
    document.getElementById('sub-latency').textContent = '평균 ' + avgLatency + 'ms';
    const kpiLatency = document.getElementById('kpi-latency');
    kpiLatency.className = 'kpi-card ' + (p95Latency < 1000 ? 'ok' : p95Latency < 2000 ? 'warn' : 'danger');

    document.getElementById('val-cost').textContent = '$' + totalCost;
    document.getElementById('sub-cost').textContent = 'dry-run 추정값';

    // 트렌드 차트
    renderTrendChart();
    // 카테고리 분포
    renderCategoryChart();
    // 사용자 랭킹
    renderRanking();
    // 비사용자
    renderInactive();
    // PM 인사이트
    renderInsights(successRate, p95Latency, totalCost);
  }

  function renderTrendChart() {
    const ctx = document.getElementById('trend-chart').getContext('2d');
    const byDate = {};
    allData.forEach(r => {
      const d = r.timestamp.substring(0, 10);
      byDate[d] = (byDate[d] || 0) + (r.cost_usd || 0);
    });
    const labels = Object.keys(byDate).sort().slice(-14);
    const values = labels.map(d => byDate[d].toFixed(4));
    if (window._trendChart) window._trendChart.destroy();
    window._trendChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: '일별 비용 ($)',
          data: values,
          borderColor: '#818cf8',
          backgroundColor: 'rgba(129,140,248,0.1)',
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointBackgroundColor: '#818cf8',
        }]
      },
      options: {
        plugins: { legend: { labels: { color: '#94a3b8' } } },
        scales: {
          x: { ticks: { color: '#475569' }, grid: { color: 'rgba(255,255,255,0.04)' } },
          y: { ticks: { color: '#475569' }, grid: { color: 'rgba(255,255,255,0.04)' } }
        }
      }
    });
  }

  function renderCategoryChart() {
    const ctx = document.getElementById('category-chart').getContext('2d');
    const cats = {};
    allData.forEach(r => { cats[r.prompt_category || '기타'] = (cats[r.prompt_category || '기타'] || 0) + 1; });
    const colors = ['#818cf8','#38bdf8','#34d399','#fb923c','#f472b6','#94a3b8'];
    if (window._catChart) window._catChart.destroy();
    window._catChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: Object.keys(cats),
        datasets: [{ data: Object.values(cats), backgroundColor: colors, borderWidth: 0 }]
      },
      options: {
        plugins: { legend: { position: 'right', labels: { color: '#94a3b8', font: { size: 11 } } } },
        cutout: '65%'
      }
    });
  }

  function renderRanking(filter = '') {
    const userMap = {};
    allData.forEach(r => {
      const uid = r.user_id || 'anonymous';
      if (!userMap[uid]) userMap[uid] = { alias: r.user_alias || uid, cost: 0, runs: 0, models: {}, success: 0, last: r.timestamp };
      userMap[uid].cost  += r.cost_usd || 0;
      userMap[uid].runs  += 1;
      userMap[uid].models[r.model] = (userMap[uid].models[r.model] || 0) + 1;
      if (r.status_code === 200) userMap[uid].success++;
      if (r.timestamp > userMap[uid].last) userMap[uid].last = r.timestamp;
    });
    allUsers = userMap;
    const sorted = Object.entries(userMap)
      .filter(([uid, u]) => !filter || u.alias.toLowerCase().includes(filter.toLowerCase()))
      .sort((a, b) => b[1].cost - a[1].cost);
    const tbody = document.getElementById('ranking-body');
    if (!sorted.length) { tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:#475569;padding:16px;">검색 결과 없음</td></tr>'; return; }
    const rankEmoji = ['🥇','🥈','🥉'];
    tbody.innerHTML = sorted.map(([uid, u], i) => {
      const topModel = Object.entries(u.models).sort((a,b) => b[1]-a[1])[0]?.[0] || '-';
      const sr = ((u.success / u.runs) * 100).toFixed(1);
      const srClass = sr >= 95 ? 'badge-ok' : sr >= 90 ? 'badge-warn' : 'badge-danger';
      const lastAgo = Math.floor((Date.now() - new Date(u.last)) / 86400000);
      const rankClass = i === 0 ? 'rank-1' : i === 1 ? 'rank-2' : i === 2 ? 'rank-3' : '';
      return `<tr>
        <td class="${rankClass}">${rankEmoji[i] || (i+1)}</td>
        <td><a class="user-link" onclick="showUserDetail('${uid}')">${u.alias}</a></td>
        <td class="metric-value">$${u.cost.toFixed(4)}</td>
        <td class="metric-value">${u.runs.toLocaleString()}</td>
        <td><span style="font-size:0.75rem;color:#94a3b8;">${topModel}</span></td>
        <td><span class="badge ${srClass}">${sr}%</span></td>
        <td style="color:#475569;font-size:0.75rem;">${lastAgo === 0 ? '오늘' : lastAgo + '일 전'}</td>
      </tr>`;
    }).join('');
  }

  function filterRanking(val) { renderRanking(val); }

  function renderInactive() {
    const sevenDaysAgo = new Date(Date.now() - 7 * 86400000);
    const activeUsers = new Set(
      allData.filter(r => new Date(r.timestamp) > sevenDaysAgo).map(r => r.user_id)
    );
    const lastSeen = {};
    allData.forEach(r => {
      if (!lastSeen[r.user_id] || r.timestamp > lastSeen[r.user_id].ts) {
        lastSeen[r.user_id] = { ts: r.timestamp, alias: r.user_alias || r.user_id };
      }
    });
    const inactive = Object.entries(lastSeen).filter(([uid]) => !activeUsers.has(uid));
    const tbody = document.getElementById('inactive-body');
    if (!inactive.length) {
      tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#22c55e;padding:16px;">✅ 모든 사용자 7일 내 활성</td></tr>';
      return;
    }
    tbody.innerHTML = inactive.map(([uid, info]) => {
      const daysAgo = Math.floor((Date.now() - new Date(info.ts)) / 86400000);
      const cls = daysAgo >= 30 ? 'badge-danger' : daysAgo >= 14 ? 'badge-warn' : 'badge-ok';
      return `<tr>
        <td><a class="user-link" onclick="showUserDetail('${uid}')">${info.alias}</a></td>
        <td class="metric-value">${daysAgo}일</td>
        <td style="color:#475569;font-size:0.75rem;">${new Date(info.ts).toLocaleDateString('ko-KR')}</td>
        <td><span class="badge ${cls}">${daysAgo >= 30 ? '긴급' : daysAgo >= 14 ? '주의' : '모니터링'}</span></td>
      </tr>`;
    }).join('');
  }

  function renderInsights(successRate, p95Latency, totalCost) {
    const insights = [];
    const sevenDaysAgo = new Date(Date.now() - 7 * 86400000);
    const activeUsers = new Set(allData.filter(r => new Date(r.timestamp) > sevenDaysAgo).map(r => r.user_id));
    const totalUsers = new Set(allData.map(r => r.user_id)).size;
    const adoptionRate = totalUsers ? Math.round(activeUsers.size / totalUsers * 100) : 0;
    const inactiveCount = totalUsers - activeUsers.size;

    if (inactiveCount > 0) insights.push(`■ 비활성 사용자 <strong>${inactiveCount}명</strong> — LLM 도입 지원 검토 필요`);
    if (successRate < 95) insights.push(`■ 성공률 ${successRate}% → SLA 95% 미달 — 에러 원인 분석 필요`);
    if (p95Latency > 2000) insights.push(`■ p95 레이턴시 ${p95Latency}ms → SLA 초과 — 모델 경량화 고려`);
    if (adoptionRate < 80) insights.push(`▲ 팀 채택률 ${adoptionRate}% → 목표 80% 미달 (${activeUsers.size}/${totalUsers}명 활성)`);
    if (totalCost > 50) insights.push(`▲ 총 비용 $${totalCost} — 상위 사용자 모델 최적화 검토 권장`);

    const categories = {};
    allData.forEach(r => { categories[r.prompt_category || '기타'] = (categories[r.prompt_category || '기타'] || 0) + 1; });
    const topCat = Object.entries(categories).sort((a,b) => b[1]-a[1])[0];
    if (topCat) insights.push(`● 주요 사용 패턴: <strong>${topCat[0]}</strong> (${topCat[1]}회) — 특화 모델 도입 효과적`);

    const insightDiv = document.getElementById('pm-insights');
    insightDiv.innerHTML = `<div class="insight-box">
      <h4>💡 PM 자동 인사이트 — ${new Date().toLocaleDateString('ko-KR')} 기준</h4>
      <ul>${insights.map(i => `<li>${i}</li>`).join('')}</ul>
    </div>`;
  }

  function showUserDetail(userId) {
    const u = allUsers[userId];
    if (!u) return;
    const userRuns = allData.filter(r => r.user_id === userId);
    const categories = {};
    userRuns.forEach(r => { categories[r.prompt_category || '기타'] = (categories[r.prompt_category || '기타'] || 0) + 1; });
    const totalCost = userRuns.reduce((s, r) => s + (r.cost_usd || 0), 0).toFixed(4);
    const topModel = Object.entries(
      userRuns.reduce((m, r) => { m[r.model] = (m[r.model] || 0)+1; return m; }, {})
    ).sort((a,b) => b[1]-a[1])[0]?.[0] || '-';

    document.getElementById('user-detail-content').innerHTML = `
      <div style="background:var(--bg-elevated);border-radius:8px;padding:16px;margin-bottom:20px;">
        <h2 style="font-size:1.25rem;margin-bottom:8px;">👤 ${u.alias}</h2>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:12px;">
          <div><div style="font-size:0.625rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">총 비용</div><div class="metric-value" style="font-size:1.5rem;">$${totalCost}</div></div>
          <div><div style="font-size:0.625rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">총 요청</div><div class="metric-value" style="font-size:1.5rem;">${u.runs.toLocaleString()}</div></div>
          <div><div style="font-size:0.625rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">선호 모델</div><div style="font-size:1rem;margin-top:4px;">${topModel}</div></div>
          <div><div style="font-size:0.625rem;color:#475569;text-transform:uppercase;margin-bottom:4px;">카테고리 분포</div><div style="font-size:0.8rem;color:#94a3b8;">${Object.entries(categories).map(([k,v]) => k+' '+v+'회').join(', ')}</div></div>
        </div>
      </div>
      <h3 style="font-size:0.875rem;color:#94a3b8;margin-bottom:12px;">최근 실행 로그</h3>
      <table class="ranking-table">
        <thead><tr><th>시각</th><th>모델</th><th>카테고리</th><th>비용</th><th>레이턴시</th><th>상태</th></tr></thead>
        <tbody>
          ${userRuns.slice(-10).reverse().map(r => {
            const sc = r.status_code === 200 ? 'badge-ok' : 'badge-danger';
            return `<tr>
              <td style="color:#475569;font-size:0.75rem;">${new Date(r.timestamp).toLocaleString('ko-KR')}</td>
              <td style="font-size:0.8rem;">${r.model}</td>
              <td><span class="badge badge-ok" style="font-size:0.65rem;">${r.prompt_category||'기타'}</span></td>
              <td class="metric-value">$${(r.cost_usd||0).toFixed(4)}</td>
              <td class="metric-value">${(r.latency_avg_ms||0).toFixed(0)}ms</td>
              <td><span class="badge ${sc}">${r.status_code||200}</span></td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
      <div class="insight-box" style="margin-top:16px;">
        <h4>💡 개인 인사이트</h4>
        <ul>
          <li>선호 모델: <strong>${topModel}</strong> — 동일 성능 경량 모델 전환 시 비용 절감 가능</li>
          <li>주요 사용 패턴: <strong>${Object.entries(categories).sort((a,b)=>b[1]-a[1])[0]?.[0]||'없음'}</strong></li>
          <li>총 ${u.runs}회 실행 — 팀 평균 대비 활성도 분석 필요</li>
        </ul>
      </div>
    `;
    document.getElementById('main-dashboard').style.display = 'none';
    document.getElementById('user-detail').style.display = 'block';
    window.scrollTo(0, 0);
  }

  function showMain() {
    document.getElementById('user-detail').style.display = 'none';
    document.getElementById('main-dashboard').style.display = 'block';
  }

  // 키보드 단축키
  document.addEventListener('keydown', e => {
    if (e.key === 'r' || e.key === 'R') loadData();
    if (e.key === 'Escape') showMain();
  });

  // 초기 로딩
  loadData();
  // 5분마다 자동 갱신
  setInterval(loadData, 5 * 60 * 1000);
  </script>
</body>
</html>
HTML_EOF

echo "✅ 경량 HTML 대시보드 생성 완료: llm-monitoring/index.html"
# 로컬 서버 실행
cd llm-monitoring && python3 -m http.server "${DASHBOARD_PORT:-3000}" &
echo "✅ 대시보드 실행 중: http://localhost:${DASHBOARD_PORT:-3000}"
```

---

### Step 4: PM 인사이트 탭 및 랭킹 시스템

(Option A / Next.js의 경우)

```bash
# PM 대시보드 API 라우트 생성
cat > app/api/ranking/route.ts << 'TS_EOF'
import { NextRequest, NextResponse } from 'next/server'
import db from '@/lib/llm-monitoring/db'

export async function GET(req: NextRequest) {
  const period = req.nextUrl.searchParams.get('period') || '30d'
  const days   = period === '7d' ? 7 : period === '90d' ? 90 : 30

  // 비용 기준 랭킹
  const costRanking = db.prepare(`
    SELECT
      user_id, user_alias,
      ROUND(SUM(cost_usd), 4)           AS total_cost,
      COUNT(*)                           AS total_runs,
      GROUP_CONCAT(DISTINCT model)       AS models_used,
      ROUND(AVG(latency_avg_ms), 0)      AS avg_latency,
      ROUND(
        AVG(CAST(successful AS REAL) / NULLIF(total_requests, 0)) * 100, 1
      )                                  AS success_rate,
      MAX(timestamp)                     AS last_seen
    FROM runs
    WHERE timestamp >= datetime('now', '-' || ? || ' days')
    GROUP BY user_id
    ORDER BY total_cost DESC
    LIMIT 20
  `).all(days)

  // 비사용자 추적 (선택 기간 내 활동 없는 등록 사용자)
  const inactiveUsers = db.prepare(`
    SELECT
      p.user_id, p.user_alias, p.team,
      MAX(r.timestamp)  AS last_seen,
      CAST((julianday('now') - julianday(MAX(r.timestamp))) AS INTEGER) AS days_inactive
    FROM user_profiles p
    LEFT JOIN runs r ON p.user_id = r.user_id
    GROUP BY p.user_id
    HAVING last_seen IS NULL
       OR days_inactive >= 7
    ORDER BY days_inactive DESC
  `).all()

  // PM 요약
  const summary = db.prepare(`
    SELECT
      COUNT(DISTINCT user_id)    AS total_users,
      COUNT(DISTINCT CASE WHEN timestamp >= datetime('now', '-7 days') THEN user_id END) AS active_7d,
      ROUND(SUM(cost_usd), 2)    AS total_cost,
      COUNT(*)                   AS total_runs
    FROM runs
    WHERE timestamp >= datetime('now', '-' || ? || ' days')
  `).get(days) as Record<string, number>

  return NextResponse.json({ costRanking, inactiveUsers, summary })
}
TS_EOF
```

---

### Step 5: 주간 PM 리포트 자동 생성

```bash
cat > generate-pm-report.sh << 'REPORT_EOF'
#!/usr/bin/env bash
# generate-pm-report.sh — 주간 PM 리포트 자동 생성 (Markdown)
set -euo pipefail

REPORT_DATE=$(date +"%Y-%m-%d")
REPORT_WEEK=$(date +"%Y-W%V")
OUTPUT_DIR="./reports"
OUTPUT="${OUTPUT_DIR}/pm-weekly-${REPORT_DATE}.md"
mkdir -p "$OUTPUT_DIR"

python3 << PYEOF > "$OUTPUT"
import json, sys
from datetime import datetime, timedelta
from collections import defaultdict

# 최근 7일 데이터 로드
try:
    records = [json.loads(l) for l in open('./data/metrics.jsonl') if l.strip()]
except FileNotFoundError:
    records = []

week_ago = (datetime.now() - timedelta(days=7)).isoformat()
week_data = [r for r in records if r.get('timestamp', '') >= week_ago]

# 집계
total_cost    = sum(r.get('cost_usd', 0) for r in week_data)
total_runs    = len(week_data)
active_users  = set(r['user_id'] for r in week_data)
all_users     = set(r['user_id'] for r in records)
inactive_users = all_users - active_users

# 사용자별 비용 랭킹
user_costs = defaultdict(lambda: {'cost': 0, 'runs': 0, 'alias': '', 'categories': defaultdict(int)})
for r in week_data:
    uid = r.get('user_id', 'unknown')
    user_costs[uid]['cost']  += r.get('cost_usd', 0)
    user_costs[uid]['runs']  += 1
    user_costs[uid]['alias']  = r.get('user_alias', uid)
    user_costs[uid]['categories'][r.get('prompt_category', '기타')] += 1

top_users = sorted(user_costs.items(), key=lambda x: x[1]['cost'], reverse=True)[:5]

# 모델별 사용량
model_usage = defaultdict(int)
for r in week_data:
    model_usage[r.get('model', 'unknown')] += 1
top_model = max(model_usage, key=model_usage.get) if model_usage else '-'

# 성공률
success_count = sum(1 for r in week_data if r.get('status_code', 200) == 200)
success_rate  = (success_count / total_runs * 100) if total_runs else 0

print(f"""# 📊 LLM 사용 주간 리포트 — {REPORT_DATE} ({REPORT_WEEK})

## Executive Summary

| 지표 | 값 |
|------|-----|
| 총 비용 | \${total_cost:.2f} |
| 총 실행 수 | {total_runs:,}회 |
| 활성 사용자 | {len(active_users)}명 |
| 채택률 | {len(active_users)}/{len(all_users)}명 ({len(active_users)/len(all_users)*100:.0f}% if all_users else 'N/A') |
| 성공률 | {success_rate:.1f}% |
| 최다 사용 모델 | {top_model} |

## 🏆 사용자 TOP 5 (비용 기준)

| 순위 | 사용자 | 비용 | 실행 수 | 주요 카테고리 |
|------|--------|------|---------|--------------|
{"".join(f"| {'🥇🥈🥉'[i] if i < 3 else i+1} | {u['alias']} | \${u['cost']:.4f} | {u['runs']} | {max(u['categories'], key=u['categories'].get) if u['categories'] else '-'} |" + chr(10) for i, (uid, u) in enumerate(top_users))}

## 💤 비활성 사용자 ({len(inactive_users)}명)

{"없음 — 모든 사용자 7일 내 활성" if not inactive_users else chr(10).join(f"- {uid}" for uid in inactive_users)}

## 💡 PM 권장 조치

{"- 비활성 사용자 " + str(len(inactive_users)) + "명 대상 온보딩/지원 검토" if inactive_users else ""}
{"- 성공률 " + f"{success_rate:.1f}%" + " — SLA 95% " + ("달성 ✅" if success_rate >= 95 else "미달 ⚠️ 에러 원인 분석 필요") }
{"- 총 비용 \$" + f"{total_cost:.2f}" + " — 전주 대비 모델 최적화 기회 검토"}

---
*자동 생성: generate-pm-report.sh | Tokuin CLI 기반*
""")
PYEOF

echo "✅ PM 리포트 생성: $OUTPUT"
cat "$OUTPUT"

# Slack 알림 (설정된 경우)
if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
  SUMMARY=$(grep -A5 "## Executive Summary" "$OUTPUT" | tail -5)
  curl -s -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-type: application/json' \
    -d "{\"text\":\"📊 주간 LLM 리포트 ($REPORT_DATE)\n$SUMMARY\"}" > /dev/null
  echo "✅ Slack 알림 전송 완료"
fi
REPORT_EOF
chmod +x generate-pm-report.sh

# 매주 월요일 오전 9시 자동 실행
(crontab -l 2>/dev/null; echo "0 9 * * 1 cd $(pwd) && bash generate-pm-report.sh >> ./data/report.log 2>&1") | crontab -
echo "✅ 주간 리포트 크론 등록 (매주 월요일 09:00)"

# 즉시 테스트 실행
bash generate-pm-report.sh
```

---

### Step 6: 비용 알림 설정

```bash
cat > check-alerts.sh << 'ALERT_EOF'
#!/usr/bin/env bash
# check-alerts.sh — 비용 임계값 초과 감지 및 Slack 알림
set -euo pipefail

THRESHOLD="${COST_THRESHOLD_USD:-10.00}"

CURRENT_COST=$(python3 << PYEOF
import json
from datetime import datetime, timedelta

today = datetime.now().date().isoformat()
try:
    records = [json.loads(l) for l in open('./data/metrics.jsonl') if l.strip()]
    today_cost = sum(r.get('cost_usd', 0) for r in records if r.get('timestamp', '')[:10] == today)
    print(f"{today_cost:.4f}")
except:
    print("0.0000")
PYEOF
)

python3 - << PYEOF
import sys
cost, threshold = float('$CURRENT_COST'), float('$THRESHOLD')
if cost > threshold:
    print(f"ALERT: 오늘 비용 \${cost:.4f}가 임계값 \${threshold:.2f}를 초과했습니다!")
    sys.exit(1)
else:
    print(f"정상: 오늘 비용 \${cost:.4f} / 임계값 \${threshold:.2f}")
    sys.exit(0)
PYEOF

# exit 1 시 Slack 알림
if [ $? -ne 0 ] && [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
  curl -s -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-type: application/json' \
    -d "{\"text\":\"⚠️ LLM 비용 임계값 초과!\n오늘 비용: \$$CURRENT_COST / 임계값: \$$THRESHOLD\"}" > /dev/null
fi
ALERT_EOF
chmod +x check-alerts.sh

# 1시간마다 비용 체크
(crontab -l 2>/dev/null; echo "0 * * * * cd $(pwd) && bash check-alerts.sh >> ./data/alerts.log 2>&1") | crontab -
echo "✅ 비용 알림 크론 등록 (매시간)"
```

---

## Privacy Policy

```yaml
# 개인정보 보호 정책 (반드시 준수)

prompt_storage:
  store_full_prompt: false      # 기본값: 원문 저장 안 함
  store_preview:     false      # 앞 100자 저장도 기본 비활성 (관리자 명시 설정 필요)
  store_hash:        true       # SHA-256 해시만 저장 (패턴 분석용)

user_data:
  anonymize_by_default: true   # user_id는 해시로 저장 가능 (LLM_USER_ID 환경변수로 제어)
  retention_days: 90            # 90일 후 오래된 데이터 정리 권장
  
compliance:
  # API 키를 절대 코드/HTML/로그 파일에 기록하지 마세요.
  # .env 파일은 반드시 .gitignore에 추가하세요.
  # 관리자 외 프롬프트 미리보기 접근을 제한하세요.
```

> ⚠️ **`store_preview: true` 활성화 시 필수 절차**
> 
> 프롬프트 미리보기 저장은 **관리자가 명시적으로** 아래 절차를 완료한 경우에만 활성화할 수 있습니다:
> 
> 1. `.env` 파일에서 `STORE_PREVIEW=true` 설정 (코드 직접 수정 금지)
> 2. 팀 내 개인정보 처리 동의 확보 (사용자에게 미리보기 저장 사실 고지)
> 3. 접근 권한을 **관리자 역할**로만 제한 (일반 사용자 열람 불가)
> 4. `retention_days` 를 명시적으로 설정하여 보관 기간 지정
> 
> 위 절차 없이 `store_preview: true`를 적용하는 것은 **MUST NOT** 위반입니다.

---

## Output Format

스킬 실행 완료 시 생성되는 파일:

```
./
├── safety-guard.sh          # 안전 게이트 (Step 0)
├── categorize_prompt.py     # 프롬프트 자동 분류
├── collect-metrics.sh       # 메트릭 수집 (Step 2)
├── generate-pm-report.sh    # PM 주간 리포트 (Step 5)
├── check-alerts.sh          # 비용 알림 (Step 6)
│
├── data/
│   ├── metrics.jsonl        # 시계열 메트릭 (JSONL 형식)
│   ├── collect.log          # 수집 로그
│   ├── alerts.log           # 알림 로그
│   └── reports/
│       └── pm-weekly-YYYY-MM-DD.md  # 자동 생성 PM 리포트
│
├── [Next.js 선택 시]
│   ├── app/admin/llm-monitoring/page.tsx
│   ├── app/admin/llm-monitoring/users/[userId]/page.tsx
│   ├── app/api/runs/route.ts
│   ├── app/api/ranking/route.ts
│   ├── app/api/metrics/route.ts        # Prometheus 엔드포인트
│   ├── components/llm-monitoring/
│   │   ├── KPICard.tsx
│   │   ├── TrendChart.tsx
│   │   ├── ModelCostBar.tsx
│   │   ├── LatencyGauge.tsx
│   │   ├── TokenDonut.tsx
│   │   ├── RankingTable.tsx
│   │   ├── InactiveUsers.tsx
│   │   ├── PMInsights.tsx
│   │   └── UserDetailPage.tsx
│   └── lib/llm-monitoring/db.ts
│
└── [경량 HTML 선택 시]
    └── llm-monitoring/
        ├── index.html       # 단일 파일 대시보드 (차트 + 랭킹 + 사용자 상세)
        └── data/
            └── metrics.jsonl
```

---

## Constraints

### MUST (반드시 지켜야 함)

- **Step 0(`safety-guard.sh`)을 항상 가장 먼저 실행할 것**
- `--dry-run`을 기본값으로 사용하고, 실제 API 호출은 `--allow-live` 플래그를 명시적으로 지정할 것
- API 키를 반드시 환경변수 또는 `.env` 파일로 관리할 것
- `.env`를 `.gitignore`에 추가할 것: `echo '.env' >> .gitignore`
- 상태 표시는 반드시 3단계 컬러 시스템(`--color-ok`, `--color-warn`, `--color-danger`)을 일관되게 사용할 것
- 사용자 링크 클릭 시 해당 사용자 개인 상세 페이지로 이동하는 드릴다운 네비게이션을 구현할 것
- PM 인사이트는 데이터 기반 자동 생성으로 구현할 것 (하드코딩 금지)

### MUST NOT (절대 하지 말 것)

- API 키를 코드, HTML, 스크립트, 로그 파일에 직접 입력하지 말 것
- 실제 API 호출(`--allow-live`)을 자동화 스크립트의 기본값으로 설정하지 말 것
- 임의의 색상 사용 금지 — 반드시 디자인 토큰 CSS 변수만 사용
- 상태 표시를 텍스트만으로 하지 말 것 (항상 색상 + 배지 병행)
- 사용자 프롬프트 원문을 데이터베이스에 저장하지 말 것 (해시만 허용)

---

## Examples

### 예시 1: 빠른 시작 (dry-run, API 키 불필요)

```bash
# 1. 안전 체크
bash safety-guard.sh

# 2. Tokuin 설치
curl -fsSL https://raw.githubusercontent.com/nooscraft/tokuin/main/install.sh | bash

# 3. 샘플 데이터 수집 (dry-run)
export LLM_USER_ID="dev-alice"
export LLM_USER_ALIAS="Alice"
bash collect-metrics.sh "Analyze user behavior patterns"
bash collect-metrics.sh "Write a Python function to parse JSON"
bash collect-metrics.sh "Translate this document to English"

# 4. 경량 대시보드 실행
cd llm-monitoring && python3 -m http.server 3000
open http://localhost:3000
```

### 예시 2: 다중 사용자 시뮬레이션 (팀 테스트)

```bash
# 여러 사용자 dry-run 시뮬레이션
for user in "alice" "backend" "analyst" "pm-charlie"; do
  export LLM_USER_ID="$user"
  export LLM_USER_ALIAS="$user"
  for category in "코딩" "분석" "번역"; do
    bash collect-metrics.sh "${category} 관련 프롬프트 예시"
  done
done

# 결과 확인
wc -l data/metrics.jsonl
```

### 예시 3: PM 주간 리포트 즉시 생성

```bash
bash generate-pm-report.sh
cat reports/pm-weekly-$(date +%Y-%m-%d).md
```

### 예시 4: 비용 알림 테스트

```bash
export COST_THRESHOLD_USD=0.01   # 낮은 임계값으로 테스트
bash check-alerts.sh
# 기대: ALERT 메시지 출력 (임계값보다 낮으면 "정상")
```

---

## References

- **Tokuin GitHub**: https://github.com/nooscraft/tokuin
- **Tokuin 설치 스크립트**: https://raw.githubusercontent.com/nooscraft/tokuin/main/install.sh
- **모델 추가 가이드**: https://github.com/nooscraft/tokuin/blob/main/ADDING_MODELS_GUIDE.md
- **프로바이더 로드맵**: https://github.com/nooscraft/tokuin/blob/main/PROVIDERS_PLAN.md
- **Contributing 가이드**: https://github.com/nooscraft/tokuin/blob/main/CONTRIBUTING.md
- **OpenRouter 모델 카탈로그**: https://openrouter.ai/models
- **한국어 블로그 가이드**: https://digitalbourgeois.tistory.com/m/2658
