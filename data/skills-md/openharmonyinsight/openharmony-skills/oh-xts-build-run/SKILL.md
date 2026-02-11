---
name: oh-xts-build-run
description: OpenHarmony XTS 编译和运行组合命令。一站式完成 XTS 测试项目的编译和运行。当用户需要执行完整的 XTS 测试流程时使用此 Skill： (1) 编译 XTS 测试项目生成 HAP 文件，(2) 运行 XTS 测试并展示结果。支持 --package 和 --api 参数传递给运行阶段。
---

# OpenHarmony XTS 编译和运行

此 Skill 将 XTS 编译 (`/oh-xts-build`) 和运行 (`/oh-xts-run`) 组合成一个完整的工作流。

## 工作流程

1. **执行编译**：运行 `/oh-xts-build`
   - 更新 List.test.ets 注册测试用例
   - 使用 hvigorw 编译生成 HAP 文件
   - 检查主 HAP 和测试 HAP 是否生成成功

2. **判断结果**：
   - 如果编译失败 → 停止流程，返回编译错误
   - 如果编译成功 → 继续执行运行

3. **执行运行**：运行 `/oh-xts-run [参数]`
   - 自动解析包名（从 pack.info 或 module.json5）
   - 运行测试并解析结果统计

4. **汇总结果**：统一展示编译和运行的完整输出

## 参数

- `--package=<package-name>`：指定包名（可选）
- `--api=<api-name>`：指定测试类名（可选）

## 实现位置

- 编译命令：`packages/cli/src/ui/commands/ohXtsBuildCommand.ts`
- 运行命令：`packages/cli/src/ui/commands/ohXtsRunCommand.ts`
- 核心模块：`packages/cli/src/modules/xts/build-runner.ts`
