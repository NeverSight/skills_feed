---
name: gitlab-cli
description: This skill should be used when users need to interact with GitLab via the glab CLI. It covers repository management (create, delete, clone, fork), CI/CD workflows (pipelines, jobs, schedules), Merge Requests, Issues, Releases, and other GitLab operations. Triggers on requests mentioning GitLab, repos, MRs, issues, pipelines, or CI/CD workflows.
---

# GitLab CLI 管理技能

通过 glab CLI 管理 GitLab 代码仓库、CI/CD Pipeline、Merge Request、Issue 等资源。

## 环境配置

- **GitLab 服务器**: `192.168.10.117:6001`
- **Web UI**: `http://192.168.10.117:6001`
- **SSH 端口**: 2222
- **API 协议**: HTTP
- **Git 协议**: SSH

验证连接状态：
```bash
glab auth status
```

## 核心功能

### 1. 仓库管理

**列出项目**
```bash
glab repo list                           # 列出所有项目
glab repo list --per-page 50             # 分页列出
glab repo search "keyword"               # 搜索项目
```

**创建项目**
```bash
glab repo create my-project              # 在当前用户下创建
glab repo create my-project --group simplexai  # 在 group 下创建
glab repo create my-project --private    # 创建私有项目
```

**其他操作**
```bash
glab repo view                           # 查看当前项目
glab repo view --web                     # 浏览器打开
glab repo clone simplexai/project        # 克隆项目
glab repo clone -g simplexai             # 克隆整个 group
glab repo delete my-project --yes        # 删除项目
```

### 2. CI/CD 管理

**Pipeline 操作**
```bash
glab ci status                           # 当前分支 pipeline 状态
glab ci list                             # 列出所有 pipeline
glab ci run                              # 运行新 pipeline
glab ci run --branch main                # 指定分支运行
glab ci run --variables "KEY:value"      # 带变量运行
glab ci cancel                           # 取消运行中的 pipeline
glab ci delete <pipeline-id>             # 删除 pipeline
```

**Job 操作**
```bash
glab ci trace                            # 查看 job 日志
glab ci trace <job-id>                   # 实时跟踪指定 job
glab ci retry <job-id>                   # 重试失败的 job
glab ci trigger <job-id>                 # 触发手动 job
glab ci artifact <ref> <job-name>        # 下载 artifacts
```

**CI 配置验证**
```bash
glab ci lint                             # 验证 .gitlab-ci.yml
```

### 3. Merge Request 管理

**创建 MR**
```bash
glab mr create                           # 交互式创建
glab mr create --fill                    # 自动填充
glab mr create --draft                   # 创建草稿
glab mr create --title "feat: xxx" --target-branch main
```

**列出和查看**
```bash
glab mr list                             # 列出打开的 MR
glab mr list --state all                 # 所有状态
glab mr view <id>                        # 查看详情
glab mr diff <id>                        # 查看 diff
```

**审核和合并**
```bash
glab mr approve <id>                     # 批准
glab mr merge <id>                       # 合并
glab mr merge <id> --squash              # Squash 合并
glab mr merge <id> --remove-source-branch
```

**其他操作**
```bash
glab mr note <id> -m "comment"           # 添加评论
glab mr checkout <id>                    # Checkout 到本地
glab mr close <id>                       # 关闭
glab mr reopen <id>                      # 重新打开
```

### 4. Issue 管理

```bash
glab issue create --title "Bug: xxx"     # 创建 issue
glab issue list                          # 列出 issue
glab issue list --label "bug"            # 按标签筛选
glab issue view <id>                     # 查看详情
glab issue note <id> -m "comment"        # 添加评论
glab issue close <id>                    # 关闭
glab issue update <id> --add-label "in-progress"
```

### 5. 变量管理

```bash
glab variable list                       # 列出变量
glab variable get MY_VAR                 # 获取变量值
glab variable set MY_VAR "value"         # 设置变量
glab variable set MY_VAR "value" --protected --masked
glab variable delete MY_VAR              # 删除变量
glab variable export                     # 导出所有变量
glab variable list --group simplexai     # Group 变量
```

### 6. Release 管理

```bash
glab release list                        # 列出 releases
glab release create v1.0.0 --notes "Release notes"
glab release view v1.0.0                 # 查看 release
glab release delete v1.0.0               # 删除 release
```

## 跨项目操作

使用 `-R` 参数指定项目：
```bash
glab mr list -R simplexai/other-project
glab ci run -R simplexai/other-project --branch main
glab issue list -R simplexai/other-project
```

## 批量操作脚本

技能提供以下批量操作脚本，位于 `scripts/` 目录：

### 批量触发 Pipeline
```bash
scripts/batch_pipeline.sh main simplexai/api simplexai/front
```

### 查看多项目 Pipeline 状态
```bash
scripts/pipeline_status.sh                    # 所有项目
scripts/pipeline_status.sh simplexai/api simplexai/front
```

### 导出变量
```bash
scripts/export_variables.sh --repo simplexai/api vars.env
scripts/export_variables.sh --group simplexai group_vars.env
```

### MR 概览
```bash
scripts/mr_overview.sh --state opened
```

## API 直接调用

对于 glab 未覆盖的功能，使用 API 直接调用：
```bash
glab api projects                        # 获取项目列表
glab api projects/simplexai%2Fapi        # 获取指定项目 (URL 编码)
glab api projects --method POST --field name=new-project
glab api projects --paginate             # 分页获取所有结果
```

## 参考文档

详细命令说明请查阅 `references/commands.md`。
