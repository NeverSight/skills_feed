---
name: oh-distributed-security-design-review
description: OpenHarmony分布式系统安全代码检视专用技能。当用户要求"检视代码安全实现"、"代码安全审查"、"安全代码review"或类似的分布式系统代码安全检视请求时触发。此技能提供18条OpenHarmony分布式业务安全设计规则的详细检视指导，涵盖授权控制、状态机、数据传输、权限管理、可信关系等安全领域。使用此技能可在通用网络安全规则基础上，针对OpenHarmony分布式系统进行专项安全检视。
---

# Code Review Skill for OpenHarmony Distributed System Security

## Overview

本技能提供OpenHarmony分布式业务安全代码检视的专业指导，包含18条安全设计规则和对应的检视要点。当检视分布式系统代码安全性时，在通用网络安全规则基础上，使用这些规则进行加强检视。

## Trigger Phrases

- "检视代码安全实现"
- "代码安全审查"
- "安全代码review"
- "检查这段代码的安全性"
- "review分布式代码安全"
- "OpenHarmony安全检视"

## Code Review Workflow

### Step 1: Understand the Code Context

首先理解代码的业务场景和所在模块：

1. **识别关键模块**: 确定代码是否涉及以下模块
   - 分布式设备管理
   - 分布式软总线
   - 其他需要分布式能力的模块

2. **识别业务类型**: 判断是否涉及以下安全敏感业务
   - 设备间认证和授权
   - 用户敏感数据传输
   - 跨设备状态机管理
   - 可信关系管理
   - 硬件资源访问

3. **确定角色**: 识别代码是主体侧(客户端)还是客体侧(服务端)

### Step 2: Load Security Rules

根据代码涉及的业务类型，加载[security_rules.md](references/security_rules.md)中对应的规则：

**快速索引关键词:**
- 跨设备传输 → Rules 3, 8, 15, 17
- 状态机 → Rule 2
- 授权/鉴权 → Rules 1, 5, 6, 8, 12
- PIN码/秘钥 → Rules 3, 8, 9, 10
- 资源申请 → Rule 4
- 权限配置 → Rules 7, 13
- 开关标记 → Rule 14
- 用户切换 → Rule 16
- 兼容代码 → Rule 18

### Step 3: Review Against Security Rules

对每个适用的安全规则，执行以下检视：

1. **定位相关代码**: 使用Grep搜索关键模式
   ```
   Grep patterns examples:
   - "auth", "authorize", "permission" for authorization checks
   - "PIN", "secret", "key" for sensitive data
   - "state", "status" for state machine
   - "random", "generate" for secret generation
   ```

2. **检查实现细节**:
   - 对照规则中的Check points逐项检查
   - 查找潜在的违规模式
   - 识别缺失的安全措施

3. **记录发现**:
   - 标记违规代码位置 (file:line)
   - 说明违反的具体规则
   - 提供修复建议

### Step 4: Apply General Security Best Practices

除了OpenHarmony特定规则外，还需检查通用安全实践：

1. **输入验证**: 所有外部输入是否经过验证
2. **错误处理**: 敏感操作是否有适当的错误处理
3. **日志安全**: 是否记录了敏感信息
4. **资源管理**: 是否有资源泄漏风险

### Step 5: Generate Review Report

生成结构化的安全检视报告，包含：

1. **执行摘要**: 发现的严重安全问题数量和等级
2. **违规清单**: 按严重程度排序的违规项
3. **规则映射**: 每个问题对应的安全规则
4. **修复建议**: 具体的代码修改建议

## Common Violation Patterns

### Pattern 1: Client-controlled Authorization (违反规则1)

**Bad Example:**
```cpp
// 客体侧直接使用主体侧传入的标志控制弹框
void handleAuthRequest(bool showPopup) {
    if (!showPopup) {
        // 直接跳过授权弹框
        grantAccess();
    }
}
```

**Correct Approach:**
```cpp
// 客体侧独立决策是否需要授权
void handleAuthRequest() {
    if (isSystemBusinessAndRegistered()) {
        // 已注册的免授权业务
        grantAccess();
    } else {
        // 默认必须弹框
        showAuthorizationDialog();
    }
}
```

### Pattern 2: Plaintext Sensitive Data (违反规则3)

**Bad Example:**
```cpp
// 明文传输PIN码
message.pin_code = userPin;
sendToRemote(message);
```

**Correct Approach:**
```cpp
// 加密后传输
encryptedPin = encryptPin(userPin, sessionKey);
message.encrypted_pin = encryptedPin;
sendToRemote(message);
```

### Pattern 3: Custom Trust Verification (违反规则8)

**Bad Example:**
```cpp
// 自行比对账号信息判断可信关系
bool isTrusted() {
    return localAccount == remoteAccount;
}
```

**Correct Approach:**
```cpp
// 依赖HiChain查询
bool isTrusted() {
    CredentialType type = HiChain.queryCredentialType(remoteDevice);
    return type == CredentialType.SAME_ACCOUNT;
}
```

### Pattern 4: Insecure Switch Defaults (违反规则14)

**Bad Example:**
```cpp
// 默认值放通
bool enableSecurityCheck = true;  // 默认启用
```

**Correct Approach:**
```cpp
// 默认值禁用
bool enableSecurityCheck = false;  // 默认禁用，需显式启用
```

## Security Rule Categories

### 1. Authorization & Authentication
- Rule 1: Object-side Authorization Control
- Rule 5: Anti-Brute Force Protection
- Rule 6: Server-side Security Logic
- Rule 12: Sensitive Data Authorization and Audit

### 2. Data Protection
- Rule 3: No Plaintext Sensitive Data Transmission
- Rule 10: Secure Random Secrets
- Rule 17: Business-level Key Isolation

### 3. Trust Management
- Rule 7: Trusted Relationship Lifecycle Minimization
- Rule 8: Trusted Relationship Verification
- Rule 9: Trusted Relationship Persistence Timing
- Rule 15: Device Legitimacy Verification
- Rule 16: User Isolation for Distributed Trust

### 4. State Machine & Process Control
- Rule 2: State Machine Context Validation

### 5. Resource Management
- Rule 4: Resource Access Parameter Validation
- Rule 11: Resource Cleanup
- Rule 13: Minimal Permission Configuration

### 6. Code Quality
- Rule 14: Secure Switch Default Values
- Rule 18: Legacy Protocol Cleanup

## Example Review Session

**User request**: "检视这段分布式设备管理代码的安全性"

**Review process**:

1. **Load security rules** → Read [security_rules.md](references/security_rules.md)
2. **Identify relevant rules** → Rules 1, 2, 7, 8, 9, 11 (设备管理相关)
3. **Search code patterns** → Grep for authorization, trust, state machine
4. **Check each rule**:
   - ✓ Rule 1: 授权流程是否在客体侧独立控制
   - ✗ Rule 2: 发现状态机未校验上下文
   - ✓ Rule 7: 可信关系生命周期管理正确
   - ✗ Rule 8: 发现自定义可信判断逻辑
5. **Generate report** → 列出违规点和修复建议

## Tips

1. **Start with keywords**: 使用security_rules.md中的关键词快速定位可疑代码
2. **Check both sides**: 分布式业务需要同时检查主体侧和客体侧代码
3. **Verify complete flows**: 跟踪完整的业务流程，不要只检查单个函数
4. **Consider edge cases**: 检查错误处理、超时、重试等边界场景
5. **Review logging**: 确保日志中不泄露敏感信息

## Resources

- **Detailed Rules**: See [security_rules.md](references/security_rules.md) for complete rule descriptions and check points
- **Quick Reference**: Use keyword mapping at the end of security_rules.md for fast rule lookup
