---
name: looker-studio-bigquery
description: Design and configure Looker Studio dashboards with BigQuery data sources. Use when creating analytics dashboards, connecting BigQuery to visualization tools, or optimizing data pipeline performance. Handles BigQuery connections, custom SQL queries, scheduled queries, dashboard design, and performance optimization.
tags: [Looker-Studio, BigQuery, dashboard, analytics, visualization, GCP, data-studio, SQL]
platforms: [Claude, ChatGPT, Gemini]
---

# Looker Studio BigQuery Integration

## When to use this skill

- **분석 대시보드 생성**: BigQuery 데이터를 시각화하여 비즈니스 인사이트 도출
- **실시간 리포팅**: 자동 새로고침되는 대시보드 구축
- **성능 최적화**: 대용량 데이터셋의 쿼리 비용 및 로딩 시간 최적화
- **데이터 파이프라인**: 스케줄된 쿼리로 ETL 프로세스 자동화
- **팀 협업**: 공유 가능한 인터랙티브 대시보드 구축

## Instructions

### Step 1: GCP BigQuery 환경 준비

**프로젝트 생성 및 활성화**

Google Cloud Console에서 새 프로젝트를 생성하고 BigQuery API를 활성화합니다.

```bash
# gcloud CLI를 사용한 프로젝트 생성
gcloud projects create my-analytics-project
gcloud config set project my-analytics-project
gcloud services enable bigquery.googleapis.com
```

**데이터셋 및 테이블 생성**

```sql
-- 데이터셋 생성
CREATE SCHEMA `my-project.analytics_dataset`
  OPTIONS(
    description="분석용 데이터셋",
    location="US"
  );

-- 예제 테이블 생성 (GA4 데이터)
CREATE TABLE `my-project.analytics_dataset.events` (
  event_date DATE,
  event_name STRING,
  user_id INT64,
  event_value FLOAT64,
  event_timestamp TIMESTAMP,
  geo_country STRING,
  device_category STRING
);
```

**IAM 권한 설정**

Looker Studio에서 BigQuery에 접근할 수 있도록 IAM 권한을 부여합니다:

| 역할 | 설명 |
|------|------|
| `BigQuery Data Viewer` | 테이블 조회 권한 |
| `BigQuery User` | 쿼리 실행 권한 |
| `BigQuery Job User` | 작업 실행 권한 |

### Step 2: Looker Studio에서 BigQuery 연결하기

**네이티브 BigQuery 커넥터 사용 (권장)**

1. Looker Studio 홈페이지에서 **+ 만들기** → **데이터 소스** 클릭
2. "BigQuery"로 검색하여 Google BigQuery 커넥터 선택
3. Google 계정으로 인증
4. 프로젝트, 데이터셋, 테이블 선택
5. **연결**을 클릭하여 데이터 소스 생성

**맞춤 SQL 쿼리 방식**

복잡한 데이터 변환이 필요할 때 SQL을 직접 작성합니다:

```sql
SELECT
  event_date,
  event_name,
  COUNT(DISTINCT user_id) as unique_users,
  SUM(event_value) as total_revenue,
  AVG(event_value) as avg_revenue_per_event
FROM `my-project.analytics_dataset.events`
WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY event_date, event_name
ORDER BY event_date DESC
```

**장점:**
- 복잡한 데이터 변환을 SQL에서 처리
- BigQuery에서 데이터를 미리 집계하여 쿼리 비용 절감
- 매번 모든 데이터를 로드하지 않아 성능 향상

**여러 테이블 조인 방식**

```sql
SELECT
  e.event_date,
  e.event_name,
  u.user_country,
  u.user_tier,
  COUNT(DISTINCT e.user_id) as unique_users,
  SUM(e.event_value) as revenue
FROM `my-project.analytics_dataset.events` e
LEFT JOIN `my-project.analytics_dataset.users` u
  ON e.user_id = u.user_id
WHERE e.event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY e.event_date, e.event_name, u.user_country, u.user_tier
```

### Step 3: 스케줄된 쿼리로 성능 최적화

라이브 쿼리 대신 **스케줄된 쿼리**를 사용하여 주기적으로 데이터를 미리 계산합니다:

```sql
-- BigQuery에서 매일 집계 데이터를 계산하여 저장
CREATE OR REPLACE TABLE `my-project.analytics_dataset.daily_summary` AS
SELECT
  CURRENT_DATE() as report_date,
  event_name,
  user_country,
  COUNT(DISTINCT user_id) as daily_users,
  SUM(event_value) as daily_revenue,
  AVG(event_value) as avg_event_value,
  MAX(event_timestamp) as last_event_time
FROM `my-project.analytics_dataset.events`
WHERE event_date = CURRENT_DATE() - 1
GROUP BY event_name, user_country
```

BigQuery UI에서 **스케줄된 쿼리**로 설정:
- 매일 자동 실행
- 결과를 새로운 테이블에 저장
- Looker Studio는 미리 계산된 테이블에 연결

**장점:**
- Looker Studio 로딩 시간 단축 (50-80%)
- BigQuery 비용 절감 (스캔 데이터 감소)
- 대시보드 새로고침 속도 향상

### Step 4: 대시보드 레이아웃 설계

**F-패턴 레이아웃**

사용자의 자연스러운 읽기 흐름을 따르는 F-패턴을 사용합니다:

```
┌─────────────────────────────────────┐
│ 헤더: 로고 | 필터/날짜선택기        │  ← 사용자가 먼저 본다
├─────────────────────────────────────┤
│ KPI 1  │ KPI 2  │ KPI 3  │ KPI 4   │  ← 핵심 지표 (3-4개)
├─────────────────────────────────────┤
│                                     │
│ 주요 차트 (시계열 또는 비교)        │  ← 깊이 있는 인사이트
│                                     │
├─────────────────────────────────────┤
│ 구체적 데이터 테이블                │  ← 상세 분석
│ (드릴다운 가능)                     │
├─────────────────────────────────────┤
│ 추가 인사이트 / 맵 / 히트맵          │
└─────────────────────────────────────┘
```

**대시보드 구성 요소**

| 요소 | 목적 | 예시 |
|------|------|------|
| **헤더** | 대시보드 제목, 로고, 필터 배치 | "2026년 Q1 판매 분석" |
| **KPI 타일** | 주요 지표 한눈에 표시 | 총 매출, 전월 대비 성장률, 활성 사용자 |
| **추세 차트** | 시간 경과에 따른 변화 | 라인 차트로 일일/주간 매출 추이 |
| **비교 차트** | 카테고리 간 비교 | 막대 차트로 지역/상품별 판매량 비교 |
| **분포 차트** | 데이터 분포 시각화 | 히트맵, 산점도, 버블 차트 |
| **상세 테이블** | 정확한 수치 제공 | 조건부 서식으로 임계값 강조 |
| **맵** | 지리적 데이터 | 국가/지역별 매출 분포 |

**실제 예시: 전자상거래 대시보드**

```
┌──────────────────────────────────────────────────┐
│ 📊 2026년 1월 판매 분석 | 🔽 국가 선택 | 📅 날짜  │
├──────────────────────────────────────────────────┤
│ 총 매출: $125,000  │ 주문수: 3,200   │ 전환율: 3.5% │
├──────────────────────────────────────────────────┤
│         일일 매출 추이 (라인 차트)                │
│    ↗ 상승 추세: +15% vs 지난달                   │
├──────────────────────────────────────────────────┤
│ 카테고리별 판매    │  상위 제품 Top 10            │
│ (막대 차트)        │  (테이블, 정렬 가능)        │
├──────────────────────────────────────────────────┤
│        지역별 매출 분포 (맵)                      │
└──────────────────────────────────────────────────┘
```

### Step 5: 인터랙티브 필터 및 컨트롤

**필터 종류**

**1. 날짜 범위 필터** (필수)
- 캘린더로 특정 기간 선택
- "지난 7일", "이번 달" 같은 사전 정의 옵션
- 데이터셋과 연결하여 모든 차트에 자동 반영

**2. 드롭다운 필터**
```
예: 국가 선택 필터
- 모든 국가
- 한국
- 일본
- 미국
선택하면 해당 국가 데이터만 표시
```

**3. 고급 필터** (SQL 기반)
```sql
-- 매출액이 $10,000 이상인 고객만 표시
WHERE customer_revenue >= 10000
```

**필터 구현 예시**

```sql
-- 1. 날짜 필터
event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL @date_range_days DAY)

-- 2. 드롭다운 필터 (사용자 입력)
WHERE country = @selected_country

-- 3. 복합 필터
WHERE event_date >= @start_date
  AND event_date <= @end_date
  AND country IN (@country_list)
  AND revenue >= @min_revenue
```

### Step 6: 쿼리 성능 최적화

**1. 파티션 키 사용**

```sql
-- ❌ 비효율적인 쿼리
SELECT * FROM events
WHERE DATE(event_timestamp) >= '2026-01-01'

-- ✅ 최적화된 쿼리 (파티션 사용)
SELECT * FROM events
WHERE event_date >= '2026-01-01'  -- 파티션 키 직접 사용
```

**2. 데이터 추출 (Extract and Load)**

매일 밤 Looker Studio 전용 테이블에 데이터를 추출합니다:

```sql
-- 매일 자정에 실행되는 스케줄 쿼리
CREATE OR REPLACE TABLE `my-project.looker_studio_data.dashboard_snapshot` AS
SELECT
  event_date,
  event_name,
  country,
  device_category,
  COUNT(DISTINCT user_id) as users,
  SUM(event_value) as revenue,
  COUNT(*) as events
FROM `my-project.analytics_dataset.events`
WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY event_date, event_name, country, device_category;
```

**3. 캐싱 전략**

- **Looker Studio 기본 캐싱**: 자동으로 3시간 동안 캐시
- **BigQuery 캐싱**: 동일한 쿼리는 이전 결과 재사용 (6시간)
- **스케줄된 쿼리 활용**: 야간에 미리 계산

**4. 대시보드 복잡도 관리**

- 한 대시보드에 최대 20-25개 차트만 사용
- 차트가 많으면 여러 탭(페이지)으로 분산
- 상관없는 메트릭끼리 그룹화하지 않기

### Step 7: Community Connector 개발 (고급)

더 복잡한 요구사항이 있다면 Community Connector를 개발합니다:

```javascript
// Community Connector 예시 (Apps Script)
function getConfig() {
  return {
    configParams: [
      {
        name: 'project_id',
        displayName: 'BigQuery Project ID',
        helpText: 'Your GCP Project ID',
        placeholder: 'my-project-id'
      },
      {
        name: 'dataset_id',
        displayName: 'Dataset ID'
      }
    ]
  };
}

function getData(request) {
  const projectId = request.configParams.project_id;
  const datasetId = request.configParams.dataset_id;

  // BigQuery에서 데이터 로드
  const bq = BigQuery.newDataset(projectId, datasetId);
  // ... 데이터 처리 로직

  return { rows: data };
}
```

**Community Connector의 장점:**
- 중앙 집중식 청구 (서비스 계정 사용)
- 커스텀 캐싱 로직
- 사전 정의된 쿼리 템플릿
- 사용자 설정 파라미터화

### Step 8: 보안 및 접근 제어

**BigQuery 수준의 보안**

```sql
-- 특정 사용자에게만 테이블 접근 권한 부여
GRANT `roles/bigquery.dataViewer`
ON TABLE `my-project.analytics_dataset.events`
TO "user@example.com";

-- 행 수준 보안 (Row-Level Security)
CREATE OR REPLACE ROW ACCESS POLICY rls_by_country
ON `my-project.analytics_dataset.events`
GRANT ('editor@company.com') TO ('KR'),
      ('viewer@company.com') TO ('US', 'JP');
```

**Looker Studio 수준의 보안**

- 대시보드 공유 시 뷰어 권한 설정 (Viewer/Editor)
- 특정 사용자/그룹에만 공유
- 데이터 소스별 권한 관리

## Output format

### 대시보드 설정 체크리스트

```markdown
## Dashboard Setup Checklist

### 데이터 소스 설정
- [ ] BigQuery 프로젝트/데이터셋 준비
- [ ] IAM 권한 설정 완료
- [ ] 스케줄된 쿼리 구성 (성능 최적화)
- [ ] 데이터 소스 연결 테스트

### 대시보드 설계
- [ ] F-패턴 레이아웃 적용
- [ ] KPI 타일 배치 (3-4개)
- [ ] 주요 차트 추가 (추세/비교)
- [ ] 상세 테이블 포함
- [ ] 인터랙티브 필터 추가

### 성능 최적화
- [ ] 파티션 키 활용 확인
- [ ] 쿼리 비용 최적화
- [ ] 캐싱 전략 적용
- [ ] 차트 수 20-25개 이하 확인

### 공유 및 보안
- [ ] 접근 권한 설정
- [ ] 데이터 보안 검토
- [ ] 공유 링크 생성
```

## Constraints

### 필수 규칙 (MUST)

1. **날짜 필터 필수**: 모든 대시보드에 날짜 범위 필터 포함
2. **파티션 사용**: BigQuery 쿼리에서 파티션 키 직접 사용
3. **권한 분리**: 데이터 소스별 접근 권한 명확히 설정

### 금지 사항 (MUST NOT)

1. **과도한 차트**: 한 대시보드에 25개 초과 차트 배치 금지
2. **SELECT ***: 전체 컬럼 조회 대신 필요한 컬럼만 선택
3. **라이브 쿼리 남용**: 대용량 테이블에 직접 연결 지양

## Best practices

| 항목 | 권장사항 |
|------|---------|
| **데이터 새로고침** | 스케줄된 쿼리 사용, 야간에 실행 |
| **대시보드 크기** | 최대 25개 차트, 필요시 여러 페이지로 분산 |
| **필터 구성** | 날짜 필터 필수, 3-5개 추가 필터로 제한 |
| **색상 팔레트** | 회사 브랜드 3-4가지 색상만 사용 |
| **타이틀/레이블** | 명확한 설명으로 직관성 확보 |
| **차트 선택** | KPI → 추세 → 비교 → 상세 순서로 배치 |
| **응답 속도** | 평균 2-3초 이내 로딩 목표 |
| **비용 관리** | 월 BigQuery 스캔량 5TB 이내 |

## References

- [Looker Studio Help](https://support.google.com/looker-studio)
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Connect to BigQuery](https://cloud.google.com/looker/docs/studio/connect-to-google-bigquery)
- [Community Connectors](https://developers.google.com/looker-studio/connector)
- [Dashboard Design Best Practices](https://lookercourses.com/dashboard-design-tips-for-looker-studio-how-to-build-clear-effective-reports/)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2026-01-14
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [monitoring-observability](../monitoring-observability/SKILL.md): 데이터 수집 및 모니터링
- [database-schema-design](../../backend/database-schema-design/SKILL.md): 데이터 모델링

### 태그
`#Looker-Studio` `#BigQuery` `#dashboard` `#analytics` `#visualization` `#GCP`

## Examples

### Example 1: 기본 대시보드 생성

```sql
-- 1. 일일 요약 테이블 생성
CREATE OR REPLACE TABLE `my-project.looker_data.daily_metrics` AS
SELECT
  event_date,
  COUNT(DISTINCT user_id) as dau,
  SUM(revenue) as total_revenue,
  COUNT(*) as total_events
FROM `my-project.analytics.events`
WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY event_date;

-- 2. Looker Studio에서 이 테이블에 연결
-- 3. KPI 스코어카드 추가: DAU, 총 매출
-- 4. 라인 차트로 일일 추세 시각화
```

### Example 2: 고급 분석 대시보드

```sql
-- 코호트 분석을 위한 데이터 준비
CREATE OR REPLACE TABLE `my-project.looker_data.cohort_analysis` AS
WITH user_cohort AS (
  SELECT
    user_id,
    DATE_TRUNC(MIN(event_date), WEEK) as cohort_week
  FROM `my-project.analytics.events`
  GROUP BY user_id
)
SELECT
  uc.cohort_week,
  DATE_DIFF(e.event_date, uc.cohort_week, WEEK) as week_number,
  COUNT(DISTINCT e.user_id) as active_users
FROM `my-project.analytics.events` e
JOIN user_cohort uc ON e.user_id = uc.user_id
GROUP BY cohort_week, week_number
ORDER BY cohort_week, week_number;
```
