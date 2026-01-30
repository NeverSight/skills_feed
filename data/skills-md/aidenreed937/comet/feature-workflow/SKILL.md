---
name: feature-workflow
description: Flutter Feature 开发工作流，从数据获取到 UI 展示的完整开发流程。当用户提到"创建功能"、"新建页面"、"开发 feature"、"添加模块"时使用此 skill。
---

# Feature 开发工作流

完整的 Feature 开发流程，确保代码分层清晰、UI 无硬编码。

---

## 🔄 工作流程图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Phase 0: 需求分析                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                          │
│  │   文字描述   │  │  UI 截图    │  │  设计稿     │                          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                          │
│         └────────────────┼────────────────┘                                 │
│                          ▼                                                  │
│              ┌───────────────────────┐                                      │
│              │  提取: 实体 / API / UI │                                      │
│              └───────────┬───────────┘                                      │
└──────────────────────────┼──────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Phase 1-4: 分层开发                                  │
│                                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│  │ Domain  │───▶│  Data   │───▶│Provider │───▶│   UI    │───▶│  Route  │   │
│  │  实体    │    │ 数据源   │    │ 状态管理 │    │  页面   │    │  路由   │   │
│  └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘   │
│       │              │              │              │              │         │
│       ▼              ▼              ▼              ▼              ▼         │
│    [检查点]       [检查点]       [检查点]       [检查点]       [检查点]      │
└──────────────────────────┬──────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Phase 5: 质量检查                                    │
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   analyze   │  │   format    │  │    test     │  │   l10n      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                                             │
│                    参考: .claude/skills/code-quality                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Phase 0: 需求分析

### 输入类型

| 输入 | 分析要点 |
|------|----------|
| **文字描述** | 提取功能点、业务规则、数据流向 |
| **UI 截图** | 识别组件结构、交互方式、状态变化 |
| **设计稿** | 提取颜色/字体（映射到 Theme）、间距、组件层级 |

### 分析输出

```markdown
## 需求分析结果

### 1. 实体定义
- 实体名称: User
- 字段: id, name, email, avatar
- 关联: UserRole (可选)

### 2. API 接口
- GET /users - 获取用户列表
- GET /users/:id - 获取用户详情
- POST /users - 创建用户

### 3. UI 组件
- UserListPage: 列表页面
- UserListItem: 列表项组件
- UserDetailPage: 详情页面

### 4. 状态流转
- Initial → Loading → Loaded/Error
- 支持下拉刷新、分页加载

### 5. 国际化文本
- userListTitle: 用户列表
- userDetailTitle: 用户详情
- emptyList: 暂无用户
```

### Phase 0 检查清单

| 检查项 | 状态 |
|--------|------|
| ☐ 实体字段已明确 | |
| ☐ API 接口已确认（或 mock 方案） | |
| ☐ UI 组件层级已拆分 | |
| ☐ 状态流转已定义 | |
| ☐ 国际化 key 已规划 | |

---

## 🚫 核心原则：UI 层禁止硬编码

### 禁止项

```dart
// ❌ 禁止：硬编码文本
Text('用户列表')

// ❌ 禁止：硬编码颜色/尺寸
Container(color: Color(0xFF2196F3), padding: EdgeInsets.all(16))

// ❌ 禁止：模拟数据
final users = [User(name: 'Test'), User(name: 'Demo')];

// ❌ 禁止：魔法数字
SizedBox(height: 24)
```

### 正确做法

```dart
// ✅ 国际化文本
Text(context.l10n.userListTitle)

// ✅ 主题颜色/间距
Container(
  color: Theme.of(context).colorScheme.primary,
  padding: const EdgeInsets.all(AppSpacing.md),
)

// ✅ 从 Provider 获取数据
final users = ref.watch(userListProvider);

// ✅ 命名常量
SizedBox(height: AppSpacing.lg)
```

---

## 📁 开发顺序（自底向上）

### Step 1: Domain 层（纯 Dart）

**目的**：定义业务实体和仓库接口

```
lib/features/<name>/domain/
├── entities/
│   └── <name>.dart          # 业务实体
└── repositories/
    └── <name>_repository.dart  # 仓库接口
```

**实体模板**：

```dart
// domain/entities/user.dart
class User {
  const User({
    required this.id,
    required this.name,
    required this.email,
  });

  final String id;
  final String name;
  final String email;

  User copyWith({String? id, String? name, String? email}) {
    return User(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) || other is User && id == other.id;

  @override
  int get hashCode => id.hashCode;
}
```

**仓库接口模板**：

```dart
// domain/repositories/user_repository.dart
import '../entities/user.dart';
import '../../../../core/utils/result.dart';

abstract class UserRepository {
  Future<Result<List<User>>> getUsers();
  Future<Result<User>> getUserById(String id);
  Future<Result<void>> saveUser(User user);
}
```

---

### Step 2: Data 层

**目的**：实现数据源和仓库

```
lib/features/<name>/data/
├── datasources/
│   ├── <name>_remote_data_source.dart  # 网络数据源
│   └── <name>_local_data_source.dart   # 本地数据源
├── models/
│   └── <name>_dto.dart                 # 数据传输对象
└── repositories/
    └── <name>_repository_impl.dart     # 仓库实现
```

**远程数据源模板**：

```dart
// data/datasources/user_remote_data_source.dart
import '../../../../core/network/dio_client.dart';
import '../models/user_dto.dart';

abstract class UserRemoteDataSource {
  Future<List<UserDto>> getUsers();
  Future<UserDto> getUserById(String id);
}

class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  UserRemoteDataSourceImpl({required this.dioClient});

  final DioClient dioClient;

  @override
  Future<List<UserDto>> getUsers() async {
    final response = await dioClient.get('/users');
    return (response.data as List)
        .map((json) => UserDto.fromJson(json))
        .toList();
  }

  @override
  Future<UserDto> getUserById(String id) async {
    final response = await dioClient.get('/users/$id');
    return UserDto.fromJson(response.data);
  }
}
```

**DTO 模板**：

```dart
// data/models/user_dto.dart
import '../../domain/entities/user.dart';

class UserDto {
  UserDto({required this.id, required this.name, required this.email});

  factory UserDto.fromJson(Map<String, dynamic> json) {
    return UserDto(
      id: json['id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
    );
  }

  final String id;
  final String name;
  final String email;

  Map<String, dynamic> toJson() => {'id': id, 'name': name, 'email': email};

  User toEntity() => User(id: id, name: name, email: email);
}
```

**仓库实现模板**：

```dart
// data/repositories/user_repository_impl.dart
import '../../../../core/error/error_mapper.dart';
import '../../../../core/utils/result.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/user_repository.dart';
import '../datasources/user_remote_data_source.dart';

class UserRepositoryImpl implements UserRepository {
  UserRepositoryImpl({required this.remoteDataSource});

  final UserRemoteDataSource remoteDataSource;

  @override
  Future<Result<List<User>>> getUsers() async {
    try {
      final dtos = await remoteDataSource.getUsers();
      return Success(dtos.map((dto) => dto.toEntity()).toList());
    } catch (e) {
      return Err(ErrorMapper.mapException(e));
    }
  }

  @override
  Future<Result<User>> getUserById(String id) async {
    try {
      final dto = await remoteDataSource.getUserById(id);
      return Success(dto.toEntity());
    } catch (e) {
      return Err(ErrorMapper.mapException(e));
    }
  }

  @override
  Future<Result<void>> saveUser(User user) async {
    // 实现保存逻辑
    return const Success(null);
  }
}
```

---

### Step 3: Presentation 层 - Provider

**目的**：状态管理和业务逻辑

```
lib/features/<name>/presentation/
└── providers/
    └── <name>_provider.dart
```

**Provider 模板（异步数据）**：

```dart
// presentation/providers/user_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../app/di.dart';
import '../../data/datasources/user_remote_data_source.dart';
import '../../data/repositories/user_repository_impl.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/user_repository.dart';

// 数据源 Provider
final userRemoteDataSourceProvider = Provider<UserRemoteDataSource>((ref) {
  return UserRemoteDataSourceImpl(dioClient: ref.watch(dioClientProvider));
});

// 仓库 Provider
final userRepositoryProvider = Provider<UserRepository>((ref) {
  return UserRepositoryImpl(
    remoteDataSource: ref.watch(userRemoteDataSourceProvider),
  );
});

// 状态定义
sealed class UserListState {
  const UserListState();
}

class UserListInitial extends UserListState {
  const UserListInitial();
}

class UserListLoading extends UserListState {
  const UserListLoading();
}

class UserListLoaded extends UserListState {
  const UserListLoaded(this.users);
  final List<User> users;
}

class UserListError extends UserListState {
  const UserListError(this.message);
  final String message;
}

// Controller
final userListControllerProvider =
    NotifierProvider<UserListController, UserListState>(
  UserListController.new,
);

class UserListController extends Notifier<UserListState> {
  @override
  UserListState build() {
    // 初始化时加载数据
    Future.microtask(loadUsers);
    return const UserListLoading();
  }

  UserRepository get _repository => ref.read(userRepositoryProvider);

  Future<void> loadUsers() async {
    state = const UserListLoading();
    final result = await _repository.getUsers();
    result.when(
      success: (users) => state = UserListLoaded(users),
      failure: (failure) => state = UserListError(failure.message),
    );
  }

  Future<void> refresh() async {
    await loadUsers();
  }
}
```

---

### Step 4: Presentation 层 - UI

**目的**：纯 UI 展示，无业务逻辑

```
lib/features/<name>/presentation/
├── pages/
│   └── <name>_page.dart      # 页面容器
└── widgets/
    └── <name>_view.dart      # 视图组件
```

**Page 模板**：

```dart
// presentation/pages/user_list_page.dart
import 'package:flutter/material.dart';

import '../../../../core/l10n/l10n.dart';
import '../../../../core/widgets/app_scaffold.dart';
import '../widgets/user_list_view.dart';

class UserListPage extends StatelessWidget {
  const UserListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      appBar: AppBar(title: Text(context.l10n.userListTitle)),
      body: const UserListView(),
    );
  }
}
```

**View 模板（处理状态）**：

```dart
// presentation/widgets/user_list_view.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/l10n/l10n.dart';
import '../../../../core/widgets/error_view.dart';
import '../../../../core/widgets/loading_indicator.dart';
import '../providers/user_provider.dart';
import 'user_list_item.dart';

class UserListView extends ConsumerWidget {
  const UserListView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(userListControllerProvider);

    return switch (state) {
      UserListInitial() => const SizedBox.shrink(),
      UserListLoading() => const LoadingIndicator(),
      UserListError(:final message) => ErrorView(
          message: message,
          onRetry: () => ref.read(userListControllerProvider.notifier).refresh(),
        ),
      UserListLoaded(:final users) => users.isEmpty
          ? Center(child: Text(context.l10n.emptyList))
          : RefreshIndicator(
              onRefresh: () =>
                  ref.read(userListControllerProvider.notifier).refresh(),
              child: ListView.builder(
                itemCount: users.length,
                itemBuilder: (context, index) => UserListItem(user: users[index]),
              ),
            ),
    };
  }
}
```

**Item 模板**：

```dart
// presentation/widgets/user_list_item.dart
import 'package:flutter/material.dart';

import '../../domain/entities/user.dart';

class UserListItem extends StatelessWidget {
  const UserListItem({super.key, required this.user});

  final User user;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return ListTile(
      leading: CircleAvatar(
        backgroundColor: theme.colorScheme.primaryContainer,
        child: Text(
          user.name.isNotEmpty ? user.name[0].toUpperCase() : '?',
          style: TextStyle(color: theme.colorScheme.onPrimaryContainer),
        ),
      ),
      title: Text(user.name, style: theme.textTheme.titleMedium),
      subtitle: Text(user.email, style: theme.textTheme.bodySmall),
    );
  }
}
```

---

### Step 5: 路由配置

```dart
// presentation/routes.dart
import 'package:go_router/go_router.dart';

import 'pages/user_list_page.dart';

class UserRoutes {
  UserRoutes._();

  static const String userList = '/users';
  static const String userDetail = '/users/:id';
}

List<GoRoute> buildUserRoutes() => [
  GoRoute(
    path: UserRoutes.userList,
    builder: (context, state) => const UserListPage(),
  ),
];
```

**注册到 app/router.dart**：

```dart
import '../features/user/presentation/routes.dart';

final routerProvider = Provider<GoRouter>((ref) => GoRouter(
  routes: [
    ...buildUserRoutes(),
    // 其他路由...
  ],
));
```

---

### Step 6: 国际化

**添加到 l10n/app_en.arb**：

```json
{
  "userListTitle": "Users",
  "emptyList": "No data available"
}
```

**添加到 l10n/app_zh.arb**：

```json
{
  "userListTitle": "用户列表",
  "emptyList": "暂无数据"
}
```

**生成**：

```bash
flutter gen-l10n
```

---

## ✅ 各阶段检查清单

### Phase 1: Domain 检查点

| 检查项 | 状态 |
|--------|------|
| ☐ 实体类使用 `const` 构造函数 | |
| ☐ 所有字段使用 `final` | |
| ☐ 实现 `copyWith` 方法 | |
| ☐ 重写 `==` 和 `hashCode` | |
| ☐ 仓库接口返回 `Result<T>` | |
| ☐ 无 Flutter 依赖（纯 Dart） | |

### Phase 2: Data 检查点

| 检查项 | 状态 |
|--------|------|
| ☐ DTO 与 Entity 分离 | |
| ☐ `fromJson` / `toJson` 实现完整 | |
| ☐ `toEntity()` 转换方法 | |
| ☐ 数据源接口 + 实现分离 | |
| ☐ 异常捕获并转换为 `Failure` | |
| ☐ 使用 `ErrorMapper.mapException()` | |

### Phase 3: Provider 检查点

| 检查项 | 状态 |
|--------|------|
| ☐ 状态使用 `sealed class` 定义 | |
| ☐ 包含 Initial/Loading/Loaded/Error 状态 | |
| ☐ Controller 继承 `Notifier` 或 `AsyncNotifier` | |
| ☐ 数据加载在 Controller 中完成 | |
| ☐ Provider 依赖链正确（DataSource → Repository → Controller） | |

### Phase 4: UI 检查点

| 检查项 | 状态 |
|--------|------|
| ☐ 文本使用 `context.l10n.xxx`（无硬编码） | |
| ☐ 颜色使用 `Theme.of(context)`（无硬编码） | |
| ☐ 间距使用命名常量（无魔法数字） | |
| ☐ 数据来自 Provider（无模拟数据） | |
| ☐ Page 与 View/Item 组件分离 | |
| ☐ 使用 `switch` 表达式处理状态 | |
| ☐ Loading/Error/Empty 状态 UI 完整 | |
| ☐ 使用 `const` 构造函数 | |

### Phase 4.5: Route & L10n 检查点

| 检查项 | 状态 |
|--------|------|
| ☐ 路由常量定义在 `routes.dart` | |
| ☐ `buildXxxRoutes()` 函数已导出 | |
| ☐ 路由已注册到 `app/router.dart` | |
| ☐ 国际化 key 已添加到 `app_en.arb` | |
| ☐ 国际化 key 已添加到 `app_zh.arb` | |
| ☐ 已运行 `flutter gen-l10n` | |

---

## 🔍 Phase 5: 质量检查

> 参考: `.claude/skills/code-quality/SKILL.md`

### 执行命令

```bash
# 1. 代码分析（必须通过）
flutter analyze --fatal-infos

# 2. 格式检查（必须通过）
dart format --set-exit-if-changed .

# 3. 运行测试（必须通过）
flutter test test/features/<name>/

# 4. 生成国际化（如有变更）
flutter gen-l10n

# 5. 依赖检查（建议）
flutter pub outdated
```

### Phase 5 检查清单

#### 5.1 静态分析

| 检查项 | 命令 | 状态 |
|--------|------|------|
| ☐ 无 analyze 错误 | `flutter analyze` | |
| ☐ 无 analyze 警告 | `flutter analyze --fatal-infos` | |
| ☐ 代码格式正确 | `dart format --set-exit-if-changed .` | |

#### 5.2 测试覆盖

| 检查项 | 状态 |
|--------|------|
| ☐ Domain 层单元测试 | |
| ☐ Provider/Controller 测试 | |
| ☐ 测试全部通过 | |

#### 5.3 安全检查

| 检查项 | 状态 |
|--------|------|
| ☐ 无硬编码 API 密钥/Token | |
| ☐ 无硬编码密码/Secret | |
| ☐ 敏感数据使用 `SecureStorage` | |
| ☐ 网络请求使用 HTTPS | |
| ☐ 无敏感信息在日志中输出 | |

#### 5.4 性能检查

| 检查项 | 标准 | 状态 |
|--------|------|------|
| ☐ 单文件行数 | < 500 行 | |
| ☐ Widget 嵌套层级 | < 10 层 | |
| ☐ 列表使用 `ListView.builder` | - | |
| ☐ 使用 `const` 构造函数 | - | |
| ☐ 避免在 `build` 中创建大对象 | - | |

#### 5.5 代码规范

| 检查项 | 状态 |
|--------|------|
| ☐ 文件命名 `snake_case` | |
| ☐ 类命名 `PascalCase` | |
| ☐ 私有成员 `_` 前缀 | |
| ☐ 导入语句已排序 | |
| ☐ 无未使用的导入/变量 | |

### 质量检查自动化（推荐）

使用子代理执行完整质量检查：

```typescript
Task({
  subagent_type: 'general-purpose',
  description: '运行 Feature 质量检查',
  prompt: `
对 lib/features/<name>/ 执行完整质量检查：

1. flutter analyze lib/features/<name>/
2. dart format --set-exit-if-changed lib/features/<name>/
3. flutter test test/features/<name>/

如有错误，分析并修复，再次验证直到全部通过。
返回检查结果摘要。

遵循 .claude/skills/code-quality/SKILL.md 中的规范。
  `,
})
```

---

## 📋 完整检查清单汇总

| 阶段 | 核心检查项 |
|------|-----------|
| Phase 0 | 需求分析完整（实体/API/UI/状态/L10n） |
| Phase 1 | Domain 纯 Dart，immutable 实体 |
| Phase 2 | Data DTO 分离，异常转 Failure |
| Phase 3 | Provider sealed class 状态 |
| Phase 4 | UI 无硬编码，数据来自 Provider |
| Phase 4.5 | 路由注册，国际化完成 |
| Phase 5 | analyze + format + test 全通过 |

---

## 🔧 常用命令速查

```bash
# 开发流程
flutter pub get                              # 获取依赖
flutter gen-l10n                             # 生成国际化

# 质量检查
flutter analyze                              # 代码分析
flutter analyze lib/features/<name>/         # 分析指定 feature
dart format .                                # 格式化
dart format lib/features/<name>/             # 格式化指定 feature

# 测试
flutter test                                 # 全部测试
flutter test test/features/<name>/           # Feature 测试
flutter test --coverage                      # 覆盖率报告

# 依赖
flutter pub outdated                         # 检查过期依赖
flutter pub upgrade                          # 升级依赖
```
