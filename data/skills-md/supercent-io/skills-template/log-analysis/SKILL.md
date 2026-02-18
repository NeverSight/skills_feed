---
name: log-analysis
description: Analyze application logs to identify errors, performance issues, and security anomalies. Use when debugging issues, monitoring system health, or investigating incidents. Handles various log formats including Apache, Nginx, application logs, and JSON logs.
tags: [logs, analysis, debugging, monitoring, grep, patterns]
platforms: [Claude, ChatGPT, Gemini]
allowed-tools: [Read, Grep, Glob]
---

# Log Analysis


## When to use this skill

- **오류 디버깅**: 애플리케이션 오류 원인 분석
- **성능 분석**: 응답 시간, 처리량 분석
- **보안 감사**: 비정상 접근 패턴 탐지
- **인시던트 대응**: 장애 발생 시 원인 조사

## Instructions

### Step 1: 로그 파일 위치 파악

```bash
# 일반적인 로그 위치
/var/log/                    # 시스템 로그
/var/log/nginx/              # Nginx 로그
/var/log/apache2/            # Apache 로그
./logs/                      # 애플리케이션 로그
```

### Step 2: 에러 패턴 검색

**일반 에러 검색**:
```bash
# ERROR 레벨 로그 검색
grep -i "error\|exception\|fail" application.log

# 최근 에러 (마지막 100줄)
tail -100 application.log | grep -i error

# 타임스탬프 포함 에러
grep -E "^\[.*ERROR" application.log
```

**HTTP 에러 코드**:
```bash
# 5xx 서버 에러
grep -E "HTTP/[0-9.]+ 5[0-9]{2}" access.log

# 4xx 클라이언트 에러
grep -E "HTTP/[0-9.]+ 4[0-9]{2}" access.log

# 특정 에러 코드
grep "HTTP/1.1\" 500" access.log
```

### Step 3: 패턴 분석

**시간별 분석**:
```bash
# 시간대별 에러 카운트
grep -i error application.log | cut -d' ' -f1,2 | sort | uniq -c | sort -rn

# 특정 시간대 로그
grep "2025-01-05 14:" application.log
```

**IP별 분석**:
```bash
# IP별 요청 수
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -20

# 특정 IP 활동
grep "192.168.1.100" access.log
```

### Step 4: 성능 분석

**응답 시간 분석**:
```bash
# Nginx 로그에서 응답 시간 추출
awk '{print $NF}' access.log | sort -n | tail -20

# 느린 요청 (1초 이상)
awk '$NF > 1.0 {print $0}' access.log
```

**요청량 분석**:
```bash
# 분당 요청 수
awk '{print $4}' access.log | cut -d: -f1,2,3 | uniq -c

# 엔드포인트별 요청 수
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -20
```

### Step 5: 보안 분석

**의심스러운 패턴**:
```bash
# SQL Injection 시도
grep -iE "(union|select|insert|update|delete|drop).*--" access.log

# XSS 시도
grep -iE "<script|javascript:|onerror=" access.log

# 디렉토리 트래버설
grep -E "\.\./" access.log

# 무차별 대입 공격
grep -E "POST.*/login" access.log | awk '{print $1}' | sort | uniq -c | sort -rn
```

## Output format

### 분석 리포트 구조

```markdown
# 로그 분석 리포트

## 요약
- 분석 기간: YYYY-MM-DD HH:MM ~ YYYY-MM-DD HH:MM
- 총 로그 라인: X,XXX
- 에러 수: XXX
- 경고 수: XXX

## 에러 분석
| 에러 유형 | 발생 횟수 | 최근 발생 |
|----------|-----------|----------|
| Error A  | 150       | 2025-01-05 14:30 |
| Error B  | 45        | 2025-01-05 14:25 |

## 권장 조치
1. [조치 1]
2. [조치 2]
```

## Best practices

1. **시간 범위 지정**: 분석할 시간 범위를 명확히 설정
2. **패턴 저장**: 자주 사용하는 grep 패턴 스크립트화
3. **컨텍스트 확인**: 에러 전후 로그도 함께 확인 (`-A`, `-B` 옵션)
4. **로그 로테이션**: 압축된 로그도 zgrep으로 검색

## Constraints

### 필수 규칙 (MUST)
1. 읽기 전용 작업만 수행
2. 민감한 정보(비밀번호, 토큰) 마스킹

### 금지 사항 (MUST NOT)
1. 로그 파일 수정 금지
2. 민감 정보 외부 노출 금지

## References

- [grep 매뉴얼](https://www.gnu.org/software/grep/manual/)
- [awk 가이드](https://www.gnu.org/software/gawk/manual/)
- [로그 분석 베스트 프랙티스](https://www.loggly.com/ultimate-guide/)

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
