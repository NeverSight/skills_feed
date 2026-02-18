---
name: pattern-detection
description: Detect patterns, anomalies, and trends in code and data. Use when identifying code smells, finding security vulnerabilities, or discovering recurring patterns. Handles regex patterns, AST analysis, and statistical anomaly detection.
tags: [patterns, anomalies, regex, code-analysis, security, trends]
platforms: [Claude, ChatGPT, Gemini]
allowed-tools: [Read, Grep, Glob]
---

# Pattern Detection


## When to use this skill

- **코드 리뷰**: 문제 패턴 사전 감지
- **보안 검토**: 취약점 패턴 스캔
- **리팩토링**: 중복 코드 식별
- **모니터링**: 이상 징후 알림

## Instructions

### Step 1: 코드 스멜 패턴 감지

**긴 함수 감지**:
```bash
# 50줄 이상 함수 찾기
grep -n "function\|def\|func " **/*.{js,ts,py,go} | \
  while read line; do
    file=$(echo $line | cut -d: -f1)
    linenum=$(echo $line | cut -d: -f2)
    # 함수 길이 계산 로직
  done
```

**중복 코드 패턴**:
```bash
# 유사한 코드 블록 검색
grep -rn "if.*==.*null" --include="*.ts" .
grep -rn "try\s*{" --include="*.java" . | wc -l
```

**매직 넘버**:
```bash
# 하드코딩된 숫자 검색
grep -rn "[^a-zA-Z][0-9]{2,}[^a-zA-Z]" --include="*.{js,ts}" .
```

### Step 2: 보안 취약점 패턴

**SQL Injection 위험**:
```bash
# 문자열 연결로 SQL 쿼리 생성
grep -rn "query.*+.*\$\|execute.*%s\|query.*f\"" --include="*.py" .
grep -rn "SELECT.*\+.*\|\|" --include="*.{js,ts}" .
```

**하드코딩된 시크릿**:
```bash
# 비밀번호, API 키 패턴
grep -riE "(password|secret|api_key|apikey)\s*=\s*['\"][^'\"]+['\"]" --include="*.{js,ts,py,java}" .

# AWS 키 패턴
grep -rE "AKIA[0-9A-Z]{16}" .
```

**위험한 함수 사용**:
```bash
# eval, exec 사용
grep -rn "eval\(.*\)\|exec\(.*\)" --include="*.{py,js}" .

# innerHTML 사용
grep -rn "innerHTML\s*=" --include="*.{js,ts}" .
```

### Step 3: 코드 구조 패턴

**임포트 분석**:
```bash
# 사용되지 않는 임포트 후보
grep -rn "^import\|^from.*import" --include="*.py" . | \
  awk -F: '{print $3}' | sort | uniq -c | sort -rn
```

**TODO/FIXME 패턴**:
```bash
# 미완성 코드 찾기
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.{js,ts,py}" .
```

**에러 핸들링 패턴**:
```bash
# 빈 catch 블록
grep -rn "catch.*{[\s]*}" --include="*.{js,ts,java}" .

# 무시되는 에러
grep -rn "except:\s*pass" --include="*.py" .
```

### Step 4: 데이터 이상 패턴

**정규식 패턴**:
```python
import re

patterns = {
    'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'phone': r'\d{3}[-.\s]?\d{4}[-.\s]?\d{4}',
    'ip_address': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
    'credit_card': r'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}',
    'ssn': r'\d{3}-\d{2}-\d{4}',
}

def detect_sensitive_data(text):
    found = {}
    for name, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            found[name] = len(matches)
    return found
```

**통계적 이상 탐지**:
```python
import numpy as np
from scipy import stats

def detect_anomalies_zscore(data, threshold=3):
    """Z-score 기반 이상치 탐지"""
    z_scores = np.abs(stats.zscore(data))
    return np.where(z_scores > threshold)[0]

def detect_anomalies_iqr(data, k=1.5):
    """IQR 기반 이상치 탐지"""
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return np.where((data < lower) | (data > upper))[0]
```

### Step 5: 트렌드 분석

```python
import pandas as pd

def analyze_trend(df, date_col, value_col):
    """시계열 트렌드 분석"""
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    # 이동 평균
    df['ma_7'] = df[value_col].rolling(window=7).mean()
    df['ma_30'] = df[value_col].rolling(window=30).mean()

    # 성장률
    df['growth'] = df[value_col].pct_change() * 100

    # 트렌드 방향
    recent_trend = df['ma_7'].iloc[-1] > df['ma_30'].iloc[-1]

    return {
        'trend_direction': 'up' if recent_trend else 'down',
        'avg_growth': df['growth'].mean(),
        'volatility': df[value_col].std()
    }
```

## Output format

### 패턴 감지 리포트

```markdown
# 패턴 감지 리포트

## 요약
- 스캔 파일 수: XXX
- 감지된 패턴: XX
- 심각도 높음: X
- 심각도 중간: X
- 심각도 낮음: X

## 감지된 패턴

### 보안 취약점 (HIGH)
| 파일 | 라인 | 패턴 | 설명 |
|------|------|------|------|
| file.js | 42 | hardcoded-secret | API 키 하드코딩 |

### 코드 스멜 (MEDIUM)
| 파일 | 라인 | 패턴 | 설명 |
|------|------|------|------|
| util.py | 100 | long-function | 함수 길이 150줄 |

## 권장 조치
1. [조치 1]
2. [조치 2]
```

## Best practices

1. **점진적 분석**: 간단한 패턴부터 시작
2. **오탐 최소화**: 정확한 정규식 사용
3. **컨텍스트 확인**: 패턴의 맥락 파악
4. **우선순위 지정**: 심각도별 정렬

## Constraints

### 필수 규칙 (MUST)
1. 읽기 전용 작업
2. 결과 검증 수행
3. 오탐 가능성 명시

### 금지 사항 (MUST NOT)
1. 코드 자동 수정 금지
2. 민감 정보 로깅 금지

## References

- [Regex101](https://regex101.com/)
- [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/)
- [Code Smell Catalog](https://refactoring.guru/refactoring/smells)

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
