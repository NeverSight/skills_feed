---
name: flutter-best-practices
description: Flutter 开发最佳实践指南，涵盖架构、依赖管理、UI 开发、平台配置。当用户提到"最佳实践"、"架构"、"Riverpod"、"GoRouter"、"Dio"、"主题"、"响应式"、"无障碍"时使用此 skill。
---

# Flutter Best Practices

确保 Flutter 代码遵循项目架构约定和最佳实践。

## 1. 环境与工具

| 配置项 | 要求 |
|--------|------|
| Flutter channel | stable |
| Dart SDK | `>=3.7.0 <4.0.0` |
| 国际化 | `flutter gen-l10n`（修改 arb 后执行） |
| 清理构建 | `flutter clean && rm -rf build/` |

## 2. 依赖管理

### 核心依赖选型

| 功能 | 推荐库 | 用途 |
|------|--------|------|
| 状态管理 | `flutter_riverpod` 3.x | Provider + StateNotifier |
| 路由 | `go_router` 17.x | 声明式导航 |
| 网络 | `dio` 5.x | HTTP 客户端 + 拦截器 |
| 轻量存储 | `shared_preferences` | 非敏感 flags |
| 安全存储 | `flutter_secure_storage` | 凭证/secrets |
| 结构化缓存 | `hive` + `hive_flutter` | 离线数据 |

### 依赖原则

```bash
# 检查过期依赖
flutter pub outdated

# 保守升级（patch 级别）
flutter pub upgrade --major-versions  # 谨慎使用
```

- 使用 caret 约束（`^x.y.z`）获取 patch 修复
- 环境变量通过 `--dart-define` 传递，不硬编码

## 3. 架构约定

### 目录结构

```
lib/
├── app/                    # 组合根
│   ├── di.dart            # 核心服务 Provider
│   └── router.dart        # GoRouter 配置
├── core/                   # 基础设施（不导入 features）
│   ├── config/            # 环境配置
│   ├── error/             # Failure + Result<T>
│   ├── network/           # Dio + 拦截器
│   ├── storage/           # 存储封装
│   ├── theme/             # 主题定义
│   └── widgets/           # 通用组件
└── features/<name>/        # 功能模块
    ├── presentation/      # UI + Provider
    ├── domain/            # 实体 + 接口（纯 Dart）
    └── data/              # 数据源 + 实现
```

### 层级规则

- `core/` **禁止**导入 `features/`
- `domain/` **禁止**导入 `package:flutter`
- Feature 间通信通过 `core/services/` 或共享接口

### 依赖注入

```dart
// app/di.dart - 核心服务
final dioClientProvider = Provider<DioClient>((ref) => DioClient());

// features/xxx/presentation/providers/ - 功能 Provider
final xxxControllerProvider = StateNotifierProvider<XxxController, XxxState>(...);
```

### 路由配置

```dart
// features/xxx/presentation/routes.dart
class XxxRoutes {
  static const xxx = '/xxx';
}

List<GoRoute> buildXxxRoutes() => [
  GoRoute(path: XxxRoutes.xxx, builder: (_, __) => const XxxPage()),
];

// app/router.dart
final routerProvider = Provider<GoRouter>((ref) => GoRouter(
  routes: [...buildXxxRoutes(), ...buildYyyRoutes()],
));
```

### 错误处理

```dart
// 使用 Result<T> 替代 try-catch
Future<Result<User>> getUser(String id) async {
  try {
    final response = await dio.get('/users/$id');
    return Success(User.fromJson(response.data));
  } on DioException catch (e) {
    return Err(NetworkFailure(e.message));
  }
}

// UI 层处理
result.when(
  success: (user) => showUser(user),
  failure: (failure) => showError(failure.message),
);
```

## 4. UI 最佳实践

### Widget 设计

| 原则 | 说明 |
|------|------|
| 小而可组合 | 拆分 Page + 叶子组件 |
| 无状态优先 | 状态放 Riverpod，不放 StatefulWidget |
| const 构造 | 减少不必要的 rebuild |
| 主题引用 | `Theme.of(context)` 而非硬编码 |

### 样式规范

```dart
// ✅ 正确：从主题获取
final color = Theme.of(context).colorScheme.primary;
final textStyle = Theme.of(context).textTheme.titleLarge;

// ❌ 错误：硬编码
final color = Color(0xFF2196F3);
final textStyle = TextStyle(fontSize: 22);
```

### 响应式布局

```dart
// 使用 LayoutBuilder 适配不同屏幕
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 600) {
      return TabletLayout();
    }
    return MobileLayout();
  },
);
```

### 无障碍

| 要求 | 实现 |
|------|------|
| 点击区域 | `≥48` 逻辑像素 |
| 图标语义 | 添加 `Semantics` 标签 |
| 字体缩放 | 尊重 `MediaQuery.textScaleFactor` |

## 5. 平台配置

### Android

```xml
<!-- AndroidManifest.xml - flutter_secure_storage 需要 -->
<uses-permission android:name="android.permission.USE_BIOMETRIC" />
```

- Java 版本：17（CI 配置）
- Gradle lint：`./gradlew lint`

### iOS

```bash
# 本地开发
cd ios && pod install && open Runner.xcworkspace

# CocoaPods 问题
pod repo update
```

## 6. 工作流清单

```bash
# 开发流程
flutter pub get
# ... 实现功能 ...
dart format --set-exit-if-changed .
flutter analyze --fatal-infos
flutter gen-l10n                    # 如有国际化变更
flutter test --coverage
```

## 7. 参考文档

| 库 | 文档 |
|---|------|
| Flutter SDK | https://docs.flutter.dev |
| flutter_riverpod | https://riverpod.dev/docs/getting_started |
| go_router | https://pub.dev/documentation/go_router/latest/ |
| dio | https://pub.dev/documentation/dio/latest/ |
| hive | https://docs.hivedb.dev/#/ |
| flutter_secure_storage | https://pub.dev/documentation/flutter_secure_storage/latest/ |

## 使用场景

1. **新建 Feature**: 遵循 presentation/domain/data 分层
2. **添加依赖**: 优先使用已选型的库
3. **编写 UI**: 无状态 + const + 主题引用
4. **错误处理**: 使用 Result<T> + Failure
5. **平台适配**: 检查 Manifest/Podfile 配置
