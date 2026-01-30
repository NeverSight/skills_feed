---
name: springboot-init
description: Define development specifications for Spring Boot monolithic projects, supporting multiple technology stack configurations.
---
# springboot-init

## 0. 技术栈配置

使用本规范前，请确认项目的技术选型：

### 0.1 核心框架版本

| 配置项 | 可选值                   | 说明 |
|--------|-----------------------|------|
| **Spring Boot** | 2.x / 3.x / 4.x       | 2.x 支持 Java 8+，3.x/4.x 需要 Java 17+ |
| **JDK** | 8 / 11 / 17 / 21 / 25 | 根据 Spring Boot 版本选择 |

**版本兼容矩阵**：

| Spring Boot | 最低 JDK | 推荐 JDK | Jakarta EE |
|-------------|----------|----------|------------|
| 2.x | 8 | 11 | javax.* |
| 3.x | 17 | 17 | jakarta.* |
| 4.x | 17 | 21 | jakarta.* |

### 0.2 ORM 框架

| 框架 | 特点 | 适用场景 |
|------|------|----------|
| **MyBatis-Plus** | 增强 MyBatis，简化 CRUD | 传统项目、快速开发 |
| **MyBatis-Flex** | 轻量级、高性能、链式查询 | 追求性能、灵活查询 |
| **Jimmer** | 不可变对象、强类型 DSL | 复杂领域模型、DDD 项目 |

### 0.3 工具库

| 库 | 说明 | 建议 |
|----|------|------|
| **Hutool** | 全能工具库（日期、加密、HTTP、JSON 等） | 推荐，减少重复代码 |
| **Apache Commons** | 经典工具库集合 | 轻量需求可选 |
| **Guava** | Google 工具库 | 集合处理、缓存需求 |

### 0.4 访问控制框架

| 框架 | 特点 | 适用场景                            |
|------|------|---------------------------------|
| **Sa-Token** | 轻量级、开箱即用、功能全面 | 快速开发、中小项目                       |
| **Spring Security** | Spring 官方、功能强大、高度可定制 | 企业级项目、复杂权限                      |
| **Shiro** | Apache 项目、简单易用 | 传统项目、简单权限、脱离Spring Boot         |
| **Casbin** | 强大、灵活、可扩展 | 复杂动态权限控制，对性能不敏感                 |
| **Keycloak** | 独立的身份认证服务 | 实现 SSO (单点登录) 和 IAM (身份识别与访问管理) |
| **自定义 AOP** | 注解 + 拦截器 | 轻量需求、完全可控                       |

---

## 1. 项目结构

### 1.1 包命名

```
com.{company}.{project}
├── controller      # REST API 端点
├── service         # 业务逻辑接口
│   └── impl        # 业务逻辑实现
├── mapper          # 数据访问层 (MyBatis-Plus/Flex)
├── repository      # 数据访问层 (Jimmer)
├── model
│   ├── entity      # 数据库实体
│   ├── dto         # 请求数据传输对象
│   ├── vo          # 响应值对象
│   └── enums       # 枚举类
├── api             # 外部 API 集成门面
├── manager         # 业务协调层
├── config          # Spring 配置类
├── annotation      # 自定义注解
├── aop             # AOP 拦截器
├── exception       # 异常类
├── utils           # 工具类
├── constant        # 常量定义
└── common          # 通用基类
```

### 1.2 分层职责

| 层级 | 职责 | 禁止事项 |
|------|------|----------|
| Controller | 接收请求、参数校验、权限控制、调用 Service、返回统一响应 | 禁止包含业务逻辑 |
| Service | 业务逻辑处理、事务管理 | 禁止直接操作 HttpServletRequest |
| Mapper/Repository | 数据库操作 | 禁止包含业务逻辑 |
| Manager | 复杂业务协调、外部 API 调用封装 | 仅用于跨服务协调 |

---

## 2. 编码规范

### 2.1 Controller 层

```java
@Tag(name = "XxxController", description = "模块描述")
@RestController
@RequestMapping("/xxx")
public class XxxController {

    @Resource  // 或 @Autowired（根据团队规范）
    private XxxService xxxService;

    @PostMapping("/action")
    @Operation(summary = "操作摘要", description = "操作描述")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "0", description = "ok"),
        @ApiResponse(responseCode = "40000", description = "参数错误"),
    })
    public BaseResponse<XxxVO> doAction(
            @RequestBody XxxRequest request,
            HttpServletRequest httpServletRequest) {
        ThrowUtils.throwIf(request == null, ErrorCode.PARAMS_ERROR);
        // 调用 Service
        return ResultUtils.success(result);
    }
}
```

**强制规范**：
- 所有 Controller 必须使用 `@Tag` 注解（OpenAPI 3.0）
- 所有方法必须使用 `@Operation` + `@ApiResponses` 注解
- 返回类型必须为 `BaseResponse<T>`
- 多参数必须封装为 Request 对象（禁止多个 `@RequestParam`）

### 2.2 Service 层

#### MyBatis-Plus 风格

```java
public interface XxxService extends IService<Xxx> {
    XxxVO doSomething(XxxRequest request);
}

@Slf4j
@Service
public class XxxServiceImpl extends ServiceImpl<XxxMapper, Xxx>
        implements XxxService {

    @Override
    @Transactional(rollbackFor = Exception.class)
    public XxxVO doSomething(XxxRequest request) {
        // 业务逻辑
    }
}
```

#### MyBatis-Flex 风格

```java
public interface XxxService extends IService<Xxx> {
    XxxVO doSomething(XxxRequest request);
}

@Slf4j
@Service
public class XxxServiceImpl extends ServiceImpl<XxxMapper, Xxx>
        implements XxxService {

    @Override
    public XxxVO doSomething(XxxRequest request) {
        // 使用 QueryWrapper 链式查询
        QueryWrapper query = QueryWrapper.create()
            .where(XXX.ID.eq(request.getId()));
        return mapper.selectOneByQuery(query);
    }
}
```

#### Jimmer 风格

```java
public interface XxxService {
    XxxVO doSomething(XxxRequest request);
}

@Slf4j
@Service
@RequiredArgsConstructor
public class XxxServiceImpl implements XxxService {

    private final JSqlClient sqlClient;

    @Override
    public XxxVO doSomething(XxxRequest request) {
        // 使用 Jimmer DSL
        return sqlClient.createQuery(XxxTable.$)
            .where(XxxTable.$.id().eq(request.getId()))
            .select(XxxTable.$)
            .fetchOne();
    }
}
```

**强制规范**：
- 使用 `@Slf4j` 注解
- 涉及多表操作必须使用 `@Transactional`

### 2.3 Mapper/Repository 层

#### MyBatis-Plus

```java
@Mapper
public interface XxxMapper extends BaseMapper<Xxx> {
    // 复杂查询使用 @Select 或 XML
}
```

#### MyBatis-Flex

```java
@Mapper
public interface XxxMapper extends BaseMapper<Xxx> {
    // 支持链式查询，无需 XML
}
```

#### Jimmer

```java
public interface XxxRepository extends JRepository<Xxx, Long> {
    // Jimmer 自动生成实现
}
```

### 2.4 Model 层

**Entity**：

```java
// MyBatis-Plus / MyBatis-Flex
@Data
@TableName("table_name")
public class Xxx implements Serializable {
    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.ASSIGN_ID)
    private Long id;

    @TableLogic
    private Integer isDelete;
}

// Jimmer（不可变对象）
@Entity
public interface Xxx {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    long id();

    String name();

    @LogicalDeleted("1")
    int isDelete();
}
```

**Request DTO**：
```java
@Data
public class XxxRequest implements Serializable {
    private static final long serialVersionUID = 1L;
    // 请求字段
}
```

**VO**：
```java
@Data
public class XxxVO implements Serializable {
    private static final long serialVersionUID = 1L;
    // 响应字段
}
```

**强制规范**：
- 所有 Request/VO 必须实现 `Serializable`
- 必须声明 `serialVersionUID`
- 使用 `@Data` 注解（Jimmer Entity 除外）

---

## 3. 统一响应规范

### 3.1 BaseResponse 结构

```java
public class BaseResponse<T> implements Serializable {
    private int code;       // 状态码
    private T data;         // 响应数据
    private String message; // 响应消息
}
```

### 3.2 ResultUtils 使用

```java
// 成功响应
return ResultUtils.success(data);

// 失败响应
return ResultUtils.error(ErrorCode.PARAMS_ERROR);
return ResultUtils.error(ErrorCode.PARAMS_ERROR, "自定义消息");
```

### 3.3 ErrorCode 枚举

| 错误码 | 常量 | 说明 |
|--------|------|------|
| 0 | SUCCESS | 成功 |
| 40000 | PARAMS_ERROR | 请求参数错误 |
| 40100 | NOT_LOGIN_ERROR | 未登录 |
| 40101 | NO_AUTH_ERROR | 无权限 |
| 40300 | FORBIDDEN_ERROR | 禁止访问 |
| 40400 | NOT_FOUND_ERROR | 数据不存在 |
| 50000 | SYSTEM_ERROR | 系统内部异常 |
| 50001 | OPERATION_ERROR | 操作失败 |

---

## 4. 异常处理规范

### 4.1 ThrowUtils 使用

```java
// 条件抛出
ThrowUtils.throwIf(condition, ErrorCode.PARAMS_ERROR);
ThrowUtils.throwIf(condition, ErrorCode.PARAMS_ERROR, "自定义消息");

// 示例
ThrowUtils.throwIf(request == null, ErrorCode.PARAMS_ERROR);
ThrowUtils.throwIf(user == null, ErrorCode.NOT_FOUND_ERROR, "用户不存在");
```

### 4.2 BusinessException 使用

```java
// 直接抛出
throw new BusinessException(ErrorCode.NO_AUTH_ERROR);
throw new BusinessException(ErrorCode.OPERATION_ERROR, "操作失败原因");
```

---

## 5. 访问控制规范

### 5.1 Sa-Token 方案

```java
// 配置类
@Configuration
public class SaTokenConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new SaInterceptor(handle -> {
            SaRouter.match("/**").check(r -> StpUtil.checkLogin());
            SaRouter.match("/admin/**").check(r -> StpUtil.checkRole("admin"));
        })).addPathPatterns("/**").excludePathPatterns("/user/login");
    }
}

// Controller 使用
@SaCheckLogin
@SaCheckRole("admin")
@PostMapping("/admin/action")
public BaseResponse<Boolean> adminAction(...) { }
```

### 5.2 Spring Security 方案

```java
// 配置类
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(auth -> auth
            .requestMatchers("/user/login").permitAll()
            .requestMatchers("/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated()
        );
        return http.build();
    }
}

// Controller 使用
@PreAuthorize("hasRole('ADMIN')")
@PostMapping("/admin/action")
public BaseResponse<Boolean> adminAction(...) { }
```

### 5.3 Shiro 方案

```java
// 配置类
@Configuration
public class ShiroConfig {
    @Bean
    public ShiroFilterFactoryBean shiroFilter(SecurityManager manager) {
        ShiroFilterFactoryBean bean = new ShiroFilterFactoryBean();
        bean.setSecurityManager(manager);
        Map<String, String> map = new LinkedHashMap<>();
        map.put("/user/login", "anon");
        map.put("/admin/**", "roles[admin]");
        map.put("/**", "authc");
        bean.setFilterChainDefinitionMap(map);
        return bean;
    }
}

// Controller 使用
@RequiresRoles("admin")
@PostMapping("/admin/action")
public BaseResponse<Boolean> adminAction(...) { }
```

### 5.4 自定义 AOP 方案

```java
// 注解定义
@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface AuthCheck {
    String mustRole() default "";
}

// AOP 拦截器
@Aspect
@Component
public class AuthInterceptor {
    @Around("@annotation(authCheck)")
    public Object doAuth(ProceedingJoinPoint joinPoint, AuthCheck authCheck) throws Throwable {
        String mustRole = authCheck.mustRole();
        // 权限校验逻辑
        return joinPoint.proceed();
    }
}

// Controller 使用
@AuthCheck(mustRole = UserConstant.ADMIN_ROLE)
@PostMapping("/admin/action")
public BaseResponse<Boolean> adminAction(...) { }
```

### 5.5 角色常量

```java
public interface UserConstant {
    String DEFAULT_ROLE = "user";   // 普通用户
    String ADMIN_ROLE = "admin";    // 管理员
    String VIP_ROLE = "vip";        // VIP 用户
}
```

---

## 6. 工具库使用规范

### 6.1 Hutool 使用

```java
// 字符串处理
StrUtil.isBlank(str);
StrUtil.format("Hello, {}", name);

// 日期处理
DateUtil.format(date, "yyyy-MM-dd");
DateUtil.parse("2024-01-01");

// 对象拷贝
BeanUtil.copyProperties(source, target);

// JSON 处理
JSONUtil.toJsonStr(object);
JSONUtil.toBean(jsonStr, Xxx.class);

// 加密
SecureUtil.md5(password);
SecureUtil.sha256(password);

// 随机数
RandomUtil.randomNumbers(6);  // 6位数字验证码
RandomUtil.randomString(32);  // 32位随机字符串
```

### 6.2 原生 Java 替代（不使用 Hutool）

```java
// 字符串处理
str == null || str.isBlank();
String.format("Hello, %s", name);

// 日期处理
LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd"));

// 对象拷贝
BeanUtils.copyProperties(source, target);  // Spring

// JSON 处理
objectMapper.writeValueAsString(object);   // Jackson
objectMapper.readValue(jsonStr, Xxx.class);

// 加密
MessageDigest.getInstance("MD5").digest(password.getBytes());

// 随机数
new Random().nextInt(1000000);
UUID.randomUUID().toString().replace("-", "");
```

---

## 7. 命名规范

### 7.1 类命名

| 类型 | 命名模式 | 示例 |
|------|----------|------|
| Controller | XxxController | UserController, PictureController |
| Service 接口 | XxxService | UserService, PictureService |
| Service 实现 | XxxServiceImpl | UserServiceImpl, PictureServiceImpl |
| Mapper | XxxMapper | UserMapper, PictureMapper |
| Repository | XxxRepository | UserRepository (Jimmer) |
| Entity | Xxx | User, Picture |
| VO | XxxVO | UserVO, PictureVO |

### 7.2 DTO 命名

| 操作类型 | 命名模式 | 示例 |
|----------|----------|------|
| 通用请求 | XxxRequest | UserRequest |
| 创建/添加 | XxxAddRequest / XxxCreateRequest | PictureAddRequest |
| 更新 | XxxUpdateRequest | UserUpdateRequest |
| 编辑 | XxxEditRequest | PictureEditRequest |
| 查询 | XxxQueryRequest | PictureQueryRequest |
| 登录 | XxxLoginRequest | UserLoginRequest |
| 注册 | XxxRegisterRequest | UserRegisterRequest |

### 7.3 方法命名

| 操作 | 命名模式 | 示例 |
|------|----------|------|
| 查询单个 | getXxx / getXxxById | getUser, getPictureById |
| 查询列表 | listXxx | listPictures |
| 分页查询 | listXxxByPage | listPictureByPage |
| 添加 | addXxx / createXxx | addPicture |
| 更新 | updateXxx | updateUser |
| 删除 | deleteXxx | deletePicture |

---

## 8. 依赖注入规范

### 8.1 推荐方式

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| `@Resource` | JSR-250 标准，按名称注入 | 推荐，明确性强 |
| `@Autowired` | Spring 原生，按类型注入 | Spring 项目通用 |
| 构造器注入 | 不可变、利于测试 | Lombok `@RequiredArgsConstructor` |

```java
// @Resource（推荐）
@Resource
private UserService userService;

// @Autowired
@Autowired
private UserService userService;

// 构造器注入（Lombok）
@RequiredArgsConstructor
@Service
public class XxxServiceImpl {
    private final UserService userService;
}
```

---

## 9. 日志规范

### 9.1 使用方式

```java
@Slf4j
@Service
public class XxxServiceImpl {
    public void doSomething() {
        log.info("操作描述, param={}", param);
        log.error("错误描述", exception);
    }
}
```

### 9.2 日志级别

| 级别 | 场景 |
|------|------|
| ERROR | 系统异常、业务关键错误 |
| WARN | 潜在问题、降级处理 |
| INFO | 重要业务操作、状态变更 |
| DEBUG | 开发调试信息 |

---

## 10. 分页规范

### 10.1 分页请求

```java
@Data
@EqualsAndHashCode(callSuper = true)
public class XxxQueryRequest extends PageRequest {
    // 查询字段
}

// PageRequest 基类
@Data
public class PageRequest implements Serializable {
    private int current = 1;
    private int pageSize = 10;
    private String sortField;
    private String sortOrder = "descend"; // ascend / descend
}
```

### 10.2 分页返回

```java
Page<XxxVO> page = xxxService.listByPage(request);
return ResultUtils.success(page);
```

---

## 11. Spring Boot 版本差异

### 11.1 包导入差异

| 功能 | Spring Boot 2.x | Spring Boot 3.x+ |
|------|-----------------|------------------|
| Servlet | `javax.servlet.*` | `jakarta.servlet.*` |
| Validation | `javax.validation.*` | `jakarta.validation.*` |
| Persistence | `javax.persistence.*` | `jakarta.persistence.*` |

### 11.2 配置差异

```yaml
# Spring Boot 2.x
spring:
  redis:
    host: localhost
    port: 6379

# Spring Boot 3.x+
spring:
  data:
    redis:
      host: localhost
      port: 6379
```

---

## 12. 禁止事项

1. **禁止** 在 Controller 中编写业务逻辑
2. **禁止** 使用多个 `@RequestParam` 接收参数（封装为 Request 对象）
3. **禁止** 返回非 `BaseResponse<T>` 类型
4. **禁止** Request/VO 不实现 `Serializable`
5. **禁止** 在 Service 中直接操作 `HttpServletRequest`
6. **禁止** 硬编码角色字符串（使用常量）
7. **禁止** 混用不同 ORM 框架的写法
8. **禁止** 在生产环境使用 DEBUG 级别日志

---

## 附录：当前项目配置

> 本项目（yun-picture-backend）使用的技术栈：

| 配置项 | 选择 |
|--------|------|
| Spring Boot | 3.5.7 |
| JDK | 17 |
| ORM | MyBatis-Plus 3.5.14 |
| 工具库 | Hutool 5.8.40 |
| 访问控制 | 自定义 AOP（@AuthCheck） |
| 依赖注入 | @Resource |
| API 文档 | SpringDoc OpenAPI 3.0 |

---

## 13. 代码模板

完整可复制的代码模板见 [references/code-templates.md](references/code-templates.md)，包含：

| 包 | 类 |
|---|---|
| common | `BaseResponse`, `PageRequest`, `DeleteRequest` |
| controller | `MainController` |
| exception | `ErrorCode`, `BusinessException`, `GlobalExceptionHandler` |
| utils | `ResultUtils`, `ThrowUtils` |
| config | `MybatisPlusConfig`, `JsonConfig`, `OpenApiConfig` |
