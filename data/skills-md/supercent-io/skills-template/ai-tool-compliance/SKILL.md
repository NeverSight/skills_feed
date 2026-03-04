---
name: ai-tool-compliance
keyword: compliance
description: 내부 AI 툴 필수 구현 가이드(P0/P1) 기반으로 권한, 비용, 로그, 보안 컴플라이언스를 설계-검증-개선하는 자동화 스킬. RBAC 설계, Gateway 원칙, Firestore 정책, 행동 로그, 비용 투명성, 기준검증 시스템의 전체 라이프사이클을 지원한다.
allowed-tools: [Read, Bash, Grep, Glob]
compatibility: "Requires python3 (stdlib only), jq, bash, bc, curl, git. PyYAML required only for install.sh (pip install pyyaml). Optional: Notion MCP tool for Notion workspace integration."
tags: [compliance, RBAC, security, cost-tracking, audit-log, gateway, firestore, deploy-gate, P0, quick, full, improve, slash-command]
platforms: [Claude, Gemini, Codex, OpenCode]
version: 1.0.0
source: user-installed skill
---

# ai-tool-compliance - 내부 AI 툴 컴플라이언스 자동화

## When to use this skill

- **신규 AI 프로젝트 시작**: 컴플라이언스 기반 구조(RBAC, Gateway, 로그, 비용 추적)를 처음부터 스캐폴딩할 때
- **배포 전 P0 전수 검증**: 13개 P0 필수 요건을 자동으로 pass/fail 판정하고 준수 점수를 산출할 때
- **RBAC 설계 및 권한 매트릭스 생성**: Super Admin/Admin/Manager/Viewer/Guest 5역할 + 게임/메뉴/기능 단위 세부 접근 제어를 정의할 때
- **기존 코드 컴플라이언스 감사**: 이미 존재하는 코드베이스를 가이드에 맞게 점검하고 위반 항목을 식별할 때
- **비용 투명성 구현**: 액션별 모델/토큰/BQ 스캔량/비용 추적 체계를 구축할 때
- **행동 로그 스키마 설계**: 전수 행동 로그 기록 체계(Firestore/BigQuery)를 설계할 때
- **역할별 검증 워크플로우**: Section 14 기반 릴리스 승인 프로세스(서비스안정화/Engineer/PM/CEO)를 구성할 때
- **기준검증 시스템 구축**: Rule Registry + Evidence Collector + Verifier Engine + Risk Scorer + Gatekeeper 아키텍처를 설정할 때

---

## Installation

```bash
npx skills add https://github.com/supercent-io/skills-template --skill ai-tool-compliance
```

---

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| 프로젝트 초기화 | `/compliance-init` | RBAC 매트릭스, Gateway boilerplate, 로그 스키마, 비용 추적 인터페이스 생성 |
| 빠른 스캔 | `/compliance-scan`, `/compliance-quick`, `/quick` | P0 핵심 항목 빠른 점검 (코드 패턴 기반) |
| 전수 검증 | `/compliance-verify`, `/compliance-full`, `/full` | 11개 P0 룰 전수 검증 + 준수 점수 산출 |
| 점수 확인 | `/compliance-score` | 현재 준수 점수(보안/권한/비용/로그) 표시 |
| 배포 게이트 | `/compliance-gate` | Green/Yellow/Red 판정 + 배포 승인/차단 결정 |
| 개선 가이드 | `/compliance-improve`, `/improve` | 위반 항목별 구체적 수정 제안 + 재검증 루프 |

### Slash Mode Router

모드 슬래시 명령어는 아래와 같이 매핑된다.

- `/quick`, `/compliance-quick` -> Quick Scan (`/compliance-scan`)
- `/full`, `/compliance-full` -> Full Verify (`/compliance-verify`)
- `/improve` -> Improve (`/compliance-improve`)

---

## 3가지 실행 모드

### 1. Quick Scan (`quick-scan`)

코드베이스를 정적 분석하여 P0 위반 가능성을 빠르게 식별한다.

**실행 방법**: `/compliance-scan`, `/compliance-quick`, `/quick` 또는 트리거 키워드 `컴플라이언스 스캔`, `quick scan`

**수행 내용**:
- Grep/Glob 기반 코드 패턴 검색
- 외부 API 직접 호출 탐지 (Gateway 우회 여부)
- Firestore 클라이언트 직접 접근 탐지
- 하드코딩된 민감 정보 탐지
- Guest 역할 누락 여부 확인

**산출물**: 위반 의심 항목 목록 (파일 경로 + 라인 번호 + 룰 ID)

**소요 시간**: 1~3분

### 2. Full Verify (`full-verify`)

11개 P0 룰을 전수 검증하고 정량적 준수 점수를 산출한다.

**실행 방법**: `/compliance-verify`, `/compliance-full`, `/full` 또는 트리거 키워드 `P0 검증`, `full verify`, `배포 검증`

**수행 내용**:
- 11개 P0 룰 각각에 대해 Evidence 수집 + pass/fail 판정
- 4개 영역별 점수 산출 (보안 40점 / 권한 25점 / 비용 20점 / 로그 15점)
- 총 준수 점수 계산 (100점 만점)
- 배포 게이트 등급 판정 (Green/Yellow/Red)
- 역할별 승인 체크리스트 생성

**산출물**: 컴플라이언스 리포트 (`compliance-report.md`)

```
## Compliance Report
- Date: 2026-03-03
- Project: my-ai-tool
- Score: 92/100 (Green)

### Rule Results
| Rule ID | Rule Name | Result | Evidence |
|---------|-----------|--------|----------|
| AUTH-P0-001 | 신규 가입자 Guest 강제 | PASS | signup.ts:45 role='guest' |
| AUTH-P0-002 | Guest 메뉴/API 접근 차단 | PASS | middleware.ts:12 guestBlock |
| ... | ... | ... | ... |

### Score Breakdown
- 보안: 33/40
- 권한: 25/25
- 비용: 17/20
- 로그: 12/15
- Total: 92/100

### Gate Decision: GREEN - 배포 승인
```

**소요 시간**: 5~15분 (프로젝트 규모에 따라 다름)

### 3. Improve (`improve`)

위반 항목에 대한 구체적 수정 가이드를 제공하고 재검증 루프를 실행한다.

**실행 방법**: `/compliance-improve`, `/improve` 또는 트리거 키워드 `컴플라이언스 개선`, `위반 수정`

**수행 내용**:
- 각 FAIL 항목에 대한 코드 레벨 수정 제안 (파일 경로 + 변경 전/후 코드)
- 수정 적용 후 해당 룰 재검증
- 점수 변화 추적 (Before -> After)
- P0 통과 후 P1 권장 요건 점진 도입 가이드

**산출물**: 수정 제안서 + 재검증 결과

### Improve 모드 자동 수정 로직

```
/compliance-improve 실행
       |
  1. 최근 verification-run.json 로드
       |
  2. FAIL 항목 추출 (rule_id + evidence)
       |
  3. 각 FAIL에 대해:
       |
     a. evidence 파일:줄번호에서 위반 코드 Read
     b. rule.remediation + rule.check_pattern.must_contain에서 수정 방향 도출
     c. 변경 전/후 코드 diff 생성
     d. Write로 수정 적용 (사용자 확인 후)
     e. 해당 룰만 재검증 (Grep 패턴 재실행)
     f. PASS 전환 확인
       |
  4. 전체 재검증 (/compliance-verify)
       |
  5. Before/After 점수 비교 출력
       |
  6. 잔여 FAIL 없으면 → P1 권장 요건 도입 가이드 제시
```

**수정 적용 우선순위**:
1. `must_not_contain` 위반 (즉시 제거 필요) → 해당 코드 삭제 또는 서버 API 호출로 교체
2. `must_contain` 미충족 (패턴 추가 필요) → remediation 가이드에 따라 코드 삽입
3. Warning (부분 충족) → 미충족 파일에만 보완 적용

---

## P0 룰 카탈로그

내부 AI 툴 필수 구현 가이드 v1.1 기반 11개 P0 룰:

| Rule ID | Category | Rule Name | Description | 배점 |
|---------|----------|-----------|-------------|------|
| AUTH-P0-001 | 권한 | 신규 가입자 Guest 강제 | 신규 가입 시 role=Guest 자동 할당, 초대 기반으로만 상위 역할 부여 | 권한 8 |
| AUTH-P0-002 | 권한 | Guest 메뉴/API 접근 차단 | Guest에게 툴명, 모델명, 내부 인프라, 비용, 구조 비노출. 허용된 메뉴/API만 접근 | 권한 7 |
| AUTH-P0-003 | 권한 | 서버 최종 권한 검증 | 모든 API 요청에 서버 사이드 권한 검증 미들웨어 필수. 클라이언트 권한 체크만으로 불충분 | 권한 10 |
| SEC-P0-004 | 보안 | Firestore 직접 접근 금지 | 클라이언트에서 Firestore 직접 read/write 금지. Cloud Functions 경유만 허용 | 보안 12 |
| SEC-P0-005 | 보안 | 외부 API Gateway 강제 | 외부 AI API(Gemini, OpenAI 등) 직접 호출 금지. 반드시 내부 Gateway(Cloud Functions) 경유 | 보안 18 |
| SEC-P0-009 | 보안 | 민감 텍스트 서버 처리 | 민감 원문(프롬프트, 응답 전문)은 서버에서만 처리. 클라이언트에는 참조값(ID)만 전달 | 보안 10 |
| COST-P0-006 | 비용 | 모델 호출 비용 로그 | 모든 AI 모델 호출 시 model, inputTokens, outputTokens, estimatedCost 기록 필수 | 비용 10 |
| COST-P0-007 | 비용 | BQ 스캔 비용 로그 | BigQuery 쿼리 실행 시 bytesProcessed, estimatedCost 기록 필수 | 비용 5 |
| COST-P0-011 | 비용 | 캐시 우선 조회 | 고비용 API 호출 전 캐시 조회 필수. 캐시 미스 시에만 실제 호출 | 비용 5 |
| LOG-P0-008 | 로그 | 실패 요청 로그 필수 | 모든 실패 요청(4xx, 5xx, timeout)에 대한 로그 기록 필수. 누락 금지 | 로그 10 |
| LOG-P0-010 | 로그 | 권한 변경 감사 로그 | Role 변경, 권한 부여/회수, 초대 발송 등 권한 관련 이벤트 전수 기록 | 로그 5 |

### 점수 체계

| 영역 | 만점 | 포함 룰 |
|------|------|---------|
| 보안 | 40 | SEC-P0-004, SEC-P0-005, SEC-P0-009 |
| 권한 | 25 | AUTH-P0-001, AUTH-P0-002, AUTH-P0-003 |
| 비용 | 20 | COST-P0-006, COST-P0-007, COST-P0-011 |
| 로그 | 15 | LOG-P0-008, LOG-P0-010 |
| **합계** | **100** | **11개 P0 룰** |

### 룰별 자동 검증 로직

각 룰의 검증은 `rules/p0-catalog.yaml`에 정의된 `check_pattern`을 기반으로 수행된다. 핵심 메커니즘은 Grep/Glob 정적 분석이다.

**판정 알고리즘 (룰당)**:

```
1. Glob(check_targets) → 대상 파일 수집
2. grep_patterns 매칭 → 해당 기능 사용 파일 식별
   - 매칭 0건 → N/A (해당 기능 미사용, 패널티 없음)
3. must_not_contain 검사 (exclude_paths 제외)
   - 매칭 발견 → 즉시 FAIL + evidence 기록
4. must_contain 검사
   - 전체 충족 → PASS
   - 부분 충족 → WARNING
   - 미충족 → FAIL
```

**룰별 핵심 Grep 패턴**:

| Rule ID | 기능 탐지 (grep_patterns) | 준수 확인 (must_contain) | 위반 탐지 (must_not_contain) |
|---------|--------------------------|-------------------------|----------------------------|
| AUTH-P0-001 | `signup\|register\|createUser` | `role.*['"]guest['"]` | `role.*['"]admin['"]` (가입 시) |
| AUTH-P0-002 | `guard\|middleware\|authorize` | `guest.*block\|guest.*deny` | -- |
| AUTH-P0-003 | `router\.(get\|post\|put\|delete)` | `auth\|verify\|authenticate` | -- |
| SEC-P0-004 | -- (전체 대상) | -- | `firebase/firestore\|getDocs\|setDoc` (클라이언트 경로) |
| SEC-P0-005 | -- (전체 대상) | -- | `fetch\(['"]https?://(?!localhost)` (클라이언트 경로) |
| SEC-P0-009 | -- (전체 대상) | -- | `res\.json\(.*password\|console\.log\(.*token` |
| COST-P0-006 | `openai\|vertexai\|gemini\|anthropic` | `cost\|token\|usage\|billing` | -- |
| COST-P0-007 | `bigquery\|BigQuery\|createQueryJob` | `totalBytesProcessed\|bytesProcessed\|cost` | -- |
| COST-P0-011 | `openai\|vertexai\|gemini\|anthropic` | `cache\|Cache\|redis\|memo` | -- |
| LOG-P0-008 | `catch\|errorHandler\|onError` | `logger\|log\.error\|winston\|pino` | -- |
| LOG-P0-010 | `updateRole\|changeRole\|setRole` | `audit\|auditLog\|eventLog` | -- |

**상세 스키마**: `rules/p0-catalog.yaml` 및 `REFERENCE.md`의 "Judgment Algorithm" 섹션 참조

---

## 검증 시나리오 (QA)

Full Verify 모드(`/compliance-verify`)에서 실행되는 5개 핵심 검증 시나리오. 각 시나리오는 관련 P0 룰을 묶어 end-to-end로 검증한다.

| ID | 시나리오 | 관련 룰 | 검증 방법 | Pass 기준 |
|----|---------|---------|----------|----------|
| SC-001 | **신규 가입 -> Guest 격리** | AUTH-P0-001, AUTH-P0-002 | 회원가입 코드에서 role=guest 할당 확인 + Guest로 보호된 API 호출 시 403 반환 패턴 확인 | role이 guest이고, 보호 API에 접근 불가 패턴 존재 시 PASS |
| SC-002 | **AI 호출 -> Gateway 경유 + 비용 기록** | SEC-P0-005, COST-P0-006, COST-P0-011 | (1) 외부 API 직접 호출 코드 부재 확인 (2) Gateway 함수 경유 확인 (3) 비용 로그 필드(model, tokens, cost) 기록 확인 (4) 캐시 조회 로직 존재 확인 | Gateway 경유 + 비용 로그 4필드 기록 + 캐시 레이어 존재 시 PASS |
| SC-003 | **Firestore 접근 -> Functions 경유 전용** | SEC-P0-004, AUTH-P0-003 | (1) 클라이언트 코드에서 Firestore SDK 직접 import 탐지 (2) 서버 사이드 권한 검증 미들웨어 존재 확인 | 클라이언트 직접 접근 코드 0건 + 서버 미들웨어 존재 시 PASS |
| SC-004 | **실패 요청 -> 로그 누락 없음** | LOG-P0-008, LOG-P0-010 | (1) error handler에서 로그 기록 호출 확인 (2) catch 블록에서 로그 누락 없음 확인 (3) 권한 변경 이벤트에 감사 로그 존재 확인 | 모든 error handler에 로그 호출 존재 + 권한 변경 감사 로그 존재 시 PASS |
| SC-005 | **민감 데이터 -> 클라이언트 비노출** | SEC-P0-009, AUTH-P0-002 | (1) API 응답에 프롬프트/응답 전문이 포함되지 않고 참조 ID만 반환 확인 (2) Guest 응답에 모델명/비용/인프라 정보 미포함 확인 | 응답에 원문 미포함 + Guest 노출 통제 확인 시 PASS |

### 시나리오별 검증 흐름

```
SC-001: grep signup/register -> assert role='guest' -> grep guestBlock/guestDeny -> assert exists
SC-002: grep fetch(https://) in client -> assert 0 hits -> grep gateway log -> assert cost fields -> assert cache check
SC-003: grep firebase/firestore in client/ -> assert 0 hits -> grep authMiddleware in functions/ -> assert exists
SC-004: grep catch blocks -> assert logAction in each -> grep roleChange -> assert auditLog
SC-005: grep res.json for raw text -> assert 0 hits -> grep guest response -> assert no model/cost info
```

---

## 역할별 Go/No-Go 체크포인트

배포 게이트 판정 후, 등급에 따라 해당 역할의 Go/No-Go 체크포인트를 통과해야 한다. **4개 역할 x 5개 항목 = 총 20개 체크포인트**.

### 서비스안정화 (5개)

| # | 체크포인트 | Go 조건 | No-Go 조건 |
|---|-----------|---------|-----------|
| 1 | SLA 영향 분석 | 기존 서비스 가용성/응답시간 SLA에 영향 없음 확인 | SLA 영향 미분석 또는 저하 예상 |
| 2 | 롤백 절차 | 롤백 절차 문서화 + 테스트 완료 | 롤백 절차 미수립 |
| 3 | 성능 테스트 | 부하/스트레스 테스트 완료 + 기준치 이내 | 성능 테스트 미실행 |
| 4 | 장애 알림 | 장애 감지 알림 채널(Slack/PagerDuty 등) 설정 완료 | 알림 채널 미설정 |
| 5 | 모니터링 대시보드 | 핵심 메트릭(에러율, 응답시간, AI 비용) 대시보드 존재 | 모니터링 부재 |

### Engineer (5개)

| # | 체크포인트 | Go 조건 | No-Go 조건 |
|---|-----------|---------|-----------|
| 1 | FAIL 룰 원인 분석 | 모든 FAIL 룰의 근본 원인 식별 + 문서화 | 원인 미식별 항목 존재 |
| 2 | 수정 코드 검증 | 수정 코드가 해당 룰의 의도를 정확히 반영 | 수정이 룰 의도와 불일치 |
| 3 | 재검증 통과 | 수정 후 재검증에서 해당 룰 PASS 전환 | 재검증 미실행 또는 여전히 FAIL |
| 4 | 회귀 영향 없음 | 수정이 다른 P0 룰에 부정적 영향 없음 확인 | 다른 룰이 새로 FAIL |
| 5 | 코드 리뷰 완료 | 수정 코드에 대한 코드 리뷰 승인 완료 | 코드 리뷰 미완료 |

### PM (5개)

| # | 체크포인트 | Go 조건 | No-Go 조건 |
|---|-----------|---------|-----------|
| 1 | 사용자 영향 평가 | 미달 항목의 사용자 영향이 수용 가능 | 사용자 영향 미평가 |
| 2 | 일정 리스크 | 수정 소요 시간이 릴리스 일정 내 | 일정 초과 예상 |
| 3 | 범위 합의 | 범위 변경 시 이해관계자 합의 완료 | 합의 미완료 |
| 4 | 비용 영향 | AI 사용 비용이 승인된 예산 범위 내 | 예산 초과 예상 |
| 5 | 커뮤니케이션 | 변경 사항이 관련 팀에 공유됨 | 미공유 |

### CEO (5개)

| # | 체크포인트 | Go 조건 | No-Go 조건 |
|---|-----------|---------|-----------|
| 1 | 비용 상한 | 월간 AI 비용이 사전 승인 예산 이내 | 예산 상한 초과 |
| 2 | 보안 리스크 | 보안 P0 전수 통과 또는 예외 사유 합리적 | P0 보안 FAIL + 예외 사유 불충분 |
| 3 | 법적/규제 리스크 | 데이터 처리가 관련 법규(개인정보보호법 등) 준수 | 법적 리스크 미검토 |
| 4 | 사업 연속성 | 배포 실패 시 사업 영향이 제한적 | 사업 중단 리스크 존재 |
| 5 | 최종 승인 | 위 4개 항목 모두 Go이면 최종 승인 | 1개라도 No-Go이면 보류 |

---

## 리포트 형식

`/compliance-verify` 실행 시 생성되는 `compliance-report.md`는 6개 섹션으로 구성된다.

### 리포트 섹션 구조 (6개)

```markdown
# Compliance Report

## 1. Summary (요약)
- 프로젝트명, 검증 일시, 검증 모드 (quick-scan / full-verify)
- 총 준수 점수 / 100
- 배포 게이트 등급 (Green / Yellow / Red)
- P0 FAIL 건수
- 검증 소요 시간

## 2. Rule Results (룰별 결과)
| Rule ID | Category | Rule Name | Result | Score | Evidence |
|---------|----------|-----------|--------|-------|----------|
| AUTH-P0-001 | 권한 | 신규 가입자 Guest 강제 | PASS | 10/10 | signup.ts:45 |
| SEC-P0-005 | 보안 | 외부 API Gateway 강제 | FAIL | 0/15 | client/api.ts:23 직접 fetch |
| ...

## 3. Score Breakdown (영역별 점수)
| 영역 | 획득 | 만점 | 비율 |
|------|------|------|------|
| 보안 | 20 | 40 | 50% |
| 권한 | 25 | 25 | 100% |
| 비용 | 17 | 20 | 85% |
| 로그 | 12 | 15 | 80% |
| **합계** | **79** | **100** | **79%** |

## 4. Failures Detail (실패 상세)
각 FAIL 항목에 대해:
- 위반 코드 위치 (파일:라인)
- 위반 내용 설명
- 권장 수정 방법 (remediation)
- 관련 검증 시나리오 ID (SC-001~SC-005)

## 5. Gate Decision (배포 판정)
- 판정 등급 + 판정 근거
- 필요한 승인 역할 목록
- 역할별 Go/No-Go 체크포인트 현황 (20개 중 미충족 항목 표시)

## 6. Recommendations (권고 사항)
- 즉시 조치: P0 FAIL 수정 (파일 경로 + 수정 가이드)
- 단기 개선: Yellow -> Green 달성 방안
- 중기 도입: P1 권장 요건 도입 순서
```

### 리포트 생성 규칙

1. **Summary는 항상 첫 페이지**: 의사결정자가 점수와 등급을 즉시 확인할 수 있어야 한다
2. **Evidence 필수**: Rule Results의 모든 PASS/FAIL 항목에 코드 증거(파일:라인) 첨부
3. **Failures Detail은 FAIL 항목만**: PASS 항목은 Rule Results 테이블에만 표시
4. **Gate Decision에 역할 매핑**: 등급에 따라 필요한 승인 역할을 자동 표시
5. **Recommendations 우선순위**: 즉시 > 단기 > 중기 순서로 정렬

---

## 배포 게이트 정책

### 등급 판정 기준

| 등급 | 점수 | 조건 | 결정 |
|------|------|------|------|
| **Green** | 90~100 | 모든 P0 PASS + 총점 90 이상 | 자동 배포 승인 |
| **Yellow** | 75~89 | 모든 P0 PASS + 총점 75~89 | 조건부 승인 (PM 확인 필요) |
| **Red** | 0~74 | 총점 74 이하 **또는** P0 FAIL 1건 이상 | 배포 차단 |

### 핵심 규칙

1. **P0 절대 규칙**: P0 FAIL이 1건이라도 있으면 총점과 무관하게 **Red** 판정. 배포 자동 차단
2. **Yellow 조건부**: 총점은 통과했으나 완벽하지 않은 경우. PM이 리스크를 검토하고 승인/반려 결정
3. **Green 자동 승인**: 모든 P0 통과 + 90점 이상이면 추가 승인 없이 배포 가능

### 게이트 실행 흐름

```
/compliance-verify 실행
       |
  11개 P0 룰 전수 검증
       |
  점수 산출 (보안+권한+비용+로그)
       |
  +----+----+----+
  |         |         |
Green     Yellow    Red
  |         |         |
자동 승인  PM 승인   배포 차단
  |       대기      |
  v         |      수정 후
배포       v      재검증
        PM 확인     |
        |    |      v
      승인  반려   /compliance-improve
        |    |
        v    v
      배포  수정 후
            재검증
```

---

## 역할별 승인 프로세스

내부 AI 툴 필수 구현 가이드 Section 14 기반. 배포 등급에 따라 필요한 승인 역할이 달라진다.

### 서비스안정화 (Service Stability)

**책임**: 장애 영향, 성능 저하, 롤백 가능성 검증

체크리스트:
- [ ] 신규 배포가 기존 서비스 SLA에 영향을 주지 않는가
- [ ] 롤백 절차가 문서화되어 있는가
- [ ] 성능 테스트(부하/스트레스)가 완료되었는가
- [ ] 장애 시 알림 채널이 설정되어 있는가

**승인 시점**: Yellow/Red 등급에서 필수

### Engineer

**책임**: 실패 룰의 근본 원인 분석 + 코드 수준 조치 + 재검증

체크리스트:
- [ ] 모든 FAIL 룰의 원인이 식별되었는가
- [ ] 수정 코드가 해당 룰의 의도를 정확히 반영하는가
- [ ] 재검증 결과 해당 룰이 PASS로 전환되었는가
- [ ] 수정이 다른 룰에 부정적 영향을 주지 않는가

**승인 시점**: Red 등급에서 필수 (수정 후 재검증 담당)

### PM (Product Manager)

**책임**: 사용자 영향, 일정 리스크, 범위 변경 승인

체크리스트:
- [ ] 컴플라이언스 미달 항목이 사용자 경험에 미치는 영향이 수용 가능한가
- [ ] 수정에 필요한 일정이 전체 릴리스 일정에 미치는 영향이 수용 가능한가
- [ ] 범위 축소/연기가 필요한 경우 이해관계자와 합의되었는가

**승인 시점**: Yellow 등급에서 필수

### CEO

**책임**: 비용 상한, 사업 리스크, 최종 승인

체크리스트:
- [ ] AI 사용 비용이 사전 승인된 예산 범위 내인가
- [ ] 보안 위험이 사업적으로 수용 가능한 수준인가
- [ ] 법적/규제 리스크가 식별 및 관리되고 있는가

**승인 시점**: 비용 상한 초과 또는 보안 P0 예외 승인 시

---

## 프로젝트 초기화 (`/compliance-init`)

### 생성되는 파일 구조

```
project/
├── compliance/
│   ├── rbac-matrix.yaml          # 5역할 x 게임/메뉴/기능 권한 매트릭스
│   ├── rules/
│   │   └── p0-rules.yaml         # 11개 P0 룰 정의
│   ├── log-schema.yaml           # 행동 로그 스키마 (Firestore/BigQuery)
│   └── cost-tracking.yaml        # 비용 추적 필드 정의
├── compliance-config.yaml        # 프로젝트 메타 + 검증 설정
└── compliance-report.md          # 검증 결과 리포트 (verify 실행 시 생성)
```

### 각 YAML 파일 스키마

**compliance-config.yaml** (프로젝트 루트):

```yaml
project:
  name: "my-ai-tool"
  type: "web-app"           # web-app | api | mobile-app | library
  tech_stack: ["typescript", "firebase", "next.js"]

verification:
  catalog_path: "compliance/rules/p0-rules.yaml"   # 기본값
  exclude_paths:                                     # 검증 제외 경로
    - "node_modules/**"
    - "dist/**"
    - "**/*.test.ts"
    - "**/*.spec.ts"

scoring:
  domain_weights:            # 합계 = 100
    security: 40
    auth: 25
    cost: 20
    logging: 15

gate:
  green_threshold: 90        # 90점 이상 = 자동 승인
  yellow_threshold: 75       # 75~89점 = PM 확인 필요
  p0_fail_override: true     # P0 FAIL 시 점수 무관 Red 판정
```

**compliance/log-schema.yaml** (행동 로그 스키마):

```yaml
log_schema:
  version: "1.0.0"
  storage:
    primary: "firestore"           # 실시간 접근용
    archive: "bigquery"            # 분석/감사용
    retention:
      hot: 90                      # 일 (Firestore)
      cold: 365                    # 일 (BigQuery)

  fields:
    - name: userId
      type: string
      required: true
    - name: action
      type: string
      required: true
      description: "수행 동작 (ai_call, role_change, login, etc.)"
    - name: timestamp
      type: timestamp
      required: true
    - name: model
      type: string
      required: false
      description: "AI 모델명 (gemini-1.5-flash 등)"
    - name: inputTokens
      type: number
      required: false
    - name: outputTokens
      type: number
      required: false
    - name: estimatedCost
      type: number
      required: false
      description: "USD 기준 예상 비용"
    - name: status
      type: string
      required: true
      enum: [success, fail, timeout, error]
    - name: errorMessage
      type: string
      required: false
    - name: metadata
      type: map
      required: false
      description: "추가 컨텍스트 (bytesProcessed, cacheHit 등)"
```

**compliance/cost-tracking.yaml** (비용 추적 필드):

```yaml
cost_tracking:
  version: "1.0.0"

  ai_models:
    required_fields:
      - model              # 모델 식별자
      - inputTokens        # 입력 토큰 수
      - outputTokens       # 출력 토큰 수
      - estimatedCost      # USD 예상 비용
    optional_fields:
      - cacheHit           # 캐시 히트 여부
      - latencyMs          # 응답 지연 (ms)

  bigquery:
    required_fields:
      - queryId            # 쿼리 식별자
      - bytesProcessed     # 스캔 바이트
      - estimatedCost      # USD 예상 비용
    optional_fields:
      - slotMs             # 슬롯 사용 시간
      - cacheHit           # BQ 캐시 히트 여부

  cost_formula:
    gemini_flash: "$0.075 / 1M input tokens, $0.30 / 1M output tokens"
    gemini_pro: "$1.25 / 1M input tokens, $5.00 / 1M output tokens"
    bigquery: "$5.00 / TB scanned"
```

### RBAC 매트릭스 기본 구조

```yaml
# compliance/rbac-matrix.yaml
roles:
  - id: super_admin
    name: Super Admin
    description: 전체 시스템 관리 + 역할 부여 권한
  - id: admin
    name: Admin
    description: 서비스 설정 + 사용자 관리
  - id: manager
    name: Manager
    description: 팀/게임 단위 관리
  - id: viewer
    name: Viewer
    description: 읽기 전용 접근
  - id: guest
    name: Guest
    description: 최소 접근 (툴명/모델명/비용/구조 비노출)

permissions:
  - resource: "dashboard"
    actions:
      super_admin: [read, write, delete, admin]
      admin: [read, write, delete]
      manager: [read, write]
      viewer: [read]
      guest: []  # 접근 불가
  # ... 게임/메뉴/기능별 확장
```

### Gateway 패턴 예시

```typescript
// functions/src/gateway/ai-gateway.ts
// 외부 API 직접 호출 금지 - 반드시 이 Gateway 경유

import { onCall, HttpsError } from "firebase-functions/v2/https";
import { verifyRole } from "../auth/rbac";
import { logAction } from "../logging/audit";
import { checkCache } from "../cache/cost-cache";

export const callAIModel = onCall(async (request) => {
  // 1. 서버 사이드 권한 검증 (AUTH-P0-003)
  const user = await verifyRole(request.auth, ["admin", "manager"]);

  // 2. Guest 접근 차단 (AUTH-P0-002)
  if (user.role === "guest") {
    throw new HttpsError("permission-denied", "Access denied");
  }

  // 3. 캐시 우선 조회 (COST-P0-011)
  const cached = await checkCache(request.data.prompt);
  if (cached) {
    await logAction({
      userId: user.uid,
      action: "ai_call",
      source: "cache",
      cost: 0,
    });
    return { result: cached, fromCache: true };
  }

  // 4. Gateway 경유 AI 호출 (SEC-P0-005)
  const result = await callGeminiViaGateway(request.data.prompt);

  // 5. 비용 로그 기록 (COST-P0-006)
  await logAction({
    userId: user.uid,
    action: "ai_call",
    model: result.model,
    inputTokens: result.usage.inputTokens,
    outputTokens: result.usage.outputTokens,
    estimatedCost: result.usage.estimatedCost,
  });

  // 6. 민감 원문은 서버에서만 처리, 클라이언트에는 참조 ID 반환 (SEC-P0-009)
  const responseRef = await storeResponse(result.text);
  return { responseId: responseRef.id, summary: result.summary };
});
```

<!-- TODO: Designer 결과 보완 예정 - compliance-report.md 의 시각적 포맷 및 대시보드 UI -->

---

## 타 스킬과의 관계

### bmad-orchestrator와의 연동

`bmad-orchestrator`가 프로젝트 전체 개발 단계(Analysis -> Planning -> Solutioning -> Implementation)를 관리한다면, `ai-tool-compliance`는 각 단계의 산출물이 컴플라이언스를 충족하는지 검증하는 보조 도구로 작동한다.

**권장 사용 순서**:
1. `/workflow-init` (bmad) -- 프로젝트 구조 수립
2. `/compliance-init` (compliance) -- 컴플라이언스 기반 구조 생성
3. Phase 3 Architecture 완료 후 `/compliance-scan` -- 아키텍처 수준 컴플라이언스 점검
4. Phase 4 Implementation 완료 후 `/compliance-verify` -- 전수 검증 + 배포 게이트 판정

### security-best-practices와의 관계

`security-best-practices`는 범용 웹 보안 패턴(OWASP, HTTPS, XSS, CSRF)을 제공한다. `ai-tool-compliance`는 이를 전제 조건으로 삼되, 조직 특화 요건(RBAC 5역할, Gateway 강제, 비용 투명성, 전수 행동 로그)에 집중한다.

| 항목 | security-best-practices | ai-tool-compliance |
|------|------------------------|--------------------|
| RBAC | 일반 언급 | 5역할 + 게임/메뉴/기능 단위 매트릭스 |
| API 보안 | Rate Limiting, CORS | Gateway 강제 + 비용 로그 |
| 데이터 보호 | XSS, CSRF, SQL Injection | 민감 원문 서버 처리 + Firestore 정책 |
| 로그 | 보안 이벤트 로깅 | 전수 행동 로그 + 스키마/보관 정책 |
| 배포 게이트 | 없음 | 준수 점수 기반 자동 차단 |

### code-review와의 관계

`code-review`가 코드 품질/가독성/보안을 주관적으로 리뷰한다면, `ai-tool-compliance`는 "내부 AI 툴 가이드를 통과하는가?"에 대한 정량적 판정(100점 만점, pass/fail)을 제공한다. 코드 리뷰 시 `/compliance-scan` 결과를 참고 자료로 활용할 수 있다.

### workflow-automation과의 관계

`workflow-automation`이 범용 CI/CD 패턴(npm scripts, Makefile, GitHub Actions)을 제공한다면, `ai-tool-compliance`는 해당 파이프라인에 삽입되는 도메인 특화 검증 단계를 제공한다.

### scripts/ 디렉토리 상세 구현

#### install.sh -- 스킬 설치 및 초기화

```bash
bash scripts/install.sh [options]
  --dry-run        변경 없이 미리보기
  --skip-checks    의존성 확인 건너뛰기
```

수행 내용:
1. 의존성 확인 (yq, jq -- 선택적, 없으면 기본 파싱 사용)
2. 모든 scripts/*.sh에 chmod +x 적용
3. rules/p0-catalog.yaml YAML 구문 검증
4. 설치 완료 요약 출력

#### verify.sh -- P0 룰 전수 검증

```bash
bash scripts/verify.sh [--rule RULE_ID] [--output JSON_PATH]
```

수행 내용:
1. `rules/p0-catalog.yaml` 파싱 (yq 또는 grep 기반)
2. 각 룰에 대해:
   - `check_targets` Glob으로 대상 파일 수집
   - `grep_patterns`로 기능 사용 여부 탐지 (미사용 시 N/A)
   - `must_not_contain` 위반 탐지 (exclude_paths 제외)
   - `must_contain` 준수 확인
   - Pass/Fail/Warning/N/A 판정 + evidence 수집
3. 결과를 `templates/verification-run.json` 형식으로 출력
4. 콘솔에 요약 테이블 출력

#### score.sh -- 준수 점수 산출

```bash
bash scripts/score.sh [--input VERIFY_JSON] [--verbose]
```

수행 내용:
1. verify.sh 결과 JSON 로드 (또는 직접 verify.sh 실행)
2. 영역별 점수 계산:
   - Pass=배점 100%, Warning=배점 50%, Fail=0%, N/A=분모 제외
   - 보안: SEC 룰 점수 합 / 보안 만점(35)
   - 권한: AUTH 룰 점수 합 / 권한 만점(30)
   - 비용: COST 룰 점수 합 / 비용 만점(20)
   - 로그: LOG 룰 점수 합 / 로그 만점(15)
3. 총점 산출 (100점 만점)
4. `templates/risk-score-report.md` 렌더링
5. `templates/remediation-task.json` 생성 (각 FAIL 항목별)

#### gate.sh -- 배포 게이트 체크

```bash
bash scripts/gate.sh
# exit 0 = Green (배포 승인)
# exit 1 = Red (배포 차단)
# exit 2 = Yellow (조건부 -- PM 확인 필요)
```

수행 내용:
1. verify.sh + score.sh 순차 실행
2. P0 FAIL 존재 여부 확인
   - 1건이라도 있으면 → Red (exit 1)
3. 총점 기반 등급 판정
   - 90+ → Green (exit 0)
   - 75~89 → Yellow (exit 2)
   - 74 이하 → Red (exit 1)
4. 등급 + 점수 + 수정 필요 목록 콘솔 출력

**CI/CD 통합 예시 (GitHub Actions)**:

```yaml
# .github/workflows/compliance-gate.yml
name: Compliance Gate
on: [pull_request]
jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run compliance gate
        run: bash .agent-skills/ai-tool-compliance/scripts/gate.sh
```
<!-- TODO: System 결과 보완 예정 - GitHub Actions 워크플로우 통합 YAML -->

---

## P1 권장 요건 (점진 도입)

P0 전수 통과 후 점진적으로 도입을 권장하는 항목:

| 영역 | 요건 | 설명 |
|------|------|------|
| 도메인 관리 | 허용 도메인 화이트리스트 | AI Gateway가 호출할 수 있는 외부 도메인 제한 |
| 사용량 통계 | 사용자별/팀별 사용량 집계 | 일/주/월 단위 사용량 대시보드 |
| 비용 통제 | 예산 상한 알림 | 팀/프로젝트별 비용 임계값 초과 시 알림 |
| 로그 보관 | 로그 보관 정책 | 90일 Hot / 365일 Cold / 이후 삭제 정책 |

### P1 v1.1 룰 카탈로그 (추가 확장)

| Rule ID | 영역 | 체크 타입 | 핵심 기준 | 배점 |
|---------|------|-----------|-----------|------|
| P1-DOM-001 | Domain Management | static_analysis | 도메인 CRUD 이력 + `createdAt/updatedAt/status/owner` 메타데이터 | 7 |
| P1-STAT-002 | Statistics | api_test | 사용자/모델/기간/게임 필터 통계 + 비용 집계 최신성(<1h) | 6 |
| P1-COST-003 | Cost Control | config_check | 예산 80% 경고 + 100% 차단(429/403) + 리셋 주기 | 6 |
| P1-LOG-004 | Logging | config_check | 로그 스키마 검증 + 6개월+ 보관 + 검색/Export | 6 |

### Notion 테이블 정렬용 표준 컬럼 (추가)

| 컬럼 | 설명 | 소스 |
|------|------|------|
| Rule ID | 기준 식별자 | rules/p1-catalog.yaml |
| Category/Domain | 컴플라이언스 영역 | rules/p1-catalog.yaml |
| Check Type | 검증 방식(static/api/config/log) | rules/*-catalog.yaml |
| Pass/Fail Condition | 판정 기준 | rules/*-catalog.yaml |
| Score Impact | 가중치 | rules/*-catalog.yaml |
| Evidence | 파일:라인 또는 설정 근거 | verify 결과 JSON |
| Owner Role | 조치 담당 역할 | compliance-report / role checklist |
| Action Queue | 1주 이내 개선 항목 | remediation-task / report |

### 기준검증 시스템 설계 (추가)

| 컴포넌트 | 책임 | 산출물 |
|----------|------|--------|
| Rule Registry | P0/P1 카탈로그 버전 관리 및 로드 정책 | `rules/catalog.json`, `rules/catalog-p1.json`, `rules/catalog-all.json` |
| Evidence Collector | 코드/설정/API 증거 수집 및 정규화 | `verify.sh` 결과의 evidence/violations |
| Verifier Engine | 룰별 PASS/FAIL/WARNING/NA 판정 | `/tmp/compliance-verify.json` |
| Risk Scorer | P0 Gate Score + P1 Maturity Score 계산 | `/tmp/compliance-score.json` |
| Gatekeeper | 배포 차단(P0)과 권고(P1) 의사결정 분리 | `gate.sh` exit code + gate summary |

### 운영 모드 (추가, 기존 흐름 유지)

| 모드 | 명령 | 동작 |
|------|------|------|
| P0 기본 | `bash scripts/verify.sh .` | 기존 P0 룰만 검증 (기본값, 역호환) |
| P0+P1 확장 | `bash scripts/verify.sh . --include-p1` | P0 검증 + P1 권장 룰 동시 검증 |
| 게이트 판정 | `bash scripts/gate.sh --score-file ...` | P0 기준으로 배포 판정, P1은 성숙도/개선 추적 |

---

## Constraints

### 필수 규칙 (MUST)

1. **P0 절대 원칙**: P0 룰 11개는 예외 없이 검증한다. 부분 검증은 허용하지 않는다
2. **서버 최종 검증**: 모든 권한 판정은 서버에서 수행한다. 클라이언트 검증만으로는 PASS 불가
3. **Gateway 강제**: 외부 AI API 직접 호출이 발견되면 무조건 FAIL. 우회 허용 불가
4. **Guest 기본값**: 신규 가입 시 Guest 외 역할 할당이 발견되면 FAIL
5. **증거 기반 판정**: 모든 pass/fail은 코드 증거(파일 경로 + 라인 번호)를 첨부한다

### 금지 사항 (MUST NOT)

1. **P0 예외 승인 남용**: P0 예외는 CEO 승인 없이 절대 허용하지 않는다
2. **점수 조작**: Evidence 없는 PASS 판정 금지
3. **Gateway 우회**: "테스트 목적" 등의 이유로 외부 API 직접 호출을 허용하지 않는다
4. **로그 선택적 기록**: 성공 요청만 기록하고 실패 요청을 누락하는 것을 허용하지 않는다

---

## Best practices

1. **Shift Left**: 프로젝트 시작 시 `/compliance-init`으로 기반 구조를 먼저 생성한 후 비즈니스 로직을 구현한다
2. **점진적 도입**: P0 전수 통과 -> P1 순서로 도입한다. P1부터 시작하지 않는다
3. **재검증 루프**: 위반 수정 후 반드시 `/compliance-verify`를 재실행하여 점수 변화를 확인한다
4. **BMAD 연동**: bmad-orchestrator Phase 4 완료 후 compliance-verify를 실행하는 것을 표준 워크플로우로 채택한다
5. **CI/CD 통합**: GitHub Actions에 compliance-gate 단계를 추가하여 자동화한다

---

## References

- 내부 AI 툴 필수 구현 가이드 v1.1 (Notion)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Firebase Security Rules](https://firebase.google.com/docs/rules)
- [Cloud Functions for Firebase](https://firebase.google.com/docs/functions)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2026-03-03
- **호환 플랫폼**: Claude, Gemini, Codex, OpenCode

### 관련 스킬
- [bmad-orchestrator](../bmad-orchestrator/SKILL.md): 개발 단계 오케스트레이션
- [security-best-practices](../security-best-practices/SKILL.md): 범용 웹 보안 패턴
- [code-review](../code-review/SKILL.md): 코드 품질/보안 리뷰
- [workflow-automation](../workflow-automation/SKILL.md): CI/CD 자동화 패턴
- [authentication-setup](../authentication-setup/SKILL.md): 인증/인가 시스템 구축
- [firebase-ai-logic](../firebase-ai-logic/SKILL.md): Firebase AI 통합

### 태그
`#compliance` `#RBAC` `#security` `#cost-tracking` `#audit-log` `#gateway` `#firestore` `#deploy-gate` `#P0` `#AI-tool`
