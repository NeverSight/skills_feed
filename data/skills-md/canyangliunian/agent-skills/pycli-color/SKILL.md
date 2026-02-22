---
name: pycli-color
description: Use when writing Python argparse CLI scripts that need colorful --help output with customizable color control (NO_COLOR/FORCE_COLOR support).
---

# pycli-color

## 何时使用

当用户要求你**编写 Python 命令行脚本（argparse）**，并希望 `-h/--help` 输出带统一配色高亮时，使用本技能。

目标是让所有脚本的 `--help` 输出呈现一致的视觉效果与可控的颜色开关策略（auto/NO_COLOR/FORCE_COLOR）。

## 核心规范（必须满足）

### 1) 机制（必须使用 argparse）

- 必须使用 `argparse`。
- 必须实现 `ColorHelpFormatter(argparse.HelpFormatter)`。
- 必须覆写 `_format_action_invocation(self, action)` 方法以控制每个 action 的 option/metavar 渲染。
- 通过 `ArgumentParser(formatter_class=ColorHelpFormatter)` 启用。

### 2) 颜色规则（token 级别）

- 任何以 `-` 开头的 option token（例如 `-h`, `--title`）必须 **青色 + 加粗**。
- 任何 metavar/占位符 token（通常满足 `p.isupper()` 或包含 `_`，例如 `TITLE`, `AJG_CSV`）必须 **黄色 + 加粗**。
- 其他 token 不着色。
- 每个被着色片段后必须追加 ANSI reset，避免串色。

推荐 ANSI：

- reset：`\x1b[0m`
- 青色加粗：`\x1b[36;1m`
- 黄色加粗：`\x1b[33;1m`

### 3) 颜色启用策略（可控且兼容）

必须实现：

- `supports_color() -> bool`
  - 默认 auto：仅当 `sys.stdout.isatty()` 为 True 且 `TERM` 不是 `dumb` 时启用颜色
  - 若环境变量 `NO_COLOR` **存在**：强制禁用颜色
  - 若 `FORCE_COLOR=1`：强制启用颜色（即便非 TTY）
- `colorize(text: str, ansi_code: str) -> str`：仅在启用颜色时加 ANSI。

注意：你的环境中常见 `NO_COLOR=1` 全局存在；若要强制彩色，请用 `FORCE_COLOR=1 python3 your_script.py -h` 直接强制启用（无需清空 NO_COLOR）。

### 4) 最小 CLI 面（用于校验）

脚本必须包含：

- 至少一个 `required=True` 参数
- 至少一个可选参数
- 至少一个带 `choices=` 的参数
- 标准入口：`if __name__ == "__main__": main()`

### 5) 测试注释（必须写入代码）

脚本中必须包含两条注释，方便手动验证：

- `NO_COLOR=1 python your_script.py -h`
- `FORCE_COLOR=1 python your_script.py -h`

## 推荐实现（可直接复制）

你可以直接参考项目内模板（相对路径）：

- `./scripts/demo_pycli_color.py`

## 给未来助手的“可复制提示词”

当你以后要求我写任何 Python CLI 脚本时，可直接粘贴下面这段（无需解释背景）：

"""
请用 argparse 实现 CLI，并让 python 脚本 -h/--help 的帮助信息支持统一彩色高亮（与你的 pycli-color 规范一致）。

必须实现：
1) supports_color()：默认 auto（仅 sys.stdout.isatty()==True 且 TERM != 'dumb' 启用）；若存在 NO_COLOR 则强制禁用；若 FORCE_COLOR=1 则强制启用（即便非 TTY）。
2) colorize(text, ansi_code)：仅在启用颜色时包裹 ANSI，否则原样返回。
3) ColorHelpFormatter(argparse.HelpFormatter)，并覆写 HelpFormatter._format_action_invocation：
   - token 以 '-' 开头（-h/--title 等）→ 青色+加粗（\x1b[36;1m）
   - token 为 metavar（全大写或含 '_'，TITLE/AJG_CSV 等）→ 黄色+加粗（\x1b[33;1m）
   - 其他 token 不着色；每段着色后追加 reset（\x1b[0m）
4) ArgumentParser(formatter_class=ColorHelpFormatter) 启用 formatter。
5) CLI 至少包含：1 个 required=True 参数、1 个可选参数、1 个 choices 参数，并包含 if __name__ == '__main__': main()。
6) 代码里必须保留测试注释：
   - NO_COLOR=1 python3 your_script.py -h
   - NO_COLOR= FORCE_COLOR=1 python3 your_script.py -h
   默认使用相对路径，并保证脚本可直接运行。
   """

