---
name: crypto-solver-skill
description: CTF 密码学自动求解工作流（RSA/ECC/Lattice 等），配套 SageMath/Python 辅助脚本。
---

# Crypto Solver Skill (for Codex)

用于快速求解 CTF 密码学题：先系统化读题和源代码，再进行漏洞识别，提出攻击计划并落地成可跑的 Python/SageMath。

## 工作方式（按阶段输出）

### Phase 1: 系统分析

- 读取题目给的所有文件（源码、输出、参数、交互协议）。
- 明确：算法类型、参数规模、密钥生成方式、消息格式、与服务交互方式。
- 输出“系统分析报告”，包括最可能的 1-3 个攻击面。

### Phase 2: 漏洞识别（PAUSE）

- 针对 Phase 1 的攻击面逐条验证：数学弱点、实现缺陷、随机性问题、协议/填充问题。
- 给出每个候选漏洞的可行性判断（需要哪些额外信息/样本）。
- 进入下一阶段前暂停，向用户询问需要的输入或确认优先级。

### Phase 3: 攻击策略（PAUSE）

- 给出明确的攻击计划：步骤、所需数据、预期产物（恢复私钥/明文/伪造签名等）。
- 明确要写哪些脚本、用哪些库（Python/SageMath），以及验证方式。
- 在开始大量写代码前暂停，让用户确认计划。

### Phase 4: 代码实现

- 生成可执行的解题代码（优先放在题目目录下，如 `solve.py` / `solve.sage`）。
- 需要 SageMath 时：优先生成 `.sage` 并在本机运行；如果环境没有 sage，再提供纯 Python 退路。
- 每次关键推断都要用计算验证（例如 gcd、根、LLL/BKZ、CRT 等）。

### Phase 5: 文档生成

- 产出 `analyse.md`：包含攻击思路、关键数学点、代码入口、运行命令、以及如何得到 flag。

## 主题提示

- RSA：低指数（`e=3`/小 e）、广播攻击、共模/共享因子（`gcd`）、Wiener、部分泄漏/Coppersmith、Fermat、rho/ECM。
- ECC：阶含小因子（Pohlig-Hellman）、奇异曲线/Smart、invalid curve、twist。
- Lattice：LWE/NTRU/背包，LLL/BKZ，small roots。

## 辅助脚本

- `tools/sage-executor.py`：执行 Sage 代码（Windows 会尝试 WSL）。
- `tools/crypto-utils.py`：常用分析/分解函数。
