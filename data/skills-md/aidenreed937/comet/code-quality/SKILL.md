---
name: code-quality
description: Flutter 项目代码质量检测和修复，包括 Dart 代码分析、格式化、测试。当用户提到"代码检查"、"分析"、"格式化"、"代码风格"、"质量检测"、"测试"时使用此 skill。
---

# Flutter 代码质量检测

确保 Flutter/Dart 代码符合项目规范，自动检测和修复问题。

## 🤖 使用子代理执行（推荐）

**代码质量检查可能产生大量输出，建议通过子代理执行**

### 为什么使用子代理

代码质量检查的输出特点：

- ✅ **通过时**：输出简洁（几行）
- ❌ **失败时**：可能产生大量错误信息
  - Dart 分析错误：5k-10k tokens
  - 格式化问题：2k-5k tokens
  - 测试失败信息：3k-5k tokens
  - **总计可达 10k-20k tokens**

### 使用建议

| 场景                      | 建议      | 原因                   |
| ------------------------- | --------- | ---------------------- |
| 完整质量检查              | 🤖 子代理 | 可能有大量错误需要修复 |
| 单项检查（如 analyze）    | 🤖 子代理 | 错误输出可能很多       |
| 格式化代码 (`dart format`) | 📝 主窗口 | 输出简洁               |
| 快速检查（确定无错误）    | 📝 主窗口 | 输出少                 |

### 子代理执行示例

```typescript
Task({
  subagent_type: 'general-purpose',
  description: '运行 Flutter 代码质量检查',
  prompt: `
运行完整代码质量检查：
1. 执行 flutter analyze, dart format, flutter test
2. 如有错误，分析并修复
3. 再次验证直到全部通过
4. 返回最终检查结果摘要

遵循 .claude/skills/code-quality/SKILL.md 中的规范。
  `,
})
```

---

## 检测工具

### 1. Dart Analyzer - 代码分析

**配置**: `analysis_options.yaml`

**主要规则**:

- Dart/Flutter 语法规范
- 类型安全检查
- 未使用变量/导入检测
- 命名规范检查
- 空安全检查

**命令**:

```bash
flutter analyze      # 分析整个项目
dart analyze lib/    # 分析指定目录
```

### 2. Dart Format - 代码格式化

**格式规则**:

- 2 空格缩进
- 行宽 80 字符（可配置）
- 自动整理导入语句

**命令**:

```bash
dart format .                # 格式化所有文件
dart format lib/ test/       # 格式化指定目录
dart format --set-exit-if-changed .  # 检查格式（CI用）
```

### 3. Flutter Test - 单元测试

**测试类型**:
- 单元测试 (Unit Tests)
- Widget 测试 (Widget Tests)
- 集成测试 (Integration Tests)

**命令**:

```bash
flutter test                    # 运行所有测试
flutter test test/unit/         # 运行指定目录测试
flutter test --coverage         # 生成覆盖率报告
flutter test --reporter=expanded  # 详细输出
```

### 4. Pub 依赖检查

**命令**:

```bash
flutter pub outdated        # 检查过期依赖
flutter pub upgrade         # 升级依赖
dart pub global run pana .  # 包质量评分（发布包时）
```

---

## 完整质量检查

运行所有检测：

```bash
# 1. 代码分析
flutter analyze

# 2. 格式检查
dart format --set-exit-if-changed .

# 3. 运行测试
flutter test

# 4. 检查依赖
flutter pub outdated
```

---

## 安全性检查清单

### 敏感信息检查

手动检查代码中是否包含：

- ❌ 硬编码的 API 密钥、Access Token
- ❌ 硬编码的密码、Secret Key
- ❌ 个人身份信息（PII）
- ❌ 内部 URL、IP 地址
- ✅ 使用环境变量或配置文件

### 常见安全漏洞

| 漏洞类型   | 检查方法            | 预防措施                      |
| ---------- | ------------------- | ----------------------------- |
| SQL 注入   | 检查 API 参数拼接   | 后端使用参数化查询            |
| 敏感操作   | 检查权限验证        | 删除/修改操作需要权限检查     |
| 数据泄露   | 搜索 `print`/`log`  | 移除或脱敏敏感日志            |
| 本地存储   | 检查 SharedPreferences | 加密敏感数据                  |
| 网络请求   | 检查 HTTP 使用      | 强制使用 HTTPS                |

### 依赖安全

定期检查：

```bash
flutter pub outdated
dart pub upgrade --dry-run
```

处理建议：

- **Critical/High**：立即升级
- **Moderate**：评估影响，计划升级
- **Low**：可选升级

---

## 性能检查清单

### 代码性能

| 检查项     | 标准               | 工具              |
| ---------- | ------------------ | ----------------- |
| 文件大小   | 单文件 < 500 行    | `wc -l <file>`    |
| Widget 嵌套 | 嵌套层级 < 10      | 手动检查 Widget 树 |
| 列表优化   | 使用 ListView.builder | 代码审查          |
| 状态管理   | 避免过度 setState  | Flutter DevTools  |
| 异步操作   | 正确处理 async/await | Dart Analyzer     |

### 构建性能

```bash
# Android APK 大小检查
flutter build apk --release
ls -lh build/app/outputs/flutter-apk/

# iOS 构建大小检查
flutter build ios --release
```

检查项：

- APK < 50MB（未分包）
- 移除未使用的资源
- 启用代码混淆和压缩

### 运行时性能

使用 Flutter DevTools 检查：

```bash
flutter run --profile
# 打开 DevTools 查看性能
```

检查要点：

- 避免不必要的 rebuild
- 使用 const 构造函数
- 列表使用 ListView.builder
- 避免在 build 方法中创建大对象

---

## 自动化流程

### Pre-commit Hook

可配置 Git Hook 在提交前运行：

```bash
# .git/hooks/pre-commit
#!/bin/bash
flutter analyze
dart format --set-exit-if-changed .
flutter test
```

### CI/CD 集成

```yaml
# .github/workflows/flutter.yml 示例
- name: Analyze
  run: flutter analyze
  
- name: Format Check
  run: dart format --set-exit-if-changed .
  
- name: Test
  run: flutter test --coverage
```

## 常见问题修复

### Dart Analyzer 错误

```dart
// ❌ 错误：未使用的导入
import 'package:flutter/material.dart';
import 'package:unused/unused.dart';

// ✅ 修复：移除未使用的导入
import 'package:flutter/material.dart';
```

### 格式问题

```dart
// ❌ 错误：格式不规范
class MyWidget extends StatelessWidget{
@override
Widget build(BuildContext context){
return Container();}
}

// ✅ 修复：运行 dart format
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
```

### 提交信息

```bash
# ❌ 错误
git commit -m "修复bug"

# ✅ 正确
git commit -m "fix: 修复登录页面验证问题"
git commit -m "feat(ui): 添加用户头像上传功能"
```

## 使用场景

1. **编写代码时**: Claude 会提示不符合规范的代码
2. **提交前**: 运行质量检查确保代码符合规范
3. **CI/CD**: 在流水线中自动运行检查
