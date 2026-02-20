---
name: system-info
description: 系统信息查询技能。用于获取电脑硬件信息、系统状态、进程列表、磁盘空间等。当用户询问电脑配置、系统状态或性能信息时使用。
version: 1.0.0
author: Naga Team
tags:
  - system
  - hardware
  - status
enabled: true
---

# 系统信息查询技能

本技能提供系统信息查询和状态监控能力。

## 可查询的信息

### 1. 硬件信息
- CPU 型号和核心数
- 内存容量和使用率
- 磁盘空间和分区
- 显卡信息

### 2. 系统状态
- 操作系统版本
- 系统运行时间
- 当前用户
- 网络状态

### 3. 进程监控
- 运行中的进程
- CPU 占用排行
- 内存占用排行

## 查询命令

### macOS/Linux
```bash
# CPU 信息
sysctl -n machdep.cpu.brand_string  # macOS
lscpu  # Linux

# 内存信息
vm_stat  # macOS
free -h  # Linux

# 磁盘空间
df -h

# 系统信息
uname -a
sw_vers  # macOS
```

### 通用 Python 方法
```python
import platform
import psutil

# 系统信息
platform.system()
platform.release()
platform.machine()

# 资源使用
psutil.cpu_percent()
psutil.virtual_memory()
psutil.disk_usage('/')
```

## 输出格式

```markdown
## 系统信息报告

### 操作系统
- 系统: macOS 14.0
- 架构: arm64

### 硬件配置
- CPU: Apple M2 Pro (12核)
- 内存: 32GB (已用 60%)
- 磁盘: 500GB (剩余 200GB)

### 当前状态
- 运行时间: 5天 12小时
- CPU 负载: 15%
- 活跃进程: 256个
```
