---
name: data-analysis
description: Analyze datasets to extract insights, identify patterns, and generate reports. Use when exploring data, creating visualizations, or performing statistical analysis. Handles CSV, JSON, SQL queries, and Python pandas operations.
tags: [data, analysis, pandas, statistics, visualization, csv, sql]
platforms: [Claude, ChatGPT, Gemini]
allowed-tools: [Read, Grep, Glob, Bash]
---

# Data Analysis


## When to use this skill

- **데이터 탐색**: 새로운 데이터셋 이해
- **리포트 생성**: 데이터 기반 인사이트 도출
- **품질 검증**: 데이터 정합성 확인
- **의사결정 지원**: 데이터 기반 추천

## Instructions

### Step 1: 데이터 로드 및 탐색

**Python (Pandas)**:
```python
import pandas as pd
import numpy as np

# CSV 로드
df = pd.read_csv('data.csv')

# 기본 정보
print(df.info())
print(df.describe())
print(df.head(10))

# 결측치 확인
print(df.isnull().sum())

# 데이터 타입
print(df.dtypes)
```

**SQL**:
```sql
-- 테이블 구조 확인
DESCRIBE table_name;

-- 샘플 데이터
SELECT * FROM table_name LIMIT 10;

-- 기본 통계
SELECT
    COUNT(*) as total_rows,
    COUNT(DISTINCT column_name) as unique_values,
    MIN(numeric_column) as min_val,
    MAX(numeric_column) as max_val,
    AVG(numeric_column) as avg_val
FROM table_name;
```

### Step 2: 데이터 정제

```python
# 결측치 처리
df['column'].fillna(df['column'].mean(), inplace=True)
df.dropna(subset=['required_column'], inplace=True)

# 중복 제거
df.drop_duplicates(inplace=True)

# 데이터 타입 변환
df['date'] = pd.to_datetime(df['date'])
df['category'] = df['category'].astype('category')

# 이상치 제거 (IQR 방식)
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['value'] >= Q1 - 1.5*IQR) & (df['value'] <= Q3 + 1.5*IQR)]
```

### Step 3: 통계 분석

```python
# 기술 통계
print(df['numeric_column'].describe())

# 그룹별 분석
grouped = df.groupby('category').agg({
    'value': ['mean', 'sum', 'count'],
    'other': 'nunique'
})
print(grouped)

# 상관관계
correlation = df[['col1', 'col2', 'col3']].corr()
print(correlation)

# 피벗 테이블
pivot = pd.pivot_table(df,
    values='sales',
    index='region',
    columns='month',
    aggfunc='sum'
)
```

### Step 4: 시각화

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 히스토그램
plt.figure(figsize=(10, 6))
df['value'].hist(bins=30)
plt.title('Distribution of Values')
plt.savefig('histogram.png')

# 박스플롯
plt.figure(figsize=(10, 6))
sns.boxplot(x='category', y='value', data=df)
plt.title('Value by Category')
plt.savefig('boxplot.png')

# 히트맵 (상관관계)
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.savefig('heatmap.png')

# 시계열
plt.figure(figsize=(12, 6))
df.groupby('date')['value'].sum().plot()
plt.title('Time Series of Values')
plt.savefig('timeseries.png')
```

### Step 5: 인사이트 도출

```python
# 상위/하위 분석
top_10 = df.nlargest(10, 'value')
bottom_10 = df.nsmallest(10, 'value')

# 트렌드 분석
df['month'] = df['date'].dt.to_period('M')
monthly_trend = df.groupby('month')['value'].sum()
growth = monthly_trend.pct_change() * 100

# 세그먼트 분석
segments = df.groupby('segment').agg({
    'revenue': 'sum',
    'customers': 'nunique',
    'orders': 'count'
})
segments['avg_order_value'] = segments['revenue'] / segments['orders']
```

## Output format

### 분석 리포트 구조

```markdown
# 데이터 분석 리포트

## 1. 데이터 개요
- 데이터셋: [이름]
- 레코드 수: X,XXX
- 컬럼 수: XX
- 기간: YYYY-MM-DD ~ YYYY-MM-DD

## 2. 주요 발견
- 인사이트 1
- 인사이트 2
- 인사이트 3

## 3. 통계 요약
| 지표 | 값 |
|------|-----|
| 평균 | X.XX |
| 중앙값 | X.XX |
| 표준편차 | X.XX |

## 4. 권장 사항
1. [권장 사항 1]
2. [권장 사항 2]
```

## Best practices

1. **데이터 이해 우선**: 분석 전 데이터 구조와 의미 파악
2. **점진적 분석**: 간단한 분석에서 복잡한 분석으로 진행
3. **시각화 활용**: 패턴 발견을 위한 다양한 차트 사용
4. **가정 검증**: 데이터에 대한 가정을 항상 검증
5. **재현 가능성**: 분석 코드와 결과를 문서화

## Constraints

### 필수 규칙 (MUST)
1. 원본 데이터 보존 (복사본으로 작업)
2. 분석 과정 문서화
3. 결과 검증

### 금지 사항 (MUST NOT)
1. 민감한 개인정보 노출 금지
2. 근거 없는 결론 도출 금지

## References

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
