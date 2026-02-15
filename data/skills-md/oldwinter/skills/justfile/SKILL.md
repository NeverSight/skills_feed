---
name: justfile
description: This skill should be used when users want to create, convert, or manage Justfiles for command automation. It handles converting Makefile, npm scripts, or shell commands to Justfile format, generating project-specific templates, and providing Justfile syntax guidance. Triggers on requests mentioning justfile, just command, command runner, Makefile conversion, or task automation.
---

# Justfile 命令自动化技能

将常用命令、Makefile、npm scripts 转换为 Justfile，便于日常开发和运维工作。

## 快速开始

### 安装 just

```bash
# macOS
brew install just

# Linux
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash

# 验证安装
just --version
```

### 基本使用

```bash
just              # 运行默认 recipe
just --list       # 列出所有 recipes
just <recipe>     # 运行指定 recipe
just -n <recipe>  # 干运行（只显示命令）
```

## 工作流程决策

根据用户需求选择合适的工作流程：

```
用户需求
├── 已有 Makefile → 转换工作流
├── 已有 package.json → npm 转换工作流
├── 有常用 shell 命令 → 命令整理工作流
├── 新项目需要自动化 → 模板生成工作流
└── 需要了解语法 → 查阅 references/syntax.md
```

## 1. Makefile 转换

将现有 Makefile 转换为 Justfile。

**自动转换**
```bash
python scripts/makefile_to_just.py Makefile justfile
```

**手动转换要点**
- 移除 `.PHONY` 声明（just 默认都是 phony）
- `$(VAR)` → `{{var}}`
- `$(shell cmd)` → `` `cmd` ``
- 保持 `@` 前缀（静默执行）
- 文件依赖需要移除或改为 recipe 依赖

**转换示例**
```makefile
# Makefile
.PHONY: build test
VERSION := $(shell git describe --tags)

build:
	go build -ldflags "-X main.version=$(VERSION)"

test: build
	go test ./...
```

转换为：
```just
# justfile
version := `git describe --tags`

build:
    go build -ldflags "-X main.version={{version}}"

test: build
    go test ./...
```

## 2. npm scripts 转换

将 package.json 中的 scripts 转换为 Justfile。

**自动转换**
```bash
python scripts/npm_to_just.py package.json justfile
```

**转换示例**
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest",
    "lint": "eslint ."
  }
}
```

转换为：
```just
set dotenv-load

default: dev

dev:
    npm run dev

build:
    npm run build

test:
    npm run test

lint:
    npm run lint

# 或者直接使用原始命令
dev:
    vite

build:
    vite build
```

## 3. Shell 命令整理

将常用 shell 命令整理为 Justfile。

**从 history 提取**
```bash
python scripts/shell_to_just.py --history justfile
```

**从文件读取**
```bash
# 创建命令列表
cat > commands.txt << 'EOF'
docker-compose up -d
docker-compose logs -f
kubectl get pods -n production
kubectl logs -f deployment/api
EOF

python scripts/shell_to_just.py commands.txt justfile
```

**手动整理模式**

收集用户常用命令，按功能分组：

```just
# === Docker ===
up:
    docker-compose up -d

down:
    docker-compose down

logs service="":
    docker-compose logs -f {{service}}

# === Kubernetes ===
pods:
    kubectl get pods -n production

logs-k8s pod:
    kubectl logs -f {{pod}} -n production
```

## 4. 项目模板生成

根据项目类型生成合适的 Justfile 模板。

### 识别项目类型

检查项目文件来识别类型：

| 文件 | 项目类型 |
|------|----------|
| `requirements.txt`, `pyproject.toml` | Python |
| `package.json` | Node.js |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `docker-compose.yml` | Docker |
| `kubernetes/`, `k8s/` | Kubernetes |
| `terraform/` | Terraform |

### 生成模板

查阅 `references/templates.md` 获取各类项目的完整模板：

- Python 项目模板
- Node.js 项目模板
- Go 项目模板
- DevOps/运维模板
- 通用开发模板
- 数据科学/ML 模板

## 常用 Recipe 模式

### 带参数的 Recipe

```just
# 必需参数
deploy env:
    kubectl apply -k overlays/{{env}}

# 默认值参数
build mode="debug":
    cargo build --{{mode}}

# 可变参数
test *args:
    pytest {{args}}
```

### 依赖关系

```just
# 简单依赖
release: build test
    ./deploy.sh

# 带参数的依赖
push: (build "release")
    docker push myapp:latest
```

### 条件执行

```just
# 跨平台
[linux]
install:
    apt install mypackage

[macos]
install:
    brew install mypackage

# 确认提示
[confirm("确定要部署到生产环境吗?")]
deploy-prod:
    kubectl apply -k overlays/prod
```

### 分组

```just
[group('development')]
dev:
    npm run dev

[group('development')]
watch:
    npm run watch

[group('testing')]
test:
    npm run test
```

### 脚本模式

```just
[script]
setup:
    #!/usr/bin/env bash
    set -euo pipefail

    echo "Setting up environment..."
    for pkg in curl git make; do
        command -v $pkg || echo "Missing: $pkg"
    done
```

## 最佳实践

### 1. 文件组织

```just
# 头部：设置和变量
set dotenv-load
set shell := ["bash", "-cu"]

project := "myapp"
version := `git describe --tags --always`

# 默认 recipe
default: dev

# 按功能分组，用注释分隔
# === 开发 ===
dev: ...

# === 构建 ===
build: ...

# === 测试 ===
test: ...
```

### 2. 命名约定

- 使用小写字母和连字符：`build-prod`
- 动词开头：`run`, `build`, `test`, `deploy`
- 私有 recipe 用下划线：`_helper`

### 3. 文档注释

```just
# 启动开发服务器 (端口 3000)
dev:
    npm run dev
```

### 4. 变量使用

```just
# 从环境变量读取，带默认值
env := env("ENV", "development")

# 从命令获取
commit := `git rev-parse --short HEAD`

# 条件变量
mode := if env == "prod" { "release" } else { "debug" }
```

## 参考资料

- `references/syntax.md` - Justfile 完整语法参考
- `references/templates.md` - 各类项目模板集合
- `scripts/makefile_to_just.py` - Makefile 转换脚本
- `scripts/npm_to_just.py` - npm scripts 转换脚本
- `scripts/shell_to_just.py` - Shell 命令提取脚本
