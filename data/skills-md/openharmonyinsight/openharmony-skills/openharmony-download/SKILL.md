---
name: openharmony-download
description: Interactive OpenHarmony source code download with mirror selection (GitCode/Gitee/GitHub), environment checking, branch selection, and real-time progress. Use when user requests:"下载 OpenHarmony", "download OpenHarmony", "下载源码", "获取源码", "拉取代码", "clone openharmony", or "repo init".
---

# OpenHarmony Download Skill

OpenHarmony 源码下载 Skill - 对话式信息收集 + 环境检查 + 前台实时下载。

## 工作流程

1. **选择镜像源**（AskUserQuestion 单选）
2. **环境检查**（逐项对话式检查，失败时引导解决）
3. **选择分支**（AskUserQuestion 单选）
4. **选择目录**（AskUserQuestion 单选）
5. **执行下载**（Bash 工具，前台实时输出）

## 对话流程

### 步骤 1：选择镜像源

```javascript
AskUserQuestion({
  questions: [{
    header: "镜像源",
    question: "请选择 OpenHarmony 镜像源",
    options: [
      { label: "GitCode", description: "推荐国内用户，速度最快" },
      { label: "Gitee", description: "国内用户" },
      { label: "GitHub", description: "国际用户" }
    ],
    multiSelect: false
  }]
})
```

### 步骤 2：环境检查

镜像源选择后，使用 Bash 工具逐项检查环境：

```javascript
Bash({ command: "bash scripts/check_env.sh git", description: "Check git installation" })
Bash({ command: "bash scripts/check_env.sh git-lfs", description: "Check git-lfs installation" })
Bash({ command: "bash scripts/check_env.sh python3", description: "Check python3 installation" })
Bash({ command: "bash scripts/check_env.sh curl", description: "Check curl installation" })
Bash({ command: "bash scripts/check_env.sh repo", description: "Check repo installation" })
Bash({ command: "bash scripts/check_env.sh git-config", description: "Check git configuration" })
Bash({ command: "bash scripts/check_env.sh disk-space", description: "Check available disk space" })
```

**检查失败时**：显示错误 + 提供安装命令 + 等待用户修复 + 重新检查

**常用安装命令**：
- git: `sudo apt-get install git` (Ubuntu/Debian)
- git-lfs: `sudo apt-get install git-lfs && git lfs install`
- repo: 见脚本输出的安装指引
- Git 配置: `git config --global user.name "Your Name" && git config --global user.email "your-email@example.com"`

### 步骤 3：选择分支

```javascript
AskUserQuestion({
  questions: [{
    header: "分支",
    question: "请选择 OpenHarmony 分支",
    options: [
      { label: "master", description: "主分支（最新开发代码）" },
      { label: "OpenHarmony-5.1.0-Release", description: "5.1.0 版本" },
      { label: "OpenHarmony-5.0.3-Release", description: "5.0.3 版本" },
      { label: "OpenHarmony-5.0.2-Release", description: "5.0.2 版本" },
      { label: "OpenHarmony-5.0.1-Release", description: "5.0.1 版本" },
      { label: "OpenHarmony-4.1-Release", description: "4.1 版本" },
      { label: "自定义分支", description: "输入自定义分支名" }
    ],
    multiSelect: false
  }]
})
```

### 步骤 4：选择目录

```javascript
AskUserQuestion({
  questions: [{
    header: "目录",
    question: "请选择下载目录",
    options: [
      { label: "默认位置", description: "~/OpenHarmony/[branch]/" },
      { label: "自定义路径", description: "指定其他位置" }
    ],
    multiSelect: false
  }]
})
```

### 步骤 5：确认并执行下载

显示配置摘要，使用 **AskUserQuestion** 确认是否开始：

```javascript
// 显示配置摘要
Claude: 好的，准备下载 OpenHarmony 源码：

配置摘要:
- 镜像源: ${MIRROR}
- 分支: ${BRANCH}
- 目录: ${DOWNLOAD_DIR}
- 并行任务: CPU核心数/4（自动计算）

下载将在前台运行，进度实时显示。
这将需要 30 分钟到数小时。

AskUserQuestion({
  questions: [{
    header: "确认",
    question: "是否开始下载？",
    options: [
      { label: "开始下载", description: "立即开始下载 OpenHarmony 源码" },
      { label: "返回重新配置", description: "返回步骤1，重新选择配置" }
    ],
    multiSelect: false
  }]
})
```

**如果选择"开始下载"**：

使用 Bash 工具执行下载脚本，传入用户选择的镜像源、分支和目录参数：

```javascript
Bash({
  command: `bash scripts/download_openharmony.sh -m ${MIRROR} -b ${BRANCH} ${CUSTOM_DIR ? `-d ${CUSTOM_DIR}` : ''}`,
  description: `Download OpenHarmony ${BRANCH} from ${MIRROR}`
})
```

下载将在前台运行，进度实时显示。

**如果选择"返回重新配置"**：
返回步骤1，重新选择镜像源、分支、目录。

## 脚本说明

### download_openharmony.sh

```bash
必需参数:
  -m MIRROR    镜像源（gitcode|gitee|github）
  -b BRANCH    分支名

可选参数:
  -d DIR       下载目录（绝对路径）
  -j JOBS      并行任务数（默认: CPU核心数/4）
```

### check_env.sh

```bash
用法: check_env.sh <check_type>

检查类型: git | git-lfs | python3 | curl | repo | git-config | disk-space | all
```

### verify_download.sh

自动验证下载完整性（下载脚本自动调用）：
- 目录结构检查
- foundation 子系统检查
- ACE Engine 组件检查
- 关键文件检查
- repo 状态检查
- 仓库完整性验证

## 验证结果处理

### 验证通过
```
✓ 验证通过！OpenHarmony 源码完整。

后续步骤:
1. 配置编译环境
2. 全量编译代码: ./build.sh --ccache --product-name rk3568
```

### 验证失败
```
✗ 验证发现问题

建议:
1. 同步缺失仓库: repo sync -c
2. 拉取 LFS 文件: repo forall -c 'git lfs pull'
3. 检查网络连接
```
