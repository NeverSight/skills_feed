---
name: update-study
description: This skill should be used when the user asks to "update study", "analyze new experiments", "update experiment document", or "refresh study notes". Features incremental detection (only analyze NEW experiments), iterative writing improvement loop with quality criteria, zero-hallucination verification, and PDF export. Usage - `/update-study logs/experiment.log study.md` or `/update-study "logs/exp1.log logs/exp2.log" results/ablation_study.md`
version: 2.0.0
---

# Update Study - Enhanced Iterative Experiment Analysis

실험 로그를 분석하여 study 문서를 업데이트하는 스킬입니다.

## Core Features

1. **Incremental Detection** - 새 실험만 분석 (이미 문서화된 실험 스킵)
2. **Iterative Writing Loop** - 글 품질 개선 루프 (clarity, coherence, insight depth)
3. **Zero Hallucination** - 로그 레벨 교차 검증
4. **PDF Export** - 최종 문서를 PDF로 변환

## Usage

```
/update-study <log_path(s)> <study_md_path>
```

- `log_path(s)`: 실험 로그 파일 경로 (공백으로 구분하여 여러 개 가능)
- `study_md_path`: 업데이트할 study markdown 파일 경로

## Arguments Parsing

`$ARGUMENTS`에서 마지막 인자가 `.md` 파일이면 study 파일, 나머지는 로그 파일로 파싱합니다.

```
예시:
  /update-study logs/exp1.log results/study.md
  → log_files: ["logs/exp1.log"]
  → study_file: "results/study.md"

  /update-study logs/exp1.log logs/exp2.log memgen_ablation_study.md
  → log_files: ["logs/exp1.log", "logs/exp2.log"]
  → study_file: "memgen_ablation_study.md"
```

---

## Workflow Overview

```
Phase 0: Incremental Detection (NEW)
  ├── logs/ 스캔
  ├── 기존 study 파싱 (이미 분석된 실험 식별)
  └── 새 실험 목록 생성 → 없으면 "No new experiments" 출력 후 종료

Phase 1: File Verification
  ├── 로그 파일 존재 확인
  └── study.md 읽기

Phase 2: Interpretation
  ├── experiment-interpreter 호출
  └── 메트릭 추출 + 초안 작성

Phase 2b: Writing Quality Loop (NEW)
  ├── Quality evaluation (clarity, coherence, insight)
  ├── Revision if needed (definition-first, topic-first)
  └── Max 3 iterations, pass at score ≥ 80

Phase 3: Append to Document
  ├── [NEW] 태그로 새 섹션 표시
  └── Timeline 테이블 업데이트

Phase 4: Verification
  ├── experiment-verifier 호출
  ├── 숫자 정확성 검증
  └── 논리 일관성 검증

Phase 5: Export (NEW)
  ├── PDF 변환 (pandoc/weasyprint)
  └── 완료 보고
```

---

## Phase 0: Incremental Detection (NEW)

### Step 0.1: 로그 디렉토리 스캔

```
1. logs/ 디렉토리에서 모든 로그 파일 목록 생성
   - 패턴: *_train.log, *_eval.log, *.log
   - 파일 수정 시간 기준 정렬

2. 입력된 로그 파일 목록과 교차 확인
```

### Step 0.2: 기존 Study 분석

```
기존 study.md에서 이미 문서화된 실험 식별:

1. 실험 헤더 패턴 검색:
   - `### E{N}:` 또는 `### Experiment:`
   - `## Experiment {N}:`

2. 로그 파일 참조 추출:
   - `[*_train.log:*]` 형식의 출처 표기
   - `Source:` 열의 파일명

3. 문서화된 실험 목록 구축:
   documented_experiments = {
       "evolve_h_only_train.log",
       "cross_attn_train.log",
       ...
   }
```

### Step 0.3: 새 실험 결정

```python
new_experiments = set(input_logs) - set(documented_experiments)

if len(new_experiments) == 0:
    print("✓ No new experiments to analyze")
    print(f"  Already documented: {len(documented_experiments)} experiments")
    exit()  # 종료
else:
    print(f"📊 Found {len(new_experiments)} new experiment(s) to analyze:")
    for exp in new_experiments:
        print(f"  - {exp}")
```

---

## Phase 1: File Verification

### Step 1.1: 파일 확인

```
1. 새 실험 로그 파일 존재 확인
   - 각 log_path에 대해 파일 존재 여부 확인
   - 존재하지 않으면 에러 메시지 출력 후 중단

2. study.md 파일 확인
   - 파일이 존재하면 Read tool로 전체 내용 읽기
   - 파일이 없으면 새로 생성할 것임을 안내

3. 로그 파일 요약 정보 추출 (빠른 스캔)
   - 실험 config 파일 경로
   - 실험 모드 (train/evaluate)
   - 최종 metric 라인 위치
```

### Step 1.2: 기존 study.md 분석

```
기존 study.md에서 확인할 사항:
- 이미 기록된 실험 목록
- 비교 가능한 baseline 결과
- 미해결 가설 목록
- 계획된 실험 목록 (이번 실험이 기존 계획에 해당하는지)
```

---

## Phase 2: Interpretation (experiment-interpreter)

### Task Tool 호출

```
Task tool 사용:
- subagent_type: "experiment-interpreter"
- prompt:

  "다음 실험 로그를 분석하고 study.md 업데이트 초안을 생성해주세요.

  ## 로그 파일
  {각 로그 파일의 전체 경로}

  ## 기존 study.md 내용 (비교용)
  {기존 study.md의 결과 요약 테이블}

  ## 이전 검증 피드백 (있는 경우)
  {verifier의 feedback_summary - 첫 iteration에는 없음}

  ## 요구사항
  1. 로그에서 모든 수치를 추출하고 (source: filepath:L행번호) 형식으로 출처 표기
  2. 기존 결과와 비교 테이블 생성
  3. 데이터에 기반한 해석 작성
  4. 각 가설은 falsifiable + prediction + falsification 포함
  5. 다음 실험은 구체적 config 변경 포함
  6. 출력은 study.md에 바로 append할 수 있는 markdown 형식

  ## 출력 형식
  references/interpretation-template.md 템플릿을 따라주세요."
```

---

## Phase 2b: Writing Quality Loop (NEW)

### Step 2b.1: Quality Evaluation

작성된 초안에 대해 품질 평가 수행:

```
평가 기준 (references/quality-criteria.md 참조):

1. Definition-First (30점)
   - 모든 전문 용어가 "X is Y" 형태로 정의되었는가?
   - 새로운 개념이 사용 전에 정의되었는가?

2. Topic-First Paragraphs (25점)
   - 모든 문단이 핵심 결과/주장으로 시작하는가?
   - 첫 문장만 읽어도 문단 내용을 파악할 수 있는가?

3. Compare-Contrast (20점)
   - 새 결과가 이전 실험과 비교되었는가?
   - 차이의 원인/해석이 제시되었는가?

4. Insight Depth (15점)
   - 표면적 기술을 넘어 "왜"에 대한 분석이 있는가?
   - 예상과 다른 결과에 대한 가설이 있는가?

5. Minimal Adjectives (10점)
   - 불필요한 수식어가 없는가?
   - 주관적 표현 대신 구체적 수치가 사용되었는가?

총점: /100
통과 기준: ≥ 80점
```

### Step 2b.2: Revision

점수가 80점 미만인 경우 수정:

```
1. [Critical: Definition Missing]
   - 미정의 용어 목록 작성
   - 각 용어에 대해 "X is Y" 정의 추가

2. [Critical: Topic-Last Paragraph]
   - 문단 재구성: 핵심 → 설명 → 근거 순서로

3. [Warning: No Comparison]
   - 이전 실험과의 비교 테이블 추가
   - 차이 분석 문단 추가

4. [Warning: Shallow Insight]
   - "왜 이런 결과가 나왔는가?" 분석 추가
   - 가설 강화

5. [Minor: Excessive Adjectives]
   - "significantly improved" → "+12.5%p"
   - "much faster" → "2.3x speedup"
```

### Step 2b.3: Iteration Control

```
최대 반복: 3회

Iteration 1: 초안 → 품질 평가 → 수정 (필요시)
  → Score ≥ 80: Phase 3으로 진행
  → Score < 80: feedback 수집

Iteration 2: 수정안 → 재평가
  → Score ≥ 80: Phase 3으로 진행
  → Score < 80: feedback 수집

Iteration 3: 최종 수정 → 재평가
  → Score ≥ 80: Phase 3으로 진행
  → Score < 80: 현재 최선 버전으로 진행 + 이슈 보고
```

---

## Phase 3: Document Update

### 추가 규칙

1. **Append Only**: 기존 내용 뒤에 새 섹션 추가. 기존 내용 수정 금지.
2. **[NEW] 태그**: 새로 추가된 실험에 `[NEW]` 태그 표시 (다음 업데이트 시 제거)
3. **구분선**: 새 실험 전에 `---` 구분선 삽입
4. **날짜 표기**: 실험 실행 날짜 (로그 타임스탬프 기반)
5. **일관된 포맷**: references/interpretation-template.md 템플릿 준수

### [NEW] 태그 처리

```markdown
---

### [NEW] Experiment: {experiment_name} ({YYYY-MM-DD})

...
```

다음 `/update-study` 실행 시:
1. 이전에 추가된 `[NEW]` 태그 모두 제거
2. 새로 추가되는 섹션에만 `[NEW]` 태그 부여

---

## Phase 4: Verification (experiment-verifier)

### Task Tool 호출

```
Task tool 사용:
- subagent_type: "experiment-verifier"
- prompt:

  "다음 study.md 업데이트 내용을 검증해주세요.

  ## 검증 대상 (새로 추가된 섹션)
  {Phase 3에서 추가한 내용}

  ## 원본 로그 파일 경로
  {각 로그 파일의 전체 경로}

  ## 기존 study.md (변경 여부 확인용)
  {기존 study.md 내용}

  ## 검증 요구사항
  1. 모든 수치를 원본 로그와 대조 (파일:라인 직접 확인)
  2. 해석의 논리적 타당성 검증
  3. 모든 가설의 falsifiability 확인
  4. 다음 실험의 실행 가능성 확인
  5. 기존 결과 변경 여부 확인

  ## 출력
  JSON 형식의 검증 보고서를 반환해주세요."
```

### 결과 처리

```python
if verdict == "PASS":
    # Phase 5로 진행
elif iteration < 3:
    # feedback_summary를 Phase 2로 전달
    # interpreter에게 수정 요청
else:
    # 최대 반복 도달
    # 현재 최선 버전 저장
    # 미해결 이슈 사용자에게 보고
```

---

## Phase 5: Export (NEW)

### Step 5.1: Markdown 확정

```
1. study.md 최종 내용 저장
2. [NEW] 태그가 포함된 섹션 확인
```

### Step 5.2: PDF 변환

```
scripts/export_pdf.py 사용:

python scripts/export_pdf.py study.md study.pdf

변환 옵션:
- TOC (Table of Contents) 포함
- [NEW] 태그 시각적 강조 (노란색 하이라이트)
- 테이블 깔끔한 포맷팅
- 코드 블록 문법 강조

Fallback 순서:
1. pandoc + LaTeX (최상의 품질)
2. weasyprint (pandoc 없을 시)
3. Markdown만 저장 (PDF 변환 실패 시 경고)
```

### Step 5.3: 완료 보고

```
✅ Update Complete!
  📄 Markdown: study.md
  📑 PDF: study.pdf (optional)
  📊 New experiments: {N}개
  🔬 Hypotheses: {N}개
  🧪 Next experiments: {N}개
```

---

## Progress Reporting

실행 중 사용자에게 상태를 보고합니다:

```
[Phase 0] Incremental Detection...
  ✓ Scanned logs/: {N}개 파일
  ✓ Already documented: {M}개 실험
  ✓ New experiments: {K}개 발견

[Phase 1] File Verification...
  ✓ 로그 파일 확인: {K}개
  ✓ study.md 읽기 완료

[Phase 2] Interpretation...
  ✓ 수치 추출: {N}개 메트릭
  ✓ 비교 테이블 생성

[Phase 2b] Writing Quality Loop...
  → Iteration 1: Score 72/100
    - Critical: Definition missing (2)
    - Warning: Topic-last paragraph (1)
  → Iteration 2: Score 85/100
    ✓ All critical issues resolved

[Phase 3] Document Update...
  ✓ 새 섹션 추가 ([NEW] 태그)

[Phase 4] Verification...
  → Numerical: {verified}/{total}
  → Logic: {sound}/{total}
  → Verdict: PASS

[Phase 5] Export...
  ✓ PDF 변환 완료

✅ Complete!
  - New experiments: {experiment_names}
  - Accuracy: {X.XX%}
  - Hypotheses: {N}개
  - Next experiments: {N}개
```

---

## Quality Criteria Summary

| Criterion | Weight | Pass Threshold |
|-----------|--------|----------------|
| Definition-First | 30점 | 용어 100% 정의 |
| Topic-First | 25점 | 문단 90% 두괄식 |
| Compare-Contrast | 20점 | 비교 테이블 필수 |
| Insight Depth | 15점 | "왜" 분석 포함 |
| Minimal Adjectives | 10점 | 수치 기반 표현 |

**Overall Pass: ≥ 80점**

---

## Additional Resources

- `references/interpretation-template.md` - 실험 해석 템플릿
- `references/quality-criteria.md` - 글 품질 평가 상세 기준
- `scripts/export_pdf.py` - PDF 변환 유틸리티

---

## Cautions

1. **로그 파일이 ground truth**: 로그에 없는 수치는 사용 불가
2. **Append Only**: 이전 결과를 절대 수정하지 않음
3. **매 수치에 출처**: `(source: filepath:L행번호)` 필수
4. **가설은 falsifiable**: 검증 불가능한 가설은 삭제
5. **최대 3회 반복**: 무한 루프 방지
6. **새 실험 우선**: 이미 문서화된 실험은 자동 스킵
7. **[NEW] 태그**: 새 추가분 명확히 표시
