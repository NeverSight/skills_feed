---
name: skills-batch-ops
description: 프로젝트에 필요한 스킬을 3채널(find-skills/인기/웹)로 탐색하고 기존 설치 스킬까지 동일 기준으로 검토해 최종 스킬 셋(keep/install/remove)을 적용할 때 사용하는 Markdown 지시형 스킬입니다.
---

# Skills Batch Ops

`skills-batch-ops`는 아래 운영 단계를 고정으로 수행하는 문서 지시형 스킬입니다.

0. 실행 가능성 프리플라이트
1. 프로젝트 분석
2. `find-skills` 기반 후보 탐색
3. 인기/사용량 기반 후보 탐색
4. 인터넷 검색 기반 후보 탐색
5. 기존 설치 스킬 인벤토리 수집
6. 합집합 병합 + 전체 `SKILL.md` 본문 검토 + 유사/중복 후보 대표 선정
7. 최종 스킬 셋 결정(dry-run)
8. 최종 스킬 셋 적용(install/remove) 및 결과 기록

## 실행 원칙

- 이 스킬은 문서 지시만 제공합니다. 스킬 내부 실행 스크립트 의존 경로를 만들지 마세요.
- 탐색 채널 `find`, `popular`, `web` 3개를 모두 시도하세요.
- 채널이 막히면 억지로 채우지 말고 `blocked`로 기록하세요.
- 후보 병합은 교집합이 아니라 합집합 기준으로 수행하세요.
- 스킬 이름만 보고 설치하지 말고, 반드시 실제 `SKILL.md` 본문을 확인하세요.
- 기존 설치 스킬도 신규 후보와 동일한 깊이로 `SKILL.md` 본문을 검토하세요.
- 유사 기능군에서는 대표 스킬을 선정하고 나머지는 대체안으로 남기세요.
- 최종 결정은 반드시 `keep | install | remove | hold` 중 하나로 명시하세요.
- 설치/삭제 전에는 반드시 dry-run 계획을 먼저 제시하세요.
- `skills` CLI 명령은 무쿼리 interactive 모드를 피하고, 가능한 한 non-interactive 형태(`find "<query>"`, `list`, `list -g`)로 실행하세요.
- 명령이 장시간 무출력 상태로 유지되면 hang으로 간주해 중단하고 `blocked_cli_hang`으로 기록하세요(권장 기준: 45초, 최소 1회 재시도).
- 채널 차단 시에는 누락 채널을 억지로 대체하지 말고 `blocked`로 닫은 뒤, Step 6에서 `method_count` 해석을 보정하세요.
- 인벤토리는 `skills list`/`skills list -g`를 우선하고, CLI 차단 시 fallback 스캔 결과를 `complete|partial|blocked` 완전성과 함께 기록하세요.
- 정보가 부족해도 질문을 남발하지 말고, 합리적 기본 가정을 적용한 뒤 `가정/영향`을 기록하세요.
- 본 스킬의 결과물 구조는 `SKILL.md`와 `references/*.md`만 허용합니다.

## 기본 산출물

실행 중 아래 문서를 생성/갱신하세요.

- `project_profile.md`
- `candidates.find.md`
- `candidates.popular.md`
- `candidates.web.md`
- `inventory.installed.md`
- `candidates.merged.md`
- `review.content.md`
- `review.manifest.md`
- `install.plan.md`
- `install.result.md`

템플릿은 `references/report-templates.md`를 사용하세요.

프리플라이트 결과는 `project_profile.md` 상단(`preflight_status`, `blocked_reason`, `elapsed_sec`)에 함께 기록하세요.

## Step 0) 실행 가능성 프리플라이트

Step 1~8을 시작하기 전에 `skills` CLI 실행 가능성을 먼저 점검하세요.

- 아래 명령을 순서대로 시도해 `ok | blocked`를 기록합니다.
  - `npx --yes skills --version`
  - `npx --yes skills --help`
  - `npx --yes skills find "test"`
  - `npx --yes skills list`
  - `npx --yes skills list -g`
- 무출력 hang 판단 기준을 미리 정합니다(권장: 45초 무출력).
- hang이 발생하면 즉시 중단 후 1회 재시도합니다.
- 재시도도 실패하면 `blocked_cli_hang`으로 분류하고, Step 2/5/8에서 degraded 모드로 진행합니다.
- 각 명령별로 `command`, `status`, `elapsed_sec`, `stderr_head`를 남겨 재현 가능하게 만드세요.

## Step 1) 프로젝트 분석

프로젝트 목표, 기술 스택, 제약사항을 먼저 정리하세요.

- 코드/문서에서 핵심 키워드(도메인, 언어, 런타임, 배포환경)를 추출합니다.
- 설치 가능한 스킬 수 상한(예: 최대 5개)과 우선순위(안정성/속도/범용성)를 정합니다.
- 사용자 입력이 부족하면 기본값을 사용하되 `가정/영향`을 남깁니다.

결과는 `project_profile.md`로 정리하세요.

## Step 2) `find-skills` 기반 후보 탐색

`find-skills`를 이용해 프로젝트 맞춤 후보를 수집하세요.

- 필요 시 `npx --yes skills add vercel-labs/skills --skill find-skills -y`로 준비합니다.
- 프로젝트 키워드 기반 질의를 2~3개 실행합니다(반드시 `find "<query>"` 형태).
- raw 결과와 함께 `owner/repo@skill`, 설치 지표, 한 줄 근거를 정리합니다.
- 채널 수행 결과를 `done | blocked`로 기록하고, `blocked`면 원인/영향을 함께 남깁니다.
- 2~3개 질의가 모두 `blocked_cli_hang`이면 `find` 채널을 `blocked`로 닫고 Step 3~6으로 진행합니다.
- `find` 채널 차단 시 Step 6에서 `method_count`를 절대 게이트로 쓰지 말고 보정 규칙을 적용합니다.

결과는 `candidates.find.md`로 정리하세요.

## Step 3) 인기/사용량 기반 후보 탐색

공개 인기 목록에서 프로젝트와 맞는 스킬을 수집하세요.

- 인기 페이지/목록에서 후보를 추립니다.
- 단순 인기만으로 승인하지 말고 프로젝트 관련성을 함께 기록합니다.
- 각 후보에 근거 URL을 남깁니다.
- 지표 정의(예: installs, ranking, stars)와 확인 시각을 남깁니다.
- 채널 수행 결과를 `done | blocked`로 기록하고, `blocked`면 원인/영향을 함께 남깁니다.
- 인기 지표 소스 우선순위는 다음과 같이 고정합니다.
  1. `skills.sh/<owner>/<repo>/<skill>` 상세 페이지 설치 지표
  2. `npx --yes skills find "<query>"` 결과의 installs
  3. GitHub API 저장소 지표(`stargazers_count`, `pushed_at`)
- 각 지표에 `metric_source`, `raw_value`, `checked_at_utc`를 함께 기록해 재현성을 확보하세요.

결과는 `candidates.popular.md`로 정리하세요.

## Step 4) 인터넷 검색 기반 후보 탐색

일반 웹 검색으로 추가 후보를 수집하세요.

- 블로그, 문서, GitHub, 커뮤니티 글 등에서 후보를 찾습니다.
- 최신성/신뢰도를 보고 우선순위를 나눕니다.
- 각 후보에 근거 URL, 왜 적합한지 한 줄 설명을 남깁니다.
- 채널 수행 결과를 `done | blocked`로 기록하고, `blocked`면 원인/영향을 함께 남깁니다.

결과는 `candidates.web.md`로 정리하세요.

## Step 5) 기존 설치 스킬 인벤토리 수집

현재 환경에 이미 설치된 스킬 목록을 수집하고 정규화하세요.

- 설치 목록 조회 명령을 먼저 확인하고(예: `npx --yes skills --help`), 아래 순서로 수집하세요.
  1. `npx --yes skills list` (project scope)
  2. `npx --yes skills list -g` (global scope)
- 조회 결과를 `owner/repo@skill` 형식으로 정규화합니다.
- 두 명령 중 하나라도 실패하면 fallback으로 아래 경로를 스캔합니다.
  - `~/.agents/skills/*/SKILL.md`
  - `<project>/.agents/skills/*/SKILL.md`
- 결과 문서에 `inventory_coverage: complete|partial|blocked`를 반드시 기록합니다.

결과는 `inventory.installed.md`로 정리하세요.

## Step 6) 합집합 병합 + 전체 `SKILL.md` 본문 검토 + 유사/중복 정리

2~5단계에서 모은 후보(탐색+기존 설치)를 합집합으로 병합한 뒤, 각 후보의 실제 `SKILL.md`를 확인하고 유사 후보를 정리하세요.

- 우선 후보 병합표를 `candidates.merged.md`에 합집합 기준으로 만듭니다.
- 각 후보에 대해 실제 `SKILL.md`를 찾아 읽습니다(기존 설치 스킬 포함).
- 아래 항목을 반드시 확인하세요:
  - frontmatter `name`, `description` 유효성
  - 본문이 구체적 워크플로를 제공하는지
  - placeholder(`TODO`, `TBD`, `PLACEHOLDER`) 과다 여부
  - 프로젝트 키워드와의 실질 적합성
- 유사/중복 후보를 기능 기준으로 클러스터링하고 대표 스킬을 선정합니다.
- 동일 기능군에서 여러 스킬을 설치하려면 보완 관계를 근거로 제시하세요.
- 기존 설치 스킬도 최종 액션(`keep | remove | hold`)을 반드시 부여하세요.

검토 기준 상세는 `references/skill-content-review-rubric.md`를 사용하세요.

검토 결과:

- `review.content.md`: 후보별 본문 검토 상세(탐색+기존 설치)
- `review.manifest.md`: `approved | pending | rejected` 판정 + `keep | install | remove | hold` 최종 액션

권장 판정 규칙:

- `approved`: 본문 검토 통과 + 유사군 대표 선정 통과 + 프로젝트 적합성 높음
- `pending`: 본문은 양호하지만 근거나 적합성, 실행 가능성 보완 필요
- `rejected`: 본문 검토 실패 또는 프로젝트와 부적합

권장 액션 규칙:

- `keep`: 기존 설치 + `approved` + 최종 세트에 유지
- `install`: 미설치 + `approved` + 최종 세트에 포함
- `remove`: 기존 설치 + (`rejected` 또는 중복 대체안) + 제거 근거/영향 정리 완료
- `hold`: 근거 부족/차단으로 즉시 변경 불가

차단 채널 보정 규칙:

- `method_count`는 참고 지표이며, 채널이 `blocked`인 실행에서는 절대 게이트로 사용하지 않습니다.
- 채널 차단이 있을 때는 `SKILL.md` 본문 통과 + 근거 URL 2개 이상 + 적합성 `high|medium`이면 `approved` 가능으로 처리합니다.
- 차단으로 인한 보정 여부를 `review.manifest.md`의 `rationale`에 명시하세요.

## Step 7) 최종 스킬 셋 결정(dry-run)

`review.manifest.md`를 바탕으로 현재 셋 대비 목표 셋의 차이를 명시하세요.

1. `install.plan.md`에 현재 셋, 목표 셋, 액션별 목록(`keep/install/remove/hold`)을 작성합니다.
2. 설치/삭제 명령을 액션별로 분리해 작성합니다.
3. 삭제 대상은 롤백 경로(재설치 명령)와 영향 범위를 함께 기록합니다.

## Step 8) 최종 스킬 셋 적용(install/remove) 및 결과 기록

실행은 `install.plan.md`의 dry-run 계획을 기준으로 진행하세요.

0. 설치/삭제 직전에 실행 가능성 재확인(`npx --yes skills --help`, `npx --yes skills list`)을 수행합니다.
1. `install` 대상은 설치를 실행하고 결과를 기록합니다.
2. `remove` 대상은 삭제를 실행하고 결과를 기록합니다.
3. `keep`/`hold` 대상은 변경 없이 판단 근거를 결과 문서에 기록합니다.
4. 재확인 실패 시 변경 실행을 중단하고 `deferred_blocked_cli`로 기록합니다.
5. `install.result.md`에 성공/실패/원인/재시도 조건(`next_retry_condition`)을 남깁니다.

명령 예시:

```bash
npx --yes skills add <owner/repo> --skill <skill-name> -y
npx --yes skills remove <owner/repo> --skill <skill-name> -y
```

## 품질 게이트

- 3개 탐색 채널은 모두 시도하되, 실패/차단 시 `blocked` 기록과 영향 보고가 있으면 완료로 처리할 수 있습니다.
- 기존 설치 스킬 인벤토리도 반드시 시도하고, 실패 시 `blocked` 사유를 기록하세요.
- 실제 `SKILL.md`를 읽지 않은 후보는 `approved`로 올리지 마세요.
- 실제 `SKILL.md`를 읽지 않은 기존 설치 스킬은 `keep`로 확정하지 마세요.
- 유사군 내 다중 `approved`는 보완 관계 근거가 없으면 허용하지 마세요.
- 기존 설치 스킬은 모두 `keep | remove | hold` 중 하나로 분류되어야 합니다.
- 설치 실패를 숨기지 말고 `install.result.md`에 그대로 기록하세요.
- 테스트/실행이 막힌 경우, 막힌 원인과 영향 범위를 분리해서 보고하세요.
- 프리플라이트 결과(`preflight_status`)와 차단 코드(`blocked_cli_hang` 등)가 누락되면 미완료로 처리합니다.
- `find`/`popular`/`web` 채널 상태를 `channel_health`로 남기고, 차단 시 `method_count` 보정 근거를 기록하세요.
- 인벤토리 결과는 `inventory_coverage=complete|partial|blocked` 중 하나를 반드시 포함해야 합니다.
- 적용 단계가 차단되면 `deferred_blocked_cli` 항목과 재시도 조건이 있어야 합니다.

## 최종 보고 형식

최종 응답은 아래 순서를 기본으로 사용하세요.

1. 프로젝트 분석 요약
2. 채널별 탐색 결과(find/popular/web)
3. 기존 설치 스킬 인벤토리 요약
4. 합집합 병합 및 유사/중복 정리 결과(대표/대체안)
5. `SKILL.md` 본문 검토 요약(통과/실패 사유)
6. 최종 스킬 셋 diff(`keep/install/remove/hold`)
7. 설치/삭제 계획 또는 실행 결과
8. 남은 리스크/추가 확인 항목

## References

- `references/source-discovery-guide.md`
- `references/skill-content-review-rubric.md`
- `references/report-templates.md`
