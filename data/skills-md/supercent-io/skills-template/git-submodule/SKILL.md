---
name: git-submodule
description: Manage Git submodules for including external repositories within a main repository. Use when working with external libraries, shared modules, or managing dependencies as separate Git repositories.
tags: [git, submodule, dependencies, version-control, modular]
platforms: [Claude, ChatGPT, Gemini]
---

# Git Submodule

## When to use this skill
- Including external Git repositories within your main project
- Managing shared libraries or modules across multiple projects
- Locking external dependencies to specific versions
- Working with monorepo-style architectures with independent components
- Cloning repositories that contain submodules
- Updating submodules to newer versions
- Removing submodules from a project

## Instructions

### Step 1: Understanding submodules

Git submodule은 메인 Git 저장소 내에 다른 Git 저장소를 포함시키는 기능입니다.

**Key concepts**:
- 서브모듈은 특정 커밋을 참조하여 버전을 고정합니다
- `.gitmodules` 파일에 서브모듈 경로와 URL이 기록됩니다
- 서브모듈 내 변경은 별도 커밋으로 관리됩니다

### Step 2: Adding submodules

**기본 추가**:
```bash
# 서브모듈 추가
git submodule add <repository-url> <path>

# 예: libs/lib 경로에 라이브러리 추가
git submodule add https://github.com/example/lib.git libs/lib
```

**특정 브랜치 추적**:
```bash
# 특정 브랜치를 추적하도록 추가
git submodule add -b main https://github.com/example/lib.git libs/lib
```

**추가 후 커밋**:
```bash
git add .gitmodules libs/lib
git commit -m "feat: add lib as submodule"
```

### Step 3: Cloning with submodules

**신규 클론 시**:
```bash
# 방법 1: 클론 시 --recursive 옵션
git clone --recursive <repository-url>

# 방법 2: 클론 후 초기화
git clone <repository-url>
cd <repository>
git submodule init
git submodule update
```

**한 줄로 초기화 및 업데이트**:
```bash
git submodule update --init --recursive
```

### Step 4: Updating submodules

**원격 최신 버전으로 업데이트**:
```bash
# 모든 서브모듈을 원격 최신으로 업데이트
git submodule update --remote

# 특정 서브모듈만 업데이트
git submodule update --remote libs/lib

# 업데이트 + 머지
git submodule update --remote --merge

# 업데이트 + 리베이스
git submodule update --remote --rebase
```

**서브모듈 참조 커밋으로 체크아웃**:
```bash
# 메인 저장소가 참조하는 커밋으로 서브모듈 체크아웃
git submodule update
```

### Step 5: Working inside submodules

**서브모듈 내에서 작업**:
```bash
# 서브모듈 디렉토리로 이동
cd libs/lib

# 브랜치 체크아웃 (detached HEAD 해제)
git checkout main

# 변경사항 작업
# ... make changes ...

# 서브모듈 내에서 커밋 및 푸시
git add .
git commit -m "feat: update library"
git push origin main
```

**메인 저장소에서 서브모듈 변경 반영**:
```bash
# 메인 저장소로 이동
cd ..

# 서브모듈 참조 업데이트
git add libs/lib
git commit -m "chore: update lib submodule reference"
git push
```

### Step 6: Batch operations

**모든 서브모듈에 명령 실행**:
```bash
# 모든 서브모듈에서 pull
git submodule foreach 'git pull origin main'

# 모든 서브모듈에서 상태 확인
git submodule foreach 'git status'

# 모든 서브모듈에서 브랜치 체크아웃
git submodule foreach 'git checkout main'

# 중첩된 서브모듈에도 명령 실행
git submodule foreach --recursive 'git fetch origin'
```

### Step 7: Removing submodules

**서브모듈 완전 제거**:
```bash
# 1. 서브모듈 등록 해제
git submodule deinit <path>

# 2. Git에서 제거
git rm <path>

# 3. .git/modules에서 캐시 제거
rm -rf .git/modules/<path>

# 4. 변경사항 커밋
git commit -m "chore: remove submodule"
```

**예시: libs/lib 제거**:
```bash
git submodule deinit libs/lib
git rm libs/lib
rm -rf .git/modules/libs/lib
git commit -m "chore: remove lib submodule"
git push
```

### Step 8: Checking submodule status

**상태 확인**:
```bash
# 서브모듈 상태 확인
git submodule status

# 상세 상태 (재귀적)
git submodule status --recursive

# 요약 정보
git submodule summary
```

**출력 해석**:
```
 44d7d1... libs/lib (v1.0.0)      # 정상 (참조 커밋과 일치)
+44d7d1... libs/lib (v1.0.0-1-g...)  # 로컬 변경 있음
-44d7d1... libs/lib               # 초기화 안 됨
```

## Examples

### Example 1: 프로젝트에 외부 라이브러리 추가

```bash
# 1. 서브모듈 추가
git submodule add https://github.com/lodash/lodash.git vendor/lodash

# 2. 특정 버전(태그)으로 고정
cd vendor/lodash
git checkout v4.17.21
cd ../..

# 3. 변경사항 커밋
git add .
git commit -m "feat: add lodash v4.17.21 as submodule"

# 4. 푸시
git push origin main
```

### Example 2: 서브모듈 포함 저장소 클론 후 설정

```bash
# 1. 저장소 클론
git clone https://github.com/myorg/myproject.git
cd myproject

# 2. 서브모듈 초기화 및 업데이트
git submodule update --init --recursive

# 3. 서브모듈 상태 확인
git submodule status

# 4. 서브모듈 브랜치 체크아웃 (개발 시)
git submodule foreach 'git checkout main || git checkout master'
```

### Example 3: 서브모듈을 최신 버전으로 업데이트

```bash
# 1. 모든 서브모듈을 원격 최신으로 업데이트
git submodule update --remote --merge

# 2. 변경사항 확인
git diff --submodule

# 3. 변경사항 커밋
git add .
git commit -m "chore: update all submodules to latest"

# 4. 푸시
git push origin main
```

### Example 4: 공유 컴포넌트를 여러 프로젝트에서 사용

```bash
# 프로젝트 A에서
git submodule add https://github.com/myorg/shared-components.git src/shared

# 프로젝트 B에서
git submodule add https://github.com/myorg/shared-components.git src/shared

# 공유 컴포넌트 업데이트 시 (각 프로젝트에서)
git submodule update --remote src/shared
git add src/shared
git commit -m "chore: update shared-components"
```

### Example 5: CI/CD에서 서브모듈 처리

```yaml
# GitHub Actions
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive  # 또는 'true'

# GitLab CI
variables:
  GIT_SUBMODULE_STRATEGY: recursive

# Jenkins
checkout scm: [
  $class: 'SubmoduleOption',
  recursiveSubmodules: true
]
```

## Advanced workflows

### 중첩 서브모듈 (Nested submodules)

```bash
# 중첩된 모든 서브모듈 초기화
git submodule update --init --recursive

# 중첩된 모든 서브모듈 업데이트
git submodule update --remote --recursive
```

### 서브모듈 URL 변경

```bash
# .gitmodules 파일 수정
git config -f .gitmodules submodule.libs/lib.url https://new-url.git

# 로컬 설정 동기화
git submodule sync

# 서브모듈 업데이트
git submodule update --init --recursive
```

### 서브모듈을 일반 디렉토리로 변환

```bash
# 1. 서브모듈 내용 백업
cp -r libs/lib libs/lib-backup

# 2. 서브모듈 제거
git submodule deinit libs/lib
git rm libs/lib
rm -rf .git/modules/libs/lib

# 3. 백업 복원 (.git 제외)
rm -rf libs/lib-backup/.git
mv libs/lib-backup libs/lib

# 4. 일반 파일로 추가
git add libs/lib
git commit -m "chore: convert submodule to regular directory"
```

### shallow 클론으로 공간 절약

```bash
# 얕은 클론으로 서브모듈 추가
git submodule add --depth 1 https://github.com/large/repo.git libs/large

# 기존 서브모듈을 얕은 클론으로 업데이트
git submodule update --init --depth 1
```

## Best practices

1. **버전 고정**: 서브모듈은 항상 특정 커밋/태그로 고정하여 재현 가능성 확보
2. **문서화**: README에 서브모듈 초기화 방법 명시
3. **CI 설정**: CI/CD 파이프라인에서 `--recursive` 옵션 사용
4. **정기 업데이트**: 보안 패치 등을 위해 정기적으로 서브모듈 업데이트
5. **브랜치 추적**: 개발 중에는 브랜치 추적 설정으로 편의성 확보
6. **권한 관리**: 서브모듈 저장소 접근 권한 확인
7. **얕은 클론**: 대용량 저장소는 `--depth` 옵션으로 공간 절약
8. **상태 확인**: 커밋 전 `git submodule status`로 상태 확인

## Common pitfalls

- **detached HEAD**: 서브모듈은 기본적으로 detached HEAD 상태. 작업 시 브랜치 체크아웃 필요
- **초기화 누락**: 클론 후 `git submodule update --init` 필수
- **참조 불일치**: 서브모듈 변경 후 메인 저장소에서 참조 업데이트 필요
- **권한 문제**: 비공개 서브모듈은 SSH 키 또는 토큰 설정 필요
- **상대 경로**: `.gitmodules`의 상대 경로 사용 시 포크에서 문제 발생 가능
- **삭제 불완전**: 서브모듈 제거 시 `.git/modules` 캐시도 삭제 필요

## Troubleshooting

### 서브모듈이 초기화되지 않음

```bash
# 강제 초기화
git submodule update --init --force
```

### 서브모듈 충돌

```bash
# 서브모듈 상태 확인
git submodule status

# 충돌 해결 후 원하는 커밋으로 체크아웃
cd libs/lib
git checkout <desired-commit>
cd ..
git add libs/lib
git commit -m "fix: resolve submodule conflict"
```

### 권한 오류 (private repository)

```bash
# SSH URL 사용
git config -f .gitmodules submodule.libs/lib.url git@github.com:org/private-lib.git
git submodule sync
git submodule update --init
```

### 서브모듈 dirty 상태

```bash
# 서브모듈 내 변경사항 확인
cd libs/lib
git status
git diff

# 변경사항 버리기
git checkout .
git clean -fd

# 또는 커밋하기
git add .
git commit -m "fix: resolve changes"
git push
```

## Configuration

### 유용한 설정

```bash
# diff에서 서브모듈 변경 표시
git config --global diff.submodule log

# status에서 서브모듈 요약 표시
git config --global status.submoduleSummary true

# push 시 서브모듈 변경 확인
git config --global push.recurseSubmodules check

# fetch 시 서브모듈도 함께 fetch
git config --global fetch.recurseSubmodules on-demand
```

### .gitmodules 예시

```ini
[submodule "libs/lib"]
    path = libs/lib
    url = https://github.com/example/lib.git
    branch = main

[submodule "vendor/tool"]
    path = vendor/tool
    url = git@github.com:example/tool.git
    shallow = true
```

## References

- [Git Submodules - Official Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [Git Submodule Tutorial - Atlassian](https://www.atlassian.com/git/tutorials/git-submodule)
- [Managing Dependencies with Submodules](https://github.blog/2016-02-01-working-with-submodules/)
- [Git Submodule Cheat Sheet](https://gist.github.com/gitaarik/8735255)
