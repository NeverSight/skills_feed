---
name: skill-launcher
description: 启动/重启 SkillLauncher 快捷启动器
triggers:
  - 启动launcher
  - 打开launcher
  - skill launcher
  - 启动skill启动器
  - 重启launcher
---

# SkillLauncher 启动器

启动或重启 SkillLauncher 进程。

## 路径说明

SkillLauncher 编译后的可执行文件位于项目目录下：
```
SkillLauncher/.build/release/SkillLauncher
```

执行前需要先确认当前目录下有 SkillLauncher 项目。

## 操作

1. **检查是否已运行**
   ```bash
   pgrep -x SkillLauncher
   ```

2. **启动**（如果没运行）
   ```bash
   nohup ./SkillLauncher/.build/release/SkillLauncher > /dev/null 2>&1 &
   ```

3. **重启**（先杀后启）
   ```bash
   pkill -x SkillLauncher
   sleep 0.5
   nohup ./SkillLauncher/.build/release/SkillLauncher > /dev/null 2>&1 &
   ```

4. **关闭**
   ```bash
   pkill -x SkillLauncher
   ```

## 用法

- "启动 launcher" → 启动进程
- "重启 launcher" → 重启进程
- "关闭 launcher" → 停止进程

## 注意

- 首次使用需要先编译：`cd SkillLauncher && swift build -c release`
- 首次运行需要授予「辅助功能」权限
- 使用 Option+Space 唤起窗口
