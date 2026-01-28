---
name: sa-token
description: Sa-Token 权限认证框架开发规范。当进行登录认证、权限校验、角色管理、JWT Token 处理时自动使用。
---

# Sa-Token 开发规范

本项目使用 Sa-Token 1.38+ 作为权限认证框架，基于 Spring Boot 4 集成。

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Sa-Token | 1.38+ | 权限认证框架 |
| Spring Boot | 4.0.1 | 后端框架 |
| Redis | - | Token 持久化（可选） |

## Maven 依赖

```xml
<!-- Sa-Token Spring Boot 3.x Starter -->
<dependency>
    <groupId>cn.dev33</groupId>
    <artifactId>sa-token-spring-boot3-starter</artifactId>
    <version>1.38.0</version>
</dependency>

<!-- Sa-Token 整合 JWT (可选) -->
<dependency>
    <groupId>cn.dev33</groupId>
    <artifactId>sa-token-jwt</artifactId>
    <version>1.38.0</version>
</dependency>
```

## 配置文件

```yaml
# application.yml
sa-token:
  # Token 名称 (同时也是 Cookie 名称)
  token-name: Authorization
  # Token 有效期 (单位：秒)，默认30天，-1 代表永久有效
  timeout: 2592000
  # Token 临时有效期 (指定时间内无操作就视为 Token 过期)
  active-timeout: -1
  # 是否允许同一账号多地同时登录
  is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 Token
  is-share: false
  # Token 风格 (uuid/simple-uuid/random-32/random-64/random-128/tik)
  token-style: uuid
  # 是否输出操作日志
  is-log: true
  # 是否从 Cookie 中读取 Token
  is-read-cookie: false
  # 是否从 Header 中读取 Token
  is-read-header: true
  # Token 前缀
  token-prefix: Bearer
```

## 核心代码模板

### 1. StpInterface 实现 (权限数据源)

```java
package com.example.security;

import cn.dev33.satoken.stp.StpInterface;
import org.springframework.stereotype.Component;
import java.util.List;

/**
 * Sa-Token 权限认证接口实现
 * 用于获取用户的权限列表和角色列表
 */
@Component
public class StpInterfaceImpl implements StpInterface {

    private final SysUserService userService;
    private final SysRoleService roleService;
    private final SysMenuService menuService;

    public StpInterfaceImpl(SysUserService userService,
                           SysRoleService roleService,
                           SysMenuService menuService) {
        this.userService = userService;
        this.roleService = roleService;
        this.menuService = menuService;
    }

    /**
     * 返回指定账号拥有的权限码集合
     * @param loginId 登录用户ID
     * @param loginType 登录类型
     * @return 权限码列表
     */
    @Override
    public List<String> getPermissionList(Object loginId, String loginType) {
        Long userId = Long.parseLong(loginId.toString());
        // 从数据库查询用户权限
        return menuService.selectPermsByUserId(userId);
    }

    /**
     * 返回指定账号拥有的角色标识集合
     * @param loginId 登录用户ID
     * @param loginType 登录类型
     * @return 角色标识列表
     */
    @Override
    public List<String> getRoleList(Object loginId, String loginType) {
        Long userId = Long.parseLong(loginId.toString());
        // 从数据库查询用户角色
        return roleService.selectRoleCodesByUserId(userId);
    }
}
```

### 2. 登录认证服务

```java
package com.example.service;

import cn.dev33.satoken.stp.StpUtil;
import cn.dev33.satoken.stp.SaTokenInfo;
import org.springframework.stereotype.Service;

/**
 * 认证服务
 */
@Service
public class AuthService {

    private final SysUserService userService;
    private final PasswordEncoder passwordEncoder;

    public AuthService(SysUserService userService, PasswordEncoder passwordEncoder) {
        this.userService = userService;
        this.passwordEncoder = passwordEncoder;
    }

    /**
     * 用户登录
     * @param username 用户名
     * @param password 密码
     * @return Token 信息
     */
    public SaTokenInfo login(String username, String password) {
        // 1. 查询用户
        SysUser user = userService.findByUsername(username);
        if (user == null) {
            throw new RuntimeException("用户不存在");
        }

        // 2. 验证密码
        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new RuntimeException("密码错误");
        }

        // 3. 检查状态
        if (user.getStatus() != 1) {
            throw new RuntimeException("账号已被禁用");
        }

        // 4. 执行登录
        StpUtil.login(user.getId());

        // 5. 返回 Token 信息
        return StpUtil.getTokenInfo();
    }

    /**
     * 用户登出
     */
    public void logout() {
        StpUtil.logout();
    }

    /**
     * 获取当前登录用户ID
     * @return 用户ID
     */
    public Long getCurrentUserId() {
        return StpUtil.getLoginIdAsLong();
    }

    /**
     * 获取当前登录用户信息
     * @return 用户信息
     */
    public SysUser getCurrentUser() {
        Long userId = getCurrentUserId();
        return userService.findById(userId);
    }
}
```

### 3. 权限注解使用

```java
package com.example.controller;

import cn.dev33.satoken.annotation.SaCheckLogin;
import cn.dev33.satoken.annotation.SaCheckPermission;
import cn.dev33.satoken.annotation.SaCheckRole;
import cn.dev33.satoken.annotation.SaIgnore;
import cn.dev33.satoken.annotation.SaMode;
import org.springframework.web.bind.annotation.*;

/**
 * 用户管理控制器
 */
@RestController
@RequestMapping("/api/sys/user")
@SaCheckLogin  // 整个控制器需要登录
public class SysUserController {

    /**
     * 获取用户列表 - 需要 sys:user:list 权限
     */
    @GetMapping
    @SaCheckPermission("sys:user:list")
    public Result<Page<SysUser>> list(SysUserQuery query) {
        return Result.success(userService.page(query));
    }

    /**
     * 新增用户 - 需要 sys:user:add 权限
     */
    @PostMapping
    @SaCheckPermission("sys:user:add")
    public Result<Void> add(@RequestBody SysUser user) {
        userService.save(user);
        return Result.success();
    }

    /**
     * 更新用户 - 需要 sys:user:edit 权限
     */
    @PutMapping("/{id}")
    @SaCheckPermission("sys:user:edit")
    public Result<Void> update(@PathVariable Long id, @RequestBody SysUser user) {
        user.setId(id);
        userService.update(user);
        return Result.success();
    }

    /**
     * 删除用户 - 需要 sys:user:delete 权限或 admin 角色
     */
    @DeleteMapping("/{id}")
    @SaCheckPermission(value = "sys:user:delete", orRole = "admin")
    public Result<Void> delete(@PathVariable Long id) {
        userService.delete(id);
        return Result.success();
    }

    /**
     * 批量操作 - 需要同时具备多个权限
     */
    @PostMapping("/batch")
    @SaCheckPermission(value = {"sys:user:add", "sys:user:edit"}, mode = SaMode.AND)
    public Result<Void> batch(@RequestBody BatchRequest request) {
        userService.batch(request);
        return Result.success();
    }

    /**
     * 角色校验 - 需要 admin 角色
     */
    @GetMapping("/admin-only")
    @SaCheckRole("admin")
    public Result<String> adminOnly() {
        return Result.success("Admin access granted");
    }

    /**
     * 忽略认证 - 公开接口
     */
    @SaIgnore
    @GetMapping("/public")
    public Result<String> publicApi() {
        return Result.success("Public API");
    }
}
```

### 4. 全局异常处理

```java
package com.example.config;

import cn.dev33.satoken.exception.NotLoginException;
import cn.dev33.satoken.exception.NotPermissionException;
import cn.dev33.satoken.exception.NotRoleException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * Sa-Token 异常处理
 */
@RestControllerAdvice
public class SaTokenExceptionHandler {

    /**
     * 未登录异常
     */
    @ExceptionHandler(NotLoginException.class)
    public Result<Void> handleNotLogin(NotLoginException e) {
        String message = switch (e.getType()) {
            case NotLoginException.NOT_TOKEN -> "未提供Token";
            case NotLoginException.INVALID_TOKEN -> "Token无效";
            case NotLoginException.TOKEN_TIMEOUT -> "Token已过期";
            case NotLoginException.BE_REPLACED -> "账号已在其他地方登录";
            case NotLoginException.KICK_OUT -> "账号已被踢下线";
            default -> "未登录";
        };
        return Result.fail(401, message);
    }

    /**
     * 无权限异常
     */
    @ExceptionHandler(NotPermissionException.class)
    public Result<Void> handleNotPermission(NotPermissionException e) {
        return Result.fail(403, "无权限: " + e.getPermission());
    }

    /**
     * 无角色异常
     */
    @ExceptionHandler(NotRoleException.class)
    public Result<Void> handleNotRole(NotRoleException e) {
        return Result.fail(403, "无角色: " + e.getRole());
    }
}
```

### 5. Sa-Token 配置类

```java
package com.example.config;

import cn.dev33.satoken.interceptor.SaInterceptor;
import cn.dev33.satoken.router.SaRouter;
import cn.dev33.satoken.stp.StpUtil;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Sa-Token 配置
 */
@Configuration
public class SaTokenConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 注册 Sa-Token 拦截器
        registry.addInterceptor(new SaInterceptor(handle -> {
            // 指定拦截路由
            SaRouter.match("/**")
                // 排除登录、注册等公开接口
                .notMatch("/api/auth/login", "/api/auth/register")
                // 排除静态资源
                .notMatch("/static/**", "/favicon.ico")
                // 校验登录
                .check(r -> StpUtil.checkLogin());
        })).addPathPatterns("/**");
    }
}
```

## 权限标识规范

```
{模块}:{实体}:{操作}

示例：
sys:user:list      - 用户列表
sys:user:add       - 新增用户
sys:user:edit      - 编辑用户
sys:user:delete    - 删除用户
sys:role:list      - 角色列表
sys:menu:list      - 菜单列表
```

## 常用 API

| API | 说明 |
|-----|------|
| `StpUtil.login(id)` | 登录 |
| `StpUtil.logout()` | 登出 |
| `StpUtil.isLogin()` | 是否已登录 |
| `StpUtil.checkLogin()` | 校验登录（未登录抛异常） |
| `StpUtil.getLoginId()` | 获取登录ID |
| `StpUtil.getLoginIdAsLong()` | 获取登录ID (Long) |
| `StpUtil.getTokenInfo()` | 获取Token信息 |
| `StpUtil.hasPermission(perm)` | 是否有权限 |
| `StpUtil.checkPermission(perm)` | 校验权限 |
| `StpUtil.hasRole(role)` | 是否有角色 |
| `StpUtil.checkRole(role)` | 校验角色 |
| `StpUtil.kickout(id)` | 踢人下线 |

## 最佳实践

1. **Token 存储**: 生产环境建议使用 Redis 存储 Token
2. **权限缓存**: 可在 StpInterface 中实现权限缓存提升性能
3. **注解优先**: 优先使用注解方式进行权限校验
4. **统一异常**: 配置全局异常处理器处理认证异常
5. **接口分层**: 公开接口使用 @SaIgnore，敏感接口使用权限注解

---
> Context7 Library: /dromara/sa-token
> 创建时间: 2026-01-13
