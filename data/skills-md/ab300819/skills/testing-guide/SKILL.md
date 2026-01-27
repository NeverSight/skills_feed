---
name: testing-guide
description: Opinionated constraints for writing effective tests. Guide unit tests, integration tests, and E2E tests with quality metrics beyond coverage. Use when users write tests, review test code, or need testing strategy. Triggers on keywords like "test", "testing", "单元测试", "集成测试", "E2E", "测试质量", "coverage", "断言".
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, AskUserQuestion
---

# Testing Guide

编写高质量测试的约束规范，确保测试真正验证行为而非仅仅覆盖代码。

## Language

- Accept questions in both Chinese and English
- Always respond in Chinese

## Trigger Conditions

- 用户正在编写测试代码
- 用户需要测试策略指导
- 用户提到测试覆盖率、断言、变异测试
- Code Review 中涉及测试代码

---

## 核心理念

```
测试的目的不是"覆盖代码"，而是"验证行为"。
测试依据来自需求，不是来自代码。
```

### 测试质量金字塔

```
Level 3: 测试有效性 ─ 变异得分≥80%, 需求追溯100%
Level 2: 断言质量   ─ 禁止弱断言, 验证行为非实现
Level 1: 代码覆盖   ─ 行/分支覆盖≥80% (必要非充分)
```

> 详细说明见 [templates/core-concepts.md](templates/core-concepts.md)

---

## Constraints

### 单元测试约束

- [ ] **每个测试必须有 ≥1 个具体断言**
- [ ] **禁止弱断言作为唯一断言** (`toBeDefined`, `toBeTruthy`, `not.toBeNull`)
- [ ] **测试名称必须描述预期行为**
- [ ] **测试依据来自需求，不是代码**
- [ ] 只 Mock 外部依赖，不 Mock 内部实现
- [ ] 每个测试只验证一个行为

> 详细指南见 [templates/unit-testing.md](templates/unit-testing.md)

### 覆盖率约束

- [ ] **行覆盖率 ≥ 80%**
- [ ] **分支覆盖率 ≥ 80%**
- [ ] 覆盖率是必要条件，不是充分条件

### 变异测试约束（推荐）

- [ ] 变异得分 ≥ 60%（建议 ≥ 80%）
- [ ] 核心业务逻辑变异得分 ≥ 80%

> 配置见 [templates/mutation-testing.md](templates/mutation-testing.md)

### 集成测试约束

- [ ] 必须验证模块间数据流
- [ ] 必须验证接口契约
- [ ] 测试数据必须独立

> 详细指南见 [templates/integration-testing.md](templates/integration-testing.md)

### E2E 测试约束

- [ ] **P0 场景必须 100% 覆盖**
- [ ] 使用显式等待，禁止硬编码延时
- [ ] 测试必须可独立运行

> 详细指南见 [templates/e2e-testing.md](templates/e2e-testing.md)

### 需求追溯约束

- [ ] 每个需求必须有对应测试
- [ ] 测试代码应标注需求ID

> 模板见 [templates/traceability-matrix.md](templates/traceability-matrix.md)

---

## 测试骨架生成

> AI 驱动的自顶向下开发：先生成测试骨架，后填充实现。

### 标注规范

测试代码必须包含追溯标注，用于 `/devdocs-sync --trace` 扫描：

```typescript
/**
 * @verifies AC-XXX - 验收标准描述
 * @testcase UT/IT/E2E-XXX
 */
test('测试名称', () => {
  // 测试代码
});
```

| 标注 | 用途 | 必须性 |
|------|------|--------|
| `@verifies AC-XXX` | 关联验收标准 | **必须** |
| `@testcase UT/IT/E2E-XXX` | 测试用例编号 | **必须** |

### 骨架生成流程

```
03-test-cases.md (测试用例设计)
        │
        ▼
生成测试骨架
        ├── describe 结构（按功能点分组）
        ├── test.skip() 占位（每个测试用例）
        ├── @verifies/@testcase 标注
        └── // TODO: 实现测试 注释
        │
        ▼
逐个实现测试
        ├── 移除 skip
        ├── 编写 AAA 结构
        └── 添加具体断言
```

### 骨架示例

```typescript
// tests/user.service.test.ts

describe('UserService', () => {
  describe('createUser', () => {
    /**
     * @verifies AC-001 - 邮箱格式校验
     * @testcase UT-001
     */
    test.skip('应该拒绝无效邮箱格式', () => {
      // TODO: 实现测试
      // Arrange: 准备无效邮箱
      // Act: 调用 createUser
      // Assert: 验证抛出 ValidationError
    });

    /**
     * @verifies AC-002 - 密码强度校验
     * @testcase UT-002
     */
    test.skip('应该拒绝弱密码', () => {
      // TODO: 实现测试
    });

    /**
     * @verifies AC-003 - 用户名唯一性
     * @testcase UT-003
     */
    test.skip('应该拒绝重复用户名', () => {
      // TODO: 实现测试
    });
  });
});
```

### 骨架生成约束

- [ ] **必须使用 `test.skip()` 或 `test.todo()` 标记未实现测试**
- [ ] **必须添加 `@verifies` 和 `@testcase` 标注**
- [ ] **必须按功能点 (F-XXX) 组织 describe 结构**
- [ ] **必须在注释中提示 AAA 结构**
- [ ] 测试名称必须描述预期行为
- [ ] 一个测试只验证一个 AC

### 与 DevDocs 协作

| 阶段 | Skill | 输入 | 输出 |
|------|-------|------|------|
| 测试设计 | `/devdocs-test-cases` | 需求文档 | 测试用例矩阵 |
| 骨架生成 | `/devdocs-dev-tasks` | 测试用例 | 测试骨架代码 |
| 测试实现 | `/testing-guide` | 骨架代码 | 完整测试 |
| 追溯同步 | `/devdocs-sync --trace` | 代码标注 | 更新矩阵 |

---

## Quick Reference

### 测试命名

```
[被测方法] 应该 [预期行为] 当 [条件]
```

### 测试结构 (AAA)

```
Arrange → Act → Assert (具体断言)
```

### 禁止的弱断言

```javascript
// ❌ 禁止
expect(result).toBeDefined();
expect(result).toBeTruthy();
expect(result).not.toBeNull();

// ✅ 要求
expect(result.status).toBe('success');
expect(result.items).toHaveLength(3);
```

### 常用命令

```bash
# 覆盖率
npm test -- --coverage          # Jest
pytest --cov=src               # pytest
go test -cover ./...           # Go

# 变异测试
npx stryker run                # JS/TS
mutmut run                     # Python
mvn pitest:mutationCoverage    # Java
```

---

## 模板索引

### 核心指南

| 模板 | 说明 |
|------|------|
| [core-concepts.md](templates/core-concepts.md) | 测试核心理念与质量金字塔详解 |
| [unit-testing.md](templates/unit-testing.md) | 单元测试完整指南 |
| [integration-testing.md](templates/integration-testing.md) | 集成测试策略与示例 |
| [e2e-testing.md](templates/e2e-testing.md) | E2E 测试最佳实践 |

### 工具配置

| 模板 | 说明 |
|------|------|
| [mutation-testing.md](templates/mutation-testing.md) | 8种语言变异测试配置 |
| [ci-integration.md](templates/ci-integration.md) | CI/CD 集成配置 |
| [traceability-matrix.md](templates/traceability-matrix.md) | 需求追溯矩阵 |
| [test-examples.md](templates/test-examples.md) | 测试代码示例集 |

### 语言最佳实践

| 语言 | 框架 | 模板 |
|------|------|------|
| JavaScript/TypeScript | Jest, Vitest | [best-practices/jest-vitest.md](templates/best-practices/jest-vitest.md) |
| Python | pytest | [best-practices/pytest.md](templates/best-practices/pytest.md) |
| Java | JUnit 5 | [best-practices/junit5.md](templates/best-practices/junit5.md) |
| C# / .NET | xUnit, NUnit | [best-practices/xunit.md](templates/best-practices/xunit.md) |
| Go | testing, testify | [best-practices/go.md](templates/best-practices/go.md) |
| Rust | cargo test | [best-practices/rust.md](templates/best-practices/rust.md) |
| Swift | XCTest | [best-practices/swift.md](templates/best-practices/swift.md) |
| C/C++ | Google Test | [best-practices/googletest.md](templates/best-practices/googletest.md) |

---

## 与其他 Skills 协作

| 场景 | Skill |
|------|-------|
| 测试用例设计 | `/devdocs-test-cases` |
| 代码可测试性 | `/code-quality` |
| 重构前测试 | `/refactor` |
