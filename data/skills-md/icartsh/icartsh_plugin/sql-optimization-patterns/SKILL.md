---
name: sql-optimization-patterns
description: SQL 쿼리 최적화, 인덱스 전략 및 EXPLAIN 분석을 마스터하여 데이터베이스 성능을 획기적으로 향상시키고 느린 쿼리를 제거합니다. 느린 쿼리 디버깅, 데이터베이스 스키마 설계 또는 애플리케이션 성능 최적화 시 사용하세요.
---

# SQL Optimization Patterns

체계적인 최적화, 올바른 인덱싱 및 쿼리 실행 계획 분석을 통해 느린 데이터베이스 쿼리를 번개처럼 빠른 작업으로 변환하세요.

## 적용 시기

- 느리게 실행되는 쿼리 디버깅
- 성능이 뛰어난 데이터베이스 스키마 설계
- 애플리케이션 응답 시간 최적화
- 데이터베이스 부하 및 비용 절감
- 데이터 증가에 따른 확장성 개선
- EXPLAIN 쿼리 실행 계획 분석
- 효율적인 인덱스 구현
- N+1 쿼리 문제 해결

## 핵심 개념 (Core Concepts)

### 1. 쿼리 실행 계획 (EXPLAIN)

EXPLAIN 출력을 이해하는 것은 최적화의 기본입니다.

**PostgreSQL EXPLAIN:**
```sql
-- 기본 실행 계획 확인
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- 실제 실행 통계 포함
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'user@example.com';

-- 더 많은 세부 정보를 포함한 상세 출력
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.*, o.order_total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days';
```

**주의 깊게 봐야 할 주요 지표:**
- **Seq Scan**: 전체 테이블 스캔 (대용량 테이블에서는 대개 느림)
- **Index Scan**: 인덱스 사용 (좋음)
- **Index Only Scan**: 테이블 접근 없이 인덱스만 사용 (가장 좋음)
- **Nested Loop**: 조인 방식 (작은 데이터셋에는 괜찮음)
- **Hash Join**: 조인 방식 (큰 데이터셋에 좋음)
- **Merge Join**: 조인 방식 (정렬된 데이터에 좋음)
- **Cost**: 추정된 쿼리 비용 (낮을수록 좋음)
- **Rows**: 추정된 반환 행 수
- **Actual Time**: 실제 실행 시간

### 2. 인덱스 전략 (Index Strategies)

인덱스는 가장 강력한 최적화 도구입니다.

**인덱스 유형:**
- **B-Tree**: 기본값, 등호(=) 및 범위 쿼리에 좋음
- **Hash**: 등호(=) 비교에만 사용
- **GIN**: 전체 텍스트 검색, 배열 쿼리, JSONB
- **GiST**: 기하학적 데이터, 전체 텍스트 검색
- **BRIN**: 데이터 간 상관관계가 있는 매우 큰 테이블을 위한 블록 범위 인덱스

```sql
-- 표준 B-Tree 인덱스
CREATE INDEX idx_users_email ON users(email);

-- 복합 인덱스 (순서가 중요합니다!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- 부분 인덱스 (행의 일부만 인덱싱)
CREATE INDEX idx_active_users ON users(email)
WHERE status = 'active';

-- 표현식 인덱스 (함수 기반 인덱스)
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- 커버링 인덱스 (추가 컬럼 포함)
CREATE INDEX idx_users_email_covering ON users(email)
INCLUDE (name, created_at);

-- 전체 텍스트 검색 인덱스
CREATE INDEX idx_posts_search ON posts
USING GIN(to_tsvector('english', title || ' ' || body));

-- JSONB 인덱스
CREATE INDEX idx_metadata ON events USING GIN(metadata);
```

### 3. 쿼리 최적화 패턴

**SELECT * 피하기:**
```sql
-- 나쁨: 불필요한 모든 컬럼을 가져옴
SELECT * FROM users WHERE id = 123;

-- 좋음: 필요한 컬럼만 명시
SELECT id, email, name FROM users WHERE id = 123;
```

**WHERE 절의 효율적 사용:**
```sql
-- 나쁨: 함수 사용으로 인덱스 활용 불가
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- 좋음: 함수 기반 인덱스(functional index) 생성 또는 정확한 일치 사용
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
-- 그 다음:
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- 또는 데이터를 정규화하여 저장
SELECT * FROM users WHERE email = 'user@example.com';
```

**JOIN 최적화:**
```sql
-- 나쁨: 카테시안 곱 생성 후 필터링
SELECT u.name, o.total
FROM users u, orders o
WHERE u.id = o.user_id AND u.created_at > '2024-01-01';

-- 좋음: 조인 전 필터링
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';

-- 더 좋음: 두 테이블 모두 사전 필터링
SELECT u.name, o.total
FROM (SELECT * FROM users WHERE created_at > '2024-01-01') u
JOIN orders o ON u.id = o.user_id;
```

## 최적화 패턴 (Optimization Patterns)

### 패턴 1: N+1 쿼리 제거

**문제: N+1 쿼리 안티 패턴**
```python
# 나쁨: N+1개의 쿼리를 실행함
users = db.query("SELECT * FROM users LIMIT 10")
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)
    # orders 처리
```

**해결책: JOIN 또는 배치 로딩(Batch Loading) 사용**
```sql
-- 해결책 1: JOIN 사용
SELECT
    u.id, u.name,
    o.id as order_id, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.id IN (1, 2, 3, 4, 5);

-- 해결책 2: 배치 쿼리
SELECT * FROM orders
WHERE user_id IN (1, 2, 3, 4, 5);
```

```python
# 좋음: JOIN 또는 배치 로드를 통한 단일 쿼리 실행
# JOIN 사용 시
results = db.query("""
    SELECT u.id, u.name, o.id as order_id, o.total
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.id IN (1, 2, 3, 4, 5)
""")

# 또는 배치 로드(Batch load)
users = db.query("SELECT * FROM users LIMIT 10")
user_ids = [u.id for u in users]
orders = db.query(
    "SELECT * FROM orders WHERE user_id IN (?)",
    user_ids
)
# user_id별로 orders 그룹화
orders_by_user = {}
for order in orders:
    orders_by_user.setdefault(order.user_id, []).append(order)
```

### 패턴 2: 페이지네이션(Pagination) 최적화

**나쁨: 대용량 테이블에서의 OFFSET 사용**
```sql
-- 큰 offset 값에서 속도 저하 발생
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 20 OFFSET 100000;  -- 매우 느림!
```

**좋음: 커서 기반 페이지네이션 (Cursor-Based Pagination)**
```sql
-- 훨씬 빠름: 커서(마지막 확인된 ID) 사용
SELECT * FROM users
WHERE created_at < '2024-01-15 10:30:00'  -- 마지막 커서
ORDER BY created_at DESC
LIMIT 20;

-- 복합 정렬 시
SELECT * FROM users
WHERE (created_at, id) < ('2024-01-15 10:30:00', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- 인덱스 필요
CREATE INDEX idx_users_cursor ON users(created_at DESC, id DESC);
```

### 패턴 3: 효율적인 집계 (Aggregate Efficiently)

**COUNT 쿼리 최적화:**
```sql
-- 나쁨: 모든 행을 카운트함
SELECT COUNT(*) FROM orders;  -- 큰 테이블에서 느림

-- 좋음: 근사치를 위한 추정치(estimates) 사용
SELECT reltuples::bigint AS estimate
FROM pg_class
WHERE relname = 'orders';

-- 좋음: 카운트 전 필터링 적용
SELECT COUNT(*) FROM orders
WHERE created_at > NOW() - INTERVAL '7 days';

-- 더 좋음: 인덱스 전용 스캔(index-only scan) 활용
CREATE INDEX idx_orders_created ON orders(created_at);
SELECT COUNT(*) FROM orders
WHERE created_at > NOW() - INTERVAL '7 days';
```

**GROUP BY 최적화:**
```sql
-- 나쁨: 그룹화 후 필터링
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 10;

-- 좋음: 가능한 경우 먼저 필터링 후 그룹화
SELECT user_id, COUNT(*) as order_count
FROM orders
WHERE status = 'completed'
GROUP BY user_id
HAVING COUNT(*) > 10;

-- 가장 좋음: 커버링 인덱스 활용
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

### 패턴 4: 서브쿼리 최적화

**상관 서브쿼리(Correlated Subqueries) 변환:**
```sql
-- 나쁨: 상관 서브쿼리 (각 행마다 실행됨)
SELECT u.name, u.email,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
FROM users u;

-- 좋음: 집계가 포함된 JOIN
SELECT u.name, u.email, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name, u.email;

-- 더 좋음: 윈도우 함수 사용
SELECT DISTINCT ON (u.id)
    u.name, u.email,
    COUNT(o.id) OVER (PARTITION BY u.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;
```

**가독성을 위한 CTE 사용:**
```sql
-- 공통 테이블 식별자(CTE) 활용
WITH recent_users AS (
    SELECT id, name, email
    FROM users
    WHERE created_at > NOW() - INTERVAL '30 days'
),
user_order_counts AS (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    WHERE created_at > NOW() - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT ru.name, ru.email, COALESCE(uoc.order_count, 0) as orders
FROM recent_users ru
LEFT JOIN user_order_counts uoc ON ru.id = uoc.user_id;
```

### 패턴 5: 배치 작업 (Batch Operations)

**배치 INSERT:**
```sql
-- 나쁨: 다수의 개별 insert 수행
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');
INSERT INTO users (name, email) VALUES ('Carol', 'carol@example.com');

-- 좋음: 배치 insert
INSERT INTO users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Carol', 'carol@example.com');

-- 더 좋음: 대량 insert 시 COPY 활용 (PostgreSQL)
COPY users (name, email) FROM '/tmp/users.csv' CSV HEADER;
```

**배치 UPDATE:**
```sql
-- 나쁨: 반복문 내 업데이트
UPDATE users SET status = 'active' WHERE id = 1;
UPDATE users SET status = 'active' WHERE id = 2;
-- ... 많은 ID를 반복

-- 좋음: IN 절을 활용한 단일 UPDATE
UPDATE users
SET status = 'active'
WHERE id IN (1, 2, 3, 4, 5, ...);

-- 더 좋음: 대량 배치 시 임시 테이블 활용
CREATE TEMP TABLE temp_user_updates (id INT, new_status VARCHAR);
INSERT INTO temp_user_updates VALUES (1, 'active'), (2, 'active'), ...;

UPDATE users u
SET status = t.new_status
FROM temp_user_updates t
WHERE u.id = t.id;
```

## 고급 기범 (Advanced Techniques)

### 구체화된 뷰 (Materialized Views)

비용이 많이 드는 쿼리를 미리 계산해 둡니다.

```sql
-- 구체화된 뷰 생성
CREATE MATERIALIZED VIEW user_order_summary AS
SELECT
    u.id,
    u.name,
    COUNT(o.id) as total_orders,
    SUM(o.total) as total_spent,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- 구체화된 뷰에 인덱스 추가
CREATE INDEX idx_user_summary_spent ON user_order_summary(total_spent DESC);

-- 구체화된 뷰 갱신
REFRESH MATERIALIZED VIEW user_order_summary;

-- 동시 갱신 (PostgreSQL, 락 최소화)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_order_summary;

-- 구체화된 뷰 쿼리 (매우 빠름)
SELECT * FROM user_order_summary
WHERE total_spent > 1000
ORDER BY total_spent DESC;
```

### 파티셔닝 (Partitioning)

성능 향상을 위해 대형 테이블을 나눕니다.

```sql
-- 날짜별 범위 파티셔닝 (PostgreSQL)
CREATE TABLE orders (
    id SERIAL,
    user_id INT,
    total DECIMAL,
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- 파티션 생성
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- 쿼리는 자동으로 적절한 파티션을 사용함
SELECT * FROM orders
WHERE created_at BETWEEN '2024-02-01' AND '2024-02-28';
-- orders_2024_q1 파티션만 스캔함
```

### 쿼리 힌트 및 최적화

```sql
-- 인덱스 사용 강제 (MySQL)
SELECT * FROM users
USE INDEX (idx_users_email)
WHERE email = 'user@example.com';

-- 병렬 쿼리 (PostgreSQL)
SET max_parallel_workers_per_gather = 4;
SELECT * FROM large_table WHERE condition;

-- 조인 힌트 (PostgreSQL)
SET enable_nestloop = OFF;  -- hash join 또는 merge join 강제
```

## 모범 사례 (Best Practices)

1. **선별적인 인덱싱**: 인덱스가 너무 많으면 쓰기 작업이 느려집니다.
2. **쿼리 성능 모니터링**: 느린 쿼리 로그(slow query logs)를 활용하세요.
3. **통계 정보 업데이트 유지**: 정기적으로 ANALYZE를 실행하세요.
4. **적절한 데이터 타입 사용**: 작은 타입일수록 성능이 좋습니다.
5. **사려 깊은 정규화**: 정규화와 성능 사이의 균형을 맞추세요.
6. **자주 접근하는 데이터 캐싱**: 애플리케이션 레벨 캐싱을 활용하세요.
7. **커넥션 풀링 (Connection Pooling)**: 데이터베이스 연결을 재사용하세요.
8. **정기적인 유지보수**: VACUUM, ANALYZE, 인덱스 재빌드 등을 수행하세요.

```sql
-- 통계 업데이트
ANALYZE users;
ANALYZE VERBOSE orders;

-- Vacuum (PostgreSQL)
VACUUM ANALYZE users;
VACUUM FULL users;  -- 공간 회수 (테이블 락 발생)

-- 인덱스 재구성
REINDEX INDEX idx_users_email;
REINDEX TABLE users;
```

## 자주 발생하는 문제 (Common Pitfalls)

- **과도한 인덱싱**: 각 인덱스는 INSERT/UPDATE/DELETE 속도를 늦춥니다.
- **사용되지 않는 인덱스**: 공간을 낭비하고 쓰기 성능을 저하시킵니다.
- **인덱스 누락**: 쿼리 속도 저하, 전체 테이블 스캔 유발.
- **암시적 타입 변환**: 인덱스 사용을 방해합니다.
- **OR 조건**: 인덱스를 효율적으로 사용하기 어렵게 만들 수 있습니다.
- **와일드카드가 앞에 붙은 LIKE**: `LIKE '%abc'`는 인덱스를 탈 수 없습니다.
- **WHERE 절의 함수**: 기능 기반 인덱스가 없다면 인덱스 사용을 방해합니다.

## 쿼리 모니터링

```sql
-- 느린 쿼리 찾기 (PostgreSQL)
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- 누락된 인덱스 찾기 (PostgreSQL)
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / seq_scan AS avg_seq_tup_read
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 10;

-- 사용되지 않는 인덱스 찾기 (PostgreSQL)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

## 리소스

- **references/postgres-optimization-guide.md**: PostgreSQL 전용 최적화
- **references/mysql-optimization-guide.md**: MySQL/MariaDB 최적화
- **references/query-plan-analysis.md**: EXPLAIN 실행 계획 심층 분석
- **assets/index-strategy-checklist.md**: 인덱스 생성 시점 및 방법
- **assets/query-optimization-checklist.md**: 단계별 최적화 가이드
- **scripts/analyze-slow-queries.sql**: 데이터베이스 내 느린 쿼리 식별
- **scripts/index-recommendations.sql**: 인덱스 권장 사항 생성
