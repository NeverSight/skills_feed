---
name: solidity-debug
description: "[AUTO-INVOKE] MUST be invoked when debugging failed on-chain transactions. Covers transaction receipt analysis, gas diagnosis, calldata decoding, revert reason extraction, and state verification using cast. Trigger: any task involving failed tx analysis, revert debugging, or on-chain transaction troubleshooting."
---

# Failed Transaction Debug Workflow (cast)

## Language Rule

- **Always respond in the same language the user is using.** If the user asks in Chinese, respond in Chinese. If in English, respond in English.

## Step 1: 获取交易回执 — 判断成功/失败

```bash
source .env
cast receipt <tx_hash> --rpc-url $RPC_URL
```

**关注字段：**

| 字段 | 含义 |
|------|------|
| `status` | 0 = 失败, 1 = 成功 |
| `gasUsed` | 实际消耗的 gas |
| `logs` | 空数组 `[]` = 交易 revert，无事件发出 |
| `to` | 目标合约地址 |

## Step 2: 获取交易详情 — 拿到 gas limit 和 input

```bash
cast tx <tx_hash> --rpc-url $RPC_URL
```

**关注字段：**

| 字段 | 含义 |
|------|------|
| `gas` | 发送方设置的 gas limit |
| `input` | 调用的 calldata（函数选择器 + 参数编码） |
| `from` / `to` | 发送方和目标合约 |
| `value` | 发送的原生代币数量 |

## Step 3: 判断失败类型 — gasUsed vs gas limit

| 现象 | 判断 | 解决方向 |
|------|------|---------|
| gasUsed / gas ≈ 100%（如 999,472 / 1,000,000） | **Out of Gas (OOG)** | 提高 gas limit 或用 eth_estimateGas |
| gasUsed 远低于 gas limit（如 50,000 / 1,000,000） | **Revert** | 需获取 revert reason，见 Step 6 |
| gasUsed 正常但 status=0 | **内部调用失败** | 检查余额、授权、内部 call 返回值 |
| 交易根本没上链 | **Nonce/Gas Price 问题** | 检查 pending 队列 |

## Step 4: 解码函数选择器 — 确定调用了什么函数

```bash
# 从 input 的前 4 字节查函数签名
cast 4byte 0xb51a038a
# 输出示例: unstake(uint256,address[],uint256[])
```

## Step 5: 解码完整 calldata — 还原调用参数

```bash
# 用 Step 4 得到的函数签名解码
cast calldata-decode "unstake(uint256,address[],uint256[])" <完整input_data>
```

解码后的参数可用于：
- 分析入参是否有误
- 直接用于重试交易

## Step 6: 获取 Revert Reason（非 OOG 场景）

```bash
# 方法 A: cast call 模拟（指定失败区块号，用交易所在区块）
cast call <to> <input_data> \
  --from <from> \
  --block-number <block_number> \
  --rpc-url $RPC_URL

# 方法 B: cast run 重放交易（需要 archive 节点）
cast run <tx_hash> --rpc-url <archive_rpc_url>

# 方法 C: 在线工具（备用）
# 使用 Tenderly 或 Blocksec Phalcon 等交易分析平台
```

## Step 7: 查询链上状态 — 确认交易失败后数据已回滚

```bash
# 查询 public 变量/映射
cast call <contract> "orderLocations(uint256)(address,uint256,bool)" <id> --rpc-url $RPC_URL

# 查询 struct 字段（按 ABI 顺序指定返回类型）
cast call <contract> "userStakeRecord(address,uint256)(uint40,uint160,bool,uint8,uint256)" <user> <index> --rpc-url $RPC_URL
```

> 失败交易的状态变更会完全回滚，需确认数据仍在原始状态。

## Step 8: 对比成功 vs 失败交易 — 找差异

将成功和失败的交易放在一起对比：

| 对比维度 | 说明 |
|---------|------|
| gas 消耗 | 判断是否 OOG |
| 调用参数 | 判断是否入参问题 |
| 目标地址 | 判断是否调错合约 |
| 区块时间 | 判断是否有时间锁等限制 |
| 合约状态 | 判断是否前置条件不满足 |

## Step 9: 重试交易

```bash
source .env

# 不指定 gas limit（让节点自动估算，推荐）
cast send <contract> "functionName(uint256,address[],uint256[])" <arg1> "[<addr1>,<addr2>]" "[<amt1>,<amt2>]" \
  --account <KEYSTORE_NAME> \
  --rpc-url $RPC_URL \
  --legacy

# 指定较高 gas limit（适用于已知消耗范围的场景）
cast send <contract> "functionName(uint256)" <arg1> \
  --account <KEYSTORE_NAME> \
  --rpc-url $RPC_URL \
  --gas-limit 2000000 \
  --legacy
```

## 安全注意事项

| 规则 | 说明 |
|------|------|
| 私钥管理 | **使用 Foundry Keystore (`--account`)** 管理私钥，禁止在命令中明文传入 |
| 模拟优先 | 真实发送前先用 `cast call` 模拟，确认不会 revert |
| 逐笔发送 | 批量重试时先发一笔验证，成功后再发剩余 |
| 状态确认 | 发送后用 `cast receipt` 确认 status=1，再用 `cast call` 确认链上状态已变更 |

## 完整示例流程

```bash
source .env

# 1. 看回执
cast receipt 0x4ca1...414f --rpc-url $RPC_URL

# 2. 看交易详情
cast tx 0x4ca1...414f --rpc-url $RPC_URL

# 3. 发现 gas=1000000, gasUsed=999472, status=0 → OOG

# 4. 解码函数选择器
cast 4byte 0xb51a038a
# → unstake(uint256,address[],uint256[])

# 5. 解码完整参数
cast calldata-decode "unstake(uint256,address[],uint256[])" 0xb51a038a...

# 6. 模拟确认能通过
cast call <contract> "unstake(uint256,address[],uint256[])" 35 "[addr1,addr2]" "[amt1,amt2]" \
  --from <from> --rpc-url $RPC_URL

# 7. 查链上状态确认订单仍未处理
cast call <contract> "orderLocations(uint256)(address,uint256,bool)" 35 --rpc-url $RPC_URL

# 8. 确认是 OOG → 不限 gas 重试
cast send <contract> "unstake(uint256,address[],uint256[])" 35 "[addr1,addr2]" "[amt1,amt2]" \
  --account <KEYSTORE_NAME> --rpc-url $RPC_URL --legacy

# 9. 确认成功
cast receipt <new_tx_hash> --rpc-url $RPC_URL
```