---
name: error-detective
description: TRACE 프레임워크(Trace, Read, Analyze, Check, Execute)를 사용한 체계적인 디버깅 및 에러 해결입니다. 에러 디버깅, 스택 트레이스(stack traces) 분석, 실패 조사, 근본 원인 분석(root cause analysis) 또는 운영 이슈 트러블슈팅 시 사용합니다.
---

# Error Detective - Systematic Debugging and Error Resolution

## 개요 (Overview)

Error Detective는 에러를 효율적으로 식별, 분석 및 해결하기 위해 체계적인 방법론을 적용하는 종합적인 디버깅 SKILL입니다. TRACE 프레임워크와 구조화된 분석 기법을 사용하여 에러의 초기 발견부터 검증된 해결까지 디버깅 과정을 안내합니다.

## 핵심 역량 (Core Capabilities)

### 스택 트레이스 분석 (Stack Trace Analysis)
- 여러 언어에 걸친 스택 트레이스 파싱 및 해석
- 근본 원인(root cause)과 증상 에러(symptom errors) 구분
- 관련 파일 경로 및 라인 번호 추출
- 호출 체인 및 에러 전파 과정 이해

### 에러 패턴 인식 (Error Pattern Recognition)
- 유형별 에러 분류 (syntax, runtime, logic, integration)
- 공통 에러 패턴 및 안티 패턴 식별
- 프레임워크별 특화 에러 인식
- 에러를 발생 가능한 근본 원인에 매핑

### 근본 원인 분석 (Root Cause Analysis)
- 증상과 기저 이슈의 구분
- 에러 체인을 따라 원래 발생 지점 추적
- 환경 이슈와 코드 이슈의 실별
- 설정 및 종속성 문제 감지

### 디버깅 워크플로우 관리
- 구조화된 조사 프로세스
- 가설 생성 및 테스트
- 이해도에 대한 반복적 정밀화
- 조사 결과 및 해결책 문서화

## TRACE 프레임워크

TRACE는 어떤 에러든 디버깅할 수 있는 체계적인 5단계 접근 방식입니다:

### T - Trace the Error (에러 추적)
**목표**: 완전한 에러 정보와 컨텍스트 캡처

1. **전체 에러 메시지 수집**
   - 전체 스택 트레이스 (처음 몇 줄만이 아닌 전체)
   - 에러 유형 및 메시지
   - 타임스탬프 및 발생 빈도
   - 에러가 발생한 환경

2. **에러 위치 식별**
   - 정확한 파일 및 라인 번호
   - 에러가 발생한 함수 또는 메서드
   - 코드 컨텍스트 (주변 라인)
   - 진입점부터 에러 지점까지의 호출 스택

3. **재현 단계 갈무리**
   - 재현을 위한 최소한의 단계
   - 사용된 입력 데이터 또는 파라미터
   - 기대 결과 vs. 실제 동작
   - 재현의 일관성 (항상 발생, 간헐적 발생, 드물게 발생)

### R - Read the Error Message (에러 메시지 읽기)
**목표**: 에러 자체에서 모든 정보 추출

1. **에러 구성 요소 파싱**
   - 에러 유형/클래스 (TypeError, ValueError 등)
   - 에러 메시지 내용
   - 권장 수정 사항 (제공되는 경우)
   - 관련 에러 또는 경고

2. **에러 시맨틱 이해**
   - 해당 언어/프레임워크에서 해당 에러 유형이 의미하는 바
   - 어떤 조건이 이 에러를 유발하는지
   - 에러 메시지가 구체적으로 무엇을 말하고 있는지
   - 에러 코드 또는 상태 코드

3. **에러 카테고리 식별**
   - Syntax error (코드 파싱 불가)
   - Runtime error (실행 중 크래시 발생)
   - Logic error (결과가 틀림, 크래시 없음)
   - Integration error (외부 시스템 실패)
   - Performance error (타임아웃, 리소스 고갈)

### A - Analyze the Context (컨텍스트 분석)
**목표**: 에러 주변의 더 넓은 컨텍스트 이해

1. **코드 분석**
   - 실패한 라인과 주변 코드 검토
   - 해당 코드의 최근 변경 사항 확인
   - 함수/메서드 시그니처 및 사용법 검토
   - 실패한 코드를 호출하거나 호출되는 관련 코드 검토

2. **데이터 분석**
   - 실패 시점의 입력값 조사
   - 데이터 타입 및 구조 확인
   - 데이터가 예상된 형식/제약 사항을 충족하는지 검증
   - 엣지 케이스(edge cases) 또는 예상치 못한 값 식별

3. **환경 분석**
   - 종속성 및 버전 확인
   - 설정 파일 검토
   - 환경 변수 검증
   - 필요한 리소스(파일, 네트워크, 메모리) 가용성 확인

4. **상태 분석**
   - 에러 발생 시점의 애플리케이션 상태
   - 이 상태로 이어진 이전 작업들
   - 관련된 공유 상태 또는 전역 변수
   - 데이터베이스 또는 외부 시스템 상태

### C - Check for Root Cause (근본 원인 확인)
**목표**: 단순한 증상이 아닌 기저의 이슈 실별

1. **에러 체인 추적**
   - 스택 트레이스의 맨 아래(첫 번째 에러)부터 시작
   - 상위로 거슬러 올라가며 원래 원인 탐색
   - 에러 발생 지점과 에러 핸들러 구분
   - 래핑되거나 다시 던져진(re-thrown) 에러 식별

2. **가설 테스트**
   - 구체적이고 테스트 가능한 가설 생성
   - 변수 격리 (한 번에 하나씩 변경)
   - 로깅/디버깅 도구를 사용하여 가정 검증
   - 확인되거나 기각된 가설 문서화

3. **일반적인 근본 원인**
   - **Null/undefined 값**: 초기화 또는 검증 누락
   - **타입 불일치 (Type mismatches)**: 잘못된 데이터 타입 전달 또는 반환
   - **Off-by-one 에러**: 배열/루프 경계 이슈
   - **경합 조건 (Race conditions)**: 타이밍에 따른 실패
   - **리소스 고갈**: 메모리, 디스크, 커넥션 부족
   - **설정 에러 (Configuration errors)**: 잘못된 설정 또는 누락된 설정
   - **종속성 이슈 (Dependency issues)**: 버전 충돌 또는 누락된 라이브러리
   - **권한 에러**: 불충분한 접속 권한
   - **네트워크 에러**: 연결성, 타임아웃, DNS 이슈
   - **데이터 손상**: 유효하지 않거나 예상치 못한 데이터 형식

### E - Execute the Fix (수정 실행)
**목표**: 해결책 구현 및 검증

1. **수정 설계**
   - 증상이 아닌 근본 원인 해결
   - 부수 효과(side effects) 및 엣지 케이스 고려
   - 필요한 경우 하위 호환성 계획
   - 가장 유지보수하기 쉬운 해결책 선택

2. **신중한 구현**
   - 최소한의 타겟팅된 변경 실시
   - 검증 및 에러 핸들링 추가
   - 향후 디버깅을 위한 로깅 포함
   - 수정 내용 및 근거 문서화

3. **철저한 검증**
   - 원래 에러가 해결되었는지 확인
   - 재현 단계를 통해 테스트
   - 엣지 케이스 및 관련 기능 테스트
   - 새로운 에러가 도입되지 않았는지 확인

4. **문서화 및 방지**
   - 에러 유발 원인 문서화
   - 해결책 및 작동 이유 문서화
   - 회귀(regression) 방지를 위한 테스트 추가
   - 필요한 경우 문서 업데이트 또는 경고 추가

## 디버깅 워크플로우

### 초기 평가 (5분)

```
1. 전체 에러 메시지 읽기
2. 에러 유형 및 심각도 식별
3. 에러 재현 가능 여부 확인
4. 영향도 평가 (차단형, 성능 저하, 단순 외관상 문제)
5. 조사 우선순위 결정
```

### 심층 조사 (15-30분)

```
1. TRACE 프레임워크를 체계적으로 적용
2. 디버깅 도구 사용 (scripts/debug_helper.py 참조)
3. 가설 생성 및 테스트
4. 진행하면서 발견 사항 문서화
5. 근본 원인으로 좁히기
```

### 해결책 구현 (상황에 따라 다름)

```
1. 근본 원인을 해결하는 수정 설계
2. 적절한 에러 핸들링과 함께 구현
3. 로깅 및 검증 추가
4. 철저한 테스트
5. 해결책 문서화
```

### 검증 및 방지 (10분)

```
1. 원래의 재현 단계로 수정 사항 검증
2. 관련 기능 테스트
3. 회귀 테스트 추가
4. 문서 업데이트
5. 배포 및 모니터링
```

## 언어별 공통 에러 패턴

### Python

**AttributeError: 'NoneType' has no attribute 'X'**
- 근본 원인: 객체를 기대했으나 변수가 None임
- 체크 사항: 초기화, 함수 반환값, API 응답
- 해결책: Null 체크 추가, 적절한 초기화 보장

**KeyError: 'key_name'**
- 근본 원인: 딕셔너리에 기대한 키가 없음
- 체크 사항: 데이터 소스, 파싱 로직, 키 철자
- 해결책: 디폴트값과 함께 .get() 사용, 데이터 구조 검증

**ImportError / ModuleNotFoundError**
- 근본 원인: 모듈이 설치되지 않았거나 경로에 없음
- 체크 사항: requirements.txt, 가상 환경, PYTHONPATH
- 해결책: 누락된 패키지 설치, 임포트 경로 수정

**IndentationError**
- 근본 원인: 일관되지 않은 여백 (탭 vs 공백)
- 체크 사항: 에디터 설정, 복사된 코드
- 해결책: 공백(PEP 8)으로 표준화, linter 사용

### JavaScript/TypeScript

**TypeError: Cannot read property 'X' of undefined**
- 근본 원인: undefined 객체의 프로퍼티에 접근
- 체크 사항: 객체 초기화, 비동기 타이밍, API 응답
- 해결책: 옵셔널 체이닝(?. 연산자), null 체크

**ReferenceError: X is not defined**
- 근본 원인: 선언 전 변수 사용 또는 스코프 벗어남
- 체크 사항: 변수 선언, 스코프, 호이스팅(hoisting) 이슈
- 해결책: 변수 선언, 스코프 수정, 임포트 확인

**Promise rejection / Uncaught (in promise)**
- 근본 원인: catch 핸들러 없이 비동기 작업 실패
- 체크 사항: API 호출, 파일 작업, async/await 사용
- 해결책: .catch() 추가 또는 await와 함께 try/catch 사용

**SyntaxError: Unexpected token**
- 근본 원인: 주로 JSON이나 코드 파싱 중 발생하는 유효하지 않은 구문
- 체크 사항: JSON 구조, 괄호 짝 맞추기, 세미콜론
- 해결책: JSON 검증, 구문 수정, 복사/붙여넣기 에러 확인

### Java

**NullPointerException**
- 근본 원인: null 객체 참조에 대해 메서드 호출
- 체크 사항: 객체 초기화, 메서드 반환값
- 해결책: Null 체크 추가, Optional 사용, 초기화 보장

**ClassNotFoundException**
- 근본 원인: classpath에서 클래스를 찾을 수 없음
- 체크 사항: 종속성, 빌드 설정, 패키지 구조
- 해결책: 종속성 추가, classpath 수정, 패키지/클래스 이름 확인

**ConcurrentModificationException**
- 근본 원인: 반복(iteration) 중에 컬렉션이 수정됨
- 체크 사항: 중첩 루프, 멀티스레딩, iterator 사용
- 해결책: iterator.remove(), CopyOnWriteArrayList 사용 또는 동기화(synchronization)

## 에러 심각도 분류

### Critical (즉시 수정)
- 애플리케이션 크래시 또는 시작 불가
- 데이터 손실 또는 손상
- 보안 취약점
- 운영 환경 중단 (Outages)
- 결제 또는 트랜잭션 실패

### High (조속히 수정)
- 주요 기능 고장
- 사용자에게 영향을 주는 성능 저하
- 여러 사용자에게 영향을 주는 에러
- 복잡한 해결 방법(Workarounds)

### Medium (수정 일정 계획)
- 부가 기능 고장
- 영향도가 있는 외관상 이슈
- 쉬운 해결 방법이 있는 에러
- 엣지 케이스 실패

### Low (백로그)
- 외관상 이슈
- 사소한 개선 사항
- 드문 엣지 케이스
- 중요하지 않은 경고

## 디버깅 도구 및 기법

### 로깅 모범 사례

```python
import logging

# 구조화된 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 컨텍스트와 함께 로깅
logger = logging.getLogger(__name__)
logger.debug(f"Processing item: {item_id}, user: {user_id}")
logger.error(f"Failed to process: {error}", exc_info=True)
```

### 전략적 중단점 (Breakpoints)

1. **에러 발생 지점**: 에러 발생 시의 정확한 상태 포착
2. **에러 발생 전**: 입력값 및 사전 조건 확인
3. **에러 발생 후**: 에러 전파 과정 관찰
4. **결정 지점 (Decision points)**: 로직 분기점 검증
5. **루프 내부**: 반복 변수 확인

### 전략적인 Print 디버깅

```python
# 컨텍스트 정보를 포함한 디버그 출력 추가
print(f"DEBUG: function_name called with {param1=}, {param2=}")
print(f"DEBUG: variable state before operation: {var=}")
print(f"DEBUG: condition check: {condition=}, result: {result=}")
```

### 이진 탐색 디버깅 (Binary Search Debugging)

에러 위치가 불분명할 때:
1. 코드 경로 중간에 체크포인트 추가
2. 에러가 체크포인트 이전인지 이후인지 판단
3. 남은 절반에 대해 반복
4. 에러 위치에 빠르게 수렴

### 고무 오리 디버깅 (Rubber Duck Debugging)

누군가에게(혹은 사물에게) 코드를 한 줄씩 설명하기:
1. 가정을 검토하게 함
2. 설명하는 중에 에러를 발견하는 경우가 많음
3. 복잡한 로직을 명확하게 함
4. 지식의 공백을 식별함

## Debug Helper 스크립트 사용

`scripts/debug_helper.py` 유틸리티는 자동화된 보조 기능을 제공합니다:

```bash
# 파일에서 스택 트레이스 파싱
python scripts/debug_helper.py parse-trace error.log

# 에러 패턴 추출
python scripts/debug_helper.py analyze-log application.log

# 디버그 세션 시작 (로그 생성)
python scripts/debug_helper.py session start "Login error investigation"

# 세션에 노트 추가
python scripts/debug_helper.py session note "Tested with different users - same error"

# 해결책과 함께 세션 종료
python scripts/debug_helper.py session close "Fixed: Added null check for user.profile"
```

## 모범 사례 (Best Practices)

### 수행할 작업 (Do's)

- **에러 메시지 전체 읽기**: 세부 사항을 건너뛰지 마세요.
- **일관된 재현**: 디버깅 전에 신뢰할 수 있는 재현 방법을 확보하세요.
- **한 번에 한 가지만 변경**: 무엇이 문제를 해결했는지 격리하세요.
- **진행하면서 문서화**: 가설, 테스트, 발견 사항을 기록하세요.
- **버전 관리 사용**: 디버깅 전에 커밋하여 필요한 경우 되돌릴 수 있게 하세요.
- **테스트 추가**: 수정 후 회귀를 방지하세요.
- **근본 원인 수정**: 증상에만 땜질하지 마세요.
- **지식 공유**: 팀을 위해 해결책을 문서화하세요.

### 피해야 할 작업 (Don'ts)

- **추측하지 말 것**: 데이터로 가정을 검증하세요.
- **에러 읽기를 건너뛰지 말 것**: 에러 메시지에는 중요한 정보가 담겨 있습니다.
- **여러 가지를 동시에 변경하지 말 것**: 무엇이 해결했는지 알 수 없게 됩니다.
- **충동적으로 코드를 삭제하지 말 것**: 먼저 주석 처리하고 왜 그 코드가 있었는지 이해하세요.
- **경고를 무시하지 말 것**: 오늘의 경고는 내일의 에러가 됩니다.
- **이해 없이 수정하지 말 것**: 다른 것을 망가뜨릴 수 있습니다.
- **테스트를 잊지 말 것**: 수정 사항이 작동하고 새로운 이슈를 만들지 않는지 확인하세요.

## 일반적인 디버깅 시나리오

### 시나리오 1: "어제는 됐는데"

**접근 방식:**
1. 최근 변경 사항 확인 (git diff, git log)
2. 종속성 업데이트 검토
3. 환경 변경 사항 확인
4. 시간에 따른 로직(time-dependent logic) 탐색
5. 환경 간 설정 비교

**일반적인 원인:**
- 최근 코드 변경
- 업데이트된 종속성
- 설정 변경
- 데이터베이스 스키마 변경
- 외부 API 변경
- 인증서 만료

### 시나리오 2: "내 컴퓨터에선 되는데"

**접근 방식:**
1. 환경 비교 (OS, 종속성, 설정)
2. 환경 변수 확인
3. 파일 경로 및 권한 검증
4. 환경 간 데이터 비교
5. 하드코딩된 가정사항 탐색

**일반적인 원인:**
- 다른 종속성 버전
- 누락된 환경 변수
- 다른 파일 경로
- 데이터베이스 상태 차이
- 운영 체제 차이
- 누락된 설정 파일

### 시나리오 3: "간헐적 실패"

**접근 방식:**
1. 실패 패턴 식별 (타이밍, 빈도, 조건)
2. 경합 조건(race conditions) 탐색
3. 리소스 가용성 확인
4. 동시 작업 검토
5. 광범위한 로깅 추가
6. 재현 시도 횟수 증가

**일반적인 원인:**
- 경합 조건
- 메모리 누수
- 외부 서비스 불안정
- 네트워크 이슈
- 타이밍 의존 로직
- 리소스 고갈

### 시나리오 4: "운영 환경에서만 에러 발생"

**접근 방식:**
1. 운영 환경 전용 설정 확인
2. 운영 데이터의 특성 검토
3. 운영 환경의 부하/규모 확인
4. 운영 환경의 종속성 검토
5. 보안/권한 설정 검토

**일반적인 원인:**
- 운영 데이터의 엣지 케이스
- 규모/부하 관련 이슈
- 운영 환경 전용 설정
- 다른 보안 정책
- 방화벽 또는 네트워크 제한
- 운영용으로만 연동된 기능

## 고급 기법

### Bisect Debugging (Git)

어떤 커밋이 버그를 도입했는지 찾기:

```bash
git bisect start
git bisect bad                 # 현재 버전에 버그가 있음
git bisect good v1.2.0        # v1.2.0 버전은 정상이였음
# Git이 중간 커밋을 체크아웃함
# 테스트 후 good/bad 마킹
git bisect good/bad
# Git이 범인 커밋을 식별할 때까지 반복
git bisect reset
```

### Heisenbug (관찰자 효과)

디버깅을 시작하면 사라지는 에러:

**전략:**
- 중단점 없이 로깅 추가
- 디버깅을 위해 운영 환경과 유사한 환경 사용
- 타이밍 및 동시성 이슈 검토
- 초기화/타이밍 종속성 확인
- 비침습적(non-intrusive) 모니터링 사용

### 메모리 프로파일링 (Memory Profiling)

메모리 누수 및 성능 확인:

```python
# Python 메모리 프로파일링
import tracemalloc

tracemalloc.start()
# ... 코드 실행 ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
```

### 네트워크 디버깅 (Network Debugging)

API 및 통합 에러 확인:

**도구:**
- 브라우저 DevTools Network 탭
- 상세 플래그(-v)를 포함한 curl
- API 테스트를 위한 Postman
- 패킷 조사를 위한 Wireshark
- 네트워크 프록시 (Charles, Fiddler)

**체크 사항:**
- Request/response 헤더
- 상태 코드
- Request/response 바디
- 타이밍 (레이턴시, 타임아웃)
- SSL/TLS 이슈

## Quick Reference

### TRACE 프레임워크 퀵 체크리스트

```
☐ T - TRACE
  ☐ 전체 에러 메시지 캡처 완료
  ☐ 스택 트레이스 수집 완료
  ☐ 재현 단계 문서화 완료
  ☐ 환경 식별 완료

☐ R - READ
  ☐ 에러 유형 식별 완료
  ☐ 에러 메시지 분석 완료
  ☐ 에러 카테고리 결정 완료
  ☐ 관련 에러 확인 완료

☐ A - ANALYZE
  ☐ 코드 검토 완료
  ☐ 데이터 조사 완료
  ☐ 환경 검증 완료
  ☐ 상태 조사 완료

☐ C - CHECK
  ☐ 에러 체인 추적 완료
  ☐ 가설 테스트 완료
  ☐ 근본 원인 식별 완료
  ☐ 가정 검증 완료

☐ E - EXECUTE
  ☐ 수정 설계 완료
  ☐ 수정 구현 완료
  ☐ 수정 검증 완료
  ☐ 방지 대책 추가 완료
```

### 에러 우선순위 매트릭스 (Error Priority Matrix)

```
영향도 →      Low        Medium       High        Critical
빈도 ↓
High         Medium     High         Critical    Critical
Medium       Low        Medium       High        Critical
Low          Low        Low          Medium      High
Rare         Backlog    Low          Medium      High
```

## 추가 자료

### 예시 (Examples)
- `examples/debugging_workflow.md` - 단계별 디버깅 프로세스 예시
- `examples/common_errors.md` - 자주 발생하는 에러 패턴 및 해결책 카탈로그
- `examples/stack_traces.txt` - 분석과 함께 제공되는 스택 트레이스 예시

### 스크립트 (Scripts)
- `scripts/debug_helper.py` - 트레이스 파싱 및 세션 관리를 위한 Python 디버깅 유틸리티

### 추가 학습
- 언어별 디버깅 문서
- 프레임워크 에러 핸들링 가이드
- 프로파일링 및 성능 분석 도구
- 테스트 및 품질 보증 실무

---

**기억하세요**: 디버깅은 탐정 수사입니다. 체계적이고 인내심을 가지며, 증거가 진실로 당신을 인도하게 하세요. 모든 에러 메시지는 당신의 이해를 기다리고 있는 단서입니다.
