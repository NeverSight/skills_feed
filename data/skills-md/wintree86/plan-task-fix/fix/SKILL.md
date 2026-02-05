---
name: fix
description: >
  Backlog manager -- track bugs, improvements, and tech debt in backlog.md.
  Backlog 관리 스킬 (버그, 개선, 기술 부채).
  Triggers: /fix, "backlog", "백로그", "bug report", "버그 등록", "개선 등록",
            "not working", "issue", "problem", "performance", "slow", "upgrade"
---

# Fix - Backlog Manager

Track bugs, improvements, and tech debt in backlog.md.
버그, 개선사항, 기술 부채를 backlog.md로 관리하는 스킬입니다.

## Usage / 사용법

```
/fix                        # Show open items / 미해결 목록 표시
/fix "description"          # Auto-classify and add / 자동 분류 등록
/fix bug "description"      # Add to Bugs / Bugs 섹션에 등록
/fix improve "description"  # Add to Improvements / Improvements 섹션에 등록
/fix debt "description"     # Add to Tech Debt / Tech Debt 섹션에 등록
/fix done                   # Complete (select) / 완료 처리 (선택형)
/fix done [ID]              # Complete specific / 특정 항목 완료
/fix clean                  # Clean completed / 완료 항목 정리
```

The first argument determines the command: `$ARGUMENTS`

---

## Project Detection / 프로젝트 감지 규칙

1. **CWD-based** - Uses current working directory as project root / 현재 작업 디렉토리를 프로젝트 루트로 사용
2. **Git root detection** - `git rev-parse --show-toplevel` / Git root로 프로젝트 루트 확인
3. **Project name** - Git root folder name / git root 폴더명 사용

### backlog.md search order / backlog.md 탐색 순서:
1. `.claude-docs/backlog.md`
2. `.claude/docs/backlog.md`
3. `docs/backlog.md`
4. `BACKLOG.md`
5. `backlog.md`

### Document folder (for new files) / 문서 폴더 결정 (신규 생성 시):
1. `.claude-docs/` if exists / 존재하면 여기에 생성
2. `.claude/docs/` if exists / 존재하면 여기에 생성
3. `docs/` if exists / 존재하면 여기에 생성
4. Otherwise: `backlog.md` in CWD / 그 외: CWD에 생성

---

## Argument Parsing / 인수 파싱 규칙

Check first token of `$ARGUMENTS`:

1. `bug`, `improve`, `debt`, `done`, `clean` → subcommand / 서브커맨드로 처리
2. Anything else (or starts with quotes) → treat as description, auto-classify / 전체를 설명으로 취급, 자동 분류

### Examples / 예시:
```
/fix bug Login keyboard overlap         → bug subcommand
/fix improve Loading speed              → improve subcommand
/fix debt deprecated API replacement    → debt subcommand
/fix Card animation flickering          → auto-classify (not a subcommand)
/fix done B1                            → done subcommand, ID: B1
/fix done                               → done subcommand, no ID (select)
/fix clean                              → clean subcommand
/fix                                    → no args, show open items
/fix 카드 애니메이션 깜빡임              → auto-classify
```

---

## backlog.md Format / backlog.md 형식

```markdown
# Backlog

**Last Updated:** YYYY-MM-DD

## Bugs
- [ ] B1 Login keyboard overlap (2026-02-03)
- [x] B2 Card animation flicker (2026-02-03) -- 2026-02-03

## Improvements
- [ ] I1 Loading speed optimization (2026-02-03)

## Tech Debt
- [ ] T1 deprecated API replacement (2026-02-03)
```

### ID System / ID 체계
- Bugs: B1, B2, B3...
- Improvements: I1, I2, I3...
- Tech Debt: T1, T2, T3...
- **IDs are never reused** (gaps allowed: B1, B3 OK) / ID는 재사용하지 않음

### Date Recording / 날짜 기록
- Registered: `(YYYY-MM-DD)` in parentheses / 등록일
- Completed: `-- YYYY-MM-DD` appended after checkbox / 완료일 추가

### Next ID Logic / 다음 ID 결정 방법
Find highest number in the section and add 1.
해당 섹션의 기존 항목에서 가장 큰 번호를 찾아 +1합니다.
- Bugs has B1, B3 → next is B4
- Improvements is empty → I1

---

## Command: (default) - Open Items / 미해결 목록 표시

Shows open items from backlog.md.
backlog.md의 미해결 항목을 표시합니다.

**Runs when no arguments are given. / 인수가 없는 경우 실행됩니다.**

### Steps / 수행 단계:
1. Search for backlog.md (see search order) / backlog.md 파일 탐색
2. Read file / 파일 읽기
3. Filter open (`- [ ]`) items only / 미해결 항목만 필터링
4. Group by section and output / 섹션별로 그룹화하여 출력

### Output format / 출력 형식:
```
📋 Backlog Status / 현황

🐛 Bugs (2 open / 2개)
- B1 Login keyboard overlap (2026-02-03)
- B3 Network error handling missing (2026-02-03)

💡 Improvements (1 open / 1개)
- I1 Loading speed optimization (2026-02-03)

🔧 Tech Debt (1 open / 1개)
- T1 deprecated API replacement (2026-02-03)

Total: 4 open items / 총 4개 미해결
```

### If no file found / 파일 없는 경우:
```
📋 No backlog found / Backlog 없음

💡 Add your first item with / 첫 항목 등록:
   /fix bug "description"
Example / 예: /fix bug Login keyboard overlap
```

---

## Command: bug / improve / debt - Add Item / 항목 등록

Adds an item to the specified section.
지정된 섹션에 항목을 등록합니다.

### Syntax / 구문:
```
/fix bug description
/fix improve description
/fix debt description
```

### Section mapping / 섹션 매핑:
| Subcommand | Section | ID Prefix |
|------------|---------|-----------|
| bug | Bugs | B |
| improve | Improvements | I |
| debt | Tech Debt | T |

### Steps / 수행 단계:
1. Search backlog.md (create if missing) / backlog.md 탐색 (없으면 생성)
2. Find last ID in section / 해당 섹션에서 마지막 ID 확인
3. Assign new ID (last + 1) / 새 ID 부여
4. Add item with today's date / 오늘 날짜와 함께 추가
5. Update `Last Updated` / 갱신
6. Save / 저장

### Output format / 출력 형식:
```
✅ Added / 등록: B3 Login keyboard overlap

📍 Section / 섹션: Bugs
📅 Date / 등록일: 2026-02-03
```

---

## Command: Auto-classify / 자동 분류 등록

When first token is not a subcommand, the full text is treated as description and auto-classified by keywords.
첫 토큰이 서브커맨드가 아닌 경우, 전체 텍스트를 설명으로 취급하고 키워드로 자동 분류합니다.

### Syntax / 구문:
```
/fix Card animation flickering
/fix deprecated package cleanup
```

### Auto-classify keywords / 자동 분류 키워드:

| Category | Keywords |
|----------|----------|
| Bug | 버그, 에러, 오류, 깨짐, 안됨, 깜빡, crash, error, bug, fix, broken, fail, 실패, not working, issue, problem |
| Improve | 개선, 향상, 빠르게, 속도, UX, UI, improve, better, enhance, 최적화, optimize, performance, slow |
| Tech Debt | deprecated, 리팩토링, 정리, 마이그레이션, refactor, cleanup, migrate, legacy, 레거시, upgrade |

### Classification rules / 분류 규칙:
1. Case-insensitive keyword search in description / 대소문자 무관 키워드 검색
2. If matched: use that category / 매칭되면 해당 분류
3. Multiple matches: first match wins (Bug > Improve > Tech Debt) / 먼저 매칭된 분류 우선
4. No match: **default to Bug** / 매칭 없으면 기본값: Bug

### Output format / 출력 형식:
```
✅ Added / 등록: B3 Card animation flickering

📍 Section / 섹션: Bugs (auto-classified / 자동 분류: "flickering" keyword)
📅 Date / 등록일: 2026-02-03
```

---

## Command: done - Mark Complete / 완료 처리

Marks an item as completed.
항목을 완료로 표시합니다.

### Syntax / 구문:
```
/fix done B1       # Specific item / 특정 항목 완료
/fix done          # Select from list / 선택형 완료 (AskUserQuestion)
```

### Steps (with ID) / 수행 단계 (ID 지정 시):
1. Find item by ID in backlog.md / backlog.md에서 해당 ID 찾기
2. Change `- [ ]` → `- [x]` / 변경
3. Append ` -- YYYY-MM-DD` completion date / 완료일 추가
4. Update `Last Updated` / 갱신
5. Save / 저장

### Steps (no ID) / 수행 단계 (ID 미지정 시):
1. Extract open items from backlog.md / 미해결 항목 추출
2. AskUserQuestion to select items (multiSelect: true) / 항목 선택
3. Mark selected items as complete / 선택된 항목 완료 처리
4. Save / 저장

### Output format / 출력 형식:
```
✅ Done / 완료: B1 Login keyboard overlap

📅 Completed / 완료일: 2026-02-03
📋 Remaining open / 남은 미해결: 3
```

### If ID not found / ID를 찾을 수 없는 경우:
```
❌ B99 not found / 찾을 수 없습니다.

📋 Open items / 미해결 항목:
- B1 Login keyboard overlap
- B3 Network error handling missing
```

---

## Command: clean - Remove Completed / 완료 항목 정리

Removes completed items (`[x]`) from backlog.md.
완료된 항목을 backlog.md에서 제거합니다.

### Steps / 수행 단계:
1. Find `- [x]` items in backlog.md / 완료 항목 찾기
2. AskUserQuestion to confirm / 정리 확인:
   - "Remove N completed items? / 완료된 N개 항목을 정리하시겠습니까?"
   - Options: "Clean / 정리" / "Cancel / 취소"
3. Remove on confirm / 확인 시 완료 항목 제거
4. Update `Last Updated` / 갱신
5. Save / 저장

### Output format / 출력 형식:
```
🧹 Cleaned / 정리 완료

Removed items / 삭제된 항목 (3):
- B2 Card animation flicker (completed / 완료: 2026-02-03)
- I2 Loading indicator added (completed / 완료: 2026-02-03)
- T1 deprecated API replacement (completed / 완료: 2026-02-03)

📋 Remaining open / 남은 미해결: 2
```

### If no completed items / 완료 항목이 없는 경우:
```
📋 No completed items to clean / 정리할 완료 항목이 없습니다.
```

---

## backlog.md Initial Template / 초기 생성 템플릿

Auto-created when first item is added and no backlog.md exists.
backlog.md가 없을 때 첫 항목 등록 시 자동 생성합니다.

```markdown
# Backlog

**Last Updated:** YYYY-MM-DD

## Bugs

## Improvements

## Tech Debt
```

### Key Rules / 핵심 규칙:
1. **3 sections required** - Bugs, Improvements, Tech Debt / 3개 섹션 필수
2. **Section headings** - Exact match: `## Bugs`, `## Improvements`, `## Tech Debt` / 정확히 일치
3. **Item format** - `- [ ] {ID} {description} (YYYY-MM-DD)` / 항목 형식
4. **Completed format** - `- [x] {ID} {description} (YYYY-MM-DD) -- YYYY-MM-DD` / 완료 형식
5. **Last Updated** - Refresh on every change / 변경 시마다 갱신

---

## Integration with /plan, /task / 연계

```
/plan  →  plan.md    (Feature planning / 기능 기획)
/task  →  task.md    (Task tracking / 태스크 추적)
/fix   →  backlog.md (Bugs/fixes/improvements / 버그/수정/개선)
```

- Each tool works independently / 각 도구는 독립적으로 동작
- Large backlog items → `/plan add` to escalate → `/fix done` to close / 큰 항목은 plan으로 이관
- Bugs found during plan work → `/fix bug "description"` to register / plan 진행 중 발견된 버그 등록

---

## Command Reference / 명령어 정리

| Command | Action | Agent | Purpose |
|---------|--------|-------|---------|
| `/fix` | Open items list / 미해결 목록 | No | Check status / 현황 확인 |
| `/fix "desc"` | Auto-classify add / 자동 분류 등록 | No | Quick add / 빠른 등록 |
| `/fix bug "desc"` | Add to Bugs / 등록 | No | Report bug / 버그 등록 |
| `/fix improve "desc"` | Add to Improvements / 등록 | No | Suggest improvement / 개선 등록 |
| `/fix debt "desc"` | Add to Tech Debt / 등록 | No | Log tech debt / 기술부채 등록 |
| `/fix done [ID]` | Mark complete / 완료 처리 | No | Close item / 항목 완료 |
| `/fix clean` | Clean completed / 완료 정리 | No | Tidy up / 정리 |

---

## Related Skills

Part of the **plan-task-fix** suite:
- `/plan` - Plan document management (plan.md) / 기획서 관리
- `/task` - Task tracking and progress (task.md) / 태스크 추적
- `/fix` - Bug/improvement backlog (backlog.md) / 백로그 관리

Install: `npx skills add wintree86/plan-task-fix`
