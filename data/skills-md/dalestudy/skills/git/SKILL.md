---
name: git
description: "Git 버전 관리 모범 관례 및 워크플로우 가이드. 다음 상황에서 사용: (1) Git 커밋 메시지 작성 시 (Conventional Commits 규칙 적용), (2) 브랜치 생성 및 관리 시 (GitHub Flow 기반), (3) PR 생성 및 병합 전략 선택 시, (4) Git 히스토리 정리 작업 시 (rebase, squash, cherry-pick), (5) Merge conflict 해결 시, (6) 'git', '.git', 'commit', 'branch', 'merge', 'rebase' 키워드가 포함된 작업 시"
license: MIT
metadata:
  author: DaleStudy
  version: "1.0.0"
allowed-tools: Bash(git:*)
---

# Git

Git 버전 관리 모범 관례 및 워크플로우 가이드.

## 커밋 메시지 컨벤션

### Conventional Commits 사용

커밋 메시지는 `<type>: <description>` 형식을 따른다:

```
feat: add form validation to login page
fix: prevent duplicate email check error on signup
docs: add installation guide to README
refactor: extract auth logic into separate module
test: add payment feature tests
chore: update dependencies
```

#### 주요 타입

| 타입       | 설명                                     | 예시                                      |
| ---------- | ---------------------------------------- | ----------------------------------------- |
| `feat`     | 새로운 기능 추가                         | `feat: add dark mode support`             |
| `fix`      | 버그 수정                                | `fix: prevent token deletion on logout`   |
| `docs`     | 문서 변경 (코드 변경 없음)               | `docs: update API documentation`          |
| `style`    | 코드 포맷팅, 세미콜론 누락 (동작 변경 X) | `style: apply ESLint rules`               |
| `refactor` | 리팩토링 (기능 변경 없음)                | `refactor: extract utility functions`     |
| `test`     | 테스트 코드 추가/수정                    | `test: add login API tests`               |
| `chore`    | 빌드, 설정 변경 (src 변경 없음)          | `chore: update Webpack config`            |
| `perf`     | 성능 개선                                | `perf: implement lazy loading for images` |

#### 상세 형식 (선택사항)

```
<type>(<scope>): <subject>

<body>

<footer>
```

예시:

```
feat(auth): implement JWT-based authentication

- Issue access and refresh tokens
- Store refresh tokens in Redis
- Add token renewal API endpoint

Closes #123
```

#### 자주 하는 실수

```bash
# ❌ 타입 누락
git commit -m "bug fix"

# ❌ 모호한 설명
git commit -m "fix: fix issue"

# ❌ 한 커밋에 여러 작업
git commit -m "feat: implement login, signup, and password reset"

# ✅ 명확하고 단일 책임
git commit -m "feat: add form validation to login page"
```

### 커밋 메시지 작성 가이드라인

1. **첫 줄은 50자 이내** - 간결한 요약
2. **현재형 사용** - "added" (X) → "add" (O)
3. **명령형 어조** - "adds" (X) → "add" (O)
4. **첫 글자 소문자** - `Feat:` (X) → `feat:` (O)
5. **마침표 금지** - `feat: add feature.` (X) → `feat: add feature` (O)
6. **본문은 72자마다 줄바꿈** - 가독성 향상
7. **Why > What** - 변경한 내용보다 변경한 이유를 설명
8. **영어로 작성** - 릴리즈 노트 생성 도구와의 호환성을 위해

## GitHub Flow 워크플로우

### 브랜치 전략

```
main (항상 배포 가능한 상태)
├── feature/login-form
├── fix/payment-error
└── refactor/user-service
```

#### 기본 브랜치

새 저장소 생성 시 기본 브랜치는 `main`을 사용한다 (과거의 `master` 대신):

```bash
# 새 저장소 초기화 시 main 브랜치로 시작
git init -b main

# 또는 기존 저장소에서 기본 브랜치 변경
git branch -m master main
git push -u origin main

# Git 전역 설정 (모든 새 저장소에 적용)
git config --global init.defaultBranch main
```

**참고**: GitHub, GitLab, Bitbucket 등 대부분의 Git 호스팅 서비스는 2020년부터 기본 브랜치를 `main`으로 사용한다.

#### 브랜치 네이밍

```bash
# 형식: <type>/<description>
feature/user-authentication
fix/header-layout-bug
refactor/payment-module
docs/api-documentation
test/user-service
chore/update-dependencies
```

### 작업 흐름

```bash
# 1. main에서 최신 상태 받기
git switch main
git pull origin main

# 2. 새 브랜치 생성
git switch -c feature/dark-mode

# 3. 작업 후 커밋
git add .
git commit -m "feat: add dark mode toggle button"

# 4. 원격 브랜치에 푸시
git push origin feature/dark-mode

# 5. GitHub에서 PR 생성
gh pr create --title "feat: add dark mode support" --body "..."

# 6. 코드 리뷰 후 main에 병합 (GitHub UI 또는 CLI)
gh pr merge <PR번호> --squash  # 또는 --merge, --rebase

# 7. 로컬 main 업데이트 및 브랜치 삭제
git switch main
git pull origin main
git branch -d feature/dark-mode
```

### PR 병합 전략

| 전략       | 설명                            | 언제 사용                    |
| ---------- | ------------------------------- | ---------------------------- |
| **Squash** | 모든 커밋을 하나로 합침         | 기능 브랜치 (권장)           |
| **Merge**  | 병합 커밋 생성, 히스토리 보존   | 릴리스 브랜치                |
| **Rebase** | 선형 히스토리 유지, 병합 커밋 X | 간단한 변경, 깔끔한 히스토리 |

```bash
# Squash (권장 - 기능 단위로 커밋 정리)
gh pr merge 123 --squash

# Merge (히스토리 보존)
gh pr merge 123 --merge

# Rebase (선형 히스토리)
gh pr merge 123 --rebase
```

## Git 히스토리 관리

### Rebase

#### Interactive Rebase (커밋 정리)

```bash
# 최근 3개 커밋 수정
git rebase -i HEAD~3

# 에디터에서 명령어 선택
# pick   → 커밋 유지
# reword → 커밋 메시지 수정
# edit   → 커밋 수정
# squash → 이전 커밋에 합침
# fixup  → 이전 커밋에 합침 (메시지 제거)
# drop   → 커밋 삭제
```

예시:

```bash
# Before
pick a1b2c3d feat: implement login feature
pick d4e5f6g fix: typo in variable name
pick g7h8i9j fix: rename variable for clarity

# After (squash 사용)
pick a1b2c3d feat: implement login feature
fixup d4e5f6g fix: typo in variable name
fixup g7h8i9j fix: rename variable for clarity
```

#### Rebase onto main (브랜치 최신화)

```bash
# 1. main 최신화
git switch main
git pull origin main

# 2. feature 브랜치를 main 위로 rebase
git switch feature/my-feature
git rebase main

# 3. 충돌 발생 시
# - 파일 수정 후
git add .
git rebase --continue

# - rebase 취소하고 싶다면
git rebase --abort
```

### Cherry-pick (특정 커밋만 가져오기)

```bash
# 다른 브랜치의 커밋 하나만 적용
git cherry-pick <commit-hash>

# 여러 커밋 적용
git cherry-pick <commit-hash1> <commit-hash2>

# 충돌 발생 시
git add .
git cherry-pick --continue
```

### Commit Amend (마지막 커밋 수정)

```bash
# 마지막 커밋 메시지만 수정
git commit --amend -m "fix: correct commit message"

# 마지막 커밋에 파일 추가
git add forgotten-file.ts
git commit --amend --no-edit

# ⚠️ 주의: 이미 push한 커밋은 amend 금지 (히스토리 변경됨)
```

### Reset vs Revert

```bash
# Reset - 커밋 취소 (히스토리 삭제)
git reset --soft HEAD~1   # 커밋만 취소, 변경사항 유지
git reset --mixed HEAD~1  # 커밋 + staging 취소, 변경사항 유지 (기본값)
git reset --hard HEAD~1   # 커밋 + 변경사항 모두 삭제 (위험!)

# ⚠️ push한 커밋은 reset 금지 → revert 사용

# Revert - 커밋을 되돌리는 새 커밋 생성 (히스토리 보존)
git revert <commit-hash>
git revert HEAD  # 마지막 커밋 되돌리기
```

## Merge Conflict 해결

### Conflict 발생 시나리오

```bash
# main을 merge하거나 rebase할 때 충돌 발생
git merge main
# 또는
git rebase main

# Auto-merging src/index.ts
# CONFLICT (content): Merge conflict in src/index.ts
```

### Conflict 해결 과정

```bash
# 1. 충돌 파일 확인
git status

# 2. 파일 열어서 수동 수정
# <<<<<<< HEAD (현재 브랜치)
# 내 변경사항
# =======
# 상대 브랜치의 변경사항
# >>>>>>> main

# 3. 마커 제거하고 코드 수정
# 4. 해결된 파일 staging
git add src/index.ts

# 5. Merge 완료
git merge --continue
# 또는 Rebase 계속
git rebase --continue
```

### Conflict 해결 전략

```bash
# 현재 브랜치 변경사항 우선
git restore --ours <file>

# 상대 브랜치 변경사항 우선
git restore --theirs <file>

# merge 취소
git merge --abort

# rebase 취소
git rebase --abort
```

## 자주 사용하는 명령어

### 브랜치 작업 (git switch)

```bash
# 기존 브랜치로 전환
git switch main
git switch feature/my-feature

# 새 브랜치 생성 + 전환
git switch -c feature/new-feature

# 이전 브랜치로 돌아가기
git switch -

# 원격 브랜치 추적하며 전환
git switch -c local-branch origin/remote-branch
```

**참고**: Git 2.23+ (2019년 8월)부터 `git switch`를 사용한다. 기존 `git checkout`은 브랜치 전환, 파일 복원 등 여러 역할을 담당해 혼란을 야기했다. `git switch`는 브랜치 전환만 담당한다.

### 파일 복원 (git restore)

```bash
# 작업 디렉토리 파일 복원 (unstaged 변경사항 취소)
git restore <file>

# Staging 취소 (unstaged로 되돌림)
git restore --staged <file>

# 작업 디렉토리 + Staging 모두 복원
git restore --staged --worktree <file>

# 특정 커밋의 파일로 복원
git restore --source=<commit-hash> <file>
```

**참고**: `git restore`는 파일 복원 전용 명령어다. 기존 `git checkout -- <file>`을 대체한다.

### 상태 확인

```bash
git status              # 변경사항 확인
git log --oneline       # 커밋 히스토리 (한 줄)
git log --graph         # 브랜치 그래프
git diff                # 변경 내용 확인
git diff --staged       # staging된 변경 내용
git show <commit-hash>  # 특정 커밋 상세보기
```

### Stash (임시 저장)

```bash
git stash               # 현재 작업 임시 저장
git stash list          # 저장된 stash 목록
git stash pop           # 마지막 stash 적용 + 삭제
git stash apply         # 마지막 stash 적용 (유지)
git stash drop          # 마지막 stash 삭제
git stash clear         # 모든 stash 삭제
```

### 원격 저장소

```bash
git remote -v           # 원격 저장소 확인
git fetch origin        # 원격 변경사항 가져오기 (병합 X)
git pull origin main    # 원격 변경사항 가져오기 + 병합
git push origin main    # 로컬 변경사항 푸시
git push -f origin main # 강제 푸시 (⚠️ 위험 - 팀 작업 시 금지)
```

## 보안 및 주의사항

### 절대 커밋하면 안 되는 파일

```bash
# .gitignore에 추가
.env                    # 환경 변수 (API 키, 비밀번호)
.env.local
*.key                   # 인증서 키
*.pem
secrets/                # 시크릿 디렉토리
node_modules/           # 의존성 (package.json으로 관리)
dist/                   # 빌드 결과물
.DS_Store               # macOS 시스템 파일
```

### 실수로 커밋한 시크릿 제거

```bash
# ⚠️ 히스토리에서 완전 삭제 (git filter-branch 대신 BFG 사용)
brew install bfg
bfg --delete-files .env
git reflog expire --expire=now --all && git gc --prune=now --aggressive

# ⚠️ 주의: 이미 푸시했다면 시크릿 즉시 폐기 후 재발급 필수
```

### Force Push 금지 (공유 브랜치)

```bash
# ❌ main/develop에 force push 절대 금지
git push -f origin main

# ✅ 개인 feature 브랜치에서만 허용
git push -f origin feature/my-branch
```

## GitHub CLI 활용

```bash
# PR 생성
gh pr create --title "feat: add new feature" --body "Description..."

# PR 목록 확인
gh pr list

# PR 상세보기
gh pr view 123

# PR 체크아웃 (로컬에서 테스트)
gh pr checkout 123

# PR 병합
gh pr merge 123 --squash

# Issue 생성
gh issue create --title "Bug found" --body "Description..."
```

## 추가 학습 자료

- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Pro Git Book (한글)](https://git-scm.com/book/ko/v2)
